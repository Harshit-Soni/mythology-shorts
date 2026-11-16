"""S01E02 backgrounds, drawn in code in the library's flat style (see forest-hunt, cosmic-court).

himalaya-peaks   Shatashringa, "the mountain of a hundred peaks" (Adi §119): path at frame 0.80
spring-forest    spring in bloom, with the trees Adi §125 names: palasha, ashoka, mango, karnikara; feet at 0.86
amaravati-court  Indra's court (also for E03): classical Indian pillars and chaitya arch, a stage on the right; feet at 0.86

1296×2112 canvas (frame 1080×1920 + margins); layers layer-far / layer-mid / layer-ground.
Run from the repo root:  python3 episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py [out_dir]
"""
import math
import os
import random
import sys
import xml.etree.ElementTree as ET

OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/backgrounds'
W, H = 1296, 2112
INK = '#1E1420'


def fy(frac):
    """Frame fraction → canvas y."""
    return frac * 1920 + 96


def write(bid, defs, far, mid, ground, desc):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" '
           f'stroke-linecap="round" stroke-linejoin="round"><desc>S01E02 | {bid} | {desc} '
           f'Made by episodes/S01E02-kindama-curses-pandu/svg/make-backgrounds.py.</desc>'
           f'<defs>{defs}<clipPath id="canvas-clip"><rect width="{W}" height="{H}"/></clipPath></defs>'
           f'<g clip-path="url(#canvas-clip)"><g id="layer-far">{far}</g><g id="layer-mid">{mid}</g>'
           f'<g id="layer-ground">{ground}</g></g></svg>')
    ET.fromstring(svg)
    os.makedirs(OUT, exist_ok=True)
    with open(f'{OUT}/{bid}.svg', 'w') as f:
        f.write(svg)
    print('wrote', f'{OUT}/{bid}.svg')


def vgrad(gid, stops):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}" />' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient>'


def curl_cloud(x, y, s, fill, stroke=None, op=1):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ''
    circles = ''.join(f'<circle cx="{x + dx * s:.0f}" cy="{y + dy * s:.0f}" r="{r * s:.0f}" />'
                      for dx, dy, r in ((0, 0, 40), (45, -18, 50), (100, -8, 42), (140, 8, 32), (-38, 10, 30)))
    curls = ''.join(f'<path d="M{x + cx * s:.0f} {y + 6 * s:.0f} q{8 * s:.0f} -{14 * s:.0f} {18 * s:.0f} 0" stroke="{stroke or fill}" stroke-width="3" />'
                    for cx in (10, 70, 120)) if stroke else ''
    return f'<g fill="{fill}" opacity="{op}"{st}>{circles}</g>{curls}'


