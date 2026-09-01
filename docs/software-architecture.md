# SCOUT MK-1 — SOFTWARE ARCHITECTURE (Field OS 1.0)
## Concurrency, scheduling, and the ASK latency budget — rev 1 (Sep 1 2026)

Companion to `hardware-architecture.md` (same date). Sources of truth this doc builds ON
TOP of, not instead of: `field-os-design-doc.md` (rev 11), the FULL SPEC rev 24 in the
build console, and `field_os/README.md`. Fixed constraints honored throughout:

- **Two screens, two jobs**: e-ink = the always-on device screen (einkd owns it),
  LCD = camera screen only, sleeps when idle. Not renegotiated here.
- **Quest progress is a SELECT over finds.db**, never a stored counter.
- **Every write is atomic** (temp file, fsync, rename).
- **Thermal cutoff is software-owned** (NTC poll → cooling-down fail ladder).
- **ASK is retrieval + structured JSON**, not freeform generation (rev 24).

> **Placeholder marks**: numbers tagged `[EST]` are estimates computed from published
> benchmarks/datasheets with the math shown; numbers tagged `[BENCH]` can only come from
> the real device — the exact bench procedure is in §7. Nothing in this doc is a
> measured SCOUT number yet.

---

## 1. The core insight: this is a SERIALIZATION problem, not a parallelism problem

The UI is modal by design (one job per screen, one state at a time), so the AI pipeline
should be too. SCAN, LISTEN, and ASK are mutually exclusive user states — a kid cannot
hold the ASK button and press the SCAN dome usefully at the same moment, and the fail
ladder already defines what happens if they try (the newest press wins, the old job is
cancelled). That means **the four heavy engines never legitimately run concurrently at
full tilt.** The "concurrency budget" is really:

1. Exactly **one foreground inference job** at a time (vision OR BirdNET OR whisper OR
   LLM), on all 4 cores but niced below the interactive processes.
