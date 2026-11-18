"""S01E04 props, drawn in code in the library's flat style (reuses the S01E02/E03 helpers).

Run from the repo root:  python3 episodes/S01E04-amba-vow-bhishma/svg/make-props.py [out_dir]
Writes assets/props/<id>.svg (800×800). Flat fills, outline #1E1420, no filters/text/images.
"""
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
glow_rings, person = P.glow_rings, P.person


def write(pid, body, desc, w=800, h=800):
    os.makedirs(OUT, exist_ok=True)
    svg = (f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" '
           f'stroke-linecap="round" stroke-linejoin="round"><desc>S01E04 | {pid} | {desc} '
           f'Made by episodes/S01E04-amba-vow-bhishma/svg/make-props.py.</desc>{body}</svg>')
    ET.fromstring(svg)
    with open(f'{OUT}/{pid}.svg', 'w') as f:
        f.write(svg)
    print('wrote', f'{OUT}/{pid}.svg')


def woman(x, base, h, fill=SIL, rim=None, op=1):
    """A modest standing woman in silhouette: head with a braid, a long skirt."""
    u = h / 10
    hy = base - h + u * 0.9
    parts = (f'<circle cx="{x}" cy="{hy:.0f}" r="{u * 0.72:.0f}" />'
             f'<path d="M{x - u * 0.5:.0f} {hy + u * 0.2:.0f} Q{x - u * 0.9:.0f} {hy + u * 2.2:.0f} {x - u * 0.5:.0f} {hy + u * 3.6:.0f}" stroke="{fill}" stroke-width="{u * 0.35:.0f}" />'
             f'<path d="M{x - u * 1.0:.0f} {hy + u * 1.1:.0f} Q{x:.0f} {hy + u * 0.7:.0f} {x + u * 1.0:.0f} {hy + u * 1.1:.0f} L{x + u * 0.8:.0f} {base - u * 4.6:.0f} L{x - u * 0.8:.0f} {base - u * 4.6:.0f}Z" />'
             f'<path d="M{x - u * 0.85:.0f} {base - u * 4.7:.0f} L{x + u * 0.85:.0f} {base - u * 4.7:.0f} L{x + u * 1.3:.0f} {base:.0f} L{x - u * 1.3:.0f} {base:.0f}Z" />')
    g = f'<g fill="{fill}" opacity="{op}">{parts}</g>'
    if rim:
        g = f'<g transform="translate(-3 -3)" fill="{rim}" opacity="0.85">{parts}</g>' + g
    return g


# 1. Amba's two sisters, Ambika and Ambalika, as silhouettes behind her (the swayamvara)
def three_princesses():
    body = glow_rings(400, 420, 320, '#F2A7B8', 3, 0.08)
    body += woman(300, 740, 520, rim='#F2A7B8', op=0.9) + woman(500, 750, 540, rim='#F2A7B8', op=0.9)
    write('three-princesses', body, "Amba's sisters Ambika and Ambalika as two modest silhouettes with a pink rim (Amba herself is the lit character in front).")


# 2. a closed palace gate (her father's; Hastinapura's)
def closed_gate():
    body = (f'<path d="M180 760 L180 260 Q400 120 620 260 L620 760Z" fill="#6E4A34" stroke="{INK}" stroke-width="6" />'
            f'<path d="M220 760 L220 290 Q400 170 580 290 L580 760Z" fill="#8E5A36" stroke="{INK}" stroke-width="4" />'
            f'<path d="M400 190 L400 760" stroke="{INK}" stroke-width="6" />'
            + ''.join(f'<circle cx="{x}" cy="{y}" r="11" fill="{GOLD}" stroke="{INK}" stroke-width="2" />' for x in (270, 330, 470, 530) for y in (360, 470, 580, 690))
            + f'<rect x="372" y="470" width="56" height="70" rx="8" fill="{GOLD_D}" stroke="{INK}" stroke-width="4" />'
            + f'<path d="M130 260 L670 260 L640 220 L160 220Z" fill="#B8862A" stroke="{INK}" stroke-width="4" />')
    write('closed-gate', body, 'a closed wooden palace gate with gold studs and a bar.')


