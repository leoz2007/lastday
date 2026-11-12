from engine import *  # noqa
from engine import _paint  # noqa

NUM = 68
TITLE = 'INTERPRÉTABILITÉ'
FULL_TITLE = 'Interprétabilité'
SLUG = 'interpretabilite'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'

# valeurs illustratives pour la « masse de nombres »
NUMS = ['0,12', '-0,48', '0,91', '0,07', '-0,33', '0,56',
        '-0,85', '0,24', '0,63', '-0,19', '0,02', '0,77',
        '0,41', '-0,66', '0,18', '-0,05', '0,94', '-0,27']


def lamp(c, t, at, on_at, x, y, r=20):
    """Voyant : gris clair, puis rouge quand il s'allume."""
    dot(c, t, at, x, y, r, PL)
    if on_at is not None and t >= on_at:
        dot(c, t, on_at, x, y, r, RED)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Que des *nombres*, aucune *règle* écrite.')
    a = S.cue('une immense quantité')
    for k, s in enumerate(NUMS):
        col, row = k % 6, k // 6
        chip(c, t, a + k * 0.04, s, 110 + col * 148, 830 + row * 90, PLL, DARK, 28, h=60, padx=14)
    pl = S.cue('Personne ne peut lire')
    if t >= pl:
        icon(c, t, pl, 'cross', 140, 1150, 50, RED)
        reveal_plain(c, t, pl + 0.1, 'Aucune règle lisible', 190, 1165, 34, WHITE, 'Medium')
    bn = S.cue("L'interprétabilité cherche")
    card(c, t, bn, 90, 1230, 900, 200, WHITE, 32, 'up')
    if prog(t, bn, 0.5) > 0.4:
        icon(c, t, bn + 0.1, 'eye', 180, 1330, 70, RED)
        reveal_plain(c, t, bn + 0.2, "Regarder à l'intérieur", 260, 1320, 36, DARK, 'Medium')
        small(c, 'Interprétabilité', 260, 1375, 20, RED)


def s2(c, t, S):
    header(c, t, S, 'Des concepts internes', "Des *voyants* qui s'allument")
    ph = S.cue("ce qui s'active")
    card(c, t, ph, 90, 540, 900, 190, LIGHT, 32, 'up')
    if prog(t, ph, 0.5) > 0.4:
        small(c, 'Texte lu par le modèle', 140, 600, 20, DARK)
        chip(c, t, ph + 0.2, '« Un dîner à Lyon, quelle bonne idée... »', 140, 630, WHITE, DARK, 30)
    ft = S.cue('concepts internes')
    card(c, t, ft, 90, 770, 900, 660, LIGHT, 32, 'up')
    if prog(t, ft, 0.5) > 0.4:
        small(c, 'Activité interne · illustratif', 140, 830, 20, DARK)
        ff = S.cue('features')
        if t >= ff:
            small(c, 'Features', 940, 830, 20, RED, align='right')
        for k in range(30):
            col, row = k % 10, k // 10
            lamp(c, t, ft + 0.2 + k * 0.02, None, 175 + col * 82, 890 + row * 64, 16)
        items = [('Ville : Lyon', 'une ville', 'Ville'),
                 ('Sujet : la cuisine', 'la cuisine', 'Sujet'),
                 ("Ton : l'ironie", "l'ironie", 'Ton')]
        for j, (s, kw, _) in enumerate(items):
            at = S.cue(kw)
            y = 1110 + j * 100
            lamp(c, t, ft + 0.3, at, 175, y, 26)
            if t >= at:
                reveal_plain(c, t, at + 0.1, s, 230, y + 12, 34, DARK, 'Medium')
        tb = S.cue('tableau de bord')
        if t >= tb:
            icon(c, t, tb, 'bolt', 880, 1210, 70, RED)


