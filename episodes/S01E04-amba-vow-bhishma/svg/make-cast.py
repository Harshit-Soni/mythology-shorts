"""S01E04 cast, made in code from the library rigs (reuse before create). Builds on S01E03's make-cast.py helpers.

Bhishma      <- pandu rig: young (crowned, dark hair) and old (white hair and beard) poses
Amba         <- the S01E02 women's build: a princess in deep red and gold
Ganga        <- the women's build: the river goddess in white and aqua, crowned, with a halo and a wave hem
Shalva       <- pandu rig: king of Saubha in purple
Parashurama  <- mandavya rig (the sage): matted hair and beard, an axe, a bow
Shikhandi    <- pandu rig: a young warrior of Panchala
Arjuna       <- + drawing-bow (the rig's own draw, in Arjuna's colours)

Every pose faces right; scenes mirror with flip.
Run from the repo root:  python3 episodes/S01E04-amba-vow-bhishma/svg/make-cast.py [out_dir]
"""
import copy
import importlib.util
import json
import os
import sys
import xml.etree.ElementTree as ET

_argv = sys.argv
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('c03', 'episodes/S01E03-urvashi-curses-arjuna/svg/make-cast.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
sys.argv = _argv
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets/characters'
C, Wm = M.C, M.Wm
group, frag, recolor, joint = C.group, C.frag, C.recolor, C.joint
NS, INK = C.NS, C.INK
GOLD, GOLD_D, GOLD_L = M.GOLD, M.GOLD_D, M.GOLD_L


def save(tree, cid, pose, title, expr=None):
    root = tree.getroot()
    root.set('data-character', cid)
    t = root.find(NS + 'title')
    if t is not None:
        t.text = title
    d = root.find(NS + 'desc')
    if d is not None:
        d.text = f'{title}. S01E04, made by episodes/S01E04-amba-vow-bhishma/svg/make-cast.py.'
    name = f'{pose}__{expr}' if expr else pose
    path = f'{OUT}/{cid}/{name}.svg'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree.write(path, encoding='unicode')
    print('wrote', path)


def unstring(r):
    group(r, 'arrow').set('style', 'display:none')
    for e in group(r, 'bow').iter():
        if e.get('data-role') == 'bowstring':
            e.set('d', 'M-70 -400L-70 440')


def pandu(skin, dhoti, sash, bow=None):
    """bow: None = remove, 'drawn' = keep the rig's draw, 'held' = unstrung bow in the hand."""
    t = ET.parse(C.SRC); r = t.getroot()
    for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
        recolor(group(r, g), dhoti)
    recolor(group(r, 'uttariya'), sash)
    recolor(r, dict(zip(C.PANDU_SKIN, skin)))
    if bow is None:
        M.remove(r, 'bow')
    elif bow == 'held':
        unstring(r)
    return t, r


# ---------- Bhishma ----------
B_SKIN = ('#EBC9A0', '#D8AF84', '#B48A62')
B_DHOTI = {'#FFF8E9': '#FBF6EA', '#F3EEDF': '#EDE5D2', '#D6C7AF': '#D4C6A8', '#B7A68F': '#AE9E80'}   # white, as befits the vow
B_SASH = {'#F3EEDF': '#3E6FA8', '#D6C7AF': '#2A4E7E'}                                               # a deep-blue uttariya


def old(r):
    """White hair and a long white beard (Bhishma at Kurukshetra)."""
    recolor(group(r, 'head'), {'#3C3031': '#EEE8DE', '#695450': '#C9C2B8'})
    group(r, 'head').extend(frag(
        f'<path d="M470 236 Q482 300 520 352 Q552 388 584 360 Q606 320 600 262 Q584 282 560 286 Q520 290 500 262 Q488 248 470 236Z" fill="#F3EEDF" stroke="{INK}" stroke-width="3" />'
        f'<path d="M520 300 Q536 330 548 350 M556 296 Q566 322 572 346" stroke="#C9C2B8" stroke-width="3" />'
        f'<path d="M548 252 Q572 246 596 254" stroke="#F3EEDF" stroke-width="9" />'))
    group(r, 'mouth-closed').set('style', 'display:none')


def bhishma():
    cid = 'bhishma'
    # young: the vow, right hand raised (s02)
    t, r = pandu(B_SKIN, B_DHOTI, B_SASH)
    Wm.arms(r, far=(-35, -125, -10), near=(10, -40, 0))
    Wm.palm(r, 'hand-far', B_SKIN)
    M.male_brows(r, 'calm')
    save(t, cid, 'vow-hand-raised', 'Bhishma · the vow, hand raised')
    # young: standing with his bow (s03)
    t, r = pandu(B_SKIN, B_DHOTI, B_SASH, bow='held')
    Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0))
    M.male_brows(r, 'angry')
    save(t, cid, 'standing-bow', 'Bhishma · standing with his bow')
    # young: drawing the bow (s04, s09)
    t, r = pandu(B_SKIN, B_DHOTI, B_SASH, bow='drawn')
    M.male_brows(r, 'angry')
    save(t, cid, 'drawing-bow', 'Bhishma · drawing his bow')
    # young: letting Amba go, an open hand (s05)
    t, r = pandu(B_SKIN, B_DHOTI, B_SASH)
    Wm.arms(r, far=(-62, -20, -30), near=(10, -40, 0))
    Wm.palm(r, 'hand-far', B_SKIN)
    M.male_brows(r, 'calm'); M.smile(r)
    save(t, cid, 'releasing', 'Bhishma · an open hand: go')
    # old: speaking by firelight (s17)
    t, r = pandu(B_SKIN, B_DHOTI, B_SASH)
    Wm.arms(r, far=(-55, -85, -20), near=(10, -40, 0))
    Wm.palm(r, 'hand-far', B_SKIN)
    old(r); M.male_brows(r, 'calm')
    save(t, cid, 'gesturing', 'Bhishma (old) · speaking, hand raised')
    # old: bow held still at his side (s18, s19); base calm, smiling variant
    for expr in (None, 'smiling'):
        t, r = pandu(B_SKIN, B_DHOTI, B_SASH, bow='held')
        Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0))
        old(r); M.male_brows(r, 'calm')
        if expr:
            group(r, 'head').extend(frag(f'<path d="M560 268 Q574 278 590 266" stroke="{INK}" stroke-width="3" />'))
        save(t, cid, 'bow-still', 'Bhishma (old) · bow held still' + (', smiling' if expr else ''), expr)


