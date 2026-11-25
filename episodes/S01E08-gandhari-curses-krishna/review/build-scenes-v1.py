"""S01E08 scene spec. Narration is parsed from 02-script.md (never retyped).
Shots + the sting for 14 beats: shots inside a beat stay in one place (wide -> close), so the picture changes about every 3 s
without the story jumping. Close-ups are the same rigs at scale 2+ with the feet below the frame (y > 1).
Run:  python3 episodes/S01E08-gandhari-curses-krishna/svg/build-scenes.py <repo root>
"""
import json, os, re, sys
root = sys.argv[1]
ep = f'{root}/episodes/S01E08-gandhari-curses-krishna'
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
sting = {**sting, 'onScreenText': {**sting['onScreenText'], 'en': 'CURSED VIII', 'hi': 'शाप VIII'}}

KF, KC, SH, FH, HS = 'red-sky-plain', 'king-court', 'sea-shore', 'forest-hunt', 'heaven-sky'  # library: feet 0.81 / 0.88 / 0.84 / 0.86 / none
DV = 'dvaraka'        # NEW: a city of nagara towers by the sea, balcony in front; feet expected 0.86
PC = 'parchment-card'
GOLD, FIRE, RED = '#E8B53A', '#E07A2E', '#C9463A'
dust = lambda n=15: {'type': 'dust', 'n': n}
embers = lambda n=20: {'type': 'embers', 'n': n}
stars = lambda n=30: {'type': 'stars', 'n': n}
rays = lambda x, y, c='#FFE6B0': {'type': 'rays', 'x': x, 'y': y, 'color': c}
glow = lambda x, y, r, c: {'type': 'glow', 'x': x, 'y': y, 'r': r, 'color': c, 'pulse': True}
card = dict(overlay='folk-art-border', type='prop-hero')
# Axis: Gandhari is always on the left facing right, Krishna on the right facing left (flip), on the field.
G = lambda pose, x, y, sc, **kw: C('gandhari', pose, x, y, sc, action=kw.pop('action', 'still'), **kw)
K = lambda pose, x, y, sc, **kw: C('krishna', pose, x, y, sc, action=kw.pop('action', 'still'), **kw)

