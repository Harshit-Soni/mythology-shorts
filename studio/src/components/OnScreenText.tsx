import React from 'react';
import { Easing, interpolate, spring } from 'remotion';
import { COLORS, sansFont, serifFont } from '../lib/fonts';
import type { CharRef, Lang, OnScreenText as OST } from '../lib/types';
import { HEAD, framePoint, pointFor } from './Character';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

type Props = {
  ost: NonNullable<OST>;
  lang: Lang;
  sec: number;
  dur: number;
  fps: number;
  chars: CharRef[];
  titleAt: number | null; // seconds into scene when a "title-in" cue fires
  writeEndAt: number | null; // seconds into scene when "write-on" should finish
  stampAt: number | null; // seconds into scene when a "stamp-next" cue fires
};

export const OnScreenText: React.FC<Props> = ({ ost, lang, sec, dur, fps, chars, titleAt, writeEndAt, stampAt }) => {
  const text = ost[lang];
  const serif = serifFont(lang);
  const sans = sansFont(lang);
  const outline = `-3px -3px 0 ${COLORS.outline}, 3px -3px 0 ${COLORS.outline}, -3px 3px 0 ${COLORS.outline}, 3px 3px 0 ${COLORS.outline}, 0 6px 14px rgba(0,0,0,0.5)`;

  switch (ost.style) {
    case 'stamp-gold': {
      const t = sec - (stampAt ?? 0.15);
      if (t < 0) return null;
      const sp = spring({ frame: t * fps, fps, config: { damping: 11, stiffness: 160 } });
      const top = stampAt !== null ? 576 - 110 : 806 - 110;
      return (
        <div style={{ position: 'absolute', top, width: 1080, textAlign: 'center', transform: `rotate(-7deg) scale(${interpolate(sp, [0, 1], [2.6, 1])})`, opacity: Math.min(1, t * 8) }}>
          <span style={{ font: `700 ${lang === 'hi' ? 190 : 150}px ${lang === 'hi' ? serif : sans}`, color: COLORS.gold, letterSpacing: lang === 'hi' ? 0 : 10, textShadow: outline }}>{text}</span>
        </div>
      );
    }
    case 'name-tag': {
      const o = interpolate(sec, [0.2, 0.6], [0, 1], clamp);
      return (
        <div style={{ position: 'absolute', left: 120, top: 210, opacity: o, transform: `translateY(${(1 - o) * 20}px)` }}>
          <div style={{ font: `700 64px ${serif}`, color: COLORS.parchment, textShadow: outline }}>{text}</div>
          <div style={{ width: 220 * o, height: 5, background: COLORS.gold, marginTop: 6, borderRadius: 3 }} />
          {ost.sub && <div style={{ font: `600 36px ${serif}`, color: COLORS.parchment, marginTop: 10, textShadow: outline, fontStyle: lang === 'en' ? 'italic' : 'normal' }}>{ost.sub[lang]}</div>}
        </div>
      );
    }
    case 'speech-bubble': {
      const who = chars.find((c) => c.id === ost.anchor) ?? chars[0];
      const head = who ? framePoint(who, pointFor(HEAD, who)) : { x: 540, y: 700 };
      const sp = spring({ frame: Math.max(0, sec - 0.1) * fps, fps, config: { damping: 14 } });
      if (sec > dur * 0.62) return null; // bubble only while the line is spoken
      const bw = 560;
      const left = Math.min(1080 - bw - 140, Math.max(60, head.x - bw / 2));
      const top = head.y - 270;
      return (
        <div style={{ position: 'absolute', left, top, width: bw, transform: `scale(${sp})`, transformOrigin: `${head.x - left}px 260px` }}>
          <div style={{ background: '#FFFBF0', border: `5px solid ${COLORS.outline}`, borderRadius: 40, padding: '26px 30px', font: `800 50px ${sans}`, color: COLORS.outline, textAlign: 'center' }}>{text}</div>
          <svg width="80" height="70" style={{ position: 'absolute', left: Math.max(20, Math.min(bw - 100, head.x - left - 40)), top: '100%', marginTop: -6 }}>
            <path d="M10 0 L70 0 L30 64 Z" fill="#FFFBF0" stroke={COLORS.outline} strokeWidth="5" />
            <rect x="12" y="0" width="56" height="8" fill="#FFFBF0" />
          </svg>
        </div>
      );
    }
    case 'law-inscription': {
      const end = writeEndAt ?? dur * 0.7;
      const q = interpolate(sec, [0.2, Math.max(0.6, end)], [0, 1], clamp);
      const chars_ = Array.from(text);
      const shown = chars_.slice(0, Math.ceil(q * chars_.length)).join('');
      return (
        <>
          {ost.source && (
            <div style={{ position: 'absolute', top: 230, width: 1080, textAlign: 'center', font: `600 38px ${serif}`, color: '#6B4A2A', opacity: interpolate(sec, [0, 0.5], [0, 1], clamp) }}>
              {ost.source[lang]}
            </div>
          )}
          <div style={{ position: 'absolute', top: 640, left: 140, width: 800, textAlign: 'center', font: `700 ${lang === 'hi' ? 104 : 116}px ${serif}`, color: '#3A2416', lineHeight: 1.25 }}>
            {shown}
          </div>
        </>
      );
    }
    case 'title-serif': {
      const at = titleAt ?? dur * 0.55;
      const t = sec - at;
      if (t < 0) return null;
      const o = interpolate(t, [0, 0.5], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
      return (
        <div style={{ position: 'absolute', top: 140, width: 1080, textAlign: 'center', opacity: o, transform: `translateY(${(1 - o) * 30}px)`, letterSpacing: lang === 'en' ? 18 * o : 0 }}>
          <span style={{ font: `700 150px ${serif}`, color: COLORS.gold, textShadow: outline }}>{text}</span>
        </div>
      );
    }
    default:
      return null;
  }
};
