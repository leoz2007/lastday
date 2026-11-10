from engine import *  # noqa
from engine import _paint  # noqa

NUM = 21
TITLE = 'MULTI-AGENTS'
FULL_TITLE = 'Multi-agents'
SLUG = 'multi_agents'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def line(c, t, at, x1, y1, x2, y2, color, width=5):
    """Trait sans pointe, tracé progressivement."""
    p = ease(prog(t, at, 0.4))
    if p > 0:
        c.drawLine(x1, y1, lerp(x1, x2, p), lerp(y1, y2, p), _paint(color, width))


def s1(c, t, S):
    opening(c, t, S, CAP, "Plus d'agents, ce n'est pas *plus intelligent*.")
    a = S.cue('plusieurs agents')
    pts = [(540, 900), (330, 1010), (750, 1010), (420, 1180), (660, 1180)]
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            line(c, t, a + 0.3 + 0.05 * (i + j), *pts[i], *pts[j], PL, 4)
    for k, (x, y) in enumerate(pts):
        dot(c, t, a + k * 0.1, x, y, 40 if k == 0 else 32, WHITE)
        icon(c, t, a + k * 0.1 + 0.1, 'bolt', x, y, 36 if k == 0 else 30, DARK)
    for k, (ic, s, kw) in enumerate([('coin', 'Plus cher', 'plus cher'), ('clock', 'Plus lent', 'plus lent'),
                                     ('cross', 'Plus fragile', 'plus fragile')]):
        at = S.cue(kw)
        x = 90 + k * 310
        chip(c, t, at, s, x, 1320, RED if k == 2 else WHITE, WHITE if k == 2 else DARK, 32)


def s2(c, t, S):
    header(c, t, S, 'Les rôles', 'Planifier, exécuter, *relire*')
    p = S.cue('Un agent planifie')
    box(c, t, p, 290, 540, 500, 120, 'Planificateur', DARK, WHITE, 36)
    ao = S.cue("appel d'offres")
    e = S.cue("D'autres agents exécutent")
    subs = ['Technique', 'Prix', 'Références']
    for k in range(3):
        x = 90 + k * 310
        arrow(c, t, e + k * 0.15, 540, 665, x + 140, 755, DARK, 5, 16)
        card(c, t, e + 0.2 + k * 0.15, x, 760, 280, 170, LIGHT, 30, 'up')
        if prog(t, e + 0.2 + k * 0.15, 0.5) > 0.4:
            icon(c, t, e + 0.3 + k * 0.15, 'doc', x + 140, 815, 46, DARK)
            plain(c, 'Exécutant', x + 140, 885, 30, DARK, 'Medium', 'center')
            if t >= ao + 0.2 + k * 0.2:
                small(c, subs[k], x + 140, 918, 18, RED, align='center')
    r = S.cue('Un dernier relit')
    for k in range(3):
        x = 90 + k * 310
        arrow(c, t, r + k * 0.1, x + 140, 935, 540, 1025, DARK, 5, 16)
    box(c, t, r + 0.3, 290, 1030, 500, 120, 'Relecteur', RED, WHITE, 36)
    rv = S.cue('renvoie')
    arrow(c, t, rv, 800, 1090, 900, 940, RED, 5, 16)
    if t >= rv + 0.2:
        small(c, 'À reprendre', 830, 1130, 20, RED)
    card(c, t, ao, 90, 1220, 900, 200, LIGHT, 32, 'up')
    if prog(t, ao, 0.5) > 0.4:
        label(c, t, ao + 0.1, "Exemple : appel d'offres", 140, 1250, PLL, DARK, 22)
        x = 140
        for k, s in enumerate(['1 plan', '3 rédacteurs', '1 relecteur']):
            w = chip(c, t, ao + 0.4 + k * 0.25, s, x, 1325, RED if k == 2 else WHITE,
                     WHITE if k == 2 else DARK, 30)
            x += w + 20


