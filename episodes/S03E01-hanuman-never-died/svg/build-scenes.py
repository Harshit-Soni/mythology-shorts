"""S03E01 scene spec. Narration is parsed from 02-script.md (never retyped; markdown *italics* stripped).
A new series sting plus shots for 13 beats. Shots inside a beat stay in one place (wide -> close), so the picture changes
about every 3 s without the story jumping. Close-ups are the same rigs at scale 2+ with the feet below the frame (y > 1).
Axis: Hanuman is on the left facing right, Rama on the right facing left (flip), whenever they're together.
Run:  python3 episodes/S03E01-hanuman-never-died/svg/build-scenes.py <repo root>
"""
import json, os, re, sys
root = sys.argv[1]
ep = f'{root}/episodes/S03E01-hanuman-never-died'
src = open(f'{ep}/02-script.md').read()

def beats(section):
    out = {}
    for line in section.split('\n'):
        m = re.match(r'^\| (\d+)[^|]*\| (.*?) \|', line)
        if m: out[int(m.group(1))] = m.group(2).strip().replace('*', '')
    return out
EN = beats(src.split('## English')[1].split('**Word count')[0])
HI = beats(src.split('## हिंदी')[1].split('**Word count')[0])
assert len(EN) == 13 and len(HI) == 13, (len(EN), len(HI))
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
def title(en, hi): return {'en': en, 'hi': hi, 'style': 'plate'}
def title_in(en, hi): return {'onWord': W(en, hi), 'do': 'title-in'}
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
# The new series sting: the same timing as Shraap's, with its own mark (an undying lamp) instead of the curse stamp.
sting = {'id': 's00', 'beat': 0, 'type': 'title-card', 'background': 'parchment-card', 'characters': [],
         'props': [{'id': 'chiranjeevi-seal', 'x': 0.5, 'y': 0.42, 'scale': 1.2, 'action': 'stamp-in'}], 'overlay': 'folk-art-border',
         'camera': {'move': 'static'}, 'narration': E, 'fixedDurationSec': 1.0,
         'onScreenText': {'en': 'CHIRANJEEVI I', 'hi': 'चिरंजीवी I', 'style': 'stamp-gold'}, 'cues': [],
         'sfx': [{'id': 'temple-bells', 'at': 0, 'volume': 0.6}, {'id': 'stamp-thud', 'at': 0.15, 'volume': 0.8}],
         'transition': 'border-wipe', 'music': 0.6, 'notes': 'Series sting for S03 Chiranjeevi, reused every episode: the border closes, an undying lamp lands, numbered I.'}

SP = 'sunrise-peak'       # NEW: a mountain top at dawn, a huge red sun low on the horizon; feet expected 0.84
HS, HP, SF, SH = 'heaven-sky', 'himalaya-peaks', 'spring-forest', 'sea-shore'   # library: no ground / 0.80 / 0.86 / 0.84
KC, RB, PN, PC = 'king-court', 'yamuna-bank', 'peepal-night', 'parchment-card'  # library: throne 0.575 + step 0.88 / 0.84 / 0.82
GOLD, SAFF = '#E8B53A', '#F2A541'
dust = lambda n=15: {'type': 'dust', 'n': n}
stars = lambda n=30: {'type': 'stars', 'n': n}
sparks = lambda n=16: {'type': 'sparks', 'n': n}
leaf = lambda n=10: {'type': 'leaf', 'n': n}
birds = lambda n=6: {'type': 'birds', 'n': n}
rays = lambda x, y, c='#FFE6B0': {'type': 'rays', 'x': x, 'y': y, 'color': c}
glow = lambda x, y, r, c: {'type': 'glow', 'x': x, 'y': y, 'r': r, 'color': c, 'pulse': True}
H = lambda pose, x, y, sc, **kw: C('hanuman', pose, x, y, sc, action=kw.pop('action', 'still'), **kw)
R = lambda pose, x, y, sc, **kw: C('rama', pose, x, y, sc, flip=kw.pop('flip', True), action=kw.pop('action', 'still'), **kw)
CLOSE = dict(y=1.4, sc=2.6)    # a head-and-shoulders close-up: face ≈ 0.36

