# Scene Spec Reference (`episodes/<ID>/03-scenes.json`)

Everything the renderer understands. If a storyboard needs something not listed here, add it to the renderer first (`src/`), then document it here.

## Episode
```json
{ "id": "S01E01", "title": {"en": "", "hi": ""}, "format": "short", "width": 1080, "height": 1920, "fps": 30,
  "sourceCredit": {"en": "", "hi": ""}, "safeZone": {"bottom": 0.2, "right": 0.12}, "scenes": [ ... ], "assets": { ... } }
```

## Sound (episode level)
`"sound": { "music": { "id", "volume": 0.32, "duckTo": 0.12, "fadeInSec", "fadeOutSec" }, "sfxVolume": 1 }`: one music bed from `assets/music/<id>.mp3`, looped if shorter than the episode. It dips to `duckTo` while the narrator speaks (merged word spans, 0.3 s ease) and fades out at the end. One sound plan serves both languages, because word cues fire per language.

## Scene
| Field | Meaning |
|---|---|
| `id` | `s01`, `s02`, … Insert shots get a suffix (`s06b`) |
| `beat` | The script beat it narrates. Insert shots share their parent's beat and have **empty narration** |
| `type` | `character` · `prop-hero` · `title-card` · `text-reveal` (informational; layout comes from the fields below) |
| `background` | id in `assets/backgrounds/`, or `split-frame` (two panels: meadow │ red plain) |
| `backgroundVariant` | `dawn` · `dusk` · `night` (colour grade on the background) |
| `frontLayer` | `true` = the background's `layer-front` (e.g. a hut) is drawn **over** the characters, so they can hide behind it |
| `characters[]` | see below |
| `props[]` | `{ id, x, y, scale, action }`: `x`,`y` = the prop's **centre** (0–1 of the frame); `scale 1` = the 800-px canvas drawn 600 px wide |
| `camera` | `{ move, from, to, focus: [x, y] }` |
| `narration` | `{ en, hi }`: **copied verbatim from 02-script.md**. Words inside "quotes" count as spoken by a character |
| `onScreenText` | `{ en, hi, style, anchor?, sub?, source? }` or `null` |
| `overlay` | `folk-art-border` · `sepia-folk-frame` (screen-space, not affected by the camera) |
| `cues[]` | `{ onWord: {en, hi}, do, target? }`: fires on the first narration word **containing** `onWord` (each language separately, so check that both words exist) |
| `transition` | how this scene hands over to the next (below) |
| `fixedDurationSec` | only for scenes with no narration that aren't insert shots (the series sting) |
| `sfx[]` | sound effects: `{ id, onWord?: {en, hi}, at?, offset?, volume? }`. Plays `assets/sfx/<id>.mp3` on the first narration word containing `onWord` (each language), else `at` seconds after the scene starts; `offset` nudges it. A plain string is a note until that file exists |
| `music` | this scene's music level, 0–1+ (default 1), eased over 0.5 s across the cut (e.g. `0.15` for a silence beat, `1.3` for a climax swell) |
| `notes` | for humans; not rendered |

## Character
`{ id, pose, expression?, x, y, scale, flip, action, variant?, speaking? }`
- **`x`,`y` = where the feet / base touch the ground** (0–1 of the frame). `scale 1` = the 1000×1600 canvas drawn 1000 px tall (a standing adult is ~870 px).
- Put `y` on the background's ground line. Measure it once per background with a grid render and note it in `assets/backgrounds/GROUND_LINES.md`.
- The pose file is `assets/characters/<id>/<pose>__<expression>.svg`, falling back to `<pose>.svg`.
- **`flip: true`** mirrors the character, and movement (`walk-left`, `run-in-hide`) then goes the way it faces. Check that the face points at whoever the character is interacting with (see the ear rule in `STYLE_GUIDE.md`).
- `speaking: true`: the mouth moves during quoted words. Eyes blink automatically.
- `variant: "b"`: a darker colourway of the same puppet (e.g. a second thief).

## Camera moves
`static` · `slow-zoom-in` / `slow-zoom-out` (`from`→`to` scale) · `fast-zoom-in` / `push-in-fast` · `slow-pan-up` / `crane-up` (`from`→`to` as a fraction of the height) · `tilt-down` · `pan-left` / `slow-pan-right` (fraction of the width) · `shake-small-then-static` · `shake-then-zoom`. `focus` sets the zoom origin.

## Actions (characters and props)
`idle`/`breathe` · `still` · `run-in-hide` (enters from off-screen on the side behind it) · `walk-left` · `walk-up-steps` · `step-forward` · `shout` · `bow` · `point` · `raise-hand` · `sway` · `glint` · `fall` · `circle` · `flicker-distant` · `descend` · `graze` · `draw-bow` · `stamp-in` (prop appears with a stamp bounce: at 0.15 s, or on its cue if one targets it) · `silhouette`, `held`, `spill`, `scatter`, `pierce`, `tip-violent` (react to cues)

## Cue effects (`do`)
| `do` | Effect |
|---|---|
| `scales-tip` / `scales-tip-violent` | the target prop tilts (violent = bigger, bouncier) |
| `spill` | the target prop pops; props with action `scatter` react too |
| `pierce` | the target prop hops |
| `stamp-next` / `stamp-in` | the target stamp prop lands; a `stamp-gold` text lands with it |
| `light-burst-saffron` | a saffron burst from the target character's hand (`HAND` table in `Character.tsx`) |
| `halo-crack-dim` | cracks draw over the target's halo, and the character dims |
| `eyes-open-glow` | glowing eyes on the target (for silhouettes) |
| `pull-fail` | the target shakes |
| `title-in` | `title-serif` text appears |
| `write-on` | `law-inscription` text finishes writing at this word |
| `hard-cut-to` | cut to the insert scene `target` at this word (that scene needs empty narration and the same beat) |
| anything else | ignored (safe to note intentions like `silence-beat`) |

## On-screen text styles
`stamp-gold` (big rotated gold stamp, e.g. शाप/CURSED) · `name-tag` (top-left serif name with optional `sub`) · `speech-bubble` (above `anchor` character's head, visible for the first ~60% of the scene) · `law-inscription` (writes on, with optional `source` line) · `title-serif` (big gold title at the top). Captions are automatic, from the narration.

## Transitions
`cut` (default) · `dissolve` · `light-wipe` · `memory-ripple` · `border-wipe` · `fade-to-night` (all crossfade into the next scene) · `flash-white` (white flash into the next) · `cut-to-black` (last scene fades to black)

## Code-drawn props (no asset file needed)
`shaap-stamp`, `seal-stamp`, `falling-light`, `stake-tip-glint`. A real file in `assets/` with the same id takes over.

## Layout rules
- Safe zones: keep faces and text out of the bottom 20% (captions and platform UI) and the right 12%.
- Characters are drawn back to front by `y`.
- Missing assets render as labelled placeholders in previews, so you can storyboard before assets exist.
