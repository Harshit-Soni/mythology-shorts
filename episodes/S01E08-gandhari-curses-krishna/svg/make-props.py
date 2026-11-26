"""S01E08 props, drawn in code in the library's flat style. People are library poses drawn as silhouettes (N.rig with one
flat fill), so every crowd matches the cast. No bodies and no blood: the field is wheels and banners, the clan's end is
silhouettes and grass turning to iron (CE 16.4.34-39).
Run from the repo root (after make-cast.py):  python3 episodes/S01E08-gandhari-curses-krishna/svg/make-props.py
"""
import importlib.util
import random
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
def load(n, p):
    spec = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
N = load('p06', 'episodes/S01E06-nahusha-becomes-a-snake/svg/make-props.py')
sys.argv = _argv
SVG, INK, GOLD, GOLD_L, GOLD_D, SIL = N.SVG, N.INK, N.GOLD, N.GOLD_L, N.GOLD_D, N.SIL
OUT = 'assets/props'
rig = N.rig
EP = 'S01E08-gandhari-curses-krishna'


def write(pid, body, desc, w=800, h=800):
    svg = (f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
           f'<desc>S01E08 | {pid} | {desc} Made by episodes/{EP}/svg/make-props.py.</desc>{body}</svg>')
    ET.fromstring(svg)
    open(f'{OUT}/{pid}.svg', 'w').write(svg)
    print('wrote', f'{OUT}/{pid}.svg')


def glow(cx, cy, r, c, n=4, o=.08): return ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r * (n - k) / n:.0f}" fill="{c}" opacity="{o}" />' for k in range(n))


def fig(path, x, base, s, fill, flip=False, rim=None):
    """A library pose as a silhouette, feet (rig base 1550) at (x, base), s = scale of the 1000x1600 canvas."""
    sx = -s if flip else s
    t = f'translate({x - 500 * sx:.1f} {base - 1550 * s:.1f}) scale({sx:.3f} {s:.3f})'
    out = ''
    if rim:
        out += f'<g transform="translate(-4 -3)">{rig(path, t, fill=rim)}</g>'
    return out + rig(path, t, fill=fill)


def wheel(cx, cy, r, rot=0, broken=False, c='#6E4A2E', cl='#9A6E44'):
    spokes = ''.join(f'<path d="M0 0 L0 {-r * .82:.0f}" stroke="{c}" stroke-width="{r * .1:.0f}" transform="rotate({a})" />' for a in range(0, 360, 45) if not (broken and a in (90, 135)))
    rim = f'<circle r="{r * .88:.0f}" stroke="{INK}" stroke-width="{r * .2 + 6:.0f}" /><circle r="{r * .88:.0f}" stroke="{c}" stroke-width="{r * .2:.0f}" /><circle r="{r * .88:.0f}" stroke="{cl}" stroke-width="{r * .05:.0f}" />'
    if broken:
        rim = (f'<path d="M{-r * .88:.0f} 0 A{r * .88:.0f} {r * .88:.0f} 0 1 1 {r * .62:.0f} {r * .62:.0f}" stroke="{INK}" stroke-width="{r * .2 + 6:.0f}" />'
               f'<path d="M{-r * .88:.0f} 0 A{r * .88:.0f} {r * .88:.0f} 0 1 1 {r * .62:.0f} {r * .62:.0f}" stroke="{c}" stroke-width="{r * .2:.0f}" />')
    hub = f'<circle r="{r * .2:.0f}" fill="{GOLD_D}" stroke="{INK}" stroke-width="5" /><circle r="{r * .08:.0f}" fill="{INK}" />'
    return f'<g transform="translate({cx} {cy}) rotate({rot})">{spokes}{rim}{hub}</g>'


