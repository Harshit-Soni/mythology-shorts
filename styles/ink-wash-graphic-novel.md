# Style: ink-wash graphic novel

The target look for the **illustrated** version of our Shorts (one painted still per shot, plus camera moves and motion effects). Chosen on 2026-11-07 to replace the flatter "animated film" test (`episodes/S01E01-*/illustrated/images/tests/sh10-nb21-1k.png`).

**Reference:** the Instagram reel "Third Eye" by Vision Machina (instagram.com/reel/DfBzp7Rx-NS, 72 s, 16:9, labelled AI content), about Shiva and the churning of the ocean.
**Frames:** 14 stills captured at 1–70 s are in `references/style-vision-machina-third-eye/frames/01–14.jpg`. That folder is **local only and git-ignored**: they're someone else's work, so they stay out of the public repo, and we never feed them to a generator. We take the *qualities* described below, not their images, characters or compositions.

## What makes the look

| Element | What we see | Frames |
|---|---|---|
| **Medium** | Hand-inked line art over loose **watercolour and ink wash** on textured cold-press paper. It reads as a painted graphic novel, not digital cel animation. Paper grain is visible everywhere. | all |
| **Line** | Black brush-ink outlines with varied weight: thick on silhouettes, thin on faces. **Dry-brush hatching** gives texture to stone, shell, rock and hair, and cross-hatching sits in the shadows. Lines stay loose and confident, not vector-clean. | 01, 03, 05 |
| **Colour wash** | Flat-ish washes with **wet-in-wet blooms**, granulation and hard drying edges. Large areas are left as bare paper white (sea foam, snow, highlights). Skin is one wash plus one shadow wash; no glossy rendering. | 03, 04, 13 |
| **Ink effects** | **Ink splatters, drips and smoke** made of spreading black ink. Poison, smoke and fury are painted as ink blooming into the paper. | 04, 06, 08, 10 |
| **Colour script** | Each moment gets **2–3 colours** and the mood changes by palette. Calm: teal sky, cream sea, warm sunrise. Poison: violet and black smoke. Fury: crimson, black and gold fire. Peace: deep navy, moon white and pale skin. | 01, 04, 07, 14 |
| **Light** | Glow comes from a source (the third eye, a ring of fire, the moon, an arrow) and is painted as **bare paper white plus a yellow wash**, with sparks around it. There's no airbrushed glow. | 07, 09, 11 |
| **Silhouettes** | Power and violence are shown as **solid black ink silhouettes against glowing washes**: a figure lifting a mountain, the cosmic dance, an archer. Big drama, no gore. | 08, 09, 11 |
| **Characters** | Semi-stylised with very readable faces. The tone can switch: comic, round and chibi-like for crowds (asuras and devas, a snake with spiral eyes), heroic anatomy and intense eyes for the hero. Expressions are exaggerated. | 02, 04, 06, 13 |
| **Framing** | Cinematic and varied: extreme close-up of the eyes, a crop showing only the legs, wide fish-eye horizons, low-angle silhouettes, and empty sky for breathing room. | 01, 05, 07, 12, 14 |
| **Mood** | Epic, with moments of warmth and humour. Sacred figures look dignified and powerful. | 06, 13 |

## Fit with our channel rules
- **Symbolic violence:** their silhouettes against fire and ink are exactly how we show the stake and the curse.
- **Respect:** deities are heroic and calm, never mocked; the comic register is only for crowds and animals.
- **Folk-art identity:** ink and wash on paper sits naturally next to our Pattachitra border and parchment cards. Keep the border overlay and the gold stamp as the channel's signature.
- **Differences we keep:** our format is **9:16 vertical** (theirs is 16:9), so compose tall. The bottom 20% stays free of faces for captions. Our palette accents (gold `#E8B53A`, saffron `#E07A2E`, indigo `#1B1A3A`) become the wash colours.

## Prompt block (prepend to every shot prompt)
> Vertical 9:16 hand-drawn graphic-novel illustration: expressive black brush-ink linework with dry-brush hatching, coloured with loose watercolour and ink washes on textured cold-press paper. Visible paper grain, wet-in-wet blooms, granulation, soft bleeding edges, ink splatters and drips; generous areas of bare paper white. A limited palette of two or three colours chosen for the mood of the moment. Light is painted as bare paper white with a warm yellow wash and small sparks around the source. Characters are semi-stylised with very readable, exaggerated expressions; skin is one flat wash plus one shadow wash. Ancient India, classical Indian architecture only. Dignified and epic. Hand-painted look: no 3D render, no glossy cel shading, no smooth digital gradients, no text, letters, watermark or border. Keep the bottom 20% of the frame free of faces and key detail.

## Colour script for S01E01 (per shot)
| Shots | Moment | Palette |
|---|---|---|
| sh01, sh01b, sh09–sh10, sh13b | Dharma's court | indigo night wash, gold halo light, paper-white steps |
| sh02 | Dawn, vow of silence | pale rose and gold dawn, cream mist, ochre sage |
| sh03–sh05b | Thieves, guards, arrest | dusk violet and black ink, orange torchlight |
| sh06 | The king's sentence | deep red and green court, gold |
| sh06b, sh07 | The stake (symbolic) | **crimson wash and black ink silhouette**; then navy night, moon, circling vultures |
| sh07b | The sage is alive | navy and moon white, gold eyes |
| sh08–sh08b | Forgiveness, the stake that won't move | navy, torch orange, black ink |
| sh11, sh12 | Childhood flashback | sepia and soft green wash, lots of paper white |
| sh13 | The curse | **crimson, saffron fire and black ink splatter**, burst of paper-white light |
| sh14 | The new law | parchment and warm lamp gold |
| sh15, sh15b | Born on Earth as Vidura | dawn gold beam over an indigo city, then warm palace light |
| sh16 | Tease: Pandu | forest green and dappled gold |

## How to generate in this style
1. **Restyle the character references first.** Our approved SVG sheets are flat vector, and as references they pull the output toward a flat cartoon (as in the sh10 test). Generate one **ink-wash character sheet** each for Mandavya and Dharma from the SVG sheets plus this prompt block. Approve them, then use those as the references for every shot. Do the same for the minor characters when they first appear.
2. **Test one shot** (sh10 again, to compare directly with the first test) before the batch.
3. Then generate the batch one shot at a time, reviewing each image zoomed in (identity, facing, composition, caption space).
4. Motion in the renderer: favour **ink-spread transitions**, drifting ink smoke, sparks and embers, and slow pushes. Avoid glossy light rays; paint-like effects suit this look.
