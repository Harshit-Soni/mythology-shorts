"""S01E06 backgrounds, drawn in code in the library's flat style (reuses the S01E02/E05 helpers).

indra-sabha     Indra's hall on the clouds: white and gold pillars, the great throne in the middle (seat base 0.60); feet 0.86
heaven-sky      the sky road of heaven: deep sky, curl-clouds, a band of stars; no ground (figures in close-up, or on the palanquin)
himalaya-gorge  a gorge in the Himalaya: snow peaks, rock walls, a cave mouth at the left; feet 0.84
1296x2112 canvas (frame 1080x1920 + margins); layers layer-far / layer-mid / layer-ground.
Run from the repo root:  python3 episodes/S01E06-nahusha-becomes-a-snake/svg/make-backgrounds.py [out_dir]
"""
import importlib.util
import math
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
GOLD, GOLD_L, GOLD_D = '#E8B53A', '#F4D17B', '#B8862A'


def finish(bid):
    p = f'{B.OUT}/{bid}.svg'
    s = open(p).read().replace(f'S01E02 | {bid}', f'S01E06 | {bid}').replace(
        'episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py', 'episodes/S01E06-nahusha-becomes-a-snake/svg/make-backgrounds.py')
    open(p, 'w').write(s)


def pillar(x, top, base, w):
    s = f'<path d="M{x - w / 2:.0f} {top + 70} L{x - w / 2:.0f} {base - 60} L{x + w / 2:.0f} {base - 60} L{x + w / 2:.0f} {top + 70}Z" fill="#F6EEE0" stroke="{INK}" stroke-width="4" />'
    s += f'<path d="M{x + w * .18:.0f} {top + 72} L{x + w * .18:.0f} {base - 62} L{x + w / 2 - 2:.0f} {base - 62} L{x + w / 2 - 2:.0f} {top + 72}Z" fill="#D9CDBE" />'
    for y in (top + 70, top + 300, base - 320, base - 96):
        s += f'<rect x="{x - w / 2 - 8:.0f}" y="{y}" width="{w + 16}" height="36" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="4" /><path d="M{x - w / 2:.0f} {y + 12} L{x + w / 2:.0f} {y + 12}" stroke="{GOLD_L}" stroke-width="4" />'
    s += f'<path d="M{x - w:.0f} {top + 20} L{x + w:.0f} {top + 20} L{x + w * .62:.0f} {top + 72} L{x - w * .62:.0f} {top + 72}Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" />'
    s += f'<path d="M{x - w * .9:.0f} {base} L{x + w * .9:.0f} {base} L{x + w * .62:.0f} {base - 60} L{x - w * .62:.0f} {base - 60}Z" fill="{GOLD_D}" stroke="{INK}" stroke-width="4" />'
    return s


