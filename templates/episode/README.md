# {{ID}}: {{TITLE}}

One story, made in one or more visual versions. The story files, beats and voice are shared; each version keeps its own folder and never edits the other's.

```
{{ID}}-<slug>/
│  SHARED BY EVERY VERSION
├─ 00-idea.md          idea, status, open items
├─ 01-research.md      cited sources
├─ 02-script.md        EN + HI script (numbered beats)
├─ 03-scenes.json      beats + narration (both versions time themselves from it), the sound plan,
│                      and the SVG version's staging (the illustrated version ignores the staging)
├─ audio/              en.mp3 / hi.mp3 + word timestamps
├─ 07-publish.md       titles, descriptions, hashtags
├─ 08-review.md        post-publish review
│
├─ svg/                VERSION: CUT-OUT SVG   (asset brief, concepts, review)
├─ illustrated/        VERSION: PAINTED STILLS (shot list, prompts, refs, shots)
└─ render/             MP4s of every version (git-ignored)
```
If the script, beats or voice change, every version needs re-rendering. Otherwise the versions never affect each other.
