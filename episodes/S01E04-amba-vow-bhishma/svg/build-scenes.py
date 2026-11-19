"""S01E04 v2 scene spec: the short, single-thread telling (13 beats). Narration is parsed from 02-script.md (never retyped).
v1 (23 beats) is kept in review/build-scenes-v1.py. Every asset is already in the library (made for v1).
Run:  python3 episodes/S01E04-amba-vow-bhishma/svg/build-scenes.py <repo root>
"""
import json, re, sys
root = sys.argv[1]
ep = f'{root}/episodes/S01E04-amba-vow-bhishma'
src = open(f'{ep}/02-script.md').read()

def beats(section):
    out = {}
    for line in section.split('\n'):
        m = re.match(r'^\| (\d+)[^|]*\| (.*?) \|', line)
        if m: out[int(m.group(1))] = m.group(2).strip()
    return out
EN = beats(src.split('## English')[1].split('**Ready cuts')[0])
HI = beats(src.split('## हिंदी')[1].split('**Ready cuts')[0])
assert len(EN) == 13 and len(HI) == 13, (len(EN), len(HI))
N = lambda b: {'en': EN[b], 'hi': HI[b]}
E = {'en': '', 'hi': ''}
W = lambda en, hi: {'en': en, 'hi': hi}
def C(id, pose, x, y, scale, flip=False, action='breathe', **kw):
    d = {'id': id, 'pose': pose, 'x': x, 'y': y, 'scale': scale, 'flip': flip, 'action': action}; d.update(kw); return d
def P(id, x, y, scale, action='idle'):
    return {'id': id, 'x': x, 'y': y, 'scale': scale, 'action': action}
def tag(en, hi, sub_en=None, sub_hi=None):
    t = {'en': en, 'hi': hi, 'style': 'name-tag'}
    if sub_en: t['sub'] = {'en': sub_en, 'hi': sub_hi}
    return t
STAMP = {'en': 'CURSED', 'hi': 'शाप', 'style': 'stamp-gold'}

e03 = json.load(open(f'{root}/episodes/S01E03-urvashi-curses-arjuna/03-scenes.json'))
sting = next(s for s in e03['scenes'] if s['id'] == 's00')
sting = {**sting, 'onScreenText': {**sting['onScreenText'], 'en': 'CURSED IV', 'hi': 'शाप IV'}}

YB = 'yamuna-bank'        # feet 0.84
HP = 'hastinapura-palace' # courtyard feet 0.90
KC = 'king-court'         # bottom step 0.88
RP = 'red-sky-plain'      # feet 0.80–0.82