def s3(c, t, S):
    header(c, t, S, 'Des circuits', 'Suivre le *chemin* du calcul')
    cr = S.cue('des circuits')
    card(c, t, cr, 90, 540, 900, 420, LIGHT, 32, 'up')
    if prog(t, cr, 0.5) > 0.4:
        small(c, 'Un circuit · illustratif', 140, 600, 20, DARK)
        chip(c, t, cr + 0.2, '« La capitale de la France est... »', 140, 630, WHITE, DARK, 28)
        nodes = [('France', 'le concept du pays', 140, PL, DARK),
                 ('Capitale', 'celui de capitale', 410, PL, DARK),
                 ('Paris', 'nom de la ville', 680, RED, WHITE)]
        prev = None
        for s, kw, x, fill, fg in nodes:
            at = S.cue(kw)
            box(c, t, at, x, 760, 230, 120, s, fill, fg, 32)
            if prev is not None:
                arrow(c, t, at - 0.2, prev + 236, 820, x - 8, 820, DARK, 5, 16)
            prev = x
        ss = S.cue('les relient')
        if t >= ss:
            small(c, 'Concepts reliés, étape par étape', 140, 925, 18, DARK)
    rf = S.cue('renforcer ou atténuer')
    card(c, t, rf, 90, 1000, 900, 430, LIGHT, 32, 'up')
    if prog(t, rf, 0.5) > 0.4:
        small(c, 'Régler un concept · illustratif', 140, 1060, 20, DARK)
        plain(c, 'Concept « cuisine »', 140, 1125, 30, DARK)
        u = clamp((t - rf - 0.3) / 1.2)
        frac = lerp(0.3, 0.9, ease(u))
        rrect(c, 140, 1150, 800, 30, 15, WHITE)
        rrect(c, 140, 1150, 800 * frac, 30, 15, RED)
        dot(c, t, rf + 0.3, 140 + 800 * frac, 1165, 26, DARK)
        ob = S.cue('observer comment')
        if t >= ob:
            small(c, 'Effet sur la réponse', 140, 1240, 20, DARK)
            box(c, t, ob, 140, 1270, 800, 120, 'La réponse parle *davantage de cuisine*', WHITE, DARK, 32)


