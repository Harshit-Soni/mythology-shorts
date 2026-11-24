"""S01E05 scene spec. Narration is parsed from 02-script.md (never retyped).
31 shots + the sting for 14 beats: shots inside a beat stay in one place (wide -> close), so the picture changes about every 3 s
without the story jumping. Close-ups are the same rigs at scale 2+ with the feet below the frame (y > 1).
Run:  python3 episodes/S01E05-karna-two-curses/svg/build-scenes.py <repo root>
"""
import json, os, re, sys
root = sys.argv[1]
ep = f'{root}/episodes/S01E05-karna-two-curses'
src = open(f'{ep}/02-script.md').read()

def beats(section):
    out = {}
    for line in section.split('\n'):
        m = re.match(r'^\| (\d+)[^|]*\| (.*?) \|', line)
        if m: out[int(m.group(1))] = m.group(2).strip()
    return out
EN = beats(src.split('## English')[1].split('**Ready cuts')[0])
HI = beats(src.split('## हिंदी')[1].split('**Ready cuts')[0])
assert len(EN) == 14 and len(HI) == 14, (len(EN), len(HI))
N = lambda b: {'en': EN[b], 'hi': HI[b]}
E = {'en': '', 'hi': ''}
W = lambda en, hi: {'en': en, 'hi': hi}
def C(id, pose, x, y, scale, flip=False, action='breathe', **kw):
    d = {'id': id, 'pose': pose, 'x': x, 'y': y, 'scale': scale, 'flip': flip, 'action': action}; d.update(kw); return d
def P(id, x, y, scale, action='idle', **kw):
    return {'id': id, 'x': x, 'y': y, 'scale': scale, 'action': action, **kw}
def tag(en, hi, sub_en=None, sub_hi=None):
    t = {'en': en, 'hi': hi, 'style': 'name-tag'}
    if sub_en: t['sub'] = {'en': sub_en, 'hi': sub_hi}
    return t
def stamp(en, hi): return {'en': en, 'hi': hi, 'style': 'stamp-gold'}
def cut(en, hi, target, **kw): return {'onWord': W(en, hi), 'do': 'hard-cut-to', 'target': target, **kw}
def S(id, beat, bg, *, chars=(), props=(), cam=None, text=None, cues=(), sfx=(), fx=(), variant=None, light=None,
      narr=None, transition='cut', notes='', type='character', **kw):
    d = {'id': id, 'beat': beat, 'type': type, 'background': bg}
    if variant: d['backgroundVariant'] = variant
    if light: d['light'] = light
    d.update({'fx': list(fx), 'characters': list(chars), 'props': list(props),
              'camera': cam or {'move': 'slow-zoom-in', 'from': 1.0, 'to': 1.06},
              'narration': narr or E, 'onScreenText': text, 'cues': list(cues), 'sfx': list(sfx)})
    d.update(kw); d.update({'transition': transition, 'notes': notes}); return d
def zoom(a, b, f=None, move='slow-zoom-in'):
    c = {'move': move, 'from': a, 'to': b}
    if f: c['focus'] = f
    return c
snd = lambda id, en=None, hi=None, at=0, vol=0.6, off=0: ({'id': id, 'onWord': W(en, hi), 'volume': vol, 'offset': off} if en else {'id': id, 'at': at, 'volume': vol})

e03 = json.load(open(f'{root}/episodes/S01E03-urvashi-curses-arjuna/03-scenes.json'))
sting = next(s for s in e03['scenes'] if s['id'] == 's00')
sting = {**sting, 'onScreenText': {**sting['onScreenText'], 'en': 'CURSED V', 'hi': 'शाप V'}}

HP = 'hastinapura-palace'  # courtyard feet 0.90
MA = 'mahendra-ashram'     # NEW: hermitage terrace on Mount Mahendra above the sea; feet expected 0.84
SS = 'sea-shore'           # NEW: beach by the hermitage; feet expected 0.84
RP = 'red-sky-plain'       # Kurukshetra; feet 0.80-0.82
BLUE, GOLD, FIRE = '#9FD3E6', '#E8B53A', '#E07A2E'  # in the battle Arjuna is always on the left, Karna on the right
dust = lambda n=15: {'type': 'dust', 'n': n}
embers = lambda n=20: {'type': 'embers', 'n': n}
glow = lambda x, y, r, c: {'type': 'glow', 'x': x, 'y': y, 'r': r, 'color': c, 'pulse': True}

