from engine import *  # noqa
from engine import _paint  # noqa

NUM = 59
TITLE = 'CONTEXTE ET OUTILS'
FULL_TITLE = 'Contexte et outils'
SLUG = 'contexte_outils'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'


def plug(c, t, at, x, y, color=DARK):
    """Petite prise : deux broches et un corps, pointe vers la droite, centre (x, y)."""
    p = back(prog(t, at, 0.35))
    if p <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(p, p)
    rrect(c, -24, -20, 30, 40, 8, color)
    rrect(c, 6, -13, 16, 6, 3, color)
    rrect(c, 6, 7, 16, 6, 3, color)
    c.restore()


def s1(c, t, S):
    opening(c, t, S, CAP, 'Sans contexte, un agent code *à l\'aveugle*.')
    a = S.cue('agent de code brillant')
    card(c, t, a, 380, 860, 320, 260, RED, 32, 'pop')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'brain', 540, 960, 80, WHITE)
        plain(c, 'Agent', 540, 1070, 32, WHITE, 'Medium', 'center')
    av = S.cue("à l'aveugle")
    if t >= av:
        icon(c, t, av, 'eye', 540, 1180, 60, WHITE)
        if t >= av + 0.3:
            c.drawLine(500, 1210, 580, 1150, _paint(RED, 8))
    items = [('Tickets', 'vos tickets', 90, 880), ('Architecture', 'votre architecture', 90, 1060),
             ('API internes', 'API internes', 760, 880)]
    for s, kw, x, y in items:
        at = S.cue(kw)
        card(c, t, at, x, y, 230, 130, WHITE, 28, 'left' if x < 400 else 'right')
        if prog(t, at, 0.5) > 0.4:
            plain(c, s, x + 115, y + 75, 26 if len(s) > 10 else 30, DARK, 'Medium', 'center')
            icon(c, t, at + 0.2, 'lock', x + 115, y + 160, 36, PL)
    po = S.cue('ouvrir des portes')
    card(c, t, po, 90, 1290, 900, 120, WHITE, 30, 'up')
    if prog(t, po, 0.5) > 0.4:
        icon(c, t, po + 0.1, 'check', 160, 1350, 50, RED)
        reveal_plain(c, t, po + 0.2, 'Ouvrir des portes, une par une', 220, 1362, 36, DARK, 'Medium')


def s2(c, t, S):
    header(c, t, S, 'Les serveurs MCP', 'Une *prise* par système')
    m = S.cue('standard pour brancher')
    card(c, t, m, 90, 540, 900, 150, DARK, 32, 'up')
    if prog(t, m, 0.5) > 0.4:
        plug(c, t, m + 0.1, 170, 615, RED)
        reveal_plain(c, t, m + 0.2, 'MCP : une prise universelle', 230, 610, 36, WHITE, 'Medium')
        small(c, 'Un standard pour brancher des outils sur un modèle', 230, 655, 18, WHITE)
    ag = S.cue('serveurs MCP internes')
    card(c, t, ag, 400, 760, 280, 640, RED, 32, 'pop')
    if prog(t, ag, 0.5) > 0.4:
        icon(c, t, ag + 0.1, 'brain', 540, 1040, 80, WHITE)
        plain(c, 'Agent', 540, 1140, 32, WHITE, 'Medium', 'center')
    rows = [('Git', 'pour Git', 0), ('Tickets', 'un pour les tickets', 0), ('Documentation', 'la documentation', 0),
            ('CMDB', 'la CMDB', 1), ('API internes', 'vos API internes', 1)]
    li, ri = 0, 0
    for s, kw, side in rows:
        at = S.cue(kw)
        if side == 0:
            y = 770 + li * 210
            li += 1
            x = 90
        else:
            y = 870 + ri * 260
            ri += 1
            x = 720
        card(c, t, at, x, y, 270, 170, LIGHT, 28, 'left' if side == 0 else 'right')
        if prog(t, at, 0.5) > 0.4:
            plain(c, s, x + 135, y + 70, 26 if len(s) > 9 else 30, DARK, 'Medium', 'center')
            if s == 'CMDB':
                small(c, 'Référentiel des', x + 135, y + 112, 16, DARK, align='center')
                small(c, 'composants du SI', x + 135, y + 138, 16, DARK, align='center')
            else:
                small(c, 'Serveur MCP', x + 135, y + 120, 16, DARK, align='center')
            if side == 0:
                plug(c, t, at + 0.2, x + 300, y + 85, DARK)
                arrow(c, t, at + 0.3, x + 325, y + 85, 395, y + 85, DARK, 4, 12)
            else:
                plug(c, t, at + 0.2, x - 30, y + 85, DARK)
                arrow(c, t, at + 0.3, x - 55, y + 85, 685, y + 85, DARK, 4, 12)


