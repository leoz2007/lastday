from engine import *  # noqa
from engine import _paint  # noqa

NUM = 49
TITLE = 'GUARDRAILS'
FULL_TITLE = 'Guardrails et modération'
SLUG = 'guardrails_moderation'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def pipeline(c, t, a_in, a_mod, a_s1, a_s2, a_out, y, on_dark=True, hot=None):
    """Entrée -> contrôle -> modèle -> contrôle -> sortie, sur une ligne."""
    fg = WHITE if on_dark else DARK
    box(c, t, a_in, 90, y, 200, 120, 'Entrée', WHITE if on_dark else LIGHT, DARK, 30)
    arrow(c, t, a_mod, 295, y + 60, 335, y + 60, fg, 5, 14)
    on1 = hot in (None, 'in')
    card(c, t, a_s1, 345, y + 10, 100, 100, RED if on1 else PL, 50, 'pop')
    icon(c, t, a_s1 + 0.1, 'shield', 395, y + 60, 56, WHITE if on1 else DARK)
    arrow(c, t, a_mod, 450, y + 60, 490, y + 60, fg, 5, 14)
    box(c, t, a_mod + 0.1, 500, y, 200, 120, 'Modèle', WHITE if on_dark else DARK,
        DARK if on_dark else WHITE, 30)
    arrow(c, t, a_mod + 0.2, 705, y + 60, 745, y + 60, fg, 5, 14)
    on2 = hot in (None, 'out')
    card(c, t, a_s2, 755, y + 10, 100, 100, RED if on2 else PL, 50, 'pop')
    icon(c, t, a_s2 + 0.1, 'shield', 805, y + 60, 56, WHITE if on2 else DARK)
    arrow(c, t, a_out, 860, y + 60, 900, y + 60, fg, 5, 14)
    icon(c, t, a_out + 0.1, 'chat', 945, y + 60, 60, fg)


def s1(c, t, S):
    opening(c, t, S, CAP, "Le modèle n'est pas *seul* à décider.")
    m = S.cue('son modèle')
    e = S.cue('ce qui entre')
    gf = S.cue('garde-fous')
    pipeline(c, t, m - 0.3, m, gf, gf + 0.3, m + 0.4, 920)
    if t >= e:
        reveal_plain(c, t, e + 0.2, 'Contrôle', 395, 1100, 26, WHITE, 'Medium', 'center')
        reveal_plain(c, t, e + 0.9, 'Contrôle', 805, 1100, 26, WHITE, 'Medium', 'center')
    g = S.cue('les guardrails')
    chip(c, t, g, 'Guardrails = garde-fous', 540, 1250, WHITE, DARK, 34, align='center')


def s2(c, t, S):
    header(c, t, S, 'En entrée', 'Vérifier *la demande*')
    a0 = S.t0 + 0.4
    pipeline(c, t, a0, a0, a0 + 0.2, a0 + 0.3, a0 + 0.4, 540, on_dark=False, hot='in')
    rows = [('Sujet interdit', 'Un sujet interdit', 'Conseil médical ?', 'shield'),
            ("Tentative d'injection", "tentative d'injection", '« Ignore tes consignes »', 'bolt'),
            ('Données personnelles', 'données personnelles', 'Carte 4970 **** ****', 'lock')]
    for k, (nm, kw, ex, ic) in enumerate(rows):
        at = S.cue(kw)
        y = 720 + k * 240
        card(c, t, at, 90, y, 900, 210, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 160, y + 105, 60, RED)
            small(c, nm, 230, y + 80, 22, DARK)
            reveal_plain(c, t, at + 0.3, ex, 230, y + 150, 32, DARK)
    ms = S.cue('on masque')
    if t >= ms:
        chip(c, t, ms, 'Masqué', 940 - chip_width('Masqué', 28), 720 + 2 * 240 + 120, RED, WHITE, 28)


