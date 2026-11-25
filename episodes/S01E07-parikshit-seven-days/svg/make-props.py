"""S01E07 props and Takshaka, drawn in code in the library's flat style. Takshaka uses S01E06's snake rig in lotus-red (CE 1.40.3: "lotus-coloured"),
with a gold jewel on his head (a design choice: lord of snakes). No hood, like Nahusha's snake, so the two read as one family.
Run from the repo root (after make-cast.py):  python3 episodes/S01E07-parikshit-seven-days/svg/make-props.py
"""
import importlib.util
import math
import os
import random
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
def load(n, p):
    spec = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
N = load('p06', 'episodes/S01E06-nahusha-becomes-a-snake/svg/make-props.py')
V = load('c07', 'episodes/S01E07-parikshit-seven-days/svg/make-cast.py')
sys.argv = _argv
SVG, INK, GOLD, GOLD_L, GOLD_D, SIL = N.SVG, N.INK, N.GOLD, N.GOLD_L, N.GOLD_D, N.SIL
OUT = 'assets/props'
curve, rig = N.curve, N.rig


def write(pid, body, desc, w=800, h=800):
    svg = (f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
           f'<desc>S01E07 | {pid} | {desc} Made by episodes/S01E07-parikshit-seven-days/svg/make-props.py.</desc>{body}</svg>')
    ET.fromstring(svg)
    open(f'{OUT}/{pid}.svg', 'w').write(svg)
    print('wrote', f'{OUT}/{pid}.svg')


def path(pts): return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
def glow(cx, cy, r, c, n=4, o=.08): return ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r * (n - k) / n:.0f}" fill="{c}" opacity="{o}" />' for k in range(n))


# ---------- Takshaka ----------
RED = dict(YEL='#B8402E', YEL_L='#E58A62', YEL_D='#7E2420', SPOT='#3E1216', BELLY='#F0C9A0')


def takshaka():
    for k, v in RED.items():
        setattr(N, k, v)
    crest = (f'<path d="M-30 -92 Q-40 -150 4 -176 Q40 -146 34 -100Z" fill="{GOLD}" stroke="{INK}" stroke-width="6" /><path d="M2 -164 L24 -134 L4 -106 L-18 -134Z" fill="#2E8A9E" stroke="{INK}" stroke-width="5" /><path d="M2 -156 L12 -136 L0 -128Z" fill="#9FD3E6" />')
    N.snake_character('takshaka', dict(id='takshaka', name={'en': 'Takshaka', 'hi': 'तक्षक'}, role='Lord of snakes, who carries out the curse', divine=False, appearsIn=['S01E07'],
                                       look='S01E06’s snake rig in lotus-red with a gold jewel on the head. No hood.', sourceNotes='CE 1.39–40 (lotus-coloured, 1.40.3). The jewel is a design choice.', poses=['rearing'],
                                       files={'rearing': 'rearing.svg'}, facing='right', notes='Tall canvas (1000x2800, baseline 1550): the neck runs off the frame. shadow: false when the base is in frame.'), crest, ('rearing',), 'Takshaka')
    names = {'coils-back': 'takshaka-coils-back', 'coils-front': 'takshaka-coils-front'}
    old = N.write
    N.write = lambda pid, body, desc, w=800, h=800: write(names[pid], body, "Takshaka's coils: " + desc, w, h) if pid in names else None
    N.coils()
    N.write = old


