"""S01E03 props, drawn in code (symbols, objects and silhouettes) in the library's flat style.

Run from the repo root:  python3 episodes/S01E03-urvashi-curses-arjuna/svg/make-props.py [out_dir]
Writes assets/props/<id>.svg (800×800). Flat fills, outline #1E1420, no filters/text/images.
Reuses the S01E02 helpers (person silhouettes, glow rings).
"""
import importlib.util
import math
import os
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('p02', 'episodes/S01E02-kindama-curses-pandu/svg/make-props.py')
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
sys.argv = _argv

SVG = P.SVG
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/props'
INK, GOLD, GOLD_L, GOLD_D, SIL = P.INK, P.GOLD, P.GOLD_L, P.GOLD_D, P.SIL
glow_rings, person = P.glow_rings, P.person
ARJ_SKIN = ('#A87048', '#8C5834', '#6A3E22')


def write(pid, body, desc, w=800, h=800):
    os.makedirs(OUT, exist_ok=True)
    svg = (f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" '
           f'stroke-linecap="round" stroke-linejoin="round"><desc>S01E03 | {pid} | {desc} '
           f'Made by episodes/S01E03-urvashi-curses-arjuna/svg/make-props.py.</desc>{body}</svg>')
    ET.fromstring(svg)
    with open(f'{OUT}/{pid}.svg', 'w') as f:
        f.write(svg)
    print('wrote', f'{OUT}/{pid}.svg')


def cloud(x, y, s, fill='#F3EEF8', stroke='#8C7FB0'):
    circles = ''.join(f'<circle cx="{x + dx * s:.0f}" cy="{y + dy * s:.0f}" r="{r * s:.0f}" />'
                      for dx, dy, r in ((0, 0, 40), (45, -18, 50), (100, -8, 42), (140, 8, 32), (-38, 10, 30)))
    return f'<g fill="{fill}" stroke="{stroke}" stroke-width="4">{circles}</g>'


def wheel(cx, cy, r):
    spokes = ''.join(f'<path d="M{cx} {cy} L{cx + r * 0.86 * math.cos(math.radians(a)):.0f} {cy + r * 0.86 * math.sin(math.radians(a)):.0f}" stroke="{GOLD_D}" stroke-width="9" />'
                     for a in range(0, 360, 30))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="26" />'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="18" />{spokes}'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.2:.0f}" fill="{GOLD}" stroke="{INK}" stroke-width="4" />')


# 1. Indra's chariot on clouds (Matali brings Arjuna to Amaravati, Vana §42–43)
def celestial_chariot():
    body = glow_rings(400, 450, 360, '#FFE6B0', 4, 0.10)
    body += (f'<path d="M210 520 L610 520 L640 430 Q600 400 560 410 L250 410 Q220 440 210 520Z" fill="{GOLD}" stroke="{INK}" stroke-width="5" />'
             f'<path d="M240 470 L600 470" stroke="{GOLD_D}" stroke-width="8" />'
             + ''.join(f'<circle cx="{x}" cy="490" r="9" fill="#B5402E" stroke="{INK}" stroke-width="2" />' for x in range(270, 600, 50))
             + f'<path d="M560 410 Q620 360 690 380 Q720 392 700 420 Q660 410 640 430" fill="{GOLD_L}" stroke="{INK}" stroke-width="4" />'
             f'<path d="M300 410 L300 190 M520 410 L520 190" stroke="{GOLD_D}" stroke-width="12" />'
             f'<path d="M300 410 L300 190 M520 410 L520 190" stroke="{INK}" stroke-width="2" />'
             f'<path d="M250 200 Q410 90 570 200 Q410 170 250 200Z" fill="#B5402E" stroke="{INK}" stroke-width="4" />'
             f'<path d="M250 200 Q410 170 570 200" stroke="{GOLD}" stroke-width="8" />'
             + ''.join(f'<circle cx="{x}" cy="{204 + abs(x - 410) * 0.05:.0f}" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="2" />' for x in range(270, 560, 40))
             + f'<path d="M410 112 L410 40" stroke="{INK}" stroke-width="6" /><path d="M410 44 L470 58 L410 76Z" fill="#E07A2E" stroke="{INK}" stroke-width="3" />'
             + wheel(330, 545, 110))
    body += cloud(120, 650, 1.6) + cloud(430, 690, 1.8) + cloud(620, 640, 1.2)
    write('celestial-chariot', body, "Indra's golden chariot with a red canopy, on curl-clouds.")