# ---------- 1. himalaya-peaks ----------
def himalaya():
    random.seed(11)
    defs = vgrad('hp-sky', ((0, '#B9CBE6'), (0.45, '#E8D8D0'), (0.75, '#F6DCC0'), (1, '#F3E6C8')))
    far = f'<rect width="{W}" height="{H}" fill="url(#hp-sky)" />'
    far += f'<circle cx="930" cy="760" r="120" fill="#FFF1D6" opacity="0.8" /><circle cx="930" cy="760" r="200" fill="#FFE9C4" opacity="0.25" />'
    # three bands of peaks (the hundred peaks), far to near
    for band, (base, hmin, hmax, fill, shade, n) in enumerate((
            (1150, 260, 520, '#DCE4F0', '#B9C6DC', 9), (1280, 220, 460, '#EEF2F8', '#AFC0D8', 8), (1420, 200, 380, '#F7F9FC', '#A3B6D2', 7))):
        x = -80
        pts = [f'-80 {base + 300}']
        peaks = ''
        while x < W + 80:
            w = random.randint(140, 220)
            h = random.randint(hmin, hmax)
            px = x + w / 2
            peaks += (f'<path d="M{x} {base} L{px:.0f} {base - h} L{x + w} {base}Z" fill="{fill}" stroke="{INK}" stroke-width="2.5" />'
                      f'<path d="M{px:.0f} {base - h} L{x + w} {base} L{px + w * 0.12:.0f} {base}Z" fill="{shade}" />'
                      f'<path d="M{px - w * 0.18:.0f} {base - h * 0.6:.0f} L{px:.0f} {base - h * 0.45:.0f} L{px + w * 0.2:.0f} {base - h * 0.62:.0f}" stroke="{shade}" stroke-width="5" />')
            x += w * 0.62
        far += peaks + f'<rect x="0" y="{base}" width="{W}" height="400" fill="{shade}" opacity="{0.6 - band * 0.1}" />'
    # mist and deodars on the mid slopes
    mid = ''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="40" fill="#FFFFFF" opacity="0.55" />'
                  for cx, cy, rx in ((300, 1400, 420), (1000, 1460, 380), (650, 1520, 500)))
    def deodar(x, y, s):
        tiers = ''.join(f'<path d="M{x - 70 * s + k * 9 * s:.0f} {y - k * 55 * s:.0f} L{x:.0f} {y - (k + 1.6) * 55 * s:.0f} L{x + 70 * s - k * 9 * s:.0f} {y - k * 55 * s:.0f}Z" '
                        f'fill="{"#2F5546" if k % 2 else "#3B6653"}" stroke="{INK}" stroke-width="2.5" />' for k in range(6))
        return f'<rect x="{x - 7 * s:.0f}" y="{y - 10:.0f}" width="{14 * s:.0f}" height="{40 * s:.0f}" fill="#5A3D2A" />{tiers}'
    for x, y, s in ((60, 1640, 1.3), (170, 1600, 1.0), (250, 1660, 1.15), (1080, 1620, 1.2), (1190, 1580, 1.0), (1250, 1660, 1.3)):
        mid += deodar(x, y, s)
    # rocky slope with a winding path (three tiny walkers go along it at frame 0.80 → canvas y 1632)
    g = fy(0.80)
    ground = (f'<path d="M0 {g - 40} Q300 {g - 90} 650 {g - 60} Q980 {g - 30} {W} {g - 80} L{W} {H} L0 {H}Z" fill="#8E8070" stroke="{INK}" stroke-width="3" />'
              f'<path d="M0 {g + 120} Q400 {g + 60} 700 {g + 90} Q1000 {g + 120} {W} {g + 60} L{W} {H} L0 {H}Z" fill="#7A6D60" />'
              f'<path d="M120 {H} Q380 {g + 200} 560 {g + 40} Q660 {g - 30} 900 {g - 50}" stroke="#CDBB9C" stroke-width="70" />'
              f'<path d="M120 {H} Q380 {g + 200} 560 {g + 40} Q660 {g - 30} 900 {g - 50}" stroke="#E2D3B6" stroke-width="30" opacity="0.7" />')
    for x, y, r in ((200, g + 30, 34), (980, g + 60, 40), (1160, g + 10, 28), (420, g + 260, 46), (900, g + 320, 52)):
        ground += (f'<path d="M{x - r} {y} Q{x - r * 0.6} {y - r} {x} {y - r * 1.1} Q{x + r * 0.8} {y - r * 0.8} {x + r} {y}Z" fill="#9C8E7D" stroke="{INK}" stroke-width="3" />'
                   f'<path d="M{x - r * 0.2} {y - r * 0.9} Q{x + r * 0.3} {y - r * 0.6} {x + r * 0.6} {y - r * 0.1}" stroke="#B9AC9A" stroke-width="5" />')
    write('himalaya-peaks', defs, far, mid, ground, 'Shatashringa: a sea of snowy peaks at dawn, deodars and mist, a rocky path (frame 0.80).')


