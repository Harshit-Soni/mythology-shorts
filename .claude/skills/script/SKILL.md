---
name: script
description: Stage 2 of the pipeline. Write the bilingual (English + Hindi) 45–60 s Shorts script for an episode, from its verified research.
argument-hint: <episode-id> [notes]
---

Write the script for episode $ARGUMENTS.

1. Read the episode's `00-idea.md` and `01-research.md`, plus `STYLE_GUIDE.md`, `LEARNINGS.md` and the series' `series.md`.
2. If key claims in `01-research.md` are still unverified, warn the user and ask whether to continue.
3. Write `02-script.md`:
   - **English:** 120–140 words in numbered beats, one beat per scene, about 2–4 s each. Beat 1 is the hook and must work in 2 seconds without context. The last beat pays off the hook and teases the next episode.
   - Each beat has a narration line plus an on-screen visual idea.
   - Use only events from the research table. Phrase anything from later retellings as "in some tellings...".
   - **हिंदी:** write it fresh in natural spoken Hindi (Devanagari) from the same beats, not translated line by line. Keep the same number of beats so one storyboard fits both. Use the Hindi names from the research file.
   - **Length budget (both languages ≤ 60 s including the 1 s sting):** EN ≤ ~140 words (the S01E01 voice reads ~2.45 words/s), HI ≤ ~140 words. Hindi narration runs ~20% longer than the English for the same beats (S01E01: EN 148 words = 61.7 s, HI 183 words = 73.3 s), so write the Hindi tight from the start.
   - Fill in the word count and estimated read time for **each** language, and list 2–3 ready cuts per language in case the voice comes out long.
4. Update Stage in `episodes/INDEX.md` to `2 Script (needs read-aloud)`.
5. Show the user the English hook line and the Hindi hook line, and remind them to read both aloud before `/storyboard <ID>`.