scenes = [sting,
 # 1 hook
 {'id': 's01', 'beat': 1, 'type': 'character', 'background': YB, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'glow', 'x': 0.68, 'y': 0.45, 'r': 0.32, 'color': '#9FD3E6', 'pulse': True}, {'type': 'sparks', 'n': 14}],
  'characters': [C('amba', 'tapas-standing', 0.3, 0.84, 1.0, action='still', expression='resolute'),
                 C('ganga', 'cursing', 0.7, 0.84, 1.05, flip=True, action='raise-hand', expression='stern')],
  'props': [P('shaap-stamp', 0.5, 0.28, 0.7, 'stamp-in')],
  'camera': {'move': 'push-in-fast', 'from': 1.0, 'to': 1.15, 'focus': [0.5, 0.55]},
  'narration': N(1), 'onScreenText': STAMP,
  'cues': [{'onWord': W('cursed', 'शाप'), 'do': 'stamp-next', 'target': 'shaap-stamp'}],
  'sfx': [{'id': 'heartbeat', 'at': 0, 'volume': 0.5}, {'id': 'thunder-crack', 'onWord': W('cursed', 'शाप'), 'volume': 0.6},
          {'id': 'stamp-thud', 'onWord': W('cursed', 'शाप'), 'offset': 0.1, 'volume': 0.8}],
  'transition': 'flash-white',
  'notes': 'Hook (flash-forward to s08b): Ganga, risen from the river, curses Amba, who stands in tapas, unbowed.'},
 # 2 the swayamvara: Bhishma carries her off
 {'id': 's02', 'beat': 2, 'type': 'character', 'background': KC, 'light': 'dawn',
  'fx': [{'type': 'dust', 'n': 15}],
  'characters': [C('bhishma', 'standing-bow', 0.26, 0.88, 0.95, action='step-forward', expression='stern'),
                 C('amba', 'standing-sad', 0.6, 0.88, 0.85, flip=True, expression='startled')],
  'props': [P('three-princesses', 0.76, 0.66, 0.75, 'still'), P('war-chariot', 0.14, 0.74, 0.7, 'still')],
  'camera': {'move': 'slow-pan-right', 'from': 0.0, 'to': 0.03},
  'narration': N(2), 'onScreenText': tag('Amba', 'अम्बा', 'princess of Kashi', 'काशी की राजकुमारी'),
  'cues': [], 'sfx': [{'id': 'drum-hit', 'onWord': W('Bhishma', 'भीष्म'), 'volume': 0.6}],
  'transition': 'cut', 'notes': 'Kashi swayamvara (king-court stands in): young Bhishma arrives with his chariot; Amba in front, her sisters as silhouettes. Adi §102.'},
 # 3 she loves Shalva; Bhishma lets her go
 {'id': 's03', 'beat': 3, 'type': 'character', 'background': HP, 'light': 'dawn',
  'fx': [{'type': 'dust', 'n': 12, 'color': '#FFE6B0'}],
  'characters': [C('amba', 'folded-hands', 0.3, 0.9, 0.95, expression='pleading'),
                 C('bhishma', 'releasing', 0.7, 0.9, 1.0, flip=True, expression='kind')],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(3), 'onScreenText': None,
  'cues': [], 'sfx': [{'id': 'temple-bells', 'onWord': W('go', 'जाने'), 'volume': 0.4}],
  'transition': 'cut', 'notes': 'Amba, palms joined, tells Bhishma her heart is Shalva\'s; he opens his hand: go. Adi §102.'},
 # 4 Shalva turns her away
 {'id': 's04', 'beat': 4, 'type': 'character', 'background': KC, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 10}],
  'characters': [C('amba', 'standing-sad', 0.26, 0.88, 0.9, expression='hurt'),
                 C('shalva', 'turning-away', 0.66, 0.88, 1.0, expression='cold', speaking=True)],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.05},
  'narration': N(4), 'onScreenText': tag('Shalva', 'शाल्व', 'king of Saubha', 'सौभ के राजा'), 'cues': [],
  'sfx': [{'id': 'heartbeat', 'onWord': W('won', 'जीत'), 'volume': 0.45}],
  'transition': 'cut', 'notes': 'Shalva turns his back on her. Udyoga §176.'},
 # 5 Bhishma's vow → nowhere to go
 {'id': 's05', 'beat': 5, 'type': 'character', 'background': HP, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.15, 'color': '#FFD1A0'}],
  'characters': [C('bhishma', 'vow-hand-raised', 0.5, 0.9, 1.0, action='still', expression='solemn')],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06, 'focus': [0.5, 0.45]},
  'narration': N(5), 'onScreenText': tag('Bhishma', 'भीष्म', 'sworn never to marry', 'आजीवन ब्रह्मचर्य की प्रतिज्ञा'),
  'cues': [{'onWord': W('Amba', 'अम्बा'), 'do': 'hard-cut-to', 'target': 's05b'}],
  'sfx': [{'id': 'gong-soft', 'at': 0.2, 'volume': 0.5}],
  'transition': 'cut', 'notes': 'Bhishma\'s vow, said once, where it matters (Udyoga §181); cut to Amba on her name.'},
 {'id': 's05b', 'beat': 5, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'fog', 'color': '#C9A2B0'}],
  'characters': [C('amba', 'standing-sad', 0.5, 0.82, 0.85, action='still', expression='sad')],
  'props': [P('closed-gate', 0.16, 0.6, 0.8, 'still'), P('closed-gate', 0.84, 0.6, 0.8, 'still')],
  'camera': {'move': 'slow-zoom-out', 'from': 1.08, 'to': 1.0},
  'narration': E, 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'wind-desolate', 'at': 0, 'volume': 0.4}],
  'music': 0.6, 'transition': 'cut', 'notes': 'Insert: Amba alone between two closed gates (her father\'s, Hastinapura\'s).'},
 # 6 her vow
 {'id': 's06', 'beat': 6, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 18}],
  'characters': [C('amba', 'resolute', 0.5, 0.82, 1.2, action='still', expression='resolute', speaking=True)],
  'props': [], 'camera': {'move': 'push-in-fast', 'from': 1.0, 'to': 1.12, 'focus': [0.5, 0.4]},
  'narration': N(6), 'onScreenText': tag('Her vow', 'अम्बा की प्रतिज्ञा'), 'cues': [],
  'sfx': [{'id': 'drum-boom-deep', 'onWord': W('kill', 'मारूँगी'), 'volume': 0.7}],
  'music': 1.1, 'transition': 'dissolve', 'notes': 'Same road, the light turns to fire: Amba, fist at her chest, makes her vow (Udyoga §189).'},
 # 7 twelve years of tapas
 {'id': 's07', 'beat': 7, 'type': 'character', 'background': YB, 'backgroundVariant': 'night', 'light': 'moon',
  'fx': [{'type': 'stars', 'n': 40}, {'type': 'fog', 'color': '#9FB3D9'}],
  'characters': [C('amba', 'tapas-standing', 0.5, 0.84, 0.95, action='still', expression='eyes-closed')],
  'props': [], 'camera': {'move': 'crane-up', 'from': 0.0, 'to': -0.05},
  'narration': N(7), 'onScreenText': tag('12 years', 'बारह बरस'),
  'cues': [], 'sfx': [{'id': 'wind-desolate', 'at': 0, 'volume': 0.35}],
  'music': 0.8, 'transition': 'dissolve', 'notes': 'Amba stands in the Yamuna, palms joined above her head, eyes closed.'},
 # 8 Ganga rises … and curses (the hook pays off)
 {'id': 's08', 'beat': 8, 'type': 'character', 'background': YB, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'glow', 'x': 0.7, 'y': 0.45, 'r': 0.32, 'color': '#9FD3E6', 'pulse': True}],
  'characters': [C('amba', 'tapas-standing', 0.3, 0.84, 0.95, action='still', expression='resolute'),
                 C('ganga', 'rising', 0.7, 0.84, 1.05, flip=True, action='ascend', expression='stern')],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(8), 'onScreenText': tag('Ganga', 'गंगा', 'Bhishma’s mother', 'भीष्म की माँ'),
  'cues': [{'onWord': W('cursed', 'शाप'), 'do': 'hard-cut-to', 'target': 's08b'}],
  'sfx': [{'id': 'shimmer-descend', 'onWord': W('Ganga', 'गंगा'), 'volume': 0.6}],
  'transition': 'cut', 'notes': 'Ganga rises from the water (Udyoga §189); cut to the curse on "cursed / शाप".'},
 {'id': 's08b', 'beat': 8, 'type': 'character', 'background': YB, 'backgroundVariant': 'night', 'light': 'night',
  'fx': [{'type': 'glow', 'x': 0.7, 'y': 0.45, 'r': 0.3, 'color': '#9FD3E6', 'pulse': True}, {'type': 'sparks', 'n': 12}],
  'characters': [C('amba', 'tapas-standing', 0.3, 0.84, 1.0, action='still', expression='resolute'),
                 C('ganga', 'cursing', 0.7, 0.84, 1.05, flip=True, action='raise-hand', expression='stern', speaking=True)],
  'props': [P('shaap-stamp', 0.5, 0.28, 0.7, 'stamp-in'), P('crooked-river', 0.5, 0.7, 1.2, 'stamp-in')],
  'camera': {'move': 'shake-then-zoom', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.55]},
  'narration': E, 'onScreenText': STAMP, 'cues': [],
  'sfx': [{'id': 'thunder-crack', 'at': 0, 'volume': 0.6}, {'id': 'stamp-thud', 'at': 0.15, 'volume': 0.8}],
  'music': 1.1, 'transition': 'flash-white', 'notes': 'Insert, the curse: the stamp lands and the dry, crooked riverbed glows at Amba\'s feet.'},
 # 9 Shiva's boon
 {'id': 's09', 'beat': 9, 'type': 'character', 'background': 'himalaya-peaks', 'light': 'divine',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.3, 'color': '#FFE6B0'}, {'type': 'stars', 'n': 25}],
  'characters': [C('amba', 'folded-hands', 0.5, 0.8, 0.75, action='still', expression='hopeful')],
  'props': [P('shiva-light', 0.5, 0.34, 1.0, 'stamp-in')],
  'camera': {'move': 'tilt-down', 'from': -0.1, 'to': 0.0},
  'narration': N(9), 'onScreenText': None,
  'cues': [{'onWord': W('Shiva', 'शिव'), 'do': 'stamp-in', 'target': 'shiva-light'}],
  'sfx': [{'id': 'temple-bells', 'onWord': W('Shiva', 'शिव'), 'volume': 0.6}],
  'transition': 'light-wipe', 'notes': 'Shiva as a symbol only (trident, crescent, a column of light). Udyoga §190.'},
 # 10 the fire → Shikhandi
 {'id': 's10', 'beat': 10, 'type': 'prop-hero', 'background': YB, 'backgroundVariant': 'night', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 30}],
  'characters': [], 'props': [P('pyre-flames', 0.5, 0.6, 1.0, 'flicker-distant'), P('rising-lights', 0.5, 0.36, 0.7, 'ascend')],
  'camera': {'move': 'crane-up', 'from': 0.0, 'to': -0.06},
  'narration': N(10), 'onScreenText': None,
  'cues': [{'onWord': W('reborn', 'शिखण्डी'), 'do': 'hard-cut-to', 'target': 's10b'}],
  'sfx': [{'id': 'gong-soft', 'at': 0.3, 'volume': 0.5}],
  'transition': 'cut', 'notes': 'Symbolic only: folk-art flames by the river, one spark rising. No figure in the fire.'},
 {'id': 's10b', 'beat': 10, 'type': 'character', 'background': HP, 'backgroundVariant': 'dawn', 'light': 'dawn',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.15, 'color': '#FFE6B0'}],
  'characters': [C('shikhandi', 'standing-bow', 0.5, 0.9, 1.0, action='step-forward', expression='resolute')],
  'props': [P('falling-light', 0.5, 0.25, 1.0, 'descend')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': E, 'onScreenText': tag('Shikhandi', 'शिखण्डी', 'born to King Drupada', 'राजा द्रुपद की सन्तान'),
  'cues': [], 'sfx': [{'id': 'shimmer-descend', 'at': 0.1, 'volume': 0.6}],
  'transition': 'cut', 'notes': 'Insert: the spark comes down; Shikhandi as a young warrior of Panchala (Udyoga §191–195).'},
 # 11 Kurukshetra: Arjuna behind Shikhandi
 {'id': 's11', 'beat': 11, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 25}, {'type': 'dust', 'n': 15}],
  'characters': [C('arjuna', 'drawing-bow', 0.2, 0.8, 0.9, action='draw-bow', expression='fierce'),
                 C('shikhandi', 'drawing-bow', 0.4, 0.82, 0.95, action='still', expression='fierce'),
                 C('bhishma', 'bow-still', 0.76, 0.82, 1.0, flip=True, action='still', expression='calm')],
  'props': [P('battle-silhouettes', 0.6, 0.62, 0.9, 'still')],
  'camera': {'move': 'slow-pan-right', 'from': 0.0, 'to': 0.03},
  'narration': N(11), 'onScreenText': tag('Kurukshetra', 'कुरुक्षेत्र', 'day ten', 'दसवाँ दिन'), 'cues': [],
  'sfx': [{'id': 'battle-distant', 'at': 0, 'volume': 0.35}, {'id': 'arrow-whoosh-magic', 'onWord': W('Arjuna', 'अर्जुन'), 'volume': 0.7}],
  'transition': 'cut', 'notes': 'Old Bhishma holds his bow still before Shikhandi (§118); Arjuna shoots from behind Shikhandi (§120).'},
 # 12 the bed of arrows
 {'id': 's12', 'beat': 12, 'type': 'prop-hero', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 15}, {'type': 'rays', 'x': 0.5, 'y': 0.35, 'color': '#FFD1A0'}],
  'characters': [], 'props': [P('bed-of-arrows', 0.5, 0.5, 1.6, 'still')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.6]},
  'narration': N(12), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'drum-boom-deep', 'at': 0.3, 'volume': 0.8}],
  'music': 0.7, 'transition': 'dissolve', 'notes': 'Bhishma on a bed of arrow shafts, held above the ground (§121). No wounds.'},
 # 13 one vow → tease E05
 {'id': 's13', 'beat': 13, 'type': 'prop-hero', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'embers', 'n': 15}],
  'characters': [], 'props': [P('bed-of-arrows', 0.5, 0.62, 1.0, 'still'), P('amba-shadow', 0.5, 0.36, 1.0, 'ascend')],
  'camera': {'move': 'crane-up', 'from': 0.0, 'to': -0.05},
  'narration': N(13), 'onScreenText': None,
  'cues': [{'onWord': W('Next', 'अगली'), 'do': 'hard-cut-to', 'target': 's13b'}],
  'sfx': [{'id': 'wind-desolate', 'at': 0, 'volume': 0.4}],
  'transition': 'cut', 'notes': 'Amba\'s shadow rises over the fallen Bhishma; cut to the tease on "Next / अगली".'},
 {'id': 's13b', 'beat': 13, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'silhouette',
  'fx': [{'type': 'embers', 'n': 20}, {'type': 'glow', 'x': 0.5, 'y': 0.45, 'r': 0.3, 'color': '#E8B53A', 'pulse': True}],
  'characters': [],
  'props': [P('karna-silhouette', 0.5, 0.6, 1.0, 'still'), P('shaap-stamp', 0.5, 0.28, 0.7, 'stamp-in')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.1},
  'narration': E, 'onScreenText': {'en': 'CURSED V', 'hi': 'शाप V', 'style': 'stamp-gold'}, 'cues': [],
  'sfx': [{'id': 'drum-hit', 'at': 0.15, 'volume': 0.9}],
  'overlay': 'folk-art-border', 'transition': 'cut-to-black',
  'notes': 'Insert, tease for S01E05 (Karna\'s curses): Karna in silhouette, golden armour glint.'},
]

