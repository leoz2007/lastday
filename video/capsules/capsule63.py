from engine import *  # noqa
from engine import _paint  # noqa

NUM = 63
TITLE = 'QUALITÉ ET CYCLE DEV'
FULL_TITLE = 'Qualité et cycle de développement'
SLUG = 'qualite_cycle_dev'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def vbar(c, t, at, x, base, w, h, color, dur=0.6):
    """Barre verticale qui monte depuis la ligne de base."""
    p = ease(prog(t, at, dur))
    if p > 0:
        rrect(c, x, base - h * p, w, h * p, 8, color)
    return p


def s1(c, t, S):
    opening(c, t, S, CAP, 'Plus de code, pas *plus de vitesse*.')
    a = S.cue('plus de code')
    card(c, t, a, 90, 830, 900, 600, WHITE, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Avec un agent · illustratif', 140, 890, 20, DARK)
        base = 1300
        icon(c, t, a + 0.1, 'code', 215, 960, 50, DARK)
        vbar(c, t, a + 0.2, 150, base, 130, 300, DARK)
        if t >= a + 0.5:
            plain(c, 'Code écrit', 215, 1360, 26, DARK, 'Medium', 'center')
        items = [('Corrections', 'plus de corrections', 160), ('Relectures', 'plus de relectures', 200),
                 ('Dette', 'plus de dette', 240)]
        for k, (s, kw, h) in enumerate(items):
            at = S.cue(kw)
            x = 380 + k * 200
            vbar(c, t, at, x, base, 130, h, RED if k == 2 else PL)
            if t >= at + 0.3:
                plain(c, s, x + 65, 1360, 26, DARK, 'Medium', 'center')
        if t >= a + 0.2:
            rrect(c, 130, base, 820, 4, 2, DARK)


def s2(c, t, S):
    header(c, t, S, 'Évals maison', 'Tester les modèles *chez vous*')
    d = S.cue('tirées de vos dépôts')
    card(c, t, d, 90, 540, 900, 470, LIGHT, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        icon(c, t, d + 0.1, 'code', 180, 620, 56, DARK)
        plain(c, 'Vos dépôts', 240, 632, 32, DARK, 'Medium')
        tk = S.cue('cinquante tickets')
        for k in range(50):
            x = 150 + (k % 10) * 40
            y = 720 + (k // 10) * 50
            dot(c, t, tk + k * 0.02, x, y, 13, PL)
        if t >= tk + 0.5:
            small(c, '50 tickets résolus · exemple', 130, 985, 18, DARK)
        rj = S.cue('chaque modèle candidat')
        arrow(c, t, rj, 560, 820, 620, 820, DARK, 6, 18)
        for k, (s, f) in enumerate([('Modèle A', 0.55), ('Modèle B', 0.8), ('Modèle C', 0.4)]):
            y = 710 + k * 95
            at = rj + 0.2 + k * 0.2
            if t >= at:
                plain(c, s, 650, y + 28, 26, DARK, 'Medium')
            bar(c, t, at, 650, y + 42, 300, 24, f, RED if k == 1 else PL, WHITE)
    r = S.cue('votre route')
    card(c, t, r, 90, 1050, 900, 170, WHITE, 32, 'up')
    if prog(t, r, 0.5) > 0.4:
        outline(c, 90, 1050, 900, 170, 32, PL)
        icon(c, t, r + 0.1, 'target', 170, 1135, 56, DARK)
        reveal_plain(c, t, r + 0.2, 'Un essai sur votre route,', 240, 1122, 34, DARK)
        reveal_plain(c, t, r + 0.35, 'pas sur circuit', 240, 1172, 34, DARK)
    o = S.cue('décision objective')
    card(c, t, o, 90, 1260, 900, 150, RED, 30, 'up')
    if prog(t, o, 0.5) > 0.4:
        icon(c, t, o + 0.1, 'check', 170, 1335, 56, WHITE)
        reveal_plain(c, t, o + 0.2, 'Changer de modèle : sur données', 240, 1348, 34, WHITE)


def s3(c, t, S):
    header(c, t, S, 'Intégration continue', 'Des *garde-fous* en CI')
    pr = S.cue('ouvertes par un agent')
    ci = S.cue("l'intégration continue")
    card(c, t, ci, 90, 540, 900, 130, LIGHT, 30, 'left')
    if prog(t, ci, 0.5) > 0.4:
        icon(c, t, ci + 0.1, 'code', 170, 605, 50, DARK)
        reveal_plain(c, t, ci + 0.2, 'Une modification proposée', 240, 618, 34, DARK)
    steps = [('check', 'Tests', 'Les tests'), ('shield', 'SAST · analyse de sécurité', 'statique de sécurité'),
             ('user', 'Revue humaine obligatoire', 'revue humaine')]
    for k, (ic, s, kw) in enumerate(steps):
        at = S.cue(kw)
        y = 730 + k * 150
        arrow(c, t, at - 0.2, 170, y - 50, 170, y - 6, DARK, 5, 14)
        card(c, t, at, 90, y, 900, 120, RED if k == 2 else WHITE, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if k == 2 else DARK
            if k < 2:
                outline(c, 90, y, 900, 120, 30, PL)
            icon(c, t, at + 0.1, ic, 170, y + 60, 50, fg)
            reveal_plain(c, t, at + 0.2, s, 240, y + 72, 34, fg)
    card(c, t, pr, 90, 1190, 900, 230, LIGHT, 32, 'up')
    if prog(t, pr, 0.5) > 0.4:
        label(c, t, pr + 0.1, "PR d'agent · règles propres", 140, 1225, PLL, DARK, 22)
        x = 140
        for k, (s, kw) in enumerate([('Étiquette visible', 'étiquette visible'),
                                     ('Périmètre limité', 'périmètre limité')]):
            at = S.cue(kw)
            chip(c, t, at, s, x, 1310, RED if k == 1 else WHITE, WHITE if k == 1 else DARK, 30)
            x += chip_width(s, 30) + 20


def s4(c, t, S):
    header(c, t, S, 'Mesurer l\'impact', 'Les quatre *métriques DORA*')
    tiles = [('bolt', 'Fréquence', 'de déploiement', 'quelle fréquence'),
             ('clock', 'Délai', "jusqu'à la production", 'en combien de temps une'),
             ('cross', "Taux d'échec", 'des déploiements', 'quelle part'),
             ('gear', 'Rétablissement', 'du service', 'rétablit-on')]
    for k, (ic, s, sub, kw) in enumerate(tiles):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        y = 560 + (k // 2) * 330
        hot = k == 2
        card(c, t, at, x, y, 440, 300, RED if hot else LIGHT, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if hot else DARK
            icon(c, t, at + 0.1, ic, x + 220, y + 90, 70, fg)
            plain(c, s, x + 220, y + 200, 34, fg, 'Medium', 'center')
            small(c, sub, x + 220, y + 250, 18, fg, align='center')
    n = S.cue('règlement européen')
    card(c, t, n, 90, 1230, 900, 180, DARK, 32, 'up')
    if prog(t, n, 0.5) > 0.4:
        icon(c, t, n + 0.1, 'cross', 170, 1320, 50, RED)
        reveal_plain(c, t, n + 0.2, 'Pas le règlement européen DORA', 240, 1310, 34, WHITE)
        reveal_plain(c, t, n + 0.35, 'Ici : livraison logicielle', 240, 1360, 30, WHITE, 'Light')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Reprise et *dette*')
    rw = S.cue('taux de reprise')
    card(c, t, rw, 90, 540, 430, 520, LIGHT, 32, 'up')
    if prog(t, rw, 0.5) > 0.4:
        small(c, 'Rework', 130, 600, 20, DARK)
        ra = S.cue('réécrite peu après')
        widths = [300, 220, 330, 260, 180, 310, 240]
        for k, w in enumerate(widths):
            redo = k in (2, 3, 5) and t >= ra
            p = ease(prog(t, rw + 0.2 + k * 0.06, 0.4))
            if p > 0:
                rrect(c, 130, 650 + k * 52, w * p, 30, 8, RED if redo else PL)
        if t >= ra:
            small(c, 'Réécrit peu après', 305, 1030, 18, RED, align='center')
    de = S.cue('la dette générée')
    card(c, t, de, 560, 540, 430, 520, LIGHT, 32, 'up')
    if prog(t, de, 0.5) > 0.4:
        small(c, 'Dette', 600, 600, 20, DARK)
        for k in range(5):
            at = de + 0.3 + k * 0.2
            card(c, t, at, 640 - (k % 2) * 20, 960 - k * 70, 280, 56, DARK if k % 2 else PL, 12, 'up')
        dp = S.cue('dupliqué')
        if t >= dp:
            small(c, 'Dupliqué, obscur', 775, 1030, 18, DARK, align='center')
    av = S.cue('avant et après')
    card(c, t, av, 90, 1100, 900, 310, RED, 32, 'up')
    if prog(t, av, 0.5) > 0.4:
        small(c, 'Avant / après · sur plusieurs mois', 140, 1160, 20, WHITE)
        for k in range(6):
            x = 140 + k * 135
            h = 70 + (k % 3) * 20 if k < 3 else 120 + k * 10
            vbar(c, t, av + 0.2 + k * 0.12, x, 1370, 90, h, WHITE if k >= 3 else PL)
        if t >= av + 0.3:
            rrect(c, 528, 1190, 4, 190, 2, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Sur quelles tâches de *nos dépôts* évaluer les modèles ?', 'Sur quelles tâches'),
        ("Quelles *règles* pour les demandes de fusion d'un agent ?", 'Quelles règles'),
        ('Quelles *mesures* suivre, avant et après ?', 'Et quelles mesures'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Choisissez vos modèles avec des *évals maison*.', 'choisissez vos modèles'),
        ('Tests, SAST, *revue humaine* ; mesurez DORA, rework et dette.', 'Gardez tests'),
    ], '64 · Gouvernance et conformité')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un agent qui écrit plus de code ne rend pas forcément votre équipe plus rapide. "
        "Il peut aussi produire plus de corrections, plus de relectures, et plus de dette. "
        "Pour le savoir, il faut mesurer.")),
    dict(kind='content', draw=s2, name='Des évals maison sur vos dépôts', text=(
        "D'abord, construisez des évals maison : des tâches réelles tirées de vos dépôts, avec leurs tests. "
        "Par exemple, cinquante tickets déjà résolus, rejoués par chaque modèle candidat. "
        "Un essai sur votre route, pas sur circuit. "
        "Changer de modèle devient une décision objective.")),
    dict(kind='content', draw=s3, name="Des garde-fous dans l'intégration continue", text=(
        "Ensuite, des garde-fous dans l'intégration continue, la CI, qui vérifie chaque modification. "
        "Les tests doivent passer. L'analyse statique de sécurité, le SAST, cherche les failles dans le code. "
        "La revue humaine reste obligatoire. Et les demandes de fusion, les PR, ouvertes par un agent "
        "ont leurs règles : étiquette visible, périmètre limité.")),
    dict(kind='content', draw=s4, name="Mesurer l'impact : les métriques DORA", text=(
        "Puis mesurez l'impact avec les métriques DORA, des indicateurs de performance de la livraison logicielle. "
        "Rien à voir avec le règlement européen du même nom. "
        "À quelle fréquence déploie-t-on ? En combien de temps une modification arrive-t-elle en production ? "
        "Quelle part des déploiements échoue ? Et en combien de temps rétablit-on le service ?")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, ajoutez deux mesures. Le taux de reprise, ou rework : "
        "la part du code d'agent réécrite peu après. "
        "Et la dette générée : du code dupliqué ou obscur, que l'équipe devra porter. "
        "Comparez avant et après l'agent, sur plusieurs mois.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Sur quelles tâches de nos dépôts évaluer les modèles ? "
        "Quelles règles pour les demandes de fusion d'un agent ? "
        "Et quelles mesures suivre, avant et après ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : choisissez vos modèles avec des évals maison, sur vos dépôts. "
        "Gardez tests, SAST et revue humaine en CI, et mesurez l'impact avec DORA, le rework et la dette. "
        "Prochaine capsule : la gouvernance et la conformité.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