# ---------- 2. spring-forest ----------
def spring():
    random.seed(7)
    defs = vgrad('sf-sky', ((0, '#E9A9B0'), (0.5, '#F4C7A6'), (1, '#F8DDB8')))
    far = f'<rect width="{W}" height="{H}" fill="url(#sf-sky)" />'
    far += f'<circle cx="420" cy="900" r="260" fill="#FFF0D0" opacity="0.35" />'
    far += f'<path d="M0 1380 Q320 1260 660 1330 Q980 1390 {W} 1300 L{W} 1600 L0 1600Z" fill="#C7A8B6" opacity="0.7" />'
    # a lotus pool at the back
    far += (f'<ellipse cx="760" cy="1430" rx="300" ry="54" fill="#9CC6D2" stroke="{INK}" stroke-width="3" />'
            f'<ellipse cx="760" cy="1424" rx="250" ry="30" fill="#B8DDE4" />')
    for x in (600, 700, 820, 900):
        far += (f'<ellipse cx="{x}" cy="1440" rx="26" ry="8" fill="#5C8A4A" />'
                f'<path d="M{x - 12} 1430 Q{x} 1400 {x + 12} 1430 Q{x} 1424 {x - 12} 1430Z" fill="#F2A7B8" stroke="{INK}" stroke-width="2" />')
    def tree(x, base, s, blossom, blossom_d, leaf, lean=0):
        trunk = (f'<path d="M{x - 26 * s} {base} Q{x - 12 * s + lean} {base - 300 * s} {x + lean} {base - 560 * s} '
                 f'Q{x + 18 * s + lean} {base - 300 * s} {x + 30 * s} {base}Z" fill="#5E3D2C" stroke="{INK}" stroke-width="3" />')
        branches = ''.join(f'<path d="M{x + lean * 0.8:.0f} {base - 400 * s:.0f} Q{x + dx * 0.6 * s:.0f} {base - (440 + dy * 0.5) * s:.0f} {x + dx * s:.0f} {base - (420 + dy) * s:.0f}" stroke="#5E3D2C" stroke-width="{14 * s:.0f}" />'
                           for dx, dy in ((-170, 160), (160, 140), (-60, 240), (90, 260)))
        canopy = ''.join(f'<ellipse cx="{x + dx * s:.0f}" cy="{base - (520 + dy) * s:.0f}" rx="{rx * s:.0f}" ry="{rx * 0.7 * s:.0f}" fill="{leaf}" stroke="{INK}" stroke-width="3" />'
                         for dx, dy, rx in ((-170, 60, 120), (150, 50, 130), (-40, 160, 150), (90, 190, 120), (0, 30, 110)))
        flowers = ''
        for _ in range(int(60 * s)):
            a = random.uniform(0, 2 * math.pi); rr = random.uniform(0, 1)
            fx = x + math.cos(a) * 230 * s * rr
            fyy = base - (580 + 110 * math.sin(a) * rr) * s
            c = blossom if random.random() > 0.3 else blossom_d
            flowers += f'<circle cx="{fx:.0f}" cy="{fyy:.0f}" r="{random.uniform(9, 16) * s:.0f}" fill="{c}" stroke="{INK}" stroke-width="1.5" />'
        return trunk + branches + canopy + flowers
    mid = ''
    # palasha (flame of the forest): sparse dark leaves, flame-orange flowers; ashoka: red clusters on green;
    # karnikara: yellow; mango blossom: cream sprays
    mid += tree(110, 1560, 1.25, '#F06A1E', '#C8452A', '#4A5A3A', lean=20)
    mid += tree(1180, 1540, 1.2, '#E8B53A', '#F4D17B', '#4E7A48', lean=-20)
    mid += tree(430, 1420, 0.75, '#D2382E', '#F06A1E', '#5C8A4A')
    mid += tree(950, 1430, 0.7, '#FFF1D6', '#F6E3C5', '#6B9455')
    # petals in the air
    for _ in range(60):
        x, y = random.uniform(0, W), random.uniform(300, 1500)
        mid += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="9" ry="5" transform="rotate({random.uniform(0, 180):.0f} {x:.0f} {y:.0f})" fill="{random.choice(("#F6C1D0", "#F2A7B8", "#F06A1E", "#F4D17B"))}" />'
    g = fy(0.86)
    ground = (f'<path d="M0 1500 Q400 1460 760 1490 Q1050 1510 {W} 1470 L{W} {H} L0 {H}Z" fill="#8FAF6A" stroke="{INK}" stroke-width="3" />'
              f'<path d="M0 1700 Q500 1660 900 1700 Q1100 1720 {W} 1690 L{W} {H} L0 {H}Z" fill="#7FA05C" />'
              f'<ellipse cx="648" cy="{g + 20:.0f}" rx="460" ry="60" fill="#9DBC78" opacity="0.7" />')
    for _ in range(70):
        x, y = random.uniform(0, W), random.uniform(1520, H - 40)
        ground += f'<path d="M{x:.0f} {y:.0f} q6 -26 18 -34 M{x + 8:.0f} {y:.0f} q2 -20 -8 -30" stroke="#5C8A4A" stroke-width="5" />'
    for _ in range(40):
        x, y = random.uniform(0, W), random.uniform(1520, H - 40)
        ground += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="9" ry="5" fill="{random.choice(("#F6C1D0", "#F06A1E", "#F4D17B"))}" />'
    write('spring-forest', defs, far, mid, ground, 'spring in full bloom: palasha, ashoka, karnikara and mango blossom, a lotus pool, petals in the air; meadow (feet at frame 0.86).')


