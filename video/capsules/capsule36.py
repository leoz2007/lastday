from engine import *  # noqa
from engine import _paint  # noqa

NUM = 36
TITLE = 'DONNÉES SYNTHÉTIQUES'
FULL_TITLE = 'Données synthétiques'
SLUG = 'donnees_synthetiques'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def doc_grid(c, t, at, x, y, cols, rows, step, size, color, dur=0.03, colors=None):
    """Une grille de documents qui apparaissent l'un après l'autre."""
    for j in range(rows):
        for i in range(cols):
            k = j * cols + i
            col = colors[k] if colors else color
            icon(c, t, at + k * dur, 'doc', x + i * step, y + j * step, size, col)


def generator(c, t, at, cx, cy, r, fill, fg):
    """Le modèle générateur : un disque avec un cerveau."""
    dot(c, t, at, cx, cy, r, fill)
    icon(c, t, at + 0.1, 'brain', cx, cy, r * 1.1, fg)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Vos jeux de test, écrits par un *modèle*.')
    re = S.cue('partir du réel')
    w = S.cue('écrits par un modèle')
    for k in range(3):
        icon(c, t, w + k * 0.12, 'doc', 150, 960 + k * 120, 70, WHITE)
    if t >= w:
        small(c, 'Vrais cas', 150, 1360, 22, WHITE, align='center')
    arrow(c, t, w + 0.4, 220, 1080, 330, 1080, WHITE, 6, 18)
    generator(c, t, w + 0.6, 420, 1080, 80, RED, WHITE)
    if t >= w + 0.6:
        small(c, 'Modèle', 420, 1210, 22, WHITE, align='center')
    arrow(c, t, w + 0.9, 515, 1080, 610, 1080, WHITE, 6, 18)
    doc_grid(c, t, w + 1.1, 655, 920, 5, 4, 74, 50, PL, 0.03)
    if t >= w + 1.3:
        small(c, 'Exemples générés', 820, 1260, 22, WHITE, align='center')
    if t >= re:
        dot(c, t, re, 150, 960, 46, RED)
        icon(c, t, re + 0.05, 'doc', 150, 960, 70, WHITE)
        chip(c, t, re + 0.1, 'Toujours partir du réel', 90, 1390, WHITE, RED, 30)


def s2(c, t, S):
    header(c, t, S, 'Le principe', 'Des exemples *générés*')
    a = S.cue('générés par un modèle')
    generator(c, t, a, 170, 640, 70, RED, WHITE)
    arrow(c, t, a + 0.2, 260, 640, 340, 640, DARK, 6, 18)
    items = [('Cas de test', 'cas de test', 'check'), ('Clients fictifs', 'clients fictifs', 'user'),
             ('Entraînement', "données d'entraînement", 'brain')]
    for k, (s, kw, ic) in enumerate(items):
        at = S.cue(kw)
        x = 360 + k * 215
        card(c, t, at, x, 545, 200, 190, LIGHT, 28, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 100, 610, 50, DARK)
            small(c, s, x + 100, 700, 18, DARK, align='center', tracking=0.5)
    p = S.cue('pseudonymisées')
    card(c, t, p, 90, 790, 900, 600, LIGHT, 36, 'up')
    if prog(t, p, 0.5) > 0.4:
        label(c, t, p + 0.1, 'Pseudonymisation', 140, 820, PLL, DARK, 22)
        rp = S.cue('remplacés')
        small(c, 'Dossier réel', 140, 945, 20, DARK)
        small(c, 'Valeurs fictives', 600, 945, 20, RED)
        rows = [('Nom', 'J. Martin', 'Personne 1'), ('Tél.', '01 23 45 67 89', '00 00 00 00 01'),
                ('Ville', 'Lille', 'Ville A')]
        for k, (f, real, fake) in enumerate(rows):
            y = 990 + k * 110
            at = p + 0.3 + k * 0.15
            if t >= at:
                small(c, f, 140, y + 50, 20, DARK)
            chip(c, t, at, real, 250, y, WHITE, DARK, 30)
            arrow(c, t, rp + k * 0.15, 520, y + 26, 585, y + 26, DARK, 5, 16)
            chip(c, t, rp + 0.2 + k * 0.15, fake, 600, y, RED, WHITE, 30)
        if t >= rp + 0.8:
            icon(c, t, rp + 0.8, 'lock', 160, 1335, 44, RED)
            reveal_plain(c, t, rp + 0.9, 'Les données réelles restent à l\'abri', 200, 1347, 28, DARK)


