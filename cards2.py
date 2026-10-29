"""cards2.py - the rest of the cast as portraits, in cards.py's style: Arena 1's other robots, then Arena 2's (The Core).

    python site/cards2.py [key ...]        -> site/img/art/card_KEY.png
"""
import math, os, random, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paint import C, gf                                          # noqa: E402
from boxart import OUT, ngon                                     # noqa: E402
from cards import card, tank                                     # noqa: E402


def _bow(a, cx, cy, s, rnd, base, rim, flap=0.0, plates=False):
    """a bowtie: two chrome wings meeting at a hub (the game's X-crossed rectangle)"""
    for side in (-1, 1):
        tip = s * (1.0 - 0.15 * flap)
        w = a.poly([(cx, cy), (cx + side * s * 1.1, cy - tip), (cx + side * s * 1.1, cy + tip)])
        a.shadow(w, 8, 14, 10, 0.45)
        a.solid(w, base, bevel=s * 0.12, chrome=0.6, rim=rim, spec=0.9, tex=0.3, rnd=rnd)
        if plates:                                                     # (armour plates and rivets)
            for k in range(3):
                x = cx + side * s * (0.45 + k * 0.25)
                h = s * (0.36 + k * 0.23)
                a.add(a.lines([(x, cy - h), (x, cy + h)], 2), C('#14100c'), -0.55)
                for yy in (-1, 1):
                    a.solid(a.ell(x + side * s * 0.1, cy + yy * h * 0.75, s * 0.035), '#d8d0c0', bevel=2, spec=0.9)
        a.glow(a.rect(cx + side * s * 1.08 - 3, cy - tip * 0.8, cx + side * s * 1.08 + 3, cy + tip * 0.8), C(rim), s * 0.05, 1.0)
    a.solid(a.ell(cx, cy, s * 0.22), '#3a3f4c', bevel=s * 0.08, chrome=0.6, spec=1.0)
    a.glow(a.ell(cx, cy, s * 0.09), C('#ff2a2a'), s * 0.12, 2.4)


def bowtie(a, cx, cy, s, rnd):
    """the small bowtie: flaps, glides, and spits one aimed dot"""
    _bow(a, cx, cy, s, rnd, '#5a8ad8', '#ff7bd5', flap=0.35)
    a.beam((cx + s * 0.1, cy + s * 0.2), (cx + s * 0.9, cy + s * 1.35), '#ffe066', w=4, g=6, k=0.7)
    a.glow(a.ell(cx + s * 0.95, cy + s * 1.42, s * 0.07), C('#fff4c2'), s * 0.1, 2.0)


def strongbow(a, cx, cy, s, rnd):
    """the strong bowtie: an armoured bowtie, a fast double shot aimed where you are heading"""
    _bow(a, cx, cy, s, rnd, '#b8862a', '#ff5a2a', plates=True)
    for d in (-0.12, 0.12):
        a.beam((cx - s * 0.2 + d * s, cy + s * 0.25), (cx - s * 0.75 + d * s, cy + s * 1.45), '#ff6a2a', w=5, core='#fff0c0', g=8, k=0.8)


