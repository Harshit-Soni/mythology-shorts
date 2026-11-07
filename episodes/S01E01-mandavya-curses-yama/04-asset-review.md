# Asset Review: S01E01

## Batch 1 (received 2026-11-07, `asset outputs/S01E01-batch-1.zip`)
**Technical check: all 11 pass.** Correct canvas sizes, all required groups present, no scripts, embedded images, external links or text. Blink and talk swaps tested and working. Renders are in `review/`.

**Overall: the style is approved.** The line weight, palette, ornament, halo and court composition match the style guide well. Dharma clearly reads as *justice*, not Yama.

### Redo (3)
| File | Problem | Fix to ask for |
|---|---|---|
| `mandavya__on-stake-silhouette` | Reads as a **cross or grave marker**, not a meditating figure. The religious connotation is wrong for this channel | A clear seated meditation silhouette (head, top knot, shoulders, crossed legs wider than the shoulders) sitting on a **thinner pole**. No horizontal crossbar shape. At thumbnail size it must read as "a person sitting on a pole" |
| `mandavya__cursing-hand-raised` | The orange cloth in his left hand looks like a **blade**, and the raised hand looks like a **wave** ("hi"), not a curse | Remove the cloth (or let it hang loosely from the shoulder). Right arm thrust **forward toward the viewer's right**, palm out and fingers spread; the left hand clenched at his side. Leaning forward, mouth open shouting |
| `mandavya__standing-confront` | Almost identical to `standing-calm`; only the eyes differ | Body language: one foot forward, chest out, chin up, fists at his sides, turned three-quarters toward the right. It should read as defiant even in silhouette |

### Improve (optional, but cheap to do now)
| File(s) | Note |
|---|---|
| `dharma__…__stern`, `__shocked` | Expressions are too subtle at the size Dharma appears on screen (about 45% scale). **Stern:** brows sharply angled down and a deeper frown. **Shocked:** eyes much wider, with the whites showing all around |
| Mandavya `mouth-open` (all poses) | Too small inside the beard, so speech won't be visible. Make the open mouth about 2× bigger, with a dark interior |
| Mandavya dhoti (all poses) | Reads as **boxy shorts**. Use a wrapped dhoti with a visible front pleat, a little longer (mid-calf) |
| Mandavya hair | The top knot looks like a **turban**. Show it as coiled, matted locks (jata) with a few loose strands |

### Approved as-is
`dharma__seated-throne__neutral`, `mandavya__meditating-arms-raised`, `mandavya__standing-bound`, `mandavya__standing-calm`, `mandavya__walking`, `bg__cosmic-court`.
(If the Mandavya dhoti and hair changes are made, redo his approved poses too, so all of them match.)

### Notes for Claude (placement, not art)
- In the court, Mandavya at scale 0.5 looks larger than the god behind him. In s09/s10, place him lower on the steps at about 0.42 scale.
- The court's steps run into the bottom 20% (caption zone). That's fine because they're plain, but keep characters' faces above it.

---

## Batch 1 v2 (received 2026-11-07, `asset outputs/S01E01-batch-1-v2.zip`)
**Technical check: all 11 pass** (same safety and structure checks as v1). Renders in `review/batch1v2-*.png`.

| Item | Result |
|---|---|
| On-stake silhouette | ✅ **Fixed.** Now clearly a seated meditating figure on a thin pole; nothing cross-like |
| Cursing pose | ✅ **Fixed.** The cloth is gone; forward thrust, open palm, clenched left fist, shouting |
| Confront pose | ✅ **Fixed.** Wide stance, fists, chin up; distinct from calm, even as a silhouette |
| Mandavya open mouth | ✅ **Fixed.** Big, dark, with teeth; clearly visible through the beard. Blink and talk swaps tested on 3 poses |
| Dhoti | ✅ **Fixed.** Long wrapped dhoti with front pleats in every pose |
| Hair | ✅ **Fixed.** Coiled jata with loose strands, no longer a turban |
| Dharma stern | ✅ **Fixed.** Clearly angled brows and frown at on-screen size |
| Dharma shocked | ⚠️ **Too comic.** The eyes became perfectly round with tiny pupils ("googly eyes"), which reads as cartoon slapstick and undercuts the climax (s13) and the respect rule. **Ask for:** keep the almond eye shape, just open it wider (whites visible above the iris), brows raised high, mouth open in a tense oval. Shocked, not silly |

