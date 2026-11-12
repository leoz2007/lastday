from engine import *  # noqa
from engine import _paint  # noqa

NUM = 18
TITLE = 'COPILOTE OU AUTOPILOTE'
FULL_TITLE = 'Copilote ou autopilote'
SLUG = 'copilote_ou_autopilote'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'

LEVELS = ['Suggestion', 'Brouillon', 'Contrôle', 'Autonome']


def text_lines(c, t, at, x, y, widths, colors, h=24, gap=50, stagger=0.08):
    for k, w in enumerate(widths):
        p = ease(prog(t, at + k * stagger, 0.5))
        if p > 0 and w * p > h:
            rrect(c, x, y + k * gap, w * p, h, h / 2, colors[k] if isinstance(colors, list) else colors)


def s1(c, t, S):
    opening(c, t, S, CAP, "L'automatisation a des *crans*.")
    a = S.cue("l'humain qui fait tout")
    b = S.cue('la machine qui fait tout')
    icon(c, t, a, 'user', 135, 930, 80, WHITE)
    if t >= a:
        small(c, 'Humain', 135, 1050, 24, WHITE, align='center')
    icon(c, t, b, 'bolt', 945, 930, 80, WHITE)
    if t >= b:
        small(c, 'Machine', 945, 1050, 24, WHITE, align='center')
    p = ease(prog(t, a + 0.2, 1.0))
    if p > 0:
        rrect(c, 135, 1142, 810 * p, 16, 8, PL)
    cr = S.cue('plusieurs crans')
    bon = S.cue('choisir le bon')
    for k, s in enumerate(LEVELS):
        x = 270 + k * 180
        on = t >= bon and k == 1
        dot(c, t, cr + k * 0.2, x, 1150, 38 if on else 26, RED if on else WHITE)
        if t >= cr + k * 0.2:
            small(c, s, x, 1240, 18, RED if on else WHITE, align='center')
    if t >= bon:
        chip(c, t, bon + 0.2, 'Action par action', 450, 1300, RED, WHITE, 32, align='center')


