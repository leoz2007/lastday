from engine import *  # noqa
from engine import _paint  # noqa

NUM = 65
TITLE = 'EXPLOITATION, ADOPTION'
FULL_TITLE = 'Exploitation et adoption'
SLUG = 'exploitation_adoption'
NEXT_CUE = 'Vous savez maintenant'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'


def server(c, t, at, cx, cy, s=100, color=DARK):
    """Picto de serveur (trois tiroirs)."""
    p = back(prog(t, at, 0.4))
    if p <= 0:
        return
    c.save()
    c.translate(cx, cy)
    c.scale(p * s / 100, p * s / 100)
    st = _paint(color, 7)
    for k in range(3):
        y = -48 + k * 34
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-44, y, 44, y + 26), 6, 6), st)
        c.drawCircle(-28, y + 13, 5, _paint(color))
        c.drawLine(4, y + 13, 30, y + 13, st)
    c.restore()


def s1(c, t, S):
    opening(c, t, S, CAP, "Déployer, ce n'est que *le début*.")
    d = S.cue("ce n'est pas la fin")
    card(c, t, d, 90, 830, 900, 220, WHITE, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Mise en service', 140, 890, 20, DARK)
        dot(c, t, d + 0.1, 170, 960, 24, RED)
        j = S.cue('chaque jour')
        arrow(c, t, j, 200, 960, 930, 960, DARK, 5, 18)
        for k in range(8):
            dot(c, t, j + 0.2 + k * 0.08, 270 + k * 80, 960, 12, DARK)
        if t >= j + 0.4:
            small(c, 'Chaque jour', 930, 1020, 18, DARK, align='right')
    items = [('gear', 'Faire tourner', 'le faire tourner', LIGHT, DARK),
             ('user', 'Changer le travail', 'changer la façon', RED, WHITE)]
    for k, (ic, s, kw, fill, fg) in enumerate(items):
        at = S.cue(kw)
        x = 90 + k * 465
        card(c, t, at, x, 1090, 435, 300, fill, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 217, 1200, 90, fg)
            plain(c, s, x + 217, 1330, 34, fg, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, 'LLMOps', "Nouveau modèle ? *Évals d'abord*")
    n = S.cue('Un nouveau modèle sort')
    box(c, t, n - 0.3, 90, 540, 410, 150, 'Modèle actuel', LIGHT, DARK, 34)
    box(c, t, n, 580, 540, 410, 150, 'Nouveau modèle', PLL, DARK, 34)
    arrow(c, t, n + 0.2, 505, 615, 572, 615, DARK, 6, 18)
    e = S.cue('Rejouez vos évals')
    card(c, t, e, 90, 730, 900, 420, LIGHT, 32, 'up')
    if prog(t, e, 0.5) > 0.4:
        small(c, 'Évals · exemple illustratif', 140, 790, 20, DARK)
        cmp_ = S.cue('comparez')
        tests = [('Tests', 0.70, 0.82), ('Refactor', 0.65, 0.60), ('Bugs', 0.55, 0.72)]
        for j, (nm, a, b) in enumerate(tests):
            y = 820 + j * 95
            plain(c, nm, 140, y + 50, 30, DARK)
            bar(c, t, e + 0.2 + j * 0.1, 330, y + 10, 600, 30, a, PL, WHITE, 0.6)
            bar(c, t, cmp_ + j * 0.1, 330, y + 48, 600, 30, b, RED, WHITE, 0.6)
        if t >= cmp_:
            small(c, 'Actuel', 330, 1125, 18, DARK)
            small(c, 'Nouveau', 460, 1125, 18, RED)
    b = S.cue('puis basculez')
    box(c, t, b, 90, 1190, 410, 200, 'Bascule', RED, WHITE, 36)
    r = S.cue('retour arrière')
    box(c, t, r, 580, 1190, 410, 200, 'Retour arrière prévu', LIGHT, DARK, 34)
    arrow(c, t, r + 0.2, 572, 1290, 508, 1290, DARK, 6, 18)


def s3(c, t, S):
    header(c, t, S, 'Disponibilité et capacité', 'Deux serveurs, *une capacité* prévue')
    f = S.cue('tombe')
    card(c, t, f - 0.4, 90, 540, 900, 330, LIGHT, 32, 'up')
    if prog(t, f - 0.4, 0.5) > 0.4:
        small(c, "Serveurs d'inférence", 140, 600, 20, DARK)
        server(c, t, f - 0.3, 260, 730, 120, DARK)
        icon(c, t, f, 'cross', 320, 790, 50, RED)
        h = S.cue('haute disponibilité')
        server(c, t, h, 520, 730, 120, DARK)
        arrow(c, t, h + 0.3, 600, 730, 760, 730, RED, 6, 18)
        icon(c, t, h + 0.5, 'user', 850, 730, 80, DARK)
        if t >= h + 0.5:
            small(c, 'Les équipes continuent', 940, 840, 18, DARK, align='right')
    p = S.cue('planifiez la capacité')
    card(c, t, p, 90, 910, 900, 510, LIGHT, 32, 'up')
    if prog(t, p, 0.5) > 0.4:
        small(c, 'Charge sur une journée · illustratif', 140, 970, 20, DARK)
        pk = S.cue('un pic le matin')
        hs = [0.25, 0.55, 0.95, 0.85, 0.5, 0.6, 0.7, 0.45, 0.2]
        for k, v in enumerate(hs):
            hh = 300 * v * ease(prog(t, p + 0.2 + k * 0.06, 0.5))
            col = RED if (k in (2, 3) and t >= pk) else PL
            if hh > 0:
                rrect(c, 160 + k * 88, 1340 - hh, 60, hh, 10, col)
        g = S.cue('GPU')
        if t >= g:
            rrect(c, 140, 1340 - 300 * 0.98 - 3, 800, 6, 3, DARK)
            chip(c, t, g, 'Capacité GPU', 940 - chip_width('Capacité GPU', 26), 990, WHITE, DARK, 26)


def s4(c, t, S):
    header(c, t, S, 'Conduite du changement', 'Former, *embarquer*, mesurer')
    rows = [('user', 'Formation des équipes', 'Formez'),
            ('target', 'Champions dans chaque équipe', 'Nommez des champions'),
            ('doc', "Playbooks par cas d'usage", 'des guides par cas')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 540 + k * 140
        hot = k == 1
        card(c, t, at, 90, y, 900, 120, RED if hot else LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if hot else DARK
            icon(c, t, at + 0.1, ic, 170, y + 60, 54, fg)
            reveal_plain(c, t, at + 0.2, s, 240, y + 72, 36, fg)
    x = 90
    for s, kw in [('Écrire des tests', 'écrire des tests'), ('Migrer', 'migrer'), ('Corriger un bug', 'corriger un bug')]:
        chip(c, t, S.cue(kw), s, x, 965, PLL, DARK, 30)
        x += chip_width(s, 30) + 18
    m = S.cue("mesurez l'adoption")
    card(c, t, m, 90, 1060, 900, 360, LIGHT, 32, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'Adoption par semaine · illustratif', 140, 1120, 20, DARK)
        for k in range(8):
            v = 0.2 + k * 0.1
            hh = 200 * v * ease(prog(t, m + 0.2 + k * 0.08, 0.5))
            if hh > 0:
                rrect(c, 160 + k * 70, 1380 - hh, 46, hh, 10, RED if k == 7 else PL)
        x0 = 740
        for j, (s, kw) in enumerate([('Qui', 'qui s'), ('Pour quoi', 'pour quoi'), ('Accepté', 'ce qui est accepté')]):
            at = S.cue(kw)
            reveal_plain(c, t, at, s, x0, 1210 + j * 60, 32, RED if j == 2 else DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "D'auteur à *architecte*")
    a = S.cue("auteur du code")
    card(c, t, a, 90, 540, 380, 200, LIGHT, 32, 'pop')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'code', 280, 610, 60, DARK)
        plain(c, 'Auteur', 280, 700, 34, DARK, 'Medium', 'center')
    r = S.cue('relecteur et d')
    arrow(c, t, r - 0.2, 480, 640, 560, 640, DARK, 6, 18)
    card(c, t, r, 570, 540, 420, 200, RED, 32, 'pop')
    if prog(t, r, 0.5) > 0.4:
        icon(c, t, r + 0.1, 'eye', 780, 610, 60, WHITE)
        plain(c, 'Relecteur, architecte', 780, 700, 32, WHITE, 'Medium', 'center')
    steps = [('Cadrer', 'cadre la demande'), ('Découper', 'découpe le travail'), ('Vérifier', 'vérifie le résultat')]
    for k, (s, kw) in enumerate(steps):
        at = S.cue(kw)
        x = 90 + k * 310
        box(c, t, at, x, 790, 280, 120, s, PLL, DARK, 34)
        if k < 2:
            arrow(c, t, at + 0.3, x + 284, 850, x + 306, 850, DARK, 5, 12)
    ch = S.cue('chef de chantier')
    card(c, t, ch, 90, 960, 900, 220, LIGHT, 32, 'up')
    if prog(t, ch, 0.5) > 0.4:
        small(c, 'Comme un chef de chantier', 140, 1020, 20, DARK)
        br = S.cue('chaque brique')
        for k in range(6):
            dot(c, t, br + k * 0.06, 170 + (k % 3) * 60, 1080 + (k // 3) * 50, 20, PL)
        m = S.cue('répond de la maison')
        icon(c, t, m, 'check', 400, 1105, 50, RED)
        reveal_plain(c, t, m + 0.1, 'Il répond du résultat', 450, 1120, 34, DARK)
    tk = S.cue('tickets')
    card(c, t, tk, 90, 1220, 900, 190, RED, 32, 'up')
    if prog(t, tk, 0.5) > 0.4:
        icon(c, t, tk + 0.1, 'doc', 170, 1315, 60, WHITE)
        reveal_plain(c, t, tk + 0.2, 'Des tickets plus précis', 240, 1329, 38, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Comment *testez-vous* un nouveau modèle ?', 'Comment testez-vous'),
        ('Qui sont les *champions* dans chaque équipe ?', 'champions'),
        ("Comment mesurez-vous l'*adoption* réelle ?", "l'adoption réelle"),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Exploitez l'agent comme un *service critique*.", "exploitez l'agent"),
        ('Accompagnez les équipes dans leur *nouveau rôle*.', 'accompagnez les équipes'),
    ], 'Vous savez *déployer* un agent de code', next_label='Saison terminée')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Déployer un agent de code, ce n'est pas la fin. C'est le début. "
        "Il faut le faire tourner chaque jour, et surtout changer la façon dont les équipes travaillent.")),
    dict(kind='content', draw=s2, name='LLMOps : changer de modèle avec des évals', text=(
        "D'abord, l'exploitation, qu'on appelle LLMOps : faire vivre les grands modèles de langage en production. "
        "Un nouveau modèle sort ? Ne basculez pas à l'aveugle. "
        "Rejouez vos évals, ces tests de référence, comparez, puis basculez, avec un retour arrière prévu.")),
    dict(kind='content', draw=s3, name='Haute disponibilité et capacité', text=(
        "Ensuite, la disponibilité. Si le serveur d'inférence tombe, toutes les équipes s'arrêtent : "
        "prévoyez la haute disponibilité, avec au moins deux serveurs. "
        "Et planifiez la capacité : combien de développeurs, à quelles heures, "
        "par exemple un pic le matin, et combien de GPU, ces processeurs graphiques qui font tourner le modèle.")),
    dict(kind='content', draw=s4, name='Conduite du changement', text=(
        "Puis la conduite du changement. Formez les équipes. "
        "Nommez des champions, des référents dans chaque équipe. "
        "Écrivez des guides par cas d'usage, des playbooks : écrire des tests, migrer une bibliothèque, corriger un bug. "
        "Et mesurez l'adoption : qui s'en sert, pour quoi, et ce qui est accepté.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, c'est une rupture culturelle. "
        "Le développeur passe du rôle d'auteur du code à celui de relecteur et d'architecte. "
        "Il cadre la demande, découpe le travail, vérifie le résultat. "
        "Comme un chef de chantier : il ne pose plus chaque brique, mais il répond de la maison. "
        "Vos tickets doivent être plus précis.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Comment testez-vous un nouveau modèle ? "
        "Qui sont les champions dans chaque équipe ? "
        "Et comment mesurez-vous l'adoption réelle ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : exploitez l'agent comme un service critique, "
        "et accompagnez les équipes dans leur nouveau rôle. "
        "C'était la dernière capsule de la saison spéciale. "
        "Merci de l'avoir suivie, et bravo pour ce parcours. "
        "Vous savez maintenant déployer un agent de code, du modèle jusqu'à son adoption. "
        "À vous de jouer !")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