def sabha():
    random.seed(2)
    defs = B.vgrad('is-sky', ((0, '#3E5FA8'), (0.4, '#86A9DA'), (0.7, '#F3D9C4'), (1, '#FBE9D0'))) + B.vgrad('is-floor', ((0, '#F4E9DA'), (1, '#CDBCD6')))
    far = f'<rect width="{W}" height="{H}" fill="url(#is-sky)" /><circle cx="648" cy="760" r="420" fill="#FFF3D2" opacity="0.35" /><circle cx="648" cy="760" r="280" fill="#FFF3D2" opacity="0.4" />'
    for x, y, s, o in ((80, 330, 1.2, .8), (900, 260, 1.0, .75), (960, 620, 1.3, .7), (20, 760, 1.1, .7), (420, 180, .7, .6)):
        far += B.curl_cloud(x, y, s, '#FFFFFF', '#D3DDEE', o)
    # canopy and pillars
    mid = pillar(150, 420, 1600, 92) + pillar(1146, 420, 1600, 92) + pillar(330, 560, 1500, 64) + pillar(966, 560, 1500, 64)
    mid += f'<path d="M40 440 Q648 220 1256 440 L1256 360 Q648 130 40 360Z" fill="{GOLD}" stroke="{INK}" stroke-width="5" /><path d="M60 420 Q648 204 1236 420" stroke="{GOLD_D}" stroke-width="10" />'
    mid += ''.join(f'<path d="M{x} {y} q22 48 44 0" fill="#C9463A" stroke="{INK}" stroke-width="3" />' for x, y in ((90 + k * 58, 436 - 152 * math.sin(math.pi * (90 + k * 58) / W) * .72) for k in range(20)))
    # the throne of heaven: a lotus-arched back, a wide cushioned seat (seat base at frame 0.60), steps
    sb = fy(0.60)
    mid += (f'<path d="M430 {sb + 10:.0f} L420 {sb - 300:.0f} Q430 {sb - 470:.0f} 540 {sb - 536:.0f} Q648 {sb - 590:.0f} 756 {sb - 536:.0f} Q866 {sb - 470:.0f} 876 {sb - 300:.0f} L866 {sb + 10:.0f}Z" fill="{GOLD}" stroke="{INK}" stroke-width="6" />'
            f'<path d="M474 {sb:.0f} L466 {sb - 290:.0f} Q478 {sb - 420:.0f} 570 {sb - 474:.0f} Q648 {sb - 512:.0f} 726 {sb - 474:.0f} Q818 {sb - 420:.0f} 830 {sb - 290:.0f} L822 {sb:.0f}Z" fill="#8E2E4E" stroke="{INK}" stroke-width="4" />'
            f'<path d="M520 {sb - 10:.0f} Q496 {sb - 400:.0f} 648 {sb - 410:.0f} Q800 {sb - 400:.0f} 776 {sb - 10:.0f}" stroke="#B5506E" stroke-width="8" />'
            + ''.join(f'<circle cx="{x}" cy="{sb + dy:.0f}" r="17" fill="{c}" stroke="{INK}" stroke-width="4" />' for x, dy, c in ((648, -534, '#C9463A'), (500, -450, '#2E8A9E'), (796, -450, '#2E8A9E'), (444, -250, '#C9463A'), (852, -250, '#C9463A')))
            + f'<path d="M618 {sb - 566:.0f} Q612 {sb - 606:.0f} 648 {sb - 616:.0f} Q684 {sb - 606:.0f} 678 {sb - 566:.0f}Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" /><circle cx="648" cy="{sb - 632:.0f}" r="18" fill="{GOLD_L}" stroke="{INK}" stroke-width="4" />'
            + f'<path d="M380 {sb - 20:.0f} Q648 {sb - 54:.0f} 916 {sb - 20:.0f} L930 {sb + 70:.0f} L366 {sb + 70:.0f}Z" fill="#A83A5C" stroke="{INK}" stroke-width="5" /><path d="M384 {sb + 6:.0f} Q648 {sb - 26:.0f} 912 {sb + 6:.0f}" stroke="{GOLD}" stroke-width="9" />'
            f'<path d="M350 {sb + 66:.0f} L946 {sb + 66:.0f} L930 {sb + 180:.0f} L366 {sb + 180:.0f}Z" fill="{GOLD}" stroke="{INK}" stroke-width="5" />'
            + ''.join(f'<path d="M{x} {sb + 160:.0f} q0 -70 34 -70 q34 0 34 70Z" fill="{GOLD_D}" stroke="{INK}" stroke-width="4" />' for x in range(400, 880, 84))
            + ''.join(f'<path d="M{330 - k * 50} {sb + 180 + k * 56:.0f} L{966 + k * 50} {sb + 180 + k * 56:.0f} L{980 + k * 50} {sb + 236 + k * 56:.0f} L{316 - k * 50} {sb + 236 + k * 56:.0f}Z" fill="{c}" stroke="{INK}" stroke-width="4" />' for k, c in enumerate(('#F4E9DA', '#E6D8C6', '#D6C6B4'))))
    g = fy(0.86)
    ground = f'<path d="M0 1590 Q648 1560 {W} 1590 L{W} {H} L0 {H}Z" fill="url(#is-floor)" stroke="{INK}" stroke-width="3" /><path d="M0 1640 Q648 1606 {W} 1640" stroke="{GOLD}" stroke-width="9" /><ellipse cx="648" cy="{g + 14:.0f}" rx="520" ry="44" fill="#FFF6E6" opacity="0.6" />'
    # the throne's lowest steps sit in front of the floor line
    for x, y, s in ((-40, 1990, 1.3), (300, 2050, 1.1), (700, 2060, 1.2), (1010, 1990, 1.4)):
        ground += B.curl_cloud(x, y, s, '#FFFFFF', '#CFC4DC', 0.9)
    B.write('indra-sabha', defs, far, mid, ground, "Indra's hall on the clouds: white and gold pillars, a canopy, the great empty throne (seat base at frame 0.60); feet at 0.86.")
    finish('indra-sabha')