def s3(c, t, S):
    header(c, t, S, 'Les avantages', 'Volume, vitesse, *cas rares*')
    v = S.cue('cent variantes')
    card(c, t, v, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, v, 0.5) > 0.4:
        small(c, "100 variantes d'une réclamation", 140, 600, 20, DARK)
        for k in range(50):
            i, j = k % 10, k // 10
            dot(c, t, v + 0.2 + k * 0.02, 175 + i * 64, 650 + j * 50, 15, PL)
        m = S.cue('quelques minutes')
        if t >= m:
            icon(c, t, m, 'clock', 910, 905, 44, RED)
            reveal_plain(c, t, m + 0.1, 'Quelques minutes, souvent', 870, 916, 28, RED, 'Medium', 'right')
    r = S.cue('les cas rares')
    card(c, t, r, 90, 990, 900, 430, LIGHT, 36, 'up')
    if prog(t, r, 0.5) > 0.4:
        label(c, t, r + 0.1, 'Cas rares, fabriqués à la demande', 140, 1020, RED, WHITE, 22)
        rare = [('Deux langues mélangées', 'deux langues', 'chat'),
                ('Demande ambiguë', 'ambiguë', 'search'),
                ('Tentative de fraude', 'fraude', 'shield')]
        for k, (s, kw, ic) in enumerate(rare):
            at = min(S.cue(kw), S.cue('deux langues') + k * 0.8)
            y = 1110 + k * 100
            icon(c, t, at, ic, 175, y + 40, 50, RED)
            chip(c, t, at + 0.1, s, 230, y + 8, WHITE, DARK, 32)


