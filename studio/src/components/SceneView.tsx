import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { MANIFEST } from '../generated/data';
import { camera, camTransform } from '../lib/motion';
import { cueTime, type Segment } from '../lib/timing';
import type { Lang } from '../lib/types';
import { Background, BackgroundFront } from './Background';
import { Character, resolvePose } from './Character';
import { Effects, type FiredCue } from './Effects';
import { OnScreenText } from './OnScreenText';
import { Overlay } from './Overlay';
import { Prop } from './Prop';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
const CODE_PROPS = new Set(['shaap-stamp', 'seal-stamp', 'falling-light', 'stake-tip-glint']);

type Props = { seg: Segment; lang: Lang; fps: number; debug: boolean; estimated: boolean };

export const SceneView: React.FC<Props> = ({ seg, lang, fps, debug, estimated }) => {
  const frame = useCurrentFrame();
  const sc = seg.scene;
  const sec = frame / fps;
  const dur = Math.max(0.001, seg.end - seg.start);
  const p = Math.min(1, sec / dur);
  const abs = seg.start + sec;

  // cues that have fired by now, with seconds since firing
  const fired: FiredCue[] = [];
  let titleAt: number | null = null;
  let writeEndAt: number | null = null;
  let stampAt: number | null = null;
  for (const c of sc.cues ?? []) {
    const at = cueTime(seg, c, lang) - seg.start;
    if (c.do === 'title-in') titleAt = at;
    if (c.do === 'write-on') writeEndAt = at + 0.3;
    if (c.do === 'stamp-next') stampAt = at;
    if (sec >= at) fired.push({ kind: c.do, target: c.target, t: sec - at });
  }

  // character-level effects
  const charFilter = (id: string) => {
    const f = fired.find((x) => x.kind === 'halo-crack-dim' && (x.target ?? id) === id);
    if (!f) return undefined;
    const q = interpolate(f.t, [0.2, 0.8], [0, 1], clamp);
    return `brightness(${1 - 0.22 * q}) saturate(${1 - 0.3 * q})`;
  };
  const shakeX = (id: string) => {
    const f = fired.find((x) => x.kind === 'pull-fail' && (x.target ?? id) === id);
    return f && f.t < 0.9 ? 14 * Math.sin(f.t * 42) * (1 - f.t / 0.9) : 0;
  };
  const speakingNow = seg.words.some((w) => w.inQuote && abs >= w.start && abs < w.end);

  const cam = camera(sc.camera, p, sec);
  const sepia = sc.overlay === 'sepia-folk-frame';

  // draw back-to-front by baseline y
  const items = [
    ...sc.props.map((pr) => ({ y: pr.y, el: (
      <Prop key={`p-${pr.id}-${pr.x}`} prop={pr} sec={sec} p={p} fps={fps} debug={debug}
        hasCue={(sc.cues ?? []).some((c) => c.target === pr.id)}
        reaction={(() => {
          const f = fired.find((x) => x.target === pr.id) ?? (pr.action === 'scatter' ? fired.find((x) => x.kind === 'spill') : undefined);
          return f ? { kind: f.kind, t: f.t } : null;
        })()} />
    ) })),
    ...sc.characters.map((c, i) => ({ y: c.y, el: (
      <Character key={`c-${c.id}-${i}`} ref_={c} frame={frame + i * 37} sec={sec} p={p} debug={debug}
        talking={!!c.speaking && speakingNow} filter={charFilter(c.id)} shakeX={shakeX(c.id)} />
    ) })),
  ].sort((a, b) => a.y - b.y);

  const missing = [
    ...(sc.background !== 'split-frame' && !MANIFEST.backgrounds[sc.background] ? [`bg:${sc.background}`] : []),
    ...sc.characters.filter((c) => !resolvePose(c)).map((c) => `${c.id}:${c.pose}`),
    ...sc.props.filter((pr) => !MANIFEST.props[pr.id] && !MANIFEST.overlays[pr.id] && !CODE_PROPS.has(pr.id)).map((pr) => pr.id),
  ];

  return (
    <AbsoluteFill style={{ overflow: 'hidden', background: '#000' }}>
      <AbsoluteFill style={{ transform: camTransform(cam), transformOrigin: cam.origin, filter: sepia ? 'sepia(0.85) contrast(0.95) brightness(1.05)' : undefined }}>
        <Background id={sc.background} variant={sc.backgroundVariant} debug={debug} backOnly={!!sc.frontLayer} />
        {items.map((x) => x.el)}
        {sc.frontLayer && <BackgroundFront id={sc.background} variant={sc.backgroundVariant} />}
        <Effects fired={fired} chars={sc.characters} />
      </AbsoluteFill>
      {sc.overlay && <Overlay id={sc.overlay} inset={sc.id === 's00' ? interpolate(sec, [0, 0.4], [0, 1], clamp) : 1} />}
      {sc.onScreenText && (
        <OnScreenText ost={sc.onScreenText} lang={lang} sec={sec} dur={dur} fps={fps} chars={sc.characters} titleAt={titleAt} writeEndAt={writeEndAt} stampAt={stampAt} />
      )}
      {debug && (
        <div style={{ position: 'absolute', right: 150, top: 120, padding: '10px 16px', background: 'rgba(0,0,0,0.6)', color: '#fff', font: '600 26px monospace', borderRadius: 10, maxWidth: 560 }}>
          {sc.id} · beat {sc.beat} · {dur.toFixed(1)}s{estimated ? ' · est. timing' : ''}
          {missing.length > 0 && <div style={{ color: '#FFB86B', fontSize: 22, marginTop: 4 }}>missing: {missing.join(', ')}</div>}
        </div>
      )}
    </AbsoluteFill>
  );
};
