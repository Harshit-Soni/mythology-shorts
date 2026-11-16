"""Build X001's detailed cast from the S01E01 rigged characters (reuse before create).

Barbarika  <- pandu/drawing-bow (archer) and king/folded-hands (prince build)
Brahmin    <- mandavya/standing-calm and mandavya/cursing-hand-raised (old ascetic build)

Each output keeps the source rig (named groups, data-pivot attributes, eye/mouth states),
recoloured by body part, with parts hidden or swapped, and new parts added in canvas space.
Run from the repo root:  python3 episodes/X001-barbarika-three-arrows/svg/derive-cast.py
"""
import os
import re
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
NS = '{%s}' % SVG
LIB = 'assets/characters'

# ---------- palettes ----------
# Barbarika: deep brown skin (Ghatotkacha's line; Khatu Shyam is dark-faced), Shyam-blue dhoti,
# saffron sash, gold crown and jewellery.
B_SKIN_KING = {'#DDA06A': '#A86B40', '#BF834F': '#8A5532', '#995B39': '#663C22'}
B_SKIN_PANDU = {'#F6E3C5': '#BC8456', '#E8CEAC': '#A86B40', '#C6A382': '#8A5532'}
B_DHOTI_KING = {'#B14B35': '#34589C', '#8E2A20': '#27447C', '#622B2B': '#1C3260', '#49252A': '#14223F'}
B_DHOTI_PANDU = {'#FFF8E9': '#4A70B5', '#F3EEDF': '#34589C', '#D6C7AF': '#27447C', '#B7A68F': '#1C3260'}
B_SASH_KING = {'#2E6B4F': '#E07A2E', '#204C3D': '#A9521A'}
B_SASH_PANDU = {'#F3EEDF': '#E58A3A', '#D6C7AF': '#B9601F'}

# Brahmin (Krishna in disguise): white hair and beard, cream dhoti, tulsi-wood mala.
W_HAIR = {'#241E25': '#8F887C', '#3C3031': '#B9B2A6', '#695450': '#DAD4C8', '#A8A39A': '#F2EEE6', '#CBC4B4': '#FFFFFF'}
W_DHOTI = {'#F6A13E': '#F4ECD8', '#E68129': '#E3D5B5', '#BC5420': '#BFAA82', '#9E451F': '#8E7B58'}
W_MALA = {'#7D3D27': '#7F6034', '#B36A3C': '#A8834A', '#C8814A': '#C9A66B'}


def load(path):
    return ET.parse(path)


def group(root, gid):
    for e in root.iter():
        if e.get('id') == gid:
            return e
    raise KeyError(gid)


def recolor(el, mapping):
    m = {k.upper(): v for k, v in mapping.items()}
    for e in el.iter():
        for a in ('fill', 'stroke', 'stop-color'):
            v = e.get(a)
            if v and v.upper() in m:
                e.set(a, m[v.upper()])


def show(root, gid, visible):
    g = group(root, gid)
    if visible:
        g.attrib.pop('style', None)
    else:
        g.set('style', 'display:none')


def frag(xml):
    """Parse an SVG fragment (canvas coordinates) into elements."""
    return list(ET.fromstring(f'<g xmlns="{SVG}">{xml}</g>'))


def add_behind(root, xml):
    """Insert before the character (canvas space, drawn behind it)."""
    idx = [i for i, c in enumerate(root) if c.get('id') == 'canvas-placement'][0]
    for k, el in enumerate(frag(xml)):
        root.insert(idx + k, el)


def add_front(root, xml):
    for el in frag(xml):
        root.append(el)


def save(tree, path, title, char_id, expression):
    root = tree.getroot()
    root.set('data-character', char_id)
    root.set('data-expression', expression)
    t = root.find(NS + 'title')
    if t is not None:
        t.text = title
    d = root.find(NS + 'desc')
    if d is not None:
        d.text = (d.text or '') + ' Derived for X001 by episodes/X001-barbarika-three-arrows/svg/derive-cast.py.'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode', xml_declaration=False)
    print('wrote', path)


def quiver(cx, cy, rot, s=1.0):
    """Barbarika's quiver with the three divine arrows (blue fletching), canvas space."""
    arrows = ''.join(
        f'<path d="M{x} -186 L{x + dx} -262" stroke="#5A3A22" stroke-width="5" />'
        f'<path d="M{x + dx} -262 Q{x + dx - 14} -292 {x + dx - 2} -318 Q{x + dx + 12} -292 {x + dx} -262Z" fill="#3E78C8" stroke="#1E1420" stroke-width="2.5" />'
        f'<path d="M{x + dx - 1} -270 Q{x + dx - 6} -290 {x + dx - 2} -308" stroke="#BFD8FF" stroke-width="2" fill="none" />'
        for x, dx in ((-18, -8), (0, 0), (18, 8))
    )
    return (
        f'<g id="quiver" transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
        f'<g id="quiver-arrows">{arrows}</g>'
        '<rect x="-36" y="-196" width="72" height="392" rx="16" fill="#6B3B1E" stroke="#1E1420" stroke-width="4" />'
        '<rect x="-36" y="-196" width="22" height="392" rx="10" fill="#552E17" />'
        '<rect x="10" y="-180" width="12" height="360" rx="6" fill="#8A5230" />'
        '<rect x="-38" y="-170" width="76" height="18" fill="#E8B53A" stroke="#1E1420" stroke-width="2.5" />'
        '<rect x="-38" y="130" width="76" height="18" fill="#E8B53A" stroke="#1E1420" stroke-width="2.5" />'
        '<circle cx="0" cy="-20" r="13" fill="#B23A2A" stroke="#E8B53A" stroke-width="4" />'
        '</g>'
    )


