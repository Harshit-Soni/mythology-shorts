"""Kunti and Madri concept sheets, built from the pandu rig (the channel's first women).

Same head construction, line weight and palette as the S01E01 cast, with a new costume:
a fitted bodice (kanchuka) to the waist, an ankle-length antariya with a border, and an uttariya.
No gold (Pandu gave their ornaments away, Adi §119): only a red thread and a bindi.

Three variations differ in the uttariya drape, face/eye proportions and expression warmth.
Run from the repo root:  python3 episodes/S01E02-kindama-curses-pandu/svg/make-concepts.py [out_dir]
"""
import copy
import os
import sys
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
NS = '{%s}' % SVG
SRC = 'assets/characters/pandu/drawing-bow.svg'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'episodes/S01E02-kindama-curses-pandu/svg/concepts'
INK = '#291C23'
PANDU_SKIN = ('#F6E3C5', '#E8CEAC', '#C6A382')
GOLDS = ('#E8B53A', '#F4D17B', '#AF762C')

WOMEN = {
    'kunti': dict(skin=('#EBB98C', '#D29A68', '#A9714A'), border='#8E2A20', border_l='#B5402E',
                  utt=('#C98A2E', '#A86E1E', '#E3A84A'), hair='knot'),
    'madri': dict(skin=('#F5D2AE', '#E3B48A', '#C08A60'), border='#2E6B4F', border_l='#3F8A68',
                  utt=('#E07A2E', '#B8601F', '#F2A04E'), hair='braid'),
}


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


def frag(xml):
    """Parse a fragment; stroke-only paths get fill="none" (SVG's default fill is black)."""
    els = list(ET.fromstring(f'<g xmlns="{SVG}">{xml}</g>'))
    for el in els:
        for e in el.iter():
            if e.tag == NS + 'path' and e.get('stroke') and e.get('fill') is None:
                e.set('fill', 'none')
    return els


def recolor(el, mapping):
    m = {k.upper(): v for k, v in mapping.items()}
    for e in el.iter():
        for a in ('fill', 'stroke'):
            v = e.get(a)
            if v and v.upper() in m:
                e.set(a, m[v.upper()])


def strip_gold(g):
    """Remove the gold ornaments (necklace, armlets, wrist cuffs and their gems) that are direct children of g."""
    for ch in list(g):
        f, st = (ch.get('fill') or '').upper(), (ch.get('stroke') or '').upper()
        if f in GOLDS or st in GOLDS or (f == '#8E2A20' and st == '#AF762C') or f == '#F4D17B':
            g.remove(ch)
        elif (ch.get('d') or '').startswith('M449 348Q515 500 581 348'):
            g.remove(ch)  # the necklace's dark outline


def joint(root, gid, t):
    g = group(root, gid)
    g.set('transform', t)
    g.set('data-base-transform', t)


def arms_clasped(root):
    """Both hands meeting at the front of the waist."""
    joint(root, 'upper-arm-far', 'translate(635 390) rotate(4)')
    joint(root, 'forearm-far', 'translate(0 127.769) rotate(40)')
    joint(root, 'hand-far', 'translate(0 116.297) rotate(10)')
    joint(root, 'upper-arm-near', 'translate(335 397) rotate(-10)')
    joint(root, 'forearm-near', 'translate(0 148.708) rotate(-48) scale(1 0.36)')
    joint(root, 'hand-near', 'translate(0 407.620) scale(1 2.7778) rotate(-20)')