lib = lambda ids: [{'id': i, 'status': 'library'} for i in ids]
doc = {
 'id': 'S01E04', 'title': {'en': 'The Woman Who Vowed to Kill Bhishma', 'hi': 'भीष्म-वध की प्रतिज्ञा'},
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Mahabharata, Udyoga & Bhishma Parva', 'hi': 'महाभारत, उद्योग और भीष्म पर्व'},
 'safeZone': {'bottom': 0.2, 'right': 0.12},
 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True},
 'sound': e03['sound'],
 'thumbnail': {'scene': 's08b', 'at': 0.5, 'series': {'en': 'Shraap · Episode 4', 'hi': 'शाप · भाग 4'},
   'title': {'en': 'The Woman Who Vowed to Kill Bhishma', 'hi': 'भीष्म-वध की प्रतिज्ञा'},
   'titleLines': {'en': ['She Vowed', 'to Kill', 'Bhishma'], 'hi': ['भीष्म-वध की', 'प्रतिज्ञा']}},
 'scenes': scenes,
 'assets': {
  'characters': [
   {'id': 'bhishma', 'status': 'library', 'poses': {p: 'library' for p in ('standing-bow', 'releasing', 'vow-hand-raised', 'bow-still')}},
   {'id': 'amba', 'status': 'library', 'poses': {p: 'library' for p in ('tapas-standing', 'standing-sad', 'folded-hands', 'resolute')}},
   {'id': 'ganga', 'status': 'library', 'poses': {'rising': 'library', 'cursing': 'library'}},
   {'id': 'shalva', 'status': 'library', 'poses': {'turning-away': 'library'}},
   {'id': 'shikhandi', 'status': 'library', 'poses': {'standing-bow': 'library', 'drawing-bow': 'library'}},
   {'id': 'arjuna', 'status': 'library', 'poses': {'drawing-bow': 'library'}}],
  'backgrounds': lib([YB, HP, KC, RP, 'himalaya-peaks']),
  'props': lib(['three-princesses', 'war-chariot', 'closed-gate', 'crooked-river', 'shiva-light', 'pyre-flames', 'rising-lights',
                'falling-light', 'battle-silhouettes', 'bed-of-arrows', 'amba-shadow', 'karna-silhouette']),
  'overlays': lib(['folk-art-border', 'shaap-stamp'])}
}

errs = []
ids = {s['id'] for s in scenes}
for s in scenes:
    for c in s.get('cues', []) + [x for x in s.get('sfx', []) if isinstance(x, dict) and 'onWord' in x]:
        for l in ('en', 'hi'):
            words = [re.sub(r'[^\wऀ-ॣ०-ॿ-]', '', w) for w in s['narration'][l].split()]
            if c['onWord'][l] not in words: errs.append((s['id'], l, c['onWord'][l]))
        if c.get('do') == 'hard-cut-to' and c['target'] not in ids: errs.append((s['id'], 'no insert', c['target']))
    for el in s.get('characters', []) + s.get('props', []):
        if el['x'] > 0.88: errs.append((s['id'], 'x>0.88', el['id']))
print('errors:', errs)
open(f'{ep}/03-scenes.json', 'w').write(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
print('scenes', len(scenes))
