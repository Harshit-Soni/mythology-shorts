"""S01E07 backgrounds, drawn in code in the library's flat style (reuses the S01E02/E06 helpers).

pillar-tower   a small palace on one tall pillar over the plain, the city far off; ground 0.84
tower-room     the room inside: two pillars, a wide round-arched window with a low sun; floor, feet 0.86
banyan-road    a road through open country, bare in the middle (a banyan is a prop); feet 0.84
Run from the repo root:  python3 episodes/S01E07-parikshit-seven-days/svg/make-backgrounds.py [out_dir]
"""
import importlib.util
import random
import sys

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('b06', 'episodes/S01E06-nahusha-becomes-a-snake/svg/make-backgrounds.py')
Q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Q)
sys.argv = _argv
B = Q.B
if len(sys.argv) > 1:
    B.OUT = sys.argv[1]
W, H, INK, fy, GOLD, GOLD_L, GOLD_D = Q.W, Q.H, Q.INK, Q.fy, Q.GOLD, Q.GOLD_L, Q.GOLD_D


def finish(bid):
    p = f'{B.OUT}/{bid}.svg'
    s = open(p).read().replace(f'S01E02 | {bid}', f'S01E07 | {bid}').replace('episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py', 'episodes/S01E07-parikshit-seven-days/svg/make-backgrounds.py')
    open(p, 'w').write(s)