def s4(c, t, S):
    header(c, t, S, 'Les limites', 'Une vue *encore partielle*')
    pa = S.cue('partielle')
    card(c, t, pa, 90, 540, 900, 380, LIGHT, 32, 'up')
    if prog(t, pa, 0.5) > 0.4:
        small(c, 'Ce que la recherche explique · illustratif', 140, 600, 20, DARK)
        pp = S.cue('une petite partie')
        for k in range(40):
            col, row = k % 10, k // 10
            fill = RED if (k in (0, 1, 10, 11) and t >= pp) else PL
            card(c, t, pa + 0.2 + k * 0.015, 140 + col * 82, 640 + row * 62, 70, 50, fill, 10, 'pop')
        if t >= pp:
            small(c, 'Compris', 140, 900, 18, RED)
            small(c, 'Encore inexpliqué', 940, 900, 18, DARK, align='right')
    ra = S.cue('raisonnement que le modèle affiche')
    card(c, t, ra, 90, 960, 420, 340, LIGHT, 32, 'up')
    if prog(t, ra, 0.5) > 0.4:
        icon(c, t, ra + 0.1, 'chat', 300, 1080, 80, DARK)
        box(c, t, ra + 0.2, 130, 1170, 340, 100, 'Raisonnement affiché', WHITE, DARK, 28)
    ci = S.cue('calcul interne')
    card(c, t, ci, 570, 960, 420, 340, LIGHT, 32, 'up')
    if prog(t, ci, 0.5) > 0.4:
        icon(c, t, ci + 0.1, 'gear', 780, 1080, 80, DARK)
        box(c, t, ci + 0.2, 610, 1170, 340, 100, 'Calcul interne', WHITE, DARK, 28)
    fd = S.cue('reflet fidèle')
    if t >= fd:
        icon(c, t, fd, 'cross', 540, 1130, 56, RED)
        reveal_plain(c, t, fd + 0.1, 'Pas forcément le même', 540, 1380, 34, RED, 'Medium', 'center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Prometteur, mais *les tests* d\'abord')
    items = [('Audit', 'des audits', 'search'),
             ('Détection', 'la détection', 'shield'),
             ('Confiance', 'plus de confiance', 'check')]
    for k, (s, kw, ic) in enumerate(items):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 540, 280, 300, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 650, 80, DARK)
            plain(c, s, x + 140, 790, 32, DARK, 'Medium', 'center')
    pr = S.cue('le premier outil')
    card(c, t, pr, 90, 880, 900, 550, RED, 32, 'up')
    if prog(t, pr, 0.5) > 0.4:
        icon(c, t, pr + 0.1, 'target', 180, 970, 60, WHITE)
        reveal_plain(c, t, pr + 0.2, "Aujourd'hui : l'évaluation", 240, 985, 38, WHITE, 'Medium')
        rows = [('Des tests sur vos propres cas', 'vos propres cas'),
                ('Rejoués à chaque changement', 'chaque changement')]
        for j, (s, kw) in enumerate(rows):
            at = S.cue(kw)
            y = 1070 + j * 150
            card(c, t, at, 140, y, 800, 120, WHITE, 24, 'left')
            if prog(t, at, 0.5) > 0.4:
                icon(c, t, at + 0.1, 'check', 210, y + 60, 50, RED)
                plain(c, s, 270, y + 72, 32, DARK, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quels *tests* prouvent le bon comportement sur nos cas ?', 'Quels tests'),
        ('Évite-t-on de prendre le *raisonnement affiché* pour une preuve ?', 'Évite-t-on'),
        ('Quels *comportements indésirables* surveiller ?', 'Et quels comportements'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("On repère des *concepts* et des *circuits*, mais une petite partie seulement.",
         "l'interprétabilité repère"),
        ('Pour décider, fiez-vous d\'abord à *vos tests*.', 'fiez-vous'),
    ], '69 · Calibration et incertitude')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle de langage ne contient aucune règle écrite, "
        "seulement une immense quantité de nombres. "
        "Personne ne peut lire, ligne à ligne, pourquoi il répond ce qu'il répond. "
        "L'interprétabilité cherche à ouvrir cette boîte noire.")),
    dict(kind='content', draw=s2, name='Des concepts internes', text=(
        "Des chercheurs observent ce qui s'active à l'intérieur, pendant le calcul. "
        "Ils repèrent des concepts internes, souvent appelés caractéristiques, ou features en anglais. "
        "Chacun s'allume pour une notion : une ville, un sujet comme la cuisine, "
        "ou un ton, comme l'ironie. Un peu comme les voyants d'un tableau de bord.")),
    dict(kind='content', draw=s3, name='Des circuits qui relient les concepts', text=(
        "Ces concepts ne travaillent pas seuls. Des travaux tracent des circuits, "
        "des chemins qui les relient. Pour trouver la capitale d'un pays, "
        "on peut voir le concept du pays activer celui de capitale, puis le nom de la ville. "
        "On peut parfois renforcer ou atténuer un concept, et observer comment la réponse change.")),
    dict(kind='content', draw=s4, name='Les limites actuelles', text=(
        "Attention : c'est une recherche active, et partielle. "
        "On ne comprend encore qu'une petite partie du fonctionnement. "
        "Et ne confondez pas avec le raisonnement que le modèle affiche : "
        "ce texte n'est pas forcément le reflet fidèle de son calcul interne.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, l'interprétabilité promet des audits, la détection de comportements indésirables, "
        "et plus de confiance. Mais aujourd'hui, le premier outil reste l'évaluation : "
        "des tests sur vos propres cas, rejoués à chaque changement.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels tests prouvent que le modèle se comporte bien sur nos cas ? "
        "Évite-t-on de prendre son raisonnement affiché pour une preuve ? "
        "Et quels comportements indésirables faut-il surveiller ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : l'interprétabilité repère des concepts et des circuits dans le modèle, "
        "mais n'en éclaire encore qu'une petite partie. "
        "Pour décider, fiez-vous d'abord à vos tests. "
        "Prochaine capsule : calibration et incertitude, ou comment savoir quand un modèle doute.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
