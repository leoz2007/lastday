from engine import *  # noqa
from engine import _paint  # noqa

NUM = 37
TITLE = 'IA SUR SITE'
FULL_TITLE = 'IA sur site et en périphérie'
SLUG = 'ia_sur_site_peripherie'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def device(c, t, at, kind, cx, cy, s=100, color=DARK):
    """Pictos d'appareils : serveur, poste de travail, téléphone, carte graphique."""
    p = back(prog(t, at, 0.4))
    if p <= 0:
        return
    c.save()
    c.translate(cx, cy)
    c.scale(p * s / 100, p * s / 100)
    st = _paint(color, 7)
    fl = _paint(color)
    if kind == 'server':
        for k in range(3):
            y = -48 + k * 34
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-44, y, 44, y + 26), 6, 6), st)
            c.drawCircle(-28, y + 13, 5, fl)
            c.drawLine(4, y + 13, 30, y + 13, st)
    elif kind == 'laptop':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-40, -40, 40, 16), 6, 6), st)
        c.drawLine(-54, 32, 54, 32, _paint(color, 10))
        c.drawLine(-12, 16, -16, 32, st)
        c.drawLine(12, 16, 16, 32, st)
    elif kind == 'phone':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-26, -48, 26, 48), 10, 10), st)
        c.drawCircle(0, 34, 5, fl)
        c.drawLine(-10, -36, 10, -36, st)
    elif kind == 'gpu':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-50, -30, 50, 30), 8, 8), st)
        c.drawCircle(-22, 0, 16, st)
        c.drawCircle(22, 0, 16, st)
        for k in range(4):
            x = -36 + k * 24
            c.drawLine(x, 30, x, 42, st)
    elif kind == 'nosignal':
        for k in range(4):
            h = 18 + k * 18
            x = -42 + k * 24
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, 40 - h, x + 14, 40), 4, 4), fl)
        c.drawLine(-44, -40, 44, 44, _paint(RED, 10))
    c.restore()


