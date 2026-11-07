# Learnings

Lessons from making and publishing episodes. One line per lesson, with the episode it came from. Scripts, storyboards and asset briefs must read this file first.

## Research & accuracy
- Popular retellings often swap details: check the god, the weapon and the numbers against the primary text. S01E01: the epic says **Dharma**, not Yama; a **stake**, not a trident; the age limit is **14** in the critical edition. (S01E01)
- Translations can contradict themselves (Ganguli: "twelfth year" and "fourteen" in one speech): cross-check with the critical edition. (S01E01)

## Script & length
- Hindi narration runs ~20% longer than the English for the same beats: S01E01 EN 148 words = 61.7 s, HI 183 words = 73.3 s. Budget ≤ ~140 words per language for ≤ 60 s. (S01E01)

## Assets
- Generators keep a style once batch 1 is approved: always do the main characters first, and give later batches the approved files as references. (S01E01)
- Make expressions about twice as strong as feels natural; open mouths must show through beards; every pose must read as a silhouette; held objects must be unambiguous (a cloth read as a blade). (S01E01 batch 1)
- Silhouettes can accidentally form religious symbols (a figure on a pole read as a cross). Check every silhouette. (S01E01)
- Deities: shocked faces can tip into slapstick (round "googly" eyes). Keep the eye shape and widen it instead. (S01E01)
- Facing: judge by the ear rule (the visible ear is the back of the head), and only zoomed in. Thumbnails misled us into "fixing" three poses that were correct. (S01E01)
- Concept PNG first for anything with no approved example (architecture, the signature border). Test overlays opaque at phone size over a real scene. (S01E01)
- Name the architecture rule explicitly (classical ancient Indian: carved pillars, chaitya arches, nagara spires; no onion domes or pointed arches). (S01E01)
- Silhouette vultures with scalloped wings read as bats: specify straight-edged wings with "finger" feathers. (S01E01 batch 3)

## Storyboard & render
- Characters float unless their `y` sits on the background's measured ground line: measure every new background (GROUND_LINES.md). (S01E01)
- Never mirror a character who must walk the other way: the movement follows facing. (S01E01 s05)
- Characters hiding behind something need a `layer-front` in the background, `frontLayer: true`, and a smaller scale (they're further away). (S01E01 s03)
- Insert shots share their parent's beat: they must have empty narration, or real-audio timing duplicates words and desyncs everything after. (S01E01, fixed in the studio)

## Voice
- ElevenLabs free tier: the shared queue is often busy. Generate one take at a time and retry later; failed takes aren't charged. (S01E01)
- Pause-based alignment (`voice:import ... auto`) worked well for beats separated by paragraph breaks: all pauses were accounted for in EN and HI. (S01E01)

## Hooks
- *(none yet: fill in after the first published episodes)*

## Topics & titles
- Reference signal (another channel, not ours): on The Knowledge Stream, mythology-figure videos (Garuda ~412k, Ashwatthama ~122k) far outperformed their history and general-knowledge videos (2k–19k), as of Nov 2026.
