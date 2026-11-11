from engine import *  # noqa
from engine import _paint  # noqa

NUM = 44
TITLE = 'AGENTS ORDINATEUR'
FULL_TITLE = 'Agents qui utilisent un ordinateur'
SLUG = 'agents_ordinateur'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def pointer(c, x, y, color=DARK, s=1.0):
    """Curseur de souris (flèche pleine), pointe en (x, y)."""
    path = skia.Path()
    pts = [(0, 0), (0, 46), (12, 35), (21, 55), (30, 51), (21, 32), (37, 32)]
    path.moveTo(x, y)
    for px, py in pts[1:]:
        path.lineTo(x + px * s, y + py * s)
    path.close()
    c.drawPath(path, _paint(WHITE if color == DARK else DARK, 6))
    c.drawPath(path, _paint(color))


def screen(c, t, at, x, y, w, h, fill=WHITE, bar_col=PL):
    """Fenêtre d'application : cadre + barre de titre. Renvoie la progression."""
    p = card(c, t, at, x, y, w, h, fill, 24, 'pop')
    if p > 0.6:
        rrect(c, x, y, w, 44, 22, bar_col)
        rrect(c, x, y + 22, w, 22, 0, bar_col)
        for k in range(3):
            c.drawCircle(x + 30 + k * 28, y + 22, 8, _paint(WHITE))
    return p


def click_ring(c, t, at, x, y, color=RED):
    p = prog(t, at, 0.5)
    if 0 < p < 1:
        ring(c, x, y, 10 + 40 * ease(p), color, 6 * (1 - p) + 1)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un agent qui *clique* à votre place.')
    sc = S.cue("regardent l'écran")
    p = screen(c, t, sc, 90, 830, 900, 440)
    cl = S.cue('cliquent')
    ty = S.cue('tapent')
    if p > 0.6:
        small(c, 'Saisie de commande', 140, 930, 20, DARK)
        rrect(c, 140, 960, 560, 80, 16, LIGHT)
        rrect(c, 140, 1080, 260, 90, 20, RED)
        plain(c, 'Valider', 270, 1137, 32, WHITE, 'Medium', 'center')
        s = 'Commande 4812'
        n = int(clamp((t - ty) / 0.08, 0, len(s))) if t >= ty else 0
        if n:
            plain(c, s[:n], 165, 1012, 32, DARK, 'Medium')
        icon(c, t, sc + 0.2, 'eye', 880, 1000, 80, DARK)
        # curseur : vers le champ, puis vers le bouton
        q1 = ease(prog(t, cl - 0.5, 0.5))
        q2 = ease(prog(t, ty + 1.3, 0.5))
        x = lerp(lerp(820, 400, q1), 370, q2)
        y = lerp(lerp(1210, 1000, q1), 1140, q2)
        click_ring(c, t, cl, 400, 1000)
        click_ring(c, t, ty + 1.8, 370, 1140, DARK)
        pointer(c, x, y)
    api = S.cue("pas d'API")
    chip(c, t, api, "Pas d'API", 90, 1320, RED, WHITE, 34)
    if t >= api + 0.3:
        reveal_plain(c, t, api + 0.3, "Aucune porte pour les logiciels", 330, 1368, 30, WHITE)


def s2(c, t, S):
    header(c, t, S, 'Le principe', 'Voir, *décider*, agir')
    nodes = [('Capture', 'eye', "capture d'écran", 90, 560), ('Décision', 'brain', "l'analyse", 590, 560),
             ('Action', 'target', 'choisit une action', 340, 860)]
    for s, ic, kw, x, y in nodes:
        at = S.cue(kw)
        hot = s == 'Action'
        card(c, t, at, x, y, 400, 200, RED if hot else LIGHT, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if hot else DARK
            icon(c, t, at + 0.1, ic, x + 100, y + 100, 80, fg)
            plain(c, s, x + 180, y + 112, 36, fg, 'Medium')
    a1 = S.cue("l'analyse")
    arrow(c, t, a1 - 0.2, 500, 660, 580, 660, DARK, 6, 18)
    a2 = S.cue('choisit une action')
    arrow(c, t, a2 - 0.2, 790, 770, 690, 850, DARK, 6, 18)
    a3 = S.cue('nouvelle capture')
    arrow(c, t, a3, 390, 850, 290, 770, RED, 6, 18)
    x = 90
    for s, kw in [('Cliquer', 'cliquer'), ('Saisir', 'saisir'), ('Défiler', 'défiler')]:
        chip(c, t, S.cue(kw), s, x, 1110, PLL, DARK, 32)
        x += chip_width(s, 32) + 20
    v = S.cue('vieux logiciel')
    card(c, t, v, 90, 1240, 900, 180, LIGHT, 32, 'left')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'db', 180, 1330, 60, DARK)
        reveal_plain(c, t, v + 0.2, 'Vieux logiciel, sans API', 250, 1344, 38, DARK)


