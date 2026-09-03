# SCOUT MK-1 - Fact Sheet

**What it is:** A real-world Pokedex. A fully offline handheld nature scanner that
identifies plants, insects, and birdsong, answers questions about what you found,
and logs every find to a map of your own exploring.

**Who it is for:** Built for a 3-year-old naturalist. Also: a first hardware build
for his dad, built entirely in public.

**Design language:** Solarpunk field journal. Golden-hour light, botanical
greens, warm paper; cyan holographic scan arcs over real nature. The device
itself keeps a phosphor-terminal LCD and a 1-bit e-ink screen - modern guts,
honest retro exterior. Brand guide: `../brand/BRAND-GUIDE.md`.

**Status:** Week 1 of 7 - bench bring-up in progress (as of Sep 1, 2026). Spec rev
25, CAD rev 24. Live status: https://jastman.github.io/Scout-Pokedex-Field-OS/

## Design drivers

1. Fully offline, dedicated-use device - does one thing well (nature recognition).
   No WiFi, no 4G, no accounts, no subscription.
2. On-device, fine-tuned LLM.
3. Portable, handheld, kid-proofed.

## Hardware highlights (spec rev 25)

- Raspberry Pi 5 + Active Cooler + NVMe storage (Pimoroni NVMe Base)
- Dual displays, one job each: 5" color LCD viewfinder (wakes only while scanning)
  + 5.83" black-and-white e-ink for the finds library
- Camera (point-and-scan viewfinder), ReSpeaker mic array (birdsong ID), GPS (BN-880)
- 60mm magenta SCAN dome (Sanwa OBSA-60UK) - one signature move a kid finds in
  two seconds - plus LISTEN and ASK buttons, D-pad, MAP button
- 4x 21700 cells on a UPS HAT, translucent shell: the batteries and brass are
  the decoration
- Target BOM: $429. Est. mass ~1.2 kg.

## FIELD OS

Custom offline OS. Species models live on the device. The interface is one app,
two displays, one handoff: scan on the color screen, the find lands on e-ink.

## Timeline

- Aug 2026: concept, spec rev 1, CAD layout A begins
- Aug 31, 2026: Pi 5 flashed and running (bench case)
- Sep 1, 2026: architecture review - spec rev 25, CAD rev 24, BOM re-priced
- 7-week build plan in progress, all public

## The family

SCOUT MINI comes first: a pocket brick with two top buttons (CAPTURE and LISTEN),
a camera on the back, one e-ink screen on the front, a mic and a small speaker.
No viewfinder - point and capture; the screen shows what you caught. It proves
the capture-to-identify loop in about 4 weeks, then SCOUT PRO (the dual-screen
field unit above) inherits the working code and parts. One brand, one OS, two
devices.

## Links

- Console (live build status, simulator, CAD viewer):
  https://jastman.github.io/Scout-Pokedex-Field-OS/
- Source (spec, CAD, BOM, plan): https://github.com/Jastman/Scout-Pokedex-Field-OS
