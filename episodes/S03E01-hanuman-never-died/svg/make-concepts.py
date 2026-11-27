"""S03E01 concept check: three looks each for Hanuman and Rama, the first figures of the Ramayana on the channel.
Made from the library rigs (pandu), like every S01 cast. The chosen look then becomes make-cast.py.

Run from the repo root:  python3 episodes/S03E01-hanuman-never-died/svg/make-concepts.py <out_dir>
"""
import importlib.util
import os
import sys

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('c08', 'episodes/S01E08-gandhari-curses-krishna/svg/make-cast.py')
X = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X)
sys.argv = _argv
OUT = sys.argv[1]
V, M, F, C, Wm = X.V, X.M, X.F, X.C, X.Wm
group, frag, recolor = C.group, C.frag, C.recolor
INK, GOLD, GOLD_D, GOLD_L = X.INK, X.GOLD, X.GOLD_D, X.GOLD_L
NS = C.NS


def write(t, name):
    os.makedirs(OUT, exist_ok=True)
    t.write(f'{OUT}/{name}.svg', encoding='unicode')
    print('wrote', name)


def before(parent, gid, frags):
    """Insert shapes into `parent` just before its child group `gid` (so eyes and mouth stay on top)."""
    kids = list(parent)
    i = next(k for k, c in enumerate(kids) if c.get('id') == gid)
    for n, e in enumerate(frag(frags)):
        parent.insert(i + n, e)


# ---------- Hanuman ----------
def tail(fur, fur_d):
    """A long tail from the lower back, sweeping behind and curling up high (drawn behind the body)."""
    d = 'M450 1010 Q330 1080 280 960 Q230 820 300 640 Q340 520 300 430 Q270 370 310 350 Q350 340 344 392'
    return (f'<path d="{d}" stroke="{INK}" stroke-width="40" stroke-linecap="round" />'
            f'<path d="{d}" stroke="{fur}" stroke-width="30" stroke-linecap="round" />'
            f'<path d="M300 900 Q262 800 304 660" stroke="{fur_d}" stroke-width="8" stroke-linecap="round" />')


def gada(x=690, top=600, base=1500):
    """A mace standing upright at his side: a round fluted head on a gold-banded shaft."""
    return (f'<path d="M{x - 9} {top + 70} L{x - 9} {base} L{x + 9} {base} L{x + 9} {top + 70}Z" fill="#8A5A2A" stroke="{INK}" stroke-width="5" />'
            + ''.join(f'<rect x="{x - 13}" y="{y}" width="26" height="16" fill="{GOLD}" stroke="{INK}" stroke-width="3" />' for y in (top + 150, top + 420, base - 60))
            + f'<circle cx="{x}" cy="{top}" r="78" fill="{GOLD}" stroke="{INK}" stroke-width="6" />'
            + ''.join(f'<path d="M{x + 70 * c:.0f} {top + 30 * s:.0f} Q{x} {top - 6} {x - 70 * c:.0f} {top - 30 * s:.0f}" stroke="{GOLD_D}" stroke-width="5" />' for c, s in ((0.95, 0.9), (0.5, 1.6), (0.0, 2.0)))
            + f'<circle cx="{x - 22}" cy="{top - 24}" r="16" fill="{GOLD_L}" />'
            + f'<path d="M{x - 12} {top - 76} L{x} {top - 112} L{x + 12} {top - 76}Z" fill="{GOLD}" stroke="{INK}" stroke-width="4" />')


def muzzle(fur, face, face_d):
    """A vanara face: the lower face becomes a full, rounded muzzle (the jaw, hanu) growing out of the profile.
    Fill first with no outline, then ink only the outer edge, so it reads as part of the head, not a mask."""
    fill = 'M508 236 Q526 204 588 198 Q614 194 632 212 Q652 236 644 264 Q634 296 598 308 Q556 316 528 298 Q506 282 508 236Z'
    return (f'<path d="{fill}" fill="{face}" />'
            f'<path d="M588 198 Q614 194 632 212 Q652 236 644 264 Q634 296 598 308 Q556 316 528 298" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" />'
            f'<path d="M510 240 Q506 276 528 298" stroke="{face_d}" stroke-width="3" />'
            f'<path d="M540 300 Q580 312 616 296" stroke="{face_d}" stroke-width="4" />'
            f'<path d="M624 220 q5 -4 9 1 M610 218 q5 -4 8 1" stroke="{INK}" stroke-width="3.5" stroke-linecap="round" />'
            f'<path d="M630 232 Q628 248 614 254" stroke="{face_d}" stroke-width="3.5" />')


