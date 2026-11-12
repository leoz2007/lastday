from engine import *  # noqa
from engine import _paint  # noqa

NUM = 35
TITLE = 'FINE-TUNING EFFICACE'
FULL_TITLE = 'Fine-tuning efficace (LoRA)'
SLUG = 'fine_tuning_lora'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def param_grid(c, t, at, x, y, cols, rows, step, r, color, hot=None, hot_at=None, dur=0.02):
    """Grille de points : les paramètres du modèle. hot = couleur après hot_at (vague)."""
    for j in range(rows):
        for i in range(cols):
            k = j * cols + i
            col = color
            if hot is not None and hot_at is not None and t >= hot_at + k * dur:
                col = hot
            dot(c, t, at + k * 0.008, x + i * step, y + j * step, r, col)


def model_block(c, t, at, x, y, w, h, fill, grid_col, locked=False, lock_at=None, lock_col=DARK,
                cols=8, rows=4, mode='up'):
    """Bloc « modèle » : carte + grille de paramètres + cadenas éventuel."""
    card(c, t, at, x, y, w, h, fill, 32, mode)
    if prog(t, at, 0.5) > 0.4:
        gw = w - (170 if locked else 80)
        step = min(gw / max(1, cols - 1), (h - 80) / max(1, rows - 1))
        gx = x + 40 + (gw - step * (cols - 1)) / 2 if locked else x + (w - step * (cols - 1)) / 2
        gy = y + (h - step * (rows - 1)) / 2
        param_grid(c, t, at + 0.1, gx, gy, cols, rows, step, min(12, step * 0.28), grid_col)
        if locked and lock_at is not None:
            dot(c, t, lock_at, x + w - 50, y + 50, 34, lock_col)
            icon(c, t, lock_at + 0.1, 'lock', x + w - 50, y + 50, 40, fill)


def s1(c, t, S):
    opening(c, t, S, CAP, "Inutile de tout *réentraîner*.")
    a = S.cue('spécialiser')
    model_block(c, t, a, 90, 860, 600, 460, PL, DARK, True, S.cue('le figer'), DARK, 8, 5)
    fg = S.cue('le figer')
    if t >= fg:
        small(c, 'Modèle gelé', 390, 1400, 24, WHITE, align='center')
    p = S.cue('petite pièce')
    arrow(c, t, p, 990, 1090, 730, 1090, WHITE, 6, 20)
    card(c, t, p + 0.2, 740, 1010, 250, 160, RED, 30, 'right')
    if prog(t, p + 0.2, 0.5) > 0.4:
        icon(c, t, p + 0.3, 'bolt', 865, 1070, 50, WHITE)
        plain(c, 'Adaptateur', 865, 1140, 28, WHITE, 'Medium', 'center')
    if t >= p + 0.8:
        small(c, 'Seule pièce entraînée', 865, 1215, 20, WHITE, align='center')


def s2(c, t, S):
    header(c, t, S, 'Fine-tuning complet', 'Tout *réentraîner*, tout stocker')
    a = S.cue('poursuivre')
    card(c, t, a, 90, 540, 900, 380, LIGHT, 36, 'up')
    tp = S.cue('tous ses paramètres')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Les paramètres du modèle', 140, 600, 20, DARK)
        param_grid(c, t, a + 0.1, 160, 660, 14, 4, 58, 14, PL, RED, tp, 0.015)
        if t >= tp + 0.9:
            reveal_plain(c, t, tp + 0.9, 'Tous modifiés', 940, 600, 26, RED, 'Medium', 'right')
    ca = S.cue('beaucoup de calcul')
    card(c, t, ca, 90, 960, 900, 150, LIGHT, 32, 'left')
    if prog(t, ca, 0.5) > 0.4:
        icon(c, t, ca + 0.1, 'bolt', 160, 1035, 56, RED)
        small(c, 'Calcul · illustratif', 230, 1010, 20, DARK)
        bar(c, t, ca + 0.2, 230, 1035, 700, 36, 1.0, RED, WHITE, 1.2)
    cp = S.cue('une copie entière')
    if t >= cp:
        small(c, 'Une copie complète par variante', 90, 1170, 20, DARK)
    for k, s in enumerate(['Variante A', 'Variante B', 'Variante C']):
        x = 90 + k * 310
        at = cp + 0.2 + k * 0.25
        model_block(c, t, at, x, 1200, 280, 160, PL, DARK, cols=6, rows=2, mode='pop')
        if t >= at + 0.3:
            small(c, s, x + 140, 1405, 20, DARK, align='center')


