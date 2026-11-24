"""S01E05 cast, made in code from the library rigs (reuse before create). Builds on the S01E03/E04 helpers.

Karna         <- pandu rig: golden-brown skin, big gold earrings. Two looks: warrior (crown, indigo and gold) and
                 student (the disguise: no crown, a topknot, plain cream cloth, no necklace or cuffs)
Parashurama   <- mandavya rig, in his E04 colours: teaching, accusing, cursing, sleeping (lying)
homa-brahmin  <- mandavya rig: iron-grey hair, cream and yellow; owner of the homa cow
Drona         <- mandavya rig: white hair and beard, slate-blue and gold

Every pose faces right; scenes mirror with flip.
Run from the repo root:  python3 episodes/S01E05-karna-two-curses/svg/make-cast.py [out_dir]
"""
import copy
import importlib.util
import json
import os
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('c04', 'episodes/S01E04-amba-vow-bhishma/svg/make-cast.py')
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
sys.argv = _argv
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
M, C, Wm = F.M, F.C, F.Wm
group, frag, recolor, joint = C.group, C.frag, C.recolor, C.joint
NS, INK, GOLD, GOLD_D, GOLD_L = C.NS, C.INK, M.GOLD, M.GOLD_D, M.GOLD_L


def save(tree, cid, pose, title, expr=None):
    root = tree.getroot()
    root.set('data-character', cid)
    for tag, text in (('title', title), ('desc', f'{title}. S01E05, made by episodes/S01E05-karna-two-curses/svg/make-cast.py.')):
        e = root.find(NS + tag)
        if e is not None:
            e.text = text
    path = f'{OUT}/{cid}/{pose}__{expr}.svg' if expr else f'{OUT}/{cid}/{pose}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode')
    print('wrote', path)


# ---------- Karna ----------
K_SKIN = ('#DDA267', '#C3854B', '#975F32')
K_DHOTI = {'#FFF8E9': '#4A6BB0', '#F3EEDF': '#34528F', '#D6C7AF': '#263D70', '#B7A68F': '#182A52'}   # indigo
K_SASH = {'#F3EEDF': GOLD, '#D6C7AF': GOLD_D}
ST_DHOTI = {'#FFF8E9': '#EFDDB6', '#F3EEDF': '#DCC596', '#D6C7AF': '#BFA473', '#B7A68F': '#957C50'}  # unbleached cloth
ST_SASH = {'#F3EEDF': '#B9855A', '#D6C7AF': '#8E6240'}


def earrings(r):
    M.hide(r, 'earrings')
    group(r, 'head').extend(frag(
        f'<circle cx="452" cy="246" r="20" fill="none" stroke="{INK}" stroke-width="12" /><circle cx="452" cy="246" r="20" fill="none" stroke="{GOLD}" stroke-width="8" />'
        f'<circle cx="452" cy="269" r="8" fill="{GOLD_L}" stroke="{INK}" stroke-width="2" />'))


def warrior(bow=None):
    t, r = F.pandu(K_SKIN, K_DHOTI, K_SASH, bow=bow)
    earrings(r)
    return t, r


def student(bow=None):
    t, r = F.pandu(K_SKIN, ST_DHOTI, ST_SASH, bow=bow)
    for g in ('upper-body', 'upper-arm-far', 'upper-arm-near', 'forearm-far', 'forearm-near', 'hand-far', 'hand-near', 'torso'):
        C.strip_gold(group(r, g))
    recolor(group(r, 'uttariya'), {'#E8B53A': '#D9B88A', '#F4D17B': '#D9B88A', '#AF762C': '#8E6240'})  # no gold trim
    head = group(r, 'head')
    head.remove(group(r, 'crown'))
    # a full cap of dark hair and a topknot where the crown was (behind the face, so it goes first)
    for k, e in enumerate(frag(
            f'<path d="M452 214 Q438 150 462 112 Q498 66 556 80 Q600 92 602 138 Q570 118 534 122 Q498 128 486 168 Q480 200 470 226Z" fill="#2C2326" stroke="{INK}" stroke-width="3" />'
            f'<path d="M474 96 Q462 58 492 38 Q526 24 544 50 Q556 78 530 92 Q500 104 474 96Z" fill="#2C2326" stroke="{INK}" stroke-width="3" />'
            f'<path d="M482 90 Q508 100 534 84" stroke="#B9855A" stroke-width="8" />'
            f'<path d="M470 130 Q500 96 552 98 M492 54 Q512 40 532 54" stroke="#574648" stroke-width="3" />')):
        head.append(e)
    earrings(r)
    return t, r