2. A **permanent interactive reservation** (1 core's worth) for the kiosk app, einkd,
   audio I/O, and gpsd — the things that make the device feel alive while it thinks.
3. Background work (thumbnail dithering, sync, tile prefetch) only in IDLE, at
   `nice 19` + `ionice -c3`.

The one true overlap in the whole product is inside ASK: **the LLM generates sentence
N+1 while Piper synthesizes and the speaker plays sentence N.** That overlap is what
makes the latency budget in §5 work — Piper's single thread rides alongside the niced
LLM threads and the kernel sorts it out.

The concurrent worst case in spec §10.1 (all four engines at once) remains the THERMAL
test load — it is the abuse case the shell must survive, not the scheduling design.

## 2. Process model (systemd units)

| Unit | What | Runs | RAM [EST] | Notes |
|---|---|---|---|---|
| `fieldos-ui.service` | cage + chromium kiosk (LCD) + localhost app server | always | 400–600 MB | The UI. DSI backlight off = its idle state; process stays. |
| `einkd.service` | Python e-ink daemon, HTTP :8100, SPI | always | ~30 MB | Serializes refreshes; full ~5 s, partial ~0.3 s. I/O-bound, near-zero CPU. |
| `askd.service` | whisper.cpp + llama.cpp (Qwen3-1.7B Q4, mmap'd) + Piper, one pipeline process | always (models resident) | ~1.6 GB | Resident so ASK never pays model-load latency. See §5. |
| `scand.service` | libcamera/picamera2 pipeline + vision model (TFLite/ONNX int8) | on demand (dome press), preloaded model | ~150–300 MB | Cold-start-to-preview is a W1 acceptance test. |
| `listend.service` | BirdNET (TFLite) over ALSA capture | on demand (LISTEN press), preloaded model | ~100 MB | 3 s window, extends to 6 s on detections. |
| `batteryd.service` | fuel-gauge poll → JSON :8200 | always, 5 s period | ~15 MB | I2C read, negligible CPU. |
| `thermd.service` | NTC/ADC poll + SoC/PMIC temps → trip logic | always, 2 s period | ~15 MB | Owns the COOLING DOWN ladder + charge-inhibit (spec §10.2). |
| `gpsd` | stock | always | ~10 MB | BN-880 on UART0. |
| gpio-keys | kernel device-tree, not a daemon | always | 0 | All 12 inputs arrive as evdev key events (§6). |

Total resident [EST]: **~2.4–2.9 GB of 8 GB** — comfortable, with >4 GB left for page
cache (map tiles, species pack, photo I/O). On a 4 GB Pi this does NOT fit with
Qwen3-1.7B resident + Chromium; the documented fallback is Qwen3-0.6B and accepting
model load on first ASK.

## 3. What runs when (state × engine)

| State | vision | BirdNET | whisper | LLM | Piper | camera | LCD | einkd |
|---|---|---|---|---|---|---|---|---|
| IDLE | — | — | — | — | — | off | off | partials |
| SCAN (dome) | **4T, nice+10** | — | — | — | — | preview+still | on | queued |
| LISTEN | — | **4T, nice+10** | — | — | — | off | on (spectrogram) | mirror line |
| ASK hold (recording) | — | — | encode stream | — | — | off | per wake rule | — |
| ASK answer | — | — | **4T → done** | **4T, nice+10** | 1 thread, overlapped | off | per wake rule | — |
| Find landing | — | — | — | — | sting via WebAudio | off | dive anim | **full refresh** |
| COOLING DOWN | refused | refused | refused | refused | — | off | off | glyph |

Rules:
- A new modal press **cancels** the running job (pthread cancel points / atomic flag
  checked between inference chunks), it never queues behind it.
- The e-ink full refresh (~5 s) is pure SPI wait — it overlaps anything for free.
- ASK during an open Find card injects that find as context (already spec'd); the
  retrieval query runs on the interactive core, <50 ms, before the LLM starts.

## 4. Scheduling: cores, threads, priorities

Pi 5 = 4× Cortex-A76. Policy:

- **The foreground inference job gets all 4 threads, at nice +10.** Published Pi 5
  llama.cpp data shows 4 threads measurably beats 3 (generation is memory-bandwidth
  bound, but the 4th thread still helps — sources in §5), and because the job runs
  niced, the interactive processes still preempt it. The 3-thread configuration is the
  documented fallback if §7.3 shows UI jank; ask_latency.sh runs the A/B.
- **No hard cpusets in v1.** `taskset`-pinning inference to cores 1–3 is the documented
  fallback if bench shows UI jank; try plain nice levels first (simpler, and the kernel
  balances better when the inference job is the only heavy thing running).
- Nice/ionice table:

| Process | nice | ionice | Why |
|---|---|---|---|
| chromium (kiosk) | 0 | best-effort 4 | The face of the device. |
| ALSA/pipewire capture + playback | -10 (rtkit ok) | — | Audio dropouts are the one unfixable artifact. |
| einkd | 0 | best-effort 4 | Tiny bursts; must not starve during inference. |
| scand/listend/askd inference threads | +10 | best-effort 6 | Heavy but interruptible; UI preempts them. |
| batteryd / thermd / gpsd | 0 | — | Trivial load; thermd must never be starved (safety). |
| sync, thumbnail dither, tile prefetch | +19 | idle (c3) | IDLE-state only. |

- **thermd is the safety authority**: at SoC ≥ 80 °C sustained or bay ≥ 45 °C it (1)
  cancels the running inference job, (2) posts COOLING DOWN to einkd, (3) inhibits
  charge if charging; at bay ≥ 50 °C it requests controlled shutdown. These thresholds
  restate spec §10.1/10.2; thermd is where they live in code.

## 5. The ASK round trip — latency budget (mic release → first audio out)

Pipeline (all on-CPU; the AI HAT+ plays no part in ASK — see hardware doc §2):

```
hold ASK ──────────────┐ release
  arecord 16 kHz mono  │
  (streaming, no cost) ▼
  whisper.cpp base.en/tiny.en  ──►  transcript
  retrieval over finds.db + species pack (SQLite FTS)  ──►  context block
  llama.cpp Qwen3-1.7B Q4: prompt eval ──► generate (streamed, sentence-split)
        │ sentence 1 ─► Piper ─► ALSA out   ◄── FIRST AUDIO (the number that matters)
        │ sentence 2+ generated WHILE sentence 1 plays
```

Budget per stage for a 4 s kid utterance, ~25-token first sentence. Published Pi 5
anchor points: ~1.5–2 B Q4 models generate ~5–8 tok/s and prompt-process ~25–32 tok/s
(Gemma 3n E2B measured pp512 31.9 / tg128 6.0 tok/s; Qwen2.5-1.5B ~10–14 tok/s;
Qwen3-1.7B Q4_K_M is a 1.28 GB file and decode is memory-bandwidth-bound, so expect
**~5–6.5 tok/s** [EST: measured effective weight-streaming bandwidth 6.6–8.2 GB/s ÷
1.28 GB]). whisper.cpp on Pi 5: tiny ≈ 1.5 s, base ≈ 3 s for a short command
(openHAB whisper-binding figures). Piper on Pi 5: RTF ~0.2–0.35, short sentence in
~0.5–1 s.

| Stage | Qwen3-1.7B | Qwen3-0.6B (~0.4 GB Q4) | Basis |
|---|---|---|---|
| whisper.cpp tiny.en, 4T | ~1.5 s | ~1.5 s | published Pi 5 figure [BENCH on toddler audio] |
| retrieval (FTS5) | <0.05 s | <0.05 s | indexed SQLite, ~10k rows |
| LLM prompt eval, ~100 uncached tok (context + transcript; system+schema prompt-cached) | [EST] ~2.5–3.5 s | [EST] ~1–1.5 s | pp ≈ 28–40 tok/s (1.7B), scales with size |
| LLM first sentence (~25 tok) | [EST] ~3.8–5 s | [EST] ~1.3–1.6 s | tg ≈ 5–6.5 vs ~16–20 tok/s [EST, bandwidth model] |
| Piper first sentence (streamed) | ~0.5–1 s | ~0.5–1 s | RTF 0.2–0.35 on Pi 5 |
| **First audio out** | **[EST] ~8.5–11 s** | **[EST] ~4.5–5.5 s** | |

Three design moves are already priced into that table — without them the 1.7B column
would be ~14–20 s:

1. **Instant acknowledgment sound + waveform swap at release** (0 ms perceived dead
   air — the device visibly "heard you"). Already in the design language.
2. **Prompt-prefix caching**: the system prompt + JSON schema (~250 tok) is identical
   every time — llama.cpp `--prompt-cache` keeps it evaluated, so only the retrieved
   context + transcript (~100 tok) is paid per question. Without it, add ~8–12 s to
   the 1.7B column. Non-negotiable.
3. **Sentence-streamed TTS**: first audio when the first sentence closes, not when
   generation ends.

**Honest conclusion the numbers force: Qwen3-1.7B misses a 4-year-old's attention span
even with every trick applied.** The W3 plan already says "drop to 0.6B if replies
lag" — the published data says it will lag, so plan for **Qwen3-0.6B as the shipping
default** and treat 1.7B as the upgrade that must EARN its way in on the bench.
Pass/fail (§7.1): **first audio ≤ 5.5 s median, full reply ≤ 15 s** — run both models,
ship the biggest one that passes. If even 0.6B misses, drop the JSON-structure tokens
from the reply path (speak plain text, validate structure only for on-screen use).

RAM/model inventory (resident under askd): Qwen3-1.7B Q4_K_M 1.28 GB (0.6B ~0.4 GB),
whisper base.en 142 MB / tiny.en 75 MB, BirdNET GLOBAL 6K v2.4 FP16 ~25 MB, Piper
en_US medium voice ~63 MB.

## 6. Input map (gpio-keys) — 12 inputs, and the stale "six buttons" guide

The W3 step-by-step guide in the console wires "six Sanwa buttons" on six free GPIOs.
**That guide predates the rev 19/20 deck and undercounts.** The real input set:

D-pad U/D/L/R + SELECT (5) + SCAN + LISTEN + ASK + MAP (4) + VOL+/VOL− (2) +
PWR-request (1) = **12 GPIO inputs**, all active-low with internal pull-ups, all in one
gpio-keys device-tree node (so the whole deck is evdev key events; Chromium reads them
as keyboard input, no daemon needed).

Pin budget after the buses claim theirs (full map in hardware doc §5): exactly 12–13
BCM pins remain free. It fits, with **zero spare pins** — the hardware doc carries the
pin-by-pin assignment and the two conflicts found (e-ink RST default = GPIO17 collides
with the ReSpeaker button; e-ink PWR pin on some Waveshare revisions defaults to GPIO18
= I2S BCLK). Both are remappable in software; neither is a blocker; both must be set
explicitly, not left at driver defaults.

## 7. Bench procedures (run these, bring back numbers)

Scripts live in `field_os/tests/bench/`. Each prints a PASS/FAIL against the stated
threshold. Run over SSH from the Mac against the bench Pi.

### 7.1 `ask_latency.sh` — full ASK round trip
Plays a canned 4 s WAV (record the actual kid once, reuse forever) into the pipeline,
timestamps each stage boundary, 10 runs, reports median + p95.
**PASS: first-audio ≤ 5.5 s median with prompt cache warm; full reply ≤ 15 s** —
run both Qwen3-0.6B and 1.7B, ship the biggest model that passes.
Also runs the A/B: whisper tiny.en vs base.en, LLM 4 vs 3 threads.

### 7.2 `concurrent_soak.sh` — the spec §10.1 thermal load, made executable
Loops all four engines simultaneously (the abuse case): whisper.cpp on a looped WAV,
llama.cpp generating continuously, vision model on a looped still, BirdNET on a looped
clip — ≥ 20 min, logging `vcgencmd measure_temp`, PMIC temp
(`vcgencmd pmic_read_adc`), bay NTC, and `vcgencmd get_throttled` every 5 s to CSV.
**PASS: SoC sustained < 80 °C, zero throttle flags, bay < 45 °C** (case closed;
outdoor-sun variant per spec §10.1).

### 7.3 UI jank probe — interactive reservation check (manual until W4/W5)
While 7.2 runs, measure: einkd partial-refresh round trip < 1 s, kiosk rAF frame time
p95 < 33 ms, audio playback underrun count = 0 over 5 min. (Scriptable only once einkd
and the kiosk exist — W4; until then it's a checklist, not a file.)
**PASS: all three.** FAIL → apply the taskset fallback from §4 and rerun.

### 7.4 Storage concurrency (only if the AI HAT+ ever goes in)
See hardware doc §2 (gate) and §8 — fio + Hailo inference loop; owned by the hardware
doc since the pass criterion is PCIe enumeration stability, not software scheduling.

## 8. Repo conflicts this doc surfaces (fix in the console, not here)

1. **LLM name drift**: FULL SPEC §5.3 and the W3 step-by-step guide still say
   Qwen2.5-3B-Instruct / Gemma 3 4B / Qwen2.5-1.5B. The W3 plan summary, design doc,
   boot screen, and rev 24 all say **Qwen3-1.7B (Q4), fallback 0.6B** — that newer pick
   is what this doc budgets for. Update spec §5.3 + the W3 guide text.
2. **LCD part vs. spec mismatch (decide, then fix the doc that loses)**: the parts
   list says "1024×600 IPS, NON-TOUCH" and links the Waveshare 5in DSI LCD (C) — but
   the (C) is a capacitive TOUCH panel ($46.99), and Waveshare's actual no-touch 5in
   DSI panel (SKU 20543) is 800×480 — the resolution the design doc §4 already lays
   out. Either buy the (C) and leave its touch electrically/software-disabled (rev 8
   honored by policy, kiosk targets 1024×600), or buy the true no-touch 20543 and the
   design doc's 800×480 layout is already correct. Hardware doc §6 prices both.
3. **"Six buttons on six free GPIOs"** (W3 guide): stale, see §6 — 12 inputs.
4. **Two speaker paths**: rev 11 added MAX98357A + 40 mm speaker, but the ReSpeaker
   2-Mics HAT has its own speaker output (3.5 mm + JST), and both codecs live on the
   Pi's single I2S interface. Note the HAT is now **v2.0 (TLV320AIC3104 codec at I2C
   0x18)** — the WM8960 v1 predates Pi 5 support and is no longer sold new, so every
   WM8960/0x1A reference in the console guides is stale. Decide one path in W4:
   (a) drive the 40 mm speaker from the HAT's own JST output (−$6, one less board —
   verify its drive level on the bench first; the AIC3104 is a headphone-class
   output), or (b) keep the MAX98357A for 3 W and route ONLY playback to it, capture
   via the HAT — a custom ALSA/device-tree split that must be bench-proven.
   Recommendation: bench (a) for loudness first; keep (b) as the fallback.
5. **"iNaturalist's open vision model" is not a turn-key download.** iNat's production
   model and the Seek on-device model are not published as offline TFLite/ONNX files.
   Real W2 candidates: the TF-Hub AIY natural-world classifiers (iNat-trained plants
   /insects/birds heads), a self-quantized model trained on iNat open data, or another
   published species classifier. Pick and validate in W2 — the "one model, 10k+ taxa,
   quantized export" line in spec §5.1 is an assumption, not a shipping artifact.