def bow_dead_snake():
    """The tip of a bow rising from the lower left, a limp snake hung over it."""
    bow = curve([(-560, 1500), (-260, 1180), (0, 910), (150, 760), (300, 560), (392, 360), (430, 250)])
    d = path(curve([(250, 640), (262, 520), (300, 400), (372, 318), (440, 300), (510, 330), (560, 430), (580, 540), (576, 630)]))
    b = glow(420, 380, 380, '#FFE6B0', 4, .06)
    b += f'<path d="{path(bow)}" stroke="{INK}" stroke-width="46" /><path d="{path(bow)}" stroke="#8A5A36" stroke-width="34" /><path d="{path(bow)}" stroke="#B98A58" stroke-width="9" transform="translate(-8 -4)" />'
    for t in (58, 72):
        x, y = bow[t]
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="26" fill="{GOLD}" stroke="{INK}" stroke-width="5" />'
    b += f'<path d="M418 268 Q440 220 486 214" stroke="{INK}" stroke-width="34" /><path d="M418 268 Q440 220 486 214" stroke="{GOLD}" stroke-width="22" /><path d="M478 218 L980 1500" stroke="#E8DCC0" stroke-width="6" />'
    b += V.dead_snake(d, 58, (576, 634), 98)
    write('bow-dead-snake', b, 'the tip of a bow lifting a limp dead snake (CE 1.36.18-19).', 800, 1500)


def banyan():
    """One banyan: the left half burnt to ash, the right half growing back green."""
    random.seed(21)
    b = f'<ellipse cx="400" cy="760" rx="330" ry="34" fill="#000" opacity="0.22" />'
    for x, y, r in ((470, 250, 150), (600, 300, 140), (680, 400, 110), (560, 170, 120), (430, 360, 100)):   # leaves, right
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4E7E4A" stroke="{INK}" stroke-width="5" />'
    for x, y, r in ((470, 240, 122), (600, 290, 112), (680, 396, 84), (560, 166, 92)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#6FA05E" />'
    trunk = 'M300 760 Q340 640 330 520 Q320 430 250 340 L286 320 Q350 390 384 440 Q400 360 384 250 L420 248 Q440 350 440 430 Q500 380 560 340 L580 366 Q500 440 486 540 Q486 650 520 760Z'
    b += f'<path d="{trunk}" fill="#7A5638" stroke="{INK}" stroke-width="6" /><clipPath id="bl"><rect x="0" y="0" width="404" height="800" /></clipPath><g clip-path="url(#bl)"><path d="{trunk}" fill="#3A3436" stroke="{INK}" stroke-width="6" /></g>'
    for x, l in ((530, 250), (600, 300), (664, 240)):   # aerial roots, right
        b += f'<path d="M{x} 420 Q{x + 8} {420 + l / 2:.0f} {x - 4} {420 + l}" stroke="{INK}" stroke-width="15" /><path d="M{x} 420 Q{x + 8} {420 + l / 2:.0f} {x - 4} {420 + l}" stroke="#8E6A48" stroke-width="9" />'
    for pts in ('M262 344 Q190 280 130 290', 'M280 330 Q230 230 170 170', 'M390 260 Q360 170 300 120', 'M330 480 Q220 430 120 440', 'M210 300 Q180 250 120 230'):   # bare burnt boughs, left
        b += f'<path d="{pts}" stroke="{INK}" stroke-width="24" /><path d="{pts}" stroke="#3A3436" stroke-width="15" />'
    for _ in range(22):
        x, y = random.uniform(90, 380), random.uniform(120, 620)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(4, 9):.0f}" fill="{random.choice(("#F0703A", "#FFB347", "#8A8388"))}" opacity="0.9" />'
    b += '<path d="M120 750 Q220 700 330 744 Q260 776 120 750Z" fill="#8A8388" opacity="0.8" />'
    for _ in range(16):
        b += f'<path d="{N.P.star(random.uniform(440, 740), random.uniform(110, 520), random.choice((13, 18)), 5)}" fill="#FFFBE0" />'
    for x, y in ((420, 470), (452, 400), (438, 300)):   # fresh leaves on the join
        b += f'<path d="M{x} {y} q34 -44 66 -20 q-18 38 -66 20Z" fill="#9FD07A" stroke="{INK}" stroke-width="4" />'
    write('banyan-reviving', b, 'a banyan, half burnt to ash by Takshaka, half growing back green (CE 1.39.5-10).')


def wave(x0, y0, l, a, n=3):
    return [(x0 + l * t / 60, y0 + a * math.sin(t / 60 * math.pi * 2 * n) * (1 - t / 75)) for t in range(61)]


