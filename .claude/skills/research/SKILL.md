---
name: research
description: Stage 1 of the pipeline. Research an episode's story from primary sources and fill 01-research.md with cited events, version differences and hook candidates.
argument-hint: <episode-id>
---

Research episode $ARGUMENTS.

1. Find `episodes/$ARGUMENTS-*/`. Read its `00-idea.md`, the series' `series.md` if it has one, `CLAUDE.md` and `LEARNINGS.md`.
2. Search the web for the story in **primary sources first**: the Ganguli Mahabharata (sacred-texts.com), the BORI critical edition notes, the Valmiki Ramayana (valmiki.iitk.ac.in) and Puranas (wisdomlib.org). Then check secondary and pop-culture versions only to note how they differ.
3. Fill in `01-research.md`:
   - **The story** table: every event the script could use, with the exact source location (text, parva or kanda, chapter or section) and a link. Leave `Verified` unchecked; the user checks those.
   - **Versions:** keep scripture, regional/folk and TV/pop-culture versions clearly apart. Say which popular details are *not* in the core text.
   - **Hook candidates:** 3 to 5 surprising and *true* angles.
   - **Names:** English and Devanagari spellings for every character and place.
4. Never fill gaps from memory without a source. If something can't be sourced, write `UNSOURCED` next to it.
5. Update the episode's Stage in `episodes/INDEX.md` to `1 Research (needs verify)`.
6. Tell the user which 3 to 5 claims matter most and need checking (with links), and that after checking them the next step is `/script <ID>`.