scenes = [sting,
 # 1 hook
 S('s01', 1, SP, light='dawn', narr=N(1), fx=[rays(0.7, 0.5), dust(10)], chars=[H('standing', 0.42, 1.4, 2.6, expression='calm')], cam=zoom(1.0, 1.06, [0.45, 0.36]),
   cues=[cut('never', 'कभी', 's01b')], sfx=[snd('gong-soft', at=0, vol=0.5)], notes='Hanuman in profile against a gold dawn: strong, calm, with his mace. Thumbnail.'),
 S('s01b', 1, PN, variant='night', light='fire', fx=[glow(0.62, 0.66, 0.25, SAFF), stars(24)], props=[P('katha-circle', 0.62, 0.74, 1.1, 'still')], chars=[H('seated-listening', 0.24, 0.84, 0.8, expression='calm')],
   cam=zoom(1.06, 1.0, move='slow-zoom-out'), sfx=[snd('night-crickets', at=0, vol=0.35)], transition='dissolve', notes='Where it ends: a story told by a lamp, and him listening at the edge (beat 12).'),
 # 2 the sun like a fruit
 S('s02', 2, SP, light='dawn', narr=N(2), fx=[birds(5), dust(8)], chars=[H('baby-reaching', 0.36, 0.84, 0.7, expression='wonder')], cam=zoom(1.0, 1.05, [0.5, 0.55]),
   cues=[cut('leaped', 'छलाँग', 's02b')], sfx=[snd('temple-bells', at=0.2, vol=0.3)], notes='A small child on a peak, the red sun rising like a fruit. CE 4.65.19.'),
 S('s02b', 2, HS, variant='dawn', light='dawn', fx=[rays(0.72, 0.28)], chars=[H('baby-leaping', 0.4, 0.8, 0.9, expression='wonder', shadow=False)], cam=zoom(0.05, -0.08, move='crane-up'),
   sfx=[snd('shimmer-descend', at=0, vol=0.4)], notes='Up into the sky toward the sun (top right). "Grab", never "swallow".'),
 # 3 the thunderbolt and the name
 S('s03', 3, HS, variant='dawn', light='divine', narr=N(3), fx=[sparks(12)], chars=[C('indra', 'hurling-vajra', 0.6, 1.2, 1.9, flip=True, action='still', expression='stern')], props=[P('vajra-flash', 0.26, 0.38, 0.8, 'glint')],
   text=tag('Indra', 'इंद्र', 'king of the gods', 'देवताओं के राजा'), cam=zoom(1.0, 1.06, [0.5, 0.36]), cues=[cut('fell', 'गिरे', 's03b'), cut('name', 'नाम', 's03c')],
   sfx=[snd('thunder-crack', 'thunderbolt', 'वज्र', vol=0.6)], notes='Indra hurls the vajra leftward, at the child. Not a villain: "not very angry" (7.35.46). CE 4.65.21.'),
 S('s03b', 3, HP, light='dawn', props=[P('vajra-flash', 0.5, 0.4, 1.0, 'glint')], chars=[H('baby-falling', 0.5, 0.62, 0.8, action='fall', expression='hurt', shadow=False)], cam=zoom(1.0, 1.08, [0.5, 0.6], 'shake-then-zoom'),
   sfx=[snd('drum-boom-deep', at=0, vol=0.6)], transition='flash-white', notes='A flash and a fall onto the peaks; no injury close-up. CE 4.65.22, 7.35.47.'),
 S('s03c', 3, PC, type='prop-hero', overlay='folk-art-border', chars=[H('baby-glowing', 0.5, 0.78, 0.9, expression='calm')], text=tag('Hanuman', 'हनुमान', 'hanu = jaw', 'हनु = जबड़ा'), cam=zoom(1.0, 1.05, [0.5, 0.5]),
   sfx=[snd('gong-soft', at=0, vol=0.4)], notes='The name card. CE 4.65.22, 7.36.11.'),
 # 4 the wind stops
 S('s04', 4, 'himalaya-gorge', variant='dusk', light='night', narr=N(4), fx=[dust(10)], chars=[C('vayu', 'holding-child', 0.46, 1.25, 2.1, action='still', expression='furious')], props=[P('wind-swirl', 0.7, 0.36, 0.9, 'circle')],
   text=tag('Vayu', 'पवनदेव', 'the wind god, his father', 'हवा के देवता, उनके पिता'), cam=zoom(1.0, 1.06, [0.48, 0.38]), cues=[cut('stopped', 'रोक', 's04b')],
   sfx=[snd('wind-desolate', at=0, vol=0.6)], notes='Vayu takes the child into a cave (7.35.48-49): grief and anger.'),
 S('s04b', 4, SF, variant='dusk', light='dusk', props=[P('still-world', 0.5, 0.7, 1.4, 'still')], cam={'move': 'static'}, music=0.2,
   sfx=[snd('heartbeat', at=0.2, vol=0.5)], notes='No wind: leaves hang, flags droop, birds and people stopped (silhouettes). The silence is the effect. CE 4.65.23, 7.35.49.'),
 # 5 the gods' gifts; Indra's boon
 S('s05', 5, HS, light='divine', narr=N(5), fx=[glow(0.5, 0.62, 0.35, GOLD), stars(20)], chars=[C('deva', 'offering', 0.2, 0.86, 0.8, action='still'), H('baby-glowing', 0.5, 0.8, 0.7, expression='calm'), C('deva', 'offering', 0.8, 0.86, 0.8, flip=True, action='still', variant='b')],
   cam=zoom(1.0, 1.05, [0.5, 0.6]), cues=[cut('Indra', 'इंद्र', 's05b')], sfx=[snd('shimmer-descend', at=0, vol=0.5)], notes='The gods around the child, in a ring of light. CE 7.36.9-24.'),
 S('s05b', 5, HS, light='divine', fx=[rays(0.5, 0.3)], chars=[C('indra', 'standing-blessing', 0.5, 1.4, 2.6, action='still', expression='smiling', speaking=True)], props=[P('seal-stamp', 0.5, 0.2, 0.6, 'stamp-in')],
   text=stamp('BY CHOICE', 'इच्छा-मृत्यु'), cues=[{'onWord': W('choose', 'चाहोगे'), 'do': 'stamp-next', 'target': 'seal-stamp'}], cam=zoom(1.0, 1.06, [0.5, 0.36]),
   sfx=[snd('stamp-thud', 'choose', 'चाहोगे', vol=0.8, off=0.1)], music=1.1, notes='Indra, now kind, gives the boon: death only by his own wish. CE 4.65.26-27.'),
 # 6 Rama's friend; the ocean; Sita
 S('s06', 6, 'red-sky-plain', variant='dawn', light='dawn', narr=N(6), chars=[H('standing', 0.3, 0.82, 0.95, expression='devoted'), R('standing', 0.68, 0.82, 0.95, expression='calm')], cam=zoom(1.0, 1.05),
   text=tag('Rama', 'राम'), cues=[cut('crossed', 'समुद्र', 's06b'), cut('Sita', 'सीता', 's06c')], sfx=[snd('temple-bells', at=0, vol=0.35)], notes='Grown: Hanuman at Rama\'s side, palms joined.'),
 S('s06b', 6, SH, variant='dawn', light='dawn', fx=[birds(4)], chars=[H('leaping', 0.42, 0.5, 1.1, expression='intent', shadow=False)], cam=zoom(0.0, 0.06, move='slow-pan-right'),
   sfx=[snd('wind-desolate', at=0, vol=0.4)], notes='One great leap over the sea. MBh 3.147.34.'),
 S('s06c', 6, SF, variant='night', light='moon', fx=[leaf(8)], chars=[C('sita', 'seated-grove', 0.5, 0.86, 1.1, action='still', expression='sad')], text=tag('Sita', 'सीता', "Rama's wife", 'राम की पत्नी'),
   cam=zoom(1.0, 1.05, [0.5, 0.55]), transition='dissolve', notes='Found in a grove: dignified, waiting. MBh 3.147.35.'),
 # 7 Rama is king; the farewell
 S('s07', 7, KC, light='dawn', narr=N(7), fx=[dust(8)], chars=[R('enthroned', 0.5, 0.575, 0.83, flip=False, expression='calm')], text=title('Ayodhya', 'अयोध्या'), cam=zoom(1.0, 1.05, [0.5, 0.42]),
   cues=[cut('goodbye', 'विदाई', 's07b')], sfx=[snd('temple-bells', at=0, vol=0.4)], notes='King at last. CE 7.38.'),
 S('s07b', 7, KC, light='dawn', chars=[R('enthroned', 0.5, 0.575, 0.83, flip=False, expression='calm'), H('bowing', 0.24, 0.88, 0.85, expression='devoted')], props=[P('vanara-crowd', 0.78, 0.84, 0.7, 'still')],
   cam=zoom(1.06, 1.0, move='slow-zoom-out'), sfx=[snd('gong-soft', at=0, vol=0.4)], notes='Friends leaving; Hanuman bows at the foot of the throne. CE 7.39.14.'),
 # 8 the request
 S('s08', 8, KC, light='dawn', narr=N(8), chars=[H('asking', 0.44, 1.4, 2.6, expression='devoted', speaking=True)], cam=zoom(1.0, 1.06, [0.45, 0.36]), cues=[cut('hear', 'सुनता', 's08b')], music=0.5,
   sfx=[snd('heartbeat', at=0, vol=0.35)], notes='Close: palms joined, eyes up to Rama. CE 7.39.15-16.'),
 S('s08b', 8, KC, light='divine', chars=[R('enthroned', 0.52, 1.2, 1.9, flip=False, expression='moved')], cam=zoom(1.0, 1.05, [0.5, 0.36]), music=0.5, notes='Rama hears it: "to hear my story".'),
 # 9 the embrace
 S('s09', 9, KC, light='divine', narr=N(9), fx=[glow(0.5, 0.5, 0.35, GOLD)], chars=[H('embraced', 0.42, 1.12, 1.7, expression='moved'), R('embracing', 0.58, 1.12, 1.7, expression='smile')], cam=zoom(1.0, 1.05, [0.5, 0.4]),
   cues=[cut('story', 'कथा', 's09b'), cut('you', 'तुम', 's09c')], sfx=[snd('shimmer-descend', at=0, vol=0.45)], music=1.1, notes='He rises from the throne and embraces him. CE 7.39.17.'),
 S('s09b', 9, KC, light='divine', chars=[R('standing', 0.52, 1.4, 2.6, expression='smile', speaking=True)], cam=zoom(1.0, 1.06, [0.5, 0.36]), notes='Close: "my story will last as long as the world". CE 7.39.18-19.'),
 S('s09c', 9, KC, light='divine', fx=[sparks(10)], chars=[H('standing', 0.44, 1.4, 2.6, expression='moved')], props=[P('rama-necklace', 0.44, 0.52, 0.5, 'glint')], cam=zoom(1.0, 1.08, [0.45, 0.45]),
   sfx=[snd('temple-bells', at=0.1, vol=0.4)], transition='dissolve', notes="Rama's own necklace now on Hanuman's chest, a glint (shown, not said). CE 7.39.20-21."),
 # 10 Rama leaves the world
 S('s10', 10, RB, variant='dawn', light='dawn', narr=N(10), fx=[rays(0.78, 0.35)], chars=[R('departing', 0.64, 0.84, 0.9, expression='calm')], text=title('Years later', 'बरसों बाद'),
   cam=zoom(0.0, 0.04, move='slow-pan-right'), cues=[title_in('Years', 'बरसों'), cut('everyone', 'सब', 's10b')], sfx=[snd('gong-soft', at=0, vol=0.45)], notes='In white, toward the light by the river. "Left the world", not died. CE 7.98-99.'),
 S('s10b', 10, RB, variant='dawn', light='dawn', props=[P('vanara-crowd', 0.42, 0.8, 1.5, 'slide-right')], chars=[R('departing', 0.8, 0.84, 0.8, expression='calm')], cam=zoom(1.0, 1.04),
   sfx=[snd('battle-distant', at=0, vol=0.25)], notes='Monkeys, bears, rakshasas and people all follow him. CE 7.98.17-20.'),
 # 11 "Stay."
 S('s11', 11, RB, variant='dawn', light='dawn', narr=N(11), chars=[H('standing', 0.32, 1.1, 1.65, expression='devoted'), R('hand-on-shoulder', 0.66, 1.1, 1.65, expression='calm', speaking=True)], cam=zoom(1.0, 1.05, [0.5, 0.4]),
   cues=[cut('Stay', 'यहीं', 's11b')], music=0.5, sfx=[snd('heartbeat', at=0, vol=0.35)], notes='Face to face; Rama\'s hand on his shoulder. CE 7.98.24-25.'),
 S('s11b', 11, RB, variant='dawn', light='divine', chars=[H('standing', 0.46, 1.4, 2.6, expression='moved')], cam=zoom(1.0, 1.07, [0.46, 0.36], 'push-in-fast'), music=0.5,
   transition='light-wipe', notes='Close: he accepts.'),
 # 12 he stayed, and listens
 S('s12', 12, RB, variant='dusk', light='dusk', narr=N(12), fx=[rays(0.8, 0.3, '#FFD9A0')], chars=[H('standing', 0.4, 0.84, 0.9, expression='calm')], text=tag('Chiranjeevi', 'चिरंजीवी', 'one who never died', 'जो कभी नहीं मरे'),
   cam=zoom(1.06, 1.0, move='slow-zoom-out'), cues=[cut('wherever', 'जहाँ', 's12b'), cut('Even', 'आज', 's12c')], sfx=[snd('wind-desolate', at=0, vol=0.3)], notes='The bank empty; he alone stays, looking where Rama went.'),
 S('s12b', 12, PN, variant='night', light='fire', fx=[glow(0.62, 0.66, 0.25, SAFF), stars(24)], props=[P('katha-circle', 0.62, 0.74, 1.1, 'still')], chars=[H('seated-listening', 0.24, 0.84, 0.8, expression='calm')],
   cam=zoom(1.0, 1.05, [0.4, 0.6]), sfx=[snd('night-crickets', at=0, vol=0.35)], notes='A storyteller and listeners by a lamp; at the edge of the light, Hanuman sits. Tradition, "it\'s said". MBh 3.147.39.'),
 S('s12c', 12, PN, variant='night', light='fire', fx=[glow(0.5, 0.5, 0.3, SAFF)], chars=[H('seated-listening', 0.48, 1.3, 2.4, expression='smile')], cam=zoom(1.0, 1.06, [0.48, 0.38]), music=1.1,
   sfx=[snd('temple-bells', at=0.2, vol=0.35)], transition='dissolve', notes='Close: eyes half closed, a small smile.'),
 # 13 tease: Bali
 S('s13', 13, PC, type='prop-hero', narr=N(13), overlay='folk-art-border', props=[P('three-steps', 0.5, 0.56, 1.5, 'still')], text=tag('Bali', 'बलि', 'next episode', 'अगली कड़ी'), cam=zoom(1.0, 1.06),
   sfx=[snd('drum-boom-deep', at=0, vol=0.6)], transition='cut-to-black', notes='A king\'s silhouette, a small figure with an umbrella, three glowing footprints. Bhagavata 8 (to research).'),
]

