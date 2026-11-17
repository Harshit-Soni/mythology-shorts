"""S01E03 cast, made in code from the library rigs (reuse before create).

Arjuna      <- pandu rig: the researched look ("young and of darkish hue", Virata §11), new poses
Brihannala  <- Arjuna (same face and build) in a woman's dress: braid, big earrings, conch bangles (Virata §2, §11)
Indra       <- pandu rig: golden skin, tall crown, gold halo
Chitrasena  <- pandu rig: sky-blue Gandharva king with a veena
Urvashi     <- the S01E02 women's build (make-concepts.py), dressed as the foremost apsara: dignified court dress
Uttara      <- the same build, younger and smaller

Every pose faces right; scenes mirror with flip. Run from the repo root:
  python3 episodes/S01E03-urvashi-curses-arjuna/svg/make-cast.py [out_dir]
"""
import copy
import importlib.util
import json
import os
import sys
import xml.etree.ElementTree as ET

E02 = 'episodes/S01E02-kindama-curses-pandu/svg'
_argv = sys.argv
sys.argv = sys.argv[:1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = _load('concepts', f'{E02}/make-concepts.py')
Wm = _load('women', f'{E02}/make-women.py')
sys.argv = _argv
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
NS, INK = C.NS, C.INK
group, frag, joint, recolor = C.group, C.frag, C.joint, C.recolor
GOLD, GOLD_D, GOLD_L = '#E8B53A', '#B8862A', '#F4D17B'

ARJ_SKIN = ('#A87048', '#8C5834', '#6A3E22')          # light, mid, shade: "of darkish hue"
A_DHOTI = {'#FFF8E9': '#C0503C', '#F3EEDF': '#A53A2A', '#D6C7AF': '#8E2A20', '#B7A68F': '#621E18'}
A_SASH = {'#F3EEDF': GOLD, '#D6C7AF': GOLD_D}


# ---------- small helpers ----------
def hide(r, gid):
    group(r, gid).set('style', 'display:none')


def unhide(r, gid):
    group(r, gid).attrib.pop('style', None)


def remove(r, gid):
    g = group(r, gid)
    C.parent_of(r, g).remove(g)


def eyes_closed(r):
    hide(r, 'eyes-open'); unhide(r, 'eyes-closed')


def mouth_open(r):
    hide(r, 'mouth-closed'); unhide(r, 'mouth-open')


def male_brows(r, mood):
    shapes = {
        'calm': ('M515 157Q534 155 558 169L556 173Q535 164 518 164Z', 'M582 165L594 154L596 160L586 170Z'),
        'up': ('M515 150Q536 138 560 152L558 158Q536 146 518 157Z', 'M582 152L594 142L597 148L586 158Z'),
        'sad': ('M515 160Q537 160 560 148L561 155Q537 167 518 167Z', 'M582 149L594 156L594 162L583 156Z'),
        'angry': ('M515 152Q537 158 562 175L558 180Q535 166 517 159Z', 'M580 175L596 156L599 162L585 180Z'),
    }[mood]
    b = group(r, 'brows')
    for ch in list(b):
        b.remove(ch)
    b.extend(frag(f'<path d="{shapes[0]}" fill="#291C23" /><path d="{shapes[1]}" fill="#291C23" />'))


def female_brows(r, mood):
    if mood == 'angry':
        b = group(r, 'brows')
        for ch in list(b):
            b.remove(ch)
        b.extend(frag('<path d="M514 154 Q537 158 562 170" stroke="#3C3031" stroke-width="6" />'
                      '<path d="M580 170 Q590 160 600 155" stroke="#3C3031" stroke-width="5" />'))
    else:
        Wm.brows(r, mood)


def smile(r):
    group(r, 'mouth-closed').extend(frag('<path d="M556 246 Q574 262 593 241" stroke="#291C23" stroke-width="2.5" />'))


def lean(r, deg, dy=0):
    for gid in ('upper-body', 'upper-body-front'):
        joint(r, gid, f'translate(0 {dy}) rotate({deg} 510 675)')


def tilt(r, deg):
    group(r, 'head').set('transform', f'rotate({deg} 510 310)')


def bangles(r, gid, n=3):
    """Gold conch bangles stacked on the wrist (the hand group's origin is the wrist)."""
    xml = ''.join(f'<ellipse cx="0" cy="{-6 - 13 * k}" rx="27" ry="8" fill="none" stroke="{GOLD}" stroke-width="7" />'
                  f'<ellipse cx="0" cy="{-6 - 13 * k}" rx="27" ry="8" fill="none" stroke="{INK}" stroke-width="1.5" />'
                  for k in range(n))
    group(r, gid).extend(frag(xml))


def save(tree, cid, pose, title, expr=None):
    root = tree.getroot()
    root.set('data-character', cid)
    t = root.find(NS + 'title')
    if t is not None:
        t.text = title
    d = root.find(NS + 'desc')
    if d is not None:
        d.text = f'{title}. S01E03, made by episodes/S01E03-urvashi-curses-arjuna/svg/make-cast.py.'
    name = f'{pose}__{expr}' if expr else pose
    path = f'{OUT}/{cid}/{name}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode')
    print('wrote', path)


