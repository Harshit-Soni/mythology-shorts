# Asset Brief: X001, Barbarika: The Head That Watched the War

Everything needed to get this episode's assets made outside this project. Generate them, drop the files into **`asset outputs/`** (or `assets/_inbox/`) using the file names below, and Claude will check them, fix them up and add them to the library.

**Work in batches. Send batch 1 first.** The two new characters set the look of the episode, so there's no point making the rest until they're right.

**Reused from the library (don't make these):** `red-sky-plain` (6 scenes, colour-graded in code), `parchment-card`, `forest-hunt`, the `split-frame` layout, `folk-art-border` and `sepia-folk-frame`.

**About the old session's images:** the Barbarika and Brahmin "master images" from the earlier reel are **anime-style**. Use them **only as a costume reference** (colours, tilak, topknot, sash), never as a style reference. This channel's look is flat vector Pattachitra-storybook (see `assets/characters/*` and the S01E01 review PNGs). Attaching one approved S01E01 character, e.g. `assets/characters/mandavya/standing-calm.svg` rendered to PNG, as the **style** reference works best.

---

## How to generate SVGs (pick what works)
| Route | Good for | Notes |
|---|---|---|
| **A. A native vector generator** (e.g. Recraft) | Characters, backgrounds | Real SVG output and style consistency |
| **B. GPT / Gemini image → PNG → vectorise** (or send the PNG and Claude traces it) | Characters, backgrounds | Best-looking art; Claude rebuilds the named groups |
| **C. Ask GPT / Gemini chat to write SVG code** | Simple props, silhouettes | Easy named groups, simpler art |
| **Plain PNG** | Anything | Fine too: transparent background, or flat white for Claude to remove |

If a route can't produce the **named groups**, deliver anyway; Claude adds them.

---

## 1. Style block: paste into EVERY prompt
> Flat 2D vector illustration for an Indian mythology storybook animation. Clean simple shapes, flat colours with 2–3 shades per material, no gradients on characters, no texture noise. Consistent dark plum outline (#1E1420), 3–4 px. Simple expressive faces: large almond eyes, small nose, gentle features. Ancient Indian clothing and ornaments (dhoti with a front pleat, uttariya, angavastram, gold jewellery), not Mughal and not modern. Respectful, dignified depiction. Palette: night #1B1A3A, dusk purple #5B3B7A to pink #E39AA0, gold #E8B53A, saffron #E07A2E, parchment #F3E6C8, deep red #8E2A20. Ornament details inspired by Pattachitra and Kalamkari folk art. Not photorealistic, not 3D, not anime, no text.

## 2. Lessons from S01E01: add to every character prompt
> - **Dhoti, not shorts:** a wrapped dhoti with a visible front pleat, soft folds.
> - **Exaggerated expressions:** faces are small on a phone; push each expression about twice as far as feels natural.
> - **Big `mouth-open`:** at least twice the size of the closed mouth, dark interior.
> - **Every pose readable as a silhouette**, and different from the character's other poses.
> - **No ambiguous objects in hands:** a bow is clearly a bow, a staff clearly a staff.
> - **Arrows:** the **silver metal arrowhead at the front**, **blue feathers (fletching) at the back**. (The old reel drew it reversed.)

## 3. Technical blocks
**Characters:**
> SVG, viewBox="0 0 1000 1600", transparent background. Character centred at x=500, feet or knee on y=1550; a standing adult's head top near y=150 and **the face centred near x=500, y=330** (the renderer's eye-glow and speech effects aim there). Flat fills, no embedded images, no <text>, no filters. Name the groups: `head`, `eyes-open`, `eyes-closed` (display:none), `mouth-closed`, `mouth-open` (display:none).

**Backgrounds:**
> SVG, viewBox="0 0 1296 2112" (a 1080×1920 portrait frame plus a 108 px margin left/right and 96 px top/bottom for camera moves). No characters. Layer groups: `layer-far` (sky, distant), `layer-mid`, `layer-ground`, and `layer-front` only if something must sit in front of characters. Keep the bottom 20% simple (captions go there). The frame's centre line is x=648.

**Props:**
> SVG, viewBox="0 0 800 800" unless stated, transparent background, object centred, no ground shadow.

**Ground lines** (where feet go): canvas y = frame fraction × 1920 + 96. Each background below gives the number to aim for.

## 4. File naming
```
<character>__<pose>__<expression>.svg   barbarika__standing-bow__calm.svg
bg__<id>.svg                            bg__peepal-night.svg
prop__<id>.svg                          prop__chakra.svg
```

## 5. Consistency tips
- Make a **design sheet first** for each character (front and three-quarter view on one canvas). After approval, attach it as the reference for every pose.
- Generate all poses of one character in a single session. For "same pose, different face", ask the tool to **edit the approved image and change only the face**.
- **Facing:** draw Barbarika **facing right** and the Brahmin **facing left** (they face each other under the tree). Claude can mirror in code.

---

# BATCH 1: lock the look (make these first)

### Barbarika (`barbarika`)
**From the sources:** Ghatotkacha's son and Bhima's grandson; he "grew to manhood at once" and was named for his hair, "like that of a Barbara" (Skanda Purana 60.62–68). The folk tradition calls him "bearer of three arrows".
**Look (design choices, noted as such):** a young warrior of about 18–20, strong and lean; warm brown skin (#9A6440, a little deeper than the S01E01 cast, a quiet nod to his rakshasa lineage, **not** monstrous: no fangs, horns or claws); **thick, wild, curly black hair** gathered in a high topknot with loose curls (his name); a **vertical red-and-saffron tilak**; gold ear studs and armlets; a **yellow uttariya sash** across the chest; a **deep-blue dhoti** with a front pleat; leather forearm guards; a tall longbow; a quiver on his back holding **exactly three arrows** (blue feathers showing). A calm, confident, kind face: he is worshipped today, so he must look noble and gentle, never arrogant.

| File | Pose / expression | Used in |
|---|---|---|
| `barbarika__standing-bow__calm.svg` | Three-quarter view **facing right**, standing tall, longbow held upright in his left hand, right hand relaxed; calm, steady gaze. Three arrows clearly visible in the quiver | s01, s03, s06 |
| `barbarika__standing-bow__confident.svg` | **Same image, only the face changed:** chin slightly up, brows raised, a small sure smile. Its `mouth-open` must be big: he says "One muhurta" in a **close-up** (shown 1.5× larger than normal) | s05 |
| `barbarika__kneeling-offering__serene.svg` | Kneeling on one knee, facing right, head bowed, **both palms open and raised forward** in offering; the bow laid on the ground in front of him; peaceful, accepting face (eyes softly closed or lowered). Feet/knee on y=1550. No sword, no blood | s11 |

### The Brahmin (Krishna in disguise) (`brahmin-krishna`)
**From the sources:** in the Khatu telling, Krishna comes disguised as a Brahmin and tests Barbarika (research #9, #11).
**Look (design choices):** an elderly Brahmin, slim and slightly stooped but strong; a long **white beard** and white hair in a small knot; a **white Vaishnava namam** (U-shaped tilak with a red centre line), a quiet hint of who he really is; ochre cloth and a cream angavastram; a tulsi-bead necklace; a plain **wooden walking staff**; **bare feet**. Skin a warm medium brown (**not blue**: the disguise must hold until the reveal). **Large, kind, knowing eyes**, the same almond shape as the cast: the eyes glow blue in the reveal shot (s07b), shown 1.6× larger, so keep the eye area clean.

| File | Pose / expression | Used in |
|---|---|---|
| `brahmin-krishna__standing-staff-pointing__serene.svg` | Three-quarter view **facing left**, leaning lightly on the staff with his left hand, **right arm raised, pointing up and to the left** (at the tree's canopy). Gentle half-smile, as if setting a friendly riddle | s06, s07b (close-up) |

### Background: the peepal tree at night (`bg__peepal-night.svg`)
A **giant ancient peepal tree** fills the left and centre, its huge canopy across the upper half of the frame: hundreds of **heart-shaped leaves with long pointed drip-tips** (the peepal's signature; not generic round leaves). A thick twisting trunk with aerial roots, rooted left of centre (canvas x ≈ 420–560). Moonlit night: sky #1B1A3A with stylised curl-clouds and a bright moon peeking through the branches. At the horizon (canvas y ≈ 1450), the edge of an **empty battlefield plain** with a few faint banners far away. **Open, flat ground** in the lower part for two figures: **feet at canvas y ≈ 1670** (frame 0.82), one at canvas x ≈ 430 and one at x ≈ 840; keep that ground clear and simple. The canopy is also the backdrop for a glowing-marks overlay, so keep the leaf mass in roughly canvas y 250–900. Layers: `layer-far` (sky, moon, clouds, horizon), `layer-mid` (tree, canopy), `layer-ground`. Used in s06, s06b, s07, s07b (Claude zooms in for the close-ups).

**→ Send batch 1; Claude reviews it before you continue.**

---

# BATCH 2: backgrounds + arrow props
> Attach the approved batch-1 files as references for style and colour.

### Backgrounds
| File | Description |
|---|---|
| `bg__cliff-night.svg` | **The hook shot.** A high **rocky cliff edge** across the foreground (flat top for one figure: **feet at canvas y ≈ 1632**, frame 0.80, centred at x=648). Behind, a **huge full moon** in the upper-middle (centre around canvas y ≈ 760, so his head silhouettes against it). Far below, on a vast dark plain, **two armies facing each other**: rows of tiny torches, banners and chariots on the left and right, a gap between them. Strong wind feeling (curl-clouds streaming). Night palette #1B1A3A → #5B3B7A with gold torch dots. Layers: `layer-far` (sky, moon), `layer-mid` (plain, armies), `layer-ground` (cliff). Used in s01 |
| `bg__khatu-shrine.svg` | **Concept first (see `04-concept-brief.md`).** The Khatu Shyam image as devotees know it, as a folk-art rendering, **not a photo copy of the real murti**: a temple sanctum niche with a carved white-marble arch (Rajasthani temple style: scalloped arch, jharokha details; no onion domes), and inside it the **sacred head image**: a dark stone face with large eyes and a tilak, an **ornate gold crown (mukut) with a peacock feather**, under heavy **rose and marigold garlands**. Brass diyas glowing, hanging bells, scattered petals, warm dawn light. **Keep the top 25% calm** (the title KHATU SHYAM sits there) and the bottom 20% simple. Devotional and respectful. Layers: `layer-far` (wall, arch), `layer-mid` (image, garlands), `layer-ground` (lamps, petals). Used in s13 |

### Props (viewBox 0 0 800 800 unless stated)
| File | Description | Used in |
|---|---|---|
| `prop__chakra.svg` | The **Sudarshana discus**: a gold disc with a serrated, flame-tipped rim, a spoked inner ring and a lotus hub; a soft glow halo drawn as lighter flat rings (no filters). Groups `disc`, `glow` | s02, s11 |
| `prop__foot-on-leaf.svg` | Ground-level close-up: the **Brahmin's bare foot** (warm medium-brown skin matching his design, not blue), seen from the side, with the hem of his ochre cloth at the ankle, **pressing down one heart-shaped peepal leaf** whose long tip sticks out from under the sole. Dignified and simple | s06b, s07 |
| `prop__glowing-arrow.svg` | One arrow, horizontal, **silver arrowhead pointing right**, **glowing blue feathers on the left**, a short blue glow trail behind. Groups `arrow`, `glow` | s07 |
| `prop__leaf-glow-marks.svg` | viewBox 0 0 1000 700. **Only the glow marks**, transparent everywhere else: 60–100 small glowing blue marks (tiny pierced-dot / tick shapes, #7FD4FF with a white core) scattered in a broad canopy shape, denser at the centre. It overlays the tree's canopy | s07 |
| `prop__ash-arrow.svg` | One arrow, horizontal, **arrowhead pointing right**, its shaft packed with **saffron-red powder** (#E07A2E / #B8361F), a long plume of red ash streaming off behind it to the left. Groups `arrow`, `ash` | s08 |

**→ Send batch 2 after batch 1 is approved.**

---

# BATCH 3: the "death-spot" medallions, silhouettes and the watching head

### Medallions (viewBox 0 0 800 800). They appear on parchment with a sepia grade, so use clear shapes and strong contrast
Each is a **round folk-art medallion** (a thin ornamental parchment-brown rim, like a Pattachitra roundel) showing one detail, with a **bold saffron-red ash mark** (#B8361F) landing on it.
| File | Inside the medallion | Used in |
|---|---|---|
| `prop__ash-mark-hair.svg` | The **white hair and top of the head** of a very old warrior (Bhishma: long white hair, a simple warrior's headband), seen from the side; the red ash mark on the hair | s09 |
| `prop__ash-mark-thigh.svg` | A warrior's **thigh in a gold-trimmed dhoti** with a heavy **mace (gada)** resting against it (Duryodhana's weapon); the red ash mark on the thigh | s09 |
| `prop__ash-mark-foot.svg` | **Krishna's foot**, **blue skin** (#3E6FB0 family), a gold anklet, turned so the **sole** is visible; the red ash mark on the sole. Reverent and simple | s09 |

### Silhouettes: solid #1E1420 (a touch of dark red rim-light allowed), no faces, no gore
| File | Description | Used in |
|---|---|---|
| `prop__jara-silhouette.svg` | A **hunter crouched among bushes**, drawing a bow **aiming right**; simple and clear | s10 |
| `prop__reclining-krishna-silhouette.svg` | A figure **resting in yoga under a tree**, half-reclining, one **foot extended toward the left** (toward the hunter). Peaceful; **no arrow, no wound**. Must not read as anything else in silhouette | s10 |
| `prop__battle-silhouettes.svg` | viewBox 0 0 1600 600. A wide band of a **distant battle**: tiny chariots, horses, elephants, banners and dust clouds, in dark red-brown silhouette (#3A1C14) with a few ember dots | s12 |
| `prop__aravan-silhouette.svg` | viewBox 0 0 400 1600. **Far away at sunset:** a tall, plain garlanded post with a **crowned head** on top, as in the Koovagam festival effigies of Aravan. ⚠️ **No crossbar or arm shapes anywhere**: S01E01 learned that a figure on a pole can read as a cross. Respectful, monumental, not gory | s14 |

### The watching head (concept first, see `04-concept-brief.md`)
| File | Description | Used in |
|---|---|---|
| `prop__barbarika-head-sky.svg` | **Barbarika's face**, matching the approved batch-1 design (curly topknot, tilak, gold ear studs) with a **small gold crown**, **very large** (it fills the sky), **translucent gold** (#E8B53A tints over sky colours), eyes open, serene, a faint smile. **The face emerges from swirling curl-clouds: no neck, no cut, nothing below the chin but cloud.** It must feel divine and peaceful, never macabre | s12 |

---

## Claude makes these in code (don't generate them)
The white flash, the eye glow (s07b), the gold stamps (**1 MUHURTA**), the write-on text (**1 month · 6 days · 1 day**), name tags and source tags, the title **KHATU SHYAM**, captions, the split-frame layout, and the night / dawn / dusk / sepia colour grading.

## Checklist
- [x] All assets made by Claude as hand-written SVG (no external generator), 2026-11-08
- [ ] Concepts: skipped (no generator); khatu-shrine and barbarika-head-sky need your phone check
- [x] Reviewed and filed: barbarika ×3, brahmin-krishna ×1, 3 backgrounds, 13 props (see 04-asset-review.md; 2 props fixed)
- [ ] Ground lines recorded in 04-asset-review.md; add them to GROUND_LINES.md when you next update the docs