def s3(c, t, S):
    header(c, t, S, 'En sortie', 'Vérifier *la réponse*')
    a0 = S.t0 + 0.4
    pipeline(c, t, a0, a0, a0 + 0.2, a0 + 0.3, a0 + 0.4, 540, on_dark=False, hot='out')
    items = [('Inapproprié', 'contenu inapproprié'), ('Info sensible', 'information sensible'),
             ('Format cassé', 'format cassé'), ('Hors sujet', 'hors sujet')]
    for k, (s, kw) in enumerate(items):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        y = 720 + (k // 2) * 150
        box(c, t, at, x, y, 440, 120, s, LIGHT, DARK, 32)
        icon(c, t, at + 0.3, 'cross', x + 395, y + 60, 34, RED)
    oo = S.cue('trois outils')
    card(c, t, oo, 90, 1050, 900, 380, LIGHT, 36, 'up')
    if prog(t, oo, 0.5) > 0.4:
        small(c, 'Trois façons de contrôler', 140, 1110, 20, DARK)
        tools = [('Règles', 'des règles simples', 'code'), ('Classificateur', 'des classificateurs', 'target'),
                 ('Modèle vérificateur', 'un second modèle', 'brain')]
        for k, (s, kw, ic) in enumerate(tools):
            at = S.cue(kw)
            x = 140 + k * 280
            icon(c, t, at, ic, x + 120, 1220, 70, RED)
            text_block(c, t, at + 0.2, s, x + 120, 1330, 28, 'Medium', DARK, RED, maxw=250,
                       align='center', max_lines=2)


def s4(c, t, S):
    header(c, t, S, 'Le compromis', 'Ni trop *strict*, ni trop *laxiste*')
    a = S.cue('Trop strict')
    card(c, t, a, 90, 540, 900, 300, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Trop strict · faux positifs', 140, 600, 20, DARK)
        icon(c, t, a + 0.2, 'user', 180, 720, 70, DARK)
        arrow(c, t, a + 0.4, 240, 720, 380, 720, DARK, 5, 16)
        icon(c, t, a + 0.6, 'shield', 430, 720, 70, RED)
        icon(c, t, S.cue('demandes légitimes'), 'cross', 530, 720, 50, RED)
        lg = S.cue('demandes légitimes')
        if t >= lg:
            reveal_plain(c, t, lg + 0.2, 'Légitime, mais bloquée', 590, 735, 28, RED, 'Medium')
    b = S.cue('Trop laxiste')
    card(c, t, b, 90, 870, 900, 300, LIGHT, 36, 'up')
    if prog(t, b, 0.5) > 0.4:
        small(c, 'Trop laxiste · faux négatifs', 140, 930, 20, DARK)
        icon(c, t, b + 0.2, 'bolt', 180, 1050, 70, RED)
        arrow(c, t, b + 0.4, 240, 1050, 380, 1050, RED, 5, 16)
        icon(c, t, b + 0.6, 'shield', 430, 1050, 70, PL)
        arrow(c, t, b + 0.8, 480, 1050, 560, 1050, RED, 5, 16)
        lp = S.cue('laisse passer')
        if t >= lp:
            reveal_plain(c, t, lp + 0.2, 'Ça passe quand même', 590, 1065, 28, RED, 'Medium')
    ex = S.cue('Par exemple')
    card(c, t, ex, 90, 1200, 900, 230, LIGHT, 36, 'up')
    if prog(t, ex, 0.5) > 0.4:
        cb = S.cue('« carte »')
        chip(c, t, cb, 'Bloquer « carte »', 140, 1240, PL, DARK, 30)
        cm = S.cue('commander une carte')
        arrow(c, t, cm, 470, 1270, 540, 1270, DARK, 5, 16)
        chip(c, t, cm + 0.2, 'Commander une carte', 555, 1240, RED, WHITE, 30)
        if t >= cm:
            reveal_plain(c, t, cm + 0.5, 'Client honnête bloqué', 140, 1385, 28, DARK, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Bloquer *clairement*, mesurer')
    m = S.cue('le message de blocage')
    card(c, t, m, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'Message de blocage', 140, 600, 20, DARK)
        cl = S.cue("n'est pas possible")
        card(c, t, cl, 140, 640, 640, 120, WHITE, 30, 'left')
        if prog(t, cl, 0.5) > 0.4:
            icon(c, t, cl + 0.1, 'chat', 200, 700, 50, DARK)
            reveal_plain(c, t, cl + 0.2, 'Je ne peux pas traiter ce point.', 250, 712, 28, DARK)
        cs = S.cue('un conseiller')
        card(c, t, cs, 140, 790, 640, 110, RED, 30, 'left')
        if prog(t, cs, 0.5) > 0.4:
            icon(c, t, cs + 0.1, 'user', 200, 845, 50, WHITE)
            reveal_plain(c, t, cs + 0.2, 'Parler à un conseiller', 250, 857, 30, WHITE)
    me = S.cue('mesurez les deux types')
    card(c, t, me, 90, 980, 900, 450, LIGHT, 36, 'up')
    if prog(t, me, 0.5) > 0.4:
        small(c, 'Deux erreurs à suivre (illustratif)', 140, 1040, 20, DARK)
        plain(c, 'Bloqué à tort', 140, 1120, 30, DARK)
        bar(c, t, me + 0.3, 140, 1145, 800, 40, 0.35, RED, WHITE, 0.8)
        plain(c, 'Passé à tort', 140, 1250, 30, DARK)
        bar(c, t, me + 0.6, 140, 1275, 800, 40, 0.2, DARK, WHITE, 0.8)
        cc = S.cue('coûte aussi')
        if t >= cc:
            reveal_plain(c, t, cc, 'Bloquer trop coûte aussi', 140, 1390, 30, RED, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Que bloque-t-on *en entrée*, et *en sortie* ?', 'Que faut-il'),
        ("Quel *message* voit l'utilisateur bloqué ?", 'Quel message'),
        ('Comment mesure-t-on les *deux types d\'erreurs* ?', 'Et comment'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Les guardrails contrôlent ce qui *entre* et ce qui *sort*.', 'les guardrails'),
        ('Ni trop stricts, ni trop laxistes : mesurez *les deux erreurs*.', 'Ni trop stricts'),
    ], '50 · Red teaming')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un bon assistant ne repose pas que sur son modèle. "
        "Autour de lui, on place des garde-fous, les guardrails : "
        "des contrôles qui filtrent ce qui entre, et ce qui sort.")),
    dict(kind='content', draw=s2, name='Les contrôles en entrée', text=(
        "En entrée, on vérifie la demande avant qu'elle n'atteigne le modèle. "
        "Un sujet interdit, comme un conseil médical sur un site bancaire. "
        "Une tentative d'injection : un texte qui essaie de détourner les consignes. "
        "Ou des données personnelles, comme un numéro de carte, qu'on masque avant l'envoi.")),
    dict(kind='content', draw=s3, name='Les contrôles en sortie', text=(
        "En sortie, on vérifie la réponse avant de l'afficher : un contenu inapproprié, "
        "une information sensible, un format cassé, ou une réponse hors sujet. "
        "Pour contrôler, trois outils : des règles simples, des classificateurs, "
        "qui trient automatiquement les textes, ou un second modèle qui relit.")),
    dict(kind='content', draw=s4, name='Le compromis', text=(
        "Tout est question de réglage. Trop strict, le filtre bloque des demandes légitimes : ce sont les faux positifs. "
        "Trop laxiste, il laisse passer ce qu'il fallait arrêter : les faux négatifs. "
        "Par exemple, bloquer le mot « carte » empêcherait de commander une carte bancaire.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, soignez le message de blocage : dites clairement ce qui n'est pas possible, "
        "et proposez une autre voie, comme un conseiller. "
        "Et mesurez les deux types d'erreurs, pas seulement ce qui passe : "
        "un filtre qui bloque trop coûte aussi des clients, et de la confiance.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Que faut-il bloquer en entrée, et en sortie ? "
        "Quel message voit l'utilisateur bloqué ? "
        "Et comment mesure-t-on les deux types d'erreurs ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : les guardrails contrôlent ce qui entre et ce qui sort du modèle. "
        "Ni trop stricts, ni trop laxistes : on mesure les deux erreurs. "
        "Prochaine capsule : le red teaming, ou comment attaquer son propre assistant.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