# ---------- Arjuna ----------
def arjuna_base(bow=True):
    t = ET.parse(C.SRC); r = t.getroot()
    for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
        recolor(group(r, g), A_DHOTI)
    recolor(group(r, 'uttariya'), A_SASH)
    recolor(r, dict(zip(C.PANDU_SKIN, ARJ_SKIN)))
    if not bow:
        remove(r, 'bow')
    return t, r


def folded_hands(r, skin):
    Wm.arms(r, far=(10, 117, 53), near=(-15, -116, -49))
    Wm.palm(r, 'hand-far', skin, narrow=True)
    Wm.palm(r, 'hand-near', skin, narrow=True)


KNEEL_DY = 430


def kneel(r):
    """Upright kneel on both knees, facing right: the upper body drops by KNEEL_DY; the dhoti is redrawn as
    thighs straight down to the knees on the ground and the shins lying back to the left."""
    lean(r, 0, KNEEL_DY)
    hide(r, 'leg-near'); hide(r, 'leg-far')
    dh = group(r, 'dhoti')
    for ch in list(dh):
        dh.remove(ch)
    g = 1532  # rig-space ground
    s0, s1, s2 = ARJ_SKIN
    dh.extend(frag(
        # feet (soles up) at the back end of the shins
        f'<path d="M262 {g - 40} Q232 {g - 70} 244 {g - 96} L276 {g - 92} Q282 {g - 60} 296 {g - 44}Z" fill="{s1}" stroke="{INK}" stroke-width="3" />'
        # shins and the dhoti over them, lying on the ground
        f'<path d="M280 {g - 86} Q420 {g - 112} 610 {g - 104} Q650 {g - 60} 620 {g} L290 {g} Q270 {g - 40} 280 {g - 86}Z" fill="#A53A2A" stroke="{INK}" stroke-width="3" />'
        f'<path d="M320 {g - 70} Q440 {g - 84} 560 {g - 80}" stroke="#8E2A20" stroke-width="5" />'
        # thighs from the hips down to the knees, a gentle forward slope
        f'<path d="M398 {650 + KNEEL_DY} Q520 {632 + KNEEL_DY} 642 {652 + KNEEL_DY} Q676 {g - 300} 668 {g - 60} Q560 {g - 30} 420 {g - 70} Q380 {g - 300} 398 {650 + KNEEL_DY}Z" fill="#C0503C" stroke="{INK}" stroke-width="3" />'
        f'<path d="M520 {660 + KNEEL_DY} Q530 {g - 260} 540 {g - 70}" stroke="#8E2A20" stroke-width="5" />'
        f'<path d="M560 {650 + KNEEL_DY} Q590 {g - 250} 600 {g - 66} L582 {g - 64} Q570 {g - 250} 548 {652 + KNEEL_DY}Z" fill="#A53A2A" />'
        f'<path d="M450 {720 + KNEEL_DY} Q470 {g - 300} 466 {g - 120}" stroke="#E07060" stroke-width="4" opacity="0.6" />'
        # waist band
        f'<path d="M394 {630 + KNEEL_DY} Q520 {612 + KNEEL_DY} 646 {634 + KNEEL_DY} L648 {672 + KNEEL_DY} Q520 {650 + KNEEL_DY} 392 {668 + KNEEL_DY}Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'))