def sky():
    random.seed(12)
    defs = B.vgrad('hs-sky', ((0, '#1B1A3A'), (0.35, '#3A3C82'), (0.65, '#8E6FB0'), (0.85, '#E3A9A8'), (1, '#F6CFA4')))
    far = f'<rect width="{W}" height="{H}" fill="url(#hs-sky)" />'
    for _ in range(90):
        x, y = random.uniform(0, W), random.uniform(0, 1100)
        far += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice((2, 2, 3, 4))}" fill="#FFF6E0" opacity="{random.uniform(.4, .95):.2f}" />'
    far += f'<path d="M-40 620 Q360 380 {W + 40} 300 L{W + 40} 470 Q420 540 -40 830Z" fill="#CFC4F0" opacity="0.14" />'
    mid = ''.join(B.curl_cloud(x, y, s, c, st, o) for x, y, s, c, st, o in (
        (60, 520, 1.1, '#B9A5D6', '#9C86C2', .75), (860, 400, 1.2, '#B9A5D6', '#9C86C2', .7), (900, 900, 1.4, '#DDBBCB', '#C29CB4', .75), (-30, 1080, 1.5, '#DDBBCB', '#C29CB4', .8), (500, 1240, 1.2, '#E8C6C4', '#CDA4A8', .8)))
    ground = ''
    for row, (y, s, c, st) in enumerate(((1440, 1.9, '#F0D2C6', '#D3ACA8'), (1640, 2.2, '#F6DFCF', '#DDBBAE'), (1850, 2.6, '#FBEBDC', '#E6CBBA'))):
        for k in range(5):
            ground += B.curl_cloud(-120 + k * 320 + row * 90, y + random.uniform(-30, 30), s, c, st, 0.96)
    ground += f'<rect x="0" y="1880" width="{W}" height="240" fill="#FBEBDC" />'
    B.write('heaven-sky', defs, far, mid, ground, 'the sky road of heaven: a deep dusk sky with stars and a pale star-road, banks of curl-clouds; no ground.')
    finish('heaven-sky')


