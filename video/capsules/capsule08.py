from engine import *  # noqa
from engine import _paint  # noqa

NUM = 8
TITLE = 'QUEL LEVIER ?'
FULL_TITLE = 'Prompting, RAG ou fine-tuning'
SLUG = 'prompting_rag_finetuning'
NEXT_CUE = 'prochaine capsule'

LEVERS = [('Prompt', 0.35), ('RAG', 0.6), ('Fine-tuning', 1.0)]


def s1(c, t, S):
    opening(c, t, S, CAP, 'Entraîner ? Rarement le *premier* levier.')
    a = S.cue('répond mal')
    box(c, t, a, 90, 900, 900, 120, 'Réponse incorrecte', LIGHT, DARK, 36, 'Medium', 30, 'up')
    icon(c, t, a + 0.4, 'cross', 920, 960, 50, RED)
    e = S.cue('entraîner le modèle')
    rr = S.cue('rarement')
    for k, (s, h) in enumerate(LEVERS):
        x = 90 + k * 310
        at = S.t0 + 0.8 + k * 0.15
        hh = 260 * h
        p = ease(prog(t, at, 0.6))
        if p > 0:
            col = PL
            if k == 2 and t >= e:
                col = RED
            if k == 0 and t >= rr:
                col = WHITE
            rrect(c, x, 1420 - hh * p, 280, hh * p, 28, col)
        if t >= at:
            small(c, f'{k + 1} · {s}', x + 140, 1130, 22, WHITE, align='center')


def s2(c, t, S):
    header(c, t, S, 'Levier 1 · Prompting', 'Changer la *consigne*')
    a = S.cue('Vous changez')
    card(c, t, a, 90, 540, 900, 260, LIGHT, 36, 'up')
    x = 140
    for s, kw in [('Consigne', 'la consigne'), ('Ton', 'le ton'), ('Format', 'le format'), ('Exemples', 'les exemples')]:
        w = chip(c, t, S.cue(kw), s, x, 620, RED, WHITE, 34)
        x += w + 16
    if t >= a + 0.3:
        bar(c, t, a + 0.3, 140, 730, 800, 22, 0.7, PL, WHITE, 0.6)
    rows = [('Rapide', 'rapide', 1.0), ('Peu coûteux', 'peu coûteux', 0.25), ('Réversible', 'réversible', 1.0)]
    for k, (s, kw, fr) in enumerate(rows):
        at = S.cue(kw)
        y = 850 + k * 130
        card(c, t, at, 90, y, 900, 110, LIGHT, 28, 'left')
        if prog(t, at, 0.5) > 0.4:
            plain(c, s, 140, y + 68, 34, DARK)
            if kw == 'réversible':
                icon(c, t, at + 0.2, 'check', 900, y + 55, 50, RED)
            else:
                bar(c, t, at + 0.2, 470, y + 42, 470, 28, fr, RED, WHITE)
    cm = S.cue('commencez')
    chip(c, t, cm, 'Consigne floue ? Commencez ici', 90, 1290, DARK, WHITE, 34)


def s3(c, t, S):
    header(c, t, S, 'Levier 2 · RAG', "Quand il manque d'*information*")
    x = 90
    for s, kw in [('Produits', 'vos produits'), ('Procédures', 'vos procédures'), ('Données changeantes', 'changent souvent')]:
        w = chip(c, t, S.cue(kw), s, x, 560, PLL, DARK, 32)
        x += w + 16
    m = S.cue('ne mémorise rien')
    box(c, t, m, 90, 680, 420, 200, 'Le modèle', LIGHT, DARK, 36)
    if t >= m + 0.3:
        small(c, 'Inchangé', 300, 920, 22, DARK, align='center')
    bp = S.cue('les bons passages')
    card(c, t, bp, 570, 680, 420, 200, WHITE, 30)
    if t >= bp + 0.2:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(570, 680, 990, 880), 30, 30), _paint(RED, 4))
        for j in range(3):
            bar(c, t, bp + 0.2 + j * 0.1, 610, 720 + j * 50, 340, 22, 0.9 - j * 0.2, RED, PLL, 0.3)
        small(c, 'À chaque question', 780, 920, 22, RED, align='center')
    arrow(c, t, bp + 0.3, 560, 780, 520, 780, RED, 6, 18)
    md = S.cue('Mettre à jour un document')
    card(c, t, md, 90, 990, 900, 420, LIGHT, 36, 'up')
    if prog(t, md, 0.5) > 0.4:
        box(c, t, md + 0.2, 140, 1060, 330, 150, 'Document v1', WHITE, DARK, 32)
        arrow(c, t, md + 0.5, 480, 1135, 590, 1135, DARK, 6)
        box(c, t, md + 0.7, 610, 1060, 330, 150, 'Document v2', RED, WHITE, 32)
        rp = S.cue('mettre à jour la réponse')
        chip(c, t, rp, 'Réponse à jour, sans réentraîner', 140, 1270, WHITE, DARK, 32)


