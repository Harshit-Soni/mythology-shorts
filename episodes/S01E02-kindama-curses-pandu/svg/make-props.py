"""S01E02 props, drawn in code (simple symbols, flames and silhouettes) or derived from library props.

Run from the repo root:  python3 episodes/S01E02-kindama-curses-pandu/svg/make-props.py [out_dir]
Writes assets/props/<id>.svg (800×800 unless noted). Flat fills, outline #1E1420, no filters/text/images.
"""
import copy
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
NS = '{%s}' % SVG
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/props'
INK = '#1E1420'
GOLD, GOLD_L, GOLD_D = '#E8B53A', '#F4D17B', '#B8862A'


def write(pid, body, w=800, h=800, desc=''):
    os.makedirs(OUT, exist_ok=True)
    svg = (f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" '
           f'stroke-linecap="round" stroke-linejoin="round"><desc>S01E02 | {pid} | {desc} '
           f'Made by episodes/S01E02-kindama-curses-pandu/svg/make-props.py.</desc>{body}</svg>')
    ET.fromstring(svg)  # must parse
    with open(f'{OUT}/{pid}.svg', 'w') as f:
        f.write(svg)
    print('wrote', f'{OUT}/{pid}.svg')


def star(cx, cy, r1, r2, n=4, rot=0):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n - 90)
        pts.append(f'{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + 'Z'


def glow_rings(cx, cy, r, color, n=4, op=0.10):
    return ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r * (1 - i / (n + 1)):.0f}" fill="{color}" opacity="{op}" />' for i in range(n))


def small_arrow(x, y, rot, s=1.0):
    """Short golden arrow: arrowhead at the front (+x), fletching at the back."""
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<path d="M-120 0 L40 0" stroke="{INK}" stroke-width="11" />'
            f'<path d="M-120 0 L40 0" stroke="{GOLD}" stroke-width="6" />'
            f'<path d="M-120 0 L-150 -16 L-136 0 L-150 16Z" fill="{GOLD_L}" stroke="{INK}" stroke-width="3" />'
            f'<path d="M-100 0 L-128 -16 L-114 0 L-128 16Z" fill="{GOLD_L}" stroke="{INK}" stroke-width="3" />'
            '</g>')


# ---------- 1. stag-wounded (from the library deer) ----------
def stag_wounded():
    t = ET.parse('assets/props/deer.svg')
    r = t.getroot()
    keep = []
    for g in list(r):
        gid = g.get('id')
        if gid in ('legs-far', 'legs-near'):
            r.remove(g)
    # body down to the ground; neck, antlers and head lifted (crying out toward the left)
    for g in r:
        gid = g.get('id')
        if gid in ('body', 'spots', 'tail'):
            g.set('transform', 'translate(0 200)')
        if gid in ('neck', 'antlers', 'head'):
            g.set('transform', 'translate(0 200) rotate(92 345 335)')
    head = [g for g in r if g.get('id') == 'head'][0]
    # wide-open eye with a faint gold glow (the sage inside), replacing the grazing deer's closed eye
    for p in list(head):
        if p.get('d', '').startswith('M187 57') or ('Q' in p.get('d', '') and p.get('stroke') == INK and p.get('fill') in (None, 'none') and len(p.get('d', '')) < 40):
            head.remove(p)
    head.append(ET.fromstring(f'<g xmlns="{SVG}">{glow_rings(198, 574, 30, GOLD, 3, 0.18)}'
                              f'<ellipse cx="198" cy="574" rx="15" ry="12" fill="#FFF8E9" stroke="{INK}" stroke-width="3" />'
                              f'<circle cx="194" cy="574" r="7" fill="{INK}" /><circle cx="191" cy="571" r="2.5" fill="#FFF8E9" /></g>'))
    # folded legs under the body, and one golden arrow in the flank
    legs = (f'<g id="legs-folded">'
            f'<path d="M380 640 Q340 660 300 668 L292 690 L410 690 Q420 660 380 640Z" fill="#925B3E" stroke="{INK}" stroke-width="3.8" />'
            f'<path d="M600 640 Q640 662 690 668 L700 690 L560 690 Q556 660 600 640Z" fill="#B57E50" stroke="{INK}" stroke-width="3.8" />'
            f'<path d="M292 682H312L310 692H290ZM688 682H702L704 692H686Z" fill="{INK}" /></g>')
    r.insert(0, ET.fromstring(f'<g xmlns="{SVG}">{legs}</g>'))
    r.append(ET.fromstring(f'<g xmlns="{SVG}" id="arrow">{small_arrow(570, 480, 52, 1.25)}</g>'))
    d = r.find(NS + 'desc')
    d.text = 'S01E02 | stag-wounded | the library deer lying wounded, head raised, eye open, one golden arrow. Made by make-props.py.'
    os.makedirs(OUT, exist_ok=True)
    t.write(f'{OUT}/stag-wounded.svg', encoding='unicode')
    print('wrote', f'{OUT}/stag-wounded.svg')


