from engine import *  # noqa
from engine import _paint  # noqa

NUM = 70
TITLE = 'BASES VECTORIELLES'
FULL_TITLE = "Bases vectorielles de l'intérieur"
SLUG = 'bases_vectorielles'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def scatter(n, seed, x0, y0, w, h):
    """Points pseudo-aléatoires reproductibles dans un rectangle."""
    pts, v = [], seed
    for _ in range(n):
        v = (v * 1103515245 + 12345) % 2147483648
        px = x0 + (v % 10007) / 10007 * w
        v = (v * 1103515245 + 12345) % 2147483648
        py = y0 + (v % 10007) / 10007 * h
        pts.append((px, py))
    return pts


def near(p, q, r):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 < r * r


CLOUD = scatter(70, 7, 130, 870, 820, 480)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Une recherche qui ne *regarde pas tout*.')
    a = S.t0 + 0.5
    q = (520, 1100)
    miss = (690, 1150)
    pts = [p for p in CLOUD if not near(p, miss, 40) and not near(p, q, 40)]
    for k, p in enumerate(pts):
        dot(c, t, a + k * 0.012, p[0], p[1], 10, PL)
    pp = S.cue('petite partie')
    seen = [p for p in pts if near(p, (440, 1080), 170)]
    for k, p in enumerate(seen):
        dot(c, t, pp + k * 0.04, p[0], p[1], 13, WHITE)
    dot(c, t, S.cue('votre question'), q[0], q[1], 22, RED)
    if t >= pp + 0.3:
        small(c, 'Examinés', 300, 880, 22, WHITE)
    rp = S.cue('rater parfois')
    dot(c, t, a + 0.4, miss[0], miss[1], 10, PL)
    if t >= rp:
        dot(c, t, rp, miss[0], miss[1], 16, RED)
        ring(c, miss[0], miss[1], 34, RED, 4)
        reveal_plain(c, t, rp + 0.1, 'Le plus proche, manqué', 960, 1420, 30, RED, 'Medium', 'right')


def s2(c, t, S):
    header(c, t, S, 'Le problème', 'Un par un, *trop lent*')
    up = S.cue('un par un')
    card(c, t, up, 90, 540, 900, 300, LIGHT, 32, 'up')
    if prog(t, up, 0.5) > 0.4:
        small(c, 'Comparer la question à chaque vecteur', 140, 600, 20, DARK)
        chip(c, t, up + 0.1, 'Question', 140, 640, RED, WHITE, 28)
        for k in range(13):
            col = DARK if t >= up + 0.3 + k * 0.12 else PL
            rrect(c, 360 + k * 42, 652, 28, 28, 8, col if t >= up + 0.2 else LIGHT)
        if t >= up + 0.3:
            plain(c, '...', 950, 680, 34, DARK, 'Medium', 'right')
        ml = S.cue('des millions')
        if t >= ml:
            reveal_plain(c, t, ml, 'Des millions de comparaisons', 140, 790, 30, RED, 'Medium')
    ia = S.cue('index approximatif')
    card(c, t, ia, 90, 870, 900, 560, LIGHT, 32, 'up')
    if prog(t, ia, 0.5) > 0.4:
        small(c, 'Index approximatif', 140, 930, 20, DARK)
        pts = scatter(40, 3, 160, 980, 760, 360)
        q = (560, 1160)
        for k, p in enumerate(pts):
            if near(p, q, 30):
                continue
            dot(c, t, ia + 0.2 + k * 0.01, p[0], p[1], 10, PL)
        pv = S.cue('plus proches voisins')
        nb = [p for p in pts if near(p, q, 140) and not near(p, q, 30)]
        for k, p in enumerate(nb):
            arrow(c, t, pv + k * 0.08, q[0], q[1], p[0], p[1], DARK, 3, 10)
            dot(c, t, pv + k * 0.08, p[0], p[1], 13, DARK)
        dot(c, t, ia + 0.3, q[0], q[1], 20, RED)
        sg = S.cue('sans garantie')
        if t >= sg:
            reveal_plain(c, t, sg, 'Rapide, sans garantie', 940, 1400, 28, RED, 'Medium', 'right')


GRAPH = [(170, 780), (300, 650), (330, 870), (470, 760), (600, 640), (640, 880),
         (770, 760), (900, 650), (880, 880)]
EDGES = [(0, 1), (0, 2), (1, 3), (2, 3), (1, 4), (3, 4), (3, 5), (4, 6), (5, 6),
         (6, 7), (6, 8), (7, 8), (2, 5)]
PATH = [0, 3, 6, 8]