def gorge():
    random.seed(7)
    defs = B.vgrad('hg-sky', ((0, '#7F9FC6'), (0.5, '#C9D6E0'), (1, '#EFE3D2')))
    far = f'<rect width="{W}" height="{H}" fill="url(#hg-sky)" /><circle cx="820" cy="520" r="96" fill="#FFF4D8" opacity="0.85" /><circle cx="820" cy="520" r="170" fill="#FFF4D8" opacity="0.25" />'
    for base, n, h0, h1, f, sh in ((1180, 7, 420, 620, '#C4D2E2', '#E6EEF5'), (1260, 6, 300, 460, '#A9BCD2', '#D8E4EE')):
        for k in range(n):
            x = -60 + k * (W + 120) / (n - 1) + random.uniform(-40, 40); h = random.uniform(h0, h1); w = random.uniform(150, 230)
            far += f'<path d="M{x - w:.0f} {base} L{x:.0f} {base - h:.0f} L{x + w:.0f} {base}Z" fill="{f}" /><path d="M{x:.0f} {base - h:.0f} L{x - w * .32:.0f} {base - h * .62:.0f} L{x - w * .1:.0f} {base - h * .68:.0f} L{x + w * .06:.0f} {base - h * .55:.0f} L{x + w * .3:.0f} {base - h * .64:.0f}Z" fill="{sh}" />'
    far += f'<rect x="0" y="1240" width="{W}" height="400" fill="#9AAFC2" />'
    # rock walls on both sides, with deodars
    def wall(pts, f, s): return f'<path d="{pts}" fill="{f}" stroke="{s}" stroke-width="5" />'
    mid = wall(f'M{W} 560 L1180 640 L1150 820 L1060 900 L1080 1090 L1000 1230 L1020 1400 L940 1640 L{W} 1660Z', '#6E6A72', INK)
    mid += f'<path d="M{W} 760 L1200 860 L1190 1080 L1120 1200 L1140 1420 L1070 1640 L{W} 1640Z" fill="#59555E" /><path d="M1150 830 L1130 1000 M1090 1110 L1110 1290 M1180 1230 L1200 1440" stroke="#46434C" stroke-width="7" />'
    mid += wall('M0 480 L120 560 L170 760 L270 860 L260 1040 L360 1160 L380 1340 L470 1640 L0 1660Z', '#767079', INK)
    mid += '<path d="M0 700 L90 800 L110 1000 L200 1120 L210 1320 L300 1640 L0 1640Z" fill="#605B65" /><path d="M150 780 L170 960 M250 1060 L240 1240 M330 1220 L350 1420" stroke="#4C4852" stroke-width="7" />'
    # the cave mouth
    mid += f'<path d="M20 1640 Q10 1330 130 1250 Q260 1220 330 1390 Q372 1520 366 1640Z" fill="#2A2630" stroke="{INK}" stroke-width="6" /><path d="M70 1640 Q70 1400 160 1330 Q250 1320 290 1450 Q316 1550 312 1640Z" fill="#1A171F" />'
    for x, b, s in ((540, 1500, .9), (640, 1470, .7), (860, 1490, .8), (760, 1460, .6)):
        for k in range(4):
            mid += f'<path d="M{x - (110 - k * 22) * s:.0f} {b - k * 70 * s:.0f} L{x:.0f} {b - (150 + k * 70) * s:.0f} L{x + (110 - k * 22) * s:.0f} {b - k * 70 * s:.0f}Z" fill="{("#2F5546", "#3B6653")[k % 2]}" stroke="{INK}" stroke-width="3" />'
        mid += f'<rect x="{x - 10 * s:.0f}" y="{b}" width="{20 * s:.0f}" height="60" fill="#5A3E2C" />'
    g = fy(0.84)
    ground = (f'<path d="M0 1560 Q260 1530 520 1552 Q820 1576 {W} 1540 L{W} {H} L0 {H}Z" fill="#8E8478" stroke="{INK}" stroke-width="4" /><path d="M0 1660 Q420 1626 840 1650 Q1100 1664 {W} 1640 L{W} {H} L0 {H}Z" fill="#7C7368" />'
              f'<ellipse cx="648" cy="{g + 14:.0f}" rx="500" ry="44" fill="#A0968A" opacity="0.6" />')
    for _ in range(12):
        x, y, r = random.uniform(0, W), random.uniform(1700, H - 60), random.uniform(16, 44)
        ground += f'<path d="M{x - r:.0f} {y:.0f} Q{x - r * .8:.0f} {y - r:.0f} {x:.0f} {y - r * 1.05:.0f} Q{x + r:.0f} {y - r * .9:.0f} {x + r:.0f} {y:.0f}Z" fill="#A79D90" stroke="{INK}" stroke-width="3" />'
    for x in (460, 500, 900, 960, 1010):
        ground += f'<path d="M{x} 1640 q-12 -34 -20 -54 M{x} 1640 q2 -40 4 -62 M{x} 1640 q12 -30 24 -46" stroke="#6A7F4A" stroke-width="5" />'
    B.write('himalaya-gorge', defs, far, mid, ground, 'a gorge in the Himalaya: snow peaks, rock walls, deodars, a cave mouth at the left; feet at frame 0.84.')
    finish('himalaya-gorge')


if __name__ == '__main__':
    sabha(); sky(); gorge()
