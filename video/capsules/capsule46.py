from engine import *  # noqa
from engine import _paint  # noqa

NUM = 46
TITLE = 'DU POC À LA PROD'
FULL_TITLE = 'Du POC à la production'
SLUG = 'poc_production'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def mini_doc(c, t, at, x, y, w, h, color):
    p = back(prog(t, at, 0.35))
    if p <= 0:
        return
    c.save()
    c.translate(x + w / 2, y + h / 2)
    c.scale(p, p)
    rrect(c, -w / 2, -h / 2, w, h, 10, color)
    c.restore()


def s1(c, t, S):
    opening(c, t, S, CAP, 'Le prototype *brille*, puis s\'arrête.')
    a = S.cue('brillent en démonstration')
    box(c, t, a, 90, 900, 240, 140, 'POC', RED, WHITE, 40)
    pr = S.cue('tient en production')
    box(c, t, pr, 710, 900, 280, 140, 'Production', WHITE, DARK, 34)
    st = S.cue("s'arrêtent là")
    if t >= st:
        p = ease(prog(t, st, 0.4))
        rrect(c, 515, 970 - 140 * p, 14, 280 * p, 7, PL)
    # des prototypes partent ; la plupart s'arrêtent au mur
    for i in range(9):
        go = a + 0.4 + i * 0.2
        u = ease(clamp((t - go) / 1.6))
        if u <= 0:
            continue
        y = 870 + (i % 3) * 70 + (i // 3) * 8
        x_end = 680 if i == 4 and t >= pr else 495
        x = lerp(350, x_end, u)
        c.drawCircle(x, y + 30, 14, _paint(WHITE if i == 4 else PL))
    pc = S.cue('montre que')
    if t >= pc:
        icon(c, t, pc, 'check', 210, 1120, 50, WHITE)
        small(c, 'Possible', 210, 1200, 22, WHITE, align='center')
    if t >= pr + 0.3:
        icon(c, t, pr + 0.3, 'cross', 850, 1120, 50, RED)
        small(c, 'Ça tient ?', 850, 1200, 22, WHITE, align='center')
    lb = S.cue('la preuve de concept')
    if t >= lb:
        reveal_plain(c, t, lb, 'POC : preuve de concept', 90, 1330, 34, WHITE)


def s2(c, t, S):
    header(c, t, S, 'Pourquoi ça bloque', 'Une démo trop *facile*')
    x = 90
    for s, kw in [('Cas faciles', 'cas faciles'), ('Pas de mesure', 'Personne ne mesure'),
                  ('Données propres', 'données sont propres')]:
        chip(c, t, S.cue(kw), s, x, 540, PLL, DARK, 30)
        x += chip_width(s, 30) + 20
    d = S.cue('la démo tourne')
    card(c, t, d, 90, 680, 440, 520, LIGHT, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        plain(c, 'Démo', 310, 750, 36, DARK, 'Medium', 'center')
        for k in range(3):
            mini_doc(c, t, d + 0.2 + k * 0.1, 140 + k * 120, 800, 100, 130, WHITE)
            for j in range(3):
                if t >= d + 0.4:
                    rrect(c, 160 + k * 120, 830 + j * 30, 60, 10, 5, PL)
        icon(c, t, d + 0.6, 'check', 310, 1040, 60, DARK)
        ch = S.cue('choisis à la main')
        if t >= ch:
            small(c, 'Choisis à la main', 310, 1150, 18, DARK, align='center')
    r = S.cue('les vraies')
    card(c, t, r, 550, 680, 440, 520, LIGHT, 32, 'up')
    if prog(t, r, 0.5) > 0.4:
        plain(c, 'Réel', 770, 750, 36, RED, 'Medium', 'center')
        for k in range(3):
            mini_doc(c, t, r + 0.2 + k * 0.1, 600 + k * 120, 800, 100, 130, WHITE)
            for j in range(3):
                if t >= r + 0.4 and not (k == 1 and j == 1):
                    rrect(c, 620 + k * 120, 830 + j * 30, [60, 30, 50][j], 10, 5, RED if (k, j) == (2, 0) else PL)
        icon(c, t, S.cue('contradictoires'), 'cross', 770, 1040, 60, RED)
        if t >= r + 0.5:
            small(c, 'Incomplet, mal scanné', 770, 1150, 18, DARK, align='center')
    m = S.cue('Personne ne mesure')
    card(c, t, m, 90, 1240, 900, 160, LIGHT, 32, 'left')
    if prog(t, m, 0.5) > 0.4:
        icon(c, t, m + 0.1, 'eye', 170, 1320, 56, DARK)
        reveal_plain(c, t, m + 0.2, 'Qualité : jamais mesurée', 240, 1333, 36, DARK)


def s3(c, t, S):
    header(c, t, S, 'Pourquoi ça bloque', 'Les sujets lourds, *trop tard*')
    a = S.cue('arrivent trop tard')
    if t >= a:
        p = ease(prog(t, a, 0.8))
        rrect(c, 130, 616, 820 * p, 8, 4, PL)
    steps = [('POC', 170), ('Démo', 390), ('Budget', 620), ('Revue', 850)]
    for k, (s, x) in enumerate(steps):
        at = a + 0.2 + k * 0.2
        dot(c, t, at, x, 620, 22, RED if k >= 2 else DARK)
        if t >= at:
            small(c, s, x, 690, 22, DARK, align='center')
    co = S.cue('Le coût à grande échelle')
    arrow(c, t, co, 620, 710, 620, 760, RED, 5, 14)
    card(c, t, co, 480, 770, 260, 260, LIGHT, 30, 'up')
    if prog(t, co, 0.5) > 0.4:
        icon(c, t, co + 0.1, 'coin', 610, 860, 70, DARK)
        plain(c, 'Coût', 610, 980, 32, DARK, 'Medium', 'center')
    se = S.cue('La sécurité')
    arrow(c, t, se, 850, 710, 850, 760, RED, 5, 14)
    card(c, t, se, 760, 770, 230, 260, LIGHT, 30, 'up')
    if prog(t, se, 0.5) > 0.4:
        icon(c, t, se + 0.1, 'lock', 875, 860, 70, DARK)
        plain(c, 'Sécurité', 875, 980, 32, DARK, 'Medium', 'center')
    if t >= co:
        small(c, 'Découverts tard', 90, 900, 20, RED)
    pp = S.cue("personne n'est propriétaire")
    card(c, t, pp, 90, 1090, 900, 220, RED, 32, 'up')
    if prog(t, pp, 0.5) > 0.4:
        icon(c, t, pp + 0.1, 'user', 190, 1200, 80, WHITE)
        reveal_plain(c, t, pp + 0.2, 'Propriétaire : personne', 280, 1215, 42, WHITE)


def s4(c, t, S):
    header(c, t, S, 'Entre les deux', 'Le travail *peu visible*')
    items = [('target', 'Evals, cas réels', 'Des evals'), ('db', 'Intégration, droits', "L'intégration"),
             ('eye', 'Supervision, traces', 'La supervision'), ('gear', 'Gestion des erreurs', 'gestion des erreurs'),
             ('shield', 'Conformité', 'la conformité'), ('user', 'Formation', 'la formation'),
             ('coin', 'Budget de fonctionnement', 'budget de fonctionnement')]
    for k, (ic, s, kw) in enumerate(items):
        at = S.cue(kw)
        full = k == 6
        x = 90 if full else 90 + (k % 2) * 460
        y = 540 + (k // 2) * 190
        w = 900 if full else 440
        hot = full
        card(c, t, at, x, y, w, 170, RED if hot else LIGHT, 30, 'pop')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if hot else DARK
            icon(c, t, at + 0.1, ic, x + 60, y + 85, 52, fg)
            plain(c, s, x + 110, y + 96, 30, fg, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Des *critères de passage*')
    rows = [('Bonnes réponses / 100 cas', 'bonnes réponses', 0.86, 0.8),
            ('Coût par demande', 'coût maximal', 0.55, 0.7),
            ('Délai de réponse', 'délai de réponse', 0.6, 0.75)]
    for k, (s, kw, f, thr) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 150
        if t >= at - 0.1:
            reveal_plain(c, t, at, s, 90, y + 30, 32, DARK)
        bar(c, t, at + 0.1, 90, y + 60, 820, 34, f, PL, LIGHT, 0.8)
        if t >= at + 0.3:
            rrect(c, 90 + 820 * thr - 4, y + 48, 8, 58, 4, DARK)
        icon(c, t, at + 0.9, 'check', 955, y + 77, 40, RED)
    if t >= S.cue('délai de réponse') + 0.6:
        small(c, 'Trait : critère fixé au POC · valeurs illustratives', 90, 1040, 18, DARK)
    ok = S.cue('on passe')
    box(c, t, ok, 90, 1100, 420, 220, 'On passe', RED, WHITE, 40, 'Medium', 32, 'up')
    no = S.cue('Sinon')
    box(c, t, no, 540, 1100, 450, 220, 'On corrige, ou on arrête', LIGHT, DARK, 36, 'Medium', 32, 'up')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quels *critères mesurables* font passer en production ?', 'Quels critères'),
        ('Qui sera *propriétaire* du service une fois lancé ?', 'Qui sera'),
        ('Quel *budget* pour le faire tourner ?', 'Et quel budget'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un POC prouve que c\'est *possible*, pas que ça *tient*.', 'un POC prouve'),
        ('Dès le départ : *critères*, propriétaire, budget.', 'Fixez dès le départ'),
    ], '47 · LLMOps et versioning')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Beaucoup de prototypes d'IA brillent en démonstration, puis s'arrêtent là. "
        "Le POC, la preuve de concept, montre que c'est possible. Pas que ça tient en production. Et ce passage se prépare dès le premier jour.")),
    dict(kind='content', draw=s2, name='Une démo trop facile', text=(
        "Pourquoi ? D'abord, la démo tourne sur des cas faciles, choisis à la main. "
        "Personne ne mesure la qualité. Et les données sont propres, alors que les vraies sont incomplètes, "
        "mal scannées ou contradictoires. Résultat : ce qui impressionnait en réunion peut décevoir dès les premiers vrais utilisateurs.")),
    dict(kind='content', draw=s3, name='Les sujets lourds découverts trop tard', text=(
        "Ensuite, les sujets lourds arrivent trop tard. "
        "Le coût à grande échelle, découvert au moment du budget. "
        "La sécurité et les droits d'accès, découverts à la revue. "
        "Et souvent, une fois la démo finie, personne n'est propriétaire du projet.")),
    dict(kind='content', draw=s4, name='Ce qui manque entre les deux', text=(
        "Entre les deux, il manque un travail peu visible. Des evals, ces tests notés, sur des cas réels. "
        "L'intégration au système d'information et aux droits d'accès. La supervision et les traces. "
        "La gestion des erreurs. Puis la conformité, la formation des équipes, et un budget de fonctionnement.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, définissez dès le POC les critères de passage. "
        "Par exemple : quel taux de bonnes réponses sur cent cas réels, quel coût maximal par demande, "
        "quel délai de réponse. Critères atteints : on passe. Sinon, on corrige, ou on arrête sans regret.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels critères mesurables font passer en production ? "
        "Qui sera propriétaire du service, une fois lancé ? "
        "Et quel budget prévoit-on pour le faire tourner ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un POC prouve que c'est possible, pas que ça tient. "
        "Fixez dès le départ les critères de passage, un propriétaire et un budget de fonctionnement. "
        "Prochaine capsule : le LLMOps, l'exploitation des modèles au quotidien, et le versioning.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
