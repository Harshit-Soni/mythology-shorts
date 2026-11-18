# Asset brief: S01E04 (made in code)

As in S01E02 and S01E03, every new asset was made in code from the library rigs (no external generator). Run each script from the repo root.

| Script | Makes |
|---|---|
| `make-cast.py` | Bhishma (young + old), Amba, Ganga, Shalva, Parashurama, Shikhandi; Arjuna + `drawing-bow` |
| `make-backgrounds.py` | `yamuna-bank` (feet at 0.84; recorded in GROUND_LINES.md) |
| `make-props.py` | three-princesses, closed-gate, crooked-river, shiva-light, bed-of-arrows, vasu-lights, karna-silhouette |
| `build-scenes.py` | `03-scenes.json` |

## Cast
| Character | Built from | Poses (all face right) | Design notes |
|---|---|---|---|
| **Bhishma** | pandu rig | young: vow-hand-raised, standing-bow, drawing-bow, releasing · old: gesturing, bow-still (+ smiling) | White dhoti (the vow), a deep-blue uttariya, a crown. The old poses add white hair and a long white beard. |
| **Amba** | S01E02 women's build | tapas-standing (+ eyes-closed), standing-sad, folded-hands, resolute | Deep red and gold, a slim gold diadem, a braid. Dignified. |
| **Ganga** | women's build | rising, cursing | White and aqua, a gold crown, a rayed halo, waves at the hem (she rises from the river). |
| **Shalva** | pandu rig | defeated, turning-away | Purple, gold sash, crown. |
| **Parashurama** | mandavya rig (sage) | standing-axe, drawing-bow | Matted hair, beard, rudraksha; a deep red-brown dhoti; a large parashu held high. |
| **Shikhandi** | pandu rig (×0.94) | standing-bow, drawing-bow | Ochre with a green sash, a small crown. Shown with dignity. |

## Checks done
- **Every asset rendered alone and in the scene stills.**
- **Fixed in review:**
  - Parashurama's axe (too small and low) and his bow (clipped at the canvas edge).
  - The crooked river read as a snake, so it was redrawn as a riverbed receding in perspective.
  - s07's silhouette light turned the gates into black blobs, so it now uses dusk.
  - The bed of arrows was lifted out of the caption band.
