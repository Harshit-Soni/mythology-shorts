"""S01E07 cast, made in code from the library rigs (reuse before create). Builds on the S01E05/E06 helpers.

Parikshit    <- pandu rig: maroon and cream, crown, a greying moustache (a mature king)
Shamika      <- mandavya rig: white hair, pale bark cloth; seated cross-legged, with and without the dead snake; gentle
Shringi      <- pandu rig in hermitage dress: topknot, ochre bark cloth, no gold (a boy: scale 0.85 in scenes)
Kashyapa     <- mandavya rig: brown-grey hair, blue-green cloth (the healer)
old-brahmin  <- mandavya rig: Takshaka in disguise: white hair, rust cloth, a pouch of gold
(Takshaka himself is made in make-props.py, with S01E06's snake rig.)

All poses face right; scenes mirror with flip.
Run from the repo root:  python3 episodes/S01E07-parikshit-seven-days/svg/make-cast.py [out_dir]
"""
import importlib.util
import json
import os
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('c06', 'episodes/S01E06-nahusha-becomes-a-snake/svg/make-cast.py')
Z = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Z)
sys.argv = _argv
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
K, F, M, C, Wm = Z.K, Z.F, Z.M, Z.C, Z.Wm
group, frag, recolor, joint = C.group, C.frag, C.recolor, C.joint
NS, INK, GOLD, GOLD_D, GOLD_L = C.NS, C.INK, M.GOLD, M.GOLD_D, M.GOLD_L


def save(tree, cid, pose, title):
    root = tree.getroot()
    root.set('data-character', cid)
    for tag, text in (('title', title), ('desc', f'{title}. S01E07, made by episodes/S01E07-parikshit-seven-days/svg/make-cast.py.')):
        e = root.find(NS + tag)
        if e is not None:
            e.text = text
    path = f'{OUT}/{cid}/{pose}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode')
    print('wrote', path)


# ---------- Parikshit ----------
P_SKIN = ('#D9A06A', '#BF834E', '#965C32')
P_DHOTI = {'#FFF8E9': '#B4524A', '#F3EEDF': '#983A36', '#D6C7AF': '#742826', '#B7A68F': '#4E1818'}
P_SASH = {'#F3EEDF': '#F2E2BC', '#D6C7AF': '#D2B884'}


def parikshit_base(bow=None):
    t, r = F.pandu(P_SKIN, P_DHOTI, P_SASH, bow=bow)
    group(r, 'head').extend(frag(
        '<path d="M544 238 Q566 228 590 234 Q606 238 610 228 Q604 250 584 247 Q562 244 544 252 Q534 250 544 238Z" fill="#3A3032" /><path d="M548 242 Q568 234 588 239" stroke="#8E8788" stroke-width="3" />'
        '<path d="M470 196 Q462 214 468 236 M478 200 Q472 216 476 232" stroke="#8E8788" stroke-width="4" />'))
    return t, r


def laugh(r):
    """A broad open laugh, and a smile for the closed mouth, so the lip-sync keeps laughing."""
    M.male_brows(r, 'up')
    for gid, svg in (('mouth-closed', f'<path d="M546 256 Q570 274 596 252" stroke="{INK}" stroke-width="5" /><path d="M540 250 q4 8 10 8 M600 246 q-2 8 -6 8" stroke="{INK}" stroke-width="3" />'),
                     ('mouth-open', f'<path d="M544 250 Q570 256 598 246 Q600 280 574 288 Q548 286 544 250Z" fill="#6E1E22" stroke="{INK}" stroke-width="4" /><path d="M550 254 Q572 259 594 251 L592 262 Q572 268 553 264Z" fill="#FFF8E9" /><path d="M560 282 Q574 274 588 280 Q576 288 560 282Z" fill="#C9586A" />')):
        g = group(r, gid)
        for ch in list(g):
            g.remove(ch)
        g.extend(frag(svg))
    group(r, 'mouth-closed').set('style', 'display:none'); group(r, 'mouth-open').attrib.pop('style', None)  # laughing at rest
    group(r, 'head').extend(frag(f'<path d="M500 206 q-10 -6 -14 -14 M502 214 q-12 -1 -18 -6" stroke="{INK}" stroke-width="2.5" />'))


