from engine import *  # noqa
from engine import _paint  # noqa

NUM = 26
TITLE = 'BIAIS ET ÉQUITÉ'
FULL_TITLE = 'Biais et équité'
SLUG = 'biais_equite'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def dossier(c, t, at, x, y, w, h, name, fill=LIGHT, name_col=DARK):
    """Petite fiche de dossier : un nom en tête, trois lignes grises identiques."""
    card(c, t, at, x, y, w, h, fill, 30, 'up')
    if prog(t, at, 0.5) > 0.4:
        icon(c, t, at + 0.1, 'user', x + 60, y + 60, 50, name_col)
        plain(c, name, x + 105, y + 72, 30, name_col)
        for j, fr in enumerate([0.9, 0.75, 0.85]):
            bar(c, t, at + 0.15 + j * 0.08, x + 30, y + 120 + j * 44, w - 60, 20, fr, PL, WHITE, 0.4)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Même dossier, deux *réponses*.')
    a = S.cue("pas d'opinion")
    d = S.cue('deux personnes')
    dossier(c, t, a, 90, 820, 430, 280, 'Prénom A')
    dossier(c, t, d, 560, 820, 430, 280, 'Prénom B')
    r = S.cue('à dossier identique')
    for k, (fr, col, ic) in enumerate([(0.85, WHITE, 'check'), (0.45, RED, 'cross')]):
        x = 90 + k * 470
        if t >= r:
            small(c, 'Appréciation', x, 1170, 22, WHITE)
        bar(c, t, r + k * 0.3, x, 1200, 360, 34, fr, col, PL, 0.8)
        icon(c, t, r + 0.6 + k * 0.3, ic, x + 400, 1217, 56, col)
    if t >= r + 1.0:
        reveal_plain(c, t, r + 1.0, 'Seul le prénom change', 540, 1340, 36, RED, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, "D'où vient le biais", 'Le modèle *reflète* ses données')
    a = S.cue('énormes volumes')
    card(c, t, a, 90, 560, 300, 300, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        for k in range(3):
            icon(c, t, a + 0.1 + k * 0.1, 'doc', 170 + k * 70, 660, 55, DARK)
        small(c, 'Textes', 240, 780, 22, DARK, align='center')
        small(c, 'humains', 240, 815, 22, DARK, align='center')
    rg = S.cue('régularités')
    arrow(c, t, rg, 400, 710, 470, 710, DARK, 6)
    card(c, t, rg + 0.2, 480, 560, 220, 300, DARK, 32, 'up')
    if prog(t, rg + 0.2, 0.5) > 0.4:
        icon(c, t, rg + 0.3, 'brain', 590, 680, 80, WHITE)
        small(c, 'Modèle', 590, 800, 22, WHITE, align='center')
    st = S.cue('stéréotypes')
    arrow(c, t, st, 710, 710, 780, 710, RED, 6)
    card(c, t, st + 0.2, 790, 560, 200, 300, RED, 32, 'up')
    if prog(t, st + 0.2, 0.5) > 0.4:
        icon(c, t, st + 0.3, 'chat', 890, 680, 70, WHITE)
        small(c, 'Réponses', 890, 800, 22, WHITE, align='center')
    m = S.cue('un métier')
    card(c, t, m, 90, 920, 900, 300, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'Association apprise (exemple)', 140, 985, 22, DARK)
        box(c, t, m + 0.2, 140, 1030, 300, 120, 'Un métier', WHITE, DARK, 34)
        g = S.cue('à un genre')
        arrow(c, t, g, 460, 1090, 620, 1090, RED, 6)
        box(c, t, g + 0.2, 640, 1030, 300, 120, 'Un genre', WHITE, DARK, 34)
    rp = S.cue('il ne les corrige pas')
    chip(c, t, rp, 'Il reflète, il ne corrige pas', 90, 1280, DARK, WHITE, 34)


def s3(c, t, S):
    header(c, t, S, 'Deux exemples', 'Où le biais *se voit*')
    a = S.cue('analyse de dossier')
    card(c, t, a, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        label(c, t, a + 0.1, 'Analyse de dossier', 140, 580, PLL, DARK, 22)
        mp = S.cue('même parcours')
        for k, chp in enumerate(['Même parcours', 'Même expérience']):
            chip(c, t, mp + k * 0.3, chp, 140 + k * 330, 650, WHITE, DARK, 30)
        ap = S.cue('appréciation différente')
        for k, (nm, fr, col) in enumerate([('Prénom A', 0.85, PL), ('Prénom B', 0.5, RED)]):
            y = 780 + k * 70
            reveal_plain(c, t, ap + k * 0.2, nm, 140, y + 26, 30, DARK)
            bar(c, t, ap + k * 0.2, 330, y, 600, 32, fr, col, WHITE, 0.8)
    r = S.cue('une rédaction')
    card(c, t, r, 90, 990, 900, 420, LIGHT, 36, 'up')
    if prog(t, r, 0.5) > 0.4:
        label(c, t, r + 0.1, 'Rédaction', 140, 1030, PLL, DARK, 22)
        o = S.cue("offre d'emploi")
        for j, fr in enumerate([0.95, 0.7, 0.85]):
            bar(c, t, o + j * 0.12, 140, 1110 + j * 50, 800, 22, fr, PL, WHITE, 0.4)
        sg = S.cue('vers un stéréotype')
        chip(c, t, sg, 'stéréotype', 520, 1260, RED, WHITE, 34)
        icon(c, t, sg + 0.3, 'eye', 220, 1300, 60, RED)
        na = S.cue('ne l\'ait demandé')
        if t >= na:
            reveal_plain(c, t, na, 'Personne ne l\'a demandé', 140, 1385, 26, DARK)


def s4(c, t, S):
    header(c, t, S, 'Tester', 'Des *paires* de cas')
    a = S.cue('paires de cas')
    du = S.cue('vous le dupliquez')
    at_ = S.cue('un seul attribut')
    for k, (nm, at) in enumerate([('Prénom A', a), ('Prénom B', du)]):
        x = 90 + k * 470
        card(c, t, at, x, 540, 430, 330, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, 'Dossier', x + 40, 600, 22, DARK)
            col = RED if (k == 1 and t >= at_) else DARK
            if k == 1 and t >= at_:
                rrect(c, x + 30, 625, 370, 64, 20, PLL)
            plain(c, nm, x + 50, 670, 32, col)
            for j, fr in enumerate([0.9, 0.7, 0.8]):
                bar(c, t, at + 0.15 + j * 0.08, x + 40, 720 + j * 44, 350, 20, fr, PL, WHITE, 0.4)
    sg = S.cue('un signal')
    box(c, t, S.cue('si la réponse change'), 90, 910, 900, 120,
        'Réponse différente : *signal*', WHITE, DARK, 36, 'Medium', 30, 'up')
    if t >= S.cue('si la réponse change') + 0.4:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, 910, 990, 1030), 30, 30), _paint(RED, 4))
    icon(c, t, sg, 'eye', 160, 970, 50, RED)
    ev = S.cue('vos evals')
    card(c, t, ev, 90, 1080, 900, 340, DARK, 36, 'up')
    if prog(t, ev, 0.5) > 0.4:
        small(c, 'Evals', 140, 1140, 22, WHITE)
        for k in range(6):
            x = 140 + k * 130
            dot(c, t, ev + 0.2 + k * 0.08, x + 25, 1210, 22, PL)
            dot(c, t, ev + 0.25 + k * 0.08, x + 70, 1210, 22, WHITE)
        rj = S.cue('on les rejoue')
        x = 140
        for s, kw in [('Nouveau modèle', 'changement de modèle'), ('Nouveau prompt', 'ou de prompt')]:
            w = chip(c, t, S.cue(kw), s, x, 1290, RED, WHITE, 30)
            x += w + 20
        icon(c, t, rj, 'gear', 900, 1325, 60, WHITE)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Les usages *sensibles*')
    a = S.cue('plus de prudence')
    x = 90
    for s, kw in [('Recrutement', 'le recrutement'), ('Crédit', 'le crédit'), ('Accès à un service', "l'accès à un service")]:
        w = chip(c, t, S.cue(kw), s, x, 560, LIGHT, DARK, 32)
        x += w + 16
    ai = S.cue("l'AI Act")
    card(c, t, ai, 90, 680, 900, 260, LIGHT, 36, 'up')
    if prog(t, ai, 0.5) > 0.4:
        icon(c, t, ai + 0.1, 'shield', 190, 810, 90, RED)
        reveal_plain(c, t, ai + 0.2, 'Règlement européen sur l\'IA', 280, 780, 32, DARK)
        hr = S.cue('à haut risque')
        label(c, t, hr, 'Certains usages : haut risque', 280, 830, RED, WHITE, 22)
    rv = S.cue('revue humaine')
    if t >= rv:
        small(c, 'Revue humaine', 90, 1010, 22, RED)
    box(c, t, rv, 90, 1040, 380, 160, 'Le modèle *aide*', LIGHT, DARK, 34)
    de = S.cue('une personne décide')
    arrow(c, t, de - 0.3, 485, 1120, 595, 1120, DARK, 6)
    box(c, t, de, 610, 1040, 380, 160, 'Une personne *décide*', RED, WHITE, 34, accent=WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles décisions touchent *directement des personnes* ?', 'Quelles décisions'),
        ('Quelles *paires de test*, sur quels attributs ?', 'Quelles paires'),
        ('Qui *relit* les cas sensibles avant de décider ?', 'qui relit'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un modèle *reflète* les biais de ses données.', 'un modèle reflète'),
        ('Testez par *paires*, gardez un *humain* sur les cas sensibles.', 'On les teste'),
    ], '27 · Mesurer la valeur')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle n'a pas d'opinion. "
        "Pourtant, il peut traiter deux personnes différemment, à dossier identique.")),
    dict(kind='content', draw=s2, name="D'où vient le biais", text=(
        "Pourquoi ? Un modèle apprend à partir d'énormes volumes de textes écrits par des humains. "
        "Il en reprend les régularités, y compris les stéréotypes. "
        "Si les textes associent plus souvent un métier à un genre, le modèle reproduit cette association. "
        "Il reflète ses données, il ne les corrige pas.")),
    dict(kind='content', draw=s3, name='Deux exemples', text=(
        "Concrètement, cela se voit de deux façons. "
        "Dans une analyse de dossier : même parcours, même expérience, "
        "mais une appréciation différente selon le prénom ou le genre. "
        "Dans une rédaction : une offre d'emploi qui glisse vers un stéréotype, "
        "sans que personne ne l'ait demandé.")),
    dict(kind='content', draw=s4, name='Tester avec des paires', text=(
        "Comment le détecter ? Avec des paires de cas. "
        "Vous prenez un dossier, vous le dupliquez, et vous ne changez qu'un seul attribut : le prénom, par exemple. "
        "Si la réponse change, c'est un signal. "
        "Ces paires entrent dans vos evals, et on les rejoue à chaque changement de modèle ou de prompt.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, certains usages demandent plus de prudence : le recrutement, le crédit, l'accès à un service. "
        "Le règlement européen sur l'intelligence artificielle, l'AI Act, classe certains de ces usages à haut risque, "
        "avec des obligations renforcées. "
        "Prévoyez alors une revue humaine : le modèle aide, une personne décide.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles décisions touchent directement des personnes ? "
        "Quelles paires de test allez-vous construire, et sur quels attributs ? "
        "Et qui relit les cas sensibles avant toute décision ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un modèle reflète les biais de ses données. "
        "On les teste par paires, dans les evals, et un humain garde la main sur les usages sensibles. "
        "Prochaine capsule : mesurer la valeur, ou comment prouver qu'un projet d'IA apporte vraiment quelque chose.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