have = lambda kind, i: os.path.exists(f'{root}/assets/{kind}/{i}.svg')
poses, bgs, prs, ovs = {}, [], [], []
for s in scenes:
    for c in s['characters']: poses.setdefault(c['id'], {})[c['pose']] = 'library' if have(f"characters/{c['id']}", c['pose']) else 'new'
    if s['background'] not in bgs: bgs.append(s['background'])
    for p in s['props']:
        if p['id'] == 'seal-stamp': continue
        if p['id'] not in prs: prs.append(p['id'])
    if s.get('overlay') and s['overlay'] not in ovs: ovs.append(s['overlay'])
st = lambda kind, i: {'id': i, 'status': 'library' if have(kind, i) else 'new'}
TITLE = {'en': 'The One Who Asked to Live as Long as a Story', 'hi': 'जो तब तक जीएँगे, जब तक कथा रहेगी'}
doc = {
 'id': 'S03E01', 'title': TITLE,
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Valmiki Ramayana, Kishkindha & Uttara Kanda', 'hi': 'वाल्मीकि रामायण, किष्किंधा और उत्तर कांड'},
 'safeZone': {'bottom': 0.2, 'right': 0.12}, 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True}, 'sound': e03['sound'],
 'thumbnail': {'scene': 's01', 'at': 0.5, 'series': {'en': 'Chiranjeevi · Episode 1', 'hi': 'चिरंजीवी · भाग 1'},
   'title': TITLE, 'titleLines': {'en': ['Why Hanuman', 'Never Died'], 'hi': ['हनुमान', 'क्यों नहीं मरे?']}},
 'scenes': scenes,
 'assets': {'characters': [{'id': i, 'status': 'library' if all(v == 'library' for v in p.values()) else 'new', 'poses': p} for i, p in poses.items()],
            'backgrounds': [st('backgrounds', i) for i in bgs], 'props': [st('props', i) for i in prs] + [{'id': 'seal-stamp', 'status': 'library'}],
            'overlays': [st('overlays', i) for i in ovs]}}

