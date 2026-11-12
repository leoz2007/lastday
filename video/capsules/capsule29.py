from engine import *  # noqa
from engine import _paint  # noqa

NUM = 29
TITLE = 'GRAPHRAG'
FULL_TITLE = 'Knowledge graph et GraphRAG'
SLUG = 'knowledge_graph_graphrag'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def link(c, t, at, x1, y1, x2, y2, color=DARK, width=6, dur=0.45):
    """Trait simple entre deux noeuds, qui se trace progressivement."""
    p = ease(prog(t, at, dur))
    if p > 0:
        c.drawLine(x1, y1, lerp(x1, x2, p), lerp(y1, y2, p), _paint(color, width))


def s1(c, t, S):
    opening(c, t, S, CAP, 'Suivre les *liens*, pas seulement les mots.')
    a = S.cue('Un RAG classique')
    card(c, t, a, 90, 830, 900, 250, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'RAG classique', 140, 890, 22, DARK)
        se = S.cue('se ressemblent')
        for k in range(3):
            x = 140 + k * 140
            icon(c, t, a + 0.2 + k * 0.12, 'doc', x + 45, 990, 70, DARK)
        for k in range(3):
            bar(c, t, se + k * 0.15, 560, 915 + k * 42, 380, 24, 1.0, PL, WHITE, 0.5)
        if t >= se + 0.6:
            small(c, 'Passages semblables', 940, 1062, 20, DARK, align='right')
    g = S.cue('graphe de connaissances')
    card(c, t, g, 90, 1120, 900, 310, WHITE, 36, 'up')
    if prog(t, g, 0.5) > 0.4:
        small(c, 'Graphe de connaissances', 140, 1180, 22, DARK)
        xs = [190, 420, 650, 880]
        sl = S.cue('suivre un lien')
        for k in range(3):
            link(c, t, g + 0.4 + k * 0.15, xs[k], 1300, xs[k + 1], 1300, PL, 8)
            link(c, t, sl + k * 0.3, xs[k], 1300, xs[k + 1], 1300, RED, 8)
        for k, x in enumerate(xs):
            dot(c, t, g + 0.3 + k * 0.15, x, 1300, 34, RED if t >= sl + k * 0.3 else DARK)
        if t >= sl + 1.0:
            small(c, "D'un document à l'autre", 940, 1395, 20, RED, align='right')


def s2(c, t, S):
    header(c, t, S, 'Le graphe', 'Des entités, des *relations*')
    ents = [('Client', 'un client', 90, 570), ('Contrat', 'un contrat', 650, 570),
            ('Produit', 'un produit', 650, 830), ('Fournisseur', 'un fournisseur', 90, 830)]
    for s, kw, x, y in ents:
        box(c, t, S.cue(kw), x, y, 340, 110, s, DARK, WHITE, 36)
    rels = [('a signé', 440, 625, 640, 625, 540, 600, 'center'),
            ('couvre', 820, 690, 820, 820, 800, 768, 'right'),
            ('dépend de', 640, 885, 440, 885, 540, 860, 'center')]
    kws = ['a signé', 'couvre', 'dépend du']
    for (s, x1, y1, x2, y2, lx, ly, al), kw in zip(rels, kws):
        at = S.cue(kw)
        arrow(c, t, at, x1, y1, x2, y2, RED, 6, 20)
        if t >= at + 0.2:
            small(c, s, lx, ly, 22, RED, align=al)
    sp = S.cue('sens précis')
    card(c, t, sp, 90, 1030, 900, 390, LIGHT, 36, 'up')
    if prog(t, sp, 0.5) > 0.4:
        small(c, 'Un fait = entité, relation, entité', 140, 1095, 22, DARK)
        w1 = chip(c, t, sp + 0.2, 'Client', 140, 1150, DARK, WHITE, 34)
        w2 = chip(c, t, sp + 0.4, 'a signé', 140 + w1 + 70, 1150, RED, WHITE, 34)
        chip(c, t, sp + 0.6, 'Contrat', 140 + w1 + w2 + 140, 1150, DARK, WHITE, 34)
        arrow(c, t, sp + 0.3, 140 + w1 + 10, 1180, 140 + w1 + 60, 1180, DARK, 5, 14)
        arrow(c, t, sp + 0.5, 140 + w1 + w2 + 80, 1180, 140 + w1 + w2 + 130, 1180, DARK, 5, 14)
        su = S.cue("qu'on peut suivre")
        if t >= su:
            icon(c, t, su, 'search', 190, 1320, 60, RED)
            reveal_plain(c, t, su + 0.1, 'Un lien typé se suit, pas à pas', 250, 1335, 32, DARK)


