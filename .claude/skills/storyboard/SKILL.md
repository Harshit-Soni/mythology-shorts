---
name: storyboard
description: Stage 3 of the pipeline. Turn an episode's script into 03-scenes.json (the scene spec the Remotion studio renders) plus a list of needed assets.
argument-hint: <episode-id>
---

Storyboard episode $ARGUMENTS.

1. Read the episode's `02-script.md`, `STYLE_GUIDE.md`, `LEARNINGS.md`, **`studio/SCENE_SPEC.md`** (every field, camera move, action, cue and text style the renderer supports), `assets/characters/SPEC.md` and `assets/backgrounds/GROUND_LINES.md`. List the library: `assets/characters/*/character.json` (poses, facing), `assets/backgrounds/`, `assets/props/`, `assets/overlays/`.
2. Write `03-scenes.json` (structure: `templates/episode/03-scenes.json`, vocabulary: SCENE_SPEC.md):
   - One scene per script beat; `narration.en` / `narration.hi` copied **verbatim** from the script (safest: generate them with a small script that parses the beat tables, rather than retyping).
   - Series scenes: keep the series sting `s00` (fixed 1 s) and the series' recurring elements (`series/<S>/series.md`).
   - Something changes every 2–4 s (camera move, action, cue, new element). Keep faces and text out of the bottom 20% and right 12%.
   - **Characters stand on the ground line** of their background (GROUND_LINES.md; for a new background use the expected ground and fix it at render time). Seated or enthroned characters use the measured seat position.
   - **Facing:** use `character.json` → `facing`; set `flip` so faces point at whoever they interact with. Movement follows facing, so never mirror someone who should walk the other way.
   - **Cues:** `onWord` must occur in that beat's narration in **both** languages. Quoted lines + `speaking: true` give lip-sync.
   - Gore or violence: symbolic only (silhouettes, an empty stake, a light burst).
   - Don't set durations (they come from the voice), except `fixedDurationSec` on narration-less scenes like the sting. Insert shots: same beat, empty narration, reached by a `hard-cut-to` cue.
   - Fill in `assets` with every character pose, background, prop and overlay, marked `library` or `new`.
3. Validate: the JSON parses; every cue word exists in both languages; no element's `x` > 0.88 or face in the bottom 20%.
4. Optionally run `npm run render -- <ID> en --stills` from `studio/` (placeholders stand in for missing assets) to check the composition early.
5. Update `episodes/INDEX.md` to `3 Storyboard`. Give the user a one-line-per-scene summary and the **new** assets list; the next step is `/assets <ID>`.
