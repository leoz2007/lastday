import math

from engine import *  # noqa
from engine import _paint  # noqa

NUM = 23
TITLE = 'RETOURS UTILISATEURS'
FULL_TITLE = 'Retours utilisateurs'
SLUG = 'retours_utilisateurs'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Vos utilisateurs mécontents se *taisent*.')
    a = S.cue('ne vous diront rien')
    pa = S.cue('Ils partent')
    un = S.cue('chaque retour')
    # une foule d'utilisateurs : la plupart s'éloignent sans rien dire, un seul parle
    cols, rows = 6, 3
    for k in range(cols * rows):
        i, j = k % cols, k // cols
        x, y = 160 + i * 150, 900 + j * 140
        speaker = (k == 8)
        if not speaker and t >= pa:
            # ceux qui partent glissent vers la droite et deviennent pâles
            u = ease(prog(t, pa + 0.05 * k, 0.8))
            x += u * 30
            col = PL if u > 0.5 else WHITE
        else:
            col = RED if (speaker and t >= un) else WHITE
        icon(c, t, a + 0.04 * k, 'user', x, y, 70, col)
    if t >= un:
        chip(c, t, un + 0.2, '1 retour', 540, 1330, RED, WHITE, 34, align='center')


def s2(c, t, S):
    header(c, t, S, 'Les formes', 'Quatre *types* de retour')
    rows = [('check', 'Pouce haut ou bas', 'Bien ou pas, sans le pourquoi', 'Le pouce', 0.25),
            ('code', 'Correction', 'La réponse attendue', 'La correction', 0.95),
            ('shield', 'Signalement', 'Un contenu gênant', 'Le signalement', 0.55),
            ('chat', 'Commentaire', "L'explication", 'le commentaire libre', 0.75)]
    rich = S.cue('pauvre')
    for k, (ic, nm, ds, kw, fr) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 185
        card(c, t, at, 90, y, 900, 160, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            dot(c, t, at + 0.05, 170, y + 80, 48, RED if k == 1 else WHITE)
            icon(c, t, at + 0.1, ic, 170, y + 80, 50, WHITE if k == 1 else DARK)
            reveal_plain(c, t, at + 0.15, nm, 250, y + 70, 34, DARK, 'Medium')
            reveal_plain(c, t, at + 0.25, ds, 250, y + 120, 26, DARK, 'Medium')
            if t >= rich:
                bar(c, t, max(at, rich) + 0.2, 770, y + 68, 180, 24, fr, RED if k == 1 else PL, WHITE, 0.6)
    if t >= rich:
        small(c, 'Information', 950, 545, 20, DARK, align='right')
    ex = S.cue('un conseiller')
    card(c, t, ex, 90, 1310, 900, 120, PLL, 30, 'up')
    if prog(t, ex, 0.5) > 0.4:
        plain(c, 'Montant : 120 €', 140, 1385, 32, DARK, 'Medium')
        c.drawLine(140, 1374, 140 + text_width('Montant : 120 €', font('Medium', 32)), 1374, _paint(RED, 4))
        reveal_plain(c, t, ex + 0.5, 'corrigé en 85 €', 450, 1385, 32, RED, 'Medium')
        small(c, 'Exemple', 940, 1385, 20, DARK, align='right')


def s3(c, t, S):
    header(c, t, S, 'Le piège', 'Un retour rare et *biaisé*')
    a = S.cue('très contents')
    card(c, t, S.cue('rare, et biaisé'), 90, 540, 900, 420, LIGHT, 36, 'up')
    if prog(t, S.cue('rare, et biaisé'), 0.5) > 0.4:
        small(c, 'Qui clique ? (illustratif)', 140, 600, 22, DARK)
        hs = [0.85, 0.3, 0.12, 0.35, 0.9]
        names = ['Fâchés', '', 'Neutres', '', 'Ravis']
        for k, h in enumerate(hs):
            x = 160 + k * 160
            hh = 240 * h * ease(prog(t, a + 0.1 * k, 0.6))
            if hh > 1:
                rrect(c, x, 880 - hh, 120, hh, 16, RED if k in (0, 4) else PL)
            if names[k] and t >= a:
                small(c, names[k], x + 60, 925, 20, DARK, align='center')
    si = S.cue('Le silence')
    if t >= si:
        reveal_plain(c, t, si, 'Silence ne veut pas dire satisfaction', 540, 1015, 30, RED, 'Medium', 'center')
    fa = S.cue('facile')
    card(c, t, fa, 90, 1060, 900, 380, LIGHT, 36, 'up')
    if prog(t, fa, 0.5) > 0.4:
        small(c, 'Assistant', 140, 1115, 20, DARK)
        for j, w in enumerate([760, 620]):
            rrect(c, 140, 1140 + j * 44, w, 24, 12, PL)
        # deux boutons sous la réponse
        for j, ic in enumerate(['check', 'cross']):
            x = 180 + j * 110
            dot(c, t, fa + 0.2 + j * 0.1, x, 1270, 40, RED if j == 1 else WHITE)
            icon(c, t, fa + 0.25 + j * 0.1, ic, x, 1270, 40, WHITE if j == 1 else DARK)
        small(c, 'Un clic', 360, 1280, 22, DARK)
        ctx = S.cue('contextualisé')
        x = 140
        for k, (s, kw) in enumerate([('Question', 'la question'), ('Réponse', 'la réponse'),
                                     ('Version du prompt', 'la version')]):
            w = chip(c, t, max(ctx, S.cue(kw)), s, x, 1340, WHITE, DARK, 28)
            x += w + 14


def s4(c, t, S):
    header(c, t, S, 'Le tri', 'Du retour au *cas de test*')
    rt = S.cue("type d'erreur")
    box(c, t, S.cue('on trie'), 90, 560, 260, 120, 'Retours', LIGHT, DARK, 34)
    cats = [('Réponse fausse', 'réponse fausse', 0.8), ('Ton inadapté', 'ton inadapté', 0.35),
            ('Document manquant', 'document manquant', 0.55)]
    arrow(c, t, rt, 360, 620, 420, 620, DARK, 6, 18)
    for k, (s, kw, fr) in enumerate(cats):
        at = S.cue(kw)
        y = 545 + k * 60
        reveal_plain(c, t, at, s, 430, y + 30, 28, DARK, 'Medium')
        bar(c, t, at + 0.1, 790, y + 10, 200, 26, fr, RED if k == 0 else PL, LIGHT, 0.6)
    tr = S.cue('sa trace')
    card(c, t, tr, 90, 760, 900, 300, LIGHT, 36, 'up')
    if prog(t, tr, 0.5) > 0.4:
        label(c, t, tr + 0.1, 'Trace', 140, 795, PLL, DARK, 22)
        items = [('user', 'Question'), ('doc', 'Documents'), ('chat', 'Réponse'), ('cross', 'Pouce bas')]
        for k, (ic, s) in enumerate(items):
            x = 210 + k * 220
            icon(c, t, tr + 0.3 + k * 0.15, ic, x, 930, 56, RED if k == 3 else DARK)
            if t >= tr + 0.3 + k * 0.15:
                small(c, s, x, 1010, 20, DARK, align='center')
            if k < 3:
                arrow(c, t, tr + 0.4 + k * 0.15, x + 50, 930, x + 165, 930, PL, 5, 14)
    ct = S.cue('cas de test')
    arrow(c, t, ct, 540, 1070, 540, 1140, RED, 6, 18)
    card(c, t, ct + 0.2, 90, 1150, 900, 280, RED, 36, 'up')
    if prog(t, ct + 0.2, 0.5) > 0.4:
        small(c, 'Evals', 140, 1210, 22, WHITE)
        for k, s in enumerate(['Cas 41 · montant de remboursement', 'Cas 42 · ton trop familier']):
            y = 1270 + k * 70
            icon(c, t, ct + 0.4 + k * 0.2, 'check', 165, y, 40, WHITE)
            reveal_plain(c, t, ct + 0.4 + k * 0.2, s, 210, y + 12, 30, WHITE)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "Une *boucle* d'amélioration")
    cx, cy, r = 540, 900, 270
    nodes = [('Collecter', 'on collecte'), ('Analyser', 'on analyse'), ('Corriger', 'on corrige'),
             ('Vérifier', 'on vérifie'), ('Déployer', 'on déploie')]
    n = len(nodes)
    for k in range(n):
        a1 = math.radians(-90 + k * 72 + 20)
        a2 = math.radians(-90 + (k + 1) * 72 - 20)
        nxt = S.cue(nodes[k + 1][1]) if k < n - 1 else S.cue('ce qui a changé')
        arrow(c, t, nxt - 0.2, cx + r * math.cos(a1), cy + r * math.sin(a1),
              cx + r * math.cos(a2), cy + r * math.sin(a2), PL, 6, 18)
    for k, (s, kw) in enumerate(nodes):
        at = S.cue(kw)
        a = math.radians(-90 + k * 72)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        box(c, t, at, x - 115, y - 45, 230, 90, s, RED if k == 2 else LIGHT, WHITE if k == 2 else DARK, 30)
    bl = S.cue('continue')
    icon(c, t, bl, 'gear', cx, cy - 10, 80, RED)
    gr = S.cue('grâce à eux')
    chip(c, t, gr, 'Corrigé grâce à vos retours', 540, 1290, PLL, DARK, 34, align='center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quels retours recueillir, et *où* à l\'écran ?', 'Quels retours'),
        ('Qui les *lit*, et à quelle fréquence ?', 'Qui les lit'),
        ('Comment un retour devient-il un *cas de test* ?', 'Et comment'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un retour est rare : rendez-le *facile* et gardez son *contexte*.', 'un retour est rare'),
        ('Reliez-le à sa *trace* et faites-en un *test*.', 'Triez-les'),
    ], '24 · Maîtriser les coûts en production')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Vos utilisateurs mécontents ne vous diront rien, pour la plupart. Ils partent, simplement. "
        "Alors chaque retour est précieux, à condition de savoir le recueillir et de s'en servir.")),
    dict(kind='content', draw=s2, name='Quatre types de retour', text=(
        "Un retour prend plusieurs formes. Le pouce, en haut ou en bas, est rapide, mais pauvre en information. "
        "La correction est la plus riche : quand un conseiller rectifie un montant dans la réponse, on sait ce qui était attendu. "
        "Le signalement alerte sur un contenu gênant. Et le commentaire libre explique le pourquoi.")),
    dict(kind='content', draw=s3, name='Rare et biaisé', text=(
        "Mais un retour est rare, et biaisé. Ceux qui cliquent sont souvent les très contents ou les très fâchés. "
        "Le silence ne veut pas dire satisfaction. "
        "Alors rendez le retour facile : un clic, juste sous la réponse. "
        "Et contextualisé : on enregistre la question, la réponse et la version du prompt.")),
    dict(kind='content', draw=s4, name='Du retour au cas de test', text=(
        "Ensuite, on trie. On regroupe les retours par type d'erreur : réponse fausse, ton inadapté, document manquant. "
        "Chaque retour est relié à sa trace, l'enregistrement complet de l'échange. "
        "Les cas les plus parlants deviennent des cas de test dans vos evals. "
        "Une erreur signalée une fois ne revient plus en silence.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, c'est une boucle d'amélioration continue. "
        "On collecte, on analyse, on corrige le prompt ou les données, on vérifie sur les evals, puis on déploie. "
        "Et dites aux utilisateurs ce qui a changé grâce à eux : c'est ce qui leur donne envie de recommencer.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels retours voulez-vous recueillir, et à quel endroit de l'écran ? "
        "Qui les lit, et à quelle fréquence ? "
        "Et comment un retour devient-il un cas de test ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un retour est rare, rendez-le facile et gardez son contexte. "
        "Triez-les, reliez-les aux traces, et faites-en des tests. "
        "Prochaine capsule : maîtriser les coûts en production.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