def arjuna():
    out = 'arjuna'
    # standing with the bow lowered (the E02 placeholder, now in the researched colouring)
    t, r = arjuna_base()
    Wm_unstring(r)
    Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0))
    save(t, out, 'standing-bow', 'Arjuna · standing with his bow')
    t, r = arjuna_base(); Wm_unstring(r)
    Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0)); male_brows(r, 'up'); mouth_open(r)
    save(t, out, 'standing-bow', 'Arjuna · standing with his bow, awed', 'awed')
    t, r = arjuna_base(); Wm_unstring(r)
    Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0)); male_brows(r, 'sad')
    save(t, out, 'standing-bow', 'Arjuna · standing with his bow, worried', 'worried')

    # bowing to an elder: palms joined, eyes closed, leaning forward, head lowered
    t, r = arjuna_base(bow=False)
    folded_hands(r, ARJ_SKIN); lean(r, 7); tilt(r, 10); eyes_closed(r)
    save(t, out, 'bowing-eyes-closed', 'Arjuna · bowing with palms joined, eyes closed')

    # kneeling, palms joined: earnest (base, speaks), eyes closed, shocked
    for expr, fn in ((None, lambda r: male_brows(r, 'sad')),
                     ('eyes-closed', lambda r: (eyes_closed(r), tilt(r, 6))),
                     ('shocked', lambda r: (male_brows(r, 'up'), mouth_open(r), tilt(r, -4)))):
        t, r = arjuna_base(bow=False)
        folded_hands(r, ARJ_SKIN); kneel(r); fn(r)
        save(t, out, 'kneeling-folded-hands', 'Arjuna · kneeling, palms joined' + (f', {expr}' if expr else ''), expr)

    # a first dance step: one arm up in a mudra, the other out behind, a slight lean; surprised at himself
    t, r = arjuna_base(bow=False)
    Wm.arms(r, far=(-155, 35, -20), near=(70, -30, 60))
    Wm.palm(r, 'hand-far', ARJ_SKIN); Wm.palm(r, 'hand-near', ARJ_SKIN)
    lean(r, -4); male_brows(r, 'up'); mouth_open(r)
    save(t, out, 'dance-step', 'Arjuna · trying a dance step')


def Wm_unstring(r):
    show_arrow = group(r, 'arrow')
    show_arrow.set('style', 'display:none')
    for e in group(r, 'bow').iter():
        if e.get('data-role') == 'bowstring':
            e.set('d', 'M-70 -400L-70 440')


# ---------- Brihannala: Arjuna in a woman's dress ----------
BRI = dict(skin=ARJ_SKIN, border='#7A2E6E', border_l='#A04890', utt=(GOLD, GOLD_D, GOLD_L), hair='braid')