def skirt(c):
    b, bl = c['border'], c['border_l']
    # an ankle-length antariya: fitted at the hips, a gentle flare to the hem, soft folds, front pleats with a
    # border down the pleat edge and at the hem
    return (
        f'<g id="antariya">'
        f'<path d="M398 628 Q520 612 640 632 Q660 760 668 900 Q690 1200 726 1474 Q520 1506 300 1474 '
        f'Q340 1200 366 900 Q376 760 398 628Z" fill="#F3EEDF" stroke="{INK}" stroke-width="3" />'
        f'<path d="M600 700 Q630 1000 680 1480 L640 1486 Q600 1000 586 720Z" fill="#E6DCC6" />'
        f'<path d="M420 700 Q400 1000 360 1480 L396 1486 Q430 1000 436 720Z" fill="#E6DCC6" />'
        f'<path d="M520 650 Q526 1060 540 1494 L506 1494 Q500 1060 498 652Z" fill="#E6DCC6" />'
        f'<path d="M498 652 Q500 1060 506 1494 M520 650 Q526 1060 540 1494 M560 642 Q574 1060 602 1492" stroke="#B7A68F" stroke-width="3" />'
        f'<path d="M430 900 Q470 940 480 1040 M620 880 Q600 960 610 1060 M400 1180 Q440 1220 446 1320" stroke="#D6C7AF" stroke-width="4" />'
        f'<path d="M300 1474 Q520 1506 726 1474 L722 1440 Q520 1470 304 1440Z" fill="{b}" stroke="{INK}" stroke-width="3" />'
        f'<path d="M314 1456 Q520 1484 712 1456" stroke="{bl}" stroke-width="4" />'
        f'<path d="M560 642 Q574 1060 602 1492 L584 1493 Q556 1060 544 644Z" fill="{b}" />'
        f'<path d="M398 628 Q520 612 640 632 L642 664 Q520 646 396 660Z" fill="{b}" stroke="{INK}" stroke-width="3" />'
        f'</g>'
    )


def feet(skin):
    """Two bare feet peeking out under the hem, pointing right (the way she faces)."""
    def foot(x):
        return (f'<path d="M{x} 1478 Q{x + 6} 1508 {x + 30} 1514 L{x + 92} 1518 Q{x + 106} 1516 {x + 100} 1504 '
                f'Q{x + 70} 1494 {x + 52} 1478Z" fill="{skin[1]}" stroke="{INK}" stroke-width="3" />'
                f'<path d="M{x + 8} 1490 Q{x + 20} 1508 {x + 44} 1510" stroke="{skin[2]}" stroke-width="3" />')
    return f'<g id="feet">{foot(400)}{foot(570)}</g>'


def bodice(c, skin):
    b = c['border']
    # a fitted, short-sleeved bodice down to the waist (covers the chest and midriff)
    return (
        f'<g id="kanchuka">'
        f'<path d="M352 372 Q420 338 470 334 Q520 346 560 332 Q620 340 655 380 L640 470 Q630 560 640 640 '
        f'Q520 622 398 632 Q410 560 392 470Z" fill="#F3EEDF" stroke="{INK}" stroke-width="3" />'
        f'<path d="M470 334 Q520 380 560 332" fill="{skin[1]}" stroke="{INK}" stroke-width="3" />'
        f'<path d="M470 334 Q520 380 560 332" stroke="{b}" stroke-width="7" />'
        f'<path d="M352 372 L330 430 L372 440 L392 400Z" fill="{b}" stroke="{INK}" stroke-width="3" />'
        f'<path d="M655 380 L676 436 L636 446 L622 402Z" fill="{b}" stroke="{INK}" stroke-width="3" />'
        f'</g>'
    )


def drape(style, c):
    u0, u1, u2 = c['utt']
    if style == 'sash':  # over the near shoulder, diagonally across the torso to the far hip, the end hanging behind
        return (f'<g id="uttariya-new">'
                f'<path d="M360 360 Q420 330 470 345 L660 600 Q650 650 610 668 L560 670 L400 420 Q370 400 360 360Z" fill="{u0}" stroke="{INK}" stroke-width="3" />'
                f'<path d="M430 360 L620 630" stroke="{u1}" stroke-width="10" />'
                f'<path d="M470 345 L660 600" stroke="{u2}" stroke-width="5" />'
                f'<path d="M560 670 Q600 760 590 860 L630 850 Q640 760 610 668Z" fill="{u1}" stroke="{INK}" stroke-width="3" />'
                f'</g>')
    if style == 'shawl':  # over both shoulders, two ends hanging down the front
        return (f'<g id="uttariya-new">'
                f'<path d="M340 370 Q420 325 520 330 Q620 325 668 372 L650 420 Q600 380 520 382 Q430 380 370 425Z" fill="{u0}" stroke="{INK}" stroke-width="3" />'
                f'<path d="M372 420 Q380 560 400 720 L452 724 Q430 560 425 405Z" fill="{u0}" stroke="{INK}" stroke-width="3" />'
                f'<path d="M640 410 Q640 560 628 720 L578 724 Q590 560 600 398Z" fill="{u0}" stroke="{INK}" stroke-width="3" />'
                f'<path d="M398 700 L452 704 M584 704 L630 700" stroke="{u1}" stroke-width="10" />'
                f'<path d="M352 380 Q520 340 660 382" stroke="{u2}" stroke-width="5" />'
                f'</g>')
    raise ValueError(style)


