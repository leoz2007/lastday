"""Moteur commun des capsules « GEN AI EN 2 MIN » (format vertical 1080x1920).

Contenu : palette, polices, helpers de dessin et d'animation, habillage permanent
(barre de progression, en-tête, pied), sous-titres, synthèse vocale ElevenLabs avec
alignement temporel, rendu par scène (skia -> ffmpeg rawvideo bgra), concaténation
et ajout de l'audio.

Chaque capsule est un module `capsules/capsuleNN.py` qui expose :
  NUM, TITLE (titre court affiché en en-tête), SLUG (nom de fichier), NEXT (str|None)
  SCENES : liste de dict(kind='open'|'content'|'end', text=str, draw=fonction)
La fonction draw(c, t, S) dessine l'illustration de la scène à l'instant absolu t ;
S.cue("mot") renvoie l'instant (absolu, en s) où le mot est prononcé dans la scène.
"""
import base64
import json
import math
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from multiprocessing import Pool

import skia

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
W, H, FPS = 1080, 1920, 30
LEAD = 0.5   # silence avant la voix (s)
TAIL = 1.0   # tenue après la voix (s)  -> vidéo = audio + 1,5 s

# ---------------------------------------------------------------- palette
def _c(h):
    h = h.lstrip('#')
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

RED = _c('f8485e')      # Red Poppy : accent unique
DARK = _c('3c3c3a')     # Dark Grey : texte
WHITE = _c('ffffff')
LIGHT = _c('efeeee')    # Light Grey : cartes
PL = _c('fca2ae')       # Poppy Light : barres / étiquettes / progressions
PLL = _c('fddade')      # Poppy Lighter : idem

# ---------------------------------------------------------------- polices
_TF = {n: skia.Typeface.MakeFromFile(os.path.join(ROOT, 'fonts', f'Montserrat-{n}.ttf'))
       for n in ('Light', 'Medium', 'Bold')}
_FONTS = {}

def font(weight, size):
    k = (weight, size)
    if k not in _FONTS:
        f = skia.Font(_TF[weight], size)
        f.setSubpixel(True)
        f.setEdging(skia.Font.Edging.kAntiAlias)
        _FONTS[k] = f
    return _FONTS[k]

