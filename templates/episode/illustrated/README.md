# Illustrated (painted stills) version: {{ID}}

Files only the illustrated version uses. Style: `styles/ink-wash-graphic-novel.md`.
```
illustrated/
├─ 03-shots.json     one painted image per shot, mapped to the beats in ../03-scenes.json
└─ images/
   ├─ prompts/       prompt sheets (Higgsfield connector, or pasted into the Gemini app by hand)
   ├─ refs/          design refs, character/location sheet tries
   ├─ raw/           images exactly as delivered (e.g. with the Gemini ✦ watermark)
   └─ shots/         the cleaned images the renderer uses
```
Approved sheets and plates go into `assets/illustrated/` (see its README).
Render: `cd studio && npm run render -- {{ID}} en --variant illustrated --final` → `render/{{ID}}-illustrated-en.mp4`
