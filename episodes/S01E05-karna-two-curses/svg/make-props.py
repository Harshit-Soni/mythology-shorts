"""S01E05 props, drawn in code in the library's flat style (reuses the S01E02 helpers).

Run from the repo root:  python3 episodes/S01E05-karna-two-curses/svg/make-props.py [out_dir]
Writes assets/props/<id>.svg (800x800). Flat fills, outline #1E1420, no filters/text/images.
"""
import importlib.util
import math
import os
import random
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('p02', 'episodes/S01E02-kindama-curses-pandu/svg/make-props.py')
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
sys.argv = _argv
SVG, INK, GOLD, GOLD_L, GOLD_D, SIL = P.SVG, P.INK, P.GOLD, P.GOLD_L, P.GOLD_D, P.SIL
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/props'
glow_rings = P.glow_rings


def write(pid, body, desc, w=800, h=800):
    os.makedirs(OUT, exist_ok=True)
    svg = (f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" '
           f'stroke-linecap="round" stroke-linejoin="round"><desc>S01E05 | {pid} | {desc} '
           f'Made by episodes/S01E05-karna-two-curses/svg/make-props.py.</desc>{body}</svg>')
    ET.fromstring(svg)
    with open(f'{OUT}/{pid}.svg', 'w') as f:
        f.write(svg)
    print('wrote', f'{OUT}/{pid}.svg')


def pol(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def wheel(cx, cy, R, wood='#8A5A36', wood_d='#6E4228', rim=GOLD, rim_d=GOLD_D, rot=8):
    s = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{INK}" stroke-width="{R * .2 + 8:.0f}" /><circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{wood}" stroke-width="{R * .2:.0f}" />'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R * 1.06:.0f}" fill="none" stroke="{rim_d}" stroke-width="{R * .07:.0f}" /><circle cx="{cx}" cy="{cy}" r="{R * 1.075:.0f}" fill="none" stroke="{rim}" stroke-width="{R * .035:.0f}" />'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R * .9:.0f}" fill="none" stroke="{wood_d}" stroke-width="4" />'
    for i in range(12):
        a = rot + i * 30
        x1, y1 = pol(cx, cy, R * .2, a); x2, y2 = pol(cx, cy, R * .9, a)
        s += f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="{INK}" stroke-width="{R * .1 + 7:.0f}" /><path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="{wood}" stroke-width="{R * .1:.0f}" />'
        x3, y3 = pol(cx, cy, R * .58, a)
        s += f'<circle cx="{x3:.0f}" cy="{y3:.0f}" r="{R * .055:.0f}" fill="{rim}" stroke="{INK}" stroke-width="2.5" />'
        x4, y4 = pol(cx, cy, R, a + 15)
        s += f'<circle cx="{x4:.0f}" cy="{y4:.0f}" r="{R * .045:.0f}" fill="{rim}" stroke="{INK}" stroke-width="2.5" />'
    s += (f'<circle cx="{cx}" cy="{cy}" r="{R * .24:.0f}" fill="{rim_d}" stroke="{INK}" stroke-width="5" /><circle cx="{cx}" cy="{cy}" r="{R * .16:.0f}" fill="{rim}" stroke="{INK}" stroke-width="4" />'
          f'<circle cx="{cx}" cy="{cy}" r="{R * .07:.0f}" fill="{wood_d}" stroke="{INK}" stroke-width="3" />')
    return s


