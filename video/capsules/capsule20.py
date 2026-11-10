from engine import *  # noqa
from engine import _paint  # noqa

NUM = 20
TITLE = 'WORKFLOWS'
FULL_TITLE = 'Workflows et chaînes de prompts'
SLUG = 'workflows_chaines_prompts'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'

STEPS = ['Extraire', 'Classer', 'Rédiger', 'Vérifier']


def s1(c, t, S):
    opening(c, t, S, CAP, "Quatre petits prompts battent *un prompt géant*.")
    g = S.cue('Un seul prompt géant')
    card(c, t, g, 90, 850, 900, 200, PL, 36, 'up')
    if prog(t, g, 0.5) > 0.4:
        icon(c, t, g + 0.1, 'doc', 190, 950, 80, DARK)
        reveal_plain(c, t, g + 0.2, 'Un prompt géant', 270, 965, 44, DARK, 'Medium')
        sw = S.cue('fait souvent moins bien')
        icon(c, t, sw, 'cross', 900, 950, 70, RED)
    q = S.cue('quatre petits prompts')
    for k, s in enumerate(STEPS):
        x = 90 + k * 240
        box(c, t, q + k * 0.2, x, 1130, 180, 120, s, WHITE if k < 3 else RED,
            DARK if k < 3 else WHITE, 28)
        if k < 3:
            arrow(c, t, q + k * 0.2 + 0.15, x + 188, 1190, x + 232, 1190, WHITE, 5, 14)
    for k, kw in enumerate(['simple', 'testable', 'réparable']):
        at = S.cue(kw)
        chip(c, t, at, kw.capitalize(), 90 + k * 300, 1320, WHITE if k else RED,
             DARK if k else WHITE, 32)


def s2(c, t, S):
    header(c, t, S, 'Chaîne de prompts', 'Une étape, *un seul travail*')
    r = S.cue('Prenez une réclamation')
    card(c, t, r, 90, 540, 900, 110, LIGHT, 30, 'up')
    if prog(t, r, 0.5) > 0.4:
        icon(c, t, r + 0.1, 'chat', 160, 595, 50, RED)
        reveal_plain(c, t, r + 0.2, 'Réclamation client', 220, 608, 34, DARK)
    outs = ['Client, commande, problème', 'Catégorie : livraison', 'Brouillon de réponse', 'Réponse conforme']
    kws = ['extraire les faits', 'classer la demande', 'rédiger une réponse', 'vérifier cette réponse']
    de = S.cue("devient l'entrée")
    for k, (s, o, kw) in enumerate(zip(STEPS, outs, kws)):
        at = S.cue(kw)
        y = 710 + k * 180
        box(c, t, at, 90, y, 360, 120, f'{k + 1}. {s}', DARK if k < 3 else RED, WHITE, 34, 'Medium', 30, 'left')
        arrow(c, t, at + 0.3, 460, y + 60, 530, y + 60, DARK, 5, 16)
        box(c, t, at + 0.4, 540, y, 450, 120, o, PLL, DARK, 28)
        if k < 3:
            arrow(c, t, de + k * 0.2, 580, y + 124, 420, y + 176, RED, 5, 16)
    arrow(c, t, r + 0.3, 270, 655, 270, 705, DARK, 5, 16)


