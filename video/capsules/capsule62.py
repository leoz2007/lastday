from engine import *  # noqa
from engine import _paint  # noqa

NUM = 62
TITLE = 'OBSERVABILITÉ AGENTS'
FULL_TITLE = 'Observabilité des agents'
SLUG = 'observabilite_agents'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def loop_arrow(c, t, at, cx, cy, r, color=RED, width=8):
    """Flèche circulaire : un agent qui tourne en rond."""
    p = ease(prog(t, at, 0.6))
    if p <= 0:
        return
    rect = skia.Rect(cx - r, cy - r, cx + r, cy + r)
    path = skia.Path()
    sweep = 300 * p
    path.addArc(rect, -90, sweep)
    c.drawPath(path, _paint(color, width))
    if p > 0.95:
        import math
        a = math.radians(-90 + sweep)
        ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        tri = skia.Path()
        dx, dy = -math.sin(a), math.cos(a)  # tangente
        nx, ny = math.cos(a), math.sin(a)
        tri.moveTo(ex + dx * 18, ey + dy * 18)
        tri.lineTo(ex + nx * 14, ey + ny * 14)
        tri.lineTo(ex - nx * 14, ey - ny * 14)
        tri.close()
        c.drawPath(tri, _paint(color))


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un agent peut échouer *en silence*.')
    tr = S.cue('il tourne')
    card(c, t, tr, 90, 830, 900, 250, WHITE, 32, 'up')
    if prog(t, tr, 0.5) > 0.4:
        small(c, 'Une session · exemple', 140, 885, 20, DARK)
        icon(c, t, tr + 0.1, 'clock', 180, 990, 56, DARK)
        ap = S.cue("dizaines d'appels")
        for k in range(14):
            dot(c, t, ap + k * 0.06, 270 + k * 44, 990, 13, DARK)
        fx = S.cue('un résultat faux')
        if t >= fx:
            icon(c, t, fx, 'cross', 920, 990, 50, RED)
    sp = S.cue('personne ne sait pourquoi')
    card(c, t, sp, 90, 1110, 900, 130, LIGHT, 30, 'left')
    if prog(t, sp, 0.5) > 0.4:
        icon(c, t, sp + 0.1, 'search', 170, 1175, 56, DARK)
        reveal_plain(c, t, sp + 0.2, 'Sans traces : aucune explication', 240, 1188, 34, DARK)
    ob = S.cue("L'observabilité")
    card(c, t, ob, 90, 1280, 900, 130, RED, 30, 'up')
    if prog(t, ob, 0.5) > 0.4:
        icon(c, t, ob + 0.1, 'eye', 170, 1345, 56, WHITE)
        reveal_plain(c, t, ob + 0.2, "Observer : voir chaque étape", 240, 1358, 36, WHITE)


def s2(c, t, S):
    header(c, t, S, 'Tracer', 'Le *carnet de bord* de l\'agent')
    tr = S.cue('de bout en bout')
    card(c, t, tr, 90, 560, 900, 600, LIGHT, 32, 'up')
    if prog(t, tr, 0.5) > 0.4:
        small(c, 'Une trace · une session', 140, 620, 20, DARK)
        spans = [('Demande', 'la demande', 0.0, 1.0, DARK),
                 ('Modèle', 'appel au modèle', 0.05, 0.25, PL),
                 ("Outil : lire", "appel d'outil", 0.3, 0.2, PLL),
                 ('Modèle', "appel d'outil", 0.5, 0.2, PL),
                 ("Outil : tests", "appel d'outil", 0.7, 0.2, PLL),
                 ('Résultat', 'le résultat', 0.9, 0.1, RED)]
        x0, w0 = 330, 610
        for k, (s, kw, a, d, col) in enumerate(spans):
            at = S.cue(kw) + (k - 2) * 0.25 * (k in (3, 4))
            y = 650 + k * 72
            if t >= at:
                plain(c, s, 140, y + 40, 26, DARK)
            p = ease(prog(t, at, 0.5))
            if p > 0:
                rrect(c, x0 + w0 * a, y + 10, max(16, w0 * d * p), 44, 10, col)
    co = S.cue("suivi d'un colis")
    if t >= co:
        reveal_plain(c, t, co, "Comme le suivi d'un colis, étape par étape", 540, 1125, 28, DARK, 'Medium', 'center')
    ex = S.cue('Des outils existent')
    if t >= ex:
        small(c, 'Exemples à date · le paysage évolue vite', 90, 1230, 20, DARK)
    x = 90
    for k, s in enumerate(['OpenTelemetry', 'Langfuse', 'Phoenix']):
        chip(c, t, ex + 0.3 + k * 0.2, s, x, 1270, RED if k == 0 else PLL, WHITE if k == 0 else DARK, 32)
        x += chip_width(s, 32) + 20


