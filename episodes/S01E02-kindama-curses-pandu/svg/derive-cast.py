"""Build S01E02's derived cast from the library rigs (reuse before create).

Pandu  <- pandu/drawing-bow: arms re-posed at their joint pivots, bow lowered or removed.
           standing-shocked, removing-crown, reaching
Arjuna <- pandu/drawing-bow recoloured (tease only; his full design comes with E03's research)

Run from the repo root:  python3 episodes/S01E02-kindama-curses-pandu/svg/derive-cast.py
"""
import copy
import os
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
NS = '{%s}' % SVG
LIB = 'assets/characters'
SRC = f'{LIB}/pandu/drawing-bow.svg'

NEAR_FOREARM = 0.36  # the drawing arm's forearm is stretched to 407 px for the bow draw; shorten it to a normal ~147


def load():
    return ET.parse(SRC)


def group(root, gid):
    for e in root.iter():
        if e.get('id') == gid:
            return e
    raise KeyError(gid)


def parent_of(root, el):
    for p in root.iter():
        if el in list(p):
            return p
    raise KeyError(el)


def show(root, gid, visible):
    g = group(root, gid)
    if visible:
        g.attrib.pop('style', None)
    else:
        g.set('style', 'display:none')


def joint(root, gid, tx, ty, rot, extra=''):
    t = f'translate({tx} {ty}) {extra} rotate({rot})'.replace('  ', ' ')
    g = group(root, gid)
    g.set('transform', t)
    g.set('data-base-transform', t)


def pose_arms(root, far, near, far_shoulder=(635, 390), near_shoulder=(335, 397)):
    """far / near = (upper, forearm, hand) rotations in degrees (0 = hanging straight down, + = toward the left)."""
    joint(root, 'upper-arm-far', *far_shoulder, far[0])
    joint(root, 'forearm-far', 0, 127.769, far[1])
    joint(root, 'hand-far', 0, 116.297, far[2])
    joint(root, 'upper-arm-near', *near_shoulder, near[0])
    g = group(root, 'forearm-near')
    t = f'translate(0 148.708) rotate({near[1]}) scale(1 {NEAR_FOREARM})'
    g.set('transform', t)
    g.set('data-base-transform', t)
    h = group(root, 'hand-near')
    t = f'translate(0 407.620) scale(1 {1 / NEAR_FOREARM:.4f}) rotate({near[2]})'
    h.set('transform', t)
    h.set('data-base-transform', t)


def unstring_bow(root):
    """Lowered bow: no arrow, string straight between the tips."""
    show(root, 'arrow', False)
    for e in group(root, 'bow').iter():
        if e.get('data-role') == 'bowstring':
            e.set('d', 'M-70 -400L-70 440')


def remove_bow(root):
    bow = group(root, 'bow')
    parent_of(root, bow).remove(bow)


MANDAVYA_TO_PANDU_SKIN = {'#CF8D55': '#E8CEAC', '#AB653C': '#C6A382', '#E5A66B': '#F6E3C5'}


def open_hand(root, gid):
    """Swap a gripping fist for Mandavya's open palm (his raised cursing hand), recoloured to Pandu's skin."""
    src = ET.parse(f'{LIB}/mandavya/cursing-hand-raised.svg').getroot()
    palm = group(src, 'hand-near')
    dst = group(root, gid)
    for c in list(dst):
        if c.tag != NS + 'g':
            dst.remove(c)
    for i, c in enumerate(e for e in palm if e.tag != NS + 'g'):
        c = copy.deepcopy(c)
        if c.get('fill', '').upper() in ('#7D3D27', '#B36A3C', '#C8814A'):
            continue  # rudraksha bracelet: Mandavya's, not Pandu's
        for e in c.iter():
            for a in ('fill', 'stroke'):
                v = e.get(a)
                if v and v.upper() in MANDAVYA_TO_PANDU_SKIN:
                    e.set(a, MANDAVYA_TO_PANDU_SKIN[v.upper()])
        dst.insert(i, c)


def lean(root, deg):
    for gid in ('upper-body', 'upper-body-front'):
        g = group(root, gid)
        t = f'rotate({deg} 510 675)'
        g.set('transform', t)
        g.set('data-base-transform', t)


