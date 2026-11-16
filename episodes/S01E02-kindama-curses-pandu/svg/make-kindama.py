"""Kindama (S01E02), lying on the ground, built from the mandavya rig.

The standing rig is laid down by rotating its lower body (legs + dhoti) and upper body about the hip by
different amounts: legs flat along the ground, the torso propped up on the near elbow, the head turned
back upright. Then the sage is made younger (black jata and a short dark beard), the dhoti turns
ochre-brown, and a spotted deerskin goes over his shoulder (his deer form).
Run from the repo root:  python3 episodes/S01E02-kindama-curses-pandu/svg/make-kindama.py [out_dir]
"""
import json
import os
import sys
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
NS = '{%s}' % SVG
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
INK = '#1E1420'
HIP = (510, 700)

HAIR = {'#A8A39A': '#3C3031', '#CBC4B4': '#4A3D3C', '#8F887C': '#2E2628', '#DAD4C8': '#55464A', '#F2EEE6': '#5E4E50', '#FFFFFF': '#5E4E50'}
DHOTI = {'#F6A13E': '#C9944A', '#E68129': '#B07A36', '#BC5420': '#8A5A24', '#9E451F': '#6E4519'}


def group(root, gid):
    for e in root.iter():
        if e.get('id') == gid:
            return e
    raise KeyError(gid)


def frag(xml):
    els = list(ET.fromstring(f'<g xmlns="{SVG}">{xml}</g>'))
    for el in els:
        for e in el.iter():
            if e.tag == NS + 'path' and e.get('stroke') and e.get('fill') is None:
                e.set('fill', 'none')
    return els


def recolor(el, m):
    m = {k.upper(): v for k, v in m.items()}
    for e in el.iter():
        for a in ('fill', 'stroke'):
            v = (e.get(a) or '').upper()
            if v in m:
                e.set(a, m[v])


def prepend(el, t):
    el.set('transform', (t + ' ' + (el.get('transform') or '')).strip())
    if el.get('data-base-transform') is not None:
        el.set('data-base-transform', el.get('transform'))


def joint(root, gid, t):
    g = group(root, gid)
    g.set('transform', t)
    g.set('data-base-transform', t)


def deerskin():
    spots = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="6" fill="#F3E6C8" />'
                    for x, y in ((600, 420), (628, 470), (590, 500), (640, 530), (612, 560), (575, 455)))
    return (f'<g id="deerskin"><path d="M548 372 Q610 350 660 392 Q676 470 668 560 Q650 610 610 618 '
            f'Q590 590 560 600 Q570 520 548 440Z" fill="#A86B3C" stroke="{INK}" stroke-width="3.5" />'
            f'<path d="M560 600 Q548 640 520 650 M668 560 Q690 600 684 640" stroke="#7A4A26" stroke-width="7" />'
            f'{spots}</g>')


def arrow_at(x, y, rot):
    return (f'<g id="arrow" transform="translate({x} {y}) rotate({rot})">'
            f'<path d="M0 0 L-150 0" stroke="{INK}" stroke-width="11" /><path d="M0 0 L-150 0" stroke="#E8B53A" stroke-width="6" />'
            f'<path d="M-150 0 L-182 -16 L-168 0 L-182 16Z" fill="#F4D17B" stroke="{INK}" stroke-width="3" />'
            f'<path d="M-130 0 L-160 -16 L-146 0 L-160 16Z" fill="#F4D17B" stroke="{INK}" stroke-width="3" /></g>')


def make_younger(r):
    recolor(r, HAIR)
    beard = group(r, 'beard')
    beard.set('transform', 'translate(0 205) scale(1 0.62) translate(0 -205)')


def lay_down(r, legs_rot, torso_rot, head_rot, place):
    # bring the standing stance's legs together first, so both lie along the ground
    prepend(group(r, 'leg-near'), 'rotate(-16 395 792)')
    prepend(group(r, 'leg-far'), 'rotate(4 574 792)')
    for gid in ('leg-far', 'leg-near', 'dhoti'):
        prepend(group(r, gid), f'rotate({legs_rot} {HIP[0]} {HIP[1]})')
    for gid in ('upper-body', 'upper-body-front'):
        prepend(group(r, gid), f'rotate({torso_rot} {HIP[0]} {HIP[1]})')
    prepend(group(r, 'head'), f'rotate({head_rot} 510 330)')
    group(r, 'canvas-placement').set('transform', place)