def strain(r):
    """Clenched teeth, knotted brows, a bead of sweat."""
    M.male_brows(r, 'angry')
    M.hide(r, 'mouth-closed')
    group(r, 'head').extend(frag(
        f'<path d="M546 246 Q568 236 592 244 Q594 258 588 264 Q566 270 548 262Z" fill="#FFF8E9" stroke="{INK}" stroke-width="3.5" />'
        f'<path d="M548 254 Q568 252 590 254 M560 243 L560 264 M571 241 L571 266 M581 242 L581 264" stroke="{INK}" stroke-width="2" />'
        f'<path d="M492 170 q-10 16 0 22 q11 -6 0 -22Z" fill="#CFE6F2" stroke="{INK}" stroke-width="2" />'))


def worry(r):
    M.male_brows(r, 'sad')
    group(r, 'mouth-closed').extend(frag(f'<path d="M556 254 Q572 246 590 256" stroke="{INK}" stroke-width="3" />'))


def glance_back(r):
    """Uneasy: pupils slide away from whoever he faces, lids a little low."""
    worry(r)
    e = group(r, 'eyes-open')
    e.set('transform', 'translate(-3 2)')


G = 1525           # rig-space ground line
SIT_DY, LUNGE_DY = 590, 380


def limb(pts, w, fill, hi):
    """A cloth-covered limb: an outlined thick stroke with a highlight along its upper edge."""
    return (f'<path d="{pts}" stroke="{INK}" stroke-width="{w + 7}" /><path d="{pts}" stroke="{fill}" stroke-width="{w}" />'
            f'<path d="{pts}" stroke="{hi}" stroke-width="{w * 0.14:.0f}" transform="translate({w * 0.06:.0f} {-w * 0.27:.0f})" />')


def clear_legs(r):
    M.hide(r, 'leg-near'); M.hide(r, 'leg-far')
    dh = group(r, 'dhoti')
    for ch in list(dh):
        dh.remove(ch)
    return dh


def waistband(hip, fill):
    return f'<path d="M394 {hip - 16} Q520 {hip - 32} 648 {hip - 14} L654 {hip + 26} Q520 {hip + 8} 388 {hip + 24}Z" fill="{fill}" stroke="{INK}" stroke-width="3" />'


def foot(x, y, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot})"><path d="M-40 -34 Q10 -44 46 -18 Q84 -6 92 14 Q80 28 20 26 L-40 24Z" fill="{K_SKIN[1]}" stroke="{INK}" stroke-width="3.5" />'
            f'<path d="M56 4 l10 14 M72 10 l6 10" stroke="{K_SKIN[2]}" stroke-width="3" /></g>')


def sit_kneel(r, d, band, lean=0):
    """Kneeling, sitting back on the heels (thighs forward), facing right."""
    M.lean(r, lean, SIT_DY)
    dh = clear_legs(r)
    a, b, c, e = d['#FFF8E9'], d['#F3EEDF'], d['#D6C7AF'], d['#B7A68F']
    hip = 640 + SIT_DY
    dh.extend(frag(
        foot(330, G - 18, 180)
        + limb(f'M800 {G - 66} Q560 {G - 40} 360 {G - 62}', 108, c, b)                 # shins flat on the ground
        + limb(f'M540 {hip + 60} Q680 {hip + 70} 806 {G - 96}', 168, c, b)             # far thigh
        + f'<path d="M392 {hip - 6} Q372 {hip + 90} 400 {G - 90} Q520 {G - 60} 640 {G - 120} L650 {hip - 6}Z" fill="{b}" stroke="{INK}" stroke-width="3.5" />'
        + limb(f'M470 {hip + 84} Q620 {hip + 96} 764 {G - 92}', 176, b, a)             # near thigh
        + f'<path d="M406 {hip + 4} Q400 {hip + 70} 410 {G - 120} L560 {hip + 4}Z" fill="{b}" />'
        + f'<path d="M430 {hip + 60} Q440 {hip + 130} 470 {G - 70} M520 {hip + 40} Q620 {hip + 60} 700 {G - 120} M480 {hip + 120} Q600 {hip + 130} 720 {G - 60}" stroke="{e}" stroke-width="5" />'
        + waistband(hip, band)))