# ---------- 3. amaravati-court ----------
def amaravati():
    random.seed(3)
    defs = (vgrad('ac-sky', ((0, '#151433'), (0.6, '#2B2560'), (1, '#4A3A7A')))
            + vgrad('ac-floor', ((0, '#8C7FB0'), (1, '#4A3A7A'))))
    far = f'<rect width="{W}" height="{H}" fill="url(#ac-sky)" />'
    for _ in range(90):
        x, y = random.uniform(0, W), random.uniform(0, 1100)
        far += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice((2, 2, 3, 4))}" fill="#FFF1D6" opacity="{random.uniform(0.5, 1):.2f}" />'
    for x, y, s in ((120, 1050, 1.6), (900, 980, 1.4), (500, 1150, 1.2), (1150, 1180, 1.3)):
        far += curl_cloud(x, y, s, '#6E5A9E', '#3B2D6B', 0.9)
    # far back: nagara spires and a chaitya arch over a small gold throne
    for x, h in ((300, 520), (648, 640), (996, 520)):
        far += (f'<path d="M{x - 90} 1230 Q{x - 80} {1230 - h * 0.7} {x} {1230 - h} Q{x + 80} {1230 - h * 0.7} {x + 90} 1230Z" fill="#3E3470" stroke="{INK}" stroke-width="3" />'
                f'<circle cx="{x}" cy="{1230 - h - 14}" r="16" fill="#E8B53A" stroke="{INK}" stroke-width="3" />'
                + ''.join(f'<path d="M{x - 80 + k * 6} {1230 - k * h * 0.14:.0f} H{x + 80 - k * 6}" stroke="#57498F" stroke-width="5" />' for k in range(1, 6)))
    far += (f'<path d="M520 1300 V1020 Q520 880 648 860 Q776 880 776 1020 V1300Z" fill="#2B2350" stroke="#E8B53A" stroke-width="10" />'
            f'<path d="M560 1300 V1040 Q560 920 648 905 Q736 920 736 1040 V1300Z" fill="#1E1840" />'
            f'<path d="M600 1250 V1120 Q600 1080 648 1074 Q696 1080 696 1120 V1250Z" fill="#E8B53A" stroke="{INK}" stroke-width="3" />'
            f'<rect x="590" y="1240" width="116" height="26" fill="#B8862A" stroke="{INK}" stroke-width="3" />'
            f'<circle cx="648" cy="1010" r="70" fill="#FFE6B0" opacity="0.25" />')
    # rows of white-and-gold carved pillars, receding (classical: base, banded shaft, bracket capital; no onion domes)
    def pillar(x, top, bot, w):
        bands = ''.join(f'<rect x="{x - w / 2:.0f}" y="{top + (bot - top) * k:.0f}" width="{w:.0f}" height="{w * 0.16:.0f}" fill="#E8B53A" stroke="{INK}" stroke-width="2" />'
                        for k in (0.22, 0.5, 0.78))
        return (f'<rect x="{x - w / 2:.0f}" y="{top:.0f}" width="{w:.0f}" height="{bot - top:.0f}" fill="#F3EEDF" stroke="{INK}" stroke-width="3" />'
                f'<rect x="{x - w / 2 + w * 0.6:.0f}" y="{top:.0f}" width="{w * 0.4:.0f}" height="{bot - top:.0f}" fill="#D6CDE0" />'
                + bands
                + f'<path d="M{x - w * 0.9:.0f} {top} L{x + w * 0.9:.0f} {top} L{x + w * 0.6:.0f} {top + w * 0.5:.0f} L{x - w * 0.6:.0f} {top + w * 0.5:.0f}Z" fill="#E8B53A" stroke="{INK}" stroke-width="3" />'
                + f'<rect x="{x - w * 0.75:.0f}" y="{bot - w * 0.3:.0f}" width="{w * 1.5:.0f}" height="{w * 0.3:.0f}" fill="#E8B53A" stroke="{INK}" stroke-width="3" />')
    mid = ''
    for k, (dx, top, bot, w) in enumerate(((330, 980, 1330, 34), (240, 860, 1400, 48), (130, 700, 1500, 66), (10, 480, 1640, 92))):
        mid += pillar(648 - dx - 60 * k, top, bot, w) + pillar(648 + dx + 60 * k, top, bot, w)
    mid += f'<path d="M0 470 H{W} V520 H0Z" fill="#E8B53A" stroke="{INK}" stroke-width="3" />'
    mid += ''.join(f'<path d="M{x} 520 l18 26 l18 -26" fill="#B8862A" stroke="{INK}" stroke-width="2" />' for x in range(0, W, 36))
    # the dancer's stage on the right
    mid += (f'<path d="M760 1500 H1296 V1600 H700Z" fill="#E6DCC6" stroke="{INK}" stroke-width="3" />'
            f'<path d="M700 1600 H1296 V1630 H690Z" fill="#E8B53A" stroke="{INK}" stroke-width="3" />'
            f'<path d="M790 1520 H1260" stroke="#F4D17B" stroke-width="4" />')
    g = fy(0.86)
    ground = (f'<path d="M0 1560 H{W} V{H} H0Z" fill="url(#ac-floor)" />'
              f'<path d="M0 1560 H{W}" stroke="{INK}" stroke-width="3" />'
              f'<path d="M0 1590 H{W}" stroke="#E8B53A" stroke-width="8" />'
              f'<path d="M0 1604 H{W}" stroke="#B8862A" stroke-width="3" />'
              + ''.join(f'<path d="M0 {y} H{W}" stroke="#7E70A8" stroke-width="3" opacity="0.6" />' for y in (1700, 1830, 1990))
              + f'<path d="M560 1604 L520 {H} H776 L736 1604Z" fill="#8E2A20" opacity="0.85" />'
              + f'<path d="M560 1604 L520 {H} M736 1604 L776 {H}" stroke="#E8B53A" stroke-width="6" />'
              + f'<ellipse cx="648" cy="1680" rx="300" ry="30" fill="#FFE6B0" opacity="0.12" />'
              + curl_cloud(80, H - 80, 1.8, '#8C7FB0', '#4A3A7A', 0.8) + curl_cloud(1050, H - 60, 1.6, '#8C7FB0', '#4A3A7A', 0.8))
    write('amaravati-court', defs, far, mid, ground, "Indra's court: night sky, nagara spires, a chaitya arch over a far gold throne, rows of white-and-gold pillars, a stage on the right; floor (feet at frame 0.86).")


if __name__ == '__main__':
    himalaya(); spring(); amaravati()
