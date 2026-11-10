from engine import *  # noqa
from engine import _paint  # noqa

NUM = 25
TITLE = 'OPEN OU PROPRIÉTAIRE'
FULL_TITLE = 'Open source ou propriétaire'
SLUG = 'open_source_proprietaire'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def frontier(c, x, y0, y1, color, dash=26, gap=18, width=5):
    """Trait vertical pointillé : la limite de votre système d'information."""
    y = y0
    while y < y1:
        c.drawLine(x, y, x, min(y + dash, y1), _paint(color, width))
        y += dash + gap


def s1(c, t, S):
    opening(c, t, S, CAP, '« Ouvert » ne veut pas dire *open source*.')
    a = S.cue('pas forcément open source')
    card(c, t, a, 90, 880, 900, 420, WHITE, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        rows = [('Poids publiés', 'check', DARK), ("Code et données d'entraînement", None, PL),
                ('Licence à lire', 'eye', RED)]
        for k, (s, ic, col) in enumerate(rows):
            at = a + 0.3 + k * 0.35
            y = 960 + k * 110
            dot(c, t, at, 160, y, 34, col)
            if ic:
                icon(c, t, at + 0.05, ic, 160, y, 40, WHITE)
            elif t >= at:
                plain(c, '?', 160, y + 13, 36, DARK, 'Bold', 'center')
            reveal_plain(c, t, at + 0.1, s, 220, y + 12, 34, DARK, 'Medium')
    ex = S.cue("d'exploitation")
    chip(c, t, ex, "Surtout une question d'exploitation", 540, 1340, RED, WHITE, 30, align='center')


def s2(c, t, S):
    header(c, t, S, 'Poids ouverts', 'Le modèle chez *vous*')
    a = S.cue('téléchargeables')
    card(c, t, a, 90, 560, 300, 190, RED, 30, 'pop')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'brain', 240, 630, 70, WHITE)
        plain(c, 'Poids', 240, 720, 30, WHITE, 'Medium', 'center')
    ch = S.cue('chez vous')
    hb = S.cue('chez un hébergeur')
    arrow(c, t, ch, 400, 620, 590, 600, DARK, 6, 18)
    box(c, t, ch + 0.2, 600, 545, 390, 100, 'Vos serveurs', LIGHT, DARK, 32)
    arrow(c, t, hb, 400, 690, 590, 715, DARK, 6, 18)
    box(c, t, hb + 0.2, 600, 665, 390, 100, 'Un hébergeur choisi', LIGHT, DARK, 32)
    pros = [('Contrôle', 'le contrôle'), ('Données chez vous', 'de vos données'),
            ('Personnalisation', 'fine-tuning')]
    y = 820
    if t >= S.cue('le contrôle'):
        small(c, 'Atouts', 90, y, 22, DARK)
    x = 90
    for k, (s, kw) in enumerate(pros):
        at = S.cue(kw)
        w = chip_width(s, 30)
        if x + w > 990:
            x, y = 90, y + 80
        chip(c, t, at, s, x, y + 20, PLL, DARK, 30)
        x += w + 14
    ex = S.cue("l'exploitation est à vous")
    card(c, t, ex, 90, 1070, 900, 360, LIGHT, 36, 'up')
    if prog(t, ex, 0.5) > 0.4:
        label(c, t, ex + 0.1, 'À votre charge', 140, 1105, RED, WHITE, 22)
        items = [('gear', 'Serveurs', 'serveurs'), ('clock', 'Mises à jour', 'mises à jour'),
                 ('shield', 'Sécurité', 'sécurité'), ('bolt', 'Montée en charge', 'montée en charge')]
        for k, (ic, s, kw) in enumerate(items):
            at = max(ex + 0.2, S.cue(kw))
            cx = 200 + k * 225
            icon(c, t, at, ic, cx, 1260, 60, DARK)
            if t >= at:
                small(c, s, cx, 1350, 18, DARK, align='center')