def s3(c, t, S):
    header(c, t, S, 'Deux idées', 'Un *graphe*, ou des *groupes*')
    g = S.cue('un graphe')
    card(c, t, g, 90, 540, 900, 440, LIGHT, 32, 'up')
    if prog(t, g, 0.5) > 0.4:
        small(c, '1 · Graphe de voisins', 140, 600, 20, DARK)
        for k, (i, j) in enumerate(EDGES):
            arrow(c, t, g + 0.2 + k * 0.03, *GRAPH[i], *GRAPH[j], PL, 4, 0)
        for k, (x, y) in enumerate(GRAPH):
            dot(c, t, g + 0.1 + k * 0.04, x, y, 16, DARK)
        pr = S.cue('de proche en proche')
        for k in range(len(PATH) - 1):
            a, b = GRAPH[PATH[k]], GRAPH[PATH[k + 1]]
            arrow(c, t, pr + k * 0.5, a[0], a[1], b[0], b[1], RED, 6, 18)
            dot(c, t, pr + k * 0.5 + 0.4, b[0], b[1], 18, RED)
        dot(c, t, pr, GRAPH[0][0], GRAPH[0][1], 18, RED)
        if t >= pr:
            small(c, 'Départ', GRAPH[0][0], GRAPH[0][1] + 60, 18, RED, align='center')
        ch = S.cue('demande son chemin')
        if t >= ch:
            small(c, 'Arrivée', GRAPH[8][0], GRAPH[8][1] + 60, 18, RED, align='center')
    pa = S.cue('le partitionnement')
    card(c, t, pa, 90, 1010, 900, 420, LIGHT, 32, 'up')
    if prog(t, pa, 0.5) > 0.4:
        small(c, '2 · Partitionnement en groupes', 140, 1070, 20, DARK)
        gp = S.cue('plus proches de la question')
        groups = [(140, 1100), (345, 1100), (550, 1100), (755, 1100)]
        for k, (x, y) in enumerate(groups):
            hot = k in (1, 2) and t >= gp
            card(c, t, pa + 0.2 + k * 0.1, x, y, 185, 230, PLL if hot else WHITE, 24, 'pop')
            if prog(t, pa + 0.2 + k * 0.1, 0.5) > 0.5:
                for m, (px, py) in enumerate(scatter(6, 11 + k, x + 30, y + 35, 125, 155)):
                    dot(c, t, pa + 0.4 + k * 0.1, px, py, 10, DARK if hot else PL)
        if t >= gp:
            chip(c, t, gp, 'Question', 545, 1352, RED, WHITE, 24, align='center')
            small(c, 'Ignoré', 232, 1385, 18, DARK, align='center')
            small(c, 'Ignoré', 847, 1385, 18, DARK, align='center')


