# SCOUT MK-1 marketing scenes - winning prompts

These are the exact prompts behind the shipped marketing set (scenes 1-5), plus the approved plan and drafted prompts for the new bug scene. Written for Gemini (Nano Banana-style image editing): start a fresh chat per image, attach the reference images listed for the scene, then paste the prompt as the message. Generate 1:1 and 9:16 in separate runs. If any on-screen text garbles, re-roll the whole image rather than asking for a fix.

Two shared text fragments are inlined verbatim into the prompts below. Shown once here so the pattern is clear:

- DEV (device description, in every prompt): "a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX."
- KID (scenes 1-2, no hands reference attached): "gripped with TWO clearly visible hands of a 5-year-old child - one small kid hand on the LEFT side of the device and one small kid hand on the RIGHT side, both little thumbs curled around the front edges, colorful kid jacket sleeves"
- HANDS (scenes 3-4, replaces KID; a hands reference image is attached): "HANDS ARE THE CRITICAL DETAIL: match the hands in the second reference image exactly - visibly a young child's hands, small and slender with short little fingers, held smaller in the frame, wrists mostly covered by colorful kid jacket sleeves. One small hand on each side of the device, little thumbs curled around the front edges. No veins, no adult proportions, no jewelry."

Hard constraints that apply to every scene: branding is SCOUT MK-1 / FIELD OS only, never POKEDEX. Hands must read as a 5-year-old's. GPS coordinates are always exactly "40.73N 73.98W" (the letter N, the letter W, never M or %). The SCROLL hint is a single down chevron plus the word SCROLL.

---

## Scene 1 - Scan (robin on a forest trail)