def snake_shadow():
    pts = [(120, 420)] + wave(140, 420, 520, 46)
    b = f'<path d="{path(pts)}" stroke="#1E1420" stroke-width="74" /><path d="M640 372 Q720 356 770 420 Q720 480 640 462Z" fill="#1E1420" /><path d="M766 420 l30 -12 M766 420 l28 14" stroke="#1E1420" stroke-width="8" />'
    write('snake-shadow', f'<g opacity="0.5">{b}</g>', 'a snake-shaped shadow on the ground.')


def fruit_worm():
    b = glow(400, 400, 370, '#E07A2E', 4, .06)
    b += (f'<path d="M400 190 Q300 130 210 220 Q110 340 170 500 Q230 660 400 676 Q570 660 630 500 Q690 340 590 220 Q500 130 400 190Z" fill="#D9573A" stroke="{INK}" stroke-width="9" />'
          f'<path d="M232 250 Q156 360 206 490" stroke="#F09A6A" stroke-width="26" /><path d="M560 600 Q640 480 596 320" stroke="#A8382A" stroke-width="22" opacity="0.7" />'
          f'<path d="M400 196 Q392 130 430 84" stroke="{INK}" stroke-width="22" /><path d="M400 196 Q392 130 430 84" stroke="#6A4A2E" stroke-width="13" /><path d="M424 120 Q500 50 600 92 Q540 168 424 120Z" fill="#6FA05E" stroke="{INK}" stroke-width="7" /><path d="M432 120 Q510 96 586 96" stroke="#3E6A3E" stroke-width="5" />'
          f'<ellipse cx="420" cy="430" rx="128" ry="104" fill="#FBE3B4" stroke="{INK}" stroke-width="7" /><ellipse cx="424" cy="440" rx="62" ry="46" fill="#4A1E18" stroke="{INK}" stroke-width="5" />')
    b += V.worm(430, 420, 4.4)
    write('fruit-worm', b, 'a red fruit bitten open, a tiny copper worm with black eyes inside (CE 1.39.29).')


def fruit_bearers():
    b = ''
    for x in (90, 420, 750):
        p = wave(x - 30, 820, 250, 20, 2)
        b += f'<path d="{path(p)}" stroke="#1E1420" stroke-width="30" /><path d="M{x + 212} 800 Q{x + 262} 796 {x + 280} 820 Q{x + 258} 846 {x + 212} 840Z" fill="#1E1420" />'
    b = f'<g opacity="0.5">{b}</g>'
    for x in (0, 330, 660):
        b += rig('mandavya/walking.svg', f'translate({x - 30} 40) scale(0.5)')
        tx, ty = x + 300, 400
        b += (f'<path d="M{tx - 78} {ty} Q{tx} {ty + 62} {tx + 78} {ty}Z" fill="{GOLD}" stroke="{INK}" stroke-width="5" /><path d="M{tx - 70} {ty + 8} Q{tx} {ty + 30} {tx + 70} {ty + 8}" stroke="{GOLD_D}" stroke-width="5" />'
              + ''.join(f'<circle cx="{tx + dx}" cy="{ty + dy}" r="26" fill="{c}" stroke="{INK}" stroke-width="4" />' for dx, dy, c in ((-40, -16, '#E0A23A'), (40, -16, '#8E9A4A'), (0, -22, '#D9573A'), (-18, -54, '#E0A23A'), (22, -52, '#D9573A'))))
    write('fruit-bearers', b, 'three ascetics carrying fruit; their shadows are snakes (CE 1.39.23-25).', 1100, 880)


