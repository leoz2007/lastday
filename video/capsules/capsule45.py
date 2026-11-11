from engine import *  # noqa
from engine import _paint  # noqa

NUM = 45
TITLE = 'PETITS MODÈLES'
FULL_TITLE = 'Petits modèles spécialisés'
SLUG = 'petits_modeles'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def grow_bar(c, t, at, x, base, w, hmax, frac, color):
    """Barre verticale qui pousse depuis sa base."""
    p = ease(prog(t, at, 0.6))
    if p <= 0:
        return
    h = max(w / 2, hmax * frac * p)
    rrect(c, x, base - h, w, h, 10, color)


def dot_grid(c, t, at, x, y, cols, rows, gap, r, color):
    for j in range(rows):
        for i in range(cols):
            dot(c, t, at + (j * cols + i) * 0.02, x + i * gap, y + j * gap, r, color)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un petit modèle peut *égaler* un grand.')
    g = S.cue('égaler un grand')
    p = S.cue('un petit modèle')
    dot(c, t, p + 0.3, 760, 990, 75, RED)
    dot(c, t, g, 320, 990, 150, PL)
    if t >= g + 0.2:
        small(c, 'Grand modèle', 320, 1185, 22, WHITE, align='center')
    if t >= p + 0.4:
        small(c, 'Petit modèle', 760, 1185, 22, WHITE, align='center')
    bar(c, t, g + 0.3, 120, 1215, 400, 26, 0.9, WHITE, DARK)
    bar(c, t, g + 0.5, 560, 1215, 400, 26, 0.88, RED, DARK)
    for s, kw, x in [('Moins cher', 'moins cher', 560), ('Plus vite', 'plus vite', 780)]:
        chip(c, t, S.cue(kw), s, x, 1290, WHITE, DARK, 28)
    sa = S.cue('sur sa tâche')
    if t >= sa:
        reveal_plain(c, t, sa, 'Sur sa tâche seulement', 120, 1330, 30, RED, 'Medium')


