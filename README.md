# SCOUT MK-1 // FIELD OS

A real-world Pokedex: a fully offline handheld nature scanner built for a 3-year-old (and a first hardware build for his dad). Point it at a plant, bug, bird, or animal and it identifies it on-device. Listen to birdsong and it names the bird. Ask it questions about what you just found. Every "Find" gets pinned on an offline CesiumJS map. No cloud, no account, no subscription.

**Try the simulator + build console:** open `index.html` (served live via GitHub Pages at the repo's Pages URL). It is a single self-contained file holding the FIELD OS simulator, the interactive 3D CAD viewer, the parts checklist with buy links, the 7-week build plan, per-step newbie guides, and copy-ready LLM prompts.

## Repo layout

- `index.html` - SCOUT Build Console v16 (FIELD OS simulator, dashboard, CAD viewer, build plan). Served at the Pages root.
- `docs/field-os-design-doc.md` - FIELD OS 1.0 UX design system (rev 11): one job per screen, tokens, screen specs.
- `docs/scout-mk1-winning-prompts.md` - the exact prompts behind the shipped marketing render set.

## Hardware (spec)

Raspberry Pi 5 + NVMe, 5" color touch LCD (viewfinder) + 5.83" B/W e-ink (card/library), dual mics, Beitian BN-880 GPS, 4x 21700 cells, 3D-printed translucent smoked-PETG shell, 60mm SCAN dome. BOM ~$375. Software: iNaturalist vision model, BirdNET, small local LLM, offline CesiumJS tiles.

Built in public. Named SCOUT MK-1, running FIELD OS. Saved items are "Finds."
