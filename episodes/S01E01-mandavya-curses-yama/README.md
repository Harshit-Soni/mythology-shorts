# S01E01: The Sage Who Put Dharma on Trial

One story, made in more than one visual version. The story files and the voice are shared, and each version has its own files.

```
S01E01-mandavya-curses-yama/
│  SHARED BY EVERY VERSION
├─ 00-idea.md            idea, status, open items
├─ 01-research.md        cited sources
├─ 02-script.md          EN + HI script (16 beats)
├─ audio/                en.mp3 / hi.mp3 + word timestamps (ElevenLabs)
├─ 07-publish.md         titles, descriptions, hashtags
├─ 08-review.md          post-publish review
│
│  VERSION 1: CUT-OUT SVG (complete: EN 61.7 s, HI 73.3 s)
├─ 03-scenes.json        scene spec the Remotion studio renders
├─ 04-asset-brief.md     brief for the SVG puppets, backgrounds, props
├─ 04-concept-brief.md   concept decisions
├─ 04-asset-review.md    review of every delivery
├─ review/               review sheets, originals kept before fixes
├─ render/               rendered MP4s (git-ignored, rebuilt by `npm run render`)
│
│  VERSION 2: ILLUSTRATED (in progress)
└─ illustrated/
   ├─ 03-shots.json      shot list: one painted image per shot, mapped to the script beats
   └─ images/
      ├─ prompts/        prompts sent to Higgsfield
      ├─ refs/           every character and location sheet try (approved ones are copied to assets/illustrated/)
      ├─ tests/          style tests (the first flat-cartoon try)
      └─ shots/          the shot images: sh01 … sh16
```

**The two versions don't touch each other.** Editing or re-rendering the SVG version uses only the root files plus `assets/characters`, `assets/backgrounds`, `assets/props` and `assets/overlays`, so nothing in `illustrated/` affects it, and the other way round. Both use the same `audio/`, so if the script or voice changes, both versions need updating.

**Going back to the SVG version:**
```
cd studio && npm run render -- S01E01 en
```
The exact state of the finished SVG version is also saved in git as the tag `S01E01-svg-v1`.