def banner(x, base, h, lean, flag, flag_d, torn=False, side=1):
    tx, ty = x + lean, base - h
    pole = f'<path d="M{x} {base} L{tx} {ty}" stroke="{INK}" stroke-width="14" /><path d="M{x} {base} L{tx} {ty}" stroke="#7A5634" stroke-width="8" />'
    w = 120 * side
    tear = f' L{tx + w * .7:.0f} {ty + 54} L{tx + w * .9:.0f} {ty + 70} L{tx + w * .6:.0f} {ty + 84}' if torn else f' Q{tx + w * 1.2:.0f} {ty + 30} {tx + w:.0f} {ty + 66}'
    fl = f'<path d="M{tx} {ty + 4} Q{tx + w * .5:.0f} {ty - 14} {tx + w:.0f} {ty + 8}{tear} Q{tx + w * .4:.0f} {ty + 92} {tx} {ty + 84}Z" fill="{flag}" stroke="{INK}" stroke-width="5" /><path d="M{tx + w * .1:.0f} {ty + 40} Q{tx + w * .5:.0f} {ty + 30} {tx + w * .8:.0f} {ty + 44}" stroke="{flag_d}" stroke-width="6" />'
    return pole + fl + f'<circle cx="{tx}" cy="{ty}" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'


# ---------- two armies ----------
KAURAVA, KAURAVA_L, PANDAVA, PANDAVA_L = '#4A1622', '#8E2A3A', '#16284E', '#3E6FA8'


def two_armies():
    random.seed(8)
    W, H = 1100, 800
    b = glow(550, 420, 520, '#FFD9A0', 3, .05)
    b += f'<path d="M0 640 Q550 600 {W} 640 L{W} {H} L0 {H}Z" fill="#7E5A44" /><path d="M520 560 L580 560 L600 {H} L500 {H}Z" fill="#9A7458" opacity="0.6" />'
    poses = ['karna/drawing-bow.svg', 'guard/pointing.svg', 'bhima/freed.svg', 'arjuna/standing-bow.svg', 'karna/watching.svg', 'guard/pulling.svg']
    for side, fill, rim, flagc, flagd in ((-1, KAURAVA, KAURAVA_L, '#B5402E', '#7E2A20'), (1, PANDAVA, PANDAVA_L, '#3E6FA8', '#2A4E7E')):
        # banners at the back, then three ranks of warriors, nearer ones bigger
        for k in range(5):
            x = 550 + side * (130 + k * 80)
            b += banner(x, 560 - k * 6, 300 + (k % 2) * 60, side * -10, flagc, flagd, side=-side)
        for rank, (base, s, n) in enumerate(((560, .2, 6), (620, .26, 5), (700, .34, 4))):
            for k in range(n):
                x = 550 + side * (110 + k * (420 / n) + rank * 20) + random.uniform(-10, 10)
                b += fig(poses[(k + rank) % len(poses)], x, base, s, fill, flip=(side == 1), rim=rim if rank == 2 else None)
    write('two-armies', b, 'two armies face each other across a gap: Kauravas in maroon on the left, Pandavas in blue on the right; banners behind.', W, H)


# ---------- the field after the war ----------
def war_remains():
    W, H = 1100, 700
    b = f'<path d="M0 470 Q300 430 560 456 Q820 480 {W} 444 L{W} {H} L0 {H}Z" fill="#6E4E3A" opacity="0.9" />'
    b += banner(150, 520, 300, 140, '#B5402E', '#7E2A20', torn=True) + banner(880, 500, 260, -150, '#3E6FA8', '#2A4E7E', torn=True, side=-1)
    b += banner(640, 470, 220, 60, '#B5402E', '#7E2A20', torn=True)
    b += wheel(330, 520, 120, 20, broken=True) + wheel(760, 560, 96, -30) + wheel(980, 600, 70, 60, broken=True)
    b += ''.join(f'<path d="M{x} {y} L{x + dx} {y - 120}" stroke="{INK}" stroke-width="9" /><path d="M{x} {y} L{x + dx} {y - 120}" stroke="#8A6A44" stroke-width="5" /><path d="M{x + dx - 8} {y - 120} l-10 -26 l26 10Z" fill="#C9B79A" stroke="{INK}" stroke-width="3" />'
                 for x, y, dx in ((460, 640, -30), (500, 630, 20), (560, 650, -50), (60, 620, 30), (1040, 640, -20), (690, 640, 40)))
    b += f'<path d="M210 610 L470 560 L480 590 L220 640Z" fill="#7A5634" stroke="{INK}" stroke-width="6" />'                    # a broken yoke
    b += ''.join(f'<g transform="translate({x} {y})"><path d="M-24 0 Q0 18 24 0 Q16 -10 0 -10 Q-16 -10 -24 0Z" fill="#9A6E44" stroke="{INK}" stroke-width="3" /><path d="M0 -10 Q-8 -30 0 -48 Q8 -30 0 -10Z" fill="#F2B544" /><path d="M0 -14 Q-3 -26 0 -36 Q3 -26 0 -14Z" fill="#FFF0B0" /></g>'
                 for x, y in ((80, 660), (420, 676), (620, 668), (900, 672), (1030, 680)))                                 # oil lamps
    write('war-remains', b, 'the field after the war: broken wheels, torn banners, arrows in the earth, a few oil lamps. No bodies.', W, H)


