# Asset brief: S01E06 (made in code)

As in S01E02–E05, every new asset was made in code from the library rigs. Run each script from the repo root, in this order.

| Script | Makes |
|---|---|
| `make-cast.py` | Nahusha, a god (`deva`), Shachi, Agastya, Bhima, Yudhishthira |
| `make-backgrounds.py` | `indra-sabha`, `heaven-sky`, `himalaya-gorge` (recorded in GROUND_LINES.md) |
| `make-props.py` | the snake (great-snake, snake-head, coils-back/front, coils-of-light, snake-eye, snake-eye-throne), throne-icon, palanquin-icon, palanquin-carried, foot-on-head, strength-stream, nahusha-falling, indra-in-lotus, dead-snake-sage. Some embed the cast, so run it after make-cast.py |
| `build-scenes.py` | `03-scenes.json` |

## Cast
| Character | Built from | Poses | Design notes (choices, not from the text, unless cited) |
|---|---|---|---|
| **Nahusha** | king rig | seated-throne (faces left), humble (+ serene), gaze | Two looks: plain cream cloth and a small crown; violet and gold, a tall crown and a halo. The halo is the glory he loses at the curse (5.17.12). |
| **deva** | pandu rig | offering, drained | One of the gods, unnamed. Drained = greyed, halo faded. |
| **Shachi** | women's build | standing-firm, speaking | Turquoise and gold, tiara, halo. Composed, never alluring. |
| **Agastya** | mandavya rig | cursing, softening | Leaf-green bark cloth, brown hair with grey. |
| **Bhima, Yudhishthira** | pandu rig | held (+ weak), freed · arriving, answering | Exile dress: topknots, no crowns or gold. Bhima broader, with a moustache. Reusable in later episodes set in the exile. |

## The snake (CE 3.175.13-14)
Huge, spotted, turmeric-yellow, a wide mouth, **four fangs**, blazing red eyes. **No hood.** E05's tease drew a hooded cobra; this is the text's description.
- A figure held in coils: put `coils-back` at y 0.835 and `coils-front` at y 0.845 around a character standing at 0.84.
- `snake-head` is a tall canvas: the head is 720 canvas units above its centre; the neck runs off the bottom of the frame.

## Checks done
- Every asset rendered alone, then all 31 shots as stills; thumbnails EN + HI.
- **Fixed in review:** the throne's pointed arch → round (architecture rule); necklace outlines left on the humble look; coils folding at their ends → redrawn as round strokes; a squared-off snake head; the neck ending in mid-air; the foot not touching the hair; a tiny rider; Indra's stray foot; a cartoon X eye on the dead snake; the eye, foot and fall made full frame; Shachi's close-ups raised; thumbnail moved from Bhima to the snake.
