# Asset brief: S01E07 (made in code)

Run each script from the repo root, in this order: `make-cast.py` → `make-backgrounds.py` → `make-props.py` → `build-scenes.py <root>`.

| Kind | What | Notes (design choices, unless cited) |
|---|---|---|
| Cast | **Parikshit** (9 poses), **Shamika** (3), **Shringi** (2), **Kashyapa** (2), **old-brahmin** (1) | Parikshit: maroon and cream, crown, greying moustache; laughs at rest, so the lip-sync keeps laughing. `sit_cross()` seats the sage rig; `pinch()` is a hand holding something tiny. |
| Snake | **Takshaka** (rearing), `takshaka-coils-back/front` | S01E06's snake rig in lotus-red (CE 1.40.3) with a jewel; no hood. Use `shadow: false`. Coils: back at y 0.86, front at y 0.895, around a figure at 0.88. |
| Backgrounds | `pillar-tower`, `tower-room`, `banyan-road` | Nagara spire and round arches (architecture rule). In GROUND_LINES.md. |
| Props | `bow-dead-snake`, `banyan-reviving`, `snake-shadow`, `fruit-worm`, `fruit-bearers`, `worm-fingertip`, `gandhari-silhouette` | The disguises are given away by snake shadows. |

**Fixed in review:** onion domes → nagara spires; a pointed window → round; a raised single finger (it could read as rude) → finger and thumb; two dead snakes in one shot; coils behind the king; the tower's top out of frame; sage close-ups too low; captions over the hand; cut-off wrist and bow; the blindfold past her face; the badge over the crown in the thumbnail.
