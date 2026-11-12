import React, { useMemo } from 'react';
import { AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from './components/Captions';
import { ShotView } from './components/ShotView';
import { Sound } from './components/Sound';
import { EPISODES } from './generated/data';
import { buildShotTimeline } from './lib/shotTiming';
import { buildTimeline } from './lib/timing';
import type { EpisodeProps } from './lib/types';

// The illustrated version: same voice, captions and beat timing as the cut-out version,
// but each beat is shown as one or more painted stills (episodes/<ID>/illustrated/03-shots.json).
const FADE = new Set(['dissolve', 'light-wipe', 'memory-ripple', 'border-wipe', 'fade-to-night', 'flash-white']);
const XFADE = 10; // frames

export const IllustratedEpisode: React.FC<EpisodeProps> = ({ episodeId, lang, debug }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const entry = EPISODES[episodeId];
  // the cut-out timeline (voice words, beat spans, scene sfx/music) drives both the shots and the sound pass
  const base = useMemo(() => buildTimeline(entry, lang), [entry, lang]);
  const tl = useMemo(() => buildShotTimeline(entry, lang, base), [entry, lang, base]);
  const byId = useMemo(() => new Map((entry.shots?.shots ?? []).map((s) => [s.id, s])), [entry]);
  const audio = entry.audio[lang];
  const last = tl.segments[tl.segments.length - 1];

  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {tl.segments.map((seg, i) => {
        const from = Math.round(seg.start * fps);
        const to = Math.round(seg.end * fps);
        const out = FADE.has(seg.shot.transition) && i < tl.segments.length - 1 ? XFADE : 0;
        const prev = tl.segments[i - 1]?.shot.transition;
        return (
          <Sequence key={`${seg.shot.id}-${i}`} from={from} durationInFrames={Math.max(1, to - from + out)} name={seg.shot.id}>
            <FadeIn active={i > 0 && FADE.has(prev ?? '')}>
              <ShotView seg={seg} lang={lang} fps={fps} debug={debug} byId={byId} />
            </FadeIn>
            {prev === 'flash-white' && <Flash />}
          </Sequence>
        );
      })}
      <Captions words={tl.words} t={frame / fps} lang={lang} />
      {last?.shot.transition === 'cut-to-black' && (
        <AbsoluteFill style={{ background: '#000', opacity: interpolate(frame, [durationInFrames - 14, durationInFrames - 1], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) }} />
      )}
      {audio && <Audio src={staticFile(audio.file)} />}
      {/* same sound plan as the cut-out version (03-scenes.json: sound, scene sfx and music levels) */}
      <Sound spec={entry.spec} tl={base} lang={lang} fps={fps} total={durationInFrames / fps} />
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

export const illustratedDuration = (episodeId: string, lang: 'en' | 'hi', fps: number) =>
  Math.ceil(buildShotTimeline(EPISODES[episodeId], lang, buildTimeline(EPISODES[episodeId], lang)).total * fps) + 6;
