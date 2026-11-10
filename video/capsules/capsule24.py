from engine import *  # noqa
from engine import _paint  # noqa

NUM = 24
TITLE = 'COÛTS EN PRODUCTION'
FULL_TITLE = 'Maîtriser les coûts en production'
SLUG = 'couts_production'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def coin_stack(c, t, at, cx, base, n, color, step=0.08):
    """Pile de pièces vue de profil, qui monte pièce par pièce."""
    for k in range(n):
        if t >= at + k * step:
            p = ease(prog(t, at + k * step, 0.3))
            y = base - k * 34 - (1 - p) * 40
            rrect(c, cx - 90, y - 26, 180, 26, 13, color)


def s1(c, t, S):
    opening(c, t, S, CAP, 'À qualité égale, la facture peut *fondre*.')
    a = S.cue('bien moins cher')
    av = S.t0 + 0.6
    coin_stack(c, t, av, 300, 1340, 12, PL, 0.06)
    if t >= av:
        small(c, 'Avant', 300, 1410, 24, WHITE, align='center')
    coin_stack(c, t, a, 780, 1340, 4, RED, 0.12)
    if t >= a:
        small(c, 'Après', 780, 1410, 24, WHITE, align='center')
        arrow(c, t, a + 0.2, 420, 1020, 660, 1180, WHITE, 6, 20)
    # les trois choix, en colonne à droite au-dessus de « Après »
    for k, (s, kw) in enumerate([('Quel modèle', 'quel modèle'), ('Quel contexte', 'quel contexte'),
                                 ('Combien de fois', 'combien de fois')]):
        chip(c, t, S.cue(kw), s, 1000 - chip_width(s, 28), 830 + k * 70, WHITE, DARK, 28)


def s2(c, t, S):
    header(c, t, S, 'Leviers 1 et 2', 'Bon *modèle*, contexte *court*')
    rows = [('Classer un email', 'pour classer', 'Petit modèle', DARK),
            ('Cas difficile', 'cas difficiles', 'Grand modèle', RED)]
    for k, (s, kw, mod, col) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 140
        box(c, t, at, 90, y, 430, 115, s, LIGHT, DARK, 32, 'Medium', 28, 'left')
        arrow(c, t, at + 0.2, 535, y + 57, 600, y + 57, DARK, 6, 18)
        box(c, t, at + 0.35, 615, y, 375, 115, mod, col, WHITE, 32)
    ct = S.cue('raccourcir')
    card(c, t, ct, 90, 880, 900, 550, LIGHT, 36, 'up')
    if prog(t, ct, 0.5) > 0.4:
        small(c, 'Levier 2 · ce qu\'on envoie à chaque appel', 140, 945, 20, DARK)
        tout = S.cue('tout le contrat')
        ex = S.cue('trois extraits')
        plain(c, 'Tout le contrat', 140, 1020, 30, DARK)
        bar(c, t, ct + 0.3, 140, 1045, 800, 40, 1.0, PL, WHITE, 0.8)
        for k in range(8):
            icon(c, t, ct + 0.6 + k * 0.06, 'coin', 170 + k * 70, 1140, 44, DARK)
        plain(c, 'Trois extraits pertinents', 140, 1240, 30, RED if t >= ex else DARK)
        bar(c, t, ex, 140, 1265, 800, 40, 0.22, RED, WHITE, 0.6)
        for k in range(2):
            icon(c, t, ex + 0.3 + k * 0.1, 'coin', 170 + k * 70, 1360, 44, RED)
        if t >= tout:
            small(c, 'Illustratif', 940, 1390, 20, DARK, align='right')


