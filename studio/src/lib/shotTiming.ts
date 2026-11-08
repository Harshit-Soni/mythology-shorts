import type { Segment, Timeline, Word } from './timing';
import type { EpisodeEntry, Lang, Shot } from './types';

// Timeline for the illustrated version. It reuses the cut-out timeline (same voice, same beats)
// and splits each beat's time span between that beat's shots: the first shot starts with the beat,
// a later shot starts on its `at` word.
export type ShotSegment = {
  shot: Shot;
  start: number;
  end: number;
  words: Word[]; // words spoken during this shot
  beatWords: Word[]; // all words of the beat (cue lookup)
  sceneSeg?: Segment; // kind 'scene': the cut-out segment to render
};
export type ShotTimeline = { segments: ShotSegment[]; words: Word[]; total: number };

const LEAD = 0.08; // cut slightly before the word lands

// Type-only imports keep this file loadable by plain Node (scripts/render.mjs), so norm is repeated here.
const norm = (s: string) => s.toLowerCase().replace(/[“”"'‘’.,!?…:;।()\-—]/g, '').trim();

export const findWord = (words: Word[], target: string | undefined): Word | undefined => {
  const t = norm(target ?? '');
  if (!t) return undefined;
  return words.find((w) => norm(w.text) === t) ?? words.find((w) => norm(w.text).includes(t));
};

// tl = buildTimeline(entry, lang): the cut-out timeline the shots are laid over.
export function buildShotTimeline(entry: EpisodeEntry, lang: Lang, tl: Timeline): ShotTimeline {
  const shots = entry.shots?.shots ?? [];
  const beats = new Map<number, { start: number; end: number; words: Word[]; segs: Segment[] }>();
  for (const s of tl.segments) {
    const b = beats.get(s.scene.beat) ?? { start: s.start, end: s.end, words: [], segs: [] };
    b.start = Math.min(b.start, s.start);
    b.end = Math.max(b.end, s.end);
    b.words.push(...s.words);
    b.segs.push(s);
    beats.set(s.scene.beat, b);
  }
  const out: ShotSegment[] = [];
  for (const [beat, b] of [...beats.entries()].sort((x, y) => x[1].start - y[1].start)) {
    const mine = shots.filter((s) => s.beat === beat);
    if (!mine.length) continue;
    const starts = mine.map((s, i) => {
      if (i === 0) return b.start;
      const w = findWord(b.words, s.at?.[lang]);
      return w ? Math.max(b.start, w.start - LEAD) : b.start + ((b.end - b.start) * i) / mine.length;
    });
    mine.forEach((shot, i) => {
      const start = starts[i];
      const end = i < mine.length - 1 ? starts[i + 1] : b.end;
      const sceneSeg = shot.kind === 'scene' ? b.segs.find((s) => s.scene.id === shot.scene) : undefined;
      out.push({
        shot, start, end, sceneSeg,
        words: b.words.filter((w) => w.start >= start - 0.01 && w.start < end),
        beatWords: b.words,
      });
    });
  }
  return { segments: out, words: tl.words, total: tl.total };
}
