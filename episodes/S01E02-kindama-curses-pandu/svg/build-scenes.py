import json, re, sys
root = sys.argv[1]
ep = f'{root}/episodes/S01E02-kindama-curses-pandu'
src = open(f'{ep}/02-script.md').read()

def beats(section):
    out = {}
    for line in section.split('\n'):
        m = re.match(r'^\| (\d+)[^|]*\| (.*?) \|', line)
        if m: out[int(m.group(1))] = m.group(2).strip()
    return out
EN = beats(src.split('## English')[1].split('**Word count')[0])
HI = beats(src.split('## हिंदी')[1].split('**Word count')[0])
assert len(EN) == 13 and len(HI) == 13, (len(EN), len(HI))
N = lambda b: {'en': EN[b], 'hi': HI[b]}
E = {'en': '', 'hi': ''}
W = lambda en, hi: {'en': en, 'hi': hi}
def C(id, pose, x, y, scale, flip=False, action='breathe', **kw):
    d = {'id': id, 'pose': pose, 'x': x, 'y': y, 'scale': scale, 'flip': flip, 'action': action}; d.update(kw); return d
def P(id, x, y, scale, action='idle'):
    return {'id': id, 'x': x, 'y': y, 'scale': scale, 'action': action}

e01 = json.load(open(f'{root}/episodes/S01E01-mandavya-curses-yama/03-scenes.json'))
sting = next(s for s in e01['scenes'] if s['id'] == 's00')

