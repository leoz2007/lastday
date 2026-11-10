from engine import *  # noqa
from engine import _paint  # noqa

NUM = 38
TITLE = 'AGENTS EN PRODUCTION'
FULL_TITLE = 'Agents en production'
SLUG = 'agents_production'
NEXT_CUE = 'Vous maîtrisez maintenant'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def flag(c, t, at, x, y, color):
    """Petit drapeau : un point de sauvegarde."""
    p = back(prog(t, at, 0.35))
    if p <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(p, p)
    c.drawLine(0, 0, 0, -44, _paint(color, 4))
    path = skia.Path()
    path.moveTo(0, -44); path.lineTo(24, -36); path.lineTo(0, -28); path.close()
    c.drawPath(path, _paint(color))
    c.restore()


def s1(c, t, S):
    opening(c, t, S, CAP, "Une démo n'est pas *un agent fiable*.")
    d = S.cue("Une démo d'agent")
    card(c, t, d, 90, 830, 900, 170, WHITE, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Démo', 140, 880, 22, DARK)
        for k in range(3):
            dot(c, t, d + 0.2 + k * 0.12, 160 + k * 110, 945, 20, DARK)
            if k < 2:
                arrow(c, t, d + 0.25 + k * 0.12, 185, 945, 245, 945, DARK, 4, 12) if k == 0 else \
                    arrow(c, t, d + 0.37, 295, 945, 355, 945, DARK, 4, 12)
        icon(c, t, d + 0.6, 'check', 470, 945, 50, RED)
        if t >= d + 0.7:
            reveal_plain(c, t, d + 0.7, 'Ça marche une fois', 940, 960, 30, DARK, 'Medium', 'right')
    p = S.cue('agent fiable en production')
    card(c, t, p, 90, 1040, 900, 210, LIGHT, 32, 'up')
    if prog(t, p, 0.5) > 0.4:
        small(c, 'Production', 140, 1090, 22, DARK)
        er = S.cue('aux erreurs')
        for k in range(12):
            x = 160 + k * 66
            bad = k == 6 and t >= er
            dot(c, t, p + 0.2 + k * 0.06, x, 1180, 16, RED if bad else DARK)
        if t >= er:
            icon(c, t, er, 'bolt', 556, 1130, 34, RED)
    for k, (s, kw) in enumerate([('Tâches longues', 'tâches longues'), ('Erreurs', 'aux erreurs'),
                                 ('Sous contrôle', 'sous contrôle')]):
        at = S.cue(kw)
        chip(c, t, at, s, 90 + k * 300, 1310, RED if k == 2 else WHITE, WHITE if k == 2 else DARK, 30)


def s2(c, t, S):
    header(c, t, S, 'Tâches longues', 'Reprendre *où on en était*')
    d = S.cue('découpez les tâches longues')
    sv = S.cue('points de sauvegarde')
    st = S.cue("s'arrête à l'étape sept")
    rp = S.cue('reprend')
    card(c, t, d, 90, 540, 900, 380, LIGHT, 36, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Dix étapes', 140, 600, 20, DARK)
        for k in range(10):
            x = 170 + k * 82
            col = DARK if k < 6 else (RED if k == 6 and t >= st else PL)
            dot(c, t, d + 0.2 + k * 0.08, x, 740, 24, col)
            if k < 6:
                flag(c, t, sv + k * 0.1, x, 700, RED)
            if k == 6 and t >= st:
                icon(c, t, st, 'cross', x, 740, 26, WHITE)
        if t >= rp:
            x7 = 170 + 6 * 82
            arrow(c, t, rp, x7, 800, x7, 770, RED, 5, 14)
            reveal_plain(c, t, rp + 0.2, "Reprise à l'étape 7, pas au début", 540, 860, 30, RED, 'Medium', 'center')
    m = S.cue('mémoire de travail')
    card(c, t, m, 90, 960, 900, 450, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        label(c, t, m + 0.1, 'Mémoire de travail', 140, 995, PLL, DARK, 22)
        rows = [('doc', 'Notes', 'des notes'), ('check', 'Fait : étapes 1 à 6', 'ce qui est fait'),
                ('clock', 'Reste : étapes 7 à 10', 'ce qui reste')]
        for j, (ic, s, kw) in enumerate(rows):
            at = S.cue(kw)
            y = 1100 + j * 100
            rrect(c, 140, y, 800, 80, 20, WHITE) if t >= at else None
            icon(c, t, at, ic, 190, y + 40, 40, RED if j == 1 else DARK)
            reveal_plain(c, t, at, s, 240, y + 52, 32, DARK, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Erreurs et garde-fous', 'Réessayer, *mais pas trop*')
    o = S.cue('Un outil ne répond pas')
    card(c, t, o, 90, 540, 900, 330, LIGHT, 36, 'up')
    if prog(t, o, 0.5) > 0.4:
        icon(c, t, o + 0.1, 'gear', 180, 660, 70, DARK)
        plain(c, 'Outil', 180, 750, 28, DARK, 'Medium', 'center')
        r = S.cue("L'agent réessaie")
        for k in range(3):
            x = 340 + k * 130
            dot(c, t, r + k * 0.3, x, 660, 34, PL)
            icon(c, t, r + k * 0.3 + 0.1, 'cross', x, 660, 30, DARK)
        if t >= r:
            small(c, 'Trois essais au plus · exemple', 300, 750, 18, DARK)
        ar = S.cue("s'arrête proprement")
        chip(c, t, ar, 'Arrêt propre', 740, 630, RED, WHITE, 30)
    g = S.cue('garde-fous')
    if t >= g:
        small(c, 'Garde-fous', 90, 930, 22, DARK)
    rows = [('shield', 'Outils autorisés', "outils autorisés"), ('lock', 'Droits minimaux', 'droits minimaux'),
            ('user', 'Validation humaine', 'validation humaine')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 960 + k * 155
        red = k == 2
        card(c, t, at, 90, y, 900, 130, RED if red else LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if red else DARK
            icon(c, t, at + 0.1, ic, 170, y + 65, 56, fg)
            reveal_plain(c, t, at + 0.15, s, 240, y + 78, 36, fg, 'Medium')
            if red:
                pm = S.cue('un paiement')
                if t >= pm:
                    chip(c, t, pm, 'Paiement', 960 - chip_width('Paiement', 28), y + 40, WHITE, RED, 28)


def s4(c, t, S):
    header(c, t, S, 'Budget et traces', 'Des *limites*, et *tout* noter')
    b = S.cue('budget par tâche')
    card(c, t, b, 90, 540, 900, 420, LIGHT, 36, 'up')
    au = S.cue('Au-delà')
    if prog(t, b, 0.5) > 0.4:
        small(c, 'Budget par tâche · illustratif', 140, 600, 20, DARK)
        rows = [("Étapes", "nombre maximal d'étapes", 1.0), ('Coût', 'un coût', 0.55), ('Durée', 'une durée', 0.4)]
        lim = 140 + 140 + 600
        for j, (s, kw, f) in enumerate(rows):
            at = S.cue(kw)
            y = 650 + j * 80
            plain(c, s, 140, y + 30, 28, DARK)
            full = j == 0 and t >= au
            bar(c, t, at, 280, y, 600, 40, f, RED if full else PL, WHITE, 1.0)
        if t >= b + 0.3:
            rrect(c, lim - 3, 630, 6, 240, 3, DARK)
            small(c, 'Plafond', lim, 905, 18, DARK, align='center')
        if t >= au:
            chip(c, t, au, "Stop et alerte", 140, 885, RED, WHITE, 26)
    tr = S.cue('une trace de chaque étape')
    card(c, t, tr, 90, 1000, 900, 430, LIGHT, 36, 'up')
    if prog(t, tr, 0.5) > 0.4:
        label(c, t, tr + 0.1, 'Traces', 140, 1035, PLL, DARK, 22)
        rows = [('eye', 'Vu : la demande du client', 'a vu'), ('brain', 'Décidé : chercher la commande', 'décidé'),
                ('gear', 'Fait : appel à l\'outil commandes', 'puis fait')]
        for j, (ic, s, kw) in enumerate(rows):
            at = S.cue(kw)
            y = 1130 + j * 90
            small(c, f'Étape {j + 1}', 140, y + 10, 18, DARK) if t >= at else None
            icon(c, t, at, ic, 280, y, 40, RED if j == 1 else DARK)
            reveal_plain(c, t, at + 0.1, s, 330, y + 12, 30, DARK, 'Medium')
        ec = S.cue('comprendre un échec')
        if t >= ec:
            reveal_plain(c, t, ec, 'Sans traces : échec inexplicable', 540, 1405, 26, RED, 'Medium', 'center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Évaluer des *scénarios complets*')
    sc = S.cue('scénarios complets')
    card(c, t, sc, 90, 540, 900, 450, LIGHT, 36, 'up')
    if prog(t, sc, 0.5) > 0.4:
        small(c, 'Un scénario de bout en bout', 140, 600, 20, DARK)
        dz = S.cue('traiter un dossier')
        pn = S.cue('en panne')
        steps = ['Dossier', '1', '2', '3', 'Fin']
        for k, s in enumerate(steps):
            x = 170 + k * 185
            at = dz + k * 0.25
            if k in (0, 4):
                box(c, t, at, x - 75, 700, 150, 90, s, DARK if k == 0 else RED, WHITE, 26)
            else:
                bad = k == 2 and t >= pn
                dot(c, t, at, x, 745, 38, RED if bad else PL)
                if bad:
                    icon(c, t, pn, 'bolt', x, 745, 40, WHITE)
            if k < 4:
                arrow(c, t, at + 0.15, x + (80 if k == 0 else 45), 745, x + 185 - (80 if k == 3 else 45), 745,
                      DARK, 4, 12)
        if t >= pn:
            reveal_plain(c, t, pn + 0.1, 'Un outil en panne au milieu', 540, 860, 30, RED, 'Medium', 'center')
        iso = S.cue('réponses isolées')
        if t >= iso:
            small(c, 'Pas seulement des réponses isolées', 540, 950, 18, DARK, align='center')
    rj = S.cue('Rejouez')
    card(c, t, rj, 90, 1030, 900, 380, LIGHT, 36, 'up')
    if prog(t, rj, 0.5) > 0.4:
        chip(c, t, S.cue('changement de modèle'), 'Nouveau modèle', 140, 1090, WHITE, DARK, 28)
        chip(c, t, S.cue('ou de prompt'), 'Nouveau prompt', 140, 1180, WHITE, DARK, 28)
        arrow(c, t, rj + 0.4, 470, 1160, 560, 1160, DARK, 6, 18)
        card(c, t, rj + 0.5, 580, 1080, 360, 160, RED, 30, 'pop')
        if prog(t, rj + 0.5, 0.5) > 0.4:
            icon(c, t, rj + 0.6, 'check', 640, 1160, 50, WHITE)
            plain(c, 'Evals rejouées', 690, 1172, 30, WHITE, 'Medium')
        ev = S.cue('les evals')
        if t >= ev:
            reveal_plain(c, t, ev, 'Evals : des tests automatiques', 540, 1340, 30, DARK, 'Medium', 'center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles actions exigent une *validation humaine* ?', 'Quelles actions'),
        ('Quel *budget* maximal par tâche ?', 'Quel budget'),
        ('Sur quels *scénarios complets* juger l\'agent ?', 'Et sur quels'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un agent fiable se construit *comme un service*.', 'un agent fiable'),
        ('Reprise, *garde-fous*, budget, traces et *evals*.', 'Des étapes reprenables'),
    ], 'Vous maîtrisez les *coulisses*', next_label='Saison terminée')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Une démo d'agent se monte vite. Un agent fiable en production, c'est une autre affaire : "
        "il doit tenir sur des tâches longues, résister aux erreurs, et rester sous contrôle.")),
    dict(kind='content', draw=s2, name='Tâches reprenables et mémoire de travail', text=(
        "D'abord, découpez les tâches longues en étapes, avec des points de sauvegarde. "
        "Si tout s'arrête à l'étape sept, l'agent reprend à l'étape sept, pas au début. "
        "Ensuite, donnez-lui une mémoire de travail : des notes, et l'état de la tâche, "
        "ce qui est fait et ce qui reste.")),
    dict(kind='content', draw=s3, name='Reprise sur erreur et garde-fous', text=(
        "Les erreurs arrivent. Un outil ne répond pas ? L'agent réessaie, mais un nombre de fois limité, "
        "puis il s'arrête proprement. Ajoutez des garde-fous : une liste d'outils autorisés, des droits minimaux, "
        "et une validation humaine avant toute action sensible, comme un paiement.")),
    dict(kind='content', draw=s4, name='Budget par tâche et traces', text=(
        "Fixez aussi un budget par tâche : un nombre maximal d'étapes, un coût, une durée. "
        "Au-delà, l'agent s'arrête et prévient. Et gardez une trace de chaque étape : "
        "ce que l'agent a vu, décidé, puis fait. Sans traces, impossible de comprendre un échec.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, évaluez l'agent sur des scénarios complets, pas sur des réponses isolées. "
        "Par exemple : traiter un dossier de bout en bout, avec un outil en panne au milieu. "
        "Rejouez ces tests, les evals, à chaque changement de modèle ou de prompt.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles actions exigent une validation humaine ? "
        "Quel budget maximal accordez-vous à chaque tâche ? "
        "Et sur quels scénarios complets jugerez-vous l'agent ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un agent fiable se construit comme un service. "
        "Des étapes reprenables, des garde-fous, un budget, des traces et des evals. "
        "C'était la dernière capsule de la saison trois, et de tout le parcours. "
        "Merci de l'avoir suivi jusqu'au bout, et bravo pour ce chemin. "
        "Vous maîtrisez maintenant les coulisses de l'IA générative. À vous de jouer !")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