# ---------- Amba and Ganga (the women's build) ----------
C.WOMEN['amba'] = dict(skin=('#F1CBA3', '#DFB085', '#BB8A60'), border=GOLD_D, border_l=GOLD,
                       utt=('#B5402E', '#8E2A20', '#D86A54'), hair='braid')
C.WOMEN['ganga'] = dict(skin=('#F7E2CC', '#EACBAE', '#C9A483'), border='#2E8A9E', border_l='#6FC3D3',
                        utt=('#9FD3E6', '#6FB0C8', '#D4F0F7'), hair='braid')


def amba_base():
    t = C.build('amba', drape_style='sash', eye_scale=1.16, warmth=0)
    r = t.getroot()
    recolor(group(r, 'dhoti'), {'#F3EEDF': '#9E2B3A', '#E6DCC6': '#84202F', '#B7A68F': '#5E1621', '#D6C7AF': '#B5485A'})
    recolor(group(r, 'kanchuka'), {'#F3EEDF': '#9E2B3A'})
    group(r, 'head').extend(frag(f'<path d="M462 118 Q520 96 598 120" stroke="{GOLD}" stroke-width="8" />'
                                 f'<circle cx="530" cy="104" r="7" fill="{GOLD}" stroke="{INK}" stroke-width="2" />'))
    return t, r