# ---------- Barbarika ----------
def barbarika():
    # 1) drawing the bow (from Pandu): the hook and the power scenes
    t = load(f'{LIB}/pandu/drawing-bow.svg')
    r = t.getroot()
    recolor(r, B_SKIN_PANDU)
    for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
        recolor(group(r, g), B_DHOTI_PANDU)
    recolor(group(r, 'uttariya'), B_SASH_PANDU)
    add_behind(r, quiver(372, 770, -14, 0.95))
    save(t, f'{LIB}/barbarika/drawing-bow__focused.svg', 'Barbarika · drawing bow', 'barbarika', 'focused')

    # 2) folded hands (from the king): meeting the Brahmin, agreeing to give his head
    t = load(f'{LIB}/king/folded-hands.svg')
    r = t.getroot()
    recolor(r, B_SKIN_KING)
    for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
        recolor(group(r, g), B_DHOTI_KING)
    for g in ('rear-drape', 'uttariya'):
        recolor(group(r, g), B_SASH_KING)
    show(r, 'moustache', False)  # young warrior
    add_behind(r, quiver(352, 640, -16, 0.95))
    save(t, f'{LIB}/barbarika/folded-hands__serene.svg', 'Barbarika · folded hands', 'barbarika', 'serene')


# ---------- Brahmin (Krishna in disguise) ----------
URDHVA_PUNDRA = 'M568 116 L570 150 Q577 161 584 150 L585 116'  # Vaishnava U tilak, replaces the Shaiva tripundra


def brahmin():
    for src, pose, expr in (('standing-calm', 'standing-calm', 'serene'), ('cursing-hand-raised', 'asking-hand-out', 'serene')):
        t = load(f'{LIB}/mandavya/{src}.svg')
        r = t.getroot()
        for g in ('hair-front', 'hair-back', 'beard', 'moustache', 'brows'):
            recolor(group(r, g), W_HAIR)
        for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
            recolor(group(r, g), W_DHOTI)
        for g in ('rudraksha-necklaces', 'hand-far', 'hand-near'):
            recolor(group(r, g), W_MALA)
        head = group(r, 'head')
        for c in head:
            if c.tag == NS + 'path' and c.get('stroke', '').upper() == '#F3E6C8' and c.get('d', '').startswith('M526 125'):
                c.set('d', URDHVA_PUNDRA)
                c.set('stroke-width', '3.6')
        # calm face: mouth closed by default (the asking pose came from a shouting curse)
        show(r, 'mouth-closed', True)
        show(r, 'mouth-open', False)
        save(t, f'{LIB}/brahmin-krishna/{pose}__{expr}.svg', f'Brahmin (Krishna) · {pose}', 'brahmin-krishna', expr)


def sky_head():
    """props/barbarika-head-sky.svg: the new Barbarika's head (crowned, eyes open) watching from
    the sky, the neck hidden in cloud, with a soft gold halo. Replaces the v1 hand-drawn head."""
    src = load(f'{LIB}/barbarika/folded-hands__serene.svg').getroot()
    vb = (286, 40, 468, 530)  # head and crown, in the rig's canvas space
    out = ET.Element(NS + 'svg', {'width': str(vb[2]), 'height': str(vb[3]), 'viewBox': ' '.join(map(str, vb)),
                                  'fill': 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round'})
    ET.SubElement(out, NS + 'desc').text = ("Barbarika's immortal head watching the war from the sky: the v2 rig's head "
                                            "(folded-hands pose), neck hidden in cloud. X001 prop, made by svg/derive-cast.py.")
    defs = ET.SubElement(out, NS + 'defs')
    rg = ET.SubElement(defs, NS + 'radialGradient', {'id': 'halo'})
    for off, op in (('0', '0.75'), ('0.55', '0.35'), ('1', '0')):
        ET.SubElement(rg, NS + 'stop', {'offset': off, 'stop-color': '#F6D27A', 'stop-opacity': op})
    ET.SubElement(out, NS + 'circle', {'cx': '520', 'cy': '280', 'r': '200', 'fill': 'url(#halo)'})
    clip = ET.SubElement(defs, NS + 'clipPath', {'id': 'above-cloud'})
    ET.SubElement(clip, NS + 'rect', {'x': '0', 'y': '0', 'width': '1000', 'height': '470'})
    body = ET.SubElement(out, NS + 'g', {'id': 'figure', 'clip-path': 'url(#above-cloud)'})
    for c in list(src):
        if c.tag in (NS + 'title', NS + 'desc') or c.get('id') == 'quiver':
            continue
        body.append(c)
    puffs_back = [(352, 470, 52, 36), (420, 452, 62, 44), (500, 446, 70, 48), (585, 450, 66, 46), (660, 466, 56, 38)]
    puffs_front = [(385, 492, 60, 36), (465, 484, 70, 42), (548, 482, 72, 44), (630, 490, 64, 38), (700, 500, 46, 28)]
    for (x, y, rx, ry) in puffs_back:
        ET.SubElement(out, NS + 'ellipse', {'cx': str(x), 'cy': str(y), 'rx': str(rx), 'ry': str(ry), 'fill': '#E9C77A', 'stroke': '#B5822A', 'stroke-width': '3'})
    for (x, y, rx, ry) in puffs_front:
        ET.SubElement(out, NS + 'ellipse', {'cx': str(x), 'cy': str(y), 'rx': str(rx), 'ry': str(ry), 'fill': '#F7E6BC', 'stroke': '#C8962A', 'stroke-width': '3'})
    path = 'assets/props/barbarika-head-sky.svg'
    ET.ElementTree(out).write(path, encoding='unicode', xml_declaration=False)
    print('wrote', path)


if __name__ == '__main__':
    barbarika()
    brahmin()
    sky_head()
