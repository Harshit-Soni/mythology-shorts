# Mythology & History Shorts Channel

Bilingual (English + Hindi) YouTube Shorts / Instagram Reels telling lesser-known stories from Indian mythology first. Roman and other mythologies or themes may come later. Videos are 2D cut-out animation rendered with Remotion from a JSON scene spec.

## Key files
- `PIPELINE.md`: the 8-stage flow from idea to published Short. Follow it; don't skip stages.
- `STYLE_GUIDE.md`: visual, narration and caption rules.
- `LEARNINGS.md`: lessons from published episodes. Read it before writing scripts or storyboards.
- `series/`: series plans and episode lists.
- `episodes/<ID>-<slug>/`: one folder per episode, files numbered by stage. Shared story files at the root; each visual version in its own subfolder (`svg/` cut-out, `illustrated/` painted stills), so the versions never collide. `episodes/INDEX.md` tracks status.
- `templates/episode/`: the files each new episode starts from.
- `assets/`: the reusable library of characters (SVG puppets, see `assets/characters/SPEC.md`), backgrounds, props and overlays.
- `assets/illustrated/`: the illustrated library of ink-wash character and location reference sheets (for image-based versions; same IDs as the SVG library). See its `README.md`; style in `styles/ink-wash-graphic-novel.md`.
- `studio/`: the Remotion renderer (Stage 6). `npm run render -- <ID> <en|hi>`; see PIPELINE.md → Stage 6. Node comes from Homebrew (`/opt/homebrew/bin`).

## Rules
1. **Accuracy first.** Every key event in a script must trace to a cited source in `01-research.md`. Scripture, regional/folk versions and TV/pop-culture versions are kept clearly apart. If a detail comes from a later or folk retelling, the script says so ("in some tellings...").
2. **Respect.** Deities and sacred figures are shown with dignity: no mockery, no sexualisation, no gore beyond what the story needs, shown symbolically.
3. **Hindi is written, not translated.** Natural spoken Hindi in Devanagari, with Sanskrit names in their proper forms. It must not read as a word-for-word translation of the English.
4. **Reuse before you create.** Check `assets/` before making any new character, background or prop.
5. **Shorts format:** 1080×1920, 45–60 s, hook in the first 2 seconds, captions always on.