def lunge(r, d, band, lean):
    """On one knee, the far leg planted in front: braced to pull, facing right."""
    M.lean(r, lean, LUNGE_DY)
    dh = clear_legs(r)
    a, b, c, e = d['#FFF8E9'], d['#F3EEDF'], d['#D6C7AF'], d['#B7A68F']
    hip = 640 + LUNGE_DY
    dh.extend(frag(
        f'<path d="M716 {G - 150} L724 {G - 40} L790 {G - 40} L786 {G - 150}Z" fill="{K_SKIN[1]}" stroke="{INK}" stroke-width="3.5" />'
        + foot(760, G - 24)
        + limb(f'M560 {hip + 60} Q680 {hip + 40} 752 {hip + 120} Q768 {hip + 220} 752 {G - 170}', 150, c, b)
        + foot(216, G - 22, 180)
        + limb(f'M486 {G - 80} Q360 {G - 60} 250 {G - 60}', 104, c, b)
        + f'<path d="M392 {hip - 6} Q380 {hip + 80} 410 {hip + 160} L620 {hip + 150} L650 {hip - 6}Z" fill="{b}" stroke="{INK}" stroke-width="3.5" />'
        + limb(f'M484 {hip + 80} Q470 {hip + 220} 500 {G - 96}', 178, b, a)
        + f'<path d="M406 {hip + 4} L420 {hip + 130} L600 {hip + 120} L634 {hip + 4}Z" fill="{b}" />'
        + f'<path d="M440 {hip + 50} Q430 {hip + 190} 470 {G - 110} M520 {hip + 40} Q520 {hip + 200} 530 {G - 130} M600 {hip + 50} Q680 {hip + 40} 730 {hip + 150}" stroke="{e}" stroke-width="5" />'
        + waistband(hip, band)))


def karna():
    cid = 'karna'
    # --- student (the disguise) ---
    for expr, fn in ((None, lambda r: M.male_brows(r, 'calm')), ('uneasy', glance_back), ('awed', lambda r: (M.male_brows(r, 'up'), M.mouth_open(r)))):
        t, r = student(); M.folded_hands(r, K_SKIN); fn(r)
        save(t, cid, 'folded-hands', 'Karna (student) · palms joined' + (f', {expr}' if expr else ''), expr)
    t, r = student('held'); Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0)); M.male_brows(r, 'calm')
    save(t, cid, 'student-bow', 'Karna (student) · standing with his bow')
    t, r = student(); M.folded_hands(r, K_SKIN); sit_kneel(r, ST_DHOTI, '#8E6240'); worry(r); M.mouth_open(r); M.tilt(r, -4)
    save(t, cid, 'kneeling-pleading', 'Karna (student) · kneeling, begging forgiveness')
    for expr, fn in ((None, worry), ('afraid', lambda r: (M.male_brows(r, 'up'), M.mouth_open(r)))):
        t, r = student(); M.folded_hands(r, K_SKIN); sit_kneel(r, ST_DHOTI, '#8E6240', lean=12); M.tilt(r, 10); fn(r)
        save(t, cid, 'bowed', 'Karna (student) · kneeling, bowed' + (f', {expr}' if expr else ''), expr)
    t, r = student(); Wm.arms(r, far=(-4, 10, 0), near=(8, -20, 0)); strain(r); M.eyes_closed(r)
    group(r, 'head').extend(frag(f'<path d="M548 196 q-6 22 -2 34" stroke="#CFE6F2" stroke-width="5" /><path d="M505 160 q-8 14 0 20 q9 -6 0 -20Z" fill="#CFE6F2" stroke="{INK}" stroke-width="2" />'))
    save(t, cid, 'enduring', 'Karna (student) · enduring, jaw clenched, eyes shut')
    seated_lap()
    # --- warrior ---
    t, r = warrior('held'); Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0)); M.male_brows(r, 'angry')
    save(t, cid, 'watching', 'Karna · watching Arjuna, bow lowered')
    t, r = warrior(); Wm.arms(r, far=(-68, -22, -30), near=(10, -40, 0)); Wm.palm(r, 'hand-far', K_SKIN); M.male_brows(r, 'up')
    save(t, cid, 'asking', 'Karna · asking, an open hand')
    t, r = warrior('drawn'); M.male_brows(r, 'angry')
    save(t, cid, 'drawing-bow', 'Karna · drawing his bow')
    t, r = warrior(); Wm.arms(r, far=(-150, -8, -10), near=(26, -30, 0)); Wm.palm(r, 'hand-far', K_SKIN)
    M.male_brows(r, 'sad'); M.mouth_open(r); M.tilt(r, -8)
    save(t, cid, 'empty-hand', 'Karna · calling the weapon, his raised hand empty')
    t, r = warrior(); Wm.arms(r, far=(-62, 6, 0), near=(-78, 4, 0)); lunge(r, K_DHOTI, GOLD, lean=20); M.tilt(r, -10); strain(r)
    save(t, cid, 'pulling-wheel', 'Karna · on his knees at the wheel, pulling')


