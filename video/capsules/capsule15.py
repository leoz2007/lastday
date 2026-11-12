from engine import *  # noqa
from engine import _paint  # noqa

NUM = 15
TITLE = 'MÉMOIRE'
FULL_TITLE = 'Mémoire et personnalisation'
SLUG = 'memoire_personnalisation'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def bubble(c, t, at, s, x, y, w, fill, fg, size=32, right=False):
    """Bulle de conversation d'une ligne ; (x, y) = coin haut gauche."""
    h = size * 2.2
    p = card(c, t, at, x, y, w, h, fill, 26, 'right' if right else 'left')
    if p > 0.4:
        dx = (1 if right else -1) * (1 - ease(p)) * 160
        plain(c, s, x + 30 + dx, y + h / 2 + size * 0.36, size, fg, 'Medium')
    return h


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un LLM ne se *souvient* de rien.')
    a1 = S.cue('Entre deux appels')
    for k in range(2):
        x = 90 + k * 560
        box(c, t, a1 + k * 0.3, x, 840, 340, 160, f'Appel {k + 1}', LIGHT, DARK, 36)
    z = S.cue('repart de zéro')
    if t >= z:
        icon(c, t, z, 'cross', 540, 920, 70, RED)
        small(c, 'Rien ne passe', 540, 1030, 22, WHITE, align='center')
    ap = S.cue("c'est l'application")
    card(c, t, ap, 90, 1150, 900, 250, RED, 36, 'up')
    if prog(t, ap, 0.5) > 0.4:
        icon(c, t, ap + 0.1, 'db', 200, 1275, 80, WHITE)
        text_block(c, t, ap + 0.2, "L'application garde la mémoire", 290, 1260, 38, 'Medium', WHITE, WHITE,
                   maxw=650, max_lines=2)
        arrow(c, t, ap + 0.5, 260, 1140, 260, 1010, WHITE, 5, 16)
        arrow(c, t, ap + 0.7, 820, 1140, 820, 1010, WHITE, 5, 16)


def s2(c, t, S):
    header(c, t, S, "L'historique", 'On *renvoie* toute la conversation')
    m1 = S.cue('mon vol est mardi')
    bubble(c, t, m1, 'Mon vol est mardi.', 330, 560, 660, LIGHT, DARK, 34, right=True)
    bubble(c, t, m1 + 0.8, "C'est noté.", 90, 670, 420, PLL, DARK, 34)
    m2 = S.cue('décale-le')
    bubble(c, t, m2, "Décale-le d'un jour.", 330, 780, 660, LIGHT, DARK, 34, right=True)
    rv = S.cue('renvoyée')
    ac = S.cue('À chaque message')
    card(c, t, ac, 90, 930, 900, 500, LIGHT, 36, 'up')
    if prog(t, ac, 0.5) > 0.4:
        label(c, t, ac + 0.1, 'Envoyé au modèle', 140, 970, WHITE, DARK, 22)
        rows = [('Mon vol est mardi.', m1, rv), ("C'est noté.", m1 + 0.8, rv), ("Décale-le d'un jour.", m2, m2)]
        for k, (s, at, hl) in enumerate(rows):
            y = 1060 + k * 100
            fill = RED if (k == 0 and t >= rv) else WHITE
            fg = WHITE if (k == 0 and t >= rv) else DARK
            if t >= at:
                box(c, t, at + 0.2, 140, y, 520, 80, s, fill, fg, 28, 'Medium', 20, 'left')
        arrow(c, t, rv - 0.3, 680, 1200, 750, 1200, DARK, 6)
        box(c, t, S.cue('suit le fil'), 770, 1100, 180, 200, 'LLM', DARK, WHITE, 40, 'Light', 28)


