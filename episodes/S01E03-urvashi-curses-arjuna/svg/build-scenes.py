"""S01E03 scene spec. Narration is parsed from 02-script.md (never retyped).
Run from anywhere:  python3 episodes/S01E03-urvashi-curses-arjuna/svg/build-scenes.py <repo root>
"""
import json, re, sys
root = sys.argv[1]
ep = f'{root}/episodes/S01E03-urvashi-curses-arjuna'
src = open(f'{ep}/02-script.md').read()

def beats(section):
    out = {}
    for line in section.split('\n'):
        m = re.match(r'^\| (\d+)[^|]*\| (.*?) \|', line)
        if m: out[int(m.group(1))] = m.group(2).strip()
    return out
EN = beats(src.split('## English')[1].split('**Word count')[0])
HI = beats(src.split('## हिंदी')[1].split('**Word count')[0])
assert len(EN) == 16 and len(HI) == 16, (len(EN), len(HI))
N = lambda b: {'en': EN[b], 'hi': HI[b]}
E = {'en': '', 'hi': ''}
W = lambda en, hi: {'en': en, 'hi': hi}
def C(id, pose, x, y, scale, flip=False, action='breathe', **kw):
    d = {'id': id, 'pose': pose, 'x': x, 'y': y, 'scale': scale, 'flip': flip, 'action': action}; d.update(kw); return d
def P(id, x, y, scale, action='idle'):
    return {'id': id, 'x': x, 'y': y, 'scale': scale, 'action': action}

e02 = json.load(open(f'{root}/episodes/S01E02-kindama-curses-pandu/03-scenes.json'))
sting = next(s for s in e02['scenes'] if s['id'] == 's00')
sting = {**sting, 'onScreenText': {**sting['onScreenText'], 'en': 'CURSED III', 'hi': 'शाप III'}}

AC = 'amaravati-court'   # floor feet ≈ 0.86; stage on the right, top ≈ 0.73–0.78 (x ≥ 0.6)
KC = 'king-court'        # throne seat x 0.5, seated base y 0.575, scale ≈ 0.83; floor feet TBC at render (≈ 0.88)
RP = 'red-sky-plain'     # standing feet ≈ 0.80–0.82