# 1. Karna's wheel, the lower part swallowed by the earth
def sunk_wheel():
    random.seed(3)
    top = 520
    body = f'<g transform="rotate(-9 400 400)">'
    # a corner of the chariot body behind, tipped with the wheel
    body += (f'<path d="M400 150 L770 122 Q800 220 776 332 L420 350Z" fill="#5E3A26" stroke="{INK}" stroke-width="6" /><path d="M404 170 L776 142 L782 176 L408 204Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" />'
             + ''.join(f'<circle cx="{450 + k * 62}" cy="{262 - k * 4}" r="13" fill="{GOLD}" stroke="{INK}" stroke-width="3" />' for k in range(5)) + '</g>')
    body += wheel(390, 400, 282)
    # earth: a torn lip over the bottom of the wheel, cracks running out
    edge = f'M10 {top + 96} L70 {top + 60} L130 {top + 66} L180 {top + 10} L240 {top + 30} L300 {top - 14} L352 {top + 22} L420 {top - 8} L470 {top + 24} L540 {top - 4} L600 {top + 34} L660 {top + 18} L720 {top + 68} L790 {top + 96}'
    body += f'<path d="{edge} Q700 {top + 190} 400 {top + 200} Q100 {top + 190} 10 {top + 96}Z" fill="#8E4A34" stroke="{INK}" stroke-width="6" />'
    body += f'<path d="M60 {top + 120} L140 {top + 98} L220 {top + 118} L330 {top + 84} L450 {top + 112} L560 {top + 88} L690 {top + 118} L740 {top + 124} Q620 {top + 184} 400 {top + 188} Q180 {top + 184} 60 {top + 120}Z" fill="#A65C40" />'
    for x, y in ((180, top + 40), (300, top + 20), (430, top + 30), (560, top + 30), (660, top + 50)):
        d = f'M{x} {y}'
        cx, cy = x, y
        for _ in range(4):
            cx += random.uniform(-40, 40); cy += random.uniform(22, 38)
            d += f' L{cx:.0f} {cy:.0f}'
        body += f'<path d="{d}" stroke="#3E1C16" stroke-width="8" /><path d="{d}" stroke="#E07A2E" stroke-width="2.5" opacity="0.7" />'
    for x, y, r in ((110, top + 8, 26), (250, top - 4, 20), (640, top - 8, 24), (716, top + 14, 16), (480, top - 20, 16)):
        body += f'<path d="M{x - r} {y + r * .5:.0f} L{x - r * .6:.0f} {y - r * .7:.0f} L{x + r * .5:.0f} {y - r * .8:.0f} L{x + r} {y + r * .4:.0f} L{x} {y + r * .8:.0f}Z" fill="#B8694A" stroke="{INK}" stroke-width="4" />'
    write('sunk-wheel', body,
          "Karna's chariot wheel, its lower part swallowed by cracked red earth.")


# 2. the homa cow, alive: white, garlanded, a bell at her neck
def homa_cow():
    def leg(x, y, dx, col):
        return (f'<path d="M{x - 30} {y} Q{x - 24 + dx} {y + 110} {x - 18 + dx} {y + 190} L{x - 24 + dx} {y + 214} L{x + 26 + dx} {y + 214} L{x + 20 + dx} {y + 190} Q{x + 30 + dx} {y + 100} {x + 36} {y}Z" fill="{col}" stroke="{INK}" stroke-width="5" />'
                f'<path d="M{x - 26 + dx} {y + 196} L{x + 24 + dx} {y + 196} L{x + 28 + dx} {y + 218} L{x - 28 + dx} {y + 218}Z" fill="#4E3A34" stroke="{INK}" stroke-width="4" />')
    b = '<ellipse cx="400" cy="702" rx="300" ry="26" fill="#000" opacity="0.14" />'
    b += leg(262, 474, -4, '#DCCFBE') + leg(536, 474, 6, '#DCCFBE')
    b += leg(206, 480, -6, '#F8F1E6') + leg(486, 484, 4, '#F8F1E6')
    # tail
    b += f'<path d="M150 360 Q96 400 108 520 Q110 560 96 590" stroke="{INK}" stroke-width="22" /><path d="M150 360 Q96 400 108 520 Q110 560 96 590" stroke="#EFE5D6" stroke-width="14" /><path d="M96 580 Q70 630 92 660 Q122 640 112 584Z" fill="#6E5A50" stroke="{INK}" stroke-width="4" />'
    # body with the zebu hump
    b += (f'<path d="M140 372 Q150 314 250 318 Q330 326 400 312 Q426 236 486 252 Q540 270 548 330 Q590 350 596 420 Q590 500 560 528 Q420 570 260 540 Q170 530 150 470 Q134 420 140 372Z" fill="#F8F1E6" stroke="{INK}" stroke-width="6" />'
          '<path d="M160 470 Q260 528 420 532 Q520 530 570 500 Q540 556 420 556 Q240 556 160 470Z" fill="#DCCFBE" />'
          '<path d="M420 320 Q440 270 486 268" stroke="#FFFFFF" stroke-width="9" /><path d="M210 340 Q300 350 380 336" stroke="#FFFFFF" stroke-width="10" />')
    # neck, dewlap, head
    b += (f'<path d="M520 300 Q590 250 640 236 L690 330 Q650 400 610 470 Q590 520 560 500 Q540 420 520 300Z" fill="#F8F1E6" stroke="{INK}" stroke-width="6" />'
          '<path d="M600 440 Q580 500 566 496 Q570 440 612 380Z" fill="#DCCFBE" />'
          f'<path d="M622 250 Q592 160 636 96 Q628 170 664 226Z" fill="#CDB79A" stroke="{INK}" stroke-width="5" /><path d="M676 226 Q706 150 690 84 Q738 150 712 238Z" fill="#E0CDB2" stroke="{INK}" stroke-width="5" />'
          f'<path d="M626 250 Q566 236 536 268 Q566 312 630 292Z" fill="#EAD9CC" stroke="{INK}" stroke-width="5" /><path d="M612 264 Q582 256 558 270 Q580 290 612 282Z" fill="#E3A79A" />'
          f'<path d="M630 232 Q672 206 714 234 Q738 290 748 350 Q752 392 716 402 Q680 404 664 372 Q628 310 630 232Z" fill="#F8F1E6" stroke="{INK}" stroke-width="6" />'
          f'<path d="M676 366 Q700 340 748 348 Q756 392 718 402 Q684 402 676 366Z" fill="#E3B3A4" stroke="{INK}" stroke-width="4" /><ellipse cx="734" cy="368" rx="6" ry="4" fill="{INK}" />'
          f'<path d="M664 286 Q682 270 702 284 Q684 300 664 286Z" fill="#FFFFFF" stroke="{INK}" stroke-width="4" /><circle cx="685" cy="285" r="8" fill="{INK}" /><circle cx="688" cy="282" r="2.5" fill="#FFF" />'
          f'<path d="M660 274 Q682 258 706 274" stroke="{INK}" stroke-width="4" /><path d="M690 388 Q712 394 734 386" stroke="{INK}" stroke-width="4" />'
          '<path d="M664 240 q8 14 0 28" stroke="#B5402E" stroke-width="9" />')
    # marigold garland and the bell
    for i in range(13):
        t = i / 12
        x = 566 + (668 - 566) * t - 20 * math.sin(math.pi * t); y = 286 + (400 - 286) * t + 130 * math.sin(math.pi * t)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="19" fill="{("#F2A03E", "#E8B53A", "#E07A2E")[i % 3]}" stroke="{INK}" stroke-width="3" /><circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#B8601F" />'
    b += bell(598, 520, 0.42)
    write('homa-cow', b, 'the homa cow, alive: a white zebu cow with a marigold garland and a bell.')