def prog(a, cx, cy, s, rnd):
    """the Prog: what a Brain makes of a human - a wiry chrome body lunging at you, a triangle head"""
    a.shadow(a.ell(cx, cy + s * 1.45, s * 0.7, s * 0.12), 0, 0, s * 0.1, 0.6)
    hip, neck = (cx + s * 0.05, cy + s * 0.45), (cx - s * 0.1, cy - s * 0.35)
    limbs = [[hip, (cx - s * 0.35, cy + s * 0.95), (cx - s * 0.55, cy + s * 1.42)],            # legs, mid-stride
             [hip, (cx + s * 0.45, cy + s * 0.95), (cx + s * 0.62, cy + s * 1.4)],
             [neck, (cx - s * 0.55, cy - s * 0.1), (cx - s * 0.95, cy - s * 0.35)],            # arms, reaching
             [neck, (cx + s * 0.45, cy + s * 0.05), (cx + s * 0.9, cy + s * 0.2)]]
    for L in limbs:
        a.solid(a.lines(L, s * 0.13), '#9aa0b4', bevel=s * 0.04, chrome=0.6, rim='#7affc8', spec=0.9, tex=0.2, rnd=rnd)
        a.solid(a.ell(*L[1], s * 0.1), '#5a6070', bevel=s * 0.04, chrome=0.5, spec=0.9)
    body = a.lines([neck, hip], s * 0.3)
    a.shadow(body, 6, 10, 8, 0.4)
    a.solid(body, '#7a8296', bevel=s * 0.1, chrome=0.6, rim='#7affc8', spec=0.8, tex=0.3, rnd=rnd)
    a.glow(a.ell(cx - s * 0.03, cy + s * 0.05, s * 0.08), C('#ff3aa8'), s * 0.1, 1.6)          # (the Brain's implant)
    hx, hy = neck[0] - s * 0.05, neck[1] - s * 0.42
    head = a.poly([(hx - s * 0.32, hy - s * 0.2), (hx + s * 0.32, hy - s * 0.2), (hx, hy + s * 0.32)])
    a.solid(head, '#c0c6d6', bevel=s * 0.08, chrome=0.7, rim='#ff3aa8', spec=1.0)
    for ex in (hx - s * 0.12, hx + s * 0.12):
        a.glow(a.ell(ex, hy - s * 0.06, s * 0.05), C('#ff2a2a'), s * 0.08, 2.4)


def quark(a, cx, cy, s, rnd):
    """the Quark: a shy pyramid of energy with a spine of light - it builds Tanks"""
    for r, c in ((1.55, '#2ad8ff'), (1.25, '#7a5aff'), (1.0, '#e0f8ff')):
        a.glow(a.poly([(cx, cy - s * r), (cx + s * r * 0.95, cy + s * r * 0.75), (cx - s * r * 0.95, cy + s * r * 0.75)]), C(c), s * 0.12, 0.45)
    m = a.poly([(cx, cy - s), (cx + s * 0.95, cy + s * 0.75), (cx - s * 0.95, cy + s * 0.75)])
    a.solid(m, '#3a9aff', bevel=s * 0.14, amb=0.5, chrome=0.55, sky=('#08103a', '#e0f4ff'), ground=('#100030', '#8a5aff'), spec=1.2)
    a.beam((cx, cy - s * 0.95), (cx, cy + s * 0.25), '#ffffff', w=s * 0.06, core='#ffffff', g=s * 0.08, k=0.9)
    a.flare(cx, cy - s * 0.25, s * 0.22, '#ffffff', 0.8)
    tank(a, cx + s * 1.15, cy + s * 1.15, s * 0.3, rnd)                 # (a Tank being built beside it)


def electrode_mine(a, cx, cy, s, rnd, k=1.0):
    """an electrode: a cross-shaped post of charged metal, crackling"""
    for ang in (0, math.pi / 2):
        dx, dy = math.cos(ang) * s, math.sin(ang) * s
        a.solid(a.lines([(cx - dx, cy - dy), (cx + dx, cy + dy)], s * 0.28), '#c8ccd8', bevel=s * 0.08, chrome=0.7, rim='#7ab8ff', spec=1.0)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a.glow(a.ell(cx + dx * s, cy + dy * s, s * 0.14), C('#7ab8ff'), s * 0.25, 1.6 * k)
    a.glow(a.ell(cx, cy, s * 0.2), C('#ffffff'), s * 0.3, 1.5 * k)
    for _ in range(int(6 * k)):                                        # (sparks jumping)
        ang = rnd.uniform(0, 2 * math.pi); r0 = s * rnd.uniform(0.9, 1.1)
        pts = [(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0)]
        for j in range(3):
            pts.append((pts[-1][0] + rnd.uniform(-s, s) * 0.35, pts[-1][1] + rnd.uniform(-s, s) * 0.35))
        a.glow(a.lines(pts, 1.4), C('#bfe0ff'), 2, 1.4 * k)


def electrode(a, cx, cy, s, rnd):
    electrode_mine(a, cx, cy, s, rnd)


