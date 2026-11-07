// Stage 5: narration. Generates one clip per script beat, joins them with pauses and writes
//   episodes/<folder>/audio/<lang>.mp3
//   episodes/<folder>/audio/<lang>.timestamps.json   { words: [{ beat, text, start, end }] }
// which the renderer picks up automatically (timing + audio).
//
//   npm run voice -- S01E01 en                              free draft voice (macOS "say")
//   npm run voice -- S01E01 hi --provider elevenlabs --voice <VOICE_ID>
//   npm run voice -- S01E01 en --provider elevenlabs --voice <ID> --speed 1.05 --beat 9   redo one beat
//
// ElevenLabs needs ELEVENLABS_API_KEY in your environment (never put the key in a file here).
// Clips are cached per beat: unchanged text + voice settings are never regenerated (no extra credits).
import { spawnSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const STUDIO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ROOT = path.resolve(STUDIO, '..');
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : d; };
const positional = argv.filter((a, i) => !a.startsWith('--') && !argv[i - 1]?.startsWith('--'));
const [ep, lang] = positional;
if (!ep || !['en', 'hi'].includes(lang)) {
  console.error('usage: npm run voice -- <EPISODE_ID> <en|hi> [--provider say|elevenlabs] [--voice ID] [--model ID] [--speed 1.0] [--beat N]');
  process.exit(1);
}
const provider = opt('provider', 'say');
const DRAFT_VOICES = { en: 'Rishi', hi: 'Lekha' };
const voice = opt('voice', provider === 'say' ? DRAFT_VOICES[lang] : undefined);
const model = opt('model', 'eleven_multilingual_v2');
const speed = Number(opt('speed', '1'));
const onlyBeat = opt('beat') ? Number(opt('beat')) : null;
if (provider === 'elevenlabs' && !voice) { console.error('--voice <VOICE_ID> is required for ElevenLabs'); process.exit(1); }
if (provider === 'elevenlabs' && !process.env.ELEVENLABS_API_KEY) { console.error('Set ELEVENLABS_API_KEY in your shell first.'); process.exit(1); }

// pauses between beats (seconds)
const GAP = 0.35;
const GAP_DRAMATIC = 0.65; // after … or ?
const LEAD = 0.15;

// ---- find the episode ----
const epRoot = path.join(ROOT, 'episodes');
const folder = fs.readdirSync(epRoot).find((d) => {
  const p = path.join(epRoot, d, '03-scenes.json');
  return fs.existsSync(p) && JSON.parse(fs.readFileSync(p, 'utf8')).id === ep;
});
if (!folder) { console.error(`episode ${ep} not found`); process.exit(1); }
const spec = JSON.parse(fs.readFileSync(path.join(epRoot, folder, '03-scenes.json'), 'utf8'));
const audioDir = path.join(epRoot, folder, 'audio');
const clipDir = path.join(audioDir, lang);
fs.mkdirSync(clipDir, { recursive: true });

// beats in order + silence owed to fixed-duration scenes (e.g. the 1 s series sting)
const beats = [];
let pendingSilence = 0;
for (const sc of spec.scenes) {
  const text = (sc.narration?.[lang] ?? '').trim();
  if (sc.fixedDurationSec) { pendingSilence += sc.fixedDurationSec; continue; }
  if (!text) continue;
  beats.push({ beat: sc.beat, text, silenceBefore: pendingSilence });
  pendingSilence = 0;
}

const run = (cmd, args, opts = {}) => {
  const r = spawnSync(cmd, args, { cwd: STUDIO, encoding: 'utf8', ...opts });
  if (r.status !== 0) { console.error(r.stderr || r.stdout); throw new Error(`${cmd} ${args[0]} failed`); }
  return r.stdout;
};
const ffmpeg = (args) => run('npx', ['remotion', 'ffmpeg', '-v', 'error', '-y', ...args]);
const duration = (file) => Number(run('npx', ['remotion', 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]).trim());
const tokens = (s) => s.split(/\s+/).filter(Boolean);

// Estimated word times inside a clip (draft voice has no alignment): proportional to word length.
function estimateWords(text, dur) {
  const t = tokens(text);
  const w = t.map((x) => x.replace(/[^\p{L}\p{N}]/gu, '').length + 2);
  const sum = w.reduce((a, b) => a + b, 0);
  const speech = Math.max(0.2, dur - 0.12);
  let at = 0.06;
  return t.map((text, i) => { const d = (w[i] / sum) * speech; const r = { text, start: at, end: at + d }; at += d; return r; });
}