def bri_base(bow=False, arms=True):
    t = ET.parse(C.SRC); r = t.getroot()
    if not bow:
        remove(r, 'bow')
    elif bow != 'draw':
        Wm_unstring(r)
    C.strip_gold(group(r, 'upper-body'))  # the necklace goes under the bodice; armlets and cuffs stay
    recolor(r, dict(zip(C.PANDU_SKIN, ARJ_SKIN)))
    if arms:
        C.arms_clasped(r)
    hide(r, 'leg-near'); hide(r, 'leg-far')
    ub = group(r, 'upper-body')
    ub.remove(group(r, 'uttariya'))
    torso = group(r, 'torso')
    for p in list(torso):
        if p.get('fill') in C.GOLDS or p.get('stroke') in C.GOLDS:
            torso.remove(p)
    idx = list(ub).index(torso) + 1
    for k, el in enumerate(frag(C.bodice(BRI, ARJ_SKIN) + C.drape('sash', BRI))):
        ub.insert(idx + k, el)
    head = group(r, 'head')
    ub.insert(list(ub).index(head), frag(C.hair('braid'))[0])
    # the face stays Arjuna's (male brows, his tilak); crown off, hair dressed, big gold earrings, kohl
    head.remove(group(r, 'crown'))
    group(r, 'hair-front').set('transform', 'translate(0 -4)')
    hide(r, 'earrings')
    head.extend(frag(f'<circle cx="450" cy="250" r="26" fill="none" stroke="{GOLD}" stroke-width="8" />'
                     f'<circle cx="450" cy="250" r="26" fill="none" stroke="{INK}" stroke-width="1.5" />'
                     f'<circle cx="450" cy="278" r="7" fill="{GOLD_D}" stroke="{INK}" stroke-width="1.5" />'))
    group(r, 'eyes-open').extend(frag(f'<path d="M516 179 Q537 166 560 176 L568 171" stroke="{INK}" stroke-width="3.5" />'))
    # a flower in the braid
    head.extend(frag('<circle cx="436" cy="196" r="10" fill="#FFF8E9" stroke="#291C23" stroke-width="2" />'
                     '<circle cx="424" cy="210" r="8" fill="#FFF8E9" stroke="#291C23" stroke-width="2" />'))
    dh = group(r, 'dhoti')
    for ch in list(dh):
        dh.remove(ch)
    dh.extend(frag(C.feet(ARJ_SKIN) + C.skirt(BRI)))
    # recolour the skirt: a deep plum antariya (not the women's cream) so Brihannala reads as a different person
    recolor(dh, {'#F3EEDF': '#8E4A86', '#E6DCC6': '#7A3C72', '#B7A68F': '#5E2A58', '#D6C7AF': '#A86AA0'})
    recolor(group(r, 'kanchuka'), {'#F3EEDF': '#8E4A86'})
    bangles(r, 'hand-far'); bangles(r, 'hand-near')
    return t, r


def brihannala():
    out = 'brihannala'
    t, r = bri_base()
    Wm.arms(r, far=(-2, 6, 0), near=(16, -146, 40))
    Wm.palm(r, 'hand-near', ARJ_SKIN)
    male_brows(r, 'calm'); smile(r)
    save(t, out, 'standing-graceful', 'Brihannala · standing, one hand at the chest')

    t, r = bri_base()
    Wm.arms(r, far=(-150, 30, -30), near=(40, -60, 10))
    Wm.palm(r, 'hand-far', ARJ_SKIN); Wm.palm(r, 'hand-near', ARJ_SKIN)
    male_brows(r, 'calm'); smile(r); tilt(r, -4)
    save(t, out, 'dance-teaching', 'Brihannala · teaching a dance, one hand raised in a mudra')

    t, r = bri_base()
    Wm.arms(r, far=(-150, -10, 0), near=(10, -40, 0))
    Wm.palm(r, 'hand-far', ARJ_SKIN)
    male_brows(r, 'calm'); tilt(r, -10)
    save(t, out, 'reaching-up', 'Brihannala · reaching up into the shami tree')

    # drawing the Gandiva: the rig's own bow-draw arms, kept; fierce
    t, r = bri_base(bow='draw', arms=False)
    male_brows(r, 'angry')
    save(t, out, 'drawing-gandiva', 'Brihannala · drawing the Gandiva')

    # the Gandiva raised high in one hand (bow vertical above the head), the other fist at the hip; calm
    t, r = bri_base(bow=False, arms=False)
    bow = copy.deepcopy(group(ET.parse(C.SRC).getroot(), 'bow'))
    for e in bow.iter():
        if e.get('id') == 'arrow':
            e.set('style', 'display:none')
        if e.get('data-role') == 'bowstring':
            e.set('d', 'M-70 -400L-70 440')
    Wm.arms(r, far=(-172, -8, 180), near=(10, -40, 0))
    group(r, 'hand-far').append(bow)
    male_brows(r, 'calm')
    save(t, out, 'gandiva-raised', 'Brihannala · the Gandiva raised high')


