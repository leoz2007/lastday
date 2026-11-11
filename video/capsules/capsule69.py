from engine import *  # noqa
from engine import _paint  # noqa

NUM = 69
TITLE = 'CALIBRATION'
FULL_TITLE = 'Calibration et incertitude'
SLUG = 'calibration_incertitude'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def pair_bars(c, t, at, x, y, w, conf, ok, lab_conf='Confiance annoncée', lab_ok='Bonnes réponses',
              fg=DARK, ok_fill=RED, bg=WHITE):
    """Deux barres : confiance annoncée, puis taux de bonnes réponses."""
    if t >= at - 0.25:
        small(c, lab_conf, x, y, 18, fg)
    bar(c, t, at, x, y + 18, w, 30, conf, PL, bg, 0.7)
    if t >= at + 0.3 - 0.25:
        small(c, lab_ok, x, y + 88, 18, fg)
    bar(c, t, at + 0.3, x, y + 106, w, 30, ok, ok_fill, bg, 0.7)


def s1(c, t, S):
    opening(c, t, S, CAP, '« Je suis *sûr* » ne prouve *rien*.')
    a = S.cue('je suis sûr')
    card(c, t, a, 90, 830, 900, 200, WHITE, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 170, 930, 70, DARK)
        reveal_plain(c, t, a + 0.2, '« Je suis sûr : le 12 mars. »', 240, 945, 36, DARK, 'Medium')
    fr = S.cue("n'a pas forcément raison")
    if t >= fr:
        icon(c, t, fr, 'cross', 920, 930, 50, RED)
    q = S.cue('sa confiance annoncée')
    card(c, t, q, 90, 1070, 900, 360, WHITE, 32, 'up')
    if prog(t, q, 0.5) > 0.4:
        small(c, 'Exemple illustratif', 140, 1130, 20, DARK)
        pair_bars(c, t, q + 0.2, 140, 1190, 800, 0.95, 0.6)
        if t >= q + 1.0:
            reveal_plain(c, t, q + 1.0, "L'écart", 940, 1395, 28, RED, 'Medium', 'right')


def s2(c, t, S):
    header(c, t, S, 'La calibration', 'Avoir raison *aussi souvent* que prévu')
    m = S.cue('un météorologue')
    card(c, t, m, 90, 540, 900, 380, LIGHT, 32, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'Annonce : 70 % de pluie · 10 jours', 140, 600, 20, DARK)
        pl = S.cue('sept fois sur dix')
        for k in range(10):
            x = 140 + k * 82
            card(c, t, m + 0.2 + k * 0.04, x, 640, 70, 120, WHITE, 14, 'pop')
            if k < 7 and t >= pl:
                dot(c, t, pl + k * 0.06, x + 35, 700, 20, RED)
        if t >= pl:
            small(c, 'Pluie', 140, 810, 18, RED)
            reveal_plain(c, t, pl + 0.5, '7 sur 10 : bien calibré', 940, 880, 30, RED, 'Medium', 'right')
    ts = S.cue('trop sûr de lui')
    card(c, t, ts, 90, 960, 900, 470, LIGHT, 32, 'up')
    if prog(t, ts, 0.5) > 0.4:
        small(c, 'Deux modèles · illustratif', 140, 1020, 20, DARK)
        plain(c, 'Bien calibré', 140, 1080, 30, DARK)
        bar(c, t, ts + 0.2, 140, 1100, 380, 30, 0.7, PL, WHITE, 0.6)
        bar(c, t, ts + 0.4, 560, 1100, 380, 30, 0.7, RED, WHITE, 0.6)
        plain(c, 'Trop sûr de lui', 140, 1220, 30, RED)
        bar(c, t, ts + 0.6, 140, 1240, 380, 30, 0.95, PL, WHITE, 0.6)
        bar(c, t, ts + 0.8, 560, 1240, 380, 30, 0.55, RED, WHITE, 0.6)
        small(c, 'Confiance', 140, 1330, 18, DARK)
        small(c, 'Bonnes réponses', 560, 1330, 18, RED)
        if t >= ts + 1.2:
            icon(c, t, ts + 1.2, 'cross', 900, 1390, 44, RED)


