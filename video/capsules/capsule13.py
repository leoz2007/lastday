from engine import *  # noqa
from engine import _paint  # noqa

NUM = 13
TITLE = 'RAISONNEMENT'
FULL_TITLE = 'Les modèles qui raisonnent'
SLUG = 'modeles_raisonnement'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def think_dots(c, t, at, x, y, n, color, step=46, r=12, dur=0.12):
    """Une rangée de points qui apparaissent l'un après l'autre (la réflexion)."""
    for k in range(n):
        dot(c, t, at + k * dur, x + k * step, y, r, color)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Certains modèles *réfléchissent* avant de répondre.')
    rows = [('Problème difficile', 'problème difficile', 'check', RED),
            ('Question simple', 'question simple', 'clock', PL)]
    for k, (s, kw, ic, col) in enumerate(rows):
        at = S.cue(kw)
        y = 900 + k * 270
        card(c, t, at, 90, y, 900, 220, WHITE if k == 0 else LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, s, 140, y + 60, 24, DARK)
            icon(c, t, at + 0.1, 'brain', 175, y + 140, 60, DARK)
            think_dots(c, t, at + 0.2, 260, y + 140, 12, col, dur=0.06)
            icon(c, t, at + 1.0, ic, 900, y + 140, 60, RED if k == 0 else DARK)
        if t >= at + 1.1:
            reveal_plain(c, t, at + 1.1, 'Ça change tout' if k == 0 else 'Du temps perdu',
                         940, y + 60, 26, RED if k == 0 else DARK, 'Medium', 'right')