# 2. a ring of divine weapons (the astras Arjuna won in heaven)
def glyph(kind):
    if kind == 'bow':
        return f'<path d="M-10 -60 Q40 0 -10 60" stroke="{GOLD}" stroke-width="10" /><path d="M-10 -60 L-10 60" stroke="{GOLD_L}" stroke-width="3" />'
    if kind == 'discus':
        return (f'<circle r="44" fill="none" stroke="{GOLD}" stroke-width="10" />'
                + ''.join(f'<path d="M0 -44 l8 -16 l8 16Z" transform="rotate({a})" fill="{GOLD}" />' for a in range(0, 360, 45))
                + f'<circle r="12" fill="{GOLD}" />')
    if kind == 'trident':
        return f'<path d="M0 60 L0 -50 M-30 -50 Q-30 -20 0 -14 Q30 -20 30 -50 M0 -50 L0 -66" stroke="{GOLD}" stroke-width="9" />'
    if kind == 'mace':
        return f'<path d="M0 64 L0 -10" stroke="{GOLD}" stroke-width="10" /><circle cy="-34" r="30" fill="{GOLD}" />'
    if kind == 'noose':
        return f'<path d="M0 60 Q-10 0 0 -10 Q46 -30 30 -58 Q0 -80 -30 -58 Q-46 -30 0 -10" stroke="{GOLD}" stroke-width="8" />'
    if kind == 'sword':
        return f'<path d="M0 60 L0 30 M-22 30 L22 30 M0 30 L0 -60 L8 -48 L8 30" stroke="{GOLD}" stroke-width="9" />'
    if kind == 'vajra':
        return (f'<path d="M0 -60 L0 60" stroke="{GOLD}" stroke-width="10" /><circle r="14" fill="{GOLD}" />'
                f'<path d="M0 -60 l-18 22 l18 -8 l18 8Z M0 60 l-18 -22 l18 8 l18 -8Z" fill="{GOLD}" />')
    return f'<path d="M-50 0 L40 0" stroke="{GOLD}" stroke-width="9" /><path d="M40 0 L22 -14 L22 14Z" fill="{GOLD}" />'  # arrow


def astra_ring():
    kinds = ('bow', 'discus', 'trident', 'mace', 'noose', 'sword', 'vajra', 'arrow')
    body = glow_rings(400, 400, 360, '#FFE6B0', 4, 0.09)
    body += f'<circle cx="400" cy="400" r="280" fill="none" stroke="{GOLD_L}" stroke-width="3" opacity="0.6" stroke-dasharray="6 18" />'
    for i, k in enumerate(kinds):
        a = math.radians(i * 45 - 90)
        x, y = 400 + 280 * math.cos(a), 400 + 280 * math.sin(a)
        body += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="70" fill="#FFF1D6" opacity="0.18" />'
                 f'<g transform="translate({x:.0f} {y:.0f})"><g opacity="0.9">{glyph(k).replace(GOLD, INK)}</g></g>'
                 f'<g transform="translate({x - 2:.0f} {y - 2:.0f})">{glyph(k)}</g>')
    write('astra-ring', body, 'a ring of glowing weapon glyphs: bow, discus, trident, mace, noose, sword, vajra, arrow.')


# 3. the family vine: Pururavas & Urvashi at the top, down to Arjuna (Adi §75)
def medallion(cx, cy, r, inner):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r + 10}" fill="{GOLD_D}" stroke="{INK}" stroke-width="4" />'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#F3E6C8" stroke="{INK}" stroke-width="3" />'
            + ''.join(f'<circle cx="{cx + (r + 10) * math.cos(math.radians(a)):.0f}" cy="{cy + (r + 10) * math.sin(math.radians(a)):.0f}" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="2" />'
                      for a in range(0, 360, 30))
            + inner)


