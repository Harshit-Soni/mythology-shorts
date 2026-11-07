# Asset Brief: S01E01, The Sage Who Put Dharma on Trial

Everything needed to get this episode's assets made outside this project. Generate the assets, drop the files into **`assets/_inbox/`** using the file names below, and Claude will check them, fix them up and add them to the library.

**Work in batches. Send batch 1 first.** It sets the look for the whole channel, so there's no point making the other assets until it's right.

---

## How to generate SVGs (pick what works)

| Route | Good for | Notes |
|---|---|---|
| **A. A native vector generator** (e.g. Recraft) | Characters, backgrounds, overlays | Real SVG illustration output and a style-consistency feature. Probably the best fit |
| **B. GPT / Gemini image → PNG → vectorise** (vectorizer.ai, Illustrator Image Trace, or send the PNG and Claude traces it) | Characters, backgrounds | Best-looking art. Named groups are lost, but Claude can rebuild them |
| **C. Ask GPT / Gemini chat to write SVG code** | Props, stamps, borders | Named groups are easy, but the art comes out simpler. Fine for simple shapes |
| **Plain PNG (no SVG at all)** | Anything | Also acceptable: Remotion can use PNGs. Use a transparent background, or plain flat white for Claude to remove |

If a route can't produce the **named groups** below, deliver the file anyway and Claude will add them.

---

## 1. Style block: paste into EVERY prompt