scenes = [sting,
 # 1 hook
 S('s01', 1, KF, light='fire', narr=N(1), fx=[embers(16)], chars=[G('cursing', 0.27, 1.16, 1.75, expression='furious'), K('standing', 0.71, 1.16, 1.75, flip=True, expression='calm')], cam=zoom(1.0, 1.06, [0.5, 0.36]),
   cues=[cut('smiled', 'वो', 's01b'), cut('made', 'उसे', 's01c')], sfx=[snd('thunder-crack', 'cursed', 'शाप', vol=0.5)], notes='A blindfolded queen, palm raised at Krishna. CE 11.25.39. Thumbnail.'),
 S('s01b', 1, KF, light='dusk', chars=[K('standing', 0.5, 1.4, 2.7, flip=True, expression='smile')], cam=zoom(1.0, 1.08, [0.5, 0.36], 'push-in-fast'), sfx=[snd('shimmer-descend', at=0, vol=0.4)], music=0.5, notes='The faint smile. CE 11.25.43.'),
 S('s01c', 1, SH, variant='night', light='silhouette', fx=[embers(14)], props=[P('clan-falling', 0.5, 0.72, 1.5, 'still'), P('dark-moon', 0.5, 0.26, 0.9, 'still')], cam=zoom(1.0, 1.06), sfx=[snd('drum-boom-deep', at=0, vol=0.6)], transition='flash-white', notes='It comes true: the end, shown first. CE 16.4.36-42.'),
 # 2 the war is over
 S('s02', 2, KF, variant='dusk', light='dusk', type='prop-hero', narr=N(2), fx=[embers(14)], props=[P('war-remains', 0.5, 0.74, 1.6, 'still'), P('vultures', 0.62, 0.26, 0.6, 'circle')], cam=zoom(0.0, 0.05, move='slow-pan-right'), cues=[cut('All', 'रानी', 's02b')], sfx=[snd('wind-desolate', at=0, vol=0.4)], music=0.6, notes='Broken wheels, banners, no bodies.'),
 S('s02b', 2, KF, variant='dusk', light='dusk', chars=[G('grief', 0.48, 1.4, 2.6, expression='grief')], props=[], cam=zoom(1.0, 1.06, [0.5, 0.38]), text=tag('Gandhari', 'गांधारी', 'mother of the Kauravas', 'कौरवों की माँ'), sfx=[snd('temple-bells', at=0.1, vol=0.3)], transition='dissolve', notes='She bound her own eyes for her blind husband (1.103.13). Hands empty.'),
 # 3 she spares the Pandavas
 S('s03', 3, KF, variant='dusk', light='dusk', narr=N(3), chars=[G('holding-back', 0.24, 0.84, 1.0, expression='grief'), C('yudhishthira', 'kneeling-bowed', 0.56, 0.84, 0.95, flip=True, action='still'), C('arjuna', 'bowing-eyes-closed', 0.8, 0.8, 0.85, flip=True, action='still')],
   cues=[cut('My', 'दोष', 's03b')], sfx=[snd('heartbeat', at=0, vol=0.45)], notes='The raised hand is held back by her own other hand. CE 11.13.2-15, 11.15.2-8.'),
 S('s03b', 3, KF, variant='dusk', light='dusk', chars=[G('holding-back', 0.5, 1.4, 2.6, expression='grief', speaking=True)], cam=zoom(1.0, 1.05, [0.5, 0.36]), music=0.5, notes='"Duryodhana..." CE 11.13.14.'),
 # 4 why did you look on?
 S('s04', 4, KF, light='fire', narr=N(4), fx=[embers(16)], props=[P('mourning-women', 0.62, 0.7, 1.3, 'still'), P('lamp-rows', 0.5, 0.86, 1.5, 'flicker-distant')], chars=[G('grief', 0.2, 0.84, 0.95, expression='grief')], cam=zoom(1.0, 1.05), cues=[cut('asked', 'वो', 's04b'), cut('Why', 'फिर', 's04c')], sfx=[snd('wind-desolate', at=0, vol=0.45)], notes='The widows among the lamps. CE 11.16.9-19.'),
 S('s04b', 4, KF, light='fire', fx=[embers(16)], chars=[G('accusing', 0.27, 1.1, 1.65, expression='anger', speaking=True), K('standing', 0.73, 1.1, 1.65, flip=True, expression='calm')], cam=zoom(1.0, 1.05, [0.5, 0.4]), sfx=[snd('drum-hit', at=0, vol=0.5)], notes='Open palm, not a pointing finger. CE 11.25.36-37.'),
 S('s04c', 4, KF, light='fire', chars=[G('accusing', 0.46, 1.4, 2.6, expression='grief', speaking=True)], cam=zoom(1.0, 1.08, [0.5, 0.36], 'push-in-fast'), music=0.4, sfx=[snd('heartbeat', at=0, vol=0.6)], notes='THE question of the episode: upeksitah, "looked on".'),
 # 5 he had tried
 S('s05', 5, KC, variant='dawn', light='dawn', narr=N(5), chars=[K('envoy', 0.28, 0.9, 1.1, expression='calm'), C('duryodhana', 'refusing', 0.72, 0.9, 1.1, flip=True, action='still')], overlay='sepia-folk-frame', cam=zoom(1.0, 1.05), cues=[cut('her', 'गांधारी', 's05b')], sfx=[snd('gong-soft', at=0, vol=0.4)], music=0.6, transition='memory-ripple', notes='Before the war: the envoy. CE 5.91, 5.93.'),
 S('s05b', 5, KC, variant='dawn', light='dawn', chars=[C('duryodhana', 'refusing', 0.5, 1.4, 2.6, flip=True, action='still')], overlay='sepia-folk-frame', text=tag('Duryodhana', 'दुर्योधन', "Gandhari's eldest son", 'गांधारी का बड़ा बेटा'), cam=zoom(1.0, 1.05, [0.5, 0.36]), sfx=[snd('drum-hit', at=0, vol=0.5)], transition='memory-ripple', notes='Proud, turned away.'),
 # 6 the curse
 S('s06', 6, KF, variant='night', light='fire', narr=N(6), fx=[{'type': 'sparks', 'n': 16}], chars=[G('cursing', 0.46, 1.16, 1.8, action='raise-hand', expression='furious', speaking=True)], props=[P('shaap-stamp', 0.5, 0.2, 0.7, 'stamp-in')], text=stamp('CURSED', 'शाप'),
   cues=[{'onWord': W('cursed', 'शाप'), 'do': 'stamp-next', 'target': 'shaap-stamp'}, cut("You'll", 'तुम', 's06b', nth={'hi': 2}), cut('thirty-sixth', 'छत्तीसवें', 's06c'), cut('meet', 'वन', 's06d')], cam=zoom(1.0, 1.06, [0.5, 0.45], 'shake-then-zoom'), sfx=[snd('thunder-crack', at=0, vol=0.5), snd('stamp-thud', 'cursed', 'शाप', vol=0.8, off=0.1)], music=1.1, notes='CE 11.25.38-40.'),
 S('s06b', 6, KF, variant='night', light='fire', fx=[{'type': 'sparks', 'n': 16}], chars=[G('cursing', 0.46, 1.4, 2.6, expression='furious', speaking=True)], cam=zoom(1.0, 1.1, [0.5, 0.36], 'push-in-fast'), sfx=[snd('drum-boom-deep', at=0, vol=0.6)], music=1.1, notes='Close: you will destroy yours.'),
 S('s06c', 6, SH, variant='night', light='silhouette', fx=[embers(12)], props=[P('dark-moon', 0.5, 0.26, 0.9, 'still'), P('clan-falling', 0.5, 0.72, 1.5, 'still')], cam=zoom(1.0, 1.05), sfx=[snd('glass-crack', at=0, vol=0.4)], transition='dissolve', notes='What she sees: his clan. CE 11.25.41.'),
 S('s06d', 6, FH, variant='night', light='silhouette', chars=[K('walking', 0.4, 0.86, 0.75, action='step-forward', expression='calm')], cam=zoom(1.06, 1.0, move='slow-zoom-out'), sfx=[snd('wind-desolate', at=0, vol=0.5)], transition='dissolve', notes='One figure among trees. CE 11.25.41 (vanecarah).'),
 # 7 I know
 S('s07', 7, KF, light='dusk', narr=N(7), chars=[K('standing', 0.5, 1.4, 2.6, flip=True, expression='smile', speaking=True)], cam=zoom(1.0, 1.06, [0.5, 0.36]), cues=[cut('Only', 'मेरे', 's07b')], sfx=[snd('shimmer-descend', at=0, vol=0.45)], music=0.4, notes='"As if slightly smiling." CE 11.25.43-44.'),
 S('s07b', 7, KF, light='dusk', chars=[K('standing', 0.46, 1.14, 1.75, flip=True, expression='smile', speaking=True), C('arjuna', 'bowing-eyes-closed', 0.8, 0.8, 0.7, flip=True, action='still')], cam=zoom(1.0, 1.06, [0.5, 0.4]), sfx=[snd('heartbeat', at=0, vol=0.45)], music=0.4, notes='The Pandavas, stricken, behind him. CE 11.25.46.'),
 # 8 thirty-six years
 S('s08', 8, DV, light='dawn', type='prop-hero', narr=N(8), fx=[dust(10)], cam=zoom(0.0, -0.05, move='crane-up'), text=tag('Dvaraka', 'द्वारका', "Krishna's city", 'कृष्ण की नगरी'), cues=[cut('omens', 'वाले', 's08b'), cut('Krishna', 'कृष्ण', 's08c')], sfx=[snd('temple-bells', at=0, vol=0.4)], notes='Thirty-six years of peace. CE 16.1.1.'),
 S('s08b', 8, DV, variant='night', light='night', type='prop-hero', fx=[embers(10)], props=[P('dark-moon', 0.5, 0.24, 1.0, 'still'), P('vultures', 0.4, 0.42, 0.6, 'circle')], cam=zoom(1.0, 1.06, [0.5, 0.3]), sfx=[snd('thunder-crack', at=0, vol=0.45)], transition='dissolve', notes='The moon gives the war\'s sign again. CE 16.3.16-18.'),
 S('s08c', 8, DV, variant='night', light='moon', chars=[K('standing', 0.6, 1.3, 2.2, flip=True, expression='grave')], props=[P('gandhari-silhouette', 0.22, 0.34, 0.75, 'still')], cam=zoom(1.0, 1.05, [0.5, 0.38]), sfx=[snd('gong-soft', at=0, vol=0.5)], music=0.5, notes='He remembers her. CE 16.3.19.'),
 # 9 to the seashore
 S('s09', 9, DV, variant='dusk', light='dusk', narr=N(9), chars=[K('standing', 0.5, 1.4, 2.6, flip=True, expression='calm')], cam=zoom(1.0, 1.05, [0.5, 0.36]), cues=[cut('led', 'अपने', 's09b')], music=0.5, sfx=[snd('heartbeat', at=0.1, vol=0.4)], notes='Able, and choosing. CE 16.9.26-27.'),
 S('s09b', 9, SH, variant='dusk', light='dusk', chars=[K('walking', 0.64, 0.86, 1.0, action='step-forward', expression='calm')], props=[P('clan-procession', 0.28, 0.76, 1.2, 'slide-right')], cam=zoom(0.0, 0.04, move='slow-pan-right'), sfx=[snd('drum-hit', at=0, vol=0.5)], transition='dissolve', notes='The pilgrimage he ordered "to make it true". CE 16.3.21-22.'),
 # 10 the clan
 S('s10', 10, SH, variant='dusk', light='silhouette', narr=N(10), props=[P('quarrel', 0.5, 0.64, 1.5, 'still')], cam=zoom(1.0, 1.06), cues=[cut('set', 'आपस', 's10b'), cut('Krishna', 'कृष्ण', 's10c')], sfx=[snd('battle-distant', at=0, vol=0.5)], notes='Satyaki and Kritavarma: the night raid thrown in the face. CE 16.4.16-27.'),
 S('s10b', 10, SH, variant='night', light='silhouette', fx=[embers(24)], props=[P('clan-falling', 0.5, 0.72, 1.6, 'still'), P('iron-grass', 0.5, 0.42, 0.9, 'glint')], cam=zoom(1.0, 1.08, [0.5, 0.6], 'shake-then-zoom'), sfx=[snd('drum-boom-deep', at=0, vol=0.6)], music=1.2, transition='flash-white', notes='Grass turns to iron (shown, not told). CE 16.4.34-39.'),
 S('s10c', 10, SH, variant='night', light='dusk', chars=[K('looking-on', 0.46, 1.1, 1.6, expression='grave')], props=[P('clan-falling', 0.5, 0.68, 0.9, 'still')], cam=zoom(1.0, 1.08, [0.48, 0.4]), sfx=[snd('heartbeat', at=0, vol=0.5)], music=0.4, notes='He stands, knowing the turn of time. CE 16.4.42. Still, sorrowful, upright.'),
 # 11 the forest
 S('s11', 11, FH, variant='dusk', light='dusk', narr=N(11), fx=[dust(10)], chars=[K('walking', 0.36, 0.86, 0.85, action='step-forward', expression='calm')], cam=zoom(1.0, 1.04), cues=[cut('lay', 'योग', 's11b'), cut('hunter', 'एक', 's11c'), cut('deer', 'समझकर', 's11d')], music=0.4, sfx=[snd('night-crickets', at=0, vol=0.4)], notes='The forest of E02, where Pandu took a sage for a deer. CE 16.5.16.'),
 S('s11b', 11, FH, variant='dusk', light='dusk', fx=[glow(0.5, 0.66, 0.3, GOLD)], chars=[K('reclining', 0.5, 0.86, 1.25, expression='asleep')], cam=zoom(1.0, 1.05, [0.5, 0.66]), sfx=[snd('temple-bells', at=0.1, vol=0.3)], music=0.4, transition='dissolve', notes='On the bare ground, in yoga. CE 16.5.16-19.'),
 S('s11c', 11, FH, variant='dusk', light='dusk', chars=[C('jara', 'drawing-bow', 0.42, 1.4, 2.5, action='still', expression='intent')], cam=zoom(1.0, 1.05, [0.5, 0.36]), sfx=[snd('bowstring-creak', at=0, vol=0.6)], notes='Close: a hunter at dusk.'),
 S('s11d', 11, FH, variant='night', light='dusk', chars=[C('jara', 'drawing-bow', 0.2, 0.86, 0.85, action='still', expression='intent')], props=[P('deer-shape-leaves', 0.7, 0.68, 0.9, 'still'), P('glowing-arrow', 0.4, 0.57, 0.5, 'fly-right')], cam=zoom(1.0, 1.04),
   cues=[{'onWord': W('shot', 'बाण'), 'do': 'fly', 'target': 'glowing-arrow'}], sfx=[snd('arrow-whoosh-magic', 'shot', 'बाण', vol=0.7)], transition='flash-white', notes='What he thinks he sees, through leaves. Only the arrow flies. CE 16.5.20.'),
 # 12 mercy
 S('s12', 12, FH, variant='dusk', light='divine', narr=N(12), fx=[glow(0.66, 0.6, 0.3, GOLD)], chars=[K('seated-blessing', 0.66, 0.86, 1.15, flip=True, expression='calm'), C('jara', 'prostrate', 0.28, 0.88, 1.0, action='still')], cam=zoom(1.0, 1.05), cues=[cut('Krishna', 'कृष्ण', 's12b'), cut('rose', 'और', 's12c')], sfx=[snd('drum-hit', at=0, vol=0.4)], notes='He sees whom he has struck. CE 16.5.20-21.'),
 S('s12b', 12, FH, variant='dusk', light='divine', fx=[glow(0.52, 0.4, 0.4, GOLD)], chars=[K('seated-blessing', 0.52, 1.18, 2.3, flip=True, expression='smile')], cam=zoom(1.0, 1.06, [0.5, 0.4]), sfx=[snd('shimmer-descend', at=0, vol=0.5)], music=0.5, transition='dissolve', notes='Close: comfort. The same faint smile. CE 16.5.21.'),
 S('s12c', 12, HS, variant='night', light='divine', fx=[rays(0.5, 0.45, '#FFE6B0'), stars(40)], chars=[K('rising', 0.5, 0.78, 1.2, action='ascend', expression='calm', shadow=False)], props=[P('rising-lights', 0.5, 0.5, 1.6, 'ascend')], cam=zoom(0.05, -0.05, move='crane-up'), sfx=[snd('shimmer-descend', at=0, vol=0.6), snd('gong-soft', at=0.2, vol=0.5)], music=1.2, transition='dissolve', notes='Filling earth and sky with light. CE 16.5.21-25.'),
 # 13 the season
 S('s13', 13, HS, variant='night', light='night', narr=N(13), type='prop-hero', fx=[stars(40)], props=[P('season-ring', 0.5, 0.44, 1.5, 'still')], overlay='folk-art-border', cam=zoom(1.0, 1.05, [0.5, 0.44]), cues=[cut('last', 'आख़िरी', 's13b')], sfx=[snd('temple-bells', at=0, vol=0.4)], music=0.7, transition='dissolve', notes='Eight emblems: stake, deer, bangles, river, wheel, snake, worm, blindfold.'),
 S('s13b', 13, HS, variant='night', light='night', type='prop-hero', fx=[stars(40), glow(0.5, 0.46, 0.35, GOLD)], props=[P('season-ring', 0.5, 0.44, 1.5, 'still'), P('peacock-feather', 0.5, 0.44, 0.9, 'descend')], overlay='folk-art-border', cam=zoom(1.05, 1.1, [0.5, 0.44]), sfx=[snd('shimmer-descend', at=0, vol=0.5)], music=0.6, notes='A peacock feather settles in the middle of the curses.'),
 # 14 Season 2
 S('s14', 14, KF, variant='night', light='night', type='prop-hero', narr=N(14), fx=[embers(16)], props=[P('war-remains', 0.5, 0.76, 1.5, 'still'), P('shaap-stamp', 0.5, 0.3, 0.7, 'stamp-in')], text=stamp('SEASON 2', 'सीज़न 2'),
   cues=[{'onWord': W('season', 'सीज़न'), 'do': 'stamp-next', 'target': 'shaap-stamp'}, cut('Ashwatthama', 'अश्वत्थामा', 's14b')], overlay='folk-art-border', sfx=[snd('stamp-thud', 'season', 'सीज़न', vol=0.8, off=0.1)], notes='The stamp word is spoken.'),
 S('s14b', 14, KF, variant='night', light='night', type='prop-hero', fx=[embers(16)], props=[P('ashwatthama-silhouette', 0.48, 0.54, 1.6, 'still')], text=tag('Ashwatthama', 'अश्वत्थामा', 'next season', 'अगला सीज़न'), overlay='folk-art-border', cam=zoom(1.0, 1.08), sfx=[snd('drum-boom-deep', at=0, vol=0.7)], transition='cut-to-black', notes='A lone warrior, walking away under a dark sky. Krishna\'s curse: CE 10.16.9-12.'),
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
 'id': 'S01E08', 'title': {'en': 'The Mother Who Cursed Krishna', 'hi': 'वो माँ, जिसने कृष्ण को शाप दिया'},
 'format': 'short', 'width': 1080, 'height': 1920, 'fps': 30,
 'sourceCredit': {'en': 'Mahabharata, Stri & Mausala Parva', 'hi': 'महाभारत, स्त्री और मौसल पर्व'},
 'safeZone': {'bottom': 0.2, 'right': 0.12}, 'grade': {'grain': 0.12, 'vignette': 0.45, 'shadows': True}, 'sound': e03['sound'],
 'thumbnail': {'scene': 's01', 'at': 0.5, 'series': {'en': 'Shraap · Episode 8', 'hi': 'शाप · भाग 8'},
   'title': {'en': 'The Mother Who Cursed Krishna', 'hi': 'वो माँ, जिसने कृष्ण को शाप दिया'}, 'titleLines': {'en': ['She Cursed', 'Krishna'], 'hi': ['कृष्ण को', 'शाप']}},
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
                at = lambda c: [i for i, w in enumerate(full) if c['onWord'][l].lower().replace("'", '').replace('-', '') in w][c.get('nth', {}).get(l, 1) - 1]
                a = at(next(c for c in cs if c['target'] == s['id'])); b = min([at(c) for c in cs if at(c) > a] + [len(full)])
                full = full[a:b]
            hits = [w for w in full if r['onWord'][l].lower().replace("'", '').replace('-', '') in w]
            if len(hits) < r.get('nth', {}).get(l, 1): errs.append((s['id'], l, r['onWord'][l], 'not heard'))
            elif hits[r.get('nth', {}).get(l, 1) - 1] not in (r['onWord'][l].lower().replace("'", '').replace('-', ''), r['onWord'][l].lower() + 's'): errs.append((s['id'], l, r['onWord'][l], f'matches inside "{hits[0]}"'))
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