def s3(c, t, S):
    header(c, t, S, 'Trois signaux', 'Latence, erreurs, *boucles*')
    la = S.cue('La latence')
    card(c, t, la, 90, 540, 900, 250, LIGHT, 32, 'left')
    if prog(t, la, 0.5) > 0.4:
        icon(c, t, la + 0.1, 'clock', 170, 615, 50, DARK)
        plain(c, 'Latence', 230, 627, 32, DARK, 'Medium')
        bar(c, t, la + 0.3, 140, 690, 800, 40, 0.55, PL, WHITE, 1.2)
        small(c, "L'attente du développeur", 940, 760, 18, DARK, align='right')
    er = S.cue("taux d'erreur")
    card(c, t, er, 90, 820, 900, 250, LIGHT, 32, 'left')
    if prog(t, er, 0.5) > 0.4:
        icon(c, t, er + 0.1, 'gear', 170, 895, 50, DARK)
        plain(c, "Erreurs d'outils", 230, 907, 32, DARK, 'Medium')
        tc = S.cue('tool calls')
        for k in range(10):
            bad = k in (2, 5, 6)
            x = 170 + k * 80
            dot(c, t, tc + k * 0.08, x, 990, 22, RED if bad else PL)
            if bad:
                icon(c, t, tc + k * 0.08 + 0.1, 'cross', x, 990, 22, WHITE)
        small(c, '3 sur 10 · illustratif', 940, 1050, 18, DARK, align='right')
    bo = S.cue('nombre de boucles')
    card(c, t, bo, 90, 1100, 900, 320, RED, 32, 'left')
    if prog(t, bo, 0.5) > 0.4:
        plain(c, 'Boucles par tâche', 140, 1170, 32, WHITE, 'Medium')
        rd = S.cue('tourne en rond')
        rt = S.cue('relance dix fois')
        loop_arrow(c, t, rt, 280, 1300, 70, WHITE, 9)
        if t >= rt:
            plain(c, 'Test', 280, 1311, 28, WHITE, 'Medium', 'center')
        n = int(clamp((t - rt) / 0.2, 0, 10)) if t >= rt else 0
        if n:
            plain(c, f'x{n}', 470, 1330, 72, WHITE, 'Medium')
        if t >= rd:
            reveal_plain(c, t, rd, 'Il tourne en rond', 940, 1320, 32, WHITE, 'Medium', 'right')


