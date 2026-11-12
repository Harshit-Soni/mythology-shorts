# Asset Review: X001

**How these were made:** there was no external image generator in this session, so Claude hand-wrote every asset as SVG code (brief route C). The generator script is kept outside the repo; the files are the source of truth. They're simpler than generator art but follow the channel's style block: flat fills, the #1E1420 outline, the palette, and named face groups.

**Concept step:** skipped for `khatu-shrine` and `barbarika-head-sky` because there was no generator to make concept PNGs. **Check both on your phone before publishing.** They are the two most sensitive images in the episode.

## Safety and structure
All 22 files: no `<script>`, `foreignObject`, `<image>`, `<text>`, external hrefs or filters. Correct viewBoxes (characters 1000×1600, backgrounds 1296×2112, props 800×800 except `leaf-glow-marks` 1000×700, `battle-silhouettes` 1600×600, `aravan-silhouette` 400×1600, `foot-on-leaf` 800×1400). Characters have `head`, `eyes-open`, `eyes-closed`, `mouth-closed` and `mouth-open`; `prepare` built the blink and talk variants for all 4 poses.

## Results
| Asset | Status | Notes |
|---|---|---|
| `barbarika` standing-bow calm / confident | ✅ approved | Reads at phone size; three blue-fletched arrows visible; faces right; the close-up (s05) holds at 1.5× |
| `barbarika` kneeling-offering serene | ✅ approved | Small in the split frame (s11); the offering hands read best at full size |
| `brahmin-krishna` standing-staff-pointing | ✅ approved | Faces left toward Barbarika; namam visible; eyes clean for the glow; the beard leaves the mouth visible |
| `peepal-night` | ✅ approved | Drip-tip heart leaves; moon; open ground |
| `cliff-night` | ✅ approved | Moon behind the head; two armies of torches below |
| `khatu-shrine` | ✅ approved, ⚠️ check | Cusped marble arch, crown with peacock feather, garlands, diyas. A folk interpretation, not the real murti |
| `chakra`, `glowing-arrow`, `ash-arrow`, `leaf-glow-marks` | ✅ approved | Arrows point **head-forward** (silver head right, blue fletching left) |
| `foot-on-leaf` | ✅ fixed by Claude | v1 floated like a boot; now 800×1400 with the ochre robe coming from the top edge |
| `ash-mark-hair` | ✅ fixed by Claude | v1 was an unreadable blob; now an old man's profile with white hair, beard, headband and the ash mark |
| `ash-mark-thigh`, `ash-mark-foot` | ✅ approved | The thigh medallion is small detail; fine on its cue |
| `jara-silhouette`, `reclining-krishna-silhouette` | ✅ approved | No wound shown |
| `battle-silhouettes` | ✅ approved | |
| `aravan-silhouette` | ✅ approved | **No crossbar**: checked against the "reads as a cross" lesson |
| `barbarika-head-sky` | ✅ approved, ⚠️ check | Translucent gold, crowned, eyes open, clouds below the chin, no neck |

## Ground lines (for `assets/backgrounds/GROUND_LINES.md` when you next update the docs)
| Background | Ground / key positions |
|---|---|
| `peepal-night` | ground from ≈ 0.68; feet at 0.82 (x 0.30 and 0.68 used) |
| `cliff-night` | cliff top flat at 0.80 between x ≈ 0.29 and 0.74 |
| `khatu-shrine` | no ground (shrine card); title area is the top 25% |

GROUND_LINES.md was **not** edited, to keep the repo's docs unchanged as you asked.

## Possible lessons for LEARNINGS.md (not added)
- Code-drawn props shown as an extreme close-up need to run off the frame edge (`foot-on-leaf` floated until the robe reached the top of a taller canvas).
- Medallion vignettes need one bold, simple shape: a profile reads, a top-of-head view doesn't.
