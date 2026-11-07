import { Easing, interpolate } from 'remotion';
import type { Camera } from './types';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
const smooth = Easing.inOut(Easing.cubic);

export type CamState = { scale: number; tx: number; ty: number; rot: number; origin: string };

// p = 0..1 progress through the scene, sec = seconds into the scene (for shakes).
export function camera(cam: Camera | undefined, p: number, sec: number): CamState {
  const c = cam ?? { move: 'static' };
  const from = c.from ?? 1;
  const to = c.to ?? 1;
  const origin = c.focus ? `${c.focus[0] * 100}% ${c.focus[1] * 100}%` : '50% 45%';
  const base: CamState = { scale: 1, tx: 0, ty: 0, rot: 0, origin };
  const e = smooth(Math.min(1, Math.max(0, p)));
  const W = 1080;
  const H = 1920;
  const shake = (amp: number, dur: number) =>
    sec < dur ? amp * (1 - sec / dur) * Math.sin(sec * 55) : 0;

  switch (c.move) {
    case 'slow-zoom-in':
    case 'slow-zoom-out':
      return { ...base, scale: interpolate(e, [0, 1], [from, to]) };
    case 'fast-zoom-in':
    case 'push-in-fast': {
      const q = interpolate(p, [0, 0.35], [0, 1], { ...clamp, easing: Easing.out(Easing.exp) });
      return { ...base, scale: interpolate(q, [0, 1], [from, to]) };
    }
    case 'slow-pan-up':
    case 'crane-up':
      return { ...base, scale: 1.06, ty: interpolate(e, [0, 1], [from, to]) * H };
    case 'tilt-down':
      return { ...base, scale: 1.06, ty: interpolate(e, [0, 1], [-(from ?? 0), -(to ?? 0)]) * H };
    case 'pan-left':
    case 'slow-pan-right':
      return { ...base, scale: 1.08, tx: interpolate(e, [0, 1], [from, to]) * W };
    case 'shake-small-then-static':
      return { ...base, scale: 1.02, tx: shake(10, 0.5) };
    case 'shake-then-zoom':
      return { ...base, scale: interpolate(e, [0, 1], [from, to]), tx: shake(16, 0.7), rot: shake(0.6, 0.7) };
    default:
      return base;
  }
}

export const camTransform = (c: CamState) =>
  `translate(${c.tx}px, ${c.ty}px) scale(${c.scale}) rotate(${c.rot}deg)`;

export type ActState = { dx: number; dy: number; scale: number; rot: number; opacity: number };

// Character / prop actions. p = 0..1 scene progress, sec = seconds into the scene,
// cueSec = seconds since this element's cue fired (or null).
// dir = +1 for the asset's own facing, -1 when mirrored: movement follows the way a character faces.
export function action(name: string | undefined, p: number, sec: number, seed: number, dir = 1): ActState {
  const s: ActState = { dx: 0, dy: 0, scale: 1, rot: 0, opacity: 1 };
  const breathe = 1 + 0.012 * Math.sin(sec * 2.2 + seed);
  switch (name) {
    case 'breathe':
    case 'idle':
    case 'still':
    case undefined:
      return { ...s, scale: name === 'still' ? 1 : breathe };
    case 'run-in-hide': {
      const q = interpolate(p, [0, 0.45], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
      return { ...s, dx: (1 - q) * 0.55 * dir, dy: q < 1 ? -0.006 * Math.abs(Math.sin(sec * 14)) : 0 };
    }
    case 'walk-left':
      return { ...s, dx: -0.1 * smooth(p) * dir, dy: -0.004 * Math.abs(Math.sin(sec * 9)) };
    case 'walk-up-steps':
      return { ...s, dx: 0.03 * smooth(p), dy: -0.1 * smooth(p), scale: 1 - 0.14 * smooth(p) + 0.006 * Math.abs(Math.sin(sec * 8)) };
    case 'step-forward': {
      const q = interpolate(sec, [0.2, 0.7], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.4)) });
      return { ...s, dx: 0.03 * q, scale: breathe * (1 + 0.04 * q) };
    }
    case 'shout':
      return { ...s, dy: -0.004 * Math.abs(Math.sin(sec * 7)), scale: breathe };
    case 'bow':
      return { ...s, rot: 3 * smooth(Math.min(1, p * 2)), scale: breathe };
    case 'raise-hand':
    case 'point':
      return { ...s, scale: breathe };
    case 'sway':
      return { ...s, rot: 2.5 * Math.sin(sec * 1.6 + seed) };
    case 'glint':
      return { ...s, scale: 0.8 + 0.4 * Math.abs(Math.sin(sec * 3)), opacity: 0.6 + 0.4 * Math.abs(Math.sin(sec * 3)) };
    case 'fall':
      return { ...s, dy: 0.45 * p, dx: 0.04 * Math.sin(sec * 2.5), rot: 40 * Math.sin(sec * 2) };
    case 'circle':
      return { ...s, dx: 0.12 * Math.cos(sec * 0.9), dy: 0.03 * Math.sin(sec * 0.9) };
    case 'flicker-distant':
      return { ...s, opacity: 0.75 + 0.25 * Math.sin(sec * 17 + seed) };
    case 'descend':
      return { ...s, dy: interpolate(p, [0, 0.5], [-0.5, 0], { ...clamp, easing: Easing.out(Easing.cubic) }) };
    case 'graze':
      return { ...s, rot: 1.5 * Math.sin(sec * 1.3) };
    case 'draw-bow':
      return { ...s, scale: 1 + 0.01 * smooth(p) };
    default:
      return { ...s, scale: breathe };
  }
}

export const hash = (s: string) => {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return h;
};