# ---------- 2. mantra-ring ----------
def mantra_ring():
    cx = cy = 400
    glyphs = []
    shapes = ['M-14 0 Q-22 20 -6 30 Q10 34 8 16', 'M0 0 L0 38 M0 18 Q14 14 16 28', 'M-12 0 Q-18 26 0 30 Q16 26 10 8',
              'M10 0 L10 38 M10 16 Q-14 10 -12 26 Q-8 36 4 30', 'M-10 0 Q8 12 -6 22 Q12 30 6 40', 'M0 0 L0 24 Q0 36 12 34']
    for i in range(22):
        a = i * 360 / 22
        g = shapes[i % len(shapes)]
        glyphs.append(f'<g transform="rotate({a:.1f} {cx} {cy}) translate({cx} {cy - 262})">'
                      f'<path d="{g}" stroke="{GOLD_D}" stroke-width="10" /><path d="{g}" stroke="{GOLD_L}" stroke-width="5" /></g>')
    glyphs.append(f'<circle cx="{cx}" cy="{cy}" r="262" stroke="{GOLD_D}" stroke-width="11" />'
                  f'<circle cx="{cx}" cy="{cy}" r="262" stroke="{GOLD_L}" stroke-width="6" />')
    body = (glow_rings(cx, cy, 330, GOLD, 4, 0.07)
            + f'<circle cx="{cx}" cy="{cy}" r="300" stroke="{GOLD}" stroke-width="4" opacity="0.6" />'
            + f'<circle cx="{cx}" cy="{cy}" r="208" stroke="{GOLD}" stroke-width="4" opacity="0.6" />'
            + f'<g id="glyphs">{"".join(glyphs)}</g>'
            + ''.join(f'<path d="{star(cx + 300 * math.cos(math.radians(a)), cy + 300 * math.sin(math.radians(a)), 14, 5)}" fill="#FFF8E9" />' for a in (45, 165, 285)))
    write('mantra-ring', body, desc='a ring of glowing abstract script (Durvasa\'s mantra), not readable words.')


# ---------- 3. wind-swirl (Vayu) ----------
def wind_swirl():
    paths = ''
    for i, (r, w, c) in enumerate(((250, 34, '#BFE3F0'), (180, 28, '#8FCBE0'), (110, 22, '#DDF2F8'))):
        d = f'M{400 - r} 430 Q{400 - r} {430 - r} 400 {430 - r} Q{400 + r * 0.9} {430 - r} {400 + r * 0.9} 430 Q{400 + r * 0.9} {430 + r * 0.55} {400 + r * 0.2} {430 + r * 0.55}'
        paths += f'<path d="{d}" stroke="{INK}" stroke-width="{w + 8}" /><path d="{d}" stroke="{c}" stroke-width="{w}" />'
    streams = ''.join(f'<path d="M{80 + k * 30} {560 + k * 40} Q{300} {600 + k * 30} {560 - k * 40} {640 + k * 25}" stroke="{c}" stroke-width="{14 - k * 3}" />'
                      for k, c in enumerate(('#BFE3F0', '#DDF2F8', '#8FCBE0')))
    write('wind-swirl', glow_rings(400, 430, 330, '#BFE3F0', 3, 0.10) + paths + streams,
          desc='a stylised wind swirl, the symbol for Vayu.')


