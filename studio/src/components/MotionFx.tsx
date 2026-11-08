import React from 'react';
import { AbsoluteFill, interpolate } from 'remotion';
import type { FxSpec } from '../lib/types';

// Ambient motion painted over an illustrated still: dust, embers, sparks, stars, light rays,
// glow, fog, torch flicker, a falling leaf, circling birds. Deterministic (seeded), so every
// render is identical. sec = seconds into the shot.
const W = 1080;
const H = 1920;
const rnd = (i: number, k: number) => {
  const x = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453;
  return x - Math.floor(x);
};
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

export const MotionFx: React.FC<{ fx: FxSpec[]; sec: number }> = ({ fx, sec }) => (
  <AbsoluteFill style={{ pointerEvents: 'none' }}>
    {fx.map((f, i) => <One key={i} f={f} sec={sec} seed={i + 1} />)}
  </AbsoluteFill>
);

const One: React.FC<{ f: FxSpec; sec: number; seed: number }> = ({ f, sec, seed }) => {
  const n = f.n ?? 30;
  switch (f.type) {
    case 'dust':
      return (
        <>
          {Array.from({ length: n }).map((_, i) => {
            const x = (rnd(i, seed) * W + sec * (8 + 14 * rnd(i, 3)) * (rnd(i, 4) > 0.5 ? 1 : -1) + W) % W;
            const y = (rnd(i, seed + 1) * H - sec * (10 + 20 * rnd(i, 5)) + H * 2) % H;
            const s = 2 + 4 * rnd(i, 6);
            const o = 0.25 + 0.45 * (0.5 + 0.5 * Math.sin(sec * (1 + rnd(i, 7) * 2) + i));
            return <div key={i} style={{ position: 'absolute', left: x, top: y, width: s, height: s, borderRadius: '50%', background: f.color ?? '#FFF3D6', opacity: o, boxShadow: `0 0 ${s * 2}px ${f.color ?? '#FFF3D6'}` }} />;
          })}
        </>
      );
    case 'embers':
    case 'sparks': {
      const up = f.type === 'embers';
      const col = f.color ?? (up ? '#FF9A3C' : '#F5C64A');
      return (
        <>
          {Array.from({ length: n }).map((_, i) => {
            const speed = 60 + 120 * rnd(i, 2);
            const phase = rnd(i, seed) * H;
            const yy = up ? (H - ((phase + sec * speed) % H)) : ((phase + sec * speed) % H);
            const x = rnd(i, seed + 7) * W + 30 * Math.sin(sec * 1.5 + i);
            const s = 3 + 5 * rnd(i, 9);
            const o = 0.5 + 0.5 * Math.sin(sec * 9 + i * 2);
            return <div key={i} style={{ position: 'absolute', left: x, top: yy, width: s, height: s, borderRadius: '50%', background: col, opacity: Math.max(0, o), boxShadow: `0 0 ${s * 3}px ${col}` }} />;
          })}
        </>
      );
    }
    case 'stars':
      return (
        <>
          {Array.from({ length: n }).map((_, i) => {
            const x = rnd(i, seed) * W;
            const y = rnd(i, seed + 2) * H * 0.42;
            const s = 2 + 3 * rnd(i, 4);
            const o = 0.2 + 0.8 * Math.max(0, Math.sin(sec * (1.2 + 2 * rnd(i, 5)) + i * 3));
            return <div key={i} style={{ position: 'absolute', left: x, top: y, width: s, height: s, borderRadius: '50%', background: '#FFFFFF', opacity: o, boxShadow: '0 0 6px #fff' }} />;
          })}
        </>
      );
    case 'rays': {
      const cx = (f.x ?? 0.5) * W;
      const cy = (f.y ?? 0.3) * H;
      const R = 1500;
      return (
        <div style={{
          position: 'absolute', left: cx - R, top: cy - R, width: 2 * R, height: 2 * R, mixBlendMode: 'screen', opacity: 0.22,
          transform: `rotate(${sec * 3}deg)`,
          background: `repeating-conic-gradient(from 0deg, ${f.color ?? '#FFE7B0'} 0deg 4deg, transparent 4deg 16deg)`,
          WebkitMaskImage: 'radial-gradient(circle, rgba(0,0,0,1) 0%, rgba(0,0,0,0.6) 25%, rgba(0,0,0,0) 60%)',
          maskImage: 'radial-gradient(circle, rgba(0,0,0,1) 0%, rgba(0,0,0,0.6) 25%, rgba(0,0,0,0) 60%)',
        }} />
      );
    }
    case 'glow': {
      const cx = (f.x ?? 0.5) * W;
      const cy = (f.y ?? 0.4) * H;
      const r = (f.r ?? 0.3) * W;
      const o = f.pulse ? 0.35 + 0.25 * Math.sin(sec * 2.4) : 0.4;
      return <div style={{ position: 'absolute', left: cx - r, top: cy - r, width: 2 * r, height: 2 * r, borderRadius: '50%', mixBlendMode: 'screen', opacity: o, background: `radial-gradient(circle, ${f.color ?? '#E8B53A'} 0%, transparent 70%)` }} />;
    }
    case 'fog':
      return (
        <>
          {[0, 1, 2].map((i) => {
            const x = -300 + ((sec * (20 + i * 10) + i * 500) % (W + 600));
            const y = H * (0.55 + 0.12 * i);
            return <div key={i} style={{ position: 'absolute', left: x - 500, top: y - 220, width: 1000, height: 440, borderRadius: '50%', opacity: 0.22, background: `radial-gradient(ellipse, ${f.color ?? '#F3E6C8'} 0%, transparent 70%)` }} />;
          })}
        </>
      );
    case 'flicker': {
      const o = 0.05 + 0.04 * Math.sin(sec * 13) + 0.03 * Math.sin(sec * 31 + 1) + 0.02 * Math.sin(sec * 7 + 2);
      return <AbsoluteFill style={{ background: f.color ?? '#FF8A2A', opacity: Math.max(0, o), mixBlendMode: 'soft-light' }} />;
    }
    case 'leaf': {
      const t = (sec % 4.5) / 4.5;
      const x = (f.x ?? 0.5) * W + 70 * Math.sin(sec * 2.2);
      const y = interpolate(t, [0, 1], [-60, H * 0.72], clamp);
      return (
        <svg width="60" height="40" viewBox="-30 -20 60 40" style={{ position: 'absolute', left: x - 30, top: y - 20, transform: `rotate(${40 * Math.sin(sec * 2.2)}deg)`, opacity: interpolate(t, [0, 0.05, 0.9, 1], [0, 1, 1, 0]) }}>
          <path d="M-26 0 Q0 -18 26 0 Q0 18 -26 0Z" fill="#7A8A3A" stroke="#1E1420" strokeWidth="2" />
          <path d="M-24 0 L24 0" stroke="#1E1420" strokeWidth="1.5" />
        </svg>
      );
    }
    case 'birds': {
      const cx = (f.x ?? 0.5) * W;
      const cy = (f.y ?? 0.2) * H;
      const r = (f.r ?? 0.25) * W;
      return (
        <>
          {Array.from({ length: f.n ?? 3 }).map((_, i) => {
            const a = sec * 0.35 + (i * Math.PI * 2) / (f.n ?? 3);
            const x = cx + r * Math.cos(a);
            const y = cy + r * 0.35 * Math.sin(a);
            const flap = 6 * Math.sin(sec * 3 + i);
            return (
              <svg key={i} width="90" height="40" viewBox="-45 -20 90 40" style={{ position: 'absolute', left: x - 45, top: y - 20, transform: `scaleX(${Math.sin(a) > 0 ? 1 : -1})` }}>
                <path d={`M-42 ${-4 + flap} L-14 -2 L0 4 L14 -2 L42 ${-4 + flap} L36 ${0 + flap} L30 ${-2 + flap} L24 ${2 + flap} L14 4 L0 10 L-14 4 L-24 ${2 + flap} L-30 ${-2 + flap} L-36 ${0 + flap}Z`} fill="#0E0B14" />
              </svg>
            );
          })}
        </>
      );
    }
    default:
      return null;
  }
};