> Flat 2D vector illustration for an Indian mythology storybook animation. Clean simple shapes, flat colours with 2–3 shades per material, no gradients on characters, no texture noise. Consistent dark plum outline (#1E1420), 3–4 px. Simple expressive faces: large almond eyes, small nose, gentle features. Ancient Indian clothing and ornaments (dhoti, uttariya, angavastram, gold jewellery, rudraksha), not Mughal and not modern. Respectful, dignified depiction. Palette: night #1B1A3A, dusk purple #5B3B7A to pink #E39AA0, gold #E8B53A, saffron #E07A2E, parchment #F3E6C8, deep red #8E2A20. Ornament details inspired by Pattachitra and Kalamkari folk art. Not photorealistic, not 3D, not anime, no text.

## 2. Technical block: paste for SVG output

**Characters:**
> SVG, viewBox="0 0 1000 1600", transparent background. Character centred at x=500 with feet or base on y=1550; standing adult's head top near y=150. Flat fills, no embedded images, no <text>, no filters. Name the groups: `head`, `eyes-open`, `eyes-closed` (display:none), `mouth-closed`, `mouth-open` (display:none). Divine characters also get `halo` behind the head.

**Backgrounds:**
> SVG, viewBox="0 0 1296 2112" (a 1080×1920 portrait frame plus extra margin on every side for camera moves). No characters. Separate the layers into groups: `layer-far` (sky, distant), `layer-mid`, `layer-ground`, and `layer-front` if anything should sit in front of characters. Keep the bottom 20% simple, because captions go there.

**Props:**
> SVG, viewBox="0 0 800 800" (or the size given below), transparent background, object centred, no ground shadow.

## 3. File naming
```
<character>__<pose>.svg                 mandavya__walking.svg
<character>__<pose>__<expression>.svg   dharma__seated-throne__stern.svg
bg__<id>.svg                            bg__cosmic-court.svg
prop__<id>.svg                          prop__scales-of-justice.svg
overlay__<id>.svg                       overlay__folk-art-border.svg
```

## 4. Consistency tips
- Make a **design sheet first** for each character (front and three-quarter view, all on one canvas). After approving it, attach it as a reference image for every pose.
- Generate all the poses for one character in a **single session**.
- Expressions: for "same pose, different face", ask the tool to **edit the approved image and change only the face**.
- Direction: draw Mandavya **facing right**, and Dharma **facing front, turned slightly to his left (toward the viewer's left)**. Claude can mirror anything in code.

---

# BATCH 1: lock the look (make these first)

### Dharma: god of justice (`dharma`)
**Look:** regal, calm, middle-aged; warm golden-brown skin (#B9814F); white and cream garments (#F3EEDF) with gold borders; tall gold crown; gold armlets and necklace; a large gold **halo disc** behind his head with Pattachitra petal rays (group `halo`). Serene, wise, slightly stern.
⚠️ **Not Yama:** no buffalo, no noose, no dark-blue skin, no fangs. He should read as *justice*, not *death*.

| File | Pose / expression |
|---|---|
| `dharma__seated-throne__neutral.svg` | Seated cross-legged or one leg down, upright, hands resting on his knees, as if on a throne (**no throne**; it's in the background). Calm face |
| `dharma__seated-throne__stern.svg` | Same image, only the face changed: brows down, firm mouth |
| `dharma__seated-throne__shocked.svg` | Same image, only the face changed: eyes wide, brows up, mouth slightly open |

### Mandavya: the sage (`mandavya`)
**Look:** lean ascetic sage, about 50; long matted hair (jata) tied in a top knot; long beard with grey streaks; bare chest with a sacred thread; ochre or saffron dhoti (#E07A2E / #C4622A); rudraksha beads; three horizontal ash lines (tripundra) on his forehead. Dignified, intense eyes.

| File | Pose / expression | Used in |
|---|---|---|
| `mandavya__meditating-arms-raised.svg` | Sitting cross-legged, **both arms raised straight up**, eyes closed, peaceful (front view) | s02–s04 |
| `mandavya__standing-bound.svg` | Standing, wrists tied in front with rope, head slightly down, eyes closed, calm | s05 |
| `mandavya__on-stake-silhouette.svg` | **Solid silhouette only** (all #1E1420, no details): a small figure sitting in meditation **on top of a tall thin pole**, seen from far away. Traditional depiction, not graphic. viewBox 0 0 1000 1600, pole from y=500 down to 1550 | s07 |
| `mandavya__standing-calm.svg` | Standing upright, hands relaxed, gentle forgiving face | s08 |
| `mandavya__walking.svg` | Side view, walking right, purposeful stride, determined face | s09 |
| `mandavya__standing-confront.svg` | Three-quarter view facing right, one foot forward, chin up, **defiant** face | s10 |
| `mandavya__cursing-hand-raised.svg` | Facing right, right arm thrust forward and up with palm open toward the viewer's right, **furious** face, hair and cloth slightly swept back | s13 |

### Background: Dharma's court (`bg__cosmic-court.svg`)
The court of the god of justice in the heavens. Deep night-purple sky (#1B1A3A → #5B3B7A) with small stars and stylised curl-clouds. A **golden throne on a raised platform** in the upper-middle (the seat at about y=1000 in the 2112-tall canvas). **Glowing stone steps** rise from the bottom-centre up to the throne (Mandavya climbs these). Tall ornate pillars at the left and right edges. Layers: `layer-far` (sky, stars), `layer-mid` (clouds, pillars), `layer-ground` (platform, throne, steps).

**→ Send batch 1 and Claude will review it before you continue.**

---

# BATCH 2: remaining characters

> **Lessons from batch 1: add these lines to the prompt for every batch 2 character.**
> - **Dhoti, not shorts:** a wrapped dhoti with a visible front pleat (kachha), soft folds, mid-calf or knee-length. Never boxy shorts.
> - **Exaggerated expressions:** the face is small on a phone, so push angry, shocked and ashamed faces about twice as far as feels natural (strongly angled brows, eyes wide with the whites showing).
> - **Big `mouth-open`:** at least twice the size of the closed mouth, with a dark interior. With a beard or moustache, it must still clearly show through.
> - **Every pose readable as a silhouette:** filled in solid black, each pose must still be recognisable and different from the character's other poses.
> - **No ambiguous objects in hands:** anything held must be obviously what it is (rope, spear, bow). Loose cloth shouldn't look like a blade.
> - **Hair:** turbans only where the brief says turban (guard). Sages and boys have their own hair.

### Young Mandavya (`young-mandavya`)
A boy of about 7 with the same face shape as adult Mandavya (big eyes, same brow), a small tuft of hair (shikha) on an otherwise short-cropped head, a simple ochre **wrapped dhoti** (see lessons above), bare-chested. If Mandavya's design changes in the batch 1 redos, match this boy to the new version.
| File | Pose |
|---|---|
| `young-mandavya__crouching-playing.svg` | Crouching, curious, one hand held out low in a **pinching pose** (the grass blade is a separate prop). Innocent, not cruel |

### King (`king`)
A regional king: gold crown, thick moustache, red and green garments (#8E2A20 / #2E6B4F), gold jewellery, stern presence.
| File | Pose |
|---|---|
| `king__seated-throne-pointing.svg` | Seated (no throne), right arm pointing forward and down at someone, angry |
| `king__folded-hands.svg` | Standing, palms pressed together (namaste), head bowed, ashamed |

### Guard (`guard`)
A royal soldier: turban, simple armour vest, dhoti, waist sash, spear.
| File | Pose |
|---|---|
| `guard__pointing.svg` | Standing, facing left, pointing with the free hand, mouth open shouting, spear in the other hand |
| `guard__dragging.svg` | Walking left, pulling a rope that goes off to the right, angry |
| `guard__pulling.svg` | Leaning back, both hands gripping something at chest height (no object drawn), straining face |

### Thief (`thief`)
A lean man, cloth tied over his head, a rough short dhoti, a shifty look. Make **one colour version**; Claude recolours the second.
| File | Pose |
|---|---|
| `thief__running.svg` | Running left, looking back over his shoulder, scared, a cloth sack slung on his back |
| `thief__captured.svg` | Standing, wrists tied, head hung down |

### Vidura (`vidura`)
An adult man of about 35, calm and wise: plain white or cream clothes with a thin gold border (a minister, **not a king**, so no crown), short neat beard, sandalwood tilak, a gentle, intelligent face.
| File | Pose |
|---|---|
| `vidura__standing-hands-clasped.svg` | Front view, hands clasped in front, serene |

### Pandu (`pandu`), tease shot only
A prince with a **noticeably pale complexion** (his name means "the pale one", Adi Parva §106), crown, archer's garments.
| File | Pose |
|---|---|
| `pandu__drawing-bow.svg` | Side view facing right, drawing a longbow at full draw, focused. Bow included |

---

# BATCH 3: backgrounds, props, overlays

> **Concept targets (approved 2026-11-07, see `04-concept-brief.md` → Decisions).** For the king's court, the palace and the border, attach the chosen concept PNG from `review/concepts/` as the visual target and apply the listed changes. The concepts are 2:3; the SVGs are wider canvases cropped to 9:16, so keep the important elements inside the central 84% of the width.

### Backgrounds (viewBox 0 0 1296 2112, layered as in §2)
| File | Description |
|---|---|
| `bg__hermitage.svg` | Forest hermitage at dawn: a large peepal tree on the left with an open spot beneath it (where the sage sits), a thatched hut on the right as a **separate group `layer-front`** (thieves hide behind it), a clearing, and a soft dawn sky (#E39AA0 → #F3E6C8). Claude makes the night version in code |
| `bg__king-court.svg` | **Target: `review/concepts/concept__court__a.png`.** Keep the pot-and-foliage pillar capitals, lion figures, oil lamps, garlands and the stepped platform. **Changes:** walls and drapes a darker brown-maroon (wood tones) so the king's red clothes stand out; **throne cushion deep green or cream, not red** (the king sits on it). The throne seat must be empty, at about the vertical middle. Claude adds the darker "sentencing" mood with colour grading in code |
| `bg__red-sky-plain.svg` | Barren flat plain, low horizon at about y=1350, huge dramatic red-orange sky, distant low hills. Keep the **sky as its own group** so Claude can recolour it for night and dawn |
| `bg__flashback-meadow.svg` | Soft, simple grassy meadow with a few wildflowers and gentle light. Claude adds the sepia tone |
| `bg__hastinapura-palace.svg` | **Target: `review/concepts/concept__palace__a.png`** (warm gold morning). Keep the composition, open sky in the top third, the empty courtyard floor, the curved torana crossbars, rectangular doors and lotus capitals. **Change: the spires** are too round, like domes. Make them **taller and narrower curved temple towers** (nagara shikhara) with vertical ribs tapering to a flat amalaka disc and a kalash on top. Separate layers: sky / spires / main hall / side pavilions / floor |
| `bg__forest-hunt.svg` | Dense forest clearing, dappled light, open space on the right for a deer |
| `bg__parchment-card.svg` | Aged parchment (#F3E6C8) with slightly darker, burnt-looking edges and faint speckles. No text |

### Props (viewBox 0 0 800 800 unless stated)
| File | Description |
|---|---|
| `prop__scales-of-justice.svg` | Ornate gold Indian-style balance scale. **Groups: `beam`, `pan-l`, `pan-r`, `stand`**, so they can tip |
| `prop__loot-sack.svg` | Tied cloth bundle with a few gold coins peeking out |
| `prop__coins.svg` | 6–8 old gold coins, each its own group |
| `prop__torch.svg` | Wooden mashaal torch; flame as its own group `flame` |
| `prop__leaf.svg` | A single peepal leaf |
| `prop__stake.svg` | viewBox 0 0 400 1600: a tall, plain dark wooden pole tapering to a point at the top. Simple and not gory |
| `prop__vultures.svg` | 3 vultures in flight as dark silhouettes, each its own group |
| `prop__grass-blade.svg` | A single long, thin grass blade, slightly curved |
| `prop__insect.svg` | A tiny beetle-like insect, simple and slightly cute (not gross) |
| `prop__deer.svg` | Spotted deer (chital), grazing, side view facing left |
| `prop__seal-stamp.svg` | Round wax-seal shape with an ornamental rim, **no text**, deep red |

### Overlays (viewBox 0 0 1080 1920, transparent centre)
| File | Description |
|---|---|
| `overlay__folk-art-border.svg` | **Target: `review/concepts/concept__border__a.png`** (classic Pattachitra flowers and creepers), **made thinner, about 8% of the width (≈86 px)**, the proportion of `concept__border__b.png`. Keep the cream flowers, gold creeper, dotted gold line and saffron inner edge. **4 lotus corner medallions as separate groups** `corner-tl`, `corner-tr`, `corner-bl`, `corner-br` (they animate), plus `band-top`, `band-bottom`, `band-left`, `band-right`. **The centre is fully transparent.** Flat colours, no texture |
| `overlay__sepia-folk-frame.svg` | A thinner border with an **arched (temple-door) window** in the centre, in sepia and brown tones, for flashbacks |
| `overlay__shaap-stamp.svg` | viewBox 0 0 800 800: a rough-edged circular rubber-stamp shape in gold (#E8B53A) with an ornamental inner ring, **no text** (Claude adds शाप / CURSED in code) |

---

## Claude makes these in code (don't generate them)
Split-frame layout, falling light beam, stake-tip glint, halo crack, saffron light burst, coin scatter, leaf fall, all on-screen text (stamps, name tags, the law inscription, captions), and the night and sepia colour grading.

## Checklist
- [x] Batch 1: dharma ×3, mandavya ×7, bg__cosmic-court (received 2026-11-07, see 04-asset-review.md)
- [x] Batch 1 reviewed: style approved
- [x] Batch 1 redos (v2, 2026-11-07): approved and filed to the library. Dharma shocked face fixed by Claude
- [x] Batch 2: young-mandavya, king ×2, guard ×3, thief ×2, vidura, pandu (approved and filed 2026-11-07; Dharma shocked fixed by Claude)
- [x] Batch 3: 7 backgrounds, 11 props, 3 overlays (approved and filed 2026-11-07)
- [ ] Redo: prop__vultures (reads as bats; see 04-asset-review.md)
