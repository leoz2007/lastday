from engine import *  # noqa
from engine import _paint  # noqa

NUM = 33
TITLE = 'ATTENTION'
FULL_TITLE = 'Transformers et attention'
SLUG = 'transformers_attention'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def avocado(c, t, at, cx, cy, s=1.0):
    """Un avocat coupé : ovale clair, noyau sombre."""
    p = back(prog(t, at, 0.4))
    if p <= 0:
        return
    k = p * s
    c.drawOval(skia.Rect(cx - 34 * k, cy - 46 * k, cx + 34 * k, cy + 46 * k), _paint(PL))
    c.drawCircle(cx, cy + 10 * k, 16 * k, _paint(DARK))


def s1(c, t, S):
    opening(c, t, S, CAP, 'Il sait à qui renvoie « *il* ».')
    a = S.cue('la cliente')
    text_block(c, t, a, 'La cliente a rappelé le vendeur, car *il* avait oublié la livraison.',
               90, 820, 44, 'Light', WHITE, RED, maxw=900, max_lines=2)
    cands = [('cliente', 220, 0.12), ('vendeur', 540, 0.8), ('livraison', 860, 0.08)]
    for k, (s, cx, w) in enumerate(cands):
        chip(c, t, a + 0.4 + k * 0.15, s, cx, 1010, WHITE, DARK, 34, align='center')
    r = S.cue('relie')
    v = S.cue('au vendeur')
    chip(c, t, r - 0.3, 'il', 540, 1300, RED, WHITE, 40, align='center')
    for k, (s, cx, w) in enumerate(cands):
        hot = k == 1 and t >= v
        arrow(c, t, r + k * 0.15, 540, 1290, cx, 1085, RED if hot else PL,
              4 + 14 * w, 18 if k != 1 else 30)
    if t >= v:
        reveal_plain(c, t, v, 'Exemple illustratif', 990, 1430, 22, WHITE, 'Medium', 'right')


def s2(c, t, S):
    header(c, t, S, "L'attention", 'Chaque mot *précise* son sens')
    rows = [('Au tribunal', 'tribunal', 'une personne', 'Une personne', 'user'),
            ('Une salade', 'salade', 'un fruit', 'Un fruit', None)]
    cm = S.cue('Chaque mot regarde')
    for k, (ctx, kw, kr, res, ic) in enumerate(rows):
        a0 = cm + k * 0.3
        at = S.cue(kw)
        y = 560 + k * 380
        card(c, t, a0, 90, y, 900, 340, LIGHT, 36, 'up')
        if prog(t, a0, 0.5) > 0.4:
            small(c, 'Phrase', 140, y + 60, 20, DARK)
            chip(c, t, a0 + 0.2, 'avocat', 660, y + 95, DARK, WHITE, 34)
            w1 = chip(c, t, at, ctx, 140, y + 95, PLL, DARK, 34)
            arrow(c, t, at + 0.2, 650, y + 125, 140 + w1 + 20, y + 125, RED, 6, 20)
            if t >= at + 0.2:
                small(c, 'Regarde', 140 + w1 + 30, y + 85, 18, RED)
            r = S.cue(kr)
            if a0 + 0.4 <= t < r:
                plain(c, '?', 720, y + 285, 44, DARK, 'Medium', 'center')
            arrow(c, t, r - 0.1, 720, y + 165, 720, y + 215, DARK, 5, 16)
            if ic:
                icon(c, t, r, ic, 660, y + 270, 56, RED)
            else:
                avocado(c, t, r, 660, y + 268, 0.75)
            if t >= r:
                reveal_plain(c, t, r + 0.1, res, 715, y + 285, 36, DARK, 'Medium')
    f = S.cue('Prenez')
    if t >= f:
        reveal_plain(c, t, f, 'Le même mot, deux sens', 540, 1400, 34, RED, 'Medium', 'center')


