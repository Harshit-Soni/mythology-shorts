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

// Sound pass. A plain string is a note (ignored unless assets/sfx/<id>.mp3 exists, then it plays at scene start).
export type SfxRef = string | { id: string; onWord?: L10n; at?: number; offset?: number; volume?: number; notes?: string };
export type SoundSpec = {
  music?: { id: string; volume?: number; duckTo?: number; fadeInSec?: number; fadeOutSec?: number };
  sfxVolume?: number;
};

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
  at?: [number, number]; // speech-bubble: speaker's head position (0..1) when there are no puppets
  y?: number; // law-inscription: vertical centre (0..1)
  light?: boolean; // law-inscription: light source label (dark backgrounds)
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
  sfx: SfxRef[];
  music?: number; // music level for this scene, 0..1 (default 1), eased across the cut
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
  sound?: SoundSpec;
  assetNotes?: unknown;
};

// Stage 5 output: one audio file per language with word-level timestamps.
export type TimestampFile = { words: { beat: number; text: string; start: number; end: number }[]; [meta: string]: unknown };

// Illustrated version (episodes/<ID>/illustrated/03-shots.json): one painted image per shot.
export type FxSpec = { type: string; x?: number; y?: number; r?: number; n?: number; color?: string; pulse?: boolean };
export type ShotCue = { onWord: L10n; do: string; x?: number; y?: number };
export type Shot = {
  id: string;
  beat: number;
  kind?: 'image' | 'scene' | 'split';
  at?: L10n; // starts on this word of its beat (else at the beat's start)
  scene?: string; // kind 'scene': render this cut-out scene (e.g. the series sting)
  split?: [string, string]; // kind 'split': left/right images taken from these shots
  image?: string;
  file?: string; // filled by prepare.mjs: public path of the image
  baseScale?: number; // extra zoom, e.g. to crop a painted border
  camera?: Camera;
  fx?: FxSpec[];
  cues?: ShotCue[];
  onScreenText?: OnScreenText;
  overlay?: string;
  transition: string;
  chars?: string[]; // characters in the shot (for the prompt; not used by the renderer)
  prompt?: string; // image prompt, kept for the record
  motion?: string; // motion notes (for a later animated-clip version)
};
export type ShotSpec = { episode: string; style?: string; shots: Shot[]; [meta: string]: unknown };

export type EpisodeEntry = {
  folder: string;
  spec: EpisodeSpec;
  audio: Partial<Record<Lang, { file: string; timestamps: TimestampFile }>>;
  shots?: ShotSpec;
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
  sfx: Record<string, FileInfo>;
  music: Record<string, FileInfo>;
};

export type EpisodeProps = { episodeId: string; lang: Lang; debug: boolean };