def bell(x, y, s, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M0 -120 Q-26 -120 -26 -92 Q-26 -70 0 -70 Q26 -70 26 -92 Q26 -120 0 -120Z" fill="none" stroke="{INK}" stroke-width="22" /><path d="M0 -120 Q-26 -120 -26 -92 Q-26 -70 0 -70 Q26 -70 26 -92 Q26 -120 0 -120Z" fill="none" stroke="{GOLD_D}" stroke-width="12" />'
            f'<circle cx="0" cy="118" r="26" fill="{GOLD_D}" stroke="{INK}" stroke-width="7" />'
            f'<path d="M-40 -72 Q0 -92 40 -72 Q76 -20 82 60 Q90 84 112 100 Q0 132 -112 100 Q-90 84 -82 60 Q-76 -20 -40 -72Z" fill="{GOLD}" stroke="{INK}" stroke-width="8" />'
            f'<path d="M-84 56 Q0 84 84 56" stroke="{GOLD_D}" stroke-width="9" /><path d="M-62 4 Q0 24 62 4" stroke="{GOLD_D}" stroke-width="7" /><path d="M-34 -58 Q-58 -10 -62 50" stroke="{GOLD_L}" stroke-width="13" /></g>')


# 3. all that is shown of the death: the bell on the sand, a broken garland
def cow_bell():
    b = '<ellipse cx="400" cy="640" rx="330" ry="54" fill="#8E6A3E" opacity="0.35" />'
    b += f'<path d="M404 372 Q470 300 560 352 Q640 410 690 520" stroke="{INK}" stroke-width="26" /><path d="M404 372 Q470 300 560 352 Q640 410 690 520" stroke="#9E3B22" stroke-width="16" /><path d="M690 520 l14 40 M690 520 l-10 42 M690 520 l34 26" stroke="#9E3B22" stroke-width="6" />'
    random.seed(6)
    for i in range(9):
        x, y = 96 + i * 34 + random.uniform(-10, 10), 640 - 46 * math.sin(i / 8 * math.pi * 1.2) + random.uniform(-10, 10)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="32" fill="{("#F2A03E", "#E8B53A", "#E07A2E")[i % 3]}" stroke="{INK}" stroke-width="5" />' + ''.join(f'<path d="M{x:.0f} {y:.0f} l{20 * math.cos(k):.0f} {20 * math.sin(k):.0f}" stroke="#B8601F" stroke-width="4" />' for k in (0, 1.05, 2.1, 3.14, 4.2, 5.2))
    for x, y in ((600, 660), (660, 690), (520, 704), (720, 640)):
        b += f'<path d="M{x} {y} q18 -16 34 0 q-14 16 -34 0Z" fill="#E8B53A" stroke="{INK}" stroke-width="3" />'
    b += bell(420, 520, 1.28, 24)
    write('cow-bell', b, "the cow's brass bell on its snapped cord, beside a broken marigold garland.")


