from engine import *  # noqa
from engine import _paint  # noqa

NUM = 67
TITLE = "LOIS D'ÉCHELLE"
FULL_TITLE = "Lois d'échelle et calcul à l'inférence"
SLUG = 'lois_echelle_inference'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def curve(c, t, at, x0, y0, w, h, color=RED, width=7, dur=1.4, n=40):
    """Courbe croissante qui s'aplatit (rendements décroissants), tracée progressivement."""
    p = ease(prog(t, at, dur))
    if p <= 0:
        return
    pts = []
    m = max(2, int(n * p))
    for k in range(m + 1):
        u = k / n
        pts.append((x0 + u * w, y0 - h * (1 - (1 - u) ** 2.6)))
    path = skia.Path()
    path.moveTo(*pts[0])
    for q in pts[1:]:
        path.lineTo(*q)
    c.drawPath(path, _paint(color, width))


def curve_y(x0, y0, w, h, u):
    return y0 - h * (1 - (1 - u) ** 2.6)


def axes(c, x0, y0, w, h):
    rrect(c, x0, y0, w, 4, 2, PL)
    rrect(c, x0, y0 - h, 4, h + 4, 2, PL)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Mieux répondre en *prenant le temps*.')
    a = S.cue('agrandir un modèle')
    card(c, t, a, 90, 830, 435, 420, WHITE, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Plus grand', 140, 890, 20, DARK)
        for k, s in enumerate([60, 100, 150]):
            card(c, t, a + 0.2 + k * 0.2, 170 + k * 110, 1200 - s * 1.8, 80, s * 1.8, PL if k < 2 else DARK, 14, 'up')
    r = S.cue('plus de temps pour réfléchir')
    card(c, t, r, 555, 830, 435, 420, RED, 32, 'up')
    if prog(t, r, 0.5) > 0.4:
        small(c, 'Plus de réflexion', 605, 890, 20, WHITE)
        icon(c, t, r + 0.1, 'clock', 772, 1010, 110, WHITE)
        for k in range(5):
            dot(c, t, r + 0.4 + k * 0.15, 650 + k * 60, 1170, 14, WHITE)
    i = S.cue("le calcul à l'inférence")
    if t >= i:
        chip(c, t, i, "Calcul à l'inférence", 540, 1290, WHITE, DARK, 32, align='center')


def s2(c, t, S):
    header(c, t, S, "Lois d'échelle", 'Plus de moyens, *mieux*, de façon prévisible')
    items = [('db', 'Données', 'les données'), ('brain', 'Paramètres', 'les paramètres'),
             ('bolt', 'Calcul', "le calcul d'entraînement")]
    for k, (ic, s, kw) in enumerate(items):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 560, 280, 220, LIGHT, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 640, 64, RED if k == 2 else DARK)
            plain(c, s, x + 140, 740, 30, DARK, 'Medium', 'center')
    o = S.cue('assez prévisible')
    card(c, t, o, 90, 820, 900, 610, LIGHT, 32, 'up')
    if prog(t, o, 0.5) > 0.4:
        small(c, 'Tendance observée · illustratif', 140, 880, 20, DARK)
        x0, y0, w, h = 190, 1330, 720, 380
        axes(c, x0, y0, w, h)
        curve(c, t, o + 0.3, x0, y0, w, h)
        small(c, 'Performance', 210, 930, 18, DARK)
        small(c, 'Données, paramètres, calcul', 910, 1385, 18, DARK, align='right')
        rc = S.cue('une recette')
        if t >= rc:
            for k, u in enumerate([0.15, 0.4, 0.7]):
                dot(c, t, rc + k * 0.15, x0 + u * w, curve_y(x0, y0, w, h, u), 16, DARK)


