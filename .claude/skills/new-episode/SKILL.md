---
name: new-episode
description: Stage 0 of the pipeline. Turn a new story idea into an episode folder from the template and register it in episodes/INDEX.md.
argument-hint: <one-line idea> [series id, e.g. S01]
---

Start a new episode for the idea: $ARGUMENTS

1. Read `PIPELINE.md` and `episodes/INDEX.md`.
2. Decide the ID:
   - If the idea belongs to a series in `series/` (or the user named one), use the next free `SxxEyy` and match it to the episode table in that series' `series.md`.
   - Otherwise use the next free `Xnnn`.
3. Pick a short kebab-case slug (e.g. `mandavya-curses-yama`).
4. Copy `templates/episode/` to `episodes/<ID>-<slug>/` (it includes the `svg/` and `illustrated/` version folders, so both flows can run for every episode without touching each other). Fill in `00-idea.md` (ID, title, series, idea, why it works, today's date), replace `{{ID}}` / `{{TITLE}}` in the README files, and leave the other files as templates.
5. Add a row to `episodes/INDEX.md` with Stage = `0 Idea`.
6. In 3 to 5 lines, tell the user: the folder created, the angle you'd take, and that the next step is `/research <ID>`.