def s3(c, t, S):
    header(c, t, S, 'Résumés et préférences', 'Résumer et *retenir*')
    gr = S.cue('grossit')
    card(c, t, gr, 90, 550, 900, 380, LIGHT, 36, 'up')
    if prog(t, gr, 0.5) > 0.4:
        small(c, 'Historique', 140, 610, 22, DARK)
        n = int(1 + 11 * ease(prog(t, gr + 0.2, 1.5)))
        for k in range(n):
            rrect(c, 140 + k * 34, 640, 24, 130, 8, PL)
        li = S.cue('une limite')
        if t >= li:
            c.drawLine(520, 625, 520, 785, _paint(RED, 6))
            small(c, 'Limite du contexte', 535, 625, 18, RED)
        rs = S.cue('on résume')
        arrow(c, t, rs, 560, 860, 620, 860, DARK, 5, 16)
        chip(c, t, rs + 0.3, 'Résumé : 3 lignes', 640, 830, RED, WHITE, 28)
        if t >= rs:
            small(c, 'Anciens échanges', 140, 875, 20, DARK)
    pr = S.cue('préférences')
    card(c, t, pr, 90, 970, 900, 460, LIGHT, 36, 'up')
    if prog(t, pr, 0.5) > 0.4:
        label(c, t, pr + 0.1, 'Préférences stockées', 140, 1010, WHITE, DARK, 22)
        prefs = [('Répondre en anglais', 'répondez en anglais'), ('Végétarien', 'végétarien')]
        for k, (s, kw) in enumerate(prefs):
            at = S.cue(kw)
            chip(c, t, at, s, 140, 1100 + k * 90, WHITE, DARK, 32)
        ri = S.cue('réinjectées')
        arrow(c, t, ri, 560, 1180, 660, 1180, DARK, 6)
        box(c, t, ri + 0.3, 680, 1090, 260, 180, 'Prompt', RED, WHITE, 38)
        nc = S.cue('nouvelle conversation')
        if t >= nc:
            small(c, 'À chaque conversation', 810, 1330, 20, DARK, align='center')


