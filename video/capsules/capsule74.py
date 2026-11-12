from engine import *  # noqa
from engine import _paint  # noqa

NUM = 74
TITLE = 'INTEROPÉRABILITÉ'
FULL_TITLE = 'Interopérabilité des agents'
SLUG = 'interoperabilite_agents'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def agent(c, t, at, cx, cy, r, fill, fg):
    """Un agent : disque plein avec un pictogramme."""
    dot(c, t, at, cx, cy, r, fill)
    if t >= at + 0.15:
        icon(c, t, at + 0.15, 'brain', cx, cy, r * 1.1, fg)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Vos agents parleront à des *agents inconnus*.')
    a = S.t0 + 0.6
    agent(c, t, a, 260, 1080, 90, WHITE, DARK)
    small(c, 'Votre agent', 260, 1220, 22, WHITE, align='center')
    others = [('Autre fournisseur', 'autre fournisseur', 900), ('Autre équipe', 'autre équipe', 1260)]
    for s, kw, y in others:
        at = S.cue(kw)
        agent(c, t, at, 820, y, 70, PL, DARK)
        if t >= at + 0.2:
            small(c, s, 820, y + 110, 20, WHITE, align='center')
    for k, (s, kw, y) in enumerate(others):
        arrow(c, t, S.cue(kw) + 0.2, 360, 1050 + k * 60, 740, y + (20 if k == 0 else -20), PL, 5, 16)
    lc = S.cue('langue commune')
    chip(c, t, lc, 'Langue commune', 545, 1360, RED, WHITE, 32, align='center')


