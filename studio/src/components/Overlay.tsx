import React from 'react';
import { AbsoluteFill, Img, interpolate, staticFile } from 'remotion';
import { MANIFEST } from '../generated/data';
import { COLORS } from '../lib/fonts';

// Screen-space overlays (not affected by the camera).
// "inset" animates the folk-art border closing in from outside the frame (series sting).
export const Overlay: React.FC<{ id: string; inset?: number }> = ({ id, inset = 0 }) => {
  const file = MANIFEST.overlays[id];
  if (id === 'folk-art-border') {
    const grow = interpolate(inset, [0, 1], [1.25, 1]);
    if (file) return <Img src={staticFile(file.file)} style={{ position: 'absolute', inset: 0, width: 1080, height: 1920, transform: `scale(${grow})` }} />;
    return <CodeBorder grow={grow} />;
  }
  if (id === 'sepia-folk-frame') {
    if (file) return <Img src={staticFile(file.file)} style={{ position: 'absolute', inset: 0, width: 1080, height: 1920 }} />;
    return <ArchFrame />;
  }
  return null;
};

// Fallback border until overlay__folk-art-border.svg exists: same proportions as the approved concept (~8% band).
const CodeBorder: React.FC<{ grow: number }> = ({ grow }) => {
  const b = 86;
  const corner = (x: number, y: number) => (
    <g transform={`translate(${x} ${y})`}>
      <circle r="58" fill={COLORS.gold} stroke={COLORS.outline} strokeWidth="4" />
      <circle r="44" fill={COLORS.red} />
      {[0, 1, 2, 3, 4].map((i) => (
        <ellipse key={i} cx="0" cy="-14" rx="10" ry="24" fill={COLORS.parchment} transform={`rotate(${(i - 2) * 32})`} />
      ))}
    </g>
  );
  return (
    <AbsoluteFill style={{ transform: `scale(${grow})` }}>
      <svg width="1080" height="1920" viewBox="0 0 1080 1920">
        <path fillRule="evenodd" fill={COLORS.red} d={`M0 0H1080V1920H0Z M${b} ${b}H${1080 - b}V${1920 - b}H${b}Z`} />
        <rect x="10" y="10" width="1060" height="1900" fill="none" stroke={COLORS.outline} strokeWidth="6" />
        <rect x={b - 14} y={b - 14} width={1080 - 2 * (b - 14)} height={1920 - 2 * (b - 14)} fill="none" stroke={COLORS.gold} strokeWidth="5" strokeDasharray="2 12" strokeLinecap="round" />
        <rect x={b - 4} y={b - 4} width={1080 - 2 * (b - 4)} height={1920 - 2 * (b - 4)} fill="none" stroke={COLORS.saffron} strokeWidth="8" />
        {Array.from({ length: 9 }).map((_, i) => (
          <g key={`h${i}`} fill={COLORS.parchment}>
            <circle cx={150 + i * 97} cy={b / 2 + 2} r="9" />
            <circle cx={150 + i * 97} cy={1920 - b / 2 - 2} r="9" />
          </g>
        ))}
        {Array.from({ length: 17 }).map((_, i) => (
          <g key={`v${i}`} fill={COLORS.parchment}>
            <circle cx={b / 2} cy={170 + i * 99} r="9" />
            <circle cx={1080 - b / 2} cy={170 + i * 99} r="9" />
          </g>
        ))}
        {corner(b / 2 + 6, b / 2 + 6)}
        {corner(1080 - b / 2 - 6, b / 2 + 6)}
        {corner(b / 2 + 6, 1920 - b / 2 - 6)}
        {corner(1080 - b / 2 - 6, 1920 - b / 2 - 6)}
      </svg>
    </AbsoluteFill>
  );
};

// Fallback flashback frame: temple-door arch window in sepia.
const ArchFrame: React.FC = () => (
  <AbsoluteFill>
    <svg width="1080" height="1920" viewBox="0 0 1080 1920">
      <path fillRule="evenodd" fill="#5A3A22" opacity="0.92" d="M0 0H1080V1920H0Z M120 1650V700Q120 330 540 300Q960 330 960 700V1650Z" />
      <path fill="none" stroke="#C9A36A" strokeWidth="10" d="M120 1650V700Q120 330 540 300Q960 330 960 700V1650Z" />
      <path fill="none" stroke="#C9A36A" strokeWidth="3" strokeDasharray="4 14" d="M96 1674V700Q96 306 540 276Q984 306 984 700V1674Z" />
    </svg>
  </AbsoluteFill>
);
