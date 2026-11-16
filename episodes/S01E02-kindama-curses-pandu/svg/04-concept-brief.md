# Concept Brief: S01E02, Kunti and Madri

Kunti and Madri are the channel's **first women**, so there's no approved example to match. Before any SVG work, get **3 rough PNG variations** of a single design sheet showing both women side by side. Claude will pick one (or combine two) in **Decisions** below, and the chosen sheet then becomes the reference for every pose in batch 1.

## What to ask for (one image per variation, 3 variations)
> [Style block from `04-asset-brief.md` §1]
> A character design sheet of two Indian queens from the Mahabharata, standing side by side, full body, three-quarter view facing right, on a plain parchment (#F3E6C8) background. Left: **Kunti**, about 30, composed and strong, cream antariya and bodice with a deep maroon-red border, a plain ochre uttariya over one shoulder and across the torso, hair in a low knot, no gold jewellery. Right: **Madri**, about 22, gentle but determined, cream antariya and bodice with a deep teal-green border, a plain saffron uttariya, hair in a single braid over one shoulder, no gold jewellery. Modest, dignified ancient Indian dress, no bare midriff. Flat 2D vector storybook style matching the attached reference character.
> **Attach:** `assets/characters/pandu/drawing-bow.svg` rendered to PNG (their husband) as the style reference.

**Vary across the three:**
- face shapes and proportions
- how the uttariya drapes
- how warm or strong the expressions are

Keep the colour keys (maroon and teal) fixed, so they stay easy to tell apart.

## Rules
- **Respect:** no sexualisation, no glamour poses, no tight or revealing clothes. They are queens living as ascetics.
- **Period:** ancient Indian dress. Not Mughal, not modern saris with stitched modern blouses, not TV-serial costume.
- **References:** only openly licensed ones (Wikimedia Commons, museum open-access collections, e.g. Ajanta-style or Pattachitra women's dress). Never Pinterest, never another channel's art.
- **No jewellery beyond a red thread and bindi** (Pandu gave their ornaments away, Adi §119).

## Review (Claude, when the concepts arrive)
1. Lay the three side by side next to Pandu at phone size.
2. Check that each woman reads as a silhouette and that they're easy to tell apart.
3. Check that they look like they belong next to Pandu, Dharma and Mandavya.
4. Pick one or combine, with reasons below, and point the brief's batch-1 rows at it.

## Decisions (2026-11-16)
**Made by Claude, not a generator** (at the owner's request): `svg/make-concepts.py` builds both women from the `pandu` rig, so they share the cast's head construction, line weight and joint pivots. The sheets are `svg/concepts/concept-{A,B,C}.svg/.png`, plus `concepts-compared.png`.

| Variation | Kunti | Madri | Verdict |
|---|---|---|---|
| A | Ochre sash over one shoulder, low hair knot | Saffron sash, braid over the shoulder | Clean, but at phone size the two differ only by colour and hair |
| B | Shawl over both shoulders | Same | Reads as a vest; flat and boxy at phone size. Rejected |
| **C** | **Ochre uttariya drawn over her head as a veil** | **Saffron sash + braid** (as A) | **Chosen** |

**Why C:**
1. The veil makes Kunti read as the elder queen at a glance and gives the two women different silhouettes (veil vs braid), not just different colours. That matters in s06, s09 and s11, where they share the frame.
2. Madri's open hair and braid keep her younger and lighter, matching the brief.
3. Both stay modest (bodice to the waist, ankle-length antariya) with no gold, per Adi §119.

**Known limits:** the faces come from Pandu's head (the jaw and nose are his). Kohl eyes, arched brows, lips, a bindi and the hair make them read as women at phone size, but a generator or a later hand-redraw could soften the jaw. Because they're built on the rig, Claude can also make their **poses** (the arms are posable) without waiting for batch 1.