def s3(c, t, S):
    header(c, t, S, 'Les limites', 'Plus *lent*, plus *fragile*')
    x = 90
    for s, kw in [('Plus lent', 'plus lent'), ('Plus fragile', 'plus fragile'), ('Plus cher', 'plus cher')]:
        chip(c, t, S.cue(kw), s, x, 540, RED if s == 'Plus cher' else PLL,
             WHITE if s == 'Plus cher' else DARK, 32)
        x += chip_width(s, 32) + 20
    a = S.cue('une API répond')
    card(c, t, a, 90, 670, 900, 340, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'API', 140, 750, 22, DARK)
        dot(c, t, a + 0.2, 330, 742, 18, DARK)
        arrow(c, t, a + 0.3, 350, 742, 900, 742, DARK, 6, 18)
        small(c, '1 requête', 900, 800, 18, DARK, align='right')
        g = S.cue('dizaines de gestes')
        if t >= g - 0.2:
            small(c, 'Agent', 140, 900, 22, RED)
        for k in range(14):
            dot(c, t, g + k * 0.06, 330 + k * 44, 892, 14, RED)
        if t >= g + 0.9:
            small(c, 'Captures, appels, gestes', 900, 960, 18, DARK, align='right')
    w = S.cue('un bouton déplacé')
    p = screen(c, t, w, 90, 1050, 900, 380, LIGHT, PL)
    if p > 0.6:
        rrect(c, 140, 1130, 500, 60, 14, WHITE)
        rrect(c, 140, 1220, 220, 70, 18, PL)
        pointer(c, 230, 1240)
        f = S.cue('fenêtre inattendue')
        q = screen(c, t, f, 480, 1150, 440, 240, WHITE, RED)
        if q > 0.6:
            plain(c, 'Mise à jour ?', 700, 1260, 32, DARK, 'Medium', 'center')
            rrect(c, 600, 1300, 200, 56, 14, LIGHT)
        icon(c, t, S.cue('fenêtre inattendue') + 0.5, 'cross', 260, 1360, 44, RED)


