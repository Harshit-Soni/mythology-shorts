"""S03E01 cast, made in code from the library rigs (reuse before create), in the looks picked at the concept check
(svg/04-concept-brief.md: Hanuman A saffron, Rama A durva green).

Hanuman  <- pandu rig: sindoor-orange body, a vanara muzzle (the hanu), a long curling tail, a gold crown and mace.
            Baby poses: the same figure at child size, a bigger head, no crown or mace.
Rama     <- pandu rig: durva-green skin (shyama), yellow silk, a red sash, crown, faint halo; bow and quiver when standing.
Sita     <- the women's rig: a plain ochre sari, no jewels (in the grove), sad.
Vayu     <- pandu rig: the wind god, pale sky-grey, silver-white cloth, a halo; cradling the baby, furious.
Indra    <- + hurling-vajra (the S01E03 Indra, the vajra thrown from a raised hand).

All poses face right; scenes mirror with flip.
Run from the repo root:  python3 episodes/S03E01-hanuman-never-died/svg/make-cast.py [out_dir]
"""
import copy
import importlib.util
import json
import math
import os
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('c08', 'episodes/S01E08-gandhari-curses-krishna/svg/make-cast.py')
X = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X)
spec = importlib.util.spec_from_file_location('k03', 'episodes/S01E03-urvashi-curses-arjuna/svg/make-cast.py')
I3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(I3)
sys.argv = _argv
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
V, M, F, K, C, Wm = X.V, X.M, X.F, X.K, X.C, X.Wm
group, frag, recolor, joint = C.group, C.frag, C.recolor, C.joint
NS, INK, GOLD, GOLD_D, GOLD_L = C.NS, X.INK, X.GOLD, X.GOLD_D, X.GOLD_L
EP = 'S03E01-hanuman-never-died'


def save(tree, cid, pose, title, expr=None):
    root = tree.getroot()
    root.set('data-character', cid)
    for tag, text in (('title', title), ('desc', f'{title}. S03E01, made by episodes/{EP}/svg/make-cast.py.')):
        e = root.find(NS + tag)
        if e is not None:
            e.text = text
    name = f'{pose}__{expr}' if expr else pose
    path = f'{OUT}/{cid}/{name}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode')
    print('wrote', path)


def before(parent, gid, frags):
    kids = list(parent)
    i = next(k for k, c in enumerate(kids) if c.get('id') == gid)
    for n, e in enumerate(frag(frags)):
        parent.insert(i + n, e)


def behind(r, xml):
    ch = group(r, 'character')
    for k, e in enumerate(frag(xml)):
        ch.insert(k, e)


def whole(r, t):
    """Prefix a transform to the whole figure (rotate for a leap or a fall, scale for a child)."""
    cp = group(r, 'canvas-placement')
    cp.set('transform', t + ' ' + cp.get('transform'))


# ================= Hanuman =================
H_SKIN = ('#E8833A', '#D06A26', '#A24E18')
H_FACE = ('#E2B080', '#C08A5A')
H_DHOTI = {'#FFF8E9': '#C9463A', '#F3EEDF': '#A93528', '#D6C7AF': '#86261C', '#B7A68F': '#5E1810'}
H_SASH = {'#F3EEDF': GOLD, '#D6C7AF': GOLD_D}
H_BAND = '#86261C'


def muzzle():
    face, face_d = H_FACE
    fill = 'M508 236 Q526 204 588 198 Q614 194 632 212 Q652 236 644 264 Q634 296 598 308 Q556 316 528 298 Q506 282 508 236Z'
    return (f'<path d="{fill}" fill="{face}" />'
            f'<path d="M588 198 Q614 194 632 212 Q652 236 644 264 Q634 296 598 308 Q556 316 528 298" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" />'
            f'<path d="M510 240 Q506 276 528 298" stroke="{face_d}" stroke-width="3" />'
            f'<path d="M540 300 Q580 312 616 296" stroke="{face_d}" stroke-width="4" />'
            f'<path d="M624 220 q5 -4 9 1 M610 218 q5 -4 8 1" stroke="{INK}" stroke-width="3.5" stroke-linecap="round" />'
            f'<path d="M630 232 Q628 248 614 254" stroke="{face_d}" stroke-width="3.5" />')