scenes = [sting,
 {'id': 's01', 'beat': 1, 'type': 'character', 'background': 'forest-hunt', 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'fog', 'color': '#9FB3D9'}, {'type': 'dust', 'n': 20}],
  'characters': [C('pandu', 'standing-shocked', 0.24, 0.86, 1.0, action='still', expression='shocked')],
  'props': [P('stag-wounded', 0.64, 0.74, 1.15, 'still')],
  'camera': {'move': 'push-in-fast', 'from': 1.0, 'to': 1.15, 'focus': [0.5, 0.66]},
  'narration': N(1), 'onScreenText': None,
  'cues': [{'onWord': W('voice', 'आवाज़'), 'do': 'pierce', 'target': 'stag-wounded'}],
  'sfx': [{'id': 'heartbeat', 'at': 0, 'volume': 0.5}, {'id': 'drum-boom-deep', 'onWord': W('human', 'इंसान'), 'volume': 0.9}],
  'transition': 'cut', 'notes': 'Hook. The wounded stag cries out with a human voice; Pandu freezes, bow lowered. New prop stag-wounded: the library deer lying on its side, one small golden arrow, eyes open. Keep the arrow small, no blood.'},
 {'id': 's02', 'beat': 2, 'type': 'character', 'background': 'forest-hunt', 'backgroundVariant': 'dawn', 'light': 'dawn',
  'fx': [{'type': 'rays', 'x': 0.8, 'y': 0.2, 'color': '#FFE6B0'}, {'type': 'dust', 'n': 20}],
  'characters': [C('pandu', 'drawing-bow', 0.3, 0.86, 0.95, action='draw-bow')],
  'props': [P('deer', 0.62, 0.8, 0.6, 'graze'), P('deer', 0.8, 0.82, 0.5, 'graze'), P('glowing-arrow', 0.52, 0.62, 0.5, 'idle')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.7]},
  'narration': N(2), 'onScreenText': None,
  'cues': [{'onWord': W('shot', 'बाण'), 'do': 'pierce', 'target': 'glowing-arrow'}],
  'sfx': [{'id': 'bowstring-creak', 'at': 0.2, 'volume': 0.6}, {'id': 'arrow-whoosh-magic', 'onWord': W('shot', 'बाण'), 'volume': 0.8}],
  'transition': 'cut', 'notes': 'Flashback a moment: the shot. Two library deer side by side in the grass (stag and mate, NOT a mating pose). Five golden arrows = the arrow prop on the cue.'},
 {'id': 's03', 'beat': 3, 'type': 'character', 'background': 'forest-hunt', 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'glow', 'x': 0.6, 'y': 0.8, 'r': 0.35, 'color': '#E8B53A', 'pulse': True}, {'type': 'sparks', 'n': 18}],
  'characters': [C('kindama', 'lying-wounded', 0.58, 0.9, 1.05, flip=True, action='still', expression='pained')],
  'props': [],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.1, 'focus': [0.58, 0.78]},
  'narration': N(3), 'onScreenText': {'en': 'Rishi Kindama', 'hi': 'ऋषि किन्दम', 'style': 'name-tag', 'sub': {'en': 'a sage in a deer’s form', 'hi': 'हिरण के रूप में ऋषि'}},
  'cues': [], 'sfx': [{'id': 'shimmer-descend', 'onWord': W('sage', 'ऋषि'), 'volume': 0.6}],
  'transition': 'light-wipe', 'notes': 'Reveal: the stag becomes the sage (light-wipe in from s02). Kindama is derived from the Mandavya rig (different face/beard/colours), lying wounded, head toward the left where Pandu stands.'},
 {'id': 's04', 'beat': 4, 'type': 'character', 'background': 'forest-hunt', 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 15}],
  'characters': [C('pandu', 'standing-shocked', 0.27, 0.86, 1.0, expression='shocked'),
                 C('kindama', 'lying-wounded', 0.66, 0.9, 1.0, flip=True, action='still', expression='pained', speaking=True)],
  'props': [], 'camera': {'move': 'slow-pan-right', 'from': 0.0, 'to': 0.03},
  'narration': N(4), 'onScreenText': None, 'cues': [], 'sfx': [],
  'transition': 'cut', 'notes': 'Two-shot. Pandu (faces right) looks down at Kindama (flipped, faces left). Kindama speaks.'},
 {'id': 's05', 'beat': 5, 'type': 'character', 'background': 'forest-hunt', 'backgroundVariant': 'night', 'light': 'night',
  'fx': [{'type': 'glow', 'x': 0.62, 'y': 0.68, 'r': 0.3, 'color': '#E07A2E', 'pulse': True}],
  'characters': [C('pandu', 'standing-shocked', 0.25, 0.86, 1.0, expression='terrified'),
                 C('kindama', 'cursing-from-ground', 0.64, 0.9, 1.05, flip=True, action='raise-hand', expression='furious', speaking=True)],
  'props': [P('shaap-stamp', 0.5, 0.3, 0.7, 'stamp-in')],
  'camera': {'move': 'shake-then-zoom', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.6]},
  'narration': N(5), 'onScreenText': None,
  'cues': [{'onWord': W('die', 'मरोगे'), 'do': 'light-burst-saffron', 'target': 'kindama'},
           {'onWord': W('die', 'मरोगे'), 'do': 'stamp-next', 'target': 'shaap-stamp'}],
  'sfx': [{'id': 'thunder-crack', 'onWord': W('die', 'मरोगे'), 'volume': 0.6}, {'id': 'stamp-thud', 'onWord': W('die', 'मरोगे'), 'offset': 0.1, 'volume': 0.8}],
  'music': 1.1, 'transition': 'flash-white', 'notes': 'The curse. Saffron burst from Kindama’s raised hand; the shaap stamp lands on "die / मरोगे". Kindama then dies (not shown).'},
 {'id': 's06', 'beat': 6, 'type': 'character', 'background': 'forest-hunt', 'backgroundVariant': 'dawn', 'light': 'dawn',
  'fx': [{'type': 'dust', 'n': 15}],
  'characters': [C('kunti', 'standing-sad', 0.2, 0.86, 0.92, expression='sad'),
                 C('pandu', 'removing-crown', 0.5, 0.86, 1.0, expression='sad'),
                 C('madri', 'standing-sad', 0.79, 0.86, 0.92, flip=True, expression='sad')],
  'props': [], 'camera': {'move': 'slow-zoom-out', 'from': 1.08, 'to': 1.0, 'focus': [0.5, 0.5]},
  'narration': N(6), 'onScreenText': None,
  'cues': [{'onWord': W('mountains', 'पहाड़ों'), 'do': 'hard-cut-to', 'target': 's06b'}],
  'sfx': [{'id': 'gong-soft', 'at': 0.3, 'volume': 0.5}],
  'transition': 'cut', 'notes': 'Pandu takes off his crown between his two wives (both face him).'},
 {'id': 's06b', 'beat': 6, 'type': 'character', 'background': 'himalaya-peaks', 'light': 'dawn',
  'fx': [{'type': 'fog', 'color': '#DCE6F5'}],
  'characters': [], 'props': [P('three-pilgrims-silhouette', 0.5, 0.8, 0.8, 'walk-left')],
  'camera': {'move': 'crane-up', 'from': 0.0, 'to': -0.06},
  'narration': E, 'onScreenText': None, 'cues': [], 'sfx': [{'id': 'wind-desolate', 'at': 0, 'volume': 0.35}],
  'transition': 'dissolve', 'notes': 'Insert: three small figures walk into snowy peaks toward Shatashringa.'},
 {'id': 's07', 'beat': 7, 'type': 'character', 'background': 'hermitage', 'backgroundVariant': 'dawn', 'light': 'dawn',
  'fx': [{'type': 'glow', 'x': 0.5, 'y': 0.45, 'r': 0.35, 'color': '#E8B53A', 'pulse': True}, {'type': 'sparks', 'n': 14}],
  'characters': [C('kunti', 'folded-hands', 0.5, 0.79, 1.0, expression='hopeful')],
  'props': [P('mantra-ring', 0.5, 0.42, 0.9, 'circle')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.5]},
  'narration': N(7), 'onScreenText': None,
  'cues': [{'onWord': W('mantra', 'मंत्र'), 'do': 'glint', 'target': 'mantra-ring'}],
  'sfx': [{'id': 'temple-bells', 'onWord': W('mantra', 'मंत्र'), 'volume': 0.6}],
  'transition': 'dissolve', 'notes': 'The hermitage stands in for the Shatashringa ashram. A ring of glowing Sanskrit-like script circles Kunti (no readable text needed).'},
 {'id': 's08', 'beat': 8, 'type': 'character', 'background': 'cosmic-court', 'light': 'divine',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.3, 'color': '#FFE6B0'}, {'type': 'stars', 'n': 30}],
  'characters': [C('dharma', 'seated-throne', 0.5, 0.471, 0.736, action='still', expression='calm'),
                 C('kunti', 'holding-baby', 0.3, 0.99, 1.15, expression='joyful')],
  'props': [P('falling-light', 0.5, 0.25, 1.0, 'descend')],
  'camera': {'move': 'tilt-down', 'from': -0.1, 'to': 0.0},
  'narration': N(8), 'onScreenText': {'en': 'Dharma', 'hi': 'धर्म', 'style': 'name-tag', 'sub': {'en': 'the god cursed in Episode 1', 'hi': 'पहली कड़ी में शापित देवता'}},
  'cues': [], 'sfx': [{'id': 'shimmer-descend', 'onWord': W('Yudhishthira', 'युधिष्ठिर'), 'volume': 0.6}],
  'transition': 'light-wipe', 'notes': 'E01 callback: the same Dharma on his throne (library rig, halo intact here). Kunti in the foreground, over the shoulder, holding baby Yudhishthira; facing right toward the throne.'},
 {'id': 's09', 'beat': 9, 'type': 'character', 'background': 'hermitage', 'backgroundVariant': 'dawn', 'light': 'dawn',
  'fx': [{'type': 'dust', 'n': 20}],
  'characters': [C('kunti', 'holding-baby', 0.3, 0.79, 0.95, expression='joyful'),
                 C('madri', 'holding-twins', 0.7, 0.79, 0.95, flip=True, expression='joyful')],
  'props': [P('wind-swirl', 0.25, 0.3, 0.6, 'stamp-in'), P('vajra-flash', 0.5, 0.24, 0.6, 'stamp-in'), P('twin-stars', 0.74, 0.3, 0.6, 'stamp-in')],
  'camera': {'move': 'slow-zoom-out', 'from': 1.06, 'to': 1.0},
  'narration': N(9), 'onScreenText': None,
  'cues': [{'onWord': W('Vayu', 'वायु'), 'do': 'stamp-in', 'target': 'wind-swirl'},
           {'onWord': W('Indra', 'इन्द्र'), 'do': 'stamp-in', 'target': 'vajra-flash'},
           {'onWord': W('Ashvin', 'अश्विनीकुमारों'), 'do': 'stamp-in', 'target': 'twin-stars'}],
  'sfx': [{'id': 'gong-soft', 'onWord': W('Vayu', 'वायु'), 'volume': 0.5}, {'id': 'thunder-crack', 'onWord': W('Indra', 'इन्द्र'), 'volume': 0.35},
          {'id': 'shimmer-descend', 'onWord': W('Ashvin', 'अश्विनीकुमारों'), 'volume': 0.5}],
  'transition': 'cut', 'notes': 'Gods as symbols only (no new god rigs): wind swirl (Vayu), vajra flash (Indra), twin stars (Ashvins), each landing on its name.'},
 {'id': 's10', 'beat': 10, 'type': 'character', 'background': 'spring-forest', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 35, 'color': '#F6C1D0'}, {'type': 'glow', 'x': 0.5, 'y': 0.4, 'r': 0.5, 'color': '#F2A7B8'}],
  'characters': [C('pandu', 'reaching', 0.2, 0.86, 1.0, expression='longing'),
                 C('madri', 'turning-away', 0.87, 0.86, 0.95, flip=False, expression='afraid')],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(10), 'onScreenText': None,
  'cues': [{'onWord': W('took', 'सच'), 'do': 'hard-cut-to', 'target': 's10b'}],
  'sfx': [{'id': 'heartbeat', 'at': 0.5, 'volume': 0.5}],
  'music': 0.7, 'transition': 'cut', 'notes': 'Spring blossoms. Pandu reaches toward Madri; she turns away with a hand raised to stop him (the text says she resisted). Keep a clear gap between their hands: they must never read as reaching for each other. Symbolic only, no embrace.'},
 {'id': 's10b', 'beat': 10, 'type': 'prop-hero', 'background': 'spring-forest', 'light': 'night',
  'fx': [{'type': 'dust', 'n': 25, 'color': '#F6C1D0'}],
  'characters': [], 'props': [P('fallen-crown', 0.5, 0.64, 1.05, 'still')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.12, 'focus': [0.5, 0.64]},
  'narration': E, 'onScreenText': None, 'cues': [], 'sfx': [{'id': 'drum-boom-deep', 'at': 0, 'volume': 0.8}],
  'music': 0.3, 'transition': 'fade-to-night', 'notes': 'Insert on "took / सच": a fallen crown in the grass, petals falling. Pandu’s death, shown only by this.'},
 {'id': 's11', 'beat': 11, 'type': 'character', 'background': 'red-sky-plain', 'backgroundVariant': 'dusk', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 30}, {'type': 'glow', 'x': 0.76, 'y': 0.62, 'r': 0.3, 'color': '#E07A2E', 'pulse': True}],
  'characters': [C('kunti', 'holding-back', 0.38, 0.82, 0.95, expression='grieving'),
                 C('madri', 'walking', 0.62, 0.82, 0.9, action='still', light='silhouette')],
  'props': [P('young-pandavas-group', 0.14, 0.74, 0.75), P('pyre-flames', 0.8, 0.66, 0.9, 'flicker-distant')],
  'camera': {'move': 'slow-pan-right', 'from': 0.0, 'to': 0.04},
  'narration': N(11), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'wind-desolate', 'at': 0, 'volume': 0.4}, {'id': 'gong-soft', 'onWord': W('fire', 'चिता'), 'volume': 0.5}],
  'music': 0.8, 'transition': 'dissolve', 'notes': 'Kunti holds the five boys back (group prop behind her). Madri, in silhouette, walks toward stylised folk-art flames. No body on the pyre.'},
 {'id': 's12', 'beat': 12, 'type': 'text-reveal', 'background': 'parchment-card', 'light': 'divine',
  'characters': [], 'props': [P('glowing-arrow', 0.5, 0.3, 0.6, 'glint'), P('five-sons-silhouette', 0.5, 0.62, 0.9, 'idle')],
  'overlay': 'folk-art-border', 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.05},
  'narration': N(12),
  'onScreenText': {'en': 'One arrow. Five sons of gods.', 'hi': 'एक बाण। पाँच देवपुत्र।', 'style': 'law-inscription', 'source': {'en': 'Mahabharata, Adi Parva', 'hi': 'महाभारत, आदि पर्व'}},
  'cues': [{'onWord': W('gods', 'देवपुत्र'), 'do': 'write-on'}],
  'sfx': [{'id': 'drum-hit', 'onWord': W('gods', 'देवपुत्र'), 'volume': 0.8}],
  'transition': 'border-wipe', 'notes': 'Payoff of the hook. The single golden arrow above five glowing figures in a row (the brothers grown).'},
 {'id': 's13', 'beat': 13, 'type': 'character', 'background': 'amaravati-court', 'light': 'divine',
  'fx': [{'type': 'stars', 'n': 30}, {'type': 'glow', 'x': 0.72, 'y': 0.4, 'r': 0.3, 'color': '#F2A7B8', 'pulse': True}],
  'characters': [C('arjuna', 'standing-bow', 0.3, 0.86, 0.95, expression='calm')],
  'props': [P('apsara-silhouette', 0.72, 0.62, 0.7), P('shaap-stamp', 0.5, 0.3, 0.7, 'stamp-in')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.1},
  'narration': N(13), 'onScreenText': {'en': 'CURSED III', 'hi': 'शाप III', 'style': 'stamp-gold'},
  'cues': [{'onWord': W('own', 'बाकी'), 'do': 'stamp-next', 'target': 'shaap-stamp'}],
  'sfx': [{'id': 'drum-hit', 'onWord': W('own', 'बाकी'), 'volume': 0.9}],
  'overlay': 'folk-art-border', 'transition': 'cut-to-black',
  'notes': 'Tease for S01E03 (Urvashi curses Arjuna). Grown Arjuna mid-distance in Indra’s court; an apsara silhouette. Both assets are needed for E03 anyway.'},
]

