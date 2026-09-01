# FIELD OS - the SCOUT MK-1 software

The actual device software lives here. The build console (`../index.html`) is the plan;
this directory is the product. Target environment: **Raspberry Pi OS Lite (64-bit),
Trixie / Debian 13**, on a Pi 5 booting from NVMe. Headless - no desktop; the UI is a
kiosk Chromium page on `cage` (single-app Wayland compositor) served from localhost.

Design source of truth: `../docs/field-os-design-doc.md` (rev 11). Hardware + safety
spec: the SPEC tab in the build console (rev 25). Architecture: `../docs/hardware-architecture.md`
and `../docs/software-architecture.md` (Sep 1 review); bench gates in `tests/bench/`.

## Architecture at a glance

Two-screen OS, one app, one handoff:
- **Top LCD (DSI, non-touch)** - camera screen ONLY: viewfinder during scans, ASK
  transcript while listening. Sleeps (~12s idle) when not scanning.
- **E-ink (SPI)** - the always-on device screen: library, wiki cards, map, badges,
  D-pad cursor. Full refresh only on major view changes, silent partials elsewhere.

```
src/fieldos/
  main.py            boot + service wiring (systemd units come later)
  hal/               hardware abstraction: buttons (gpio-keys), displays,
                     camera (libcamera/rpicam), GPS (gpsd), UPS HAT fuel gauge (I2C),
                     thermistor, audio in/out (ReSpeaker / MAX98357A)
  idloop/            the ID loop: vision scan (iNaturalist model, TFLite/ONNX),
                     LISTEN (BirdNET), confidence thresholds, the permanent
                     toxic/mushroom "candidate only" warning layer (rev 24)
  ask/               ASK brain: whisper.cpp ASR -> retrieval over the local field
                     DB with structured JSON out -> Piper TTS. No fine-tuning in v1
                     (LoRA later, trained off-device). Qwen3-1.7B via llama.cpp.
  data/              finds log: atomic writes ONLY (temp file, fsync, rename),
                     GeoJSON + thumbnails, offline CesiumJS tile store, home-WiFi
                     sync script to the public web twin
tests/               bench tests run over SSH from the Mac
```

## Hard rules (spec rev 24, non-negotiable)

1. **Every write is atomic.** Temp file, fsync, rename. Never unplug a running Pi.
2. **PWR button requests a controlled shutdown** (gpio-keys -> systemd poweroff).
   The slide switch on the top edge is the frozen-unit backup only.
3. **Danger layer is permanent UI**: toxic/mushroom/dangerous matches always render
   the "CANDIDATE ONLY - do not consume or handle" band.
4. **Thermal cutoff is software-owned** (the UPS HAT has none): poll the battery-bay
   NTC thermistor, fail to a "cooling down" e-ink glyph, never silently throttle.
5. **No cloud, no accounts on the device.** The only token anywhere lives in the
   home-WiFi web twin, never on the unit.

## Week mapping (the 7-week plan in the console)

- W1: bench bring-up - OS on NVMe, DSI LCD, camera preview, kiosk skeleton
- W2: `idloop` vision + BirdNET on CPU, mic HAT
- W3: `ask` brain + GPS wiring
- W4: `hal` buttons/e-ink/audio + kiosk skin
- W5: power - fuel gauge UI, soft-shutdown path, load + thermal tests
- W6: case transplant + offline tile download
- W7: field map + sync + web twin, launch

Dev setup (W1): `python3 -m venv .venv` inside `~/scout`, everything pip-installed
in the venv, kiosk served by `python3 -m http.server` until a real server earns it.
