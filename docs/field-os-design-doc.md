# FIELD OS 1.0 - DESIGN.md
## SCOUT MK-1 "Field Unit 01" - UX design pass, rev 11 (Aug 28 2026)

A plain-text design system for the whole device OS. Paste the TOKENS block into every
prompt or PR that touches a screen. One job per screen (locked rev 8): the 5" LCD is
the CAMERA SCREEN - viewfinder / LISTEN spectrogram / ID reveal - and it is OFF
(black, backlight dead) when there is nothing to see. Rev 11 (Jake's call, Aug 28)
adds two jobs beyond scanning: a FIND PHOTO VIEWER (full color, while the matching
card is open on the e-ink) and the ASK VOICE UI (your amber waveform while you talk,
the AI's phosphor waveform + reply text when it answers - piper TTS reads it aloud).
The 5.83" B/W e-ink is THE DEVICE SCREEN - always on at 0W: library, quests, badges,
map, field cards. D-pad + center SELECT is the only navigation, plus a VOL +/-
rocker on the top edge. Non-touch LCD. No typing anywhere. Voice-first (toddler STT).

REV 11 CHANGES (Aug 28, Jake's steering):
1. BUGFIX - MAP FROM CARD: pressing MAP on a Find's card now closes the card (and any
   LCD overlay) before loading the map. Layer ordering fixed; Cesium tiles own the
   e-ink canvas. The map is the showcase surface - never blocked.
2. REAL FIND PHOTOS: the still captured at scan time is saved with the Find and
   becomes the card's art (Bayer-dithered to 1-bit through the real e-ink pipeline).
   Pre-device Finds carry reference photos from the offline species pack
   (iNaturalist-derived, labeled). 1-bit sprites stay everywhere else in the OS.
3. LCD PHOTO VIEWER: while any Find's card is open on the e-ink, the top LCD shows
   the Find's real photo in full color, with a provenance caption.
4. ASK VOICE UI: hold ASK, the LCD shows a live amber waveform reacting to the kid's
   voice; when the local AI answers, a different shape + color (phosphor, rounded)
   with the reply text below, while piper TTS reads it aloud. Implies TTS in the OS.
5. HARDWARE: speaker (MAX98357A I2S amp + 40mm 8ohm 3W), VOL +/- rocker (2 tactiles,
   top edge, same gpio-keys daemon), USB-C PD panel charge port (bottom edge, wired
   to the UPS HAT charge input). Reflected in BOM, build plan, tokens, blueprint.

---

## 1. TOKENS

### Type
- PIXEL (Press Start 2P): names, tab labels, buttons, numbers that matter. ALL CAPS.
- MONO (single-weight): micro-labels, coordinates, metadata rows. ALL CAPS on e-ink.
- Kid rule: icons carry meaning, type carries detail. A 4-year-old reads the icons,
  dad reads the micro-type.

### LCD palette (camera screen)
- BG       #070a07  (near-black, never pure #000 - OLED-bright text needs a floor)
- PHOS     #57f7a0  (phosphor green - primary: HUD, text, sprites)
- MAGENTA  #ff3d9a  (SCAN only - the dome's color, shutter moments)
- CYAN     #2ee6e6  (LISTEN / audio)
- AMBER    #ffc857  (ASK, warnings, low battery)
- RED      #ff5a5a  (fail states only - never decoration)
- DIM      #2a4a38  (secondary text, grid lines)

### E-ink palette (device screen) - TRUE 1-BIT
- PAPER    #f2ecdd  (sim only - the panel itself is cream)
- INK      #101010
- Shade is DITHER, not gray: 4 levels via 2x2 Bayer (25/50/75%). Any CSS gray on the
  e-ink is a lie the panel cannot tell. Photos and art = dithered bitmaps.

### Space & shape
- LCD: 4px base unit. HUD margins 8px. Cards radiused 6px, 1px PHOS stroke.
- E-ink: 2px base unit. Card grid 3-up, 8px gutters. Cursor = 2px INK invert box.
- Every interactive element gets a 1-bit hover/cursor state - the inverted block IS
  the focus ring. No drop shadows anywhere. Depth = dither, not blur.

### Motion (LCD only - e-ink never animates)
- Shutter freeze: instant (0ms). Theater scans: 400ms. ID reveal pop: 250ms spring.
- Dive-to-e-ink handoff: 1500ms, creature shrinks toward the bezel gap.
- E-ink "motion" = the refresh itself: full ~5s flash-invert (Polaroid landing),
  partial ~0.3s (cursor, filters, highlight blink). Budget is law:
  FULL refreshes ONLY for tab changes, landings, badges. Everything else partial.

### Sound (WebAudio-synthesized, zero files - same as device)
- Dome thunk, shutter bleep, scan blips, ID two-note, dive sweep, find sting,
  quest fanfare, badge glockenspiel, poof (release), bonk (error). One new rule:
  FAIL STATES GET A SOFT TWO-NOTE DESCENDING TONE, never a harsh buzz - failing is
  part of exploring, not a punishment.

---

## 2. SPRITES - 1-BIT, HAND-DRAWN, NO EMOJI

Every critter, taxon icon, badge glyph, and map pin is a hand-drawn 16x16 1-bit
bitmap rendered to canvas. Same bitmap on both screens: tinted PHOS on the LCD,
INK on e-ink. This replaces every emoji in the OS (emoji are OS-dependent, they
clash with the pixel face, and they cannot dither onto a 1-bit panel).

Grid: 16x16 master, rendered nearest-neighbor at 2x/3x/4x. Silhouette-first: each
sprite must read at 16px in pure black. Detail = white knockout pixels, never outlines
thinner than 1px.

Sprite set v1: robin, cardinal, jay, sparrow, monarch, ladybug, bumblebee, maple leaf,
dandelion, squirrel. Taxon icons (8x8): bird, bug, plant, mammal. UI icons (8x8):
star, pip, pin, home, search, ear, eye, leaf, bolt, lock, check, cross.

---

## 3. SURFACE 1 - BOOT / LOADING

Cold boot (PWR slide or first press): 6.8s. Wake boot: 1.9s.

- PHASE A - MARK (0-1.5s): black screen, MK-1 bird mark draws in pixel-by-pixel
  (raster fill, left to right). Boot jingle.
- PHASE B - WORD (1.5-4.5s): "FIELD OS" pixel word + version micro-type. Progress bar
  fills in 12 steps; each step names its stage under the bar in micro-type
  (EINKD / CAMD / GPSD / BIRDNET / INAT-VISION / QWEN / QUESTS...). Soft click per step.
- PHASE C - READY (4.5-6.8s): bar completes, two-note ID chime, cut to viewfinder.
  First boot only: PHASE C becomes DEAL - three quest cards slide across the e-ink
  (full refresh) while the LCD holds "3 QUESTS DEALT".
- VERBOSE FACE (hidden): double-tap or V flips to the text POST. Same timings.

Boot fail states (each = pixel icon + one kid line + one dad line):
- BATTERY < 10%: battery glyph, "TOO SLEEPY - CHARGE ME", "UPS-HAT REPORTS <10% -
  REFUSING SCAN BOOT". Boots to e-ink-only mode (library still browsable at 0W).
- NVME MISSING: chip glyph, "MY BRAIN CARD IS MISSING", "2280 NOT DETECTED - RESEAT
  UNDER THE 4 TORX".
- E-INK HANDSHAKE FAIL: screens glyph, "MY PAPER SCREEN IS ASLEEP", "EPD5IN83 SPI
  TIMEOUT - CHECK HAT SEATING". LCD continues alone.

---

## 4. SURFACE 2 - CAMERA VIEWFINDER (LCD)

Layout (5" 800x480):
- Corner brackets, 1px PHOS, 24px arms - the frame IS the AF region.
- Top-left: mode dot + "VIEWFINDER LIVE". Top-right: "CAM0 - IMX708 - ZOOM 1.0x".
- Bottom-left micro-pips: battery (4 bars), GPS (satellite icon, solid = fix).
- Bottom-right: taxon hint when a quest is active (tiny quest icon + "QUEST").
- Center: AF box, 96px square, breathes 4px at 1Hz. Locks solid on half-press.
- D-pad U/D = digital zoom 1.0-3.0x in 0.5 steps (readout updates, 200ms ease).
- Idle: auto-sleep at 12s. At 9s the HUD fades to DIM and a "Z Z Z" drifts up the
  right edge - the only warning, no modal.
- Non-touch: a tap bonks and toasts "NO TOUCH - USE THE DECK".

Viewfinder fail states:
- TOO DARK: scene drops to 12% brightness, amber bulb icon, "TOO DARK - FIND SOME
  LIGHT". Shutter still works (flash assist fires).
- CAMERA GONE: LCD holds a static error card (camera glyph, "I CAN'T SEE",
  "CAM0 UNPLUGGED - CHECK THE RIBBON"), e-ink unaffected.

---

## 5. SURFACE 3 - BIRD LISTENING + ID (LCD)

Press LISTEN: LCD wakes straight into the listening screen (an audio scan is a scan).

- Header: pulsing dot + "LISTENING . . ." + REC timer (0.1s ticks).
- Center: live phosphor spectrogram (scrolling FFT waterfall, dithered edges) +
  26-bar waveform strip beneath it.
- Detection cue: when BirdNET fires, a cyan tick lands on the waterfall at that
  second and a soft blip plays - the kid SEES the bird get heard.
- Footer: "LISTEN = CANCEL". Sub: "BIRDNET // MIC0+MIC1 - TOP EDGE".
- Window: 3s minimum, extends to 6s while detections keep firing. ID reveal uses the
  SAME card as a visual scan (one grammar).
- E-ink mirrors support only: "LISTENING..." + static wave icon + "LIVE VIEW UP TOP".

Listening fail states:
- NOTHING HEARD (6s, no detection): ear glyph, "TOO QUIET - WAIT FOR A SONG",
  "NO BIRDNET DETECTION IN WINDOW". DOME = listen again, LISTEN = back.
- TOO WINDY: wind glyph, "TOO WINDY - SHIELD THE TOP", "DUAL-MIC REJECTION
  SATURATED". Same actions.

---

## 6. SURFACE 4 - CAPTURE UX + FAIL LADDER (LCD)

The 7 beats stay: POINT / SCAN / ID / CONFIRM / DIVE / LANDING / LIBRARY.
Confidence bar is honest: it shows the model's number, and below 60% the flow
forks instead of faking it.

- CONF 80%+: straight to ID card. CONF 60-79%: card shows a small "?" chip.
- CONF < 60% - NOT SURE card: top-2 guesses side by side (two mini-cards),
  "NOT SURE - WHICH ONE?" D-pad L/R picks, CENTER confirms, DOME = rescan,
  LISTEN = release. Kid words, real probability under each.
- BLUR / TOO WIGGLY: frame ghost-shakes, "TOO WIGGLY - HOLD STILL", one action:
  DOME retries instantly (no dead end).
- SCAN TIMEOUT (>3s inference): hourglass, "STILL THINKING...", auto-retries once,
  then offers DOME.
- ALREADY LOGGED (species in library): KEEP still works; the card stamps a
  "DUPLICATE - SIGHTING #4" ribbon instead of minting a new card number.
  Reward preserved: +1 sighting counts toward streaks.
- STORAGE FULL (>10k cards): floppy glyph, "MY BRAIN IS FULL - ASK DAD",
  "NVME 95% - ARCHIVE IN THE WEB TWIN". KEEP disabled, scan still works.

Every fail: soft descending two-note, one pixel illustration, one kid sentence,
exactly one primary action. No fail is a dead end - the dome always gets you out.

---

## 7. SURFACE 5 - THE FIELD CARD (e-ink) - POKEMON CARD MIRROR

The field card is a trading card. Mirror of the Pokemon card anatomy, 1-bit:

+----------------------------------------------------------------+
| [type icon] AMERICAN ROBIN ...................... ***.. NO.003 |  header band
|----------------------------------------------------------------|
|  +----------------------------------------------------------+  |
|  |              DITHERED ART WINDOW (real photo, Bayer-dithered 1-bit)                |  |  art window
|  |        corner-notched frame, foil zigzag if R3+          |  |
|  +----------------------------------------------------------+  |
|  THRUSH  -  BACKYARD  -  YEAR-ROUND        [region][season]    |  type band
|----------------------------------------------------------------|
|  (ruler) SIZE 23-28CM   (wing) WINGSPAN 31-41CM                |  stats rows
|  (note)  CALL "CHEERILY-CHEERUP"                               |  3 per-taxon
|----------------------------------------------------------------|
|  * FUN FACT - pulls worms from the lawn after rain. One of     |  ability box
|    the first birds back in spring.                             |  (the Pokemon
|----------------------------------------------------------------|   "attack" slot)
|  ! WATCH OUT - none. Friendly.                                 |  watch-out row
|----------------------------------------------------------------|
|  LOGGED 2026-08-27  40.73N 73.98W   [stamp]  FIELD UNIT 01     |  footer band
+----------------------------------------------------------------+

- LOGGED stamp: rotated 1-bit rubber-stamp box, top-right of the art window.
- Scroll down for more: D-pad DOWN pages the card. Page dots on the right edge:
  P1 card / P2 WHERE+WHEN (mini map + time-of-day icon) / P3 RELATED FINDS
  (3 mini-cards of same taxon) / P4 ASK ("HOLD ASK: WHAT DOES IT EAT?").
  Page turns are partial refreshes (~0.3s); leaving to the grid is a full refresh.
- The landing card (fresh find) is this exact card + highlight ring blink.

---

## 8. SURFACE 6 - FINDS LIBRARY (e-ink) - SEARCH, FILTER, SORT

- Tab strip: LIBRARY / QUESTS / MAP / BADGES (full refresh between tabs).
- Filter row: one strip of 1-bit icon chips - ALL / bird / bug / plant / mammal +
  sort chip (NEWEST / RAREST / A-Z, cycles) + count readout ("12 FINDS").
- Grid: 3-up mini field-cards (sprite, name in pixel caps, rarity pips, NEW tag on
  unviewed). Cursor = inverted block; SELECT opens the full field card.
- Search without typing: icon chips are the search. Richer queries are voice -
  footer hint: "HOLD ASK + SAY: SHOW ME RED BIRDS".
- Empty states per filter: big taxon glyph + "NO BUGS YET" + "SCAN ONE!" + dome icon.
- New-find landing: after the 5s Polaroid refresh, the new mini-card blinks its
  highlight ring with two 0.3s partials.

---

## 9. SURFACE 7 - QUESTS + BADGES + MARKS

Quests tab: one active quest card on top (name, pips as filled/empty 1-bit circles,
reward medallion preview, flavor line), then the deal queue beneath. Progress is a
SELECT over finds.db - never a stored counter.

Badge case: 3-up medallion grid. Earned = full medallion + name arc. Locked =
20% dither silhouette + "???" + unlock hint on SELECT.

MEDALLION CONSTRUCTION (all badges): 24px 1-bit coin. Outer ring, 8 notches
(gear-cut edge), 2px ring stroke, glyph centered, name arc printed beneath in
micro-type. Earned mints with a glockenspiel arpeggio + full-refresh badge card.

Badge set v1 (glyph descriptions, drawn as bitmaps):
- FIRST CONTACT - 4-point star over a horizon line       (first find)
- FIVE ALIVE    - open hand, five finger dots            (5 finds)
- FULL HOUSE    - house silhouette, 4 taxon pips inside  (all 4 taxa)
- BIRD BUDDY    - bird head, beak open singing           (quest)
- WINGFINDER    - single spread wing                     (quest)
- FINDER        - the SCAN dome itself, ringed           (quest)
- STREAK x3     - flame with 3 inner ticks               (3-day streak)
- EARLY BIRD    - rising sun over a worm                 (find before 8am)
- NIGHT OWL     - crescent moon + wide eye               (find after 8pm)
- CARTOGRAPHER  - compass rose + pin                     (finds in 5 regions)

MK-1 brand mark (already on the boot screen): pixel bird in a rounded square -
keep, it is the one allowed logo (TE-style, back of shell).

---

## 10. SURFACE 8 - MAP (e-ink) + CESIUM

On-device map (1-bit, top-down, offline tiles):
- Dithered tile backdrop (park paths, pond, tree masses read as dither textures).
- Find pins: 8x8 pin glyph + taxon mini-icon, from finds.db coords.
- Home marker (house glyph), crosshair cursor panned by D-pad (partial refreshes),
  SELECT cycles zoom 1x/2x/3x around the cursor.
- Footer: live coords "40.73N 73.98W - GPS FIX" + zoom readout + pin count.
- North tick top-right, scale bar bottom-left. Legend row: pin / home / you.

Cesium (the 3D globe) is the WEB TWIN's map, not the device's - week 5. On-device
stays 1-bit top-down because the panel cannot do shaded terrain. The map screen's
job on-device: where did I find things. Cesium's job in the twin: the globe,
regions, 3D find trails. The sim mocks the e-ink map honestly and links the twin.

---

## 11. RULES (DO / DON'T)

DO: one job per screen. 1-bit everything on e-ink. Icons first. Honest timings.
    Every fail has one way out (the dome). Kid words on top, dad words beneath.
    Full refresh = major moment only. Sprites read at 16px.
DON'T: emoji. Gray on e-ink. Menus-in-menus. Typing. Touch on the LCD.
    Shadows/blur/glassmorphism. >1 accent per screen. Modals. Punishing fails.
    Any animation on e-ink. Any logo but the MK-1 mark.