doc = {
 'id': 'S01E02', 'title': {'en': 'The Deer Who Cursed a King', 'hi': 'जब हिरण ने राजा को शाप दिया'},
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Mahabharata, Adi Parva (Sambhava Parva)', 'hi': 'महाभारत, आदि पर्व (सम्भव पर्व)'},
 'safeZone': {'bottom': 0.2, 'right': 0.12},
 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True},
 'sound': e01['sound'],
 'thumbnail': {'scene': 's05', 'at': 0.6, 'series': {'en': 'Shraap · Episode 2', 'hi': 'शाप · भाग 2'},
   'title': {'en': 'The Deer Who Cursed a King', 'hi': 'जब हिरण ने राजा को शाप दिया'},
   'titleLines': {'en': ['The Deer Who', 'Cursed a King'], 'hi': ['जब हिरण ने', 'राजा को शाप दिया']}},
 'scenes': scenes,
 'assets': {
  'characters': [
   {'id': 'pandu', 'status': 'library', 'poses': {'drawing-bow': 'library', 'standing-shocked': 'new', 'removing-crown': 'new', 'reaching': 'new'}},
   {'id': 'dharma', 'status': 'library', 'poses': {'seated-throne': 'library'}},
   {'id': 'kindama', 'status': 'new', 'poses': {'lying-wounded': 'new', 'cursing-from-ground': 'new'}, 'derive': 'mandavya'},
   {'id': 'kunti', 'status': 'new', 'poses': {'standing-sad': 'new', 'folded-hands': 'new', 'holding-baby': 'new', 'holding-back': 'new'}},
   {'id': 'madri', 'status': 'new', 'poses': {'standing-sad': 'new', 'holding-twins': 'new', 'turning-away': 'new', 'walking': 'new'}},
   {'id': 'arjuna', 'status': 'new', 'poses': {'standing-bow': 'new'}, 'notes': 'E03 lead; derive from pandu'}],
  'backgrounds': [
   {'id': 'forest-hunt', 'status': 'library'}, {'id': 'hermitage', 'status': 'library'}, {'id': 'cosmic-court', 'status': 'library'},
   {'id': 'red-sky-plain', 'status': 'library'}, {'id': 'parchment-card', 'status': 'library'},
   {'id': 'himalaya-peaks', 'status': 'new'}, {'id': 'spring-forest', 'status': 'new'}, {'id': 'amaravati-court', 'status': 'new', 'notes': 'Indra’s court, also needed for E03'}],
  'props': [
   {'id': 'deer', 'status': 'library'}, {'id': 'stag-wounded', 'status': 'new', 'notes': 'derive from the deer prop'}, {'id': 'glowing-arrow', 'status': 'library'}, {'id': 'falling-light', 'status': 'library'},
   {'id': 'mantra-ring', 'status': 'new'}, {'id': 'wind-swirl', 'status': 'new'}, {'id': 'vajra-flash', 'status': 'new'}, {'id': 'twin-stars', 'status': 'new'},
   {'id': 'three-pilgrims-silhouette', 'status': 'new'}, {'id': 'fallen-crown', 'status': 'new'}, {'id': 'pyre-flames', 'status': 'new'},
   {'id': 'young-pandavas-group', 'status': 'new'}, {'id': 'five-sons-silhouette', 'status': 'new'}, {'id': 'apsara-silhouette', 'status': 'new'}],
  'overlays': [{'id': 'folk-art-border', 'status': 'library'}, {'id': 'shaap-stamp', 'status': 'library'}]}
}

# validate
errs = []
for s in scenes:
    for c in s.get('cues', []) + [x for x in s.get('sfx', []) if isinstance(x, dict) and 'onWord' in x]:
        for l in ('en', 'hi'):
            if c['onWord'][l] not in s['narration'][l]: errs.append((s['id'], l, c['onWord'][l]))
    for el in s.get('characters', []) + s.get('props', []):
        if el['x'] > 0.88: errs.append((s['id'], 'x>0.88', el['id']))
print('errors:', errs)
open(f'{ep}/03-scenes.json', 'w').write(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
print('scenes', len(scenes))
