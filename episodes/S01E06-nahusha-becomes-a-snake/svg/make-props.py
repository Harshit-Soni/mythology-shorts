"""S01E06 props, drawn in code in the library's flat style; a few embed the library rigs (sages, Nahusha, Indra).

The snake follows the text (CE 3.175.13-14): huge, spotted, turmeric-yellow, red-eyed, four-fanged. No hood.
Run from the repo root (after make-cast.py):  python3 episodes/S01E06-nahusha-becomes-a-snake/svg/make-props.py [out_dir]
"""
import json
import copy
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
CH = 'assets/characters'
NS = '{%s}' % SVG
glow_rings = P.glow_rings
YEL, YEL_L, YEL_D, SPOT, BELLY = '#DDAE3C', '#F0CE72', '#B07F22', '#6E4420', '#F3E0A8'


def write(pid, body, desc, w=800, h=800):
    os.makedirs(OUT, exist_ok=True)
    svg = (f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" '
           f'stroke-linecap="round" stroke-linejoin="round"><desc>S01E06 | {pid} | {desc} '
           f'Made by episodes/S01E06-nahusha-becomes-a-snake/svg/make-props.py.</desc>{body}</svg>')
    ET.fromstring(svg)
    with open(f'{OUT}/{pid}.svg', 'w') as f:
        f.write(svg)
    print('wrote', f'{OUT}/{pid}.svg')


def rig(path, transform, only=None, drop=(), fill=None, show=()):
    """A library pose as a fragment: ids removed, hidden groups dropped; fill = one flat colour (a silhouette)."""
    r = ET.parse(f'{CH}/{path}').getroot()
    for e in r.iter():
        if e.get('id') in show:
            e.attrib.pop('style', None)
    root = r
    if only:
        root = next(e for e in r.iter() if e.get('id') == only)
    root = copy.deepcopy(root)

    def prune(e):
        for c in list(e):
            if c.get('id') in drop or 'display:none' in (c.get('style') or '') or c.tag in (NS + 'title', NS + 'desc', NS + 'metadata'):
                e.remove(c)
            else:
                prune(c)
    prune(root)
    for e in root.iter():
        for a in ('id', 'data-pivot', 'data-role', 'data-base-transform', 'data-character'):
            e.attrib.pop(a, None)
        if fill:
            for a in ('fill', 'stroke'):
                if e.get(a) and e.get(a) != 'none':
                    e.set(a, fill)
    inner = ''.join(ET.tostring(c, encoding='unicode') for c in root)
    inner = inner.replace('ns0:', '').replace(f' xmlns:ns0="{SVG}"', '').replace(f' xmlns="{SVG}"', '')
    t0 = '' if only else ''
    return f'<g transform="{transform}" fill="none">{inner}</g>'


def curve(ps, k=14):
    """A smooth line through the points (Catmull-Rom)."""
    q = [ps[0]] + list(ps) + [ps[-1]]
    out = []
    for i in range(1, len(q) - 2):
        a, b, c, d = q[i - 1:i + 3]
        for j in range(k):
            t = j / k
            out.append(tuple(.5 * (2 * b[m] + (c[m] - a[m]) * t + (2 * a[m] - 5 * b[m] + 4 * c[m] - d[m]) * t * t + (3 * b[m] - a[m] - 3 * c[m] + d[m]) * t ** 3) for m in (0, 1)))
    return out + [ps[-1]]


# ---------- the snake ----------
def sample(fn, n=90):
    return [fn(i / (n - 1)) for i in range(n)]


def snake(pts, w, taper=None, light=False):
    """A snake's body along pts. w = width; taper(t) scales it. Outline, body, belly shade, highlight, spots."""
    taper = taper or (lambda t: 1)
    n = len(pts)
    d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)

    def strip(scale, off=0.0):
        L, R = [], []
        for i, (x, y) in enumerate(pts):
            x0, y0 = pts[max(0, i - 1)]; x1, y1 = pts[min(n - 1, i + 1)]
            a = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(a), math.cos(a)
            ww = w * taper(i / (n - 1)) / 2
            L.append((x + nx * ww * (off + scale), y + ny * ww * (off + scale))); R.append((x + nx * ww * (off - scale), y + ny * ww * (off - scale)))
        return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in L + R[::-1]) + 'Z'
    if light:
        return (f'<path d="{strip(1.5)}" fill="#FFE08A" opacity="0.25" /><path d="{strip(1)}" fill="#FFE9A8" opacity="0.85" stroke="{GOLD}" stroke-width="4" /><path d="{strip(.45)}" fill="#FFFBE8" />')
    s = f'<path d="{strip(1)}" fill="{YEL}" stroke="{INK}" stroke-width="6" /><path d="{strip(.34, .62)}" fill="{YEL_D}" opacity="0.75" /><path d="{strip(.13, -.62)}" fill="{YEL_L}" opacity="0.9" />'
    step = max(3, int(w / (math.dist(pts[0], pts[1]) + 1) * 0.62))
    for i in range(step // 2, n - 2, step):
        x, y = pts[i]; x1, y1 = pts[min(n - 1, i + 1)]; a = math.degrees(math.atan2(y1 - y, x1 - x)); ww = w * taper(i / (n - 1))
        s += f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})"><path d="M{-ww * .22:.0f} 0 Q0 {-ww * .36:.0f} {ww * .22:.0f} 0 Q0 {ww * .3:.0f} {-ww * .22:.0f} 0Z" fill="{SPOT}" stroke="{INK}" stroke-width="3" /><ellipse rx="{ww * .09:.0f}" ry="{ww * .07:.0f}" fill="{YEL_L}" /></g>'
    return s


