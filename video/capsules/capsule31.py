from engine import *  # noqa
from engine import _paint  # noqa

NUM = 31
TITLE = "OPTIMISER L'INFÉRENCE"
FULL_TITLE = "Optimiser l'inférence"
SLUG = 'optimiser_inference'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def chips_row(c, t, at, words, x, y, fill, fg, size=34, gap=16, step=0.12):
    """Une rangée de pastilles ; renvoie la liste des (x, largeur)."""
    out = []
    for k, w in enumerate(words):
        wd = chip(c, t, at + k * step, w, x, y, fill, fg, size)
        out.append((x, wd))
        x += wd + gap
    return out


def s1(c, t, S):
    opening(c, t, S, CAP, 'Plus *rapide*, moins *cher*, presque aussi bon.')
    a = S.t0 + 0.6
    dot(c, t, a, 105, 850, 12, PL)
    dot(c, t, a + 0.1, 285, 850, 12, RED)
    if t >= a:
        small(c, 'Avant', 130, 859, 24, WHITE)
        small(c, 'Après', 310, 859, 24, WHITE)
    inf = S.cue("l'inférence")
    s = "À l'inférence"
    chip(c, t, inf, s, 990 - chip_width(s, 30), 825, WHITE, RED, 30)
    rows = [('Délai', 'plus vite', 0.9, 0.45, RED), ('Coût', 'moins cher', 0.9, 0.4, RED),
            ('Qualité', 'presque égale', 0.9, 0.86, WHITE)]
    for k, (nm, kw, f1, f2, col) in enumerate(rows):
        at = S.cue(kw)
        y = 960 + k * 160
        if t >= at - 0.2:
            small(c, nm, 90, y, 24, WHITE)
        bar(c, t, at, 90, y + 22, 900, 30, f1, PL, DARK, 0.6)
        bar(c, t, at + 0.3, 90, y + 66, 900, 30, f2, col, DARK, 0.6)
    if t >= S.cue('presque égale') + 0.6:
        small(c, 'Illustratif', 990, 1430, 20, WHITE, align='right')


