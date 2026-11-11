from engine import *  # noqa
from engine import _paint  # noqa

NUM = 53
TITLE = "GOUVERNANCE DE L'IA"
FULL_TITLE = "Gouvernance de l'IA en entreprise"
SLUG = 'gouvernance_ia'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Gouverner, ce n\'est pas *freiner*.')
    # des projets épars, puis rangés
    rg = S.cue('qui utilise quoi')
    u = ease(prog(t, rg, 1.0))
    scat = [(160, 900), (420, 1010), (700, 880), (880, 1060), (260, 1150), (600, 1180)]
    for k, (x0, y0) in enumerate(scat):
        x1, y1 = 140 + (k % 3) * 290, 900 + (k // 3) * 150
        x, y = lerp(x0, x1, u), lerp(y0, y1, u)
        if t >= S.t0 + 0.6 + k * 0.1:
            card(c, t, S.t0 + 0.6 + k * 0.1, x, y, 250, 110, WHITE, 26, 'pop')
            if prog(t, S.t0 + 0.6 + k * 0.1, 0.5) > 0.4:
                icon(c, t, S.t0 + 0.7 + k * 0.1, ['chat', 'doc', 'search', 'code', 'eye', 'db'][k],
                     x + 60, y + 55, 44, DARK)
                plain(c, f'Usage {k + 1}', x + 100, y + 66, 26, DARK, 'Medium')
    dv = S.cue('décider vite')
    if t >= dv:
        chip(c, t, dv, 'Risque faible : feu vert rapide', 540, 1260, RED, WHITE, 32, align='center')


def s2(c, t, S):
    header(c, t, S, 'Le registre', 'Un *registre* des usages')
    reg = S.cue('un registre des usages')
    card(c, t, reg, 90, 540, 900, 540, LIGHT, 36, 'up')
    if prog(t, reg, 0.5) > 0.4:
        cols = [('Qui', 'qui le porte', 140), ('Quoi', 'ce qu', 330),
                ('Données', 'quelles données', 560), ('Risque', 'quel niveau de risque', 800)]
        for s, kw, x in cols:
            at = S.cue(kw)
            if t >= at:
                small(c, s, x, 610, 22, RED)
        rrect(c, 140, 635, 800, 4, 2, PL)
        rows = [('RH', 'Résumé réunions', 'Internes', 'Faible', 'résumé de réunions', PL),
                ('Support', 'Assistant client', 'Clients', 'Élevé', 'ou un assistant', RED)]
        for j, (q, w, d, r, kw, col) in enumerate(rows):
            at = S.cue(kw)
            y = 670 + j * 200
            card(c, t, at, 140, y, 800, 160, WHITE, 26, 'left')
            if prog(t, at, 0.5) > 0.4:
                plain(c, q, 160, y + 92, 26, DARK, 'Medium')
                plain(c, w.split(' ')[0], 330, y + 75, 26, DARK, 'Medium')
                plain(c, w.split(' ', 1)[1], 330, y + 112, 26, DARK, 'Medium')
                plain(c, d, 560, y + 92, 26, DARK, 'Medium')
                chip(c, t, at + 0.3, r, 790, y + 55, col, WHITE if col == RED else DARK, 26)
    if t >= S.cue('Par exemple'):
        reveal_plain(c, t, S.cue('Par exemple'), 'Une ligne par usage, mise à jour', 540, 1260, 32, DARK,
                     'Medium', 'center')
        icon(c, t, S.cue('Par exemple'), 'db', 540, 1360, 60, RED)


def s3(c, t, S):
    header(c, t, S, 'Validation', 'Proportionnée au *risque*')
    lv = [('Usage interne, peu sensible', 'peu sensible', 'Validation légère', 0.3, PL),
          ('Usage client ou sensible', 'décisions sensibles', 'Examen approfondi', 0.9, RED)]
    for k, (s, kw, v, f, col) in enumerate(lv):
        at = S.cue(kw)
        y = 540 + k * 300
        card(c, t, at, 90, y, 900, 270, LIGHT, 36, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, s, 140, y + 60, 20, DARK)
            small(c, 'Niveau de contrôle', 140, y + 110, 18, DARK)
            bar(c, t, at + 0.2, 140, y + 130, 800, 40, f, col, WHITE, 0.9)
            icon(c, t, at + 0.4, 'check' if k == 0 else 'shield', 170, y + 220, 40, RED if k else DARK)
            reveal_plain(c, t, at + 0.4, v, 220, y + 232, 34, DARK, 'Medium')
    ai = S.cue("l'AI Act")
    card(c, t, ai, 90, 1150, 900, 270, RED, 36, 'up')
    if prog(t, ai, 0.5) > 0.4:
        small(c, 'AI Act européen · le principe', 140, 1210, 20, WHITE)
        for j in range(4):
            h = 40 + j * 35
            rrect(c, 140 + j * 90, 1380 - h, 60, h * min(1, prog(t, ai + 0.2 + j * 0.1, 0.3)), 12, WHITE)
        text_block(c, t, ai + 0.5, 'Plus de risque, plus d\'exigences', 540, 1320, 34, 'Medium', WHITE, WHITE,
                   maxw=420, max_lines=2)


def s4(c, t, S):
    header(c, t, S, 'Comité et suivi', 'Décider *ensemble*, suivre *dans le temps*')
    cm = S.cue('un comité')
    card(c, t, cm, 90, 540, 900, 420, LIGHT, 36, 'up')
    if prog(t, cm, 0.5) > 0.4:
        small(c, 'Le comité', 140, 600, 20, DARK)
        dot(c, t, cm + 0.1, 540, 770, 70, RED)
        icon(c, t, cm + 0.2, 'target', 540, 770, 60, WHITE)
        mem = [('Métier', 'le métier', 'user', 250, 690), ('Juridique', 'le juridique', 'shield', 830, 690),
               ('Sécurité', 'la sécurité', 'lock', 250, 880), ('Données', 'les équipes données', 'db', 830, 880)]
        for s, kw, ic, x, y in mem:
            at = S.cue(kw)
            if t >= at:
                c.drawLine(x, y - 15, 540, 770, _paint(PL, 4)) if prog(t, at, 0.4) >= 1 else None
            chip(c, t, at, s, x, y - 40, WHITE, DARK, 28, align='center')
    rg = S.cue("règles d'usage communes")
    card(c, t, rg, 90, 990, 900, 160, LIGHT, 32, 'left')
    if prog(t, rg, 0.5) > 0.4:
        icon(c, t, rg + 0.1, 'doc', 170, 1070, 54, DARK)
        reveal_plain(c, t, rg + 0.15, 'Règles communes', 240, 1060, 34, DARK, 'Medium')
        oa = S.cue('outils autorisés')
        if t >= oa:
            reveal_plain(c, t, oa, 'Ex. : outils autorisés', 240, 1110, 26, DARK, 'Medium')
    sv = S.cue('dans le temps')
    card(c, t, sv, 90, 1180, 900, 240, LIGHT, 32, 'up')
    if prog(t, sv, 0.5) > 0.4:
        small(c, 'Suivi', 140, 1240, 20, DARK)
        rrect(c, 140, 1320, 800, 6, 3, PL)
        inc = S.cue('incidents signalés')
        rv = S.cue('revues régulières')
        for k in range(4):
            x = 200 + k * 220
            dot(c, t, rv + k * 0.12, x, 1323, 20, DARK)
        if t >= rv:
            small(c, 'Revues', 200, 1385, 18, DARK)
        icon(c, t, inc, 'bolt', 530, 1290, 40, RED)
        if t >= inc:
            small(c, 'Incident', 560, 1275, 18, RED)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'La gouvernance, *une alliée*')
    st = [('Inscrire tôt au registre', 'tôt au registre', 'doc'),
          ('Documenter données et risques', 'documentez', 'shield')]
    for k, (s, kw, ic) in enumerate(st):
        at = S.cue(kw)
        y = 550 + k * 150
        card(c, t, at, 90, y, 900, 130, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 170, y + 65, 52, DARK)
            reveal_plain(c, t, at + 0.15, s, 240, y + 77, 34, DARK, 'Medium')
    pv = S.cue('vous passez plus vite')
    card(c, t, pv, 90, 870, 900, 300, LIGHT, 36, 'up')
    if prog(t, pv, 0.5) > 0.4:
        small(c, 'Délai de validation · illustratif', 140, 930, 20, DARK)
        plain(c, 'Dossier tardif', 140, 1000, 28, DARK)
        bar(c, t, pv + 0.2, 140, 1020, 800, 34, 0.9, PL, WHITE, 0.8)
        plain(c, 'Dossier prêt tôt', 140, 1100, 28, RED)
        bar(c, t, pv + 0.4, 140, 1120, 800, 34, 0.4, RED, WHITE, 0.8)
    ob = S.cue('accélérer les projets sûrs')
    card(c, t, ob, 90, 1210, 900, 200, RED, 36, 'up')
    if prog(t, ob, 0.5) > 0.4:
        icon(c, t, ob + 0.1, 'bolt', 180, 1310, 60, WHITE)
        reveal_plain(c, t, ob + 0.2, 'Accélérer, pas bloquer', 250, 1328, 44, WHITE, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Votre usage est-il inscrit au *registre* ?', 'Votre usage'),
        ('Quel *niveau de risque*, donc quelle validation ?', 'Quel niveau'),
        ('Qui suit les *incidents* après le lancement ?', 'Et qui suit'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un *registre*, une validation *proportionnée* au risque.', 'un registre'),
        ('Un comité, des règles communes, un suivi, pour *accélérer*.', 'Un comité'),
    ], '54 · Estimer et planifier un projet IA')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Gouverner l'IA, ce n'est pas freiner les projets. "
        "C'est savoir qui utilise quoi, avec quelles données, et décider vite quand le risque est faible. Sans ce cadre, les usages se multiplient en silence.")),
    dict(kind='content', draw=s2, name='Le registre des usages', text=(
        "Tout commence par un registre des usages. Pour chaque usage : qui le porte, ce qu'il fait, "
        "quelles données il manipule, et quel niveau de risque il présente. "
        "Par exemple, un résumé de réunions interne, ou un assistant qui répond directement aux clients.")),
    dict(kind='content', draw=s3, name='Des niveaux de validation selon le risque', text=(
        "Ensuite, des niveaux de validation selon le risque. Un usage interne, peu sensible : une validation légère. "
        "Un usage client, ou qui touche des décisions sensibles : un examen approfondi. "
        "C'est aussi le principe de l'AI Act, le règlement européen sur l'IA : "
        "plus le risque est élevé, plus les exigences sont fortes.")),
    dict(kind='content', draw=s4, name='Comité, règles communes et suivi', text=(
        "Pour décider, un comité réunit le métier, le juridique, la sécurité et les équipes données. "
        "Il fixe des règles d'usage communes, comme les outils autorisés ou les données interdites. "
        "Et il suit les usages dans le temps : incidents signalés, revues régulières.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, la gouvernance est une alliée. Inscrivez votre projet tôt au registre, "
        "documentez données et risques, et vous passez plus vite, car le comité a déjà ce qu'il lui faut. "
        "L'objectif : accélérer les projets sûrs, pas les bloquer.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Votre usage est-il inscrit au registre ? "
        "Quel niveau de risque présente-t-il, et donc quel niveau de validation ? "
        "Et qui suit les incidents après le lancement ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un registre, et une validation proportionnée au risque. "
        "Un comité, des règles communes et un suivi, pour accélérer les projets sûrs. "
        "Sur la conformité, le juridique reste l'arbitre. "
        "Prochaine capsule : estimer et planifier un projet IA, la dernière de la saison.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
