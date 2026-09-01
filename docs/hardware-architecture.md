# SCOUT MK-1 — HARDWARE ARCHITECTURE
## Storage decision, corrected budgets, stack plan, fit-check — rev 1 (Sep 1 2026)

Companion to `software-architecture.md`. This doc resolves the open items from the
Aug 31 external review, **verified against the repo** (parts list, FULL SPEC rev 24,
weekly guides, `cad/build_pokedex.py` rev 23) **and against current part data**
(researched Sep 1 2026; sources listed in §9). Everything tagged `[EST]` is computed
from datasheets/published benchmarks with the math shown; `[BENCH]` means only the
real hardware can answer it and the test is named.

**Verification verdict on the prior review, in one paragraph:** finding 1 (PCIe
conflict) is real and the repo already flags it (spec §9, AI HAT+ marked OPTIONAL) —
but the review's option (a) is dead: Pineboards shut down (~Feb 2025) and the Ai
Bundle is delisted/out of stock. Finding 2 is aimed at the wrong target — the repo
never claims the Hailo runs the LLM; spec §5.1/§9 already say v1 runs on CPU.
Finding 3 (battery weight) confirmed, and it's worse: the whole mass budget is broken,
not just the cell line (§3). Finding 4: the repo already contains the exact thermal
procedure (spec §10.1) — it's now executable as `field_os/tests/bench/concurrent_soak.sh`.
Finding 5: the GPS is a wired BN-880 UART module, not a HAT (the HAT is a dismissed
alt), so the header pile is smaller than the review assumed — but the CAD has harder
problems the review missed (§7). Finding 6 (budget) confirmed: real prices land
~$400–460 (§6), and the repo itself carries three different totals ($376 tracker,
~$375 spec §3, $345–395 footnote).

---

## 1. DECISION: storage & accelerator topology

**v1 ships CPU-only. The owned NVMe SSD gets the whole PCIe lane via the Pimoroni
NVMe Base (PIM699, $15.99). No AI accelerator inside the shell. A defined, bench-gated
upgrade path to the AI HAT+ exists (§2) and the shell reserves for it.**

### Why this is the pick and not a punt

1. **The CPU meets the spec's own targets.** The spec's scan budget is "one-shot
   inference well under a second" with a 3 s timeout state. Published Pi 5 CPU numbers
   for int8 classification: MobileNetV2 ~12 ms, EfficientNet-Lite0 ~18 ms per frame; a
   Seek-class model (~16k taxa head) is bigger, call it **~0.1–0.5 s [EST]** — inside
   budget with margin. BirdNET: a Pi 3B+ analyzes a 3 s window in ~500 ms; on the Pi 5
   that's **~100–250 ms [EST]**. The LLM runs on CPU no matter what (next point).
2. **The Hailo-8L cannot run the LLM** — confirmed: no LLM/GenAI category in the
   Hailo-8/8L model zoo, no DRAM interface for streaming weights. LLM support is the
   Hailo-10H's feature (see §2, AI HAT+ 2). So the accelerator's only real job here is
   "vision/audio off the CPU" — worth having only if the CPU misses the targets above.
3. **The Hailo doesn't accelerate OUR vision model until someone ports it.** There is
   no published iNaturalist-taxa HEF. Buying the HAT buys a fast ResNet/ViT demo, not
   a faster SCOUT scan, until a Dataflow-Compiler port of the chosen species model is
   done — a real project in itself. (The whole "which vision model" question is a W2
   task; see software doc §8.5.)
4. **Every multi-device PCIe topology carries documented reliability baggage** —
   exactly the risk the review flagged, now with receipts: the Pi 5 NVMe-behind-switch
   boot bug (raspberrypi/firmware #1833, fixed only for some switches by EEPROM
   2024-10-21); Hailo MSI failure behind switches needing a dtoverlay
   (raspberrypi/linux #6206); Hailo enumeration loss on some switch boards (Geekworm
   reports) and under marginal power. A direct FFC-to-NVMe-Base link has none of these
   failure modes.
5. **The combo-board option is gone anyway**: Pineboards is out of business; the Ai
   Bundle (BM2L-AIS-H8L, ASM1182e switch, Gen2) shows out-of-stock/unavailable at
   every EU reseller checked and no US listing. The nearest living substitute
   (Pimoroni NVMe Base Duo + a bare Hailo-8L M.2 module) means sourcing the M.2 module
   separately and re-entering all of point 4.