# 4. the insect (Shanti 3): like a hog, eight feet, sharp fangs, needle bristles
def worm_body(cx, cy, s, rot=0):
    g = f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
    for i, x in enumerate((-190, -90, 20, 120)):                                  # four legs on each side = eight
        g += (f'<path d="M{x} 60 q-34 70 -70 80 l-18 50" stroke="{INK}" stroke-width="24" /><path d="M{x} 60 q-34 70 -70 80 l-18 50" stroke="#5E2A2A" stroke-width="14" />'
              f'<path d="M{x + 44} 70 q40 60 56 90 l26 40" stroke="{INK}" stroke-width="26" /><path d="M{x + 44} 70 q40 60 56 90 l26 40" stroke="#7A3838" stroke-width="16" />')
    for i in range(24):                                                            # bristles
        a = 186 + i * 7.2
        x1, y1 = -20 + 250 * math.cos(math.radians(a)), 150 * math.sin(math.radians(a))
        l = 1.36 + .12 * (i % 3)
        g += f'<path d="M{x1:.0f} {y1:.0f} L{-20 + 250 * l * math.cos(math.radians(a + 5)):.0f} {150 * l * math.sin(math.radians(a + 5)):.0f}" stroke="{INK}" stroke-width="9" />'
    g += f'<path d="M-282 10 Q-270 -140 -60 -152 Q150 -150 226 -40 Q250 60 130 110 Q-60 150 -220 106 Q-280 80 -282 10Z" fill="#8E3F3C" stroke="{INK}" stroke-width="9" />'
    g += '<path d="M-220 84 Q-60 130 120 96 Q60 140 -80 132 Q-180 124 -220 84Z" fill="#5E2A2A" />'
    g += ''.join(f'<path d="M{x} {-148 + abs(x + 40) * .18:.0f} Q{x - 40} 0 {x} {118 - abs(x + 40) * .1:.0f}" stroke="#5E2A2A" stroke-width="9" />' for x in (-190, -100, -10, 80))
    g += '<path d="M-200 -70 Q-110 -124 10 -120" stroke="#C4726A" stroke-width="14" opacity="0.8" />'
    # hog-like head and snout, fangs
    g += (f'<path d="M150 -96 Q232 -120 288 -66 Q344 -54 352 -6 Q352 40 296 46 Q230 92 150 76 Q110 -10 150 -96Z" fill="#9E4A44" stroke="{INK}" stroke-width="9" />'
          f'<path d="M306 -50 Q356 -44 356 0 Q352 40 308 38 Q292 -6 306 -50Z" fill="#C98A7E" stroke="{INK}" stroke-width="7" /><ellipse cx="334" cy="-16" rx="7" ry="10" fill="{INK}" /><ellipse cx="334" cy="14" rx="7" ry="10" fill="{INK}" />'
          f'<path d="M166 -92 L140 -160 L214 -112Z" fill="#7A3838" stroke="{INK}" stroke-width="7" />'
          f'<path d="M220 46 L236 118 L262 48Z M268 44 L290 112 L306 40Z" fill="#FFF8E9" stroke="{INK}" stroke-width="6" />'
          f'<path d="M206 52 Q256 66 310 42" stroke="{INK}" stroke-width="8" />'
          f'<path d="M212 -44 Q238 -66 268 -40 Q240 -22 212 -44Z" fill="#F2C14E" stroke="{INK}" stroke-width="6" /><path d="M241 -54 L241 -32" stroke="{INK}" stroke-width="8" /><path d="M200 -66 L270 -56" stroke="{INK}" stroke-width="11" />')
    return g + '</g>'


