import React, { useMemo } from 'react';
import { AbsoluteFill, Freeze, Img, staticFile } from 'remotion';
import { SceneView } from './components/SceneView';
import { EPISODES } from './generated/data';
import { BRAND } from './lib/brand';
import { COLORS, sansFont, serifFont } from './lib/fonts';
import { buildTimeline } from './lib/timing';
import type { Lang } from './lib/types';

// The cover / thumbnail for an episode (1080x1920): one frame of the cut-out version
// (03-scenes.json "thumbnail".scene, at "at" 0..1 through it), the series label on top and
// the title below. Text stays inside the centre 1080x1350, which Instagram's 4:5 grid shows.
// Latin series labels (e.g. "Indian Mythology" on the Hindi cover too) keep the English style
const devanagari = (s: string) => /[\u0900-\u097F]/.test(s);

export type ThumbProps = { episodeId: string; lang: Lang; scene?: string };

export const Thumbnail: React.FC<ThumbProps> = ({ episodeId, lang, scene }) => {
  const entry = EPISODES[episodeId];
  const spec = entry.spec.thumbnail!;
  const tl = useMemo(() => buildTimeline(entry, lang), [entry, lang]);
  const id = scene ?? spec.scene;
  const seg = tl.segments.find((s) => s.scene.id === id) ?? tl.segments[0];
  const fps = entry.spec.fps;
  const frame = Math.round((seg.end - seg.start) * (spec.at ?? 0.5) * fps);
  const lines = spec.titleLines?.[lang] ?? [spec.title[lang]];
  const hi = lang === 'hi';
  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {/* the scene sits higher than in the video, so the figure clears the title */}
      <AbsoluteFill style={{ transform: `translateY(${-(spec.lift ?? 260)}px)` }}>
        <Freeze frame={frame}>
          <SceneView seg={seg} lang={lang} fps={fps} debug={false} estimated={false} grade={entry.spec.grade} />
        </Freeze>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(10,8,24,0.82) 0%, rgba(10,8,24,0) 30%, rgba(10,8,24,0) 52%, rgba(10,8,24,0.88) 78%, rgba(10,8,24,0.95) 100%)' }} />
      {/* series label */}
      <div style={{ position: 'absolute', top: 300, width: '100%', display: 'flex', justifyContent: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 18, padding: '12px 34px 12px 14px', borderRadius: 70, border: `3px solid ${COLORS.gold}`, background: 'rgba(14,13,34,0.72)' }}>
          <Img src={staticFile(BRAND.emblem)} style={{ width: 76, height: 76 }} />
          <span style={{ font: devanagari(spec.series[lang]) ? `700 46px ${sansFont('hi')}` : `800 40px ${sansFont('en')}`, letterSpacing: devanagari(spec.series[lang]) ? 1 : 7, color: COLORS.gold, textTransform: 'uppercase' }}>
            {spec.series[lang]}
          </span>
        </div>
      </div>
      {/* title */}
      <div style={{ position: 'absolute', bottom: 1920 - 1580, width: '100%', textAlign: 'center', padding: '0 40px', boxSizing: 'border-box' }}>
        {lines.map((l, i) => (
          <div key={i} style={{
            font: hi ? `400 ${i === 0 ? 168 : 124}px ${serifFont('hi')}` : `700 ${i === 0 ? 132 : 100}px ${serifFont('en')}`,
            lineHeight: hi ? 1.25 : 1.05, letterSpacing: hi ? 0 : 3, whiteSpace: 'nowrap', textTransform: hi ? undefined : 'uppercase',
            color: i === 0 ? COLORS.gold : COLORS.parchment,
            WebkitTextStroke: `3px ${COLORS.outline}`, paintOrder: 'stroke fill',
            textShadow: '0 6px 24px rgba(0,0,0,0.75), 0 0 2px rgba(0,0,0,0.9)',
          }}>{l}</div>
        ))}
        <div style={{ marginTop: 22, font: `700 34px ${serifFont('en')}`, letterSpacing: 6, color: COLORS.gold, opacity: 0.9 }}>{BRAND.name}</div>
      </div>
    </AbsoluteFill>
  );
};
