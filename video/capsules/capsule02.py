from engine import *  # noqa
from engine import _paint  # noqa

NUM = 2
TITLE = 'TOKENS'
FULL_TITLE = 'Tokens et fenêtre de contexte'
SLUG = 'tokens_contexte'
NEXT_CUE = 'prochaine capsule'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un LLM ne lit pas des mots. Il lit des *tokens*.')
    # une phrase qui se découpe en tokens, puis chaque token « coûte »
    phrase = ['Je', ' veux', ' rési', 'lier', ' mon', ' contrat']
    at = S.cue('Il lit')
    x0, y = 90, 1010
    if t < at:
        plain(c, 'Je veux résilier mon contrat', 90, y + 40, 46, WHITE, 'Medium')
    else:
        x = x0
        for i, tok in enumerate(phrase):
            w = chip(c, t, at + i * 0.12, tok.strip(), x, y - 20, PLL, DARK, 40)
            x += w + 14
    pay = S.cue('se paie')
    x = x0
    for i, tok in enumerate(phrase):
        w = chip_width(tok.strip(), 40)
        icon(c, t, pay + i * 0.1, 'coin', x + w / 2, y + 140, 60, RED)
        x += w + 14
    if t >= pay:
        reveal_plain(c, t, pay + 0.7, '6 tokens = 6 unités facturées', 90, y + 260, 34, WHITE, 'Medium')


def s2(c, t, S):
    header(c, t, S, 'Le token', 'Un *morceau* de texte')
    a1 = S.cue('« chat »')
    card(c, t, a1 - 0.2, 90, 520, 900, 470, LIGHT, 36)
    if t >= a1 - 0.1:
        reveal_plain(c, t, a1, 'chat', 140, 620, 44, DARK, 'Medium')
        chip(c, t, a1 + 0.3, 'chat', 560, 572, RED, WHITE, 36)
        small(c, '1 token', 940, 620, 24, DARK, align='right')
    a2 = S.cue('anticonstitutionnellement')
    reveal_plain(c, t, a2, 'anticonstitutionnellement', 140, 740, 44, DARK, 'Medium')
    x = 140
    for i, part in enumerate(['anti', 'constitution', 'nelle', 'ment']):
        w = chip(c, t, a2 + 0.6 + i * 0.15, part, x, 790, PLL, DARK, 36)
        x += w + 12
    if t >= a2 + 1.0:
        small(c, 'Découpage illustratif', 140, 940, 22, DARK)
    # facturation : entrée / sortie
    a3 = S.cue('facturation')
    label(c, t, a3, 'Ce qui est facturé', 90, 1040, PLL, DARK)
    ain, aout, cher = S.cue('envoie'), S.cue('répond'), S.cue('plus cher')
    box(c, t, ain, 90, 1120, 430, 120, 'Entrée', LIGHT, DARK, 38)
    box(c, t, aout, 560, 1120, 430, 120, 'Sortie', LIGHT, DARK, 38)
    for k in range(3):
        icon(c, t, ain + 0.3 + k * 0.1, 'coin', 160 + k * 70, 1320, 50, RED)
    for k in range(5 if t >= cher else 3):
        icon(c, t, (aout + 0.3 + k * 0.1) if k < 3 else cher + (k - 3) * 0.15, 'coin',
             630 + k * 70, 1320, 50, RED)
    if t >= cher:
        reveal_plain(c, t, cher + 0.3, 'souvent plus cher', 560, 1430, 32, RED, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Fenêtre de contexte', 'Une *mémoire* de travail')
    # le cadre de la fenêtre
    fx, fy, fw, fh = 90, 720, 520, 700
    a0 = S.t0 + 0.4
    if t >= a0:
        p = ease(prog(t, a0, 0.6))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(fx, fy + fh * (1 - p), fx + fw, fy + fh), 36, 36),
                    _paint(DARK, 6))
        small(c, 'Fenêtre', fx + fw / 2, fy + fh + 50, 22, DARK, align='center')
    blocks = [('Consigne', 'consigne', PL), ('Historique', 'historique', PLL),
              ('Documents', 'documents', PL), ('Réponse', 'réponse', PLL)]
    bh, gap = 140, 20
    for i, (name, kw, col) in enumerate(blocks):
        at = S.cue(kw)
        y = fy + fh - 24 - (i + 1) * bh - i * gap
        box(c, t, at, fx + 24, y, fw - 48, bh, name, col, DARK, 36, 'Medium', 26, 'up')
    ov = S.cue('dépasse')
    y = fy - 105
    box(c, t, ov, fx + 24, y, fw - 48, 130, 'Le surplus', RED, WHITE, 36, 'Medium', 26, 'up')
    if t >= ov + 0.4:
        icon(c, t, ov + 0.4, 'cross', fx + fw - 70, y + 20, 70, DARK, bg=WHITE)
    # entre deux appels
    a = S.cue('ne se souvient')
    rx = 660
    label(c, t, a, 'Entre deux appels', rx, 620, PLL, DARK, 22)
    box(c, t, a + 0.2, rx, 700, 330, 150, 'Appel 1', LIGHT, DARK, 36)
    box(c, t, a + 0.9, rx, 1000, 330, 150, 'Appel 2', LIGHT, DARK, 36)
    arrow(c, t, a + 0.6, rx + 165, 870, rx + 165, 980, DARK, 6)
    ap = S.cue("l'application")
    box(c, t, ap, rx, 1250, 330, 170, "L'*appli* renvoie l'essentiel", WHITE, DARK, 32)
    if t >= ap:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(rx, 1250, rx + 330, 1420), 30, 30), _paint(RED, 5))