def s2(c, t, S):
    header(c, t, S, 'Crans 1 et 2', "L'humain décide *avant*")
    a = S.cue('Premier cran')
    card(c, t, a, 90, 540, 900, 360, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        label(c, t, a + 0.1, '1 · Suggestion', 140, 575, RED, WHITE, 22)
        icon(c, t, a + 0.2, 'doc', 165, 700, 50, DARK)
        reveal_plain(c, t, a + 0.2, 'Ticket : « Facture en double »', 215, 712, 34, DARK)
        ca = S.cue('catégorie suggérée')
        on = t >= ca
        chip(c, t, a + 0.4, 'Catégorie : Facturation ?', 140, 775, RED if on else PLL,
             WHITE if on else DARK, 32)
    ac, ig = S.cue('accepte'), S.cue('ignore')
    x0 = 140 + chip_width('Catégorie : Facturation ?', 32) + 30
    w1 = chip(c, t, ac, 'Accepter', x0, 775, DARK, WHITE, 32)
    chip(c, t, ig, 'Ignorer', x0 + w1 + 14, 775, WHITE, DARK, 32)
    d = S.cue('Deuxième cran')
    card(c, t, d, 90, 950, 900, 470, LIGHT, 36, 'up')
    if prog(t, d, 0.5) > 0.4:
        label(c, t, d + 0.1, '2 · Brouillon', 140, 985, RED, WHITE, 22)
    rd = S.cue('rédige')
    co = S.cue('la corrige')
    cols = [PL, PL, RED if t >= co else PL, PL]
    text_lines(c, t, rd, 140, 1075, [700, 660, 690, 480], cols, 24, 52)
    if t >= co:
        icon(c, t, co, 'user', 940, 1190, 44, RED)
    rl = S.cue('la relit')
    icon(c, t, rl, 'eye', 940, 1090, 50, DARK)
    en = S.cue("puis l'envoie")
    chip(c, t, en, 'Envoyer', 140, 1310, RED, WHITE, 34)
    if t >= en + 0.2:
        reveal_plain(c, t, en + 0.2, "Validé par l'humain", 360, 1352, 32, DARK)


def s3(c, t, S):
    header(c, t, S, 'Crans 3 et 4', "L'humain contrôle *après*")
    a = S.cue('Troisième cran')
    card(c, t, a, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        label(c, t, a + 0.1, '3 · Automatique + contrôle', 140, 575, RED, WHITE, 22)
    cs = S.cue('classés seuls')
    ec = S.cue('échantillon')
    for k in range(8):
        at = cs + k * 0.12
        x = 140 + k * 90
        p = card(c, t, at, x, 680, 70, 90, PL, 14, 'pop')
        if p > 0.5:
            sel = t >= ec + 0.2 and k in (2, 6)
            rrect(c, x, 680, 70, 90, 14, RED if sel else PL)
            for j in range(3):
                rrect(c, x + 14, 702 + j * 20, 42, 8, 4, WHITE if sel else DARK)
    icon(c, t, ec, 'eye', 900, 725, 60, RED)
    if t >= ec:
        reveal_plain(c, t, ec + 0.2, 'Un humain vérifie un échantillon', 140, 870, 32, DARK)
    d = S.cue('Dernier cran')
    card(c, t, d, 90, 990, 900, 430, LIGHT, 36, 'up')
    if prog(t, d, 0.5) > 0.4:
        label(c, t, d + 0.1, '4 · Autonome', 140, 1025, RED, WHITE, 22)
    ag = S.cue("L'assistant agit")
    box(c, t, ag, 140, 1110, 300, 150, 'Assistant', DARK, WHITE, 34)
    rp = S.cue('rappel')
    arrow(c, t, rp - 0.2, 455, 1185, 580, 1185, DARK, 6)
    box(c, t, rp, 590, 1110, 350, 150, 'Rappel de rendez-vous envoyé', WHITE, DARK, 30)
    sr = S.cue('sans relecture')
    if t >= sr:
        chip(c, t, sr, 'Aucune relecture', 140, 1300, PLL, DARK, 30)


def rot_small(c, s, x, y, size, color):
    """Petites capitales tournées de 90 degrés, centrées sur (x, y)."""
    c.save()
    c.translate(x, y)
    c.rotate(-90)
    small(c, s, 0, size * 0.35, size, color, align='center')
    c.restore()


def s4(c, t, S):
    header(c, t, S, 'Choisir', 'Risque et *réversibilité*')
    dq = S.cue('deux questions')
    cw, ch, g = 385, 330, 20
    x0, y0 = 205, 560
    cl = S.cue('Classer un ticket')
    rb = S.cue('Rembourser')
    cells = {(0, 0): ('À arbitrer', LIGHT, DARK), (1, 0): ('Humain avant', RED, WHITE),
             (0, 1): ('Automatiser', PLL, DARK), (1, 1): ('À arbitrer', LIGHT, DARK)}
    for (i, j), (s, fill, fg) in cells.items():
        at = dq + 0.15 * (i + 2 * j)
        x, y = x0 + i * (cw + g), y0 + j * (ch + g)
        lit = (i, j) == (0, 1) and t >= cl or (i, j) == (1, 0) and t >= rb
        p = card(c, t, at, x, y, cw, ch, fill if lit else LIGHT, 30, 'pop')
        if p > 0.6 and lit:
            plain(c, s, x + cw / 2, y + 90, 34, fg, 'Medium', 'center')
    rq = S.cue('Que coûte')
    arrow(c, t, rq, 150, y0 + 2 * ch + g, 150, y0 + 10, DARK, 5, 18)
    if t >= rq:
        rot_small(c, 'Risque', 110, y0 + ch + g / 2, 22, DARK)
    an = S.cue("l'annuler")
    if t >= an:
        small(c, 'Facile à annuler', x0 + cw / 2, y0 + 2 * ch + g + 55, 22, DARK, align='center')
        small(c, 'Difficile à annuler', x0 + cw * 1.5 + g, y0 + 2 * ch + g + 55, 22, DARK, align='center')
    cy = y0 + ch + g
    chip(c, t, cl + 0.2, 'Classer un ticket', x0 + cw / 2, cy + 170, WHITE, DARK, 28, align='center')
    chip(c, t, rb + 0.2, 'Rembourser', x0 + cw * 1.5 + g, y0 + 170, WHITE, RED, 28, align='center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "Monter d'un cran avec la *confiance*")
    a = S.cue('on mesure')
    card(c, t, S.cue('en brouillon'), 90, 590, 900, 560, LIGHT, 36, 'up')
    if prog(t, S.cue('en brouillon'), 0.5) > 0.4:
        small(c, 'Envoyés sans modification', 140, 650, 22, DARK)
    vals = [0.3, 0.42, 0.55, 0.72, 0.78, 0.8]
    base, hmax = 1060, 330
    el = S.cue('reste élevée')
    for k, v in enumerate(vals):
        at = a + 0.25 * k
        p = ease(prog(t, at, 0.6))
        if p <= 0:
            continue
        x = 160 + k * 135
        h = hmax * v * p
        rrect(c, x, base - h, 90, h, 14, RED if (k >= 3 and t >= el) else PL)
        small(c, f'Sem. {k + 1}', x + 45, base + 50, 18, DARK, align='center')
    if t >= el:
        yy = base - hmax * 0.7
        rrect(c, 140, yy - 2, 820, 4, 2, DARK)
        small(c, 'Seuil', 140, yy - 14, 18, DARK)
    w1 = chip_width('Brouillon', 34)
    mo = S.cue("monte d'un cran")
    chip(c, t, S.cue('en brouillon'), 'Brouillon', 90, 1230, DARK, WHITE, 34)
    arrow(c, t, mo, 90 + w1 + 20, 1260, 90 + w1 + 120, 1260, DARK, 6)
    chip(c, t, mo + 0.3, 'Automatique + contrôle', 90 + w1 + 140, 1230, RED, WHITE, 34)
    rd = S.cue('Si elle baisse')
    if t >= rd:
        x2 = 90 + w1 + 140 + chip_width('Automatique + contrôle', 34) / 2
        arrow(c, t, rd, x2, 1310, x2, 1370, RED, 5, 0)
        arrow(c, t, rd + 0.3, x2, 1370, 90 + w1 / 2, 1370, RED, 5, 0)
        arrow(c, t, rd + 0.6, 90 + w1 / 2, 1370, 90 + w1 / 2, 1305, RED, 5, 18, 0.3)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Que coûte une erreur, et peut-on l'*annuler* ?", 'Que coûte'),
        ('Qui *valide*, et à quel moment ?', 'Qui valide'),
        ("Quel *indicateur* pour monter d'un cran ?", 'quel indicateur'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le niveau dépend du *risque* et de la *réversibilité*.', 'choisissez'),
        ('Il évolue avec la *confiance mesurée*.', 'Puis faites'),
    ], "19 · Gérer l'échec")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Automatiser, ce n'est pas tout ou rien. "
        "Entre l'humain qui fait tout et la machine qui fait tout, il existe plusieurs crans. "
        "Et c'est à vous de choisir le bon cran, action par action.")),
    dict(kind='content', draw=s2, name='Suggestion et brouillon', text=(
        "Premier cran : la suggestion. L'assistant propose, l'humain accepte d'un clic, ou ignore. "
        "Par exemple, une catégorie suggérée sur un ticket. "
        "Deuxième cran : le brouillon. L'assistant rédige une réponse complète, "
        "et l'humain la relit, la corrige, puis l'envoie. L'humain reste maître de chaque envoi.")),
    dict(kind='content', draw=s3, name='Action automatique et action autonome', text=(
        "Troisième cran : l'action automatique, avec un contrôle a posteriori. "
        "Les tickets sont classés seuls, sans attendre, et chaque semaine, quelqu'un vérifie un échantillon. "
        "Dernier cran : l'action autonome. L'assistant agit sans relecture, "
        "par exemple pour envoyer un rappel de rendez-vous, une action peu risquée.")),
    dict(kind='content', draw=s4, name='Choisir selon le risque et la réversibilité', text=(
        "Comment choisir ? Croisez deux questions. Que coûte une erreur ? Et peut-on l'annuler facilement ? "
        "Classer un ticket : peu de risque, et on corrige en un clic, donc on peut automatiser. "
        "Rembourser un client : une erreur coûte cher et se rattrape mal, donc un humain valide avant.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, le niveau n'est pas figé. On démarre prudemment, en brouillon, et on mesure : "
        "quelle part des brouillons part sans aucune modification ? "
        "Quand cette part reste élevée, semaine après semaine, on monte d'un cran. "
        "Si elle baisse, on redescend.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Que coûte une erreur, et peut-on l'annuler ? "
        "Qui valide, et à quel moment ? "
        "Et quel indicateur permettra de monter d'un cran ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : choisissez le niveau d'automatisation selon le risque et la réversibilité. "
        "Puis faites-le évoluer avec la confiance mesurée. "
        "Prochaine capsule : gérer l'échec, quand le modèle se trompe ou que le service ne suit plus.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
