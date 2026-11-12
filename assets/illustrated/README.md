# Illustrated asset library

Reference sheets for the **illustrated** version of our Shorts (painted stills plus camera moves, see `episodes/<ID>/illustrated/03-shots.json`). It's the counterpart of the SVG puppet library in `assets/characters/`: same IDs, a different style.

A sheet here is a **reference, not a puppet**. Every shot is painted anew by the image model with the sheet attached, so the sheet keeps the face, costume and style consistent across shots and across episodes.

**Style:** `styles/ink-wash-graphic-novel.md`. Every sheet in this library is in that style. If we ever add a second style, it gets its own sheet files (`sheet.<style>.png`) under the same IDs.

## Layout
```
assets/illustrated/
  characters/<id>/
    sheet.png                 approved model sheet (16:9): full body front + three-quarter + 3 expression heads
    sheet-facing-left.png     (optional) mirrored copy when the model keeps drawing one direction
    sheet.<variant>.png       (optional) age or story variants: sheet.young.png, sheet.old.png
    character.md              design lock, generation record, Higgsfield IDs, history
  locations/<id>/
    sheet.png                 approved empty location plate (9:16), no characters
    location.md               same record as a character
```
`<id>` is the same kebab-case ID as in `assets/characters/` (e.g. `dharma`, `young-mandavya`) so both libraries stay linked.

## Rules
1. **Reuse before you create.** Check here before writing a sheet prompt. A recurring character or place needs a sheet; a one-shot place can be prompt-only.
2. **Design lock.** `character.md` lists what must never change (e.g. Dharma's crown, tilak, halo). Every shot prompt copies that list.
3. **Every shot attaches the sheets** of the characters and the location in it. On Higgsfield, pass the sheet's **media or job ID** from `character.md` as an `image_references` input; there's no need to upload it again.
4. **Facing:** judge it zoomed in with the ear rule (the visible ear is the back of the head). If a sheet faces the wrong way, mirror it (free) instead of regenerating, as long as the design is symmetrical (crown, tilak, jewellery).
5. **Approval:** a sheet enters the library only after the user approves it. Rejected tries stay in the episode's `illustrated/images/refs/`.
6. **Variants:** an age or story change (young Vidura, Pandu after the curse) is a new variant sheet under the same ID, not a new character.

## Generating a sheet (Higgsfield, Nano Banana 2.1)
- **Character:** 16:9, 1k, thinking high. References: the SVG sheet (`assets/characters/<id>/sheet.svg` rendered to PNG) for the design, plus an approved ink-wash sheet (e.g. Mandavya's) for the style. Prompt: design lock, then "Image 1 = design, Image 2 = style", the layout (front, three-quarter, 3 heads), then the style block from the style guide.
- **Location:** 9:16, 1k, empty, no people, with the composition the shots need (where the throne is, where characters stand, the bottom 20% clear).
- Cost on 2026-11-07: 1.5 credits at 1k, 2 at 2k, 3 at 4k.

## Index
| ID | Type | Sheet | First approved | Used in |
|---|---|---|---|---|
| mandavya | character | sheet.png | S01E01 (2026-11-07) | S01E01 |
| dharma | character | sheet.png, sheet-facing-left.png | S01E01 (2026-11-07) | S01E01 |
| king | character | sheet.png | S01E01 (2026-11-08) | S01E01 |
| guard | character | sheet.png | S01E01 (2026-11-08) | S01E01 |
| thief | character | sheet.png (two thieves) | S01E01 (2026-11-08) | S01E01 |
| cosmic-court | location | sheet.png | S01E01 (2026-11-07) | S01E01 |
| hermitage | location | sheet.png | S01E01 (2026-11-07) | S01E01 |
| stake-hill | location | sheet.png | S01E01 (2026-11-07) | S01E01 |
| barbarika | character | sheet.png | X001 (2026-11-12) | X001 |
| brahmin-krishna | character | sheet.png, sheet-facing-left.png | X001 (2026-11-12) | X001 |
| peepal-night | location | sheet.png | X001 (2026-11-12) | X001 |
