import React, { useMemo } from 'react';
import { COLORS, sansFont } from '../lib/fonts';
import type { Word } from '../lib/timing';
import type { Lang } from '../lib/types';

// Word-by-word captions: 2–4 words on screen, current word in gold (STYLE_GUIDE.md → Type).
// Sits at ~70% height, above the bottom-20% platform-UI zone.
type Chunk = { words: Word[]; start: number; end: number };

function chunk(words: Word[]): Chunk[] {
  const out: Chunk[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) out.push({ words: cur, start: cur[0].start, end: cur[cur.length - 1].end });
    cur = [];
  };
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    if (cur.length && cur[0].sceneId !== w.sceneId) flush();
    cur.push(w);
    const brk = /[,.!?…:;।"”]$/.test(w.text);
    if (cur.length >= 3 || brk) flush();
  }
  flush();
  // keep each chunk visible until the next one starts (no flicker in pauses < 0.6 s)
  for (let i = 0; i < out.length - 1; i++) {
    const gap = out[i + 1].start - out[i].end;
    out[i].end = gap < 0.6 ? out[i + 1].start : out[i].end + 0.3;
  }
  if (out.length) out[out.length - 1].end += 0.4;
  return out;
}

export const Captions: React.FC<{ words: Word[]; t: number; lang: Lang }> = ({ words, t, lang }) => {
  const chunks = useMemo(() => chunk(words), [words]);
  const c = chunks.find((x) => t >= x.start && t < x.end);
  if (!c) return null;
  const size = lang === 'hi' ? 70 : 66;
  return (
    <div style={{ position: 'absolute', top: 1310, left: 70, width: 940, textAlign: 'center', lineHeight: 1.25 }}>
      {c.words.map((w, i) => {
        const active = t >= w.start && t < (c.words[i + 1]?.start ?? c.end);
        const clean = w.text.replace(/["“”]/g, '');
        return (
          <span
            key={i}
            style={{
              font: `${lang === 'hi' ? 700 : 800} ${size}px ${sansFont(lang)}`,
              color: active ? COLORS.gold : '#FFFFFF',
              WebkitTextStroke: `12px ${COLORS.outline}`,
              paintOrder: 'stroke fill',
              display: 'inline-block',
              margin: '0 12px',
              transform: active ? 'scale(1.08)' : 'none',
              textShadow: '0 6px 16px rgba(0,0,0,0.45)',
            }}
          >
            {clean}
          </span>
        );
      })}
    </div>
  );
};
