import React from 'react';
import { AbsoluteFill, Audio, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { MANIFEST } from '../generated/data';
import { BRAND } from '../lib/brand';
import { COLORS, sansFont, serifFont } from '../lib/fonts';
import type { Lang } from '../lib/types';
import { Grain } from './Grade';
import { MotionFx } from './MotionFx';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

// The channel end card: the last BRAND.endCardSec seconds of every video (both versions).
// Emblem, name, tagline and the handle, on the logo's indigo, with gold dust and grain.
// Everything sits above the Shorts UI zone at the bottom.
// One card for every video: always in English (the brand's look), whatever the video's language.
export const EndCard: React.FC<{ lang: Lang }> = () => {
  const lang = 'en' as const;
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = f / fps;
  const fadeIn = interpolate(f, [0, 8], [0, 1], clamp);
  const rise = (delay: number) => ({
    opacity: interpolate(sec, [delay, delay + 0.35], [0, 1], clamp),
    transform: `translateY(${interpolate(sec, [delay, delay + 0.45], [24, 0], { ...clamp, easing: (x) => 1 - (1 - x) ** 3 })}px)`,
  });
  const emblemScale = interpolate(sec, [0, 1.6], [0.9, 1.0], { ...clamp, easing: (x) => 1 - (1 - x) ** 2 });
  const sfx = MANIFEST.sfx[BRAND.endCardSfx];
  return (
    <AbsoluteFill style={{ opacity: fadeIn, background: `radial-gradient(ellipse 80% 60% at 50% 40%, #2C2A5E 0%, ${COLORS.night} 55%, #0E0D22 100%)` }}>
      <MotionFx fx={[{ type: 'dust', n: 36, color: '#F6D27A' }, { type: 'glow', x: 0.5, y: 0.37, r: 0.42, color: COLORS.gold, pulse: true }]} sec={sec + 3} />
      <div style={{ position: 'absolute', left: 540 - 300, top: 420, width: 600, height: 600, transform: `scale(${emblemScale})`, opacity: interpolate(sec, [0, 0.3], [0, 1], clamp),
        borderRadius: '50%', boxShadow: '0 0 60px rgba(232,181,58,0.35)' }}>
        <Img src={staticFile(BRAND.emblem)} style={{ width: 600, height: 600 }} />
      </div>
      <div style={{ position: 'absolute', top: 1080, width: '100%', textAlign: 'center', ...rise(0.25) }}>
        <div style={{ font: `700 104px ${serifFont('en')}`, letterSpacing: 6, color: COLORS.gold, textShadow: '0 4px 18px rgba(0,0,0,0.6)' }}>{BRAND.name}</div>
      </div>
      <div style={{ position: 'absolute', top: 1215, width: '100%', textAlign: 'center', ...rise(0.5),
        font: `italic 600 52px ${serifFont('en')}`, color: COLORS.parchment }}>
        {BRAND.tagline[lang]}
      </div>
      <div style={{ position: 'absolute', top: 1330, width: '100%', display: 'flex', justifyContent: 'center', ...rise(0.75) }}>
        <div style={{ padding: '14px 40px', borderRadius: 60, border: `3px solid ${COLORS.gold}`, background: 'rgba(14,13,34,0.55)',
          font: `600 42px ${sansFont(lang)}`, color: COLORS.parchment, display: 'flex', gap: 16, alignItems: 'baseline' }}>
          <span>{BRAND.cta[lang]}</span>
          <span style={{ color: COLORS.gold, fontFamily: sansFont('en') }}>{BRAND.handle[lang]}</span>
        </div>
      </div>
      <Grain amount={0.1} frame={f} />
      {sfx && <Audio src={staticFile(sfx.file)} volume={0.55} />}
    </AbsoluteFill>
  );
};