# ---------- Indra ----------
I_SKIN = ('#F4D6A6', '#E3BC86', '#BC9160')
I_DHOTI = {'#FFF8E9': '#E3A84A', '#F3EEDF': '#C98A2E', '#D6C7AF': '#A86E1E', '#B7A68F': '#7E4E12'}
I_SASH = {'#F3EEDF': '#B5402E', '#D6C7AF': '#8E2A20'}


def halo(r, cx=510, cy=175, rad=170):
    ub = group(r, 'upper-body')
    ub.insert(0, frag(f'<g id="halo"><circle cx="{cx}" cy="{cy}" r="{rad + 30}" fill="#FFE6B0" opacity="0.35" />'
                      f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="#FFF1D6" opacity="0.5" stroke="{GOLD}" stroke-width="12" />'
                      f'<circle cx="{cx}" cy="{cy}" r="{rad - 14}" fill="none" stroke="{GOLD_L}" stroke-width="4" />'
                      + ''.join(f'<path d="M{cx} {cy - rad - 6} l10 -22 l10 22Z" transform="rotate({a} {cx} {cy})" fill="{GOLD}" stroke="{INK}" stroke-width="2" />'
                                for a in range(0, 360, 20)) + '</g>')[0])


def indra():
    def base():
        t = ET.parse(C.SRC); r = t.getroot()
        remove(r, 'bow')
        for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
            recolor(group(r, g), I_DHOTI)
        recolor(group(r, 'uttariya'), I_SASH)
        recolor(r, dict(zip(C.PANDU_SKIN, I_SKIN)))
        cr = group(r, 'crown')
        cr.set('transform', 'translate(510 115) scale(1.12 1.35) translate(-510 -115)')
        halo(r)
        # abhaya: the far forearm raised, palm out; the near hand holds a small vajra at the hip
        Wm.arms(r, far=(-35, -125, -10), near=(10, -40, 0))
        Wm.palm(r, 'hand-far', I_SKIN)
        group(r, 'hand-near').extend(frag(
            f'<g transform="rotate(90)"><path d="M-70 0 L70 0" stroke="{GOLD_D}" stroke-width="14" />'
            f'<path d="M-70 0 l-26 -18 l6 18 l-6 18Z M70 0 l26 -18 l-6 18 l6 18Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
            f'<circle r="16" fill="{GOLD}" stroke="{INK}" stroke-width="3" /></g>'))
        return t, r
    t, r = base(); male_brows(r, 'calm'); smile(r)
    save(t, 'indra', 'standing-blessing', 'Indra · standing, blessing (abhaya)')
    t, r = base(); male_brows(r, 'up'); smile(r); tilt(r, 4)
    save(t, 'indra', 'standing-blessing', 'Indra · smiling warmly', 'smiling')


# ---------- Chitrasena ----------
CH_SKIN = ('#F2D0AC', '#DDB48A', '#B88A62')
CH_DHOTI = {'#FFF8E9': '#7FB0DE', '#F3EEDF': '#5B8FC9', '#D6C7AF': '#3E6FA8', '#B7A68F': '#2A4E7E'}
CH_SASH = {'#F3EEDF': '#F2A7B8', '#D6C7AF': '#D07A92'}


