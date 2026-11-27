"""S03E01 props, drawn in code in the library's flat style. Crowds are library poses drawn as silhouettes (the S01E08
fig() helper), so they match the cast.

chiranjeevi-seal  the series mark: an undying lamp (diya) in a gold seal ring, for the sting
katha-circle      a storyteller and listeners round a lamp at night (Hanuman is added in the scene as a character)
still-world       the moment the wind stopped: a limp banner, birds hanging in the air, a deer frozen, leaves stuck mid-fall
vanara-crowd      monkeys and people gathered, following Rama
rama-necklace     Rama's moon-bright necklace with a beryl (vaidurya) pendant (CE 7.39.20)
three-steps       next episode: King Bali, a small figure with an umbrella (Vamana), three glowing footprints
Run from the repo root (after make-cast.py):  python3 episodes/S03E01-hanuman-never-died/svg/make-props.py
"""
import importlib.util
import math
import random
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
def load(n, p):
    spec = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
P8 = load('p08', 'episodes/S01E08-gandhari-curses-krishna/svg/make-props.py')
sys.argv = _argv
SVG, INK, GOLD, GOLD_L, GOLD_D = P8.SVG, P8.INK, P8.GOLD, P8.GOLD_L, P8.GOLD_D
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/props'
fig, glow = P8.fig, P8.glow
EP = 'S03E01-hanuman-never-died'


def write(pid, body, desc, w=800, h=800):
    svg = (f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
           f'<desc>S03E01 | {pid} | {desc} Made by episodes/{EP}/svg/make-props.py.</desc>{body}</svg>')
    ET.fromstring(svg)
    open(f'{OUT}/{pid}.svg', 'w').write(svg)
    print('wrote', f'{OUT}/{pid}.svg')


def diya(cx, cy, s=1.0, flame=True):
    """A clay oil lamp with a tall flame."""
    out = (f'<path d="M{cx - 90 * s:.0f} {cy:.0f} Q{cx} {cy + 90 * s:.0f} {cx + 90 * s:.0f} {cy:.0f} L{cx + 120 * s:.0f} {cy - 22 * s:.0f} Q{cx + 40 * s:.0f} {cy - 6 * s:.0f} {cx - 90 * s:.0f} {cy:.0f}Z" fill="#B4643A" stroke="{INK}" stroke-width="{6 * s:.1f}" />'
           f'<path d="M{cx - 70 * s:.0f} {cy + 10 * s:.0f} Q{cx} {cy + 60 * s:.0f} {cx + 70 * s:.0f} {cy + 10 * s:.0f}" stroke="#D8884E" stroke-width="{6 * s:.1f}" />')
    if flame:
        fx, fy_ = cx + 92 * s, cy - 24 * s
        out = (glow(fx, fy_ - 60 * s, 200 * s, '#FFD27A', 4, .12)
               + out
               + f'<path d="M{fx:.0f} {fy_:.0f} Q{fx - 46 * s:.0f} {fy_ - 70 * s:.0f} {fx + 4 * s:.0f} {fy_ - 160 * s:.0f} Q{fx + 44 * s:.0f} {fy_ - 70 * s:.0f} {fx:.0f} {fy_:.0f}Z" fill="#F7A23A" stroke="{INK}" stroke-width="{5 * s:.1f}" />'
               + f'<path d="M{fx:.0f} {fy_ - 8 * s:.0f} Q{fx - 20 * s:.0f} {fy_ - 50 * s:.0f} {fx + 2 * s:.0f} {fy_ - 100 * s:.0f} Q{fx + 20 * s:.0f} {fy_ - 50 * s:.0f} {fx:.0f} {fy_ - 8 * s:.0f}Z" fill="#FFE9A8" />')
    return out


