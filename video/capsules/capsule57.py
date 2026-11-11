from engine import *  # noqa
from engine import _paint  # noqa

NUM = 57
TITLE = 'HARNESS, AGENT DE CODE'
FULL_TITLE = "Le harness, l'agent de code"
SLUG = 'harness_agent_code'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'

HARNESSES = ['Claude Code', 'OpenCode', 'Cline', 'Roo', 'Kilo', 'Continue', 'Aider']


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def terminal(c, t, at, x, y, w, h):
    """Fenêtre de terminal : fond sombre, invite et lignes de commande."""
    p = card(c, t, at, x, y, w, h, DARK, 24, 'pop')
    if p > 0.6:
        for k in range(3):
            c.drawCircle(x + 30 + k * 26, y + 28, 7, _paint(PL))
        for k, lw in enumerate([0.7, 0.5, 0.8]):
            yy = y + 80 + k * 50
            plain(c, '>', x + 30, yy + 20, 28, RED, 'Bold')
            rrect(c, x + 60, yy, (w - 100) * lw * ease(prog(t, at + 0.3 + k * 0.2, 0.4)) + 1, 18, 9, WHITE)
    return p


def editor(c, t, at, x, y, w, h):
    """Fenêtre d'éditeur : arborescence, code, panneau de conversation."""
    p = card(c, t, at, x, y, w, h, WHITE, 24, 'pop')
    if p > 0.6:
        outline(c, x, y, w, h, 24, DARK, 4)
        rrect(c, x + 16, y + 20, 70, h - 40, 12, LIGHT)
        for k, lw in enumerate([0.9, 0.6, 0.75, 0.5]):
            rrect(c, x + 100, y + 30 + k * 40, (w - 260) * lw * ease(prog(t, at + 0.3 + k * 0.15, 0.4)) + 1,
                  16, 8, PL)
        rrect(c, x + w - 140, y + 20, 124, h - 40, 12, PLL)
        icon(c, t, at + 0.5, 'chat', x + w - 78, y + h / 2, 50, DARK)
    return p


def s1(c, t, S):
    opening(c, t, S, CAP, "Le modèle a besoin d'*un harnais*.")
    h = S.cue('le harness')
    cx, cy = 540, 1080
    if t >= h:
        r = 220 * ease(prog(t, h, 0.6))
        c.drawCircle(cx, cy, r, _paint(WHITE, 10))
    card(c, t, S.cue('Le modèle seul'), cx - 90, cy - 90, 180, 180, RED, 90, 'pop')
    icon(c, t, S.cue('Le modèle seul') + 0.1, 'brain', cx, cy, 90, WHITE)
    acts = [('Lire', 'lit les fichiers', 'doc', 220, 880), ('Commander', 'lance les commandes', 'code', 860, 880),
            ('Éditer', 'applique les éditions', 'gear', 540, 1380)]
    for s, kw, ic, x, y in acts:
        at = S.cue(kw)
        w = chip_width(s, 30)
        chip(c, t, at, s, x - w / 2, y - 26, WHITE, DARK, 30)
    dv = S.cue('chaque matin')
    if t >= dv:
        icon(c, t, dv, 'user', 860, 1330, 50, WHITE)


