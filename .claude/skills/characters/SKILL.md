---
name: characters
description: Stage 4 of the pipeline. Create the new SVG character puppets, backgrounds and props an episode's storyboard needs, following the asset spec and style guide.
argument-hint: <episode-id> [only <asset-id>]
---

Build the assets for episode $ARGUMENTS.

1. Read the episode's `03-scenes.json` (the `assets` block), `01-research.md` (for how characters should look), `STYLE_GUIDE.md` and `assets/characters/SPEC.md`.
2. For each asset marked `new`, or only the one named in the arguments:
   - **Character:** write `character.json` first. Base `look` on the research and traditional iconography, and record where it comes from in `sourceNotes`. Then draw `<id>.svg` exactly as the spec says: named groups, `data-pivot` on movable parts, the outline colour, palette colours.
   - **Background:** `assets/backgrounds/<id>.svg`, 1080×1920, split into `<g id="layer-far">`, `layer-mid` and `layer-ground` for parallax.
   - **Prop:** `assets/props/<id>.svg`, centred and transparent.
3. Render a PNG preview of each new SVG (e.g. `rsvg-convert` if installed, otherwise headless Chrome) and look at it. Fix anything that looks broken or off-style before calling it done.
4. Add the episode ID to `appearsIn` for every library character used. In `03-scenes.json`, mark the new assets `library`.
5. Update Stage in `episodes/INDEX.md` to `4 Assets`.
6. Show the user the previews and ask for feedback on the character designs before going further.