# --- checks (same as S01E08) ---------------------------------------------------
errs, ids = [], [s['id'] for s in scenes]
assert len(ids) == len(set(ids))
clean = lambda t: [re.sub(r"[^\wऀ-ॣ०-ॿ]", '', w).lower() for w in t.split()]
norm = lambda w: w.lower().replace("'", '').replace('-', '')
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
                at = lambda c: [i for i, w in enumerate(full) if norm(c['onWord'][l]) in w][c.get('nth', {}).get(l, 1) - 1]
                a = at(next(c for c in cs if c['target'] == s['id'])); b = min([at(c) for c in cs if at(c) > a] + [len(full)])
                full = full[a:b]
            hits = [w for w in full if norm(r['onWord'][l]) in w]
            if len(hits) < r.get('nth', {}).get(l, 1): errs.append((s['id'], l, r['onWord'][l], 'not heard'))
            elif hits[r.get('nth', {}).get(l, 1) - 1] not in (norm(r['onWord'][l]), norm(r['onWord'][l]) + 's'): errs.append((s['id'], l, r['onWord'][l], f'matches inside "{hits[0]}"'))
        if r.get('do') == 'hard-cut-to':
            t = next((x for x in scenes if x['id'] == r['target']), None)
            if not t or t['beat'] != s['beat'] or any(t['narration'].values()): errs.append((s['id'], 'bad insert', r['target']))
    for el in s['characters'] + s['props']:
        if el['x'] > 0.88: errs.append((s['id'], 'x>0.88', el['id']))
for s in scenes:
    if s['beat'] and not any(s['narration'].values()) and not any(c.get('target') == s['id'] for x in scenes for c in x['cues']): errs.append((s['id'], 'never cut to'))
for b in range(1, 14):
    if b not in parent or parent[b]['narration'] != N(b): errs.append((b, 'narration not verbatim'))
print('errors:', errs)
json.dump(doc, open(f'{ep}/03-scenes.json', 'w'), ensure_ascii=False, indent=2); open(f'{ep}/03-scenes.json', 'a').write('\n')
print('scenes', len(scenes), '| new:', {k: [x['id'] + (':' + ','.join(p for p, v in x['poses'].items() if v == 'new') if 'poses' in x else '') for x in v if x['status'] == 'new'] for k, v in doc['assets'].items()})