LAP_DY = 560


def seated_lap():
    """Karna seated cross-legged, hands resting wide, so a sleeping head fits in his lap (drawn with the guru lying in front)."""
    for expr in (None, 'pained'):
        t, r = student()
        Wm.arms(r, far=(-22, 30, 0), near=(20, -30, 0))
        M.lean(r, 0, LAP_DY)
        M.hide(r, 'leg-near'); M.hide(r, 'leg-far')
        dh = group(r, 'dhoti')
        for ch in list(dh):
            dh.remove(ch)
        a, b, c, d = ST_DHOTI['#FFF8E9'], ST_DHOTI['#F3EEDF'], ST_DHOTI['#D6C7AF'], ST_DHOTI['#B7A68F']
        g, hip = 1525, 640 + LAP_DY
        s1 = K_SKIN[1]
        dh.extend(frag(
            limb(f'M470 {hip + 40} Q330 {hip + 70} 206 {g - 96}', 150, b, a)                              # thighs out to the knees
            + limb(f'M580 {hip + 40} Q720 {hip + 70} 842 {g - 96}', 150, b, a)
            + f'<path d="M400 {hip - 8} Q520 {hip - 24} 644 {hip - 8} L690 {g - 60} Q520 {g - 20} 350 {g - 60}Z" fill="{b}" />'
            + limb(f'M842 {g - 84} Q640 {g - 30} 470 {g - 54}', 104, c, b)                                # shins crossing in front
            + limb(f'M206 {g - 84} Q400 {g - 10} 590 {g - 46}', 104, b, a)
            + f'<path d="M588 {g - 96} Q650 {g - 100} 690 {g - 66} Q706 {g - 30} 660 {g - 8} Q610 {g} 590 {g - 8}Z" fill="{s1}" stroke="{INK}" stroke-width="3.5" />'
            + f'<path d="M462 {g - 92} Q410 {g - 92} 384 {g - 58} Q380 {g - 34} 410 {g - 22}" fill="{s1}" stroke="{INK}" stroke-width="3" />'
            + f'<path d="M300 {g - 110} Q380 {g - 140} 440 {g - 120} M620 {g - 130} Q700 {g - 150} 780 {g - 118} M290 {g - 60} Q380 {g - 30} 470 {g - 44}" stroke="{d}" stroke-width="4" />'
            + f'<path d="M394 {hip - 14} Q520 {hip - 30} 648 {hip - 12} L652 {hip + 26} Q520 {hip + 8} 390 {hip + 24}Z" fill="#8E6240" stroke="{INK}" stroke-width="3" />'))
        if expr:
            strain(r)
        else:
            M.male_brows(r, 'calm')
        M.tilt(r, 8)
        save(t, 'karna', 'guru-on-lap', 'Karna (student) · seated, his guru’s head in his lap' + (f', {expr}' if expr else ''), expr)


# ---------- the mandavya-rig sages ----------
FURY = 'assets/characters/mandavya/cursing-hand-raised.svg'  # furious face, open mouth, near arm thrown out
CALM = 'assets/characters/mandavya/standing-calm.svg'
DH = ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap')


