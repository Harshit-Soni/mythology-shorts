"""S01E06 cast, made in code from the library rigs (reuse before create). Builds on the S01E05 helpers.

Nahusha       <- king rig. Two looks: humble (plain cloth, small crown) and proud (violet and gold, tall crown, halo)
deva          <- pandu rig: one of the gods (unnamed): teal, crown, halo; offering, drained
Shachi        <- women's build: Indra's queen, turquoise and gold, tiara, halo
Agastya       <- mandavya rig: leaf-green bark cloth, darker skin
Bhima, Yudhishthira <- pandu rig in exile dress: topknot, no crown or gold. Bhima is broader

All poses face right (Nahusha's throne pose faces left, as in the king rig); scenes mirror with flip.
Run from the repo root:  python3 episodes/S01E06-nahusha-becomes-a-snake/svg/make-cast.py [out_dir]
"""
import importlib.util
import json
import os
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('c05', 'episodes/S01E05-karna-two-curses/svg/make-cast.py')
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)
sys.argv = _argv
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
F, M, C, Wm = K.F, K.M, K.C, K.Wm
group, frag, recolor, joint = C.group, C.frag, C.recolor, C.joint
NS, INK, GOLD, GOLD_D, GOLD_L = C.NS, C.INK, M.GOLD, M.GOLD_D, M.GOLD_L


def save(tree, cid, pose, title, expr=None):
    root = tree.getroot()
    root.set('data-character', cid)
    for tag, text in (('title', title), ('desc', f'{title}. S01E06, made by episodes/S01E06-nahusha-becomes-a-snake/svg/make-cast.py.')):
        e = root.find(NS + tag)
        if e is not None:
            e.text = text
    path = f'{OUT}/{cid}/{pose}__{expr}.svg' if expr else f'{OUT}/{cid}/{pose}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode')
    print('wrote', path)


def scale_crown(r, sx, sy):
    group(r, 'crown').set('transform', f'translate(510 115) scale({sx} {sy}) translate(-510 -115)')


# ---------- Nahusha (king rig) ----------
VIOLET = {'#B14B35': '#7E5BB0', '#8E2A20': '#5C3D8C', '#622B2B': '#3E2664', '#49252A': '#2A1848', '#2E6B4F': '#C9463A', '#204C3D': '#8E2A20'}
PLAIN = {'#B14B35': '#E8D6AE', '#8E2A20': '#CDB686', '#622B2B': '#A08A5C', '#49252A': '#7C6A44', '#2E6B4F': '#8E9AA8', '#204C3D': '#66727E'}
KING = 'assets/characters/king/'


def k_arms(r, far, near):
    joint(r, 'upper-arm-far', f'translate(635 390) rotate({far[0]})')
    joint(r, 'forearm-far', f'translate(0 225.610) rotate({far[1]})')
    joint(r, 'hand-far', f'translate(0 206.206) rotate({far[2]})')
    joint(r, 'upper-arm-near', f'translate(335 397) rotate({near[0]})')
    joint(r, 'forearm-near', f'translate(0 214.870) rotate({near[1]})')
    joint(r, 'hand-near', f'translate(0 242.128) rotate({near[2]})')


def face(r, mood):
    """The king rig's face is drawn furious or ashamed: redraw brows and mouth."""
    M.male_brows(r, mood)
    r_open, r_closed = group(r, 'mouth-open'), group(r, 'mouth-closed')
    r_open.set('style', 'display:none')
    r_closed.attrib.pop('style', None)