def veena():
    """A rudra-veena style instrument held diagonally across the body: two gourds, a long fretted neck."""
    frets = ''.join(f'<path d="M{430 + k * 26} {720 - k * 30} l12 10" stroke="{GOLD_L}" stroke-width="4" />' for k in range(9))
    return (f'<g id="veena">'
            f'<path d="M380 760 L720 380" stroke="#6E4228" stroke-width="30" />'
            f'<path d="M380 760 L720 380" stroke="#A86E48" stroke-width="18" />'
            f'{frets}'
            f'<path d="M386 756 L716 384" stroke="#FFF1D6" stroke-width="1.5" />'
            f'<circle cx="420" cy="790" r="74" fill="#C98A2E" stroke="{INK}" stroke-width="4" />'
            f'<circle cx="420" cy="790" r="50" fill="#A86E1E" />'
            f'<circle cx="690" cy="440" r="56" fill="#C98A2E" stroke="{INK}" stroke-width="4" />'
            f'<circle cx="690" cy="440" r="36" fill="#A86E1E" />'
            f'<path d="M716 384 q22 -26 8 -48 q-20 -6 -26 18" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
            f'</g>')


def chitrasena():
    t = ET.parse(C.SRC); r = t.getroot()
    remove(r, 'bow')
    for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
        recolor(group(r, g), CH_DHOTI)
    recolor(group(r, 'uttariya'), CH_SASH)
    recolor(r, dict(zip(C.PANDU_SKIN, CH_SKIN)))
    group(r, 'crown').set('transform', 'translate(510 115) scale(0.8) translate(-510 -115)')
    ubf = group(r, 'upper-body-front')
    ubf.insert(0, frag(veena())[0])
    Wm.arms(r, far=(-20, -125, -30), near=(-25, -40, 0))
    male_brows(r, 'up'); smile(r)
    save(t, 'chitrasena', 'playing-veena', 'Chitrasena · playing the veena')


# ---------- Urvashi and Uttara (the women's build) ----------
C.WOMEN['urvashi'] = dict(skin=('#F7DAB9', '#EBC39C', '#C99C74'), border=GOLD_D, border_l=GOLD,
                          utt=('#9B6BC7', '#7A4FA6', '#C9A2EC'), hair='braid')
C.WOMEN['uttara'] = dict(skin=('#F2CBA6', '#E0B088', '#BE8A62'), border='#2E8A8A', border_l='#4FB0B0',
                         utt=('#F2C14E', '#D49A2A', '#F8DA8A'), hair='braid')


def urvashi_base():
    t = C.build('urvashi', drape_style='sash', eye_scale=1.18, warmth=1)
    r = t.getroot()
    # court dress: rose antariya and bodice, gold borders, a tiara, a gold necklace over the bodice, jasmine in the braid
    recolor(group(r, 'dhoti'), {'#F3EEDF': '#F2B8CF', '#E6DCC6': '#E39CB9', '#B7A68F': '#B86A8E', '#D6C7AF': '#D88AAA'})
    recolor(group(r, 'kanchuka'), {'#F3EEDF': '#F2B8CF'})
    group(r, 'head').extend(frag(
        f'<path d="M458 116 Q520 88 602 118" stroke="{GOLD}" stroke-width="11" />'
        f'<path d="M458 116 Q520 88 602 118" stroke="{INK}" stroke-width="1.5" />'
        f'<circle cx="532" cy="98" r="11" fill="#B5402E" stroke="{GOLD}" stroke-width="4" />'
        f'<circle cx="450" cy="236" r="12" fill="{GOLD}" stroke="{INK}" stroke-width="2" />'))
    ub = group(r, 'upper-body')
    ub.extend(frag(f'<path d="M478 352 Q520 400 556 350" stroke="{GOLD}" stroke-width="9" />'
                   f'<circle cx="517" cy="392" r="10" fill="#B5402E" stroke="{GOLD}" stroke-width="4" />'))
    br = group(r, 'hair-braid')
    br.extend(frag(''.join(f'<circle cx="{440 + i * 4}" cy="{318 + i * 38}" r="6" fill="#FFF8E9" stroke="{INK}" stroke-width="1.5" />' for i in range(7))))
    bangles(r, 'hand-far', 2); bangles(r, 'hand-near', 2)
    return t, r