def worm(x, y, s=1.0):
    """The copper worm with black eyes (CE 1.39.29), small enough to sit on a fingertip."""
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-18 8 Q-8 -14 2 2 Q12 16 22 -6" stroke="{INK}" stroke-width="17" /><path d="M-18 8 Q-8 -14 2 2 Q12 16 22 -6" stroke="#C4622E" stroke-width="11" />'
            f'<path d="M-18 6 Q-8 -14 2 0" stroke="#E79A66" stroke-width="3" /><circle cx="23" cy="-8" r="9" fill="#C4622E" stroke="{INK}" stroke-width="3" /><circle cx="26" cy="-10" r="3" fill="{INK}" /></g>')


def pinch(r, hand, skin):
    """Finger and thumb meeting at a tip (the hand hangs along +y), three relaxed fingers behind: it holds something tiny."""
    Wm.palm(r, hand, skin)
    h = group(r, hand)
    for ch in list(h):
        h.remove(ch)
    a, b, _ = skin
    def f(d, w): return f'<path d="{d}" stroke="{INK}" stroke-width="{w + 6}" /><path d="{d}" stroke="{a}" stroke-width="{w}" />'
    h.extend(frag(f('M18 50 Q52 74 46 108', 17) + f('M22 40 Q62 56 62 86', 16) + f('M22 28 Q62 36 70 60', 15)
                  + f'<path d="M-26 -8 Q-36 30 -24 64 Q0 80 30 62 Q40 30 26 -8Z" fill="{a}" stroke="{INK}" stroke-width="3" />'
                  + f('M14 52 Q30 92 8 124', 20) + f('M-16 48 Q-40 88 -6 124', 19) + f'<path d="M-18 56 Q-34 86 -14 112" stroke="{b}" stroke-width="4" />'))


def parikshit():
    cid = 'parikshit'
    t, r = parikshit_base(); Wm.arms(r, far=(-8, 6, 0), near=(10, -20, 0)); M.male_brows(r, 'sad')
    save(t, cid, 'waiting', 'Parikshit · grave, waiting')
    t, r = parikshit_base('held'); Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0)); K.worry(r); M.lean(r, 5); M.tilt(r, 4)
    group(r, 'head').extend(frag(f'<path d="M492 170 q-10 16 0 22 q11 -6 0 -22Z" fill="#CFE6F2" stroke="{INK}" stroke-width="2" />'))
    save(t, cid, 'hunting', 'Parikshit · on the hunt, tired, bow in hand')
    t, r = parikshit_base(); Wm.arms(r, far=(-68, -22, -30), near=(10, -40, 0)); Wm.palm(r, 'hand-far', P_SKIN); K.worry(r); M.mouth_open(r)
    save(t, cid, 'asking', 'Parikshit · asking, a hand out')
    t, r = parikshit_base(); Wm.arms(r, far=(-30, -60, 0), near=(26, -70, 0)); K.strain(r)
    save(t, cid, 'furious', 'Parikshit · furious, teeth clenched')
    t, r = parikshit_base(); M.folded_hands(r, P_SKIN); K.worry(r); M.tilt(r, 12)
    save(t, cid, 'regret', 'Parikshit · sorry for what he did, palms joined')
    t, r = parikshit_base(); Wm.arms(r, far=(-18, -84, -20), near=(22, -64, 0)); Wm.palm(r, 'hand-far', P_SKIN); laugh(r); M.tilt(r, -6)
    save(t, cid, 'laughing', 'Parikshit · laughing with relief')
    t, r = parikshit_base(); Wm.arms(r, far=(-40, -104, 0), near=(22, -64, 0)); pinch(r, 'hand-far', P_SKIN); laugh(r)
    group(r, 'hand-far').extend(frag(worm(0, 142, 1.2)))
    save(t, cid, 'worm-raised', 'Parikshit · laughing, the worm between finger and thumb')
    t, r = parikshit_base(); Wm.arms(r, far=(-16, -206, 0), near=(16, -40, 0)); pinch(r, 'hand-far', P_SKIN); laugh(r); M.tilt(r, -4)
    group(r, 'hand-far').extend(frag(worm(0, 140, 1.0)))
    save(t, cid, 'to-neck', 'Parikshit · laughing, putting the worm to his own neck')
    t, r = parikshit_base(); Wm.arms(r, far=(-4, 4, 0), near=(6, -6, 0)); M.male_brows(r, 'up'); M.mouth_open(r)
    save(t, cid, 'shocked', 'Parikshit · arms pinned, shocked')