def nahusha():
    cid = 'nahusha'
    t = ET.parse(KING + 'seated-throne-pointing.svg'); r = t.getroot()
    recolor(r, VIOLET); face(r, 'calm'); scale_crown(r, 1.08, 1.25)
    M.halo(r)
    save(t, cid, 'seated-throne', 'Nahusha (proud) · on the throne of heaven, pointing')
    for expr in (None, 'serene'):
        t = ET.parse(KING + 'folded-hands.svg'); r = t.getroot()
        recolor(r, PLAIN); face(r, 'sad' if not expr else 'calm'); scale_crown(r, 0.72, 0.62)
        for g in ('torso', 'upper-body'):
            C.strip_gold(group(r, g))
        for e in list(group(r, 'upper-body')):  # the necklaces' dark outlines
            if (e.get('d') or '').startswith(('M444 348Q515', 'M427 365Q515')):
                group(r, 'upper-body').remove(e)
        group(r, 'head').set('transform', 'rotate(4 473 310)')
        if expr:
            M.eyes_closed(r)
        save(t, cid, 'humble', 'Nahusha (humble) · palms joined, a plain king' + (', serene' if expr else ''), expr)
    t = ET.parse(KING + 'folded-hands.svg'); r = t.getroot()
    recolor(r, VIOLET); face(r, 'calm'); scale_crown(r, 1.08, 1.25)
    k_arms(r, far=(-14, -10, 0), near=(22, -34, 0))
    group(r, 'head').set('transform', '')
    M.halo(r)
    group(r, 'eyes-open').extend(frag(
        '<circle cx="540" cy="180" r="34" fill="#FFE08A" opacity="0.5" /><circle cx="591" cy="180" r="22" fill="#FFE08A" opacity="0.5" />'
        '<circle cx="541" cy="180" r="11" fill="#FFF6C8" stroke="#E8B53A" stroke-width="4" /><circle cx="590" cy="180" r="7" fill="#FFF6C8" stroke="#E8B53A" stroke-width="3" />'))
    save(t, cid, 'gaze', 'Nahusha (proud) · the gaze that takes strength')


# ---------- a god ----------
D_SKIN = ('#F3D3A4', '#E0B988', '#B88E60')
D_DHOTI = {'#FFF8E9': '#5FB0A6', '#F3EEDF': '#3F8F88', '#D6C7AF': '#2C6E6A', '#B7A68F': '#1C4C4A'}
D_SASH = {'#F3EEDF': '#F2C9B0', '#D6C7AF': '#D49A80'}


def deva():
    t, r = F.pandu(D_SKIN, D_DHOTI, D_SASH); M.halo(r)
    Wm.arms(r, far=(-58, -34, -30), near=(-34, -64, -10)); Wm.palm(r, 'hand-far', D_SKIN); Wm.palm(r, 'hand-near', D_SKIN)
    M.male_brows(r, 'up')
    save(t, 'deva', 'offering', 'A god · offering the throne, hands out')
    t, r = F.pandu(D_SKIN, D_DHOTI, D_SASH); M.halo(r)
    group(r, 'halo').set('opacity', '0.3')
    Wm.arms(r, far=(-8, 6, 0), near=(14, 4, 0)); M.lean(r, 13); M.tilt(r, 18); M.male_brows(r, 'sad'); M.mouth_open(r)
    recolor(r, {'#F3D3A4': '#DCCBB2', '#E0B988': '#C2AE92', '#B88E60': '#978470', '#5FB0A6': '#8FA8A4', '#3F8F88': '#6E8885'})
    save(t, 'deva', 'drained', 'A god · his strength gone, sagging')


# ---------- Shachi ----------
C.WOMEN['shachi'] = dict(skin=('#F3CFA6', '#E2B588', '#BE8C62'), border=GOLD_D, border_l=GOLD, utt=('#E9C46A', '#C99A3A', '#F6DE9C'), hair='braid')


