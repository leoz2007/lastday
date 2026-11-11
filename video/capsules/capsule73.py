from engine import *  # noqa
from engine import _paint  # noqa

NUM = 73
TITLE = 'SPEC-DRIVEN DEV'
FULL_TITLE = 'Spec-driven development'
SLUG = 'spec_driven_development'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def s1(c, t, S):
    opening(c, t, S, CAP, "La meilleure instruction est *un document*.")
    m = S.cue("n'est pas un message")
    msgs = [('Ajoute un bouton', 870), ('Non, plutôt en haut', 990), ('Et aussi un filtre', 1110)]
    for k, (s, y) in enumerate(msgs):
        at = m + k * 0.3
        icon(c, t, at, 'chat', 130, y + 30, 46, PL)
        chip(c, t, at + 0.1, s, 170, y, WHITE, DARK, 26)
    fe = S.cue("au fil de l'eau")
    if t >= fe:
        small(c, "Au fil de l'eau", 90, 1240, 20, WHITE)
    d = S.cue("C'est un document")
    card(c, t, d, 630, 840, 360, 440, WHITE, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        icon(c, t, d + 0.1, 'doc', 810, 930, 70, RED)
        sp = S.cue('spécification écrite')
        for k, w in enumerate([260, 220, 280, 180, 240]):
            if t >= sp + k * 0.1:
                rrect(c, 680, 1010 + k * 46, w, 20, 10, PL if k else RED)
    sd = S.cue('spec-driven development')
    if t >= sd:
        reveal_plain(c, t, sd, 'Développement piloté par la spec', 540, 1390, 34, WHITE, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, 'La spécification', 'Le *quoi* et le *pourquoi*')
    q = S.cue('le quoi')
    card(c, t, q, 90, 540, 900, 890, LIGHT, 36, 'up')
    if prog(t, q, 0.5) <= 0.4:
        return
    icon(c, t, q + 0.1, 'doc', 160, 620, 56, RED)
    plain(c, 'spec/annulation.md', 210, 635, 30, DARK)
    secs = [('Quoi', 'Annuler une commande', 'le besoin'),
            ('Pourquoi', 'Moins d\'appels au support', 'les utilisateurs')]
    for k, (h, s, kw) in enumerate(secs):
        at = S.cue(kw)
        y = 690 + k * 130
        card(c, t, at, 140, y, 800, 110, WHITE, 24, 'left')
        if prog(t, at, 0.5) > 0.4:
            small(c, h, 180, y + 45, 18, RED)
            plain(c, s, 180, y + 88, 30, DARK)
    ca = S.cue("critères d'acceptation")
    if t >= ca:
        small(c, "Critères d'acceptation", 140, 990, 20, RED)
    crit = [('Possible tant que non expédiée', 'tant qu\'elle'),
            ('Refusée une fois expédiée', 'tant qu\'elle'),
            ('Le client reçoit une confirmation', 'tant qu\'elle')]
    for k, (s, kw) in enumerate(crit):
        at = S.cue(kw) + k * 0.4
        y = 1020 + k * 120
        card(c, t, at, 140, y, 800, 100, WHITE, 24, 'left')
        if prog(t, at, 0.5) > 0.4:
            c.drawCircle(195, y + 50, 26, _paint(RED))
            icon(c, t, at + 0.1, 'check', 195, y + 50, 30, WHITE)
            plain(c, s, 245, y + 61, 30, DARK)


STEPS = [('Spécification', 'le quoi', 'la spécification'),
         ('Plan technique', 'le comment', 'le plan technique'),
         ('Tâches', 'découpage', 'petites tâches'),
         ('Implémentation', "par l'agent", 'les implémente'),
         ('Vérification', 'vs critères', 'on vérifie')]


def s3(c, t, S):
    header(c, t, S, "L'enchaînement", 'Cinq étapes, *un humain* entre')
    hv = S.cue('un humain valide')
    for k, (nm, sub, kw) in enumerate(STEPS):
        at = S.cue(kw) if kw != 'la spécification' else S.t0 + 0.6
        y = 545 + k * 180
        card(c, t, at, 90, y, 640, 130, RED if k == 3 else LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if k == 3 else DARK
            plain(c, f'{k + 1}', 140, y + 82, 40, WHITE if k == 3 else RED, 'Bold')
            plain(c, nm, 200, y + 64, 34, fg)
            small(c, sub, 200, y + 105, 18, fg)
        if k < 4:
            nxt = S.cue(STEPS[k + 1][2])
            arrow(c, t, nxt - 0.3, 410, y + 135, 410, y + 175, DARK, 5, 14)
            # point de validation humaine
            va = hv + k * 0.2
            if t >= va:
                c.drawCircle(860, y + 155, 40, _paint(PLL))
                icon(c, t, va, 'user', 860, y + 150, 40, RED)
                rrect(c, 735, y + 153, 80, 4, 2, PL)
    if t >= hv + 1.0:
        small(c, 'Validation', 860, 1440, 18, RED, align='center')


def s4(c, t, S):
    header(c, t, S, 'Versionnée', 'La spec devient *la référence*')
    v = S.cue('versionnée avec le code')
    card(c, t, v, 90, 540, 900, 520, LIGHT, 36, 'up')
    if prog(t, v, 0.5) > 0.4:
        small(c, 'Le même dépôt, au fil des versions', 140, 600, 20, DARK)
        rrect(c, 260, 860, 640, 6, 3, DARK)
        for k in range(3):
            at = v + 0.3 + k * 0.4
            x = 320 + k * 260
            dot(c, t, at, x, 863, 18, RED)
            chip(c, t, at + 0.1, f'v{k + 1}', x, 900, WHITE, DARK, 24, align='center')
            box(c, t, at + 0.1, x - 100, 640, 200, 80, 'Spec', RED if k == 2 else WHITE,
                WHITE if k == 2 else DARK, 28, mode='pop')
            box(c, t, at + 0.2, x - 100, 740, 200, 80, 'Code', WHITE, DARK, 28, mode='pop')
        if t >= v + 1.5:
            small(c, 'Elles évoluent ensemble', 140, 1010, 18, RED)
    rs = S.cue('on relit la spec')
    card(c, t, rs, 90, 1100, 900, 330, LIGHT, 36, 'up')
    if prog(t, rs, 0.5) > 0.4:
        icon(c, t, rs + 0.1, 'chat', 200, 1200, 56, PL)
        plain(c, 'Historique de conversation', 260, 1212, 30, DARK)
        icon(c, t, rs + 0.1, 'cross', 900, 1200, 40, DARK)
        icon(c, t, rs + 0.3, 'doc', 200, 1330, 60, RED)
        plain(c, 'La spec : la source des choix', 260, 1342, 30, RED)
        icon(c, t, rs + 0.3, 'check', 900, 1330, 40, RED)
        na = S.cue('nouvel arrivant')
        if t >= na:
            icon(c, t, na, 'user', 760, 1330, 40, DARK)
            icon(c, t, na + 0.2, 'gear', 830, 1330, 36, DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'La PO *au centre*')
    q = S.cue('la qualité de la spec')
    card(c, t, q, 90, 540, 900, 300, LIGHT, 36, 'up')
    if prog(t, q, 0.5) > 0.4:
        small(c, 'Illustratif', 140, 600, 20, DARK)
        icon(c, t, q + 0.1, 'user', 160, 700, 56, RED)
        plain(c, 'Spec', 220, 680, 28, DARK)
        bar(c, t, q + 0.3, 220, 700, 260, 30, 0.85, RED, WHITE, 0.6)
        arrow(c, t, q + 0.8, 510, 715, 590, 715, DARK, 5, 16)
        plain(c, 'Code', 620, 680, 28, DARK)
        bar(c, t, q + 1.0, 620, 700, 300, 30, 0.85, RED, WHITE, 0.6)
        if t >= q + 1.4:
            small(c, 'Une spec précise, un code meilleur en général', 140, 800, 18, DARK)
    va = S.cue('trop vague')
    card(c, t, va, 90, 880, 900, 260, LIGHT, 36, 'up')
    if prog(t, va, 0.5) > 0.4:
        small(c, 'Limite 1 · spec vague', 140, 940, 20, DARK)
        chip(c, t, va + 0.2, '« Gérer les annulations »', 140, 970, WHITE, DARK, 28)
        pl = S.cue('plausible, mais faux')
        if t >= pl:
            icon(c, t, pl, 'code', 180, 1085, 44, DARK)
            reveal_plain(c, t, pl + 0.1, 'Code plausible, mais faux', 230, 1097, 32, RED, 'Medium')
    fg = S.cue('une spec figée')
    card(c, t, fg, 90, 1170, 900, 260, LIGHT, 36, 'up')
    if prog(t, fg, 0.5) > 0.4:
        small(c, 'Limite 2 · spec figée', 140, 1230, 20, DARK)
        icon(c, t, fg + 0.1, 'clock', 180, 1320, 56, DARK)
        reveal_plain(c, t, fg + 0.2, 'Elle vieillit', 240, 1335, 32, DARK, 'Medium')
        mj = S.cue('mettez-la à jour')
        if t >= mj:
            chip(c, t, mj, "Spec d'abord, puis l'agent", 520, 1302, RED, WHITE, 26)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Nos critères d'acceptation sont-ils *vérifiables* ?", 'Nos critères'),
        ("Qui *valide* le plan et les tâches avant le code ?", 'Qui valide'),
        ('Qui tient la spec *à jour* quand le besoin change ?', 'Et qui tient'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("La *spécification* guide l'agent, étape par étape.", 'la spécification guide'),
        ('Précise et *à jour*, elle conditionne la qualité du code.', 'Précise'),
    ], '74 · Interopérabilité des agents')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Avec un agent de code, la meilleure instruction n'est pas un message. C'est un document. "
        "Le spec-driven development, ou développement piloté par la spécification, "
        "fait travailler l'agent à partir d'une spécification écrite, plutôt que de demandes au fil de l'eau.")),
    dict(kind='content', draw=s2, name='La spécification', text=(
        "Tout part de la spécification, la spec. Elle dit le quoi et le pourquoi : "
        "le besoin, les utilisateurs, les règles. "
        "Elle fixe surtout les critères d'acceptation, les conditions vérifiables d'une fonctionnalité terminée. "
        "Par exemple : un client peut annuler sa commande tant qu'elle n'est pas expédiée.")),
    dict(kind='content', draw=s3, name="L'enchaînement des étapes", text=(
        "Vient ensuite le plan technique, qui décrit le comment : l'architecture, les données, les choix. "
        "Il est découpé en petites tâches. L'agent les implémente une par une, "
        "puis on vérifie le résultat contre les critères. "
        "Entre chaque étape, un humain valide avant de continuer.")),
    dict(kind='content', draw=s4, name='Une spec versionnée', text=(
        "La spécification est versionnée avec le code, dans le même dépôt. "
        "Elle devient la référence : quand une question se pose, on relit la spec, "
        "pas l'historique d'une conversation. "
        "Un nouvel arrivant, humain ou agent, sait d'où vient chaque choix.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, la PO est au centre : la qualité de la spec conditionne la qualité du code. "
        "Mais attention aux limites. Une spec trop vague produit du code plausible, mais faux. "
        "Et une spec figée vieillit : quand le besoin change, mettez-la à jour d'abord, "
        "puis laissez l'agent suivre.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. "
        "Nos critères d'acceptation sont-ils vraiment vérifiables ? "
        "Qui valide le plan et les tâches avant que l'agent code ? "
        "Et qui tient la spec à jour quand le besoin change ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : avec un agent de code, la spécification guide le travail, étape par étape. "
        "Précise et tenue à jour, elle conditionne la qualité du code. "
        "Prochaine capsule : l'interopérabilité des agents, quand des agents de systèmes différents travaillent ensemble.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