def sage(src, dhoti, hair=None, skin=None):
    t = ET.parse(src); r = t.getroot()
    for g in DH:
        recolor(group(r, g), dict(zip(('#F6A13E', '#E68129', '#BC5420', '#9E451F'), dhoti)))
    if hair:
        for g in ('hair-back', 'head'):
            recolor(group(r, g), dict(zip(('#241E25', '#3C3031', '#695450', '#A8A39A', '#CBC4B4'), hair)))
    if skin:
        recolor(r, dict(zip(('#E5A66B', '#CF8D55', '#AB653C'), skin)))
    return t, r


def fury_near(r, up, fore, hand):
    joint(r, 'upper-arm-near', f'translate(335 397) rotate({up})')
    joint(r, 'forearm-near', f'translate(0 214.238) rotate({fore})')
    joint(r, 'hand-near', f'translate(0 276.978) rotate({hand})')


def raised(r, up, fore, hand, skin):
    """The far arm raised beside the face (so it never crosses it), palm open; the near arm hangs in a fist."""
    fury_near(r, 16, -10, 0)
    joint(r, 'upper-arm-far', f'translate(635 390) rotate({up})')
    joint(r, 'forearm-far', f'translate(0 215.205) rotate({fore})')
    joint(r, 'hand-far', f'translate(0 178.045) rotate({hand})')
    open_palm(r, 'hand-far', skin)


PARA = ('#B8553A', '#9E3B22', '#6E2A18', '#4E1C10')


def open_palm(r, gid, skin):
    Wm.palm(r, gid, skin)


def parashurama():
    cid, sk = 'parashurama', Wm.MANDAVYA_SKIN
    t, r = sage(CALM, PARA)
    F.m_arms(r, far=(-24, -118, 20), near=(18, -10, 0)); open_palm(r, 'hand-far', sk)
    save(t, cid, 'teaching', 'Parashurama · teaching, a hand raised')
    t, r = sage(FURY, PARA)  # the arm thrown straight at the one he accuses
    save(t, cid, 'accusing', 'Parashurama · accusing, an arm thrown out')
    t, r = sage(FURY, PARA)
    raised(r, -162, -10, 0, sk)
    save(t, cid, 'cursing', 'Parashurama · cursing, a palm raised high')
    # asleep on his back: the whole figure turned so the head lies at the left, scaled to fit the canvas width
    t, r = sage(CALM, PARA)
    F.m_arms(r, far=(6, 60, 20), near=(10, -62, 0))
    M.eyes_closed(r)
    M.hide(r, 'leg-near'); M.hide(r, 'leg-far')
    sk0, sk1 = sk[0], sk[1]
    legs = ''.join(f'<path d="M{x} 1080 Q{x - 8} 1250 {x + 12} 1370 L{x + 78} 1370 Q{x + 96} 1240 {x + 92} 1080Z" fill="{f}" stroke="{INK}" stroke-width="3.5" />'
                   f'<path d="M{x + 10} 1362 Q{x + 2} 1420 {x + 34} 1432 Q{x + 120} 1440 {x + 152} 1420 Q{x + 150} 1396 {x + 82} 1362Z" fill="{f}" stroke="{INK}" stroke-width="3.5" />'
                   for x, f in ((540, sk1), (400, sk0)))
    ch = group(r, 'character')
    for k, e in enumerate(frag(legs)):
        ch.insert(k, e)
    cp = group(r, 'canvas-placement')
    cp.set('transform', 'translate(-60 1738) scale(0.7) rotate(-90) ' + cp.get('transform'))
    save(t, cid, 'sleeping', 'Parashurama · asleep on his back, head at the left')


def homa_brahmin():
    cid = 'homa-brahmin'
    hair = ('#4A4548', '#6E686A', '#989294', '#D2CDC4', '#E6E1D8')
    skin = ('#EBC093', '#D8A576', '#B27C50')
    cloth = ('#F6E7B8', '#EAD08A', '#C9A552', '#9A7A34')
    t, r = sage(CALM, cloth, hair, skin)
    F.m_arms(r, far=(-18, -120, 30), near=(16, -118, 0)); open_palm(r, 'hand-far', skin)
    b = group(r, 'brows')
    for ch in list(b):
        b.remove(ch)
    b.extend(frag('<path d="M510 164 Q532 162 558 150 L560 156 Q536 170 514 171Z" fill="#6E686A" /><path d="M582 150 L596 158 L596 164 L583 157Z" fill="#6E686A" />'))
    save(t, cid, 'standing-grief', 'The Brahmin · grieving over his cow')
    t, r = sage(FURY, cloth, hair, skin)
    raised(r, -112, -42, 0, skin)
    save(t, cid, 'cursing', 'The Brahmin · cursing, palm raised')


