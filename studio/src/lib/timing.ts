import type { Cue, EpisodeEntry, Lang, Scene } from './types';

// Builds the episode timeline: when each scene starts/ends and when each word is spoken.
// Without audio (before Stage 5) word times are ESTIMATED from text length.
// With audio/<lang>.timestamps.json they come from the voice track.

export type Word = {
  text: string;
  start: number; // seconds, absolute
  end: number;
  sceneId: string;
  idx: number; // index within its scene
  inQuote: boolean; // inside "..." -> spoken by an on-screen character
};
export type Segment = { scene: Scene; start: number; end: number; words: Word[] };
export type Timeline = { segments: Segment[]; words: Word[]; total: number; estimated: boolean };

const RATE: Record<Lang, number> = { en: 2.6, hi: 3.0 }; // words per second (Hindi words are shorter)
const LEAD = 0.1; // silence before first word of a beat
const TAIL = 0.3; // pause after last word
const TAIL_DRAMATIC = 0.6; // after … or ?
const MIN_SCENE = 1.2;
const MIN_INSERT = 0.8;

export const tokenize = (s: string) => s.split(/\s+/).filter(Boolean);
export const norm = (s: string) =>
  s.toLowerCase().replace(/[“”"'‘’.,!?…:;।()\-—]/g, '').trim();

function markQuotes(tokens: string[]): boolean[] {
  let open = false;
  return tokens.map((t) => {
    const opens = /^["“]/.test(t);
    const closes = /["”][.,!?…।]*$/.test(t) && !(opens && t.length === 1);
    if (opens) open = true;
    const inside = open;
    if (closes) open = false;
    return inside;
  });
}

function estimateScene(scene: Scene, lang: Lang, t0: number): Segment {
  if (scene.fixedDurationSec) {
    return { scene, start: t0, end: t0 + scene.fixedDurationSec, words: [] };
  }
  const tokens = tokenize(scene.narration[lang] ?? '');
  const quotes = markQuotes(tokens);
  const speech = tokens.length / RATE[lang];
  const weights = tokens.map((t) => norm(t).length + 3);
  const wsum = weights.reduce((a, b) => a + b, 0) || 1;
  let t = t0 + LEAD;
  const words: Word[] = tokens.map((text, idx) => {
    const d = (weights[idx] / wsum) * speech;
    const w = { text, start: t, end: t + d, sceneId: scene.id, idx, inQuote: quotes[idx] };
    t += d;
    // tiny breath after commas / sentence ends
    if (/[,;:]$/.test(text)) t += 0.12;
    if (/[.!?।…]["”]?$/.test(text) && idx < tokens.length - 1) t += 0.25;
    return w;
  });
  const last = tokens[tokens.length - 1] ?? '';
  const tail = /[…?]["”]?$/.test(last) ? TAIL_DRAMATIC : TAIL;
  const end = Math.max(t + tail, t0 + MIN_SCENE);
  return { scene, start: t0, end, words };
}

function fromTimestamps(entry: EpisodeEntry, lang: Lang): Timeline | null {
  const a = entry.audio[lang];
  if (!a) return null;
  const segments: Segment[] = [];
  const all: Word[] = [];
  let t = 0;
  for (const scene of entry.spec.scenes) {
    if (scene.fixedDurationSec) {
      segments.push({ scene, start: t, end: t + scene.fixedDurationSec, words: [] });
      t += scene.fixedDurationSec;
      continue;
    }
    // scenes without narration in this language (e.g. an insert shot sharing a beat) get no words;
    // they're placed by their hard-cut cue below
    if (!tokenize(scene.narration[lang] ?? '').length) continue;
    const raw = a.timestamps.words.filter((w) => w.beat === scene.beat);
    if (!raw.length) continue;
    const quotes = markQuotes(raw.map((w) => w.text));
    const words = raw.map((w, idx) => ({
      text: w.text, start: w.start, end: w.end, sceneId: scene.id, idx, inQuote: quotes[idx],
    }));
    const start = Math.min(t, words[0].start - LEAD);
    segments.push({ scene, start, end: words[words.length - 1].end + TAIL, words });
    all.push(...words);
    t = segments[segments.length - 1].end;
  }
  // close gaps: each segment ends where the next begins
  for (let i = 0; i < segments.length - 1; i++) segments[i].end = segments[i + 1].start;
  return { segments, words: all, total: t, estimated: false };
}

export function cueTime(seg: Segment, cue: Cue, lang: Lang): number {
  const target = norm(cue.onWord?.[lang] ?? '');
  const w = target ? seg.words.find((x) => norm(x.text).includes(target)) : undefined;
  return w ? w.start : seg.start + (seg.end - seg.start) * 0.5;
}

export function buildTimeline(entry: EpisodeEntry, lang: Lang): Timeline {
  const real = fromTimestamps(entry, lang);
  const base: Timeline = real ?? (() => {
    const segments: Segment[] = [];
    let t = 0;
    for (const scene of entry.spec.scenes) {
      const hasWords = tokenize(scene.narration[lang] ?? '').length > 0;
      if (!hasWords && !scene.fixedDurationSec) continue; // insert shot: placed by its hard-cut cue
      const seg = estimateScene(scene, lang, t);
      segments.push(seg);
      t = seg.end;
    }
    return { segments, words: segments.flatMap((s) => s.words), total: t, estimated: true };
  })();

  // Hard cuts: "do": "hard-cut-to", "target": "<sceneId>" splits a beat into scene + insert shot.
  const byId = new Map(entry.spec.scenes.map((s) => [s.id, s]));
  const out: Segment[] = [];
  let shift = 0;
  for (const seg of base.segments) {
    const s = { ...seg, start: seg.start + shift, end: seg.end + shift, words: seg.words.map((w) => ({ ...w, start: w.start + shift, end: w.end + shift })) };
    const cut = seg.scene.cues.find((c) => c.do === 'hard-cut-to' && c.target && byId.has(c.target));
    if (!cut) { out.push(s); continue; }
    const at = cueTime(s, cut, lang);
    let insertEnd = s.end;
    if (insertEnd - at < MIN_INSERT) {
      // estimated timing: just add time. Real audio: never add time (it would desync the voice);
      // the insert borrows from the next scene's opening pause instead.
      if (base.estimated) shift += MIN_INSERT - (insertEnd - at);
      insertEnd = at + MIN_INSERT;
    }
    out.push({ ...s, end: at });
    out.push({ scene: byId.get(cut.target!)!, start: at, end: insertEnd, words: [] });
  }
  if (!base.estimated) for (let i = 1; i < out.length; i++) if (out[i].start < out[i - 1].end) out[i] = { ...out[i], start: out[i - 1].end };
  return { segments: out, words: out.flatMap((s) => s.words), total: base.total + shift, estimated: base.estimated };
}