def _paint(color, stroke=None):
    p = skia.Paint(AntiAlias=True, Color=color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p

# ---------------------------------------------------------------- animation
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def ease(x):  # ease-out cubique
    x = clamp(x)
    return 1 - (1 - x) ** 3

def ease_io(x):
    x = clamp(x)
    return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2

def back(x):  # léger dépassement
    x = clamp(x)
    c1 = 1.4
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2

def prog(t, at, dur=0.45):
    if at is None:
        return 1.0
    return clamp((t - at) / dur)

def lerp(a, b, p):
    return a + (b - a) * p

# ---------------------------------------------------------------- texte
def text_width(s, f, tracking=0.0):
    if not s:
        return 0.0
    ws = f.getWidths(f.textToGlyphs(s))
    return sum(ws) + tracking * (len(ws) - 1)

def _draw_run(c, s, x, y, f, color, tracking):
    if not s:
        return
    glyphs = f.textToGlyphs(s)
    ws = f.getWidths(glyphs)
    xs, acc = [], x
    for w in ws:
        xs.append(acc)
        acc += w + tracking
    blob = skia.TextBlob.MakeFromPosTextH(s, xs, y, f)
    c.drawTextBlob(blob, 0, 0, _paint(color))

NBSP = '\u00a0'

def glue(s):
    """Espaces insécables de la typographie française (« x », ? ! : ;)."""
    s = re.sub(r'«\s+', '«' + NBSP, s)
    s = re.sub(r'\s+([»?!:;])', NBSP + r'\1', s)
    return s

def _draw_word(c, w, x, y, f, color, accent, tr):
    for seg, acc in w:
        _draw_run(c, seg, x, y, f, accent if acc else color, tr)
        x += text_width(seg, f, tr) + tr
    return x - tr

def parse_rich(s):
    """'texte *accent*. texte' -> liste de mots ; un mot = liste de (segment, accent?)"""
    s = glue(s)
    words, cur, seg, acc = [], [], '', False
    for ch in s + ' ':
        if ch == '*':
            if seg:
                cur.append((seg, acc)); seg = ''
            acc = not acc
        elif ch.isspace() and ch != NBSP:
            if seg:
                cur.append((seg, acc)); seg = ''
            if cur:
                words.append(cur); cur = []
        else:
            seg += ch
    return words

def _wtext(w):
    return ''.join(x[0] for x in w) if isinstance(w, list) else w[0]

def wrap_rich(words, f, maxw, tracking=0.0):
    lines, cur = [], []
    sp = text_width(' ', f) + tracking
    for w in words:
        trial = cur + [w]
        width = sum(text_width(_wtext(x), f, tracking) for x in trial) + sp * (len(trial) - 1)
        if cur and width > maxw:
            lines.append(cur)
            cur = [w]
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines

def rich_line_width(line, f, tracking):
    sp = text_width(' ', f) + tracking
    return sum(text_width(_wtext(x), f, tracking) for x in line) + sp * (len(line) - 1)

def text_block(c, t, at, s, x, y, size, weight='Light', color=DARK, accent=RED,
               maxw=900, align='left', lh=1.18, tracking=None, stagger=0.08,
               max_lines=4, reveal=True):
    """Texte multi-lignes ; *mot* = accent. Apparition ligne par ligne par
    glissement sous masque (pas de transparence). y = ligne de base de la 1re ligne.
    Renvoie l'ordonnée sous le bloc."""
    f = font(weight, size)
    if tracking is None:
        tracking = -0.025 * size if weight == 'Light' else 0.0
    lines = wrap_rich(parse_rich(s), f, maxw, tracking)
    if len(lines) > max_lines:
        raise ValueError(f'Texte trop long ({len(lines)} lignes > {max_lines}) : {s}')
    step = size * lh
    sp = text_width(' ', f) + tracking
    for i, line in enumerate(lines):
        p = ease(prog(t, None if at is None else at + i * stagger, 0.5)) if reveal else 1.0
        if p <= 0:
            continue
        lw = rich_line_width(line, f, tracking)
        lx = x if align == 'left' else (x - lw / 2 if align == 'center' else x - lw)
        ly = y + i * step
        c.save()
        c.clipRect(skia.Rect(lx - 20, ly - size * 1.05, lx + lw + 20, ly + size * 0.32))
        oy = (1 - p) * size * 1.2
        cx = lx
        for w in line:
            cx = _draw_word(c, w, cx, ly + oy, f, color, accent, tracking) + sp
        c.restore()
    return y + len(lines) * step

def measure_lines(s, size, weight, maxw, tracking=None):
    f = font(weight, size)
    if tracking is None:
        tracking = -0.025 * size if weight == 'Light' else 0.0
    return len(wrap_rich(parse_rich(s), f, maxw, tracking))

def label(c, t, at, s, x, y, bg=PLL, fg=DARK, size=24, align='left'):
    """Étiquette : Bold capitales dans une pastille arrondie. (x,y) = coin haut gauche."""
    f = font('Bold', size)
    s = s.upper()
    tr = size * 0.12
    tw = text_width(s, f, tr)
    w, h = tw + size * 1.6, size * 2.0
    if align == 'center':
        x -= w / 2
    elif align == 'right':
        x -= w
    p = back(prog(t, at, 0.4))
    if p <= 0:
        return w
    c.save()
    c.translate(x, y + h / 2)
    c.scale(p, p)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, -h / 2, w, h / 2), h / 2, h / 2), _paint(bg))
    if p > 0.6:
        _draw_run(c, s, size * 0.8, size * 0.36, f, fg, tr)
    c.restore()
    return w

def rrect(c, x, y, w, h, r, color):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color))

def card(c, t, at, x, y, w, h, fill=LIGHT, r=36, mode='pop'):
    """Carte arrondie. mode 'pop' (zoom), 'up' (glisse depuis le bas), 'left', 'right'."""
    p = prog(t, at, 0.5)
    if p <= 0:
        return 0.0
    c.save()
    if mode == 'pop':
        k = back(p)
        c.translate(x + w / 2, y + h / 2)
        c.scale(k, k)
        c.translate(-(x + w / 2), -(y + h / 2))
    elif mode == 'up':
        c.translate(0, (1 - ease(p)) * 120)
        k = ease(p)
        c.translate(x + w / 2, y + h / 2); c.scale(0.9 + 0.1 * k, 0.9 + 0.1 * k); c.translate(-(x + w / 2), -(y + h / 2))
    elif mode in ('left', 'right'):
        d = -1 if mode == 'left' else 1
        c.translate(d * (1 - ease(p)) * 160, 0)
        k = ease(p)
        c.translate(x + w / 2, y + h / 2); c.scale(0.85 + 0.15 * k, 0.85 + 0.15 * k); c.translate(-(x + w / 2), -(y + h / 2))
    rrect(c, x, y, w, h, r, fill)
    c.restore()
    return p

def box(c, t, at, x, y, w, h, s, fill=LIGHT, fg=DARK, size=34, weight='Medium',
        r=30, mode='pop', accent=RED, lh=1.2):
    """Carte avec texte centré (multi-lignes)."""
    p = card(c, t, at, x, y, w, h, fill, r, mode)
    if p <= 0.35:
        return
    f = font(weight, size)
    tr = -0.025 * size if weight == 'Light' else 0
    lines = wrap_rich(parse_rich(s), f, w - 40, tr)
    n = len(lines)
    by = y + h / 2 - (n * size * lh) / 2 + size * 0.85
    if mode == 'up':
        by += (1 - ease(p)) * 120
    if mode in ('left', 'right'):
        pass
    for i, line in enumerate(lines):
        lw = rich_line_width(line, f, tr)
        cx = x + w / 2 - lw / 2
        dx = 0
        if mode in ('left', 'right'):
            dx = (-1 if mode == 'left' else 1) * (1 - ease(p)) * 160
        sp = text_width(' ', f) + tr
        for wd in line:
            cx = _draw_word(c, wd, cx + dx, by + i * size * lh, f, fg, accent, tr) - dx + sp