def s3(c, t, S):
    header(c, t, S, 'Rendements décroissants', 'Chaque gain coûte *plus cher*')
    a = S.cue('rendements sont décroissants')
    card(c, t, a, 90, 540, 900, 560, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Moyens pour un même petit gain · illustratif', 140, 600, 20, DARK)
        m = S.cue('multiplier les moyens')
        for k, f in enumerate([0.12, 0.25, 0.5, 1.0]):
            y = 650 + k * 100
            plain(c, f'Gain {k + 1}', 140, y + 45, 28, DARK if k < 3 else RED)
            bar(c, t, (a + 0.3 if k < 2 else m) + k * 0.2, 300, y + 20, 640, 34, f,
                RED if k == 3 else PL, WHITE, 0.6)
        if t >= m + 1.0:
            small(c, 'Toujours plus de moyens', 940, 1070, 18, RED, align='right')
    p = S.cue('prudence')
    card(c, t, p, 90, 1140, 900, 290, RED, 32, 'up')
    if prog(t, p, 0.5) > 0.4:
        icon(c, t, p + 0.1, 'eye', 175, 1240, 64, WHITE)
        text_block(c, t, p + 0.2, 'Des tendances observées, pas des lois physiques', 250, 1230, 36,
                   'Medium', WHITE, WHITE, maxw=690, max_lines=2)
        ch = S.cue('peuvent changer')
        if t >= ch:
            small(c, 'Elles peuvent évoluer', 250, 1380, 18, WHITE)


def s4(c, t, S):
    header(c, t, S, "Calcul à l'inférence", 'Réfléchir *au moment de répondre*')
    rows = [('clock', 'Réfléchir plus longtemps', 'réfléchir plus longtemps'),
            ('target', 'Plusieurs essais, le meilleur', 'plusieurs essais'),
            ('check', 'Vérifier sa réponse', 'vérifier sa réponse')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 540 + k * 130
        card(c, t, at, 90, y, 900, 110, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 165, y + 55, 50, RED)
            reveal_plain(c, t, at + 0.2, s, 230, y + 67, 34, DARK)
            if k == 1:
                for j in range(3):
                    card(c, t, at + 0.4 + j * 0.15, 840 + j * 45, y + 25, 34, 60, RED if j == 1 else PL, 8, 'pop')
    cp = S.cue('relit sa copie')
    if t >= cp:
        icon(c, t, cp, 'doc', 130, 960, 44, DARK)
        reveal_plain(c, t, cp + 0.1, 'Comme un élève qui relit sa copie', 175, 972, 30, DARK)
    d = S.cue('tâches difficiles')
    card(c, t, d, 90, 1030, 900, 400, LIGHT, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Gain de la réflexion · illustratif', 140, 1090, 20, DARK)
        plain(c, 'Tâche difficile', 140, 1180, 30, RED)
        bar(c, t, d + 0.2, 470, 1155, 470, 34, 0.85, RED, WHITE, 0.8)
        sm = S.cue('sur les simples')
        plain(c, 'Tâche simple', 140, 1290, 30, DARK)
        bar(c, t, sm, 470, 1265, 470, 34, 0.12, PL, WHITE, 0.6)
        if t >= sm + 0.4:
            small(c, 'Peu de gain', 940, 1360, 18, DARK, align='right')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Doser *l\'effort* selon la tâche')
    a = S.cue('plus de délai')
    card(c, t, a, 90, 540, 900, 300, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Plus de réflexion, par requête · illustratif', 140, 600, 20, DARK)
        rows = [('clock', 'Délai', 'plus de délai', 0.75), ('coin', 'Coût', 'plus de coût', 0.7),
                ('target', 'Qualité', 'avec la qualité', 0.6)]
        for k, (ic, s, kw, f) in enumerate(rows):
            at = S.cue(kw)
            y = 640 + k * 62
            icon(c, t, at, ic, 160, y + 20, 36, RED if k == 2 else DARK)
            plain(c, s, 200, y + 32, 28, RED if k == 2 else DARK)
            bar(c, t, at, 360, y + 6, 580, 30, f, RED if k == 2 else PL, WHITE, 0.6)
    e = S.cue("choisissez l'effort")
    tasks = [('Trier un courriel', 'trier un courriel', 'Effort léger', 1, PLL, DARK),
             ('Analyser un contrat', 'analyser un contrat', 'Effort poussé', 4, RED, WHITE)]
    for k, (s, kw, lab, n, fill, fg) in enumerate(tasks):
        at = S.cue(kw)
        x = 90 + k * 465
        card(c, t, at, x, 880, 435, 300, fill, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            small(c, lab, x + 40, 940, 20, fg)
            for j in range(4):
                rrect(c, x + 40 + j * 90, 990, 70, 70, 14, (WHITE if fill == RED else RED) if j < n else (PL if fill == PLL else WHITE))
            plain(c, s, x + 40, 1130, 32, fg)
    ev = S.cue('sur vos évals')
    card(c, t, ev, 90, 1220, 900, 210, LIGHT, 32, 'up')
    if prog(t, ev, 0.5) > 0.4:
        icon(c, t, ev + 0.1, 'check', 170, 1325, 60, RED)
        reveal_plain(c, t, ev + 0.2, 'Mesurer le gain réel sur vos évals', 240, 1338, 36, DARK)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles tâches sont *vraiment difficiles* ?', 'Quelles tâches'),
        ('Quels *délai et coût* par requête acceptez-vous ?', 'Quel délai'),
        ('Le gain est-il *mesuré sur vos évals* ?', 'Et le gain'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Plus de moyens, *meilleurs modèles*, mais des gains décroissants.', 'plus de données'),
        ('Réfléchir plus aide sur les *tâches difficiles* : dosez l\'effort.', 'réfléchir plus longtemps aide'),
    ], '68 · Interprétabilité')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Pour mieux répondre, on peut agrandir un modèle. "
        "Mais un même modèle peut aussi répondre mieux, simplement en prenant plus de temps pour réfléchir. "
        "C'est le calcul à l'inférence.")),
    dict(kind='content', draw=s2, name="Les lois d'échelle", text=(
        "D'abord, les lois d'échelle, en anglais scaling laws. "
        "On observe que les performances progressent de façon assez prévisible "
        "quand on augmente trois ingrédients : les données, les paramètres, ces réglages appris par le modèle, "
        "et le calcul d'entraînement. Comme une recette qu'on agrandit, le résultat suit une tendance.")),
    dict(kind='content', draw=s3, name='Des rendements décroissants', text=(
        "Mais les rendements sont décroissants. "
        "Chaque nouveau gain coûte plus cher : il faut souvent multiplier les moyens pour progresser encore un peu. "
        "Et prudence : ce sont des tendances observées, pas des lois physiques. Elles peuvent changer.")),
    dict(kind='content', draw=s4, name="Le calcul à l'inférence", text=(
        "D'où une autre piste : dépenser plus de calcul au moment de répondre, l'inférence. "
        "Le modèle peut réfléchir plus longtemps, faire plusieurs essais puis garder le meilleur, "
        "ou vérifier sa réponse, comme un élève qui relit sa copie. "
        "C'est utile sur les tâches difficiles, beaucoup moins sur les simples.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, plus de réflexion veut dire plus de délai et plus de coût par requête, "
        "à mettre en balance avec la qualité. "
        "Choisissez l'effort selon la tâche : léger pour trier un courriel, plus poussé pour analyser un contrat. "
        "Et mesurez le gain sur vos évals, vos tests de référence.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles tâches sont vraiment difficiles ? "
        "Quel délai et quel coût par requête acceptez-vous ? "
        "Et le gain est-il mesuré sur vos évals ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : plus de données, de paramètres et de calcul améliorent les modèles, "
        "avec des rendements décroissants. "
        "Réfléchir plus longtemps aide sur les tâches difficiles, à un coût : dosez l'effort. "
        "Prochaine capsule : l'interprétabilité, pour regarder à l'intérieur d'un modèle.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
