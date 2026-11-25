"""S01E07 scene spec. Narration is parsed from 02-script.md (never retyped).
Shots + the sting for 13 beats: shots inside a beat stay in one place (wide -> close), so the picture changes about every 3 s
without the story jumping. Close-ups are the same rigs at scale 2+ with the feet below the frame (y > 1).
Run:  python3 episodes/S01E07-parikshit-seven-days/svg/build-scenes.py <repo root>
"""
import json, os, re, sys
root = sys.argv[1]
ep = f'{root}/episodes/S01E07-parikshit-seven-days'
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
sting = {**sting, 'onScreenText': {**sting['onScreenText'], 'en': 'CURSED VII', 'hi': 'शाप VII'}}

FH, HM, HP = 'forest-hunt', 'hermitage', 'hastinapura-palace'  # library: feet 0.86 / 0.78 / 0.90
PT = 'pillar-tower'   # NEW: a small palace on one tall pillar, open sky; ground expected 0.84
TR = 'tower-room'     # NEW: inside it, a wide window with the sky; feet expected 0.86
BR = 'banyan-road'    # NEW: a road through open country, room for a banyan in the middle; feet expected 0.84
PC = 'parchment-card'
GOLD, FIRE, RED = '#E8B53A', '#E07A2E', '#C9463A'
dust = lambda n=15: {'type': 'dust', 'n': n}
embers = lambda n=20: {'type': 'embers', 'n': n}
stars = lambda n=30: {'type': 'stars', 'n': n}
rays = lambda x, y, c='#FFE6B0': {'type': 'rays', 'x': x, 'y': y, 'color': c}
glow = lambda x, y, r, c: {'type': 'glow', 'x': x, 'y': y, 'r': r, 'color': c, 'pulse': True}
card = dict(overlay='folk-art-border', type='prop-hero')