def amba():
    sk = C.WOMEN['amba']['skin']
    # tapas: both palms joined high above her head, eyes closed variant
    for expr in (None, 'eyes-closed'):
        t, r = amba_base()
        Wm.arms(r, far=(-168, 8, 20), near=(-158, -18, -20))
        Wm.palm(r, 'hand-far', sk, narrow=True); Wm.palm(r, 'hand-near', sk, narrow=True)
        M.female_brows(r, 'firm')
        if expr:
            M.eyes_closed(r)
        save(t, 'amba', 'tapas-standing', 'Amba · tapas, palms joined above her head' + (', eyes closed' if expr else ''), expr)
    t, r = amba_base(); M.tilt(r, 5); M.female_brows(r, 'sad')
    save(t, 'amba', 'standing-sad', 'Amba · standing, sad')
    t, r = amba_base()
    M.folded_hands(r, sk); M.female_brows(r, 'up'); Wm.eyes_up(r)
    save(t, 'amba', 'folded-hands', 'Amba · palms joined, pleading')
    t, r = amba_base()
    Wm.arms(r, far=(-2, 6, 0), near=(16, -146, 40))
    M.female_brows(r, 'angry'); M.tilt(r, -3)
    save(t, 'amba', 'resolute', 'Amba · a fist at her heart, resolute')


def ganga_base():
    t = C.build('ganga', drape_style='shawl', eye_scale=1.12, warmth=1)
    r = t.getroot()
    recolor(group(r, 'dhoti'), {'#F3EEDF': '#F4FBFD', '#E6DCC6': '#D4ECF2', '#B7A68F': '#8FBFCC', '#D6C7AF': '#BFE0E8'})
    recolor(group(r, 'kanchuka'), {'#F3EEDF': '#F4FBFD'})
    M.halo(r)
    group(r, 'head').extend(frag(
        f'<path d="M454 120 L470 70 L492 104 L520 52 L548 104 L570 70 L590 120 Q520 100 454 120Z" fill="{GOLD}" stroke="{INK}" stroke-width="3" />'
        f'<circle cx="520" cy="96" r="9" fill="#2E8A9E" stroke="{INK}" stroke-width="2" />'))
    # waves rising at the hem: she comes up out of the river
    dh = group(r, 'dhoti')
    dh.extend(frag(''.join(f'<path d="M{260 + k * 120} 1500 q30 -60 60 0 q30 -60 60 0" fill="#6FB0C8" stroke="{INK}" stroke-width="3" opacity="0.95" />' for k in range(5))
                   + f'<path d="M250 1520 Q520 1480 790 1520 L790 1560 L250 1560Z" fill="#6FB0C8" stroke="{INK}" stroke-width="3" />'))
    M.bangles(r, 'hand-far', 2); M.bangles(r, 'hand-near', 2)
    return t, r


def ganga():
    sk = C.WOMEN['ganga']['skin']
    t, r = ganga_base()
    Wm.arms(r, far=(-60, -40, -20), near=(60, -30, 20))
    Wm.palm(r, 'hand-far', sk); Wm.palm(r, 'hand-near', sk)
    M.female_brows(r, 'firm'); Wm.mouth(r, open_=True)
    save(t, 'ganga', 'rising', 'Ganga · rising from the river, palms open')
    t, r = ganga_base()
    Wm.arms(r, far=(-118, -18, -14), near=(14, -40, 10))
    Wm.palm(r, 'hand-far', sk)
    M.female_brows(r, 'angry'); Wm.mouth(r, open_=True)
    save(t, 'ganga', 'cursing', 'Ganga · cursing, palm raised')


# ---------- Shalva ----------
S_SKIN = ('#E3BC92', '#CFA276', '#AA7C52')
S_DHOTI = {'#FFF8E9': '#8A6CB5', '#F3EEDF': '#6A4C93', '#D6C7AF': '#4E3672', '#B7A68F': '#36244F'}


def shalva():
    t, r = pandu(S_SKIN, S_DHOTI, M.A_SASH)
    Wm.arms(r, far=(-40, -30, 0), near=(70, 10, 0))
    Wm.palm(r, 'hand-far', S_SKIN); Wm.palm(r, 'hand-near', S_SKIN)
    M.lean(r, -8); M.male_brows(r, 'up'); M.mouth_open(r)
    save(t, 'shalva', 'defeated', 'Shalva · staggering back, defeated')
    # turning away to the right; the near (back) hand flung back toward her: "go"
    t, r = pandu(S_SKIN, S_DHOTI, M.A_SASH)
    Wm.arms(r, far=(-6, -10, 0), near=(92, -8, 95))
    Wm.palm(r, 'hand-near', S_SKIN)
    M.male_brows(r, 'calm')
    save(t, 'shalva', 'turning-away', 'Shalva · turning away, a hand flung back')


