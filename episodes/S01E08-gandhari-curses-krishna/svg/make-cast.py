"""S01E08 cast, made in code from the library rigs (reuse before create). Builds on the S01E05-E07 helpers.

Krishna     <- pandu rig: dark cloud-blue skin (meghavapuh, CE 16.9.7), yellow silk (pitambara), a crown with a peacock
               feather, a faint halo. Calm in every pose: never hurt, never beaten.
Gandhari    <- the women's rig (Kunti's build): an older queen in deep plum, grey in her hair, a small crown, and the
               folded white cloth she bound over her own eyes (CE 1.103.13). Brows show her feeling above the band.
Duryodhana  <- pandu rig: maroon and gold, crown, a black moustache; a palm raised to refuse
Jara        <- the exile rig: dark skin, bark-brown loincloth, hair tied up; drawing a bow, and fallen to his knees

All poses face right; scenes mirror with flip.
Run from the repo root:  python3 episodes/S01E08-gandhari-curses-krishna/svg/make-cast.py [out_dir]
"""
import importlib.util
import json
import os
import sys

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('c07', 'episodes/S01E07-parikshit-seven-days/svg/make-cast.py')
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
sys.argv = _argv
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
Z, K, F, M, C, Wm = V.Z, V.K, V.F, V.M, V.C, V.Wm
group, frag, recolor, joint = C.group, C.frag, C.recolor, C.joint
NS, INK, GOLD, GOLD_D, GOLD_L = C.NS, C.INK, M.GOLD, M.GOLD_D, M.GOLD_L
EP = 'S01E08-gandhari-curses-krishna'


def save(tree, cid, pose, title, expr=None):
    root = tree.getroot()
    root.set('data-character', cid)
    for tag, text in (('title', title), ('desc', f'{title}. S01E08, made by episodes/{EP}/svg/make-cast.py.')):
        e = root.find(NS + tag)
        if e is not None:
            e.text = text
    name = f'{pose}__{expr}' if expr else pose
    path = f'{OUT}/{cid}/{name}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode')
    print('wrote', path)


def clear(g):
    for ch in list(g):
        g.remove(ch)


def set_mouth(r, closed=None, open_=None, rest_open=False):
    """Replace the mouth shapes (the lip-sync swaps mouth-closed / mouth-open)."""
    if closed is not None:
        g = group(r, 'mouth-closed'); clear(g); g.extend(frag(closed))
    if open_ is not None:
        g = group(r, 'mouth-open'); clear(g); g.extend(frag(open_))
    if rest_open:
        group(r, 'mouth-closed').set('style', 'display:none'); group(r, 'mouth-open').attrib.pop('style', None)


def lying(r, dx=-60):
    """The whole figure turned to lie on its back, head at the left (S01E05's sleeping Parashurama)."""
    cp = group(r, 'canvas-placement')
    cp.set('transform', f'translate({dx} 1738) scale(0.7) rotate(-90) ' + cp.get('transform'))


# ---------- Krishna ----------
KR_SKIN = ('#5B78B4', '#46619C', '#2F4676')                   # cloud-dark blue
KR_DHOTI = {'#FFF8E9': '#F2C230', '#F3EEDF': '#DDA81E', '#D6C7AF': '#B78514', '#B7A68F': '#86600C'}   # yellow silk
KR_SASH = {'#F3EEDF': '#E87A3A', '#D6C7AF': '#B85A26'}
FEATHER = (f'<g id="peacock-feather" transform="translate(568 46) rotate(24)"><path d="M0 120 Q-4 60 0 0" stroke="{INK}" stroke-width="7" /><path d="M0 120 Q-4 60 0 0" stroke="#5E8A3A" stroke-width="4" />'
           + ''.join(f'<path d="M0 {y} q{-w} -10 {-w - 6} -26 M0 {y} q{w} -10 {w + 6} -26" stroke="#4E8F52" stroke-width="3" />' for y, w in ((100, 10), (80, 16), (60, 20), (40, 22)))
           + f'<ellipse cx="0" cy="-8" rx="30" ry="40" fill="#2E8A6E" stroke="{INK}" stroke-width="4" /><ellipse cx="0" cy="-2" rx="19" ry="26" fill="#E2B33A" />'
           + f'<ellipse cx="0" cy="2" rx="12" ry="16" fill="#2C5FA8" /><ellipse cx="0" cy="4" rx="6" ry="8" fill="#16244A" /></g>')


