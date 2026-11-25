"""S01E06 scene spec. Narration is parsed from 02-script.md (never retyped).
30 shots + the sting for 15 beats: shots inside a beat stay in one place (wide -> close), so the picture changes about every 3 s
without the story jumping. Close-ups are the same rigs at scale 2+ with the feet below the frame (y > 1).
Run:  python3 episodes/S01E06-nahusha-becomes-a-snake/svg/build-scenes.py <repo root>
"""
import json, os, re, sys
root = sys.argv[1]
ep = f'{root}/episodes/S01E06-nahusha-becomes-a-snake'
src = open(f'{ep}/02-script.md').read()

def beats(section):
    out = {}
    for line in section.split('\n'):
        m = re.match(r'^\| (\d+)[^|]*\| (.*?) \|', line)
        if m: out[int(m.group(1))] = m.group(2).strip()
    return out
EN = beats(src.split('## English')[1].split('**Ready cuts')[0])
HI = beats(src.split('## हिंदी')[1].split('**Ready cuts')[0])
assert len(EN) == 15 and len(HI) == 15, (len(EN), len(HI))
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
sting = {**sting, 'onScreenText': {**sting['onScreenText'], 'en': 'CURSED VI', 'hi': 'शाप VI'}}

SB = 'indra-sabha'         # NEW: Indra's hall on the clouds, its throne in the middle; feet expected 0.86, seat base expected 0.60
SK = 'heaven-sky'          # NEW: the sky road of heaven, clouds and stars; no ground
GG = 'himalaya-gorge'      # NEW: a Himalayan gorge with a cave mouth; feet expected 0.84
PC = 'parchment-card'
BLUE, GOLD, FIRE = '#9FD3E6', '#E8B53A', '#E07A2E'  # the snake is always on the left of the gorge, Yudhishthira on the right
dust = lambda n=15: {'type': 'dust', 'n': n}
embers = lambda n=20: {'type': 'embers', 'n': n}
stars = lambda n=30: {'type': 'stars', 'n': n}
rays = lambda x, y, c='#FFE6B0': {'type': 'rays', 'x': x, 'y': y, 'color': c}
glow = lambda x, y, r, c: {'type': 'glow', 'x': x, 'y': y, 'r': r, 'color': c, 'pulse': True}
card = dict(overlay='folk-art-border', type='prop-hero')

