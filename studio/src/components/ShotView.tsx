import React from 'react';
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { COLORS } from '../lib/fonts';
import { camera, camTransform } from '../lib/motion';
import { findWord, type ShotSegment } from '../lib/shotTiming';
import type { Lang, Shot } from '../lib/types';
import { MotionFx } from './MotionFx';
import { OnScreenText } from './OnScreenText';
import { Overlay } from './Overlay';
import { SceneView } from './SceneView';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
const W = 1080;
const H = 1920;

type Props = { seg: ShotSegment; lang: Lang; fps: number; debug: boolean; byId: Map<string, Shot> };

// One illustrated shot: a painted still (cover-fit, with a camera move), ambient motion effects,
// cue effects (burst, shake, dim), on-screen text and optional overlay frame.
export const ShotView: React.FC<Props> = ({ seg, lang, fps, debug, byId }) => {
  const frame = useCurrentFrame();
  const sh = seg.shot;
  const sec = frame / fps;
  const dur = Math.max(0.001, seg.end - seg.start);
  const p = Math.min(1, sec / dur);

  if (sh.kind === 'scene' && seg.sceneSeg) {
    return <SceneView seg={seg.sceneSeg} lang={lang} fps={fps} debug={debug} estimated={false} />;
  }

  // cue times, in seconds from the start of the shot
  const cueAt = (word: string | undefined) => {
    const w = findWord(seg.words, word) ?? findWord(seg.beatWords, word);
    return w ? w.start - seg.start : dur * 0.5;
  };
  const fired = (sh.cues ?? []).map((c) => ({ c, at: cueAt(c.onWord?.[lang]) }));
  const firedT = (kind: string) => {
    const f = fired.find((x) => x.c.do === kind);
    return f && sec >= f.at ? sec - f.at : null;
  };
  const titleAt = fired.find((x) => x.c.do === 'title-in')?.at ?? null;
  const writeOn = fired.find((x) => x.c.do === 'write-on');
  const stampAt = fired.find((x) => x.c.do === 'stamp-next')?.at ?? null;

  const shakeT = firedT('shake');
  const shake = shakeT !== null && shakeT < 0.8 ? 18 * (1 - shakeT / 0.8) * Math.sin(shakeT * 50) : 0;
  const dimT = firedT('dim');
  const dim = dimT === null ? 0 : interpolate(dimT, [0.1, 0.9], [0, 1], clamp);
  const burst = fired.find((x) => x.c.do === 'burst');

  const cam = camera(sh.camera, p, sec);
  const base = sh.baseScale ?? 1.04;
  const transform = `translate(${shake}px, 0px) ${camTransform({ ...cam, scale: cam.scale * base })}`;
  const sepia = sh.overlay === 'sepia-folk-frame';

  return (
    <AbsoluteFill style={{ overflow: 'hidden', background: '#000' }}>
      <AbsoluteFill style={{ transform, transformOrigin: cam.origin, filter: `${sepia ? 'sepia(0.35) ' : ''}brightness(${1 - 0.25 * dim}) saturate(${1 - 0.3 * dim})` }}>
        {sh.kind === 'split' ? <Split shot={sh} byId={byId} /> : <Still file={sh.file} label={sh.id} />}
        <MotionFx fx={sh.fx ?? []} sec={sec} />
      </AbsoluteFill>
      {burst && sec >= burst.at && <Burst t={sec - burst.at} x={(burst.c.x ?? 0.5) * W} y={(burst.c.y ?? 0.35) * H} />}
      <Vignette />
      {sh.overlay && <Overlay id={sh.overlay} inset={1} />}
      {sh.onScreenText && (
        <OnScreenText ost={sh.onScreenText} lang={lang} sec={sec} dur={dur} fps={fps} chars={[]}
          titleAt={titleAt} writeEndAt={writeOn ? writeOn.at + 0.3 : null} stampAt={stampAt} />
      )}
      {debug && (
        <div style={{ position: 'absolute', right: 150, top: 120, padding: '10px 16px', background: 'rgba(0,0,0,0.6)', color: '#fff', font: '600 26px monospace', borderRadius: 10 }}>
          {sh.id} · beat {sh.beat} · {dur.toFixed(1)}s{!sh.file && sh.kind !== 'split' ? ' · NO IMAGE' : ''}
        </div>
      )}
    </AbsoluteFill>
  );
};

const Still: React.FC<{ file?: string; label: string }> = ({ file, label }) =>
  file ? (
    <Img src={staticFile(file)} style={{ position: 'absolute', inset: 0, width: W, height: H, objectFit: 'cover' }} />
  ) : (
    <AbsoluteFill style={{ background: '#2A2238', color: '#fff', font: '600 40px sans-serif', alignItems: 'center', justifyContent: 'center' }}>{label}: image missing</AbsoluteFill>
  );

// Two halves side by side (e.g. the child's "mistake" next to the stake), with a folk-art divider.
const Split: React.FC<{ shot: Shot; byId: Map<string, Shot> }> = ({ shot, byId }) => {
  const [a, b] = (shot.split ?? []).map((id) => byId.get(id));
  const half = (s: Shot | undefined, left: number, filter?: string) => (
    <div style={{ position: 'absolute', left, top: 0, width: W / 2, height: H, overflow: 'hidden' }}>
      {s?.file && <Img src={staticFile(s.file)} style={{ position: 'absolute', left: -W / 4, top: 0, width: W, height: H, objectFit: 'cover', filter }} />}
    </div>
  );
  return (
    <AbsoluteFill>
      {half(a, 0, 'sepia(0.5)')}
      {half(b, W / 2)}
      <div style={{ position: 'absolute', left: W / 2 - 18, top: 0, width: 36, height: H, background: `repeating-linear-gradient(180deg, ${COLORS.red} 0 30px, ${COLORS.gold} 30px 36px, ${COLORS.saffron} 36px 60px, ${COLORS.gold} 60px 66px)`, boxShadow: '0 0 18px rgba(0,0,0,0.5)' }} />
    </AbsoluteFill>
  );
};

const Burst: React.FC<{ t: number; x: number; y: number }> = ({ t, x, y }) => {
  const r = interpolate(t, [0, 0.7], [40, 1500], clamp);
  const o = interpolate(t, [0, 0.12, 1.1], [0, 0.95, 0], clamp);
  return <div style={{ position: 'absolute', left: x - r, top: y - r, width: 2 * r, height: 2 * r, borderRadius: '50%', opacity: o, mixBlendMode: 'screen',
    background: `radial-gradient(circle, rgba(255,250,230,1) 0%, ${COLORS.saffron} 30%, rgba(224,122,46,0.35) 60%, rgba(224,122,46,0) 72%)` }} />;
};

const Vignette: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: 'none', background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.35) 100%)' }} />
);