def worm_fingertip():
    """A king's hand, finger and thumb meeting, the worm held up between them."""
    a, c, e = V.P_SKIN
    def f(d, w): return f'<path d="{d}" stroke="{INK}" stroke-width="{w + 14}" /><path d="{d}" stroke="{a}" stroke-width="{w}" /><path d="{d}" stroke="{c}" stroke-width="{w * .14:.0f}" transform="translate({w * .28:.0f} 4)" opacity="0.7" />'
    b = glow(430, 260, 330, '#FFE6B0', 4, .09)
    b += f('M520 640 Q650 560 640 420', 58) + f('M530 690 Q700 640 704 510', 54) + f('M530 740 Q710 720 736 610', 48)
    b += (f'<path d="M286 1520 L280 900 Q276 760 300 640 Q360 560 470 580 Q570 600 580 700 Q570 800 556 900 L556 1520Z" fill="{a}" stroke="{INK}" stroke-width="9" /><path d="M320 900 Q306 780 322 680" stroke="{c}" stroke-width="16" />')
    b += f('M500 650 Q570 470 456 318', 70) + f('M346 660 Q300 450 424 316', 72)
    b += f'<path d="M434 316 Q452 300 466 320 Q462 346 446 350Z" fill="#F3D3B0" stroke="{INK}" stroke-width="4" /><path d="M330 520 Q356 508 378 516 M336 548 Q360 538 384 544 M516 500 Q534 508 552 504" stroke="{e}" stroke-width="5" />'
    b += (f'<path d="M280 800 Q420 840 560 796 L560 852 Q420 894 282 852Z" fill="{GOLD}" stroke="{INK}" stroke-width="7" />' + ''.join(f'<circle cx="{x}" cy="{y}" r="14" fill="{k}" stroke="{INK}" stroke-width="4" />' for x, y, k in ((346, 842, '#C9463A'), (424, 852, '#2E8A9E'), (502, 842, '#C9463A'))))
    b += V.worm(436, 262, 3.0)
    write('worm-fingertip', b, 'a king’s hand, the copper worm held up between finger and thumb.', 800, 1500)


def gandhari():
    b = glow(400, 380, 350, '#E07A2E', 4, .08)
    src = 'kunti/' + sorted(f for f in os.listdir('assets/characters/kunti') if f.endswith('.svg'))[0]
    b += rig(src, 'translate(52 -236) scale(0.68)', fill='#E8B53A') + rig(src, 'translate(60 -230) scale(0.68)', fill=SIL)
    b += f'<g transform="translate(56 -66) scale(0.86 1)"><path d="M356 184 Q410 172 452 184 L450 214 Q408 204 358 216Z" fill="#F2E2BC" stroke="{INK}" stroke-width="5" /><path d="M358 200 Q316 220 300 270 M358 208 Q326 240 322 292" stroke="#F2E2BC" stroke-width="11" /></g>'
    # a peacock feather in front of her
    b += (f'<path d="M640 760 Q650 560 610 380" stroke="{INK}" stroke-width="14" /><path d="M640 760 Q650 560 610 380" stroke="#7E9A4A" stroke-width="8" />'
          + ''.join(f'<path d="M{640 - 4 * k:.0f} {720 - 34 * k} q{s * 60} -16 {s * 78} -52" stroke="#5E8A4E" stroke-width="5" />' for k in range(9) for s in (-1, 1))
          + f'<ellipse cx="604" cy="330" rx="72" ry="96" fill="#5E8A4E" stroke="{INK}" stroke-width="6" transform="rotate(-10 604 330)" /><ellipse cx="604" cy="324" rx="50" ry="64" fill="#C79A3A" transform="rotate(-10 604 324)" /><ellipse cx="603" cy="322" rx="36" ry="46" fill="#2E8A9E" transform="rotate(-10 603 322)" /><ellipse cx="602" cy="316" rx="20" ry="25" fill="#1E2A5A" transform="rotate(-10 602 316)" />')
    write('gandhari-silhouette', b, 'Gandhari, blindfolded, in silhouette, a peacock feather before her (E08 tease).')


if __name__ == '__main__':
    bow_dead_snake(); banyan(); snake_shadow(); fruit_worm(); fruit_bearers(); worm_fingertip(); gandhari(); takshaka()