# ---------- women on the field ----------
def mourning_women():
    W, H = 1000, 800
    b = glow(500, 520, 420, '#FFB070', 3, .06)
    for path, x, base, s, flip in (('kunti/standing-sad.svg', 210, 740, .36, False), ('madri/turning-away.svg', 420, 700, .3, True), ('kunti/holding-back.svg', 640, 720, .34, True), ('madri/standing-sad.svg', 840, 760, .38, True)):
        b += fig(path, x, base, s, SIL, flip, rim='#E8A070')
    b += ''.join(f'<g transform="translate({x} {y})"><path d="M-24 0 Q0 18 24 0 Q16 -10 0 -10 Q-16 -10 -24 0Z" fill="#9A6E44" stroke="{INK}" stroke-width="3" /><path d="M0 -10 Q-8 -30 0 -48 Q8 -30 0 -10Z" fill="#F2B544" /></g>'
                 for x, y in ((120, 770), (330, 780), (540, 770), (740, 784), (940, 776)))
    write('mourning-women', b, 'widows of the war in silhouette, heads bowed, lamps at their feet.', W, H)


# ---------- the clan's end ----------
CLAN, CLAN_RIM = '#1E1A2A', '#C9D2E0'


def iron_bar(x1, y1, x2, y2, w=12):
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK}" stroke-width="{w + 6}" /><path d="M{x1} {y1} L{x2} {y2}" stroke="#6E7684" stroke-width="{w}" />'
            f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#C9D2E0" stroke-width="{w * .3:.0f}" transform="translate(-2 -2)" />')


def clan_falling():
    random.seed(3)
    W, H = 1100, 800
    b = glow(550, 500, 520, '#9AB0D0', 3, .05)
    b += f'<path d="M0 650 Q550 620 {W} 650 L{W} {H} L0 {H}Z" fill="#2E2A3A" opacity="0.7" />'
    people = [('guard/pulling.svg', 140, 700, .34, False), ('karna/drawing-bow.svg', 300, 680, .3, True), ('bhima/freed.svg', 470, 720, .38, False),
              ('guard/dragging.svg', 640, 700, .34, True), ('thief/running.svg', 800, 690, .32, False), ('guard/pointing.svg', 960, 720, .36, True),
              ('karna/kneeling-pleading.svg', 380, 760, .34, False), ('urvashi/arguing.svg', 720, 770, .3, True)]
    for path, x, base, s, flip in people:
        b += fig(path, x, base, s, CLAN, flip, rim=CLAN_RIM)
    for x, y, a in ((200, 420, 30), (360, 440, -40), (560, 400, 20), (700, 430, -30), (880, 420, 35)):
        b += f'<g transform="rotate({a} {x} {y})">{iron_bar(x, y - 90, x, y + 90)}</g>'
    write('clan-falling', b, "the Yadavas falling on one another in silhouette, rushes turned to iron bars in their hands. No blood (CE 16.4.36-41).", W, H)


def quarrel():
    W, H = 1000, 800
    b = glow(500, 440, 420, '#F0A060', 3, .07)
    b += fig('mandavya/cursing-hand-raised.svg', 330, 760, .44, CLAN, rim='#F0A060') + fig('urvashi/arguing.svg', 690, 760, .46, CLAN, flip=True, rim='#F0A060')
    for path, x, s, flip in (('guard/pointing.svg', 110, .26, False), ('karna/watching.svg', 900, .26, True), ('madri/standing-sad.svg', 520, .22, False)):
        b += fig(path, x, 640, s, '#3A3046', flip)
    b += ''.join(f'<path d="M{x} {y} l{dx} {dy}" stroke="#F0D090" stroke-width="6" />' for x, y, dx, dy in ((420, 300, 30, -30), (430, 340, 40, 0), (580, 300, -30, -30), (570, 340, -40, 0)))
    write('quarrel', b, 'two men who fought on opposite sides of the war, face to face, shouting; others turning to look (CE 16.4.16-27).', W, H)