def s3(c, t, S):
    header(c, t, S, 'Leviers 3 et 4', 'Mettre en *cache*, écrire *court*')
    q = S.cue("horaires d'ouverture")
    box(c, t, q, 90, 560, 380, 120, "Horaires d'ouverture ?", LIGHT, DARK, 30)
    arrow(c, t, q + 0.3, 480, 620, 570, 620, DARK, 6, 18)
    dc = S.cue('déjà calculée')
    card(c, t, q + 0.4, 580, 545, 410, 150, RED, 30, 'pop')
    if prog(t, q + 0.4, 0.5) > 0.4:
        icon(c, t, q + 0.5, 'db', 650, 620, 60, WHITE)
        plain(c, 'Cache', 720, 610, 32, WHITE, 'Medium')
        if t >= dc:
            reveal_plain(c, t, dc, 'Réponse prête', 720, 655, 26, WHITE, 'Medium')
    cp = S.cue('cache de prompt')
    card(c, t, cp, 90, 740, 900, 300, LIGHT, 36, 'up')
    if prog(t, cp, 0.5) > 0.4:
        small(c, 'Le même début, à chaque appel', 140, 800, 20, DARK)
        fx = S.cue('la partie fixe')
        for k in range(2):
            y = 840 + k * 80
            bar(c, t, cp + 0.2 + k * 0.2, 140, y, 520, 44, 1.0, PL, WHITE, 0.5)
            bar(c, t, cp + 0.4 + k * 0.2, 680, y, 260, 44, 1.0, DARK, WHITE, 0.5)
        if t >= fx:
            reveal_plain(c, t, fx, 'Partie fixe : en cache', 140, 1010, 26, RED, 'Medium')
            reveal_plain(c, t, fx + 0.2, 'Question', 940, 1010, 26, DARK, 'Medium', 'right')
    ln = S.cue('limiter la longueur')
    card(c, t, ln, 90, 1090, 900, 340, LIGHT, 36, 'up')
    if prog(t, ln, 0.5) > 0.4:
        small(c, 'Longueur de la réponse', 140, 1150, 20, DARK)
        plain(c, 'Sans limite', 140, 1215, 28, DARK)
        bar(c, t, ln + 0.2, 340, 1190, 600, 34, 1.0, PL, WHITE, 1.0)
        plain(c, 'Avec limite', 140, 1290, 28, RED)
        bar(c, t, ln + 0.5, 340, 1265, 600, 34, 0.4, RED, WHITE, 0.6)
        so = S.cue('la sortie')
        if t >= so:
            reveal_plain(c, t, so, 'La sortie coûte souvent plus cher', 140, 1380, 28, RED, 'Medium')