def tower():
    random.seed(4)
    defs = B.vgrad('pt-sky', ((0, '#5C6FA8'), (0.35, '#B79AB8'), (0.6, '#F0B98C'), (0.8, '#F8DDB0')))
    far = f'<rect width="{W}" height="{H}" fill="url(#pt-sky)" /><circle cx="930" cy="1250" r="120" fill="#FFE2A0" /><circle cx="930" cy="1250" r="210" fill="#FFE2A0" opacity="0.3" />'
    for x, y, s in ((60, 420, 1.1), (900, 330, 1.0), (980, 760, 1.2), (30, 900, 1.2)):
        far += B.curl_cloud(x, y, s, '#F6D9C4', '#D9AFA4', .75)
    far += f'<path d="M0 1400 Q300 1330 620 1390 Q960 1450 {W} 1370 L{W} 1640 L0 1640Z" fill="#A98A78" /><path d="M0 1480 Q420 1420 800 1470 Q1080 1500 {W} 1450 L{W} 1660 L0 1660Z" fill="#8E7262" />'
    for x, h in ((70, 120), (150, 170), (230, 110), (1060, 130), (1140, 190), (1230, 120)):   # the city, far off
        far += f'<path d="M{x - 46} 1480 L{x - 44} {1480 - h * .5:.0f} Q{x - 34} {1480 - h} {x - 10} {1480 - h - 60} L{x + 10} {1480 - h - 60} Q{x + 34} {1480 - h} {x + 44} {1480 - h * .5:.0f} L{x + 46} 1480Z" fill="#8A6A60" /><rect x="{x - 14}" y="{1480 - h - 72}" width="28" height="14" rx="6" fill="#C79A5A" />'
    c, g, top = 648, fy(0.83), 1010
    mid = ''
    # the pillar
    mid += (f'<path d="M{c - 74} {top} L{c - 92} {g} L{c + 92} {g} L{c + 74} {top}Z" fill="#E6D3B4" stroke="{INK}" stroke-width="6" /><path d="M{c + 20} {top} L{c + 30} {g} L{c + 88} {g} L{c + 70} {top}Z" fill="#C4AB88" />'
            + ''.join(f'<rect x="{c - 92}" y="{y}" width="184" height="34" rx="9" fill="{GOLD}" stroke="{INK}" stroke-width="5" /><path d="M{c - 80} {y + 11} L{c + 80} {y + 11}" stroke="{GOLD_L}" stroke-width="5" />' for y in (1120, 1310, 1500))
            + f'<path d="M{c - 170} {g + 30:.0f} L{c + 170} {g + 30:.0f} L{c + 120} {g - 60:.0f} L{c - 120} {g - 60:.0f}Z" fill="#D2BB96" stroke="{INK}" stroke-width="6" /><path d="M{c - 210} {g + 74:.0f} L{c + 210} {g + 74:.0f} L{c + 170} {g + 30:.0f} L{c - 170} {g + 30:.0f}Z" fill="#B89E78" stroke="{INK}" stroke-width="6" />'
            + f'<path d="M{c - 300} {top - 70} Q{c - 160} {top + 40} {c - 76} {top + 60} L{c + 76} {top + 60} Q{c + 160} {top + 40} {c + 300} {top - 70}Z" fill="#C9A878" stroke="{INK}" stroke-width="6" />'
            + ''.join(f'<path d="M{c + k * 46} {top - 60} q-6 70 {-k * 14} 104" stroke="#9A7C54" stroke-width="6" />' for k in range(-5, 6)))
    # the house on it
    b = top - 70
    mid += (f'<rect x="{c - 320}" y="{b - 44}" width="640" height="48" rx="8" fill="{GOLD_D}" stroke="{INK}" stroke-width="6" />'
            f'<rect x="{c - 270}" y="{b - 300}" width="540" height="258" fill="#F2E2C4" stroke="{INK}" stroke-width="6" /><rect x="{c + 120}" y="{b - 300}" width="148" height="256" fill="#D8C29C" />'
            + ''.join(f'<path d="M{x - 46} {b - 46} L{x - 46} {b - 170} Q{x - 46} {b - 224} {x} {b - 228} Q{x + 46} {b - 224} {x + 46} {b - 170} L{x + 46} {b - 46}Z" fill="#6A3A2E" stroke="{INK}" stroke-width="5" /><path d="M{x - 30} {b - 50} L{x - 30} {b - 166} Q{x - 30} {b - 206} {x} {b - 208} Q{x + 30} {b - 206} {x + 30} {b - 166} L{x + 30} {b - 50}Z" fill="#F0A850" opacity="0.85" />' for x in (c - 170, c, c + 170))
            + f'<path d="M{c - 330} {b - 296} Q{c} {b - 360} {c + 330} {b - 296} L{c + 300} {b - 250} Q{c} {b - 306} {c - 300} {b - 250}Z" fill="#B4524A" stroke="{INK}" stroke-width="6" />'
            + f'<path d="M{c - 170} {b - 316} L{c - 160} {b - 380} Q{c - 130} {b - 500} {c - 46} {b - 560} L{c + 46} {b - 560} Q{c + 130} {b - 500} {c + 160} {b - 380} L{c + 170} {b - 316} Q{c} {b - 352} {c - 170} {b - 316}Z" fill="{GOLD}" stroke="{INK}" stroke-width="6" />'
            + ''.join(f'<path d="M{c - 166 + k * 22:.0f} {b - 356 - k * 48:.0f} Q{c} {b - 384 - k * 46:.0f} {c + 166 - k * 22:.0f} {b - 356 - k * 48:.0f}" stroke="{GOLD_D}" stroke-width="8" />' for k in range(5))
            + f'<path d="M{c - 52} {b - 330} Q{c - 40} {b - 480} {c - 16} {b - 558} M{c + 52} {b - 330} Q{c + 40} {b - 480} {c + 16} {b - 558}" stroke="{GOLD_D}" stroke-width="7" />'
            + f'<rect x="{c - 62}" y="{b - 592}" width="124" height="36" rx="17" fill="{GOLD_L}" stroke="{INK}" stroke-width="5" /><path d="M{c - 20} {b - 590} Q{c - 26} {b - 628} {c} {b - 640} Q{c + 26} {b - 628} {c + 20} {b - 590}Z" fill="{GOLD_L}" stroke="{INK}" stroke-width="5" />'
            + f'<path d="M{c + 4} {b - 638} L{c + 4} {b - 740}" stroke="{INK}" stroke-width="8" /><path d="M{c + 6} {b - 738} Q{c + 80} {b - 722} {c + 130} {b - 686} Q{c + 70} {b - 682} {c + 6} {b - 676}Z" fill="#B4524A" stroke="{INK}" stroke-width="5" />')
    gy = fy(0.84)
    ground = f'<path d="M0 1620 Q420 1580 860 1606 Q1120 1620 {W} 1590 L{W} {H} L0 {H}Z" fill="#B89466" stroke="{INK}" stroke-width="4" /><path d="M0 1800 Q520 1760 {W} 1800 L{W} {H} L0 {H}Z" fill="#A07E54" /><ellipse cx="648" cy="{gy + 24:.0f}" rx="520" ry="50" fill="#CFAE7E" opacity="0.5" />'
    for _ in range(9):
        x, y, r = random.uniform(0, W), random.uniform(1780, H - 60), random.uniform(14, 34)
        ground += f'<path d="M{x - r:.0f} {y:.0f} Q{x - r * .8:.0f} {y - r:.0f} {x:.0f} {y - r:.0f} Q{x + r:.0f} {y - r * .9:.0f} {x + r:.0f} {y:.0f}Z" fill="#8E6E48" stroke="{INK}" stroke-width="3" />'
    B.write('pillar-tower', defs, far, ground, mid, 'a small palace on one tall pillar over the plain, the city far off, a low sun; ground at frame 0.84.')
    finish('pillar-tower')