def s3(c, t, S):
    header(c, t, S, 'Les couches', 'Une représentation *affinée*')
    e = S.cue('empile')
    chip(c, t, S.t0 + 0.4, '« avocat »', 370, 1370, DARK, WHITE, 32, align='center')
    layers = [('Couche basse', 'la forme', 'Forme', 2),
              ('Couche du milieu', 'le sens', 'Sens', 5),
              ('Couche haute', 'les liens', 'Liens', 8)]
    for k, (nm, kw, lab, nred) in enumerate(layers):
        y = 1170 - k * 190
        arrow(c, t, e + k * 0.3, 370, y + (195 if k == 0 else 185), 370, y + 140, DARK, 5, 14)
        card(c, t, e + k * 0.3, 90, y, 560, 130, LIGHT, 30, 'up')
        if prog(t, e + k * 0.3, 0.5) > 0.4:
            small(c, nm, 130, y + 50, 18, DARK)
            at = S.cue(kw)
            for j in range(8):
                dot(c, t, e + k * 0.3 + 0.1 + j * 0.04, 150 + j * 62, y + 92, 18,
                    RED if (j < nred and t >= at) else PL)
            chip(c, t, at, lab, 700, y + 36, RED if k == 2 else PLL, WHITE if k == 2 else DARK, 32)
    so = S.cue('À la sortie')
    arrow(c, t, so - 0.2, 370, 790, 370, 735, DARK, 5, 14)
    card(c, t, so, 90, 560, 900, 160, RED, 32, 'pop')
    if prog(t, so, 0.5) > 0.4:
        icon(c, t, so + 0.1, 'user', 170, 640, 56, WHITE)
        reveal_plain(c, t, so + 0.2, 'Avocat : une personne', 230, 655, 40, WHITE, 'Medium')


def tri_grid(c, t, at, x0, y0, n, step, r, color):
    """Grille triangulaire : chaque token (ligne) regarde ceux qui le précèdent."""
    for i in range(n):
        for j in range(i + 1):
            dot(c, t, at + (i * n + j) * 0.012, x0 + j * step, y0 + i * step, r,
                RED if i == j else color)


