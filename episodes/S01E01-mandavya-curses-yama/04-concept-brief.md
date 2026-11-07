# Concept Brief: S01E01, before batch 3

Quick, rough **PNG concept images** for the 3 assets that have no approved example yet. These aren't production files, just a target to agree on before anyone draws SVGs. Use GPT, Gemini or any image model.

**Make 3 variations of each (A, B, C)**, put them in `asset outputs/S01E01-concepts/`, and Claude will review them and pick one (or combine parts of several). The batch 3 SVG maker then gets the chosen concept as its exact target.

```
concept__palace__a.png   concept__palace__b.png   concept__palace__c.png
concept__court__a.png    concept__court__b.png    concept__court__c.png
concept__border__a.png   concept__border__b.png   concept__border__c.png
```

**Size:** portrait 9:16 (or 2:3 if 9:16 isn't offered). **Attach as style reference:** `assets/backgrounds/cosmic-court.svg` (render or screenshot it) and `review/batch2-all.png`, so the concepts match the approved look.

---

## Style block (paste first in every prompt)
> Flat 2D vector-style illustration for an Indian mythology storybook animation, matching the attached reference. Clean simple shapes, flat colours with 2–3 shades, dark plum outlines (#1E1420). Palette: night #1B1A3A, dusk purple #5B3B7A, pink #E39AA0, gold #E8B53A, saffron #E07A2E, parchment #F3E6C8, deep red #8E2A20. No people, no text, no watermark. Not photorealistic, not 3D.

## The architecture rule (for the palace and court)
The Mahabharata gives no buildings we can copy, so we use **classical ancient Indian** visual vocabulary. This is a design choice, kept consistent.

| ✅ Use | ❌ Avoid (reads as Mughal, Islamic or European) |
|---|---|
| Carved stone pillars with pot-and-foliage capitals (Ellora, Hampi) | Onion domes |
| Horseshoe "chaitya" arch windows (gavaksha), as in Ajanta and Karla caves | Pointed or cusped Islamic arches |
| Curved temple spires (nagara shikhara) with an amalaka disc on top | Minarets, Mughal jaali screens |
| Sanchi-style torana gateways (two posts, three curved crossbars) | Greek columns, European palace features |
| Sloped tiled or wooden roofs on pavilions, as painted in the Ajanta murals | Marble-white Taj-style buildings |
| Lion-footed throne (simhasana), oil-lamp stands (deepa), hanging garlands | Chandeliers, Persian carpets |

**Openly licensed references** (safe to attach to the image model): on Wikimedia Commons, search *Ajanta Caves paintings*, *Sanchi Stupa torana*, *Vitthala Temple Hampi*, *Ellora Kailasa temple*. Don't attach Pinterest or other channels' art.

---

## 1. Hastinapura palace (`palace`), used in s15
> [style block] A grand ancient Indian palace courtyard in Hastinapura, seen from the front, in calm morning light. Classical ancient Indian architecture: carved stone pillared verandas, two or three curved temple-style spires (nagara shikhara) behind, multi-tiered pavilion roofs, a Sanchi-style torana gateway, saffron banners on poles. Open, empty stone courtyard floor in the foreground centre (a character will stand there). The **top third is open soft sky** (a beam of light descends there). No onion domes, no pointed arches, no minarets. Portrait 9:16.

**Variations to ask for:** A = warm gold morning; B = cooler dawn with pink sky; C = closer, more intimate courtyard.

## 2. King's court (`court`), used in s06
> [style block] Interior of an ancient Indian royal court hall (mandapa), seen from the front. A **lion-footed golden throne (simhasana) on a raised stepped platform in the centre**, empty (the king is added separately), with its seat at about the vertical middle of the image. Rows of carved stone pillars on both sides, chaitya-arch windows high on the walls, deep red and gold hanging drapes, tall brass oil-lamp stands with flames, a patterned stone floor. Mood: power and judgement. No onion domes, no pointed arches, no chandeliers. Portrait 9:16.

**Variations:** A = warm lamplight, red-dominant; B = darker and more ominous (a stern tone for the sentencing); C = brighter and grander.

## 3. Folk-art border (`border`): the channel's signature
Used on the series sting, title cards, the law card (s14) and the tease (s16). It's the most important of the three.
> [style block, but no outlines on the motifs] An ornamental **frame border** for a 9:16 portrait image, inspired by Odisha Pattachitra painting borders: several parallel bands about 8% of the image width in total — a thin dark outer line, a deep red band with a repeating flower and creeper motif, a thin gold dotted line, and a narrow saffron inner band. **Ornate corner pieces** (lotus or floral medallions). The **centre is completely plain white** (it becomes transparent). Symmetrical, crisp, flat colours, no texture, no text.

**Variations:** A = classic Pattachitra floral creeper; B = Kalamkari-style flowing vine with leaves; C = a bolder, simpler version (fewer bands, larger motif) that reads well when small on a phone.

**Animation note:** the series sting has the border closing in from the edges, so the corner pieces should be self-contained medallions that can move separately.

---

## What happens next
1. Claude reviews the 9 concepts and picks or combines one per asset, with notes.
2. The chosen concepts become the targets in the batch 3 brief.
3. Batch 3 (SVG) is made: 7 backgrounds, 11 props, 3 overlays. Only these 3 assets need a concept. The hermitage, plain, meadow, forest and parchment are simple enough to go straight to SVG.

---

## Decisions (2026-11-07)
Concepts received in `asset outputs/S01E01-concepts 2/` (9 PNGs, made with the approved court and cast as style references, no Pinterest). Chosen files are copied to `review/concepts/`, along with side-by-side comparisons and a phone-size test of the borders.

### Palace → **A** (warm gold morning), with taller spires
- **Why A:** the best open sky for the falling light in s15, a clean empty floor for Vidura, and warm gold that contrasts with the purple of Dharma's court, so earth looks different from heaven.
- **Not B:** its purple bell-shaped spires read as domes, closest to the "Mughal" look we're avoiding.
- **Not C:** the big foreground pillars give nice depth but would be cropped at 9:16, and the sky is too small for the light beam.
- **Change:** A's spires are still a bit round. Make them taller, narrower curved nagara towers with an amalaka disc.

### King's court → **A** (warm red lamplight), with recolours
- **Why A:** it's the most authentically ancient-Indian (pot-and-foliage pillar capitals, as at Ellora), and its warm, earthly palette keeps the **human king's court clearly different from Dharma's purple cosmic court**. B is atmospheric but looks too much like Dharma's court (purple, a gold throne up steps), and viewers could mix up the two.
- **Not C:** too bright and cheerful for a death sentence.
- **Changes:** the king wears red, so the red walls and red throne cushion would swallow him. Use darker brown-maroon walls and a green or cream cushion. The ominous mood of B is added in code (a darker grade and vignette for s06).

### Border → **A's design at B's thickness**
- **Phone-size test** (opaque, over a scene, `review/concepts/border-phone-test.png`): A is the most distinctive and still readable small, and it reads as real Pattachitra. B is elegant but less distinctive. C is clear but generic, without the signature feel.
- **Change:** A's band is about 10.5% of the width, which takes too much from the picture on the tease and card scenes. Slim it to about 8%, like B. The corners stay as separate lotus medallions for the sting animation.
