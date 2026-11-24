"""S01E05 backgrounds, drawn in code in the library's flat style (reuses the S01E02 helpers).

mahendra-ashram  Parashurama's hermitage: a stone terrace high on Mount Mahendra, a thatched hut, a banyan, the sea far below; feet 0.84
sea-shore        the beach near the hermitage (Shanti 2: "on the sea-coast by the side of that asylum"); feet 0.84
1296x2112 canvas (frame 1080x1920 + margins); layers layer-far / layer-mid / layer-ground.
Run from the repo root:  python3 episodes/S01E05-karna-two-curses/svg/make-backgrounds.py [out_dir]
"""
import importlib.util
import random
import sys

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('b02', 'episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py')
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)
sys.argv = _argv
if len(sys.argv) > 1:
    B.OUT = sys.argv[1]
W, H, INK, fy = B.W, B.H, B.INK, B.fy


def finish(bid):
    p = f'{B.OUT}/{bid}.svg'
    s = open(p).read().replace(f'S01E02 | {bid}', f'S01E05 | {bid}').replace(
        'episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py', 'episodes/S01E05-karna-two-curses/svg/make-backgrounds.py')
    open(p, 'w').write(s)


def leaves(cx, cy, r, cols, n=9, seed=1):
    rnd = random.Random(seed)
    return ''.join(f'<ellipse cx="{cx + rnd.uniform(-r, r):.0f}" cy="{cy + rnd.uniform(-r * .55, r * .55):.0f}" rx="{r * rnd.uniform(.45, .65):.0f}" ry="{r * rnd.uniform(.3, .45):.0f}" '
                   f'fill="{rnd.choice(cols)}" stroke="{INK}" stroke-width="3" />' for _ in range(n))