scenes = [sting,
 # 1 hook
 S('s01', 1, SB, light='divine', narr=N(1), fx=[rays(0.5, 0.25), {'type': 'sparks', 'n': 14}],
   chars=[C('nahusha', 'seated-throne', 0.5, 0.6, 0.9, action='still', expression='proud')], cam=zoom(1.0, 1.1, [0.5, 0.45], 'push-in-fast'),
   text=tag('Nahusha', 'नहुष', 'a human king', 'एक मनुष्य राजा'), cues=[cut('became', 'वो', 's01b')], sfx=[snd('gong-soft', at=0.1, vol=0.6)],
   notes='A human king on the throne of heaven. CE 5.11.'),
 S('s01b', 1, GG, variant='dusk', light='dusk', type='prop-hero', fx=[{'type': 'fog', 'color': '#9FB3D9'}], props=[P('great-snake', 0.5, 0.56, 1.5, 'sway')], cam=zoom(1.0, 1.12, [0.5, 0.5], 'shake-then-zoom'),
   sfx=[snd('drum-boom-deep', at=0, vol=0.65)], transition='flash-white', notes='Hard cut: the same being as a great coiled snake (spotted, turmeric-yellow, red eyes, no hood: 3.175.13-14).'),
 # 2 trailer: three cards
 S('s02', 2, PC, narr=N(2), props=[P('throne-icon', 0.5, 0.46, 1.25, 'still')], cam=zoom(1.0, 1.05), cues=[cut('palanquin', 'पालकी', 's02b'), cut('riddle', 'एक', 's02c', nth={'hi': 3})],
   sfx=[snd('drum-hit', at=0.1, vol=0.5)], notes='Trailer 1/3: the throne.', **card),
 S('s02b', 2, PC, props=[P('palanquin-icon', 0.5, 0.46, 1.25, 'still')], cam=zoom(1.0, 1.05), sfx=[snd('drum-hit', at=0, vol=0.5)], notes='Trailer 2/3: the empty palanquin.', **card),
 S('s02c', 2, PC, props=[P('snake-eye', 0.5, 0.46, 1.3, 'still')], cam=zoom(1.0, 1.08, [0.5, 0.46], 'push-in-fast'), sfx=[snd('drum-hit', at=0, vol=0.6)], transition='flash-white', notes='Trailer 3/3, the riddle: a great red eye.', **card),
 # 3 too weak
 S('s03', 3, SB, light='dawn', narr=N(3), fx=[dust(12)],
   chars=[C('nahusha', 'humble', 0.27, 0.86, 1.05, expression='humble', speaking=True), C('deva', 'offering', 0.74, 0.86, 1.15, flip=True, expression='pleading')],
   text=tag('Nahusha', 'नहुष', 'king on earth', 'धरती के राजा'), cues=[cut("I'm", 'मैं', 's03b')], sfx=[snd('wind-desolate', at=0, vol=0.25)],
   notes='The throne stands empty behind them; a god offers it to a plain king. CE 5.10.46-5.11.3.'),
 S('s03b', 3, SB, light='dawn', chars=[C('nahusha', 'humble', 0.46, 1.5, 2.9, action='still', expression='humble', speaking=True)], cam=zoom(1.0, 1.05, [0.5, 0.4]),
   transition='dissolve', notes='Close: the line that returns at the end.'),
 # 4 the power
 S('s04', 4, SB, light='divine', narr=N(4), fx=[glow(0.5, 0.36, 0.2, GOLD), {'type': 'sparks', 'n': 12}],
   chars=[C('nahusha', 'gaze', 0.46, 1.5, 2.9, action='still', expression='proud')], cam=zoom(1.0, 1.1, [0.52, 0.36], 'push-in-fast'), cues=[cut('took', 'उसका', 's04b')],
   sfx=[snd('shimmer-descend', 'power', 'शक्ति', vol=0.6)], notes='Close: his eyes light up. CE 5.11.6.'),
 S('s04b', 4, SB, light='dusk', chars=[C('nahusha', 'gaze', 0.24, 0.86, 1.0, action='still', expression='proud'), C('deva', 'drained', 0.74, 0.86, 1.12, flip=True, action='still', expression='weak')],
   props=[P('strength-stream', 0.5, 0.5, 0.95, 'idle', light='none')], cam=zoom(1.0, 1.05), sfx=[snd('glass-crack', at=0.2, vol=0.4)], transition='dissolve', notes='The god sags; a stream of light runs from him to the king\'s eyes.'),
 # 5 Shachi
 S('s05', 5, SB, light='fire', narr=N(5), fx=[embers(14)], chars=[C('nahusha', 'seated-throne', 0.5, 0.6, 0.9, action='point', expression='proud')], cam=zoom(1.32, 1.42, [0.5, 0.42]),
   cues=[cut("Indra", 'इन्द्र', 's05b')], sfx=[snd('drum-hit', 'demanded', 'रोकता', vol=0.5)], notes='Splendid, pointing. CE 5.11.13-15.'),
 S('s05b', 5, SB, light='dusk', chars=[C('shachi', 'standing-firm', 0.5, 1.12, 2.0, action='still', expression='firm')], cam=zoom(1.0, 1.05, [0.5, 0.45]), text=tag('Shachi', 'शची', 'queen of Indra', 'इन्द्र की रानी'),
   sfx=[snd('heartbeat', at=0, vol=0.5)], music=0.7, transition='dissolve', notes='Composed, unafraid.'),
 # 6 the trap
 S('s06', 6, SB, variant='night', light='moon', narr=N(6), fx=[stars(25)], chars=[C('shachi', 'standing-firm', 0.3, 0.86, 1.0, action='still', expression='firm')],
   props=[P('indra-in-lotus', 0.72, 0.56, 0.85, 'idle')], cues=[cut('Come', 'ऋषियों', 's06b')], sfx=[snd('shimmer-descend', at=0, vol=0.35)], music=0.6,
   notes='Indra, hidden in a lotus stem, gives her the plan (5.15.1-4): he is only a glowing silhouette.'),
 S('s06b', 6, SB, variant='dusk', light='dusk', chars=[C('shachi', 'speaking', 0.5, 1.28, 2.6, action='still', expression='calm', speaking=True)], cam=zoom(1.0, 1.06, [0.5, 0.36]),
   sfx=[snd('heartbeat', at=0, vol=0.4)], transition='dissolve', notes='Close: she says it. Strategy, not flirtation.'),
 # 7 the palanquin and the foot
 S('s07', 7, SK, variant='dusk', light='dusk', narr=N(7), type='prop-hero', fx=[stars(30)], props=[P('palanquin-carried', 0.5, 0.52, 1.12, 'idle')], cam=zoom(0.0, 0.04, move='slow-pan-right'),
   cues=[cut('set', 'अगस्त्य', 's07b')], sfx=[snd('drum-hit', at=0.2, vol=0.5)], music=1.1, notes='Four sages carry him along the sky road. CE 5.15.20-21, 5.17.8.'),
 S('s07b', 7, SK, variant='dusk', light='fire', type='prop-hero', props=[P('foot-on-head', 0.5, 0.5, 1.82, 'still')], cam=zoom(1.0, 1.1, [0.5, 0.5], 'push-in-fast'), text=tag('Agastya', 'अगस्त्य'),
   sfx=[snd('drum-boom-deep', 'foot', 'पैर', vol=0.65)], music=0.5, transition='flash-white', notes='Close: a jewelled foot on a sage\'s matted hair. CE 5.17.11 (a touch, not a kick).'),
 # 8 the curse
 S('s08', 8, SK, variant='night', light='fire', narr=N(8), fx=[{'type': 'sparks', 'n': 16}], chars=[C('agastya', 'cursing', 0.5, 1.12, 1.6, flip=True, action='raise-hand', expression='furious', speaking=True)],
   props=[P('shaap-stamp', 0.5, 0.3, 0.7, 'stamp-in')], text=stamp('CURSED', 'शाप'), cam=zoom(1.0, 1.06, [0.5, 0.45], 'shake-then-zoom'),
   cues=[{'onWord': W('cursed', 'शाप'), 'do': 'stamp-next', 'target': 'shaap-stamp'}, cut('Fall', 'स्वर्ग', 's08b')],
   sfx=[snd('thunder-crack', 'cursed', 'शाप', vol=0.6), snd('stamp-thud', 'cursed', 'शाप', vol=0.8, off=0.1)], music=1.1, notes='CE 5.17.12-15.'),
 S('s08b', 8, SK, variant='night', light='night', type='prop-hero', fx=[stars(30)], props=[P('nahusha-falling', 0.46, 0.4, 1.8, 'plunge')], cam=zoom(1.0, 1.05), sfx=[snd('wind-desolate', at=0, vol=0.5)],
   transition='dissolve', notes='He falls head down, crown coming off, legs already coils (3.178.38).'),
 # 9 pity
 S('s09', 9, SK, variant='night', light='moon', narr=N(9), fx=[stars(30)], chars=[C('agastya', 'softening', 0.46, 1.48, 2.5, flip=True, action='still', expression='kind', speaking=True)], cam=zoom(1.0, 1.06, [0.5, 0.36]),
   sfx=[snd('temple-bells', 'Yudhishthira', 'युधिष्ठिर', vol=0.5)], music=0.6, transition='fade-to-night', notes='Close: his anger goes. CE 3.178.39-40.'),
 # 10 Bhima
 S('s10', 10, GG, light='dawn', narr=N(10), fx=[{'type': 'fog', 'color': '#C9D6E0'}], chars=[C('bhima', 'held', 0.5, 0.84, 1.0, flip=True, action='still', expression='strain')],
   props=[P('coils-back', 0.5, 0.835, 1.25, 'still'), P('coils-front', 0.5, 0.845, 1.25, 'still'), P('snake-head', 0.2, 0.7, 0.75, 'idle')], text=tag('Bhima', 'भीम', 'the strongest Pandava', 'सबसे बलवान पाण्डव'), cues=[cut('took', 'बल', 's10b')],
   sfx=[snd('drum-boom-deep', 'seized', 'जकड़कर', vol=0.6)], cam=zoom(1.0, 1.06, [0.5, 0.55], 'shake-then-zoom'), notes='CE 3.175.16-21.'),
 S('s10b', 10, GG, light='dusk', chars=[C('bhima', 'held', 0.56, 1.46, 2.7, flip=True, action='still', expression='weak')], props=[P('strength-stream', 0.27, 0.475, 1.1, 'idle', light='none')], cam=zoom(1.0, 1.05, [0.5, 0.36]),
   sfx=[snd('glass-crack', at=0.1, vol=0.4)], music=0.6, transition='dissolve', notes='Close: the same light leaves him as left the god in s04b. CE 3.176.22.'),
 # 11 the riddle
 S('s11', 11, GG, variant='dusk', light='dusk', narr=N(11), chars=[C('bhima', 'held', 0.72, 0.84, 0.9, flip=True, action='still', expression='weak')],
   props=[P('coils-back', 0.72, 0.835, 1.1, 'still'), P('coils-front', 0.72, 0.845, 1.1, 'still'), P('snake-head', 0.28, 0.72, 1.0, 'idle')], cues=[cut('Then', 'तभी', 's11b'), cut('Answer', 'उत्तर', 's11c')],
   sfx=[snd('heartbeat', at=0.1, vol=0.5)], music=0.7, notes='The great head comes level with Bhima. CE 3.176.13-16.'),
 S('s11b', 11, GG, variant='dusk', light='dusk', chars=[C('yudhishthira', 'arriving', 0.72, 0.84, 1.0, flip=True, action='step-forward', expression='alarmed')], props=[P('snake-head', 0.26, 0.74, 1.0, 'idle')],
   text=tag('Yudhishthira', 'युधिष्ठिर'), sfx=[snd('gong-soft', at=0, vol=0.5)], notes='CE 3.176.51-3.177.5.'),
 S('s11c', 11, GG, variant='night', light='night', type='prop-hero', props=[P('snake-head', 0.44, 0.93, 1.8, 'idle')], cam=zoom(1.0, 1.06, [0.5, 0.45]), sfx=[snd('drum-hit', at=0, vol=0.5)], music=0.6, transition='dissolve', notes='Close: it asks. CE 3.177.12, 15.'),
 # 12 the answer
 S('s12', 12, GG, light='dawn', narr=N(12), fx=[dust(8)], chars=[C('yudhishthira', 'answering', 0.54, 1.44, 2.8, flip=True, action='still', expression='calm', speaking=True)], cam=zoom(1.0, 1.06, [0.5, 0.36]),
   cues=[cut('conduct', 'आचरण', 's12b')], sfx=[snd('temple-bells', 'compassion', 'दया', vol=0.35)], music=0.6, notes='Close, quiet. CE 3.177.16.'),
 S('s12b', 12, GG, light='dawn', fx=[rays(0.7, 0.2)], chars=[C('yudhishthira', 'answering', 0.74, 0.84, 1.0, flip=True, expression='calm', speaking=True)], props=[P('snake-head', 0.26, 0.74, 1.0, 'idle')], cam=zoom(1.0, 1.05),
   transition='dissolve', notes='Wide: the two face each other as equals. CE 3.177.20-21.'),
 # 13 the curse breaks
 S('s13', 13, GG, variant='dusk', light='dusk', narr=N(13), type='prop-hero', props=[P('snake-eye-throne', 0.5, 0.5, 1.0, 'still')], cam=zoom(1.0, 1.08, [0.5, 0.46]), cues=[cut('curse', 'शाप', 's13b')], sfx=[snd('heartbeat', at=0.1, vol=0.4)], music=0.5,
   notes='The throne reflected in its eye. CE 3.178.30.'),
 S('s13b', 13, GG, light='divine', fx=[glow(0.36, 0.5, 0.3, GOLD), {'type': 'sparks', 'n': 20}], chars=[C('bhima', 'freed', 0.74, 0.84, 1.0, flip=True, expression='awed')], props=[P('coils-of-light', 0.34, 0.58, 1.3, 'ascend')],
   cam=zoom(1.0, 1.06), sfx=[snd('shimmer-descend', at=0, vol=0.6), snd('glass-crack', at=0, vol=0.4)], transition='flash-white', notes='The coils turn to light; Bhima is free. CE 3.178.44-45.'),
 # 14 loop
 S('s14', 14, GG, light='divine', narr=N(14), fx=[rays(0.46, 0.2), {'type': 'sparks', 'n': 14}], chars=[C('nahusha', 'humble', 0.46, 1.5, 2.9, action='still', expression='serene')], cam=zoom(1.0, 1.05, [0.5, 0.38]),
   cues=[cut('rose', 'फिर', 's14b')], sfx=[snd('temple-bells', at=0.1, vol=0.5)], notes='The plain, modest king of beat 3 again, at peace.'),
 S('s14b', 14, SK, light='divine', fx=[rays(0.5, 0.2), stars(20), glow(0.5, 0.45, 0.25, GOLD)], chars=[C('nahusha', 'humble', 0.5, 0.74, 0.8, action='ascend', expression='serene')], cam=zoom(0.0, -0.05, move='crane-up'),
   sfx=[snd('shimmer-descend', at=0, vol=0.5)], transition='dissolve', notes='He rises to heaven.'),
 # 15 tease E07
 S('s15', 15, 'forest-hunt', variant='dusk', light='dusk', narr=N(15), type='prop-hero', fx=[embers(12), glow(0.5, 0.45, 0.3, FIRE)], props=[P('dead-snake-sage', 0.46, 0.55, 1.7, 'still'), P('shaap-stamp', 0.5, 0.29, 0.7, 'stamp-in')],
   text=stamp('CURSED VII', 'शाप VII'), cues=[{'onWord': W('king', 'राजा'), 'do': 'stamp-next', 'target': 'shaap-stamp'}], cam=zoom(1.0, 1.08), sfx=[snd('drum-hit', 'king', 'राजा', vol=0.8)],
   overlay='folk-art-border', transition='cut-to-black', notes='Tease for E07: a sage in silent meditation, a dead snake laid over his shoulders (CE 1.36.18).'),
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
 'id': 'S01E06', 'title': {'en': 'The King of Heaven Who Became a Snake', 'hi': 'स्वर्ग का राजा, जो साँप बना'},
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Mahabharata, Udyoga & Vana Parva', 'hi': 'महाभारत, उद्योग और वन पर्व'},
 'safeZone': {'bottom': 0.2, 'right': 0.12}, 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True}, 'sound': e03['sound'],
 'thumbnail': {'scene': 's01b', 'at': 0.5, 'series': {'en': 'Shraap · Episode 6', 'hi': 'शाप · भाग 6'},
   'title': {'en': 'The King of Heaven Who Became a Snake', 'hi': 'स्वर्ग का राजा, जो साँप बना'}, 'titleLines': {'en': ['The King', 'Who Became', 'a Snake'], 'hi': ['स्वर्ग का राजा', 'जो साँप बना']}},
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
                at = lambda c: [i for i, w in enumerate(full) if c['onWord'][l].lower().replace("'", '') in w][c.get('nth', {}).get(l, 1) - 1]
                a = at(next(c for c in cs if c['target'] == s['id'])); b = min([at(c) for c in cs if at(c) > a] + [len(full)])
                full = full[a:b]
            hits = [w for w in full if r['onWord'][l].lower().replace("'", '') in w]
            if len(hits) < r.get('nth', {}).get(l, 1): errs.append((s['id'], l, r['onWord'][l], 'not heard'))
            elif hits[0] != r['onWord'][l].lower().replace("'", ''): errs.append((s['id'], l, r['onWord'][l], f'matches inside "{hits[0]}"'))
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