def s2(c, t, S):
    header(c, t, S, 'Alléger le modèle', 'Moins de *précision*, un *élève*')
    q = S.cue('La quantification')
    card(c, t, q, 90, 540, 900, 420, LIGHT, 36, 'up')
    if prog(t, q, 0.5) > 0.4:
        small(c, 'Quantification · un poids stocké', 140, 600, 20, DARK)
        chip(c, t, q + 0.2, '0,7348291', 140, 630, PL, DARK, 40)
        mp = S.cue('moins de précision')
        arrow(c, t, mp, 440, 665, 540, 665, DARK, 6, 18)
        chip(c, t, mp + 0.3, '0,73', 560, 630, RED, WHITE, 40)
        lg = S.cue('plus léger')
        if t >= lg - 0.2:
            small(c, 'Mémoire · illustratif', 140, 780, 20, DARK)
            plain(c, 'Avant', 140, 832, 28, DARK)
            plain(c, 'Après', 140, 890, 28, RED)
        bar(c, t, lg, 300, 806, 640, 32, 1.0, PL, WHITE, 0.6)
        bar(c, t, lg + 0.3, 300, 864, 640, 32, 0.5, RED, WHITE, 0.6)
        pq = S.cue('perte de qualité')
        if t >= pq:
            icon(c, t, pq, 'eye', 820, 665, 56, DARK)
            reveal_plain(c, t, pq, 'Qualité à vérifier', 940, 740, 24, RED, 'Medium', 'right')
    d = S.cue('La distillation')
    card(c, t, d, 90, 1000, 900, 430, LIGHT, 36, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Distillation', 140, 1060, 20, DARK)
        dot(c, t, d + 0.2, 240, 1210, 90, DARK)
        icon(c, t, d + 0.3, 'brain', 240, 1210, 80, WHITE)
        small(c, 'Grand modèle', 240, 1350, 20, DARK, align='center')
        im = S.cue('imiter')
        arrow(c, t, im, 350, 1210, 720, 1210, DARK, 6, 18)
        for k in range(3):
            icon(c, t, im + 0.2 + k * 0.15, 'doc', 430 + k * 105, 1150, 44, DARK)
        dot(c, t, im + 0.5, 800, 1210, 55, RED)
        icon(c, t, im + 0.6, 'brain', 800, 1210, 50, WHITE)
        if t >= im + 0.5:
            small(c, 'Petit modèle', 800, 1350, 20, DARK, align='center')
        tk = S.cue('classer des tickets')
        chip(c, t, tk, 'Une tâche : classer des tickets', 535, 1250, WHITE, DARK, 24, align='center')


def s3(c, t, S):
    header(c, t, S, 'Mieux utiliser le matériel', 'Regrouper et *réutiliser*')
    b = S.cue('Le batching')
    card(c, t, b, 90, 540, 900, 420, LIGHT, 36, 'up')
    if prog(t, b, 0.5) > 0.4:
        small(c, 'Batching · traitement par lots', 140, 600, 20, DARK)
        for k in range(6):
            icon(c, t, b + 0.2 + k * 0.08, 'chat', 180 + (k % 3) * 95, 690 + (k // 3) * 95, 56, DARK)
        en = S.cue('les calculer ensemble')
        arrow(c, t, en, 460, 737, 580, 737, DARK, 6, 18)
        card(c, t, en + 0.3, 600, 650, 340, 175, RED, 30, 'pop')
        if prog(t, en + 0.3, 0.5) > 0.4:
            icon(c, t, en + 0.4, 'gear', 680, 737, 64, WHITE)
            plain(c, 'Un lot', 740, 750, 36, WHITE, 'Medium')
        dv = S.cue('en traite davantage')
        if t >= dv:
            icon(c, t, dv, 'check', 160, 905, 40, RED)
            reveal_plain(c, t, dv, 'Plus de requêtes', 195, 916, 28, DARK)
        at_ = S.cue('attend un peu')
        if t >= at_:
            icon(c, t, at_, 'clock', 620, 905, 40, RED)
            reveal_plain(c, t, at_, "Un peu d'attente", 660, 916, 28, DARK)
    cp = S.cue('Le cache de prompt')
    card(c, t, cp, 90, 1000, 900, 430, LIGHT, 36, 'up')
    if prog(t, cp, 0.5) > 0.4:
        small(c, 'Cache de prompt · appels successifs', 140, 1060, 20, DARK)
        di = S.cue('début de prompt identique')
        for k in range(3):
            y = 1095 + k * 70
            at = cp + 0.2 + k * 0.15
            col = RED if (k > 0 and t >= di + 0.2 * k) else PL
            bar(c, t, at, 140, y, 540, 44, 1.0, col, WHITE, 0.4)
            bar(c, t, at + 0.15, 700, y, 240, 44, 1.0, DARK, WHITE, 0.4)
        if t >= di:
            reveal_plain(c, t, di, 'Même début : calcul réutilisé', 140, 1350, 28, RED, 'Medium')
            reveal_plain(c, t, di + 0.2, 'Question', 940, 1350, 28, DARK, 'Medium', 'right')


def s4(c, t, S):
    header(c, t, S, 'Décodage spéculatif', 'Le petit *propose*, le grand *valide*')
    words = ['Votre', 'colis', 'arrive', 'demain']
    p = S.cue('propose')
    card(c, t, p, 90, 540, 900, 250, LIGHT, 36, 'up')
    if prog(t, p, 0.5) > 0.4:
        small(c, 'Petit modèle · propose plusieurs mots', 140, 600, 20, DARK)
        chips_row(c, t, p + 0.2, words, 140, 650, PLL, DARK, 36)
    v = S.cue('les vérifie')
    card(c, t, v, 90, 830, 900, 360, LIGHT, 36, 'up')
    if prog(t, v, 0.5) > 0.4:
        small(c, 'Grand modèle · vérifie en une passe', 140, 890, 20, DARK)
        pos = chips_row(c, t, v + 0.1, words, 140, 930, WHITE, DARK, 36, step=0.05)
        ec = S.cue('premier écart')
        for k, (x, wd) in enumerate(pos[:3]):
            dot(c, t, v + 0.5 + k * 0.15, x + wd / 2, 1080, 26, RED)
            icon(c, t, v + 0.6 + k * 0.15, 'check', x + wd / 2, 1080, 28, WHITE)
        x, wd = pos[3]
        if t >= ec:
            icon(c, t, ec, 'cross', x + wd + 40, 963, 36, RED)
        chip(c, t, ec + 0.3, 'lundi', x + wd / 2, 1050, RED, WHITE, 36, align='center')
    pv = S.cue('plus vite')
    card(c, t, pv, 90, 1230, 900, 180, RED, 36, 'up')
    if prog(t, pv, 0.5) > 0.4:
        icon(c, t, pv + 0.1, 'bolt', 170, 1320, 60, WHITE)
        reveal_plain(c, t, pv + 0.2, 'Plus rapide', 230, 1308, 38, WHITE, 'Medium')
        sq = S.cue('sans perte')
        if t >= sq:
            reveal_plain(c, t, sq, 'En général, même réponse', 230, 1366, 30, WHITE, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Toujours *mesurer*')
    cp = S.cue('compromis')
    x = 90
    for k, s in enumerate(['Délai', 'Coût', 'Qualité']):
        w = chip(c, t, cp + k * 0.15, s, x, 545, PLL, DARK, 32)
        x += w + 16
    ev = S.cue('vos evals')
    card(c, t, ev, 90, 650, 900, 780, LIGHT, 36, 'up')
    if prog(t, ev, 0.5) > 0.4:
        label(c, t, ev + 0.1, 'Evals · chiffres illustratifs', 140, 690, PLL, DARK, 22)
        small(c, 'Avant', 520, 800, 20, DARK)
        small(c, 'Après', 760, 800, 20, RED)
        cc = S.cue('cas critiques')
        rows = [('Délai', 0.8, 0.45), ('Coût', 0.8, 0.4), ('Qualité', 0.9, 0.87), ('Cas critiques', 0.9, 0.5)]
        for j, (nm, f1, f2) in enumerate(rows):
            at = S.cue('avant et après') + j * 0.3 if j < 3 else cc
            y = 840 + j * 95
            if t >= at:
                plain(c, nm, 140, y + 28, 30, RED if j == 3 else DARK)
            bar(c, t, at, 520, y + 4, 210, 30, f1, PL, WHITE, 0.6)
            bar(c, t, at + 0.15, 760, y + 4, 210, 30, f2, RED, WHITE, 0.6)
        pg = S.cue("n'est pas un gain")
        if t >= pg:
            card(c, t, pg, 140, 1250, 800, 130, RED, 30, 'pop')
            if prog(t, pg, 0.5) > 0.4:
                icon(c, t, pg + 0.1, 'cross', 210, 1315, 50, WHITE)
                plain(c, 'Plus rapide, mais pas un gain', 260, 1327, 34, WHITE, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Qu'est-ce qui compte le plus : *délai*, *coût* ou *qualité* ?", "Qu'est-ce qui"),
        ('Quelle *perte de qualité* est acceptable, sur quels cas ?', 'Quelle perte'),
        ('Quelles *evals* rejouer après chaque optimisation ?', 'Et quelles evals'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Alléger, regrouper, réutiliser : l\'inférence *s\'optimise*.', 'alléger le modèle'),
        ('Chaque gain se *vérifie* sur vos evals.', 'chaque gain'),
    ], '32 · Le RAG avancé')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un même assistant peut souvent répondre plus vite et coûter moins cher, à qualité presque égale. "
        "Tout se joue à l'inférence, le moment où le modèle calcule ses réponses.")),
    dict(kind='content', draw=s2, name='Quantification et distillation', text=(
        "Première piste : alléger le modèle. La quantification stocke ses poids, les nombres appris à l'entraînement, "
        "avec moins de précision, comme une photo compressée. Le modèle devient plus léger, souvent plus rapide, "
        "avec parfois une légère perte de qualité. La distillation, elle, entraîne un petit modèle à imiter un grand, "
        "sur une seule tâche, par exemple classer des tickets.")),
    dict(kind='content', draw=s3, name='Batching et cache de prompt', text=(
        "Deuxième piste : mieux utiliser le matériel. Le batching, ou traitement par lots, regroupe plusieurs requêtes "
        "pour les calculer ensemble. Le serveur en traite davantage, mais chacune attend un peu. "
        "Le cache de prompt réutilise le calcul d'un début de prompt identique, "
        "comme de longues consignes répétées à chaque appel.")),
    dict(kind='content', draw=s4, name='Le décodage spéculatif', text=(
        "Troisième piste : le décodage spéculatif. Un petit modèle rapide propose plusieurs mots d'avance. "
        "Le grand modèle les vérifie d'un coup, garde ceux qu'il aurait écrits, et corrige au premier écart. "
        "Quand le petit devine bien, la réponse arrive plus vite, en général sans perte de qualité.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, chaque optimisation est un compromis entre délai, coût et qualité. "
        "Mesurez toujours son effet sur vos evals, avant et après. "
        "Un modèle plus rapide qui se trompe davantage sur vos cas critiques n'est pas un gain.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Qu'est-ce qui compte le plus ici : le délai, le coût ou la qualité ? "
        "Quelle perte de qualité est acceptable, et sur quels cas ? "
        "Et quelles evals rejoue-t-on après chaque optimisation ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : alléger le modèle, regrouper les requêtes, réutiliser le calcul, l'inférence s'optimise. "
        "Mais chaque gain se vérifie sur vos evals. "
        "Prochaine capsule : le RAG avancé, pour retrouver les bons passages.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
