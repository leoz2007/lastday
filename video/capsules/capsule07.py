from engine import *  # noqa
from engine import _paint  # noqa

NUM = 7
TITLE = 'CHOIX DU MODÈLE'
FULL_TITLE = 'Choix du modèle, coûts et latence'
SLUG = 'choix_modele_couts_latence'
NEXT_CUE = 'prochaine capsule'


def s1(c, t, S):
    opening(c, t, S, CAP, "Le meilleur modèle n'est pas le plus *gros*.")
    a = S.cue('le plus gros')
    sizes = [(230, 80, 'Petit'), (500, 130, 'Moyen'), (820, 180, 'Grand')]
    ja = S.cue('juste assez bon')
    for k, (x, r, s) in enumerate(sizes):
        col = RED if (k == 1 and t >= ja) else PL
        dot(c, t, a + k * 0.2, x, 1120, r, col)
        if t >= a + k * 0.2:
            small(c, s, x, 1350, 24, WHITE, align='center')
    if t >= ja:
        chip(c, t, ja, 'juste assez bon', 500, 900, WHITE, RED, 32, align='center')


def s2(c, t, S):
    header(c, t, S, 'Les gammes', 'Grand ou *petit* modèle')
    rows = [('Capacité', 0.9, 0.5), ('Vitesse', 0.4, 0.9), ('Coût', 0.9, 0.25)]
    g, p = S.cue('de grands modèles'), S.cue('des petits modèles')
    for k, (title, at, col) in enumerate([('Grand modèle', g, RED), ('Petit modèle', p, DARK)]):
        x = 90 + k * 460
        card(c, t, at, x, 540, 440, 420, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            dot(c, t, at + 0.1, x + 70, 610, 34 if k == 0 else 20, col)
            plain(c, title, x + 120, 622, 32, DARK)
            for j, (nm, a1, a2) in enumerate(rows):
                y = 700 + j * 85
                small(c, nm, x + 40, y, 20, DARK)
                bar(c, t, at + 0.3 + j * 0.15, x + 40, y + 18, 360, 24, a1 if k == 0 else a2, col, WHITE, 0.6)
    ex = [('Classer des emails', 'classer des emails', 'Petit'), ('Extraire un numéro de contrat', 'extraire un numéro', 'Petit'),
          ('Analyser un dossier juridique', 'dossier juridique', 'Grand')]
    for k, (s, kw, m) in enumerate(ex):
        at = S.cue(kw)
        y = 1010 + k * 140
        box(c, t, at, 90, y, 640, 115, s, LIGHT, DARK, 32, 'Medium', 28, 'left')
        chip(c, t, at + 0.3, m, 760, y + 25, RED if m == 'Grand' else DARK, WHITE, 32)


def s3(c, t, S):
    header(c, t, S, 'Le prix', 'Au *million* de tokens')
    a = S.cue('par million')
    card(c, t, a, 90, 540, 900, 330, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Tarifs illustratifs', 140, 600, 22, DARK)
        e, s_ = S.cue("pour l'entrée"), S.cue('pour la sortie')
        for k, (nm, at, fr) in enumerate([('Entrée', e, 0.3), ('Sortie', s_, 0.75)]):
            y = 650 + k * 95
            plain(c, nm, 140, y + 36, 32, DARK)
            bar(c, t, at, 330, y + 10, 610, 36, fr, RED if k else PL, WHITE, 0.8)
        ec = S.cue("L'écart de prix")
        if t >= ec:
            reveal_plain(c, t, ec, "Écart petit / grand : souvent important", 140, 845, 28, RED)
    f = S.cue('Faites le calcul')
    terms = [('Tokens par appel', 'tokens par appel'), ('Appels par jour', 'appels par jour'), ('Prix', 'fois prix')]
    y = 930
    for k, (s, kw) in enumerate(terms):
        at = S.cue(kw)
        box(c, t, at, 190, y + k * 115, 800, 95, s, LIGHT, DARK, 34, 'Medium', 28, 'left')
        if k > 0 and t >= at:
            plain(c, '×', 140, y + k * 115 + 66, 64, RED, 'Medium', 'center')
    es = S.cue('Une estimation')
    box(c, t, es, 190, 1290, 800, 120, '= coût estimé', RED, WHITE, 38, 'Medium', 28, 'up')


def s4(c, t, S):
    header(c, t, S, 'La latence', 'Le *temps* de réponse')
    lg = S.cue('longueur')
    card(c, t, lg, 90, 540, 900, 170, LIGHT, 32, 'left')
    if prog(t, lg, 0.5) > 0.4:
        small(c, 'Réponse longue = attente longue', 140, 600, 22, DARK)
        bar(c, t, lg + 0.2, 140, 630, 300, 30, 1.0, PL, WHITE, 0.4)
        bar(c, t, lg + 0.5, 470, 630, 470, 30, 1.0, RED, WHITE, 0.8)
    st = S.cue('streaming')
    card(c, t, st, 90, 760, 900, 430, LIGHT, 36, 'up')
    if prog(t, st, 0.5) > 0.4:
        small(c, 'Sans streaming', 140, 830, 22, DARK)
        small(c, 'Avec streaming', 140, 1010, 22, RED)
        T = 4.0
        u = clamp((t - st - 0.5) / T)
        # sans streaming : attente puis tout d'un coup
        if u < 0.95:
            icon(c, t, st + 0.5, 'clock', 175, 900, 50, DARK)
            bar(c, t, None, 230, 885, 700 * max(u, 0.02), 26, 1.0, PL, PL)
        else:
            for j in range(2):
                rrect(c, 140, 870 + j * 40, 780 - j * 220, 24, 12, DARK)
        # avec streaming : mots au fil de l'eau
        words = [90, 140, 70, 120, 100, 160, 80, 130, 110, 90]
        x, y = 140, 1050
        for j, wdt in enumerate(words):
            if u >= j / len(words):
                if x + wdt > 940:
                    x, y = 140, y + 44
                rrect(c, x, y, wdt, 26, 13, RED)
                x += wdt + 14
    ch = S.cue('Pour un chat')
    chip(c, t, ch, 'Chat : précieux', 90, 1250, RED, WHITE, 32)
    nu = S.cue('traitement de nuit')
    chip(c, t, nu, 'Traitement de nuit : secondaire', 90 + chip_width('Chat : précieux', 32) + 20, 1250, PLL, DARK, 32)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'On peut *combiner*')
    a = S.cue('trie les demandes')
    box(c, t, S.t0 + 0.4, 90, 560, 280, 130, 'Demandes', LIGHT, DARK, 34)
    arrow(c, t, a - 0.2, 380, 625, 440, 625, DARK, 6)
    box(c, t, a, 450, 540, 540, 170, 'Petit modèle : *tri*', DARK, WHITE, 36)
    sp = S.cue('simples')
    arrow(c, t, sp, 620, 720, 380, 800, DARK, 5, 16)
    box(c, t, sp + 0.2, 90, 810, 400, 130, 'Simples : réponse directe', LIGHT, DARK, 30)
    df = S.cue('demandes difficiles')
    arrow(c, t, df, 820, 720, 820, 800, RED, 5, 16)
    box(c, t, df + 0.2, 590, 810, 400, 130, 'Difficiles : *grand modèle*', LIGHT, DARK, 30)
    ev = S.cue('vos evals')
    card(c, t, S.cue('jamais définitif'), 90, 1010, 900, 410, LIGHT, 36, 'up')
    if t >= S.cue('jamais définitif') + 0.3:
        label(c, t, S.cue('jamais définitif') + 0.2, 'Comparer avant de changer', 140, 1050, PLL, DARK, 22)
        for k, (nm, fr) in enumerate([('Modèle actuel', 0.78), ('Nouveau modèle', 0.84)]):
            y = 1150 + k * 110
            plain(c, nm, 140, y + 30, 30, DARK)
            bar(c, t, ev + k * 0.3, 140, y + 50, 800, 30, fr, RED if k else PL, WHITE, 0.9)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Quel *temps de réponse* l'utilisateur accepte-t-il ?", 'Quel temps'),
        ('Quel *budget* par mois, ou par utilisateur ?', 'Quel budget'),
        ('Quel *niveau de qualité* minimum, mesuré sur vos evals ?', 'quel niveau'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Choisissez le *plus petit modèle* qui passe vos tests.', 'choisissez'),
        ('Coût, latence et qualité se décident *ensemble*.', 'Coût, latence'),
    ], '08 · Prompting, RAG ou fine-tuning')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Le meilleur modèle n'est pas toujours le plus gros. "
        "C'est souvent celui qui est juste assez bon, pour un coût et un délai acceptables.")),
    dict(kind='content', draw=s2, name='Grand ou petit modèle', text=(
        "Les fournisseurs proposent des gammes : de grands modèles, plus capables sur les raisonnements complexes, "
        "et des petits modèles, plus rapides et bien moins chers. "
        "Pour classer des emails ou extraire un numéro de contrat, un petit modèle suffit souvent. "
        "Pour analyser un dossier juridique, un grand modèle fait la différence.")),
    dict(kind='content', draw=s3, name='Le prix au token', text=(
        "Le prix s'exprime en général par million de tokens, avec un tarif pour l'entrée et un autre pour la sortie. "
        "L'écart de prix entre un petit et un grand modèle peut être important. "
        "Faites le calcul : tokens par appel, fois appels par jour, fois prix. "
        "Une estimation simple, faite tôt, évite les mauvaises surprises.")),
    dict(kind='content', draw=s4, name='La latence', text=(
        "La latence, c'est le temps de réponse. Elle dépend de la taille du modèle, et surtout de la longueur de ce qu'il écrit. "
        "Le streaming affiche la réponse au fil de l'eau : l'utilisateur lit dès les premiers mots. "
        "Pour un chat, c'est précieux. Pour un traitement de nuit, la latence compte peu.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, on peut combiner. Un petit modèle trie les demandes, il traite les plus simples, "
        "et seules les demandes difficiles partent vers le grand modèle. "
        "Et le choix n'est jamais définitif : les modèles évoluent vite, et vos evals permettent de comparer avant de changer.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel temps de réponse l'utilisateur accepte-t-il ? "
        "Quel budget par mois, ou par utilisateur ? "
        "Et quel niveau de qualité minimum, mesuré sur vos evals ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : choisissez le plus petit modèle qui passe vos tests. "
        "Coût, latence et qualité se décident ensemble. "
        "Prochaine capsule : prompting, RAG ou fine-tuning, quel levier utiliser, et quand.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