def room():
    defs = B.vgrad('tr-wall', ((0, '#7A3E38'), (1, '#A8685A'))) + B.vgrad('tr-sky', ((0, '#6A5C9A'), (0.5, '#E89A6A'), (1, '#FCE0A0'))) + B.vgrad('tr-floor', ((0, '#C99A6A'), (1, '#8E6040')))
    far = f'<rect width="{W}" height="{H}" fill="url(#tr-wall)" />'
    win = 'M330 1240 L330 660 C330 470 470 348 648 348 C826 348 966 470 966 660 L966 1240Z'
    far += f'<defs><clipPath id="tr-win"><path d="{win}" /></clipPath></defs><g clip-path="url(#tr-win)"><rect x="300" y="300" width="700" height="980" fill="url(#tr-sky)" /><circle cx="700" cy="1080" r="120" fill="#FFE9B0" /><circle cx="700" cy="1080" r="210" fill="#FFE9B0" opacity="0.35" />'
    far += B.curl_cloud(350, 700, .9, '#F2B890', '#D08C70', .7) + B.curl_cloud(760, 560, .8, '#E8A890', '#C47E70', .6)
    far += '<path d="M300 1180 Q520 1120 740 1170 Q900 1200 1000 1150 L1000 1300 L300 1300Z" fill="#7E5348" /></g>'
    far += f'<path d="{win}" stroke="{INK}" stroke-width="30" /><path d="{win}" stroke="{GOLD}" stroke-width="18" />'
    mid = f'<rect x="270" y="1226" width="756" height="54" rx="10" fill="{GOLD_D}" stroke="{INK}" stroke-width="5" /><path d="M280 1242 L1016 1242" stroke="{GOLD_L}" stroke-width="7" />'
    mid += Q.pillar(160, 250, 1640, 110) + Q.pillar(1136, 250, 1640, 110)
    mid += f'<path d="M0 190 L{W} 190 L{W} 300 L0 300Z" fill="{GOLD_D}" stroke="{INK}" stroke-width="5" /><path d="M0 216 L{W} 216" stroke="{GOLD_L}" stroke-width="8" />' + ''.join(f'<path d="M{x} 298 q26 54 52 0" fill="#C9463A" stroke="{INK}" stroke-width="3" />' for x in range(-10, W, 56))
    for x in (300, 996):   # hanging lamps
        mid += f'<path d="M{x} 300 L{x} 440" stroke="{INK}" stroke-width="6" /><path d="M{x - 38} 440 Q{x} 508 {x + 38} 440Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" /><path d="M{x} 440 q-20 -34 0 -62 q20 28 0 62Z" fill="#FFB347" stroke="{INK}" stroke-width="3" />'
    g = fy(0.86)
    ground = f'<path d="M0 1600 L{W} 1600 L{W} {H} L0 {H}Z" fill="url(#tr-floor)" stroke="{INK}" stroke-width="4" /><path d="M0 1640 L{W} 1640" stroke="{GOLD}" stroke-width="8" /><path d="M200 {H} L360 1680 L936 1680 L1096 {H}Z" fill="#8E2E3E" stroke="{INK}" stroke-width="4" /><path d="M250 {H} L396 1706 L900 1706 L1046 {H}" stroke="{GOLD}" stroke-width="9" /><ellipse cx="648" cy="{g + 14:.0f}" rx="380" ry="36" fill="#FFD9A0" opacity="0.25" />'
    B.write('tower-room', defs, far, mid, ground, 'the room on the pillar: two pillars, hanging lamps, a wide round-arched window with a low sun; feet at frame 0.86.')
    finish('tower-room')