def urvashi():
    sk = C.WOMEN['urvashi']['skin']
    out = 'urvashi'
    # dancing: one arm curved overhead, the other extended behind at shoulder height; a gentle head tilt; smiling
    t, r = urvashi_base()
    Wm.arms(r, far=(-165, 45, 30), near=(95, -10, 90))
    Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk)
    female_brows(r, 'calm'); Wm.mouth(r, smile=True); tilt(r, -6)
    save(t, out, 'dancing', 'Urvashi · dancing')

    # walking at night toward Arjuna's door; hopeful
    t, r = urvashi_base()
    Wm.arms(r, far=(-12, -14, 0), near=(14, -40, 10))
    Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk)
    female_brows(r, 'up'); Wm.mouth(r, smile=True); Wm.feet_walking(r, sk)
    save(t, out, 'walking', 'Urvashi · walking, hopeful')

    # surprised, one hand at the chest (base) / hurt
    for expr, fn in ((None, lambda r: (female_brows(r, 'up'), Wm.mouth(r, open_=True))),
                     ('hurt', lambda r: (female_brows(r, 'sad'), tilt(r, 4)))):
        t, r = urvashi_base()
        Wm.arms(r, far=(-14, -10, 0), near=(16, -146, 40))
        Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk)
        fn(r)
        save(t, out, 'standing-surprised', 'Urvashi · standing, a hand at the chest' + (f', {expr}' if expr else ', surprised'), expr)

    # cursing: the far arm thrust forward and up, palm open toward him; furious
    t, r = urvashi_base()
    Wm.arms(r, far=(-118, -18, -14), near=(14, -40, 10))
    Wm.palm(r, 'hand-far', sk)
    female_brows(r, 'angry'); Wm.mouth(r, open_=True)
    save(t, out, 'cursing-hand-raised', 'Urvashi · cursing, palm raised')


def uttara():
    sk = C.WOMEN['uttara']['skin']
    t = C.build('uttara', drape_style='sash', eye_scale=1.22, head_scale=1.06, warmth=2)
    r = t.getroot()
    cp = group(r, 'canvas-placement')
    cp.set('transform', 'translate(500 1550) scale(0.86) translate(-500 -1550) ' + cp.get('transform'))
    recolor(group(r, 'dhoti'), {'#F3EEDF': '#FFF1D6'})
    Wm.arms(r, far=(-150, 30, -30), near=(40, -60, 10))
    Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk)
    Wm.brows(r, 'up'); Wm.mouth(r, smile=True); tilt(r, -4)
    save(t, 'uttara', 'dancing', 'Princess Uttara · dancing')


