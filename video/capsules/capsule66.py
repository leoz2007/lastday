from engine import *  # noqa
from engine import _paint  # noqa

NUM = 66
TITLE = 'MIXTURE OF EXPERTS'
FULL_TITLE = 'Mixture of Experts'
SLUG = 'mixture_of_experts'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def grid(c, t, at, x, y, cols, rows, sz, gap, active, on=RED, off=PL, step=0.03, at_on=None):
    """Grille d'experts (carrés). active = indices allumés à at_on (ou at)."""
    at_on = at if at_on is None else at_on
    for k in range(cols * rows):
        i, j = k % cols, k // cols
        xx, yy = x + i * (sz + gap), y + j * (sz + gap)
        hot = k in active and t >= at_on
        card(c, t, at + k * step, xx, yy, sz, sz, on if hot else off, 10, 'pop')


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un modèle *immense*, actif *en partie*.')
    a = S.cue('énormément de paramètres')
    card(c, t, a, 90, 830, 900, 400, WHITE, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Experts du modèle · illustratif', 140, 890, 20, DARK)
        p = S.cue('une petite partie')
        grid(c, t, a + 0.2, 160, 920, 10, 3, 58, 18, {3, 16}, RED, PL, 0.015, p)
    for s, kw, fill, fg in [('Taille totale : très grande', 'énormément', WHITE, DARK),
                            ('Actifs par token : quelques-uns', 'une petite partie', RED, WHITE)]:
        at = S.cue(kw) + 0.4
        chip(c, t, at, s, 90, 1270 if fill == WHITE else 1370, fill, fg, 30)


def s2(c, t, S):
    header(c, t, S, 'Experts et routeur', 'Un aiguilleur choisit *quelques experts*')
    h = S.cue('grand hôpital')
    card(c, t, h, 90, 540, 900, 230, LIGHT, 32, 'up')
    if prog(t, h, 0.5) > 0.4:
        small(c, "Comme à l'hôpital", 140, 600, 20, DARK)
        icon(c, t, h + 0.2, 'user', 190, 690, 70, DARK)
        ac = S.cue('un accueil oriente')
        arrow(c, t, ac - 0.2, 240, 690, 300, 690, DARK, 5, 14)
        chip(c, t, ac, 'Accueil', 310, 660, DARK, WHITE, 28)
        for k in range(5):
            xx = 560 + k * 85
            icon(c, t, h + 0.4 + k * 0.08, 'user', xx + 20, 690, 54, RED if (k in (1, 3) and t >= ac + 0.4) else PL)
        arrow(c, t, ac + 0.3, 475, 690, 540, 690, DARK, 5, 14)
    r = S.cue('le routeur')
    card(c, t, r - 0.6, 90, 810, 900, 620, LIGHT, 32, 'up')
    if prog(t, r - 0.6, 0.5) > 0.4:
        small(c, 'Dans le modèle', 140, 870, 20, DARK)
        tk = S.cue('pour chaque token')
        chip(c, t, tk, 'facture', 130, 1090, WHITE, DARK, 30)
        arrow(c, t, tk + 0.2, 290, 1120, 345, 1120, DARK, 5, 14)
        box(c, t, r, 355, 1060, 200, 120, 'Routeur', DARK, WHITE, 32)
        names = ['Expert 1', 'Expert 2', 'Expert 3', 'Expert 4', 'Expert 5', 'Expert 6']
        q = S.cue('seulement quelques experts')
        for k, nm in enumerate(names):
            y = 900 + k * 85
            hot = k in (1, 4) and t >= q
            box(c, t, S.cue('les experts sont') + k * 0.08, 680, y, 270, 68, nm, RED if hot else WHITE,
                WHITE if hot else DARK, 26)
            if k in (1, 4):
                arrow(c, t, q, 560, 1120, 672, y + 34, RED, 5, 16)
        rp = S.cue('les autres restent')
        if t >= rp:
            small(c, 'Les autres : au repos', 140, 1380, 18, DARK)


def s3(c, t, S):
    header(c, t, S, 'Calcul par token', "Grand au total, *léger* à l'usage")
    d = S.cue('un modèle dense')
    m = S.cue('le mélange d\'experts répond')
    for k, (title, at, active) in enumerate([('Modèle dense', d, set(range(16))),
                                              ("Mélange d'experts", S.cue('la taille totale'), {2, 13})]):
        x = 90 + k * 465
        card(c, t, at, x, 540, 435, 470, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, title, x + 50, 600, 20, RED if k == 1 else DARK)
            on_at = at + 0.6 if k == 0 else S.cue('seule une fraction')
            grid(c, t, at + 0.2, x + 76, 630, 4, 4, 62, 14, active, RED, WHITE, 0.02, on_at)
            if t >= on_at:
                small(c, 'Tout s\'active' if k == 0 else 'Quelques-uns', x + 50, 985, 18, DARK)
    card(c, t, d + 0.3, 90, 1050, 900, 380, LIGHT, 32, 'up')
    if prog(t, d + 0.3, 0.5) > 0.4:
        small(c, 'À taille totale égale · illustratif', 140, 1110, 20, DARK)
        small(c, 'Calcul par token', 140, 1160, 18, DARK)
        plain(c, 'Dense', 140, 1225, 28, DARK)
        bar(c, t, d + 0.5, 440, 1200, 500, 32, 0.95, PL, WHITE, 0.8)
        plain(c, "Mélange d'experts", 140, 1300, 28, RED)
        bar(c, t, m, 440, 1275, 500, 32, 0.25, RED, WHITE, 0.8)
        if t >= m + 0.4:
            icon(c, t, m + 0.4, 'bolt', 160, 1370, 40, RED)
            reveal_plain(c, t, m + 0.5, 'Souvent plus rapide, moins cher', 200, 1382, 28, DARK)


def s4(c, t, S):
    header(c, t, S, 'Les limites', 'Tout doit tenir *en mémoire*')
    a = S.cue('tous les experts doivent')
    card(c, t, a, 90, 540, 900, 450, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Mémoire GPU · illustratif', 140, 600, 20, DARK)
        g = S.cue('mémoire GPU')
        rrect(c, 140, 630, 800, 230, 24, WHITE)
        grid(c, t, a + 0.2, 165, 650, 12, 3, 46, 20, {4, 21}, RED, PL, 0.01, a + 0.2)
        small(c, 'Actifs', 140, 900, 18, RED)
        small(c, 'Au repos, mais chargés', 940, 900, 18, DARK, align='right')
        if t >= g:
            bar(c, t, g, 140, 930, 800, 28, 1.0, DARK, WHITE, 0.8)
    th = S.cue('des thèmes lisibles')
    card(c, t, th, 90, 1030, 900, 400, LIGHT, 32, 'up')
    if prog(t, th, 0.5) > 0.4:
        small(c, 'Pas forcément un thème par expert', 140, 1090, 20, DARK)
        x = 140
        for s, kw in [('Droit ?', 'le droit'), ('Cuisine ?', 'la cuisine')]:
            at = S.cue(kw)
            w = chip(c, t, at, s, x, 1130, WHITE, DARK, 30)
            icon(c, t, at + 0.3, 'cross', x + w + 30, 1157, 40, RED)
            x += w + 110
        em = S.cue("émerge de l'entraînement")
        if t >= em:
            icon(c, t, em, 'brain', 180, 1310, 70, DARK)
            text_block(c, t, em + 0.1, "Une spécialité qui *émerge*, souvent difficile à lire", 250, 1290,
                       32, 'Medium', DARK, RED, maxw=680, max_lines=2)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Vitesse, *mémoire*, évaluation')
    v = S.cue("coût d'inférence")
    card(c, t, v, 90, 540, 900, 200, LIGHT, 32, 'left')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'bolt', 170, 640, 60, DARK)
        icon(c, t, v + 0.2, 'coin', 260, 640, 60, DARK)
        text_block(c, t, v + 0.3, 'Vitesse et *coût* par réponse', 330, 652, 36, 'Medium', DARK, RED,
                   maxw=620, max_lines=1)
    s = S.cue('sur site')
    card(c, t, s, 90, 780, 900, 380, LIGHT, 32, 'left')
    if prog(t, s, 0.5) > 0.4:
        small(c, 'Hébergement sur site · illustratif', 140, 840, 20, DARK)
        icon(c, t, s + 0.1, 'db', 175, 960, 70, DARK)
        pa = S.cue('pas sur la part active')
        tt = S.cue('sur la taille totale')
        plain(c, 'Part active', 260, 950, 28, DARK)
        bar(c, t, pa, 560, 925, 380, 32, 0.2, PL, WHITE, 0.6)
        plain(c, 'Mémoire à prévoir', 260, 1040, 28, RED)
        bar(c, t, tt, 560, 1015, 380, 32, 1.0, RED, WHITE, 0.8)
        if t >= pa:
            small(c, 'Dimensionner sur la taille totale', 260, 1110, 18, DARK)
    e = S.cue('évaluez sur vos propres tâches')
    card(c, t, e, 90, 1200, 900, 220, RED, 32, 'left')
    if prog(t, e, 0.5) > 0.4:
        icon(c, t, e + 0.1, 'target', 175, 1310, 64, WHITE)
        reveal_plain(c, t, e + 0.2, 'Évaluer sur vos propres tâches', 250, 1323, 38, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quels *vitesse et coût* par réponse visez-vous ?', 'Quelle vitesse'),
        ('Sur site, le modèle *tient-il en mémoire* ?', 'Hébergé sur site'),
        ("L'avez-vous testé sur *vos propres tâches* ?", "Et l'avez-vous"),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un routeur active *quelques experts* par token : moins de calcul.', 'un routeur'),
        ('Mais *tous les experts* restent en mémoire.', 'mais tous les experts'),
    ], "67 · Lois d'échelle")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle peut avoir énormément de paramètres, ses réglages appris, "
        "et n'en faire travailler qu'une petite partie pour chaque mot. "
        "C'est le principe du Mixture of Experts, ou mélange d'experts.")),
    dict(kind='content', draw=s2, name='Des experts et un routeur', text=(
        "Imaginez un grand hôpital. Plutôt qu'un seul généraliste, il compte de nombreux spécialistes, "
        "et un accueil oriente chaque patient. "
        "Dans le modèle, les experts sont des sous-réseaux. "
        "L'aiguilleur, le routeur, choisit pour chaque token, un morceau de mot, seulement quelques experts. "
        "Les autres restent au repos.")),
    dict(kind='content', draw=s3, name='Moins de calcul par token', text=(
        "Résultat : la taille totale du modèle peut être très grande, "
        "mais seule une fraction travaille pour chaque token. "
        "Comparez avec un modèle dense, où tout s'active à chaque fois : à taille totale égale, il calcule bien plus. "
        "Le mélange d'experts répond donc souvent plus vite, et moins cher.")),
    dict(kind='content', draw=s4, name='Mémoire et experts peu lisibles', text=(
        "Mais attention : même au repos, tous les experts doivent tenir en mémoire. "
        "Il faut donc beaucoup de mémoire GPU, celle des processeurs graphiques. "
        "Et les experts ne sont pas forcément des thèmes lisibles, comme le droit ou la cuisine. "
        "Leur spécialité émerge de l'entraînement, souvent difficile à interpréter.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, cette architecture joue sur la vitesse et le coût d'inférence, c'est-à-dire de chaque réponse. "
        "Pour un hébergement sur site, dimensionnez la mémoire sur la taille totale, pas sur la part active. "
        "Et ne jugez pas sur l'architecture : évaluez sur vos propres tâches.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelle vitesse et quel coût par réponse visez-vous ? "
        "Hébergé sur site, le modèle tient-il en mémoire ? "
        "Et l'avez-vous testé sur vos propres tâches ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un routeur n'active que quelques experts par token, donc moins de calcul. "
        "Mais tous les experts restent en mémoire : dimensionnez et testez en conséquence. "
        "Prochaine capsule : les lois d'échelle, et le calcul au moment de répondre.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