def s4(c, t, S):
    header(c, t, S, 'Les risques', 'Trop *lisse*, trop *semblable*')
    u = S.cue('uniformes')
    card(c, t, u, 90, 540, 900, 260, LIGHT, 36, 'up')
    if prog(t, u, 0.5) > 0.4:
        small(c, 'Réel', 140, 610, 20, DARK)
        small(c, 'Généré', 140, 720, 20, RED)
        sizes = [18, 30, 12, 26, 20, 34, 14, 24, 30, 16]
        for k, r in enumerate(sizes):
            dot(c, t, u + 0.1 + k * 0.04, 330 + k * 66, 600, r, DARK)
            dot(c, t, u + 0.5 + k * 0.04, 330 + k * 66, 710, 22, PL)
    b = S.cue('sont recopiés')
    card(c, t, b, 90, 840, 900, 230, LIGHT, 36, 'up')
    if prog(t, b, 0.5) > 0.4:
        generator(c, t, b + 0.1, 190, 955, 60, DARK, WHITE)
        dot(c, t, b + 0.3, 235, 905, 18, RED)
        arrow(c, t, b + 0.3, 270, 955, 350, 955, DARK, 5, 16)
        for k in range(6):
            x = 400 + k * 90
            icon(c, t, b + 0.5 + k * 0.08, 'doc', x, 955, 56, DARK)
            dot(c, t, b + 0.6 + k * 0.08, x + 24, 925, 12, RED)
        small(c, 'Biais et erreurs recopiés', 400, 1045, 20, DARK)
    m = S.cue("l'effet miroir")
    card(c, t, m, 90, 1110, 900, 310, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        label(c, t, m + 0.1, 'Effet miroir', 140, 1140, RED, WHITE, 22)
        generator(c, t, m + 0.2, 200, 1310, 55, PL, DARK)
        small(c, 'Produit', 200, 1395, 18, DARK, align='center')
        arrow(c, t, m + 0.4, 265, 1310, 335, 1310, DARK, 5, 16)
        icon(c, t, m + 0.5, 'doc', 380, 1310, 56, DARK)
        arrow(c, t, m + 0.6, 425, 1310, 495, 1310, DARK, 5, 16)
        generator(c, t, m + 0.7, 560, 1310, 55, PL, DARK)
        small(c, 'Évalue', 560, 1395, 18, DARK, align='center')
        mb = S.cue('meilleurs')
        bar(c, t, mb, 660, 1290, 280, 36, 0.95, RED, WHITE, 0.8)
        if t >= mb + 0.6:
            small(c, 'Score trop beau', 940, 1270, 18, RED, align='right')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Garder un pied dans le *réel*')
    steps = [('Partir de vrais cas', 'partez de vrais cas', 'doc'),
             ('Relecture par des experts', 'relire un échantillon', 'eye'),
             ('Mélanger réel et synthétique', 'mélangez', 'gear')]
    for k, (s, kw, ic) in enumerate(steps):
        at = S.cue(kw)
        y = 560 + k * 150
        card(c, t, at, 90, y, 900, 125, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            dx = -(1 - ease(prog(t, at, 0.5))) * 160
            icon(c, t, at + 0.1, ic, 160 + dx, y + 62, 54, RED)
            plain(c, s, 230 + dx, y + 74, 34, DARK, 'Medium')
            if k == 2:
                bar(c, t, at + 0.3, 760, y + 48, 180, 30, 0.6, DARK, PL, 0.6)
    j = S.cue('jeu de test réel')
    card(c, t, j, 90, 1030, 900, 380, RED, 36, 'up')
    if prog(t, j, 0.5) > 0.4:
        icon(c, t, j + 0.1, 'lock', 180, 1120, 70, WHITE)
        plain(c, 'Jeu de test réel, intouché', 250, 1135, 38, WHITE, 'Medium')
        nv = S.cue('ne sert jamais')
        for k, (s, x) in enumerate([('Pas pour générer', 140), ('Pas pour entraîner', 520)]):
            if t >= nv + k * 0.2:
                chip(c, t, nv + k * 0.2, s, x, 1210, WHITE, RED, 30)
        jp = min(S.cue('juge de paix'), nv + 1.2)
        if t >= jp:
            icon(c, t, jp, 'target', 170, 1340, 50, WHITE)
            reveal_plain(c, t, jp + 0.1, 'La mesure de référence', 220, 1352, 32, WHITE, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('De quels *vrais cas* partent les données générées ?', 'De quels vrais cas'),
        ('Qui *relit* un échantillon, avec quels critères ?', 'Qui relit'),
        ('Le *test réel* reste-t-il bien à l\'écart ?', 'le jeu de test'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le synthétique apporte *volume* et *cas rares*, pas la vérité du terrain.', 'les données synthétiques'),
        ('Partez du réel, faites relire, gardez un *test réel* intouché.', 'Partez du réel'),
    ], '37 · IA sur site et en périphérie')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Vos meilleurs jeux de test peuvent être écrits par un modèle. "
        "À une condition : partir du réel, et ne jamais le perdre de vue.")),
    dict(kind='content', draw=s2, name='Des exemples générés', text=(
        "Les données synthétiques sont des exemples générés par un modèle : des cas de test variés, "
        "des questions de clients fictifs, des données d'entraînement. "
        "Ou des données pseudonymisées : les noms et coordonnées sont remplacés par des valeurs fictives, "
        "pour limiter l'exposition des données personnelles réelles.")),
    dict(kind='content', draw=s3, name='Les avantages', text=(
        "Les avantages : le volume, la vitesse et la couverture. "
        "Il vous faut cent variantes d'une réclamation ? En général, quelques minutes suffisent. "
        "Surtout, on peut fabriquer les cas rares : un client qui mélange deux langues, "
        "une demande ambiguë, une tentative de fraude.")),
    dict(kind='content', draw=s4, name='Les risques', text=(
        "Mais attention. Les exemples générés manquent souvent de réalisme, et sont trop uniformes. "
        "Les biais et les erreurs du modèle générateur sont recopiés. "
        "Et il y a l'effet miroir : quand un modèle évalue des données produites par un modèle similaire, "
        "les résultats paraissent meilleurs qu'ils ne le sont.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, partez de vrais cas, et demandez des variations. "
        "Faites relire un échantillon par des experts métier. Mélangez réel et synthétique. "
        "Et gardez un jeu de test réel, intouché, qui ne sert jamais à générer ni à entraîner : "
        "c'est votre juge de paix.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. De quels vrais cas partent les données générées ? "
        "Qui relit un échantillon, et avec quels critères ? "
        "Et le jeu de test réel reste-t-il bien à l'écart ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : les données synthétiques apportent du volume et des cas rares, pas la vérité du terrain. "
        "Partez du réel, faites relire, et gardez un test réel intouché. "
        "Prochaine capsule : l'IA sur site et en périphérie, quand le modèle tourne chez vous ou sur l'appareil.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
