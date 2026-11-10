from engine import *  # noqa
from engine import _paint  # noqa

NUM = 27
TITLE = 'MESURER LA VALEUR'
FULL_TITLE = 'Mesurer la valeur'
SLUG = 'mesurer_valeur'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def s1(c, t, S):
    opening(c, t, S, CAP, "La démo n'est pas la *valeur*.")
    a = S.cue('démo impressionnante')
    card(c, t, a, 90, 820, 430, 380, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'eye', 305, 940, 90, DARK)
        reveal_plain(c, t, a + 0.2, 'Démo', 305, 1080, 40, DARK, 'Medium', 'center')
        pr = S.cue('ne prouve rien')
        icon(c, t, pr, 'cross', 305, 1145, 50, RED)
    m = S.cue('se mesure')
    card(c, t, m, 560, 820, 430, 380, RED, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        for k, h in enumerate([60, 100, 150, 200]):
            x = 640 + k * 75
            card(c, t, m + 0.2 + k * 0.12, x, 1080 - h, 50, h, WHITE, 14, 'up')
        reveal_plain(c, t, m + 0.4, 'Mesure', 775, 1150, 40, WHITE, 'Medium', 'center')
    av = S.cue('avant le lancement')
    chip(c, t, av, 'Avant le lancement', 540, 1260, WHITE, RED, 36, align='center')


def s2(c, t, S):
    header(c, t, S, 'Les indicateurs', 'Trois mesures *dès le cadrage*')
    rows = [('clock', 'Temps gagné par tâche', 'temps gagné', 0.7),
            ('check', 'Qualité : corrections, evals', 'la qualité', 0.85),
            ('user', 'Adoption : usage réel', "l'adoption", 0.55)]
    for k, (ic, s, kw, fr) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 250
        card(c, t, at, 90, y, 900, 220, LIGHT, 36, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 180, y + 110, 80, RED)
            reveal_plain(c, t, at + 0.15, s, 260, y + 90, 36, DARK)
            bar(c, t, at + 0.3, 260, y + 130, 680, 34, fr, RED if k == 0 else PL, WHITE, 0.9)
    fq = S.cue('à quelle fréquence')
    chip(c, t, fq, 'Qui revient, et à quelle fréquence ?', 90, 1330, DARK, WHITE, 30)


def s3(c, t, S):
    header(c, t, S, 'Et aussi', 'Satisfaction et *coût par tâche*')
    a = S.cue('la satisfaction')
    card(c, t, a, 90, 540, 900, 280, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 190, 680, 90, DARK)
        av = S.cue('un simple avis')
        small(c, 'Avis après usage', 290, 630, 22, DARK)
        for k in range(5):
            dot(c, t, av + k * 0.12, 320 + k * 90, 720, 30, RED if k < 4 else PL)
    co = S.cue('le coût par tâche')
    card(c, t, co, 90, 860, 900, 330, LIGHT, 36, 'up')
    if prog(t, co, 0.5) > 0.4:
        small(c, 'Coût par tâche (exemple)', 140, 920, 22, DARK)
        ap = S.cue('appels au modèle')
        rl = S.cue('temps de relecture')
        bar(c, t, ap, 140, 960, 300, 60, 1.0, PL, WHITE, 0.6)
        bar(c, t, rl, 460, 960, 480, 60, 1.0, RED, WHITE, 0.8)
        if t >= ap:
            small(c, 'Appels au modèle', 140, 1070, 20, DARK)
        if t >= rl:
            small(c, 'Temps de relecture', 460, 1070, 20, RED)
        if t >= rl + 0.6:
            reveal_plain(c, t, rl + 0.6, 'La relecture compte aussi', 140, 1150, 32, DARK)
    ri = S.cue('ne fait rien gagner')
    box(c, t, ri, 90, 1240, 900, 140, 'Plus rapide mais tout à relire : *rien gagné*',
        DARK, WHITE, 34, 'Medium', 30, 'up')


def s4(c, t, S):
    header(c, t, S, 'La référence', "Mesurer *avant*, comparer à l'existant")
    a = S.cue('une référence')
    card(c, t, a, 90, 560, 900, 520, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        label(c, t, a + 0.1, 'Exemple illustratif', 140, 600, PLL, DARK, 22)
        small(c, 'Traiter une réclamation', 140, 700, 22, DARK)
        v = S.cue('vingt minutes')
        reveal_plain(c, t, v, "Aujourd'hui", 140, 790, 32, DARK)
        bar(c, t, v, 360, 760, 580, 44, 1.0, DARK, WHITE, 0.9)
        if t >= v + 0.5:
            plain(c, '20 min', 920, 740, 26, DARK, 'Bold', 'right')
        cp = S.cue("Comparez ensuite")
        reveal_plain(c, t, cp, 'Avec l\'outil', 140, 900, 32, RED)
        bar(c, t, cp, 360, 870, 580, 44, 0.45, RED, WHITE, 0.9)
        if t >= cp + 0.6:
            plain(c, '? min', 640, 850, 26, RED, 'Bold')
        mt = S.cue('mêmes tâches')
        if t >= mt:
            reveal_plain(c, t, mt, 'Mêmes tâches, même mesure', 140, 1030, 30, DARK)
    sa = S.cue('Sans ce chiffre')
    card(c, t, sa, 90, 1130, 900, 200, DARK, 36, 'up')
    if prog(t, sa, 0.5) > 0.4:
        icon(c, t, sa + 0.1, 'target', 190, 1230, 80, RED)
        plain(c, 'Sans point de départ,', 280, 1215, 34, WHITE)
        plain(c, 'pas de preuve', 280, 1265, 34, RED)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "L'*usage réel* d'abord")
    a = S.cue('usage réel')
    card(c, t, a, 90, 540, 900, 460, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Utilisateurs actifs par semaine (exemple)', 140, 600, 22, DARK)
        dl = S.cue('délaissé')
        hs = [0.95, 0.85, 0.6, 0.4, 0.28, 0.2]
        for k, h in enumerate(hs):
            x = 160 + k * 135
            hh = 280 * h
            col = RED if (t >= dl and k >= 3) else PL
            card(c, t, a + 0.2 + k * 0.12, x, 940 - hh, 90, hh, col, 16, 'up')
            if t >= a + 0.2 + k * 0.12:
                small(c, f'S{k + 1}', x + 45, 980, 20, DARK, align='center')
    x = 90
    for s, kw in [('Qui revient', 'qui revient'), ('Quelles tâches', 'sur quelles tâches'),
                  ('Où on abandonne', 'abandonnent')]:
        w = chip(c, t, S.cue(kw), s, x, 1050, DARK, WHITE, 30)
        x += w + 16
    dl = S.cue('délaissé')
    box(c, t, dl, 90, 1170, 900, 150, 'Apprécié en démo, délaissé en un mois : *pas de valeur*',
        WHITE, DARK, 34, 'Medium', 30, 'up')
    if t >= dl + 0.4:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, 1170, 990, 1320), 30, 30), _paint(RED, 4))


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Quelle *tâche* améliorer, et comment la mesure-t-on aujourd'hui ?", 'Quelle tâche'),
        ('Quel *résultat*, à quelle date, signera le succès ?', 'Quel résultat'),
        ('Qui *suit* ces indicateurs après le lancement ?', 'qui suit'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('La valeur se définit *avant* le lancement, avec une *référence*.', 'la valeur se définit'),
        ("Temps, qualité, usage, coût : comparez à l'*existant*.", 'Temps, qualité'),
    ], '28 · Conduite du changement')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Une démo impressionnante ne prouve rien. "
        "La valeur se mesure, et cette mesure se prépare avant le lancement, pas après.")),
    dict(kind='content', draw=s2, name='Les indicateurs', text=(
        "Définissez vos indicateurs dès le cadrage. Le temps gagné par tâche, d'abord. "
        "Puis la qualité : la part de réponses corrigées par les utilisateurs, et vos evals. "
        "Enfin l'adoption : combien de personnes utilisent vraiment l'outil, et à quelle fréquence. Pour chacun, notez dès maintenant comment vous le calculez.")),
    dict(kind='content', draw=s3, name='Satisfaction et coût', text=(
        "Ajoutez la satisfaction : un simple avis après usage suffit pour commencer, une note et un commentaire libre. "
        "Et le coût par tâche, qui inclut les appels au modèle, mais aussi le temps de relecture. "
        "Une tâche plus rapide, mais à relire entièrement, ne fait rien gagner.")),
    dict(kind='content', draw=s4, name='La référence', text=(
        "Surtout, mesurez une référence avant de lancer. "
        "Par exemple, imaginons que traiter une réclamation prenne aujourd'hui vingt minutes. "
        "Sans ce chiffre de départ, impossible de dire si l'outil fait mieux, ni de combien. "
        "Comparez ensuite à l'existant, sur les mêmes tâches, avec la même méthode de mesure.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, l'usage réel compte plus que les déclarations d'intérêt ou l'enthousiasme d'une réunion. "
        "Suivez qui revient, sur quelles tâches, et à quel moment les gens abandonnent. "
        "Un outil apprécié en démo, mais délaissé au bout d'un mois, n'apporte pas de valeur, même s'il a beaucoup plu.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelle tâche voulez-vous améliorer, et comment la mesure-t-on aujourd'hui ? "
        "Quel résultat, à quelle date, dira que c'est un succès ? "
        "Et qui suit ces indicateurs après le lancement ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : la valeur se définit avant le lancement, avec une référence mesurée. "
        "Temps, qualité, usage, satisfaction, coût : comparez toujours à l'existant, chiffres à l'appui. "
        "Prochaine capsule : la conduite du changement, ou comment embarquer vraiment les équipes.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