def s3(c, t, S):
    header(c, t, S, 'La recherche', 'Retrouver *le bon passage*')
    tg = S.cue('trop grandes')
    card(c, t, tg, 90, 540, 900, 380, LIGHT, 36, 'up')
    ix = S.cue('On indexe')
    rt = S.cue('passages utiles')
    if prog(t, tg, 0.5) > 0.4:
        small(c, 'Code et documentation d\'architecture', 140, 600, 20, DARK)
        for k in range(24):
            col, row = k % 8, k // 8
            x = 150 + col * 70
            y = 640 + row * 80
            hit = k in (5, 18) and t >= rt
            rrect(c, x, y, 50, 60, 8, RED if hit else (PL if t >= ix + k * 0.03 else WHITE))
        if t >= rt:
            arrow(c, t, rt + 0.2, 720, 750, 790, 750, DARK, 6, 18)
            box(c, t, rt + 0.3, 800, 690, 160, 120, '2 passages', RED, WHITE, 26)
        if t >= ix:
            small(c, 'Index', 150, 895, 18, DARK)
    rg = S.cue('le RAG')
    card(c, t, rg, 90, 960, 900, 160, DARK, 32, 'up')
    if prog(t, rg, 0.5) > 0.4:
        icon(c, t, rg + 0.1, 'search', 170, 1040, 60, RED)
        reveal_plain(c, t, rg + 0.2, 'RAG : chercher, puis générer', 240, 1035, 36, WHITE, 'Medium')
        small(c, 'Génération augmentée par recherche', 240, 1080, 18, WHITE)
    ex = S.cue('règle de nommage')
    card(c, t, ex, 90, 1160, 900, 250, LIGHT, 32, 'up')
    if prog(t, ex, 0.5) > 0.4:
        small(c, 'Exemple', 140, 1215, 20, DARK)
        icon(c, t, ex + 0.1, 'doc', 180, 1310, 60, DARK)
        reveal_plain(c, t, ex + 0.2, 'Règle : svc-domaine-fonction', 240, 1300, 32, DARK, 'Medium')
        cr = S.cue("avant d'en créer un")
        if t >= cr:
            chip(c, t, cr, 'svc-paie-calcul', 240, 1330, RED, WHITE, 26)