def road():
    random.seed(9)
    defs = B.vgrad('br-sky', ((0, '#7FB0D2'), (0.5, '#CFE0DC'), (1, '#F6E6C4')))
    far = f'<rect width="{W}" height="{H}" fill="url(#br-sky)" />'
    for x, y, s in ((90, 360, 1.2), (820, 300, 1.1), (520, 620, .9), (1000, 760, 1.1)):
        far += B.curl_cloud(x, y, s, '#FFFFFF', '#C9D6DC', .8)
    far += f'<path d="M0 1260 Q260 1150 560 1240 Q860 1330 {W} 1200 L{W} 1640 L0 1640Z" fill="#9DB48E" /><path d="M0 1380 Q360 1310 700 1370 Q1000 1420 {W} 1350 L{W} 1640 L0 1640Z" fill="#86A074" />'
    for x, y, r in ((70, 1370, 60), (150, 1390, 46), (1130, 1380, 64), (1220, 1370, 50), (1040, 1400, 40)):
        far += f'<circle cx="{x}" cy="{y - r}" r="{r}" fill="#5E7E54" stroke="{INK}" stroke-width="3" /><rect x="{x - 7}" y="{y - 8}" width="14" height="46" fill="#5A3E2C" />'
    ground = f'<path d="M0 1540 Q420 1500 860 1526 Q1100 1540 {W} 1510 L{W} {H} L0 {H}Z" fill="#A9B06A" stroke="{INK}" stroke-width="4" /><path d="M0 1700 Q500 1640 {W} 1690 L{W} 1860 Q520 1820 0 1890Z" fill="#D9BE8E" stroke="{INK}" stroke-width="3" /><path d="M40 1780 Q520 1726 {W - 40} 1768" stroke="#BFA070" stroke-width="8" stroke-dasharray="90 60" /><path d="M0 1890 Q520 1820 {W} 1860 L{W} {H} L0 {H}Z" fill="#98A05C" />'
    for _ in range(14):
        x, y = random.uniform(0, W), random.choice((random.uniform(1570, 1650), random.uniform(1920, 2060)))
        ground += f'<path d="M{x:.0f} {y:.0f} q-12 -34 -20 -50 M{x:.0f} {y:.0f} q2 -38 4 -58 M{x:.0f} {y:.0f} q12 -30 24 -44" stroke="#6F7E3E" stroke-width="5" />'
    B.write('banyan-road', defs, far, '', ground, 'a road through open country, bare in the middle for a tree; feet at frame 0.84.')
    finish('banyan-road')


if __name__ == '__main__':
    tower(); room(); road()