H_MOUTH = f'<path d="M556 274 Q594 286 632 262" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" />'
H_SMILE = f'<path d="M552 268 Q594 298 634 256" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" /><path d="M552 268 l-6 -6" stroke="{INK}" stroke-width="4" />'
H_OPEN = f'<path d="M562 268 Q596 264 630 262 Q620 292 596 294 Q572 292 562 268Z" fill="#6E1E22" stroke="{INK}" stroke-width="3.5" /><path d="M570 270 Q596 268 622 266 L620 272 Q596 274 572 276Z" fill="#FFF8E9" />'
H_WONDER = f'<path d="M580 266 Q600 260 616 268 Q614 292 598 294 Q582 290 580 266Z" fill="#6E1E22" stroke="{INK}" stroke-width="3.5" />'


def tail_standing():
    d = 'M450 1010 Q330 1080 280 960 Q230 820 300 640 Q340 520 300 430 Q270 370 310 350 Q350 340 344 392'
    return tail(d)


def tail_seated(hip):
    d = f'M430 {hip + 230} Q260 {hip + 300} 220 {hip + 200} Q190 {hip + 90} 250 {hip + 20} Q290 {hip - 20} 300 {hip + 30}'
    return tail(d)


def tail(d):
    s0, s1, s2 = H_SKIN
    return (f'<path d="{d}" stroke="{INK}" stroke-width="40" stroke-linecap="round" />'
            f'<path d="{d}" stroke="{s0}" stroke-width="30" stroke-linecap="round" />'
            f'<path d="{d}" stroke="{s2}" stroke-width="6" stroke-linecap="round" stroke-dasharray="1 70" transform="translate(-6 0)" />')


def gada(scale=1.0):
    """A gold mace for the far hand (hand-local: the wrist at the origin, the hand pointing +y); the head rises up -y."""
    s = scale
    top = -420 * s
    return (f'<g id="gada" transform="translate(0 30)">'
            f'<path d="M-10 {top + 60} L-10 {250 * s} L10 {250 * s} L10 {top + 60}Z" fill="#8A5A2A" stroke="{INK}" stroke-width="5" />'
            + ''.join(f'<rect x="-14" y="{y}" width="28" height="16" fill="{GOLD}" stroke="{INK}" stroke-width="3" />' for y in (top + 120, -40, 210 * s))
            + f'<circle cx="0" cy="{top}" r="{82 * s}" fill="{GOLD}" stroke="{INK}" stroke-width="6" />'
            + ''.join(f'<path d="M{74 * s * c:.0f} {top + 32 * s * q:.0f} Q0 {top - 6} {-74 * s * c:.0f} {top - 32 * s * q:.0f}" stroke="{GOLD_D}" stroke-width="5" />' for c, q in ((0.95, 0.9), (0.5, 1.6), (0.0, 2.0)))
            + f'<circle cx="{-24 * s:.0f}" cy="{top - 26 * s:.0f}" r="{16 * s:.0f}" fill="{GOLD_L}" />'
            + f'<path d="M-12 {top - 80 * s:.0f} L0 {top - 118 * s:.0f} L12 {top - 80 * s:.0f}Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" /></g>')


def hold_gada(r, scale=1.0):
    h = group(r, 'hand-far')
    for k, e in enumerate(frag(gada(scale))):
        h.insert(k, e)          # behind the fist, so the fingers wrap it


def h_face(r, mood='calm'):
    mouths = {'calm': H_MOUTH, 'smile': H_SMILE, 'wonder': H_WONDER, 'open': H_OPEN}
    X.set_mouth(r, closed=mouths.get(mood, H_MOUTH), open_=H_OPEN)
    M.male_brows(r, {'calm': 'calm', 'smile': 'calm', 'devoted': 'up', 'moved': 'sad', 'wonder': 'up', 'hurt': 'sad', 'intent': 'angry'}.get(mood, 'calm'))


