---
name: voice
description: Stage 5 of the pipeline. Generate the episode narration in English and Hindi with ElevenLabs, align it to the script beats and write the audio + word timestamps the renderer uses.
argument-hint: <episode-id> [en|hi]
---

Narration for $ARGUMENTS. Read `PIPELINE.md` → Stage 5 first (the voice id, model and both routes are there).

1. **Text:** the language's narration from `02-script.md`, one paragraph per beat, verbatim.
2. **Generate (ElevenLabs connector, no API key):** `creative_generate_speech` with the channel voice and model from PIPELINE.md, `generations_count: 1`, in the episode's ElevenLabs flow if it has one (pass `flow_id` so all takes stay together). Price it first with `estimate_only` if the user hasn't approved spend for this episode.
   - If it fails with "free generations are busy": **stop, start no other generation that turn**, tell the user in one sentence (nothing was charged), and offer to retry.
   - When it has started, check completion with `creative_get_generations` (don't hammer it: do useful work between checks), then download `full_res_url` with curl into the scratchpad.
3. **Import with exact word times** (from `studio/`): run `creative_transcribe_audio` (Scribe, free on Starter) connected to the speech node, download `words_download_url`, drop the `[tag]` tokens (and tag fragments like `awe,` from `[with awe, slowly]`), then `npm run voice:import -- <ID> <lang> <take.mp3> <words.json>`. It must say 0 interpolated. Don't ship an `auto` import: it only finds beat boundaries, and captions drift by up to ~1.7 s inside a beat (S01E02).
4. **Length:** the import prints where the speech ends. Target ≤ 60 s including the 1 s sting. If over, propose specific cuts in `02-script.md` (the script lists candidates); the user decides whether to regenerate.
5. Optional free draft before spending credits: `npm run voice -- <ID> <lang>` (macOS voices).
6. Update `00-idea.md` and `episodes/INDEX.md` (stage + length per language), then hand over to `/render`.
