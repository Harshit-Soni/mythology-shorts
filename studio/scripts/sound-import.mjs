// Import a generated sound into the library, level-normalised so the mix volumes in
// 03-scenes.json mean the same thing for every file.
//
//   npm run sound:import -- <file> sfx <id>     sound effect → assets/sfx/<id>.m4a   (peak −3 dBFS)
//   npm run sound:import -- <file> music <id>   music bed    → assets/music/<id>.m4a (average −20 dBFS, peak ≤ −1)
//
// Uses macOS afconvert (decode/encode); the gain is applied here.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const [src, kind, id] = process.argv.slice(2);
if (!src || !['sfx', 'music'].includes(kind) || !id) {
  console.error('usage: npm run sound:import -- <file> <sfx|music> <id>');
  process.exit(1);
}
const run = (a) => {
  const r = spawnSync('afconvert', a, { stdio: 'inherit' });
  if (r.status !== 0) process.exit(r.status ?? 1);
};
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sound-import-'));
const wav = path.join(tmp, 'in.wav');
run(['-f', 'WAVE', '-d', 'LEI16@44100', '-c', '2', path.resolve(src), wav]);

// minimal WAV parse (afconvert writes plain PCM chunks)
const buf = fs.readFileSync(wav);
let off = 12, dataOff = -1, dataLen = 0;
while (off < buf.length - 8) {
  const tag = buf.toString('ascii', off, off + 4);
  const len = buf.readUInt32LE(off + 4);
  if (tag === 'data') { dataOff = off + 8; dataLen = Math.min(len, buf.length - dataOff); break; }
  off += 8 + len + (len % 2);
}
if (dataOff < 0) { console.error('no audio data'); process.exit(1); }
const n = dataLen / 2;
const get = (i) => buf.readInt16LE(dataOff + 2 * i);

let peak = 0;
for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(get(i)));
peak /= 32768;
// "active" level: RMS of the louder half of 400 ms windows (ignores silence)
const win = 44100 * 2 * 0.4;
const rms = [];
for (let s = 0; s + win <= n; s += win) {
  let acc = 0;
  for (let i = s; i < s + win; i++) acc += get(i) * get(i);
  rms.push(Math.sqrt(acc / win) / 32768);
}
rms.sort((a, b) => a - b);
const act = rms.slice(Math.floor(rms.length / 2));
const active = act.length ? Math.sqrt(act.reduce((a, r) => a + r * r, 0) / act.length) : peak;
const db = (v) => 20 * Math.log10(Math.max(v, 1e-9));

let gainDb = kind === 'sfx' ? -3 - db(peak) : -20 - db(active);
gainDb = Math.min(gainDb, -1 - db(peak)); // never clip
const g = 10 ** (gainDb / 20);
for (let i = 0; i < n; i++) {
  const v = Math.max(-32768, Math.min(32767, Math.round(get(i) * g)));
  buf.writeInt16LE(v, dataOff + 2 * i);
}
fs.writeFileSync(wav, buf);

const outDir = path.join(ROOT, 'assets', kind);
fs.mkdirSync(outDir, { recursive: true });
for (const ext of ['.mp3', '.wav', '.m4a']) fs.rmSync(path.join(outDir, id + ext), { force: true });
const out = path.join(outDir, `${id}.m4a`);
run(['-f', 'm4af', '-d', 'aac', '-b', kind === 'music' ? '192000' : '160000', wav, out]);
fs.rmSync(tmp, { recursive: true, force: true });
console.log(
  `${kind}/${id}: peak ${db(peak).toFixed(1)} dBFS, active ${db(active).toFixed(1)} dBFS, gain ${gainDb >= 0 ? '+' : ''}${gainDb.toFixed(1)} dB → ${path.relative(ROOT, out)}` +
    (db(peak) < -45 ? '  ⚠ very quiet source: listen before using' : ''),
);