def s3(c, t, S):
    header(c, t, S, 'Le piège', 'La confiance *en mots*')
    words = [('« Je suis certain »', 'je suis certain', 560),
             ('« Probablement »', 'probablement', 760)]
    for s, kw, y in words:
        at = S.cue(kw)
        card(c, t, at, 90, y - 20, 900, 160, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, 'chat', 170, y + 60, 60, DARK)
            reveal_plain(c, t, at + 0.2, s, 240, y + 72, 36, DARK, 'Medium')
    nm = S.cue('pas des mesures fiables')
    if t >= nm:
        for y in (620, 820):
            icon(c, t, nm, 'cross', 910, y, 50, RED)
    g = S.cue('des mots générés')
    card(c, t, g, 90, 1000, 900, 430, LIGHT, 32, 'up')
    if prog(t, g, 0.5) > 0.4:
        small(c, 'Comment la réponse est produite', 140, 1060, 20, DARK)
        toks = ['Je', 'suis', 'certain', ':', 'le', '12', 'mars']
        x = 140
        for k, w in enumerate(toks):
            fill = RED if w == 'certain' else WHITE
            fg = WHITE if w == 'certain' else DARK
            x += chip(c, t, g + 0.2 + k * 0.12, w, x, 1100, fill, fg, 32) + 12
        cr = S.cue('comme le reste')
        if t >= cr:
            reveal_plain(c, t, cr, 'Un mot généré comme les autres', 140, 1290, 34, RED, 'Medium')
            reveal_plain(c, t, cr + 0.3, "Pas la lecture d'une jauge", 140, 1360, 34, DARK, 'Medium')