**Status:** filed to the library (`assets/characters/dharma/`, `assets/characters/mandavya/`, `assets/backgrounds/cosmic-court.svg`) with `character.json` for both. `seated-throne__shocked.svg` stays in use as a placeholder until the fix arrives; send it with batch 2.

**Minor, no action needed:** the standing-bound and standing-calm silhouettes are similar, but they appear in different scenes, so that's fine.

---

## Dharma shocked: fixed by Claude (2026-11-07)
Replaced only the `eyes-open`, `brows` and `mouth-open` groups in `assets/characters/dharma/seated-throne__shocked.svg`. The eyes keep Dharma's almond shape, opened wider, with the pupils dropped so white shows above them, plus an upper-lid crease. The brows are raised and arched with tension at the inner ends. The mouth is a smaller, tense oval with a dark-red interior and a teeth line, so it no longer merges into the beard. The body, halo and other groups are untouched, and the file passes all checks. Before/after: `review/dharma-shocked-fix.png`. Original kept at `review/dharma-shocked-v2-original.svg`.

## Batch 2 (received 2026-11-07, `asset outputs/S01E01-batch-2 2/`)
**Technical check: all 10 pass.** Rendered next to the library's Mandavya and Dharma: same line weight, palette and proportions. Blink and talk tested on the king, guard, Vidura and young Mandavya; all work, and the open mouths are clearly visible. Every pose is distinct as a silhouette. Renders in `review/batch2-*.png`.

| Character | Result |
|---|---|
| Young Mandavya | ✅ Reads as a curious, innocent child; matches the adult's face shape; wrapped dhoti; pinching hand low and to the right |
| King ×2 | ✅ Seated pointing reads as angry and commanding; folded hands reads as ashamed |
| Guard ×3 | ✅ Three clearly different silhouettes. The dragging rope runs to the edge on purpose |
| Thief ×2 | ✅ Running left and looking back; captured with head hung down. Flat head cloth, not a turban |
| Vidura | ✅ Calm, no crown, cream with gold trim. Clearly a minister |
| Pandu | ✅ Pale complexion, full draw, facing right. **Minor:** the red forehead tilak is a thin vertical slash that could read as a cut at close range. It doesn't matter in the distant tease shot, but give him a clearer tilak shape when his full pose set is made for S01E02 |

**Status:** all 10 approved and filed into `assets/characters/<id>/` with a `character.json` each.

---

## Batch 3 (received 2026-11-07, `asset outputs/S01E01-batch-3/`)
**Technical check: all 21 pass** (7 backgrounds, 11 props, 3 overlays). Every background has `layer-far`, `layer-mid` and `layer-ground`; the hermitage hut is in `layer-front`; the scales have `beam`, `pan-l`, `pan-r` and `stand`; the border has 4 corner groups plus 4 bands with a transparent centre. Renders in `review/batch3-*.png`.

The concept decisions were followed: palace A with narrow nagara spires; court A with brown-maroon walls and a green throne cushion; border A at 86 px.

| Item | Result |
|---|---|
| 7 backgrounds, 3 overlays | ✅ approved |
| 10 props | ✅ approved |
| `vultures` | ⚠️ **Redo:** the scalloped wings read as **bats**, which is confusing in a night scene. Ask for: broad straight-edged wings with separated "finger" feathers at the tips, a small bald head on a long neck, a ruff of feathers at the base of the neck, gliding (not flapping). The current file is in use until then |

All filed into `assets/backgrounds/`, `assets/props/` and `assets/overlays/`.

## Facing and alignment fixes (2026-11-07)
Checked every pose by the ear rule: in three-quarter or side view, the visible ear is on the back of the head, so the face points away from it.
- **`thief/running`:** body runs left but the face looked back to the right. **Head mirrored** at its neck pivot so he faces where he runs. Original in `review/facing-originals/`.
- All other poses were already consistent (Mandavya confronting and cursing face right toward Dharma; the pulling guard faces his hands; Pandu faces his arrow).
- **Scene fixes** in `03-scenes.json` (previous version in `review/03-scenes.before-alignment.json`):
  - s05: no character is mirrored any more (a mirrored guard was facing right while walking left). The procession walks left, the lead guard's rope trails back to the prisoners.
  - The renderer now moves a mirrored character the way it faces.
  - Every character stands on the ground line of its real background: hermitage ≈0.76–0.80, red plain ≈0.80, court throne seat 0.575, palace floor 0.90, forest 0.86, meadow 0.78.
  - s03: the thieves run in from the left and duck behind the hut (the hut is drawn over them, `"frontLayer": true`).
  - s11: the grass blade and insect sit at the boy's pinching hand.