def alarka():
    write('alarka-worm', glow_rings(400, 420, 360, '#B5402E', 3, 0.07) + worm_body(418, 420, 0.92, -6),
          'the insect Alarka (Shanti 3): like a hog, eight feet, sharp fangs, needle bristles.')


# 5. the insect on the cloth over his thigh, one thin red line
def worm_on_thigh():
    b = (f'<path d="M-30 330 Q170 190 420 214 Q640 236 830 360 L830 830 L-30 830Z" fill="#E3CFA2" stroke="{INK}" stroke-width="7" />'
         '<path d="M-30 620 Q200 500 440 520 Q660 544 830 640 L830 830 L-30 830Z" fill="#CFB883" /><path d="M-30 760 Q240 660 460 676 Q680 694 830 780 L830 830 L-30 830Z" fill="#BFA473" />'
         '<path d="M30 400 Q200 290 400 296 M500 290 Q660 330 790 430 M40 540 Q240 420 440 430 M560 450 Q690 480 810 560 M60 700 Q260 600 470 610" stroke="#957C50" stroke-width="7" />'
         '<path d="M50 330 Q220 228 420 238" stroke="#F6EACB" stroke-width="10" />')
    b += '<path d="M560 356 Q586 440 566 520 Q556 590 580 680" stroke="#A62A26" stroke-width="9" /><ellipse cx="560" cy="350" rx="30" ry="13" fill="#A62A26" opacity="0.85" />'
    b += worm_body(410, 236, 0.6, 18)
    write('worm-on-thigh', b, 'close-up: the insect on the cloth over his thigh, one thin red line; no wound. Placed so the cloth runs off the bottom of the frame.')


# 6. the Brahmin's words as a vision: a wheel of light, sinking
def wheel_light():
    b = glow_rings(400, 380, 380, '#F2A03E', 4, 0.09)
    g = ''.join(f'<circle cx="400" cy="380" r="{r}" fill="none" stroke="{c}" stroke-width="{w}" opacity="{o}" />' for r, c, w, o in ((250, '#F2A03E', 34, .35), (250, '#FFE6A8', 12, 1), (216, '#FFE6A8', 5, .9), (52, '#FFE6A8', 10, 1)))
    for i in range(12):
        x1, y1 = pol(400, 380, 52, i * 30 + 6); x2, y2 = pol(400, 380, 216, i * 30 + 6)
        g += f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="#F2A03E" stroke-width="20" opacity="0.3" /><path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="#FFE6A8" stroke-width="7" />'
    b += f'<defs><clipPath id="wl"><rect x="0" y="0" width="800" height="520" /></clipPath></defs><g clip-path="url(#wl)">{g}</g>'
    b += '<path d="M70 524 L150 508 L220 530 L300 506 L370 526 L450 504 L530 528 L610 508 L730 526" stroke="#FFE6A8" stroke-width="10" /><path d="M200 530 l-30 60 l22 46 M400 520 l14 70 l-22 60 M600 520 l34 56 l-16 60" stroke="#F2A03E" stroke-width="7" opacity="0.9" />'
    write('wheel-light', b, "the curse as a vision: a chariot wheel drawn in light, half sunk below a cracking line of earth.")


# 7. the weapon that doesn't come: the astra ring, dark and cracked
def ring_dark():
    src = open('assets/props/astra-ring.svg').read()
    inner = src[src.index('>', src.index('<desc')) and src.index('</desc>') + 7:src.rindex('</svg>')]
    import re
    def grey(m):
        h = m.group(0)[1:]
        r, g, b_ = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        v = int((.3 * r + .59 * g + .11 * b_) * .42 + 22)
        return '#%02X%02X%02X' % (v, v, min(255, v + 10))
    inner = re.sub(r'#[0-9A-Fa-f]{6}', grey, inner)
    b = f'<circle cx="400" cy="400" r="350" fill="#241A2A" opacity="0.45" />{inner}'
    for d in ('M400 60 L430 190 L384 290 L420 400 L360 520 L400 640 L380 740', 'M420 400 L540 430 L640 520', 'M384 290 L270 270 L150 210', 'M360 520 L250 560 L170 640', 'M430 190 L540 150'):
        b += f'<path d="{d}" stroke="#0E0A12" stroke-width="14" /><path d="{d}" stroke="#7A6E86" stroke-width="3" />'
    write('astra-ring-dark', b, 'the Brahmastra ring gone dark and cracked: the weapon does not come.')