def layer(a, cx, cy, s, rnd):
    """the mine layer: a hexagonal saucer that drops electrodes behind it and scuttles off"""
    for ex, ey in ((-1.25, 0.95), (-0.55, 1.35), (0.45, 1.5)):          # (the mines it left)
        electrode_mine(a, cx + ex * s, cy + ey * s, s * 0.22, rnd, k=0.75)
    hexm = a.poly(ngon(cx, cy, s * 1.0, 6, sy=0.62))
    a.shadow(hexm, 8, 16, 12, 0.5)
    a.solid(hexm, '#8a3a9a', bevel=s * 0.14, chrome=0.6, rim='#ffb36b', spec=0.9, tex=0.3, rnd=rnd)
    a.add(a.lines([(cx - s * 0.98, cy), (cx + s * 0.98, cy)], 3), C('#1a0820'), -0.6)
    for i in range(5):
        a.glow(a.ell(cx + (i - 2) * s * 0.3, cy + s * 0.18, s * 0.04), C('#ffe066'), s * 0.05, 1.6)
    dome = a.ell(cx, cy - s * 0.32, s * 0.36, s * 0.26) * (a.yy < cy - s * 0.12)
    a.solid(dome, '#c8a0ff', bevel=s * 0.08, chrome=0.7, spec=1.0, rim='#ffb36b')
    a.glow(a.ell(cx, cy - s * 0.36, s * 0.07), C('#ff2a2a'), s * 0.1, 2.2)


def praetorian(a, cx, cy, s, rnd):
    """the Praetorian: the elite guard - a gold armoured diamond with lances either side, charging"""
    for side in (-1, 1):
        a.solid(a.lines([(cx + side * s * 0.75, cy), (cx + side * s * 1.45, cy)], s * 0.12), '#d0d6e2', bevel=3, chrome=0.7, spec=1.0, rim='#ff5a2a')
        a.glow(a.ell(cx + side * s * 1.48, cy, s * 0.06), C('#ff7a2a'), s * 0.1, 2.0)
    m = a.poly([(cx, cy - s), (cx + s * 0.85, cy), (cx, cy + s), (cx - s * 0.85, cy)])
    a.shadow(m, 10, 16, 12, 0.5)
    a.solid(m, '#c9a23a', bevel=s * 0.14, chrome=0.7, sky=('#2a1040', '#fff2b0'), ground=('#3a1a00', '#ffb347'), spec=1.0,
            rim='#ff5a2a', tex=0.2, rnd=rnd)
    inner = a.poly([(cx, cy - s * 0.55), (cx + s * 0.45, cy), (cx, cy + s * 0.55), (cx - s * 0.45, cy)])
    a.solid(inner, '#7a1a10', bevel=s * 0.06, chrome=0.4, spec=0.7)
    a.glow(a.ell(cx, cy, s * 0.13, s * 0.08), C('#ff2a2a'), s * 0.15, 2.4)
    a.beam((cx + s * 0.2, cy + s * 0.9), (cx + s * 0.7, cy + s * 1.5), '#ffe066', w=4, g=6, k=0.7)   # (its aimed spark)


def splitter(a, cx, cy, s, rnd):
    """the Splitter: a diamond with a crack down its middle - shoot it and two shards fly"""
    crack = [(0.0, -1.0), (0.06, -0.35), (-0.08, 0.1), (0.05, 0.45), (0.0, 1.0)]
    for side in (-1, 1):                                               # (the halves, pulling apart along the crack)
        off = side * s * 0.06
        edge = [(cx + off + x * s, cy + y * s) for x, y in crack]
        m = a.poly(edge + [(cx + off + side * s * 0.78, cy)])
        a.shadow(m, 8, 14, 10, 0.45)
        a.solid(m, '#3ab878', bevel=s * 0.1, chrome=0.6, rim='#ffe066', spec=0.9, tex=0.25, rnd=rnd)
    cl = [(cx + x * s, cy + y * s) for x, y in crack]
    a.glow(a.lines(cl, 3), C('#ffe066'), s * 0.08, 2.0)
    a.add(a.lines(cl, 1.5), C('#ffffff'))
    for k, (dx, dy) in enumerate(((1.3, -0.75), (1.45, 0.55))):         # (two shards, already flying)
        tx, ty = cx + dx * s, cy + dy * s
        t = a.poly(ngon(tx, ty, s * 0.26, 3, a0=-math.pi / 2))
        a.glow(t, C('#ffe066'), s * 0.1, 0.8)
        a.solid(t, '#5ad89a', bevel=s * 0.05, chrome=0.6, spec=1.0, rim='#ffe066')
        a.beam((tx - s * 0.3, ty + (0.15 if k else -0.15) * s), (tx - s * 0.75, ty + (0.4 if k else -0.4) * s), '#ffe066', w=2, g=4, k=0.5)