# ---------- 4. vajra-flash (Indra) ----------
def vajra_flash():
    rays = ''.join(f'<path d="M400 400 L{400 + 360 * math.cos(math.radians(a)):.0f} {400 + 360 * math.sin(math.radians(a)):.0f}" '
                   f'stroke="{GOLD_L}" stroke-width="{10 if i % 2 else 18}" opacity="0.55" />' for i, a in enumerate(range(0, 360, 22)))
    prong = (f'<path d="M400 120 Q350 190 372 262 L400 250 L428 262 Q450 190 400 120Z" fill="{GOLD}" stroke="{INK}" stroke-width="5" />'
             f'<path d="M372 262 Q320 230 300 160 Q340 196 380 214Z" fill="{GOLD_D}" stroke="{INK}" stroke-width="5" />'
             f'<path d="M428 262 Q480 230 500 160 Q460 196 420 214Z" fill="{GOLD_D}" stroke="{INK}" stroke-width="5" />')
    body = (glow_rings(400, 400, 360, GOLD, 4, 0.09) + rays
            + f'<g id="vajra" transform="rotate(-30 400 400)">{prong}'
            + f'<g transform="rotate(180 400 400)">{prong}</g>'
            + f'<rect x="372" y="300" width="56" height="200" rx="22" fill="{GOLD}" stroke="{INK}" stroke-width="5" />'
            + f'<ellipse cx="400" cy="400" rx="44" ry="30" fill="#8E2A20" stroke="{INK}" stroke-width="5" />'
            + f'<ellipse cx="392" cy="392" rx="12" ry="7" fill="#E07A2E" /></g>')
    write('vajra-flash', body, desc="Indra's vajra (a double-ended thunderbolt) in a burst of light.")


# ---------- 5. twin-stars (Ashvins) ----------
def twin_stars():
    body = (glow_rings(290, 400, 200, '#FFE6B0', 3, 0.12) + glow_rings(510, 400, 200, '#FFE6B0', 3, 0.12)
            + f'<path d="{star(290, 400, 150, 42)}" fill="{GOLD_L}" stroke="{INK}" stroke-width="5" />'
            + f'<path d="{star(510, 400, 150, 42)}" fill="{GOLD_L}" stroke="{INK}" stroke-width="5" />'
            + f'<path d="{star(290, 400, 70, 22, 4, 45)}" fill="#FFF8E9" />'
            + f'<path d="{star(510, 400, 70, 22, 4, 45)}" fill="#FFF8E9" />')
    write('twin-stars', body, desc='twin stars, the symbol for the Ashvins.')


# ---------- 6. fallen-crown (Pandu's own crown, from his rig) ----------
def fallen_crown():
    src = ET.parse('assets/characters/pandu/drawing-bow.svg').getroot()
    crown = [e for e in src.iter() if e.get('id') == 'crown'][0]
    crown = copy.deepcopy(crown)
    crown.set('transform', 'translate(400 470) rotate(-72) scale(2.1) translate(-510 -95)')
    petals = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="9" transform="rotate({a} {x} {y})" fill="{c}" stroke="{INK}" stroke-width="2" />'
                     for x, y, a, c in ((170, 600, 20, '#F6C1D0'), (250, 650, -30, '#F2A7B8'), (560, 620, 40, '#F6C1D0'),
                                        (640, 560, -10, '#E07A2E'), (470, 680, 15, '#F2A7B8'), (330, 300, 60, '#F6C1D0'), (590, 330, -40, '#F2A7B8')))
    grass = ''.join(f'<path d="M{x} 720 Q{x + 8} {660 - (x % 50)} {x + 22} {630 - (x % 40)}" stroke="#3F6B3A" stroke-width="7" />'
                    for x in range(60, 760, 34))
    body = (f'<ellipse cx="400" cy="640" rx="330" ry="70" fill="#5C8A4A" opacity="0.55" />{grass}'
            + ET.tostring(crown, encoding='unicode').replace('ns0:', '').replace(':ns0', '') + petals)
    body = re.sub(r'\sxmlns(:\w+)?="[^"]+"', '', body)
    write('fallen-crown', body, desc="Pandu's crown (from his rig) lying on its side in the grass among petals.")


