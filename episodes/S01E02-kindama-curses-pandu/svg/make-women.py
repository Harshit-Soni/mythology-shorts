"""Kunti's and Madri's S01E02 poses, from the approved concept C (svg/04-concept-brief.md → Decisions).

Builds on make-concepts.py (the pandu rig re-dressed): this file only re-poses the arms, swaps in open palms,
sets each pose's face, and adds the babies. Every pose faces right; the renderer mirrors where a scene needs it.
Run from the repo root:  python3 episodes/S01E02-kindama-curses-pandu/svg/make-women.py [out_dir]
"""
import copy
import importlib.util
import json
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('concepts', os.path.join(HERE, 'make-concepts.py'))
C = importlib.util.module_from_spec(spec)
sys.argv, _argv = sys.argv[:1], sys.argv
spec.loader.exec_module(C)
sys.argv = _argv
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
INK = C.INK
group, frag, joint = C.group, C.frag, C.joint
NS = C.NS

CONCEPT_C = {'kunti': dict(drape_style='shawl', eye_scale=1.1, use_veil=True),
             'madri': dict(drape_style='sash', eye_scale=1.18, warmth=2)}
MANDAVYA_SKIN = ('#E5A66B', '#CF8D55', '#AB653C')  # light, mid, shade


def arms(r, far, near):
    """(upper, forearm, hand) rotations; 0 = hanging down, + = toward the left. The near forearm is the rig's
    stretched one, shortened to normal length (see make-concepts.arms_clasped)."""
    joint(r, 'upper-arm-far', f'translate(635 390) rotate({far[0]})')
    joint(r, 'forearm-far', f'translate(0 127.769) rotate({far[1]})')
    joint(r, 'hand-far', f'translate(0 116.297) rotate({far[2]})')
    joint(r, 'upper-arm-near', f'translate(335 397) rotate({near[0]})')
    joint(r, 'forearm-near', f'translate(0 148.708) rotate({near[1]}) scale(1 0.36)')
    joint(r, 'hand-near', f'translate(0 407.620) scale(1 2.7778) rotate({near[2]})')


def palm(r, gid, skin, thread=False, narrow=False):
    """Swap the gripping fist for Mandavya's open palm, in this woman's skin. narrow=True closes the fingers
    (a side-on flat hand, for palms pressed together)."""
    src = ET.parse('assets/characters/mandavya/cursing-hand-raised.svg').getroot()
    p = group(src, 'hand-near')
    dst = group(r, gid)
    for ch in list(dst):
        if ch.tag != NS + 'g':
            dst.remove(ch)
    m = dict(zip(MANDAVYA_SKIN, skin))
    i = 0
    for ch in p:
        if ch.tag == NS + 'g' or (ch.get('fill') or '').upper() in ('#7D3D27', '#B36A3C', '#C8814A'):
            continue
        ch = copy.deepcopy(ch)
        for e in ch.iter():
            for a in ('fill', 'stroke'):
                v = (e.get(a) or '').upper()
                if v in m:
                    e.set(a, m[v])
        dst.insert(i, ch)
        i += 1
    if narrow:
        g = ET.SubElement(dst, NS + 'g', {'transform': 'scale(0.42 1)'})
        for ch in [c for c in list(dst) if c.tag != NS + 'g' or c is g][:-1]:
            dst.remove(ch)
            g.append(ch)
    if thread:
        dst.extend(frag('<path d="M-24 -8 Q0 -16 24 -8" stroke="#B5402E" stroke-width="4" />'))


def brows(r, mood):
    shapes = {
        'calm': ('M514 166 Q535 150 560 160', 'M582 160 Q590 153 598 158'),
        'sad': ('M514 164 Q537 162 560 150', 'M582 151 Q590 154 598 160'),       # inner ends (by the nose) raised
        'up': ('M514 158 Q535 140 560 150', 'M582 150 Q590 143 598 148'),        # raised high: hope, fear, joy
        'firm': ('M514 162 Q537 156 560 158', 'M582 158 Q590 156 598 158'),      # level: resolve
    }[mood]
    b = group(r, 'brows')
    for ch in list(b):
        b.remove(ch)
    b.extend(frag(f'<path d="{shapes[0]}" stroke="#3C3031" stroke-width="5" />'
                  f'<path d="{shapes[1]}" stroke="#3C3031" stroke-width="4" />'))


def mouth(r, open_=False, smile=False):
    C.group(r, 'mouth-open').attrib.pop('style', None) if open_ else C.group(r, 'mouth-open').set('style', 'display:none')
    mc = group(r, 'mouth-closed')
    if open_:
        mc.set('style', 'display:none')
    if smile:
        mc.extend(frag('<path d="M556 246 Q574 262 593 241" stroke="#291C23" stroke-width="2.5" />'))