def s4(c, t, S):
    header(c, t, S, 'Pourquoi pas tout ?', 'Trois *limites*')
    rows = [('La fenêtre a une *limite*', 'une limite'),
            ('Chaque token *coûte* et ralentit', 'se paie'),
            ("L'info utile se *noie*", 'noyé')]
    y = 520
    for i, (s, kw) in enumerate(rows):
        h = check_row(c, t, S.cue(kw), 90, y, 900, s, i + 1, 36)
        y += h + 24
    # 100 pages -> 3 paragraphes
    a = S.cue('cent pages')
    card(c, t, a - 0.2, 90, 1000, 900, 450, LIGHT, 36)
    if t >= a:
        for k in range(12):
            col, row = k % 4, k // 4
            px, py = 140 + col * 70, 1060 + row * 100
            at = a + k * 0.05
            p = back(prog(t, at, 0.3))
            if p > 0:
                rrect(c, px, py, 56 * p, 76 * p, 10, WHITE)
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(px, py, px + 56 * p, py + 76 * p), 10, 10),
                            _paint(DARK, 3))
        small(c, '100 pages', 140, 1400, 24, DARK)
    q = S.cue('une seule question')
    arrow(c, t, q, 450, 1210, 590, 1210, DARK, 6)
    icon(c, t, q, 'search', 520, 1140, 60, DARK)
    tp = S.cue('trois paragraphes')
    for k in range(3):
        bar(c, t, tp + k * 0.15, 630, 1100 + k * 80, 310, 44, 1.0, RED, PLL, 0.5)
    if t >= tp:
        small(c, '3 paragraphes utiles', 630, 1400, 24, RED)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Le token, une donnée de *conception*')
    rows = [('Coût par utilisateur', 'coût par utilisateur', 0.75, 'coin'),
            ('Temps de réponse', 'temps de réponse', 0.55, 'clock'),
            ('Mémoire de la conversation', 'longue conversation', 0.9, 'chat')]
    y = 640
    for name, kw, fr, ic in rows:
        at = S.cue(kw)
        card(c, t, at - 0.15, 90, y, 900, 170, LIGHT, 32, 'left')
        if t >= at:
            icon(c, t, at, ic, 170, y + 85, 70, RED)
            reveal_plain(c, t, at, name, 250, y + 70, 36, DARK, 'Medium')
            bar(c, t, at + 0.3, 250, y + 100, 680, 26, fr, RED, PLL)
        y += 200
    y = 1300
    x = 90
    for s, kw in [('Résumer', 'quoi résumer'), ('Oublier', 'quoi oublier'), ('Aller chercher', 'aller chercher')]:
        w = chip(c, t, S.cue(kw), s, x, y, RED, WHITE, 36)
        x += w + 20


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quel *volume* de texte entre et sort à chaque appel ?', 'Quel volume'),
        ("Combien d'appels par jour, pour combien d'*utilisateurs* ?", "Combien d'appels"),
        ('Que fait-on si un document *dépasse* la fenêtre ?', 'Que fait-on'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Le token est l'unité de *coût* et de *limite*.", "l'unité"),
        ('Le contexte est une mémoire de travail, *pas une archive*.', 'La fenêtre'),
    ], '03 · Prompting et system prompt')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle de langage ne lit pas des mots. Il lit des tokens. Et chaque token se paie.")),
    dict(kind='content', draw=s2, name='Le token', text=(
        "Un token, c'est un morceau de texte : un mot court, une syllabe, parfois un signe. "
        "Le mot « chat » tient en un seul token. "
        "Un mot long comme « anticonstitutionnellement » est découpé en plusieurs morceaux. "
        "Les tokens sont aussi l'unité de facturation : on paie ce qu'on envoie au modèle, et ce qu'il répond. "
        "La réponse coûte souvent plus cher.")),
    dict(kind='content', draw=s3, name='La fenêtre de contexte', text=(
        "La fenêtre de contexte, c'est la mémoire de travail du modèle pour un échange. "
        "La consigne, l'historique, les documents et la réponse doivent y tenir ensemble. "
        "Ce qui dépasse est tronqué ou refusé. "
        "Le modèle ne se souvient de rien entre deux appels : l'application lui renvoie, à chaque fois, ce dont il a besoin.")),
    dict(kind='content', draw=s4, name='Pourquoi ne pas tout envoyer', text=(
        "Pourquoi ne pas tout envoyer ? D'abord, même une grande fenêtre a une limite. "
        "Ensuite, chaque token envoyé se paie et rallonge le temps de réponse. "
        "Enfin, noyé dans un long contexte, le modèle peut rater l'information utile. "
        "Imaginez cent pages de contrat pour une seule question : mieux vaut lui donner les trois paragraphes qui comptent.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, le token devient une donnée de conception. "
        "Il pèse sur le coût par utilisateur, le temps de réponse, et ce que l'assistant garde d'une longue conversation. "
        "Il faut choisir quoi résumer, quoi oublier, et quoi aller chercher.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel volume de texte entre et sort à chaque appel ? "
        "Combien d'appels par jour, pour combien d'utilisateurs ? "
        "Que fait-on quand un document dépasse la fenêtre ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le token est l'unité de coût et de limite. "
        "La fenêtre de contexte est une mémoire de travail, pas une archive. "
        "Prochaine capsule : écrire un prompt comme une vraie spécification fonctionnelle.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