def s2(c, t, S):
    header(c, t, S, 'Les protocoles', 'Des outils, puis des *agents*')
    m = S.cue('MCP')
    card(c, t, m, 90, 540, 900, 300, LIGHT, 32, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'MCP · Agent vers outils et données', 140, 600, 20, DARK)
        agent(c, t, m + 0.2, 220, 720, 56, DARK, WHITE)
        tools = [('db', 'données'), ('gear', 'outils'), ('doc', 'outils')]
        for k, (ic, kw) in enumerate(tools):
            at = S.cue(kw) + k * 0.15
            x = 560 + k * 170
            if k == 0:
                arrow(c, t, at, 290, 720, x - 60, 720, DARK, 4, 12)
            dot(c, t, at, x, 720, 52, WHITE)
            icon(c, t, at + 0.1, ic, x, 720, 52, DARK)
    aa = S.cue('agent à agent')
    card(c, t, aa, 90, 870, 900, 330, LIGHT, 32, 'up')
    if prog(t, aa, 0.5) > 0.4:
        small(c, 'Agent à agent', 140, 930, 20, DARK)
        agent(c, t, aa + 0.2, 240, 1060, 56, DARK, WHITE)
        agent(c, t, aa + 0.35, 840, 1060, 56, RED, WHITE)
        arrow(c, t, aa + 0.5, 310, 1040, 770, 1040, DARK, 4, 12)
        arrow(c, t, aa + 0.7, 770, 1080, 310, 1080, RED, 4, 12)
        ex = S.cue('A2A')
        chip(c, t, ex, 'A2A · exemple à date', 540, 1120, WHITE, DARK, 26, align='center')
    pr = S.cue('prise standard')
    card(c, t, pr, 90, 1230, 900, 200, RED, 32, 'up')
    if prog(t, pr, 0.5) > 0.4:
        icon(c, t, pr + 0.1, 'bolt', 170, 1330, 60, WHITE)
        reveal_plain(c, t, pr + 0.2, 'Comme une prise standard', 230, 1320, 38, WHITE)
        jn = S.cue('encore jeunes')
        if t >= jn:
            reveal_plain(c, t, jn, 'Des standards jeunes, qui évoluent', 230, 1380, 26, WHITE, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Le principe', 'Se décrire, puis *déléguer*')
    cv = S.cue('carte de visite')
    card(c, t, cv, 90, 540, 900, 470, LIGHT, 32, 'up')
    if prog(t, cv, 0.5) > 0.4:
        small(c, "Carte de l'agent", 140, 600, 20, DARK)
        rrect(c, 140, 640, 800, 330, 24, WHITE)
        agent(c, t, cv + 0.2, 250, 760, 70, RED, WHITE)
        rows = [('Qui il est', 'qui il est', 'Agent conformité'),
                ('Ce qu\'il sait faire', 'ce qu\'il sait faire', 'Vérifier un fournisseur'),
                ('Comment le joindre', 'comment le joindre', 'Adresse du service')]
        for k, (lab, kw, val) in enumerate(rows):
            at = S.cue(kw)
            y = 700 + k * 90
            if t >= at:
                small(c, lab, 370, y, 18, RED)
            reveal_plain(c, t, at + 0.1, val, 370, y + 40, 30, DARK, 'Medium')
    steps = [('Lire la carte', 'la lit'), ('Déléguer', 'délègue une tâche'), ('Suivre', 'suit son avancement')]
    for k, (s, kw) in enumerate(steps):
        at = S.cue(kw)
        x = 90 + k * 310
        box(c, t, at, x, 1060, 280, 140, s, RED if k == 1 else PLL, WHITE if k == 1 else DARK, 32)
        if k < 2:
            arrow(c, t, at + 0.3, x + 284, 1130, x + 306, 1130, DARK, 5, 12)
    st = S.cue('suit son avancement') + 0.2
    if t >= st:
        small(c, 'Avancement de la tâche', 90, 1290, 18, DARK)
        bar(c, t, st, 90, 1320, 900, 36, 0.7, RED, PLL, 0.8)


def s4(c, t, S):
    header(c, t, S, 'Exemple', "L'achat consulte la *conformité*")
    a = S.cue("l'agent d'achat")
    card(c, t, a, 90, 540, 380, 340, LIGHT, 32, 'pop')
    if prog(t, a, 0.5) > 0.4:
        agent(c, t, a + 0.1, 280, 660, 60, DARK, WHITE)
        plain(c, "Agent d'achat", 280, 790, 32, DARK, 'Medium', 'center')
        small(c, 'Votre entreprise', 280, 840, 18, DARK, align='center')
    b = S.cue("l'agent conformité")
    card(c, t, b, 610, 540, 380, 340, LIGHT, 32, 'pop')
    if prog(t, b, 0.5) > 0.4:
        agent(c, t, b + 0.1, 800, 660, 60, RED, WHITE)
        plain(c, 'Agent conformité', 800, 790, 32, DARK, 'Medium', 'center')
        small(c, 'Autre équipe', 800, 840, 18, DARK, align='center')
    cf = S.cue('Il confie')
    arrow(c, t, cf, 480, 640, 600, 640, DARK, 5, 16)
    if t >= cf:
        chip(c, t, cf + 0.1, 'Vérifier ce fournisseur', 540, 920, PLL, DARK, 30, align='center')
    av = S.cue('renvoie son avis')
    arrow(c, t, av, 600, 720, 480, 720, RED, 5, 16)
    if t >= av:
        chip(c, t, av + 0.1, 'Avis : fournisseur conforme', 540, 1010, RED, WHITE, 30, align='center')
    po = S.cue('poursuit')
    card(c, t, po, 90, 1120, 440, 200, LIGHT, 32, 'up')
    if prog(t, po, 0.5) > 0.4:
        icon(c, t, po + 0.1, 'check', 180, 1220, 60, RED)
        reveal_plain(c, t, po + 0.2, 'Poursuit', 240, 1235, 38, DARK)
    ar = S.cue('poursuit') + 0.3
    card(c, t, ar, 550, 1120, 440, 200, LIGHT, 32, 'up')
    if prog(t, ar, 0.5) > 0.4:
        icon(c, t, ar, 'cross', 640, 1220, 50, DARK)
        reveal_plain(c, t, ar + 0.05, "S'arrête", 700, 1235, 38, DARK)
    if t >= ar + 0.3:
        small(c, "Selon l'avis reçu", 540, 1380, 20, DARK, align='center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Faire confiance, *avec preuves*')
    rows = [('user', 'Identité', 'Qui est cet agent, preuve à l\'appui', 'Identité'),
            ('lock', 'Droits délégués', 'Au nom de qui, avec quelles limites', 'Droits délégués'),
            ('shield', 'Réponse reçue', 'Une donnée, jamais un ordre', 'une injection')]
    for k, (ic, lab, sub, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 540 + k * 220
        hot = k == 2
        card(c, t, at, 90, y, 900, 195, RED if hot else LIGHT, 32, 'left')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if hot else DARK
            icon(c, t, at + 0.1, ic, 175, y + 98, 60, fg)
            reveal_plain(c, t, at + 0.15, lab, 250, y + 85, 36, fg)
            reveal_plain(c, t, at + 0.25, sub, 250, y + 140, 28, fg, 'Medium')
    tr = S.cue('traçabilité')
    if t >= tr:
        small(c, 'Trace de bout en bout', 90, 1230, 20, DARK)
    if t >= tr:
        rrect(c, 90, 1300, 900 * ease(prog(t, tr, 0.9)), 6, 3, PL)
    for k, s in enumerate(['Demande', 'Délégation', 'Avis', 'Décision']):
        x = 130 + k * 273
        dot(c, t, tr + 0.2 + k * 0.2, x, 1303, 18, RED)
        if t >= tr + 0.3 + k * 0.2:
            small(c, s, x, 1360, 18, DARK, align='center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Comment chaque agent *prouve-t-il* son identité ?', 'Comment chaque agent'),
        ("Qui *répond* d'une erreur de l'agent d'en face ?", 'Qui répond'),
        ("Peut-on *retracer* l'échange de bout en bout ?", 'retracer'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('MCP relie aux outils, l\'agent à agent relie *les agents*.', 'MCP relie'),
        ('Chaque délégation : *identité*, limites et traces.', 'Chaque délégation'),
    ], '75 · Calcul confidentiel')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Bientôt, vos agents travailleront avec des agents que vous n'avez pas construits : "
        "chez un autre fournisseur, ou dans une autre équipe. "
        "Pour coopérer, il leur faut une langue commune.")),
    dict(kind='content', draw=s2, name='MCP et protocoles agent à agent', text=(
        "Vous connaissez MCP, pour Model Context Protocol : il relie un agent à des outils et à des données. "
        "Les protocoles agent à agent relient deux agents entre eux. "
        "A2A, pour Agent to Agent, en est un exemple à date. "
        "C'est comme une prise standard : peu importe qui a fabriqué l'appareil. "
        "Mais ces standards sont encore jeunes, et ils évoluent.")),
    dict(kind='content', draw=s3, name='Se découvrir, se décrire, déléguer', text=(
        "Concrètement, chaque agent publie une sorte de carte de visite : "
        "qui il est, ce qu'il sait faire, comment le joindre. "
        "Un autre agent la lit, lui délègue une tâche, puis suit son avancement.")),
    dict(kind='content', draw=s4, name="Exemple : l'achat et la conformité", text=(
        "Exemple. L'agent d'achat de votre entreprise prépare une commande. "
        "Il confie la vérification du fournisseur à l'agent conformité d'une autre équipe. "
        "Celui-ci contrôle, puis renvoie son avis. "
        "L'agent d'achat poursuit, ou s'arrête.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, chaque échange pose une question de confiance. "
        "Identité : qui est cet agent, et peut-il le prouver ? "
        "Droits délégués : il agit au nom de qui, avec quelles limites ? "
        "Et la réponse reçue peut contenir une injection, des instructions cachées : "
        "traitez-la comme une donnée, jamais comme un ordre. "
        "Enfin, gardez une traçabilité de bout en bout.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Comment chaque agent prouve-t-il son identité ? "
        "Qui répond d'une erreur de l'agent d'en face ? "
        "Et peut-on retracer l'échange de bout en bout ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : MCP relie un agent à ses outils, les protocoles agent à agent relient les agents entre eux. "
        "Chaque délégation demande une identité, des limites et des traces. "
        "Prochaine capsule : le calcul confidentiel.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