def head_tilt(r, deg):
    group(r, 'head').set('transform', f'rotate({deg} 510 310)')


def eyes_up(r, dy=-3):
    e = group(r, 'eyes-open')
    e.set('transform', (e.get('transform') or '') + f' translate(0 {dy})')


def baby(cx, cy, skin, s=1.0, rot=-12):
    """A baby wrapped in a cream cloth, face at the right end (toward the mother's face)."""
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
            f'<ellipse cx="0" cy="0" rx="86" ry="50" fill="#FFF8E9" stroke="{INK}" stroke-width="3.5" />'
            f'<path d="M-70 -10 Q-10 10 50 -30 M-60 22 Q0 34 60 6" stroke="#D6C7AF" stroke-width="4" />'
            f'<path d="M30 -46 Q86 -60 98 -6 Q92 36 52 40 Z" fill="#F3EEDF" stroke="{INK}" stroke-width="3" />'
            f'<circle cx="66" cy="-6" r="27" fill="{skin[0]}" stroke="{INK}" stroke-width="3" />'
            f'<path d="M58 -10 Q62 -6 66 -10 M74 -10 Q78 -6 82 -10" stroke="{INK}" stroke-width="2.5" />'
            f'<path d="M66 6 Q71 10 76 6" stroke="#B5534A" stroke-width="2.5" />'
            f'<circle cx="60" cy="2" r="5" fill="#E8A090" opacity="0.6" />'
            f'</g>')


def add_front(r, xml, before_arms=True):
    """Insert into upper-body-front: before the arms (so the arms wrap around it) or after them."""
    ubf = group(r, 'upper-body-front')
    els = frag(xml)
    if before_arms:
        for k, el in enumerate(els):
            ubf.insert(k, el)
    else:
        ubf.extend(els)


def turn_head_back(r):
    """Madri looks back over her shoulder: the head mirrored at the neck (the ear rule then puts her face left)."""
    h = group(r, 'head')
    h.set('transform', 'translate(1020 0) scale(-1 1)')
    # her braid follows the back of the head, now on the right
    br = group(r, 'hair-braid')
    br.set('transform', 'translate(1015 0) scale(-1 1)')


def feet_walking(r, skin):
    f = group(r, 'feet')
    f.set('transform', 'translate(30 0)')


def save(tree, name, pose, title):
    root = tree.getroot()
    root.set('data-character', name)
    t = root.find(NS + 'title')
    if t is not None:
        t.text = title
    d = root.find(NS + 'desc')
    if d is not None:
        d.text = f'{title}. S01E02, built from the pandu rig by episodes/S01E02-kindama-curses-pandu/svg/make-women.py (concept C).'
    path = f'{OUT}/{name}/{pose}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode')
    print('wrote', path)


def new(name):
    t = C.build(name, **CONCEPT_C[name])
    return t, t.getroot(), C.WOMEN[name]['skin']


def kunti():
    # s06: standing, hands clasped low, head bowed, sad
    t, r, sk = new('kunti')
    head_tilt(r, 5); brows(r, 'sad')
    save(t, 'kunti', 'standing-sad', 'Kunti · standing, sad')

    # s07: palms pressed together at the chest, eyes lifted, hopeful
    t, r, sk = new('kunti')
    arms(r, far=(10, 117, 53), near=(-15, -116, -49))
    palm(r, 'hand-far', sk, narrow=True); palm(r, 'hand-near', sk, thread=True, narrow=True)
    brows(r, 'up'); eyes_up(r); head_tilt(r, -4)
    save(t, 'kunti', 'folded-hands', 'Kunti · palms together, hopeful')

    # s08, s09: cradling baby Yudhishthira, joyful
    t, r, sk = new('kunti')
    arms(r, far=(8, 82, 20), near=(-5, -99, -20))
    add_front(r, baby(515, 470, sk))
    brows(r, 'up'); mouth(r, smile=True); head_tilt(r, 6)
    save(t, 'kunti', 'holding-baby', 'Kunti · holding a baby, joyful')

    # s11: arms spread low and wide, holding the children back; grieving, crying out
    t, r, sk = new('kunti')
    arms(r, far=(14, 112, 40), near=(58, 6, 20))
    palm(r, 'hand-far', sk); palm(r, 'hand-near', sk, thread=True)
    brows(r, 'sad'); mouth(r, open_=True)
    save(t, 'kunti', 'holding-back', 'Kunti · holding the children back, grieving')