def shachi_base():
    t = C.build('shachi', drape_style='shawl', eye_scale=1.16, warmth=0)
    r = t.getroot()
    recolor(group(r, 'dhoti'), {'#F3EEDF': '#2E7E96', '#E6DCC6': '#256A80', '#B7A68F': '#174A5C', '#D6C7AF': '#4E9DB2'})
    recolor(group(r, 'kanchuka'), {'#F3EEDF': '#2E7E96'})
    M.halo(r)
    group(r, 'head').extend(frag(
        f'<path d="M456 122 L470 78 L494 106 L524 56 L554 104 L576 78 L598 122 Q526 98 456 122Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
        f'<circle cx="524" cy="98" r="10" fill="#C9463A" stroke="{INK}" stroke-width="2" /><circle cx="450" cy="240" r="12" fill="{GOLD}" stroke="{INK}" stroke-width="2" />'))
    group(r, 'upper-body').extend(frag(f'<path d="M478 352 Q520 402 556 350" stroke="{GOLD}" stroke-width="9" /><circle cx="517" cy="394" r="10" fill="#C9463A" stroke="{GOLD}" stroke-width="4" />'))
    M.bangles(r, 'hand-far', 2); M.bangles(r, 'hand-near', 2)
    return t, r


def shachi():
    sk = C.WOMEN['shachi']['skin']
    t, r = shachi_base(); M.female_brows(r, 'firm')
    save(t, 'shachi', 'standing-firm', 'Shachi · standing, composed, hands clasped')
    t, r = shachi_base(); Wm.arms(r, far=(-20, -118, 0), near=(16, -60, 10)); Wm.palm(r, 'hand-far', sk); M.female_brows(r, 'firm')
    save(t, 'shachi', 'speaking', 'Shachi · speaking, one hand raised')


# ---------- Agastya ----------
A_HAIR = ('#3A2E2A', '#5C4A40', '#84705F', '#CFC6B8', '#E4DCCF')
A_SKIN = ('#C98F5C', '#B07746', '#86552E')
BARK = ('#A9B86A', '#7F9248', '#586A2E', '#3A481C')


def agastya():
    t, r = K.sage(K.FURY, BARK, A_HAIR, A_SKIN); K.raised(r, -118, -38, 0, A_SKIN)
    save(t, 'agastya', 'cursing', 'Agastya · cursing, palm raised')
    t, r = K.sage(K.CALM, BARK, A_HAIR, A_SKIN); F.m_arms(r, far=(-20, -124, 10), near=(16, -10, 0)); Wm.palm(r, 'hand-far', A_SKIN)
    b = group(r, 'brows')
    for ch in list(b):
        b.remove(ch)
    b.extend(frag('<path d="M511 163 Q533 160 557 151 L559 157 Q535 168 515 170Z" fill="#5C4A40" /><path d="M583 152 L595 158 L595 164 L584 158Z" fill="#5C4A40" />'))
    save(t, 'agastya', 'softening', 'Agastya · his anger gone, a palm raised in blessing')
    t, r = K.sage(K.CALM, BARK, A_HAIR, A_SKIN); F.m_arms(r, far=(-34, -112, 0), near=(16, -10, 0)); pointing(r, 'hand-far', A_SKIN)
    b = group(r, 'brows')
    for ch in list(b):
        b.remove(ch)
    b.extend(frag('<path d="M509 150 Q533 154 560 170 L556 178 Q530 166 508 162Z" fill="#5C4A40" /><path d="M580 172 L598 158 L600 166 L584 179Z" fill="#5C4A40" />'))
    save(t, 'agastya', 'rebuking', 'Agastya · rebuking the king, one finger raised, stern')


def pointing(r, hand, skin):
    """One finger raised: the open palm's hand redrawn as a fist with the index finger up (the hand hangs along +y)."""
    Wm.palm(r, hand, skin)
    h = group(r, hand)
    for ch in list(h):
        h.remove(ch)
    a, b, _ = skin
    h.extend(frag(f'<path d="M-13 60 Q-16 128 -8 140 Q2 148 8 138 Q14 110 13 60Z" fill="{a}" stroke="{INK}" stroke-width="3" />'
                  f'<path d="M-26 -6 Q-36 40 -28 74 Q0 96 34 78 Q46 40 28 -6Z" fill="{a}" stroke="{INK}" stroke-width="3" />'
                  f'<path d="M2 76 Q4 60 2 46 M18 76 Q22 60 18 46" stroke="{b}" stroke-width="4" /><path d="M-30 30 Q-6 26 8 44 Q-4 58 -28 52Z" fill="{a}" stroke="{INK}" stroke-width="3" />'))


