// Stage 5 (ElevenLabs flow route): import one finished narration take + its Scribe word transcript.
//
//   npm run voice:import -- S01E01 en <take.mp3> <transcript.json>
//   npm run voice:import -- S01E01 en <take.mp3> auto      (free: beats from pauses, words estimated)
//
// transcript.json = Scribe words: [{ "text": "The", "start": 0.12, "end": 0.25 }, ...]
//   (a { words: [...] } object is accepted too; non-word entries such as spacing are ignored)
//
// Every script word is matched to a spoken word (order-preserving alignment), so captions,
// cues and lip-sync use the script's own words even if the transcript spells something
// differently. Unmatched script words get times interpolated from their neighbours.
// Writes episodes/<folder>/audio/<lang>.mp3 (with silence added for the series sting)
// and audio/<lang>.timestamps.json, which the renderer picks up automatically.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const STUDIO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ROOT = path.resolve(STUDIO, '..');
const [ep, lang, takePath, transcriptPath] = process.argv.slice(2);
if (!ep || !['en', 'hi'].includes(lang) || !takePath || !transcriptPath) {
  console.error('usage: npm run voice:import -- <EPISODE_ID> <en|hi> <take.mp3> <transcript.json>');
  process.exit(1);
}
const LEAD = 0.15; // silence before the first word, after any fixed-duration opening scenes

const epRoot = path.join(ROOT, 'episodes');
const folder = fs.readdirSync(epRoot).find((d) => {
  const p = path.join(epRoot, d, '03-scenes.json');
  return fs.existsSync(p) && JSON.parse(fs.readFileSync(p, 'utf8')).id === ep;
});
if (!folder) { console.error(`episode ${ep} not found`); process.exit(1); }
const spec = JSON.parse(fs.readFileSync(path.join(epRoot, folder, '03-scenes.json'), 'utf8'));

// script tokens in order, with their beat; silence owed to opening fixed scenes (series sting)
const script = [];
let opening = 0;
let seenWords = false;
for (const sc of spec.scenes) {
  if (sc.fixedDurationSec && !seenWords) opening += sc.fixedDurationSec;
  for (const t of (sc.narration?.[lang] ?? '').split(/\s+/).filter(Boolean)) {
    script.push({ beat: sc.beat, text: t });
    seenWords = true;
  }
}