def s3(c, t, S):
    header(c, t, S, 'Propriétaire', 'Le modèle *via une API*')
    a = S.cue('via une API')
    frontier(c, 560, 560, 990, PL)
    if t >= a:
        small(c, 'Chez vous', 320, 580, 20, DARK, align='center')
        small(c, 'Fournisseur', 800, 580, 20, DARK, align='center')
    box(c, t, a, 90, 640, 400, 160, 'Votre application', LIGHT, DARK, 32)
    ap = S.cue('votre application appelle')
    arrow(c, t, ap, 500, 690, 620, 690, DARK, 6, 18)
    card(c, t, a + 0.3, 630, 620, 360, 200, DARK, 30, 'pop')
    if prog(t, a + 0.3, 0.5) > 0.4:
        icon(c, t, a + 0.4, 'brain', 810, 690, 60, WHITE)
        plain(c, 'Modèle', 810, 785, 30, WHITE, 'Medium', 'center')
    rt = S.cue('rien à opérer')
    arrow(c, t, rt, 620, 760, 500, 760, RED, 6, 18)
    if t >= rt:
        chip(c, t, rt + 0.1, 'Rien à opérer', 630, 850, PLL, DARK, 28)
    ds = S.cue('vos données sortent')
    if t >= ds:
        u = ease(prog(t, ds, 1.2))
        x = lerp(200, 760, u)
        chip(c, t, ds, 'Données', x - 80, 925, RED, WHITE, 28)
    dp = S.cue('vous dépendez')
    card(c, t, dp, 90, 1010, 900, 420, LIGHT, 36, 'up')
    if prog(t, dp, 0.5) > 0.4:
        label(c, t, dp + 0.1, 'Dépendance', 140, 1045, PLL, DARK, 22)
        for k, (ic, s, kw) in enumerate([('coin', 'Ses prix', 'ses prix'),
                                         ('gear', 'Ses changements de version', 'changements de version'),
                                         ('doc', 'Ses conditions', 'ses conditions')]):
            at = S.cue(kw)
            y = 1140 + k * 90
            icon(c, t, at, ic, 165, y + 20, 44, RED)
            reveal_plain(c, t, at + 0.1, s, 215, y + 32, 32, DARK)