# ---------- Bhima and Yudhishthira, in exile ----------
def exile(skin, dhoti, sash):
    t, r = F.pandu(skin, dhoti, sash)
    for g in ('upper-body', 'upper-arm-far', 'upper-arm-near', 'forearm-far', 'forearm-near', 'hand-far', 'hand-near', 'torso'):
        C.strip_gold(group(r, g))
    recolor(group(r, 'uttariya'), {'#E8B53A': sash['#F3EEDF'], '#F4D17B': sash['#F3EEDF'], '#AF762C': sash['#D6C7AF']})
    head = group(r, 'head')
    head.remove(group(r, 'crown')); M.hide(r, 'earrings')
    for e in frag(f'<path d="M452 214 Q438 150 462 112 Q498 66 556 80 Q600 92 602 138 Q570 118 534 122 Q498 128 486 168 Q480 200 470 226Z" fill="#2C2326" stroke="{INK}" stroke-width="3" />'
                  f'<path d="M474 96 Q462 58 492 38 Q526 24 544 50 Q556 78 530 92 Q500 104 474 96Z" fill="#2C2326" stroke="{INK}" stroke-width="3" />'
                  f'<path d="M482 90 Q508 100 534 84" stroke="#B9855A" stroke-width="8" /><path d="M470 130 Q500 96 552 98 M492 54 Q512 40 532 54" stroke="#574648" stroke-width="3" />'):
        head.append(e)
    return t, r


BH_SKIN = ('#E0AA74', '#C88E58', '#9C673A')
BH_DHOTI = {'#FFF8E9': '#B98A58', '#F3EEDF': '#976A3E', '#D6C7AF': '#744E2A', '#B7A68F': '#50341A'}
BH_SASH = {'#F3EEDF': '#6A7F4A', '#D6C7AF': '#4A5C30'}
YU_SKIN = ('#F0CDA4', '#DBB287', '#B58960')
YU_DHOTI = {'#FFF8E9': '#F4EAD2', '#F3EEDF': '#E2D4B4', '#D6C7AF': '#C4B28C', '#B7A68F': '#98865F'}
YU_SASH = {'#F3EEDF': '#8AA0B8', '#D6C7AF': '#627A94'}


def broad(r):
    """Bhima: wider and a little taller than his brothers, with a moustache."""
    cp = group(r, 'canvas-placement')
    cp.set('transform', 'translate(500 1550) scale(1.22 1.04) translate(-500 -1550) ' + cp.get('transform'))
    group(r, 'head').set('transform', 'translate(510 310) scale(0.9 1) translate(-510 -310)')
    group(r, 'head').extend(frag('<path d="M546 236 Q566 228 590 234 Q604 238 606 228 Q600 246 584 244 Q564 242 546 248Z" fill="#2C2326" />'))


def bhima():
    for expr in (None, 'weak'):
        t, r = exile(BH_SKIN, BH_DHOTI, BH_SASH); Wm.arms(r, far=(-4, 4, 0), near=(6, -6, 0))
        if expr:
            K.worry(r); M.eyes_closed(r); M.tilt(r, 10)
        else:
            K.strain(r)
        broad(r)
        save(t, 'bhima', 'held', 'Bhima (exile) · arms pinned' + (', his strength gone' if expr else ', straining'), expr)
    t, r = exile(BH_SKIN, BH_DHOTI, BH_SASH); Wm.arms(r, far=(-30, -60, -20), near=(16, -60, 0)); Wm.palm(r, 'hand-far', BH_SKIN)
    M.male_brows(r, 'up'); M.mouth_open(r); broad(r)
    save(t, 'bhima', 'freed', 'Bhima (exile) · free, awed')


