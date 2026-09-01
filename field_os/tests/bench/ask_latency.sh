#!/usr/bin/env bash
# SCOUT MK-1 bench: ASK round-trip latency (software-architecture.md §5 / §7.1).
# Simulates: ASK release -> whisper transcribe -> retrieval -> LLM (prompt-cached)
# -> first sentence -> Piper synthesis start. Prints per-stage seconds and the
# first-audio total, over N runs (median matters, run >= 10).
#
# PASS: first_audio median <= 5.5 s (prompt cache warm); full reply <= 15 s.
# Run once with MODEL=qwen3-0.6b and once with qwen3-1.7b; ship the biggest PASS.
# Record the canned WAV from the actual kid once; toddler speech is the test.
set -u
N="${N:-10}"
WHISPER="${WHISPER:-$HOME/scout/whisper.cpp}"
WMODEL="${WMODEL:-$WHISPER/models/ggml-tiny.en.bin}"     # A/B with base.en
LLAMA="${LLAMA:-$HOME/scout/llama.cpp}"
MODEL="${MODEL:-$HOME/scout/models/qwen3-1.7b-q4_k_m.gguf}"
THREADS="${THREADS:-4}"                                   # A/B with 3 if UI janks
WAV="${WAV:-$HOME/scout/testdata/kid_question_4s.wav}"
PIPER_VOICE="${PIPER_VOICE:-$HOME/scout/models/piper/en_US-lessac-medium.onnx}"
CACHE="${CACHE:-/tmp/ask_prompt.cache}"
SYSPROMPT='You are SCOUT, a nature guide for a young child. Answer from the provided field notes only. Reply with short spoken sentences.'

now() { date +%s.%N; }
runs_first=(); runs_full=()

for i in $(seq 1 "$N"); do
  t0=$(now)
  # 1. STT
  TR=$("$WHISPER/build/bin/whisper-cli" -t "$THREADS" -m "$WMODEL" -f "$WAV" -nt 2>/dev/null)
  t1=$(now)
  # 2. retrieval stand-in: FTS query over the species pack (or finds.db when present)
  CTX=$(sqlite3 "$HOME/scout/finds.db" \
    "SELECT snippet FROM species_fts WHERE species_fts MATCH 'robin' LIMIT 3;" 2>/dev/null || echo "The American Robin is a thrush. It eats worms and berries.")
  t2=$(now)
  # 3. LLM, prompt-cached system prefix, streamed; capture time-to-first-sentence
  OUTF=$(mktemp)
  "$LLAMA/build/bin/llama-cli" -t "$THREADS" -m "$MODEL" -n 160 --no-display-prompt \
      --prompt-cache "$CACHE" \
      -p "$SYSPROMPT
FIELD NOTES: $CTX
CHILD ASKED: $TR
ANSWER:" > "$OUTF" 2>/dev/null &
  LPID=$!
  t3=""
  while kill -0 $LPID 2>/dev/null; do
    grep -qm1 '[.!?]' "$OUTF" && { t3=$(now); break; }
    sleep 0.05
  done
  wait $LPID; t4=$(now); [ -z "$t3" ] && t3=$t4
  # 4. Piper on the first sentence, time to synthesis complete (streamed in prod)
  head -c 400 "$OUTF" | piper --model "$PIPER_VOICE" --output_file /tmp/ask_out.wav >/dev/null 2>&1
  t5=$(now)
  first=$(echo "$t1 $t0 $t3 $t2 $t5 $t4" | awk '{print ($1-$2)+($3-$4)+($5-$6)}')  # stt + llm-to-1st-sentence + tts
  full=$(echo "$t5 $t0" | awk '{print $1-$2}')
  echo "run $i: stt=$(echo "$t1 $t0"|awk '{printf "%.2f",$1-$2}')s retr=$(echo "$t2 $t1"|awk '{printf "%.2f",$1-$2}')s llm1st=$(echo "$t3 $t2"|awk '{printf "%.2f",$1-$2}')s llmfull=$(echo "$t4 $t2"|awk '{printf "%.2f",$1-$2}')s tts=$(echo "$t5 $t4"|awk '{printf "%.2f",$1-$2}')s | first_audio=$(printf '%.2f' "$first")s full=$(printf '%.2f' "$full")s"
  runs_first+=("$first"); runs_full+=("$full"); rm -f "$OUTF"
done

med() { printf '%s\n' "$@" | sort -n | awk '{a[NR]=$1} END{print a[int((NR+1)/2)]}'; }
MF=$(med "${runs_first[@]}"); MU=$(med "${runs_full[@]}")
echo "median first_audio=${MF}s (PASS <= 5.5), median full=${MU}s (PASS <= 15)"
awk -v f="$MF" -v u="$MU" 'BEGIN{ if (f<=5.5 && u<=15) {print "PASS"} else {print "FAIL"; exit 1} }'