# 8. Nahusha (E06 tease): a crowned king whose shadow is a serpent
def nahusha():
    b = glow_rings(400, 360, 370, '#E8B53A', 4, 0.09)
    # his shadow on the wall: a cobra rearing up, hood spread, coils at the floor
    sh, hi = '#6A2438', '#E8B53A'
    b += (f'<path d="M470 776 Q600 716 752 752 Q792 786 730 798 L480 798Z" fill="{sh}" /><path d="M520 720 Q640 676 728 712 Q756 738 712 752 Q600 752 520 720Z" fill="{sh}" stroke="#4A1626" stroke-width="5" />'
          f'<path d="M660 720 Q560 640 596 520 Q610 450 596 396 L700 396 Q706 470 690 540 Q676 620 744 712Z" fill="{sh}" />'
          f'<path d="M648 96 Q716 92 732 160 Q796 220 778 316 Q752 408 648 414 Q544 408 518 316 Q500 220 564 160 Q580 92 648 96Z" fill="{sh}" stroke="#4A1626" stroke-width="6" />'
          f'<path d="M648 104 Q708 104 714 168 Q716 226 648 246 Q580 226 582 168 Q588 104 648 104Z" fill="#7E3048" />'
          f'<path d="M596 152 L634 170 L604 182Z M700 152 L662 170 L692 182Z" fill="{hi}" /><circle cx="613" cy="170" r="5" fill="#1E1420" /><circle cx="683" cy="170" r="5" fill="#1E1420" />'
          f'<path d="M648 236 L648 284 M648 284 L630 312 M648 284 L666 312" stroke="#E07A2E" stroke-width="8" />'
          f'<path d="M556 220 Q536 310 600 380 M740 220 Q760 310 696 380" stroke="#8E3A50" stroke-width="9" />'
          + ''.join(f'<path d="M{610 - k * 2} {430 + k * 44} Q648 {446 + k * 44} {694 - k * 3} {430 + k * 44}" stroke="#8E3A50" stroke-width="6" />' for k in range(6)))
    # the king in front: a tall tiered kirita, earrings, a draped shoulder cloth
    king = ('<path d="M186 196 Q190 156 214 148 Q214 112 238 104 Q242 66 260 40 Q278 66 282 104 Q306 112 306 148 Q330 156 334 196 Q260 222 186 196Z" />'
            '<path d="M192 186 Q188 300 260 330 Q332 300 328 186Z" /><path d="M222 306 L298 306 L306 366 L214 366Z" />'
            '<path d="M214 352 Q128 366 104 452 Q84 560 96 660 L138 668 Q146 580 162 520 L150 798 L370 798 L358 520 Q374 580 382 668 L424 660 Q436 560 416 452 Q392 366 306 352Z" />')
    b += f'<g fill="{GOLD}" transform="translate(6 -5)" opacity="0.95">{king}</g><g fill="{SIL}">{king}</g>'
    b += (f'<path d="M190 190 Q260 216 330 190 M214 150 Q260 168 306 150 M238 106 Q260 116 282 106" stroke="{GOLD}" stroke-width="8" /><circle cx="260" cy="176" r="12" fill="{GOLD}" /><circle cx="260" cy="138" r="8" fill="{GOLD}" />'
          f'<circle cx="184" cy="268" r="17" fill="none" stroke="{GOLD}" stroke-width="8" /><circle cx="336" cy="268" r="17" fill="none" stroke="{GOLD}" stroke-width="8" />'
          f'<path d="M196 382 Q260 458 324 382" stroke="{GOLD}" stroke-width="8" /><path d="M300 356 Q220 470 156 560" stroke="{GOLD}" stroke-width="10" opacity="0.85" /><path d="M156 520 Q260 546 364 520" stroke="{GOLD}" stroke-width="9" />')
    write('nahusha-silhouette', b, 'a crowned king in silhouette; the shadow behind him is a rearing cobra (E06 tease: Nahusha).')


if __name__ == '__main__':
    sunk_wheel(); homa_cow(); cow_bell(); alarka(); worm_on_thigh(); wheel_light(); ring_dark(); nahusha()
