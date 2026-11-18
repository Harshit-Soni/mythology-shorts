"""S01E04 background, drawn in code in the library's flat style (see S01E02 make-backgrounds.py).

yamuna-bank   the bank of the Yamuna: a wide river across the middle of the frame, far hills, kadamba trees and reeds;
              the near bank is where figures stand (feet at frame ≈ 0.84). Used for Amba's tapas, Ganga's curse,
              the pyre and the Vasus.
1296×2112 canvas (frame 1080×1920 + margins); layers layer-far / layer-mid / layer-ground.
Run from the repo root:  python3 episodes/S01E04-amba-vow-bhishma/svg/make-backgrounds.py [out_dir]
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


def yamuna():
    random.seed(21)
    defs = (B.vgrad('yb-sky', ((0, '#2E3A6B'), (0.45, '#C98BA0'), (0.75, '#F4C7A6'), (1, '#F8DDB8')))
            + B.vgrad('yb-water', ((0, '#6E8FB8'), (0.5, '#4E6F9E'), (1, '#36507E'))))
    far = f'<rect width="{W}" height="{H}" fill="url(#yb-sky)" />'
    far += '<circle cx="880" cy="980" r="110" fill="#FFF1D6" opacity="0.75" /><circle cx="880" cy="980" r="190" fill="#FFE9C4" opacity="0.2" />'
    # far hills
    far += f'<path d="M0 1150 Q220 1020 460 1100 Q700 1180 900 1080 Q1100 990 {W} 1080 L{W} 1260 L0 1260Z" fill="#8E7A9E" opacity="0.8" />'
    far += f'<path d="M0 1210 Q300 1130 640 1190 Q960 1240 {W} 1170 L{W} 1300 L0 1300Z" fill="#6E5F86" opacity="0.85" />'
    # the river: a wide band, with the far bank's tree line
    mid = (f'<path d="M0 1290 Q648 1250 {W} 1290 L{W} 1640 Q648 1600 0 1640Z" fill="url(#yb-water)" />'
           f'<path d="M0 1290 Q648 1250 {W} 1290" stroke="#2A3A5E" stroke-width="3" />')
    for _ in range(26):
        x, y = random.uniform(40, W - 60), random.uniform(1320, 1600)
        w = random.uniform(40, 120)
        mid += f'<path d="M{x:.0f} {y:.0f} q{w / 2:.0f} -8 {w:.0f} 0" stroke="#A9C3E0" stroke-width="4" opacity="0.7" />'
    mid += '<path d="M780 1300 L980 1300 L1040 1600 L720 1600Z" fill="#FFE9C4" opacity="0.12" />'  # the moon's path on the water
    def kadamba(x, base, s):
        trunk = f'<path d="M{x - 14 * s:.0f} {base} Q{x - 6 * s:.0f} {base - 220 * s:.0f} {x:.0f} {base - 320 * s:.0f} Q{x + 8 * s:.0f} {base - 220 * s:.0f} {x + 16 * s:.0f} {base}Z" fill="#4E3424" stroke="{INK}" stroke-width="3" />'
        crown = ''.join(f'<ellipse cx="{x + dx * s:.0f}" cy="{base - (330 + dy) * s:.0f}" rx="{rx * s:.0f}" ry="{rx * 0.7 * s:.0f}" fill="{c}" stroke="{INK}" stroke-width="3" />'
                        for dx, dy, rx, c in ((-90, 10, 100, '#2F5546'), (80, 0, 110, '#3B6653'), (0, 80, 120, '#3B6653'), (-20, -40, 90, '#4A7A5E')))
        balls = ''.join(f'<circle cx="{x + random.uniform(-150, 150) * s:.0f}" cy="{base - random.uniform(300, 440) * s:.0f}" r="{7 * s:.0f}" fill="#F4D17B" stroke="{INK}" stroke-width="1.5" />' for _ in range(14))
        return trunk + crown + balls
    mid += kadamba(150, 1300, 0.9) + kadamba(1120, 1290, 1.0) + kadamba(980, 1300, 0.6)
    # the near bank: sand and grass; feet at frame 0.84
    g = fy(0.84)
    ground = (f'<path d="M0 1620 Q400 1580 760 1610 Q1050 1630 {W} 1600 L{W} {H} L0 {H}Z" fill="#C9B08A" stroke="{INK}" stroke-width="3" />'
              f'<path d="M0 1700 Q500 1670 900 1700 Q1100 1715 {W} 1690 L{W} {H} L0 {H}Z" fill="#B89C74" />'
              f'<ellipse cx="648" cy="{g + 16:.0f}" rx="460" ry="40" fill="#D6BF98" opacity="0.6" />')
    for x0 in list(range(20, 260, 26)) + list(range(1040, 1290, 26)):
        h = random.uniform(80, 170)
        ground += f'<path d="M{x0} 1660 q{random.uniform(-14, 14):.0f} -{h / 2:.0f} {random.uniform(-10, 10):.0f} -{h:.0f}" stroke="#5C7A3E" stroke-width="6" />'
        ground += f'<ellipse cx="{x0 + random.uniform(-6, 6):.0f}" cy="{1660 - h:.0f}" rx="6" ry="18" fill="#8E6A3E" />'
    for _ in range(30):
        x, y = random.uniform(0, W), random.uniform(1700, H - 40)
        ground += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(6, 16):.0f}" ry="5" fill="#9C8466" />'
    B.write('yamuna-bank', defs, far, mid, ground,
            'the bank of the Yamuna at dusk: far hills, a wide river with the moon on the water, kadamba trees, reeds; near bank (feet at frame 0.84).')
    p = f'{B.OUT}/yamuna-bank.svg'
    s = open(p).read().replace('S01E02 | yamuna-bank', 'S01E04 | yamuna-bank').replace(
        'episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py', 'episodes/S01E04-amba-vow-bhishma/svg/make-backgrounds.py')
    open(p, 'w').write(s)


if __name__ == '__main__':
    yamuna()