NECKLACE = (''.join(f'<circle cx="{510 + 118 * math.sin(a / 22):.0f}" cy="{330 + 150 * math.cos(a / 22):.0f}" r="11" fill="#F7F2E6" stroke="{INK}" stroke-width="3" />' for a in range(-30, 31, 4))
            + f'<path d="M510 470 L540 500 L510 548 L480 500Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" /><ellipse cx="510" cy="504" rx="17" ry="22" fill="#3E9A86" stroke="{INK}" stroke-width="3" /><ellipse cx="505" cy="496" rx="5" ry="7" fill="#BFEFE0" />')


def hanuman_base(tail_=True):
    t, r = F.pandu(H_SKIN, H_DHOTI, H_SASH)
    before(group(r, 'head'), 'eyes-open', muzzle())
    h_face(r)
    if tail_:
        behind(r, tail_standing())
    return t, r


def baby(r, head=1.3):
    """Child proportions: no crown, a bigger head, the whole figure at 0.55, feet still on the base line."""
    M.hide(r, 'crown')
    joint(r, 'head', f'translate(510 330) scale({head}) translate(-510 -330)')
    whole(r, 'translate(500 1550) scale(0.55) translate(-500 -1550)')
    group(r, 'head').extend(frag('<path d="M470 150 Q520 110 586 140 Q560 120 520 124 Q490 128 470 150Z" fill="#3C3031" />'))  # a tuft of hair


def hanuman():
    cid, sk = 'hanuman', H_SKIN
    # --- adult ---
    for expr, mood in ((None, 'calm'), ('devoted', 'smile'), ('moved', 'moved'), ('necklace', 'moved')):
        t, r = hanuman_base(); Wm.arms(r, far=(-24, -56, 80), near=(10, -24, 0)); hold_gada(r); h_face(r, mood)
        if expr == 'devoted':
            M.male_brows(r, 'up')
        if expr in ('moved', 'necklace'):
            M.eyes_closed(r); X.set_mouth(r, closed=H_SMILE)
        if expr == 'necklace':     # Rama's gift on his chest: pearls and a beryl pendant (CE 7.39.20-21)
            group(r, 'upper-body').extend(frag(NECKLACE))
        save(t, cid, 'standing', 'Hanuman · standing tall with his mace, calm' + (f', {expr}' if expr else ''), expr)
    for expr, mood in ((None, 'devoted'), ('smile', 'smile')):
        t, r = F.pandu(sk, H_DHOTI, H_SASH); before(group(r, 'head'), 'eyes-open', muzzle()); h_face(r, mood)
        M.folded_hands(r, sk); V.sit_cross(r, tuple(H_DHOTI[k] for k in ('#FFF8E9', '#F3EEDF', '#D6C7AF', '#B7A68F')), sk)
        behind(r, tail_seated(640 + V.LAP)); M.tilt(r, 6)
        if expr:
            M.eyes_closed(r)
        save(t, cid, 'seated-listening', 'Hanuman · seated cross-legged, palms joined, listening' + (', eyes closed, smiling' if expr else ''), expr)
    t, r = F.pandu(sk, H_DHOTI, H_SASH); before(group(r, 'head'), 'eyes-open', muzzle()); h_face(r, 'devoted')
    M.folded_hands(r, sk); K.sit_kneel(r, H_DHOTI, H_BAND, lean=22); M.tilt(r, 14); behind(r, tail_seated(640 + K.SIT_DY))
    save(t, cid, 'bowing', 'Hanuman · kneeling, bowed low, palms joined')
    t, r = F.pandu(sk, H_DHOTI, H_SASH); before(group(r, 'head'), 'eyes-open', muzzle()); h_face(r, 'devoted')
    M.folded_hands(r, sk); K.sit_kneel(r, H_DHOTI, H_BAND, lean=-2); M.tilt(r, -10); Wm.eyes_up(r); behind(r, tail_seated(640 + K.SIT_DY))
    save(t, cid, 'asking', 'Hanuman · kneeling, palms joined, looking up: asking')
    t, r = hanuman_base(); Wm.arms(r, far=(-84, -24, 0), near=(-36, -70, 0)); Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk)
    h_face(r, 'moved'); M.eyes_closed(r); X.set_mouth(r, closed=H_SMILE); M.lean(r, 6)
    save(t, cid, 'embraced', 'Hanuman · held in an embrace, arms around, eyes closed, moved')
    t, r = hanuman_base(); Wm.arms(r, far=(-160, -6, 0), near=(30, -40, 0)); Wm.palm(r, 'hand-far', sk); h_face(r, 'intent')
    group(r, 'hand-near').extend(frag(gada(0.8).replace('id="gada" transform="translate(0 30)"', 'transform="translate(0 30) rotate(180)"')))
    whole(r, 'rotate(-58 500 900)')
    save(t, cid, 'leaping', 'Hanuman · in mid-leap over the sea, one arm reaching ahead, the mace in the other')
    # --- baby ---
    t, r = hanuman_base(); Wm.arms(r, far=(-150, -20, 0), near=(-20, -60, 0)); Wm.palm(r, 'hand-far', sk); h_face(r, 'wonder'); M.tilt(r, -14); baby(r)
    save(t, cid, 'baby-reaching', 'Hanuman (baby) · reaching up at the rising sun, wide-eyed')
    t, r = hanuman_base(); Wm.arms(r, far=(-166, -8, 0), near=(-150, 10, 0)); Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk); h_face(r, 'wonder'); M.tilt(r, -10); baby(r)
    whole(r, 'rotate(-30 500 1200)')
    save(t, cid, 'baby-leaping', 'Hanuman (baby) · leaping up into the sky, both arms reaching')
    t, r = hanuman_base(); Wm.arms(r, far=(-120, -30, 0), near=(-140, 20, 0)); h_face(r, 'hurt'); M.eyes_closed(r); baby(r)
    whole(r, 'rotate(140 500 1200)')
    save(t, cid, 'baby-falling', 'Hanuman (baby) · tumbling down, eyes shut (no wound shown)')
    t, r = F.pandu(sk, H_DHOTI, H_SASH); before(group(r, 'head'), 'eyes-open', muzzle()); h_face(r, 'smile')
    Wm.arms(r, far=(-22, 30, 0), near=(20, -30, 0)); V.sit_cross(r, tuple(H_DHOTI[k] for k in ('#FFF8E9', '#F3EEDF', '#D6C7AF', '#B7A68F')), sk)
    behind(r, tail_seated(640 + V.LAP)); M.halo(r, rad=150); baby(r, head=1.35)
    save(t, cid, 'baby-glowing', 'Hanuman (baby) · seated in a ring of light, smiling')