def s2(c, t, S):
    header(c, t, S, 'Le principe', "D'abord *réfléchir*, puis répondre")
    a = S.cue("produit d'abord")
    box(c, t, S.t0 + 0.4, 90, 540, 900, 110, 'Question', LIGHT, DARK, 36)
    arrow(c, t, a - 0.1, 540, 660, 540, 720, DARK, 6)
    card(c, t, a, 90, 730, 900, 330, PLL, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Raisonnement', 140, 790, 22, DARK)
        steps = [('Décomposer', 'décompose'), ('Essayer', 'essaie'), ('Vérifier', 'vérifie'), ('Corriger', 'corrige')]
        for k, (s, kw) in enumerate(steps):
            at = S.cue(kw)
            x = 140 + (k % 2) * 410
            y = 830 + (k // 2) * 105
            chip(c, t, at, f'{k + 1}. {s}', x, y, WHITE, DARK, 32)
    r = S.cue('réponse finale')
    arrow(c, t, r - 0.1, 540, 1070, 540, 1130, DARK, 6)
    box(c, t, r, 90, 1140, 900, 110, 'Réponse finale', RED, WHITE, 36)
    v = S.cue('affiché')
    x = 90
    for s, kw in [('Affiché', 'affiché'), ('Résumé', 'résumé'), ('Masqué', 'masqué')]:
        w = chip(c, t, S.cue(kw), s, x, 1300, DARK, WHITE, 32)
        x += w + 16
    if t >= v:
        small(c, 'Selon le fournisseur', 990, 1345, 20, DARK, align='right')


def s3(c, t, S):
    header(c, t, S, 'Le gain', 'Les problèmes à *étapes*')
    x = 90
    for s, kw in [('Calcul', 'un calcul'), ('Logique', 'analyse logique'), ('Code', 'du code'),
                  ('Planning', 'un planning')]:
        w = chip(c, t, S.cue(kw), s, x, 540, PLL, DARK, 32)
        x += w + 16
    ex = S.cue('dix règles')
    card(c, t, ex, 90, 660, 900, 230, LIGHT, 32, 'up')
    if prog(t, ex, 0.5) > 0.4:
        icon(c, t, ex + 0.1, 'doc', 170, 775, 80, DARK)
        reveal_plain(c, t, ex + 0.2, 'Contrat : 10 règles à vérifier,', 250, 760, 32, DARK)
        reveal_plain(c, t, ex + 0.35, 'certaines dépendent des autres', 250, 810, 32, DARK)
    rows = [('Sans réflexion', 'Sans réflexion', [1, 1, 0, 1, 0, 0, 1, 0, 1, 0]),
            ('Avec réflexion', 'Avec, il', [1] * 10)]
    for k, (nm, kw, vals) in enumerate(rows):
        at = S.cue(kw)
        y = 950 + k * 230
        card(c, t, at, 90, y, 900, 200, WHITE if k else LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            if k:
                outline(c, 90, y, 900, 200, 32, RED)
            small(c, nm, 140, y + 55, 22, RED if k else DARK)
            for j, ok in enumerate(vals):
                cx = 165 + j * 83
                dot(c, t, at + 0.2 + j * 0.08, cx, y + 125, 30, RED if ok else PL)
                icon(c, t, at + 0.3 + j * 0.08, 'check' if ok else 'cross', cx, y + 125, 34,
                     WHITE if ok else DARK)


def s4(c, t, S):
    header(c, t, S, 'Le prix', 'Réfléchir *coûte*')
    a = S.cue('bien plus de tokens')
    card(c, t, a, 90, 540, 900, 330, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Tokens générés · exemple illustratif', 140, 600, 22, DARK)
        small(c, 'Réflexion', 140, 670, 22, DARK)
        bar(c, t, a + 0.2, 140, 690, 800, 40, 1.0, PL, WHITE, 1.0)
        small(c, 'Réponse', 140, 780, 22, DARK)
        bar(c, t, a + 0.6, 140, 800, 800, 40, 0.18, RED, WHITE, 0.5)
    p = S.cue('se paient')
    if t >= p:
        for k in range(6):
            icon(c, t, p + k * 0.08, 'coin', 150 + k * 62, 930, 50, RED)
        reveal_plain(c, t, p + 0.5, 'Chaque token se paie', 540, 945, 32, DARK)
    w = S.cue("l'attente")
    card(c, t, w, 90, 1010, 900, 170, LIGHT, 32, 'left')
    if prog(t, w, 0.5) > 0.4:
        icon(c, t, w + 0.1, 'clock', 170, 1095, 60, DARK)
        u = clamp((t - w - 0.3) / 2.5)
        rrect(c, 240, 1080, 700, 30, 15, WHITE)
        rrect(c, 240, 1080, max(30, 700 * u), 30, 15, RED)
        small(c, 'Attente avant la réponse', 240, 1150, 20, DARK)
    e = S.cue('régler cet effort')
    if t >= e:
        small(c, "Niveau d'effort", 90, 1240, 22, DARK)
    x = 90
    lv = [('Faible', PLL, DARK), ('Moyen', PL, DARK), ('Élevé', RED, WHITE)]
    for k, (s, bg, fg) in enumerate(lv):
        wd = chip(c, t, e + 0.2 + k * 0.2, s, x, 1270, bg, fg, 34)
        x += wd + 16
    b = S.cue('budget de réflexion')
    chip(c, t, b, 'Budget max', x + 30, 1270, DARK, WHITE, 34)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "Doser l'*effort*")
    rows = [('Classer un email', 'classer un email', 'Faible', PLL, DARK),
            ('Reformuler une phrase', 'reformuler', 'Faible', PLL, DARK),
            ('Analyser un contrat', 'par type de demande', 'Élevé', RED, WHITE)]
    for k, (s, kw, lv, bg, fg) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 140
        box(c, t, at, 90, y, 600, 115, s, LIGHT, DARK, 32, 'Medium', 28, 'left')
        arrow(c, t, at + 0.2, 700, y + 57, 750, y + 57, DARK, 5, 16)
        box(c, t, at + 0.3, 770, y, 220, 115, lv, bg, fg, 32, 'Medium', 28)
    ev = S.cue('vos evals')
    card(c, t, ev, 90, 1010, 900, 400, LIGHT, 36, 'up')
    if prog(t, ev, 0.5) > 0.4:
        label(c, t, ev + 0.1, 'Evals · chiffres illustratifs', 140, 1045, PLL, DARK, 22)
        small(c, 'Effort faible', 520, 1145, 20, DARK)
        small(c, 'Effort élevé', 760, 1145, 20, RED)
        crit = [('Qualité', 'qualité', 0.8, 0.88), ('Coût', 'coût', 0.25, 0.8), ('Délai', 'délai', 0.2, 0.75)]
        for j, (nm, kw, f1, f2) in enumerate(crit):
            at = S.cue('comparent') + j * 0.35
            y = 1185 + j * 70
            if t >= at:
                plain(c, nm, 140, y + 26, 30, DARK)
            bar(c, t, at, 520, y + 4, 210, 28, f1, PL, WHITE, 0.6)
            bar(c, t, at + 0.15, 760, y + 4, 210, 28, f2, RED, WHITE, 0.6)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('La tâche demande-t-elle *plusieurs étapes* ?', 'La tâche demande'),
        ("Quel *délai* l'utilisateur peut-il accepter ?", 'Quel délai'),
        ('Le *gain de qualité* justifie-t-il le coût ?', 'le gain de qualité'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un modèle qui raisonne écrit sa *réflexion* avant de répondre.', 'un modèle qui raisonne'),
        ('Plus fiable sur le complexe, mais plus *lent* et plus *cher*.', 'Plus fiable'),
    ], '14 · Multimodal')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Certains modèles prennent le temps de réfléchir avant de répondre. "
        "Sur un problème difficile, ça change tout. Sur une question simple, c'est du temps perdu.")),
    dict(kind='content', draw=s2, name='Réfléchir avant de répondre', text=(
        "Un modèle de raisonnement produit d'abord une réflexion : il décompose le problème, "
        "il essaie une piste, il vérifie, il corrige. Puis il écrit sa réponse finale. "
        "Cette réflexion, ce sont des tokens générés comme les autres. "
        "Selon le fournisseur, elle est affichée, résumée ou masquée.")),
    dict(kind='content', draw=s3, name='Ce que ça apporte', text=(
        "Le gain se voit sur les problèmes à plusieurs étapes : un calcul, une analyse logique, du code, un planning sous contraintes. "
        "Exemple : vérifier qu'un contrat respecte dix règles, dont certaines dépendent des autres. "
        "Sans réflexion, le modèle risque de sauter des étapes. Avec, il les enchaîne et se relit.")),
    dict(kind='content', draw=s4, name='Le coût de la réflexion', text=(
        "Mais réfléchir coûte. La réflexion peut demander bien plus de tokens que la réponse elle-même, "
        "et ces tokens se paient. Elle rallonge aussi l'attente, parfois de plusieurs secondes, ou bien plus. "
        "Beaucoup de modèles permettent de régler cet effort, ou de fixer un budget de réflexion.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, réservez la réflexion aux tâches qui la méritent. "
        "Pour classer un email ou reformuler une phrase, elle n'apporte presque rien. "
        "La bonne approche : un niveau d'effort par type de demande, validé par vos evals, "
        "qui comparent qualité, coût et délai.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. La tâche demande-t-elle plusieurs étapes de raisonnement ? "
        "Quel délai l'utilisateur peut-il accepter ? "
        "Et le gain de qualité, mesuré sur vos evals, justifie-t-il le coût ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un modèle qui raisonne écrit sa réflexion avant de répondre. "
        "Plus fiable sur les problèmes complexes, mais plus lent et plus cher. "
        "Prochaine capsule : les modèles multimodaux, qui lisent aussi les images, les documents et la voix.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
