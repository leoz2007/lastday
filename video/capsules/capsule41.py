from engine import *  # noqa
from engine import _paint  # noqa

NUM = 41
TITLE = 'CONTEXT ENGINEERING'
FULL_TITLE = 'Context engineering'
SLUG = 'context_engineering'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'

LAYERS = [('Instructions', 'Les instructions'), ('Outils', 'la description des outils'),
          ('Mémoire et historique', 'la mémoire'), ('Documents récupérés', 'les documents récupérés'),
          ('Exemples', 'quelques exemples'), ('État de la tâche', "l'état de la tâche")]


def s1(c, t, S):
    opening(c, t, S, CAP, 'Votre prompt n\'est qu\'*une partie* du contexte.')
    fw = S.cue('fenêtre de contexte')
    card(c, t, fw, 290, 830, 500, 480, WHITE, 32, 'up')
    pp = S.cue('petite partie')
    if prog(t, fw, 0.5) > 0.4:
        small(c, 'Fenêtre de contexte', 540, 885, 20, DARK, align='center')
        cols = [PLL, PL, PLL, PL]
        for k, col in enumerate(cols):
            at = fw + 0.3 + k * 0.15
            if t >= at:
                p = ease(prog(t, at, 0.4))
                rrect(c, 330, 920 + k * 76, 420 * p, 60, 20, col)
    # le prompt, petit bloc rouge
    a = S.t0 + 0.8
    if t >= a:
        p = ease(prog(t, a, 0.4))
        y = lerp(1060, 1225, ease(prog(t, fw, 0.5)))
        rrect(c, 330, y, 200 * p, 60, 20, RED)
        if p > 0.6:
            plain(c, 'Prompt', 430, y + 40, 26, WHITE, 'Medium', 'center')
    if t >= pp:
        reveal_plain(c, t, pp, 'Une petite partie', 550, 1265, 26, RED, 'Medium')
    ce = S.cue('context engineering')
    if t >= ce:
        chip(c, t, ce, 'Ingénierie du contexte', 540, 1350, RED, WHITE, 30, align='center')


def s2(c, t, S):
    header(c, t, S, 'La fenêtre', 'Ce qui *entre* à chaque appel')
    ex = {0: ('Remboursements', 'la politique de remboursement'), 1: ('Commandes', "l'outil de commande"),
          3: ('Dossier client', 'le dossier du client')}
    for k, (s, kw) in enumerate(LAYERS):
        at = S.cue(kw)
        y = 550 + k * 120
        box(c, t, at, 90, y, 540, 100, s, RED if k == 5 else LIGHT, WHITE if k == 5 else DARK, 30, mode='left')
        if k in ex:
            nm, ekw = ex[k]
            ea = S.cue(ekw)
            arrow(c, t, ea, 640, y + 50, 690, y + 50, DARK, 5, 14)
            chip(c, t, ea + 0.2, nm, 700, y + 24, PLL, DARK, 28)
    sc = S.cue('service client')
    if t >= sc:
        small(c, 'Exemple : service client', 700, 1300, 20, DARK)


def window(c, t, at, x, y, w, h, fill, n, overflow=False):
    """Fenêtre de contexte : cadre et n blocs empilés depuis le bas."""
    card(c, t, at, x, y, w, h, WHITE, 24, 'pop')
    if prog(t, at, 0.5) < 0.4:
        return
    for k in range(n):
        a = at + 0.2 + k * 0.08
        if t < a:
            continue
        p = ease(prog(t, a, 0.3))
        by = y + h - 20 - (k + 1) * 34
        if by < y + 10 and not overflow:
            break
        rrect(c, x + 20, by, (w - 40) * p, 26, 13, fill if by >= y + 10 else RED)