def s3(c, t, S):
    header(c, t, S, 'Tests par étape', 'Chaque étape a *ses tests*')
    pr = S.cue('son propre prompt')
    ts = S.cue('ses propres tests')
    st = S.cue('se trompe')
    rates = [0.95, 0.55, 0.9, 0.92]
    for k, s in enumerate(STEPS):
        x = 90 + k * 230
        bad = k == 1 and t >= st
        card(c, t, pr + k * 0.15, x, 540, 210, 380, RED if bad else LIGHT, 30, 'up')
        if prog(t, pr + k * 0.15, 0.5) > 0.4:
            fg = WHITE if bad else DARK
            plain(c, s, x + 105, 610, 30, fg, 'Medium', 'center')
            icon(c, t, pr + k * 0.15 + 0.1, 'doc', x + 105, 690, 50, fg)
            small(c, 'Prompt', x + 105, 760, 18, fg, align='center')
            if t >= ts - 0.25:
                small(c, 'Tests', x + 105, 820, 18, fg, align='center')
                bar(c, t, ts + k * 0.15, x + 25, 840, 160, 22, rates[k], WHITE if bad else RED,
                    PLL if bad else WHITE, 0.8)
            if k == 1:
                icon(c, t, st, 'cross', x + 105, 885, 36, WHITE)
    if t >= ts + 0.8:
        small(c, 'Taux de réussite illustratifs', 90, 965, 20, DARK)
    u = S.cue('prompt unique')
    card(c, t, u, 90, 1010, 900, 410, LIGHT, 32, 'up')
    if prog(t, u, 0.5) > 0.4:
        label(c, t, u + 0.1, 'Prompt unique', 140, 1045, PLL, DARK, 22)
        hid = S.cue('se cache')
        widths = [520, 460, 560, 400, 500, 540]
        for j, w in enumerate(widths):
            y = 1135 + j * 42
            rrect(c, 140, y, w, 22, 11, PL)
            if j == 3 and t >= hid:
                dot(c, t, hid, 140 + w - 120, y + 11, 14, RED)
        on = S.cue('on ne sait pas')
        icon(c, t, on, 'search', 850, 1220, 90, DARK)
        if t >= on + 0.2:
            reveal_plain(c, t, on + 0.2, 'Quoi corriger ?', 850, 1340, 30, RED, 'Medium', 'center')