scenes = [sting,
 # 1 hook: the wheel everyone remembers
 S('s01', 1, RP, variant='dusk', light='fire', type='prop-hero', narr=N(1), fx=[embers(), dust(25)],
   props=[P('sunk-wheel', 0.5, 0.5, 1.5, 'still')], cam=zoom(1.0, 1.1, [0.5, 0.6], 'shake-then-zoom'),
   cues=[cut('Few', 'क्यों', 's01b')], sfx=[snd('drum-boom-deep', at=0, vol=0.8), snd('battle-distant', at=0, vol=0.3)],
   notes='Close on a chariot wheel, half swallowed by cracked red earth.'),
 S('s01b', 1, RP, variant='dusk', light='fire', fx=[embers(), dust(20)],
   chars=[C('karna', 'pulling-wheel', 0.58, 0.83, 1.35, flip=True, action='still', expression='strain')],
   props=[P('sunk-wheel', 0.3, 0.68, 0.85, 'still')], cam=zoom(1.06, 1.0, [0.5, 0.55], 'slow-zoom-out'),
   text=tag('Karna', 'कर्ण'), sfx=[snd('heartbeat', at=0, vol=0.45)], transition='flash-white',
   notes='Pull back: Karna, both hands on it, cannot lift it.'),
 # 2 trailer: lie / cow / insect
 S('s02', 2, MA, light='dawn', narr=N(2), chars=[C('karna', 'folded-hands', 0.5, 1.5, 2.9, action='still', expression='uneasy')],
   cam=zoom(1.0, 1.05), cues=[cut('cow', 'गाय', 's02b'), cut('insect', 'कीड़ा', 's02c')], sfx=[snd('drum-hit', 'lie', 'झूठ', vol=0.5)],
   notes='Trailer 1/3, the lie: close on Karna\'s joined palms and a glance aside.'),
 S('s02b', 2, SS, light='dawn', type='prop-hero', props=[P('homa-cow', 0.5, 0.62, 1.4, 'still')], cam=zoom(1.0, 1.05),
   sfx=[snd('drum-hit', at=0, vol=0.5), snd('temple-bells', at=0, vol=0.3)], notes='Trailer 2/3: the cow, alive and garlanded, a bell at her neck.'),
 S('s02c', 2, 'parchment-card', overlay='folk-art-border', type='prop-hero', props=[P('alarka-worm', 0.5, 0.47, 1.3, 'sway')], cam=zoom(1.0, 1.08, [0.5, 0.55], 'push-in-fast'),
   sfx=[snd('drum-hit', at=0, vol=0.6)], transition='flash-white', notes='Trailer 3/3: the insect (Shanti 3: eight feet, fangs, needle bristles), very close.'),
 # 3 Drona refuses
 S('s03', 3, HP, light='dawn', narr=N(3), fx=[dust(12)],
   chars=[C('arjuna', 'drawing-bow', 0.64, 0.9, 1.0, flip=False, action='draw-bow', expression='calm'),
          C('karna', 'watching', 0.22, 0.9, 0.95, action='still', expression='envious')],
   cues=[cut('Karna', 'कर्ण', 's03b')], sfx=[snd('bowstring-creak', at=0.1, vol=0.5)], text=tag('Arjuna', 'अर्जुन'),
   notes='Arjuna draws; Karna watches from behind. Shanti 2 (CE 12.2.9).'),
 S('s03b', 3, HP, light='dawn', fx=[dust(12)],
   chars=[C('karna', 'asking', 0.28, 0.9, 1.0, expression='earnest'), C('drona', 'refusing', 0.7, 0.9, 1.0, flip=True, expression='stern')],
   props=[P('astra-ring', 0.5, 0.36, 0.6, 'stamp-in')], cam=zoom(1.0, 1.1, [0.6, 0.5]),
   text=tag('Drona', 'द्रोण', 'teacher of Arjuna and Karna', 'अर्जुन और कर्ण के गुरु'),
   cues=[{'onWord': W('Brahmastra', 'ब्रह्मास्त्र'), 'do': 'stamp-in', 'target': 'astra-ring'}],
   sfx=[snd('shimmer-descend', 'Brahmastra', 'ब्रह्मास्त्र', vol=0.5), snd('gong-soft', 'refused', 'मना', vol=0.6)],
   transition='dissolve', notes='Karna asks; the weapon glows between them; Drona\'s palm says no. CE 12.2.9-13.'),
 # 4 the lie
 S('s04', 4, MA, light='dawn', narr=N(4), fx=[{'type': 'rays', 'x': 0.7, 'y': 0.2, 'color': '#FFE6B0'}],
   chars=[C('karna', 'folded-hands', 0.28, 0.84, 0.95, expression='calm'), C('parashurama', 'standing-axe', 0.7, 0.84, 1.05, flip=True, expression='stern')],
   text=tag('Parashurama', 'परशुराम', 'Mount Mahendra', 'महेन्द्र पर्वत'), cues=[cut('lied', 'झूठ', 's04b')],
   sfx=[snd('gong-soft', 'Parashurama', 'परशुराम', vol=0.5)], notes='Plain student\'s cloth, no crown: he has come disguised. CE 12.2.14-16.'),
 S('s04b', 4, MA, light='dawn', chars=[C('karna', 'folded-hands', 0.46, 1.5, 2.9, action='still', expression='uneasy', speaking=True)],
   cam=zoom(1.0, 1.06, [0.5, 0.4]), sfx=[snd('heartbeat', at=0, vol=0.5)], transition='dissolve', notes='Close: he says it. Lip-sync on the quote.'),
 # 5 the cow
 S('s05', 5, SS, variant='dusk', light='dusk', narr=N(5), fx=[dust(10)],
   chars=[C('karna', 'student-bow', 0.2, 0.84, 0.85, action='still', expression='calm')],
   props=[P('glowing-arrow', 0.48, 0.5, 0.55, 'glint'), P('homa-cow', 0.76, 0.67, 0.55, 'graze')], cam=zoom(0.0, 0.03, move='slow-pan-right'),
   cues=[cut('accident', 'गाय', 's05b')], sfx=[snd('arrow-whoosh-magic', 'killed', 'अनजाने', vol=0.6)],
   notes='He practises by the sea; far off, half hidden by dunes, a cow. The arrow is in the air. No hit shown. CE 12.2.19-20 (arrow: Karna Parva 8.29.33).'),
 S('s05b', 5, SS, variant='dusk', light='dusk',
   chars=[C('karna', 'kneeling-pleading', 0.25, 0.84, 1.15, expression='stricken'), C('homa-brahmin', 'standing-grief', 0.72, 0.84, 1.0, flip=True, expression='stern')],
   props=[P('cow-bell', 0.5, 0.82, 0.5, 'still')], cam=zoom(1.0, 1.06),
   sfx=[snd('temple-bells', at=0, vol=0.35)], music=0.6, notes='A bell and a broken garland on the sand between them: all we see of the death. He owns up and begs. CE 12.2.21-22.'),
 # 6 the first curse
 S('s06', 6, SS, variant='dusk', light='fire', narr=N(6), fx=[{'type': 'sparks', 'n': 14}],
   chars=[C('homa-brahmin', 'cursing', 0.5, 1.12, 1.6, flip=True, action='raise-hand', expression='furious', speaking=True)],
   props=[P('shaap-stamp', 0.5, 0.26, 0.7, 'stamp-in')], text=stamp('CURSED', 'शाप'),
   cam=zoom(1.0, 1.06, [0.5, 0.45], 'shake-then-zoom'),
   cues=[{'onWord': W('cursed', 'शाप'), 'do': 'stamp-next', 'target': 'shaap-stamp'}, cut('earth', 'धरती', 's06b')],
   sfx=[snd('thunder-crack', 'cursed', 'शाप', vol=0.6), snd('stamp-thud', 'cursed', 'शाप', vol=0.8, off=0.1)], music=1.1,
   notes='The Brahmin, waist-up. First stamp. CE 12.2.23-26.'),
 S('s06b', 6, SS, variant='night', light='fire', fx=[glow(0.62, 0.62, 0.3, FIRE)],
   chars=[C('karna', 'kneeling-pleading', 0.25, 0.84, 1.15, action='still', expression='stricken')],
   props=[P('wheel-light', 0.64, 0.56, 1.05, 'fall')], cam=zoom(1.0, 1.08, [0.5, 0.55]),
   sfx=[snd('drum-boom-deep', at=0.1, vol=0.6), snd('heartbeat', 'Careless', 'असावधानी', vol=0.6)], transition='dissolve',
   notes='His words as a vision: a wheel drawn in light sinks into the sand before the kneeling Karna.'),
 # 7 he learns the weapon
 S('s07', 7, MA, variant='night', light='divine', narr=N(7), fx=[{'type': 'stars', 'n': 35}, glow(0.5, 0.4, 0.3, GOLD), {'type': 'sparks', 'n': 14}],
   chars=[C('karna', 'folded-hands', 0.24, 0.84, 0.95, expression='awed'), C('parashurama', 'teaching', 0.74, 0.84, 1.05, flip=True, expression='kind')],
   props=[P('astra-ring', 0.5, 0.4, 1.0, 'circle')], cam=zoom(1.0, 1.08, [0.5, 0.42]), text=tag('The Brahmastra', 'ब्रह्मास्त्र'),
   sfx=[snd('shimmer-descend', at=0.1, vol=0.6)], transition='dissolve', notes='The weapon as a blazing ring between guru and pupil. CE 12.3.1-3.'),
 # 8 the insect
 S('s08', 8, MA, light='dawn', narr=N(8), fx=[dust(8)],
   chars=[C('karna', 'guru-on-lap', 0.36, 0.8, 1.15, action='still', expression='calm'), C('parashurama', 'sleeping', 0.58, 0.83, 1.4, action='still')], cam=zoom(1.0, 1.06, [0.5, 0.6]),
   cues=[cut('insect', 'कीड़ा', 's08b'), cut('sleep', 'जागें', 's08c')], sfx=[snd('wind-desolate', at=0, vol=0.2)], music=0.6,
   notes='Karna seated cross-legged; Parashurama asleep in front of him, his head in Karna\'s lap. CE 12.3.4-5.'),
 S('s08b', 8, MA, light='dawn', type='prop-hero', props=[P('worm-on-thigh', 0.5, 0.74, 2.0, 'still')], cam=zoom(1.0, 1.1, [0.5, 0.55]),
   sfx=[snd('heartbeat', at=0, vol=0.6)], music=0.5, notes='Close: the insect on the folded cloth over his thigh, one thin red line. No wound. CE 12.3.6-7.'),
 S('s08c', 8, MA, light='dawn', chars=[C('karna', 'enduring', 0.5, 1.53, 3.0, action='still', expression='pained')],
   cam=zoom(1.0, 1.08, [0.5, 0.4]), sfx=[snd('heartbeat', at=0, vol=0.7)], music=0.4, transition='flash-white', notes='Close: jaw clenched, one tear, not a tremor. CE 12.3.8-9.'),
 # 9 found out
 S('s09', 9, MA, light='fire', narr=N(9), fx=[{'type': 'sparks', 'n': 10}],
   chars=[C('karna', 'bowed', 0.25, 0.84, 1.15, expression='afraid'), C('parashurama', 'accusing', 0.7, 0.84, 1.1, flip=True, action='point', expression='furious', speaking=True)],
   cues=[cut('Tell', 'सच', 's09b')], cam=zoom(1.0, 1.05), sfx=[snd('drum-hit', at=0.1, vol=0.6)], music=1.0,
   notes='Parashurama is on his feet. CE 12.3.10-11, 24-25.'),
 S('s09b', 9, MA, light='fire', chars=[C('parashurama', 'accusing', 0.6, 1.45, 2.6, flip=True, action='still', expression='furious', speaking=True)],
   cam=zoom(1.0, 1.06, [0.5, 0.4], 'push-in-fast'), sfx=[snd('thunder-crack', at=0, vol=0.35)], notes='Close on his eyes.'),
 # 10 the second curse
 S('s10', 10, MA, variant='dusk', light='dusk', narr=N(10), chars=[C('karna', 'bowed', 0.44, 0.92, 2.0, action='still', expression='ashamed', speaking=True)],
   cam=zoom(1.0, 1.05, [0.5, 0.5]), cues=[cut('second', 'दूसरा', 's10b')], music=0.5, transition='flash-white', notes='Waist-up: he tells the truth. CE 12.3.26-28.'),
 S('s10b', 10, MA, variant='dusk', light='fire', fx=[{'type': 'sparks', 'n': 14}, glow(0.36, 0.5, 0.22, GOLD)],
   chars=[C('karna', 'bowed', 0.23, 0.84, 1.1, action='still', expression='ashamed'), C('parashurama', 'cursing', 0.72, 0.84, 0.96, flip=True, action='raise-hand', expression='furious', speaking=True)],
   props=[P('shaap-stamp', 0.5, 0.24, 0.7, 'stamp-in')], text=stamp('CURSED', 'शाप'),
   cam=zoom(1.0, 1.06, [0.5, 0.5], 'shake-then-zoom'), cues=[{'onWord': W('curse', 'शाप'), 'do': 'stamp-next', 'target': 'shaap-stamp'}],
   sfx=[snd('thunder-crack', 'curse', 'शाप', vol=0.6), snd('stamp-thud', 'curse', 'शाप', vol=0.8, off=0.1), snd('glass-crack', 'fail', 'साथ', vol=0.5)], music=1.1,
   transition='fade-to-night', notes='Second stamp. CE 12.3.29-31.'),
 # 11 both come due
 S('s11', 11, RP, variant='dusk', light='fire', narr=N(11), fx=[embers(25), dust(20)],
   chars=[C('arjuna', 'drawing-bow', 0.22, 0.82, 0.95, action='draw-bow', expression='fierce'), C('karna', 'drawing-bow', 0.76, 0.82, 0.95, flip=True, action='draw-bow', expression='fierce')],
   props=[P('battle-silhouettes', 0.5, 0.63, 0.9, 'still')], text=tag('Kurukshetra', 'कुरुक्षेत्र', 'Karna Parva', 'कर्ण पर्व'),
   cues=[cut('wheel', 'पहिया', 's11b'), cut('weapon', 'अस्त्र', 's11c')], sfx=[snd('battle-distant', at=0, vol=0.4), snd('arrow-whoosh-magic', at=0.4, vol=0.5)], music=1.2,
   notes='The duel. CE 8.66.'),
 S('s11b', 11, RP, variant='dusk', light='fire', type='prop-hero', fx=[dust(30), embers(15)],
   props=[P('sunk-wheel', 0.5, 0.5, 1.5, 'still')], cam=zoom(1.0, 1.08, [0.5, 0.6], 'shake-then-zoom'),
   sfx=[snd('drum-boom-deep', at=0, vol=0.9)], notes='Curse 1: the hook\'s image again. CE 8.66.42.'),
 S('s11c', 11, RP, variant='dusk', light='dusk', fx=[embers(15)],
   chars=[C('karna', 'empty-hand', 0.5, 1.12, 1.6, flip=True, action='still', expression='stricken')], props=[P('astra-ring-dark', 0.4, 0.3, 0.75, 'still')],
   cam=zoom(1.0, 1.05, [0.5, 0.45]), sfx=[snd('glass-crack', at=0.1, vol=0.5)], music=0.5, notes='Curse 2: he calls; the ring above his palm stays dark and cracked. CE 8.66.42.'),
 # 12 caught up with the wheel
 S('s12', 12, RP, variant='dusk', light='fire', narr=N(12), fx=[embers(20), dust(20)],
   chars=[C('karna', 'pulling-wheel', 0.6, 0.83, 1.4, flip=True, action='still', expression='strain')], props=[P('sunk-wheel', 0.31, 0.68, 0.9, 'still')],
   cam=zoom(1.0, 1.06, [0.5, 0.6]), cues=[{'onWord': W('wheel', 'पहिये'), 'do': 'pull-fail', 'target': 'karna'}, cut('Arjuna', 'अर्जुन', 's12b')],
   sfx=[snd('heartbeat', at=0.2, vol=0.6)], music=0.6, notes='CE 8.67.23, "cakre visaktam".'),
 S('s12b', 12, RP, variant='dusk', light='fire', fx=[embers(20), {'type': 'sparks', 'n': 20}],
   chars=[C('arjuna', 'drawing-bow', 0.4, 1.12, 1.6, action='still', expression='fierce')], props=[P('glowing-arrow', 0.7, 0.5, 0.7, 'glint')],
   cam=zoom(1.0, 1.1, [0.6, 0.5], 'push-in-fast'), sfx=[snd('arrow-whoosh-magic', at=0.1, vol=0.9)], transition='flash-white',
   notes='We stay on Arjuna; the arrow leaves and the screen goes white. The death itself isn\'t shown.'),
 # 13 the loop closes
 S('s13', 13, 'parchment-card', overlay='folk-art-border', type='prop-hero', narr=N(13), props=[P('cow-bell', 0.5, 0.47, 1.25, 'still')], cam=zoom(1.0, 1.05),
   cues=[cut('wheel', 'पहिया', 's13b'), cut('lie', 'कीड़े', 's13c'), cut('took', 'झूठ', 's13d', nth={'en': 2, 'hi': 1})], sfx=[snd('temple-bells', at=0, vol=0.4)], music=0.6,
   notes='The cow\'s bell on the sand.'),
 S('s13b', 13, RP, variant='dusk', light='dusk', type='prop-hero', fx=[dust(10)], props=[P('sunk-wheel', 0.5, 0.5, 1.2, 'still')], cam=zoom(1.05, 1.0, move='slow-zoom-out'),
   notes='The wheel, alone now.'),
 S('s13c', 13, 'parchment-card', overlay='folk-art-border', type='prop-hero', props=[P('alarka-worm', 0.5, 0.47, 1.3, 'sway')], cam=zoom(1.0, 1.05), notes='The insect from the trailer.'),
 S('s13d', 13, RP, variant='dusk', light='dusk', type='prop-hero', fx=[{'type': 'rays', 'x': 0.5, 'y': 0.3, 'color': '#FFD1A0'}, glow(0.5, 0.35, 0.25, GOLD)],
   props=[P('astra-ring-dark', 0.5, 0.53, 0.7, 'still'), P('rising-lights', 0.5, 0.34, 0.9, 'ascend')], cam=zoom(0.0, -0.05, move='crane-up'),
   sfx=[snd('shimmer-descend', at=0, vol=0.5)], transition='dissolve', notes='The dark ring, and the light that rose from Karna (CE 8.67.27).'),
 # 14 tease E06
 S('s14', 14, 'amaravati-court', variant='night', light='night', type='prop-hero', narr=N(14), fx=[embers(15), glow(0.5, 0.42, 0.3, GOLD)],
   props=[P('nahusha-silhouette', 0.48, 0.54, 1.15, 'still'), P('shaap-stamp', 0.5, 0.26, 0.7, 'stamp-in')], text=stamp('CURSED VI', 'शाप VI'),
   cues=[{'onWord': W('snake', 'साँप'), 'do': 'stamp-next', 'target': 'shaap-stamp'}], cam=zoom(1.0, 1.1), sfx=[snd('drum-hit', 'snake', 'साँप', vol=0.9)],
   overlay='folk-art-border', transition='cut-to-black', notes='Tease for E06: a crowned king whose shadow is a serpent (Nahusha, CE 5.17.11-16).'),
]