scenes = [sting,
 # 1 hook
 {'id': 's01', 'beat': 1, 'type': 'character', 'background': AC, 'backgroundVariant': 'night', 'light': 'night',
  'fx': [{'type': 'stars', 'n': 30}, {'type': 'glow', 'x': 0.68, 'y': 0.55, 'r': 0.3, 'color': '#E07A2E', 'pulse': True}],
  'characters': [C('arjuna', 'kneeling-folded-hands', 0.3, 0.86, 0.95, expression='eyes-closed'),
                 C('urvashi', 'cursing-hand-raised', 0.68, 0.86, 1.0, flip=True, action='raise-hand', expression='furious')],
  'props': [P('shaap-stamp', 0.5, 0.3, 0.7, 'stamp-in')],
  'camera': {'move': 'push-in-fast', 'from': 1.0, 'to': 1.15, 'focus': [0.5, 0.6]},
  'narration': N(1), 'onScreenText': {'en': 'CURSED', 'hi': 'शाप', 'style': 'stamp-gold'},
  'cues': [{'onWord': W('cursed', 'शाप'), 'do': 'light-burst-saffron', 'target': 'urvashi'},
           {'onWord': W('cursed', 'शाप'), 'do': 'stamp-next', 'target': 'shaap-stamp'}],
  'sfx': [{'id': 'heartbeat', 'at': 0, 'volume': 0.5}, {'id': 'thunder-crack', 'onWord': W('cursed', 'शाप'), 'volume': 0.6},
          {'id': 'stamp-thud', 'onWord': W('cursed', 'शाप'), 'offset': 0.1, 'volume': 0.8}],
  'transition': 'flash-white',
  'notes': 'Hook (flash-forward to s10). Arjuna kneels, eyes closed, palms joined; Urvashi (flipped, faces him) raises her hand; saffron burst + stamp on "cursed / शाप". Dignified: Urvashi in full court dress, nothing revealing.'},
 # 2 Amaravati
 {'id': 's02', 'beat': 2, 'type': 'character', 'background': AC, 'light': 'divine',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.15, 'color': '#FFE6B0'}, {'type': 'stars', 'n': 25}],
  'characters': [C('arjuna', 'standing-bow', 0.34, 0.86, 0.95, action='step-forward', expression='awed')],
  'props': [P('celestial-chariot', 0.66, 0.5, 0.9, 'descend')],
  'camera': {'move': 'tilt-down', 'from': -0.12, 'to': 0.0},
  'narration': N(2),
  'onScreenText': {'en': 'Amaravati', 'hi': 'अमरावती', 'style': 'name-tag', 'sub': {'en': 'Mahabharata, Vana Parva', 'hi': 'महाभारत, वन पर्व'}},
  'cues': [], 'sfx': [{'id': 'shimmer-descend', 'onWord': W('Amaravati', 'अमरावती'), 'volume': 0.6}],
  'transition': 'dissolve',
  'notes': 'Indra’s charioteer Matali brought him (Vana §42–43): the golden chariot settles behind him on the clouds as the camera tilts down from the spires. Source tag on screen once.'},
 # 3 weapons
 {'id': 's03', 'beat': 3, 'type': 'character', 'background': AC, 'light': 'divine',
  'fx': [{'type': 'glow', 'x': 0.5, 'y': 0.42, 'r': 0.35, 'color': '#E8B53A', 'pulse': True}, {'type': 'sparks', 'n': 18}],
  'characters': [C('arjuna', 'standing-bow', 0.3, 0.86, 0.95, expression='calm'),
                 C('indra', 'standing-blessing', 0.7, 0.86, 1.0, flip=True, expression='proud')],
  'props': [P('astra-ring', 0.5, 0.4, 0.8, 'circle'), P('vajra-flash', 0.5, 0.3, 0.6, 'stamp-in')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06, 'focus': [0.5, 0.5]},
  'narration': N(3), 'onScreenText': None,
  'cues': [{'onWord': W('thunderbolt', 'वज्र'), 'do': 'stamp-in', 'target': 'vajra-flash'}],
  'sfx': [{'id': 'thunder-crack', 'onWord': W('thunderbolt', 'वज्र'), 'volume': 0.5}],
  'transition': 'cut',
  'notes': 'Indra (new, gold halo, faces Arjuna) and Arjuna. A ring of glowing weapon glyphs circles between them; the vajra lands on "thunderbolt / वज्र".'},
 # 4 learn to dance
 {'id': 's04', 'beat': 4, 'type': 'character', 'background': AC, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 20, 'color': '#FFE6B0'}],
  'characters': [C('arjuna', 'dance-step', 0.3, 0.86, 0.95, action='sway', expression='surprised'),
                 C('chitrasena', 'playing-veena', 0.7, 0.86, 0.95, flip=True, expression='smiling')],
  'props': [],
  'camera': {'move': 'slow-pan-right', 'from': 0.0, 'to': 0.03},
  'narration': N(4),
  'onScreenText': {'en': 'Chitrasena', 'hi': 'चित्रसेन', 'style': 'name-tag', 'sub': {'en': 'king of the Gandharvas', 'hi': 'गन्धर्वों के राजा'}},
  'cues': [], 'sfx': [{'id': 'temple-bells', 'onWord': W('dance', 'नाचना'), 'volume': 0.5}],
  'transition': 'cut',
  'notes': 'A light beat: the archer, bow laid aside, tries a first dance step (one hand raised in a mudra, one foot lifted) while Chitrasena plays the veena. This is in the critical edition (Vana §44).'},
 # 5 the court dance
 {'id': 's05', 'beat': 5, 'type': 'character', 'background': AC, 'light': 'divine',
  'fx': [{'type': 'stars', 'n': 25}, {'type': 'glow', 'x': 0.72, 'y': 0.55, 'r': 0.3, 'color': '#F2A7B8', 'pulse': True}],
  'characters': [C('arjuna', 'standing-bow', 0.22, 0.88, 0.9, action='still', expression='awed'),
                 C('urvashi', 'dancing', 0.7, 0.76, 0.85, flip=True, action='sway', expression='smiling')],
  'props': [P('apsara-silhouette', 0.5, 0.62, 0.6, 'sway'), P('apsara-silhouette', 0.86, 0.6, 0.55, 'sway')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.1, 'focus': [0.7, 0.55]},
  'narration': N(5), 'onScreenText': None,
  'cues': [], 'sfx': [{'id': 'temple-bells', 'at': 0.2, 'volume': 0.4}],
  'transition': 'cut',
  'notes': 'Urvashi dances on the stage (feet on the stage top ≈ 0.76), lit; the other apsaras are the library silhouettes behind. Arjuna watches from the floor at left. Camera drifts toward Urvashi. Graceful classical pose, fully dressed.'},
 # 6 popular telling: the night visit
 {'id': 's06', 'beat': 6, 'type': 'character', 'background': AC, 'backgroundVariant': 'night', 'light': 'moon',
  'fx': [{'type': 'stars', 'n': 40}, {'type': 'fog', 'color': '#9FB3D9'}],
  'characters': [C('urvashi', 'walking', 0.62, 0.86, 0.95, flip=True, action='walk-left', expression='hopeful')],
  'props': [],
  'camera': {'move': 'slow-pan-right', 'from': 0.03, 'to': 0.0},
  'narration': N(6),
  'onScreenText': {'en': 'The popular telling', 'hi': 'प्रचलित कथा', 'style': 'name-tag', 'sub': {'en': 'Vana Parva §46 (vulgate)', 'hi': 'वन पर्व §46 (प्रचलित पाठ)'}},
  'cues': [], 'sfx': [{'id': 'night-crickets', 'at': 0, 'volume': 0.4}],
  'transition': 'dissolve',
  'notes': 'The honesty tag: from here to s11 is the vulgate. Moonlit court; Urvashi (flipped) walks left toward Arjuna’s door. Movement follows facing.'},
 # 7 he bows
 {'id': 's07', 'beat': 7, 'type': 'character', 'background': AC, 'backgroundVariant': 'night', 'light': 'moon',
  'fx': [{'type': 'stars', 'n': 30}],
  'characters': [C('arjuna', 'bowing-eyes-closed', 0.32, 0.86, 0.95, action='bow', expression='eyes-closed'),
                 C('urvashi', 'standing-surprised', 0.7, 0.86, 0.95, flip=True, action='still', expression='surprised')],
  'props': [],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06, 'focus': [0.5, 0.55]},
  'narration': N(7), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'heartbeat', 'onWord': W('bowed', 'प्रणाम'), 'volume': 0.45}],
  'transition': 'memory-ripple',
  'notes': 'Arjuna bows with closed eyes and joined palms, as to an elder (§46); Urvashi stops, surprised.'},
 # 8 family line
 {'id': 's08', 'beat': 8, 'type': 'prop-hero', 'background': 'parchment-card', 'light': 'divine',
  'characters': [], 'props': [P('family-vine', 0.5, 0.5, 1.2, 'glint')],
  'overlay': 'sepia-folk-frame',
  'camera': {'move': 'slow-pan-up', 'from': 0.04, 'to': 0.0},
  'narration': N(8),
  'onScreenText': {'en': 'King Pururavas', 'hi': 'राजा पुरूरवा', 'style': 'name-tag', 'sub': {'en': 'Urvashi’s husband, Arjuna’s ancestor', 'hi': 'उर्वशी के पति, अर्जुन के पूर्वज'}},
  'cues': [{'onWord': W('Pururavas', 'पुरूरवा'), 'do': 'glint', 'target': 'family-vine'}],
  'sfx': [{'id': 'gong-soft', 'onWord': W('Pururavas', 'पुरूरवा'), 'volume': 0.5}],
  'transition': 'memory-ripple',
  'notes': 'A folk-art family vine on parchment (Adi §75): a royal couple medallion at the top (Pururavas & Urvashi), a vine running down through small medallions to a bow-and-crown medallion (Arjuna) at the bottom. No readable names inside the art; the name-tag carries it.'},
 # 9 "as Kunti is to me"
 {'id': 's09', 'beat': 9, 'type': 'character', 'background': AC, 'backgroundVariant': 'night', 'light': 'moon',
  'fx': [{'type': 'glow', 'x': 0.3, 'y': 0.6, 'r': 0.3, 'color': '#FFE6B0', 'pulse': True}],
  'characters': [C('arjuna', 'kneeling-folded-hands', 0.3, 0.86, 0.95, expression='earnest', speaking=True),
                 C('urvashi', 'standing-surprised', 0.7, 0.86, 0.95, flip=True, action='still', expression='hurt')],
  'props': [],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.08, 'focus': [0.35, 0.6]},
  'narration': N(9), 'onScreenText': None, 'cues': [], 'sfx': [],
  'transition': 'cut',
  'notes': 'Arjuna kneels at her feet and speaks ("as Kunti… so are you"); a warm glow around him. Urvashi’s face turns from surprise to hurt.'},
 # 10 the curse
 {'id': 's10', 'beat': 10, 'type': 'character', 'background': AC, 'backgroundVariant': 'night', 'light': 'night',
  'fx': [{'type': 'glow', 'x': 0.68, 'y': 0.55, 'r': 0.3, 'color': '#E07A2E', 'pulse': True}, {'type': 'sparks', 'n': 15}],
  'characters': [C('arjuna', 'kneeling-folded-hands', 0.3, 0.86, 0.95, expression='shocked'),
                 C('urvashi', 'cursing-hand-raised', 0.68, 0.86, 1.0, flip=True, action='raise-hand', expression='furious', speaking=True)],
  'props': [P('shaap-stamp', 0.5, 0.3, 0.7, 'stamp-in')],
  'camera': {'move': 'shake-then-zoom', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.6]},
  'narration': N(10), 'onScreenText': {'en': 'CURSED', 'hi': 'शाप', 'style': 'stamp-gold'},
  'cues': [{'onWord': W('cursed', 'शाप'), 'do': 'light-burst-saffron', 'target': 'urvashi'},
           {'onWord': W('manhood', 'पुरुषत्व'), 'do': 'stamp-next', 'target': 'shaap-stamp'}],
  'sfx': [{'id': 'thunder-crack', 'onWord': W('cursed', 'शाप'), 'volume': 0.6},
          {'id': 'stamp-thud', 'onWord': W('manhood', 'पुरुषत्व'), 'volume': 0.8}],
  'music': 1.1, 'transition': 'flash-white',
  'notes': 'The curse (the hook pays off). Burst from her raised hand on "cursed / शाप"; the stamp lands on "manhood / पुरुषत्व". Same framing as s01 so the viewer recognises it.'},
 # 11 Indra smiles
 {'id': 's11', 'beat': 11, 'type': 'character', 'background': AC, 'backgroundVariant': 'dawn', 'light': 'divine',
  'fx': [{'type': 'rays', 'x': 0.7, 'y': 0.2, 'color': '#FFE6B0'}, {'type': 'sparks', 'n': 12}],
  'characters': [C('arjuna', 'standing-bow', 0.3, 0.86, 0.95, expression='worried'),
                 C('indra', 'standing-blessing', 0.7, 0.86, 1.0, flip=True, expression='smiling', speaking=True)],
  'props': [P('year-ring', 0.5, 0.3, 0.7, 'idle')],
  'camera': {'move': 'slow-zoom-out', 'from': 1.06, 'to': 1.0},
  'narration': N(11), 'onScreenText': None,
  'cues': [{'onWord': W('one', 'एक'), 'do': 'glint', 'target': 'year-ring'}],
  'sfx': [{'id': 'shimmer-descend', 'onWord': W('smiled', 'मुस्कुराए'), 'volume': 0.5}],
  'transition': 'light-wipe',
  'notes': 'Indra, warm and smiling, blesses Arjuna. Above them a ring of 13 segments (the exile years); on "one / एक" the last segment lights alone.'},
 # 12 Brihannala arrives
 {'id': 's12', 'beat': 12, 'type': 'character', 'background': KC, 'light': 'dawn',
  'fx': [{'type': 'dust', 'n': 15}],
  'characters': [C('king', 'seated-throne-pointing', 0.5, 0.575, 0.83, action='still', expression='curious'),
                 C('brihannala', 'standing-graceful', 0.24, 0.88, 0.95, action='step-forward', expression='calm')],
  'props': [],
  'camera': {'move': 'slow-zoom-out', 'from': 1.08, 'to': 1.0, 'focus': [0.4, 0.6]},
  'narration': N(12),
  'onScreenText': {'en': 'Brihannala', 'hi': 'बृहन्नला', 'style': 'name-tag', 'sub': {'en': 'Arjuna, in the year of hiding', 'hi': 'अज्ञातवास में अर्जुन'}},
  'cues': [], 'sfx': [{'id': 'gong-soft', 'onWord': W('Brihannala', 'बृहन्नला'), 'volume': 0.5}],
  'transition': 'cut',
  'notes': 'Virata = the library king on the throne (seated-throne-pointing faces left, toward the newcomer: "whence comes this person?", Virata §11). Brihannala at left: tall, a long braid, large earrings, conch bangles, a woman’s dress, dignified. Floor ground line of king-court to be measured at render.'},
 # 13 bangles, then teaching Uttara
 {'id': 's13', 'beat': 13, 'type': 'prop-hero', 'background': 'parchment-card', 'light': 'dusk', 'overlay': 'sepia-folk-frame',
  'characters': [], 'props': [P('bangles-scarred-arm', 0.5, 0.46, 1.45, 'still')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.12, 'focus': [0.5, 0.48]},
  'narration': N(13), 'onScreenText': None,
  'cues': [{'onWord': W('Arjuna', 'अर्जुन'), 'do': 'hard-cut-to', 'target': 's13b'}],
  'sfx': [{'id': 'bowstring-creak', 'at': 0.2, 'volume': 0.4}],
  'transition': 'cut',
  'notes': 'Close-up (Virata §2): a strong forearm with bowstring scars; gold conch bangles slide down over them. Then cut to the lesson.'},
 {'id': 's13b', 'beat': 13, 'type': 'character', 'background': KC, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 15, 'color': '#FFE6B0'}],
  'characters': [C('brihannala', 'dance-teaching', 0.3, 0.88, 0.95, action='sway', expression='smiling'),
                 C('uttara', 'dancing', 0.7, 0.88, 0.85, flip=True, action='sway', expression='joyful')],
  'props': [], 'camera': {'move': 'slow-pan-right', 'from': 0.0, 'to': 0.03},
  'narration': E, 'onScreenText': None, 'cues': [], 'sfx': [{'id': 'temple-bells', 'at': 0.2, 'volume': 0.4}],
  'transition': 'cut',
  'notes': 'Insert: Brihannala, one hand in a mudra, teaches; young Princess Uttara copies the step. Teacher and pupil, nothing more (she later trusts him "as a father", Virata §72).'},
 # 14 cattle raid: shami tree, then alone vs the army
 {'id': 's14', 'beat': 14, 'type': 'character', 'background': 'forest-hunt', 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 20}, {'type': 'glow', 'x': 0.62, 'y': 0.45, 'r': 0.25, 'color': '#E8B53A', 'pulse': True}],
  'characters': [C('brihannala', 'reaching-up', 0.32, 0.86, 0.95, expression='determined')],
  'props': [P('shami-tree', 0.66, 0.6, 1.3, 'still'), P('gandiva', 0.6, 0.42, 0.7, 'idle')],
  'camera': {'move': 'crane-up', 'from': 0.0, 'to': -0.05},
  'narration': N(14), 'onScreenText': None,
  'cues': [{'onWord': W('Gandiva', 'गाण्डीव'), 'do': 'glint', 'target': 'gandiva'},
           {'onWord': W('alone', 'अकेले'), 'do': 'hard-cut-to', 'target': 's14b'}],
  'sfx': [{'id': 'battle-distant', 'at': 0, 'volume': 0.35}, {'id': 'bowstring-creak', 'onWord': W('Gandiva', 'गाण्डीव'), 'volume': 0.6}],
  'transition': 'cut',
  'notes': 'The shami tree where the Pandavas hid their weapons (Virata §38–43): Brihannala reaches up; the Gandiva, wrapped in the branches, glints on its name.'},
 {'id': 's14b', 'beat': 14, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 25}, {'type': 'dust', 'n': 20}],
  'characters': [C('brihannala', 'drawing-gandiva', 0.28, 0.82, 1.0, action='draw-bow', expression='fierce')],
  'props': [P('battle-silhouettes', 0.68, 0.7, 1.1, 'still'), P('gandiva-shockwave', 0.55, 0.6, 1.0, 'stamp-in')],
  'camera': {'move': 'shake-small-then-static'},
  'narration': E, 'onScreenText': None,
  'cues': [],
  'sfx': [{'id': 'arrow-whoosh-magic', 'at': 0.1, 'volume': 0.7}, {'id': 'drum-boom-deep', 'at': 0.4, 'volume': 0.9}],
  'music': 1.2, 'transition': 'cut',
  'notes': 'Insert from "alone / अकेले": the braid flying, Brihannala draws the Gandiva; a gold shock-ring from the bowstring rolls over the Kuru army in silhouette, which freezes (Virata §65: stunned, not killed). Bhishma is NOT singled out here.'},
 # 15 payoff
 {'id': 's15', 'beat': 15, 'type': 'character', 'background': RP, 'backgroundVariant': 'dawn', 'light': 'dawn',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.2, 'color': '#FFE6B0'}, {'type': 'dust', 'n': 15}],
  'characters': [C('brihannala', 'gandiva-raised', 0.5, 0.82, 1.05, action='still', expression='calm')],
  'props': [],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06, 'focus': [0.5, 0.45]},
  'narration': N(15),
  'onScreenText': {'en': 'The curse became the disguise.', 'hi': 'शाप ही भेस बन गया।', 'style': 'title-serif'},
  'cues': [{'onWord': W('disguise', 'भेस'), 'do': 'title-in'}],
  'sfx': [{'id': 'drum-hit', 'onWord': W('disguise', 'भेस'), 'volume': 0.8}],
  'transition': 'border-wipe',
  'notes': 'Hero tableau, centred: Brihannala, braid in the wind, Gandiva raised at dawn. Dignity, not a joke.'},
 # 16 tease E04
 {'id': 's16', 'beat': 16, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'silhouette',
  'fx': [{'type': 'embers', 'n': 20}, {'type': 'glow', 'x': 0.66, 'y': 0.45, 'r': 0.3, 'color': '#E07A2E', 'pulse': True}],
  'characters': [],
  'props': [P('bhishma-silhouette', 0.36, 0.62, 1.0, 'still'), P('amba-shadow', 0.68, 0.55, 1.0, 'ascend'), P('shaap-stamp', 0.5, 0.3, 0.7, 'stamp-in')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.1},
  'narration': N(16), 'onScreenText': {'en': 'CURSED IV', 'hi': 'शाप IV', 'style': 'stamp-gold'},
  'cues': [{'onWord': W('Bhishma', 'भीष्म'), 'do': 'stamp-next', 'target': 'shaap-stamp'}],
  'sfx': [{'id': 'drum-hit', 'onWord': W('Bhishma', 'भीष्म'), 'volume': 0.9}],
  'overlay': 'folk-art-border', 'transition': 'cut-to-black',
  'notes': 'Tease for S01E04 (Amba’s vow). Bhishma, white-bearded, in silhouette; a woman’s tall shadow rises behind him. Both silhouettes are reusable for E04.'},
]

