export type Lang = 'en' | 'hi';
export type L10n = Record<Lang, string>;

export type CharRef = {
  id: string;
  pose: string;
  expression?: string;
  x: number; // 0..1 of frame width: where the character's feet/base sit
  y: number; // 0..1 of frame height
  scale: number; // 1 = the 1000x1600 canvas drawn 1000px tall
  flip?: boolean;
  action?: string;
  variant?: string;
  speaking?: boolean; // flaps mouth during quoted narration
};

export type PropRef = { id: string; x: number; y: number; scale: number; action?: string };

export type Cue = { onWord: L10n; do: string; target?: string; notes?: string };

export type Camera = {
  move: string;
  from?: number;
  to?: number;
  focus?: [number, number];
};

export type OnScreenText = {
  en: string;
  hi: string;
  style: string;
  anchor?: string;
  sub?: L10n;
  source?: L10n;
} | null;

export type Scene = {
  id: string;
  beat: number;
  type: string;
  background: string;
  backgroundVariant?: string;
  characters: CharRef[];
  props: PropRef[];
  camera: Camera;
  narration: L10n;
  onScreenText: OnScreenText;
  cues: Cue[];
  sfx: string[];
  transition: string;
  overlay?: string;
  fixedDurationSec?: number;
  frontLayer?: boolean; // draw the background's layer-front over the characters
  notes?: string;
};

export type EpisodeSpec = {
  id: string;
  title: L10n;
  fps: number;
  width: number;
  height: number;
  sourceCredit: L10n;
  scenes: Scene[];
  format?: string;
  safeZone?: { bottom: number; right: number };
  assets?: unknown;
  assetNotes?: unknown;
};

// Stage 5 output: one audio file per language with word-level timestamps.
export type TimestampFile = { words: { beat: number; text: string; start: number; end: number }[]; [meta: string]: unknown };

export type EpisodeEntry = {
  folder: string;
  spec: EpisodeSpec;
  audio: Partial<Record<Lang, { file: string; timestamps: TimestampFile }>>;
};

export type PoseInfo = {
  file: string;
  w: number;
  h: number;
  face: boolean;
  eyes: 'open' | 'closed';
  mouth: 'open' | 'closed';
  variants: Record<string, string>; // "open|closed" -> file
};
export type FileInfo = { file: string; w: number | null; h: number | null; back?: string; front?: string };
export type Manifest = {
  characters: Record<string, Record<string, PoseInfo>>;
  backgrounds: Record<string, FileInfo>;
  props: Record<string, FileInfo>;
  overlays: Record<string, FileInfo>;
};

export type EpisodeProps = { episodeId: string; lang: Lang; debug: boolean };