def s4(c, t, S):
    header(c, t, S, 'Les paquets', 'Un *miroir*, pas Internet')
    a = S.cue('ne doit pas sortir')
    card(c, t, a, 90, 540, 900, 600, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        box(c, t, a + 0.1, 130, 760, 200, 130, 'Agent', RED, WHITE, 32)
        box(c, t, a + 0.2, 760, 590, 190, 110, 'Internet', WHITE, DARK, 28)
        arrow(c, t, a + 0.3, 340, 780, 750, 660, PL, 5, 16)
        icon(c, t, a + 0.6, 'cross', 545, 715, 44, RED)
        mi = S.cue('miroir interne')
        arrow(c, t, mi, 340, 840, 470, 900, DARK, 6, 18)
        card(c, t, mi + 0.2, 480, 820, 260, 240, DARK, 30, 'pop')
        if prog(t, mi + 0.2, 0.5) > 0.4:
            icon(c, t, mi + 0.3, 'db', 610, 900, 60, WHITE)
            plain(c, 'Miroir', 610, 990, 30, WHITE, 'Medium', 'center')
            small(c, 'Copie contrôlée', 610, 1030, 16, WHITE, align='center')
        cp = S.cue('dépôts publics')
        arrow(c, t, cp, 855, 710, 750, 880, DARK, 5, 14)
        va = S.cue('paquets validés')
        if t >= va:
            for k in range(3):
                icon(c, t, va + k * 0.15, 'check', 800 + k * 60, 960, 34, RED)
            small(c, 'Validés', 860, 1020, 18, RED, align='center')
    ex = S.cue('comme Artifactory')
    if t >= ex:
        small(c, 'Exemples à date', 90, 1210, 22, DARK)
    x = 90
    for s, kw in [('Artifactory', 'Artifactory'), ('Nexus', 'Nexus')]:
        x += chip(c, t, S.cue(kw), s, x, 1240, PLL, DARK, 32) + 20
    if t >= S.cue('Nexus') + 0.4:
        reveal_plain(c, t, S.cue('Nexus') + 0.4, 'Le paysage évolue vite', 90, 1390, 28, DARK, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Les droits *du développeur*')
    d = S.cue('les droits du développeur')
    card(c, t, d, 90, 540, 430, 420, LIGHT, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        icon(c, t, d + 0.1, 'user', 305, 640, 80, DARK)
        plain(c, 'Julie', 305, 740, 34, DARK, 'Medium', 'center')
    ag = S.cue('au nom de quelqu')
    card(c, t, ag, 560, 540, 430, 420, RED, 32, 'up')
    if prog(t, ag, 0.5) > 0.4:
        icon(c, t, ag + 0.1, 'brain', 775, 640, 80, WHITE)
        plain(c, 'Son agent', 775, 740, 34, WHITE, 'Medium', 'center')
    arrow(c, t, ag + 0.3, 525, 640, 555, 640, DARK, 5, 14)
    pa = S.cue('tickets de la paie')
    for k, (s, ok) in enumerate([('Tickets Mobile', True), ('Tickets Paie', False)]):
        y = 790 + k * 75
        for x0, fg, bgc in [(130, DARK, WHITE), (600, DARK, WHITE)]:
            if t >= pa + k * 0.2:
                chip(c, t, pa + k * 0.2, s, x0, y, bgc, fg, 24)
                icon(c, t, pa + k * 0.2 + 0.2, 'check' if ok else 'cross', x0 + 330, y + 22, 32,
                     (DARK if x0 < 400 else WHITE) if ok else (RED if x0 < 400 else WHITE))
    su = S.cue('super compte')
    card(c, t, su, 90, 1000, 900, 170, DARK, 32, 'up')
    if prog(t, su, 0.5) > 0.4:
        icon(c, t, su + 0.1, 'cross', 170, 1085, 50, RED)
        reveal_plain(c, t, su + 0.2, 'Jamais de super compte', 240, 1098, 38, WHITE, 'Medium')
    pr = S.cue('un propriétaire')
    card(c, t, pr, 90, 1210, 900, 170, LIGHT, 32, 'up')
    if prog(t, pr, 0.5) > 0.4:
        plug(c, t, pr + 0.1, 170, 1295, DARK)
        reveal_plain(c, t, pr + 0.2, 'Un connecteur, un propriétaire', 240, 1308, 36, DARK, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Quels systèmes *lire*, et lesquels *modifier* ?", 'Quels systèmes'),
        ("Quelle documentation est assez *fiable* pour l'index ?", 'Quelle documentation'),
        ("Comment les *droits* passent-ils à l'agent ?", 'Et comment'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Un agent n'est utile que s'il *voit* votre SI.", "un agent n'est utile"),
        ('MCP, recherche, miroir : avec les *droits du développeur*.', 'Des serveurs MCP'),
    ], '60 · Sécurité des agents')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un agent de code brillant, mais sans accès à votre système d'information, code à l'aveugle. "
        "Il ne connaît ni vos tickets, ni votre architecture, ni vos API internes. "
        "Il faut lui ouvrir des portes, une par une.")),
    dict(kind='content', draw=s2, name='Des serveurs MCP internes', text=(
        "Ces portes, ce sont souvent des serveurs MCP internes. "
        "Rappel : MCP est un standard pour brancher des outils sur un modèle, comme une prise universelle. "
        "Un serveur pour Git, un pour les tickets, un pour la documentation, "
        "un pour la CMDB, le référentiel des composants du système d'information, et d'autres pour vos API internes.")),
    dict(kind='content', draw=s3, name='Recherche et RAG sur le code et la documentation', text=(
        "Ensuite, la recherche. Le code et la documentation d'architecture sont trop grandes "
        "pour tout donner au modèle. On indexe, puis on retrouve les passages utiles : "
        "c'est le RAG, la génération augmentée par recherche. "
        "Exemple : l'agent retrouve la règle de nommage des services avant d'en créer un.")),
    dict(kind='content', draw=s4, name='Un miroir de paquets plutôt qu\'Internet', text=(
        "Puis les paquets, ces bibliothèques que le code télécharge. "
        "L'agent ne doit pas sortir librement sur Internet. "
        "Il passe par un miroir interne, une copie contrôlée des dépôts publics, "
        "comme Artifactory ou Nexus, exemples à date. Seuls les paquets validés y entrent.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, une règle : chaque accès suit les droits du développeur. "
        "L'agent agit au nom de quelqu'un, jamais avec un super compte. "
        "Si Julie ne voit pas les tickets de la paie, son agent non plus. "
        "Et chaque connecteur a un propriétaire, qui le maintient.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels systèmes l'agent doit-il lire, et lesquels modifier ? "
        "Quelle documentation est assez fiable pour être indexée ? "
        "Et comment les droits du développeur passent-ils à l'agent ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un agent n'est utile que s'il voit votre système d'information. "
        "Des serveurs MCP, une recherche sur le code, un miroir de paquets, "
        "toujours avec les droits du développeur. "
        "Prochaine capsule : la sécurité des agents.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