def krishna_base():
    t, r = F.pandu(KR_SKIN, KR_DHOTI, KR_SASH)
    M.halo(r, rad=150)
    group(r, 'halo').set('opacity', '0.75')
    head = group(r, 'head')
    head.extend(frag(FEATHER))
    # a soft, calm face: gentle brows
    M.male_brows(r, 'calm')
    group(r, 'upper-body').extend(frag(  # vanamala: a garland of forest flowers
        '<path d="M410 360 Q450 560 520 640 Q590 560 630 360" stroke="#4E8F52" stroke-width="12" />'
        + ''.join(f'<circle cx="{x}" cy="{y}" r="11" fill="{c}" stroke="{INK}" stroke-width="2" />'
                  for x, y, c in ((420, 420, '#F2F0E4'), (440, 500, '#E05A6A'), (470, 570, '#F2C230'), (520, 636, '#F2F0E4'), (570, 570, '#E05A6A'), (600, 500, '#F2C230'), (620, 420, '#F2F0E4')))))
    return t, r


def k_smile(r):
    set_mouth(r, closed=f'<path d="M552 248 Q574 262 596 244" stroke="{INK}" stroke-width="4" />')


def k_grave(r):
    M.male_brows(r, 'sad')


def krishna():
    cid, sk = 'krishna', KR_SKIN
    for expr in (None, 'smile'):
        t, r = krishna_base(); Wm.arms(r, far=(-8, 8, 0), near=(10, -16, 0))
        if expr:
            k_smile(r)
        save(t, cid, 'standing', 'Krishna · standing, calm' + (', a faint smile' if expr else ''), expr)
    t, r = krishna_base(); Wm.arms(r, far=(-62, -30, -20), near=(10, -24, 0)); Wm.palm(r, 'hand-far', sk)
    save(t, cid, 'envoy', 'Krishna · the envoy, an open palm: asking for peace')
    t, r = krishna_base(); Wm.arms(r, far=(14, 10, 0), near=(-14, -10, 0)); M.lean(r, 3)
    save(t, cid, 'walking', 'Krishna · walking, calm')
    t, r = krishna_base(); Wm.arms(r, far=(-4, 6, 0), near=(6, -8, 0)); k_grave(r); M.tilt(r, 8)
    save(t, cid, 'looking-on', 'Krishna · standing still, grave, looking on')
    t, r = krishna_base(); Wm.arms(r, far=(4, 40, 10), near=(8, -46, 0)); M.eyes_closed(r); k_smile(r)
    M.hide(r, 'leg-near'); M.hide(r, 'leg-far')
    sk0, sk1 = sk[0], sk[1]
    a, b = KR_DHOTI['#FFF8E9'], KR_DHOTI['#F3EEDF']
    legs = ''.join(f'<path d="M{x} 1040 Q{x - 8} 1250 {x + 12} 1370 L{x + 78} 1370 Q{x + 96} 1240 {x + 92} 1040Z" fill="{f}" stroke="{INK}" stroke-width="3.5" />'
                   f'<path d="M{x + 10} 1362 Q{x + 2} 1420 {x + 34} 1432 Q{x + 120} 1440 {x + 152} 1420 Q{x + 150} 1396 {x + 82} 1362Z" fill="{s}" stroke="{INK}" stroke-width="3.5" />'
                   for x, f, s in ((540, b, sk1), (400, a, sk0)))
    ch = group(r, 'character')
    for k, e in enumerate(frag(legs)):
        ch.insert(k, e)
    lying(r)
    save(t, cid, 'reclining', 'Krishna · lying on the bare ground in yoga, eyes closed, head at the left')
    t, r = krishna_base(); Wm.arms(r, far=(-24, -118, 20), near=(18, -10, 0)); Wm.palm(r, 'hand-far', sk); k_smile(r)
    V.sit_cross(r, tuple(KR_DHOTI[k] for k in ('#FFF8E9', '#F3EEDF', '#D6C7AF', '#B7A68F')), sk)
    save(t, cid, 'seated-blessing', 'Krishna · seated, a palm raised in blessing, comforting')
    t, r = krishna_base(); Wm.arms(r, far=(-24, -118, 20), near=(30, -40, 0)); Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk); M.eyes_closed(r); k_smile(r)
    group(r, 'halo').set('opacity', '1')
    save(t, cid, 'rising', 'Krishna · rising in light, a palm raised, eyes closed, at peace')


