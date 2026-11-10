from engine import *  # noqa
from engine import _paint  # noqa

NUM = 6
TITLE = 'EVALS'
FULL_TITLE = 'Évaluation (evals)'
SLUG = 'evaluation_evals'
NEXT_CUE = 'prochaine capsule'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Trois exemples en démo ne *prouvent* rien.')
    a = S.cue('trois exemples')
    for k in range(3):
        x = 90 + k * 160
        card(c, t, a + k * 0.2, x, 820, 140, 140, LIGHT, 28)
        icon(c, t, a + 0.3 + k * 0.2, 'check', x + 70, 890, 60, RED)
    if t >= a:
        small(c, 'Démo', 90, 1010, 22, WHITE)
    s = S.cue('Sans évaluation')
    for k in range(40):
        col, row = k % 10, k // 10
        dot(c, t, s + k * 0.025, 110 + col * 96, 1080 + row * 75, 16, PL)
    if t >= s + 0.8:
        chip(c, t, s + 0.8, 'Et tous les autres cas ?', 90, 1360, RED, WHITE, 34)


def s2(c, t, S):
    header(c, t, S, 'Jeu de tests', 'Des cas et des *réponses attendues*')
    a = S.cue('jeu de tests')
    card(c, t, a, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Question', 140, 610, 22, DARK)
        rq = S.cue('réponse attendue')
        if t >= rq:
            small(c, 'Attendu', 560, 610, 22, RED)
        for k in range(4):
            y = 650 + k * 68
            bar(c, t, S.cue('questions réelles') + k * 0.15, 140, y, 360, 26, 0.6 + 0.1 * (k % 3), PL, WHITE, 0.4)
            bar(c, t, rq + k * 0.15, 560, y, 380, 26, 0.5 + 0.12 * ((k + 1) % 3), RED, WHITE, 0.4)
    ca = S.cue("critères d'acceptation")
    chip(c, t, ca, "= vos critères d'acceptation", 90, 960, DARK, WHITE, 32)
    ex = S.cue('cinquante questions')
    pi = S.cue('dix pièges')
    for k in range(50):
        col, row = k % 10, k // 10
        x, y = 100 + col * 90, 1080 + row * 62
        at = ex + k * 0.015
        p = back(prog(t, at, 0.3))
        if p > 0:
            col_ = RED if (k >= 40 and t >= pi) else PL
            rrect(c, x + 30 * (1 - p), y + 22 * (1 - p), 60 * p, 44 * p, 12, col_)
    x = 90
    for s, kw in [('Hors sujet', 'hors sujet'), ('Ambiguës', 'ambiguës'), ('Malveillantes', 'malveillantes')]:
        w = chip(c, t, S.cue(kw), s, x, 1400, PLL, DARK, 30)
        x += w + 16


def s3(c, t, S):
    header(c, t, S, 'Mesurer', 'Des critères, pas un *texte exact*')
    a = S.cue('deux réponses différentes')
    for k in range(2):
        x = 90 + k * 460
        card(c, t, a + k * 0.3, x, 540, 440, 230, LIGHT, 30, 'up')
        if prog(t, a + k * 0.3, 0.5) > 0.4:
            small(c, f'Réponse {"AB"[k]}', x + 40, 600, 22, DARK)
            for j, fr in enumerate([[0.9, 0.5, 0.7], [0.6, 0.85, 0.4]][k]):
                bar(c, t, a + k * 0.3 + 0.2, x + 40, 630 + j * 40, 360, 20, fr, PL, WHITE, 0.4)
    cr = [('Juste', 'juste'), ('Complète', 'complète'), ('Fidèle aux sources', 'fidèle'), ('Polie', 'polie')]
    y = 840
    for k, (s, kw) in enumerate(cr):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        yy = y + (k // 2) * 120
        card(c, t, at, x, yy, 440, 100, LIGHT, 28, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, 'check', x + 55, yy + 50, 50, RED)
            plain(c, s, x + 100, yy + 62, 32, DARK)
    tr = S.cue('taux de réussite')
    card(c, t, tr, 90, 1130, 900, 300, LIGHT, 32, 'up')
    if prog(t, tr, 0.5) > 0.4:
        small(c, 'Taux de réussite sur tout le jeu', 140, 1200, 22, DARK)
        bar(c, t, tr + 0.3, 140, 1240, 800, 40, 0.82, RED, WHITE, 1.2)
        im = S.cue('une impression')
        if t >= im:
            reveal_plain(c, t, im, 'et non une impression sur un exemple', 140, 1360, 30, DARK)


def s4(c, t, S):
    header(c, t, S, 'LLM-as-judge', 'Un modèle *juge* les réponses')
    ins = [('Question', 'la question'), ('Réponse', 'la réponse'), ('Grille de notation', 'grille')]
    for k, (s, kw) in enumerate(ins):
        at = S.cue(kw)
        box(c, t, at, 90, 540 + k * 130, 440, 110, s, LIGHT, DARK, 32, 'Medium', 28, 'left')
        arrow(c, t, at + 0.3, 540, 595 + k * 130, 620, 720, DARK, 5, 16)
    j = S.cue('comme juge')
    box(c, t, j, 630, 610, 360, 220, 'Modèle *juge*', RED, WHITE, 40, 'Light', 32, accent=WHITE)
    g = S.cue('grille')
    chip(c, t, g + 0.8, 'Note : 4 / 5', 680, 870, PLL, DARK, 32)
    cal = S.cue('se calibre')
    card(c, t, cal, 90, 990, 900, 450, LIGHT, 36, 'up')
    if prog(t, cal, 0.5) > 0.4:
        label(c, t, cal + 0.1, 'Calibrage', 140, 1030, PLL, DARK, 22)
        hu = S.cue('experts humains')
        vals = [(0.8, 0.75), (0.5, 0.55), (0.9, 0.85), (0.6, 0.65)]
        for k, (a1, a2) in enumerate(vals):
            x = 160 + k * 150
            h1, h2 = 260 * a1, 260 * a2
            p1 = ease(prog(t, cal + 0.3 + k * 0.1, 0.6))
            rrect(c, x, 1380 - h1 * p1, 50, h1 * p1, 14, RED) if p1 > 0 else None
            p2 = ease(prog(t, hu + k * 0.1, 0.6))
            if p2 > 0:
                rrect(c, x + 60, 1380 - h2 * p2, 50, h2 * p2, 14, PL)
        if t >= cal + 0.3:
            small(c, 'Juge', 790, 1200, 22, RED)
        if t >= hu:
            icon(c, t, hu, 'user', 820, 1300, 60, DARK)
            small(c, 'Experts', 790, 1400, 22, DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Une *recette* continue')
    x = 90
    for s, kw in [('Prompt', 'de prompt'), ('Documents', 'de documents'), ('Modèle', 'de modèle')]:
        w = chip(c, t, S.cue(kw), s, x, 540, PLL, DARK, 34)
        x += w + 16
    r = S.cue('on relance')
    arrow(c, t, r, 540, 630, 540, 690, DARK, 6)
    box(c, t, r, 90, 700, 900, 130, 'On relance le *jeu de tests*', LIGHT, DARK, 38)
    sb = S.cue('le score baisse')
    card(c, t, sb, 90, 890, 900, 200, RED, 32, 'up')
    if prog(t, sb, 0.5) > 0.4:
        icon(c, t, sb + 0.1, 'cross', 180, 990, 70, WHITE)
        text_block(c, t, sb + 0.2, 'Score en baisse : pas de mise en production', 250, 975, 36, 'Medium',
                   WHITE, WHITE, maxw=700, max_lines=2)
    er = S.cue('Et les erreurs')
    card(c, t, er, 90, 1150, 900, 280, LIGHT, 32, 'up')
    if prog(t, er, 0.5) > 0.4:
        box(c, t, er + 0.2, 130, 1210, 330, 160, 'Erreurs en production', WHITE, DARK, 30)
        arrow(c, t, er + 0.6, 475, 1290, 600, 1290, RED, 6)
        en = S.cue('enrichissent')
        box(c, t, en, 620, 1210, 330, 160, 'Nouveaux cas de test', RED, WHITE, 30)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Qui écrit les *cas de test* et les réponses attendues ?', 'Qui écrit'),
        ('Quel *score minimum* pour passer en production ?', 'Quel score'),
        ('Qui, côté métier, *valide le juge* ?', 'Qui, côté métier'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Pas de mise en production sans *jeu de tests*.', 'pas de mise'),
        ('Des critères, un score, une recette *relancée à chaque changement*.', 'Des critères'),
    ], '07 · Choix du modèle, coûts et latence')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un assistant qui réussit trois exemples en démo ne prouve rien. "
        "Sans évaluation, vous ne savez pas s'il marche vraiment, ni s'il marchera encore demain.")),
    dict(kind='content', draw=s2, name='Le jeu de tests', text=(
        "Une évaluation commence par un jeu de tests : une liste de questions réelles, "
        "avec pour chacune la réponse attendue, ou les critères d'une bonne réponse. "
        "C'est l'équivalent de vos critères d'acceptation. "
        "Par exemple, cinquante questions de clients, dont dix pièges : hors sujet, ambiguës ou malveillantes.")),
    dict(kind='content', draw=s3, name='Des critères et un score', text=(
        "Avec un LLM, la même question peut produire deux réponses différentes. "
        "On ne vérifie donc pas un texte exact, mais des critères : la réponse est-elle juste, complète, fidèle aux sources, polie ? "
        "On mesure un taux de réussite sur tout le jeu, pas une impression sur un exemple.")),
    dict(kind='content', draw=s4, name='Le LLM-as-judge', text=(
        "Pour noter des centaines de réponses, on utilise souvent un autre modèle comme juge : c'est le LLM-as-judge. "
        "On lui donne la question, la réponse et une grille de notation précise. "
        "Mais un juge se calibre : on compare régulièrement ses notes à celles d'experts humains, sur un échantillon.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, les evals deviennent votre recette continue. "
        "À chaque changement de prompt, de documents ou de modèle, on relance le jeu de tests. "
        "Si le score baisse, on ne met pas en production. "
        "Et les erreurs vues en production enrichissent le jeu de tests.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Qui écrit les cas de test et les réponses attendues ? "
        "Quel score minimum faut-il atteindre pour passer en production ? "
        "Et qui, côté métier, valide le juge ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : pas de mise en production sans jeu de tests. "
        "Des critères, un score, et une recette relancée à chaque changement. "
        "Prochaine capsule : choisir son modèle, entre qualité, coût et temps de réponse.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