def veil(c):
    """The uttariya drawn over the head and down behind the shoulders (variation C, Kunti)."""
    u0, u1, u2 = c['utt']
    return (f'<g id="veil">'
            f'<path d="M420 210 Q410 120 470 98 Q540 80 590 112 Q610 130 606 160 Q590 128 540 118 Q470 116 452 170 '
            f'Q440 230 452 300 Q380 420 330 520 L300 500 Q360 360 420 210Z" fill="{u0}" stroke="{INK}" stroke-width="3" />'
            f'<path d="M470 100 Q540 84 600 128" stroke="{u2}" stroke-width="5" />'
            f'<path d="M430 220 Q420 330 350 470" stroke="{u1}" stroke-width="8" />'
            f'</g>')


def hair(kind):
    if kind == 'knot':
        return (f'<g id="hair-knot"><circle cx="438" cy="292" r="44" fill="#3C3031" stroke="{INK}" stroke-width="3" />'
                f'<path d="M412 280 Q438 262 462 282 M410 302 Q438 286 466 304" stroke="#695450" stroke-width="3" /></g>')
    # braid: from behind the ear, over the near shoulder and down the front
    links = ''.join(f'<ellipse cx="{430 + i * 4}" cy="{300 + i * 38}" rx="22" ry="24" fill="#3C3031" stroke="{INK}" stroke-width="3" />'
                    f'<path d="M{414 + i * 4} {292 + i * 38} Q{430 + i * 4} {306 + i * 38} {446 + i * 4} {292 + i * 38}" stroke="#695450" stroke-width="3" />'
                    for i in range(8))
    return f'<g id="hair-braid">{links}<path d="M450 606 L462 640 L436 640Z" fill="#3C3031" stroke="{INK}" stroke-width="3" /><circle cx="449" cy="604" r="7" fill="#B5402E" /></g>'


def face(root, c, eye_scale, warmth):
    head = group(root, 'head')
    # no crown; a bindi instead of the vertical tilak
    head.remove(group(root, 'crown'))
    for p in list(head):
        if p.get('d', '').startswith('M565 141L569 158'):
            head.remove(p)
    head.extend(frag('<circle cx="567" cy="152" r="6" fill="#B5402E" stroke="#291C23" stroke-width="1.5" />'))
    group(root, 'earrings').set('style', 'display:none')
    # larger eyes with a kohl wing, softer brows, coloured lips
    eyes = group(root, 'eyes-open')
    eyes.set('transform', f'translate(538 178) scale({eye_scale}) translate(-538 -178)')
    eyes.extend(frag(f'<path d="M516 179 Q537 166 560 176 L568 171" stroke="{INK}" stroke-width="3.5" fill="none" />'))
    group(root, 'eyes-closed').set('transform', f'translate(538 178) scale({eye_scale}) translate(-538 -178)')
    brows = group(root, 'brows')
    for ch in list(brows):
        brows.remove(ch)
    brows.extend(frag(f'<path d="M514 166 Q535 150 560 160" stroke="#3C3031" stroke-width="5" fill="none" />'
                      f'<path d="M582 160 Q590 153 598 158" stroke="#3C3031" stroke-width="4" fill="none" />'))
    mc = group(root, 'mouth-closed')
    curve = 'M558 249 Q574 243 590 247 Q574 258 558 249Z' if warmth < 2 else 'M556 247 Q574 246 592 243 Q578 263 556 247Z'
    if warmth >= 1:  # a gentle smile: lift the corner of the closed mouth line
        for ch in mc:
            if ch.get('d', '').startswith('M558 249Q574 243 590 249'):
                ch.set('d', 'M558 250Q574 251 591 244')
    mc.insert(0, frag(f'<path d="{curve}" fill="#B5534A" stroke="#291C23" stroke-width="1.5" />')[0])
    # hair: no crown, so the front hair covers the top of the head
    hf = group(root, 'hair-front')
    hf.set('transform', 'translate(0 -4)')