Recipe: first-person POV, sunny forest trail, American Robin ahead in soft focus. Top screen is the live viewfinder, bottom screen is the robin e-ink field card.
Attach: device reference showing the robin viewfinder + robin card (devref-scan).
Verbatim on-screen text: HUD "AF-S  1/250  ISO 400" and "40.73N 73.98W"; card title "AMERICAN ROBIN"; card header "NO.001", region "BACKYARD"; footer "FIELD UNIT 01 - CARD #001" then chevron + SCROLL. (The originally shipped card said CARD #003 - the canonical v15 UI says NO.001, use that.)

### 1:1

```
First-person POV photo: a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. gripped with TWO clearly visible hands of a 5-year-old child - one small kid hand on the LEFT side of the device and one small kid hand on the RIGHT side, both little thumbs curled around the front edges, colorful kid jacket sleeves at chest height on a sunny forest trail. Ahead in the real scene, an American Robin sits on a branch in soft focus. The device TOP screen is a live camera viewfinder showing that same robin framed with green AF brackets and small green HUD text; the BOTTOM screen is a cream e-ink field card with a big dithered bird photo, large AMERICAN ROBIN title and an icon row. Shallow depth of field, warm natural light, screens sharp and legible. Copy the screen content faithfully from the device reference, including exact footer text and the SCROLL hint.
```

### 9:16

```
First-person POV photo, vertical composition: a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. gripped with TWO clearly visible hands of a 5-year-old child - one small kid hand on the LEFT side of the device and one small kid hand on the RIGHT side, both little thumbs curled around the front edges, colorful kid jacket sleeves at chest height on a sunny forest trail. Ahead in the real scene, an American Robin sits on a branch in soft focus. The device TOP screen is a live camera viewfinder showing that same robin framed with green AF brackets and small green HUD text; the BOTTOM screen is a cream e-ink field card with a big dithered bird photo, large AMERICAN ROBIN title and an icon row. Shallow depth of field, warm natural light, screens sharp and legible. Copy the screen content faithfully from the device reference, including the SCROLL hint and the exact footer text: the GPS coordinates must read exactly "40.73N 73.98W" everywhere they appear, on both the viewfinder HUD and the e-ink footer - the letter N, the letter W, never M or %.
```

---

## Scene 2 - Listen (recording birdsong in a backyard)

Recipe: first-person POV, sunny backyard garden, late afternoon. Child is recording birdsong; top screen is the LISTENING interface, bottom screen is the robin e-ink card. Songbird on a garden fence in soft focus.
Attach: device reference showing the LISTENING screen + robin card (devref-listen).
Verbatim on-screen text: LCD "LISTENING . . ." at top, "LISTEN = CANCEL" at bottom, REC timer, BIRDNET footer; card footer coords "40.73N 73.98W". The prompt deliberately limits LCD text to two strings so the model does not invent more.

### 1:1

```
First-person POV photo: a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. gripped with TWO clearly visible hands of a 5-year-old child - one small kid hand on the LEFT side of the device and one small kid hand on the RIGHT side, both little thumbs curled around the front edges, colorful kid jacket sleeves held up at chest height in a sunny backyard garden in late afternoon. The child is recording birdsong: the device TOP screen shows a live LISTENING interface with a bright green audio waveform spectrogram, exactly as in the device reference - the only text on that screen is "LISTENING . . ." at the top and "LISTEN = CANCEL" at the bottom, nothing else; the BOTTOM screen is a cream e-ink field card with a dithered bird photo. A songbird is perched on a garden fence in soft focus in the background. Warm golden light, shallow depth of field, screens sharp and legible. Copy the screen content faithfully from the device reference. The GPS coordinates in the e-ink footer must read exactly "40.73N 73.98W" - 73.98W, never 23.96W or any other digits.
```

### 9:16

```
First-person POV photo, vertical composition: a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. gripped with TWO clearly visible hands of a 5-year-old child - one small kid hand on the LEFT side of the device and one small kid hand on the RIGHT side, both little thumbs curled around the front edges, colorful kid jacket sleeves held up at chest height in a sunny backyard garden in late afternoon. The child is recording birdsong: the device TOP screen shows a live LISTENING interface with a bright green audio waveform spectrogram, exactly as in the device reference - the only text on that screen is "LISTENING . . ." at the top and "LISTEN = CANCEL" at the bottom, nothing else; the BOTTOM screen is a cream e-ink field card with a dithered bird photo. A songbird is perched on a garden fence in soft focus in the background. Warm golden light, shallow depth of field, screens sharp and legible. Copy the screen content faithfully from the device reference. The GPS coordinates in the e-ink footer must read exactly "40.73N 73.98W" - 73.98W, never 23.96W or any other digits.
```

---

## Scene 3 - Plant ID (bracken fern on the forest floor)

Recipe: first-person POV, device held low over a shaded fern-covered forest floor, one large frond right in front of the device. Top screen is the fern viewfinder, bottom screen is the fern e-ink card.
Attach: device reference (devref-plant) + hands reference (ref-hands-bar, a crop of shipped scene 1 with the card area blurred - the blur matters; an unblurred reference leaked its robin card text into the fern card).
Verbatim on-screen text: HUD "AF-S"; card title "BRACKEN FERN"; header "NO.009" and footer "CARD #009" must agree; POISONOUS row "YES - DO NOT EAT", EDIBLE row "NO" (the shipped 1x1 said "YES - LEAVES" - the canonical v15 UI says "YES - DO NOT EAT"); region "PARK"; coords "40.73N 73.98W"; footer ends after the FIELD UNIT 01 - CARD # line, then chevron + SCROLL.

### 1:1

```
First-person POV photo: a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. held low over a shaded forest floor covered in green ferns, dappled sunlight. One large fern frond is right in front of the device in the real scene. HANDS ARE THE CRITICAL DETAIL: match the hands in the second reference image exactly - visibly a young child's hands, small and slender with short little fingers, held smaller in the frame, wrists mostly covered by colorful kid jacket sleeves. One small hand on each side of the device, little thumbs curled around the front edges. No veins, no adult proportions, no jewelry. The device TOP screen is a live camera viewfinder showing the fern frond in close-up with green AF brackets and small green HUD text reading "AF-S"; the BOTTOM screen is a cream e-ink plant field card with a big dithered fern photo and a large BRACKEN FERN title. On the card stats, the POISONOUS row reads "YES - LEAVES" and the EDIBLE row reads "NO"; the card number is NO.009 in the header and CARD #009 in the footer, matching exactly. Shallow depth of field, screens sharp and legible. Footer coords read exactly "40.73N 73.98W"; footer ends after the FIELD UNIT 01 - CARD # line; SCROLL hint is a single chevron plus the word SCROLL.
```

(For the canonical-content regen, the POISONOUS row is quoted as "YES - DO NOT EAT" instead of "YES - LEAVES", matching the vetted v15 card.)

### 9:16

```
First-person POV photo: a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. held low over a shaded forest floor covered in green ferns, dappled sunlight. One large fern frond is right in front of the device in the real scene. HANDS ARE THE CRITICAL DETAIL: match the hands in the second reference image exactly - visibly a young child's hands, small and slender with short little fingers, held smaller in the frame, wrists mostly covered by colorful kid jacket sleeves. One small hand on each side of the device, little thumbs curled around the front edges. No veins, no adult proportions, no jewelry. The device TOP screen is a live camera viewfinder showing the fern frond in close-up with green AF brackets and small green HUD text reading "AF-S"; the BOTTOM screen is a cream e-ink plant field card with a big dithered fern photo and a large BRACKEN FERN title. Shallow depth of field, screens sharp and legible. Footer coords read exactly "40.73N 73.98W"; footer ends after the FIELD UNIT 01 - CARD # line; SCROLL hint is a single chevron plus the word SCROLL. Vertical composition.
```

---

## Scene 4 - Ask (Q&A about the robin, park path)

Recipe: first-person POV, device at chest height on a sunny park path. Top screen fully OFF and black - that is deliberate, keep it. Bottom screen is the e-ink ASK chat. Amber ASK button subtly lit.
Attach: device reference with black top screen + ASK e-ink (devref-ask) + hands reference.
Verbatim on-screen text: title "ASK - AMERICAN ROBIN"; footer exactly "FIELD NOTE 01 - PALMETTO LAKE - NO CLOUD". 1:1 ships with a single exchange: Q "WHAT DOES IT EAT?" / "American Robins eat seeds, berries and bugs." 9:16 ships with exactly two short stacked exchanges: Q1 "WHERE DOES IT SLEEP?" / "Robins sleep in thick trees and shrubs, tucked close to the trunk." + Q2 "WHAT DOES IT EAT?" / "American Robins eat seeds, berries and bugs." Keep every answer to one short sentence - longer answers smudged at card scale and failed review.

### 1:1

```
First-person POV photo: a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. held at chest height on a sunny park path, trees soft in the background. HANDS ARE THE CRITICAL DETAIL: match the hands in the second reference image exactly - visibly a young child's hands, small and slender with short little fingers, held smaller in the frame, wrists mostly covered by colorful kid jacket sleeves. One small hand on each side of the device, little thumbs curled around the front edges. No veins, no adult proportions, no jewelry. The device TOP screen is fully OFF and black; the BOTTOM screen is a cream e-ink ASK screen showing a friendly follow-up Q&A chat about the animal just identified. The amber ASK button is subtly lit. Shallow depth of field, e-ink text sharp and legible. The e-ink footer must read exactly "FIELD NOTE 01 - PALMETTO LAKE - NO CLOUD".
```

### 9:16

```
First-person POV photo: a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. held at chest height on a sunny park path, trees soft in the background. HANDS ARE THE CRITICAL DETAIL: match the hands in the second reference image exactly - visibly a young child's hands, small and slender with short little fingers, held smaller in the frame, wrists mostly covered by colorful kid jacket sleeves. One small hand on each side of the device, little thumbs curled around the front edges. No veins, no adult proportions, no jewelry. The device TOP screen is fully OFF and black; the BOTTOM screen is a cream e-ink ASK screen showing a friendly follow-up Q&A chat about the animal just identified: exactly two short exchanges, each answer a single short sentence, every line fully legible with no cut-off or partial text. The amber ASK button is subtly lit. Shallow depth of field, e-ink text sharp and legible. The e-ink footer must read exactly "FIELD NOTE 01 - PALMETTO LAKE - NO CLOUD". Vertical composition.
```

---

## Scene 5 - Bedroom recap (badge case at night)

Recipe: not POV. Warm lamp-lit kid's bedroom at night, small child in pajamas sitting on a bed, holding the device in both tiny hands with screens facing camera. Top screen off and dark; bottom screen is the badge-case library screen. Dinosaur duvet, stuffed animals soft in background. No listening UI indoors.
Attach: device reference with black top screen + badge case e-ink (devref-bed). No hands reference - the child's hands are small in frame and described inline.
Verbatim on-screen text: tabs "LIBRARY QUESTS MAP BADGES" with BADGES active; footer "4 / 10 MEDALLIONS MINTED - FINISH QUESTS TO UNLOCK"; locked badges show "???".

### 1:1

```
Warm lamp-lit kid's bedroom at night. A small child in pajamas sits on a bed holding a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. in both tiny hands, screens facing camera: top screen off and dark, bottom screen a cream e-ink library screen with badge icons and quest checkmarks. Dinosaur duvet, stuffed animals soft in the background. Cozy bedtime mood, e-ink sharp and legible.
```

### 9:16

```
Warm lamp-lit kid's bedroom at night. A small child in pajamas sits on a bed holding a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. in both tiny hands, screens facing camera: top screen off and dark, bottom screen a cream e-ink library screen with badge icons and quest checkmarks. Dinosaur duvet, stuffed animals soft in the background. Cozy bedtime mood, e-ink sharp and legible. Vertical composition.
```

---

## Scene 6 - Bug (new scene, approved plan, not yet shipped)

Recipe: not POV. Low-angle shot at the kid's eye level in a sunny meadow garden: a 5-year-old crouches and points the device at a monarch butterfly resting on a flower, device front facing the camera. Top screen is the monarch viewfinder at ZOOM 2.0x, bottom screen is the monarch e-ink card.
Attach: device reference (devref-bug) + hands reference.
Verbatim on-screen text: HUD "AF-S" and "ZOOM 2.0x"; card title "MONARCH BUTTERFLY"; header "NO.003", region "PARK"; coords "40.73N 73.98W"; footer ends after the FIELD UNIT 01 - CARD # line, then chevron + SCROLL.

### 1:1

```
Low-angle photo at a crouching child's eye level in a sunny meadow garden: a small 5-year-old kid in a colorful jacket crouches down, pointing a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. at a monarch butterfly resting on a flower right in front of them, the device front facing the camera. HANDS ARE THE CRITICAL DETAIL: match the hands in the second reference image exactly - visibly a young child's hands, small and slender with short little fingers, wrists mostly covered by colorful kid jacket sleeves. One small hand on each side of the device, little thumbs curled around the front edges. No veins, no adult proportions, no jewelry. The device TOP screen is a live camera viewfinder showing the monarch in close-up with green AF brackets and small green HUD text reading "AF-S" and "ZOOM 2.0x"; the BOTTOM screen is a cream e-ink field card with a big dithered monarch photo and a large MONARCH BUTTERFLY title. Shallow depth of field, warm natural light, screens sharp and legible. Footer coords read exactly "40.73N 73.98W"; SCROLL hint is a single chevron plus the word SCROLL.
```

### 9:16

```
Low-angle photo at a crouching child's eye level in a sunny meadow garden, vertical composition: a small 5-year-old kid in a colorful jacket crouches down, pointing a tall dark translucent smoke-gray handheld device, exactly matching the device reference: TWO stacked screens on the upper half, control deck below with a magenta round SCAN dome button on the right, dark D-pad cross on the left, amber ASK and green MAP buttons along the bottom, small cyan LISTEN button at bottom-right of the dome. Branding reads SCOUT MK-1 / FIELD OS only, never POKEDEX. at a monarch butterfly resting on a flower right in front of them, the device front facing the camera. HANDS ARE THE CRITICAL DETAIL: match the hands in the second reference image exactly - visibly a young child's hands, small and slender with short little fingers, wrists mostly covered by colorful kid jacket sleeves. One small hand on each side of the device, little thumbs curled around the front edges. No veins, no adult proportions, no jewelry. The device TOP screen is a live camera viewfinder showing the monarch in close-up with green AF brackets and small green HUD text reading "AF-S" and "ZOOM 2.0x"; the BOTTOM screen is a cream e-ink field card with a big dithered monarch photo and a large MONARCH BUTTERFLY title. Shallow depth of field, warm natural light, screens sharp and legible. Footer coords read exactly "40.73N 73.98W"; SCROLL hint is a single chevron plus the word SCROLL.
```

---

## Notes from the review loop (why the guardrails exist)

- Quote every string that must survive and add a "never X" for its known garble (coords, AF-S). Unquoted UI text gets invented or smudged.
- Simplify the reference's screen text rather than letting the model render dense UI: the shipped scene 4 9x16 failed once on a smudged second answer line; single-sentence answers fixed it.
- The hands reference must have its e-ink card area blurred. An unblurred one leaked robin-card text into the fern card.
- Device proportions come from the attached device reference, not the prompt. Use the canonical v15 front render (135 x 297 x 67.8 mm, tall ~2.2:1 slab, e-ink screen larger than the LCD) as the base for every devref so all scenes agree.
