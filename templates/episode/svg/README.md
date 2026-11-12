# Cut-out SVG version: {{ID}}

Files only the SVG version uses. Stage 4 (`/assets {{ID}}`) writes them here:
- `04-asset-brief.md`: style block, specs and a description of every new SVG puppet, background and prop
- `04-concept-brief.md`: concept rounds for anything with no approved precedent
- `04-asset-review.md`: the review of every delivery and the fixes made

Approved assets go into the shared library (`assets/characters`, `assets/backgrounds`, `assets/props`, `assets/overlays`).
Render: `cd studio && npm run render -- {{ID}} en --final` → `render/{{ID}}-en.mp4`