def s4(c, t, S):
    header(c, t, S, 'Le vocabulaire', 'Lire la *licence*')
    a = S.cue('au sens strict')
    cols = [('Poids ouverts', 600), ('Open source strict', 850)]
    rows = [('Poids', 'Oui', 'Oui'), ('Code d\'entraînement', 'Pas toujours', 'Oui'),
            ('Données d\'entraînement', 'Pas toujours', 'Décrites')]
    card(c, t, S.cue('Attention au vocabulaire'), 90, 540, 900, 420, LIGHT, 36, 'up')
    if prog(t, S.cue('Attention au vocabulaire'), 0.5) > 0.4:
        for nm, cx in cols:
            small(c, nm, cx, 610, 18, RED if cx == 850 and t >= a else DARK, align='center')
        dn = S.cue('ne sont pas toujours publiés')
        for k, (nm, v1, v2) in enumerate(rows):
            y = 690 + k * 95
            at = S.cue('Open weights') + 0.3 * k if k == 0 else dn + 0.3 * (k - 1)
            reveal_plain(c, t, at, nm, 140, y + 12, 28, DARK)
            chip(c, t, at + 0.1, v1, 600 - chip_width(v1, 24) / 2, y - 22, WHITE if k else PLL, DARK, 24)
            if t >= a:
                chip(c, t, max(a, at) + 0.2, v2, 850 - chip_width(v2, 24) / 2, y - 22, PLL, DARK, 24)
    li = S.cue('certaines licences')
    card(c, t, li, 90, 1000, 900, 430, LIGHT, 36, 'up')
    if prog(t, li, 0.5) > 0.4:
        icon(c, t, li + 0.1, 'doc', 175, 1080, 60, DARK)
        plain(c, 'Licence', 230, 1093, 32, DARK, 'Medium')
        for k, w in enumerate([780, 700]):
            rrect(c, 140, 1140 + k * 46, w, 22, 11, PL)
        cl = [("Usage commercial limité", "l'usage commercial"),
              ("Conditions selon la taille", 'taille')]
        for k, (s, kw) in enumerate(cl):
            at = S.cue(kw)
            y = 1240 + k * 70
            if t >= at:
                rrect(c, 140, y, 10, 50, 5, RED)
            reveal_plain(c, t, at, s, 170, y + 38, 30, RED, 'Medium')
        jr = S.cue('votre juridique')
        chip(c, t, jr, 'Juridique', 990 - 40 - chip_width('Juridique', 26), 1070, RED, WHITE, 26)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Choisir sur des *critères*')
    a = S.cue('des critères')
    if t >= a:
        small(c, 'Poids ouverts', 90, 580, 20, DARK)
        small(c, 'Propriétaire', 990, 580, 20, DARK, align='right')
    crit = [('Données sensibles', 'sensibilité des données', 0.15),
            ('Capacités pointues', 'capacités nécessaires', 0.8),
            ('Équipe pour opérer', "compétences de l'équipe", 0.3),
            ('Coût total', 'coût total', 0.5)]
    for k, (s, kw, pos) in enumerate(crit):
        at = S.cue(kw)
        y = 640 + k * 105
        reveal_plain(c, t, at, s, 90, y + 10, 28, DARK)
        bar(c, t, at, 470, y - 10, 520, 14, 1.0, LIGHT, LIGHT, 0.4)
        dot(c, t, at + 0.2, 470 + 520 * pos, y - 3, 22, RED)
    cb = S.cue('combinent')
    card(c, t, cb, 90, 1060, 900, 370, LIGHT, 36, 'up')
    if prog(t, cb, 0.5) > 0.4:
        ab = S.cue("couche d'abstraction")
        box(c, t, cb + 0.2, 140, 1180, 300, 130, 'Votre produit', WHITE, DARK, 30)
        for k, (s, kw, col, fg) in enumerate([('Propriétaire : cas complexes', 'tâches complexes', DARK, WHITE),
                                              ('Ouvert : données sensibles', 'données sensibles', RED, WHITE)]):
            at = S.cue(kw, nth=1) if k == 0 else S.cue('hébergé en interne')
            y = 1110 + k * 160
            arrow(c, t, at, 450, 1245, 540, y + 65, DARK, 5, 16)
            box(c, t, at + 0.2, 550, y, 400, 130, s, col, fg, 28)
        if t >= ab:
            label(c, t, ab, "Couche d'abstraction", 140, 1120, PLL, DARK, 18)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles données ont le droit de *sortir* de chez vous ?', 'Quelles données'),
        ('Qui *exploitera* le modèle, avec quelles compétences ?', 'Qui exploitera'),
        ('Que dit la *licence* sur votre usage ?', 'Et que dit'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Poids ouverts : *contrôle*, et exploitation à assumer.', 'poids ouverts, c'),
        ('API propriétaire : *simplicité*, et dépendance.', 'API propriétaire'),
        ('Lisez toujours la *licence*.', 'Lisez toujours'),
    ], '26 · Biais et équité')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle « ouvert » n'est pas forcément open source. "
        "Et choisir entre ouvert et propriétaire, c'est surtout une question d'exploitation, pas seulement de qualité.")),
    dict(kind='content', draw=s2, name='Les modèles à poids ouverts', text=(
        "Un modèle à poids ouverts, c'est un modèle dont les paramètres appris, les poids, sont téléchargeables. "
        "Vous l'hébergez chez vous, ou chez un hébergeur de votre choix. "
        "Vous gardez le contrôle de vos données, "
        "et vous pouvez l'adapter, par exemple par fine-tuning sur votre vocabulaire métier. "
        "Mais l'exploitation est à vous : serveurs, mises à jour, sécurité, montée en charge.")),
    dict(kind='content', draw=s3, name='Les modèles propriétaires', text=(
        "Un modèle propriétaire s'utilise via une API, un service en ligne que votre application appelle. "
        "Ils sont souvent les plus capables, et il n'y a rien à opérer. "
        "Mais vous dépendez du fournisseur : ses prix, ses changements de version, ses conditions. "
        "Et vos données sortent de chez vous : le contrat doit le couvrir.")),
    dict(kind='content', draw=s4, name='Open weights et licence', text=(
        "Attention au vocabulaire. Open weights ne veut pas toujours dire open source au sens strict : "
        "le code et les données d'entraînement ne sont pas toujours publiés. "
        "Et certaines licences limitent l'usage commercial, ou posent des conditions selon la taille de l'entreprise. "
        "Faites lire la licence par votre juridique.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, décidez sur des critères : sensibilité des données, capacités nécessaires, "
        "compétences de l'équipe, coût total, exploitation comprise. "
        "Beaucoup d'équipes combinent : un modèle propriétaire pour les tâches complexes, "
        "un modèle ouvert hébergé en interne pour les données sensibles, "
        "derrière une couche d'abstraction.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles données ont le droit de sortir de chez vous ? "
        "Qui exploitera le modèle, et avec quelles compétences ? "
        "Et que dit la licence sur votre usage ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : poids ouverts, c'est le contrôle, avec une exploitation à assumer. "
        "API propriétaire, c'est la simplicité, avec une dépendance. "
        "Lisez toujours la licence. "
        "Prochaine capsule : biais et équité.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