def ashram():
    random.seed(5)
    defs = (B.vgrad('ma-sky', ((0, '#6FA3C9'), (0.45, '#BFD9E0'), (0.75, '#F7E3BE'), (1, '#F6D3A0')))
            + B.vgrad('ma-sea', ((0, '#8FBFD0'), (1, '#4F8AA8'))))
    far = f'<rect width="{W}" height="{H}" fill="url(#ma-sky)" />'
    far += '<circle cx="360" cy="820" r="105" fill="#FFF3D2" opacity="0.9" /><circle cx="360" cy="820" r="190" fill="#FFE9B8" opacity="0.28" />'
    far += B.curl_cloud(820, 430, 1.1, '#FFFFFF', '#D9E6EA', 0.85) + B.curl_cloud(150, 600, 0.8, '#FFFFFF', '#D9E6EA', 0.7)
    far += f'<rect x="0" y="1090" width="{W}" height="520" fill="url(#ma-sea)" />'
    far += ''.join(f'<path d="M{random.uniform(0, W):.0f} {random.uniform(1110, 1330):.0f} q30 -8 60 0" stroke="#CFE8EE" stroke-width="4" opacity="0.7" />' for _ in range(26))
    far += '<path d="M300 1092 L420 1092 L470 1400 L250 1400Z" fill="#FFF3D2" opacity="0.2" />'
    # Mahendra's shoulders, far to near
    mid = f'<path d="M{W} 900 Q1130 930 1050 1080 Q960 1200 820 1330 L820 1620 L{W} 1620Z" fill="#7F9C8C" />'
    mid += f'<path d="M0 1150 Q160 1120 260 1230 Q360 1350 520 1420 Q620 1480 700 1620 L0 1620Z" fill="#6A8A74" />'
    mid += f'<path d="M{W} 1130 Q1170 1150 1080 1270 Q960 1390 820 1440 Q700 1500 620 1620 L{W} 1620Z" fill="#5C7C66" stroke="#4A6654" stroke-width="3" />'
    # the hut (right, at the back of the terrace)
    hx, hb = 1020, 1560
    mid += (f'<path d="M{hx - 190} {hb} L{hx - 176} {hb - 230} L{hx + 250} {hb - 230} L{hx + 260} {hb}Z" fill="#B98A58" stroke="{INK}" stroke-width="4" />'
            + ''.join(f'<path d="M{x} {hb - 228} L{x + 4} {hb}" stroke="#946A40" stroke-width="5" />' for x in range(hx - 150, hx + 250, 46))
            + f'<path d="M{hx - 40} {hb} L{hx - 40} {hb - 140} Q{hx + 14} {hb - 196} {hx + 68} {hb - 140} L{hx + 68} {hb}Z" fill="#3E2A1E" stroke="{INK}" stroke-width="4" />'
            f'<path d="M{hx - 260} {hb - 206} Q{hx - 60} {hb - 480} {hx + 40} {hb - 500} Q{hx + 140} {hb - 480} {hx + 330} {hb - 206} Q{hx + 30} {hb - 250} {hx - 260} {hb - 206}Z" fill="#D9B05E" stroke="{INK}" stroke-width="4" />'
            + ''.join(f'<path d="M{hx + 40} {hb - 492} Q{hx + 40 + d * .5:.0f} {hb - 360} {hx + 40 + d} {hb - 224}" stroke="#B08A3E" stroke-width="4" />' for d in range(-250, 270, 50)))
    # the banyan (left)
    mid += (f'<path d="M-60 1600 Q60 1500 70 1250 Q60 1120 10 1000 L130 1010 Q150 1120 190 1060 L236 1084 Q190 1180 180 1300 Q190 1500 270 1600Z" fill="#6E4C34" stroke="{INK}" stroke-width="4" />'
            '<path d="M90 1080 Q110 1300 96 1560 M140 1120 Q140 1320 170 1570" stroke="#52372A" stroke-width="6" />'
            + ''.join(f'<path d="M{x} {y} q{random.uniform(-10, 10):.0f} {l * .5:.0f} 0 {l}" stroke="#7E5A3E" stroke-width="6" />' for x, y, l in ((250, 1030, 260), (300, 990, 180), (350, 960, 240), (20, 1020, 280)))
            + leaves(110, 930, 260, ('#3B6653', '#4A7A5E', '#2F5546'), 16, 3) + leaves(300, 900, 130, ('#4A7A5E', '#3B6653'), 6, 8))
    g = fy(0.84)
    ground = (f'<path d="M0 1560 Q320 1535 700 1548 Q1040 1558 {W} 1540 L{W} {H} L0 {H}Z" fill="#B7A48A" stroke="{INK}" stroke-width="3" />'
              f'<path d="M0 1640 Q500 1612 900 1630 Q1120 1640 {W} 1624 L{W} {H} L0 {H}Z" fill="#A8947A" />'
              f'<ellipse cx="648" cy="{g + 14:.0f}" rx="480" ry="46" fill="#C6B497" opacity="0.7" />')
    for _ in range(16):
        x, y = random.uniform(-20, W), random.uniform(1650, H - 60)
        ground += f'<path d="M{x:.0f} {y:.0f} l{random.uniform(80, 170):.0f} {random.uniform(-8, 8):.0f}" stroke="#8E7B62" stroke-width="4" opacity="0.7" />'
    for x in (30, 90, 1190, 1250, 1150):
        ground += f'<path d="M{x} 1650 q-14 -40 -24 -64 M{x} 1650 q0 -46 4 -76 M{x} 1650 q12 -36 26 -56" stroke="#5C7A3E" stroke-width="6" />'
    # a small fire altar at the terrace edge
    ground += (f'<path d="M560 1600 L760 1600 L738 1552 L582 1552Z" fill="#9A5A3E" stroke="{INK}" stroke-width="4" /><path d="M574 1576 L748 1576" stroke="#7A4230" stroke-width="4" />'
               f'<path d="M630 1552 Q612 1510 650 1470 Q654 1500 676 1506 Q696 1524 690 1552Z" fill="#F2A03E" stroke="{INK}" stroke-width="3" /><path d="M646 1552 Q640 1530 656 1510 Q672 1530 670 1552Z" fill="#FFE08A" />')
    B.write('mahendra-ashram', defs, far, mid, ground, "Parashurama's hermitage on Mount Mahendra: a stone terrace, a thatched hut, a banyan and a fire altar, the sea far below; feet at frame 0.84.")
    finish('mahendra-ashram')


def palm(x, base, h, lean, s=1.0, seed=1):
    rnd = random.Random(seed)
    tx, ty = x + lean, base - h
    p = (f'<path d="M{x - 18 * s:.0f} {base} Q{x + lean * .2 - 10:.0f} {base - h * .5:.0f} {tx - 9:.0f} {ty} L{tx + 9:.0f} {ty} Q{x + lean * .2 + 18:.0f} {base - h * .5:.0f} {x + 20 * s:.0f} {base}Z" fill="#7E5A3E" stroke="{INK}" stroke-width="3" />')
    for a, l in ((-165, 190), (-140, 210), (-110, 180), (-70, 180), (-40, 210), (-12, 190), (20, 150), (200, 150)):
        import math
        ex, ey = tx + math.cos(math.radians(a)) * l * s, ty + math.sin(math.radians(a)) * l * .55 * s + 60 * s
        mx, my = (tx + ex) / 2, min(ty, ey) - 46 * s
        p += f'<path d="M{tx:.0f} {ty:.0f} Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f} Q{mx:.0f} {my + 44 * s:.0f} {tx:.0f} {ty + 12:.0f}Z" fill="{rnd.choice(("#3B6653", "#4A7A5E", "#2F5546"))}" stroke="{INK}" stroke-width="3" />'
    p += ''.join(f'<circle cx="{tx + d:.0f}" cy="{ty + 18:.0f}" r="{13 * s:.0f}" fill="#8E6A3E" stroke="{INK}" stroke-width="3" />' for d in (-14, 12))
    return p