# ---------- 7. pyre-flames ----------
def pyre_flames():
    logs = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="16" fill="#6B3B1E" stroke="{INK}" stroke-width="5" transform="rotate({a} {x + w / 2} {y + 19})" />'
                   for x, y, w, a in ((150, 640, 500, -4), (130, 690, 540, 3), (190, 600, 420, 2)))
    def flame(cx, h, w, c1, c2):
        d = (f'M{cx - w} 620 Q{cx - w * 1.1} {620 - h * 0.45} {cx - w * 0.3} {620 - h * 0.7} Q{cx - w * 0.5} {620 - h * 0.9} {cx} {620 - h} '
             f'Q{cx + w * 0.2} {620 - h * 0.75} {cx + w * 0.55} {620 - h * 0.62} Q{cx + w * 1.1} {620 - h * 0.4} {cx + w} 620Z')
        inner = (f'M{cx - w * 0.5} 620 Q{cx - w * 0.55} {620 - h * 0.35} {cx} {620 - h * 0.6} Q{cx + w * 0.55} {620 - h * 0.35} {cx + w * 0.5} 620Z')
        return f'<path d="{d}" fill="{c1}" stroke="{INK}" stroke-width="5" /><path d="{inner}" fill="{c2}" />'
    flames = (flame(270, 330, 110, '#E07A2E', GOLD_L) + flame(530, 360, 115, '#E07A2E', GOLD_L)
              + flame(400, 500, 150, '#C8452A', '#F0A02E') + flame(400, 300, 70, GOLD, '#FFF1C2'))
    sparks = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD_L}" />' for x, y, r in ((300, 120, 7), (470, 90, 6), (560, 170, 8), (230, 200, 5), (420, 40, 5)))
    write('pyre-flames', glow_rings(400, 440, 380, '#E07A2E', 4, 0.08) + flames + logs + sparks,
          desc='folk-art stylised flames on a log pyre; no body.')


# ---------- silhouettes ----------
SIL = '#1E1420'