def chiranjeevi_seal():
    b = glow(400, 400, 360, '#FFE6B0', 3, .1)
    b += f'<circle cx="400" cy="400" r="300" fill="#F4E4C0" stroke="{INK}" stroke-width="10" /><circle cx="400" cy="400" r="300" stroke="{GOLD}" stroke-width="26" /><circle cx="400" cy="400" r="262" stroke="{GOLD_D}" stroke-width="5" />'
    # an endless knot of small leaves round the ring: never-ending
    b += ''.join(f'<path d="M400 112 q14 -18 0 -36 q-14 18 0 36Z" fill="{GOLD_D}" transform="rotate({a} 400 400)" />' for a in range(0, 360, 15))
    b += diya(370, 520, 1.25)
    write('chiranjeevi-seal', b, 'The Chiranjeevi series mark: an undying oil lamp inside a gold seal ring with a ring of small leaves.')


def katha_circle():
    W, H = 1100, 800
    b = glow(560, 520, 420, '#FFB45A', 4, .10)
    dark, rim = '#2A1C16', '#E8853A'
    # the storyteller, seated, one hand raised (the gentle sage, mirrored to face the listeners), and the listeners round the lamp
    b += fig('shamika/gentle.svg', 820, 690, 0.36, dark, flip=True, rim=rim)
    for path, x, base, s, flip in (('shamika/seated-silent.svg', 330, 720, 0.33, False), ('kunti/standing-sad.svg', 470, 740, 0.30, False),
                                   ('shamika/seated-silent.svg', 220, 760, 0.36, False), ('homa-brahmin/standing-grief.svg', 640, 760, 0.30, False)):
        b += fig(path, x, base, s, dark, flip=flip, rim=rim)
    b += diya(560, 720, 0.55)
    write('katha-circle', b, 'Night: a storyteller with a hand raised and listeners in silhouette round an oil lamp, rimmed in its light.', W, H)


def still_world():
    W, H = 1100, 800
    random.seed(4)
    b = ''
    # a banner hanging dead straight from its pole
    b += (f'<path d="M180 760 L180 160" stroke="{INK}" stroke-width="14" /><path d="M180 760 L180 160" stroke="#7A5634" stroke-width="8" />'
          f'<path d="M186 170 L270 170 L262 420 L230 390 L196 430Z" fill="#C9463A" stroke="{INK}" stroke-width="5" /><circle cx="180" cy="156" r="10" fill="{GOLD}" stroke="{INK}" stroke-width="3" />')
    # birds stopped mid-air, wings frozen; a faint ring round each to say "held"
    for x, y, s in ((520, 200, 1.0), (640, 150, 0.8), (760, 230, 0.9), (880, 170, 0.7)):
        b += (f'<circle cx="{x}" cy="{y}" r="{46 * s:.0f}" stroke="#F4EBD8" stroke-width="3" stroke-dasharray="6 10" opacity="0.8" />'
              f'<path d="M{x - 34 * s:.0f} {y + 6 * s:.0f} Q{x - 14 * s:.0f} {y - 20 * s:.0f} {x} {y} Q{x + 14 * s:.0f} {y - 20 * s:.0f} {x + 34 * s:.0f} {y + 6 * s:.0f}" stroke="{INK}" stroke-width="{7 * s:.1f}" />')
    # leaves stopped in mid-fall
    for _ in range(9):
        x, y = random.uniform(380, 1040), random.uniform(320, 560)
        b += f'<path d="M{x:.0f} {y:.0f} q14 -16 28 0 q-14 16 -28 0Z" fill="#7E9A4A" stroke="{INK}" stroke-width="3" transform="rotate({random.uniform(0, 180):.0f} {x + 14:.0f} {y:.0f})" />'
    # a deer standing frozen, head up
    b += (f'<g transform="translate(700 520)"><path d="M0 0 Q60 -30 150 -10 Q190 0 196 40 L180 220 L166 220 L170 80 Q120 90 60 80 L50 220 L36 220 L30 70 Q-10 60 -20 20 Z" fill="#B07A4A" stroke="{INK}" stroke-width="5" />'
          f'<path d="M150 -10 Q170 -80 200 -110 L226 -100 Q210 -60 196 -4Z" fill="#B07A4A" stroke="{INK}" stroke-width="5" /><circle cx="214" cy="-96" r="5" fill="{INK}" />'
          f'<path d="M206 -112 l-10 -40 m4 16 l-16 -12 M218 -112 l8 -40 m-4 16 l14 -14" stroke="#6E4A2E" stroke-width="6" /></g>')
    write('still-world', b, 'The moment the wind stopped: a banner hanging straight, birds held still in the air, leaves stopped mid-fall, a frozen deer.', W, H)


