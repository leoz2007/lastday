from engine import *  # noqa
from engine import _paint  # noqa

NUM = 64
TITLE = 'GOUVERNANCE'
FULL_TITLE = 'Gouvernance et conformité'
SLUG = 'gouvernance_conformite'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'


def doc_lines(c, t, at, x, y, w, n, hot=(), gap=46):
    """Lignes d'un document ; les lignes de `hot` passent en rouge."""
    for k in range(n):
        p = ease(prog(t, at + k * 0.08, 0.4))
        if p <= 0:
            continue
        ww = (w if k % 3 else w * 0.75) * p
        rrect(c, x, y + k * gap, ww, 18, 9, RED if k in hot else PL)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Sans règles, un agent est *un risque*.')
    a = S.cue('sans règles écrites')
    card(c, t, a, 90, 830, 900, 200, WHITE, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'code', 190, 930, 80, DARK)
        reveal_plain(c, t, a + 0.2, 'Agent de code', 270, 944, 38, DARK)
        icon(c, t, a + 0.5, 'cross', 900, 930, 60, RED)
    items = [('check', 'Permis ?', 'ce qui est permis'), ('db', 'Dépôts ?', 'sur quels dépôts'),
             ('user', 'Qui tranche ?', 'qui tranche')]
    for k, (ic, s, kw) in enumerate(items):
        at = S.cue(kw)
        x = 90 + k * 310
        hot = k == 2
        card(c, t, at, x, 1080, 280, 300, RED if hot else LIGHT, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if hot else DARK
            icon(c, t, at + 0.1, ic, x + 140, 1190, 80, fg)
            plain(c, s, x + 140, 1320, 32, fg, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, "Politique d'usage", 'Permis, interdit, *et où*')
    cols = [(90, 'Autorisé', 'check', DARK, 'Ce qui est autorisé',
             [('Générer des tests', 'générer des tests'), ('Expliquer du code', 'expliquer du code')]),
            (550, 'Interdit', 'cross', RED, 'Ce qui est interdit',
             [('Coller un secret', 'coller un secret'), ('Envoyer un dépôt', 'dépôt confidentiel'),
              ('confidentiel dehors', 'dépôt confidentiel')])]
    for x, title, ic, col, kw, rows in cols:
        at = S.cue(kw)
        card(c, t, at, x, 540, 440, 360, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 70, 615, 50, col)
            reveal_plain(c, t, at + 0.15, title, x + 120, 630, 38, col, 'Medium')
            for j, (s, kw2) in enumerate(rows):
                a2 = S.cue(kw2) + (0.15 if j == 2 else 0)
                reveal_plain(c, t, a2, s, x + 50, 730 + j * 56, 32, DARK, 'Medium')
    cl = S.cue('classement par sensibilité')
    card(c, t, cl, 90, 940, 900, 480, LIGHT, 32, 'up')
    if prog(t, cl, 0.5) > 0.4:
        small(c, 'Par sensibilité du dépôt · exemple', 140, 1000, 20, DARK)
        rows = [('Public', 'Tout modèle validé', PLL, DARK, 'dépôt public'),
                ('Interne', 'Modèle sur site seul', PL, DARK, 'classement par sensibilité'),
                ('Critique', "Pas d'agent", RED, WHITE, 'dépôt critique')]
        for j, (nm, rule, fill, fg, kw) in enumerate(rows):
            at = S.cue(kw) + (0.4 if j == 1 else 0)
            y = 1040 + j * 120
            if t >= at:
                rrect(c, 140, y, 800, 100, 24, WHITE)
                icon(c, t, at, 'lock' if j == 2 else 'db', 195, y + 50, 44, RED if j == 2 else DARK)
                plain(c, nm, 250, y + 62, 34, DARK, 'Medium')
            w = chip_width(rule, 28)
            chip(c, t, at, rule, 915 - w, y + 26, fill, fg, 28)


def s3(c, t, S):
    header(c, t, S, 'Propriété intellectuelle', 'Code généré, *licences* lues')
    a = S.cue('À qui appartient')
    card(c, t, a, 90, 540, 900, 300, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'code', 180, 650, 70, DARK)
        reveal_plain(c, t, a + 0.2, 'À qui appartient', 260, 640, 36, DARK)
        reveal_plain(c, t, a + 0.3, 'le code généré ?', 260, 690, 36, RED)
        sl = S.cue('soumis à licence')
        chip(c, t, sl, 'Code tiers repris ?', 140, 750, WHITE, DARK, 30)
    p = S.cue('poids ouverts')
    card(c, t, p, 90, 880, 520, 540, LIGHT, 32, 'up')
    if prog(t, p, 0.5) > 0.4:
        small(c, 'Licence du modèle', 140, 950, 20, DARK)
        hot = []
        if t >= S.cue('limitent des usages'):
            hot.append(2)
        if t >= S.cue('imposent des conditions'):
            hot.append(5)
        doc_lines(c, t, p + 0.2, 140, 1000, 250, 8, hot)
        if 2 in hot:
            small(c, 'Usages limités', 560, 1080, 18, RED, align='right')
        if 5 in hot:
            small(c, 'Conditions', 560, 1218, 18, RED, align='right')
    j = S.cue('lire par le juridique')
    arrow(c, t, j, 620, 1150, 700, 1150, DARK, 6, 18)
    card(c, t, j + 0.2, 710, 880, 280, 540, RED, 32, 'pop')
    if prog(t, j + 0.2, 0.5) > 0.4:
        icon(c, t, j + 0.3, 'user', 850, 1080, 90, WHITE)
        plain(c, 'Juridique', 850, 1220, 34, WHITE, 'Medium', 'center')
        icon(c, t, j + 0.6, 'eye', 850, 1320, 60, WHITE)


def s4(c, t, S):
    header(c, t, S, 'Réglementation', 'AI Act, RGPD, *votre secteur*')
    rows = [("L'AI Act", 'AI Act', 'Usages classés par risque'),
            ('Le RGPD', 'RGPD', 'Données personnelles'),
            ('règlement européen DORA', 'DORA (finance)', 'Résilience, prestataires tiers')]
    for k, (kw, nm, sub) in enumerate(rows):
        at = S.cue(kw)
        y = 540 + k * 190
        hot = k == 2
        card(c, t, at, 90, y, 900, 170, RED if hot else LIGHT, 32, 'left')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if hot else DARK
            icon(c, t, at + 0.1, 'shield' if k != 1 else 'lock', 170, y + 85, 60, fg)
            reveal_plain(c, t, at + 0.15, nm, 240, y + 72, 38, fg, 'Medium')
            reveal_plain(c, t, at + 0.25, sub, 240, y + 124, 30, fg, 'Medium')
        if k == 0:
            r = S.cue('niveau de risque')
            for j in range(4):
                h = 22 * (j + 1)
                hh = h * ease(prog(t, r + j * 0.12, 0.4))
                if hh > 0:
                    rrect(c, 760 + j * 52, y + 130 - hh, 34, hh, 8, RED if j == 3 else PL)
        if k == 2:
            pr = S.cue('prestataires informatiques')
            icon(c, t, pr, 'gear', 900, y + 85, 56, WHITE)
    r = S.cue('Rien à voir')
    card(c, t, r, 90, 1140, 900, 280, LIGHT, 32, 'up')
    if prog(t, r, 0.5) > 0.4:
        box(c, t, r + 0.1, 130, 1190, 360, 180, 'Règlement DORA', RED, WHITE, 32)
        icon(c, t, r + 0.3, 'cross', 540, 1280, 50, DARK)
        box(c, t, r + 0.4, 590, 1190, 360, 180, 'Métriques DORA (capsule 63)', PL, DARK, 30)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'La conformité, *une exigence*')
    n1 = S.cue('Chaque nouveau dépôt')
    n2 = S.cue('nouveau modèle')
    chip(c, t, n1, 'Nouveau dépôt', 90, 560, PLL, DARK, 30)
    chip(c, t, n2, 'Nouveau modèle', 90, 660, PLL, DARK, 30)
    v = S.cue('passe par une validation')
    arrow(c, t, v, 400, 620, 470, 620, DARK, 6, 18)
    card(c, t, v + 0.1, 480, 540, 260, 180, RED, 32, 'pop')
    if prog(t, v + 0.1, 0.5) > 0.4:
        icon(c, t, v + 0.2, 'shield', 610, 610, 60, WHITE)
        plain(c, 'Validation', 610, 690, 28, WHITE, 'Medium', 'center')
    arrow(c, t, v + 0.4, 750, 630, 820, 630, DARK, 6, 18)
    icon(c, t, v + 0.6, 'check', 900, 630, 70, DARK)
    d = S.cue('ce délai')
    card(c, t, d, 90, 770, 900, 150, LIGHT, 32, 'left')
    if prog(t, d, 0.5) > 0.4:
        icon(c, t, d + 0.1, 'clock', 170, 845, 56, DARK)
        reveal_plain(c, t, d + 0.15, 'Délai prévu au planning', 240, 858, 36, DARK)
    g = S.cue('Tenez un registre')
    card(c, t, g, 90, 950, 900, 260, LIGHT, 32, 'left')
    if prog(t, g, 0.5) >= 1:
        small(c, 'Registre', 140, 1010, 20, DARK)
        cols = [('Qui', 'user'), ('Quel modèle', 'brain'), ('Quel dépôt', 'db')]
        for k, (s, ic) in enumerate(cols):
            x = 140 + k * 280
            rrect(c, x, 1040, 260, 130, 22, WHITE)
            icon(c, t, g + 0.2 + k * 0.15, ic, x + 55, 1105, 44, RED if k == 1 else DARK)
            reveal_plain(c, t, g + 0.25 + k * 0.15, s, x + 95, 1117, 28, DARK)
    j = S.cue('la conformité tranchent')
    card(c, t, j, 90, 1250, 900, 170, RED, 32, 'up')
    if prog(t, j, 0.5) > 0.4:
        icon(c, t, j + 0.1, 'user', 170, 1335, 60, WHITE)
        reveal_plain(c, t, j + 0.2, 'Juridique et conformité tranchent', 240, 1349, 36, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quels *dépôts* peut-il lire, selon leur sensibilité ?', 'Quels dépôts'),
        ('Le juridique a-t-il validé la *licence* du modèle ?', 'validé la licence'),
        ("Quelles *règles sectorielles* s'appliquent ?", 'règles sectorielles'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Une *politique d'usage* écrite, dépôt par dépôt.", "politique d'usage"),
        ('Licences lues, règlements identifiés : le *juridique* tranche.', 'des licences lues'),
    ], '65 · Exploitation et adoption')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un agent de code sans règles écrites est un risque juridique. "
        "Avant de le déployer, l'entreprise doit dire ce qui est permis, sur quels dépôts, "
        "et qui tranche en cas de doute.")),
    dict(kind='content', draw=s2, name="Une politique d'usage claire", text=(
        "D'abord, une politique d'usage claire. Ce qui est autorisé : générer des tests, expliquer du code. "
        "Ce qui est interdit : coller un secret, envoyer un dépôt confidentiel vers un modèle externe. "
        "Et sur quels dépôts : la règle suit le classement par sensibilité. "
        "Un dépôt public n'a pas les droits d'un dépôt critique.")),
    dict(kind='content', draw=s3, name='Propriété intellectuelle et licences', text=(
        "Deuxième sujet : la propriété intellectuelle. À qui appartient le code généré, "
        "et reprend-il du code soumis à licence ? "
        "Les modèles à poids ouverts, installés chez vous, ont aussi leur licence. "
        "Certaines limitent des usages, ou imposent des conditions. "
        "Faites-les lire par le juridique.")),
    dict(kind='content', draw=s4, name='AI Act, RGPD et règlement DORA', text=(
        "Troisième sujet : la réglementation. L'AI Act, le règlement européen sur l'IA, "
        "classe les usages par niveau de risque. "
        "Le RGPD, le règlement général sur la protection des données, couvre les données personnelles, "
        "même dans un dépôt. Et chaque secteur ajoute ses règles. "
        "En finance, le règlement européen DORA, sur la résilience opérationnelle numérique, "
        "encadre notamment le recours aux prestataires informatiques tiers. "
        "Rien à voir avec les métriques DORA vues précédemment.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, la conformité devient une exigence. "
        "Chaque nouveau dépôt, chaque nouveau modèle passe par une validation : prévoyez ce délai. "
        "Tenez un registre : qui utilise quel modèle, sur quel dépôt. "
        "Et le juridique et la conformité tranchent : consultez-les tôt.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels dépôts l'agent peut-il lire, selon leur sensibilité ? "
        "Le juridique a-t-il validé la licence du modèle ? "
        "Et quelles règles sectorielles s'appliquent ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : une politique d'usage écrite, des licences lues, des règlements identifiés. "
        "Et le juridique et la conformité tranchent. "
        "Prochaine capsule : exploitation et adoption.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
