import { loadFont as loadPoppins } from '@remotion/google-fonts/Poppins';
import { loadFont as loadHind } from '@remotion/google-fonts/Hind';
import { loadFont as loadCormorant } from '@remotion/google-fonts/CormorantGaramond';
import { loadFont as loadTiro } from '@remotion/google-fonts/TiroDevanagariHindi';
import type { Lang } from './types';

const poppins = loadPoppins('normal', { weights: ['600', '800'], subsets: ['latin'] });
const hind = loadHind('normal', { weights: ['600', '700'], subsets: ['devanagari', 'latin'] });
const cormorant = loadCormorant('normal', { weights: ['600', '700'], subsets: ['latin'] });
const tiro = loadTiro('normal', { weights: ['400'], subsets: ['devanagari', 'latin'] });

// Captions / bubbles: bold sans. Titles / inscriptions: serif. (STYLE_GUIDE.md → Type)
export const sansFont = (lang: Lang) => (lang === 'hi' ? hind.fontFamily : poppins.fontFamily);
export const serifFont = (lang: Lang) => (lang === 'hi' ? tiro.fontFamily : cormorant.fontFamily);

export const COLORS = {
  outline: '#1E1420',
  gold: '#E8B53A',
  saffron: '#E07A2E',
  parchment: '#F3E6C8',
  red: '#8E2A20',
  night: '#1B1A3A',
  dusk: '#5B3B7A',
  pink: '#E39AA0',
};