# 3. the crooked river (Ganga's curse): a dry, winding riverbed that glows as the curse lands
def crooked_river():
    """A dry riverbed receding into the distance: wide at the front, narrowing as it winds away (perspective), so it
    reads as a river and not a snake. Cracked sand, a thin thread of water, banks of dry grass."""
    # centre line from the front (bottom) to the horizon (top), with a half-width that shrinks with distance
    pts = [(400 + 190 * math.sin(t * 8.5) * (1 - t * 0.55), 790 - t * 540, 120 * (1 - t) + 12) for t in [i / 60 for i in range(61)]]
    left = ' L'.join(f'{x - w:.0f} {y:.0f}' for x, y, w in pts)
    right = ' L'.join(f'{x + w:.0f} {y:.0f}' for x, y, w in reversed(pts))
    bed = f'M{left} L{right}Z'
    water = 'M' + ' L'.join(f'{x + w * 0.15 * math.sin(i):.0f} {y:.0f}' for i, (x, y, w) in enumerate(pts))
    random.seed(4)
    cracks = ''
    for x, y, w in pts[:40:5]:
        for _ in range(3):
            cx, cy = x + random.uniform(-w * 0.8, w * 0.8), y + random.uniform(-10, 10)
            cracks += f'<path d="M{cx:.0f} {cy:.0f} l{random.uniform(-w * 0.2, w * 0.2):.0f} {random.uniform(-8, 8):.0f} l{random.uniform(-w * 0.2, w * 0.2):.0f} {random.uniform(-6, 6):.0f}" stroke="#8E7258" stroke-width="3" />'
    banks = ''.join(f'<path d="M{x - w - 10:.0f} {y:.0f} q-8 -{14 + w * 0.08:.0f} 4 -{22 + w * 0.12:.0f} M{x + w + 10:.0f} {y:.0f} q8 -{14 + w * 0.08:.0f} -4 -{22 + w * 0.12:.0f}" stroke="#A8925A" stroke-width="4" />'
                    for x, y, w in pts[::6])
    body = (glow_rings(400, 520, 330, '#E8B53A', 3, 0.08)
            + f'<path d="{bed}" fill="#C9A986" stroke="#6E5440" stroke-width="5" />'
            + f'<path d="{bed}" fill="#E0C29A" opacity="0.5" transform="translate(0 -6)" />'
            + cracks + banks
            + f'<path d="{water}" stroke="#9FD3E6" stroke-width="7" opacity="0.9" />')
    write('crooked-river', body, 'a dry, winding riverbed receding into the distance, cracked sand and a thread of water: the crooked river of Ganga\'s curse.')


# 4. Shiva as a symbol only: a column of light, the trishula and the crescent moon
def shiva_light():
    body = glow_rings(400, 400, 380, '#FFE6B0', 5, 0.1)
    body += f'<path d="M340 800 L370 40 L430 40 L460 800Z" fill="#FFF1D6" opacity="0.35" />'
    tri = (f'<path d="M400 640 L400 210" stroke="{INK}" stroke-width="18" /><path d="M400 640 L400 210" stroke="{GOLD}" stroke-width="10" />'
           f'<path d="M330 200 Q330 290 400 300 Q470 290 470 200" stroke="{INK}" stroke-width="18" /><path d="M330 200 Q330 290 400 300 Q470 290 470 200" stroke="{GOLD}" stroke-width="10" />'
           f'<path d="M330 200 L318 150 L344 180Z M470 200 L482 150 L456 180Z M400 210 L384 140 L400 110 L416 140Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" />'
           f'<ellipse cx="400" cy="330" rx="26" ry="16" fill="#C9CED6" stroke="{INK}" stroke-width="3" />')
    moon = f'<path d="M520 150 A70 70 0 1 0 600 250 A56 56 0 1 1 520 150Z" fill="#FFF8E9" stroke="{INK}" stroke-width="4" />'
    write('shiva-light', body + tri + moon, 'Shiva as a symbol only: a column of light, the gold trishula with its damaru, and the crescent moon.')