# ---------- Parashurama (mandavya rig) ----------
MAND = 'assets/characters/mandavya/standing-calm.svg'
P_DHOTI = {}


def m_arms(r, far, near):
    joint(r, 'upper-arm-far', f'translate(635 390) rotate({far[0]})')
    joint(r, 'forearm-far', f'translate(0 210.523) rotate({far[1]})')
    joint(r, 'hand-far', f'translate(0 222.122) rotate({far[2]})')
    joint(r, 'upper-arm-near', f'translate(335 397) rotate({near[0]})')
    joint(r, 'forearm-near', f'translate(0 209.029) rotate({near[1]})')
    joint(r, 'hand-near', f'translate(0 215.856) rotate({near[2]})')


AXE = (f'<g id="parashu"><path d="M0 -40 L0 330" stroke="#6E4228" stroke-width="16" /><path d="M0 -40 L0 330" stroke="{INK}" stroke-width="2" fill="none" />'
       f'<path d="M0 -40 Q70 -70 96 -10 Q60 20 0 10Z" fill="#C9CED6" stroke="{INK}" stroke-width="4" />'
       f'<path d="M10 -36 Q62 -56 82 -14" stroke="#F3F5F8" stroke-width="5" fill="none" /></g>')


def parashurama():
    def base():
        t = ET.parse(MAND); r = t.getroot()
        # darker, weathered; dhoti in deep red-brown (a warrior-sage) instead of Mandavya's saffron
        for g in ('dhoti-back', 'dhoti-near-wrap', 'dhoti-front-pleat', 'waist-wrap'):
            recolor(group(r, g), {'#F6A13E': '#B8553A', '#E68129': '#9E3B22', '#BC5420': '#6E2A18', '#9E451F': '#4E1C10'})
        return t, r
    t, r = base()
    m_arms(r, far=(-10, -150, 160), near=(15, -10, 0))
    axe = frag(AXE)[0]; axe.set('transform', 'translate(0 -60) scale(1.5)')
    group(r, 'hand-far').append(axe)
    save(t, 'parashurama', 'standing-axe', 'Parashurama · standing with his axe')
    t, r = base()
    m_arms(r, far=(-45, -40, 85), near=(-70, -95, 0))
    bow = copy.deepcopy(group(ET.parse(C.SRC).getroot(), 'bow'))
    group(r, 'hand-far').append(bow)
    save(t, 'parashurama', 'drawing-bow', 'Parashurama · drawing his bow')


# ---------- Shikhandi ----------
K_SKIN = ('#D9A577', '#C08A5C', '#986640')
K_DHOTI = {'#FFF8E9': '#C9742E', '#F3EEDF': '#A85A22', '#D6C7AF': '#844417', '#B7A68F': '#5E300E'}


def shikhandi():
    def base(bow):
        t, r = pandu(K_SKIN, K_DHOTI, {'#F3EEDF': '#2E6B4F', '#D6C7AF': '#1F4E39'}, bow=bow)
        group(r, 'crown').set('transform', 'translate(510 115) scale(0.78) translate(-510 -115)')
        cp = group(r, 'canvas-placement')
        cp.set('transform', 'translate(500 1550) scale(0.94) translate(-500 -1550) ' + cp.get('transform'))
        return t, r
    t, r = base('held')
    Wm.arms(r, far=(-12, -14, 45), near=(10, -40, 0))
    M.male_brows(r, 'calm')
    save(t, 'shikhandi', 'standing-bow', 'Shikhandi · standing with a bow')
    t, r = base('drawn')
    M.male_brows(r, 'angry')
    save(t, 'shikhandi', 'drawing-bow', 'Shikhandi · drawing the bow')


def arjuna_drawing():
    t, r = M.arjuna_base(bow=True)
    M.male_brows(r, 'angry')
    save(t, 'arjuna', 'drawing-bow', 'Arjuna · drawing the Gandiva')