scenes = [sting,
 # 1 hook: he knows; the tower; his own hand
 S('s01', 1, TR, light='dusk', narr=N(1), chars=[C('parikshit', 'waiting', 0.48, 1.46, 2.7, action='still', expression='grave')], cam=zoom(1.0, 1.06, [0.5, 0.36]),
   text=tag('Parikshit', 'परीक्षित', 'king of Hastinapura', 'हस्तिनापुर के राजा'), cues=[cut('shut', 'हर', 's01b'), cut('Then', 'फिर', 's01c')], sfx=[snd('heartbeat', at=0.1, vol=0.5)], notes='Close: a good king who knows the day. CE 1.37.14.'),
 S('s01b', 1, PT, variant='dusk', light='dusk', type='prop-hero', fx=[embers(10)], cam=zoom(0.0, -0.05, move='crane-up'), sfx=[snd('drum-hit', at=0, vol=0.5)], notes='The house on one pillar. CE 1.38.28.'),
 S('s01c', 1, TR, variant='dusk', light='fire', chars=[C('parikshit', 'to-neck', 0.48, 1.46, 2.7, action='still', expression='laughing')], cam=zoom(1.0, 1.1, [0.5, 0.38], 'push-in-fast'), sfx=[snd('drum-boom-deep', at=0, vol=0.6)], transition='flash-white',
   notes='Hard cut: smiling, something tiny at his own neck. The end, shown first. CE 1.39.32.'),
 # 2 the deer
 S('s02', 2, FH, light='dawn', narr=N(2), fx=[dust(14)], chars=[C('parikshit', 'hunting', 0.3, 0.86, 1.0, action='step-forward', expression='tired')], props=[P('deer', 0.76, 0.72, 0.6, 'idle')], cam=zoom(0.0, 0.05, move='slow-pan-right'),
   text=tag('Parikshit', 'परीक्षित', "Arjuna's grandson", 'अर्जुन के पौत्र'), cues=[cut('lost', 'हिरण', 's02b')], sfx=[snd('bowstring-creak', at=0.2, vol=0.35)], notes='A good hunter follows his wounded deer. CE 1.36.11-14.'),
 S('s02b', 2, FH, variant='dusk', light='dusk', chars=[C('parikshit', 'hunting', 0.48, 1.44, 2.6, action='still', expression='tired')], cam=zoom(1.0, 1.05, [0.5, 0.36]), sfx=[snd('wind-desolate', at=0, vol=0.3)], transition='dissolve', notes='Close: the deer is gone; he is spent.'),
 # 3 the silent sage
 S('s03', 3, HM, light='dawn', narr=N(3), fx=[dust(10)], chars=[C('shamika', 'seated-silent', 0.68, 0.8, 0.95, flip=True, action='still', expression='calm'), C('parikshit', 'asking', 0.25, 0.8, 0.95, expression='tired')],
   cues=[cut('who', 'मौन', 's03b')], sfx=[snd('wind-desolate', at=0, vol=0.25)], notes='He asks for his deer (not for water). CE 1.36.15-17.'),
 S('s03b', 3, HM, light='dawn', chars=[C('shamika', 'seated-silent', 0.52, 1.2, 2.5, flip=True, action='still', expression='calm')], cam=zoom(1.0, 1.05, [0.5, 0.4]), text=tag('Shamika', 'शमीक', 'a vow of silence', 'मौन व्रत'), music=0.5, transition='dissolve', notes='Close: eyes open, lips closed, unmoving. CE 1.36.18.'),
 # 4 the dead snake
 S('s04', 4, HM, light='fire', narr=N(4), chars=[C('parikshit', 'furious', 0.48, 1.46, 2.7, action='still', expression='furious')], cam=zoom(1.0, 1.08, [0.5, 0.36], 'push-in-fast'),
   cues=[cut('laid', 'ऋषि', 's04b')], sfx=[snd('drum-hit', at=0, vol=0.5)], notes='Close: the one bad moment.'),
 S('s04b', 4, HM, light='dusk', chars=[C('shamika', 'with-snake', 0.66, 0.96, 1.5, flip=True, action='still', expression='calm')], props=[P('bow-dead-snake', 0.24, 0.5, 1.1, 'still')], cam=zoom(1.0, 1.06, [0.6, 0.45]),
   sfx=[snd('drum-boom-deep', 'snake', 'साँप', vol=0.6)], music=0.5, transition='dissolve', notes='The tip of his bow, the limp snake, the shoulder. The sage does not move. CE 1.36.18-19.'),
 # 5 the curse
 S('s05', 5, HM, variant='dusk', light='dusk', narr=N(5), chars=[C('shamika', 'with-snake', 0.5, 1.2, 2.5, flip=True, action='still', expression='calm')], cam=zoom(1.0, 1.05, [0.5, 0.4]),
   cues=[cut('young', 'छोटे', 's05b'), cut('Takshaka', 'सात', 's05c')], sfx=[snd('temple-bells', at=0.1, vol=0.3)], music=0.6, notes='No anger in him. CE 1.36.19, 1.38.18.'),
 S('s05b', 5, HM, variant='dusk', light='dusk', chars=[C('shamika', 'with-snake', 0.72, 0.8, 0.95, flip=True, action='still', expression='calm'), C('shringi', 'grief', 0.3, 0.8, 0.85, expression='grief')], text=tag('Shringi', 'शृंगी', 'his son', 'ऋषि के पुत्र'),
   sfx=[snd('heartbeat', at=0, vol=0.5)], notes='The boy sees his father. CE 1.37.16-17.'),
 S('s05c', 5, HM, variant='night', light='fire', fx=[{'type': 'sparks', 'n': 16}], chars=[C('shringi', 'cursing', 0.48, 1.24, 2.0, action='raise-hand', expression='furious', speaking=True)], props=[P('shaap-stamp', 0.5, 0.3, 0.7, 'stamp-in')], text=stamp('CURSED', 'शाप'),
   cues=[{'onWord': W('lord', 'नागराज'), 'do': 'stamp-next', 'target': 'shaap-stamp'}], cam=zoom(1.0, 1.06, [0.5, 0.45], 'shake-then-zoom'), sfx=[snd('thunder-crack', at=0, vol=0.5), snd('stamp-thud', 'lord', 'नागराज', vol=0.8, off=0.1)], music=1.1, transition='dissolve',
   notes='Water in his palm, the words out. CE 1.37.11-14.'),
 # 6 it can't be unsaid
 S('s06', 6, HM, variant='dusk', light='moon', narr=N(6), chars=[C('shamika', 'gentle', 0.5, 1.46, 2.6, action='still', expression='sad', speaking=True)], cam=zoom(1.0, 1.05, [0.5, 0.36]), text=None,
   cues=[cut('But', 'पर', 's06b')], music=0.5, notes='He takes the king\'s side. CE 1.37.20-27.'),
 S('s06b', 6, HM, variant='night', light='moon', chars=[C('shamika', 'gentle', 0.3, 0.8, 1.0, action='still', expression='sad'), C('shringi', 'grief', 0.64, 0.8, 0.85, flip=True, expression='grief')], sfx=[snd('glass-crack', 'unsaid', 'वापस', vol=0.35)], transition='dissolve', notes='Father and son; the curse stands. CE 1.38.1-3.'),
 # 7 the tower
 S('s07', 7, HP, light='dusk', narr=N(7), chars=[C('parikshit', 'regret', 0.48, 1.46, 2.6, action='still', expression='grief')], cam=zoom(1.0, 1.05, [0.5, 0.36]), cues=[cut('shut', 'एक', 's07b'), cut('ringed', 'पहरे', 's07c')], music=0.6,
   sfx=[snd('gong-soft', at=0, vol=0.4)], notes='He grieves more for the act than for his death. CE 1.38.22-25.'),
 S('s07b', 7, PT, light='dawn', type='prop-hero', cam=zoom(0.05, -0.04, move='crane-up'), sfx=[snd('drum-hit', at=0, vol=0.5)], notes='One pillar. CE 1.38.28.'),
 S('s07c', 7, PT, variant='night', light='night', fx=[stars(30)], chars=[C('guard', 'pointing', 0.22, 0.86, 0.75, action='still'), C('guard', 'pointing', 0.78, 0.86, 0.75, flip=True, action='still', variant='b')], props=[P('mantra-ring', 0.5, 0.36, 1.2, 'idle', light='none'), P('torch', 0.36, 0.76, 0.5, 'flicker-distant')], cam=zoom(1.0, 1.06),
   sfx=[snd('night-crickets', at=0, vol=0.4)], notes='Guards, healers, mantras all round. CE 1.38.29.'),
 # 8 the healer and the gold
 S('s08', 8, BR, light='dawn', narr=N(8), fx=[dust(10)], chars=[C('kashyapa', 'walking', 0.3, 0.84, 1.0, action='step-forward', expression='calm')], cam=zoom(0.0, 0.04, move='slow-pan-right'), text=tag('Kashyapa', 'काश्यप', 'the healer', 'वैद्य'),
   cues=[cut('cure', 'जो', 's08b'), cut('Takshaka', 'तक्षक', 's08c'), cut('turn', 'लौटा', 's08d')], sfx=[snd('drum-hit', 'seventh', 'सातवें', vol=0.5)], notes='The seventh day. CE 1.38.31-33.'),
 S('s08b', 8, BR, light='divine', fx=[{'type': 'sparks', 'n': 18}], chars=[C('kashyapa', 'reviving', 0.24, 0.84, 1.0, action='still', expression='calm')], props=[P('banyan-reviving', 0.62, 0.56, 1.4, 'idle')], cam=zoom(1.0, 1.05), sfx=[snd('shimmer-descend', at=0, vol=0.5)], transition='dissolve', notes='One picture of the test: the side Takshaka burnt is ash; the healer brings it back, leaf by leaf. CE 1.39.4-10.'),
 S('s08c', 8, BR, variant='dusk', light='dusk', chars=[C('old-brahmin', 'offering-gold', 0.3, 0.84, 1.0, action='still'), C('kashyapa', 'reviving', 0.72, 0.84, 1.0, flip=True, action='still', expression='calm')], props=[P('coins', 0.5, 0.56, 0.45, 'glint'), P('snake-shadow', 0.3, 0.86, 0.9, 'sway')], cam=zoom(1.0, 1.05),
   sfx=[snd('coins-spill', 'paid', 'धन', vol=0.6)], notes='Takshaka as an old Brahmin; the shadow tells. CE 1.39.13-17.'),
 S('s08d', 8, BR, variant='dusk', light='dusk', chars=[C('kashyapa', 'walking', 0.3, 0.84, 0.8, flip=True, action='walk-left', expression='calm')], cam=zoom(1.0, 0.96, move='slow-zoom-out'), music=0.5, transition='fade-to-night', notes='He goes home. (He also saw the king\'s time was over: 1.39.19.)'),
 # 9 the fruit
 S('s09', 9, BR, variant='night', light='night', narr=N(9), chars=[C('takshaka', 'rearing', 0.46, 1.04, 1.7, shadow=False, action='still')], cam=zoom(1.0, 1.06, [0.5, 0.4]), cues=[cut('worm', 'कीड़ा', 's09b'), cut('sent', 'भेंट', 's09c')], sfx=[snd('wind-desolate', at=0, vol=0.4)], notes='The lord of snakes, lotus-red. CE 1.40.3.'),
 S('s09b', 9, PC, props=[P('fruit-worm', 0.5, 0.46, 1.3, 'still')], cam=zoom(1.0, 1.08, [0.5, 0.46], 'push-in-fast'), sfx=[snd('drum-hit', at=0, vol=0.5)], notes='A copper speck with black eyes, in a fruit. CE 1.39.29.', **card),
 S('s09c', 9, PT, variant='dusk', light='dusk', type='prop-hero', props=[P('fruit-bearers', 0.5, 0.72, 1.1, 'idle')], cam=zoom(1.0, 1.05), sfx=[snd('heartbeat', at=0, vol=0.4)], notes='Ascetics with fruit; their shadows are snakes. CE 1.39.23-25.'),
 # 10 the laugh
 S('s10', 10, PT, variant='dusk', light='dusk', narr=N(10), type='prop-hero', fx=[glow(0.5, 0.62, 0.25, FIRE)], cam=zoom(1.0, 1.08, [0.5, 0.45]), cues=[cut("I'm", 'राजा', 's10b'), cut('Let', 'ये', 's10c')], sfx=[snd('gong-soft', at=0, vol=0.5)], music=0.6, notes='The last sunset behind the tower.'),
 S('s10b', 10, TR, variant='dusk', light='fire', chars=[C('parikshit', 'laughing', 0.46, 1.46, 2.6, action='still', expression='laughing', speaking=True)], props=[], cam=zoom(1.0, 1.06, [0.5, 0.36]), transition='dissolve', notes='Relief: he thinks he has won. CE 1.39.30.'),
 S('s10c', 10, TR, variant='dusk', light='fire', chars=[C('parikshit', 'worm-raised', 0.44, 1.46, 2.6, action='still', expression='laughing', speaking=True)], cam=zoom(1.0, 1.08, [0.55, 0.36], 'push-in-fast'), sfx=[snd('heartbeat', 'curse', 'शाप', vol=0.6)], music=0.5, transition='dissolve',
   notes='The worm on his fingertip, at eye level. Thumbnail. CE 1.39.30-31.'),
 # 11 Takshaka
 S('s11', 11, TR, variant='dusk', light='fire', narr=N(11), chars=[C('parikshit', 'to-neck', 0.48, 1.46, 2.7, action='still', expression='laughing')], cam=zoom(1.0, 1.06, [0.5, 0.38]), cues=[cut('It', 'वो', 's11b', nth={'en': 2})], sfx=[snd('heartbeat', at=0, vol=0.6)], music=0.3, notes='The hook again. CE 1.39.32.'),
 S('s11b', 11, TR, variant='night', light='night', fx=[embers(16)], chars=[C('parikshit', 'shocked', 0.5, 0.88, 1.05, action='still', expression='shocked'), C('takshaka', 'rearing', 0.24, 0.9, 1.25, shadow=False, action='still')], props=[P('takshaka-coils-back', 0.5, 0.86, 1.3, 'still'), P('takshaka-coils-front', 0.5, 0.87, 1.3, 'still')], cam=zoom(1.0, 1.08, [0.5, 0.5], 'shake-then-zoom'),
   sfx=[snd('thunder-crack', at=0, vol=0.6)], music=1.2, transition='flash-white', notes='The coils close round him. No bite shown; the burning house (1.40.4) is left out. CE 1.39.33.'),
 # 12 the two snakes
 S('s12', 12, HM, variant='dusk', light='dusk', narr=N(12), type='prop-hero', props=[P('bow-dead-snake', 0.5, 0.48, 1.9, 'still')], cam=zoom(1.0, 1.06, [0.5, 0.46]), cues=[cut('living', 'ज़िंदा', 's12b')], music=0.5, sfx=[snd('temple-bells', at=0.1, vol=0.3)], notes='The same gesture, first...'),
 S('s12b', 12, TR, variant='dusk', light='fire', type='prop-hero', props=[P('worm-fingertip', 0.5, 0.48, 1.9, 'still')], cam=zoom(1.0, 1.08, [0.5, 0.46]), music=0.4, notes='...and last.'),
 # 13 tease E08
 S('s13', 13, 'red-sky-plain', variant='dusk', light='dusk', narr=N(13), type='prop-hero', fx=[embers(16)], props=[P('gandhari-silhouette', 0.46, 0.56, 1.6, 'still'), P('shaap-stamp', 0.5, 0.29, 0.7, 'stamp-in')],
   text=stamp('CURSED VIII', 'शाप VIII'), cues=[{'onWord': W('cursed', 'शाप'), 'do': 'stamp-next', 'target': 'shaap-stamp'}], cam=zoom(1.0, 1.08), sfx=[snd('drum-hit', 'cursed', 'शाप', vol=0.8)], overlay='folk-art-border', transition='cut-to-black', notes='Tease for E08: a blindfolded queen; a peacock feather.'),
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
 'id': 'S01E07', 'title': {'en': 'The King With Seven Days to Live', 'hi': 'राजा, जिसके पास सात दिन थे'},
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Mahabharata, Adi Parva', 'hi': 'महाभारत, आदि पर्व'},
 'safeZone': {'bottom': 0.2, 'right': 0.12}, 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True}, 'sound': e03['sound'],
 'thumbnail': {'scene': 's10c', 'at': 0.5, 'series': {'en': 'Shraap · Episode 7', 'hi': 'शाप · भाग 7'},
   'title': {'en': 'The King With Seven Days to Live', 'hi': 'राजा, जिसके पास सात दिन थे'}, 'titleLines': {'en': ['Seven Days', 'to Live'], 'hi': ['सात दिन में', 'मौत']}},
 'scenes': scenes,
 'assets': {'characters': [{'id': i, 'status': 'library' if all(v == 'library' for v in p.values()) else 'new', 'poses': p} for i, p in poses.items()],
            'backgrounds': [st('backgrounds', i) for i in bgs], 'props': [st('props', i) for i in prs],
            'overlays': [st('overlays', i) for i in ovs + ['shaap-stamp']]}}

# --- checks -----------------------------------------------------------------
errs, ids = [], [s['id'] for s in scenes]
assert len(ids) == len(set(ids))
clean = lambda t: [re.sub(r"[^\wऀ-ॣ०-ॿ]", '', w).lower() for w in t.split()]
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
            elif hits[r.get('nth', {}).get(l, 1) - 1] not in (r['onWord'][l].lower().replace("'", ''), r['onWord'][l].lower() + 's'): errs.append((s['id'], l, r['onWord'][l], f'matches inside "{hits[0]}"'))
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