def family_vine():
    vine = (f'<path d="M400 230 C300 300 500 340 400 400 C300 460 500 500 400 560 C340 600 420 620 400 640" stroke="#4A6B3A" stroke-width="16" />'
            f'<path d="M400 230 C300 300 500 340 400 400 C300 460 500 500 400 560 C340 600 420 620 400 640" stroke="#7FA05C" stroke-width="7" />')
    leaves = ''.join(f'<path d="M{x} {y} q{s * 40} -30 {s * 70} 0 q{-s * 30} 26 {-s * 70} 0Z" fill="#7FA05C" stroke="{INK}" stroke-width="2.5" />'
                     for x, y, s in ((380, 290, -1), (440, 330, 1), (360, 430, -1), (430, 470, 1), (380, 530, -1), (420, 600, 1)))
    small = ''.join(medallion(400, y, 26, f'<circle cx="400" cy="{y}" r="10" fill="#B5402E" />') for y in (400, 520))
    def fig(x, crown):
        top = (f'<path d="M{x - 9} 104 L{x} 86 L{x + 9} 104Z" fill="{GOLD}" stroke="{INK}" stroke-width="2" />' if crown
               else f'<path d="M{x + 8} 110 Q{x + 18} 140 {x + 10} 170" stroke="{SIL}" stroke-width="6" />')
        return (f'<circle cx="{x}" cy="112" r="11" fill="{SIL}" />{top}'
                f'<path d="M{x - 11} 126 Q{x} 120 {x + 11} 126 L{x + 22} 196 Q{x} 204 {x - 22} 196Z" fill="{SIL}" />')
    top = medallion(400, 150, 70, fig(372, True) + fig(428, False))
    arjuna = (f'<path d="M376 668 L382 640 L392 656 L400 632 L408 656 L418 640 L424 668Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.5" />'
              f'<path d="M370 678 L430 678" stroke="{GOLD_D}" stroke-width="6" />'
              f'<path d="M366 700 L434 700" stroke="#6E4228" stroke-width="5" /><path d="M434 700 l-12 -7 l0 14Z" fill="#6E4228" />')
    bottom = medallion(400, 680, 58, arjuna)
    write('family-vine', vine + leaves + small + top + bottom,
          'a folk-art family vine on parchment: a royal couple (Pururavas and Urvashi) at the top, down to a crown-and-bow medallion (Arjuna).')


# 4. the thirteen years of exile, the last one lit
def year_ring():
    body = glow_rings(400, 400, 360, '#FFE6B0', 3, 0.07)
    n, r = 13, 250
    for i in range(n):
        a0, a1 = math.radians(-90 + i * 360 / n + 3), math.radians(-90 + (i + 1) * 360 / n - 3)
        p0 = (400 + r * math.cos(a0), 400 + r * math.sin(a0)); p1 = (400 + r * math.cos(a1), 400 + r * math.sin(a1))
        lit = i == n - 1
        d = f'M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}'
        if lit:
            body += f'<path d="{d}" stroke="#FFE6B0" stroke-width="80" opacity="0.35" />'
        body += (f'<path d="{d}" stroke="{INK}" stroke-width="50" />'
                 f'<path d="{d}" stroke="{GOLD if lit else "#6E5A7E"}" stroke-width="40" />')
    body += (f'<circle cx="400" cy="400" r="70" fill="{GOLD}" stroke="{INK}" stroke-width="5" opacity="0.9" />'
             + P.star(400, 400, 54, 18, 8, 0).join([f'<path d="', f'" fill="#FFF1D6" stroke="{INK}" stroke-width="3" />']))
    write('year-ring', body, 'the thirteen years of exile as a ring of segments; only the last (the year in hiding) is lit gold.')