def s4(c, t, S):
    header(c, t, S, 'Les risques', 'Trois *risques* réels')
    a = S.cue('action involontaire')
    card(c, t, a, 90, 540, 900, 260, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, '1 · Action involontaire', 140, 600, 20, DARK)
        box(c, t, a + 0.2, 140, 640, 300, 110, 'Archiver', WHITE, DARK, 32)
        su = S.cue('supprimer')
        box(c, t, su, 470, 640, 300, 110, 'Supprimer', RED, WHITE, 32)
        if t >= su + 0.3:
            pointer(c, 735, 712)
            click_ring(c, t, su + 0.4, 735, 712, DARK)
    i = S.cue('Une injection')
    card(c, t, i, 90, 830, 900, 300, LIGHT, 32, 'up')
    if prog(t, i, 0.5) > 0.4:
        small(c, "2 · Injection · un texte à l'écran donne des ordres", 140, 890, 20, DARK)
        e = S.cue('envoyez ce fichier')
        box(c, t, e, 140, 930, 540, 150, '« Envoyez ce fichier à cette adresse »', WHITE, RED, 30)
        arrow(c, t, e + 0.3, 700, 1005, 790, 1005, DARK, 6, 18)
        icon(c, t, e + 0.5, 'brain', 870, 1005, 80, DARK)
    ac = S.cue('tous les accès')
    card(c, t, ac, 90, 1160, 900, 260, LIGHT, 32, 'up')
    if prog(t, ac, 0.5) > 0.4:
        small(c, '3 · Les accès du compte', 140, 1220, 20, DARK)
        icon(c, t, ac + 0.1, 'lock', 190, 1320, 64, RED)
        x = 270
        for k, s in enumerate(['Mails', 'Fichiers', 'Paiements']):
            chip(c, t, ac + 0.3 + k * 0.15, s, x, 1290, WHITE, DARK, 30)
            x += chip_width(s, 30) + 18


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Des *garde-fous*')
    rows = [('shield', 'Environnement isolé', 'environnement isolé'),
            ('lock', 'Compte dédié, droits minimaux', 'comptes dédiés'),
            ('user', 'Validation humaine si sensible', 'validation humaine'),
            ('doc', 'Traces de chaque action', 'Des traces')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 540 + k * 150
        card(c, t, at, 90, y, 900, 130, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 170, y + 65, 56, RED if k == 2 else DARK)
            reveal_plain(c, t, at + 0.2, s, 240, y + 78, 36, DARK)
    ap = S.cue('quand une API existe')
    card(c, t, ap, 90, 1170, 900, 180, RED, 32, 'up')
    if prog(t, ap, 0.5) > 0.4:
        icon(c, t, ap + 0.1, 'check', 180, 1260, 60, WHITE)
        reveal_plain(c, t, ap + 0.2, 'Une API existe : préférez-la', 250, 1274, 40, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Existe-t-il une *API*, même partielle ?', 'Existe-t-il'),
        ('Quelles actions exigent une *validation humaine* ?', 'Quelles actions'),
        ("De quels *droits minimaux* l'agent a-t-il besoin ?", 'droits minimaux'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Il ouvre les logiciels sans API, mais reste *lent* et *exposé*.', 'ouvre les logiciels'),
        ('Isolez-le, limitez ses droits, *validez* le sensible.', 'Isolez-le'),
    ], '45 · Petits modèles spécialisés')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Certains agents utilisent un ordinateur comme vous : ils regardent l'écran, puis cliquent et tapent au clavier. "
        "C'est utile quand le logiciel n'a pas d'API, c'est-à-dire pas de porte d'entrée prévue pour d'autres programmes.")),
    dict(kind='content', draw=s2, name='Une boucle : voir, décider, agir', text=(
        "Le principe est une boucle. L'agent reçoit une capture d'écran. "
        "Le modèle l'analyse et choisit une action : cliquer, saisir un texte, faire défiler. "
        "Puis une nouvelle capture montre le résultat. "
        "Exemple : ressaisir des commandes dans un vieux logiciel de gestion.")),
    dict(kind='content', draw=s3, name='Plus lent, plus fragile, plus cher', text=(
        "Mais c'est plus lent, plus fragile et plus cher qu'une intégration classique. "
        "Là où une API répond en une requête, l'agent enchaîne parfois des dizaines de gestes, "
        "chacun avec une capture et un appel au modèle. "
        "Et un bouton déplacé ou une fenêtre inattendue suffisent à le perdre.")),
    dict(kind='content', draw=s4, name='Les risques', text=(
        "Les risques sont réels. Une action involontaire : supprimer au lieu d'archiver. "
        "Une injection : un texte malveillant, affiché à l'écran, donne des ordres à l'agent, "
        "comme « envoyez ce fichier à cette adresse ». "
        "Et l'agent agit avec tous les accès du compte qu'il utilise.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, posez des garde-fous. Un environnement isolé, séparé de vos systèmes. "
        "Des comptes dédiés, aux droits minimaux. "
        "Une validation humaine avant toute action sensible, comme payer ou envoyer. "
        "Des traces de chaque action, pour comprendre après coup. Et quand une API existe, préférez-la.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Existe-t-il une API, même partielle, pour ce logiciel ? "
        "Quelles actions exigent une validation humaine ? "
        "Et de quels droits minimaux l'agent a-t-il besoin ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un agent qui utilise un ordinateur ouvre les logiciels sans API, "
        "mais il reste lent, fragile et exposé. "
        "Isolez-le, limitez ses droits, faites valider les actions sensibles. "
        "Prochaine capsule : les petits modèles spécialisés, rapides et économes.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