have = lambda kind, i: os.path.exists(f'{root}/assets/{kind}/{i}.svg')
poses, bgs, prs, ovs = {}, [], [], []
for s in scenes:
    for c in s['characters']: poses.setdefault(c['id'], {})[c['pose']] = 'library' if have(f"characters/{c['id']}", c['pose']) else 'new'
    if s['background'] not in bgs: bgs.append(s['background'])
    for p in s['props']:
        if p['id'] == 'shaap-stamp': continue
        if p['id'] not in prs: prs.append(p['id'])
    if s.get('overlay') and s['overlay'] not in ovs: ovs.append(s['overlay'])
st = lambda kind, i: {'id': i, 'status': 'library' if have(kind, i) or i == 'falling-light' else 'new'}
doc = {
 'id': 'S01E05', 'title': {'en': 'The Warrior Cursed Twice', 'hi': 'दो बार शापित योद्धा'},
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Mahabharata, Shanti & Karna Parva', 'hi': 'महाभारत, शान्ति और कर्ण पर्व'},
 'safeZone': {'bottom': 0.2, 'right': 0.12}, 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True}, 'sound': e03['sound'],
 'thumbnail': {'scene': 's01b', 'at': 0.5, 'series': {'en': 'Shraap · Episode 5', 'hi': 'शाप · भाग 5'},
   'title': {'en': "Why Karna's Wheel Sank", 'hi': 'कर्ण का पहिया क्यों धँसा?'}, 'titleLines': {'en': ['Why Karna’s', 'Wheel Sank'], 'hi': ['कर्ण का पहिया', 'क्यों धँसा?']}},
 'scenes': scenes,
 'assets': {'characters': [{'id': i, 'status': 'library' if all(v == 'library' for v in p.values()) else 'new', 'poses': p} for i, p in poses.items()],
            'backgrounds': [st('backgrounds', i) for i in bgs], 'props': [st('props', i) for i in prs],
            'overlays': [st('overlays', i) for i in ovs + ['shaap-stamp']]}}