def s3(c, t, S):
    header(c, t, S, 'Quand c\'est utile', 'Trois cas *favorables*')
    rows = [('clock', 'Tâche longue', 'Une tâche longue'), ('bolt', 'Parallélisable', 'parallélisable'),
            ('brain', 'Expertises distinctes', 'des expertises distinctes')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 290
        card(c, t, at, 90, y, 900, 260, LIGHT, 32, 'left')
        if prog(t, at, 0.5) < 0.4:
            continue
        icon(c, t, at + 0.1, ic, 180, y + 80, 64, RED)
        reveal_plain(c, t, at + 0.15, s, 250, y + 100, 38, DARK)
        if k == 0:
            cx = S.cue('le contexte')
            small(c, "Contexte d'un agent", 140, y + 170, 18, DARK)
            bar(c, t, at + 0.3, 140, y + 190, 480, 30, 1.0, PL, WHITE, 0.8)
            if t >= cx:
                bar(c, t, cx, 140, y + 190, 800, 30, 1.0, RED, PL, 1.0)
                rrect(c, 615, y + 180, 6, 50, 3, DARK)
        elif k == 1:
            mt = S.cue('en même temps')
            for j in range(3):
                bar(c, t, mt, 140 + j * 270, y + 175, 250, 30, 1.0, RED if j == 0 else PL, WHITE, 1.0)
            if t >= mt:
                small(c, '3 recherches en parallèle', 140, y + 240, 18, DARK)
        else:
            oi = S.cue('ses propres instructions')
            xx = 140
            for j, s2_ in enumerate(['Juridique', 'Finance', 'Technique']):
                w = chip(c, t, oi + j * 0.2, s2_, xx, y + 160, WHITE, DARK, 30)
                xx += w + 18


def s4(c, t, S):
    header(c, t, S, "Quand c'est inutile", 'Chaque agent a un *coût*')
    a = S.cue('ajoute des appels')
    card(c, t, a, 90, 540, 900, 420, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, '1 agent', 400, 600, 18, DARK)
        small(c, '4 agents', 700, 600, 18, RED)
        rows = [('Coût', 'du coût', 0.22, 0.85), ('Latence', 'la latence', 0.25, 0.7),
                ('Complexité', 'de la complexité', 0.15, 0.9)]
        for k, (nm, kw, f1, f2) in enumerate(rows):
            at = S.cue(kw)
            y = 650 + k * 95
            plain(c, nm, 140, y + 30, 30, DARK)
            if t >= at - 0.25:
                bar(c, t, at, 400, y + 5, 540, 18, f1, PL, WHITE, 0.6)
                bar(c, t, at + 0.2, 400, y + 32, 540, 18, f2, RED, WHITE, 0.8)
        small(c, 'Ordres de grandeur illustratifs', 140, 935, 18, DARK)
    er = S.cue('une erreur du planificateur')
    box(c, t, er, 90, 1140, 280, 140, 'Plan erroné', RED, WHITE, 34)
    pg = S.cue('se propage')
    cp = S.cue('copiée')
    for k in range(3):
        y = 1010 + k * 140
        arrow(c, t, pg + k * 0.15, 380, 1210, 550, y + 50, DARK, 5, 16)
        bad = t >= cp + k * 0.2
        card(c, t, pg + 0.2 + k * 0.15, 560, y, 430, 105, PLL, 28, 'left')
        if prog(t, pg + 0.2 + k * 0.15, 0.5) > 0.4:
            plain(c, f'Exécutant {k + 1}', 600, y + 64, 30, DARK)
            if bad:
                dot(c, t, cp + k * 0.2, 930, y + 52, 26, RED)
                icon(c, t, cp + k * 0.2 + 0.1, 'cross', 930, y + 52, 26, WHITE)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Commencez *simple*')
    steps = [('Workflow', 'ou un workflow', 160), ('Un agent', 'Un seul agent', 260),
             ('Multi-agents', 'un deuxième agent', 360)]
    for k, (s, kw, h) in enumerate(steps):
        at = S.cue(kw)
        x = 90 + k * 310
        y = 1000 - h
        box(c, t, at, x, y, 280, h, s, RED if k == 0 else (LIGHT if k == 1 else PLL), WHITE if k == 0 else DARK, 32)
    cs = S.cue('commencez simple')
    if t >= cs:
        small(c, 'Du plus simple au plus complexe', 90, 600, 20, DARK)
    arrow(c, t, cs + 0.2, 90, 1040, 980, 1040, PL, 5, 16)
    ev = S.cue('vos evals')
    card(c, t, ev, 90, 1100, 900, 330, LIGHT, 32, 'up')
    if prog(t, ev, 0.5) > 0.4:
        label(c, t, ev + 0.1, 'Avant le deuxième agent', 140, 1130, PLL, DARK, 22)
        for k, (nm, fr, kw) in enumerate([('Gain mesuré', 0.7, 'vrai gain'), ('Coût en plus', 0.45, 'le coût en plus')]):
            at = S.cue(kw)
            y = 1225 + k * 95
            plain(c, nm, 140, y + 28, 30, DARK)
            bar(c, t, at, 430, y, 510, 34, fr, RED if k == 0 else PL, WHITE, 0.8)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Un *seul agent* suffirait-il ?', 'Un seul agent'),
        ('Qui *vérifie* le travail des autres ?', 'Qui vérifie'),
        ('Combien *coûte* une demande, tous appels compris ?', 'Et combien'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Plusieurs agents : pour le *long*, le *parallèle*, le *spécialisé*.', 'plusieurs agents'),
        ('Sinon, *commencez simple*.', 'Sinon'),
    ], '22 · Observabilité et traces')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Mettre plusieurs agents sur une tâche ne la rend pas forcément plus intelligente. "
        "Parfois, c'est juste plus cher, plus lent, et plus fragile. "
        "Avant d'en ajouter, demandez-vous ce que chacun apporte vraiment.")),
    dict(kind='content', draw=s2, name='Les rôles des agents', text=(
        "Dans un système multi-agents, chaque agent a un rôle. Un agent planifie : il découpe la demande en sous-tâches. "
        "D'autres agents exécutent, chacun la sienne. "
        "Un dernier relit le résultat, et renvoie ce qui ne va pas. "
        "Par exemple, pour répondre à un appel d'offres : un plan, trois rédacteurs, un relecteur.")),
    dict(kind='content', draw=s3, name='Quand c\'est utile', text=(
        "C'est utile dans trois cas. Une tâche longue, qui déborderait le contexte d'un seul agent. "
        "Une tâche parallélisable : plusieurs recherches menées en même temps. "
        "Ou des expertises distinctes, chaque agent avec ses propres instructions et ses outils. "
        "Chaque agent garde alors un contexte court, centré sur sa sous-tâche.")),
    dict(kind='content', draw=s4, name='Quand c\'est inutile', text=(
        "Mais chaque agent ajoute des appels au modèle, donc du coût et de la latence. "
        "Les échanges entre agents ajoutent de la complexité. "
        "Et une erreur du planificateur se propage à tous les autres : elle est copiée, pas corrigée. "
        "Et quand le résultat est faux, il faut retrouver quel agent s'est trompé.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, commencez simple. Un seul agent bien outillé, ou un workflow, règle déjà beaucoup de cas. "
        "Ajoutez un deuxième agent seulement quand vos evals montrent un vrai gain, "
        "qui justifie le coût en plus. Mesurez avant d'empiler.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Un seul agent suffirait-il ? "
        "Qui vérifie le travail des autres agents ? "
        "Et combien coûte une demande, une fois tous les appels additionnés ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : plusieurs agents, c'est utile pour des tâches longues, parallèles, ou très spécialisées. "
        "Sinon, commencez simple. "
        "Prochaine capsule : observabilité et traces, pour comprendre ce que fait vraiment votre système.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