# 5. close-up: a scarred archer's forearm and gold conch bangles (Virata §2)
def bangles_scarred_arm():
    s0, s1, s2 = ARJ_SKIN
    arm = (f'<path d="M-20 520 Q200 470 520 430 Q600 420 640 400 L660 470 Q600 500 520 506 Q220 540 -20 600Z" fill="{s0}" stroke="{INK}" stroke-width="5" />'
           f'<path d="M-20 580 Q240 530 520 500 Q600 494 650 468" stroke="{s2}" stroke-width="10" opacity="0.6" />'
           # the hand, relaxed, fingers toward the right
           f'<path d="M626 392 Q690 360 748 380 Q784 396 780 430 Q776 466 740 478 Q690 488 660 476Z" fill="{s0}" stroke="{INK}" stroke-width="5" />'
           f'<path d="M712 384 Q740 400 742 430 M740 432 Q760 446 776 446 M690 470 Q720 470 740 478" stroke="{s2}" stroke-width="4" />'
           f'<path d="M700 386 Q690 404 672 410" stroke="{s2}" stroke-width="4" />')
    scars = ''.join(f'<path d="M{x} {y} q30 -6 60 -10" stroke="#D9A07A" stroke-width="7" /><path d="M{x} {y + 6} q30 -6 60 -10" stroke="{s2}" stroke-width="2" />'
                    for x, y in ((150, 520), (180, 540), (240, 505), (270, 525), (330, 498), (360, 515)))
    bangle = lambda x: (f'<ellipse cx="{x}" cy="{470 - (x - 420) * 0.12:.0f}" rx="22" ry="62" fill="none" stroke="{INK}" stroke-width="22" />'
                        f'<ellipse cx="{x}" cy="{470 - (x - 420) * 0.12:.0f}" rx="22" ry="62" fill="none" stroke="{GOLD}" stroke-width="15" />'
                        f'<ellipse cx="{x - 4}" cy="{462 - (x - 420) * 0.12:.0f}" rx="14" ry="52" fill="none" stroke="{GOLD_L}" stroke-width="4" />')
    body = glow_rings(420, 470, 330, '#FFE6B0', 3, 0.07) + arm + scars + ''.join(bangle(x) for x in (420, 470, 520, 570))
    write('bangles-scarred-arm', body, 'close-up: a strong forearm with pale bowstring scars, gold conch bangles slid down over them.')


# 6. the shami tree at the cremation ground, the weapons bundle in its branches (Virata §5, §38–43)
def shami_tree():
    trunk = (f'<path d="M370 790 Q360 640 390 560 Q350 480 280 430 L300 410 Q370 450 410 520 Q430 450 500 400 L516 420 Q450 480 432 560 Q450 660 440 790Z" fill="#5E3D2C" stroke="{INK}" stroke-width="5" />'
             f'<path d="M392 760 Q384 660 404 580 M420 760 Q426 660 418 600" stroke="#7A5440" stroke-width="5" />'
             f'<path d="M300 420 Q240 360 200 360 M500 410 Q560 330 610 320 M410 520 Q420 400 400 300" stroke="#5E3D2C" stroke-width="16" />')
    leaves = ''
    import random
    random.seed(5)
    for cx, cy, rr in ((200, 330, 110), (330, 260, 130), (480, 230, 130), (610, 300, 110), (400, 180, 100)):
        leaves += f'<ellipse cx="{cx}" cy="{cy}" rx="{rr}" ry="{rr * 0.6:.0f}" fill="#5C7A3E" stroke="{INK}" stroke-width="4" />'
        for _ in range(26):
            x = cx + random.uniform(-rr * 0.9, rr * 0.9); y = cy + random.uniform(-rr * 0.5, rr * 0.5)
            leaves += f'<path d="M{x:.0f} {y:.0f} l{random.uniform(-14, 14):.0f} {random.uniform(-10, 10):.0f}" stroke="#86A85E" stroke-width="5" />'
    bundle = (f'<path d="M520 300 Q560 250 640 262 Q680 290 650 340 Q600 370 540 350Z" fill="#B8A07A" stroke="{INK}" stroke-width="4" />'
              f'<path d="M560 262 L570 350 M610 260 L616 352" stroke="#8E2A20" stroke-width="7" />')
    ground = f'<ellipse cx="400" cy="790" rx="260" ry="20" fill="#3A2A20" opacity="0.4" />'
    write('shami-tree', ground + trunk + leaves + bundle, 'a gnarled shami tree with feathery leaves; a cloth-wrapped bundle tied in its branches.')