def person(x, base, h, rim=None, robe=True, hair='knot', arms='down', stride=0):
    """A simple dignified standing silhouette (head, torso, legs or robe). h = height in px, feet at base."""
    u = h / 10
    hy = base - h + u * 0.9
    parts = [f'<circle cx="{x}" cy="{hy:.0f}" r="{u * 0.75:.0f}" />']
    if hair == 'knot':
        parts.append(f'<circle cx="{x - u * 0.15:.0f}" cy="{hy - u * 0.8:.0f}" r="{u * 0.4:.0f}" />')
    elif hair == 'crown':
        parts.append(f'<path d="M{x - u * 0.6:.0f} {hy - u * 0.5:.0f} L{x:.0f} {hy - u * 1.9:.0f} L{x + u * 0.6:.0f} {hy - u * 0.5:.0f}Z" />')
    parts.append(f'<path d="M{x - u * 1.1:.0f} {hy + u * 1.1:.0f} Q{x:.0f} {hy + u * 0.7:.0f} {x + u * 1.1:.0f} {hy + u * 1.1:.0f} '
                 f'L{x + u * 0.9:.0f} {base - u * 4.2:.0f} L{x - u * 0.9:.0f} {base - u * 4.2:.0f}Z" />')
    if robe:
        parts.append(f'<path d="M{x - u * 0.95:.0f} {base - u * 4.3:.0f} L{x + u * 0.95:.0f} {base - u * 4.3:.0f} '
                     f'L{x + u * 1.3 + stride:.0f} {base:.0f} L{x - u * 1.3 + stride:.0f} {base:.0f}Z" />')
    else:
        parts.append(f'<path d="M{x - u * 0.9:.0f} {base - u * 4.3:.0f} L{x - u * 0.2:.0f} {base - u * 4.3:.0f} L{x - u * 0.4 - stride:.0f} {base:.0f} L{x - u * 1.0 - stride:.0f} {base:.0f}Z" />'
                     f'<path d="M{x + u * 0.2:.0f} {base - u * 4.3:.0f} L{x + u * 0.9:.0f} {base - u * 4.3:.0f} L{x + u * 1.0 + stride:.0f} {base:.0f} L{x + u * 0.4 + stride:.0f} {base:.0f}Z" />')
    if arms == 'down':
        for sgn in (-1, 1):
            parts.append(f'<path d="M{x + sgn * u * 1.0:.0f} {hy + u * 1.2:.0f} L{x + sgn * u * 1.45:.0f} {base - u * 4.6:.0f} L{x + sgn * u * 1.1:.0f} {base - u * 4.5:.0f} L{x + sgn * u * 0.75:.0f} {hy + u * 1.4:.0f}Z" />')
    g = f'<g fill="{SIL}">{"".join(parts)}</g>'
    if rim:
        g = f'<g transform="translate(-3 -3)" fill="{rim}" opacity="0.9">{"".join(parts)}</g>' + g
    return g


def three_pilgrims():
    # walking left into the mountains (the renderer's walk-left moves it): king, two queens, small with staff-less hands
    body = (person(300, 700, 300, robe=False, hair='knot', stride=-18)
            + person(450, 700, 270, robe=True, hair='knot', stride=-14)
            + person(580, 700, 260, robe=True, hair='knot', stride=-12)
            + f'<ellipse cx="440" cy="706" rx="260" ry="12" fill="{SIL}" opacity="0.25" />')
    write('three-pilgrims-silhouette', body, desc='Pandu, Kunti and Madri as small walking silhouettes.')


def young_pandavas():
    heights = (300, 270, 240, 200, 200)  # Yudhishthira, Bhima, Arjuna, the twins (born a year apart)
    xs = (140, 270, 390, 510, 620)
    body = ''.join(person(x, 720, h, rim='#E07A2E', robe=False, hair='knot', arms='down') for x, h in zip(xs, heights))
    write('young-pandavas-group', body, desc='the five Pandava boys as silhouettes of different heights, warm fire rim.')


def five_sons():
    xs = (110, 255, 400, 545, 690)
    heights = (520, 560, 540, 500, 500)
    glow = ''.join(glow_rings(x, 720 - h * 0.55, h * 0.45, GOLD, 3, 0.10) for x, h in zip(xs, heights))
    body = glow + ''.join(person(x, 760, h, rim=GOLD, robe=False, hair='knot') for x, h in zip(xs, heights))
    write('five-sons-silhouette', body, desc='the five Pandavas grown, standing in a row with gold rims.')


def apsara():
    # a classical dance pose, modest: long skirt, one arm raised in a mudra, the other curved out
    u = 60
    body = (glow_rings(400, 360, 330, '#F2A7B8', 3, 0.10)
            + f'<g fill="{SIL}">'
            + f'<circle cx="410" cy="170" r="{u * 0.75:.0f}" />'
            + f'<circle cx="440" cy="135" r="{u * 0.4:.0f}" />'
            + '<path d="M370 225 Q410 205 450 225 L440 400 L380 400Z" />'
            + '<path d="M375 395 L445 395 Q520 560 560 720 L240 720 Q300 560 375 395Z" />'
            + '<path d="M445 240 Q520 220 560 150 L585 120 L600 135 L575 170 Q540 245 452 275Z" />'
            + '<path d="M372 250 Q300 300 250 290 L235 300 L245 315 Q310 330 380 285Z" />'
            + '<path d="M380 300 Q340 420 300 520 Q330 430 395 320Z" opacity="0.7" />'
            + '</g>'
            + f'<g fill="none" stroke="#F2A7B8" stroke-width="4" opacity="0.8">'
            + '<path d="M240 720 Q300 560 375 395" /><path d="M560 720 Q520 560 445 395" /></g>')
    write('apsara-silhouette', body, desc='an apsara in a classical dance pose, modest, as a silhouette with a pink rim (E03 tease).')