def s2(c, t, S):
    header(c, t, S, 'Petit et ajusté', 'Expert d\'un *seul travail*')
    a = S.cue('moins de paramètres')
    card(c, t, a, 90, 540, 900, 300, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Paramètres · schéma illustratif', 140, 600, 20, DARK)
        dot_grid(c, t, a + 0.2, 160, 650, 9, 4, 44, 12, PL)
        small(c, 'Grand', 330, 815, 18, DARK, align='center')
        dot_grid(c, t, a + 0.6, 740, 690, 4, 2, 44, 12, RED)
        small(c, 'Petit', 806, 815, 18, RED, align='center')
    j = S.cue("l'ajuster")
    card(c, t, j, 90, 880, 900, 260, LIGHT, 32, 'up')
    if prog(t, j, 0.5) > 0.4:
        ex = S.cue('vos exemples')
        for k in range(3):
            icon(c, t, ex + k * 0.12, 'doc', 170 + k * 70, 990, 60, DARK)
        if t >= ex:
            small(c, 'Vos exemples', 140, 1100, 18, DARK)
        arrow(c, t, ex + 0.4, 380, 1010, 520, 1010, DARK, 6, 18)
        ep = S.cue('Il devient expert')
        box(c, t, ep, 540, 930, 400, 160, 'Modèle ajusté', RED, WHITE, 34)
    x = 90
    st = S.cue('seul travail')
    for k, s in enumerate(['Classer', 'Extraire', 'Router']):
        chip(c, t, st + 0.3 + k * 0.3, s, x, 1190, PLL, DARK, 34)
        x += chip_width(s, 34) + 24
    if t >= st + 1.2:
        small(c, 'Router : envoyer vers le bon service', 90, 1330, 20, DARK)


def s3(c, t, S):
    header(c, t, S, 'Les gains', 'Moins cher, plus *rapide*')
    cards = [('coin', 'Moins cher', 'coûte moins cher'), ('bolt', 'Plus rapide', 'plus vite'),
             ('lock', 'Chez soi', "l'héberger chez soi")]
    for k, (ic, s, kw) in enumerate(cards):
        at = S.cue(kw)
        x = 90 + k * 310
        hot = k == 2
        card(c, t, at, x, 540, 280, 300, RED if hot else LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if hot else DARK
            icon(c, t, at + 0.1, ic, x + 140, 650, 80, fg)
            plain(c, s, x + 140, 790, 32, fg, 'Medium', 'center')
    r = S.cue('Pour router')
    card(c, t, r, 90, 880, 900, 540, LIGHT, 36, 'up')
    if prog(t, r, 0.5) > 0.4:
        small(c, 'Routage à gros volume', 140, 945, 20, DARK)
        for k in range(8):
            dot(c, t, r + 0.2 + k * 0.05, 160, 1000 + k * 48, 14, PL)
        arrow(c, t, r + 0.5, 190, 1170, 270, 1170, DARK, 6, 16)
        box(c, t, r + 0.6, 290, 1090, 260, 160, 'Petit modèle', RED, WHITE, 30)
        dest = ['Facturation', 'Technique', 'Commercial']
        for k, s in enumerate(dest):
            y = 1000 + k * 125
            arrow(c, t, r + 0.9 + k * 0.15, 560, 1170, 640, y + 50, DARK, 5, 14)
            box(c, t, r + 1.0 + k * 0.15, 660, y, 290, 100, s, WHITE, DARK, 28)


def s4(c, t, S):
    header(c, t, S, 'La contrepartie', 'Il *généralise* moins bien')
    a = S.cue('généralise moins bien')
    card(c, t, a, 90, 540, 900, 560, LIGHT, 36, 'up')
    base, hmax = 1000, 330
    ht = S.cue('Hors de sa tâche')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Qualité · illustratif', 140, 600, 20, DARK)
        groups = [('Sa tâche', a + 0.2, 0.9, 0.88), ('Hors tâche', ht, 0.75, 0.35)]
        for g, (nm, at, fg_, fp) in enumerate(groups):
            x = 200 + g * 400
            grow_bar(c, t, at, x, base, 110, hmax, fg_, PL)
            grow_bar(c, t, at + 0.2, x + 140, base, 110, hmax, fp, RED if g == 1 else DARK)
            if t >= at:
                small(c, nm, x + 125, 1060, 22, DARK, align='center')
        dot(c, t, a + 0.3, 700, 640, 12, PL)
        small(c, 'Grand', 725, 648, 18, DARK)
        dot(c, t, a + 0.3, 840, 640, 12, DARK)
        small(c, 'Petit', 865, 648, 18, DARK)
        ia = S.cue('avec assurance')
        icon(c, t, ia, 'cross', 795, 560 + 440 - hmax * 0.35 - 60, 44, RED)
    v = S.cue('validez le petit modèle')
    card(c, t, v, 90, 1140, 900, 200, RED, 32, 'up')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'check', 180, 1240, 60, WHITE)
        reveal_plain(c, t, v + 0.2, 'Validé sur vos evals', 250, 1254, 40, WHITE)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'La *cascade*')
    a = S.cue('la cascade')
    vol = S.cue('traite le volume')
    box(c, t, a, 260, 620, 320, 170, 'Petit modèle', DARK, WHITE, 34)
    box(c, t, vol, 680, 620, 310, 170, 'Traité', LIGHT, DARK, 34)
    arrow(c, t, vol, 590, 705, 670, 705, DARK, 6, 18)
    hs = S.cue('il hésite')
    arrow(c, t, hs, 420, 800, 420, 950, RED, 6, 18)
    gm = S.cue('passe au grand modèle')
    box(c, t, gm, 260, 960, 320, 170, 'Grand modèle', RED, WHITE, 34)
    box(c, t, gm + 0.3, 680, 960, 310, 170, 'Traité', LIGHT, DARK, 34)
    arrow(c, t, gm + 0.3, 590, 1045, 670, 1045, DARK, 6, 18)
    # flux de demandes
    for i in range(14):
        st = a + 0.3 + i * 0.4
        u = (t - st) / 1.6
        if not 0 < u < 1:
            continue
        hard = i % 5 == 3 and t >= hs
        if u < 0.4:
            x, y = lerp(110, 260, u / 0.4), 705
        elif not hard:
            x, y = lerp(580, 680, (u - 0.4) / 0.6), 705
        else:
            x, y = 420, lerp(790, 960, (u - 0.4) / 0.6)
        c.drawCircle(x, y, 14, _paint(RED if hard else PL))
    if t >= vol:
        small(c, 'Le volume', 835, 830, 20, DARK, align='center')
    if t >= gm + 0.3:
        small(c, 'Les cas difficiles', 835, 1170, 20, RED, align='center')
    pf = S.cue('prix fort')
    card(c, t, pf, 90, 1230, 900, 160, LIGHT, 32, 'left')
    if prog(t, pf, 0.5) > 0.4:
        icon(c, t, pf + 0.1, 'coin', 170, 1310, 56, RED)
        reveal_plain(c, t, pf + 0.2, 'Le prix fort, pour les cas difficiles', 240, 1323, 36, DARK)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('La tâche est-elle *étroite* et *stable* ?', 'La tâche'),
        ("Assez d'*exemples* pour ajuster et évaluer ?", "assez d'exemples"),
        ('Quels cas renvoyer vers un *grand modèle* ?', 'Et quels cas'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Sur une tâche étroite, un petit modèle peut *suffire*.', 'sur une tâche étroite'),
        ('Validez-le sur vos *evals* ; un grand pour les *cas difficiles*.', 'Validez-le'),
    ], '46 · Du POC à la production')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Sur une tâche bien précise, un petit modèle peut égaler un grand. "
        "Pour moins cher, et plus vite. À une condition : qu'il reste sur sa tâche.")),
    dict(kind='content', draw=s2, name='Petit, et parfois ajusté', text=(
        "Un petit modèle a moins de paramètres, ces réglages internes appris pendant l'entraînement. "
        "Il demande donc moins de matériel. On peut aussi l'ajuster, c'est-à-dire poursuivre son entraînement "
        "sur vos exemples, comme des milliers d'emails déjà classés par votre équipe. "
        "Il devient expert d'un seul travail : classer, extraire, ou router, c'est-à-dire aiguiller une demande.")),
    dict(kind='content', draw=s3, name='Moins cher, plus rapide, chez soi', text=(
        "Les gains sont concrets. Chaque requête coûte moins cher, et la réponse arrive plus vite. "
        "Comme il est léger, on peut parfois l'héberger chez soi : les données restent dans votre système d'information. "
        "Pour router des demandes vers le bon service, à très gros volume, ça compte.")),
    dict(kind='content', draw=s4, name='Il généralise moins bien', text=(
        "La contrepartie : il généralise moins bien. Hors de sa tâche, il décroche vite. "
        "Face à une demande d'un type nouveau, il peut se tromper avec assurance, "
        "là où un grand modèle s'adapte mieux. "
        "Alors, validez le petit modèle sur vos evals, vos jeux de cas de test notés, avant de l'adopter.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, un schéma revient souvent : la cascade. Le petit modèle traite le volume. "
        "Quand il hésite, ou qu'un contrôle échoue, la demande passe au grand modèle. "
        "Vous payez le prix fort seulement pour les cas difficiles.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. La tâche est-elle étroite et stable ? "
        "A-t-on assez d'exemples pour ajuster le modèle, et pour l'évaluer ? "
        "Et quels cas renvoie-t-on vers un grand modèle ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : sur une tâche étroite, un petit modèle peut faire aussi bien qu'un grand, "
        "pour moins cher et plus vite. "
        "Validez-le sur vos evals, et gardez un grand modèle pour les cas difficiles. "
        "Prochaine capsule : passer du POC à la production.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
