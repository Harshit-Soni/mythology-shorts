// Render an episode (or one scene, or stills) into episodes/<folder>/render/.
//
//   npm run render -- S01E01 en                  full preview (debug labels on)
//   npm run render -- S01E01 hi --final          final video (no debug labels)
//   npm run render -- S01E01 en --scene s09      just one scene
//   npm run render -- S01E01 en --stills         one PNG per scene (mid-scene) for quick review
//   add --variant illustrated                    the painted-stills version (illustrated/03-shots.json)
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const STUDIO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ROOT = path.resolve(STUDIO, '..');
const args = process.argv.slice(2);
const [ep, lang = 'en'] = args.filter((a) => !a.startsWith('--') && !['--scene', '--variant'].includes(args[args.indexOf(a) - 1]));
const flag = (n) => args.includes(`--${n}`);
const opt = (n) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : undefined; };
if (!ep || !['en', 'hi'].includes(lang)) {
  console.error('usage: npm run render -- <EPISODE_ID> <en|hi> [--final] [--scene <id>] [--stills]');
  process.exit(1);
}

const run = (cmd, a) => {
  const r = spawnSync(cmd, a, { cwd: STUDIO, stdio: 'inherit' });
  if (r.status !== 0) process.exit(r.status ?? 1);
};
run('node', ['scripts/prepare.mjs']);

const { EPISODES } = await import(path.join(STUDIO, 'src/generated/data.ts'));
const { buildTimeline } = await import(path.join(STUDIO, 'src/lib/timing.ts'));
const { buildShotTimeline } = await import(path.join(STUDIO, 'src/lib/shotTiming.ts'));
const entry = EPISODES[ep];
if (!entry) { console.error(`episode ${ep} not found`); process.exit(1); }
const fps = entry.spec.fps;
const variant = opt('variant'); // undefined = cut-out version, 'illustrated' = painted stills
if (variant && variant !== 'illustrated') { console.error(`unknown variant ${variant}`); process.exit(1); }
if (variant && !entry.shots) { console.error(`${ep} has no illustrated/03-shots.json`); process.exit(1); }
const tl = variant
  ? (() => { const t = buildShotTimeline(entry, lang, buildTimeline(entry, lang)); return { ...t, estimated: false, segments: t.segments.map((s) => ({ ...s, scene: { id: s.shot.id } })) }; })()
  : buildTimeline(entry, lang);
const tag = variant ? `-${variant}` : '';
const outDir = path.join(ROOT, 'episodes', entry.folder, 'render');
fs.mkdirSync(outDir, { recursive: true });
const comp = `${ep}${tag}-${lang}`;
const final = flag('final');
const props = JSON.stringify({ episodeId: ep, lang, debug: !final });
const rem = (a) => run('npx', ['remotion', ...a, `--props=${props}`]);

if (flag('stills')) {
  const dir = path.join(outDir, `stills${tag}-${lang}`);
  fs.mkdirSync(dir, { recursive: true });
  for (const s of tl.segments) {
    const frame = Math.round(((s.start + s.end) / 2) * fps);
    rem(['still', 'src/index.ts', comp, path.join(dir, `${s.scene.id}.png`), `--frame=${frame}`]);
  }
  console.log(`stills → ${dir}`);
} else if (opt('scene')) {
  const id = opt('scene');
  const s = tl.segments.find((x) => x.scene.id === id);
  if (!s) { console.error(`scene ${id} not in timeline`); process.exit(1); }
  const a = Math.round(s.start * fps);
  const b = Math.max(a, Math.round(s.end * fps) - 1);
  const out = path.join(outDir, `${ep}${tag}-${lang}-${id}${final ? '' : '-preview'}.mp4`);
  rem(['render', 'src/index.ts', comp, out, `--frames=${a}-${b}`]);
  console.log(`→ ${out}`);
} else {
  const out = path.join(outDir, `${ep}${tag}-${lang}${final ? '' : '-preview'}.mp4`);
  rem(['render', 'src/index.ts', comp, out]);
  console.log(`→ ${out}  (${tl.total.toFixed(1)}s, ${tl.estimated ? 'estimated timing: no voice track yet' : 'timed from voice track'})`);
}