def s4(c, t, S):
    header(c, t, S, 'Levier 3 · Fine-tuning', 'Réentraîner sur des *exemples*')
    a = S.cue('des centaines')
    card(c, t, a - 0.2, 90, 540, 470, 360, LIGHT, 32)
    for k in range(48):
        col, row = k % 8, k // 8
        at = a + k * 0.02
        p = back(prog(t, at, 0.3))
        if p > 0:
            rrect(c, 125 + col * 52, 575 + row * 52, 38 * p, 38 * p, 9, PL)
    if t >= a:
        small(c, "Exemples d'entraînement", 325, 940, 22, DARK, align='center')
    arrow(c, t, a + 0.8, 575, 720, 655, 720, DARK, 6)
    st = S.cue('un style')
    card(c, t, st, 670, 540, 320, 360, RED, 32)
    if prog(t, st, 0.5) > 0.4:
        icon(c, t, st + 0.1, 'gear', 830, 680, 90, WHITE)
        plain(c, 'Modèle', 830, 810, 32, WHITE, 'Medium', 'center')
        plain(c, 'ajusté', 830, 850, 32, WHITE, 'Medium', 'center')
    costs = [('Plus long', 'plus long'), ('Des données de qualité', 'données de qualité'),
             ('Réentraîner à chaque mise à jour', 'nouvel entraînement')]
    for k, (s, kw) in enumerate(costs):
        at = S.cue(kw)
        box(c, t, at, 90, 990 + k * 110, 900, 90, s, LIGHT, DARK, 32, 'Medium', 26, 'left')
    fc = S.cue('des faits qui changent')
    w = chip(c, t, fc, 'Pas pour des faits qui changent', 90, 1340, DARK, WHITE, 32)
    icon(c, t, fc + 0.3, 'cross', 90 + w + 50, 1368, 50, RED)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Une règle *simple*')
    rows = [('Comportement', 'Prompt', 'de comportement'), ('Connaissance', 'RAG', 'de connaissance'),
            ('Style constant, à grande échelle', 'Fine-tuning', 'le fine-tuning se discute')]
    for k, (pb, lv, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 200
        box(c, t, at, 90, y, 520, 170, pb, LIGHT, DARK, 34, 'Medium', 30, 'left')
        arrow(c, t, at + 0.3, 620, y + 85, 690, y + 85, DARK, 6)
        box(c, t, at + 0.4, 700, y, 290, 170, lv, RED, WHITE, 36, 'Medium', 30)
    cb = S.cue('on combine')
    chip(c, t, cb, 'Souvent : les trois combinés', 90, 1220, DARK, WHITE, 36)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Le problème vient-il de la *consigne* ou de l'*information* ?", 'Le problème vient'),
        ('Les données *changent*-elles souvent ?', 'Les données'),
        ("A-t-on assez d'*exemples de qualité* pour entraîner ?", 'Dispose-t-on'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("D'abord le *prompt*, ensuite le *RAG*.", "d'abord le prompt"),
        ('Le *fine-tuning* en dernier recours, avec des données.', 'le fine-tuning en dernier'),
    ], '09 · Sécurité et conformité')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Quand un assistant répond mal, le réflexe est souvent de vouloir entraîner le modèle. "
        "C'est pourtant rarement le premier levier à actionner.")),
    dict(kind='content', draw=s2, name='Levier un : le prompting', text=(
        "Premier levier : le prompting. Vous changez la consigne, le ton, le format, les exemples. "
        "C'est rapide, peu coûteux, et réversible en quelques minutes. "
        "Si le problème vient d'une consigne floue ou d'un format mal respecté, commencez toujours par là.")),
    dict(kind='content', draw=s3, name='Levier deux : le RAG', text=(
        "Deuxième levier : le RAG. Il sert quand le modèle manque d'information : vos produits, vos procédures, "
        "des données qui changent souvent. Le modèle ne mémorise rien de nouveau : on lui fournit les bons passages à chaque question. "
        "Mettre à jour un document suffit pour mettre à jour la réponse.")),
    dict(kind='content', draw=s4, name='Levier trois : le fine-tuning', text=(
        "Troisième levier : le fine-tuning. On réentraîne un modèle sur des centaines ou des milliers d'exemples, "
        "pour lui apprendre un style, un format ou une tâche très répétitive. "
        "C'est plus long, il faut des données de qualité, et chaque mise à jour demande un nouvel entraînement. "
        "Ce n'est pas le bon outil pour lui apprendre des faits qui changent.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, retenez une règle simple. Un problème de comportement ? Le prompt. "
        "Un problème de connaissance ? Le RAG. "
        "Un style très constant, à grande échelle, que le prompt ne suffit pas à obtenir ? Là, le fine-tuning se discute. "
        "Et souvent, on combine les trois.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Le problème vient-il de la consigne, ou de l'information ? "
        "Les données changent-elles souvent ? "
        "Dispose-t-on d'exemples de qualité, en nombre suffisant, pour entraîner ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : d'abord le prompt, ensuite le RAG, "
        "et le fine-tuning en dernier recours, quand on a les données pour le faire. "
        "Prochaine capsule : la sécurité et la conformité, de la prompt injection à l'AI Act.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