def drona():
    hair = ('#8F887C', '#B9B2A6', '#DAD4C8', '#F2EEE6', '#FFFFFF')
    skin = ('#E3B283', '#CC9666', '#A46E44')
    t, r = sage(CALM, ('#8FA6C4', '#6C86A8', '#4C6486', '#344860'), hair, skin)
    F.m_arms(r, far=(-34, -96, -14), near=(14, -14, 0)); open_palm(r, 'hand-far', skin)
    ub = group(r, 'upper-body')
    ub.insert(list(ub).index(group(r, 'head')), frag(
        f'<path d="M398 372 Q470 520 640 650 L600 668 Q430 560 372 392Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" /><path d="M392 392 Q470 540 612 652" stroke="{GOLD_D}" stroke-width="5" />')[0])
    save(t, 'drona', 'refusing', 'Drona · a raised palm: no')


def character_json():
    cast = {
        'karna': dict(name={'en': 'Karna', 'hi': 'कर्ण'}, role='Son of Kunti and Surya, raised as a charioteer’s son; Arjuna’s rival', divine=False,
                      look='Golden-brown skin and large gold earrings in every pose. Warrior: gold crown, indigo dhoti, gold sash. Student (his disguise at Parashurama’s ashram): no crown, a topknot, plain unbleached cloth, no necklace or cuffs.',
                      sourceNotes='Shanti §II–III; Karna Parva §42, §90–91. By the last battle he has given away his natural armour and earrings (Shanti §V); the battle poses wear ordinary gold (CE 8.66.32–33 mentions his ornaments).',
                      poses=['folded-hands', 'student-bow', 'kneeling-pleading', 'bowed', 'enduring', 'guru-on-lap', 'watching', 'asking', 'drawing-bow', 'empty-hand', 'pulling-wheel'],
                      expressions=['calm', 'uneasy', 'awed', 'afraid', 'pained']),
        'homa-brahmin': dict(name={'en': 'The Brahmin of the homa cow', 'hi': 'होम-धेनु के ब्राह्मण'}, role='The Brahmin whose cow Karna killed unknowingly', divine=False,
                             look='The sage rig with iron-grey hair and beard, cream and yellow cloth.', sourceNotes='Shanti §II (unnamed in the text).', poses=['standing-grief', 'cursing']),
        'drona': dict(name={'en': 'Drona', 'hi': 'द्रोण'}, role='Teacher of arms to the Pandavas, the Kauravas and Karna', divine=False,
                      look='The sage rig with white hair and beard, a slate-blue dhoti and a gold sash.', sourceNotes='Shanti §II.', poses=['refusing']),
    }
    for cid, d in cast.items():
        files = {f[:-4]: f for f in sorted(os.listdir(f'{OUT}/{cid}')) if f.endswith('.svg')}
        out = {'id': cid, **d, 'appearsIn': ['S01E05'], 'files': files, 'facing': 'per pose, see facingByPose (ear rule)',
               'facingByPose': {p: 'right' for p in d['poses']},
               'notes': 'Made in code by episodes/S01E05-karna-two-curses/svg/make-cast.py. All poses face right; mirror with flip.'}
        json.dump(out, open(f'{OUT}/{cid}/character.json', 'w'), ensure_ascii=False, indent=2)
        print('wrote', f'{OUT}/{cid}/character.json')
    p = f'{OUT}/parashurama/character.json'
    if os.path.exists(p):
        j = json.load(open(p))
        for pose in ('teaching', 'accusing', 'cursing', 'sleeping'):
            if pose not in j['poses']:
                j['poses'].append(pose)
            j['files'][pose] = f'{pose}.svg'
            j['facingByPose'][pose] = 'up (lying on his back, head at the left)' if pose == 'sleeping' else 'right'
        if 'S01E05' not in j['appearsIn']:
            j['appearsIn'].append('S01E05')
        json.dump(j, open(p, 'w'), ensure_ascii=False, indent=2)
        print('updated', p)


if __name__ == '__main__':
    karna(); parashurama(); homa_brahmin(); drona(); character_json()