### Exact v1 parts

| Part | P/N | Price (Sep 2026) |
|---|---|---|
| NVMe adapter | Pimoroni NVMe Base for Pi 5, PIM699 | $15.99 |
| SSD | owned (2280, from the Argon ONE V3) | $0 |
| Recovery card | official Raspberry Pi A2 microSD 128 GB (SC1645) — Pi 5 does A2 command queuing; SanDisk Extreme is the alt (High Endurance has NO A2) | $32.95 (in `misc`) |

Config: EEPROM `BOOT_ORDER=0xf416` (NVMe first), bootloader ≥ 2024-10-21 as a matter
of hygiene. The microSD stays flashed as the recovery/boot-fallback card.

### The tradeoff, stated honestly

What CPU-only costs: the scan reveal is ~0.1–0.5 s slower than a Hailo-accelerated one
(imperceptible inside the 7-beat scan choreography), and during the rare
LISTEN-while-ASK overlap the jobs serialize (software doc §1 shows the UI already
serializes them). What it buys: −$78 (HAT + heatsink), −3 W peak thermal load inside a
sealed PETG shell, one fewer board in a 45 mm-deep stack, zero PCIe-switch risk
surface, and no dependency on an unported model. If the W2 bench proves the vision
model misses "under a second," the upgrade path below is pre-planned rather than a
redesign.

## 2. The bench-gated upgrade path (and when to take it)

**Trigger**: `vision_once.py` on the real W2 model > 1.5 s median on CPU, OR the §7.3
jank probe fails during scan states.