def s3(c, t, S):
    header(c, t, S, 'Extraction', 'Le LLM *construit* le graphe')
    d = S.cue('vos documents')
    card(c, t, d, 90, 560, 250, 280, LIGHT, 30, 'up')
    if prog(t, d, 0.5) > 0.4:
        icon(c, t, d + 0.1, 'doc', 215, 640, 70, DARK)
        for k, w in enumerate([170, 140, 160]):
            rrect(c, 130, 720 + k * 34, w, 16, 8, PL)
    m = S.cue('par un LLM')
    arrow(c, t, m, 350, 700, 405, 700, DARK, 6, 18)
    box(c, t, m + 0.1, 415, 610, 210, 180, 'LLM', RED, WHITE, 48, 'Light', 30)
    r = S.cue('repère les entités')
    arrow(c, t, r, 635, 700, 690, 700, DARK, 6, 18)
    card(c, t, r + 0.1, 700, 560, 290, 280, LIGHT, 30, 'up')
    if prog(t, r + 0.1, 0.5) > 0.4:
        pr = S.cue('propose les relations')
        link(c, t, pr, 770, 650, 920, 760, RED, 6)
        dot(c, t, r + 0.2, 770, 650, 30, DARK)
        dot(c, t, r + 0.4, 920, 760, 30, DARK)
        if t >= pr:
            small(c, 'Relation', 770, 800, 18, RED)
    ex = S.cue('la phrase')
    card(c, t, ex, 90, 890, 900, 270, LIGHT, 36, 'up')
    if prog(t, ex, 0.5) > 0.4:
        small(c, 'Exemple', 140, 950, 20, DARK)
        reveal_plain(c, t, ex + 0.1, '« Ce client a signé le contrat de maintenance »', 140, 1010, 30, DARK)
        de = S.cue('deux entités')
        w1 = chip(c, t, de, 'Client', 140, 1050, DARK, WHITE, 30)
        w2 = chip(c, t, de + 0.3, 'a signé', 140 + w1 + 50, 1050, RED, WHITE, 30)
        chip(c, t, de + 0.15, 'Contrat de maintenance', 140 + w1 + w2 + 100, 1050, DARK, WHITE, 30)
        arrow(c, t, de + 0.3, 140 + w1 + 6, 1076, 140 + w1 + 44, 1076, DARK, 5, 14)
        arrow(c, t, de + 0.4, 140 + w1 + w2 + 56, 1076, 140 + w1 + w2 + 94, 1076, DARK, 5, 14)
    er = S.cue('se trompe parfois')
    card(c, t, er, 90, 1200, 900, 230, LIGHT, 36, 'up')
    if prog(t, er, 0.5) > 0.4:
        icon(c, t, er + 0.1, 'cross', 170, 1290, 60, RED)
        chip(c, t, S.cue('un nom mal reconnu'), 'Nom mal reconnu', 240, 1255, WHITE, DARK, 30)
        chip(c, t, S.cue('un lien oublié'), 'Lien oublié', 610, 1255, WHITE, DARK, 30)
        vf = S.cue('un lien oublié') + 0.8
        if t >= vf:
            icon(c, t, vf, 'eye', 170, 1380, 50, DARK)
            reveal_plain(c, t, vf + 0.1, 'Relecture et contrôles', 240, 1392, 30, RED, 'Medium')


