import React from 'react';
import { AbsoluteFill, interpolate } from 'remotion';
import { COLORS } from '../lib/fonts';
import type { CharRef } from '../lib/types';
import { HAND, HEAD, K, framePoint, pointFor } from './Character';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

export type FiredCue = { kind: string; target?: string; t: number }; // t = seconds since cue (>= 0)

// Stage-space effects (move with the camera). Character-level effects (dim, shake)
// are applied in SceneView via filters.
export const Effects: React.FC<{ fired: FiredCue[]; chars: CharRef[] }> = ({ fired, chars }) => {
  const find = (id?: string) => chars.find((c) => c.id === id) ?? chars[0];
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {fired.map((f, i) => {
        const c = find(f.target);
        if (!c) return null;
        if (f.kind === 'light-burst-saffron') {
          const hand = framePoint(c, HAND[`${c.id}:${c.pose}`] ?? pointFor(HEAD, c));
          const r = interpolate(f.t, [0, 0.7], [40, 1500], clamp);
          const o = interpolate(f.t, [0, 0.15, 1.2], [0, 1, 0], clamp);
          return (
            <div key={i} style={{ position: 'absolute', left: hand.x - r, top: hand.y - r, width: 2 * r, height: 2 * r, borderRadius: '50%', opacity: o,
              background: `radial-gradient(circle, rgba(255,250,230,1) 0%, ${COLORS.saffron} 30%, rgba(224,122,46,0.35) 60%, rgba(224,122,46,0) 72%)` }} />
          );
        }
        if (f.kind === 'halo-crack-dim') {
          const head = framePoint(c, pointFor(HEAD, c));
          const s = K * c.scale;
          const q = interpolate(f.t, [0, 0.35], [0, 1], clamp);
          const R = 165 * s * 1.6;
          const cracks = ['M0 -1 L-0.18 -0.55 L-0.05 -0.4 L-0.3 0', 'M0.05 -1 L0.25 -0.6 L0.12 -0.45 L0.4 -0.2', 'M-0.9 -0.3 L-0.55 -0.25 L-0.6 -0.05', 'M0.95 -0.15 L0.6 -0.1 L0.7 0.1'];
          return (
            <svg key={i} viewBox="-1 -1 2 2" style={{ position: 'absolute', left: head.x - R, top: head.y - 1.08 * R, width: 2 * R, height: 2 * R, overflow: 'visible' }}>
              {cracks.map((d, j) => (
                <path key={j} d={d} fill="none" stroke={COLORS.outline} strokeWidth={0.03} pathLength={1} strokeDasharray="1" strokeDashoffset={1 - q} strokeLinecap="round" />
              ))}
            </svg>
          );
        }
        if (f.kind === 'eyes-open-glow') {
          const head = framePoint(c, pointFor(HEAD, c));
          const o = interpolate(f.t, [0, 0.25], [0, 1], clamp) * (0.75 + 0.25 * Math.sin(f.t * 6));
          const sz = 70 * c.scale;
          return (
            <div key={i} style={{ position: 'absolute', left: head.x - sz, top: head.y - sz * 0.6, width: sz * 2, height: sz * 1.2, opacity: o,
              background: `radial-gradient(circle at 35% 50%, #FFF7D6 0 6%, rgba(255,215,120,0.8) 9%, transparent 22%), radial-gradient(circle at 65% 50%, #FFF7D6 0 6%, rgba(255,215,120,0.8) 9%, transparent 22%)` }} />
          );
        }
        if (f.kind === 'flash') {
          return <AbsoluteFill key={i} style={{ background: '#fff', opacity: interpolate(f.t, [0, 0.25], [0.8, 0], clamp) }} />;
        }
        return null;
      })}
    </AbsoluteFill>
  );
};
