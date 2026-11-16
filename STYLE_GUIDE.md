# Style Guide

## Visual direction
**Reference:** The Knowledge Stream (youtube.com/@TheKnowledgeStream), e.g. *Garuda: The Bird Who Challenged the Gods*. It uses flat 2D vector characters with dark outlines, soft gradient skies, stylised curl-clouds, glowing gold halos and chakras, and symbolic props (the amrit kalash) as hero shots.

**Our twist, so we look related but different:** flat vector characters on top of **Indian folk-art framing**: Pattachitra / Kalamkari-style borders, motifs and textures, used for scene frames, chapter cards and transitions. That frame becomes the channel's signature.

### Rules
- **Characters:** flat colours, 2–3 shades each, 3–4 px dark outline (`#1E1420`), simple faces with large expressive eyes. Three-quarter or side view. Cut-out puppets that don't turn around (see `assets/characters/SPEC.md`).
- **Readable on a phone** (learned in the S01E01 asset review): exaggerate expressions; make open mouths big and visible through beards; every pose must be recognisable as a silhouette; nothing in a character's hand may be ambiguous.
- **Clothing and hair:** dhotis are wrapped with a front pleat, never boxy shorts. Sages wear matted jata, not turbans. Avoid any shape that could read as another religion's symbol (e.g. a cross-shaped silhouette).
- **Backgrounds:** gradient sky plus 2–3 parallax layers (far, mid, ground). No outlines on far layers.
- **Divine figures** get a gold halo or chakra element (`#E8B53A`) with a soft glow.
- **Motion:** slow parallax, gentle character "breathing" (1–2% scale), blinks, small gestures. Avoid fast or jittery motion; it should feel like a storybook.
- **Detail bar for characters** (learned from the 2026-11-15 comparison with The Knowledge Stream): the S01E01 rigs are the minimum standard, with draped dhoti folds, two or three shading tones plus highlights, jewellery and named joint groups. A plain block-shaped puppet doesn't pass. For a new character, **derive from an existing rig first** (recolour by body part, swap the face, hair and marks, add props; see `episodes/X001-*/svg/derive-cast.py`). Draw from scratch only when no body fits. Crowds and armies are existing rigs in `silhouette` light, which hides repeated faces.
- **Composition:** the subject fills 50–70% of the frame height. Use centred, temple-like tableaux for divine moments, two-shots facing each other for dialogue, and close-ups (feet, hands, a face) for story details instead of separate simplified props. No large empty sky above small figures.
- **Finish (cut-out version):** every episode sets a top-level `grade` in `03-scenes.json` (`{"grain": 0.12, "vignette": 0.45, "shadows": true}`). Each scene sets a `light` matching its background (`night`, `moon`, `dusk`, `dawn`, `fire`, `silhouette`, `divine`), which grades the characters and adds a rim light (a character or prop can override it with its own `light`, e.g. a glowing divine figure over armies in silhouette), plus ambient `fx` (`stars`, `fog`, `rays`, `glow`, `embers`, `dust`, `sparks`, `flicker`). Keep rays for reveals and divine moments only.
- **Chapter cards** (for longer pieces): roman numeral plus a serif title inside a folk-art border.

### Palette (draft, adjust after the pilot)
| Role | Hex |
|---|---|
| Night sky top | `#1B1A3A` |
| Dusk sky | `#5B3B7A` → `#E39AA0` |
| Gold / divine | `#E8B53A` |
| Saffron accent | `#E07A2E` |
| Outline | `#1E1420` |
| Parchment (cards) | `#F3E6C8` |

### Type
- Titles: a serif with character (e.g. *Cormorant Garamond* / *Tiro Devanagari Hindi* for Hindi).
- Captions: a bold sans (*Poppins* / *Hind* for Hindi), white with a dark stroke, 2–4 words on screen at a time, current word highlighted in gold.

## Format (Shorts / Reels)
- 1080×1920, 30 fps, 45–60 s.
- Keep a safe zone: nothing important in the bottom 20% or the right 12%, where platform UI covers it.
- **0–2 s hook:** a striking image plus a line that creates a question. Never open with "Long ago..." or "Today we'll learn...".
- **Change the image every 2–4 s:** a new scene, a camera move or a new element.
- **Ending:** pay off the hook, then a one-line link to the next episode ("But Yama wasn't the only god to be cursed...").

## Narration voice
- Storyteller, not lecturer. Present tense works well for drama.
- Short sentences. One idea per sentence.
- English: about 2.5 words per second. Hindi runs slightly longer; time it separately.
- Name the source on screen once, in small text (e.g. "Mahabharata, Adi Parva"). It builds trust.
