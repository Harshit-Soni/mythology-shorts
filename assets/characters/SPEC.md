# Character Sheet Spec (SVG)

Each character is a folder: `assets/characters/<id>/` (id is kebab-case, e.g. `dharma`, `mandavya`).

```
<id>/
  character.json       # metadata (below)
  <pose>.svg           # one SVG file per pose, e.g. standing.svg, walking.svg
  sheet.png            # optional: the approved design sheet, for reference
```

**One file per pose** is easier to get from a generator than one fully rigged puppet. Remotion swaps poses on word cues and adds the motion (breathing, bob, camera).

## SVG rules (every pose file)
- `viewBox="0 0 1000 1600"`, transparent background. The character stands (or sits) on the baseline at **y=1550**, centred at **x=500**. Keep the character's scale the same in every pose (a standing adult's head top is around y=150).
- Flat fills only. Outline `#1E1420`, 3–4 px. 2–3 shades per material. **No** embedded raster images, **no** `<text>`, **no** filters (except a blur on `halo`).
- **Required named groups** in every pose of a speaking or reacting character (Dharma, Mandavya, Vidura, king, guard):

| Group id | Purpose |
|---|---|
| `head` | The whole head |
| `eyes-open` | Visible by default |
| `eyes-closed` | Same position, with `style="display:none"` (swapped in for blinks) |
| `mouth-closed` | Visible by default |
| `mouth-open` | With `style="display:none"` (swapped in for speech) |
| `halo` | Divine characters only, behind the head |

- **Optional groups** (nice to have, not required): `arm-l`, `arm-r`, `body`, `prop-*` (held items). If a generator can't produce named groups, that's fine: deliver the file and I'll split and name the groups myself.

## character.json
```json
{
  "id": "dharma",
  "name": { "en": "Dharma", "hi": "धर्म" },
  "role": "God of justice and righteousness",
  "divine": true,
  "appearsIn": ["S01E01"],
  "look": "Regal, calm, middle-aged; warm golden-brown skin; white and gold garments; gold crown; large gold halo disc behind his head. Not Yama's iconography (no buffalo or noose).",
  "sourceNotes": "The epic gives no fixed visual description of Dharma here; this is a design choice. He is kept visually distinct from Yama on purpose.",
  "poses": ["seated-throne"],
  "expressions": ["neutral", "stern", "shocked"],
  "palette": { "skin": "#B9814F", "garment": "#F3EEDF", "gold": "#E8B53A" }
}
```

## Workflow
1. The episode's `04-asset-brief.md` describes each asset. Generate the files from it.
2. Drop the files into `assets/_inbox/`, named as the brief says.
3. Claude checks them against this spec and `STYLE_GUIDE.md`, fixes groups and naming, writes `character.json`, and moves them into the library.
4. Add the episode ID to `appearsIn`. The character is now in the library for future episodes.