# ---------- Gandhari ----------
C.WOMEN['gandhari'] = dict(skin=('#E9BE94', '#D3A274', '#AD7A50'), border='#C9A23A', border_l='#E3C062', utt=('#5E2F5E', '#47214A', '#7A447A'), hair='knot')
G_ROBE = {'#F3EEDF': '#6E3A6E', '#E6DCC6': '#5A2C5A', '#B7A68F': '#3C1A40', '#D6C7AF': '#874E86'}
BAND = '#F7F2E6'


def gandhari_base():
    t = C.build('gandhari', drape_style='shawl', eye_scale=1.1, warmth=0)
    r = t.getroot()
    recolor(group(r, 'dhoti'), G_ROBE)
    recolor(group(r, 'kanchuka'), {'#F3EEDF': '#6E3A6E'})
    # grey in the hair
    recolor(r, {'#3C3031': '#5E5658', '#695450': '#9A9294'})
    head = group(r, 'head')
    # the blindfold: a folded white band over both eyes, knotted at the back of the head; no eyes to blink
    for gid in ('eyes-open', 'eyes-closed'):
        clear(group(r, gid))
    head.extend(frag(
        f'<path d="M444 170 Q520 156 606 166 L608 208 Q522 196 446 212Z" fill="{BAND}" stroke="{INK}" stroke-width="3.5" />'
        f'<path d="M448 184 Q522 172 606 180 M448 198 Q522 186 606 194" stroke="#D9D0BE" stroke-width="3" />'
        f'<path d="M450 176 Q430 190 416 230 Q424 236 436 228 Q446 206 458 196 Q440 214 438 250 Q448 254 456 244 Q458 214 470 198Z" fill="{BAND}" stroke="{INK}" stroke-width="3" />'
        f'<path d="M460 106 Q520 86 594 110 L586 92 L568 100 L552 76 L530 96 L512 72 L494 96 L476 82 L470 102Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
        f'<circle cx="530" cy="100" r="7" fill="#C9463A" stroke="{INK}" stroke-width="2" />'))
    M.bangles(r, 'hand-far', 2); M.bangles(r, 'hand-near', 2)
    return t, r


def g_brows(r, mood):
    """Brows above the band, drawn thick so they read at phone size."""
    d = {'grief': ('M512 150 Q536 150 560 136', 'M582 138 Q592 142 600 150'),
         'anger': ('M512 140 Q537 146 562 158', 'M580 158 Q590 148 600 142'),
         'furious': ('M510 136 Q537 146 564 162', 'M578 162 Q590 148 602 138')}[mood]
    b = group(r, 'brows'); clear(b)
    b.extend(frag(f'<path d="{d[0]}" stroke="#4A4042" stroke-width="7" /><path d="{d[1]}" stroke="#4A4042" stroke-width="6" />'))


G_OPEN = f'<path d="M554 240 Q574 236 594 240 Q592 270 574 274 Q556 270 554 240Z" fill="#6E1E22" stroke="{INK}" stroke-width="3" /><path d="M560 242 Q574 240 588 242 L586 248 Q574 250 562 248Z" fill="#FFF8E9" />'
G_SAD = f'<path d="M556 254 Q574 242 594 252" stroke="{INK}" stroke-width="4" /><path d="M558 256 Q574 248 590 254" stroke="#B5534A" stroke-width="5" />'


def gandhari():
    cid, sk = 'gandhari', C.WOMEN['gandhari']['skin']
    t, r = gandhari_base(); g_brows(r, 'grief'); set_mouth(r, closed=G_SAD, open_=G_OPEN); M.tilt(r, 8)
    save(t, cid, 'grief', 'Gandhari · blindfolded, head bowed in grief')
    for expr, mood in ((None, 'anger'), ('grief', 'grief')):
        t, r = gandhari_base(); Wm.arms(r, far=(-74, -22, -20), near=(14, -40, 10)); Wm.palm(r, 'hand-far', sk); g_brows(r, mood); set_mouth(r, closed=G_SAD, open_=G_OPEN)
        save(t, cid, 'accusing', 'Gandhari · an open palm held out to Krishna, asking why' + (', grieving' if expr else ''), expr)
    t, r = gandhari_base(); Wm.arms(r, far=(-162, -10, 0), near=(14, -40, 10)); Wm.palm(r, 'hand-far', sk); g_brows(r, 'furious'); set_mouth(r, closed=G_SAD, open_=G_OPEN, rest_open=True); M.tilt(r, -4)
    save(t, cid, 'cursing', 'Gandhari · cursing, a palm raised high')