// ElevenLabs character alignment -> words (split on whitespace, same as the script's tokens).
function wordsFromAlignment(al) {
  const out = [];
  let cur = null;
  al.characters.forEach((ch, i) => {
    if (/\s/.test(ch)) { if (cur) { out.push(cur); cur = null; } return; }
    const s = al.character_start_times_seconds[i];
    const e = al.character_end_times_seconds[i];
    if (!cur) cur = { text: ch, start: s, end: e };
    else { cur.text += ch; cur.end = e; }
  });
  if (cur) out.push(cur);
  return out;
}

async function makeClip(b, i) {
  const base = path.join(clipDir, `beat-${String(b.beat).padStart(2, '0')}`);
  const settings = { provider, voice, model: provider === 'elevenlabs' ? model : null, speed, text: b.text };
  const hash = crypto.createHash('sha1').update(JSON.stringify(settings)).digest('hex').slice(0, 12);
  const metaPath = `${base}.json`;
  if (fs.existsSync(metaPath) && (onlyBeat === null || onlyBeat !== b.beat)) {
    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
    if (meta.hash === hash && fs.existsSync(meta.wav)) return meta;
  }
  const wav = `${base}.wav`;
  let words;
  if (provider === 'say') {
    // macOS "say" writes compressed AIFF-C by default, which ffmpeg can't read: ask for plain WAV
    const rate = Math.round((lang === 'en' ? 175 : 165) * speed);
    run('say', ['-v', voice, '-r', String(rate), '-o', wav, '--data-format=LEI16@44100', b.text]);
    words = estimateWords(b.text, duration(wav));
  } else {
    const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voice)}/with-timestamps?output_format=mp3_44100_128`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'xi-api-key': process.env.ELEVENLABS_API_KEY },
      body: JSON.stringify({
        text: b.text,
        model_id: model,
        voice_settings: { stability: 0.5, similarity_boost: 0.75, style: 0.25, speed, use_speaker_boost: true },
        previous_text: beats[i - 1]?.text ?? null,
        next_text: beats[i + 1]?.text ?? null,
        seed: 1000 + b.beat,
      }),
    });
    if (!res.ok) throw new Error(`ElevenLabs ${res.status}: ${await res.text()}`);
    const data = await res.json();
    const mp3 = `${base}.mp3`;
    fs.writeFileSync(mp3, Buffer.from(data.audio_base64, 'base64'));
    ffmpeg(['-i', mp3, '-ar', '44100', '-ac', '1', wav]);
    words = wordsFromAlignment(data.alignment);
  }
  const expected = tokens(b.text).length;
  if (words.length !== expected) console.warn(`  beat ${b.beat}: ${words.length} words timed vs ${expected} in script (captions may drift)`);
  const meta = { beat: b.beat, hash, wav, duration: duration(wav), words };
  fs.writeFileSync(metaPath, JSON.stringify(meta, null, 1));
  console.log(`  beat ${b.beat}: ${meta.duration.toFixed(2)}s`);
  return meta;
}

console.log(`voice: ${ep} ${lang} via ${provider}${voice ? ` (${voice})` : ''}${speed !== 1 ? ` speed ${speed}` : ''}`);
const clips = [];
for (let i = 0; i < beats.length; i++) clips.push(await makeClip(beats[i], i));

// ---- assemble: [silence][clip][gap][clip]... with global word times ----
const parts = [];
const words = [];
let t = 0;
const silence = (sec) => {
  const f = path.join(clipDir, `sil-${Math.round(sec * 1000)}.wav`);
  if (!fs.existsSync(f)) ffmpeg(['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', sec.toFixed(3), f]);
  parts.push(f);
  t += sec;
};
clips.forEach((c, i) => {
  const b = beats[i];
  const before = i === 0 ? b.silenceBefore + LEAD : b.silenceBefore + (/[…?]["”]?$/.test(beats[i - 1].text) ? GAP_DRAMATIC : GAP);
  silence(before);
  for (const w of c.words) words.push({ beat: c.beat, text: w.text, start: +(t + w.start).toFixed(3), end: +(t + w.end).toFixed(3) });
  parts.push(c.wav);
  t += c.duration;
});
silence(0.4);

const listFile = path.join(clipDir, 'concat.txt');
fs.writeFileSync(listFile, parts.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join('\n'));
const outMp3 = path.join(audioDir, `${lang}.mp3`);
ffmpeg(['-f', 'concat', '-safe', '0', '-i', listFile, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-ac', '2', '-b:a', '192k', outMp3]);
fs.writeFileSync(
  path.join(audioDir, `${lang}.timestamps.json`),
  JSON.stringify({ episode: ep, lang, provider, voice, model: provider === 'elevenlabs' ? model : null, speed, draft: provider === 'say', total: +t.toFixed(3), words }, null, 1),
);
console.log(`→ ${outMp3}  (${t.toFixed(1)}s, ${words.length} words timed${provider === 'say' ? ', DRAFT voice: word times estimated inside each beat' : ''})`);