def s4(c, t, S):
    header(c, t, S, 'Les réglages', 'Rappel, vitesse, *mémoire*')
    rp = S.cue('le rappel')
    card(c, t, rp, 90, 540, 900, 470, LIGHT, 32, 'up')
    if prog(t, rp, 0.5) > 0.4:
        fp = S.cue('Fouiller plus')
        p = ease(prog(t, fp, 1.2))
        small(c, 'Plus on fouille (illustratif)', 140, 600, 20, DARK)
        rows = [('Rappel', 'le rappel', lerp(0.6, 0.92, p), RED),
                ('Vitesse', 'la vitesse', lerp(0.85, 0.45, p), DARK),
                ('Mémoire', 'et la mémoire', 0.55, PL)]
        for k, (s, kw, f, col) in enumerate(rows):
            at = S.cue(kw)
            y = 650 + k * 115
            if t >= at - 0.25:
                small(c, s, 140, y + 20, 20, DARK)
            if t >= at - 0.25:
                rrect(c, 140, y + 40, 800, 36, 18, WHITE)
                rrect(c, 140, y + 40, max(36, 800 * f * ease(prog(t, at, 0.8))), 36, 18, col)
        if t >= fp:
            reveal_plain(c, t, fp, 'Meilleur rappel, plus lent', 940, 985, 26, RED, 'Medium', 'right')
    cp = S.cue('compresser')
    card(c, t, cp, 90, 1040, 900, 390, LIGHT, 32, 'up')
    if prog(t, cp, 0.5) > 0.4:
        small(c, 'Compression des vecteurs', 140, 1100, 20, DARK)
        chip(c, t, cp + 0.1, '0,1274  -0,4821  0,9135', 140, 1140, WHITE, DARK, 28)
        if t >= cp + 0.2:
            rrect(c, 140, 1220, 380, 30, 15, PL)
        arrow(c, t, cp + 0.4, 560, 1190, 640, 1190, DARK, 5, 14)
        mp = S.cue('moins de place')
        chip(c, t, mp, '0,1  -0,5  0,9', 670, 1140, WHITE, DARK, 28)
        if t >= mp + 0.1:
            rrect(c, 670, 1220, 120, 30, 15, RED)
        if t >= cp + 0.2:
            small(c, 'Mémoire', 140, 1290, 18, DARK)
        if t >= mp + 0.1:
            small(c, 'Mémoire', 670, 1290, 18, DARK)
        pc = S.cue('un peu de précision')
        if t >= pc:
            reveal_plain(c, t, pc, 'Un peu moins précis', 940, 1390, 28, RED, 'Medium', 'right')
            small(c, 'Valeurs illustratives', 140, 1390, 18, DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Filtres, droits, *suppressions*')
    ft = S.cue('les filtres')
    card(c, t, ft, 90, 540, 900, 520, LIGHT, 32, 'up')
    if prog(t, ft, 0.5) > 0.4:
        small(c, 'Filtrer après la recherche', 140, 600, 20, DARK)
        small(c, 'Dix voisins trouvés', 140, 660, 18, DARK)
        ok = {3}
        pr = S.cue('presque rien')
        for k in range(10):
            x = 170 + k * 80
            dot(c, t, ft + 0.2 + k * 0.05, x, 720, 22, DARK)
        ma = S.cue('mal combiné')
        box(c, t, ma, 140, 780, 800, 90, 'Filtre : vos droits, cette année', WHITE, DARK, 28)
        arrow(c, t, ma + 0.2, 540, 880, 540, 930, DARK, 5, 14)
        for k in range(10):
            x = 170 + k * 80
            if t >= pr:
                dot(c, t, pr + k * 0.03, x, 980, 22, RED if k in ok else PL)
        if t >= pr + 0.3:
            small(c, 'Un seul résultat', 940, 1040, 18, RED, align='right')
    dr = S.cue('les droits doivent')
    card(c, t, dr, 90, 1090, 435, 340, LIGHT, 32, 'up')
    if prog(t, dr, 0.5) > 0.4:
        icon(c, t, dr + 0.1, 'lock', 307, 1210, 80, RED)
        text_block(c, t, dr + 0.2, 'Droits *dans* la recherche', 307, 1340, 30, 'Medium', DARK,
                   RED, maxw=360, align='center', max_lines=2)
    su = S.cue('un document supprimé')
    card(c, t, su, 555, 1090, 435, 340, LIGHT, 32, 'up')
    if prog(t, su, 0.5) > 0.4:
        icon(c, t, su + 0.1, 'doc', 772, 1210, 80, DARK)
        if t >= su + 0.3:
            icon(c, t, su + 0.3, 'cross', 822, 1250, 50, RED)
        text_block(c, t, su + 0.2, 'Supprimé : *introuvable*', 772, 1340, 30, 'Medium', DARK,
                   RED, maxw=360, align='center', max_lines=2)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quel *rappel* mesure-t-on, sur nos données ?', 'Quel rappel'),
        ('Les *droits* sont-ils appliqués dans la recherche ?', 'Les droits'),
        ('Quand une *suppression* disparaît-elle des résultats ?', 'Et en combien'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Des voisins *proches*, pas toujours les plus proches.', 'trouve vite'),
        ('Mesurez le *rappel*, appliquez les *droits* dans la recherche.', 'Mesurez le rappel'),
    ], '71 · Évaluer un agent')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "En général, une base vectorielle ne compare pas votre question à tous ses vecteurs. "
        "Elle n'en examine qu'une petite partie, et accepte de rater parfois le plus proche. "
        "C'est voulu, pour aller vite.")),
    dict(kind='content', draw=s2, name='Le problème : tout comparer est trop lent', text=(
        "Rappel : chaque document devient un vecteur, une liste de nombres qui représente son sens. "
        "Chercher, c'est trouver les vecteurs les plus proches de la question. "
        "Les comparer un par un, sur des millions, est trop lent. "
        "D'où un index approximatif : il cherche les plus proches voisins, vite, sans garantie.")),
    dict(kind='content', draw=s3, name='Deux idées : graphe et groupes', text=(
        "Première idée : un graphe. Chaque vecteur est relié à quelques voisins. "
        "On part d'un point et on avance de proche en proche, comme on demande son chemin. "
        "Deuxième idée : le partitionnement. On range les vecteurs en groupes, "
        "et on ne fouille que les groupes les plus proches de la question.")),
    dict(kind='content', draw=s4, name='Rappel, vitesse, mémoire, compression', text=(
        "Tout se règle entre trois choses : le rappel, c'est-à-dire la part des vrais plus proches retrouvés, "
        "la vitesse, et la mémoire. Fouiller plus de groupes améliore le rappel, mais ralentit. "
        "On peut aussi compresser les vecteurs : ils prennent moins de place, "
        "au prix d'un peu de précision.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, surveillez les filtres sur les métadonnées, comme les droits ou les dates. "
        "Mal combiné, un filtre appliqué après la recherche peut ne laisser presque rien. "
        "Les droits doivent s'appliquer dans la recherche. "
        "Et un document supprimé ne doit plus remonter.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel rappel mesure-t-on, sur nos données ? "
        "Les droits d'accès sont-ils appliqués dans la recherche ? "
        "Et en combien de temps une suppression disparaît-elle des résultats ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : une base vectorielle trouve vite des voisins proches, pas toujours les plus proches. "
        "Mesurez le rappel sur vos données, et appliquez les droits dans la recherche. "
        "Prochaine capsule : évaluer un agent, sur toute une suite d'actions.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
