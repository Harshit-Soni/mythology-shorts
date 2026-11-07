import React from 'react';
import { Easing, Img, interpolate, spring, staticFile } from 'remotion';
import { MANIFEST } from '../generated/data';
import { COLORS } from '../lib/fonts';
import { action, hash } from '../lib/motion';
import type { PropRef } from '../lib/types';
import { H, W } from './Character';
import { Placeholder } from './Placeholder';

const P = 0.75; // prop canvas px -> frame px at scale 1

// Props drawn in code (no asset file needed). A real file in assets/ overrides these.
const CODE_PROPS = new Set(['shaap-stamp', 'seal-stamp', 'falling-light', 'stake-tip-glint']);

export type PropReaction = { kind: string; t: number } | null; // t = seconds since cue fired

type Props = { prop: PropRef; sec: number; p: number; fps: number; reaction: PropReaction; hasCue: boolean; debug: boolean };

export const Prop: React.FC<Props> = ({ prop, sec, p, fps, reaction, hasCue, debug }) => {
  const a = action(prop.action, p, sec, hash(prop.id) % 5);
  const file = MANIFEST.props[prop.id] ?? MANIFEST.overlays[prop.id];
  let rot = a.rot;
  let scale = a.scale;
  let opacity = a.opacity;
  let dy = a.dy;

  // stamps: hidden until their cue (or 0.15 s into the scene if they have none)
  const isStamp = prop.action === 'stamp-in';
  if (isStamp) {
    if (hasCue && !reaction) return null;
    const t = reaction && (reaction.kind === 'stamp-next' || reaction.kind === 'stamp-in') ? reaction.t : sec - 0.15;
    if (t < 0) return null;
    const sp = spring({ frame: t * fps, fps, config: { damping: 11, stiffness: 160 } });
    scale *= interpolate(sp, [0, 1], [2.6, 1]);
    opacity = Math.min(1, t * 8);
    rot += -7;
  }
  if (reaction && reaction.t >= 0) {
    const sp = spring({ frame: reaction.t * fps, fps, config: { damping: reaction.kind.endsWith('violent') ? 6 : 12 } });
    if (reaction.kind.startsWith('scales-tip')) rot += (reaction.kind.endsWith('violent') ? -18 : -8) * sp;
    if (reaction.kind === 'spill' || reaction.kind === 'scatter') scale *= 1 + 0.15 * Math.sin(Math.min(1, reaction.t * 3) * Math.PI);
    if (reaction.kind === 'pierce') dy += -0.01 * Math.sin(Math.min(1, reaction.t * 4) * Math.PI);
  }

  const cx = (prop.x + a.dx) * W;
  const cy = (prop.y + dy) * H;
  const style = (w: number, h: number): React.CSSProperties => ({
    position: 'absolute', left: cx - w / 2, top: cy - h / 2, width: w, height: h,
    transform: `rotate(${rot}deg) scale(${scale})`, opacity,
  });

  if (file) {
    const w = (file.w ?? 800) * P * prop.scale;
    const h = (file.h ?? 800) * P * prop.scale;
    return <Img src={staticFile(file.file)} style={style(w, h)} />;
  }
  if (CODE_PROPS.has(prop.id)) return <CodeProp id={prop.id} scale={prop.scale} style={style} sec={sec} />;

  const tall = prop.id === 'stake';
  const w = (tall ? 160 : 380) * prop.scale;
  const h = (tall ? 640 : 380) * prop.scale;
  return <Placeholder label={prop.id} style={{ ...style(w, h), transform: undefined }} debug={debug} />;
};

const CodeProp: React.FC<{ id: string; scale: number; sec: number; style: (w: number, h: number) => React.CSSProperties }> = ({ id, scale, sec, style }) => {
  if (id === 'shaap-stamp' || id === 'seal-stamp') {
    const d = 560 * scale;
    const c = id === 'seal-stamp' ? COLORS.red : COLORS.gold;
    return (
      <svg viewBox="0 0 200 200" style={style(d, d)}>
        <circle cx="100" cy="100" r="92" fill="none" stroke={c} strokeWidth="9" strokeDasharray="3 2 40 3 22 2" />
        <circle cx="100" cy="100" r="76" fill="none" stroke={c} strokeWidth="3" />
        {id === 'seal-stamp' && <circle cx="100" cy="100" r="70" fill={c} opacity="0.9" />}
        {Array.from({ length: 16 }).map((_, i) => (
          <circle key={i} cx={100 + 84 * Math.cos((i / 16) * Math.PI * 2)} cy={100 + 84 * Math.sin((i / 16) * Math.PI * 2)} r="3" fill={c} />
        ))}
      </svg>
    );
  }
  if (id === 'falling-light') {
    return (
      <div style={{ ...style(260 * scale, 1500 * scale), background: `linear-gradient(180deg, rgba(255,240,190,0) 0%, rgba(255,226,140,0.75) 40%, rgba(255,245,215,0.95) 100%)`, filter: 'blur(14px)', borderRadius: 200 }} />
    );
  }
  // stake-tip-glint
  const g = 140 * scale + 40 * Math.abs(Math.sin(sec * 3));
  return (
    <svg viewBox="-50 -50 100 100" style={style(g, g)}>
      <path d="M0 -48 L7 -7 L48 0 L7 7 L0 48 L-7 7 L-48 0 L-7 -7Z" fill="#FFF3C4" />
      <circle r="9" fill="#fff" />
    </svg>
  );
};

export const fadeIn = (t: number, d = 0.3) => interpolate(t, [0, d], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.quad) });