def madri():
    # s06: one hand at her chest, the other hanging, head bowed
    t, r, sk = new('madri')
    arms(r, far=(-2, 6, 0), near=(16, -146, 40))
    palm(r, 'hand-near', sk, thread=True)
    head_tilt(r, 5); brows(r, 'sad')
    save(t, 'madri', 'standing-sad', 'Madri · standing, sad')

    # s09: the twins, one in each arm, joyful
    t, r, sk = new('madri')
    arms(r, far=(8, 82, 20), near=(-5, -99, -20))
    add_front(r, baby(455, 452, sk, 0.78, -24))
    add_front(r, baby(560, 540, sk, 0.78, -4), before_arms=False)
    brows(r, 'up'); mouth(r, smile=True)
    save(t, 'madri', 'holding-twins', 'Madri · holding the twins, joyful')

    # s10: walking away to the right, looking back over her shoulder, a hand raised back toward Pandu: "stop"; afraid
    t, r, sk = new('madri')
    arms(r, far=(-14, -6, 0), near=(92, -8, 95))
    palm(r, 'hand-near', sk, thread=True)
    turn_head_back(r)
    brows(r, 'up'); mouth(r, open_=True)
    feet_walking(r, sk)
    save(t, 'madri', 'turning-away', 'Madri · turning away, a hand raised to stop him, afraid')

    # s11: walking toward the pyre, palms together at the chest, resolute (shown as a silhouette)
    t, r, sk = new('madri')
    arms(r, far=(10, 117, 53), near=(-15, -116, -49))
    palm(r, 'hand-far', sk, narrow=True); palm(r, 'hand-near', sk, thread=True, narrow=True)
    brows(r, 'firm')
    feet_walking(r, sk)
    save(t, 'madri', 'walking', 'Madri · walking, palms together, resolute')


def character_json():
    common = {
        'appearsIn': ['S01E02'], 'divine': False, 'facing': 'per pose, see facingByPose (ear rule)',
        'notes': ('Built from the pandu rig (same head construction and joint pivots; legs hidden under the antariya) by '
                  'episodes/S01E02-kindama-curses-pandu/svg/make-women.py, concept C. All poses face right; mirror in the '
                  'scene with flip. No gold: Pandu gave his wives\' ornaments away (Adi §119).'),
    }
    data = {
        'kunti': dict(name={'en': 'Kunti', 'hi': 'कुन्ती'}, role='Pandu\'s elder wife; mother of Yudhishthira, Bhima and Arjuna (and Karna)',
                      look='About 30, composed and strong. Warm medium-brown skin. Cream bodice and antariya with a maroon border; an ochre uttariya worn over her head as a veil. Red thread, bindi, no gold.',
                      sourceNotes='Born Pritha of the Yadavas, adopted by Kuntibhoja (Adi §111). The veil and colours are design choices (concept C).',
                      poses=['standing-sad', 'folded-hands', 'holding-baby', 'holding-back'],
                      expressions=['sad', 'hopeful', 'joyful', 'grieving'],
                      palette={'skin': '#D29A68', 'garment': '#F3EEDF', 'border': '#8E2A20', 'uttariya': '#C98A2E'}),
        'madri': dict(name={'en': 'Madri', 'hi': 'माद्री'}, role='Pandu\'s younger wife; mother of Nakula and Sahadeva',
                      look='About 22, gentle but determined. Lighter warm skin. Cream bodice and antariya with a teal border; a saffron uttariya over one shoulder; a long braid. Red thread, bindi, no gold.',
                      sourceNotes='Princess of the Madras (Adi §124–125). The text says she resisted Pandu at his death (§125): nothing in her design suggests otherwise.',
                      poses=['standing-sad', 'holding-twins', 'turning-away', 'walking'],
                      expressions=['sad', 'joyful', 'afraid', 'resolute'],
                      palette={'skin': '#E3B48A', 'garment': '#F3EEDF', 'border': '#2E6B4F', 'uttariya': '#E07A2E'}),
    }
    for cid, d in data.items():
        facing = {p: 'right' for p in d['poses']}
        if cid == 'madri':
            facing['turning-away'] = 'body right, head looking back left (mirrored head)'
        out = {'id': cid, **d, **common, 'files': {p: f'{p}.svg' for p in d['poses']}, 'facingByPose': facing}
        with open(f'{OUT}/{cid}/character.json', 'w') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print('wrote', f'{OUT}/{cid}/character.json')


if __name__ == '__main__':
    kunti(); madri(); character_json()
