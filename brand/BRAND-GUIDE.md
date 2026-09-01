# SCOUT / FIELD OS - Brand Guide

ONE brand system covers both devices in the family: SCOUT LITE (the pocket brick)
and SCOUT PRO (the full field unit, f.k.a. MK-1). Same marks, same palette, same
voice - the devices differ in hardware, never in identity.

A real-world Pokedex, built in public. This guide keeps every post, render, and page
looking like it came from the same field unit.

## Logos

Three marks live in `brand/` (color + monochrome each). SVG only - they scale from
favicon to billboard.

| File | Use |
|---|---|
| `logo-badge.svg` | The primary mark. Circular field badge - social avatars, stickers, the "patch." |
| `logo-icon.svg` | App icon / favicon / anywhere a square or squircle is needed. Abstracts the deck: terminal screen, e-ink card, D-pad, SCAN dome. |
| `logo-wordmark.svg` | Horizontal lockup for headers, post banners, video slates. The O is the SCAN dome. The cursor block blinks when the SVG is viewed directly. |
| `*-mono.svg` | One-color versions. Ink is `currentColor` - the file picks up the text color of wherever it is embedded (defaults to black). On the console's dark background, set `color: #57f7a0`. |

### Clearspace
Give every mark breathing room equal to the SCAN dome's diameter on all sides.
Never stretch, recolor outside the palette, add effects (shadows, gradients,
outlines), or place the color versions on busy photos without a dark scrim.

### Minimum sizes
- Badge: 32 px digital / 15 mm print
- Icon: 16 px (it was designed as a favicon first)
- Wordmark: 120 px wide digital (below that, use the badge or icon)

## Color

| Name | Hex | Role |
|---|---|---|
| Phosphor Green | `#57f7a0` | Primary. Terminal glow, strokes, headlines on dark. |
| SCAN Magenta | `#ff3d9a` | One signature move. The dome, and only the dome (plus its ring). Never for text. |
| Console Black | `#07090d` | Backgrounds. |
| Panel | `#0c1017` | Cards, icon ground. |
| Ink | `#c8d6e5` | Body text on dark. |
| Dim | `#5f7386` | Captions, metadata, inactive UI. |
| Amber | `#ffc857` | Status, warnings, "in progress," the status LED. Use sparingly. |
| E-ink Paper | `#e9e4d6` | The second screen. Light backgrounds when a light theme is unavoidable. |
| Signal Cyan | `#2ee6e6` | Accents: links, GPS/map data. Rarest of all. |

Rule of thumb: a frame is green and black, with exactly one magenta thing in it.

## Typography

- **Display / labels:** Press Start 2P (Google Fonts), ALL CAPS, generous letter
  spacing. This is the FIELD OS boot-screen voice.
- **Body / data:** monospace - ui-monospace, SFMono, Menlo, Consolas. Real specs,
  real numbers, lowercase is fine here.
- Never set long paragraphs in the pixel font. It is for titles, tags, and buttons.

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