def pixel_disc(c, cx, cy, r, cell, color):
    """Un disque dessiné en carrés : petites cases = précis, grandes cases = quantifié."""
    n = int(r * 2 / cell) + 1
    x0, y0 = cx - r, cy - r
    for i in range(n):
        for j in range(n):
            px, py = x0 + i * cell + cell / 2, y0 + j * cell + cell / 2
            if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                rrect(c, x0 + i * cell + 1, y0 + j * cell + 1, cell - 2, cell - 2, 2, color)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un modèle peut tourner *chez vous*.')
    f = S.cue('fournisseur distant')
    card(c, t, f, 90, 850, 900, 120, PL, 30, 'up')
    if prog(t, f, 0.5) > 0.4:
        reveal_plain(c, t, f + 0.1, 'Toujours chez un fournisseur distant ?', 140, 925, 34, DARK, 'Medium')
        icon(c, t, f + 0.5, 'cross', 920, 910, 50, RED)
    items = [('server', 'Serveur interne', 'serveur interne'),
             ('laptop', 'Poste de travail', 'poste de travail'),
             ('phone', 'Téléphone', 'téléphone')]
    for k, (kd, s, kw) in enumerate(items):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 1030, 280, 360, WHITE if k < 2 else RED, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            fg = DARK if k < 2 else WHITE
            device(c, t, at + 0.1, kd, x + 140, 1170, 130, fg)
            plain(c, s, x + 140, 1330, 30, fg, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, 'Pourquoi en local', 'Quatre *raisons*')
    x = 90
    for s, kw in [('Sur site : chez vous', 'sur site'), ("Périphérie : sur l'appareil", 'en périphérie')]:
        w = chip(c, t, S.cue(kw), s, x, 540, PLL, DARK, 30)
        x += w + 16
    cells = [('lock', 'Confidentialité', 'Dossier patient', 'La confidentialité'),
             ('nosignal', 'Hors connexion', 'Machine en usine', 'Le hors connexion'),
             ('clock', 'Latence réduite', 'Moins d\'attente', 'latence réduite'),
             ('coin', 'Coût prévisible', 'Matériel, pas à l\'appel', 'coût prévisible')]
    for k, (ic, s, ex, kw) in enumerate(cells):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        y = 660 + (k // 2) * 380
        red = k == 0
        card(c, t, at, x, y, 440, 350, RED if red else LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if red else DARK
            if ic == 'nosignal':
                device(c, t, at + 0.1, ic, x + 220, y + 110, 90, DARK)
            else:
                icon(c, t, at + 0.1, ic, x + 220, y + 110, 90, fg)
            plain(c, s, x + 220, y + 240, 36, fg, 'Medium', 'center')
            small(c, ex, x + 220, y + 300, 20, fg, align='center')


def s3(c, t, S):
    header(c, t, S, 'La contrainte', 'Des modèles *plus petits*')
    m = S.cue('tenir en mémoire')
    card(c, t, m, 90, 540, 900, 370, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, "Mémoire de l'appareil", 140, 600, 20, DARK)
        outline(c, 140, 625, 560, 60, 18, DARK, 5)
        bar(c, t, m + 0.3, 150, 635, 760, 40, 1.0, PL, LIGHT, 0.8)
        if t >= m + 1.0:
            icon(c, t, m + 1.0, 'cross', 930, 655, 40, RED)
            small(c, 'Grand modèle : ne tient pas', 140, 720, 18, DARK)
        cg = S.cue('cartes graphiques')
        device(c, t, cg, 'gpu', 220, 815, 100, DARK)
        if t >= cg:
            reveal_plain(c, t, cg + 0.2, 'Calcul : souvent des cartes graphiques', 300, 828, 28, DARK, 'Medium')
    q = S.cue('quantifiés')
    card(c, t, q, 90, 950, 900, 480, LIGHT, 36, 'up')
    if prog(t, q, 0.5) > 0.4:
        label(c, t, q + 0.1, 'Quantifier', 140, 985, PLL, DARK, 22)
        ph = S.cue('photo plus compressée')
        if t >= q + 0.3:
            pixel_disc(c, 300, 1180, 110, 14, DARK)
            small(c, 'Précis · lourd', 300, 1340, 20, DARK, align='center')
        if t >= ph:
            arrow(c, t, ph, 450, 1180, 600, 1180, DARK, 6, 18)
        if t >= ph + 0.4:
            pixel_disc(c, 780, 1180, 110, 44, RED)
            small(c, 'Léger · moins fin', 780, 1340, 20, RED, align='center')
        mc = S.cue('moins capables')
        if t >= mc:
            reveal_plain(c, t, mc, 'En général, moins capable', 540, 1400, 28, DARK, 'Medium', 'center')


def s4(c, t, S):
    header(c, t, S, "L'exploitation", "C'est *à vous* de l'assurer")
    rows = [('gear', 'Mises à jour', 'mises à jour'), ('shield', 'Sécurité', 'La sécurité'),
            ('eye', 'Supervision', 'la supervision')]
    cv = S.cue("c'est vous")
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 190
        card(c, t, at, 90, y, 900, 160, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 180, y + 80, 64, DARK)
            reveal_plain(c, t, at + 0.15, s, 250, y + 93, 38, DARK, 'Medium')
            if k == 2:
                pts = [0.6, 0.65, 0.62, 0.7, 0.68]
                for j, v in enumerate(pts):
                    dot(c, t, at + 0.3 + j * 0.1, 560 + j * 70, y + 130 - v * 100, 12, PL)
        tag = cv if k == 0 else at + 0.3
        if t >= tag:
            chip(c, t, tag, 'Vous', 980 - chip_width('Vous', 28), y + 55, RED, WHITE, 28)
    pl = S.cue('se planifie')
    card(c, t, pl, 90, 1160, 900, 180, DARK, 32, 'up')
    if prog(t, pl, 0.5) > 0.4:
        icon(c, t, pl + 0.1, 'clock', 190, 1250, 70, WHITE)
        reveal_plain(c, t, pl + 0.2, 'À planifier dès le départ', 270, 1265, 40, WHITE, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Une architecture *mixte*')
    b = S.cue('architecture mixte')
    box(c, t, b, 290, 550, 500, 110, 'Demande', LIGHT, DARK, 36)
    ag = S.cue("règle d'aiguillage")
    arrow(c, t, b + 0.3, 540, 665, 540, 725, DARK, 6, 18)
    card(c, t, b + 0.4, 340, 735, 400, 110, DARK, 30, 'pop')
    if prog(t, b + 0.4, 0.5) > 0.4:
        icon(c, t, b + 0.5, 'gear', 410, 790, 50, WHITE)
        plain(c, 'Aiguillage', 460, 803, 32, WHITE, 'Medium')
    if t >= ag:
        small(c, 'Une règle par demande', 540, 885, 20, RED, align='center')
    lo = S.cue('petit modèle local')
    arrow(c, t, lo, 340, 790, 300, 935, DARK, 6, 18)
    card(c, t, lo + 0.2, 90, 945, 430, 470, LIGHT, 32, 'up')
    if prog(t, lo + 0.2, 0.5) > 0.4:
        device(c, t, lo + 0.3, 'server', 305, 1040, 90, DARK)
        plain(c, 'Petit modèle local', 305, 1145, 32, DARK, 'Medium', 'center')
        chip(c, t, S.cue('simples'), 'Simple', 130, 1180, WHITE, DARK, 28)
        chip(c, t, S.cue('sensibles'), 'Sensible', 300, 1180, RED, WHITE, 28)
        mq = S.cue('masquer les noms')
        if t >= mq:
            icon(c, t, mq, 'doc', 160, 1330, 50, DARK)
            reveal_plain(c, t, mq + 0.1, 'Masquer les noms', 200, 1342, 28, DARK, 'Medium')
    gd = S.cue('grand modèle distant')
    arrow(c, t, gd, 740, 790, 780, 935, DARK, 6, 18)
    card(c, t, gd + 0.2, 560, 945, 430, 470, RED, 32, 'up')
    if prog(t, gd + 0.2, 0.5) > 0.4:
        icon(c, t, gd + 0.3, 'brain', 775, 1040, 90, WHITE)
        plain(c, 'Grand modèle distant', 775, 1145, 32, WHITE, 'Medium', 'center')
        chip(c, t, S.cue('demandes complexes'), 'Complexe', 600, 1180, WHITE, DARK, 28)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles données ne doivent *jamais sortir* ?', 'Quelles données'),
        ('Faut-il fonctionner *sans réseau* ?', 'Le service'),
        ('Qui assure *mises à jour* et supervision ?', 'Et qui assure'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Local : *confidentialité* et autonomie, avec des modèles plus petits.', 'le local apporte'),
        ('Mixez *local* et *distant* selon la tâche.', 'Mixez'),
    ], '38 · Agents en production')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Une IA générative n'a pas besoin de tourner chez un fournisseur distant. "
        "Un modèle peut fonctionner sur un serveur interne, un poste de travail, ou même un téléphone.")),
    dict(kind='content', draw=s2, name='Pourquoi faire tourner le modèle en local', text=(
        "On parle d'IA sur site, ou en périphérie quand le modèle tourne sur l'appareil. "
        "Quatre raisons. La confidentialité : les données ne sortent pas, comme un dossier patient. "
        "Le hors connexion : une machine en usine fonctionne sans réseau. "
        "Une latence réduite : moins d'attente, car rien ne voyage. "
        "Et un coût prévisible : du matériel, plutôt qu'une facture à chaque appel.")),
    dict(kind='content', draw=s3, name='Des modèles plus petits ou quantifiés', text=(
        "La contrainte, c'est le matériel. Le modèle doit tenir en mémoire et calculer vite, "
        "souvent sur des cartes graphiques. On choisit donc des modèles plus petits, ou quantifiés. "
        "Quantifier, c'est stocker chaque nombre du modèle avec moins de précision, "
        "comme une photo plus compressée : plus léger, un peu moins fin. "
        "Ils sont en général moins capables.")),
    dict(kind='content', draw=s4, name="L'exploitation à assumer", text=(
        "Autre contrainte : l'exploitation. Les mises à jour du modèle et des logiciels, c'est vous. "
        "La sécurité des machines aussi. Et la supervision : vérifier que le service répond, "
        "et que la qualité tient dans le temps. Ce travail se planifie dès le départ.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, pensez architecture mixte. Un petit modèle local traite les tâches simples ou sensibles, "
        "comme masquer les noms d'un document. Un grand modèle distant prend les demandes complexes. "
        "Une règle d'aiguillage choisit, demande par demande.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles données ne doivent jamais sortir ? "
        "Le service doit-il fonctionner sans réseau ? "
        "Et qui assure les mises à jour et la supervision ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le local apporte confidentialité, autonomie et coût prévisible, "
        "au prix de modèles plus petits et d'une exploitation à assumer. "
        "Mixez local et distant selon la tâche. "
        "Prochaine capsule : les agents en production, et ce qui les rend fiables.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