def bar(c, t, at, x, y, w, h, frac, fill=RED, bg=PLL, dur=0.9):
    """Barre qui se remplit (frac 0..1)."""
    if at is not None and t < at - 0.25:
        return
    rrect(c, x, y, w, h, h / 2, bg)
    p = ease_io(prog(t, at, dur)) * frac
    if p > 0:
        rrect(c, x, y, max(h, w * p), h, h / 2, fill)

def arrow(c, t, at, x1, y1, x2, y2, color=DARK, width=6, head=22, dur=0.45):
    p = ease(prog(t, at, dur))
    if p <= 0:
        return
    ex, ey = lerp(x1, x2, p), lerp(y1, y2, p)
    c.drawLine(x1, y1, ex, ey, _paint(color, width))
    if p > 0.5:
        a = math.atan2(y2 - y1, x2 - x1)
        path = skia.Path()
        path.moveTo(ex, ey)
        path.lineTo(ex - head * math.cos(a - 0.5), ey - head * math.sin(a - 0.5))
        path.lineTo(ex - head * math.cos(a + 0.5), ey - head * math.sin(a + 0.5))
        path.close()
        c.drawPath(path, _paint(color))

def dot(c, t, at, x, y, r, color=RED):
    p = back(prog(t, at, 0.35))
    if p > 0:
        c.drawCircle(x, y, r * p, _paint(color))

def ring(c, x, y, r, color, width):
    c.drawCircle(x, y, r, _paint(color, width))

def chip(c, t, at, s, x, y, fill=PLL, fg=DARK, size=34, weight='Medium', padx=22, h=None,
         align='left'):
    """Pastille de texte (ex. un token). Renvoie sa largeur."""
    f = font(weight, size)
    tw = text_width(s, f)
    w = tw + 2 * padx
    h = h or size * 1.75
    if align == 'center':
        x -= w / 2
    p = back(prog(t, at, 0.35))
    if p > 0:
        c.save()
        c.translate(x + w / 2, y + h / 2)
        c.scale(p, p)
        rrect(c, -w / 2, -h / 2, w, h, 18, fill)
        if p > 0.5:
            _draw_run(c, s, -tw / 2, size * 0.36, f, fg, 0)
        c.restore()
    return w

def chip_width(s, size=34, weight='Medium', padx=22):
    return text_width(s, font(weight, size)) + 2 * padx

def flow_chips(c, t, items, x, y, maxw, size=34, gap=14, line_h=None, **kw):
    """items = [(texte, at, fill, fg)] disposés en lignes."""
    line_h = line_h or size * 1.75 + gap
    cx, cy = x, y
    for it in items:
        s, at = it[0], it[1]
        fill = it[2] if len(it) > 2 else PLL
        fg = it[3] if len(it) > 3 else DARK
        w = chip_width(s, size)
        if cx + w > x + maxw and cx > x:
            cx, cy = x, cy + line_h
        chip(c, t, at, s, cx, cy, fill, fg, size, **kw)
        cx += w + gap
    return cy + line_h

def check_row(c, t, at, x, y, w, s, num, size=34, fill=LIGHT, accent=RED, h=None):
    """Ligne de checklist : carte + pastille numérotée + texte (2 lignes max)."""
    f = font('Medium', size)
    lines = wrap_rich(parse_rich(s), f, w - 150, 0)
    if len(lines) > 2:
        raise ValueError('check_row trop long : ' + s)
    h = h or (size * 1.25 * len(lines) + 56)
    p = card(c, t, at, x, y, w, h, fill, 30, 'left')
    if p <= 0.3:
        return h
    dx = -(1 - ease(p)) * 160
    cy = y + h / 2
    c.drawCircle(x + 62 + dx, cy, 30, _paint(accent))
    nf = font('Bold', 28)
    ns = str(num)
    _draw_run(c, ns, x + 62 + dx - text_width(ns, nf) / 2, cy + 10, nf, WHITE, 0)
    by = cy - (len(lines) * size * 1.25) / 2 + size * 0.9
    for i, line in enumerate(lines):
        cx = x + 118 + dx
        sp = text_width(' ', f)
        for wd in line:
            cx = _draw_word(c, wd, cx, by + i * size * 1.25, f, DARK, accent, 0) + sp
    return h