def s4(c, t, S):
    header(c, t, S, "RAG sur l'historique", 'Chercher dans le *passé*')
    q = S.cue('Quel hôtel')
    chip(c, t, q, "« Quel hôtel m'aviez-vous conseillé à Lyon ? »", 90, 550, RED, WHITE, 30)
    mo = S.cue("mois d'échanges")
    card(c, t, mo, 90, 670, 560, 760, LIGHT, 36, 'up')
    rt = S.cue('retrouve')
    months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin']
    if prog(t, mo, 0.5) > 0.4:
        small(c, 'Historique archivé', 140, 730, 22, DARK)
        for k, m in enumerate(months):
            y = 770 + k * 105
            hit = (k == 2 and t >= rt)
            card(c, t, mo + 0.2 + k * 0.08, 140, y, 460, 80, RED if hit else WHITE, 20, 'left')
            if t >= mo + 0.4 + k * 0.08:
                plain(c, m, 170, y + 52, 28, WHITE if hit else DARK, 'Medium')
                for j in range(3):
                    rrect(c, 360 + j * 75, y + 32, 60, 16, 8, WHITE if hit else PLL)
    ch = S.cue('on cherche')
    icon(c, t, ch, 'search', 820, 820, 100, DARK)
    if t >= ch:
        small(c, 'Passages utiles', 820, 930, 22, DARK, align='center')
    arrow(c, t, rt, 610, 1030, 700, 1100, RED, 6)
    box(c, t, rt + 0.3, 700, 1060, 290, 220, 'Prompt + *mars*', LIGHT, DARK, 34)
    if t >= S.cue('seulement lui'):
        small(c, 'Un seul échange', 845, 1340, 20, RED, align='center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Une mémoire *visible*')
    co = S.cue('consentement')
    chip(c, t, co, 'Consentement', 90, 550, RED, WHITE, 32)
    rt = S.cue('ce qui est retenu')
    card(c, t, rt, 90, 660, 900, 440, LIGHT, 36, 'up')
    cr = S.cue('corriger')
    ef = S.cue('tout effacer')
    if prog(t, rt, 0.5) > 0.4:
        label(c, t, rt + 0.1, "Ce que l'assistant retient", 140, 700, WHITE, DARK, 22)
        items = ['Langue : anglais', 'Régime : végétarien', 'Ville : Lyon']
        for k, s in enumerate(items):
            y = 790 + k * 95
            gone = t >= ef + 0.2
            rrect(c, 140, y, 800, 75, 18, WHITE)
            if not gone:
                plain(c, s, 170, y + 48, 30, DARK, 'Medium')
            else:
                rrect(c, 170, y + 30, 300, 16, 8, PLL)
            if k == 0 and t >= cr and not gone:
                small(c, 'Modifier', 910, y + 47, 20, RED, align='right')
    ds = S.cue('désactiver')
    chip(c, t, ds, 'Désactiver', 90, 1140, LIGHT, DARK, 32)
    chip(c, t, ef, 'Tout effacer', 90 + chip_width('Désactiver', 32) + 20, 1140, RED, WHITE, 32)
    rz = S.cue('les résumés')
    parts = ['Historique', 'Résumés', 'Index']
    for k, s in enumerate(parts):
        x = 90 + k * 310
        at = rz + k * 0.2
        box(c, t, at, x, 1260, 280, 150, s, LIGHT, DARK, 32)
        icon(c, t, at + 0.3, 'cross', x + 250, 1280, 40, RED)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Que *retenir*, et combien de temps ?', 'Que faut-il'),
        ("Où l'utilisateur *voit*-il et corrige-t-il sa mémoire ?", "Où l'utilisateur"),
        ('Comment garantir un *effacement complet* ?', 'Et comment'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Le modèle n'a *pas de mémoire* : l'application en construit une.", 'le modèle'),
        ('Ce qui est retenu reste *visible* et *effaçable*.', "Ce qu'elle retient"),
    ], "16 · Trouver le bon cas d'usage")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un LLM ne se souvient de rien. Entre deux appels, il repart de zéro. "
        "La mémoire d'un assistant, c'est l'application qui la fabrique.")),
    dict(kind='content', draw=s2, name="L'historique renvoyé", text=(
        "À chaque message, l'application renvoie toute la conversation au modèle. "
        "C'est ce qui donne l'impression qu'il suit le fil. "
        "Vous écrivez : « Mon vol est mardi. » Puis : « Décale-le d'un jour. » "
        "Le modèle comprend, parce que la première phrase lui est renvoyée avec la seconde.")),
    dict(kind='content', draw=s3, name='Résumés et préférences', text=(
        "Mais l'historique grossit, et la fenêtre de contexte a une limite. "
        "Alors on résume les anciens échanges en quelques lignes. "
        "On peut aussi stocker des préférences : « répondez en anglais », « je suis végétarien ». "
        "Elles sont réinjectées dans le prompt à chaque nouvelle conversation, sans que vous ayez à les répéter.")),
    dict(kind='content', draw=s4, name="Le RAG sur l'historique", text=(
        "Sur des mois d'échanges, on fait du RAG : on cherche dans l'historique les passages utiles "
        "à la question, et on ne réinjecte que ceux-là. "
        "Vous demandez : « Quel hôtel m'aviez-vous conseillé à Lyon ? » "
        "L'application retrouve l'échange concerné, et seulement lui.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, la mémoire touche aux données personnelles. "
        "Il faut le consentement de l'utilisateur, et lui montrer ce qui est retenu. "
        "Il doit pouvoir corriger, désactiver, ou tout effacer : c'est le droit à l'oubli. "
        "Et l'effacement doit aussi toucher les résumés et les index de recherche.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Que faut-il vraiment retenir, et pendant combien de temps ? "
        "Où l'utilisateur voit-il et corrige-t-il ce qui est retenu ? "
        "Et comment garantir un effacement complet ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le modèle n'a pas de mémoire, c'est l'application qui en construit une. "
        "Ce qu'elle retient doit rester visible, et effaçable. "
        "Prochaine capsule : trouver le bon cas d'usage, celui où l'IA générative apporte vraiment quelque chose.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