def s4(c, t, S):
    header(c, t, S, 'GraphRAG', 'Suivre les liens, puis *répondre*')
    q = S.cue('quels clients')
    card(c, t, q, 90, 540, 900, 110, LIGHT, 30, 'up')
    if prog(t, q, 0.5) > 0.4:
        icon(c, t, q + 0.1, 'chat', 150, 595, 50, RED)
        reveal_plain(c, t, q + 0.2, 'Fournisseur en défaut : quels clients ?', 200, 607, 32, DARK)
    cols = [('Fournisseur', 'part du fournisseur', [890]),
            ('Produits', 'ses produits', [820, 960]),
            ('Contrats', 'les contrats', [780, 890, 1000]),
            ('Clients', 'les clients', [780, 890, 1000])]
    xs = [170, 420, 670, 920]
    edges = {1: [(0, 0), (0, 1)], 2: [(0, 0), (0, 1), (1, 2)], 3: [(0, 0), (1, 1), (2, 2)]}
    times = [S.cue(kw) for _, kw, _ in cols]
    for k in range(1, 4):
        for a, b in edges[k]:
            y1, y2 = cols[k - 1][2][a], cols[k][2][b]
            link(c, t, times[k] - 0.1, xs[k - 1], y1, xs[k], y2, RED, 6)
    for k, (s, kw, ys) in enumerate(cols):
        at = times[k]
        if t >= at:
            small(c, s, xs[k], 730, 20, DARK, align='center')
        for j, y in enumerate(ys):
            dot(c, t, at + j * 0.08, xs[k], y, 28, RED if k in (0, 3) else DARK)
    fm = S.cue('au modèle')
    arrow(c, t, fm, 540, 1045, 540, 1095, DARK, 6, 18)
    box(c, t, fm + 0.1, 90, 1105, 900, 110, 'Faits trouvés, puis réponse rédigée', RED, WHITE, 34)
    v = S.cue('Un RAG vectoriel')
    card(c, t, v, 90, 1260, 900, 170, LIGHT, 32, 'up')
    if prog(t, v, 0.5) > 0.4:
        small(c, 'RAG vectoriel', 140, 1315, 20, DARK)
        icon(c, t, v + 0.1, 'search', 170, 1375, 44, DARK)
        sm = S.cue('extraits semblables')
        reveal_plain(c, t, sm, 'Des extraits semblables, sans les liens', 220, 1388, 30, DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Un graphe a un *coût*')
    rows = [('Suivre des liens', 'suivent des liens', 'Graphe', RED),
            ('Retrouver une clause', 'retrouver une clause', 'RAG classique', DARK)]
    for k, (s, kw, sol, col) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 140
        box(c, t, at, 90, y, 470, 115, s, LIGHT, DARK, 32, 'Medium', 28, 'left')
        arrow(c, t, at + 0.2, 575, y + 57, 635, y + 57, DARK, 6, 18)
        box(c, t, at + 0.35, 650, y, 340, 115, sol, col, WHITE, 32)
    co = S.cue('Prévoyez les coûts')
    card(c, t, co, 90, 880, 900, 330, LIGHT, 36, 'up')
    if prog(t, co, 0.5) > 0.4:
        small(c, 'Les coûts à prévoir', 140, 940, 20, DARK)
        items = [('gear', 'Construire', 'construire le graphe'), ('clock', 'Mettre à jour', 'le tenir à jour'),
                 ('eye', 'Contrôler', "contrôler l'extraction")]
        for k, (ic, s, kw) in enumerate(items):
            at = S.cue(kw)
            x = 140 + k * 280
            card(c, t, at, x, 975, 250, 200, WHITE, 28, 'pop')
            if prog(t, at, 0.5) > 0.4:
                icon(c, t, at + 0.1, ic, x + 125, 1045, 60, RED)
                plain(c, s, x + 125, 1140, 28, DARK, 'Medium', 'center')
    me = S.cue('choisissez')
    card(c, t, me, 90, 1260, 900, 150, RED, 32, 'up')
    if prog(t, me, 0.5) > 0.4:
        icon(c, t, me + 0.1, 'user', 180, 1335, 60, WHITE)
        reveal_plain(c, t, me + 0.2, 'Entités et relations : avec le métier', 250, 1350, 36, WHITE, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Vos questions *suivent-elles des liens* ?', 'Vos questions'),
        ('Quelles *entités et relations* comptent pour le métier ?', 'Quelles entités'),
        ('Qui *met à jour* le graphe quand les documents changent ?', 'Et qui met'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un graphe relie des *entités* par des *relations typées*.', 'un graphe de connaissances'),
        ('GraphRAG *suit ces liens* pour croiser plusieurs documents.', 'GraphRAG suit'),
    ], "30 · L'inférence, de près")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un RAG classique retrouve des passages qui se ressemblent. "
        "Il ne sait pas suivre un lien d'un document à l'autre. "
        "C'est ce que permet un graphe de connaissances.")),
    dict(kind='content', draw=s2, name='Des entités et des relations', text=(
        "Un graphe de connaissances, ou knowledge graph, relie des entités par des relations typées. "
        "Des entités : un client, un contrat, un produit, un fournisseur. "
        "Des relations : le client a signé le contrat, qui couvre le produit, qui dépend du fournisseur. "
        "Chaque lien a un sens précis, qu'on peut suivre.")),
    dict(kind='content', draw=s3, name='Extraire le graphe des documents', text=(
        "Ce graphe peut être extrait de vos documents par un LLM. "
        "Il repère les entités, puis propose les relations. "
        "La phrase « ce client a signé le contrat de maintenance » donne deux entités et un lien. "
        "Mais l'extraction se trompe parfois : un nom mal reconnu, un lien oublié. Elle se vérifie.")),
    dict(kind='content', draw=s4, name='GraphRAG : suivre les liens', text=(
        "GraphRAG combine recherche dans le graphe et génération. "
        "Question : quels clients sont touchés si ce fournisseur fait défaut ? "
        "Le système part du fournisseur, suit les liens vers ses produits, les contrats, puis les clients, "
        "et transmet ces faits au modèle, qui répond. "
        "Un RAG vectoriel, qui cherche par proximité de sens, ramènerait seulement des extraits semblables.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, réservez le graphe aux questions qui suivent des liens : dépendances, impacts. "
        "Pour retrouver une clause, un RAG classique suffit souvent. "
        "Prévoyez les coûts : construire le graphe, le tenir à jour, contrôler l'extraction. "
        "Et choisissez entités et relations avec le métier.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Vos questions suivent-elles des liens ? "
        "Quelles entités et relations comptent pour le métier ? "
        "Et qui met le graphe à jour quand les documents changent ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un graphe de connaissances relie des entités par des relations typées. "
        "GraphRAG suit ces liens pour répondre aux questions qui croisent plusieurs documents. "
        "Prochaine capsule : l'inférence, de près.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