def s2(c, t, S):
    header(c, t, S, 'Deux formats', 'Ligne de commande ou *éditeur*')
    v = S.cue('la voiture')
    if t >= v:
        reveal_plain(c, t, v, 'Le modèle est le moteur, le harness la voiture', 90, 570, 30, DARK, 'Medium')
    cl = S.cue('la CLI')
    terminal(c, t, cl, 90, 620, 430, 300)
    if t >= cl + 0.3:
        label(c, t, cl + 0.3, 'CLI · terminal', 90, 940, PLL, DARK, 22)
    ide = S.cue("l'IDE")
    editor(c, t, ide, 560, 620, 430, 300)
    if t >= ide + 0.3:
        label(c, t, ide + 0.3, 'IDE · éditeur', 560, 940, PLL, DARK, 22)
    e = S.cue('Exemples à date')
    card(c, t, e, 90, 1050, 900, 370, LIGHT, 36, 'up')
    if prog(t, e, 0.5) > 0.4:
        small(c, 'Exemples à date', 140, 1110, 20, DARK)
        items = [(s, e + 0.2 + k * 0.1, RED if k == 0 else WHITE, WHITE if k == 0 else DARK)
                 for k, s in enumerate(HARNESSES)]
        flow_chips(c, t, items, 140, 1140, 800, 30, 16)
        ev = S.cue('évolue vite')
        if t >= ev:
            icon(c, t, ev, 'clock', 160, 1375, 36, DARK)
            reveal_plain(c, t, ev, 'Le paysage évolue vite', 195, 1386, 28, DARK, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Compatibilité', 'Se brancher sur *votre modèle*')
    a = S.cue("point d'accès")
    box(c, t, a - 0.3, 90, 560, 250, 150, 'Harness', DARK, WHITE, 34)
    arrow(c, t, a, 350, 635, 420, 635, DARK, 6, 18)
    card(c, t, a + 0.2, 430, 540, 300, 190, LIGHT, 30, 'pop')
    if prog(t, a + 0.2, 0.5) > 0.4:
        small(c, 'Endpoint interne', 580, 595, 18, DARK, align='center')
        f = S.cue('format')
        chip(c, t, f + 0.3, 'Format OpenAI', 580 - chip_width('Format OpenAI', 24) / 2, 615, WHITE, DARK, 24)
        chip(c, t, f + 0.6, 'Format Anthropic', 580 - chip_width('Format Anthropic', 24) / 2, 672, WHITE, DARK, 24)
    m = S.cue('votre modèle interne')
    arrow(c, t, m, 740, 635, 810, 635, DARK, 6, 18)
    card(c, t, m + 0.1, 820, 560, 170, 150, RED, 30, 'pop')
    icon(c, t, m + 0.2, 'brain', 905, 635, 70, WHITE)
    ap = S.cue("L'API")
    if t >= ap:
        reveal_plain(c, t, ap, "API : l'interface entre deux logiciels", 90, 800, 30, DARK, 'Medium')
    cc = S.cue("n'a pas été conçu")
    card(c, t, cc, 90, 860, 900, 540, LIGHT, 36, 'up')
    if prog(t, cc, 0.5) > 0.4:
        small(c, 'Même harness, autre modèle · exemple', 140, 920, 20, DARK)
        rows = [('Modèle prévu', 'check', RED, 'Consignes suivies'), ('Autre modèle', 'cross', DARK, 'Consignes mal suivies')]
        for k, (s, ic, col, res) in enumerate(rows):
            at = cc + 0.3 + k * 0.6 if k == 0 else S.cue('mal passer')
            y = 970 + k * 200
            card(c, t, at, 140, y, 800, 170, WHITE, 28, 'left')
            if prog(t, at, 0.5) > 0.4:
                icon(c, t, at + 0.1, 'brain', 210, y + 85, 56, PL if k else DARK)
                plain(c, s, 270, y + 75, 30, DARK, 'Medium')
                small(c, res, 270, y + 120, 18, RED if k else DARK)
                icon(c, t, at + 0.3, ic, 880, y + 85, 50, RED if k else DARK)


def s4(c, t, S):
    header(c, t, S, 'Configuration', 'Centraliser les *règles*')
    a = S.cue('centralisez la configuration')
    box(c, t, a, 340, 540, 400, 120, 'Configuration centrale', RED, WHITE, 30)
    for k in range(3):
        x = 200 + k * 340
        arrow(c, t, a + 0.3 + k * 0.1, 540, 670, x, 740, DARK, 5, 16)
        icon(c, t, a + 0.5 + k * 0.1, 'code', x, 790, 60, DARK)
    if t >= a + 0.8:
        small(c, 'Tous les postes', 540, 870, 18, DARK, align='center')
    rows = [('gear', 'Réglages gérés', 'réglages gérés'), ('lock', 'Permissions', 'Des permissions'),
            ('check', 'Outils autorisés', "outils autorisés"), ('doc', 'Fichiers de règles', 'fichiers de règles')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 910 + k * 125
        card(c, t, at, 90, y, 900, 105, LIGHT, 28, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 160, y + 52, 46, RED if k == 3 else DARK)
            reveal_plain(c, t, at + 0.15, s, 220, y + 64, 32, DARK, 'Medium')
            if k == 3:
                x = 590
                for j, f in enumerate(['CLAUDE.md', 'AGENTS.md']):
                    w = chip(c, t, at + 0.4 + j * 0.15, f, x, y + 28, WHITE, DARK, 26)
                    x += w + 14
    lv = S.cue("livret d'accueil")
    if t >= lv:
        icon(c, t, lv, 'user', 130, 1440 - 30, 40, DARK)
        reveal_plain(c, t, lv + 0.1, "Le livret d'accueil de chaque nouvel arrivant", 170, 1420, 28, DARK, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Des *skills* versionnées')
    sk = S.cue('Une skill')
    card(c, t, sk, 90, 540, 900, 260, LIGHT, 36, 'up')
    if prog(t, sk, 0.5) > 0.4:
        label(c, t, sk + 0.1, 'Skill', 140, 575, RED, WHITE, 22)
        mg = S.cue('migration de base de données')
        icon(c, t, mg, 'db', 190, 710, 60, DARK)
        if t >= mg:
            reveal_plain(c, t, mg, 'Écrire une migration, à la façon maison', 250, 722, 32, DARK, 'Medium')
    v = S.cue('Versionnez')
    card(c, t, v, 90, 830, 900, 230, LIGHT, 36, 'up')
    if prog(t, v, 0.5) > 0.4:
        small(c, 'Versions', 140, 890, 20, DARK)
        bar(c, t, v + 0.1, 170, 955, 740, 10, 1.0, PL, LIGHT, 0.6)
        for k, s in enumerate(['v1.0', 'v1.1', 'v1.2']):
            x = 200 + k * 330
            at = v + 0.3 + k * 0.25
            dot(c, t, at, x, 960, 20, RED if k == 2 else DARK)
            if t >= at:
                plain(c, s, x, 1020, 28, RED if k == 2 else DARK, 'Medium', 'center')
    d = S.cue('distribuez-les')
    card(c, t, d, 90, 1090, 900, 320, LIGHT, 36, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Toutes les équipes', 140, 1150, 20, DARK)
        for k, s in enumerate(['Équipe A', 'Équipe B', 'Équipe C', 'Équipe D']):
            x = 140 + k * 205
            at = d + 0.2 + k * 0.12
            box(c, t, at, x, 1185, 185, 90, s, WHITE, DARK, 26)
            icon(c, t, S.cue('mêmes bonnes pratiques') + k * 0.1, 'check', x + 92, 1335, 40, RED)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Le harness se branche-t-il sur votre *point d'accès* ?", 'Le harness se branche'),
        ('Qui gère les *réglages* et les *permissions* ?', 'Qui gère'),
        ('Comment vos *skills* sont-elles versionnées et distribuées ?', 'Et comment'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Le harness fait tourner l'agent *autour du modèle*.", 'le harness fait tourner'),
        ('Branchez, *centralisez*, distribuez vos *conventions*.', 'Vérifiez'),
    ], '58 · Le LLM hub')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Le modèle seul ne touche à rien. Autour de lui, le harness fait tourner l'agent : "
        "il lit les fichiers, lance les commandes, applique les éditions. "
        "C'est l'outil que vos développeurs ouvrent chaque matin.")),
    dict(kind='content', draw=s2, name='Deux formats : CLI ou IDE', text=(
        "Le harness, c'est la voiture autour du moteur. Il existe en deux formats. "
        "En ligne de commande, la CLI, dans le terminal. Ou dans l'éditeur de code, l'IDE. "
        "Exemples à date : Claude Code, et d'autres à l'écran. Le paysage évolue vite.")),
    dict(kind='content', draw=s3, name="Compatibilité avec votre point d'accès", text=(
        "Vérifiez d'abord la compatibilité. Le harness doit accepter un point d'accès personnalisé, "
        "un endpoint, au format d'API d'OpenAI ou d'Anthropic. "
        "L'API, c'est l'interface entre logiciels : ce format le branche sur votre modèle interne. "
        "Testez-le aussi avec des modèles pour lesquels il n'a pas été conçu : ses consignes peuvent mal passer.")),
    dict(kind='content', draw=s4, name='Une configuration centralisée', text=(
        "Ensuite, centralisez la configuration. Des réglages gérés, imposés à tous les postes. "
        "Des permissions : ce que l'agent fait sans demander. Une liste d'outils autorisés. "
        "Et des fichiers de règles dans chaque dépôt, qui donnent les conventions du projet. "
        "Comme le livret d'accueil remis à chaque nouvel arrivant.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, traitez vos conventions comme du code. Une skill, c'est un savoir-faire packagé "
        "pour l'agent : par exemple, la façon maison d'écrire une migration de base de données. "
        "Versionnez ces skills, puis distribuez-les à toutes les équipes. "
        "Chacune applique alors les mêmes bonnes pratiques.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Le harness se branche-t-il sur votre point d'accès interne ? "
        "Qui gère les réglages et les permissions ? "
        "Et comment vos skills sont-elles versionnées et distribuées ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le harness fait tourner l'agent autour du modèle. "
        "Vérifiez qu'il se branche sur votre point d'accès, centralisez sa configuration, "
        "et distribuez vos conventions à toutes les équipes. "
        "Prochaine capsule : le LLM hub, la porte d'entrée commune vers vos grands modèles de langage.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
