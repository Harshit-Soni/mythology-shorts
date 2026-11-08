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

---

## Full-cast detailed rigs (received 2026-11-08, `asset outputs/S01E01-full-cast-rigs 2/`)
A detailed redraw of all 8 characters: 20 SVGs with the same file names as the library, plus a joint rig (`cast-rig.js`, `manifest.json`, `preview.html`). **Not filed yet**; the library is unchanged.

**Technical check: all 20 pass.** `viewBox 0 0 1000 1600`; no scripts, `<image>`, `<text>`, filters, gradients or external references; unique ids; every speaking pose has `head`, `eyes-open/closed` and `mouth-open/closed`; Dharma has `halo`. The silhouette has no face groups, as before. The files are 25–58 KB (the old ones are about 13 KB), with `data-*` joint attributes.

**How it was checked:** old vs new side by side (`review/fullcast/old-vs-new-*.png`); head close-ups with the blink and talk swaps (`review/fullcast/faces-*.png`); and stills of the real scenes, rendered once with the library and once with the new files swapped in temporarily, then the library restored (`review/fullcast/scenes-before-after-*.png`).

**Overall:**
- The drawing is clearly better: real anatomy, cloth folds, facial planes. Mandavya, Vidura, Pandu and the guard look good in the scenes.
- The cost: the heads are smaller and the expressions are restrained, so at phone size most faces read as "neutral". This goes against the LEARNINGS rule (make expressions about twice as strong as feels natural).
- The blink and talk swaps work on all 19 detailed poses.

**Facing (ear rule, checked on the close-ups):**
- Facing left: Dharma, the king (seated pointing), the guard, the thief.
- Facing right: Mandavya (every pose), Vidura, Pandu, young Mandavya, the king (folded hands).
- Earlier, Dharma, the king, Vidura, young Mandavya and Mandavya's calm, bound and meditating poses faced the front.

| File | Result |
|---|---|
| `dharma__seated-throne__neutral / stern / shocked` | ⚠️ **Redo.** (1) The three expressions are almost the same at on-screen size, and the s01 hook and the s13 climax depend on stern and shocked reading in under a second. (2) Dharma now wears **the same tall gold crown as the king**, so the god and the mortal king look alike. (3) Seated, he fills much less of the throne than before, and reads small and thin in s01/s10/s13 (I can fix the size in the scenes). |
| `king__seated-throne-pointing` | ✅ Approve after Dharma's crown is changed (the king can keep this crown). The angry face is weak, but the pointing arm carries s06 |
| `king__folded-hands` | ✅ Approve. **Correction (v3 review):** he faces **right** (ear rule, checked zoomed in), so in s08 he faces away from Mandavya. Scene fix: `flip: true` for the king in s08 (he only bows, so mirroring is safe) |
| `mandavya__standing-calm / confront / cursing-hand-raised / meditating-arms-raised` | ✅ Approve. In s13 the cursing arm points straight at Dharma, which reads well. Confront would be stronger with a fiercer brow (optional) |
| `mandavya__standing-bound` | 🔧 **Small fix (Claude):** he faces right, but the s05 procession walks left. I'll mirror the whole pose at x=500 so he faces where he walks; the original goes to `review/` |
| `mandavya__walking` | ⚠️ **Redo:** this is a wide standing stance facing the viewer, not a walk. It's used for s09, climbing the steps |
| `mandavya__on-stake-silhouette` | ✅ Approve. Smaller and slimmer, still reads as a seated figure on a pole; no symbol shapes |
| `guard__pointing / dragging / pulling` | ✅ Approve on pose and facing (all face left, same as before). The angry and strain faces are weak (optional redo) |
| `thief__running` | ⚠️ **Redo:** this reads as a crouching lunge, not a run, and the face is calm where the scene needs "scared" |
| `thief__captured` | ✅ Approve |
| `vidura__standing-hands-clasped` | ✅ Approve |
| `pandu__drawing-bow` | ✅ Approve. The thin tilak slash from batch 2 is still there; fix it in S01E02 |
| `young-mandavya__crouching-playing` | ✅ Approve. In s11/s12 the grass blade and insect must move to the new pinching hand (scene fix, Claude) |

**Redo wording for the generator** (give it the approved new files as style references):
1. **Dharma, seated on the throne, three expressions:**
   - "Keep this drawing style and pose, but make him read as a god, not a king: replace the tall pointed crown with a **wide jewelled kirita with a lotus finial** and a pearl string, clearly different from the king's crown.
   - Keep the large gold halo.
   - Make the seated figure broader and larger (shoulders and knees as wide as the previous version) so he fills the throne.
   - Expressions about twice as strong as natural:
     - **stern:** brows pulled down hard into a V, mouth a tight flat line, eyes narrowed.
     - **shocked:** brows lifted high, eyes opened wide (keep the almond shape, no round googly eyes), mouth dropped open showing the dark inside.
     - **neutral:** calm, eyes half-lidded.
   - All three must look different at thumbnail size."