# ================= Rama =================
R_SKIN = ('#4E7A68', '#3C6454', '#284A3C')
R_DHOTI = {'#FFF8E9': '#F2C230', '#F3EEDF': '#DDA81E', '#D6C7AF': '#B78514', '#B7A68F': '#86600C'}
R_SASH = {'#F3EEDF': '#C9463A', '#D6C7AF': '#93301F'}
R_WHITE = {'#FFF8E9': '#FBF8F0', '#F3EEDF': '#EEE8DA', '#D6C7AF': '#D4CBB6', '#B7A68F': '#AEA48E'}
QUIVER = (f'<g transform="translate(440 470) rotate(-14)"><rect x="-28" y="0" width="56" height="300" rx="14" fill="#8A5A2A" stroke="{INK}" stroke-width="5" />'
          + ''.join(f'<path d="M{x} 0 L{x} -70 M{x - 10} -70 L{x} -96 L{x + 10} -70Z" stroke="{INK}" stroke-width="5" fill="#E8E0C8" />' for x in (-14, 0, 14))
          + f'<rect x="-30" y="40" width="60" height="16" fill="{GOLD}" stroke="{INK}" stroke-width="3" /></g>')


def rama_base(bow=None, white=False, halo=0.6):
    t, r = F.pandu(R_SKIN, R_WHITE if white else R_DHOTI, {'#F3EEDF': '#F4EFE2', '#D6C7AF': '#D8CFBC'} if white else R_SASH, bow=bow)
    M.halo(r, rad=150); group(r, 'halo').set('opacity', str(halo))
    M.male_brows(r, 'calm')
    return t, r


