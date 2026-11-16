# Asset Brief: S01E02, The Deer Who Cursed a King

Everything this episode needs that isn't in the library yet. **Only the first two parts below need an external generator.** Claude makes the rest itself by deriving it from the existing rigs or drawing it in code, as it did for X001.

Drop deliveries into **`asset outputs/`** using the file names below, and Claude will check them, fix them up and file them.

**Reused from the library (don't make these):**
- **Characters and backgrounds:** `pandu` (drawing-bow), `dharma` (seated-throne); backgrounds `forest-hunt`, `hermitage`, `cosmic-court`, `red-sky-plain` and `parchment-card` (colour-graded in code).
- **Props, overlays and sound:** `deer`, `glowing-arrow`, `falling-light`, `folk-art-border`, `shaap-stamp`, and the whole sound kit.

## Who makes what
| Asset | Made by | Why |
|---|---|---|
| **Kunti**, **Madri** (4 poses each) | **Generator, batch 1** (after a concept round) | The channel's first women: there's no rig to derive from |
| **Kindama** (2 poses) | **Generator, batch 1** | Lying poses can't be bent out of a standing rig. Use Mandavya as the style reference |
| 3 backgrounds: `himalaya-peaks`, `spring-forest`, `amaravati-court` | **Generator, batch 2** | New places |
| Pandu: `standing-shocked`, `removing-crown`, `reaching` | Claude, from the `pandu` rig (arms re-posed at their joint pivots) | Same character, new arm positions |
| Arjuna (`standing-bow`, tease only) | Claude, from `pandu` / `barbarika` | Mid-distance in a 2 s tease. His full design comes with E03's research |
| 11 props | Claude, in code | Symbols, silhouettes and flames: simple shapes |

---

## 1. Style block: paste into EVERY prompt
> Flat 2D vector illustration for an Indian mythology storybook animation. Clean simple shapes, flat colours with 2–3 shades per material, no gradients on characters, no texture noise. Consistent dark plum outline (#1E1420), 3–4 px. Simple expressive faces: large almond eyes, small nose, gentle features. Ancient Indian clothing and ornaments, not Mughal and not modern. Respectful, dignified depiction. Palette: night #1B1A3A, dusk purple #5B3B7A to pink #E39AA0, gold #E8B53A, saffron #E07A2E, parchment #F3E6C8, deep red #8E2A20. Ornament details inspired by Pattachitra and Kalamkari folk art. Not photorealistic, not 3D, not anime, no text.

## 2. Add to every character prompt (lessons from S01E01 and X001)
> - **Exaggerated expressions:** faces are small on a phone, so push each expression about twice as far as feels natural; detailed redraws tend to soften faces, so keep them strong.
> - **Big `mouth-open`:** at least twice the size of the closed mouth, dark interior, visible through any beard.
> - **Every pose readable as a silhouette**, and different from the character's other poses.
> - **No ambiguous objects in hands:** a baby is clearly a baby in a wrapped cloth; an arrow is clearly an arrow.
> - **Keep the facing exactly as written.** A redraw can quietly turn a pose the other way.

**For the women (Kunti and Madri), also add:**
> Modest, dignified ancient Indian dress: a fitted short-sleeved bodice (kanchuka), an ankle-length draped wrap (antariya) with a front pleat, and an uttariya draped over one shoulder and across the torso. No bare midriff, no tight or revealing clothes, no glamour poses. Long black hair in a braid or a low knot. They are queens living as ascetics in the forest: real, warm, strong faces, not fashion-model faces.

## 3. Technical blocks
**Characters:**
> SVG, viewBox="0 0 1000 1600", transparent background. Centred at x=500 with feet (or the body resting on the ground) on y=1550; a standing adult's head top near y=150 and **the face centred near x=500, y=330**. Flat fills, no embedded images, no `<text>`, no filters. Named groups: `head`, `eyes-open`, `eyes-closed` (display:none), `mouth-closed`, `mouth-open` (display:none). Keep each character the same scale in every pose.

**Backgrounds:**
> SVG, viewBox="0 0 1296 2112" (a 1080×1920 portrait frame plus 108 px margin left/right and 96 px top/bottom for camera moves). No characters. Layer groups: `layer-far` (sky, distant), `layer-mid`, `layer-ground`, and `layer-front` only if something must sit in front of characters. Keep the bottom 20% simple (captions go there). Frame centre line: x=648.

**Ground lines:** canvas y = frame fraction × 1920 + 96. Each background below gives the number.

## 4. File naming
```
<character>__<pose>__<expression>.svg   kunti__holding-baby__joyful.svg
bg__<id>.svg                            bg__spring-forest.svg
```
PNG is fine too (transparent background, or flat white for Claude to remove); Claude rebuilds the named groups.

---

# BATCH 1: the cast (fixes the look)

**Concept round first for Kunti and Madri**, because they're the channel's first women: see `04-concept-brief.md`. Once a concept is picked, make a **design sheet** for each, then all of a character's poses in one session with the sheet attached.
**Style reference to attach:** an approved S01E01 character rendered to PNG, e.g. `assets/characters/pandu/drawing-bow.svg` (Pandu is their husband, so they should clearly belong in the same world).
**Facing:** draw **every pose of all three characters facing right**. Claude mirrors in code where a scene needs it.

### Kunti (`kunti`)
**From the sources:** born Pritha of the Yadavas, adopted by King Kuntibhoja (Adi §111); Pandu's elder wife. When Pandu renounced the throne, he gave **his wives' ornaments** away to Brahmanas (Adi §119), so in the forest she wears **almost no jewellery**.
**Look (design choices, noted as such):**
- A woman of about 30, composed and strong; the one the family leans on.
- Warm medium-brown skin; long black hair in a low knot.
- Cream antariya and bodice with a **deep maroon-red border** (#8E2A20).
- A plain **ochre uttariya**; one thin red thread at the wrist and a small red bindi, and no gold.
- Her colour key is **maroon**, so she reads differently from Madri at a glance.

| File | Pose / expression | Used in |
|---|---|---|
| `kunti__standing-sad__sad.svg` | Standing, three-quarter view facing right, hands loosely clasped in front, head slightly bowed; sad, worried brows | s06 |
| `kunti__folded-hands__hopeful.svg` | Standing, facing right, **palms pressed together at the chest** (namaste), eyes lifted upward; hopeful, reverent | s07 |
| `kunti__holding-baby__joyful.svg` | Standing, facing right, cradling **a baby wrapped in a cream cloth** in both arms (the baby's small face visible); radiant, joyful smile, eyes on the baby | s08 (big foreground, shown 1.15×), s09 |
| `kunti__holding-back__grieving.svg` | Standing, facing right, **both arms spread out low and wide behind her**, as if holding children back behind her; face turned right toward something terrible, grieving, mouth open in a cry | s11 |

### Madri (`madri`)
**From the sources:** princess of the Madras (Adi §124–125); Pandu's younger wife; mother of the twins Nakula and Sahadeva. **When Pandu dies, the text says she resisted him** (§125). Nothing in her design or poses may suggest she tempted him.
**Look (design choices):**
- Younger, about 22; gentle but determined.
- Slightly lighter warm skin than Kunti; long black hair in a single braid over one shoulder.
- Cream antariya and bodice with a **deep teal-green border** (#2E6B4F); a plain **saffron uttariya**.
- No gold, the same as Kunti. Her colour key is **teal**.

| File | Pose / expression | Used in |
|---|---|---|
| `madri__standing-sad__sad.svg` | Standing, facing right, one hand at her chest, head slightly bowed; sad | s06 |
| `madri__holding-twins__joyful.svg` | Standing, facing right, holding **two babies** in cream cloths, one in each arm; joyful, laughing | s09 |
| `madri__turning-away__afraid.svg` | **Body facing right, walking away**, head **turned back over her left shoulder** (looking left, back at Pandu), **her left hand raised back toward him, palm out, in a clear "stop"**; afraid, brows up, mouth open. Fully and modestly clothed; nothing romantic or suggestive in the pose | s10 |
| `madri__walking__resolute.svg` | Walking slowly, facing right, upright and calm, **palms together at the chest**; eyes forward, resolute, at peace. Shown as a dark silhouette against fire, so the **outline must read clearly**: no loose cloth trailing behind | s11 |

### Kindama (`kindama`)
**From the sources:** "a Rishi's son of great ascetic merit", a **muni who lived on fruit and roots**, who took a deer's form with his wife **out of modesty** (Adi §118). The epic gives no further description, so the look is a design choice.
**Look (design choices):**
- A **younger** sage than Mandavya, about 35, lean.
- **Black** jata (matted locks) in a top knot and a **short dark beard** (not Mandavya's long white one).
- Warm brown skin, three horizontal ash lines of tripundra on the forehead, a rudraksha mala.
- A plain ochre dhoti and **a spotted deerskin over one shoulder**, a quiet link to his deer form.
- **Large, gentle eyes** that turn fierce in the curse.

**Style reference to attach:** `assets/characters/mandavya/cursing-hand-raised.svg` as a PNG (same world, a clearly different man).

| File | Pose / expression | Used in |
|---|---|---|
| `kindama__lying-wounded__pained.svg` | **Lying on his left side on the ground**, propped up on his left elbow, head toward the **right** side of the canvas, facing right; his right hand pressed to his side, where **one small golden arrow shaft** sticks out (no blood, no wound shown). Pained, gasping, mouth open. The body rests on y=1550 and spans roughly x 150–850 | s03, s04 |
| `kindama__cursing-from-ground__furious.svg` | Same place on the ground, pushed up on his left hand, **right arm raised high, palm open, fingers spread**, toward the right; furious, eyes wide, mouth wide open mid-curse. The raised hand must read clearly in silhouette (Claude adds a saffron light burst from it) | s05 |

**→ Send batch 1 (after the concept pick); Claude reviews it before you continue.**

---

# BATCH 2: backgrounds
> Attach the approved `forest-hunt` and `hermitage` backgrounds (rendered to PNG) as style references.

| File | Description | Used in |
|---|---|---|
| `bg__himalaya-peaks.svg` | **Shatashringa, "the mountain of a hundred peaks"** (Adi §119): a sea of many sharp snowy peaks, receding in layers, under a pale dawn sky (#F3E6C8 into soft blue). Mid: a slope of deodar/pine trees and mist. Ground: a **narrow rocky path** winding up from lower-left to centre, where three tiny walkers go; path at canvas y ≈ 1632 (frame 0.80). Calm, vast, lonely. Layers far/mid/ground | s06b |
| `bg__spring-forest.svg` | **Spring in full bloom**, from the trees the text names (§125): flame-orange **palasha** flowers, red **ashoka** clusters, **mango blossom**, yellow **karnikara/champaka**, and a lotus pool at the back. Petals in the air. Soft pink-gold dusk light. A clear open meadow in the lower third for two standing figures: **feet at canvas y ≈ 1747** (frame 0.86), at canvas x ≈ 450 and x ≈ 840. Beautiful but slightly too bright, almost dreamlike. Layers far/mid/ground | s10, s10b (Claude zooms in on the ground) |
| `bg__amaravati-court.svg` | **Indra's court in Amaravati** (also needed for E03): an open celestial hall on clouds, rows of white-and-gold carved pillars (**classical ancient Indian**: carved pillars, chaitya arches, nagara spires; **no onion domes or pointed arches**), a raised stage on the right for a dancer, a gold throne far back. Night-blue sky with stars and curl-clouds. Floor: **feet at canvas y ≈ 1747** (frame 0.86). Layers far/mid/ground | s13 (E03 later) |

**→ Send batch 2 after batch 1 is approved.**

---

## Claude makes these (don't generate)
- **Pandu's poses**, derived from his rig by re-posing the arms at their joint pivots:
  - `standing-shocked`: the bow lowered, the other hand at his chest, recoiling.
  - `removing-crown`: both hands lifting the crown off.
  - `reaching`: one arm outstretched to the right.
  - His look stays as filed: "the pale one" (Adi §106).
- **Arjuna, `standing-bow`**, for the tease only: derived from `pandu`/`barbarika`, seen mid-distance. His full design comes after E03's research.
- **Props** (code-drawn SVG, 800×800):
  - `stag-wounded`: the library deer lying on its side, eyes open, one small golden arrow.
  - `mantra-ring`: a ring of glowing abstract script, not readable words.
  - `wind-swirl` (Vayu), `vajra-flash` (Indra's thunderbolt), `twin-stars` (the Ashvins).
  - `fallen-crown`: Pandu's own crown, lifted from his rig, lying in the grass with petals.
  - `pyre-flames`: folk-art stylised flames on a log base, no body.
  - Silhouettes: `three-pilgrims-silhouette`, `young-pandavas-group` (five boys of different heights), `five-sons-silhouette` (five grown men in a row, glowing rims), `apsara-silhouette` (a dancer in a graceful classical pose; modest, for E03).
- **Effects:** the light burst, the stamps, the name tags, the law-inscription card, captions and all colour grading.

## Checklist
- [x] Concept round: Kunti + Madri, made by Claude from the pandu rig; **C picked** (Kunti veiled, Madri with sash + braid), see `04-concept-brief.md` → Decisions
- [x] Kunti ×4 and Madri ×4 poses: **made by Claude** from concept C (`svg/make-women.py`), filed 2026-11-16, checked in the scene stills
- [x] Kindama ×2: **made by Claude** from the mandavya rig, laid down by rotating lower and upper body about the hip (`svg/make-kindama.py`), 2026-11-16
- [x] 3 backgrounds: **made by Claude** in code (`svg/make-backgrounds.py`), 2026-11-16; ground lines added to `assets/backgrounds/GROUND_LINES.md`
- [x] Claude-made (2026-11-16): Pandu ×3 poses, Arjuna ×1 (placeholder), 11 props, all filed. Scripts: `svg/derive-cast.py`, `svg/make-props.py`. Design change: `removing-crown` shows the crown **held at his chest** (his arms are too short to lift it off cleanly without crossing his face)
- [x] All filed into the library with `character.json` (`appearsIn: S01E02`); every scene checked in stills. **No external generator was needed for this episode.**
