import React from 'react';
import { AbsoluteFill } from 'remotion';
import { K } from './Character';
import type { CharRef } from '../lib/types';

// The finishing layer for the cut-out version: it makes flat vector puppets sit in their
// scene. Scene light grades the characters and props to match the background and adds a rim
// light; contact shadows ground them; film grain and a vignette tie the frame together.
// All opt-in (03-scenes.json: top-level "grade", per-scene "light"), so older episodes render as before.

const W = 1080;
const H = 1920;

// filter for characters and props, by scene light. The 0-blur drop-shadow is the rim light.
export const LIGHT: Record<string, string> = {
  night: 'brightness(0.74) saturate(0.82) hue-rotate(-6deg) drop-shadow(-3px -2px 0 rgba(165,190,255,0.55))',
  moon: 'brightness(0.86) saturate(0.9) drop-shadow(-3px -3px 0 rgba(215,228,255,0.7))',
  dusk: 'brightness(0.92) sepia(0.12) saturate(1.02) drop-shadow(4px -2px 0 rgba(255,170,95,0.55))',
  dawn: 'brightness(1.0) sepia(0.08) drop-shadow(3px -3px 0 rgba(255,214,140,0.6))',
  fire: 'brightness(0.95) sepia(0.22) saturate(1.18) drop-shadow(4px -1px 0 rgba(255,140,60,0.6))',
  silhouette: 'brightness(0.1) contrast(1.15) saturate(0.4) drop-shadow(3px -2px 0 rgba(255,140,60,0.75))',
  divine: 'brightness(1.04) drop-shadow(0 0 14px rgba(255,214,120,0.55)) drop-shadow(0 0 3px rgba(255,236,180,0.9))',
};

export const ContactShadows: React.FC<{ chars: CharRef[] }> = ({ chars }) => (
  <AbsoluteFill style={{ pointerEvents: 'none' }}>
    {chars.map((c, i) => {
      if (c.y > 1.02) return null; // feet off-frame: no ground to shadow
      const w = 520 * K * c.scale;
      const h = w * 0.16;
      return (
        <div key={i} style={{ position: 'absolute', left: c.x * W - w / 2, top: c.y * H - h / 2, width: w, height: h, borderRadius: '50%',
          background: 'radial-gradient(ellipse, rgba(10,6,14,0.55) 0%, rgba(10,6,14,0.25) 45%, rgba(10,6,14,0) 72%)' }} />
      );
    })}
  </AbsoluteFill>
);

// Animated film grain: fractal noise re-seeded every 2 frames, blended as overlay.
export const Grain: React.FC<{ amount: number; frame: number }> = ({ amount, frame }) => (
  <svg width={W} height={H} style={{ position: 'absolute', inset: 0, mixBlendMode: 'overlay', opacity: amount, pointerEvents: 'none' }}>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={Math.floor(frame / 2) % 97} stitchTiles="stitch" />
      <feColorMatrix type="saturate" values="0" />
    </filter>
    <rect width={W} height={H} filter="url(#grain)" />
  </svg>
);

export const Vignette: React.FC<{ amount: number }> = ({ amount }) => (
  <AbsoluteFill style={{ pointerEvents: 'none', background: `radial-gradient(ellipse 75% 62% at 50% 46%, rgba(0,0,0,0) 55%, rgba(8,4,12,${amount}) 100%)` }} />
);
