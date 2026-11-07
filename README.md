# Mythology & History Shorts

A pipeline for making bilingual (English + Hindi) YouTube Shorts and Instagram Reels about Indian mythology and history: research → script → storyboard → SVG assets → ElevenLabs narration → Remotion render.

**First episode:** *S01E01, The Sage Who Put Dharma on Trial* (Series 1: *Shraap, Curses That Shaped the Mahabharata*).

## How it works
Each idea goes through 8 stages; each stage writes one file into the episode's folder. See **[PIPELINE.md](PIPELINE.md)** for the full flow.

```
0 Idea → 1 Research → 2 Script → 3 Storyboard → 4 Assets → 5 Voice → 6 Render → 7 Publish → 8 Review
```

The centre of the system is each episode's `03-scenes.json`: a scene spec the renderer reads. Characters are SVG puppets with blink and talk face groups; cues fire effects on specific spoken words; one storyboard renders both languages.

## Layout
| Path | What |
|---|---|
| `PIPELINE.md`, `STYLE_GUIDE.md`, `CLAUDE.md`, `LEARNINGS.md` | Process, visual and narration rules, channel rules, lessons |
| `series/` | Series plans and episode lists |
| `episodes/<ID>-<slug>/` | One folder per episode: research, script, scene spec, asset briefs and reviews, narration audio + word timestamps |
| `assets/` | Reusable library: `characters/` (one SVG per pose + `character.json`), `backgrounds/`, `props/`, `overlays/` |
| `templates/episode/` | Starting files for a new episode |
| `studio/` | Remotion renderer + voice scripts |
| `.claude/skills/` | Claude Code commands for each stage (`/new-episode`, `/research`, `/script`, `/storyboard`, `/characters`, `/publish-kit`) |

## Render an episode
Requires Node.js.
```bash
cd studio
npm install
npm run render -- S01E01 en --final     # → episodes/S01E01-*/render/S01E01-en.mp4
npm run render -- S01E01 hi --final
npm run studio                           # live preview in the browser
```
Rendered videos aren't committed (they're large and rebuildable).

## Narration
Voice: ElevenLabs. Takes are imported with word timings (`npm run voice:import`), or generated beat by beat with an API key in your shell (`npm run voice`). Details in [PIPELINE.md → Stage 5](PIPELINE.md).

## Sources
Story content is researched from primary texts (K. M. Ganguli's public-domain translation of the Mahabharata, cross-checked with the BORI critical edition). Each episode's `01-research.md` cites every event.