def s4(c, t, S):
    header(c, t, S, 'De meilleurs signaux', 'Quatre *indices* de doute')
    rows = [('Probabilités des tokens', 'probabilités des tokens'),
            ('Accord entre réponses', "l'accord entre"),
            ('Vérification par les sources', 'par les sources'),
            ('Un second modèle vérificateur', 'un second modèle')]
    for k, (s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 540 + k * 225
        card(c, t, at, 90, y, 900, 200, LIGHT, 32, 'left')
        if prog(t, at, 0.5) < 0.4:
            continue
        small(c, s, 140, y + 55, 20, DARK)
        a = at + 0.2
        if k == 0:
            for j, f in enumerate([0.85, 0.1, 0.05]):
                bar(c, t, a + j * 0.1, 140, y + 85 + j * 34, 500, 22, f, RED if j == 0 else PL, WHITE, 0.6)
            plain(c, 'Disponibles ou non', 940, y + 130, 26, DARK, 'Medium', 'right')
        elif k == 1:
            for j, (w, ok) in enumerate([('12 mars', True), ('12 mars', True), ('3 avril', False)]):
                chip(c, t, a + j * 0.15, w, 140 + j * 200, y + 90, WHITE if ok else RED,
                     DARK if ok else WHITE, 28)
            dv = S.cue('si elles divergent')
            if t >= dv:
                reveal_plain(c, t, dv, 'Méfiance', 940, y + 130, 26, RED, 'Medium', 'right')
        elif k == 2:
            icon(c, t, a, 'doc', 180, y + 125, 60, DARK)
            arrow(c, t, a + 0.2, 230, y + 125, 380, y + 125, DARK, 5, 16)
            icon(c, t, a + 0.4, 'check', 430, y + 125, 50, RED)
            plain(c, 'La réponse est-elle appuyée ?', 940, y + 135, 26, DARK, 'Medium', 'right')
        else:
            icon(c, t, a, 'brain', 180, y + 125, 60, DARK)
            arrow(c, t, a + 0.2, 230, y + 125, 380, y + 125, DARK, 5, 16)
            icon(c, t, a + 0.4, 'brain', 430, y + 125, 60, RED)
            plain(c, 'Relit et vérifie', 940, y + 135, 26, DARK, 'Medium', 'right')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Mesurer, puis *fixer un seuil*')
    ms = S.cue('vos propres cas')
    card(c, t, ms, 90, 540, 900, 330, LIGHT, 32, 'up')
    if prog(t, ms, 0.5) > 0.4:
        small(c, 'Sur vos cas · illustratif', 140, 600, 20, DARK)
        pair_bars(c, t, S.cue('comparez'), 140, 650, 800, 0.85, 0.7)
    sl = S.cue('des seuils')
    card(c, t, sl, 90, 910, 900, 320, LIGHT, 32, 'up')
    if prog(t, sl, 0.5) > 0.4:
        small(c, 'Confiance de chaque cas', 140, 970, 20, DARK)
        rrect(c, 140, 1060, 800, 8, 4, PL)
        pts = [(0.15, 0.0), (0.3, 0.1), (0.55, 0.2), (0.7, 0.3), (0.82, 0.4), (0.92, 0.5)]
        for f, d in pts:
            dot(c, t, sl + 0.2 + d, 140 + 800 * f, 1064, 16, DARK if f > 0.45 else RED)
        rrect(c, 140 + 800 * 0.45 - 3, 1010, 6, 110, 3, RED)
        small(c, 'Seuil', 140 + 800 * 0.45, 1000, 18, RED, align='center')
        hu = S.cue('vers un humain')
        if t >= hu:
            icon(c, t, hu, 'user', 220, 1170, 50, RED)
            reveal_plain(c, t, hu + 0.1, 'Sous le seuil : un humain', 260, 1182, 26, RED, 'Medium')
            reveal_plain(c, t, hu + 0.2, 'Sinon : automatique', 940, 1182, 26, DARK, 'Medium', 'right')
    x = 90
    for s, kw in [('Afficher le doute', 'afficher le doute'), ('Trier pour relecture', 'trier les cas')]:
        at = S.cue(kw)
        card(c, t, at, x, 1270, 440, 160, RED, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, 'eye' if x == 90 else 'search', x + 70, 1350, 50, WHITE)
            plain(c, s, x + 120, 1362, 30, WHITE, 'Medium')
        x += 460


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quel *signal de confiance*, mesuré sur nos cas ?', 'Quel signal'),
        ('Quel *seuil* déclenche le passage à un humain ?', 'Quel seuil'),
        ("Comment *montrer le doute* à l'utilisateur ?", 'Et comment'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Bien calibré : raison *aussi souvent* qu\'annoncé. Un « je suis sûr » ne prouve rien.',
         'un modèle bien calibré'),
        ('Mesurez sur *vos cas*, puis fixez vos *seuils*.', 'mesurez'),
    ], '70 · Bases vectorielles')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle qui vous dit « je suis sûr » n'a pas forcément raison. "
        "Les modèles de langage peuvent être trop sûrs d'eux. "
        "La vraie question : sa confiance annoncée correspond-elle à son taux de bonnes réponses ?")),
    dict(kind='content', draw=s2, name='Être bien calibré', text=(
        "Être bien calibré, c'est avoir raison à peu près aussi souvent que sa confiance l'annonce. "
        "Pensez à un météorologue : quand il annonce soixante-dix pour cent de pluie, "
        "il devrait pleuvoir environ sept fois sur dix. "
        "Un modèle trop sûr de lui annonce beaucoup, et se trompe plus souvent qu'annoncé.")),
    dict(kind='content', draw=s3, name='Le piège de la confiance en mots', text=(
        "Piège classique : la confiance exprimée en mots. "
        "« Je suis certain », ou « probablement », ne sont pas des mesures fiables. "
        "Ce sont des mots générés, comme le reste de la réponse, "
        "pas la lecture d'une jauge interne.")),
    dict(kind='content', draw=s4, name='De meilleurs signaux', text=(
        "Il existe de meilleurs indices. Les probabilités des tokens, ces morceaux de mots, "
        "quand elles sont disponibles. "
        "L'accord entre plusieurs réponses à la même question : si elles divergent, méfiance. "
        "La vérification par les sources. Ou un second modèle, chargé de vérifier.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, mesurez la calibration sur vos propres cas : "
        "comparez la confiance annoncée au taux de bonnes réponses. "
        "Puis fixez des seuils : sous le seuil, on escalade vers un humain. "
        "Vous pouvez aussi afficher le doute, et trier les cas pour la relecture.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel signal de confiance utilise-t-on, "
        "et est-il mesuré sur nos cas ? "
        "Quel seuil déclenche le passage à un humain ? "
        "Et comment montre-t-on le doute à l'utilisateur ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un modèle bien calibré a raison aussi souvent qu'il l'annonce, "
        "et un « je suis sûr » ne prouve rien. Mesurez sur vos cas, puis fixez vos seuils. "
        "Prochaine capsule : les bases vectorielles, pour retrouver vite ce qui se ressemble.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
