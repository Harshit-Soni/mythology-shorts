import React, { useMemo } from 'react';
import { Audio, Sequence, staticFile } from 'remotion';
import { MANIFEST } from '../generated/data';
import { cueTime, type Timeline } from '../lib/timing';
import type { EpisodeSpec, Lang, SfxRef } from '../lib/types';

// Sound pass: one music bed (ducked under the narration, level per scene) plus
// one-shot sound effects at a scene's start or on a spoken word (same cue words as the visuals).
const DUCK_PAD_IN = 0.15; // start dipping this long before a word
const DUCK_PAD_OUT = 0.25; // stay dipped this long after a word
const DUCK_RAMP = 0.3; // seconds to ease between full and ducked
const LEVEL_RAMP = 0.5; // seconds to ease a scene's music level across a cut

const clamp01 = (x: number) => Math.max(0, Math.min(1, x));

export const Sound: React.FC<{ spec: EpisodeSpec; tl: Timeline; lang: Lang; fps: number; total: number }> = ({ spec, tl, lang, fps, total }) => {
  const music = spec.sound?.music;
  const musicFile = music ? MANIFEST.music[music.id] : undefined;

  // narration intervals, merged so short gaps between words don't pump the music
  const talk = useMemo(() => {
    const out: [number, number][] = [];
    for (const w of tl.words) {
      const a = w.start - DUCK_PAD_IN;
      const b = w.end + DUCK_PAD_OUT;
      const last = out[out.length - 1];
      if (last && a <= last[1] + 0.35) last[1] = Math.max(last[1], b);
      else out.push([a, b]);
    }
    return out;
  }, [tl]);

  const sfx = useMemo(() => {
    const list: { key: string; file: string; t: number; volume: number }[] = [];
    const base = spec.sound?.sfxVolume ?? 1;
    tl.segments.forEach((seg, i) => {
      for (const ref of seg.scene.sfx ?? []) {
        const o: Exclude<SfxRef, string> = typeof ref === 'string' ? { id: ref } : ref;
        const f = MANIFEST.sfx[o.id];
        if (!f) continue; // not generated yet: a note only
        const r = o;
        const t0 = o.onWord ? cueTime(seg, { onWord: o.onWord, do: 'sfx' }, lang) : seg.start + (o.at ?? 0);
        list.push({ key: `${seg.scene.id}-${i}-${r.id}`, file: f.file, t: Math.max(0, t0 + (o.offset ?? 0)), volume: base * (o.volume ?? 1) });
      }
    });
    return list;
  }, [spec, tl, lang]);

  const musicVolume = (frame: number) => {
    if (!music) return 0;
    const t = frame / fps;
    const vol = music.volume ?? 0.25;
    const ducked = music.duckTo ?? vol * 0.4;
    // distance to the nearest narration interval (0 while speaking)
    let d = Infinity;
    for (const [a, b] of talk) {
      if (t >= a && t <= b) { d = 0; break; }
      d = Math.min(d, t < a ? a - t : t - b);
    }
    const duck = clamp01(d / DUCK_RAMP); // 0 = fully ducked, 1 = full
    // scene level, eased from the previous scene's level across the cut
    const i = Math.max(0, tl.segments.findIndex((s) => t >= s.start && t < s.end));
    const lvl = (k: number) => tl.segments[k]?.scene.music ?? 1;
    const s = tl.segments[i];
    const level = s && i > 0 && t - s.start < LEVEL_RAMP ? lvl(i - 1) + (lvl(i) - lvl(i - 1)) * ((t - s.start) / LEVEL_RAMP) : lvl(i);
    const fadeIn = clamp01(t / (music.fadeInSec ?? 0.5));
    const fadeOut = clamp01((total - t) / (music.fadeOutSec ?? 1.5));
    return (ducked + (vol - ducked) * duck) * level * fadeIn * fadeOut;
  };

  return (
    <>
      {musicFile && <Audio src={staticFile(musicFile.file)} volume={musicVolume} loop />}
      {sfx.map((x) => (
        <Sequence key={x.key} from={Math.round(x.t * fps)} name={`sfx ${x.key}`} layout="none">
          <Audio src={staticFile(x.file)} volume={x.volume} />
        </Sequence>
      ))}
    </>
  );
};