def build(name, drape_style, eye_scale=1.15, head_scale=1.0, warmth=1, use_veil=False):
    c = WOMEN[name]
    t = ET.parse(SRC)
    r = t.getroot()
    skin = c['skin']
    # no bow, no gold
    bow = group(r, 'bow')
    parent_of(r, bow).remove(bow)
    for gid in ('upper-body', 'upper-arm-far', 'upper-arm-near', 'hand-far', 'hand-near', 'forearm-far', 'forearm-near'):
        strip_gold(group(r, gid))
    recolor(r, dict(zip(PANDU_SKIN, skin)))
    arms_clasped(r)
    # narrower stance (under a skirt)
    for gid in ('leg-near', 'leg-far'):
        group(r, gid).set('style', 'display:none')
    # torso: the bodice over the bare chest, the old sash and necklace removed
    ub = group(r, 'upper-body')
    ub.remove(group(r, 'uttariya'))
    torso = group(r, 'torso')
    for p in list(torso):
        if p.get('fill') in GOLDS or p.get('stroke') in GOLDS:
            torso.remove(p)
    idx = list(ub).index(torso) + 1
    for k, el in enumerate(frag(bodice(c, skin) + drape(drape_style, c))):
        ub.insert(idx + k, el)
    # hair behind the head, veil over it
    head = group(r, 'head')
    if use_veil:
        ub.insert(list(ub).index(head) + 1, frag(veil(c))[0])
    else:
        ub.insert(list(ub).index(head), frag(hair(c['hair']))[0])
    if head_scale != 1.0:
        head.set('transform', f'translate(510 310) scale({head_scale}) translate(-510 -310)')
    face(r, c, eye_scale, warmth)
    # the dhoti becomes the antariya
    dh = group(r, 'dhoti')
    for ch in list(dh):
        dh.remove(ch)
    dh.extend(frag(feet(skin) + skirt(c)))
    # a red thread on the near wrist
    group(r, 'hand-near').extend(frag('<path d="M-24 -8 Q0 -16 24 -8" stroke="#B5402E" stroke-width="4" />'))
    # women slightly shorter than Pandu, feet on the same baseline
    cp = group(r, 'canvas-placement')
    cp.set('transform', 'translate(500 1550) scale(0.95) translate(-500 -1550) ' + cp.get('transform'))
    return t


def sheet(variant, label, kunti_tree, madri_tree):
    """One concept sheet: both women side by side on parchment, 2000×1600."""
    def inner(tree, dx):
        r = tree.getroot()
        kids = ''.join(ET.tostring(ch, encoding='unicode') for ch in r if ch.tag != NS + 'desc' and ch.tag != NS + 'title')
        return f'<g transform="translate({dx} 0)">{kids}</g>'
    body = (f'<rect width="2000" height="1600" fill="#F3E6C8" />'
            f'<ellipse cx="500" cy="1556" rx="230" ry="20" fill="#D9C7A2" /><ellipse cx="1500" cy="1556" rx="230" ry="20" fill="#D9C7A2" />'
            + inner(kunti_tree, 0) + inner(madri_tree, 1000))
    svg = f'<svg xmlns="{SVG}" width="2000" height="1600" viewBox="0 0 2000 1600"><desc>S01E02 concept {variant}: {label}</desc>{body}</svg>'
    svg = svg.replace('ns0:', '').replace('xmlns:ns0="http://www.w3.org/2000/svg"', '')
    os.makedirs(OUT, exist_ok=True)
    path = f'{OUT}/concept-{variant}.svg'
    with open(path, 'w') as f:
        f.write(svg)
    print('wrote', path)


VARIANTS = {
    'A': ('sash: uttariya over one shoulder, oval face, calm', dict(drape_style='sash', eye_scale=1.15), dict(drape_style='sash', eye_scale=1.15)),
    'B': ('shawl: uttariya over both shoulders, rounder face, warmer smile', dict(drape_style='shawl', eye_scale=1.22, head_scale=1.05, warmth=2),
          dict(drape_style='shawl', eye_scale=1.22, head_scale=1.05, warmth=2)),
    'C': ('Kunti veiled (elder), Madri with a sash and braid', dict(drape_style='shawl', eye_scale=1.1, use_veil=True), dict(drape_style='sash', eye_scale=1.18, warmth=2)),
}

if __name__ == '__main__':
    for v, (label, k, m) in VARIANTS.items():
        sheet(v, label, build('kunti', **k), build('madri', **m))
