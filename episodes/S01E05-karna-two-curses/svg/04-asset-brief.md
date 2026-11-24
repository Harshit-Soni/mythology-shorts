# Asset brief: S01E05 (made in code)

As in S01E02–E04, every new asset was made in code from the library rigs (no external generator). Run each script from the repo root.

| Script | Makes |
|---|---|
| `make-cast.py` | Karna (11 poses), Parashurama (+ teaching, accusing, cursing, sleeping), the Brahmin of the homa cow, Drona |
| `make-backgrounds.py` | `mahendra-ashram`, `sea-shore` (feet at 0.84; recorded in GROUND_LINES.md) |
| `make-props.py` | sunk-wheel, homa-cow, cow-bell, alarka-worm, worm-on-thigh, wheel-light, astra-ring-dark, nahusha-silhouette |
| `build-scenes.py` | `03-scenes.json` |

## Cast
| Character | Built from | Poses (all face right) | Design notes (choices, not from the text, unless cited) |
|---|---|---|---|
| **Karna, warrior** | pandu rig | watching, asking, drawing-bow, empty-hand, pulling-wheel | Golden-brown skin, gold crown, **indigo** dhoti, gold sash: reads apart from Arjuna (dark, red) on the red plain. Ordinary gold: he has given away his natural armour and earrings by then (Shanti 5). |
| **Karna, student** | pandu rig | folded-hands (+ uneasy, awed), student-bow, kneeling-pleading, bowed (+ afraid), enduring, guru-on-lap (+ pained) | His disguise: no crown, a topknot, plain unbleached cloth, no necklace or cuffs. The big gold earrings stay (he was born with them), so he's recognisable in both looks. |
| **Parashurama** | mandavya rig | teaching, accusing, cursing, sleeping | E04 colours. `sleeping` lies on his back, head at the left, for Karna's lap. |
| **The Brahmin** (`homa-brahmin`) | mandavya rig | standing-grief, cursing | Unnamed in the text. Iron-grey hair, cream and yellow. Dignified, not a villain. |
| **Drona** | mandavya rig | refusing | White hair and beard, slate-blue, gold sash. |

## Props tied to the text
- **alarka-worm:** "like a hog in shape… eight feet… very keen teeth… bristles like needles" (Shanti 3). Used for the trailer and the loop on a parchment card.
- **worm-on-thigh:** a thin red line only; no wound.
- **cow-bell:** the cow's death is never shown; the bell and a broken garland stand for it.

## Checks done
- Every asset rendered alone, then all 32 shots as stills; faces zoomed (ear rule); thumbnails EN + HI.
- **Fixed in review:** hands clipped at the canvas edge (Drona, teaching); arms crossing faces (both curses); the wheel pull redrawn as a lunge on one knee; kneeling and cross-legged bodies redrawn (they read as a box and a cushion); the insect and the bell floated over landscapes → parchment cards; the Nahusha tease blacked out by `light: silhouette` → `night`, cobra and kirita redrawn; the second stamp covered Parashurama's hand; confession close-up hid behind captions; close-ups tightened.