def head(x, y, s, rot=0, flip=1, light=False):
    """The snake's head in profile, facing right: no hood; red eye, four fangs, a forked tongue."""
    if light:
        return f'<g transform="translate({x} {y}) rotate({rot}) scale({s * flip} {s})"><path d="M-130 -74 Q-20 -126 110 -84 Q196 -50 210 -6 Q200 40 110 60 Q-20 92 -130 72Z" fill="#FFE9A8" stroke="{GOLD}" stroke-width="5" /></g>'
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s * flip} {s})">'
            f'<path d="M188 26 Q250 34 284 20 M284 20 l34 -20 M284 20 l36 14" stroke="#B5243A" stroke-width="9" />'
            f'<path d="M-130 20 Q-20 60 96 46 Q150 60 196 34 Q190 84 120 100 Q-10 118 -120 84 Q-168 60 -130 20Z" fill="{BELLY}" stroke="{INK}" stroke-width="6" />'
            f'<path d="M-100 22 Q40 70 186 32 Q150 70 60 74 Q-40 72 -100 40Z" fill="#8E2A34" />'
            f'<path d="M96 40 L106 78 L120 42Z M142 42 L152 74 L164 40Z" fill="#FFF8E9" stroke="{INK}" stroke-width="4" /><path d="M84 86 L94 62 L104 88Z M130 84 L138 62 L148 82Z" fill="#FFF8E9" stroke="{INK}" stroke-width="4" />'
            f'<path d="M-130 -70 Q-20 -126 110 -84 Q196 -50 210 0 Q206 34 150 34 Q20 56 -126 36 Q-196 -20 -130 -70Z" fill="{YEL}" stroke="{INK}" stroke-width="6" />'
            f'<path d="M-130 -58 Q-20 -106 104 -70 Q170 -44 190 -8" stroke="{YEL_L}" stroke-width="10" />'
            f'<path d="M-120 12 Q20 40 150 22 Q196 18 204 2" stroke="{YEL_D}" stroke-width="9" />'
            f'<path d="M-96 -44 Q-70 -78 -40 -50 Q-66 -22 -96 -44Z M-24 -70 Q6 -96 30 -66 Q4 -46 -24 -70Z M-80 -4 Q-58 -24 -36 -4 Q-58 12 -80 -4Z" fill="{SPOT}" stroke="{INK}" stroke-width="3" />'
            f'<ellipse cx="78" cy="-32" rx="33" ry="26" fill="#C92B2B" stroke="{INK}" stroke-width="6" /><ellipse cx="80" cy="-32" rx="23" ry="18" fill="#F0563A" /><ellipse cx="82" cy="-32" rx="7" ry="19" fill="{INK}" /><circle cx="72" cy="-40" r="5" fill="#FFF" />'
            f'<path d="M36 -56 Q80 -76 124 -44" stroke="{INK}" stroke-width="9" /><ellipse cx="184" cy="-14" rx="6" ry="4" fill="{INK}" /></g>')


def ring(cx, cy, rx, ry, a0, a1, n=60):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1)))) for i in range(n)]


def loop(cx, cy, rx, ry, a0, a1, w, light=False):
    """A coil half as thick strokes (round ends), so tight curves don't fold over themselves."""
    pts = ring(cx, cy, rx, ry, a0, a1)
    d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
    if light:
        return (f'<path d="{d}" stroke="#FFE08A" stroke-width="{w * 1.4:.0f}" opacity="0.3" /><path d="{d}" stroke="{GOLD}" stroke-width="{w + 8:.0f}" /><path d="{d}" stroke="#FFE9A8" stroke-width="{w}" /><path d="{d}" stroke="#FFFBE8" stroke-width="{w * .45:.0f}" />')
    out = (f'<path d="{d}" stroke="{INK}" stroke-width="{w + 12}" /><path d="{d}" stroke="{YEL}" stroke-width="{w}" /><path d="{d}" stroke="{YEL_D}" stroke-width="{w * .3:.0f}" opacity="0.75" transform="translate(0 {w * .3:.0f})" />'
           f'<path d="{d}" stroke="{YEL_L}" stroke-width="{w * .12:.0f}" transform="translate(0 {-w * .3:.0f})" />')
    for i in range(7, len(pts) - 5, 11):
        x, y = pts[i]; x1, y1 = pts[i + 1]; a = math.degrees(math.atan2(y1 - y, x1 - x))
        out += f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})"><path d="M{-w * .2:.0f} 0 Q0 {-w * .34:.0f} {w * .2:.0f} 0 Q0 {w * .28:.0f} {-w * .2:.0f} 0Z" fill="{SPOT}" stroke="{INK}" stroke-width="3" /><ellipse rx="{w * .08:.0f}" ry="{w * .06:.0f}" fill="{YEL_L}" /></g>'
    return out