def s4(c, t, S):
    header(c, t, S, 'Le coût', "L'attention *coûte cher*")
    a = S.cue('qui le précèdent')
    d = S.cue('le texte double')
    card(c, t, a, 90, 560, 430, 520, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Texte court', 305, 620, 20, DARK, align='center')
        tri_grid(c, t, a + 0.2, 235, 760, 4, 46, 14, PL)
        small(c, '4 tokens', 305, 1040, 20, DARK, align='center')
    card(c, t, d, 560, 560, 430, 520, LIGHT, 36, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Texte deux fois plus long', 775, 620, 20, DARK, align='center')
        tri_grid(c, t, d + 0.2, 635, 670, 8, 40, 12, PL)
        small(c, '8 tokens', 775, 1040, 20, DARK, align='center')
    if t >= d + 1.2:
        small(c, 'Chaque point : un regard · illustratif', 90, 1120, 18, DARK)
    fw = S.cue('fenêtres de contexte')
    card(c, t, fw, 90, 1160, 430, 270, LIGHT, 32, 'up')
    if prog(t, fw, 0.5) > 0.4:
        small(c, 'Fenêtre limitée', 140, 1220, 20, DARK)
        bar(c, t, fw + 0.2, 140, 1270, 330, 36, 1.0, PL, WHITE, 0.8)
        if t >= fw + 0.6:
            rrect(c, 380, 1250, 6, 76, 3, RED)
            small(c, 'Limite', 383, 1370, 18, RED, align='center')
    sl = S.cue('plus lentes')
    card(c, t, sl, 560, 1160, 430, 270, LIGHT, 32, 'up')
    if prog(t, sl, 0.5) > 0.4:
        icon(c, t, sl + 0.1, 'clock', 640, 1290, 70, RED)
        reveal_plain(c, t, sl + 0.2, 'Plus lent', 700, 1280, 34, DARK, 'Medium')
        reveal_plain(c, t, sl + 0.3, 'sur les longs textes', 700, 1330, 26, DARK, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "Plus de contexte n'est pas *mieux*")
    m = S.cue('noyée au milieu')
    card(c, t, m, 90, 560, 900, 470, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'Information bien exploitée · illustratif', 140, 620, 20, DARK)
        vals = [0.95, 0.75, 0.5, 0.35, 0.3, 0.32, 0.4, 0.6, 0.85, 0.95]
        e = S.cue('au début ou à la fin')
        for k, v in enumerate(vals):
            x = 150 + k * 80
            h = 260 * v
            at = m + 0.2 + k * 0.06
            if t >= at:
                p = ease(prog(t, at, 0.5))
                end = k in (0, 1, 8, 9) and t >= e
                rrect(c, x, 920 - h * p, 56, h * p, 12, RED if end else PL)
        rrect(c, 140, 940, 800, 10, 5, DARK)
        small(c, 'Début', 140, 990, 18, DARK)
        small(c, 'Milieu', 540, 990, 18, DARK, align='center')
        small(c, 'Fin', 940, 990, 18, DARK, align='right')
    pu = S.cue('les passages utiles')
    td = S.cue('tout le dossier')
    card(c, t, pu, 90, 1080, 900, 350, LIGHT, 36, 'up')
    if prog(t, pu, 0.5) > 0.4:
        small(c, 'Ce que vous envoyez', 140, 1140, 20, DARK)
        plain(c, 'Passages utiles', 140, 1210, 30, RED)
        bar(c, t, pu + 0.2, 140, 1230, 800, 36, 0.25, RED, WHITE, 0.6)
        icon(c, t, pu + 0.5, 'check', 380, 1248, 40, RED)
        if t >= td:
            plain(c, 'Tout le dossier', 140, 1325, 30, DARK)
        bar(c, t, td, 140, 1345, 800, 36, 1.0, PL, WHITE, 0.8)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelle *longueur de contexte* faut-il vraiment ?', 'Quelle longueur'),
        ('Quel *délai* accepter sur un long document ?', 'Quel délai'),
        ("L'information clé risque-t-elle d'être *noyée* ?", "l'information clé"),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Avec l'attention, chaque mot *regarde* les autres pour préciser son sens.", "grâce à l'attention"),
        ("Les longs contextes *coûtent* : envoyez l'essentiel, bien placé.", 'Mais ce regard'),
    ], '34 · Comment un modèle est entraîné')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle de langage sait à qui renvoie un pronom, sans règle de grammaire écrite à la main. "
        "Dans « la cliente a rappelé le vendeur, car il avait oublié la livraison », "
        "il relie « il » au vendeur.")),
    dict(kind='content', draw=s2, name="L'attention", text=(
        "Le secret s'appelle l'attention. C'est le cœur du transformer, l'architecture des grands modèles de langage. "
        "Chaque mot regarde les autres mots du texte pour préciser son sens. "
        "Prenez « avocat ». Près de « tribunal », c'est une personne. Près de « salade », c'est un fruit.")),
    dict(kind='content', draw=s3, name='Des couches empilées', text=(
        "Ce regard ne se fait pas une seule fois. Un transformer empile de nombreuses couches, "
        "et chacune affine la représentation de chaque mot. "
        "En simplifiant : les premières couches captent plutôt la forme, les suivantes le sens, "
        "les plus hautes les liens dans tout le texte. À la sortie, l'avocat est une personne.")),
    dict(kind='content', draw=s4, name="Le coût de l'attention", text=(
        "Mais l'attention coûte cher. Chaque token, un petit morceau de texte, regarde tous ceux qui le précèdent. "
        "Quand le texte double, le travail d'attention fait bien plus que doubler. "
        "D'où des fenêtres de contexte limitées, et des réponses plus lentes sur les longs documents.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, plus de contexte n'est pas toujours mieux. "
        "Une information noyée au milieu d'un très long contexte peut être moins bien exploitée qu'au début ou à la fin. "
        "Envoyez les passages utiles plutôt que tout le dossier, et testez sur de vrais documents longs.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelle longueur de contexte vos cas d'usage demandent-ils vraiment ? "
        "Quel délai est acceptable sur un long document ? "
        "Et l'information clé risque-t-elle d'être noyée au milieu ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : grâce à l'attention, chaque mot regarde les autres pour préciser son sens. "
        "Mais ce regard coûte cher sur les longs contextes : envoyez l'essentiel, bien placé. "
        "Prochaine capsule : comment un modèle est entraîné.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