def s4(c, t, S):
    header(c, t, S, 'Journaliser', 'Des prompts *sous contrôle*')
    p = S.cue('données personnelles')
    card(c, t, p, 90, 540, 900, 170, LIGHT, 32, 'up')
    if prog(t, p, 0.5) > 0.4:
        icon(c, t, p + 0.1, 'doc', 170, 625, 56, DARK)
        reveal_plain(c, t, p + 0.2, 'Prompt : « Corrige le compte de', 240, 612, 30, DARK)
        reveal_plain(c, t, p + 0.3, 'Mme Martin, née le ... »', 240, 660, 30, RED)
    rg = S.cue('RGPD')
    if t >= rg:
        label(c, t, rg, 'RGPD · protection des données', 90, 780, RED, WHITE, 24)
    rows = [('clock', 'Durée de conservation', 'durée de conservation'),
            ('lock', 'Accès restreints', 'accès restreints'),
            ('eye', "Piste d'audit : qui a lu quoi", "piste d'audit")]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 830 + k * 150
        card(c, t, at, 90, y, 900, 130, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 170, y + 65, 56, RED if k == 2 else DARK)
            reveal_plain(c, t, at + 0.2, s, 240, y + 78, 36, DARK)
    j = S.cue('le juridique tranche')
    card(c, t, j, 90, 1290, 900, 130, DARK, 30, 'up')
    if prog(t, j, 0.5) > 0.4:
        icon(c, t, j + 0.1, 'shield', 170, 1355, 56, WHITE)
        reveal_plain(c, t, j + 0.2, 'Le juridique tranche les détails', 240, 1368, 34, WHITE)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Une *fonctionnalité*, pas un bonus')
    d = S.cue('tableaux de bord')
    card(c, t, d, 90, 540, 900, 420, LIGHT, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Tableau de bord · équipe A', 140, 600, 20, DARK)
        tiles = [('Latence', 0.5), ('Erreurs', 0.3), ('Boucles', 0.8)]
        for k, (s, f) in enumerate(tiles):
            x = 140 + k * 270
            at = d + 0.2 + k * 0.15
            card(c, t, at, x, 640, 250, 280, WHITE, 24, 'pop')
            if prog(t, at, 0.5) > 0.4:
                plain(c, s, x + 125, 700, 28, DARK, 'Medium', 'center')
                bh = 160 * f
                al = S.cue('Des alertes') if k == 2 else None
                col = RED if (al is not None and t >= al) else PL
                p = ease(prog(t, at + 0.2, 0.6))
                rrect(c, x + 85, 890 - bh * p, 80, bh * p, 8, col)
    a = S.cue('cinq boucles')
    card(c, t, a, 90, 1000, 900, 220, RED, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        for k in range(6):
            dot(c, t, a + 0.1 + k * 0.12, 170 + k * 70, 1080, 20, WHITE if k < 5 else DARK)
        st = S.cue("s'arrête et prévient")
        chip(c, t, st, 'Stop et alerte', 620, 1050, WHITE, RED, 30)
        if t >= a + 0.3:
            small(c, 'Seuil · exemple', 140, 1170, 18, WHITE)
    co = S.cue('reliez chaque trace')
    card(c, t, co, 90, 1260, 900, 150, LIGHT, 30, 'left')
    if prog(t, co, 0.5) > 0.4:
        icon(c, t, co + 0.1, 'doc', 170, 1335, 50, DARK)
        arrow(c, t, co + 0.2, 220, 1335, 300, 1335, DARK, 5, 16)
        icon(c, t, co + 0.3, 'coin', 350, 1335, 50, RED)
        reveal_plain(c, t, co + 0.4, 'Chaque trace, son coût', 420, 1347, 34, DARK)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Que *tracer*, et combien de temps le garder ?', 'Que faut-il tracer'),
        ('Qui peut *lire* les prompts journalisés ?', 'Qui peut lire'),
        ("À combien de *boucles* l'agent s'arrête-t-il ?", 'combien de boucles'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Tracez chaque session, suivez latence, erreurs et *boucles*.', 'tracez chaque session'),
        ('Prompts journalisés : *durée*, *accès* restreints, audit.', 'Journalisez les prompts'),
    ], '63 · Qualité et cycle de développement')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un agent de code peut échouer en silence. Par exemple, il tourne vingt minutes, "
        "enchaîne des dizaines d'appels, puis rend un résultat faux. "
        "Personne ne sait pourquoi. "
        "L'observabilité, c'est voir ce que fait l'agent, étape par étape.")),
    dict(kind='content', draw=s2, name='Tracer les sessions de bout en bout', text=(
        "D'abord, tracez chaque session de bout en bout. "
        "Une trace, c'est le carnet de bord de l'agent : la demande, chaque appel au modèle, "
        "chaque appel d'outil, puis le résultat. Comme le suivi d'un colis. "
        "Des outils existent, à date, comme OpenTelemetry ou Langfuse ; le paysage évolue vite.")),
    dict(kind='content', draw=s3, name='Latence, erreurs d\'outils et boucles', text=(
        "Suivez ensuite trois signaux. La latence : combien de temps attend le développeur. "
        "Le taux d'erreur des appels d'outils, les tool calls : un outil qui échoue fait dérailler la tâche. "
        "Et le nombre de boucles par tâche : un agent qui relance dix fois le même test tourne en rond.")),
    dict(kind='content', draw=s4, name='Journaliser les prompts, conformément au RGPD', text=(
        "Les prompts contiennent parfois des données personnelles. "
        "Journalisez-les en conformité avec le RGPD, le règlement européen sur la protection des données : "
        "une durée de conservation définie, des accès restreints, "
        "et une piste d'audit, qui dit qui a lu quoi. Sur les détails, le juridique tranche.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, l'observabilité est une fonctionnalité, pas un bonus. "
        "Prévoyez des tableaux de bord par équipe. Des alertes, aussi : "
        "par exemple, au-delà de cinq boucles sur la même étape, l'agent s'arrête et prévient. "
        "Et reliez chaque trace à son coût.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Que faut-il tracer, et combien de temps le garder ? "
        "Qui peut lire les prompts journalisés ? "
        "Et à partir de combien de boucles l'agent doit-il s'arrêter ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : tracez chaque session, et suivez latence, erreurs d'outils et boucles. "
        "Journalisez les prompts avec une durée de conservation, des accès restreints et une piste d'audit. "
        "Prochaine capsule : la qualité et le cycle de développement.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
