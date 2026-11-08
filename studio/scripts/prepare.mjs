// Copies the asset library + episode specs into the studio and writes src/generated/data.ts.
// For every character pose with face groups it also writes 4 face variants
// (eyes open/closed x mouth closed/open) so blinking and talking are plain image swaps.
//
// Usage: node scripts/prepare.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const STUDIO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ROOT = path.resolve(STUDIO, '..');
const PUB = path.join(STUDIO, 'public');
const OUT_ASSETS = path.join(PUB, 'assets');
const OUT_EPISODES = path.join(PUB, 'episodes');
const GEN = path.join(STUDIO, 'src', 'generated');

const rm = (p) => fs.rmSync(p, { recursive: true, force: true });
const mkdir = (p) => fs.mkdirSync(p, { recursive: true });
const rel = (p) => path.relative(PUB, p).split(path.sep).join('/');

rm(OUT_ASSETS);
rm(OUT_EPISODES);
mkdir(OUT_ASSETS);
mkdir(OUT_EPISODES);
mkdir(GEN);

const viewBoxOf = (svg) => {
  const m = svg.match(/viewBox="([\d.\s-]+)"/);
  if (!m) return null;
  const [, , w, h] = m[1].trim().split(/\s+/).map(Number);
  return { w, h };
};

// Set a <g id="..."> group's visibility in an SVG string.
function setGroupVisible(svg, id, visible) {
  const re = new RegExp(`<g\\b[^>]*\\bid="${id}"[^>]*>`);
  const m = svg.match(re);
  if (!m) return svg;
  let tag = m[0];
  tag = tag.replace(/style="([^"]*)"/, (_, s) => {
    const rest = s.replace(/display\s*:\s*none\s*;?/g, '').trim();
    return rest ? `style="${rest}"` : '';
  });
  if (!visible) {
    tag = /style="/.test(tag)
      ? tag.replace(/style="/, 'style="display:none;')
      : tag.replace(/>$/, ' style="display:none">');
  }
  tag = tag.replace(/\s+>/, '>').replace(/\s{2,}/g, ' ');
  return svg.replace(m[0], tag);
}
const isHidden = (svg, id) =>
  new RegExp(`<g\\b[^>]*\\bid="${id}"[^>]*display\\s*:\\s*none`).test(svg);
const hasGroup = (svg, id) => new RegExp(`<g\\b[^>]*\\bid="${id}"`).test(svg);

const manifest = { characters: {}, backgrounds: {}, props: {}, overlays: {}, sfx: {}, music: {} };

// ---- characters ----
const charRoot = path.join(ROOT, 'assets', 'characters');
for (const cid of fs.existsSync(charRoot) ? fs.readdirSync(charRoot) : []) {
  const dir = path.join(charRoot, cid);
  if (!fs.statSync(dir).isDirectory()) continue;
  const outDir = path.join(OUT_ASSETS, 'characters', cid);
  mkdir(outDir);
  manifest.characters[cid] = {};
  for (const f of fs.readdirSync(dir)) {
    if (!f.endsWith('.svg') || f === 'sheet.svg') continue;
    const key = f.slice(0, -4);
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const vb = viewBoxOf(svg) ?? { w: 1000, h: 1600 };
    const face = ['eyes-open', 'eyes-closed', 'mouth-closed', 'mouth-open'].every((g) => hasGroup(svg, g));
    const base = path.join(outDir, f);
    fs.writeFileSync(base, svg);
    const info = { file: rel(base), w: vb.w, h: vb.h, face, eyes: 'open', mouth: 'closed', variants: {} };
    if (face) {
      info.eyes = isHidden(svg, 'eyes-open') ? 'closed' : 'open';
      info.mouth = isHidden(svg, 'mouth-closed') ? 'open' : 'closed';
      for (const e of ['open', 'closed']) {
        for (const m of ['closed', 'open']) {
          let v = setGroupVisible(svg, 'eyes-open', e === 'open');
          v = setGroupVisible(v, 'eyes-closed', e === 'closed');
          v = setGroupVisible(v, 'mouth-closed', m === 'closed');
          v = setGroupVisible(v, 'mouth-open', m === 'open');
          const out = path.join(outDir, `${key}.e-${e}.m-${m}.svg`);
          fs.writeFileSync(out, v);
          info.variants[`${e}|${m}`] = rel(out);
        }
      }
    }
    manifest.characters[cid][key] = info;
  }
}

