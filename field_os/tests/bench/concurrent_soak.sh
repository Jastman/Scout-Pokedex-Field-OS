#!/usr/bin/env bash
# SCOUT MK-1 bench: spec §10.1 sustained concurrent-load thermal soak, executable.
# Runs all four inference engines AT ONCE (the abuse case, worse than any real UI
# state) for DURATION seconds, logging SoC temp, PMIC temp, throttle flags, and the
# battery-bay NTC to CSV. Run once on the open bench, once in the closed shell,
# once in direct sun (spec §10.1).
#
# PASS: SoC sustained < 80 C, get_throttled == 0x0 throughout, bay NTC < 45 C.
# FAIL: anything else -> the shell goes back to CAD (more vent area / spreader plate).
#
# Prereqs (paths below assume the W2/W3 install layout in ~/scout):
#   whisper.cpp built at ~/scout/whisper.cpp   (+ a 10s test WAV)
#   llama.cpp   built at ~/scout/llama.cpp     (+ Qwen3-1.7B Q4 GGUF on the NVMe)
#   vision + BirdNET loop scripts (tests/bench/loops/) using the W2 models
#   bay NTC readable via tests/bench/read_bay_ntc.sh (prints C, or "NA" pre-install)
set -u
DURATION="${DURATION:-1800}"            # 30 min default
OUT="${OUT:-soak_$(date +%Y%m%d_%H%M%S).csv}"
WHISPER="${WHISPER:-$HOME/scout/whisper.cpp}"
LLAMA="${LLAMA:-$HOME/scout/llama.cpp}"
MODEL="${MODEL:-$HOME/scout/models/qwen3-1.7b-q4_k_m.gguf}"
WAV="${WAV:-$HOME/scout/testdata/kid_question_4s.wav}"
BIRD_WAV="${BIRD_WAV:-$HOME/scout/testdata/robin_6s.wav}"
STILL="${STILL:-$HOME/scout/testdata/leaf_1024.jpg}"

echo "soak: $DURATION s, logging to $OUT"
echo "t_s,soc_c,pmic_c,throttled,bay_c" > "$OUT"

pids=()
loop() { while true; do "$@" >/dev/null 2>&1; done }

# 1. whisper.cpp loop (3 threads)
loop "$WHISPER/build/bin/whisper-cli" -t 3 -m "$WHISPER/models/ggml-base.en.bin" -f "$WAV" & pids+=($!)
# 2. llama.cpp continuous generation (3 threads)
loop "$LLAMA/build/bin/llama-cli" -t 3 -m "$MODEL" -n 256 --no-display-prompt \
     -p "Describe an American Robin for a five year old." & pids+=($!)
# 3. vision model loop (TFLite int8 classify on a still, 3 threads)
loop python3 "$(dirname "$0")/loops/vision_once.py" "$STILL" & pids+=($!)
# 4. BirdNET loop on a canned clip
loop python3 "$(dirname "$0")/loops/birdnet_once.py" "$BIRD_WAV" & pids+=($!)

cleanup() { for p in "${pids[@]}"; do pkill -P "$p" 2>/dev/null; kill "$p" 2>/dev/null; done; }
trap cleanup EXIT

fail=0
start=$(date +%s)
while (( $(date +%s) - start < DURATION )); do
  t=$(( $(date +%s) - start ))
  soc=$(vcgencmd measure_temp | grep -oE '[0-9.]+')
  # PMIC die temp: EXT_THERM or the ADC labelled temp on Pi 5 firmware
  pmic=$(vcgencmd pmic_read_adc 2>/dev/null | grep -i temp | grep -oE '[0-9.]+' | head -1)
  thr=$(vcgencmd get_throttled | cut -d= -f2)
  bay=$("$(dirname "$0")/read_bay_ntc.sh" 2>/dev/null || echo NA)
  echo "$t,$soc,${pmic:-NA},$thr,$bay" >> "$OUT"
  awk -v s="$soc" 'BEGIN{exit !(s>=80)}' && { echo "HOT: SoC ${soc}C at t=${t}s"; fail=1; }
  [ "$thr" != "0x0" ] && { echo "THROTTLED: $thr at t=${t}s"; fail=1; }
  [ "$bay" != "NA" ] && awk -v b="$bay" 'BEGIN{exit !(b>=45)}' && { echo "BAY HOT: ${bay}C at t=${t}s"; fail=1; }
  sleep 5
done

cleanup
if [ "$fail" -eq 0 ]; then echo "PASS: sustained <80C SoC, no throttle, bay <45C ($OUT)";
else echo "FAIL: see $OUT - shell goes back to CAD (spec 10.1)"; exit 1; fi