def iron_grass():
    W, H = 800, 800
    b = glow(400, 400, 360, '#C9D2E0', 3, .07)
    for k, (x, a) in enumerate(((230, -18), (330, -6), (430, 6), (530, 18))):
        top = 120 + (k % 2) * 40
        b += (f'<g transform="rotate({a} {x} 700)"><path d="M{x} 700 Q{x - 20} 520 {x - 4} 460" stroke="{INK}" stroke-width="30" /><path d="M{x} 700 Q{x - 20} 520 {x - 4} 460" stroke="#6E9A4A" stroke-width="22" />'
              + iron_bar(x - 4, 470, x + 8, top, 30)
              + f'<path d="M{x - 4} 480 q-14 -16 0 -34 q14 18 0 34Z" fill="#E8F0FF" opacity="0.9" /></g>')
    write('iron-grass', b, 'blades of eraka grass turning into iron bars (CE 16.4.34-39).', W, H)


def clan_procession():
    W, H = 1200, 700
    b = ''
    src = open('assets/props/war-chariot.svg').read()
    inner = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    inner = inner.split('</desc>')[-1]
    for x, s in ((0, .5), (420, .44)):
        b += f'<g transform="translate({x} 300) scale({s})" opacity="0.95">{inner}</g>'
    for path, x, base, s in (('madri/walking.svg', 260, 640, .26), ('urvashi/walking.svg', 360, 650, .27), ('mandavya/walking.svg', 700, 650, .28), ('madri/walking.svg', 820, 640, .25), ('mandavya/walking.svg', 960, 660, .29)):
        b += fig(path, x, base, s, '#3A2E3A', rim='#F2C28A')
    write('clan-procession', b, "the Yadavas on the way to the sea: chariots and people walking to the right (CE 16.3.21-22).", W, H)


# ---------- the forest ----------
def deer_shape_leaves():
    W, H = 800, 800
    b = ''
    # what the hunter sees: something tawny and still, deep in the leaves
    b += f'<ellipse cx="420" cy="470" rx="190" ry="70" fill="#D9A24A" /><ellipse cx="420" cy="470" rx="190" ry="70" fill="none" stroke="#8A5A26" stroke-width="5" />'
    b += ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="#F4D58A" />' for x, y in ((340, 450), (390, 480), (450, 456), (500, 486), (540, 460)))
    random.seed(5)
    for k in range(70):
        x, y = random.uniform(40, 760), random.uniform(260, 720)
        if 250 < x < 590 and 430 < y < 510 and k % 3:
            continue
        r = random.uniform(30, 60); c = random.choice(('#3E6A3E', '#4E7E46', '#2E5434', '#5E8E50'))
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * .55:.0f}" fill="{c}" stroke="{INK}" stroke-width="3" transform="rotate({random.uniform(-40, 40):.0f} {x:.0f} {y:.0f})" />'
    write('deer-shape-leaves', b, "what the hunter sees: a tawny shape, still, deep in the leaves (CE 16.5.20).", W, H)


def ashwatthama():
    W, H = 800, 800
    b = glow(400, 380, 360, '#9AA6C8', 4, .07)
    b += f'<path d="M80 720 Q400 690 720 720" stroke="#3A3046" stroke-width="10" /><ellipse cx="400" cy="728" rx="150" ry="16" fill="#1E1A2A" opacity="0.6" />'
    b += fig('mandavya/walking.svg', 400, 724, .45, SIL, flip=True, rim='#C9D2E0')
    b += f'<circle cx="400" cy="140" r="12" fill="#C9463A" /><circle cx="400" cy="140" r="28" fill="#C9463A" opacity="0.25" />'
    write('ashwatthama-silhouette', b, 'a lone warrior walking alone under a cold sky, a red mark where the jewel was taken from his brow (CE 10.16).', W, H)


if __name__ == '__main__':
    two_armies(); war_remains(); mourning_women(); clan_falling(); quarrel(); iron_grass(); clan_procession(); deer_shape_leaves(); ashwatthama()
