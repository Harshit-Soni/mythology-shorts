import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { MANIFEST } from '../generated/data';
import { COLORS } from '../lib/fonts';

// Backgrounds are 1296x2112 canvases; the 1080x1920 frame sits in the middle (margin for camera moves).
const BW = 1296;
const BH = 2112;

const VARIANT_FILTER: Record<string, string> = {
  night: 'brightness(0.62) saturate(0.75) hue-rotate(-12deg)',
  dusk: 'brightness(0.8) saturate(0.9)',
  dawn: 'brightness(1.05) saturate(0.9)',
  default: '',
};

// Colour stand-ins until the real background exists (so previews still read).
const FALLBACK: Record<string, string> = {
  hermitage: `linear-gradient(180deg, ${COLORS.pink} 0%, ${COLORS.parchment} 45%, #6E8B4E 70%, #4E6B3A 100%)`,
  'king-court': `linear-gradient(180deg, #3B1D1A 0%, #6A2A22 45%, #4A2A24 72%, #3A2422 100%)`,
  'red-sky-plain': `linear-gradient(180deg, #5E1712 0%, #B8361F 40%, #E07A2E 66%, #3A1C14 70%, #241210 100%)`,
  'flashback-meadow': `linear-gradient(180deg, #F3E6C8 0%, #E9D9A8 50%, #A9B66A 68%, #7E8F48 100%)`,
  'parchment-card': `radial-gradient(ellipse at 50% 45%, #F7ECD2 0%, ${COLORS.parchment} 55%, #D8BF8C 100%)`,
  'hastinapura-palace': `linear-gradient(180deg, #F8D9B0 0%, #F3E6C8 38%, #E8B53A 52%, #C98B4A 66%, #D9B98A 100%)`,
  'forest-hunt': `linear-gradient(180deg, #DDE7C4 0%, #7FA05A 40%, #3F6633 70%, #2C4A26 100%)`,
  'cosmic-court': `linear-gradient(180deg, ${COLORS.night} 0%, ${COLORS.dusk} 70%, #8B6F95 100%)`,
};

export const Background: React.FC<{ id: string; variant?: string; debug: boolean; backOnly?: boolean }> = ({ id, variant, debug, backOnly }) => {
  const filter = VARIANT_FILTER[variant ?? 'default'] ?? '';
  if (id === 'split-frame') return <SplitFrame />;
  const file = MANIFEST.backgrounds[id];
  if (file) {
    return (
      <Img
        src={staticFile(backOnly && file.back ? file.back : file.file)}
        style={{ position: 'absolute', left: -(BW - 1080) / 2, top: -(BH - 1920) / 2, width: BW, height: BH, filter: filter || undefined }}
      />
    );
  }
  return (
    <AbsoluteFill style={{ background: FALLBACK[id] ?? '#333', filter: filter || undefined }}>
      {debug && (
        <div style={{ position: 'absolute', top: 260, width: '100%', textAlign: 'center', color: 'rgba(255,255,255,0.8)', font: '600 34px sans-serif', textShadow: '0 2px 6px #000' }}>
          background “{id}” not made yet
        </div>
      )}
    </AbsoluteFill>
  );
};

export const BackgroundFront: React.FC<{ id: string; variant?: string }> = ({ id, variant }) => {
  const file = MANIFEST.backgrounds[id];
  if (!file?.front) return null;
  const filter = VARIANT_FILTER[variant ?? 'default'] ?? '';
  return <Img src={staticFile(file.front)} style={{ position: 'absolute', left: -(BW - 1080) / 2, top: -(BH - 1920) / 2, width: BW, height: BH, filter: filter || undefined }} />;
};

// Layout for "split-frame": two panels (memory | punishment) divided by a folk-art strip.
const Panel: React.FC<{ id: string; left: number; filter?: string }> = ({ id, left, filter }) => {
  const file = MANIFEST.backgrounds[id];
  return (
    <div style={{ position: 'absolute', left, top: 0, width: 540, height: 1920, overflow: 'hidden', background: FALLBACK[id], filter }}>
      {file && <Img src={staticFile(file.file)} style={{ position: 'absolute', left: -108 - (left === 0 ? 270 : 270), top: -96, width: 1296, height: 2112 }} />}
    </div>
  );
};
const SplitFrame: React.FC = () => (
  <AbsoluteFill>
    <Panel id="flashback-meadow" left={0} filter="sepia(0.6)" />
    <Panel id="red-sky-plain" left={540} />
    <div style={{ position: 'absolute', left: 522, top: 0, width: 36, height: 1920, background: `repeating-linear-gradient(180deg, ${COLORS.red} 0 30px, ${COLORS.gold} 30px 36px, ${COLORS.saffron} 36px 60px, ${COLORS.gold} 60px 66px)`, boxShadow: '0 0 18px rgba(0,0,0,0.5)' }} />
  </AbsoluteFill>
);