# ---------- Shamika ----------
S_HAIR = ('#8F887C', '#B9B2A6', '#DAD4C8', '#F2EEE6', '#FFFFFF')
S_SKIN = ('#E7B98A', '#D09C6C', '#A8744A')
S_CLOTH = ('#EBD9B0', '#D3BC88', '#AE9560', '#82693C')
LAP = 560


def sit_cross(r, cloth, skin):
    """Cross-legged (E05's seated_lap, for the sage rig), hands on the knees."""
    M.lean(r, 0, LAP)
    M.hide(r, 'leg-near'); M.hide(r, 'leg-far')
    dh = group(r, 'dhoti')
    for ch in list(dh):
        dh.remove(ch)
    a, b, c, d = cloth
    g, hip, s1 = 1525, 640 + LAP, skin[1]
    dh.extend(frag(
        K.limb(f'M470 {hip + 40} Q330 {hip + 70} 206 {g - 96}', 150, b, a) + K.limb(f'M580 {hip + 40} Q720 {hip + 70} 842 {g - 96}', 150, b, a)
        + f'<path d="M400 {hip - 8} Q520 {hip - 24} 644 {hip - 8} L690 {g - 60} Q520 {g - 20} 350 {g - 60}Z" fill="{b}" />'
        + K.limb(f'M842 {g - 84} Q640 {g - 30} 470 {g - 54}', 104, c, b) + K.limb(f'M206 {g - 84} Q400 {g - 10} 590 {g - 46}', 104, b, a)
        + f'<path d="M588 {g - 96} Q650 {g - 100} 690 {g - 66} Q706 {g - 30} 660 {g - 8} Q610 {g} 590 {g - 8}Z" fill="{s1}" stroke="{INK}" stroke-width="3.5" />'
        + f'<path d="M462 {g - 92} Q410 {g - 92} 384 {g - 58} Q380 {g - 34} 410 {g - 22}" fill="{s1}" stroke="{INK}" stroke-width="3" />'
        + f'<path d="M300 {g - 110} Q380 {g - 140} 440 {g - 120} M620 {g - 130} Q700 {g - 150} 780 {g - 118}" stroke="{d}" stroke-width="4" />'
        + f'<path d="M394 {hip - 14} Q520 {hip - 30} 648 {hip - 12} L652 {hip + 26} Q520 {hip + 8} 390 {hip + 24}Z" fill="{b}" />'))


def soft_brows(r):
    b = group(r, 'brows')
    for ch in list(b):
        b.remove(ch)
    b.extend(frag('<path d="M511 163 Q533 160 557 151 L559 157 Q535 168 515 170Z" fill="#B9B2A6" /><path d="M583 152 L595 158 L595 164 L584 158Z" fill="#B9B2A6" />'))


def dead_snake(d, w, head_at, rot):
    x, y = head_at
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{w + 10}" /><path d="{d}" stroke="#7E9A62" stroke-width="{w}" /><path d="{d}" stroke="#A9C086" stroke-width="{w * .18:.0f}" transform="translate({-w * .24:.0f} {-w * .1:.0f})" />'
            f'<path d="{d}" stroke="#4A5E36" stroke-width="{w * .3:.0f}" stroke-dasharray="2 {w * 1.1:.0f}" />'
            f'<g transform="translate({x} {y}) rotate({rot}) scale({w / 40:.2f})"><path d="M-20 -24 Q46 -42 88 -8 Q94 10 78 20 Q28 34 -20 24Z" fill="#7E9A62" stroke="{INK}" stroke-width="5" /><path d="M32 -8 Q44 -2 56 -10" stroke="{INK}" stroke-width="5" /></g>')