def shieldbot(a, cx, cy, s, rnd):
    """the Shield bot: a cube behind a swinging shield - shots off the front bounce away"""
    body = a.rect(cx - s * 0.75, cy - s * 0.6, cx + s * 0.35, cy + s * 0.6, r=s * 0.1)
    a.shadow(body, 8, 14, 10, 0.5)
    a.solid(body, '#5a6a8a', bevel=s * 0.12, chrome=0.55, rim='#3ad7ff', spec=0.8, tex=0.35, rnd=rnd)
    a.glow(a.rect(cx - s * 0.5, cy - s * 0.12, cx + s * 0.1, cy - s * 0.02), C('#ff3030'), s * 0.06, 2.0)
    for i in range(3):
        a.add(a.lines([(cx - s * 0.65, cy + s * (0.2 + i * 0.12)), (cx + s * 0.25, cy + s * (0.2 + i * 0.12))], 2), C('#10141c'), -0.5)
    sh = np.clip(a.ell(cx + s * 0.1, cy, s * 0.95, s * 1.15) - a.ell(cx - s * 0.05, cy, s * 0.95, s * 1.2), 0, 1) * (a.xx > cx + s * 0.45)
    a.glow(sh, C('#3ad7ff'), s * 0.2, 1.4)
    a.solid(sh, '#9adfff', bevel=s * 0.05, chrome=0.6, spec=1.2, rim='#ffffff')
    for dy, ang in ((-0.5, -0.5), (0.35, 0.45)):                        # (shots glancing off)
        hx, hy = cx + s * 0.98, cy + dy * s
        a.burst(hx, hy, s * 0.12, rnd, cols=('#ffffff', '#9adfff', '#3ad7ff'), spikes=8)
        a.beam((hx + s * 0.05, hy), (hx + s * 0.7, hy + ang * s), '#ffe066', w=3, g=5, k=0.6)


def phaser(a, cx, cy, s, rnd):
    """the Phaser: two triangles of energy - solid one moment, half gone the next"""
    up = a.poly(ngon(cx, cy, s, 3, a0=-math.pi / 2))
    dn = a.poly(ngon(cx, cy, s, 3, a0=math.pi / 2))
    a.glow(np.maximum(up, dn), C('#b04aff'), s * 0.3, 0.6)
    a.solid(up, '#d05aff', bevel=s * 0.12, chrome=0.65, sky=('#200a40', '#f0e0ff'), ground=('#100020', '#ff7bd5'), spec=1.1)
    ghost = np.clip(dn - up * 0.6, 0, 1)                                # (the second, phasing out: scan lines through it)
    scan = (np.sin(a.yy * 0.9) > 0.2).astype(np.float32)
    a.add(ghost * scan, C('#7a5aff'), 0.55)
    a.add(np.clip(dn - gf(dn, 3), 0, 1) * 2.0, C('#e0c8ff'), 0.9)
    a.glow(a.ell(cx, cy, s * 0.12), C('#ffffff'), s * 0.15, 2.2)
    for _ in range(40):                                                # (the bits it is made of, drifting)
        x, y = cx + rnd.gauss(0, s * 0.9), cy + rnd.gauss(0, s * 0.9)
        a.glow(a.ell(x, y, 1.6), C('#e0c8ff'), 3, 1.2)


