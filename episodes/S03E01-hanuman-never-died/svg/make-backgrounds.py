"""S03E01 background, drawn in code in the library's flat style (reuses the S01E02/E07/E08 helpers).

sunrise-peak   a mountain top at dawn: a flat rocky summit on the left that ends in a cliff, ranges of peaks below in
               mist, and a huge red sun rising on the right like a ripe fruit (CE 4.65.19). Feet 0.84.
Run from the repo root:  python3 episodes/S03E01-hanuman-never-died/svg/make-backgrounds.py [out_dir]
"""
import importlib.util
import random
import sys

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('b08', 'episodes/S01E08-gandhari-curses-krishna/svg/make-backgrounds.py')
Q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Q)
sys.argv = _argv
B = Q.B
if len(sys.argv) > 1:
    B.OUT = sys.argv[1]
W, H, INK, fy, GOLD = Q.W, Q.H, Q.INK, Q.fy, Q.GOLD


def finish(bid):
    p = f'{B.OUT}/{bid}.svg'
    s = open(p).read().replace(f'S01E02 | {bid}', f'S03E01 | {bid}').replace('episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py', 'episodes/S03E01-hanuman-never-died/svg/make-backgrounds.py')
    open(p, 'w').write(s)


def ridge(base, amp, n, seed, fill, stroke=True):
    random.seed(seed)
    xs = [k * W / n for k in range(n + 1)]
    pts = ' '.join(f'L{x:.0f} {base - random.uniform(.3, 1) * amp:.0f}' for x in xs)
    st = f' stroke="{INK}" stroke-width="4"' if stroke else ''
    return f'<path d="M0 {H} L0 {base} {pts} L{W} {H}Z" fill="{fill}"{st} />'


def sunrise_peak():
    defs = (B.vgrad('sp-sky', ((0, '#2E3A6E'), (0.3, '#6E5A8E'), (0.55, '#E07A6A'), (0.72, '#F6B26A'), (1, '#FCE2B0')))
            + '<radialGradient id="sp-sun" cx="0.42" cy="0.38" r="0.7"><stop offset="0" stop-color="#FF8A4A" /><stop offset="0.7" stop-color="#E8462E" /><stop offset="1" stop-color="#C2321E" /></radialGradient>')
    far = f'<rect width="{W}" height="{H}" fill="url(#sp-sky)" />'
    sx, sy, sr = 880, fy(0.55), 240
    far += ''.join(f'<circle cx="{sx}" cy="{sy:.0f}" r="{sr + d}" fill="#FFB070" opacity="{o}" />' for d, o in ((220, .10), (130, .16), (60, .22)))
    far += (f'<circle cx="{sx}" cy="{sy:.0f}" r="{sr}" fill="url(#sp-sun)" stroke="{INK}" stroke-width="5" />'
            f'<ellipse cx="{sx - 80}" cy="{sy - 90:.0f}" rx="60" ry="34" fill="#FFC890" opacity="0.6" transform="rotate(-30 {sx - 80} {sy - 90:.0f})" />')
    for x, y, s in ((140, 420, 1.1), (420, 300, 0.8), (1100, 360, 0.9)):
        far += B.curl_cloud(x, y, s, '#F6C6B0', '#C98A8A', .7)
    # ranges of peaks in the valley, far to near, half lost in mist
    mid = (ridge(fy(0.66), 220, 9, 3, '#7A6A96', stroke=False) + f'<rect x="0" y="{fy(0.66):.0f}" width="{W}" height="300" fill="#F4C8A8" opacity="0.35" />'
           + ridge(fy(0.72), 200, 7, 5, '#5E5480') + f'<rect x="0" y="{fy(0.72):.0f}" width="{W}" height="300" fill="#F4C8A8" opacity="0.30" />'
           + ridge(fy(0.80), 160, 6, 9, '#46406A'))
    # the summit: a flat rock shelf from the left, ending in a cliff at x ~ 900; feet at 0.84
    g = fy(0.80)
    ground = (f'<path d="M0 {g + 10:.0f} Q260 {g - 30:.0f} 560 {g - 8:.0f} Q760 {g + 6:.0f} 900 {g + 40:.0f} L960 {g + 180:.0f} L930 {g + 420:.0f} L1010 {H} L0 {H}Z" fill="#8E6A56" stroke="{INK}" stroke-width="6" />'
              f'<path d="M0 {g + 40:.0f} Q300 {g + 4:.0f} 600 {g + 24:.0f} Q780 {g + 36:.0f} 900 {g + 70:.0f}" stroke="#B48A6E" stroke-width="10" />'
              f'<path d="M900 {g + 40:.0f} L960 {g + 180:.0f} L930 {g + 420:.0f} L1010 {H} L860 {H} L880 {g + 300:.0f}Z" fill="#6E4E3E" />'
              + ''.join(f'<path d="M{x} {y:.0f} l{dx} {dy}" stroke="#6E4E3E" stroke-width="6" />' for x, y, dx, dy in ((120, g + 160, 60, 40), (380, g + 220, -40, 60), (640, g + 140, 50, 50), (240, g + 330, 70, 20), (520, g + 360, -30, 50)))
              # a few hardy shrubs at the back of the shelf
              + ''.join(f'<circle cx="{x}" cy="{g - 6:.0f}" r="{r}" fill="#4E6A3A" stroke="{INK}" stroke-width="4" />' for x, r in ((40, 34), (90, 24), (720, 22))))
    B.write('sunrise-peak', defs, far, mid, ground, 'A mountain top at dawn: a rock shelf on the left ending in a cliff, peaks in mist below, a huge red sun rising like a ripe fruit on the right; feet at frame 0.84.')
    finish('sunrise-peak')


if __name__ == '__main__':
    sunrise_peak()