def yudhishthira():
    t, r = exile(YU_SKIN, YU_DHOTI, YU_SASH); Wm.arms(r, far=(-70, -14, -20), near=(16, -40, 0)); Wm.palm(r, 'hand-far', YU_SKIN); M.male_brows(r, 'up'); M.mouth_open(r)
    save(t, 'yudhishthira', 'arriving', 'Yudhishthira (exile) · arriving, alarmed, a hand out')
    t, r = exile(YU_SKIN, YU_DHOTI, YU_SASH); Wm.arms(r, far=(-28, -112, -6), near=(12, -40, 0)); Wm.palm(r, 'hand-far', YU_SKIN); M.male_brows(r, 'calm')
    save(t, 'yudhishthira', 'answering', 'Yudhishthira (exile) · answering, a calm palm raised')


def character_json():
    cast = {
        'nahusha': dict(name={'en': 'Nahusha', 'hi': 'नहुष'}, role='The human king made lord of heaven; ancestor of the Pandavas', divine=False,
                        look='The king rig. Humble: plain cream cloth, grey sash, a small crown, no necklace. Proud: violet and gold, red sash, a tall crown, a halo (the glory he loses at the curse).',
                        sourceNotes='CE 5.11–17; 3.175–178.', poses=['seated-throne', 'humble', 'gaze'], expressions=['serene'], facing={'seated-throne': 'left'}),
        'deva': dict(name={'en': 'A god', 'hi': 'एक देवता'}, role='One of the gods of heaven (unnamed)', divine=True, look='Fair gold skin, teal dhoti, crown, halo. Drained: greyed, halo faded.',
                     sourceNotes='CE 5.11.1–6.', poses=['offering', 'drained']),
        'shachi': dict(name={'en': 'Shachi (Indrani)', 'hi': 'शची (इन्द्राणी)'}, role='Indra’s queen', divine=True, look='Turquoise and gold, a gold shawl, a tiara, a halo, a braid. Composed and resolute, never alluring.',
                       sourceNotes='CE 5.11–15.', poses=['standing-firm', 'speaking']),
        'agastya': dict(name={'en': 'Agastya', 'hi': 'अगस्त्य'}, role='The sage who curses Nahusha', divine=False, look='The sage rig in leaf-green bark cloth, brown hair with grey, darker skin.',
                        sourceNotes='CE 5.17; 3.178.37–40.', poses=['cursing', 'softening', 'rebuking']),
        'bhima': dict(name={'en': 'Bhima', 'hi': 'भीम'}, role='The second Pandava, strongest of men', divine=False, look='Exile dress: topknot, no crown or gold, brown bark cloth, a green sash. Broad, with a moustache.',
                      sourceNotes='CE 3.175–176.', poses=['held', 'freed'], expressions=['weak']),
        'yudhishthira': dict(name={'en': 'Yudhishthira', 'hi': 'युधिष्ठिर'}, role='The eldest Pandava, king of dharma', divine=False, look='Exile dress: topknot, no crown or gold, pale cloth, a grey-blue sash. Fair and calm.',
                             sourceNotes='CE 3.177–178.', poses=['arriving', 'answering']),
    }
    for cid, d in cast.items():
        files = {f[:-4]: f for f in sorted(os.listdir(f'{OUT}/{cid}')) if f.endswith('.svg')}
        fac = d.pop('facing', {})
        out = {'id': cid, **d, 'appearsIn': ['S01E06'], 'files': files, 'facing': 'per pose, see facingByPose (ear rule)', 'facingByPose': {p: fac.get(p, 'right') for p in d['poses']},
               'notes': 'Made in code by episodes/S01E06-nahusha-becomes-a-snake/svg/make-cast.py. Mirror with flip.'}
        json.dump(out, open(f'{OUT}/{cid}/character.json', 'w'), ensure_ascii=False, indent=2)
        print('wrote', f'{OUT}/{cid}/character.json')


if __name__ == '__main__':
    nahusha(); deva(); shachi(); agastya(); bhima(); yudhishthira(); character_json()