def small(c, s, x, y, size=26, color=DARK, weight='Bold', align='left', tracking=None, upper=True):
    f = font(weight, size)
    if upper:
        s = s.upper()
    tr = size * 0.1 if tracking is None else tracking
    tw = text_width(s, f, tr)
    if align == 'center':
        x -= tw / 2
    elif align == 'right':
        x -= tw
    _draw_run(c, s, x, y, f, color, tr)
    return tw

def plain(c, s, x, y, size=32, color=DARK, weight='Medium', align='left'):
    """Texte simple sans animation (1 ligne)."""
    f = font(weight, size)
    tr = -0.025 * size if weight == 'Light' else 0
    tw = text_width(s, f, tr)
    if align == 'center':
        x -= tw / 2
    elif align == 'right':
        x -= tw
    _draw_run(c, s, x, y, f, color, tr)
    return tw

def reveal_plain(c, t, at, s, x, y, size=32, color=DARK, weight='Medium', align='left'):
    """1 ligne qui monte sous masque."""
    p = ease(prog(t, at, 0.45))
    if p <= 0:
        return
    f = font(weight, size)
    tr = -0.025 * size if weight == 'Light' else 0
    tw = text_width(s, f, tr)
    lx = x - tw / 2 if align == 'center' else (x - tw if align == 'right' else x)
    c.save()
    c.clipRect(skia.Rect(lx - 10, y - size * 1.05, lx + tw + 10, y + size * 0.32))
    _draw_run(c, s, lx, y + (1 - p) * size * 1.2, f, color, tr)
    c.restore()

# ---------------------------------------------------------------- icônes simples
def icon(c, t, at, kind, cx, cy, s=80, color=DARK, bg=None):
    """Pictos géométriques simples (traits arrondis)."""
    p = back(prog(t, at, 0.4))
    if p <= 0:
        return
    c.save()
    c.translate(cx, cy)
    c.scale(p * s / 100, p * s / 100)
    st = _paint(color, 8)
    fl = _paint(color)
    if bg is not None:
        c.drawCircle(0, 0, 70, _paint(bg))
    if kind == 'doc':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-32, -42, 32, 42), 10, 10), st)
        for yy in (-18, 0, 18):
            c.drawLine(-18, yy, 18, yy, st)
    elif kind == 'search':
        c.drawCircle(-8, -8, 26, st)
        c.drawLine(12, 12, 36, 36, _paint(color, 12))
    elif kind == 'gear':
        for i in range(8):
            a = i * math.pi / 4
            c.drawLine(28 * math.cos(a), 28 * math.sin(a), 42 * math.cos(a), 42 * math.sin(a), _paint(color, 14))
        c.drawCircle(0, 0, 28, st)
        c.drawCircle(0, 0, 10, fl)
    elif kind == 'user':
        c.drawCircle(0, -18, 20, st)
        path = skia.Path()
        path.addArc(skia.Rect(-38, 10, 38, 80), 180, 180)
        c.drawPath(path, st)
    elif kind == 'chat':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-42, -34, 42, 24), 16, 16), st)
        path = skia.Path(); path.moveTo(-18, 24); path.lineTo(-26, 42); path.lineTo(0, 24)
        c.drawPath(path, st)
    elif kind == 'db':
        c.drawOval(skia.Rect(-36, -44, 36, -20), st)
        c.drawLine(-36, -32, -36, 32, st); c.drawLine(36, -32, 36, 32, st)
        path = skia.Path(); path.addArc(skia.Rect(-36, -12, 36, 12), 0, 180); c.drawPath(path, st)
        path = skia.Path(); path.addArc(skia.Rect(-36, 20, 36, 44), 0, 180); c.drawPath(path, st)
    elif kind == 'shield':
        path = skia.Path()
        path.moveTo(0, -44); path.lineTo(36, -30); path.lineTo(32, 10)
        path.quadTo(24, 34, 0, 46); path.quadTo(-24, 34, -32, 10); path.lineTo(-36, -30); path.close()
        c.drawPath(path, st)
        c.drawLine(-12, 2, -2, 14, st); c.drawLine(-2, 14, 16, -10, st)
    elif kind == 'check':
        c.drawLine(-28, 2, -8, 24, _paint(color, 12)); c.drawLine(-8, 24, 30, -22, _paint(color, 12))
    elif kind == 'cross':
        c.drawLine(-24, -24, 24, 24, _paint(color, 12)); c.drawLine(24, -24, -24, 24, _paint(color, 12))
    elif kind == 'clock':
        c.drawCircle(0, 0, 40, st); c.drawLine(0, 0, 0, -24, st); c.drawLine(0, 0, 18, 8, st)
    elif kind == 'coin':
        c.drawCircle(0, 0, 40, st); c.drawCircle(0, 0, 24, st)
    elif kind == 'lock':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-34, -6, 34, 44), 10, 10), st)
        path = skia.Path(); path.addArc(skia.Rect(-22, -44, 22, 4), 180, 180); c.drawPath(path, st)
        c.drawLine(-22, -20, -22, -6, st); c.drawLine(22, -20, 22, -6, st)
    elif kind == 'brain':
        c.drawCircle(-14, -10, 24, st); c.drawCircle(14, -10, 24, st)
        c.drawCircle(-14, 14, 22, st); c.drawCircle(14, 14, 22, st)
    elif kind == 'bolt':
        path = skia.Path(); path.moveTo(8, -46); path.lineTo(-24, 6); path.lineTo(0, 6)
        path.lineTo(-8, 46); path.lineTo(24, -6); path.lineTo(0, -6); path.close()
        c.drawPath(path, fl)
    elif kind == 'code':
        c.drawLine(-14, -26, -38, 0, st); c.drawLine(-38, 0, -14, 26, st)
        c.drawLine(14, -26, 38, 0, st); c.drawLine(38, 0, 14, 26, st)
    elif kind == 'eye':
        path = skia.Path(); path.moveTo(-44, 0); path.quadTo(0, -40, 44, 0); path.quadTo(0, 40, -44, 0)
        c.drawPath(path, st); c.drawCircle(0, 0, 12, fl)
    elif kind == 'target':
        c.drawCircle(0, 0, 40, st); c.drawCircle(0, 0, 22, st); c.drawCircle(0, 0, 6, fl)
    c.restore()

