---
name: render
description: Stage 6 of the pipeline. Render an episode with the Remotion studio, review the frames (alignment, facing, cues, captions, both languages) and produce the final videos.
argument-hint: <episode-id> [en|hi] [final]
---

Render $ARGUMENTS. Read `PIPELINE.md` → Stage 6 and `studio/SCENE_SPEC.md`. Node is Homebrew's (`export PATH=/opt/homebrew/bin:$PATH`); run from `studio/` (first time: `npm install`).

1. **Preview:** `npm run render -- <ID> <lang>` (debug labels on: scene id, duration, missing assets). Without audio, timing is estimated; with `audio/<lang>.timestamps.json` it follows the voice.
2. **Review frames:** extract a frame per scene (mid-scene, plus right after each cue) with `npx remotion ffmpeg -ss <t> -i <video> -frames:v 1` and put them on one contact sheet. Compute times from the timeline (`node --input-type=module -e` importing `src/generated/data.ts` and `src/lib/timing.ts`). Check:
   - every character stands on its background's ground line (`assets/backgrounds/GROUND_LINES.md`), nobody floats or overlaps badly
   - faces point at who they interact with; mirrored characters move the way they face
   - cues land on their words (each language); speech bubbles and titles don't cover faces
   - nothing important in the bottom 20% / right 12%
   - Hindi: Devanagari renders correctly (conjuncts), captions highlight word by word
3. **Sync check (real audio):** every timeline word must equal the timestamps file by position (0 off-sync), and the video and audio durations must match.
4. **Grid check (new backgrounds):** render the background cropped to 9:16 with a 0.05 grid to read its ground line, key spots and the hut/throne positions. Record them in GROUND_LINES.md.
5. Fix positions, flips and cues in `03-scenes.json` (save the previous version in `review/` before big changes), or the renderer in `src/` (then update SCENE_SPEC.md). Re-render and re-check.
6. **Final:** `npm run render -- <ID> <lang> --final` for both languages → `render/<ID>-<lang>.mp4`. The user then does the GATE: watch on a phone with sound on and off.
