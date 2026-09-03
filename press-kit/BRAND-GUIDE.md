# SCOUT / FIELD OS - Brand Guide (v2, Sep 2 2026: SOLARPUNK)

ONE brand system covers both devices in the family: SCOUT LITE (the pocket brick)
and SCOUT PRO (the full field unit, f.k.a. MK-1). Same marks, same palette, same
voice - the devices differ in hardware, never in identity.

A real-world Pokedex, built in public. This guide keeps every post, render, and page
looking like it came from the same field unit.

## The world: solarpunk field journal

The brand world is **painterly solarpunk**: golden-hour light, lush saturated
greens, technology nestled into nature rather than imposed on it, and soft cyan
holographic UI floating over real scenes. Think a naturalist's field journal from
a hopeful future - warm paper, botanical ink, sun.

Two zones, always:
- **The journal (brand world):** warm cream paper, deep botanical green ink,
  solar amber, holo cyan. Painterly illustration is welcome here.
- **The device (FIELD OS):** the hardware keeps its own voice - phosphor-green
  terminal on near-black LCD, and a strictly monochrome e-ink screen. The dark
  device sits inside the bright journal; that contrast is the look.

## Logos

Three marks live in `brand/` (color + monochrome each). SVG only - they scale from
favicon to billboard.

| File | Use |
|---|---|
| `logo-badge.svg` | The primary mark. A cream field patch: sun-ray tick ring, SCOUT arched over the magenta dome. Social avatars, stickers, the boot screen, the device back-shell decal. |
| `logo-icon.svg` | App icon / favicon / anywhere a square or squircle is needed. Canopy-green ground abstracting the deck: terminal screen, e-ink card, D-pad, SCAN dome. |
| `logo-wordmark.svg` | Horizontal lockup for headers, post banners, video slates. Pixel SCOUT with the O as the dome, umber FIELD OS, blinking amber cursor when viewed directly. |
| `*-mono.svg` | One-color versions. Ink is `currentColor` - the file picks up the text color of wherever it is embedded. |

### Clearspace
Give every mark breathing room equal to the SCAN dome's diameter on all sides.
Never stretch, recolor outside the palette, add effects (shadows, gradients,
outlines), or place the color versions on busy photos without a paper or canopy
scrim behind them.

### Minimum sizes
- Badge: 32 px digital / 15 mm print
- Icon: 16 px (it was designed as a favicon first)
- Wordmark: 120 px wide digital (below that, use the badge or icon)

## Color

| Name | Hex | Role |
|---|---|---|
| Canopy | `#1E4D33` | Deep botanical green. Brand ink: headlines, rings, panel bands. |
| Leaf | `#2E7D44` | Primary UI green on paper: links-on-cream, active states, progress. |
| Paper | `#F7F0DC` | The field journal page. Badge patch fill, light backgrounds. |
| Parchment | `#F2EAD6` | Page ground for the console and layouts. |
| Solar | `#E8A33D` | Golden-hour amber: sun glints, the wordmark cursor, highlights. |
| Solar Deep | `#C07A10` | Amber that survives on cream: status, warnings, prices. |
| Holo | `#45C4CE` | Cyan hologram accents - the scan arcs in illustration. Rarest. |
| Holo Deep | `#0E8A96` | Cyan that survives on cream: links, GPS/map data. |
| Dome | `#E83E8C` | One signature move. The SCAN dome, and only the dome (plus its ring). Never for text. Hardware truth: the physical button is magenta. |
| Umber | `#6B4A2F` | Warm brown shadow: secondary text on paper (FIELD OS under the wordmark). |
| FIELD OS Phosphor | `#57F7A0` | DEVICE ZONE ONLY. Terminal glow on the color LCD. |
| Console Black | `#07090D` | DEVICE ZONE ONLY. LCD/viewport backgrounds. |
| E-ink Paper | `#F4F2EC` | DEVICE ZONE ONLY. The second screen, always 1-bit. |

Rule of thumb: a frame is paper and green, with one warm pool of sunlight, exactly
one magenta thing, and cyan only where the device is sensing something.

## Typography

- **Display / labels:** Press Start 2P (Google Fonts), ALL CAPS, generous letter
  spacing. This is the FIELD OS boot-screen voice.
- **Body / data:** monospace - ui-monospace, SFMono, Menlo, Consolas. Real specs,
  real numbers, lowercase is fine here.
- Never set long paragraphs in the pixel font. It is for titles, tags, and buttons.

## Motifs

- **Sun-ray tick ring** - the badge's dial doubles as a rising sun.
- **Holo scan arcs** - thin cyan concentric arcs and reticles floating over real
  plants and animals. The visual signature of a Find.
- **Botanical line work** - fern fronds and leaf sprigs, single-weight green line.
- **Painterly golden hour** - illustration is warm, brushed, nature-dominant;
  tech sits quietly inside it.

## Voice (build-in-public)

- Terse. Technical but warm. Written by a dad building a thing for his kid, not a
  company launching a product.
- Say the real numbers: spec revisions, prices, mass, what broke. "The rev 23
  layout was not assemblable" is a better sentence than "we iterated."
- ALL CAPS is UI microcopy, not prose. Posts read like a good lab notebook.
- The device is "it," not "he/she." The kid is the naturalist; the device is the tool.
- Signature sign-off style: status-strip syntax - `W1 - BENCH BRING-UP - IN PROGRESS`.

## The story in one line

A fully offline handheld nature scanner - a real-world Pokedex - built for a
3-year-old, and a first hardware build for his dad.