def s4(c, t, S):
    header(c, t, S, 'Leviers 5 et 6', 'Quotas et *traitement par lots*')
    q = S.cue('quotas par utilisateur')
    fr = [0.35, 1.0, 0.6]
    ab = S.cue('qui s\'emballent')
    for k, f in enumerate(fr):
        at = q + k * 0.2
        y = 600 + k * 100
        icon(c, t, at, 'user', 130, y + 40, 60, RED if k == 1 and t >= ab else DARK)
        bar(c, t, at + 0.1, 190, y + 25, 560, 30, f, RED if k == 1 else PL, LIGHT, 1.0)
    if t >= ab:
        chip(c, t, ab, 'Quota atteint', 775, 675, RED, WHITE, 28)
    if t >= q:
        small(c, 'Appels du jour', 190, 590, 20, DARK)
    lo = S.cue('par lots')
    card(c, t, lo, 90, 900, 900, 530, LIGHT, 36, 'up')
    if prog(t, lo, 0.5) > 0.4:
        small(c, 'Pas besoin de temps réel', 140, 960, 20, DARK)
        rg = S.cue('on regroupe')
        tk = S.cue('tickets de la veille')
        for k in range(8):
            i, j = k % 4, k // 4
            at = tk + k * 0.08
            x0, y0 = 160 + i * 90, 1020 + j * 110
            if t >= rg:
                u = ease(prog(t, rg + k * 0.05, 0.7))
                x0, y0 = lerp(x0, 600 + i * 80, u), lerp(y0, 1060 + j * 100, u)
            icon(c, t, at, 'doc', x0 + 30, y0 + 40, 56, DARK)
        if t >= rg:
            card(c, t, rg + 0.5, 560, 1250, 380, 120, RED, 28, 'pop')
            if prog(t, rg + 0.5, 0.5) > 0.4:
                icon(c, t, rg + 0.6, 'clock', 620, 1310, 50, WHITE)
                plain(c, 'Lot de nuit', 670, 1322, 32, WHITE, 'Medium')
        mc = S.cue('moindre coût')
        if t >= mc:
            reveal_plain(c, t, mc, 'Souvent moins cher', 160, 1340, 28, RED, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Le coût *par utilisateur*')
    a = S.cue('coût par utilisateur')
    card(c, t, a, 90, 540, 900, 520, LIGHT, 36, 'up')
    pg = S.cue('une poignée')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Coût par utilisateur (illustratif)', 140, 600, 20, DARK)
        vals = [0.95, 0.7, 0.18, 0.14, 0.11, 0.09, 0.07]
        for k, v in enumerate(vals):
            y = 640 + k * 50
            col = RED if (k < 2 and t >= pg) else PL
            icon(c, t, a + 0.2 + k * 0.08, 'user', 165, y + 16, 34, DARK)
            bar(c, t, a + 0.3 + k * 0.08, 210, y + 4, 730, 26, v, col, WHITE, 0.7)
        if t >= pg:
            reveal_plain(c, t, pg + 0.3, 'Une poignée pèse lourd', 140, 1025, 28, RED, 'Medium')
    al = S.cue('une alerte')
    card(c, t, al, 90, 1110, 900, 320, LIGHT, 36, 'up')
    if prog(t, al, 0.5) > 0.4:
        small(c, 'Budget du mois', 140, 1170, 20, DARK)
        bar(c, t, al + 0.2, 140, 1210, 800, 44, 0.84, RED, WHITE, 1.2)
        lx = 140 + 800 * 0.8
        if t >= al + 0.4:
            rrect(c, lx - 3, 1195, 6, 74, 3, DARK)
            small(c, 'Seuil d\'alerte', lx, 1305, 20, DARK, align='center')
        if t >= al + 1.4:
            icon(c, t, al + 1.4, 'bolt', 180, 1370, 44, RED)
            reveal_plain(c, t, al + 1.4, 'Alerte envoyée', 220, 1382, 30, RED, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quel *coût par utilisateur* le modèle économique tolère-t-il ?', 'Quel coût'),
        ('Quelles demandes peuvent passer *par lots* ?', 'Quelles demandes'),
        ('Qui est *alerté* si la facture dérape ?', 'Et qui est'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le coût se *pilote*, levier par levier.', 'le coût se pilote'),
        ('Mesurez-le *par utilisateur*, agissez sur ce qui pèse le plus.', 'Mesurez-le'),
    ], '25 · Open source ou propriétaire')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Le même assistant, à qualité égale, peut coûter bien moins cher. "
        "Tout se joue dans quelques choix : quel modèle, quel contexte, et combien de fois on l'appelle.")),
    dict(kind='content', draw=s2, name='Le bon modèle, un contexte court', text=(
        "Premier levier : choisir le modèle par tâche. Un petit modèle pour classer, un grand pour les cas difficiles. "
        "Deuxième levier : raccourcir les prompts et le contexte. Chaque token envoyé se paie, à chaque appel. "
        "Par exemple, envoyer trois extraits pertinents plutôt que tout le contrat.")),
    dict(kind='content', draw=s3, name='Cache et longueur des réponses', text=(
        "Troisième levier : la mise en cache. Une question fréquente, comme les horaires d'ouverture, "
        "peut recevoir une réponse déjà calculée. "
        "Certains fournisseurs proposent aussi un cache de prompt : la partie fixe, répétée à chaque appel, est facturée moins cher. "
        "Quatrième levier : limiter la longueur des réponses, car la sortie coûte souvent plus cher que l'entrée.")),
    dict(kind='content', draw=s4, name='Quotas et traitement par lots', text=(
        "Cinquième levier : des quotas par utilisateur. Un plafond d'appels par jour protège des abus et des boucles qui s'emballent. "
        "Sixième levier : le traitement par lots, quand le temps réel n'est pas nécessaire. "
        "Pour résumer les tickets de la veille, on regroupe les demandes et on les traite la nuit, souvent à moindre coût.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, suivez le coût par utilisateur, pas seulement la facture globale. "
        "Souvent, une poignée d'usages pèse très lourd : c'est là qu'on agit en premier. "
        "Et prévoyez une alerte quand le budget du mois approche de sa limite.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel coût par utilisateur votre modèle économique peut-il supporter ? "
        "Quelles demandes peuvent attendre un traitement par lots ? "
        "Et qui est alerté si la facture dérape ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le coût se pilote, levier par levier. "
        "Mesurez-le par utilisateur, et agissez d'abord sur les usages qui pèsent le plus. "
        "Prochaine capsule : open source ou propriétaire, comment choisir son modèle.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