def shamika():
    cid = 'shamika'
    for pose, snake in (('seated-silent', False), ('with-snake', True)):
        t, r = K.sage(K.CALM, S_CLOTH, S_HAIR, S_SKIN); F.m_arms(r, far=(-20, 26, 0), near=(18, -26, 0)); soft_brows(r)
        sit_cross(r, S_CLOTH, S_SKIN)
        if snake:
            group(r, 'upper-body-front').extend(frag(dead_snake('M286 690 Q262 560 296 450 Q330 366 392 384 Q440 404 446 500 Q450 600 436 690', 42, (436, 694), 96)))
        save(t, cid, pose, 'Shamika · seated, silent' + (', the dead snake on his shoulder' if snake else ''))
    t, r = K.sage(K.CALM, S_CLOTH, S_HAIR, S_SKIN); F.m_arms(r, far=(-34, -70, -10), near=(16, -10, 0)); Wm.palm(r, 'hand-far', S_SKIN); soft_brows(r)
    save(t, cid, 'gentle', 'Shamika · gentle, a hand held out')


# ---------- Shringi ----------
H_SKIN = ('#E6B587', '#CF9868', '#A66F42')
H_DHOTI = {'#FFF8E9': '#E8B45E', '#F3EEDF': '#D0953E', '#D6C7AF': '#A87028', '#B7A68F': '#774C18'}
H_SASH = {'#F3EEDF': '#8E5A36', '#D6C7AF': '#6A3E22'}


def shringi():
    cid = 'shringi'
    t, r = Z.exile(H_SKIN, H_DHOTI, H_SASH); Wm.arms(r, far=(-30, -70, -10), near=(14, -90, 0)); Wm.palm(r, 'hand-far', H_SKIN); K.worry(r); M.mouth_open(r); M.tilt(r, 6)
    group(r, 'head').extend(frag(f'<path d="M552 204 q-7 14 0 22 q9 -6 0 -22Z" fill="#CFE6F2" stroke="{INK}" stroke-width="2" /><path d="M590 206 q-5 12 1 18" stroke="#CFE6F2" stroke-width="5" />'))
    save(t, cid, 'grief', 'Shringi · a boy seeing his father shamed, in tears')
    t, r = Z.exile(H_SKIN, H_DHOTI, H_SASH); Wm.arms(r, far=(-112, -34, 0), near=(22, -50, 0)); Wm.palm(r, 'hand-far', H_SKIN); M.male_brows(r, 'angry'); M.mouth_open(r)
    group(r, 'hand-far').extend(frag('<path d="M-22 80 q-6 18 2 24 q8 -6 -2 -24Z M16 84 q-5 16 2 22 q7 -6 -2 -22Z" fill="#CFE6F2" stroke="#6FA6C4" stroke-width="2" />'))
    save(t, cid, 'cursing', 'Shringi · cursing, water in his raised palm')


# ---------- Kashyapa, and Takshaka as an old Brahmin ----------
KA_HAIR = ('#3E3631', '#5E544C', '#8A7E72', '#BDB4A6', '#DAD3C6')
KA_SKIN = ('#D8A272', '#BE8656', '#946038')
KA_CLOTH = ('#8FC0B4', '#629E92', '#43766E', '#2C524D')
OB_CLOTH = ('#C98A6A', '#A9654A', '#7E4330', '#56291C')