def rama():
    cid, sk = 'rama', R_SKIN
    for expr in (None, 'smile'):
        t, r = rama_base('held'); Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0)); behind(r, QUIVER)
        if expr:
            X.k_smile(r)
        save(t, cid, 'standing', 'Rama · standing with his bow, calm' + (', smiling' if expr else ''), expr)
    for expr in (None, 'moved'):
        t, r = rama_base(halo=0.8); Wm.arms(r, far=(-22, 30, 0), near=(20, -30, 0)); V.sit_cross(r, tuple(R_DHOTI[k] for k in ('#FFF8E9', '#F3EEDF', '#D6C7AF', '#B7A68F')), sk)
        if expr:
            M.male_brows(r, 'up'); X.k_smile(r)
        save(t, cid, 'enthroned', 'Rama · seated on the throne, a king' + (', moved' if expr else ''), expr)
    t, r = rama_base(); Wm.arms(r, far=(-86, -22, 0), near=(-40, -70, 0)); Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk); X.k_smile(r); M.lean(r, 6)
    save(t, cid, 'embracing', 'Rama · embracing, arms around, smiling')
    t, r = rama_base(white=True, halo=1.0); Wm.arms(r, far=(-34, -100, -10), near=(10, -24, 0)); Wm.palm(r, 'hand-far', sk); X.k_smile(r); M.lean(r, 3)
    M.hide(r, 'crown')
    save(t, cid, 'departing', 'Rama · leaving the world, in white, a hand raised in blessing, at peace')
    t, r = rama_base(); Wm.arms(r, far=(-78, -6, 0), near=(10, -24, 0)); Wm.palm(r, 'hand-far', sk)
    save(t, cid, 'hand-on-shoulder', 'Rama · a hand held out onto a friend\'s shoulder, speaking')


# ================= Sita =================
C.WOMEN['sita'] = dict(skin=('#F1CBA3', '#DFB085', '#BB8A60'), border='#B5402E', border_l='#D86A54', utt=('#D8A64A', '#B8862E', '#ECC878'), hair='braid')


def sita():
    t = C.build('sita', drape_style='shawl', eye_scale=1.16, warmth=0)
    r = t.getroot()
    recolor(group(r, 'dhoti'), {'#F3EEDF': '#D8A64A', '#E6DCC6': '#B8862E', '#B7A68F': '#7E5A1A', '#D6C7AF': '#C99A3E'})
    recolor(group(r, 'kanchuka'), {'#F3EEDF': '#B5402E'})
    C.arms_clasped(r)
    M.female_brows(r, 'sad'); M.tilt(r, 8)
    save(t, 'sita', 'waiting', 'Sita · in the grove, hands clasped, sad but steady')


# ================= Vayu =================
VY_SKIN = ('#B9C6D6', '#9CAEC2', '#73879E')
VY_DHOTI = {'#FFF8E9': '#F4F6F8', '#F3EEDF': '#E1E6EC', '#D6C7AF': '#C2CAD4', '#B7A68F': '#98A2AE'}
VY_SASH = {'#F3EEDF': '#7FA8C9', '#D6C7AF': '#5A86AA'}


def vayu():
    t, r = F.pandu(VY_SKIN, VY_DHOTI, VY_SASH)
    M.halo(r, rad=150); group(r, 'halo').set('opacity', '0.5')
    recolor(group(r, 'head'), {'#3C3031': '#E8ECF0', '#695450': '#B8C0CA'})          # silver-white hair
    Wm.arms(r, far=(-30, -84, 20), near=(-24, -92, 0))
    M.male_brows(r, 'angry'); M.mouth_open(r); M.tilt(r, -4)
    # the child in his arms: baby Hanuman, eyes closed, laid across the chest (a copy of the baby figure, ids stripped)
    bt, br = hanuman_base(); Wm.arms(br, far=(-20, 30, 0), near=(10, -20, 0)); h_face(br, 'hurt'); M.eyes_closed(br); M.hide(br, 'crown')
    joint(br, 'head', 'translate(510 330) scale(1.3) translate(-510 -330)')
    kid = copy.deepcopy(group(br, 'canvas-placement'))
    for e in kid.iter():
        e.attrib.pop('id', None)
    wrap = ET.Element(NS + 'g', {'transform': 'translate(610 470) rotate(-78) scale(0.36) translate(-500 -900)'})
    wrap.append(kid)
    group(r, 'upper-body-front').insert(0, wrap)
    save(t, 'vayu', 'holding-child', 'Vayu · the wind god holding his hurt child, furious')