def face(root, mouth_open=False, brows_dy=0, head_tilt=0):
    show(root, 'mouth-open', mouth_open)
    show(root, 'mouth-closed', not mouth_open)
    if brows_dy:
        group(root, 'brows').set('transform', f'translate(0 {brows_dy})')
    if head_tilt:
        h = group(root, 'head')
        h.set('transform', f'rotate({head_tilt} 510 310)')
        h.set('data-base-transform', f'rotate({head_tilt} 510 310)')


def save(tree, path, title, char_id, expression):
    root = tree.getroot()
    root.set('data-character', char_id)
    root.set('data-expression', expression)
    t = root.find(NS + 'title')
    if t is not None:
        t.text = title
    d = root.find(NS + 'desc')
    if d is not None:
        d.text = (d.text or '') + ' Derived for S01E02 by episodes/S01E02-kindama-curses-pandu/svg/derive-cast.py.'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode', xml_declaration=False)
    print('wrote', path)


def pandu(out=f'{LIB}/pandu'):
    # s04/s05: the bow lowered at his side, the other hand at his chest, recoiling; mouth open in shock
    t = load(); r = t.getroot()
    unstring_bow(r)
    pose_arms(r, far=(-12, -14, 45), near=(18, -150, 40))
    lean(r, -3)
    face(r, mouth_open=True, brows_dy=-9)
    save(t, f'{out}/standing-shocked.svg', 'Pandu · standing, shocked', 'pandu', 'shocked')

    # s06: the crown taken off and held in both hands at his chest, head bowed (renouncing the throne)
    t = load(); r = t.getroot()
    remove_bow(r)
    pose_arms(r, far=(10, 110, 30), near=(18, -150, 40))
    crown = group(r, 'crown')
    parent_of(r, crown).remove(crown)
    crown.set('transform', 'translate(505 455) scale(0.9) translate(-510 -95)')
    group(r, 'upper-body-front').append(crown)
    face(r, head_tilt=8)
    save(t, f'{out}/removing-crown.svg', 'Pandu · holding his crown, renouncing', 'pandu', 'sad')

    # s10: leaning forward, one arm reaching out to the right
    t = load(); r = t.getroot()
    remove_bow(r)
    pose_arms(r, far=(-72, -6, -30), near=(6, 8, 0))
    open_hand(r, 'hand-far')
    lean(r, 4)
    save(t, f'{out}/reaching.svg', 'Pandu · reaching out', 'pandu', 'longing')


# Arjuna (tease only): a design placeholder until E03's research. Deeper skin and a red dhoti
# so he reads as a different prince from Pandu at a glance.
A_SKIN = {'#F6E3C5': '#C99466', '#E8CEAC': '#B07A4E', '#C6A382': '#8E5A36'}
A_DHOTI = {'#FFF8E9': '#C0503C', '#F3EEDF': '#A53A2A', '#D6C7AF': '#8E2A20', '#B7A68F': '#621E18'}
A_SASH = {'#F3EEDF': '#E8B53A', '#D6C7AF': '#B8862A'}


def recolor(el, mapping):
    m = {k.upper(): v for k, v in mapping.items()}
    for e in el.iter():
        for a in ('fill', 'stroke'):
            v = e.get(a)
            if v and v.upper() in m:
                e.set(a, m[v.upper()])


def arjuna(out=f'{LIB}/arjuna'):
    t = load(); r = t.getroot()
    for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
        recolor(group(r, g), A_DHOTI)
    recolor(group(r, 'uttariya'), A_SASH)
    recolor(r, A_SKIN)
    unstring_bow(r)
    pose_arms(r, far=(-12, -14, 45), near=(10, -40, 0))
    save(t, f'{out}/standing-bow.svg', 'Arjuna · standing with his bow', 'arjuna', 'calm')


if __name__ == '__main__':
    import sys
    base = sys.argv[1] if len(sys.argv) > 1 else None
    pandu(f'{base}/pandu' if base else f'{LIB}/pandu')
    arjuna(f'{base}/arjuna' if base else f'{LIB}/arjuna')