# 5. the bed of arrows: old Bhishma lying on arrow shafts, held above the ground; no wounds
def bed_of_arrows():
    random.seed(8)
    shafts = ''
    for x in range(140, 690, 22):
        h = random.uniform(150, 200)
        a = random.uniform(-8, 8)
        shafts += (f'<g transform="rotate({a:.0f} {x} 620)"><path d="M{x} 620 L{x} {620 - h:.0f}" stroke="#6E4228" stroke-width="7" />'
                   f'<path d="M{x - 9} {620 - h + 10:.0f} L{x} {620 - h - 14:.0f} L{x + 9} {620 - h + 10:.0f}" fill="#E8B53A" stroke="{INK}" stroke-width="2" /></g>')
    ground = f'<path d="M60 640 Q400 600 740 640 L740 700 L60 700Z" fill="#7A4E34" opacity="0.7" />'
    y = 440  # the body lies along y≈440, head at the left
    figure = (f'<path d="M190 {y - 20} Q330 {y - 46} 470 {y - 30} L640 {y - 10} Q680 {y} 660 {y + 18} L470 {y + 30} Q330 {y + 40} 190 {y + 30}Z" fill="#FBF6EA" stroke="{INK}" stroke-width="4" />'
              f'<path d="M260 {y - 34} Q300 {y + 6} 340 {y - 36}" stroke="#3E6FA8" stroke-width="16" />'
              f'<circle cx="150" cy="{y - 12}" r="44" fill="#EBC9A0" stroke="{INK}" stroke-width="4" />'
              f'<path d="M112 {y - 50} Q150 {y - 72} 196 {y - 46} L196 {y - 30} L112 {y - 30}Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
              f'<path d="M150 {y + 28} Q180 {y + 74} 236 {y + 40} Q200 {y + 26} 182 {y + 14}Z" fill="#F3EEDF" stroke="{INK}" stroke-width="3" />'
              f'<path d="M118 {y - 26} Q100 {y + 10} 116 {y + 40}" stroke="#EEE8DE" stroke-width="12" />'
              f'<path d="M140 {y - 18} Q150 {y - 12} 162 {y - 18}" stroke="{INK}" stroke-width="3" />'
              f'<path d="M660 {y + 4} Q700 {y - 6} 720 {y + 12}" stroke="#EBC9A0" stroke-width="22" />')
    body = glow_rings(400, 440, 340, '#FFD1A0', 3, 0.08) + ground + shafts + figure
    write('bed-of-arrows', body, 'old Bhishma lying on a bed of arrow shafts, held above the ground, eyes closed, at peace; no wounds shown.')


# 6. the eight Vasus as lights in a ring
def vasu_lights():
    body = glow_rings(400, 400, 360, '#FFE6B0', 3, 0.08)
    for i in range(8):
        a = math.radians(i * 45 - 90)
        x, y = 400 + 250 * math.cos(a), 400 + 250 * math.sin(a)
        body += (glow_rings(round(x), round(y), 70, '#FFF1D6', 3, 0.18)
                 + f'<circle cx="{x:.0f}" cy="{y:.0f}" r="26" fill="#FFF8E9" stroke="{GOLD}" stroke-width="5" />'
                 + f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="{GOLD}" />')
    write('vasu-lights', body, 'the eight Vasus as eight lights in a ring.')


# 7. Karna (E05 tease): a silhouette with the golden armour and earrings catching the sun
def karna_silhouette():
    body = glow_rings(400, 330, 300, '#E8B53A', 4, 0.12)
    body += f'<circle cx="400" cy="300" r="170" fill="#E8B53A" opacity="0.35" />'
    body += person(400, 780, 640, rim='#E8B53A', robe=False, hair='knot')
    u = 64
    hy = 780 - 640 + u * 0.9
    body += (f'<path d="M{400 - u * 1.05:.0f} {hy + u * 1.2:.0f} Q400 {hy + u * 0.8:.0f} {400 + u * 1.05:.0f} {hy + u * 1.2:.0f} L{400 + u * 0.85:.0f} {hy + u * 3.4:.0f} L{400 - u * 0.85:.0f} {hy + u * 3.4:.0f}Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" opacity="0.95" />'
             + ''.join(f'<path d="M{400 - u * 0.8:.0f} {hy + u * (1.6 + k * 0.45):.0f} L{400 + u * 0.8:.0f} {hy + u * (1.6 + k * 0.45):.0f}" stroke="{GOLD_D}" stroke-width="5" />' for k in range(4))
             + f'<circle cx="{400 - u * 0.7:.0f}" cy="{hy + u * 0.3:.0f}" r="14" fill="{GOLD}" stroke="{INK}" stroke-width="2" />'
             + f'<circle cx="{400 + u * 0.7:.0f}" cy="{hy + u * 0.3:.0f}" r="14" fill="{GOLD}" stroke="{INK}" stroke-width="2" />'
             + f'<path d="M560 180 Q680 440 560 700" stroke="{SIL}" stroke-width="14" />')
    write('karna-silhouette', body, 'Karna as a silhouette against the sun, his golden armour and earrings catching the light, a bow (E05 tease).')


if __name__ == '__main__':
    three_princesses(); closed_gate(); crooked_river(); shiva_light(); bed_of_arrows(); vasu_lights(); karna_silhouette()
