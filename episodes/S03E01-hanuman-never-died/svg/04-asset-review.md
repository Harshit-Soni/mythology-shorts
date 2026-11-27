# Asset review: S03E01

Everything was made in code by Claude (SVG-first): `make-cast.py`, `make-backgrounds.py` and `make-props.py` in this folder, in the looks picked at the concept check (`04-concept-brief.md`: Hanuman A, Rama A). Nothing was delivered by an outside generator, so there's no untrusted file to vet.

## Checked (2026-11-27)
- **All 24 character files** were rendered on one sheet, the heads zoomed. The Hanuman muzzle reads as a vanara face, not a mask. The calm, devoted, moved (eyes closed, smile) and talking mouths all work. Rama reads as Rama, not Krishna, side by side.
- **Placeholder-free stills** (`render/stills-en`, all 30 shots). These were fixed after the first pass:
  - **Kneeling and seated close-ups** (s08, s08b, s12c) had their faces in the caption zone. They were lifted (y 0.74–0.80).
  - **The babies read too small** in s02, s03c and s05. They were scaled up.
  - **The necklace prop was hidden** behind Hanuman in s09c. It's now part of a pose, `hanuman/standing__necklace`.
  - **Vayu's child hung at his waist.** It's now cradled across his chest, and the shot is lifted clear of the captions.
- **Facing:** every pose faces right. Hanuman is always on the left facing right and Rama on the right, flipped. Indra is flipped to throw leftward, at the child.
- **Dignity:** no cartoon snout or grin. The fall is a tumble with eyes shut, with no wound shown, and Rama's departure is in white light.

## Known limits (fine at this size, worth knowing)
- Seated poses use the library's cross-legged lap, which is a broad shape at close range (s12c, s08b).
- Vayu's child is a small copy of the baby figure, so it has no blink or talk swaps. It doesn't need them: the child is unconscious.
- `katha-circle` borrows library poses as silhouettes (the sage Shamika and Kunti), so the listeners match the cast's style.