# --- checks -----------------------------------------------------------------
errs, ids = [], [s['id'] for s in scenes]
assert len(ids) == len(set(ids))
clean = lambda t: [re.sub(r"[^\wऀ-ॣ०-ॿ]", '', w).lower() for w in re.sub("[’']s\\b", '', t).split()]
parent = {}
for s in scenes:
    if any(s['narration'].values()): parent[s['beat']] = s
for s in scenes:
    refs = [c for c in s['cues']] + [x for x in s['sfx'] if isinstance(x, dict) and 'onWord' in x]
    for r in refs:
        for l in ('en', 'hi'):
            full = clean((s if any(s['narration'].values()) else parent[s['beat']])['narration'][l])
            if not any(s['narration'].values()):            # an insert hears only the words after its own cut, up to the next
                cs = [c for c in parent[s['beat']]['cues'] if c['do'] == 'hard-cut-to']
                at = lambda c: [i for i, w in enumerate(full) if c['onWord'][l].lower() in w][c.get('nth', {}).get(l, 1) - 1]
                a = at(next(c for c in cs if c['target'] == s['id'])); b = min([at(c) for c in cs if at(c) > a] + [len(full)])
                full = full[a:b]
            hits = [w for w in full if r['onWord'][l].lower() in w]
            if len(hits) < r.get('nth', {}).get(l, 1): errs.append((s['id'], l, r['onWord'][l], 'not heard'))
            elif hits[0] != r['onWord'][l].lower(): errs.append((s['id'], l, r['onWord'][l], f'matches inside "{hits[0]}"'))
        if r.get('do') == 'hard-cut-to':
            t = next((x for x in scenes if x['id'] == r['target']), None)
            if not t or t['beat'] != s['beat'] or any(t['narration'].values()): errs.append((s['id'], 'bad insert', r['target']))
    for el in s['characters'] + s['props']:
        if el['x'] > 0.88: errs.append((s['id'], 'x>0.88', el['id']))
for s in scenes:
    if s['beat'] and not any(s['narration'].values()) and s['id'] != 's00' and not any(c.get('target') == s['id'] for x in scenes for c in x['cues']): errs.append((s['id'], 'never cut to'))
print('errors:', errs)
json.dump(doc, open(f'{ep}/03-scenes.json', 'w'), ensure_ascii=False, indent=2); open(f'{ep}/03-scenes.json', 'a').write('\n')
print('scenes', len(scenes), '| new:', {k: [x['id'] + (':' + ','.join(p for p, v in x['poses'].items() if v == 'new') if 'poses' in x else '') for x in v if x['status'] == 'new'] for k, v in doc['assets'].items()})