def sniper(a, cx, cy, s, rnd):
    """the Sniper: a square sight that locks a line on you, then fires down it"""
    a.beam((cx, cy), (cx + s * 1.6, cy + s * 1.9), '#ff2a2a', w=2, core='#ffd0d0', g=5, k=0.8)   # (the aiming line)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):                   # (the cross hairs)
        a.solid(a.lines([(cx, cy), (cx + dx * s * 1.25, cy + dy * s * 1.25)], s * 0.08), '#a0a8bc', bevel=2, chrome=0.6, spec=0.9, rim='#ff5a5a')
    fr = np.clip(a.rect(cx - s * 0.75, cy - s * 0.75, cx + s * 0.75, cy + s * 0.75, r=s * 0.06) -
                 a.rect(cx - s * 0.58, cy - s * 0.58, cx + s * 0.58, cy + s * 0.58, r=s * 0.04), 0, 1)
    a.shadow(fr, 8, 14, 10, 0.5)
    a.solid(fr, '#4a5266', bevel=s * 0.06, chrome=0.6, rim='#ff5a5a', spec=0.9, tex=0.3, rnd=rnd)
    a.solid(a.ell(cx, cy, s * 0.36), '#20242e', bevel=s * 0.1, chrome=0.5, spec=0.6)
    a.glow(a.ell(cx, cy, s * 0.16), C('#ff2a2a'), s * 0.2, 2.4)
    a.fill(a.ell(cx, cy, s * 0.06), C('#ffe0e0'))
    for k in range(1, 4):                                              # (the lens's rings)
        a.add(np.clip(a.ell(cx, cy, s * 0.1 * k) - a.ell(cx, cy, s * 0.1 * k - 1.5), 0, 1), C('#ff8a8a'), 0.4)


def orbiter(a, cx, cy, s, rnd):
    """the Orbiter: a hexagonal disc that circles you, closer and closer - it only has to touch"""
    oy = cy + s * 0.55
    for k in range(3):                                                 # (its orbit, a breathing ring of light)
        r = s * (1.5 - k * 0.3)
        ring = np.clip(a.ell(cx, oy, r, r * 0.38) - a.ell(cx, oy, r - 2, r * 0.38 - 2), 0, 1)
        a.glow(ring, C('#2affa0'), 4, 0.5 - k * 0.12)
    a.glow(a.ell(cx, oy, s * 0.06), C('#ffffff'), s * 0.1, 1.5)          # (you, at the middle)
    ox, oyy = cx + s * 0.5, cy - s * 0.2
    for k in range(5, 0, -1):                                          # (its trail)
        t = k * 0.16
        tx, ty = cx + s * 1.5 * math.cos(-0.5 + t), oy + s * 0.57 * math.sin(-0.5 + t) - s * 0.25
        a.glow(a.ell(tx, ty, s * 0.3 * (1 - k * 0.12)), C('#2affa0'), s * 0.1, 0.25)
    hexm = a.poly(ngon(ox, oyy, s * 0.78, 6))
    a.shadow(hexm, 8, 14, 10, 0.5)
    a.solid(hexm, '#2a8a6a', bevel=s * 0.12, chrome=0.6, rim='#c8ff7a', spec=1.0, tex=0.25, rnd=rnd)
    a.solid(a.lines([(ox, oyy), (ox + s * 0.76, oyy)], s * 0.12), '#d0f0e0', bevel=2, chrome=0.6, spec=1.0)
    a.glow(a.ell(ox, oyy, s * 0.12), C('#c8ff7a'), s * 0.15, 2.2)


def fence(a, cx, cy, s, rnd):
    """the laser fence: two posts and a lethal beam between them - shoot a post"""
    for side in (-1, 1):
        px = cx + side * s * 1.05
        post = a.rect(px - s * 0.32, cy - s * 0.1, px + s * 0.32, cy + s * 0.55, r=s * 0.05)
        a.shadow(post, 8, 14, 10, 0.5)
        a.solid(post, '#5a6070', bevel=s * 0.08, chrome=0.6, rim='#ff5a5a', spec=0.9, tex=0.35, rnd=rnd)
        a.solid(a.lines([(px, cy - s * 0.1), (px, cy - s * 0.65)], s * 0.07), '#c8ccd8', bevel=2, chrome=0.7, spec=1.0)
        a.glow(a.ell(px, cy - s * 0.68, s * 0.07), C('#ff3030'), s * 0.12, 2.4)
        a.glow(a.ell(px - side * s * 0.32, cy + s * 0.22, s * 0.08), C('#ff6a6a'), s * 0.1, 2.0)
    a.beam((cx - s * 0.75, cy + s * 0.22), (cx + s * 0.75, cy + s * 0.22), '#ff2a4a', w=7, g=10, k=1.1)
    for _ in range(12):                                                # (sparks off the beam)
        x = cx + rnd.uniform(-0.7, 0.7) * s
        a.glow(a.lines([(x, cy + s * 0.22), (x + rnd.uniform(-10, 10), cy + s * 0.22 + rnd.uniform(-20, 20))], 1.2), C('#ffd0d0'), 2, 1.2)