def s3(c, t, S):
    header(c, t, S, 'LoRA', 'Geler, puis *ajouter*')
    g = S.cue('le modèle est gelé')
    model_block(c, t, g, 90, 540, 560, 300, PL, DARK, True, g + 0.4, DARK, 8, 3)
    ad = S.cue('adaptateurs')
    arrow(c, t, ad, 830, 690, 665, 690, DARK, 6, 18)
    card(c, t, ad + 0.1, 840, 610, 150, 160, RED, 28, 'right')
    if prog(t, ad + 0.1, 0.5) > 0.4:
        icon(c, t, ad + 0.2, 'bolt', 915, 690, 50, WHITE)
    if t >= ad + 0.5:
        small(c, 'Adaptateur', 915, 810, 20, DARK, align='center')
    fr = S.cue('une fraction')
    card(c, t, fr, 90, 880, 900, 250, LIGHT, 36, 'up')
    if prog(t, fr, 0.5) > 0.4:
        small(c, 'Taille à stocker · illustratif', 140, 935, 20, DARK)
        plain(c, 'Modèle', 140, 1000, 28, DARK)
        bar(c, t, fr + 0.2, 380, 975, 560, 32, 1.0, PL, WHITE, 0.8)
        plain(c, 'Adaptateur', 140, 1080, 28, RED)
        bar(c, t, fr + 0.6, 380, 1055, 560, 32, 0.06, RED, WHITE, 0.5)
    pc = S.cue('un par client')
    if t >= pc:
        small(c, 'Un seul modèle de base', 90, 1190, 20, DARK)
    model_block(c, t, pc, 90, 1220, 420, 200, PL, DARK, True, pc + 0.3, DARK, 6, 2, 'up')
    names = ['Client A', 'Client B', 'Tâche : résumé']
    for k, s in enumerate(names):
        at = pc + 0.4 + k * 0.25
        y = 1220 + k * 70
        active = (k == int(((t - pc - 1.5) / 0.9)) % 3) if t >= pc + 1.5 else k == 0
        fill = RED if active else PLL
        fg = WHITE if active else DARK
        chip(c, t, at, s, 640, y, fill, fg, 28, h=56)
        if active and t >= pc + 0.5:
            arrow(c, t, None, 630, y + 28, 525, 1320, RED, 4, 14)