# ---------------------------------------------------------------- alignement
class Timeline:
    """Texte complet + temps de début/fin par caractère (alignement ElevenLabs)."""

    def __init__(self, text, align):
        chars = align['characters']
        st = align['character_start_times_seconds']
        en = align['character_end_times_seconds']
        aligned = ''.join(chars)
        if aligned != text:
            # Remappe par correspondance de séquences si l'API a normalisé le texte.
            import difflib
            sm = difflib.SequenceMatcher(None, text, aligned, autojunk=False)
            s2, e2 = [None] * len(text), [None] * len(text)
            for a, b, n in sm.get_matching_blocks():
                for k in range(n):
                    s2[a + k], e2[a + k] = st[b + k], en[b + k]
            last = 0.0
            for i in range(len(text)):
                if s2[i] is None:
                    s2[i], e2[i] = last, last
                last = e2[i]
            st, en = s2, e2
        self.text = text
        self.st = [x + LEAD for x in st]
        self.en = [x + LEAD for x in en]
        self.words = []  # (mot, i0, i1, t0, t1)
        raw = [(m.group(), m.start(), m.end() - 1) for m in re.finditer(r'\S+', text)]
        merged = []
        for w, i0, i1 in raw:
            if merged and (re.fullmatch(r'[»?!:;]', w) or merged[-1][0].endswith('«')):
                pw, p0, _ = merged[-1]
                merged[-1] = (pw + NBSP + w, p0, i1)
            else:
                merged.append((w, i0, i1))
        for w, i0, i1 in merged:
            self.words.append((w, i0, i1, self.st[i0], self.en[i1]))

    def time_at(self, idx):
        return self.st[idx]


class Scene:
    def __init__(self, idx, spec, tl, offset):
        self.idx = idx
        self.spec = spec
        self.kind = spec['kind']
        self.text = spec['text']
        self.tl = tl
        self.off = offset  # index du 1er caractère de la scène dans le texte complet
        self.speech0 = tl.st[offset]
        self.t0 = self.t1 = 0.0
        self._cache = {}

    def cue(self, word, nth=1, shift=0.0):
        """Instant où `word` (sous-chaîne, insensible à la casse) est prononcé
        pour la nth-ième fois dans le texte de la scène."""
        k = (word, nth)
        if k not in self._cache:
            low = self.text.lower()
            pos = -1
            for _ in range(nth):
                pos = low.find(word.lower(), pos + 1)
                if pos < 0:
                    raise KeyError(f'Scène {self.idx + 1} : mot clé introuvable « {word} »')
            self._cache[k] = self.tl.st[self.off + pos]
        return self._cache[k] + shift

    @property
    def start(self):
        return self.speech0


