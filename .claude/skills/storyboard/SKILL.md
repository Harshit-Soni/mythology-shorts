---
name: storyboard
description: Stage 3 of the pipeline. Turn an episode's script into 03-scenes.json (the Remotion scene spec) plus a list of needed assets.
argument-hint: <episode-id>
---

Storyboard episode $ARGUMENTS.

1. Read the episode's `02-script.md`, `STYLE_GUIDE.md`, `LEARNINGS.md`, `assets/characters/SPEC.md`, and list what's already in `assets/characters/`, `assets/backgrounds/` and `assets/props/`.
2. Write `03-scenes.json`, following the structure in `templates/episode/03-scenes.json`:
   - One scene per script beat, with `narration.en` and `narration.hi` copied exactly from the script.
   - Scene `type`: `character` | `prop-hero` (a symbolic object fills the frame) | `title-card` | `text-reveal`.
   - Choose camera moves and character actions so something changes every 2–4 s. Keep important content out of the bottom 20% and right 12% (the safe zone).
   - Don't set durations; they come from the voice timestamps later.
   - **Reuse** library assets where possible. Fill in `assets` with every character, background and prop, marked `library` or `new`.
3. Check the JSON parses (e.g. `python3 -m json.tool`).
4. Update Stage in `episodes/INDEX.md` to `3 Storyboard`.
5. Give the user a scene-by-scene summary (one line each) and the list of **new** assets, then say the next step is `/characters <ID>`.