H_MOUTH = f'<path d="M556 274 Q594 286 632 262" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" />'
H_MOUTH_OPEN = f'<path d="M562 268 Q596 264 630 262 Q620 292 596 294 Q572 292 562 268Z" fill="#6E1E22" stroke="{INK}" stroke-width="3.5" />'
LOOKS_H = {
    'A': dict(name='saffron (temple sindoor)', skin=('#E8833A', '#D06A26', '#A24E18'), face=('#E2B080', '#C08A5A'),
              dhoti={'#FFF8E9': '#C9463A', '#F3EEDF': '#A93528', '#D6C7AF': '#86261C', '#B7A68F': '#5E1810'}, sash={'#F3EEDF': GOLD, '#D6C7AF': GOLD_D}),
    'B': dict(name='golden fur', skin=('#D9A65A', '#C08A40', '#93682A'), face=('#F2DDB8', '#D2B88E'),
              dhoti={'#FFF8E9': '#E0782E', '#F3EEDF': '#C4621E', '#D6C7AF': '#9A4A14', '#B7A68F': '#6E340C'}, sash={'#F3EEDF': '#C9463A', '#D6C7AF': '#93301F'}),
    'C': dict(name='earth-brown', skin=('#9C7656', '#825E42', '#5E422C'), face=('#E8C9A6', '#C8A27E'),
              dhoti={'#FFF8E9': '#F2C230', '#F3EEDF': '#DDA81E', '#D6C7AF': '#B78514', '#B7A68F': '#86600C'}, sash={'#F3EEDF': '#C9463A', '#D6C7AF': '#93301F'}),
}


def hanuman(key):
    L = LOOKS_H[key]
    sk = L['skin']
    t, r = F.pandu(sk, L['dhoti'], L['sash'])
    head = group(r, 'head')
    before(head, 'eyes-open', muzzle(sk[0], *L['face']))
    X.set_mouth(r, closed=H_MOUTH, open_=H_MOUTH_OPEN)
    M.male_brows(r, 'calm')
    M.folded_hands(r, sk)
    ch = group(r, 'character')
    for k, e in enumerate(frag(tail(sk[0], sk[2]))):
        ch.insert(k, e)
    group(r, 'canvas-placement').extend(frag(gada()))
    write(t, f'hanuman-{key}')


# ---------- Rama ----------
LOOKS_R = {
    'A': dict(name='durva-green dark (shyama, like durva grass)', skin=('#4E7A68', '#3C6454', '#284A3C')),
    'B': dict(name='deep indigo', skin=('#3E4F86', '#2F3E6E', '#1F2A4E')),
    'C': dict(name='dusky blue-grey', skin=('#5E7088', '#4A5A72', '#323E52')),
}
R_DHOTI = {'#FFF8E9': '#F2C230', '#F3EEDF': '#DDA81E', '#D6C7AF': '#B78514', '#B7A68F': '#86600C'}
R_SASH = {'#F3EEDF': '#C9463A', '#D6C7AF': '#93301F'}


def rama(key):
    L = LOOKS_R[key]
    t, r = F.pandu(L['skin'], R_DHOTI, R_SASH, bow='held')
    Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0))
    M.halo(r, rad=150); group(r, 'halo').set('opacity', '0.6')
    M.male_brows(r, 'calm'); X.k_smile(r)
    # a quiver of arrows over the back shoulder
    ch = group(r, 'character')
    for k, e in enumerate(frag(f'<g transform="translate(440 470) rotate(-14)"><rect x="-28" y="0" width="56" height="300" rx="14" fill="#8A5A2A" stroke="{INK}" stroke-width="5" />'
                              + ''.join(f'<path d="M{x} 0 L{x} -70 M{x - 10} -70 L{x} -96 L{x + 10} -70Z" stroke="{INK}" stroke-width="5" fill="#E8E0C8" />' for x in (-14, 0, 14))
                              + f'<rect x="-30" y="40" width="60" height="16" fill="{GOLD}" stroke="{INK}" stroke-width="3" /></g>')):
        ch.insert(k, e)
    write(t, f'rama-{key}')


if __name__ == '__main__':
    for k in 'ABC':
        hanuman(k); rama(k)