def s4(c, t, S):
    header(c, t, S, 'Workflow ou agent', 'Chemin *fixé* ou chemin *libre*')
    w = S.cue('Un workflow codé')
    card(c, t, w, 90, 540, 440, 530, LIGHT, 32, 'up')
    if prog(t, w, 0.5) > 0.4:
        plain(c, 'Workflow codé', 310, 615, 34, DARK, 'Medium', 'center')
        for k in range(4):
            x = 150 + k * 107
            dot(c, t, w + 0.3 + k * 0.15, x, 740, 24, DARK)
            if k < 3:
                arrow(c, t, w + 0.4 + k * 0.15, x + 30, 740, x + 77, 740, DARK, 4, 12)
        small(c, 'Toujours le même ordre', 310, 820, 18, DARK, align='center')
        p = S.cue("C'est prévisible")
        chip(c, t, p, 'Prévisible', 130, 880, RED, WHITE, 30)
        chip(c, t, S.cue('plus simple à tester'), 'Simple à tester', 130, 980, PLL, DARK, 30)
    a = S.cue('Un agent libre')
    card(c, t, a, 550, 540, 440, 530, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        plain(c, 'Agent libre', 770, 615, 34, DARK, 'Medium', 'center')
        pts = [(620, 700), (760, 770), (680, 790), (880, 700), (920, 790)]
        for k in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[k], pts[k + 1]
            arrow(c, t, a + 0.4 + k * 0.15, x1, y1, x2, y2, PL, 4, 12)
        for k, (x, y) in enumerate(pts):
            dot(c, t, a + 0.3 + k * 0.15, x, y, 20, DARK)
        small(c, 'Il choisit ses étapes', 770, 860, 18, DARK, align='center')
        chip(c, t, S.cue('plus souple'), 'Souple', 590, 880, PLL, DARK, 30)
        chip(c, t, S.cue('moins prévisible'), 'Moins prévisible', 590, 980, PLL, DARK, 30)
    pf = S.cue('préférez le workflow')
    card(c, t, pf, 90, 1160, 900, 150, RED, 32, 'up')
    if prog(t, pf, 0.5) > 0.4:
        icon(c, t, pf + 0.1, 'check', 180, 1235, 60, WHITE)
        reveal_plain(c, t, pf + 0.2, 'Chemin connu : workflow', 250, 1250, 40, WHITE, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Des *points de contrôle*')
    b = S.t0 + 0.4
    pc = S.cue('points de contrôle')
    for k, s in enumerate(STEPS):
        x = 90 + k * 240
        box(c, t, b + k * 0.15, x, 560, 180, 110, s, LIGHT, DARK, 28)
        if k < 3:
            gx = x + 210
            dot(c, t, pc + k * 0.2, gx, 615, 24, RED)
            icon(c, t, pc + k * 0.2 + 0.1, 'check', gx, 615, 26, WHITE)
    ex = S.cue("l'extraction est complète")
    card(c, t, ex, 90, 740, 900, 280, LIGHT, 32, 'up')
    if prog(t, ex, 0.5) > 0.4:
        label(c, t, ex + 0.1, 'Contrôles', 140, 770, PLL, DARK, 22)
        rows = [('Extraction complète ?', ex), ('Catégorie connue ?', S.cue('la catégorie existe'))]
        for j, (s, at) in enumerate(rows):
            y = 870 + j * 80
            reveal_plain(c, t, at + 0.2, s, 140, y + 12, 34, DARK)
            dot(c, t, at + 0.4, 920, y, 26, RED)
            icon(c, t, at + 0.5, 'check', 920, y, 28, WHITE)
    outs = [('cross', "S'arrêter", "on s'arrête"), ('gear', 'Réessayer', 'on réessaie'), ('user', 'Un humain', 'à un humain')]
    dt = S.cue('En cas de doute')
    if t >= dt:
        small(c, 'En cas de doute', 90, 1080, 22, DARK)
    for k, (ic, s, kw) in enumerate(outs):
        at = S.cue(kw)
        x = 90 + k * 310
        fill = RED if k == 2 else LIGHT
        fg = WHITE if k == 2 else DARK
        card(c, t, at, x, 1110, 280, 230, fill, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 1190, 70, fg)
            plain(c, s, x + 140, 1300, 32, fg, 'Medium', 'center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles étapes peut-on *séparer* clairement ?', 'Quelles étapes'),
        ("Comment *tester* chacune d'elles ?", 'Comment teste'),
        ('Que faire quand un *contrôle échoue* ?', 'Et que fait'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Des *étapes simples*, chacune avec son prompt et ses tests.', 'découpez'),
        ('Chemin connu : un *workflow*, pas un agent.', 'Un chemin connu'),
    ], '21 · Multi-agents')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un seul prompt géant fait souvent moins bien que quatre petits prompts enchaînés. "
        "Découper une tâche, c'est rendre chaque étape simple, testable et réparable.")),
    dict(kind='content', draw=s2, name='La chaîne de prompts', text=(
        "Prenez une réclamation client. Première étape : extraire les faits, le client, la commande, le problème. "
        "Deuxième étape : classer la demande. Troisième : rédiger une réponse. "
        "Quatrième : vérifier cette réponse avant l'envoi. "
        "Chaque étape a un seul travail, et sa sortie devient l'entrée de la suivante.")),
    dict(kind='content', draw=s3, name='Un prompt et des tests par étape', text=(
        "Chaque étape a son propre prompt, court et précis. Et surtout, ses propres tests. "
        "Si la classification se trompe, vous le voyez tout de suite, à cet endroit précis. "
        "Avec un prompt unique, l'erreur se cache dans la masse, et on ne sait pas quoi corriger. "
        "Avec des étapes, vous en corrigez une sans casser les autres.")),
    dict(kind='content', draw=s4, name='Workflow codé ou agent libre', text=(
        "Un workflow codé suit un chemin fixé à l'avance : toujours les mêmes étapes, dans le même ordre. "
        "C'est prévisible, et plus simple à tester. "
        "Un agent libre choisit lui-même ses étapes : il est plus souple, mais moins prévisible. "
        "Quand le chemin est connu, préférez le workflow.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, les passages entre étapes deviennent des points de contrôle. "
        "On vérifie par exemple que l'extraction est complète, et que la catégorie existe bien. "
        "Ce sont des règles simples, écrites dans le code, pas confiées au modèle. "
        "En cas de doute, on s'arrête, on réessaie, ou on passe la main à un humain.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles étapes peut-on séparer clairement ? "
        "Comment teste-t-on chacune d'elles ? "
        "Et que fait-on quand un contrôle échoue entre deux étapes ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : découpez une tâche complexe en étapes simples, chacune avec son prompt et ses tests. "
        "Un chemin connu mérite un workflow, pas un agent. "
        "Prochaine capsule : les systèmes multi-agents, quand plusieurs agents travaillent ensemble.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
