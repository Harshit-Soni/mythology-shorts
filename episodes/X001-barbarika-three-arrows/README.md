# X001: Barbarika, the Warrior Who Gave His Head

One story, made in two visual versions. The story files, beats and voice are shared; each version keeps its own files and never edits the other's.

```
X001-barbarika-three-arrows/
│  SHARED BY BOTH VERSIONS
├─ 00-idea.md             idea, the Khatu-story decision, status
├─ 01-research.md         cited sources (Skanda Purana, Khatu tradition, Odia and Tamil versions)
├─ 02-script.md           EN + HI script (14 beats)
├─ 03-scenes.json         beats + narration (copied from the script) and the sound plan; both versions
│                         time themselves from it. It also holds the SVG version's staging
│                         (characters, props, camera), which the illustrated version ignores.
├─ 05-voice-direction.md  ElevenLabs takes, direction tags, the beat 9 fix
├─ audio/                 en.mp3 / hi.mp3 + word timestamps (the voice both versions use);
│                         takes/ keeps the raw takes, the beat 9 splice and the tempo fits
├─ 07-publish.md          titles, descriptions, hashtags, comment replies
├─ 08-review.md           post-publish review
│
│  VERSION 1: CUT-OUT SVG (rendered: EN ≈60 s, HI ≈61 s)
├─ svg/
│  ├─ 04-asset-brief.md   brief for the SVG puppets, backgrounds, props (all drawn by Claude as SVG)
│  ├─ 04-concept-brief.md concept notes (skipped: no generator)
│  └─ 04-asset-review.md  review of every asset, fixes made
│     library: assets/characters/{barbarika,brahmin-krishna}, assets/backgrounds, assets/props
│
│  VERSION 2: ILLUSTRATED (rendered: EN ≈60 s, HI ≈61 s)
├─ illustrated/
│  ├─ 03-shots.json       18 painted shots mapped to the beats (camera, fx, cues, text)
│  └─ images/
│     ├─ prompts/         prompt sheets pasted into Gemini (Nano Banana), by hand
│     ├─ refs/            design refs, sheet tries, the peepal plate
│     ├─ raw/             Gemini originals as delivered (with the ✦ watermark)
│     └─ shots/           the cleaned shots the renderer uses (watermark cropped out)
│     library: assets/illustrated/characters/{barbarika,brahmin-krishna}, assets/illustrated/locations/peepal-night
│
└─ render/                MP4s for both versions, with sound; *-voiceonly.mp4 = before the sound pass (git-ignored; rebuilt by npm run render)
```

**Rendering each version** (from `studio/`):
```
npm run render -- X001 en --final                        cut-out SVG   → render/X001-en.mp4
npm run render -- X001 en --variant illustrated --final  illustrated   → render/X001-illustrated-en.mp4
```
Swap `en` for `hi` for the Hindi cut.

**What's shared, and what that means:** if the script, the beats or the voice change, both versions need re-rendering. The sound plan (music bed + effects in `03-scenes.json`) also plays under both. Everything else is version-only: editing `svg/` or the SVG library never changes the illustrated cut, and editing `illustrated/` never changes the SVG cut.
