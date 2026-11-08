import React, { useMemo } from 'react';
import { AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from './components/Captions';
import { SceneView } from './components/SceneView';
import { Sound } from './components/Sound';
import { EPISODES } from './generated/data';
import { buildTimeline } from './lib/timing';
import type { EpisodeProps } from './lib/types';

// Scene "transition" = how this scene hands over to the next one.
const FADE = new Set(['dissolve', 'light-wipe', 'memory-ripple', 'border-wipe', 'fade-to-night', 'flash-white']);
const XFADE = 10; // frames

export const Episode: React.FC<EpisodeProps> = ({ episodeId, lang, debug }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const entry = EPISODES[episodeId];
  const tl = useMemo(() => buildTimeline(entry, lang), [entry, lang]);
  const audio = entry.audio[lang];
  const t = frame / fps;
  const last = tl.segments[tl.segments.length - 1];

  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {tl.segments.map((seg, i) => {
        const from = Math.round(seg.start * fps);
        const to = Math.round(seg.end * fps);
        const out = FADE.has(seg.scene.transition) && i < tl.segments.length - 1 ? XFADE : 0;
        const fadeIn = i > 0 && FADE.has(tl.segments[i - 1].scene.transition);
        return (
          <Sequence key={`${seg.scene.id}-${i}`} from={from} durationInFrames={Math.max(1, to - from + out)} name={seg.scene.id}>
            <FadeIn active={fadeIn}>
              <SceneView seg={seg} lang={lang} fps={fps} debug={debug} estimated={tl.estimated} />
            </FadeIn>
            {i > 0 && tl.segments[i - 1].scene.transition === 'flash-white' && <Flash />}
          </Sequence>
        );
      })}
      <Captions words={tl.words} t={t} lang={lang} />
      {last?.scene.transition === 'cut-to-black' && (
        <AbsoluteFill style={{ background: '#000', opacity: interpolate(frame, [durationInFrames - 14, durationInFrames - 1], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) }} />
      )}
      {audio && <Audio src={staticFile(audio.file)} />}
      <Sound spec={entry.spec} tl={tl} lang={lang} fps={fps} total={durationInFrames / fps} />
    </AbsoluteFill>
  );
};

const FadeIn: React.FC<{ active: boolean; children: React.ReactNode }> = ({ active, children }) => {
  const f = useCurrentFrame();
  const o = active ? interpolate(f, [0, XFADE], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) : 1;
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const Flash: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: '#fff', opacity: interpolate(f, [0, 8], [0.9, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) }} />;
};

export const episodeDuration = (episodeId: string, lang: 'en' | 'hi', fps: number) =>
  Math.ceil(buildTimeline(EPISODES[episodeId], lang).total * fps) + 6;