def great_snake():
    b = '<ellipse cx="400" cy="706" rx="330" ry="44" fill="#000" opacity="0.25" />'
    for cy, rx, ry, w in ((610, 290, 78, 128), (520, 238, 64, 118), (440, 186, 50, 108)):
        b += loop(400, cy, rx, ry, 180, 360, w * .86) + loop(400, cy + 14, rx, ry, 0, 180, w * .86)
    neck = sample(lambda t: (330 + 60 * math.sin(t * 3.4) - 70 * t, 440 - 262 * t), 60)
    b += snake(neck, 112, lambda t: 1 - .06 * t)
    b += snake(sample(lambda t: (640 + 110 * t, 640 + 60 * math.sin(t * 4)), 40), 70, lambda t: 1 - .92 * t)
    b += head(350, 180, 1.0, -4)
    write('great-snake', b, 'the great snake coiled, head raised: spotted, turmeric-yellow, red-eyed, no hood.')


RINGS = ((-150, 188, 44, 92), (-20, 204, 50, 100), (112, 214, 54, 106))


def coils():
    yc, front, back, lit = 272, '', '', ''
    for dy, rx, ry, w in RINGS:
        back += loop(400, yc + dy, rx, ry, 180, 360, w * .9)
        front += loop(400, yc + dy + 16, rx, ry, 0, 180, w * .9)
        lit += loop(400, 400 + dy, rx, ry, 180, 360, w * .7, light=True) + loop(400, 400 + dy + 16, rx, ry, 0, 180, w * .7, light=True)
    write('coils-back', back, 'the far halves of three coils (behind a held figure; use with coils-front).', 800, 1200)
    write('coils-front', front, 'the near halves of three coils (in front of a held figure).', 800, 1200)
    lit = glow_rings(400, 400, 370, '#FFE08A', 4, 0.1) + lit
    random.seed(3)
    lit += ''.join(f'<path d="{P.star(random.uniform(90, 710), random.uniform(60, 740), 16, 5)}" fill="#FFFBE8" />' for _ in range(22))
    write('coils-of-light', lit, 'the snake\'s coils turning into light as the curse breaks.')


def snake_head():
    """Tall canvas (800x2100): the neck runs off the bottom of the frame. The head is at canvas y 330."""
    neck = sample(lambda t: (90 + 50 * math.sin(t * 4.6) + 170 * t ** 3, 2160 - 1750 * t - 60 * math.sin(t * 2.6)), 170)
    b = snake(neck, 240, lambda t: 1.1 - .2 * t) + head(420, 330, 1.5, 6)
    write('snake-head', b, "the great snake's head and neck rising from the ground, facing right.", 800, 2100)