// normalise for matching: lower-case, strip punctuation and quotes; numbers → words for English
const NUM = { '14': 'fourteen', '12': 'twelve' };
const norm = (s) => {
  let x = s.toLowerCase().replace(/[“”"'‘’.,!?…:;।()\-—]/g, '').trim();
  if (lang === 'en' && NUM[x]) x = NUM[x];
  return x;
};

let timed;
let matched;
let n = script.length;
if (transcriptPath === 'auto') {
  ({ timed, matched } = autoAlign());
} else {
  const raw = JSON.parse(fs.readFileSync(transcriptPath, 'utf8'));
  const spoken = (Array.isArray(raw) ? raw : raw.words ?? raw.transcripts?.[0]?.words ?? [])
    .filter((w) => (w.type ?? 'word') === 'word' && String(w.text ?? '').trim())
    .map((w) => ({ text: String(w.text).trim(), start: Number(w.start), end: Number(w.end) }));
  if (!spoken.length) { console.error('no words in transcript'); process.exit(1); }

  const A = script.map((w) => norm(w.text));
  const B = spoken.map((w) => norm(w.text));

  // order-preserving alignment (LCS with fuzzy equality: exact, or one is a prefix of the other)
  const same = (a, b) => a && b && (a === b || (a.length > 2 && b.length > 2 && (a.startsWith(b) || b.startsWith(a))));
  n = A.length;
  const m = B.length;
  const dp = Array.from({ length: n + 1 }, () => new Int32Array(m + 1));
  for (let i = n - 1; i >= 0; i--)
    for (let j = m - 1; j >= 0; j--)
      dp[i][j] = same(A[i], B[j]) ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
  const match = new Array(n).fill(-1);
  for (let i = 0, j = 0; i < n && j < m; ) {
    if (same(A[i], B[j])) { match[i] = j; i++; j++; }
    else if (dp[i + 1][j] >= dp[i][j + 1]) i++;
    else j++;
  }

  // fill unmatched script words by interpolating between matched neighbours
  timed = script.map((w, i) => (match[i] >= 0 ? { ...w, start: spoken[match[i]].start, end: spoken[match[i]].end } : { ...w }));
  for (let i = 0; i < n; i++) {
    if (timed[i].start !== undefined) continue;
    let k = i;
    while (k < n && timed[k].start === undefined) k++;
    const prevEnd = i > 0 ? timed[i - 1].end : 0;
    const nextStart = k < n ? timed[k].start : spoken[m - 1].end;
    const step = (nextStart - prevEnd) / (k - i);
    for (let q = i; q < k; q++) { timed[q].start = prevEnd + step * (q - i); timed[q].end = timed[q].start + step * 0.9; }
  }
  matched = match.filter((x) => x >= 0).length;
}

// Free alignment without a transcript: beat boundaries = the pauses that best fit the expected
// beat lengths (from text length), words spread over each beat's speech, skipping internal pauses.
function autoAlign() {
  const ff = spawnSync('npx', ['remotion', 'ffmpeg', '-hide_banner', '-i', path.resolve(takePath), '-af', 'silencedetect=noise=-35dB:d=0.2', '-f', 'null', '-'], { cwd: STUDIO, encoding: 'utf8' });
  const log = ff.stderr;
  const sil = [];
  for (const m of log.matchAll(/silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)/g)) sil.push({ s: +m[1], e: +m[2] });
  const dur = Number(spawnSync('npx', ['remotion', 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path.resolve(takePath)], { cwd: STUDIO, encoding: 'utf8' }).stdout.trim());
  const speechStart = sil.length && sil[0].s < 0.05 ? sil.shift().e : 0;
  const speechEnd = sil.length && sil[sil.length - 1].e > dur - 0.05 ? sil.pop().s : dur;
  const beats = [...new Set(script.map((w) => w.beat))];
  const weight = (b) => script.filter((w) => w.beat === b).reduce((a, w) => a + norm(w.text).length + 3, 0) + 6;
  const W = beats.map(weight);
  const Wsum = W.reduce((a, b) => a + b, 0);
  const K = beats.length - 1; // boundaries to choose
  const S = sil.length;
  if (S < K) throw new Error(`only ${S} pauses found for ${K} beat boundaries; use a Scribe transcript instead`);
  const total = speechEnd - speechStart;
  const mid = (x) => (x.s + x.e) / 2;
  // dp[k][i] = best cost using silence i as boundary k
  const INF = 1e18;
  const cost = Array.from({ length: K }, () => new Float64Array(S).fill(INF));
  const from = Array.from({ length: K }, () => new Int32Array(S).fill(-1));
  const segCost = (a, b, k) => { const exp = (W[k] / Wsum) * total; const d = b - a; return ((d - exp) / exp) ** 2; };
  const bonus = (x) => -0.15 * Math.min(1, (x.e - x.s) / 0.6);
  for (let i = 0; i < S; i++) cost[0][i] = segCost(speechStart, mid(sil[i]), 0) + bonus(sil[i]);
  for (let k = 1; k < K; k++)
    for (let i = k; i < S; i++)
      for (let j = k - 1; j < i; j++) {
        const c = cost[k - 1][j] + segCost(mid(sil[j]), mid(sil[i]), k) + bonus(sil[i]);
        if (c < cost[k][i]) { cost[k][i] = c; from[k][i] = j; }
      }
  let best = -1;
  let bestC = INF;
  for (let i = K - 1; i < S; i++) { const c = cost[K - 1][i] + segCost(mid(sil[i]), speechEnd, K); if (c < bestC) { bestC = c; best = i; } }
  const chosen = [];
  for (let k = K - 1, i = best; k >= 0; i = from[k][i], k--) chosen.unshift(i);
  const bounds = [speechStart, ...chosen.map((i) => sil[i]), speechEnd];
  const out = [];
  beats.forEach((b, k) => {
    const a = k === 0 ? speechStart : bounds[k].e;
    const z = k === K ? speechEnd : bounds[k + 1].s;
    // speech intervals inside the beat (minus its internal pauses)
    const inner = sil.filter((x) => x.s > a && x.e < z && !chosen.some((ci) => sil[ci] === x));
    const spans = [];
    let cur = a;
    for (const x of inner) { spans.push([cur, x.s]); cur = x.e; }
    spans.push([cur, z]);
    const speech = spans.reduce((t, [p, q]) => t + (q - p), 0);
    const ws = script.filter((w) => w.beat === b);
    const wt = ws.map((w) => norm(w.text).length + 2);
    const wsum = wt.reduce((x, y) => x + y, 0);
    const at = (t) => { // map speech-time offset -> clock time
      for (const [p, q] of spans) { if (t <= q - p) return p + t; t -= q - p; }
      return z;
    };
    let acc = 0;
    ws.forEach((w, i) => {
      const d = (wt[i] / wsum) * speech;
      out.push({ ...w, start: at(acc + 0.001), end: at(acc + d) });
      acc += d;
    });
    console.log(`  beat ${String(b).padStart(2)}: ${a.toFixed(2)}–${z.toFixed(2)}s (${(z - a).toFixed(2)}s, expected ${((W[k] / Wsum) * total).toFixed(2)}s)`);
  });
  return { timed: out, matched: 'auto (pause-based, no transcript)' };
}

// shift by opening silence: the take's first word lands at (opening + LEAD)
const firstWord = timed[0].start;
const spokenEnd = timed[timed.length - 1].end;
const shift = opening + LEAD - firstWord;
const words = timed.map((w) => ({ beat: w.beat, text: w.text, start: +(w.start + shift).toFixed(3), end: +(w.end + shift).toFixed(3) }));

// audio: pad (or trim) the start so it matches the shifted times; normalise loudness
const audioDir = path.join(epRoot, folder, 'audio');
fs.mkdirSync(audioDir, { recursive: true });
const out = path.join(audioDir, `${lang}.mp3`);
const filter = shift >= 0 ? `adelay=${Math.round(shift * 1000)}:all=1,` : `atrim=start=${(-shift).toFixed(3)},asetpts=PTS-STARTPTS,`;
const r = spawnSync('npx', ['remotion', 'ffmpeg', '-v', 'error', '-y', '-i', path.resolve(takePath), '-af', `${filter}loudnorm=I=-16:TP=-1.5:LRA=11`, '-ar', '44100', '-ac', '2', '-b:a', '192k', out], { cwd: STUDIO, encoding: 'utf8' });
if (r.status !== 0) { console.error(r.stderr); process.exit(1); }
fs.copyFileSync(path.resolve(takePath), path.join(audioDir, `${lang}.take.mp3`));
if (transcriptPath !== 'auto') fs.copyFileSync(path.resolve(transcriptPath), path.join(audioDir, `${lang}.scribe.json`));

const total = words[words.length - 1].end + 0.4;
fs.writeFileSync(
  path.join(audioDir, `${lang}.timestamps.json`),
  JSON.stringify({ episode: ep, lang, source: transcriptPath === 'auto' ? 'elevenlabs-flow, pause-aligned' : 'elevenlabs-flow + scribe', matched: typeof matched === 'string' ? matched : `${matched}/${n}`, total: +total.toFixed(3), words }, null, 1),
);
console.log(`→ ${out}`);
console.log(typeof matched === 'string' ? `  timing: ${matched}; speech ends at ${total.toFixed(1)}s` : `  ${matched}/${n} script words matched to the transcript (${n - matched} interpolated); speech ends at ${total.toFixed(1)}s`);