def vanara_crowd():
    W, H = 1200, 800
    random.seed(9)
    b = ''
    people = ['hanuman/standing__devoted.svg', 'hanuman/standing.svg', 'king/folded-hands.svg', 'kunti/folded-hands.svg', 'hanuman/standing.svg', 'guard/pointing.svg']
    fills = ['#7A4A2A', '#8E5A34', '#5E3E2A', '#6E4A30']
    for row, (base, s) in enumerate(((560, 0.26), (660, 0.30), (780, 0.34))):
        x = 60 + row * 30
        while x < W - 40:
            b += fig(random.choice(people), x, base, s * random.uniform(.92, 1.06), fills[(row + int(x)) % 4], flip=random.random() < .2, rim='#F6C890')
            x += random.uniform(120, 170)
    write('vanara-crowd', b, 'A crowd of monkeys (tails up) and people in silhouette, rimmed in dawn light, all facing right: following Rama.', W, H)


def rama_necklace():
    b = glow(400, 420, 300, '#FFF1C8', 3, .14)
    # pearls hanging in a U from the two shoulders down to the pendant
    b += ''.join(f'<circle cx="{400 + 250 * math.sin(a / 30):.0f}" cy="{500 - 200 * math.cos(a / 30):.0f}" r="18" fill="#F7F2E6" stroke="{INK}" stroke-width="4" />' for a in range(-40, 41, 5))
    b += (f'<path d="M400 560 L460 620 L400 720 L340 620Z" fill="{GOLD}" stroke="{INK}" stroke-width="6" />'
          f'<ellipse cx="400" cy="630" rx="34" ry="44" fill="#3E9A86" stroke="{INK}" stroke-width="5" /><ellipse cx="390" cy="614" rx="10" ry="14" fill="#BFEFE0" />')
    write('rama-necklace', b, "Rama's necklace: a moon-white string of pearls with a gold pendant set with a green beryl (vaidurya), glowing.")


def three_steps():
    W, H = 1000, 800
    b = glow(500, 360, 440, '#FFE6B0', 3, .08)
    # the king, tall, on the right, and the small figure with an umbrella on the left (silhouettes: next time's story)
    b += fig('king/folded-hands.svg', 760, 640, 0.42, '#3A2A3E', flip=True, rim='#F6C890')
    b += fig('shamika/gentle.svg', 300, 640, 0.22, '#3A2A3E', rim='#F6C890')
    b += (f'<path d="M300 262 L300 470" stroke="{INK}" stroke-width="8" /><path d="M220 290 Q300 220 380 290Z" fill="#E8B53A" stroke="{INK}" stroke-width="6" />')
    # three glowing footprints rising in an arc: earth, sky, and the last one
    for k, (x, y, r) in enumerate(((420, 720, 0), (520, 470, -20), (640, 220, -40))):
        b += glow(x, y, 90, '#FFD27A', 3, .18)
        b += (f'<g transform="translate({x} {y}) rotate({r})"><path d="M-26 40 Q-34 -10 -14 -40 Q6 -60 22 -36 Q34 -6 22 40 Q0 56 -26 40Z" fill="{GOLD}" stroke="{INK}" stroke-width="5" />'
              + ''.join(f'<circle cx="{dx}" cy="{dy}" r="{rr}" fill="{GOLD}" stroke="{INK}" stroke-width="3" />' for dx, dy, rr in ((-20, -58, 9), (-4, -66, 8), (12, -62, 7), (24, -52, 6), (32, -40, 5)))
              + '</g>')
    write('three-steps', b, 'Next episode: King Bali (silhouette) facing a small figure with an umbrella (Vamana), and three glowing footprints rising in an arc.', W, H)


if __name__ == '__main__':
    chiranjeevi_seal(); katha_circle(); still_world(); vanara_crowd(); rama_necklace(); three_steps()
