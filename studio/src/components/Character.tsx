import React from 'react';
import { Img, staticFile } from 'remotion';
import { MANIFEST } from '../generated/data';
import { action, hash } from '../lib/motion';
import type { CharRef, PoseInfo } from '../lib/types';
import { Placeholder } from './Placeholder';

export const K = 0.625; // canvas px -> frame px at scale 1 (1600-tall canvas => 1000px)
export const W = 1080;
export const H = 1920;

export function resolvePose(ref: CharRef): { key: string; info: PoseInfo } | null {
  const poses = MANIFEST.characters[ref.id];
  if (!poses) return null;
  const tries = [
    ref.expression ? `${ref.pose}__${ref.expression}` : null,
    ref.pose,
    `${ref.pose}__neutral`,
    Object.keys(poses).find((k) => k.startsWith(`${ref.pose}__`)) ?? null,
  ].filter(Boolean) as string[];
  for (const k of tries) if (poses[k]) return { key: k, info: poses[k] };
  return null;
}

// Approximate head and hand points in canvas units, for bubbles and effects.
export const HEAD: Record<string, [number, number]> = {
  // Detailed cast (2026-11-08): face centres from the delivery's placement-anchors.json.
  'dharma:seated-throne': [504, 654], // halo centre (the halo crack is drawn around it)
  'mandavya:on-stake-silhouette': [495, 275],
  'mandavya:meditating-arms-raised': [526, 796],
  'mandavya:walking': [562, 312],
  'mandavya:standing-bound-left': [474, 311],
  'mandavya:cursing-hand-raised': [557, 314],
  'young-mandavya:crouching-playing': [517, 986],
  'king:seated-throne-pointing': [470, 796],
  'king:folded-hands': [544, 323],
  'guard:pulling': [537, 311],
  'thief:running': [335, 351],
  'thief:captured': [456, 323],
  'pandu:drawing-bow': [493, 495],
  default: [500, 312],
};
export const HAND: Record<string, [number, number]> = {
  'mandavya:cursing-hand-raised': [830, 492], // cursePalm
};
export const pointFor = (table: Record<string, [number, number]>, ref: CharRef) =>
  table[`${ref.id}:${ref.pose}`] ?? table.default ?? HEAD.default;

// Frame-space position of a canvas point for this character (ignores actions).
export function framePoint(ref: CharRef, canvas: [number, number]) {
  const s = K * ref.scale;
  const fx = ref.flip ? 1000 - canvas[0] : canvas[0];
  return { x: ref.x * W + (fx - 500) * s, y: ref.y * H + (canvas[1] - 1550) * s };
}

type Props = {
  ref_: CharRef;
  frame: number;
  sec: number;
  p: number;
  talking: boolean;
  filter?: string;
  shakeX?: number;
  debug: boolean;
};

export const Character: React.FC<Props> = ({ ref_: r, frame, sec, p, talking, filter, shakeX = 0, debug }) => {
  const seed = hash(`${r.id}${r.x}`);
  const a = action(r.action, p, sec, seed % 7, r.flip ? -1 : 1);
  const pose = resolvePose(r);
  const s = K * r.scale * a.scale;
  const baseX = (r.x + a.dx) * W + shakeX;
  const baseY = (r.y + a.dy) * H;

  if (!pose) {
    return (
      <Placeholder
        label={`${r.id} · ${r.pose}`}
        style={{ left: baseX - 300 * r.scale, top: baseY - 900 * r.scale, width: 600 * r.scale, height: 900 * r.scale }}
        debug={debug}
      />
    );
  }

  const { info } = pose;
  let src = info.file;
  if (info.face) {
    const blink = info.eyes === 'open' && (frame + (seed % 97)) % 104 < 4;
    const eyes = blink ? 'closed' : info.eyes;
    const flap = talking && Math.floor(frame / 4) % 2 === 0;
    const mouth = talking ? (flap ? 'open' : 'closed') : info.mouth;
    src = info.variants[`${eyes}|${mouth}`] ?? info.file;
  }
  // variant "b" of a character = simple recolour (e.g. second thief)
  const variantFilter = r.variant === 'b' ? 'brightness(0.8) contrast(1.08) saturate(0.85)' : '';
  const w = info.w * s;
  const h = info.h * s;
  return (
    <Img
      src={staticFile(src)}
      style={{
        position: 'absolute',
        width: w,
        height: h,
        left: baseX - 500 * s,
        top: baseY - 1550 * s,
        transformOrigin: `${500 * s}px ${1550 * s}px`,
        transform: `${r.flip ? 'scaleX(-1)' : ''} rotate(${a.rot}deg)`,
        opacity: a.opacity,
        filter: [variantFilter, filter].filter(Boolean).join(' ') || undefined,
      }}
    />
  );
};