# the court scenes: characters ~15% larger so they fill 50–70% of the frame height (STYLE_GUIDE → Composition)
for s in scenes:
    if s.get('background') == AC:
        for c in s.get('characters', []):
            c['scale'] = round(c['scale'] * 1.15, 3)

doc = {
 'id': 'S01E03', 'title': {'en': 'The Apsara Who Cursed Arjuna', 'hi': 'जब अप्सरा ने अर्जुन को शाप दिया'},
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Mahabharata, Vana Parva & Virata Parva', 'hi': 'महाभारत, वन पर्व और विराट पर्व'},
 'safeZone': {'bottom': 0.2, 'right': 0.12},
 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True},
 'sound': e02['sound'],
 'thumbnail': {'scene': 's10', 'at': 0.5, 'series': {'en': 'Shraap · Episode 3', 'hi': 'शाप · भाग 3'},
   'title': {'en': 'The Apsara Who Cursed Arjuna', 'hi': 'जब अप्सरा ने अर्जुन को शाप दिया'},
   'titleLines': {'en': ['The Apsara', 'Who Cursed', 'Arjuna'], 'hi': ['जब अप्सरा ने', 'अर्जुन को शाप दिया']}},
 'scenes': scenes,
 'assets': {
  'characters': [
   {'id': 'arjuna', 'status': 'library', 'poses': {'standing-bow': 'redo', 'kneeling-folded-hands': 'new', 'bowing-eyes-closed': 'new', 'dance-step': 'new'},
    'notes': 'Upgrade the E02 placeholder to a researched design: dark complexion ("young and of darkish hue", Virata §11), crown, Gandiva. All poses face right.'},
   {'id': 'urvashi', 'status': 'new', 'poses': {'dancing': 'new', 'walking': 'new', 'standing-surprised': 'new', 'cursing-hand-raised': 'new'},
    'derive': 'kunti / madri rig', 'notes': 'Foremost apsara: celestial jewellery, a flowing veil, a soft glow, dignified court dress (no sexualisation). Faces right; flipped in scene. Expressions: smiling, hopeful, surprised, hurt, furious. Needs a HAND entry for light-burst-saffron.'},
   {'id': 'indra', 'status': 'new', 'poses': {'standing-blessing': 'new'}, 'derive': 'king / pandu rig + gold halo',
    'notes': 'King of the gods: tall crown, gold halo, vajra at the hip. Faces right. Expressions: proud, smiling.'},
   {'id': 'chitrasena', 'status': 'new', 'poses': {'playing-veena': 'new'}, 'derive': 'pandu rig', 'notes': 'Gandharva king: lighter, airy colours, a veena. Faces right.'},
   {'id': 'brihannala', 'status': 'new', 'poses': {'standing-graceful': 'new', 'dance-teaching': 'new', 'reaching-up': 'new', 'drawing-gandiva': 'new', 'gandiva-raised': 'new'},
    'derive': 'arjuna rig', 'notes': 'Arjuna in disguise (Virata §2, §11): long braid, large earrings, gold conch bangles, a woman’s dress, same face and build as Arjuna. Dignified and strong, never comic. Faces right.'},
   {'id': 'uttara', 'status': 'new', 'poses': {'dancing': 'new'}, 'derive': 'madri rig, younger', 'notes': 'Princess of Matsya, a young girl. Faces right.'},
   {'id': 'king', 'status': 'library', 'poses': {'seated-throne-pointing': 'library'}, 'notes': 'stands in for King Virata'}],
  'backgrounds': [
   {'id': 'amaravati-court', 'status': 'library'}, {'id': 'king-court', 'status': 'library', 'notes': 'Virata’s court; measure the floor ground line'},
   {'id': 'forest-hunt', 'status': 'library'}, {'id': 'red-sky-plain', 'status': 'library'}, {'id': 'parchment-card', 'status': 'library'}],
  'props': [
   {'id': 'vajra-flash', 'status': 'library'}, {'id': 'apsara-silhouette', 'status': 'library'}, {'id': 'battle-silhouettes', 'status': 'library'},
   {'id': 'celestial-chariot', 'status': 'new', 'notes': 'Indra’s golden chariot on curl-clouds (Matali drives it)'},
   {'id': 'astra-ring', 'status': 'new', 'notes': 'a ring of glowing weapon glyphs (bow, discus, trident, noose…)'},
   {'id': 'family-vine', 'status': 'new', 'notes': 'folk-art family vine: royal couple at top, medallions down to a bow-and-crown medallion'},
   {'id': 'year-ring', 'status': 'new', 'notes': '13 arc segments, the last one lit'},
   {'id': 'bangles-scarred-arm', 'status': 'new', 'notes': 'close-up forearm with bowstring scars and gold conch bangles'},
   {'id': 'shami-tree', 'status': 'new', 'notes': 'the shami tree at the cremation ground, a wrapped bundle in its branches'},
   {'id': 'gandiva', 'status': 'new', 'notes': 'Arjuna’s great bow, gold-banded; reuse for the rest of the series'},
   {'id': 'gandiva-shockwave', 'status': 'new', 'notes': 'a gold sound-ring rolling outward'},
   {'id': 'bhishma-silhouette', 'status': 'new', 'notes': 'E04 tease; white beard, bow, armour'},
   {'id': 'amba-shadow', 'status': 'new', 'notes': 'E04 tease; a tall woman’s shadow, hair loose'}],
  'overlays': [{'id': 'folk-art-border', 'status': 'library'}, {'id': 'sepia-folk-frame', 'status': 'library'}, {'id': 'shaap-stamp', 'status': 'library'}]}
}

# validate
errs = []
for s in scenes:
    for c in s.get('cues', []) + [x for x in s.get('sfx', []) if isinstance(x, dict) and 'onWord' in x]:
        for l in ('en', 'hi'):
            if c['onWord'][l] not in s['narration'][l]: errs.append((s['id'], l, c['onWord'][l]))
    for c in s.get('cues', []):
        if c['do'] == 'hard-cut-to':
            t = next((x for x in scenes if x['id'] == c['target']), None)
            if not t or t['beat'] != s['beat'] or t['narration'] != E: errs.append((s['id'], 'bad insert', c['target']))
    for el in s.get('characters', []) + s.get('props', []):
        if el['x'] > 0.88: errs.append((s['id'], 'x>0.88', el['id']))
print('errors:', errs)
open(f'{ep}/03-scenes.json', 'w').write(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
print('scenes', len(scenes))