**Path**: AI HAT+ 13 TOPS ($70 CanaKit / $76.95 PiShop) on the PCIe FFC + 16 mm
stacking header (officially clears the Active Cooler; board adds ~3.2 mm + heatsink,
~$8 aftermarket pad — the base AI HAT+ ships bare, already in the repo's parts notes)
— and the NVMe moves OFF PCIe to USB3:

| Part | Detail | Price |
|---|---|---|
| USB3 M.2 enclosure | **ASMedia ASM236x** chipset (e.g. Unitek 10 Gbps ~$20–41, Plugable USBC-NVME $22.95 — verify chipset rev before buying). **Avoid Realtek RTL9210/B**: documented unresolved Pi 5 disconnect/IO-error issue (raspberrypi/linux #7080). | ~$21–41 |

Config that MUST accompany USB boot here: the Pi is powered from the UPS HAT, not a
PD negotiation, so the bootloader defaults USB ports to 600 mA and **disables USB
boot** — set `usb_max_current_enable=1` and `PSU_MAX_CURRENT=5000` in the EEPROM.
USB3 ceiling ~400 MB/s and ~5k+ IOPS — still far above SQLite + thumbnail needs.

**Watch item, not a recommendation**: the AI HAT+ 2 (Jan 2026, $130, Hailo-10H, 40
TOPS INT4, 8 GB onboard) DOES run LLMs. It would be the first hardware that changes
the ASK latency math (software doc §5). It shares the same single PCIe lane, the same
storage displacement, and adds an immature toolchain — revisit only if the 0.6B-model
ASK bench fails AND the product survives contact with the kids.

**Gate before any of this enters the shell**: `field_os/tests/bench/pcie_storage_soak.sh`
— 20/20 cold boots with both devices enumerated, then ≥15 min of concurrent fio +
`hailortcli benchmark` with zero dmesg PCIe/NVMe errors and stable FPS.

## 3. Mass budget — corrected (the finding is bigger than the cells)

Current repo figures (LAYOUT LAB): total ~830 g; line items "cells ~187 g, Pi + HAT
stack ~200 g, screens ~160 g, buttons ~70 g, shell + misc ~110 g." Two problems before
any correction: those line items sum to **727 g, not 830 g**, and several are far off
current part data.

| Line | Repo budget | Corrected | Basis |
|---|---|---|---|
| 4× Samsung 50E cells | 187 g | **276 g** | 69 g/cell max, Samsung spec sheet |
| UPS HAT (E) board | (inside "stack") | **130 g** | retailer spec, without cells |
| Pi 5 + Active Cooler | (inside "stack" 200 g) | 46 + ~35 g [EST] | official Pi 5 mass; cooler unpublished |
| NVMe Base + SSD | (inside "stack") | ~30 g [EST] | board + 2280 stick |
| ReSpeaker v2 + BN-880 + MAX98357A + RTC cell | (inside "stack") | ~40 g [EST] | BN-880 = 10 g sourced; rest small boards |
| 5" DSI LCD (C) | (inside "screens" 160 g) | ~120–150 g | listed item weight 0.15 kg |
| 5.83" e-ink panel + driver HAT | (inside "screens") | ~70 g [EST] | 125.4×99.5×1.18 mm glass + driver board |
| Buttons/deck (60 mm Sanwa + OBSF-24 + 7 tactiles + TPU caps) | 70 g | ~100–130 g [EST] | the 60 mm Sanwa is a large mechanical part [BENCH: weigh it] |
| Speaker 40 mm | (—) | ~25 g [EST] | typical 40 mm 8 Ω |
| Shell print | (inside "shell+misc" 110 g) | **~290 g [EST]** | net shell surface ≈ 92,000 mm² × 2.5 mm wall × 1.27 g/cm³ PETG ≈ 292 g, before baffle/duct/bosses (+~30 g) |
| Inserts, Torx, standoffs, wiring, gaskets | (—) | ~50 g [EST] | |
| **Total** | **~830 g claimed** | **~1,210–1,290 g [EST ±15%]** | |

**The device as currently specced is ~1.2 kg, not 830 g** — half again the number the
kid-grip call was made on, and the Layout Lab chip already warned "840 g is real."
1.2 kg is two-handed-with-effort for a 5-year-old and heavy on a neck lanyard
(compare: iPad 10.9" = 477 g). This does NOT change the locked deck or layout — it
changes what must happen before printing:

1. **Re-run the kid hold test with a 1.2 kg weighted mockup**, not the old figure.
   That test, not this doc, decides if mass is a blocker.
2. The two biggest levers if it fails, in order: the **battery subsystem (406 g =
   pack + board, a third of the device)** — a 2-cell topology would save ~200 g but
   the UPS HAT (E) is a locked 4S board (rev 24), so this reopens a settled decision
   and is flagged, not recommended; and the **shell wall strategy** (2.5 mm uniform →
   2.0 mm + internal ribs saves ~60–70 g [EST] — but see §7 crush-wall requirement
   first).
3. Weigh every part on arrival and keep a running true total in the console.

## 4. Power budget — corrected (the good news section)

Pack: 4S1P × 4,900 mAh min = **~72–74 Wh**. Sourced anchor points: Pi 5 idle
~2.4–3.3 W, full 4-core sustained load ~9–10 W; LCD (C) backlight-on ~2.5 W [EST from
comparable Waveshare DSI panels ~500 mA @5 V]; camera ~0.7 W; GPS ~0.15–0.25 W;
Hailo-8L would add ~3 W (not in v1); e-ink ~0 W static.

| Posture | Draw at 5 V rail [EST] | From pack (÷~0.88 buck) | Runtime on 74 Wh [EST] |
|---|---|---|---|
| Idle field posture (e-ink on, LCD off, GPS hot, CPU idle) | ~3.2 W | ~3.6 W | **~18 h** |
| Mixed field day (scans + listens + asks, LCD duty-cycled) | ~5.5–7 W avg | ~6.3–8 W | **~9–11 h** |
| Sustained abuse (soak test load + LCD) | ~13–14 W | ~15–16 W | ~4.5 h |

The repo's "4–7 h mixed use" claim is **conservative — real mixed use lands ~9–11 h
[EST]**. The 5 V/6 A buck rating clears the worst case with margin: sustained abuse ≈
14 W ÷ 5 V ≈ **2.8 A**, plus Hailo later ≈ 3.4 A, against 6 A rated — ✓. Pack-side
current at 14 W ≈ 1 A across 4S — trivial for 9.8 A-rated 50E cells — ✓ (rev 24's
verification stands). Charge policy stays as spec §10.2: moderate rate, never
unattended fast-charge (no hardware thermal cutoff — confirmed again; see §5 gauge).

**One rev-24 claim to re-verify on the bench**: "5 V/6 A sustained" is Waveshare's
rated figure; the wiki does not qualify duty cycle. The W5 load test already covers
this — watch the fuel gauge current AND `vcgencmd get_throttled` under-voltage bits.

## 5. Electrical map — buses, addresses, pins (three repo errors fixed here)

### I2C1 (GPIO 2/3) address map — no conflicts, but two console corrections

| Device | Address | Note |
|---|---|---|
| UPS HAT (E) monitor | **0x2D** | **The console's W5 guide says "MAX17040 at 0x36" — that is WRONG for this board.** The UPS HAT (E) exposes an onboard MCU at 0x2D (register map: 0x10 VBUS V/I/P, 0x20 battery block, 0x30 per-cell voltages ×4, 0x02 charge state) fronting a TI BQ4050 gauge + IP2368 PD charger. The W5 i2cdetect step, the batteryd prompt, and the blueprint tab all need updating; telemetry is richer than MAX17040 (per-cell voltages → balance monitoring in the diagnostics screen). |
| ReSpeaker 2-Mics codec | **0x18** (v2, TLV320AIC3104) | v1 (WM8960 @ 0x1A) predates Pi 5 support and is no longer sold new — buy v2.0; console guides referencing WM8960 are stale. |
| BN-880 compass | 0x1E (HMC5883L) or **0x0D (QMC5883L)** — batch-dependent | run i2cdetect on arrival; optional in v1 (MAP uses GPS fix only). |
| ADS1115 (bay NTC) | 0x48 | **Required, not optional**: Pi GPIO is digital-only, so the parts-list phrasing "10k NTC + voltage divider (or ADC breakout)" understates it — without the ADC there is no thermistor reading, and thermd IS the thermal cutoff. |

(LCD (C) touch, if that panel is chosen, lives on the DSI ribbon's own I2C — not this
bus; leave the touch overlay disabled per rev 8.)

### Other buses

- **UART0 (GPIO 14/15)**: BN-880, default 9600 baud (console guide assumes gpsd
  autodetect — fine, but set the baud explicitly in `/etc/default/gpsd`).
- **I2S (GPIO 18–21)**: ReSpeaker capture + speaker path (software doc §8.4 decision).
- **SPI0 (GPIO 8/10/11)**: e-ink. Two default-pin collisions to remap in `epdconfig.py`:
  Waveshare defaults **RST=17 collides with the ReSpeaker button (GPIO17)** → move
  e-ink RST to GPIO27; **PWR=18 collides with I2S BCLK** → strap the e-ink PWR pin
  high (or any free pin) — never leave these at driver defaults. DC=25, BUSY=24 stay.
  The ReSpeaker's APA102 LEDs also sit on SPI0 — they'll flash garbage during e-ink
  transfers; they're sealed inside the shell (harmless), or snip/mask them.

### gpio-keys pin budget — 12 inputs, 12 pins left. Exactly.

| Input | BCM | Input | BCM |
|---|---|---|---|
| D-UP | 4 | LISTEN | 22 |
| D-DOWN | 5 | ASK | 23 |
| D-LEFT | 6 | MAP | 26 |
| D-RIGHT | 12 | VOL+ | 0* |
| SELECT | 13 | VOL− | 1* |
| SCAN | 16 | PWR-request | 7 |

*GPIO 0/1 are the HAT-EEPROM ID pins — legitimate as inputs on a hand-wired bonnet
build (no HAT EEPROM probing needed), with fixed pull-ups already on-board; don't hold
them low through a cold boot. GPIO 17 is burned by the ReSpeaker's own button; GPIO 27
is now e-ink RST; 24/25 e-ink DC/BUSY; 9 stays reserved with SPI0. **Zero spare pins**
— the W3 guide's "six free GPIOs" text is stale (it predates the rev 19/20 deck; the
software doc §6 has the full count) and any new input from here on needs an I2C
expander.

### Mechanical stack (depth axis, 45 mm shell, ~40.5 mm internal)

The UPS HAT (E) is designed to pogo-mount directly under the Pi — but the NVMe Base
also mounts under the Pi (7 mm standoffs), and **both cannot own the underside**. The
concept CAD's answer (UPS board 50 mm away, "pogo pass-through" slot in the baffle) is
not physically real — pogo pins reach millimetres, not centimetres. **Resolution:
remote-mount the UPS HAT exactly where the CAD already places it and abandon the pogo
pins as the power path** — power the Pi from the UPS via short heavy leads into the
40-pin header 5 V/GND (through the bonnet; two pins per rail) or via a USB-C pigtail
into the Pi's power port, plus the I2C pair. [BENCH W5: confirm the board tolerates
remote sensing — its USB-A out proves it serves loads off-board; solderable output
pads are unconfirmed, so plan the USB-C pigtail as the fallback.]

Depth stack at the Pi bay, v1 (front → back):

| Layer | mm |
|---|---|
| Front plate | 2.5 |
| e-ink panel + clearance | 1.2 + 2 |
| Clearance to cooler fins | 2 |
| Active Cooler above Pi PCB | ≤16 (officially clears 16 mm headers; fins 13.7) |
| Pi 5 PCB | 1.6 |
| NVMe Base under Pi (standoffs + board + SSD) | ~9 |
| Clearance + back wall | 1 + 2.5 |
| **Total** | **~37.8 of 40.5** ✓ (margin ~2.7 mm — DSI/FPC routing lives here; tight but real) |

With the §2 upgrade (AI HAT+ replaces nothing — it stacks): 16 mm header + 3.2 board +
~6 heatsink above the Pi, NVMe Base **removed** (SSD went to USB) → ~38.6 mm ✓. The
upgrade does NOT fit with the NVMe Base still under the Pi (~46+ mm) — which is
another reason the SSD must move to USB when the Hailo goes in.

## 6. Cost budget — corrected (live prices, Sep 1 2026)

Repo says: tracker $376 / spec ~$375 (range $355–405) / footnote $345–395 — three
different numbers; the review guessed $420–480. Reality with today's prices:

| Item | Repo line | Current | Note |
|---|---|---|---|
| NVMe Base | $15 | $15.99 | |
| 5" DSI LCD | $40 | **$46.99** | (C) w/ touch-disabled; the listed "1024×600 NON-TOUCH" part does not exist — the true no-touch panel is 800×480 (~$46). Decide (software doc §8.2). |
| Camera Module 3 Wide | $35 | $35 | |
| e-ink 5.83" | $40 | $39.99 | |
| Deck buttons | $15 | **~$46** | OBSA-60UK alone is **$39.80** — and see §7: it's SQUARE. + OBSF-24 ~$3 + 12 mm tactiles ~$3 |
| D-pad (5× B3F + cap) | $8 | ~$6 | |
| ReSpeaker 2-Mics **v2** | $20 | **$10.80** | DigiKey; buy v2, not old v1 stock |
| BN-880 | $22 | ~$22 | hobby/drone shop |
| Bonnet + stacking header | $15 | $15 | |
| Active Cooler | $5 | $5 | |
| Speaker + I2S amp | $12 | ~$10 | MAX98357A $5.95 + 40 mm speaker ~$4 (may drop to $4 if the HAT drives the speaker — software doc §8.4) |
| VOL tactiles | $2 | $2 | |
| USB-C pigtail | $6 | ~$8 | |
| Bay NTC + **ADS1115** | $6 | **~$12** | ADC is mandatory (§5) |
| Gasket stock | $4 | $4 | |
| UPS HAT (E) | $33 | $32.99 | (Amazon $44.99 — buy direct) |
| 4× Samsung 50E | $36 | **$24–36** | $5.99/cell on sale, reg $8.99 — 18650batterystore/IMR |
| Shell print | $42 | $42–55 | mass ↑ (§3) may push quotes up |
| Misc (incl. A2 microSD $33, RTC cell, standoffs, 45 W PD) | $35 | ~$45 | microSD alone is $33 official |
| AI HAT+ heatsink line | $8 | **$0 in v1** | moves to the §2 upgrade path |
| **v1 total** | **$376 claimed** | **~$429 (range ~$400–460)** | |
| §2 upgrade path, if triggered | — | +~$100–120 | AI HAT+ $70 + pad $8 + ASM236x enclosure $21–41 |

So the honest v1 number is **~$429 ±10%** — over every repo figure, under nothing the
prior review feared only because the accelerator stays out. APPLIED Sep 1: the console
tracker now carries these prices and computes $429; the three old totals are gone.

## 7. FIT-CHECK against `cad/build_pokedex.py` rev 23 — what does not fit

The vent math checks out (computed slot area 34.76 mm² → intake 348 / exhaust 556 mm²,
matches the spec exactly), the ears are exactly 46.0 mm from SCAN as claimed, the
4-cell bay matches rev 11, and the baffle/duct/chimney concept is sound. The following
do NOT survive contact with real part dimensions — the CAD is concept-grade (it says
so itself) and these are the items the tolerance pass must fix, ordered by severity:

1. **The SCAN button and the battery pack occupy the same depth zone — impossible.**
   The 60 mm Sanwa (any 60 mm arcade button) needs ~25–35 mm behind the panel
   [BENCH: measure the real part — no accessible drawing publishes it]; the UPS HAT +
   cells assembly needs ~27 mm; the deck zone is ~40.5 mm deep. 25+27 > 40.5. The CAD
   hides this by drawing the dome as a decorative squashed sphere with no switch body
   and the cells 50 mm from their own carrier board. **The pack must move out of the
   deck zone entirely** — candidate placement: behind the LCD (z ≈ 60–116, where
   ~33 mm of depth is free behind the 5 mm panel), which also shortens the path from
   pack to the top-edge exhaust; costs: top-heavy CG (weigh in the §3 mockup test) and
   the camera bump + duct must shift left/right to clear the 88×56 board. This is a
   layout regen, not a nudge.
2. **OBSA-60UK is a 60×60 mm SQUARE button, not a round dome.** (Sound
   Voltex/Ongeki thin-profile type, $39.80.) The entire CMF language says round
   magenta dome. Either the design absorbs a square SCAN pad (it's the actual arcade
   rhythm-game part — arguably on-brand), or the part number changes (60 mm round
   illuminated "dome" arcade buttons exist from other makers at $10–20; Sanwa's round
   large buttons are a different family). **Repo wins on naming the part; reality says
   the named part isn't the drawn shape. Decide before CAD regen; the panel cutout
   differs.**
3. **UPS pogo-pin fiction** — resolved by §5's remote-mount decision; the baffle's
   "pogo pass-through slot" gets deleted and replaced by a wire grommet.
4. **NVMe Base drawn on the wrong side**: the CAD shows the SSD board 10 mm behind
   (component side of) the Pi; the real board mounts under the SD-card side. With the
   Pi's underside facing front in the current orientation, the SSD stack intrudes
   toward the e-ink driver PCB region — resolved by the §5 depth table's orientation
   (components/cooler toward back wall, NVMe toward front, e-ink driver board moved
   off-axis).
5. **Exhaust duct collides with the e-ink driver PCB** (duct y −14.5→−6.5 × z 22–138
   at x −12→2 passes through the "PCB_EInkBonnet" volume at y −14.8→−13.2, z 37–67).
   Move the driver board off the duct line (it hangs on an FPC; it can sit left of
   x = −20) or route the duct at the shell's left flank.
6. **Blower drawn on the wrong face**: the Active Cooler is modeled on the Pi's front
   side while the SoC is modeled on its back side. Cosmetic in concept CAD, but the
   duct inlet position (and therefore the §5 depth stack) depends on getting this
   right in the regen.
7. **BN-880 footprint wrong**: drawn 40×18 mm; the real module is **28×28×10 mm,
   10 g**. Easier fit than drawn — but it needs its 28×28 sky window in plain PETG at
   the top face, and the top zone currently also hosts camera bump, both mics, PWR
   slide, VOL rocker, duct outlet, and exhaust grille. Draw the top edge to scale
   before committing.
8. **MAP drawn Ø20 against a Ø24 part** (OBSF-24 needs a 24 mm panel hole).
9. **Missing from CAD entirely**: VOL rocker (top edge), 40 mm speaker + grille
   (DON'T-rule-compliant: grille must be a functional hole pattern), MAX98357A, RTC
   coin cell, bay NTC + ADS1115, ReSpeaker board, and the AI HAT+ that the rev 10
   checklist claims was clearance-checked ("HAT-stack clearance pass" — there is no
   AI HAT in the model). The exploded-view list still references Cell_5/Cell_6 from
   the dead 6-cell layout.
10. **Cell-bay crush wall does not exist as a parameter** (review finding 3,
    confirmed): the pack is protected by the 2.5 mm cosmetic wall and a 2 mm baffle
    shelf. Requirement for the regen: a named `cell_bay` collection with its own
    wall-thickness parameter (≥3 mm + ribs, independent of `WALL`), a lid that
    captures the cells against holder spring-out on drop, and ≥5 mm crumple gap from
    the outer shell on the bottom edge (the drop-landing face).

**Net verdict for "can I print it": No — not the rev 23 geometry.** Shell OUTER
dimensions (135×290×45) survive; the 45 mm depth holds IF the pack leaves the deck zone.

**APPLIED Sep 1 — CAD rev 24 regenerated** (`cad/build_pokedex.py`, .blend/.glb, and the
console's embedded copies): pack behind the e-ink inside a new `cell_bay` crush box
(3 mm walls + 2 mm lid, own parameters), Pi + cooler + NVMe Base behind the LCD (duct
shortened 116→22 mm), switch bodies modeled, pogo fiction deleted, GPS/MAP footprints
corrected, VOL/speaker/ReSpeaker/bonnet/RTC/ADC modeled, back exhaust vents moved
behind the cooler. An AABB collision pass over the internals reports ZERO overlaps.
Two additional findings from that pass: **a Ø40 front-firing speaker cannot clear the
dome + MAP switch bodies** — it now fires through the BACK shell behind the D-pad —
and the D-pad side gaskets carried the same h/d dimension swap as the rev 23 duct
(fixed). Three envelopes remain placeholders to MEASURE on arrival, flagged in the
script: UPS HAT (E) + holders (96×76×26 modeled), 60 mm button behind-panel depth
(32 mm modeled), Active Cooler height (16 mm modeled). The tolerance/snap-fit pass
still stands between rev 24 and a print.

## 8. Bench procedures — the numbers only hardware can give

All scripts in `field_os/tests/bench/` (committed alongside this doc), each with an
explicit PASS/FAIL:

| Question | Script | PASS |
|---|---|---|
| Storage topology stable? (§1/§2) | `pcie_storage_soak.sh` | 20/20 cold boots enumerate; 15 min fio (+Hailo if fitted) zero PCIe/NVMe dmesg errors |
| Thermals in the closed shell? (spec §10.1) | `concurrent_soak.sh` | SoC <80 °C sustained, `get_throttled`=0x0, bay <45 °C, ≥20 min, closed shell, then direct sun |
| ASK fast enough? | `ask_latency.sh` | first audio ≤5.5 s median (per model; ship the biggest that passes) |
| UI alive under load? | §7.3 (software doc) | e-ink partial <1 s, no audio underruns |
| Vision model fast enough on CPU? (§2 trigger) | `loops/vision_once.py` timed | <1.5 s median, else upgrade path |
| 6 A buck real? (§4) | W5 load test (console) | no under-voltage throttle bits at max load |
| Kid can hold it? (§3) | 1.2 kg weighted mockup | the kid, not this doc, decides |

## 9. Primary sources

Pi 5 power/throttle: official docs (power supplies; frequency management). PCIe switch
boot: raspberrypi/firmware #1833 + rpi-eeprom release notes 2024-05-13/2024-10-21.
Hailo-behind-switch: raspberrypi/linux #6206; Hailo community threads (Geekworm switch;
NVMe/undervoltage). Pineboards status: RPi forums t=384981; ThePiHut delistings.
AI HAT+ price/mounting: raspberrypi.com/products/ai-hat, CanaKit, PiShop, Pimoroni
(16 mm header/Active Cooler clearance). Hailo-8L model zoo (no LLM; classification
FPS): hailo-ai/hailo_model_zoo. UPS HAT (E): Waveshare wiki + register map;
int08h/waveshare-ups-hat-e driver (0x2D, BQ4050/IP2368); raspberrypi.dk /
core-electronics (88×56 mm, 130 g). Samsung 50E: SDI spec V1.0 (69 g max);
18650batterystore/IMR pricing. NVMe Base: Pimoroni/Adafruit (under-mount, 7 mm
standoffs). ReSpeaker v2: Seeed/Kiwi (TLV320AIC3104), DigiKey pricing; v1 overlay
(WM8960 0x1A) Seeed GitHub. e-ink pins: waveshareteam/e-Paper `epdconfig.py`. BN-880:
FlyingTech (28×28×10 mm, 10 g), ArduPilot docs (9600 NMEA). OBSA-60UK square/thin
profile: Coin Op Express, rhythm-cons wiki. LLM/whisper/Piper/BirdNET/classification
benchmarks: see software-architecture.md §5 and the research log in the PR/commit
description.