def shore():
    random.seed(9)
    defs = (B.vgrad('ss-sky', ((0, '#5F86B4'), (0.4, '#E3B9A0'), (0.62, '#F9DCA8'), (1, '#FBE9C6')))
            + B.vgrad('ss-sea', ((0, '#7FB2BE'), (0.6, '#4A8AA0'), (1, '#3A7690'))))
    far = f'<rect width="{W}" height="{H}" fill="url(#ss-sky)" />'
    far += '<circle cx="520" cy="1080" r="130" fill="#FFF0C4" opacity="0.95" /><circle cx="520" cy="1080" r="230" fill="#FFE2A0" opacity="0.3" />'
    far += B.curl_cloud(760, 520, 1.2, '#FFF1E0', '#E8CDB8', 0.85) + B.curl_cloud(170, 720, 0.8, '#FFF1E0', '#E8CDB8', 0.7)
    mid = f'<rect x="0" y="1150" width="{W}" height="420" fill="url(#ss-sea)" />'
    mid += '<path d="M430 1152 L610 1152 L700 1560 L340 1560Z" fill="#FFE9B0" opacity="0.28" />'
    mid += f'<path d="M{W} 960 Q1190 980 1120 1060 Q1060 1130 960 1160 L{W} 1160Z" fill="#6A7F86" />'   # Mahendra's headland
    for y, n, sw in ((1200, 9, 3), (1270, 8, 4), (1350, 7, 5), (1440, 6, 6)):
        mid += ''.join(f'<path d="M{random.uniform(0, W):.0f} {y + random.uniform(-16, 16):.0f} q{40 + sw * 6} -{6 + sw} {80 + sw * 12} 0" stroke="#BFE0E4" stroke-width="{sw}" opacity="0.8" />' for _ in range(n))
    # breakers on the sand
    mid += (f'<path d="M0 1540 Q160 1500 330 1536 Q520 1576 720 1536 Q940 1496 1120 1540 Q1220 1560 {W} 1530 L{W} 1620 L0 1620Z" fill="#EAF6F4" />'
            f'<path d="M0 1540 Q160 1500 330 1536 Q520 1576 720 1536 Q940 1496 1120 1540 Q1220 1560 {W} 1530" stroke="#9CC6CC" stroke-width="5" />')
    g = fy(0.84)
    ground = (f'<path d="M0 1590 Q200 1556 420 1584 Q700 1620 960 1578 Q1140 1556 {W} 1582 L{W} {H} L0 {H}Z" fill="#E6C893" stroke="#B8965E" stroke-width="3" />'
              f'<path d="M0 1700 Q420 1664 860 1694 Q1100 1708 {W} 1686 L{W} {H} L0 {H}Z" fill="#DBB97E" />'
              f'<ellipse cx="648" cy="{g + 14:.0f}" rx="480" ry="42" fill="#EED7A8" opacity="0.7" />')
    ground += palm(70, 1660, 720, 120, 1.0, 2) + palm(1240, 1640, 600, -90, 0.9, 5)
    for x in list(range(10, 200, 24)) + list(range(1130, 1290, 24)):
        h = random.uniform(60, 120)
        ground += f'<path d="M{x} 1668 q{random.uniform(-16, 16):.0f} -{h / 2:.0f} {random.uniform(-14, 14):.0f} -{h:.0f}" stroke="#8E9A4A" stroke-width="6" />'
    for _ in range(40):
        x, y = random.uniform(0, W), random.uniform(1720, H - 40)
        ground += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(4, 12):.0f}" ry="4" fill="#C49F62" />'
    for x, y, r in ((260, 1800, 20), (980, 1840, 24), (760, 1960, 16)):
        ground += f'<path d="M{x - r} {y} Q{x} {y - r * 1.6:.0f} {x + r} {y} Q{x} {y + r * .5:.0f} {x - r} {y}Z" fill="#F3E2CC" stroke="{INK}" stroke-width="2.5" /><path d="M{x} {y} L{x - r * .5:.0f} {y - r * .7:.0f} M{x} {y} L{x} {y - r * .9:.0f} M{x} {y} L{x + r * .5:.0f} {y - r * .7:.0f}" stroke="#B98F6A" stroke-width="2" />'
    B.write('sea-shore', defs, far, mid, ground, 'the beach below Mount Mahendra: a low sun on the sea, breakers, palms, dune grass; feet at frame 0.84.')
    finish('sea-shore')


if __name__ == '__main__':
    ashram(); shore()