def character_json():
    cast = {
        'bhishma': dict(name={'en': 'Bhishma', 'hi': 'भीष्म'}, role='Son of Ganga and Shantanu; the Kuru patriarch bound by his vow', divine=False,
                        look='Fair, in white (the vow) with a deep-blue uttariya and a gold crown. Young poses: dark hair. Old poses (Kurukshetra): white hair and a long white beard.',
                        sourceNotes='Adi §100 (the vow), §102; Udyoga §174–190; Bhishma Parva §108–121.',
                        poses=['vow-hand-raised', 'standing-bow', 'drawing-bow', 'releasing', 'gesturing', 'bow-still'],
                        facingByPose=None, notes_extra='young: vow-hand-raised, standing-bow, drawing-bow, releasing; old: gesturing, bow-still'),
        'amba': dict(name={'en': 'Amba', 'hi': 'अम्बा'}, role='Eldest princess of Kashi; reborn as Shikhandi', divine=False,
                     look='A princess in deep red with gold borders and a red sash, a slim gold diadem, a long braid.',
                     sourceNotes='Adi §102; Udyoga §175–190.', poses=['tapas-standing', 'standing-sad', 'folded-hands', 'resolute']),
        'ganga': dict(name={'en': 'Ganga', 'hi': 'गंगा'}, role='The river goddess; Bhishma’s mother', divine=True,
                      look='White and aqua, a gold crown, a rayed halo, waves rising at her hem.',
                      sourceNotes='Udyoga §189 (her curse on Amba).', poses=['rising', 'cursing']),
        'shalva': dict(name={'en': 'Shalva', 'hi': 'शाल्व'}, role='King of Saubha; the king Amba loved', divine=False,
                       look='A king in purple with a gold sash and crown.', sourceNotes='Adi §102; Udyoga §176.', poses=['defeated', 'turning-away']),
        'parashurama': dict(name={'en': 'Parashurama', 'hi': 'परशुराम'}, role='The warrior-sage, Bhishma’s teacher', divine=False,
                            look='The sage rig (matted hair, beard, rudraksha) in a deep red-brown dhoti, with his axe (parashu) and a bow.',
                            sourceNotes='Udyoga §178–189.', poses=['standing-axe', 'drawing-bow']),
        'shikhandi': dict(name={'en': 'Shikhandi', 'hi': 'शिखण्डी'}, role='Drupada’s child; Amba reborn', divine=False,
                          look='A young warrior of Panchala in ochre with a green sash and a small crown.',
                          sourceNotes='Udyoga §191–195; Bhishma Parva §108–121. Shown with dignity, in the text’s own terms.', poses=['standing-bow', 'drawing-bow']),
    }
    for cid, d in cast.items():
        files = {f[:-4]: f for f in sorted(os.listdir(f'{OUT}/{cid}')) if f.endswith('.svg')}
        extra = d.pop('notes_extra', '')
        d.pop('facingByPose', None)
        out = {'id': cid, **d, 'appearsIn': ['S01E04'], 'files': files, 'facing': 'per pose, see facingByPose (ear rule)',
               'facingByPose': {p: 'right' for p in d['poses']},
               'notes': ('Made in code by episodes/S01E04-amba-vow-bhishma/svg/make-cast.py. All poses face right; mirror with flip. ' + extra).strip()}
        with open(f'{OUT}/{cid}/character.json', 'w') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print('wrote', f'{OUT}/{cid}/character.json')
    # Arjuna: add the new pose to his existing file
    p = f'{OUT}/arjuna/character.json'
    if os.path.exists(p):
        j = json.load(open(p))
        if 'drawing-bow' not in j['poses']:
            j['poses'].append('drawing-bow')
        j['files']['drawing-bow'] = 'drawing-bow.svg'
        j.setdefault('facingByPose', {})['drawing-bow'] = 'right'
        if 'S01E04' not in j.get('appearsIn', []):
            j.setdefault('appearsIn', []).append('S01E04')
        json.dump(j, open(p, 'w'), ensure_ascii=False, indent=2)
        print('updated', p)


if __name__ == '__main__':
    bhishma(); amba(); ganga(); shalva(); parashurama(); shikhandi(); arjuna_drawing(); character_json()
