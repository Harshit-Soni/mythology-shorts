"""S01E08 background, drawn in code in the library's flat style (reuses the S01E02/E06/E07 helpers).

dvaraka   Krishna's city on the sea: white-and-gold nagara spires (no onion domes), walls, the sea, a terrace in front;
          feet 0.86. Used mostly as a wide establishing shot and behind close-ups.
Run from the repo root:  python3 episodes/S01E08-gandhari-curses-krishna/svg/make-backgrounds.py [out_dir]
"""
import importlib.util
import random
import sys

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('b07', 'episodes/S01E07-parikshit-seven-days/svg/make-backgrounds.py')
Q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Q)
sys.argv = _argv
B = Q.B
if len(sys.argv) > 1:
    B.OUT = sys.argv[1]
W, H, INK, fy, GOLD, GOLD_L, GOLD_D = Q.W, Q.H, Q.INK, Q.fy, Q.GOLD, Q.GOLD_L, Q.GOLD_D


def finish(bid):
    p = f'{B.OUT}/{bid}.svg'
    s = open(p).read().replace(f'S01E02 | {bid}', f'S01E08 | {bid}').replace('episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py', 'episodes/S01E08-gandhari-curses-krishna/svg/make-backgrounds.py')
    open(p, 'w').write(s)


def spire(x, base, h, w, body='#F4EAD6', shade='#D8C6A6', top=GOLD):
    """A nagara temple tower: a curved shikhara with ribbed courses, an amalaka and a gold finial."""
    return (f'<path d="M{x - w} {base} L{x - w} {base - h * .28:.0f} Q{x - w * .92:.0f} {base - h * .8:.0f} {x} {base - h} Q{x + w * .92:.0f} {base - h * .8:.0f} {x + w} {base - h * .28:.0f} L{x + w} {base}Z" fill="{body}" stroke="{INK}" stroke-width="5" />'
            f'<path d="M{x + w * .15:.0f} {base - h + 6} Q{x + w * .8:.0f} {base - h * .78:.0f} {x + w - 4} {base - h * .28:.0f} L{x + w - 4} {base} L{x + w * .3:.0f} {base}Z" fill="{shade}" />'
            + ''.join(f'<path d="M{x - w * (1 - k * .06):.0f} {base - h * (.32 + k * .1):.0f} Q{x} {base - h * (.34 + k * .1):.0f} {x + w * (1 - k * .06):.0f} {base - h * (.32 + k * .1):.0f}" stroke="{shade}" stroke-width="5" />' for k in range(6))
            + f'<ellipse cx="{x}" cy="{base - h - 8:.0f}" rx="{w * .32:.0f}" ry="{w * .12:.0f}" fill="{GOLD_L}" stroke="{INK}" stroke-width="4" />'
            f'<path d="M{x - 6} {base - h - 14:.0f} L{x} {base - h - 44:.0f} L{x + 6} {base - h - 14:.0f}Z" fill="{top}" stroke="{INK}" stroke-width="3" />'
            f'<path d="M{x} {base - h - 40:.0f} L{x} {base - h - 70:.0f} L{x + 26} {base - h - 62:.0f} L{x} {base - h - 54:.0f}" fill="#C9463A" stroke="{INK}" stroke-width="3" />')


def dvaraka():
    random.seed(11)
    defs = B.vgrad('dv-sky', ((0, '#5C78B4'), (0.45, '#9CB8D8'), (0.75, '#F2D6B0'), (1, '#F8E6C4'))) + B.vgrad('dv-sea', ((0, '#5E9AB4'), (1, '#2E6A8A')))
    far = f'<rect width="{W}" height="{H}" fill="url(#dv-sky)" />'
    for x, y, s in ((120, 360, 1.2), (880, 280, 1.0), (1040, 620, 1.1), (300, 700, .9)):
        far += B.curl_cloud(x, y, s, '#FFFFFF', '#C9D6E8', .85)
    sea = 1400
    far += f'<rect x="0" y="{sea}" width="{W}" height="{H - sea}" fill="url(#dv-sea)" />'
    far += ''.join(f'<path d="M{x} {y} q30 -14 60 0" stroke="#BFE0EC" stroke-width="5" />' for x, y in ((random.uniform(0, W - 60), random.uniform(sea + 40, H - 300)) for _ in range(26)))
    # the city: walls along the shore, towers rising behind (white and gold, as the epic's golden city)
    mid = ''
    for x, h, w in ((180, 380, 80), (420, 520, 100), (648, 700, 130), (880, 540, 104), (1110, 400, 84), (300, 300, 64), (1000, 320, 66)):
        mid += spire(x, 1300, h, w)
    mid += (f'<path d="M0 1300 L{W} 1300 L{W} 1430 L0 1430Z" fill="#EADBBE" stroke="{INK}" stroke-width="6" />'
            + ''.join(f'<rect x="{x}" y="1268" width="44" height="36" fill="#EADBBE" stroke="{INK}" stroke-width="5" />' for x in range(10, W, 88))
            + ''.join(f'<path d="M{x} 1430 V1350 Q{x} 1322 {x + 26} 1318 Q{x + 52} 1322 {x + 52} 1350 V1430Z" fill="#7A5A44" stroke="{INK}" stroke-width="4" />' for x in range(70, W, 220))
            + f'<path d="M0 1400 L{W} 1400" stroke="{GOLD}" stroke-width="10" />')
    # a terrace in front, where a figure can stand (feet ~0.86)
    g = fy(0.83)
    ground = (f'<path d="M0 {g:.0f} L{W} {g:.0f} L{W} {H} L0 {H}Z" fill="#D9C4A0" stroke="{INK}" stroke-width="6" />'
              f'<path d="M0 {g + 20:.0f} L{W} {g + 20:.0f}" stroke="{GOLD}" stroke-width="10" />'
              + ''.join(f'<path d="M{x} {g + 60:.0f} L{x + 120} {H}" stroke="#BFA780" stroke-width="5" />' for x in range(-200, W, 190))
              + ''.join(f'<rect x="{x}" y="{g - 150:.0f}" width="34" height="150" fill="#F2E6CE" stroke="{INK}" stroke-width="5" /><rect x="{x - 8}" y="{g - 168:.0f}" width="50" height="22" fill="{GOLD}" stroke="{INK}" stroke-width="4" />' for x in (30, 1232))
              + f'<path d="M30 {g - 110:.0f} L1266 {g - 110:.0f}" stroke="#F2E6CE" stroke-width="10" /><path d="M30 {g - 110:.0f} L1266 {g - 110:.0f}" stroke="{INK}" stroke-width="2" transform="translate(0 6)" />'
              + ''.join(f'<path d="M{x} {g - 104:.0f} L{x} {g:.0f}" stroke="#F2E6CE" stroke-width="12" />' for x in range(110, 1232, 80)))
    B.write('dvaraka', defs, far, ground, mid, "Dvaraka, Krishna's city on the sea: white-and-gold nagara spires above the shore walls, the sea, a balustraded terrace in front; feet at frame 0.86.")
    finish('dvaraka')


if __name__ == '__main__':
    dvaraka()
