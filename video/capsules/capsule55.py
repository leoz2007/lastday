from engine import *  # noqa
from engine import _paint  # noqa

NUM = 55
TITLE = 'MODÈLE DE SOUVERAINETÉ'
FULL_TITLE = 'Le modèle de souveraineté'
SLUG = 'modele_souverainete'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def gpu(c, t, at, x, y, w=150, h=70, color=DARK, led=RED):
    """Carte GPU stylisée : un boîtier, des ailettes, un témoin."""
    p = card(c, t, at, x, y, w, h, color, 14, 'pop')
    if p > 0.6:
        for k in range(4):
            rrect(c, x + 18 + k * 26, y + 16, 12, h - 32, 6, WHITE)
        c.drawCircle(x + w - 26, y + h / 2, 9, _paint(led))


def s1(c, t, S):
    opening(c, t, S, CAP, '« On premise » a *plusieurs sens*.')
    p = S.cue('plusieurs choses')
    card(c, t, p, 90, 830, 900, 290, WHITE, 36, 'up')
    if prog(t, p, 0.5) > 0.4:
        small(c, 'Où tourne le modèle ?', 140, 890, 22, DARK)
        bar(c, t, p + 0.2, 160, 965, 760, 16, 1.0, PL, LIGHT, 0.7)
        pts = [('Tout sur site', 180), ('Hybride', 540), ('Cloud privé', 900)]
        for k, (s, x) in enumerate(pts):
            a = p + 0.5 + k * 0.2
            dot(c, t, a, x, 973, 26, RED if k == 0 else DARK)
            if t >= a:
                al = 'left' if k == 0 else ('right' if k == 2 else 'center')
                xx = 140 if k == 0 else (940 if k == 2 else 540)
                reveal_plain(c, t, a, s, xx, 1060, 32, DARK, 'Medium', al)
    ct = S.cue('conditionne tout le reste')
    if t >= ct:
        small(c, 'Ce choix conditionne', 90, 1200, 22, WHITE)
    x = 90
    for k, (s, kw) in enumerate([('Le modèle autorisé', 'le modèle autorisé'), ('Les coûts', 'les coûts'),
                                 ('La qualité', 'la qualité')]):
        at = S.cue(kw)
        w = chip(c, t, at, s, x, 1240, RED if k == 0 else WHITE, WHITE if k == 0 else DARK, 30)
        x += w + 20