def centipede(a, cx, cy, s, rnd):
    """the Centipede: a head and a chain of hexagon segments - hit the middle and there are two"""
    path = [(cx + s * 1.05 - k * s * 0.36, cy + s * 0.35 + math.sin(k * 0.9 + 0.5) * s * 0.35) for k in range(8)]
    for k in range(len(path) - 1, 0, -1):                              # (tail first, behind)
        x, y = path[k]
        m = a.poly(ngon(x, y, s * 0.25, 6))
        a.shadow(m, 6, 12, 8, 0.35)
        a.solid(m, '#8a7a2a', bevel=s * 0.06, chrome=0.55, rim='#2affa0', spec=0.8, tex=0.3, rnd=rnd)
        for side in (-1, 1):
            a.add(a.lines([(x, y + side * s * 0.2), (x - s * 0.06, y + side * s * 0.36)], 2.2), C('#c8b060'), 0.8)
    hx, hy = path[0][0] + s * 0.1, path[0][1] - s * 0.05
    for side in (-1, 1):                                               # antennae
        a.solid(a.lines([(hx + side * s * 0.15, hy - s * 0.25), (hx + side * s * 0.45, hy - s * 0.7)], s * 0.05), '#d0d6e2', bevel=2, chrome=0.6, spec=1.0)
        a.glow(a.ell(hx + side * s * 0.46, hy - s * 0.72, s * 0.05), C('#2affa0'), s * 0.08, 2.2)
    head = a.poly(ngon(hx, hy, s * 0.36, 6))
    a.shadow(head, 8, 14, 10, 0.5)
    a.solid(head, '#c9a23a', bevel=s * 0.1, chrome=0.65, sky=('#2a1040', '#fff2b0'), ground=('#3a1a00', '#ffb347'), spec=1.0, rim='#2affa0')
    for ex in (hx - s * 0.13, hx + s * 0.13):
        a.glow(a.ell(ex, hy - s * 0.04, s * 0.06), C('#ff2a2a'), s * 0.08, 2.4)


CARDS = [
    ('bowtie', 'BOWTIE', 'FLAPS, GLIDES AND FIRES', bowtie, 'space', 11, 0.3, 0.42),
    ('strongbow', 'STRONG BOWTIE', 'IT AIMS WHERE YOU ARE GOING', strongbow, 'desert', 12, 0.3, 0.4),
    ('prog', 'PROG', 'WHAT A BRAIN MAKES OF A HUMAN', prog, 'arena', 13, 0.3, 0.38),
    ('quark', 'QUARK', 'IT BUILDS TANKS', quark, 'factory', 14, 0.26, 0.42),
    ('layer', 'MINE LAYER', 'SEVEN ELECTRODES TO DROP', layer, 'desert', 15, 0.28, 0.36),
    ('electrode', 'ELECTRODE', 'IT KILLS ON CONTACT', electrode, 'arena', 16, 0.3, 0.42),
    ('praetorian', 'PRAETORIAN', 'THE ELITE GUARD', praetorian, 'factory', 17, 0.3, 0.4),
    ('splitter', 'SPLITTER', 'SHOOT IT AND GET TWO', splitter, 'core', 18, 0.3, 0.42),
    ('shieldbot', 'SHIELD BOT', 'HIT IT IN THE FLANK', shieldbot, 'core', 19, 0.3, 0.42),
    ('phaser', 'PHASER', 'NOW YOU SEE IT', phaser, 'core', 20, 0.32, 0.42),
    ('sniper', 'SNIPER', 'ONE SHOT, NO SECOND AIM', sniper, 'core', 21, 0.3, 0.38),
    ('orbiter', 'ORBITER', 'IT ONLY HAS TO TOUCH YOU', orbiter, 'core', 22, 0.32, 0.4),
    ('fence', 'LASER FENCE', 'SHOOT A POST TO BREAK IT', fence, 'core', 23, 0.3, 0.45),
    ('centipede', 'CENTIPEDE', 'HIT THE MIDDLE, GET TWO', centipede, 'core', 24, 0.28, 0.42),
]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:]
    for key, name, sub, fn, kind, seed, sc, cy in CARDS:
        if not which or key in which:
            card(os.path.join(OUT, 'card_%s.png' % key), name, sub, fn, kind, seed, sc, cy)
            print(key, 'done', flush=True)