# ---------- character.json ----------
def character_json():
    cast = {
        'arjuna': dict(name={'en': 'Arjuna', 'hi': 'अर्जुन'}, role='Third Pandava; son of Indra and Kunti', divine=False,
                       look='A young prince "of darkish hue" (Virata §11): deep brown skin, gold crown, red dhoti, gold sash, gold armlets; the Gandiva bow.',
                       sourceNotes='Son of Indra (Adi §123). Complexion from Virata §11 ("young and of darkish hue"). The red dhoti is a design choice carried over from S01E02.',
                       poses=['standing-bow', 'bowing-eyes-closed', 'kneeling-folded-hands', 'dance-step'],
                       expressions=['calm', 'awed', 'worried', 'eyes-closed', 'earnest', 'shocked', 'surprised'],
                       appearsIn=['S01E02', 'S01E03']),
        'brihannala': dict(name={'en': 'Brihannala', 'hi': 'बृहन्नला'}, role='Arjuna in disguise during the year in hiding', divine=False,
                           look='Arjuna\'s face and build in a plum bodice and antariya with a gold sash; a long braid with a flower, large gold earrings, conch bangles over the bowstring scars.',
                           sourceNotes='Virata §2 (the plan: bangles, earrings, braid), §11 (arrival; dance teacher to Uttara), §38–45, §65 (the Gandiva, the battle). Dignified, never comic.',
                           poses=['standing-graceful', 'dance-teaching', 'reaching-up', 'drawing-gandiva', 'gandiva-raised'],
                           expressions=['calm', 'smiling', 'determined', 'fierce'], appearsIn=['S01E03']),
        'indra': dict(name={'en': 'Indra', 'hi': 'इन्द्र'}, role='King of the gods; Arjuna\'s father', divine=True,
                      look='Golden skin, a tall gold crown, a gold halo with rays, saffron-gold dhoti, crimson sash; the far hand raised in abhaya, a small vajra in the other.',
                      sourceNotes='Vana §44, §46. The colours are design choices.',
                      poses=['standing-blessing'], expressions=['proud', 'smiling'], appearsIn=['S01E03']),
        'chitrasena': dict(name={'en': 'Chitrasena', 'hi': 'चित्रसेन'}, role='King of the Gandharvas; Arjuna\'s teacher of music and dance', divine=True,
                           look='Fair, sky-blue dhoti, pink sash, a smaller crown; plays a two-gourd veena.',
                           sourceNotes='Vana §44. The instrument is a design choice.',
                           poses=['playing-veena'], expressions=['smiling'], appearsIn=['S01E03']),
        'urvashi': dict(name={'en': 'Urvashi', 'hi': 'उर्वशी'}, role='Foremost of the apsaras; wife of Pururavas, ancestress of the Kurus', divine=True,
                        look='Fair, rose bodice and antariya with gold borders, a violet sash, a gold tiara, necklace and bangles, jasmine in a long braid. Dignified court dress: nothing revealing (CLAUDE.md rule 2).',
                        sourceNotes='Vana §45–46 (vulgate), Adi §75. The colours are design choices.',
                        poses=['dancing', 'walking', 'standing-surprised', 'cursing-hand-raised'],
                        expressions=['smiling', 'hopeful', 'surprised', 'hurt', 'furious'], appearsIn=['S01E03']),
        'uttara': dict(name={'en': 'Uttara', 'hi': 'उत्तरा'}, role='Princess of Matsya, Virata\'s daughter; Brihannala\'s pupil, later Abhimanyu\'s wife', divine=False,
                       look='A young girl: cream antariya with a teal border, a yellow sash, a braid. Smaller than the adults.',
                       sourceNotes='Virata §11, §72.', poses=['dancing'], expressions=['joyful'], appearsIn=['S01E03']),
    }
    for cid, d in cast.items():
        files = {}
        for p in d['poses']:
            for f in sorted(os.listdir(f'{OUT}/{cid}')):
                if f.startswith(p) and f.endswith('.svg'):
                    files[f[:-4]] = f
        out = {'id': cid, **d, 'files': files, 'facing': 'per pose, see facingByPose (ear rule)',
               'facingByPose': {p: 'right' for p in d['poses']},
               'notes': 'Made in code by episodes/S01E03-urvashi-curses-arjuna/svg/make-cast.py from the pandu rig (the women via S01E02 make-concepts.py). All poses face right; mirror with flip.'}
        with open(f'{OUT}/{cid}/character.json', 'w') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print('wrote', f'{OUT}/{cid}/character.json')


if __name__ == '__main__':
    arjuna(); brihannala(); indra(); chitrasena(); urvashi(); uttara(); character_json()
