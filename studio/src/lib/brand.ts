// The channel's identity, used by the end card and thumbnails on every episode.
// Source of truth for the wording: channel/brand-kit.md. Emblem: assets/brand/emblem.png
// (made from channel/logo/final/icon-master-2000.png, round, transparent corners).
export const BRAND = {
  name: 'THE LOST GYAAN',
  nameHi: 'द लॉस्ट ज्ञान',
  // every end card points to the main handle; its bio links the English account (@thelostgyaan_en)
  handle: { en: '@thelostgyaan', hi: '@thelostgyaan' },
  emblem: 'assets/brand/emblem.png',
  tagline: { en: 'What history forgot, we remember', hi: 'जो इतिहास भूल गया, वो हमें याद है' },
  cta: { en: 'Follow', hi: 'फ़ॉलो करें' },
  endCardSec: 2,
  endCardSfx: 'shimmer-descend',
};