def s3(c, t, S):
    header(c, t, S, 'Le dosage', 'Ni *trop peu*, ni *trop*')
    tp = S.cue('Trop peu de contexte')
    card(c, t, tp, 90, 540, 440, 540, LIGHT, 32, 'up')
    if prog(t, tp, 0.5) > 0.4:
        small(c, 'Trop peu', 130, 600, 22, DARK)
        window(c, t, tp + 0.2, 150, 680, 320, 240, PL, 1)
        dv = S.cue('le modèle devine')
        if t >= dv:
            plain(c, '?', 310, 830, 90, RED, 'Medium', 'center')
        de = S.cue('délai de livraison')
        if t >= de:
            text_block(c, t, de, 'Il invente un *délai*', 130, 970, 30, 'Medium', DARK, RED,
                       maxw=360, max_lines=2)
    tr = S.cue('Trop de contexte')
    card(c, t, tr, 550, 540, 440, 540, LIGHT, 32, 'up')
    if prog(t, tr, 0.5) > 0.4:
        small(c, 'Trop', 590, 600, 22, DARK)
        window(c, t, tr + 0.2, 610, 680, 320, 240, PL, 8, overflow=True)
        pm = S.cue('perdue au milieu')
        if t >= pm:
            dot(c, t, pm, 770, 900 - 4 * 34 + 13, 16, DARK)
        ch = S.cue('coûte plus cher')
        if t >= ch:
            icon(c, t, ch, 'coin', 640, 970, 44, RED)
            reveal_plain(c, t, ch + 0.1, 'Plus cher', 680, 982, 30, RED, 'Medium')
    acts = [('Ordonner', 'ordonner'), ('Résumer', 'résumer'), ('Élaguer', 'élaguer')]
    fd = S.cue('Il faut donc')
    for k, (s, kw) in enumerate(acts):
        at = fd + 0.3 + k * 0.4
        box(c, t, at, 90 + k * 310, 1140, 280, 120, s, RED, WHITE, 34)


def column(c, t, at, x, base, blocks):
    """Colonne de blocs empilés depuis base. blocks = [(hauteur, couleur)]."""
    y = base
    for k, (h, col) in enumerate(blocks):
        a = at + k * 0.08
        if t < a:
            continue
        p = ease(prog(t, a, 0.3))
        y -= h + 6
        rrect(c, x, y + (1 - p) * 20, 140, h, 12, col)