# 7. the Gandiva
def gandiva():
    body = glow_rings(400, 400, 360, '#FFE6B0', 4, 0.10)
    bow = 'M420 40 Q200 400 420 760'
    body += (f'<path d="{bow}" stroke="{INK}" stroke-width="34" />'
             f'<path d="{bow}" stroke="#7A4A2A" stroke-width="24" />'
             f'<path d="M412 60 Q214 400 412 740" stroke="#A86E48" stroke-width="6" />'
             f'<path d="M420 40 L420 760" stroke="#FFF1D6" stroke-width="3" />')
    for t in (0.12, 0.3, 0.5, 0.7, 0.88):
        x = (1 - t) ** 2 * 420 + 2 * (1 - t) * t * 200 + t ** 2 * 420
        y = (1 - t) ** 2 * 40 + 2 * (1 - t) * t * 400 + t ** 2 * 760
        body += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="22" ry="11" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
    body += (f'<path d="M420 40 l-12 -24 l24 0Z M420 760 l-12 24 l24 0Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
             f'<circle cx="310" cy="400" r="20" fill="#B5402E" stroke="{GOLD}" stroke-width="6" />')
    write('gandiva', body, "Arjuna's great bow, the Gandiva: dark wood, gold bands, a red jewel at the grip, a soft glow.")


# 8. the twang of the Gandiva: a gold sound-ring rolling outward
def gandiva_shockwave():
    body = ''
    for i, (r, w, op) in enumerate(((340, 10, 0.35), (270, 16, 0.6), (190, 22, 0.85), (110, 12, 0.6))):
        body += f'<circle cx="400" cy="400" r="{r}" fill="none" stroke="{GOLD}" stroke-width="{w}" opacity="{op}" />'
    body += ''.join(f'<path d="M{400 + 130 * math.cos(math.radians(a)):.0f} {400 + 130 * math.sin(math.radians(a)):.0f} L{400 + 370 * math.cos(math.radians(a)):.0f} {400 + 370 * math.sin(math.radians(a)):.0f}" stroke="{GOLD_L}" stroke-width="5" opacity="0.6" />'
                    for a in range(0, 360, 24))
    body += glow_rings(400, 400, 120, '#FFF1D6', 3, 0.2)
    write('gandiva-shockwave', body, 'concentric gold sound-rings and rays: the twang of the Gandiva that stunned the Kuru army.')


# 9. Bhishma (E04 tease): a tall old warrior in silhouette, white beard and hair lit
def bhishma_silhouette():
    body = person(400, 770, 660, rim='#E07A2E', robe=False, hair='crown')
    u = 66
    hy = 770 - 660 + u * 0.9
    body += (f'<path d="M{400 - u * 0.5:.0f} {hy + u * 0.3:.0f} Q400 {hy + u * 2.2:.0f} {400 + u * 0.6:.0f} {hy + u * 0.3:.0f} Q400 {hy + u * 1.0:.0f} {400 - u * 0.5:.0f} {hy + u * 0.3:.0f}Z" fill="#F3EEDF" stroke="{INK}" stroke-width="3" />'
             f'<path d="M{400 - u * 0.7:.0f} {hy - u * 0.3:.0f} Q{400 - u * 1.4:.0f} {hy + u * 0.8:.0f} {400 - u * 1.1:.0f} {hy + u * 1.6:.0f}" stroke="#F3EEDF" stroke-width="10" />'
             f'<path d="M560 160 Q690 420 560 680" stroke="{SIL}" stroke-width="14" /><path d="M560 160 L560 680" stroke="#E07A2E" stroke-width="2" opacity="0.7" />')
    write('bhishma-silhouette', body, 'Bhishma as a tall silhouette with a crown and bow; only his white beard and hair are lit (E04 tease).')


# 10. Amba (E04 tease): a tall woman's shadow, hair loose
def amba_shadow():
    body = glow_rings(400, 360, 340, '#B5402E', 3, 0.10)
    hair = (f'<path d="M400 110 Q300 140 280 300 Q260 420 220 520 Q300 420 330 330 Q350 230 400 170Z" fill="#2A1630" opacity="0.9" />'
            f'<path d="M420 110 Q500 150 520 300 Q540 380 580 440 Q500 380 470 300Z" fill="#2A1630" opacity="0.9" />')
    fig = person(400, 780, 680, rim='#B5402E', robe=True, hair=None)
    write('amba-shadow', f'<g opacity="0.88">{hair}{fig}</g>', 'a tall woman\'s shadow with loose flowing hair, a red rim of light (E04 tease: Amba).')


if __name__ == '__main__':
    celestial_chariot(); astra_ring(); family_vine(); year_ring(); bangles_scarred_arm()
    shami_tree(); gandiva(); gandiva_shockwave(); bhishma_silhouette(); amba_shadow()