def eye(reflect=False):
    b = f'<rect x="20" y="20" width="760" height="760" rx="90" fill="{YEL}" stroke="{INK}" stroke-width="9" />'
    random.seed(5)
    for y in range(80, 780, 92):
        for x in range(70 + (y // 92 % 2) * 46, 790, 92):
            b += f'<path d="M{x - 46} {y} Q{x} {y - 52} {x + 46} {y} Q{x} {y + 52} {x - 46} {y}Z" fill="{random.choice((YEL, YEL_L, YEL_D, YEL))}" stroke="{YEL_D}" stroke-width="4" />'
    for x, y, r in ((130, 150, 60), (670, 170, 70), (150, 640, 66), (640, 660, 58)):
        b += f'<path d="M{x - r} {y} Q{x} {y - r} {x + r} {y} Q{x} {y + r * .8:.0f} {x - r} {y}Z" fill="{SPOT}" stroke="{INK}" stroke-width="5" />'
    b += f'<path d="M90 400 Q250 190 420 190 Q600 200 716 400 Q590 610 400 610 Q220 606 90 400Z" fill="{INK}" /><ellipse cx="404" cy="400" rx="262" ry="186" fill="#A31F26" /><ellipse cx="404" cy="400" rx="206" ry="168" fill="#D93A2C" /><ellipse cx="404" cy="400" rx="140" ry="150" fill="#F0703A" />'
    if not reflect:
        b += f'<ellipse cx="404" cy="400" rx="42" ry="164" fill="{INK}" /><circle cx="330" cy="310" r="30" fill="#FFF3D8" /><circle cx="300" cy="360" r="12" fill="#FFF3D8" />'
    else:
        b += f'<ellipse cx="404" cy="400" rx="150" ry="172" fill="#2A1420" />'
        b += (f'<path d="M324 500 L320 380 Q324 300 404 276 Q484 300 488 380 L484 500Z" fill="{GOLD}" stroke="{INK}" stroke-width="5" /><path d="M346 496 L342 390 Q348 330 404 310 Q460 330 466 390 L462 496Z" fill="#8E2E4E" />'
              f'<path d="M306 494 Q404 474 502 494 L506 530 L302 530Z" fill="#A83A5C" stroke="{INK}" stroke-width="4" /><path d="M298 528 L510 528 L502 556 L306 556Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" /><circle cx="404" cy="292" r="9" fill="#C9463A" /><circle cx="320" cy="300" r="22" fill="#FFF3D8" opacity="0.8" />')
    edge = b
    b = ''
    b += f'<path d="M78 372 Q250 150 430 160 Q620 176 730 376" stroke="{INK}" stroke-width="26" /><path d="M96 430 Q240 634 404 636 Q596 630 712 430" stroke="{YEL_D}" stroke-width="18" />'
    if not reflect:
        write('snake-eye', f'<defs><clipPath id="se"><rect x="20" y="20" width="760" height="760" rx="90" /></clipPath></defs><g clip-path="url(#se)">{edge}{b}</g><rect x="20" y="20" width="760" height="760" rx="90" stroke="{INK}" stroke-width="9" />', "the great snake's red eye (the riddle).")
        return
    # full frame (1440x2560 at scale 1 = the whole 1080x1920): scales everywhere, the eye in the middle
    full = f'<rect width="1440" height="2560" fill="{YEL}" />'
    for y in range(0, 2640, 130):
        for x in range((y // 130 % 2) * 65 - 65, 1570, 130):
            full += f'<path d="M{x - 65} {y} Q{x} {y - 74} {x + 65} {y} Q{x} {y + 74} {x - 65} {y}Z" fill="{random.choice((YEL, YEL_L, YEL_D, YEL, YEL))}" stroke="{YEL_D}" stroke-width="5" />'
    for x, y, r in ((170, 300, 120), (1240, 420, 140), (220, 2060, 130), (1180, 2160, 120), (720, 160, 100), (700, 2400, 110), (120, 1720, 90), (1330, 1700, 90)):
        full += f'<path d="M{x - r} {y} Q{x} {y - r} {x + r} {y} Q{x} {y + r * .8:.0f} {x - r} {y}Z" fill="{SPOT}" stroke="{INK}" stroke-width="7" />'
    lid = edge[edge.index('<path d="M90 400'):]
    write('snake-eye-throne', f'{full}<g transform="translate(720 1120) scale(1.66) translate(-404 -400)">{lid}{b}</g>', "full frame: the great snake's red eye, the throne of heaven reflected in it.", 1440, 2560)


# ---------- the throne and the palanquin ----------
def throne_icon():
    b = glow_rings(400, 360, 370, GOLD, 4, .08)
    b += (f'<path d="M236 520 L226 300 Q236 150 330 116 Q400 90 470 116 Q564 150 574 300 L564 520Z" fill="{GOLD}" stroke="{INK}" stroke-width="7" /><path d="M274 516 L266 310 Q276 190 350 162 Q400 144 450 162 Q524 190 534 310 L526 516Z" fill="#8E2E4E" stroke="{INK}" stroke-width="5" />'
          f'<path d="M318 510 Q300 270 400 244 Q500 270 482 510" stroke="#B5506E" stroke-width="9" /><circle cx="400" cy="126" r="18" fill="#C9463A" stroke="{INK}" stroke-width="5" /><path d="M376 100 Q372 70 400 62 Q428 70 424 100Z" fill="{GOLD_L}" stroke="{INK}" stroke-width="5" />'
          f'<path d="M190 506 Q400 470 610 506 L622 576 L178 576Z" fill="#A83A5C" stroke="{INK}" stroke-width="6" /><path d="M196 532 Q400 500 604 532" stroke="{GOLD}" stroke-width="10" /><path d="M164 572 L636 572 L622 676 L178 676Z" fill="{GOLD}" stroke="{INK}" stroke-width="6" />'
          + ''.join(f'<path d="M{x} 658 q0 -60 30 -60 q30 0 30 60Z" fill="{GOLD_D}" stroke="{INK}" stroke-width="5" />' for x in (206, 286, 366, 446, 526))
          + f'<path d="M140 674 L660 674 L684 730 L116 730Z" fill="#F4E9DA" stroke="{INK}" stroke-width="6" />')
    write('throne-icon', b, 'the throne of heaven, empty.')


def palanquin(x, y, s, rider=''):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-150 -60 L-150 -330 M150 -60 L150 -330" stroke="{INK}" stroke-width="24" /><path d="M-150 -60 L-150 -330 M150 -60 L150 -330" stroke="{GOLD}" stroke-width="14" />'
            f'<path d="M-130 -70 L-130 -300 L130 -300 L130 -70Z" fill="#5C2E52" opacity="0.85" />{rider}'
            f'<path d="M-150 -320 Q-110 -240 -134 -120 L-158 -110 L-166 -320Z M150 -320 Q110 -240 134 -120 L158 -110 L166 -320Z" fill="#C9463A" stroke="{INK}" stroke-width="4" />'
            f'<path d="M-200 -320 Q-120 -440 0 -452 Q120 -440 200 -320Z" fill="{GOLD}" stroke="{INK}" stroke-width="6" /><path d="M-190 -330 Q0 -372 190 -330" stroke="{GOLD_D}" stroke-width="9" /><path d="M-18 -448 Q-22 -486 0 -496 Q22 -486 18 -448Z" fill="{GOLD_L}" stroke="{INK}" stroke-width="5" />'
            + ''.join(f'<path d="M{k} -322 q17 34 34 0" fill="#C9463A" stroke="{INK}" stroke-width="3" />' for k in range(-198, 190, 36))
            + f'<path d="M-190 -78 L190 -78 L172 -10 L-172 -10Z" fill="#8E2E4E" stroke="{INK}" stroke-width="6" /><path d="M-184 -62 L184 -62" stroke="{GOLD}" stroke-width="10" />'
            + ''.join(f'<circle cx="{k}" cy="-34" r="11" fill="{GOLD}" stroke="{INK}" stroke-width="3" />' for k in range(-140, 150, 56))
            + '</g>')


def pole(x0, x1, y):
    return (f'<path d="M{x0} {y} L{x1} {y}" stroke="{INK}" stroke-width="34" /><path d="M{x0} {y} L{x1} {y}" stroke="#8A5A36" stroke-width="24" /><path d="M{x0} {y - 6} L{x1} {y - 6}" stroke="#B98A58" stroke-width="6" />'
            f'<circle cx="{x0}" cy="{y}" r="24" fill="{GOLD}" stroke="{INK}" stroke-width="5" /><circle cx="{x1}" cy="{y}" r="24" fill="{GOLD}" stroke="{INK}" stroke-width="5" />')


def palanquin_icon():
    write('palanquin-icon', glow_rings(400, 400, 370, '#C9463A', 4, .06) + pole(40, 760, 560) + palanquin(400, 590, 1.08), 'an empty palanquin.')


def palanquin_carried():
    rider = rig('nahusha/seated-throne.svg', 'translate(-128 -478) scale(0.265)')
    S = 0.43
    far = ''.join(rig('mandavya/walking.svg', f'translate({x} 96) scale({S})') for x in (40, 700))
    near = rig('mandavya/walking.svg', f'translate(-60 130) scale({S})') + rig('agastya/softening.svg', f'translate(800 130) scale({S})')
    b = ('<ellipse cx="600" cy="808" rx="560" ry="30" fill="#4E2E5A" opacity="0.25" />'
         f'<g opacity="0.82">{far}</g>' + pole(60, 1150, 300) + palanquin(600, 370, 0.92, rider) + near)
    write('palanquin-carried', b, 'Nahusha in a palanquin carried by sages (Agastya at the front, right).', 1200, 850)


def foot_on_head():
    """Agastya's bowed head at the bottom, a jewelled golden-anklet foot set on his matted hair."""
    hd = rig('agastya/softening.svg', 'translate(-690 60) scale(2.0)', only=None, drop=('upper-body-front', 'dhoti', 'leg-far', 'leg-near'), show=('eyes-closed',))
    sk = ('#DDA06A', '#BF834F', '#995B39')
    ft = (f'<path d="M300 -40 L520 -40 Q512 90 520 160 Q640 196 720 232 Q760 258 736 286 Q600 320 420 300 Q300 290 286 220 Q276 100 300 -40Z" fill="{sk[0]}" stroke="{INK}" stroke-width="8" />'
          f'<path d="M300 -40 L372 -40 Q352 110 372 220 Q420 288 560 300 Q380 312 310 270 Q276 200 300 -40Z" fill="{sk[1]}" />'
          + ''.join(f'<path d="M{x} {y} q22 4 24 22" stroke="{sk[2]}" stroke-width="5" />' for x, y in ((640, 226), (672, 238), (702, 250)))
          + f'<path d="M292 60 Q410 104 520 56 L522 108 Q410 156 288 112Z" fill="{GOLD}" stroke="{INK}" stroke-width="6" />' + ''.join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}" stroke="{INK}" stroke-width="4" />' for x, y, c in ((330, 102, '#C9463A'), (408, 118, '#2E8A9E'), (486, 100, '#C9463A')))
          + f'<path d="M280 -60 L540 -60 L534 -8 Q410 30 288 -8Z" fill="#5C3D8C" stroke="{INK}" stroke-width="6" /><path d="M288 -14 Q410 22 534 -14" stroke="{GOLD}" stroke-width="10" />')
    leg = f'<path d="M292 -900 L528 -900 L540 -50 L280 -50Z" fill="#5C3D8C" stroke="{INK}" stroke-width="6" /><path d="M360 -900 Q340 -400 352 -60 M440 -900 Q470 -400 462 -60" stroke="#3E2664" stroke-width="9" /><path d="M400 -900 Q396 -500 404 -60" stroke="#7E5BB0" stroke-width="7" />'
    b = f'<defs><clipPath id="fh"><rect x="0" y="0" width="800" height="1430" /></clipPath></defs><g clip-path="url(#fh)"><g transform="translate(0 330)"><g transform="translate(70 60)">{hd}</g><g transform="translate(-60 138)">{leg}{ft}</g></g></g>'
    write('foot-on-head', b, "full-frame close-up: a jewelled foot set on Agastya's matted hair.", 800, 1430)


# ---------- light, the fall, Indra, the tease ----------
def strength_stream():
    def band(off, w, c, o): return f'<path d="M760 {250 + off} Q600 {120 + off} 420 {230 + off} Q240 {340 + off} 40 {190 + off}" stroke="{c}" stroke-width="{w}" opacity="{o}" />'
    b = band(0, 120, '#FFE08A', .18) + band(0, 70, '#FFE08A', .35) + band(0, 28, '#FFF6C8', .9) + band(-34, 9, '#FFFBE8', .9) + band(36, 9, '#FFFBE8', .8)
    random.seed(8)
    b += ''.join(f'<path d="{P.star(random.uniform(60, 740), random.uniform(120, 360), 15, 5)}" fill="#FFFBE8" />' for _ in range(14))
    write('strength-stream', f'<g transform="translate(0 130)">{b}</g>', "a god's strength as a stream of light, from the right to the left.")


def falling():
    body = rig('nahusha/gaze.svg', 'translate(770 600) rotate(168) scale(0.46)', drop=('halo', 'crown', 'dhoti', 'leg-far', 'leg-near', 'rear-drape'))
    tail = snake(curve([(474, 312), (466, 260), (440, 190), (448, 110), (520, 62), (610, 84), (640, 160), (590, 214), (530, 190)]), 108, lambda t: 1 - .86 * t)
    sash = f'<g transform="translate(474 292) rotate(-11)"><path d="M-66 -26 Q0 -8 66 -26 L60 24 Q0 42 -60 24Z" fill="#5E3A9E" stroke="{INK}" stroke-width="5" /><path d="M-60 12 Q0 30 60 12" stroke="{GOLD}" stroke-width="8" /></g>'
    crown = rig('nahusha/gaze.svg', 'translate(30 420) rotate(-32) scale(0.5) translate(-300 60)', only='crown')
    b = glow_rings(500, 430, 300, '#B5506E', 3, .06) + ''.join(f'<path d="M{x} {y} l0 -{l}" stroke="#E3D3F0" stroke-width="5" opacity="0.5" />' for x, y, l in ((140, 420, 130), (250, 250, 110), (680, 520, 150), (740, 320, 120), (90, 640, 90), (330, 700, 80))) + tail + body + sash + crown
    write('nahusha-falling', b, 'Nahusha falling head down, his legs already a snake, his crown coming off.')


def pleading():
    body = rig('nahusha/humble.svg', 'translate(396 486) rotate(-20) scale(0.56) translate(-505 -800)', drop=('crown', 'dhoti', 'leg-far', 'leg-near', 'rear-drape', 'uttariya'))
    tail = snake(curve([(400, 500), (408, 550), (404, 620), (430, 700), (520, 742), (620, 700), (644, 610), (590, 548), (530, 570)]), 124, lambda t: 1 - .95 * t)
    sash = f'<g transform="translate(398 496) rotate(-18)"><path d="M-78 -24 Q0 -6 78 -24 L72 30 Q0 50 -72 30Z" fill="#5E3A9E" stroke="{INK}" stroke-width="5" /><path d="M-72 16 Q0 36 72 16" stroke="{GOLD}" stroke-width="8" /></g>'
    b = glow_rings(400, 400, 340, '#B5506E', 3, .06) + ''.join(f'<path d="M{x} {y} l0 -{l}" stroke="#E3D3F0" stroke-width="5" opacity="0.5" />' for x, y, l in ((90, 300, 130), (190, 640, 110), (690, 330, 150), (740, 560, 110), (120, 720, 90), (640, 160, 100))) + tail + body + sash
    write('nahusha-pleading', b, 'Nahusha, half snake, uncrowned, palms joined, begging as he falls (CE 3.178.38-39).')


def snake_character():
    """The snake as a speaking rig: head, eyes and mouth groups (assets/characters/SPEC.md). The canvas is taller than 1600 so the neck runs off the frame."""
    def face(x, y, s, rot, low):
        lid = f'<path d="M42 -38 Q78 -70 114 -38 Q80 -30 42 -38Z" fill="{YEL}" stroke="{INK}" stroke-width="5" />' if low else ''
        brow = f'<path d="M34 -64 Q78 -74 124 -34" stroke="{INK}" stroke-width="9" />' if low else f'<path d="M36 -56 Q80 -76 124 -44" stroke="{INK}" stroke-width="9" />'
        up_fangs = f'<path d="M96 40 L106 78 L120 42Z M142 42 L152 74 L164 40Z" fill="#FFF8E9" stroke="{INK}" stroke-width="4" />'
        jaw = f'<path d="M-130 20 Q-20 60 96 46 Q150 60 196 34 Q190 84 120 100 Q-10 118 -120 84 Q-168 60 -130 20Z" fill="{BELLY}" stroke="{INK}" stroke-width="6" />'
        return (f'<g id="head" transform="translate({x} {y}) rotate({rot}) scale({s})">'
                f'<g id="mouth-open" style="display:none"><path d="M170 60 Q236 84 276 72 M276 72 l32 -14 M276 72 l34 18" stroke="#B5243A" stroke-width="9" />'
                f'<g transform="translate(-120 40) rotate(10) translate(120 -40)">{jaw}</g><path d="M-100 22 Q40 64 190 28 Q168 110 96 128 Q0 124 -100 44Z" fill="#8E2A34" stroke="{INK}" stroke-width="4" />'
                f'<path d="M40 98 Q100 76 150 96 Q110 122 60 116Z" fill="#C9586A" /><path d="M96 122 L106 92 L118 122Z M130 112 L138 86 L148 106Z" fill="#FFF8E9" stroke="{INK}" stroke-width="4" />{up_fangs}</g>'
                f'<g id="mouth-closed"><g transform="translate(0 -22)">{jaw}</g><path d="M100 44 L106 62 L116 45Z M146 42 L152 58 L161 41Z" fill="#FFF8E9" stroke="{INK}" stroke-width="3" /></g>'
                f'<path d="M-130 -70 Q-20 -126 110 -84 Q196 -50 210 0 Q206 34 150 34 Q20 56 -126 36 Q-196 -20 -130 -70Z" fill="{YEL}" stroke="{INK}" stroke-width="6" />'
                f'<path d="M-130 -58 Q-20 -106 104 -70 Q170 -44 190 -8" stroke="{YEL_L}" stroke-width="10" /><path d="M-120 12 Q20 40 150 22 Q196 18 204 2" stroke="{YEL_D}" stroke-width="9" />'
                f'<path d="M-96 -44 Q-70 -78 -40 -50 Q-66 -22 -96 -44Z M-24 -70 Q6 -96 30 -66 Q4 -46 -24 -70Z M-80 -4 Q-58 -24 -36 -4 Q-58 12 -80 -4Z" fill="{SPOT}" stroke="{INK}" stroke-width="3" />'
                f'<g id="eyes-open"><ellipse cx="78" cy="-32" rx="33" ry="26" fill="#C92B2B" stroke="{INK}" stroke-width="6" /><ellipse cx="80" cy="-32" rx="23" ry="18" fill="#F0563A" /><ellipse cx="82" cy="-32" rx="7" ry="19" fill="{INK}" /><circle cx="72" cy="-40" r="5" fill="#FFF" />{lid}</g>'
                f'<g id="eyes-closed" style="display:none"><ellipse cx="78" cy="-32" rx="33" ry="26" fill="{YEL_D}" stroke="{INK}" stroke-width="5" /><path d="M46 -28 Q78 -10 110 -28" stroke="{INK}" stroke-width="6" /></g>'
                f'{brow}<ellipse cx="184" cy="-14" rx="6" ry="4" fill="{INK}" /></g>')
    out = 'assets/characters/nahusha-snake'
    os.makedirs(out, exist_ok=True)
    for pose, pts, hd, title in (
            ('rearing', [(80, 2840), (150, 2340), (120, 1840), (60, 1340), (90, 900), (190, 640), (350, 500)], (450, 480, 1.5, 4, False), 'rearing, speaking, weary'),
            ('bowed', [(80, 2840), (150, 2340), (120, 1840), (60, 1340), (90, 900), (200, 640), (360, 560)], (450, 590, 1.5, 22, True), 'head lowered, remorseful')):
        pts = [(x + 80, y) for x, y in pts]
        hd = (hd[0] + 80, *hd[1:])
        body = snake(curve(pts, 26), 240, lambda t: 1.1 - .2 * t)
        svg = (f'<svg xmlns="{SVG}" width="1000" height="2800" viewBox="0 0 1000 2800" fill="none" stroke-linecap="round" stroke-linejoin="round" data-character="nahusha-snake">'
               f'<title>Nahusha as the great snake · {title}</title><desc>S01E06, made by episodes/S01E06-nahusha-becomes-a-snake/svg/make-props.py.</desc>{body}{face(*hd)}</svg>')
        ET.fromstring(svg)
        open(f'{out}/{pose}.svg', 'w').write(svg)
        print('wrote', f'{out}/{pose}.svg')
    json.dump({'id': 'nahusha-snake', 'name': {'en': 'Nahusha (the great snake)', 'hi': 'नहुष (साँप)'}, 'role': 'Nahusha after the curse', 'divine': False, 'appearsIn': ['S01E06'],
               'look': 'Huge, spotted, turmeric-yellow, red-eyed, four fangs, no hood. Weary rather than fierce.', 'sourceNotes': 'CE 3.175.13-14.', 'poses': ['rearing', 'bowed'],
               'files': {'rearing': 'rearing.svg', 'bowed': 'bowed.svg'}, 'facing': 'right',
               'notes': 'A tall canvas (1000x2800, baseline still 1550): the neck runs off the bottom of the frame. The head is about 1070 canvas units above the baseline (bowed: 960).'},
              open(f'{out}/character.json', 'w'), ensure_ascii=False, indent=2)


def indra_lotus():
    b = glow_rings(400, 360, 360, '#FFE6A8', 5, .1)
    b += f'<path d="M400 640 Q386 720 400 800" stroke="{INK}" stroke-width="26" /><path d="M400 640 Q386 720 400 800" stroke="#4E7A4E" stroke-width="16" />'
    for a, l, c in ((-72, 300, '#D47A9E'), (72, 300, '#D47A9E'), (-44, 350, '#E89AB8'), (44, 350, '#E89AB8')):
        b += f'<g transform="translate(400 640) rotate({a})"><path d="M0 0 Q-92 {-l * .5:.0f} 0 {-l} Q92 {-l * .5:.0f} 0 0Z" fill="{c}" stroke="{INK}" stroke-width="5" /></g>'
    b += rig('indra/standing-blessing.svg', 'translate(168 110) scale(0.46 0.4)', fill='#FFE6A8', drop=('halo', 'leg-far', 'leg-near', 'dhoti'))
    for a, l, c in ((-20, 250, '#F2B8CF'), (20, 250, '#F2B8CF'), (0, 220, '#F8D0E0')):
        b += f'<g transform="translate(400 650) rotate({a})"><path d="M0 0 Q-96 {-l * .5:.0f} 0 {-l} Q96 {-l * .5:.0f} 0 0Z" fill="{c}" stroke="{INK}" stroke-width="5" opacity="0.97" /></g>'
    write('indra-in-lotus', b, 'Indra hidden in a lotus: a small glowing figure among the petals (CE 5.16.11-12: in a lotus stem).')


def dead_snake_sage():
    b = glow_rings(290, 420, 340, '#E07A2E', 3, .08)
    fig = rig('karna/guru-on-lap.svg', 'translate(-70 -250) scale(0.66)', fill=SIL)
    rim = rig('karna/guru-on-lap.svg', 'translate(-76 -256) scale(0.66)', fill='#E8B53A')
    jata = f'<path d="M236 400 Q212 470 240 560 L268 556 Q256 470 268 410Z M310 396 Q336 470 300 520 Q276 500 276 440Z" fill="{SIL}" />'
    b += rim + fig + jata
    b += f'<ellipse cx="242" cy="712" rx="140" ry="46" fill="{SIL}" />'  # no light between the legs
    pts = curve([(104, 664), (112, 600), (128, 532), (166, 472), (244, 432), (316, 440), (358, 500), (376, 596), (374, 650)])
    n = len(pts)
    d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
    b += f'<path d="{d}" stroke="{INK}" stroke-width="50" /><path d="{d}" stroke="#7E9A62" stroke-width="40" /><path d="{d}" stroke="#A9C086" stroke-width="8" transform="translate(0 -11)" />'
    b += ''.join(f'<ellipse cx="{pts[i][0]:.0f}" cy="{pts[i][1]:.0f}" rx="12" ry="9" fill="#4A5E36" />' for i in range(6, n - 6, 9))
    x, y = pts[-1]
    b += f'<g transform="translate({x:.0f} {y:.0f}) rotate(94)"><path d="M-20 -26 Q50 -44 92 -8 Q96 12 80 20 Q30 36 -20 26Z" fill="#7E9A62" stroke="{INK}" stroke-width="5" /><path d="M32 -10 Q44 -4 56 -12" stroke="{INK}" stroke-width="5" /></g>'
    write('dead-snake-sage', f'<g transform="translate(110 40)">{b}</g>', 'a sage in silent meditation, a dead snake laid over his shoulders (E07 tease).')


if __name__ == '__main__':
    great_snake(); coils(); snake_head(); eye(); eye(True); throne_icon(); palanquin_icon(); palanquin_carried(); foot_on_head(); strength_stream(); falling(); pleading(); snake_character(); indra_lotus(); dead_snake_sage()