// ---- backgrounds / props / overlays (svg or png) ----
for (const kind of ['backgrounds', 'props', 'overlays']) {
  const dir = path.join(ROOT, 'assets', kind);
  if (!fs.existsSync(dir)) continue;
  const outDir = path.join(OUT_ASSETS, kind);
  mkdir(outDir);
  for (const f of fs.readdirSync(dir)) {
    if (!/\.(svg|png)$/.test(f)) continue;
    const id = f.replace(/\.(svg|png)$/, '');
    const out = path.join(outDir, f);
    fs.copyFileSync(path.join(dir, f), out);
    const text = f.endsWith('.svg') ? fs.readFileSync(out, 'utf8') : null;
    const vb = text ? viewBoxOf(text) : null;
    manifest[kind][id] = { file: rel(out), w: vb?.w ?? null, h: vb?.h ?? null };
    // backgrounds with a front layer (e.g. the hermitage hut) get back/front halves so
    // characters can be drawn between them ("frontLayer": true in a scene)
    if (kind === 'backgrounds' && text && hasGroup(text, 'layer-front')) {
      const back = path.join(outDir, `${id}.back.svg`);
      const front = path.join(outDir, `${id}.front.svg`);
      fs.writeFileSync(back, setGroupVisible(text, 'layer-front', false));
      let fr = text;
      for (const g of ['layer-far', 'layer-mid', 'layer-ground']) fr = setGroupVisible(fr, g, false);
      fs.writeFileSync(front, fr);
      manifest[kind][id].back = rel(back);
      manifest[kind][id].front = rel(front);
    }
  }
}

// ---- sound library: sound effects and music beds ----
for (const kind of ['sfx', 'music']) {
  const dir = path.join(ROOT, 'assets', kind);
  if (!fs.existsSync(dir)) continue;
  const outDir = path.join(OUT_ASSETS, kind);
  mkdir(outDir);
  for (const f of fs.readdirSync(dir)) {
    if (!/\.(mp3|wav)$/.test(f)) continue;
    const out = path.join(outDir, f);
    fs.copyFileSync(path.join(dir, f), out);
    manifest[kind][f.replace(/\.(mp3|wav)$/, '')] = { file: rel(out), w: null, h: null };
  }
}

// ---- episodes ----
const episodes = {};
const epRoot = path.join(ROOT, 'episodes');
for (const d of fs.readdirSync(epRoot)) {
  const specPath = path.join(epRoot, d, '03-scenes.json');
  if (!fs.existsSync(specPath)) continue;
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  if (!spec.scenes?.length) continue;
  const audio = {};
  for (const lang of ['en', 'hi']) {
    const mp3 = path.join(epRoot, d, 'audio', `${lang}.mp3`);
    const ts = path.join(epRoot, d, 'audio', `${lang}.timestamps.json`);
    if (fs.existsSync(mp3) && fs.existsSync(ts)) {
      const outDir = path.join(OUT_EPISODES, spec.id);
      mkdir(outDir);
      fs.copyFileSync(mp3, path.join(outDir, `${lang}.mp3`));
      audio[lang] = { file: `episodes/${spec.id}/${lang}.mp3`, timestamps: JSON.parse(fs.readFileSync(ts, 'utf8')) };
    }
  }
  // illustrated version: copy each shot's approved image
  let shots;
  const shotsPath = path.join(epRoot, d, 'illustrated', '03-shots.json');
  if (fs.existsSync(shotsPath)) {
    shots = JSON.parse(fs.readFileSync(shotsPath, 'utf8'));
    const outDir = path.join(OUT_EPISODES, spec.id, 'shots');
    mkdir(outDir);
    for (const sh of shots.shots) {
      if (!sh.image) continue;
      const src = path.join(epRoot, d, 'illustrated', sh.image);
      if (!fs.existsSync(src)) { console.warn(`prepare: ${sh.id} image not found: ${sh.image}`); continue; }
      const out = path.join(outDir, `${sh.id}${path.extname(src)}`);
      fs.copyFileSync(src, out);
      sh.file = rel(out);
    }
  }
  episodes[spec.id] = { folder: d, spec, audio, ...(shots ? { shots } : {}) };
}

fs.writeFileSync(
  path.join(GEN, 'data.ts'),
  `// GENERATED by scripts/prepare.mjs. Do not edit.\n` +
    `import type { Manifest, EpisodeEntry } from '../lib/types';\n` +
    `export const MANIFEST: Manifest = ${JSON.stringify(manifest, null, 1)};\n` +
    `export const EPISODES: Record<string, EpisodeEntry> = ${JSON.stringify(episodes, null, 1)};\n`,
);

const nChar = Object.values(manifest.characters).reduce((a, c) => a + Object.keys(c).length, 0);
console.log(
  `prepare: ${Object.keys(manifest.characters).length} characters (${nChar} poses), ` +
    `${Object.keys(manifest.backgrounds).length} backgrounds, ${Object.keys(manifest.props).length} props, ` +
    `${Object.keys(manifest.overlays).length} overlays; episodes: ${Object.keys(episodes).join(', ')}`,
);