2. **`mandavya__walking`:** "Side three-quarter view facing right, mid-stride: the front (right) leg forward with the heel down, the back leg pushing off on the toes, the arms swinging in opposition, the body leaning slightly forward, a determined face (lowered brows, set jaw). Same proportions and baseline as `standing-calm`."
3. **`thief__running`:** "Facing left and running hard: the body leaning well forward, one foot off the ground, the arms pumping, the loot sack over the shoulder. A scared face: wide eyes, raised brows, open mouth. The silhouette must read as a run, not a crouch."
4. Optional: stronger angry faces for the guard (all 3 poses) and the king pointing: "brows down into a V, teeth showing in a shout".

**Studio work needed when these are filed (Claude):**
- Update the `HEAD` and `HAND` anchors in `studio/src/components/Character.tsx`. Several heads moved, so the speech bubbles, the s13 saffron burst from the cursing hand and the halo crack must be re-aimed.
- Rescale Dharma on the cosmic court.
- Move the grass blade and insect in s11/s12.
- Re-check every scene's facing.
- **Joint rig:** our renderer swaps whole SVG images. Using the delivered joint rig (head tilt, arm and leg swing) would need the studio to draw the characters as inline SVG. That is optional, a separate studio change.

### v3 redos (received 2026-11-08, `asset outputs/S01E01-full-cast-rigs-v3/`)
Nine files changed and eleven are byte-identical to v2 (checked against the delivery's `changed-files.json` and our own file compare). **All 20 pass** the structure and safety checks. Sheets: `review/fullcast/v3full.png` (v2 vs v3), `v3faces.png` (close-ups with blink and talk), `v3sil.png` (silhouettes), `v3sc.png`, `zoom.png` and `zoom2.png` (real scene stills with v3 swapped in temporarily; library restored).

| File | Result |
|---|---|
| `dharma__seated-throne__neutral / stern / shocked` | ✅ **Approved.** A wide jewelled kirita with green gems, clearly different from the king's tall crown. The figure is bigger and fills the throne in s01/s09/s13, so no extra scaling is needed. At frame size, stern (hard brow, flat mouth) and shocked (lifted brow, wide almond eye, open mouth) read at once. Faces left, toward Mandavya |
| `mandavya__walking` | ✅ **Approved.** A real mid-stride walk facing right, which reads as walking in the silhouette and on the s09 steps |
| `thief__running` | ✅ **Approved.** Leaning forward mid-run with the sack, a scared face (wide eyes, open mouth), facing left. The s03 flip makes him run right as planned |
| `guard__pointing / dragging / pulling` | ✅ **Approved.** Heavier V-brows and a shouting mouth; facing unchanged (left) |
| `king__seated-throne-pointing` | ✅ **Approved.** A lowered, angry brow |

**Status:** the full cast (v2 approved files + v3 redos) is approved and ready to file. Filing work (Claude): copy the 20 files into `assets/characters/`; mirror `mandavya/standing-bound` for s05; set `flip: true` on the s08 king; update the `HEAD`/`HAND` anchors from `placement-anchors.json` (bubble, cursing palm, halo); move the grass blade and insect to young Mandavya's `pinchTip` in s11/s12; update each `character.json` (facing); re-render EN + HI.

### Filed (2026-11-08)
- All 20 files copied into `assets/characters/<id>/`. The previous flat versions are kept in `review/svg-v1-characters/`, and the scene spec before these changes in `review/03-scenes.before-fullcast.json`.
- **New pose `mandavya/standing-bound-left.svg`** (Claude): the approved `standing-bound` mirrored about x=500 in one wrapper group, so he faces the way the s05 procession walks. Face groups are unchanged, so blink and talk still work.
- **Scene fixes in `03-scenes.json`:**
  - s05: Mandavya uses `standing-bound-left`.
  - s08: the king has `flip: true`, so he faces Mandavya.
  - s11: the grass blade moves to (0.584, 0.695) and the insect to (0.639, 0.760), at the boy's `pinchTip`.
  - s12: the grass blade moves to (0.364, 0.721).
- **Studio:** the `HEAD` and `HAND` anchors in `studio/src/components/Character.tsx` now come from `placement-anchors.json`: face centres, Dharma's halo centre and the cursing palm (830, 492).
- **Checked at the cue moments:** the s07 eye glow sits on the silhouette's head, the s13 saffron burst on the cursing palm, and the halo crack on Dharma's halo. Every scene's facing was checked in the stills.
- Each `character.json` has a `facingByPose` entry and updated looks for Dharma, the king and the guard.
- The vultures are still the old bat-like file (their redo is still open).

## Vultures redo (received 2026-11-08, `prop__vultures.svg`, v3)
✅ **Approved and filed** into `assets/props/vultures.svg`; the old bat-like file is kept as `review/vultures-v1-bats.svg`.
- **Technical check:** paths only, no scripts, images or external references; `viewBox 0 0 800 800`; same `vulture-1/2/3` groups as before.
- **Look:** broad straight-edged wings with five separated finger feathers each, a bald head on a long bare neck, a neck ruff, a short fan tail, gliding.
- **At phone size and in s07** (`review/vultures-v3-vs-v1.png`, `review/vultures-v3-s07.png`): clearly vultures, no longer bats, and they don't crowd the silhouette's glowing eyes.