# ---------- Duryodhana ----------
DY_SKIN = ('#D9A06A', '#BF834E', '#965C32')
DY_DHOTI = {'#FFF8E9': '#8E2A3A', '#F3EEDF': '#74202E', '#D6C7AF': '#561622', '#B7A68F': '#3A0E16'}
DY_SASH = {'#F3EEDF': GOLD, '#D6C7AF': GOLD_D}


def duryodhana():
    t, r = F.pandu(DY_SKIN, DY_DHOTI, DY_SASH)
    group(r, 'head').extend(frag('<path d="M544 238 Q566 226 590 232 Q608 236 614 224 Q608 252 586 247 Q562 243 544 252 Q532 250 544 238Z" fill="#241C1E" />'))
    Wm.arms(r, far=(-96, -30, -40), near=(16, -60, 0)); Wm.palm(r, 'hand-far', DY_SKIN); M.male_brows(r, 'angry'); M.tilt(r, -6)
    save(t, 'duryodhana', 'refusing', 'Duryodhana · chin up, a palm raised: refusing peace')


# ---------- Jara ----------
J_SKIN = ('#8E5A36', '#764826', '#56321A')
J_DHOTI = {'#FFF8E9': '#8A6A42', '#F3EEDF': '#6E5232', '#D6C7AF': '#523C22', '#B7A68F': '#382814'}
J_SASH = {'#F3EEDF': '#5E7040', '#D6C7AF': '#44522C'}


def jara():
    cid = 'jara'
    pandu = F.pandu
    F.pandu = lambda *a, **k: pandu(*a, bow='drawn')   # the exile look, but keeping the archer rig's drawn bow
    try:
        t, r = Z.exile(J_SKIN, J_DHOTI, J_SASH)
    finally:
        F.pandu = pandu
    M.male_brows(r, 'angry')
    save(t, cid, 'drawing-bow', 'Jara · a hunter drawing his bow, intent')
    t, r = Z.exile(J_SKIN, J_DHOTI, J_SASH)
    M.folded_hands(r, J_SKIN); K.sit_kneel(r, J_DHOTI, '#523C22', lean=30); M.male_brows(r, 'up'); M.mouth_open(r); M.tilt(r, 16)
    save(t, cid, 'prostrate', 'Jara · fallen to his knees, bowed, palms joined, horrified')


def character_json():
    cast = {
        'krishna': dict(divine=True, name={'en': 'Krishna', 'hi': 'कृष्ण'}, role='Vasudeva Krishna of Dvaraka, the Pandavas’ friend and charioteer',
                        look='The pandu rig: cloud-dark blue skin, yellow silk, a peacock feather in the crown, a forest garland, a faint halo. Calm in every pose.',
                        sourceNotes='CE 16.9.7 (cloud-dark), 16.5.20 (yellow robe). Never shown hurt.', poses=['standing', 'envoy', 'walking', 'looking-on', 'reclining', 'seated-blessing', 'rising']),
        'gandhari': dict(divine=False, name={'en': 'Gandhari', 'hi': 'गांधारी'}, role='Queen of Hastinapura, mother of the hundred Kauravas',
                         look='The women’s rig: deep plum, grey in the hair, a small crown, and the folded white cloth over her eyes. No eyes to blink.',
                         sourceNotes='CE 1.103.13 (the blindfold), 11.25 (the curse).', poses=['grief', 'accusing', 'cursing']),
        'duryodhana': dict(divine=False, name={'en': 'Duryodhana', 'hi': 'दुर्योधन'}, role='Gandhari’s eldest son, who refused peace',
                           look='The pandu rig: maroon and gold, crown, a black moustache.', sourceNotes='CE 5.127.', poses=['refusing']),
        'jara': dict(divine=False, name={'en': 'Jara', 'hi': 'जरा'}, role='The hunter who took Krishna for a deer', look='The exile rig: dark skin, bark-brown cloth, hair tied up.',
                     sourceNotes='CE 16.5.19–21. An ordinary, horrified man; forgiven.', poses=['drawing-bow', 'prostrate']),
    }
    for cid, d in cast.items():
        files = {f[:-4]: f for f in sorted(os.listdir(f'{OUT}/{cid}')) if f.endswith('.svg')}
        out = {'id': cid, **d, 'appearsIn': ['S01E08'], 'files': files, 'facing': 'right', 'facingByPose': {p: 'right' for p in d['poses']},
               'notes': f'Made in code by episodes/{EP}/svg/make-cast.py. Mirror with flip.'}
        json.dump(out, open(f'{OUT}/{cid}/character.json', 'w'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    krishna(); gandhari(); duryodhana(); jara(); character_json()