# v2 (16-beat script)
def cracked_rock():
    # baby Bhima fell from Kunti's lap and the rock shattered (Adi §123): a boulder split by bright cracks, shards flying
    rock = (f'<path d="M150 640 Q130 520 210 440 Q280 360 400 350 Q530 345 610 420 Q690 500 660 640 Z" fill="#8C8478" stroke="{INK}" stroke-width="7" />'
            f'<path d="M210 600 Q230 500 300 450 Q360 420 420 418" stroke="#A79F92" stroke-width="16" />'
            f'<path d="M660 640 Q640 560 600 520" stroke="#6E675D" stroke-width="18" />')
    cracks = ('M400 352 L380 430 L430 470 L390 560 L420 640', 'M380 430 L300 470 L250 560', 'M430 470 L520 500 L560 590', 'M390 560 L320 610')
    glow = ''.join(f'<path d="{d}" stroke="{GOLD_L}" stroke-width="18" opacity="0.55" />' for d in cracks)
    lines = ''.join(f'<path d="{d}" stroke="{INK}" stroke-width="8" />' for d in cracks)
    shards = ''.join(f'<path d="M{x} {y} l{a} {b} l{c} {d} Z" fill="#8C8478" stroke="{INK}" stroke-width="5" />'
                     for x, y, a, b, c, d in ((300, 300, 40, -20, -10, 45), (520, 280, 35, 25, -45, 10), (170, 400, -30, -30, 45, -5), (640, 380, 40, -10, -20, 40), (420, 250, 20, -35, 20, 35)))
    dust = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#CFC6B6" opacity="0.6" />' for x, y, r in ((200, 650, 30), (300, 670, 24), (560, 665, 28), (650, 650, 22)))
    write('cracked-rock', glow_rings(400, 480, 280, GOLD_L, 3, 0.08) + dust + rock + glow + lines + shards,
          desc='a boulder split by glowing cracks, shards flying (baby Bhima shatters a rock).')


def rising_lights():
    # the rishis set out for Brahma's realm (Adi §120): small warm lights rising into the sky, Pandu left below
    lights = ''
    for x, y, r in ((220, 560, 26), (330, 470, 22), (430, 380, 28), (540, 300, 20), (610, 200, 24), (300, 260, 18), (480, 140, 20)):
        lights += glow_rings(x, y, r * 3.2, '#FFE6B0', 3, 0.12)
        lights += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD_L}" stroke="{GOLD_D}" stroke-width="3" />'
        lights += f'<circle cx="{x - r * 0.3}" cy="{y - r * 0.3}" r="{r * 0.35}" fill="#FFFBEA" />'
    trail = '<path d="M220 700 Q260 560 330 470 Q400 400 430 380 Q500 330 540 300 Q590 250 610 200" stroke="#FFE6B0" stroke-width="6" opacity="0.35" stroke-dasharray="4 18" />'
    write('rising-lights', trail + lights, desc='warm points of light rising into the sky (the rishis leaving for Brahma\'s realm).')


if __name__ == '__main__':
    stag_wounded(); mantra_ring(); wind_swirl(); vajra_flash(); twin_stars(); fallen_crown()
    pyre_flames(); three_pilgrims(); young_pandavas(); five_sons(); apsara()
    cracked_rock(); rising_lights()