def s4(c, t, S):
    header(c, t, S, 'Pour un agent', 'Un contexte *qui évolue*')
    ch = S.cue('à chaque étape')
    card(c, t, ch, 90, 540, 900, 410, LIGHT, 32, 'up')
    if prog(t, ch, 0.5) > 0.4:
        small(c, 'Sans tri', 140, 600, 20, DARK)
        lim = 640
        rrect(c, 140, lim - 3, 800, 6, 3, DARK)
        small(c, 'Limite', 940, lim - 15, 18, DARK, align='right')
        rs = S.cue('long résultat')
        for k in range(4):
            at = ch + 0.3 + k * 0.25 if k < 2 else rs + (k - 2) * 0.3
            hs = ([(50, PL)] * (k + 1) + [(60, PLL)] * k)[:6]
            column(c, t, at, 140 + k * 190, 910, hs)
            small(c, f'Étape {k + 1}', 210 + k * 190, 935, 18, DARK, align='center')
        vt = S.cue('se remplit vite')
        if t >= vt:
            icon(c, t, vt, 'cross', 910, 700, 44, RED)
    eg = S.cue("On garde l'essentiel")
    card(c, t, eg, 90, 990, 900, 440, LIGHT, 32, 'up')
    if prog(t, eg, 0.5) > 0.4:
        small(c, 'Avec tri', 140, 1050, 20, DARK)
        items = [('Résultat utile', 'le résultat utile', PL), ('Résumé des étapes', 'un résumé', PLL),
                 ('Objectif', "l'objectif", RED)]
        for k, (s, kw, col) in enumerate(items):
            at = S.cue(kw)
            y = 1090 + k * 105
            box(c, t, at, 140, y, 520, 85, s, col, WHITE if col == RED else DARK, 30, mode='left')
        te = S.cue('toujours en tête')
        if t >= te:
            icon(c, t, te, 'target', 810, 1300, 90, RED)
        icon(c, t, eg + 0.3, 'check', 810, 1160, 60, DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Le contexte est une *spécification*')
    sp = S.cue('une spécification')
    card(c, t, sp, 90, 540, 900, 400, LIGHT, 32, 'up')
    if prog(t, sp, 0.5) > 0.4:
        icon(c, t, sp + 0.1, 'doc', 190, 680, 110, DARK)
        rows = [('Ce qui entre', 'Ce qui entre'), ('Dans quel ordre', 'dans quel ordre'),
                ('Sous quelle forme', 'sous quelle forme')]
        for k, (s, kw) in enumerate(rows):
            at = S.cue(kw)
            y = 600 + k * 80
            dot(c, t, at, 320, y + 20, 14, RED)
            reveal_plain(c, t, at, s, 350, y + 32, 32, DARK, 'Medium')
        vs = S.cue('versionnez-le')
        chip(c, t, vs, 'Version 1', 320, 850, PLL, DARK, 26)
        chip(c, t, vs + 0.3, 'Version 2', 320 + chip_width('Version 1', 26) + 16, 850, RED, WHITE, 26)
    ev = S.cue('avec les evals')
    card(c, t, ev, 90, 980, 900, 450, LIGHT, 32, 'up')
    if prog(t, ev, 0.5) > 0.4:
        small(c, 'Evals : questions et réponses attendues', 140, 1040, 20, DARK)
        bars = [('Version 1', 0.75, PL, ev + 0.3), ('Version 2', 0.55, RED, S.cue('Retirer un document'))]
        for k, (s, f, col, at) in enumerate(bars):
            y = 1080 + k * 110
            if t >= at - 0.25:
                small(c, s, 140, y + 30, 20, DARK)
            bar(c, t, at, 330, y + 8, 600, 34, f, col, WHITE, 0.8)
        rd = S.cue('Retirer un document')
        if t >= rd:
            small(c, 'Scores illustratifs', 140, 1320, 18, DARK)
        pc = S.cue('peut changer')
        if t >= pc:
            reveal_plain(c, t, pc, 'Un changement se mesure', 940, 1390, 30, RED, 'Medium', 'right')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('De quoi le modèle a-t-il *vraiment besoin*, par tâche ?', 'De quoi'),
        ('Que *résume*-t-on, que *retire*-t-on, quand ça s\'allonge ?', 'Que résume'),
        ('Quelles *evals* vérifient un changement de contexte ?', 'Et quelles evals'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le modèle ne sait que ce qui est *dans sa fenêtre*.', 'le modèle ne sait'),
        ('Choisir, ordonner, résumer, et *tester* ce contexte.', 'Choisissez'),
    ], '42 · Les embeddings au-delà du RAG')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Le prompt que vous écrivez n'est souvent qu'une petite partie de ce que le modèle lit. "
        "À chaque appel, sa fenêtre de contexte se remplit de bien d'autres choses. "
        "Les concevoir, c'est le context engineering : l'ingénierie du contexte.")),
    dict(kind='content', draw=s2, name='Ce qui entre dans la fenêtre', text=(
        "Qu'y a-t-il dans cette fenêtre ? Les instructions, la description des outils disponibles, "
        "la mémoire et un résumé de l'historique, les documents récupérés, quelques exemples, "
        "et l'état de la tâche en cours. Pour un assistant de service client : "
        "la politique de remboursement, l'outil de commande, et le dossier du client.")),
    dict(kind='content', draw=s3, name='Ni trop peu, ni trop', text=(
        "Trop peu de contexte, et le modèle devine : il invente un délai de livraison qu'on ne lui a pas donné. "
        "Trop de contexte, et il se noie : l'information utile est perdue au milieu, et chaque appel coûte plus cher. "
        "Il faut donc ordonner, résumer, élaguer.")),
    dict(kind='content', draw=s4, name='Pour un agent, étape par étape', text=(
        "Pour un agent, le contexte change à chaque étape. Il appelle un outil, reçoit un long résultat, puis un autre. "
        "Sans tri, la fenêtre se remplit vite. "
        "On garde l'essentiel : le résultat utile, un résumé des étapes passées, et l'objectif, toujours en tête.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, traitez le contexte comme une spécification. Ce qui entre, dans quel ordre, "
        "sous quelle forme : écrivez-le, versionnez-le. Puis testez-le avec les evals, "
        "vos questions et leurs réponses attendues. Retirer un document, ou résumer l'historique, "
        "peut changer les réponses.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. De quoi le modèle a-t-il vraiment besoin, pour chaque tâche ? "
        "Que résume-t-on, et que retire-t-on, quand la conversation s'allonge ? "
        "Et quelles evals vérifient qu'un changement de contexte ne dégrade rien ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le modèle ne sait que ce que vous mettez dans sa fenêtre. "
        "Choisissez, ordonnez, résumez, et testez ce contexte comme une spécification. "
        "Prochaine capsule : les embeddings au-delà du RAG, pour classer, regrouper et comparer.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