def kashyapa():
    t = ET.parse('assets/characters/mandavya/walking.svg'); r = t.getroot()
    recolor(r, {**dict(zip(('#F6A13E', '#E68129', '#BC5420', '#9E451F'), KA_CLOTH)), **dict(zip(('#241E25', '#3C3031', '#695450', '#A8A39A', '#CBC4B4'), KA_HAIR)), **dict(zip(('#E5A66B', '#CF8D55', '#AB653C'), KA_SKIN))})
    save(t, 'kashyapa', 'walking', 'Kashyapa · the healer, walking')
    t, r = K.sage(K.CALM, KA_CLOTH, KA_HAIR, KA_SKIN); F.m_arms(r, far=(-40, -70, -10), near=(16, -10, 0)); Wm.palm(r, 'hand-far', KA_SKIN)
    save(t, 'kashyapa', 'reviving', 'Kashyapa · a palm held out, bringing life back')
    t, r = K.sage(K.CALM, OB_CLOTH, S_HAIR, ('#C9B090', '#AE9474', '#86704F')); F.m_arms(r, far=(-4, -80, 0), near=(16, -10, 0)); Wm.palm(r, 'hand-far', ('#C9B090', '#AE9474', '#86704F')); M.lean(r, 6); M.tilt(r, -6)
    group(r, 'hand-far').extend(frag(f'<path d="M-34 70 Q-60 120 -40 168 Q0 190 44 166 Q64 118 36 70Z" fill="#B9855A" stroke="{INK}" stroke-width="4" /><path d="M-30 78 Q2 92 34 78" stroke="{GOLD}" stroke-width="8" />'
                                      + ''.join(f'<circle cx="{x}" cy="{y}" r="12" fill="{GOLD}" stroke="{INK}" stroke-width="3" />' for x, y in ((-18, 62), (4, 54), (24, 62)))))
    save(t, 'old-brahmin', 'offering-gold', 'Takshaka as an old Brahmin · holding out a pouch of gold')


def character_json():
    cast = {
        'parikshit': dict(name={'en': 'Parikshit', 'hi': 'परीक्षित'}, role='King of Hastinapura, son of Abhimanyu, Arjuna’s grandson', look='The pandu rig: maroon and cream, crown, a greying moustache.', sourceNotes='CE 1.36–40; 1.45.23 (sixty years old).',
                          poses=['waiting', 'hunting', 'asking', 'furious', 'regret', 'laughing', 'worm-raised', 'to-neck', 'shocked']),
        'shamika': dict(name={'en': 'Shamika', 'hi': 'शमीक'}, role='The silent sage who forgave the king', look='The sage rig with white hair and beard, pale bark cloth. Calm in every pose.', sourceNotes='CE 1.36–38.', poses=['seated-silent', 'with-snake', 'gentle']),
        'shringi': dict(name={'en': 'Shringi', 'hi': 'शृंगी'}, role='Shamika’s young son, who cursed the king', look='A boy in ochre bark cloth, a topknot, no gold. Scale about 0.85 in scenes.', sourceNotes='CE 1.36–37.', poses=['grief', 'cursing']),
        'kashyapa': dict(name={'en': 'Kashyapa', 'hi': 'काश्यप'}, role='The healer who was paid to turn back', look='The sage rig, brown-grey hair, blue-green cloth.', sourceNotes='CE 1.38–39. Not the Kashyapa who fathered the snakes.', poses=['walking', 'reviving']),
        'old-brahmin': dict(name={'en': 'Takshaka as an old Brahmin', 'hi': 'वृद्ध ब्राह्मण (तक्षक)'}, role='Takshaka in disguise', look='White hair, rust cloth, ashen skin, a pouch of gold.', sourceNotes='CE 1.38.34.', poses=['offering-gold']),
    }
    for cid, d in cast.items():
        files = {f[:-4]: f for f in sorted(os.listdir(f'{OUT}/{cid}')) if f.endswith('.svg')}
        out = {'id': cid, 'divine': False, **d, 'appearsIn': ['S01E07'], 'files': files, 'facing': 'right', 'facingByPose': {p: 'right' for p in d['poses']},
               'notes': 'Made in code by episodes/S01E07-parikshit-seven-days/svg/make-cast.py. Mirror with flip.'}
        json.dump(out, open(f'{OUT}/{cid}/character.json', 'w'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    parikshit(); shamika(); shringi(); kashyapa(); character_json()