def s2(c, t, S):
    header(c, t, S, 'Option 1', 'Le *tout sur site*')
    m = S.cue('vous faites tourner')
    card(c, t, m, 90, 540, 900, 560, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        outline(c, 130, 600, 820, 460, 28, DARK, 6)
        label(c, t, m + 0.1, 'Vos murs', 160, 575, DARK, WHITE, 22)
        w = S.cue('poids ouverts')
        box(c, t, w, 170, 660, 360, 120, 'Modèle open-weight', RED, WHITE, 30)
        if t >= w + 0.3:
            small(c, 'Poids téléchargeables', 350, 820, 18, DARK, align='center')
        g = S.cue('propres GPU')
        for k in range(3):
            gpu(c, t, g + k * 0.15, 610, 650 + k * 85, 280, 66)
        if t >= g + 0.4:
            small(c, 'Vos GPU', 750, 935, 18, DARK, align='center')
        d = S.cue('Aucune donnée')
        icon(c, t, d, 'doc', 200, 1000, 56, DARK)
        icon(c, t, d + 0.1, 'code', 280, 1000, 56, DARK)
        if t >= d + 0.2:
            reveal_plain(c, t, d + 0.2, 'Données et code restent ici', 330, 1012, 30, DARK, 'Medium')
            icon(c, t, d + 0.4, 'lock', 900, 1000, 50, RED)
    sv = S.cue('souveraineté est maximale')
    card(c, t, sv, 90, 1130, 900, 130, RED, 30, 'left')
    if prog(t, sv, 0.5) > 0.4:
        icon(c, t, sv + 0.1, 'shield', 170, 1195, 56, WHITE)
        reveal_plain(c, t, sv + 0.2, 'Souveraineté maximale', 240, 1208, 38, WHITE, 'Medium')
    cu = S.cue('cuisine maison')
    if t >= cu:
        icon(c, t, cu, 'user', 130, 1350, 50, DARK)
        reveal_plain(c, t, cu + 0.1, 'Cuisine maison : tout maîtriser, tout assurer', 180, 1362, 30, DARK, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Le revers', 'Souvent *un cran* en dessous')
    a = S.cue('mode agentique')
    card(c, t, a, 90, 540, 900, 330, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Qualité agentique · illustratif', 140, 600, 20, DARK)
        cr = S.cue('un cran en dessous')
        plain(c, 'Open-weight', 140, 690, 30, DARK)
        bar(c, t, cr, 400, 662, 540, 40, 0.68, PL, WHITE, 0.8)
        fr = S.cue('dits frontier')
        plain(c, 'Frontier', 140, 790, 30, RED)
        bar(c, t, fr, 400, 762, 540, 40, 0.88, RED, WHITE, 0.8)
    e = S.cue('dix fichiers')
    card(c, t, e, 90, 900, 900, 360, LIGHT, 36, 'up')
    if prog(t, e, 0.5) > 0.4:
        small(c, 'Une modification sur 10 fichiers · exemple', 140, 960, 20, DARK)
        ab = S.cue("aboutit d'un côté")
        rp = S.cue('plus de reprises')
        for row, (lab, at, bad) in enumerate([('Frontier', ab, ()), ('Open-weight', rp, (3, 7))]):
            y = 1010 + row * 110
            plain(c, lab, 140, y + 50, 28, RED if row == 0 else DARK)
            for k in range(10):
                x = 380 + k * 56
                col = RED if k in bad and t >= at + 0.6 else (PL if row == 1 else DARK)
                card(c, t, at + k * 0.05, x, y + 10, 42, 54, col, 8, 'pop')
            if row == 0:
                icon(c, t, at + 0.6, 'check', 945, y + 37, 40, RED)
            else:
                icon(c, t, at + 0.6, 'clock', 945, y + 37, 40, DARK)
    ex = S.cue('exploitation reste')
    chip(c, t, ex, 'Exploitation : à votre charge', 90, 1300, DARK, WHITE, 32)


def s4(c, t, S):
    header(c, t, S, 'Option 2', 'Cloud *privé* ou *hybride*')
    m = S.cue('modèles frontier')
    card(c, t, m, 90, 560, 250, 300, LIGHT, 32, 'pop')
    if prog(t, m, 0.5) > 0.4:
        icon(c, t, m + 0.1, 'code', 215, 680, 80, DARK)
        small(c, 'Vos équipes', 215, 800, 20, DARK, align='center')
    arrow(c, t, m + 0.3, 350, 710, 440, 710, DARK, 6, 18)
    ue = S.cue('région européenne')
    card(c, t, m + 0.4, 450, 540, 540, 380, LIGHT, 36, 'pop')
    if prog(t, m + 0.4, 0.5) > 0.4:
        outline(c, 480, 570, 480, 320, 26, RED if t >= ue else PL, 6)
        if t >= ue:
            label(c, t, ue, 'Région UE', 510, 545, RED, WHITE, 22)
        box(c, t, m + 0.6, 520, 620, 400, 110, 'Modèle frontier', RED, WHITE, 32)
        o = S.cue('grands clouds')
        if t >= o:
            small(c, 'Exemples à date', 520, 790, 18, DARK)
        x = 520
        for k, s in enumerate(['Bedrock', 'Vertex', 'Azure']):
            w = chip(c, t, o + 0.2 + k * 0.15, s, x, 810, WHITE, DARK, 24)
            x += w + 12
    nc = S.cue('non-conservation')
    card(c, t, nc, 90, 960, 900, 140, LIGHT, 30, 'left')
    if prog(t, nc, 0.5) > 0.4:
        icon(c, t, nc + 0.1, 'lock', 170, 1030, 56, DARK)
        reveal_plain(c, t, nc + 0.2, 'Non-conservation : selon le contrat', 240, 1043, 34, DARK, 'Medium')
    bc = S.cue('le bon compromis')
    card(c, t, bc, 90, 1130, 900, 140, RED, 30, 'left')
    if prog(t, bc, 0.5) > 0.4:
        icon(c, t, bc + 0.1, 'check', 170, 1200, 56, WHITE)
        reveal_plain(c, t, bc + 0.2, 'Souvent le bon compromis', 240, 1213, 38, WHITE, 'Medium')
    jr = S.cue('le juridique')
    if t >= jr:
        icon(c, t, jr, 'doc', 130, 1350, 44, DARK)
        reveal_plain(c, t, jr + 0.1, 'Le juridique valide chaque contrat', 180, 1362, 30, DARK, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Classer les dépôts par *sensibilité*')
    cl = S.cue('Classez vos dépôts')
    card(c, t, cl, 90, 540, 900, 680, LIGHT, 36, 'up')
    if prog(t, cl, 0.5) > 0.4:
        small(c, 'Dépôt', 140, 610, 20, DARK)
        small(c, 'Sensibilité', 470, 610, 20, DARK)
        small(c, 'Modèle autorisé', 940, 610, 20, DARK, align='right')
        rows = [('Outils internes', 'Les outils internes', 0.25, 'Cloud privé', False),
                ('Applications', 'Les outils internes', 0.55, 'Selon contrat', False),
                ('Cœur bancaire', 'Le cœur bancaire', 0.95, 'Sur site', True)]
        for k, (s, kw, f, mod, hot) in enumerate(rows):
            at = S.cue(kw) + (0.4 if k == 1 else 0)
            y = 650 + k * 180
            card(c, t, at, 120, y, 840, 150, WHITE, 28, 'left')
            if prog(t, at, 0.5) > 0.4:
                icon(c, t, at + 0.1, 'code', 175, y + 75, 44, RED if hot else DARK)
                plain(c, s, 215, y + 85, 28, DARK, 'Medium')
                bar(c, t, at + 0.2, 470, y + 60, 220, 30, f, RED if hot else PL, LIGHT, 0.6)
                cw = chip_width(mod, 26)
                chip(c, t, at + 0.5, mod, 930 - cw, y + 52, RED if hot else PLL, WHITE if hot else DARK, 26)
    d = S.cue('décide du modèle')
    card(c, t, d, 90, 1250, 900, 150, RED, 30, 'up')
    if prog(t, d, 0.5) > 0.4:
        icon(c, t, d + 0.1, 'target', 170, 1325, 56, WHITE)
        reveal_plain(c, t, d + 0.2, 'Le classement décide du modèle', 240, 1338, 36, WHITE, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles données ne doivent *jamais sortir* ?', 'Quelles données'),
        ('Quels *contrats* et régions le juridique accepte-t-il ?', 'Quels contrats'),
        ('Quel *niveau de sensibilité* pour chaque dépôt ?', 'Et quel niveau'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("« On premise » : *plusieurs* modèles de souveraineté.", 'recouvre'),
        ('La *sensibilité* du dépôt décide du modèle.', 'Classez vos dépôts'),
    ], '56 · Modèles et inférence')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "« On premise », c'est-à-dire chez vous, peut vouloir dire plusieurs choses. "
        "Et ce choix conditionne tout le reste : le modèle autorisé, les coûts, "
        "la qualité de vos agents de code.")),
    dict(kind='content', draw=s2, name='Option un : le tout sur site', text=(
        "Première option : le tout sur site. Vous faites tourner des modèles open-weight, à poids ouverts et téléchargeables, "
        "sur vos propres GPU, les processeurs graphiques qui calculent. "
        "Aucune donnée ne sort de vos murs : la souveraineté est maximale. "
        "Comme une cuisine maison : vous maîtrisez tout, mais vous assurez tout.")),
    dict(kind='content', draw=s3, name='Le revers : la qualité agentique', text=(
        "Le revers : en mode agentique, quand l'agent enchaîne seul les actions, "
        "ces modèles sont souvent un cran en dessous des modèles les plus avancés, dits frontier. "
        "Exemple illustratif : une modification sur dix fichiers aboutit d'un côté, "
        "demande plus de reprises de l'autre. Et l'exploitation reste à votre charge.")),
    dict(kind='content', draw=s4, name='Option deux : cloud privé ou hybride', text=(
        "Deuxième option : le cloud privé ou hybride. Vous accédez aux modèles frontier "
        "via les grands clouds, par exemple Bedrock ou Vertex, à date. "
        "Les appels restent en région européenne, et certains contrats prévoient la non-conservation des données. "
        "Souvent le bon compromis, mais le juridique valide chaque contrat.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, pas de modèle unique pour tout. "
        "Classez vos dépôts de code, les repos, par sensibilité. "
        "Les outils internes peuvent passer par le cloud privé. "
        "Le cœur bancaire reste sur vos propres serveurs. "
        "Ce classement décide du modèle autorisé pour chaque dépôt.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles données ne doivent jamais sortir de vos murs ? "
        "Quels contrats et quelles régions votre juridique accepte-t-il ? "
        "Et quel niveau de sensibilité donnez-vous à chaque dépôt ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : « on premise » recouvre plusieurs modèles de souveraineté. "
        "Le tout sur site protège le plus ; le cloud privé, souvent le meilleur compromis. "
        "Classez vos dépôts pour décider du modèle autorisé. "
        "Prochaine capsule : modèles et inférence.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