def build_subs(tl, scenes, size=42, maxw=920, max_lines=2):
    """Blocs de sous-titres de 2 lignes max : découpe par phrase, puis répartition
    équilibrée des mots ; regroupe les phrases courtes."""
    f = font('Medium', size)

    def nlines(ws):
        return len(wrap_rich([[(x[0], False)] for x in ws], f, maxw))

    def split_balanced(ws):
        if nlines(ws) <= max_lines:
            return [ws]
        best = None
        for i in range(1, len(ws)):
            l, r = ws[:i], ws[i:]
            if nlines(l) <= max_lines and nlines(r) <= max_lines:
                diff = abs(sum(len(x[0]) for x in l) - sum(len(x[0]) for x in r))
                score = diff - (60 if re.search(r'[,:;]$', l[-1][0]) else 0)
                if best is None or score < best[0]:
                    best = (score, [l, r])
        if best:
            return best[1]
        for k in range(1, len(ws) + 1):
            total = sum(len(x[0]) + 1 for x in ws)
            parts, cur, acc = [], [], 0
            for x in ws:
                cur.append(x)
                acc += len(x[0]) + 1
                if acc >= total * (len(parts) + 1) / k and len(parts) < k - 1:
                    parts.append(cur); cur = []
            if cur:
                parts.append(cur)
            if all(nlines(p) <= max_lines for p in parts):
                return parts
        return [[x] for x in ws]

    chunks = []
    for sc in scenes:
        a, b = sc.off, sc.off + len(sc.text)
        ws = [w for w in tl.words if a <= w[1] < b]
        sentences, cur = [], []
        for w in ws:
            cur.append(w)
            if re.search(r'[.?!]$', w[0]):
                sentences.append(cur); cur = []
        if cur:
            sentences.append(cur)
        pending = []
        for sent in sentences:
            parts = split_balanced(sent)
            for p in parts:
                if pending and nlines(pending + p) <= max_lines:
                    pending = pending + p
                else:
                    if pending:
                        chunks.append(pending)
                    pending = p
        if pending:
            chunks.append(pending)
    out = []
    for i, ch in enumerate(chunks):
        t0 = ch[0][3]
        t1 = chunks[i + 1][0][3] if i + 1 < len(chunks) else ch[-1][4] + 0.6
        t1 = min(t1, ch[-1][4] + 1.2)
        txt = ' '.join(x[0] for x in ch)
        out.append((t0, t1, txt))
    return out


def draw_subs(c, t, subs, color, size=42, cy=1600, maxw=920):
    f = font('Medium', size)
    for t0, t1, txt in subs:
        if t0 <= t < t1:
            words = [[(w, False)] for w in txt.split(' ')]
            lines = wrap_rich(words, f, maxw)
            if len(lines) == 2:  # équilibre les deux lignes
                best = None
                for k in range(1, len(words)):
                    l1, l2 = words[:k], words[k:]
                    w1, w2 = rich_line_width(l1, f, 0), rich_line_width(l2, f, 0)
                    if max(w1, w2) <= maxw:
                        sc = abs(w1 - w2) - (120 if re.search(r'[,:;.?]$', l1[-1][0][0]) else 0)
                        if best is None or sc < best[0]:
                            best = (sc, [l1, l2])
                if best:
                    lines = best[1]
            lh = size * 1.3
            y0 = cy - (len(lines) - 1) * lh / 2 + size * 0.35
            for i, ln in enumerate(lines):
                s = ' '.join(_wtext(w) for w in ln)
                plain(c, s, W / 2, y0 + i * lh, size, color, 'Medium', 'center')
            return

# ---------------------------------------------------------------- habillage
def draw_chrome(c, cap, idx, p_scene, kind):
    if kind == 'open':
        fg, on, off = WHITE, RED, PL
    elif kind == 'end':
        fg, on, off = WHITE, WHITE, PL
    else:
        fg, on, off = DARK, RED, PLL
    # barre de progression 7 segments
    n, x0, x1, y, h, gap = 7, 60, W - 60, 72, 10, 12
    sw = (x1 - x0 - gap * (n - 1)) / n
    for i in range(n):
        sx = x0 + i * (sw + gap)
        rrect(c, sx, y, sw, h, h / 2, off)
        fr = 1.0 if i < idx else (p_scene if i == idx else 0.0)
        if fr > 0:
            rrect(c, sx, y, max(h, sw * fr), h, h / 2, on)
    small(c, 'GEN AI EN 2 MIN', 60, 140, 24, fg)
    small(c, f'{cap.NUM:02d} · {cap.TITLE}', W - 60, 140, 24, fg, align='right')
    small(c, 'DEVOTEAM AI APPS', W / 2, 1862, 24, fg, align='center')


BG = {'open': DARK, 'content': WHITE, 'end': RED}
SUB = {'open': WHITE, 'content': DARK, 'end': WHITE}

# ---------------------------------------------------------------- synthèse vocale
VOICE_ID = 'VuE88ydpXAhBTNxFI7WF'   # Julien - Friendly French Tech Explainer
MODELS = ['eleven_v4', 'eleven_multilingual_v2']


