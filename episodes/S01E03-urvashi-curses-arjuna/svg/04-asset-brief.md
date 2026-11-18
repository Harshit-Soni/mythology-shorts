# Asset brief: S01E03 (made in code)

As in S01E02, every new asset was made by Claude in code from the library rigs (no external generator). Scripts in this folder:

| Script | Makes |
|---|---|
| `make-cast.py` | Arjuna (researched look + 3 new poses), Brihannala, Indra, Chitrasena, Urvashi, Uttara |
| `make-props.py` | celestial-chariot, astra-ring, family-vine, year-ring, bangles-scarred-arm, shami-tree, gandiva, gandiva-shockwave, bhishma-silhouette, amba-shadow |
| `build-scenes.py` | `03-scenes.json` |

Run each from the repo root. They import the S01E02 helpers (`make-concepts.py`, `make-women.py`, `make-props.py`).

## Cast
| Character | Built from | Poses (all face right) | Design notes |
|---|---|---|---|
| **Arjuna** | pandu rig | standing-bow (+ awed, worried), bowing-eyes-closed, kneeling-folded-hands (+ eyes-closed, shocked), dance-step | Deeper brown skin: "young and of darkish hue" (Virata §11). This also recolours the E02 tease pose; E02's finished renders are unaffected. |
| **Brihannala** | Arjuna | standing-graceful, dance-teaching, reaching-up, drawing-gandiva, gandiva-raised | Arjuna's own face and build; plum bodice and antariya, gold sash, braid with flowers, big gold hoops, conch bangles (Virata §2). Dignified, never comic. |
| **Indra** | pandu rig | standing-blessing (+ smiling) | Golden skin, tall crown, rayed gold halo, abhaya hand, a small vajra in the other hand. |
| **Chitrasena** | pandu rig | playing-veena | Sky-blue dhoti, pink sash, smaller crown, a two-gourd veena. |
| **Urvashi** | S01E02 women's build | dancing, walking, standing-surprised (+ hurt), cursing-hand-raised | Rose court dress with gold borders, violet sash, tiara, necklace, bangles, jasmine braid. Nothing revealing (CLAUDE.md rule 2). |
| **Uttara** | S01E02 women's build, ×0.86 | dancing | A young princess: cream and teal, yellow sash. |

Renderer: `HAND['urvashi:cursing-hand-raised'] = [730, 545]` (the curse burst comes from her palm).

## Checks done
- Every pose rendered alone (sheet) and in the scene stills; faces read at frame size, facing follows `flip`.
- Fixed in review: Chitrasena's hands now on the veena; Brihannala's reaching pose (the near arm crossed the face); the family vine's medallions read as faces (redrawn as two standing figures, and a crown + bow); the close-up hand.
- Court scenes (`amaravati-court`) scale characters ×1.15 to fill 50–70% of the frame height.
- s13's close-up moved to a parchment detail card (on the throne room it read as a log on the throne).

## v2 additions (2026-11-18)
- **Cast** (in `make-cast.py` → `v2_poses()`, `uttar()`, `abhimanyu()`):
  - **Prince Uttar** (from the pandu rig: fair, small crown, teal dhoti, ×0.88): boasting, fleeing, stunned.
  - **Abhimanyu** (×0.92, Arjuna's colouring, sky-blue dhoti): folded hands.
  - **New poses:** Arjuna blessing, Brihannala running (braid swung back), Urvashi arguing, Uttara pleading.
- **Props** (in `make-props.py`): war-chariot, dice-board (chaupar board + pasa dice), cattle-raid (the riders have topknots, not pointed crowns, per the silhouette lesson), year-ring-complete.
- **Fixes in review:**
  - Bhishma's scene light changed from `silhouette` to `dusk`: the silhouette grade also greyed out the gold year ring.
  - The dice board and the cattle were lifted out of the caption band.
