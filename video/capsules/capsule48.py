from engine import *  # noqa
from engine import _paint  # noqa

NUM = 48
TITLE = 'A/B TESTING'
FULL_TITLE = "A/B testing d'un assistant"
SLUG = 'ab_testing_assistant'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'

# répartition « au hasard » fixe : True = groupe B
SPLIT = [False, True, True, False, True, False, False, True, False, True, True, False]


def s1(c, t, S):
    opening(c, t, S, CAP, 'Le dernier mot revient aux *utilisateurs*.')
    ev = S.cue('Vos evals')
    card(c, t, ev, 90, 830, 900, 130, WHITE, 32, 'up')
    if prog(t, ev, 0.5) > 0.4:
        icon(c, t, ev + 0.1, 'check', 160, 895, 50, DARK)
        reveal_plain(c, t, ev + 0.2, 'Evals : la version B semble meilleure', 220, 908, 32, DARK)
    ab = S.cue('deux versions')
    box(c, t, ab, 90, 1030, 420, 150, 'Version A', PL, DARK, 40)
    box(c, t, ab + 0.2, 570, 1030, 420, 150, 'Version B', RED, WHITE, 40)
    us = S.cue('vos utilisateurs')
    for k in range(8):
        x = 140 + k * 115
        icon(c, t, us + k * 0.08, 'user', x, 1300, 60, WHITE)
    cr = S.cue('conditions réelles')
    if t >= cr:
        reveal_plain(c, t, cr, 'En conditions réelles', 540, 1420, 34, WHITE, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, 'Le principe', 'Deux groupes, *tirés au hasard*')
    a = S.cue('On répartit')
    card(c, t, a, 90, 540, 900, 400, LIGHT, 36, 'up')
    sp = S.cue('Le groupe A')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Répartition au hasard', 140, 600, 20, DARK)
        for k, isb in enumerate(SPLIT):
            x0, y0 = 170 + (k % 6) * 140, 700 + (k // 6) * 100
            u = ease(prog(t, sp, 0.8))
            if isb:
                n = sum(1 for j in range(k) if SPLIT[j])
                x1, y1 = 610 + (n % 3) * 120, 760 + (n // 3) * 110
            else:
                n = sum(1 for j in range(k) if not SPLIT[j])
                x1, y1 = 170 + (n % 3) * 120, 760 + (n // 3) * 110
            x, y = lerp(x0, x1, u), lerp(y0, y1, u)
            col = DARK if t < sp else (RED if isb else DARK)
            icon(c, t, a + 0.2 + k * 0.05, 'user', x, y, 50, col)
        if t >= sp + 0.6:
            small(c, 'Groupe A · version actuelle', 140, 680, 18, DARK)
            small(c, 'Groupe B · nouvelle version', 580, 680, 18, RED)
    vo = S.cue('volontaires')
    card(c, t, vo, 90, 1000, 900, 330, LIGHT, 36, 'up')
    if prog(t, vo, 0.5) > 0.4:
        small(c, 'Le piège des volontaires', 140, 1060, 20, DARK)
        for k in range(3):
            icon(c, t, vo + 0.2 + k * 0.1, 'user', 180 + k * 90, 1160, 56, RED)
        reveal_plain(c, t, vo + 0.4, 'Les plus motivés', 140, 1270, 28, DARK)
        pd = S.cue('profils différents')
        icon(c, t, pd, 'cross', 860, 1160, 60, RED)
        if t >= pd:
            reveal_plain(c, t, pd + 0.2, 'Biais de profil', 940, 1270, 28, RED, 'Medium', 'right')


def s3(c, t, S):
    header(c, t, S, "L'indicateur", 'Choisir *avant* de lancer')
    a = S.cue('un indicateur principal')
    items = [('Taux de résolution', 'taux de résolution'), ('Satisfaction', 'la satisfaction'),
             ('Escalades', "nombre d'escalades")]
    for k, (s, kw) in enumerate(items):
        at = S.cue(kw)
        y = 560 + k * 120
        hot = k == 0
        box(c, t, at, 90, y, 600, 100, s, RED if hot else LIGHT, WHITE if hot else DARK, 32,
            'Medium', 26, 'left')
        if hot:
            chip(c, t, at + 0.3, 'Principal', 720, y + 22, DARK, WHITE, 28)
    if t >= a:
        icon(c, t, a, 'target', 930, 740, 60, RED)
    dv = S.cue('la durée et le volume')
    card(c, t, dv, 90, 940, 900, 490, LIGHT, 36, 'up')
    if prog(t, dv, 0.5) > 0.4:
        small(c, 'Écart entre A et B (illustratif)', 140, 1000, 20, DARK)
        tp = S.cue('trop peu de conversations')
        plain(c, 'Peu de conversations', 140, 1070, 28, DARK)
        # petit volume : estimation qui oscille
        if t >= dv + 0.3:
            ph = (t - dv) * 3.0
            f = 0.5 + 0.3 * math.sin(ph) if t < tp + 2.0 else 0.62
            rrect(c, 140, 1095, 800, 34, 17, WHITE)
            rrect(c, 140, 1095, 800 * f, 34, 17, PL)
        hz = S.cue('du hasard')
        if t >= hz:
            reveal_plain(c, t, hz, 'Peut-être du hasard', 140, 1180, 28, RED, 'Medium')
        plain(c, 'Assez de volume', 140, 1280, 28, DARK)
        bar(c, t, dv + 0.5, 140, 1305, 800, 34, 0.7, RED, WHITE, 1.2)
        if t >= hz:
            reveal_plain(c, t, hz + 0.3, 'Écart stable', 140, 1390, 28, DARK, 'Medium')


def s4(c, t, S):
    header(c, t, S, 'Les pièges', 'Trois pièges *classiques*')
    # 1. regarder trop tôt
    a = S.cue('Regarder trop tôt')
    card(c, t, a, 90, 540, 900, 270, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, '1 · Regarder trop tôt', 140, 600, 20, DARK)
        pts = [0.5, 0.75, 0.3, 0.8, 0.45, 0.6, 0.55, 0.58]
        for k, v in enumerate(pts):
            dot(c, t, a + 0.2 + k * 0.1, 160 + k * 90, 770 - v * 120, 12, DARK)
        ar = S.cue('vous plaît')
        if t >= ar:
            rrect(c, 160 + 3 * 90 - 3, 630, 6, 160, 3, RED)
            reveal_plain(c, t, ar, 'Stop !', 940, 700, 32, RED, 'Medium', 'right')
    # 2. trop d'indicateurs
    m = S.cue('Multiplier les indicateurs')
    card(c, t, m, 90, 840, 900, 280, LIGHT, 32, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, "2 · Trop d'indicateurs", 140, 900, 20, DARK)
        hz = S.cue('par hasard')
        for k in range(20):
            x = 160 + (k % 10) * 62
            y = 950 + (k // 10) * 70
            hot = k == 13 and t >= hz
            rrect(c, x, y, 50, 50, 12, RED if hot else PL) if t >= m + 0.2 + k * 0.03 else None
        if t >= hz:
            reveal_plain(c, t, hz + 0.2, "L'un bouge", 940, 1050, 28, RED, 'Medium', 'right')
    # 3. nouveauté
    n = S.cue("l'effet de nouveauté")
    card(c, t, n, 90, 1150, 900, 280, LIGHT, 32, 'up')
    if prog(t, n, 0.5) > 0.4:
        small(c, '3 · Effet de nouveauté', 140, 1210, 20, DARK)
        it = S.cue('intrigue')
        rt = it + 0.8
        vals = [0.9, 0.75, 0.55, 0.42, 0.38, 0.36]
        for k, v in enumerate(vals):
            at = n + 0.2 + k * 0.12 if k < 2 else it + (k - 2) * 0.15
            h = 130 * v
            if t >= at:
                p = ease(prog(t, at, 0.4))
                rrect(c, 160 + k * 100, 1390 - h * p, 60, h * p, 10, RED if k < 2 else PL)
        if t >= rt:
            reveal_plain(c, t, rt + 0.3, "L'intérêt retombe", 940, 1320, 28, RED, 'Medium', 'right')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Evals *puis* A/B test')
    steps = [('Evals hors ligne', 'Côté produit', LIGHT, DARK), ('A/B test', 'complète', RED, WHITE),
             ('Déploiement', "d'exposer", DARK, WHITE)]
    for k, (s, kw, fill, fg) in enumerate(steps):
        at = S.cue(kw)
        y = 560 + k * 200
        box(c, t, at, 90, y, 560, 140, s, fill, fg, 36)
        if k < 2:
            arrow(c, t, at + 0.3, 370, y + 146, 370, y + 194, DARK, 6, 16)
    fl = S.cue('filtrent')
    if t >= fl:
        icon(c, t, fl, 'shield', 760, 630, 70, DARK)
        reveal_plain(c, t, fl + 0.2, 'Filtrer avant', 690, 735, 28, DARK, 'Medium')
    rb = S.cue('le retour arrière')
    card(c, t, rb, 90, 1180, 900, 250, LIGHT, 36, 'up')
    if prog(t, rb, 0.5) > 0.4:
        small(c, 'Si B se dégrade', 140, 1240, 20, DARK)
        box(c, t, rb + 0.2, 560, 1280, 330, 110, 'Groupe B', PL, DARK, 32)
        rs = S.cue('le rebascule')
        arrow(c, t, rs, 550, 1335, 470, 1335, RED, 6, 18)
        box(c, t, rs + 0.3, 140, 1280, 320, 110, 'Version A', RED, WHITE, 32)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quel *indicateur principal*, fixé avant de lancer ?', "Quel est l'indicateur"),
        ('Quelle *durée* et quel *volume* pour conclure ?', 'Combien de temps'),
        ('Qui peut *arrêter* le test et revenir en arrière ?', 'Et qui peut'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Deux versions, de vrais utilisateurs, *tirés au hasard*.', 'un A/B test'),
        ('Un indicateur choisi avant, assez de volume, et de la *patience*.', 'Un indicateur'),
    ], '49 · Guardrails et modération')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Vos evals disent que la nouvelle version est meilleure. Mais vos utilisateurs n'ont pas encore voté. "
        "L'A/B testing leur donne la parole : on compare deux versions, en conditions réelles.")),
    dict(kind='content', draw=s2, name='Le principe : deux groupes au hasard', text=(
        "On répartit les utilisateurs au hasard, en deux groupes. "
        "Le groupe A garde la version actuelle, le groupe B reçoit la nouvelle. "
        "Le hasard est essentiel. Si l'on donnait la nouvelle version aux seuls volontaires, "
        "les plus motivés, on comparerait des profils différents, pas des versions.")),
    dict(kind='content', draw=s3, name="Choisir l'indicateur, prévoir le volume", text=(
        "Avant de lancer, choisissez un indicateur principal. "
        "Par exemple, le taux de résolution sans conseiller, la satisfaction, ou le nombre d'escalades vers un humain. "
        "Puis fixez la durée et le volume nécessaires. "
        "Sur trop peu de conversations, un écart entre A et B peut n'être que du hasard.")),
    dict(kind='content', draw=s4, name='Trois pièges classiques', text=(
        "Trois pièges reviennent souvent. Regarder trop tôt, et arrêter dès que la courbe vous plaît. "
        "Multiplier les indicateurs : à force d'en suivre vingt, l'un finira par bouger par hasard. "
        "Et l'effet de nouveauté : une nouvelle version intrigue, puis l'intérêt retombe.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, l'A/B testing complète les evals hors ligne, il ne les remplace pas. "
        "Les evals filtrent d'abord, sur des cas de test, avant d'exposer de vrais utilisateurs. "
        "Et prévoyez le retour arrière : si le groupe B se dégrade, on le rebascule sur la version A.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel est l'indicateur principal, décidé avant de lancer ? "
        "Combien de temps, et combien de conversations, pour conclure ? "
        "Et qui peut arrêter le test et revenir en arrière ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un A/B test compare deux versions sur de vrais utilisateurs, tirés au hasard. "
        "Un indicateur choisi avant, assez de volume, et de la patience. "
        "Prochaine capsule : les guardrails et la modération, les garde-fous autour du modèle.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