def kindama_common(r):
    make_younger(r)
    recolor(group(r, 'dhoti'), DHOTI)
    ub = group(r, 'upper-body')
    torso = group(r, 'torso')
    idx = list(ub).index(torso) + 1
    for k, el in enumerate(frag(deerskin())):
        ub.insert(idx + k, el)


def save(t, pose, title, expression):
    root = t.getroot()
    root.set('data-character', 'kindama')
    root.set('data-expression', expression)
    tt = root.find(NS + 'title')
    if tt is not None:
        tt.text = title
    d = root.find(NS + 'desc')
    if d is not None:
        d.text = f'{title}. S01E02, built from the mandavya rig by episodes/S01E02-kindama-curses-pandu/svg/make-kindama.py.'
    path = f'{OUT}/kindama/{pose}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    t.write(path, encoding='unicode')
    print('wrote', path)


PLACE = 'translate(250 930) scale(0.66)'


def lying_wounded():
    t = ET.parse('assets/characters/mandavya/standing-calm.svg'); r = t.getroot()
    kindama_common(r)
    # near arm props him up (elbow and forearm on the ground); far hand pressed to his side by the arrow
    joint(r, 'upper-arm-near', 'translate(335 397) rotate(-38)')
    joint(r, 'forearm-near', 'translate(0 209.029) rotate(-62)')
    joint(r, 'upper-arm-far', 'translate(635 390) rotate(-4)')
    joint(r, 'forearm-far', 'translate(0 210.523) rotate(60)')
    group(r, 'mouth-open').attrib.pop('style', None)
    group(r, 'mouth-closed').set('style', 'display:none')
    b = group(r, 'brows')
    b.set('transform', 'rotate(8 540 180)')
    ub = group(r, 'upper-body')
    lay_down(r, 86, 52, -40, PLACE)
    r.extend(frag(arrow_at(596, 1404, 112)))  # canvas space: in his side at the hip, shaft and feathers sticking up
    save(t, 'lying-wounded', 'Kindama · lying wounded', 'pained')


def cursing_from_ground():
    t = ET.parse('assets/characters/mandavya/cursing-hand-raised.svg'); r = t.getroot()
    kindama_common(r)
    # pushed up on the far hand; the near arm raised high, palm open, toward the right
    joint(r, 'upper-arm-near', 'translate(335 397) rotate(-168)')
    joint(r, 'forearm-near', 'translate(0 214.238) rotate(8)')
    joint(r, 'upper-arm-far', 'translate(635 390) rotate(-26)')
    joint(r, 'forearm-far', 'translate(0 215.205) rotate(-30)')
    ub = group(r, 'upper-body')
    lay_down(r, 86, 32, -24, PLACE)
    r.extend(frag(arrow_at(596, 1404, 112)))
    save(t, 'cursing-from-ground', 'Kindama · cursing from the ground', 'furious')


def character_json():
    d = {'id': 'kindama', 'name': {'en': 'Kindama', 'hi': 'किन्दम'},
         'role': 'A sage who lived in the forest in a deer\'s form; cursed Pandu (Adi Parva §118)',
         'divine': False, 'appearsIn': ['S01E02'],
         'look': 'A younger sage (~35): black jata in a top knot, a short dark beard, tripundra, rudraksha, an ochre-brown dhoti and a spotted deerskin over his shoulder.',
         'sourceNotes': '"A Rishi\'s son of great ascetic merit", a muni living on fruit and roots, in a deer\'s form out of modesty (Adi §118). No physical description in the text; the deerskin is a design nod to his deer form.',
         'poses': ['lying-wounded', 'cursing-from-ground'], 'expressions': ['pained', 'furious'],
         'files': {'lying-wounded': 'lying-wounded.svg', 'cursing-from-ground': 'cursing-from-ground.svg'},
         'facing': 'per pose, see facingByPose (ear rule)',
         'facingByPose': {'lying-wounded': 'right (head to the right)', 'cursing-from-ground': 'right (head to the right)'},
         'notes': 'Built from the mandavya rig (lower and upper body rotated about the hip) by episodes/S01E02-kindama-curses-pandu/svg/make-kindama.py. In S01E02 he is flipped so he faces Pandu on the left.'}
    with open(f'{OUT}/kindama/character.json', 'w') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print('wrote', f'{OUT}/kindama/character.json')


if __name__ == '__main__':
    lying_wounded(); cursing_from_ground(); character_json()