# ================= Indra: hurling the vajra =================
def indra():
    t = ET.parse(C.SRC); r = t.getroot()
    I3.remove(r, 'bow')
    for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
        recolor(group(r, g), I3.I_DHOTI)
    recolor(group(r, 'uttariya'), I3.I_SASH)
    recolor(r, dict(zip(C.PANDU_SKIN, I3.I_SKIN)))
    group(r, 'crown').set('transform', 'translate(510 115) scale(1.12 1.35) translate(-510 -115)')
    I3.halo(r)
    Wm.arms(r, far=(-150, -20, 0), near=(14, -40, 0))
    group(r, 'hand-far').extend(frag(
        f'<g transform="translate(0 40)"><path d="M0 -90 L0 90" stroke="{GOLD_D}" stroke-width="16" />'
        f'<path d="M0 -90 l-22 -30 l22 8 l22 -8Z M0 90 l-22 30 l22 -8 l22 8Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
        f'<circle r="18" fill="{GOLD}" stroke="{INK}" stroke-width="3" /></g>'))
    M.male_brows(r, 'angry'); M.lean(r, 4)
    save(t, 'indra', 'hurling-vajra', 'Indra · the vajra raised high to hurl, stern (not raging)')


def character_json():
    cast = {
        'hanuman': dict(divine=True, name={'en': 'Hanuman', 'hi': 'हनुमान'}, role='Son of Vayu; Rama\'s devoted friend; a Chiranjeevi',
                        look='Concept A: sindoor-orange body, a pale vanara muzzle (the hanu), a long tail curling up, gold crown and mace, red dhoti. Baby poses: child size, no crown.',
                        sourceNotes='Valmiki CE 4.65, 7.35-36, 7.39, 7.98. Colours are a design choice (svg/04-concept-brief.md). Shown with dignity: no cartoon snout.',
                        poses=['standing', 'seated-listening', 'bowing', 'asking', 'embraced', 'leaping', 'baby-reaching', 'baby-leaping', 'baby-falling', 'baby-glowing']),
        'rama': dict(divine=True, name={'en': 'Rama', 'hi': 'राम'}, role='King of Ayodhya', look='Concept A: durva-green skin (shyama), yellow silk, red sash, crown, halo; bow and quiver when standing; white when departing.',
                     sourceNotes='Valmiki. Not to be mistaken for Krishna: no peacock feather, a different skin.', poses=['standing', 'enthroned', 'embracing', 'departing', 'hand-on-shoulder']),
        'sita': dict(divine=True, name={'en': 'Sita', 'hi': 'सीता'}, role="Rama's wife", look='The women\'s rig: a plain ochre sari, no jewels (in the grove).', sourceNotes='MBh 3.147.35 (found by Hanuman).', poses=['waiting']),
        'vayu': dict(divine=True, name={'en': 'Vayu', 'hi': 'वायु'}, role='The wind god, Hanuman\'s father', look='The pandu rig: pale sky-grey, silver-white hair streaming, white cloth, a blue sash, halo.',
                     sourceNotes='Valmiki CE 4.65.23, 7.35.48-49. Colours are a design choice.', poses=['holding-child']),
    }
    for cid, d in cast.items():
        files = {f[:-4]: f for f in sorted(os.listdir(f'{OUT}/{cid}')) if f.endswith('.svg')}
        out = {'id': cid, **d, 'appearsIn': ['S03E01'], 'files': files, 'facing': 'right', 'facingByPose': {p: 'right' for p in d['poses']},
               'notes': f'Made in code by episodes/{EP}/svg/make-cast.py. Mirror with flip.'}
        json.dump(out, open(f'{OUT}/{cid}/character.json', 'w'), ensure_ascii=False, indent=2)
    # Indra: add the new pose to the library entry
    p = f'{OUT}/indra/character.json'
    if os.path.exists(p):
        d = json.load(open(p))
        if 'hurling-vajra' not in d['poses']:
            d['poses'].append('hurling-vajra'); d['facingByPose']['hurling-vajra'] = 'right'
        d['files']['hurling-vajra'] = 'hurling-vajra.svg'
        if 'S03E01' not in d['appearsIn']:
            d['appearsIn'].append('S03E01')
        json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    hanuman(); rama(); sita(); vayu(); indra(); character_json()
