"""S01E04 scene spec. Narration is parsed from 02-script.md (never retyped).
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
EN = beats(src.split('## English')[1].split('**Word count')[0])
HI = beats(src.split('## हिंदी')[1].split('**Ready cuts')[0])
assert len(EN) == 23 and len(HI) == 23, (len(EN), len(HI))
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

YB = 'yamuna-bank'        # NEW background: river bank; feet expected ≈ 0.84 (measure at render)
HP = 'hastinapura-palace' # courtyard feet ≈ 0.90
KC = 'king-court'         # standing on the bottom step ≈ 0.88
RP = 'red-sky-plain'      # feet ≈ 0.80–0.82
HM = 'hermitage'          # feet ≈ 0.76–0.80

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
  'notes': 'Hook (flash-forward to s13): Ganga, rising from the river, curses Amba, who stands in tapas, unbowed.'},
 # 2 Bhishma's vow
 {'id': 's02', 'beat': 2, 'type': 'character', 'background': HP, 'backgroundVariant': 'dawn', 'light': 'dawn',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.15, 'color': '#FFE6B0'}],
  'characters': [C('bhishma', 'vow-hand-raised', 0.5, 0.9, 1.0, action='still', expression='solemn')],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.45]},
  'narration': N(2), 'onScreenText': tag('Bhishma', 'भीष्म', 'his vow: never to marry, never to rule', 'प्रतिज्ञा: न विवाह, न राज'),
  'cues': [], 'sfx': [{'id': 'gong-soft', 'onWord': W('vow', 'प्रतिज्ञा'), 'volume': 0.6}],
  'transition': 'dissolve', 'notes': 'Young Bhishma (Devavrata), right hand raised in an oath. Adi §100.'},
 # 3 the swayamvara
 {'id': 's03', 'beat': 3, 'type': 'character', 'background': KC, 'light': 'dawn',
  'fx': [{'type': 'dust', 'n': 15}],
  'characters': [C('bhishma', 'standing-bow', 0.26, 0.88, 0.95, action='step-forward', expression='stern'),
                 C('amba', 'standing-sad', 0.6, 0.88, 0.85, flip=True, expression='startled')],
  'props': [P('three-princesses', 0.76, 0.66, 0.75, 'still'), P('war-chariot', 0.14, 0.74, 0.7, 'still')],
  'camera': {'move': 'slow-pan-right', 'from': 0.0, 'to': 0.03},
  'narration': N(3), 'onScreenText': tag('Kashi', 'काशी', 'the swayamvara of three princesses', 'तीन राजकुमारियों का स्वयंवर'),
  'cues': [], 'sfx': [{'id': 'drum-hit', 'onWord': W('chariot', 'रथ'), 'volume': 0.6}],
  'transition': 'cut', 'notes': 'Kashi swayamvara (king-court stands in): Bhishma arrives alone; the three princesses (Amba lit in front, her sisters as silhouettes). Adi §102.'},
 # 4 the kings, and Shalva
 {'id': 's04', 'beat': 4, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'fire',
  'fx': [{'type': 'dust', 'n': 25}],
  'characters': [C('bhishma', 'drawing-bow', 0.24, 0.82, 1.0, action='draw-bow', expression='fierce'),
                 C('shalva', 'defeated', 0.56, 0.82, 0.95, flip=True, expression='hurt'),
                 C('amba', 'standing-sad', 0.82, 0.82, 0.8, flip=True, expression='sad')],
  'props': [P('battle-silhouettes', 0.6, 0.62, 0.9, 'still')],
  'camera': {'move': 'shake-small-then-static'},
  'narration': N(4), 'onScreenText': tag('Shalva', 'शाल्व', 'king of Saubha', 'सौभ के राजा'),
  'cues': [], 'sfx': [{'id': 'arrow-whoosh-magic', 'at': 0.3, 'volume': 0.6}, {'id': 'battle-distant', 'at': 0, 'volume': 0.35}],
  'transition': 'cut', 'notes': 'Bhishma fights off the kings; Shalva falls back; Amba looks at Shalva.'},
 # 5 "My heart belongs to Shalva"
 {'id': 's05', 'beat': 5, 'type': 'character', 'background': HP, 'light': 'dawn',
  'fx': [{'type': 'dust', 'n': 12, 'color': '#FFE6B0'}],
  'characters': [C('amba', 'folded-hands', 0.3, 0.9, 0.95, expression='pleading', speaking=True),
                 C('bhishma', 'releasing', 0.7, 0.9, 1.0, flip=True, expression='kind')],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(5), 'onScreenText': tag('Amba', 'अम्बा', 'eldest princess of Kashi', 'काशी की बड़ी राजकुमारी'),
  'cues': [], 'sfx': [{'id': 'temple-bells', 'onWord': W('go', 'जाने'), 'volume': 0.4}],
  'transition': 'cut', 'notes': 'Amba tells Bhishma her heart is Shalva\'s; he opens his hand: go. Adi §102.'},
 # 6 Shalva turns her away
 {'id': 's06', 'beat': 6, 'type': 'character', 'background': KC, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 10}],
  'characters': [C('amba', 'standing-sad', 0.26, 0.88, 0.9, expression='hurt'),
                 C('shalva', 'turning-away', 0.66, 0.88, 1.0, expression='cold', speaking=True)],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.05},
  'narration': N(6), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'heartbeat', 'onWord': W('Go', 'जाओ'), 'volume': 0.45}],
  'transition': 'cut', 'notes': 'Shalva turns his back on her (faces right, away), a hand raised: "go". Udyoga §176.'},
 # 7 nowhere to go
 {'id': 's07', 'beat': 7, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'fog', 'color': '#C9A2B0'}],
  'characters': [C('amba', 'standing-sad', 0.5, 0.82, 0.85, action='still', expression='sad')],
  'props': [P('closed-gate', 0.16, 0.6, 0.8, 'still'), P('closed-gate', 0.84, 0.6, 0.8, 'still')],
  'camera': {'move': 'slow-zoom-out', 'from': 1.08, 'to': 1.0},
  'narration': N(7), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'wind-desolate', 'at': 0, 'volume': 0.4}],
  'music': 0.6, 'transition': 'dissolve', 'notes': 'Amba alone on a road between two closed palace gates (her father\'s, Hastinapura\'s).'},
 # 8 Parashurama
 {'id': 's08', 'beat': 8, 'type': 'character', 'background': HM, 'light': 'dawn',
  'fx': [{'type': 'rays', 'x': 0.7, 'y': 0.2, 'color': '#FFE6B0'}],
  'characters': [C('amba', 'folded-hands', 0.3, 0.79, 0.9, expression='pleading'),
                 C('parashurama', 'standing-axe', 0.68, 0.79, 1.0, flip=True, expression='stern')],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(8), 'onScreenText': tag('Parashurama', 'परशुराम', 'Bhishma’s own teacher', 'भीष्म के गुरु'),
  'cues': [], 'sfx': [{'id': 'gong-soft', 'onWord': W('Parashurama', 'परशुराम'), 'volume': 0.5}],
  'transition': 'cut', 'notes': 'Udyoga §178–180.'},
 # 9 the 23-day duel
 {'id': 's09', 'beat': 9, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 25}, {'type': 'sparks', 'n': 15}],
  'characters': [C('bhishma', 'drawing-bow', 0.26, 0.82, 1.0, action='draw-bow', expression='fierce'),
                 C('parashurama', 'drawing-bow', 0.74, 0.82, 1.0, flip=True, action='draw-bow', expression='fierce')],
  'props': [P('gandiva-shockwave', 0.5, 0.5, 0.8, 'stamp-in')],
  'camera': {'move': 'shake-then-zoom', 'from': 1.0, 'to': 1.06, 'focus': [0.5, 0.5]},
  'narration': N(9), 'onScreenText': tag('23 days', '२३ दिन', 'Udyoga Parva §185', 'उद्योग पर्व §185'),
  'cues': [{'onWord': W('twenty-three', 'तेईस'), 'do': 'stamp-in', 'target': 'gandiva-shockwave'}],
  'sfx': [{'id': 'arrow-whoosh-magic', 'at': 0.2, 'volume': 0.7}, {'id': 'drum-boom-deep', 'onWord': W('conceded', 'हार'), 'volume': 0.7}],
  'music': 1.15, 'transition': 'cut', 'notes': 'Teacher and pupil face to face; arrows meet in a burst of light. Udyoga §182–188.'},
 # 10 "no refuge"
 {'id': 's10', 'beat': 10, 'type': 'character', 'background': HM, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 10}],
  'characters': [C('amba', 'resolute', 0.3, 0.79, 0.9, expression='resolute', speaking=True),
                 C('parashurama', 'standing-axe', 0.7, 0.79, 1.0, flip=True, expression='sad', speaking=True)],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.08, 'focus': [0.3, 0.5]},
  'narration': N(10), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'heartbeat', 'onWord': W('myself', 'ख़ुद'), 'volume': 0.5}],
  'transition': 'dissolve', 'notes': 'Udyoga §189. Amba, fist at her chest, eyes hard.'},
 # 11 twelve years of tapas
 {'id': 's11', 'beat': 11, 'type': 'character', 'background': YB, 'backgroundVariant': 'night', 'light': 'moon',
  'fx': [{'type': 'stars', 'n': 40}, {'type': 'fog', 'color': '#9FB3D9'}],
  'characters': [C('amba', 'tapas-standing', 0.5, 0.84, 0.95, action='still', expression='eyes-closed')],
  'props': [], 'camera': {'move': 'crane-up', 'from': 0.0, 'to': -0.05},
  'narration': N(11), 'onScreenText': tag('12 years of tapas', 'बारह बरस का तप', 'Udyoga Parva §189', 'उद्योग पर्व §189'),
  'cues': [], 'sfx': [{'id': 'wind-desolate', 'at': 0, 'volume': 0.35}],
  'music': 0.8, 'transition': 'dissolve', 'notes': 'Amba stands in the Yamuna, palms joined above her head, eyes closed.'},
 # 12 Ganga rises
 {'id': 's12', 'beat': 12, 'type': 'character', 'background': YB, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'glow', 'x': 0.7, 'y': 0.45, 'r': 0.32, 'color': '#9FD3E6', 'pulse': True}],
  'characters': [C('amba', 'tapas-standing', 0.3, 0.84, 0.95, action='still', expression='resolute'),
                 C('ganga', 'rising', 0.7, 0.84, 1.05, flip=True, action='ascend', expression='stern', speaking=True)],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(12), 'onScreenText': tag('Ganga', 'गंगा', 'Bhishma’s mother', 'भीष्म की माँ'),
  'cues': [], 'sfx': [{'id': 'shimmer-descend', 'onWord': W('Ganga', 'गंगा'), 'volume': 0.6}],
  'transition': 'cut', 'notes': 'Udyoga §189: Ganga questions her. Ganga crowned, with a small makara at her side.'},
 # 13 the curse
 {'id': 's13', 'beat': 13, 'type': 'character', 'background': YB, 'backgroundVariant': 'night', 'light': 'night',
  'fx': [{'type': 'glow', 'x': 0.7, 'y': 0.45, 'r': 0.3, 'color': '#9FD3E6', 'pulse': True}, {'type': 'sparks', 'n': 12}],
  'characters': [C('amba', 'tapas-standing', 0.3, 0.84, 1.0, action='still', expression='resolute'),
                 C('ganga', 'cursing', 0.7, 0.84, 1.05, flip=True, action='raise-hand', expression='stern', speaking=True)],
  'props': [P('shaap-stamp', 0.5, 0.28, 0.7, 'stamp-in'), P('crooked-river', 0.5, 0.7, 1.2, 'stamp-in')],
  'camera': {'move': 'shake-then-zoom', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.55]},
  'narration': N(13), 'onScreenText': STAMP,
  'cues': [{'onWord': W('crooked', 'टेढ़ी'), 'do': 'stamp-next', 'target': 'shaap-stamp'},
           {'onWord': W('half', 'आधा'), 'do': 'stamp-in', 'target': 'crooked-river'}],
  'sfx': [{'id': 'thunder-crack', 'onWord': W('crooked', 'टेढ़ी'), 'volume': 0.6}, {'id': 'stamp-thud', 'onWord': W('crooked', 'टेढ़ी'), 'offset': 0.1, 'volume': 0.8}],
  'music': 1.1, 'transition': 'flash-white', 'notes': 'The curse (the hook pays off): the stamp on "crooked / टेढ़ी"; on "half / आधा" a dry winding riverbed glows out from Amba\'s feet.'},
 # 14 Shiva's boon
 {'id': 's14', 'beat': 14, 'type': 'character', 'background': 'himalaya-peaks', 'light': 'divine',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.3, 'color': '#FFE6B0'}, {'type': 'stars', 'n': 25}],
  'characters': [C('amba', 'folded-hands', 0.5, 0.8, 0.75, action='still', expression='hopeful')],
  'props': [P('shiva-light', 0.5, 0.34, 1.0, 'stamp-in')],
  'camera': {'move': 'tilt-down', 'from': -0.1, 'to': 0.0},
  'narration': N(14), 'onScreenText': None,
  'cues': [{'onWord': W('Shiva', 'शिव'), 'do': 'stamp-in', 'target': 'shiva-light'}],
  'sfx': [{'id': 'temple-bells', 'onWord': W('Shiva', 'शिव'), 'volume': 0.6}],
  'transition': 'light-wipe', 'notes': 'Shiva as a symbol only (trident, crescent, a column of light), above Amba. Udyoga §190.'},
 # 15 the pyre (symbolic)
 {'id': 's15', 'beat': 15, 'type': 'prop-hero', 'background': YB, 'backgroundVariant': 'night', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 30}],
  'characters': [], 'props': [P('pyre-flames', 0.5, 0.6, 1.0, 'flicker-distant'), P('rising-lights', 0.5, 0.36, 0.7, 'ascend')],
  'camera': {'move': 'crane-up', 'from': 0.0, 'to': -0.06},
  'narration': N(15), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'gong-soft', 'at': 0.3, 'volume': 0.5}],
  'music': 0.5, 'transition': 'fade-to-night', 'notes': 'Symbolic only: folk-art flames by the river, one spark rising. No figure in the fire.'},
 # 16 reborn as Shikhandi
 {'id': 's16', 'beat': 16, 'type': 'character', 'background': HP, 'backgroundVariant': 'dawn', 'light': 'dawn',
  'fx': [{'type': 'rays', 'x': 0.5, 'y': 0.15, 'color': '#FFE6B0'}],
  'characters': [C('shikhandi', 'standing-bow', 0.5, 0.9, 1.0, action='step-forward', expression='resolute')],
  'props': [P('falling-light', 0.5, 0.25, 1.0, 'descend')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(16), 'onScreenText': tag('Shikhandi', 'शिखण्डी', 'born to King Drupada', 'राजा द्रुपद की सन्तान'),
  'cues': [], 'sfx': [{'id': 'shimmer-descend', 'at': 0.2, 'volume': 0.6}],
  'transition': 'cut', 'notes': 'The spark descends; Shikhandi as a young warrior of Panchala (Udyoga §191–195).'},
 # 17 Bhishma tells the Pandavas
 {'id': 's17', 'beat': 17, 'type': 'character', 'background': RP, 'backgroundVariant': 'night', 'light': 'night',
  'fx': [{'type': 'stars', 'n': 30}, {'type': 'glow', 'x': 0.5, 'y': 0.6, 'r': 0.3, 'color': '#E07A2E', 'pulse': True}],
  'characters': [C('arjuna', 'standing-bow', 0.28, 0.82, 0.95, expression='worried'),
                 C('bhishma', 'gesturing', 0.7, 0.82, 1.0, flip=True, expression='calm', speaking=True)],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(17), 'onScreenText': tag('Kurukshetra', 'कुरुक्षेत्र', 'the ninth night', 'नौवीं रात'),
  'cues': [], 'sfx': [{'id': 'night-crickets', 'at': 0, 'volume': 0.35}],
  'transition': 'cut', 'notes': 'Bhishma §108: by firelight, Bhishma himself tells Arjuna (and the Pandavas) how to bring him down.'},
 # 18 day ten: Shikhandi's arrows
 {'id': 's18', 'beat': 18, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 25}, {'type': 'dust', 'n': 20}],
  'characters': [C('shikhandi', 'drawing-bow', 0.28, 0.82, 1.0, action='draw-bow', expression='fierce'),
                 C('bhishma', 'bow-still', 0.72, 0.82, 1.0, flip=True, action='still', expression='calm')],
  'props': [P('battle-silhouettes', 0.6, 0.62, 0.9, 'still')],
  'camera': {'move': 'slow-pan-right', 'from': 0.0, 'to': 0.03},
  'narration': N(18), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'arrow-whoosh-magic', 'at': 0.2, 'volume': 0.7}],
  'transition': 'cut', 'notes': 'Bhishma §118: Shikhandi shoots; Bhishma holds his bow still and will not strike back.'},
 # 19 Arjuna's arrows
 {'id': 's19', 'beat': 19, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'fire',
  'fx': [{'type': 'embers', 'n': 25}],
  'characters': [C('arjuna', 'drawing-bow', 0.2, 0.8, 0.9, action='draw-bow', expression='fierce'),
                 C('shikhandi', 'drawing-bow', 0.4, 0.82, 0.95, action='still', expression='fierce'),
                 C('bhishma', 'bow-still', 0.76, 0.82, 1.0, flip=True, action='still', expression='smiling', speaking=True)],
  'props': [], 'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.08, 'focus': [0.7, 0.5]},
  'narration': N(19), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'arrow-whoosh-magic', 'at': 0.1, 'volume': 0.7}, {'id': 'drum-hit', 'onWord': W('Arjuna', 'अर्जुन'), 'volume': 0.6}],
  'transition': 'cut', 'notes': 'Bhishma §120: Arjuna behind Shikhandi with the Gandiva; Bhishma smiles: "These are not Shikhandi\'s arrows."'},
 # 20 the bed of arrows
 {'id': 's20', 'beat': 20, 'type': 'prop-hero', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'dust', 'n': 15}, {'type': 'rays', 'x': 0.5, 'y': 0.35, 'color': '#FFD1A0'}],
  'characters': [], 'props': [P('bed-of-arrows', 0.5, 0.5, 1.6, 'still')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.08, 'focus': [0.5, 0.6]},
  'narration': N(20), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'drum-boom-deep', 'at': 0.3, 'volume': 0.8}],
  'music': 0.7, 'transition': 'dissolve', 'notes': 'Bhishma lying on a bed of arrow shafts, held above the ground (§121). No wounds shown.'},
 # 21 one vow
 {'id': 's21', 'beat': 21, 'type': 'prop-hero', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'silhouette',
  'fx': [{'type': 'embers', 'n': 15}],
  'characters': [], 'props': [P('bed-of-arrows', 0.5, 0.62, 1.0, 'still'), P('amba-shadow', 0.5, 0.36, 1.0, 'ascend')],
  'camera': {'move': 'crane-up', 'from': 0.0, 'to': -0.05},
  'narration': N(21), 'onScreenText': None, 'cues': [],
  'sfx': [{'id': 'wind-desolate', 'at': 0, 'volume': 0.4}],
  'transition': 'dissolve', 'notes': 'Amba\'s shadow rises over the fallen Bhishma, then fades.'},
 # 22 the Vasus curse Arjuna
 {'id': 's22', 'beat': 22, 'type': 'character', 'background': YB, 'backgroundVariant': 'dusk', 'light': 'dusk',
  'fx': [{'type': 'glow', 'x': 0.5, 'y': 0.3, 'r': 0.3, 'color': '#FFE6B0', 'pulse': True}],
  'characters': [C('arjuna', 'standing-bow', 0.5, 0.84, 0.95, action='still', expression='worried', light='silhouette')],
  'props': [P('vasu-lights', 0.5, 0.3, 1.0, 'circle')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
  'narration': N(22), 'onScreenText': tag('The Vasus', 'वसु', 'Ashvamedhika Parva §81', 'आश्वमेधिक पर्व §81'),
  'cues': [], 'sfx': [{'id': 'thunder-crack', 'onWord': W('cursed', 'शाप'), 'volume': 0.5}],
  'transition': 'cut', 'notes': 'Eight Vasu lights over the Ganga; Arjuna below in shadow.'},
 # 23 tease E05
 {'id': 's23', 'beat': 23, 'type': 'character', 'background': RP, 'backgroundVariant': 'dusk', 'light': 'silhouette',
  'fx': [{'type': 'embers', 'n': 20}, {'type': 'glow', 'x': 0.5, 'y': 0.45, 'r': 0.3, 'color': '#E8B53A', 'pulse': True}],
  'characters': [],
  'props': [P('karna-silhouette', 0.5, 0.6, 1.0, 'still'), P('shaap-stamp', 0.5, 0.28, 0.7, 'stamp-in')],
  'camera': {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.1},
  'narration': N(23), 'onScreenText': {'en': 'CURSED V', 'hi': 'शाप V', 'style': 'stamp-gold'},
  'cues': [{'onWord': W('Karna', 'कर्ण'), 'do': 'stamp-next', 'target': 'shaap-stamp'}],
  'sfx': [{'id': 'drum-hit', 'onWord': W('Karna', 'कर्ण'), 'volume': 0.9}],
  'overlay': 'folk-art-border', 'transition': 'cut-to-black',
  'notes': 'Tease for S01E05 (Karna\'s curses): Karna in silhouette, a glint of golden armour and earrings.'},
]

doc = {
 'id': 'S01E04', 'title': {'en': 'The Woman Who Vowed to Kill Bhishma', 'hi': 'भीष्म-वध की प्रतिज्ञा'},
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Mahabharata, Udyoga & Bhishma Parva', 'hi': 'महाभारत, उद्योग और भीष्म पर्व'},
 'safeZone': {'bottom': 0.2, 'right': 0.12},
 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True},
 'sound': e03['sound'],
 'thumbnail': {'scene': 's13', 'at': 0.5, 'series': {'en': 'Shraap · Episode 4', 'hi': 'शाप · भाग 4'},
   'title': {'en': 'The Woman Who Vowed to Kill Bhishma', 'hi': 'भीष्म-वध की प्रतिज्ञा'},
   'titleLines': {'en': ['She Vowed', 'to Kill', 'Bhishma'], 'hi': ['भीष्म-वध की', 'प्रतिज्ञा']}},
 'scenes': scenes,
 'assets': {
  'characters': [
   {'id': 'bhishma', 'status': 'new', 'poses': {'vow-hand-raised': 'new', 'standing-bow': 'new', 'drawing-bow': 'new', 'releasing': 'new', 'gesturing': 'new', 'bow-still': 'new'},
    'notes': 'Full rig from the pandu rig: young (s02–s05, s09) and old (s17–s19) as expression/variant? → two looks: "young" poses and "old" poses (white beard, white hair) — decide in /assets'},
   {'id': 'amba', 'status': 'new', 'poses': {'tapas-standing': 'new', 'standing-sad': 'new', 'folded-hands': 'new', 'resolute': 'new'}, 'derive': 'S01E02 women build'},
   {'id': 'ganga', 'status': 'new', 'poses': {'rising': 'new', 'cursing': 'new'}, 'notes': 'river goddess: crowned, water-blue and white, a small makara'},
   {'id': 'shalva', 'status': 'new', 'poses': {'defeated': 'new', 'turning-away': 'new'}, 'derive': 'pandu/king rig'},
   {'id': 'parashurama', 'status': 'new', 'poses': {'standing-axe': 'new', 'drawing-bow': 'new'}, 'derive': 'mandavya rig (sage) + axe, bow'},
   {'id': 'shikhandi', 'status': 'new', 'poses': {'standing-bow': 'new', 'drawing-bow': 'new'}, 'derive': 'uttar / pandu rig'},
   {'id': 'arjuna', 'status': 'library', 'poses': {'standing-bow': 'library', 'drawing-bow': 'new'}}],
  'backgrounds': [{'id': 'yamuna-bank', 'status': 'new', 'notes': 'river bank with reeds; water across the frame; feet ≈ 0.84'},
                  {'id': 'hastinapura-palace', 'status': 'library'}, {'id': 'king-court', 'status': 'library'},
                  {'id': 'red-sky-plain', 'status': 'library'}, {'id': 'hermitage', 'status': 'library'}, {'id': 'himalaya-peaks', 'status': 'library'}],
  'props': [
   {'id': 'three-princesses', 'status': 'new', 'notes': 'the two sisters as silhouettes behind'},
   {'id': 'closed-gate', 'status': 'new'}, {'id': 'crooked-river', 'status': 'new', 'notes': 'a dry winding riverbed, glowing'},
   {'id': 'shiva-light', 'status': 'new', 'notes': 'trident, crescent and a column of light; Shiva as a symbol only'},
   {'id': 'bed-of-arrows', 'status': 'new', 'notes': 'Bhishma lying on arrow shafts above the ground; no wounds'},
   {'id': 'vasu-lights', 'status': 'new', 'notes': 'eight lights in a ring'},
   {'id': 'karna-silhouette', 'status': 'new', 'notes': 'E05 tease; golden armour and earrings glint'},
   {'id': 'war-chariot', 'status': 'library'}, {'id': 'battle-silhouettes', 'status': 'library'}, {'id': 'gandiva-shockwave', 'status': 'library'},
   {'id': 'pyre-flames', 'status': 'library'}, {'id': 'rising-lights', 'status': 'library'}, {'id': 'amba-shadow', 'status': 'library'}],
  'overlays': [{'id': 'folk-art-border', 'status': 'library'}, {'id': 'shaap-stamp', 'status': 'library'}]}
}

errs = []
for s in scenes:
    for c in s.get('cues', []) + [x for x in s.get('sfx', []) if isinstance(x, dict) and 'onWord' in x]:
        for l in ('en', 'hi'):
            words = s['narration'][l].split()
            if not any(c['onWord'][l] in w for w in words): errs.append((s['id'], l, c['onWord'][l]))
    for el in s.get('characters', []) + s.get('props', []):
        if el['x'] > 0.88: errs.append((s['id'], 'x>0.88', el['id']))
print('errors:', errs)
open(f'{ep}/03-scenes.json', 'w').write(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
print('scenes', len(scenes))