def s4(c, t, S):
    header(c, t, S, 'Ce que ça apprend', 'La *forme*, pas les faits')
    b = S.cue('apprend bien')
    card(c, t, b, 90, 540, 900, 300, LIGHT, 36, 'up')
    if prog(t, b, 0.5) > 0.4:
        label(c, t, b + 0.1, 'Apprend bien', 140, 570, RED, WHITE, 22)
        items = [('Style', 'un style'), ('Format', 'un format'), ('Vocabulaire', 'vocabulaire'),
                 ('Tâche répétitive', 'tâche répétitive')]
        x, y = 140, 660
        for k, (s, kw) in enumerate(items):
            w = chip_width(s, 32)
            if x + w > 950:
                x, y = 140, y + 80
            chip(c, t, S.cue(kw), s, x, y, WHITE, DARK, 32)
            x += w + 16
    ex = S.cue('comptes rendus')
    card(c, t, ex, 90, 870, 900, 220, LIGHT, 32, 'left')
    if prog(t, ex, 0.5) > 0.4:
        icon(c, t, ex + 0.1, 'doc', 170, 980, 80, DARK)
        small(c, 'Compte rendu de sinistre', 250, 925, 20, DARK)
        for k, (lab, w) in enumerate([('Faits', 460), ('Dommages', 380), ('Suite', 420)]):
            y = 950 + k * 42
            if t >= ex + 0.3 + k * 0.2:
                rrect(c, 250, y, 150, 26, 13, RED)
                bar(c, t, ex + 0.3 + k * 0.2, 420, y, w, 26, 1.0, PL, LIGHT, 0.5)
    m = S.cue('apprend mal')
    card(c, t, m, 90, 1120, 580, 300, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        label(c, t, m + 0.1, 'Apprend mal', 140, 1150, DARK, WHITE, 22)
        small(c, 'Les faits qui changent', 140, 1260, 20, DARK)
        for k, (s, kw) in enumerate([('Tarifs', 'tarifs'), ('Stock', 'stock')]):
            at = S.cue(kw)
            x = 140 + k * 220
            w = chip(c, t, at, s, x, 1290, WHITE, DARK, 30)
            icon(c, t, at + 0.2, 'cross', x + w + 28, 1320, 34, RED)
    r = S.cue("c'est le rôle")
    arrow(c, t, r, 680, 1270, 740, 1270, DARK, 6, 18)
    card(c, t, r + 0.15, 750, 1120, 240, 300, RED, 36, 'pop')
    if prog(t, r + 0.15, 0.5) > 0.4:
        icon(c, t, r + 0.25, 'search', 870, 1230, 70, WHITE)
        plain(c, 'RAG', 870, 1345, 44, WHITE, 'Medium', 'center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Des *exemples*, puis des *evals*')
    d = S.cue('les données')
    if t >= d:
        small(c, "Les exemples d'entraînement", 90, 570, 20, DARK)
    for k, (s, kw, ic) in enumerate([('De qualité', 'de qualité', 'check'),
                                     ('Représentatifs', 'représentatifs', 'target'),
                                     ('Relus', 'relus par le métier', 'eye')]):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 600, 280, 190, LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 665, 56, RED)
            plain(c, s, x + 140, 755, 28, DARK, 'Medium', 'center')
    sa = S.cue('surapprentissage')
    card(c, t, sa, 90, 830, 900, 160, LIGHT, 32, 'left')
    if prog(t, sa, 0.5) > 0.4:
        icon(c, t, sa + 0.1, 'doc', 160, 910, 56, DARK)
        arrow(c, t, sa + 0.3, 210, 910, 290, 910, DARK, 5, 16)
        icon(c, t, sa + 0.5, 'chat', 340, 910, 56, RED)
        reveal_plain(c, t, sa + 0.6, 'Il récite ses exemples', 400, 922, 32, DARK)
    ev = S.cue('avec vos evals')
    card(c, t, ev, 90, 1030, 900, 390, LIGHT, 36, 'up')
    if prog(t, ev, 0.5) > 0.4:
        label(c, t, ev + 0.1, 'Evals · chiffres illustratifs', 140, 1060, PLL, DARK, 22)
        small(c, 'Avant', 560, 1160, 20, DARK)
        small(c, 'Après', 780, 1160, 20, RED)
        crit = [('Tâche visée', 0.55, 0.9), ('Capacités générales', 0.85, 0.6)]
        ap = S.cue('Mesurez-les')
        for j, (nm, f1, f2) in enumerate(crit):
            y = 1200 + j * 95
            plain(c, nm, 140, y + 28, 28, DARK)
            bar(c, t, ev + 0.3 + j * 0.2, 560, y + 4, 190, 30, f1, PL, WHITE, 0.6)
            bar(c, t, ap + j * 0.3, 780, y + 4, 190, 30, f2, RED, WHITE, 0.6)
        if t >= ap + 0.9:
            small(c, 'À surveiller', 940, 1395, 20, RED, align='right')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Le besoin porte-t-il sur la *forme*, ou sur des faits qui changent ?', 'Le besoin porte'),
        ('Avez-vous des *exemples relus* et représentatifs ?', 'Avez-vous'),
        ('Le modèle visé *permet-il* un fine-tuning ?', 'le modèle visé'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('LoRA gèle le modèle et entraîne une *petite pièce*, légère et échangeable.', 'LoRA gèle'),
        ('Pour le style et le format, oui. Pour les *faits*, le RAG.', 'Idéal pour'),
    ], '36 · Données synthétiques')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Pour spécialiser un modèle, inutile de le réentraîner en entier. "
        "On peut le figer, et n'entraîner qu'une petite pièce ajoutée.")),
    dict(kind='content', draw=s2, name='Le fine-tuning complet', text=(
        "Le fine-tuning, ou ajustement fin, consiste à poursuivre l'entraînement d'un modèle sur vos exemples. "
        "En version complète, on modifie tous ses paramètres, ces réglages internes. "
        "C'est lourd : beaucoup de calcul, et une copie entière du modèle à stocker pour chaque variante.")),
    dict(kind='content', draw=s3, name='LoRA : geler et ajouter', text=(
        "LoRA, une méthode d'adaptation légère, et les méthodes proches font autrement. "
        "Le modèle est gelé : on entraîne seulement de petites pièces ajoutées, appelées adaptateurs. "
        "Un adaptateur pèse une fraction du modèle : il se stocke et s'échange facilement. "
        "On en garde un par client ou par tâche, sur le même modèle de base.")),
    dict(kind='content', draw=s4, name='Ce que ça apprend, ou pas', text=(
        "Ce que ça apprend bien : un style, un format de sortie, un vocabulaire métier, une tâche répétitive. "
        "Par exemple, rédiger des comptes rendus de sinistre toujours structurés pareil. "
        "Ce que ça apprend mal : les faits qui changent, comme des tarifs ou un stock. "
        "Ça, c'est le rôle du RAG, pas du fine-tuning.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, tout repose sur les données : des exemples de qualité, représentatifs, relus par le métier. "
        "Deux risques : le surapprentissage, quand le modèle récite ses exemples au lieu de généraliser, "
        "et la perte de capacités générales. "
        "Mesurez-les avec vos evals, avant et après.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Le besoin porte-t-il sur la forme, ou sur des faits qui changent ? "
        "Avez-vous des exemples relus et représentatifs ? "
        "Et le modèle visé le permet-il : poids ouverts, c'est-à-dire téléchargeables, "
        "ou offre de fine-tuning du fournisseur ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : LoRA gèle le modèle et entraîne une petite pièce ajoutée, légère et échangeable. "
        "Idéal pour le style et le format. Pour les faits, préférez le RAG. "
        "Prochaine capsule : les données synthétiques, quand un modèle génère vos exemples.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