def tts(text, mp3_path, json_path):
    """Une seule génération réussie par capsule : si les fichiers existent, on ne
    régénère pas."""
    if os.path.exists(mp3_path) and os.path.exists(json_path):
        print('  audio déjà présent, pas de nouvelle génération')
        return json.load(open(json_path))
    key = os.environ.get('ELEVENLABS_API_KEY')
    if not key:
        sys.exit('ELEVENLABS_API_KEY absente')
    last_err = None
    for model in MODELS:
        for fmt in ('mp3_44100_192', 'mp3_44100_128'):
            url = (f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps'
                   f'?output_format={fmt}')
            body = json.dumps({'text': text, 'model_id': model, 'language_code': 'fr'}).encode()
            req = urllib.request.Request(url, data=body, method='POST', headers={
                'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    d = json.load(r)
            except urllib.error.HTTPError as e:
                msg = e.read().decode('utf-8', 'replace')[:300]
                last_err = f'{model}/{fmt}: HTTP {e.code} {msg}'
                print('  refus API :', last_err)
                if e.code in (401, 429) or e.code >= 500:
                    sys.exit('Arrêt : ' + last_err)
                continue
            audio = base64.b64decode(d['audio_base64'])
            with open(mp3_path, 'wb') as fh:
                fh.write(audio)
            meta = {'model_id': model, 'output_format': fmt, 'voice_id': VOICE_ID,
                    'text': text, 'alignment': d['alignment'],
                    'normalized_alignment': d.get('normalized_alignment')}
            with open(json_path, 'w') as fh:
                json.dump(meta, fh, ensure_ascii=False)
            print(f'  voix générée avec {model} ({fmt})')
            return meta
    sys.exit('Échec de la synthèse : ' + str(last_err))


def audio_duration(path):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                   '-of', 'csv=p=0', path])
    return float(out.strip())

# ---------------------------------------------------------------- rendu
_STATE = {}


def _render_scene(i):
    cap, scenes, subs, total = _STATE['cap'], _STATE['scenes'], _STATE['subs'], _STATE['total']
    sc = scenes[i]
    f0, f1 = round(sc.t0 * FPS), round(sc.t1 * FPS)
    path = os.path.join(_STATE['tmp'], f'scene{i + 1}.mp4')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra',
           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
           '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS), path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    for fr in range(f0, f1):
        t = fr / FPS
        c.clear(BG[sc.kind])
        sc.spec['draw'](c, t, sc)
        p_scene = clamp((t - sc.t0) / max(0.01, sc.t1 - sc.t0))
        draw_chrome(c, cap, i, p_scene, sc.kind)
        draw_subs(c, t, subs, SUB[sc.kind])
        proc.stdin.write(surf.toarray().tobytes())  # BGRA -> -pix_fmt bgra
    proc.stdin.close()
    proc.wait()
    return path


def render(cap, only_frames=None):
    num = f'{cap.NUM:02d}'
    audio_dir = os.path.join(ROOT, 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    mp3 = os.path.join(audio_dir, f'capsule{num}.mp3')
    js = os.path.join(audio_dir, f'capsule{num}.json')
    full = ' '.join(s['text'].strip() for s in cap.SCENES)
    nwords = len(full.split())
    print(f'Capsule {num} : {nwords} mots')
    fake = bool(os.environ.get('FAKE_TTS'))
    if fake:  # maquette sans appel API : alignement uniforme
        n = len(full)
        meta = {'text': full, 'alignment': {'characters': list(full),
                'character_start_times_seconds': [i * 0.062 for i in range(n)],
                'character_end_times_seconds': [(i + 1) * 0.062 for i in range(n)]}}
    else:
        meta = tts(full, mp3, js)
    if meta['text'] != full:
        print('  ATTENTION : le texte a changé depuis la génération ; on garde l\'audio existant')
        full = meta['text']
    tl = Timeline(full, meta['alignment'])
    adur = len(full) * 0.062 if fake else audio_duration(mp3)
    total = LEAD + adur + TAIL
    scenes, off = [], 0
    for i, s in enumerate(cap.SCENES):
        txt = s['text'].strip()
        pos = full.find(txt, off)
        if pos < 0:
            raise ValueError('scène introuvable dans le texte audio')
        scenes.append(Scene(i, dict(s, text=txt), tl, pos))
        off = pos + len(txt)
    for i, sc in enumerate(scenes):
        sc.t0 = 0.0 if i == 0 else max(scenes[i - 1].speech0 + 0.5, sc.speech0 - 0.15)
    for i, sc in enumerate(scenes):
        sc.t1 = scenes[i + 1].t0 if i + 1 < len(scenes) else total
    subs = build_subs(tl, scenes)
    tmp = os.path.join(ROOT, 'build', f'capsule{num}')
    os.makedirs(tmp, exist_ok=True)
    with open(os.path.join(tmp, 'timing.json'), 'w') as fh:
        json.dump({'audio': adur, 'total': total,
                   'scenes': [[sc.t0, sc.t1] for sc in scenes],
                   'subs': subs}, fh, ensure_ascii=False, indent=1)
    _STATE.update(cap=cap, scenes=scenes, subs=subs, total=total, tmp=tmp)

    if only_frames:  # aperçu rapide d'images isolées
        surf = skia.Surface(W, H)
        c = surf.getCanvas()
        for t in only_frames:
            sc = next(s for s in scenes if s.t0 <= t < s.t1)
            c.clear(BG[sc.kind])
            sc.spec['draw'](c, t, sc)
            draw_chrome(c, cap, sc.idx, clamp((t - sc.t0) / (sc.t1 - sc.t0)), sc.kind)
            draw_subs(c, t, subs, SUB[sc.kind])
            surf.makeImageSnapshot().save(os.path.join(tmp, f'preview_{t:06.2f}.png'))
        return

    with Pool(min(4, os.cpu_count() or 2)) as pool:
        parts = pool.map(_render_scene, range(len(scenes)))
    lst = os.path.join(tmp, 'concat.txt')
    with open(lst, 'w') as fh:
        for p in parts:
            fh.write(f"file '{p}'\n")
    silent = os.path.join(tmp, 'video.mp4')
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
                           '-i', lst, '-c', 'copy', silent])
    out_dir = os.path.join(REPO, 'out')
    os.makedirs(out_dir, exist_ok=True)
    final = os.path.join(out_dir, f'capsule{num}_{cap.SLUG}.mp4')
    delay = int(LEAD * 1000)
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', mp3,
                           '-filter_complex', f'[1:a]adelay={delay}|{delay},apad[a]',
                           '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac',
                           '-b:a', '192k', '-shortest', '-movflags', '+faststart', final])
    print('  ->', final)
    return final


def write_script_md(cap):
    num = f'{cap.NUM:02d}'
    lines = [f'# Capsule {num} · {cap.FULL_TITLE}', '',
             f'Texte de la voix off ({len(" ".join(s["text"] for s in cap.SCENES).split())} mots).', '']
    names = {'open': 'Accroche', 'end': 'À retenir'}
    for i, s in enumerate(cap.SCENES):
        nm = s.get('name') or names.get(s['kind'], 'Explication')
        lines += [f'## Scène {i + 1} · {nm}', '', s['text'].strip(), '']
    os.makedirs(os.path.join(REPO, 'scripts'), exist_ok=True)
    with open(os.path.join(REPO, 'scripts', f'capsule{num}.md'), 'w') as fh:
        fh.write('\n'.join(lines))

# ---------------------------------------------------------------- gabarits de scènes
def header(c, t, S, lab, title, at_title=None, size=80, y_label=250, y_title=400, max_lines=2):
    """Étiquette + titre d'une scène de contenu. Renvoie l'ordonnée sous le titre."""
    a = S.t0 + 0.1
    label(c, t, a, lab, 90, y_label, PLL, DARK)
    return text_block(c, t, at_title or a + 0.15, title, 90, y_title, size, 'Light', DARK,
                      RED, maxw=900, max_lines=max_lines)


def opening(c, t, S, cap, title, size=96):
    a = S.t0 + 0.15
    label(c, t, a, f'CAPSULE {cap.NUM:02d}', 90, 300, RED, WHITE)
    return text_block(c, t, a + 0.25, title, 90, 470, size, 'Light', WHITE, RED,
                      maxw=900, max_lines=3, stagger=0.12)


def questions(c, t, S, title, items, y0=600, gap=36, size=36):
    """items = [(texte, mot_clé)]"""
    header(c, t, S, 'Au cadrage', title)
    y = y0
    for i, (s, kw) in enumerate(items):
        h = check_row(c, t, S.cue(kw), 90, y, 900, s, i + 1, size)
        y += h + gap
    # pictogramme de cadrage
    icon(c, t, S.cue(items[0][1]), 'target', 940, 290, 70, RED)


def ending(c, t, S, cap, cards, next_title=None):
    """Scène finale sur fond Red Poppy. cards = [(texte, mot_clé)]"""
    a = S.t0 + 0.1
    label(c, t, a, 'À retenir', 90, 250, WHITE, RED)
    y = 360
    for s, kw in cards:
        at = S.cue(kw)
        n = measure_lines(s, 44, 'Medium', 780)
        h = n * 44 * 1.25 + 70
        card(c, t, at, 90, y, 900, h, WHITE, 36, 'up')
        if prog(t, at, 0.5) > 0.3:
            dy = (1 - ease(prog(t, at, 0.5))) * 120
            c.drawCircle(150, y + h / 2 + dy, 14, _paint(RED))
            text_block(c, t, None, s, 190, y + 35 + 44 * 0.9 + dy, 44, 'Medium', DARK, RED,
                       maxw=780, max_lines=3, reveal=False)
        y += h + 30
    # la série : 10 pastilles
    at = S.cue(cap.NEXT_CUE) if cap.NEXT_CUE else S.t0 + 1.0
    yy = max(y + 70, 1180)
    small(c, 'La série', 90, yy, 24, WHITE)
    for k in range(10):
        x = 90 + 22 + k * 88
        col = WHITE if k + 1 <= cap.NUM else PL
        dot(c, t, a + 0.3 + k * 0.05, x, yy + 50, 22 if k + 1 == cap.NUM else 16, col)
    if next_title:
        bw = 900
        box(c, t, at, 90, yy + 150, bw, 150, next_title, WHITE, RED, 40, 'Medium', 36, 'up')
        if prog(t, at, 0.5) > 0.6:
            small(c, 'Prochaine capsule', 90, yy + 130, 22, WHITE)
