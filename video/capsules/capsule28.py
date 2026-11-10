from engine import *  # noqa
from engine import _paint  # noqa

NUM = 28
TITLE = 'CONDUITE DU CHANGEMENT'
FULL_TITLE = 'Conduite du changement'
SLUG = 'conduite_changement'
NEXT_CUE = 'dernière capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def s1(c, t, S):
    opening(c, t, S, CAP, "Un outil non *adopté* ne sert à rien.")
    a = S.cue('la technique')
    card(c, t, a, 390, 900, 300, 220, LIGHT, 36, 'pop')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'gear', 540, 990, 80, DARK)
        small(c, 'Outil', 540, 1085, 22, DARK, align='center')
    eq = S.cue('les équipes')
    ad = S.cue("l'adoptent")
    pos = [(170, 900), (170, 1120), (910, 900), (910, 1120), (300, 1330), (540, 1330), (780, 1330)]
    for k, (x, y) in enumerate(pos):
        on = t >= ad + 0.2 + k * 0.12
        icon(c, t, eq + k * 0.1, 'user', x, y, 70, RED if on else PL)
    if t >= ad:
        for k, (x, y) in enumerate(pos):
            if t >= ad + 0.2 + k * 0.12:
                c.drawLine(lerp(x, 540, 0.25), lerp(y, 1010, 0.25), lerp(x, 540, 0.6), lerp(y, 1010, 0.6), _paint(RED, 4))


def s2(c, t, S):
    header(c, t, S, 'Former', "L'*usage*, pas la technique")
    a = S.cue('fait bien')
    b = S.cue('fait mal')
    for k, (title, at, fill, items, ic) in enumerate([
            ('Fait bien', a, LIGHT, [('Résumer', 'résumer'), ('Reformuler', 'reformuler')], 'check'),
            ('Fait mal', b, DARK, [('Garantir un chiffre', 'garantir un chiffre')], 'cross')]):
        x = 90 + k * 470
        card(c, t, at, x, 560, 430, 470, fill, 36, 'up')
        if prog(t, at, 0.5) > 0.4:
            fg = DARK if k == 0 else WHITE
            icon(c, t, at + 0.1, ic, x + 70, 640, 60, RED)
            plain(c, title, x + 120, 655, 36, fg)
            for j, (s, kw) in enumerate(items):
                box(c, t, S.cue(kw), x + 40, 720 + j * 140, 350, 110, s, WHITE if k == 0 else RED,
                    DARK if k == 0 else WHITE, 32, 'Medium', 26, 'up')
    fo = S.cue('Une personne formée')
    card(c, t, fo, 90, 1080, 900, 300, LIGHT, 36, 'up')
    if prog(t, fo, 0.5) > 0.4:
        icon(c, t, fo + 0.1, 'user', 190, 1230, 90, DARK)
        cf = S.cue('faire confiance')
        vr = S.cue('quand vérifier')
        chip(c, t, cf, 'Quand faire confiance', 290, 1130, WHITE, DARK, 32)
        chip(c, t, vr, 'Quand vérifier', 290, 1250, RED, WHITE, 32)
        icon(c, t, vr + 0.2, 'eye', 650, 1295, 60, RED)


def s3(c, t, S):
    header(c, t, S, "Règles d'usage", 'Des règles *claires*, écrites')
    a = S.cue("règles d'usage claires")
    card(c, t, a, 90, 560, 900, 640, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'doc', 170, 640, 70, RED)
        plain(c, "Charte d'usage (exemple)", 230, 655, 34, DARK)
        rows = [('check', 'Données autorisées', 'le droit d', RED),
                ('lock', 'Données interdites', 'lesquelles jamais', DARK),
                ('eye', 'Vérifier avant d\'envoyer', 'faut vérifier', RED)]
        for k, (ic, s, kw, col) in enumerate(rows):
            at = S.cue(kw)
            y = 720 + k * 150
            card(c, t, at, 130, y, 820, 120, WHITE, 28, 'left')
            if prog(t, at, 0.5) > 0.4:
                icon(c, t, at + 0.1, ic, 200, y + 60, 55, col)
                reveal_plain(c, t, at + 0.15, s, 260, y + 72, 34, DARK)
    x = 90
    for s, kw in [('Simples', 'règles simples'), ('Écrites', 'écrites'), ('Connues de tous', 'connues de tous')]:
        w = chip(c, t, S.cue(kw), s, x, 1260, RED, WHITE, 34)
        x += w + 16


def s4(c, t, S):
    header(c, t, S, 'Embarquer', 'Les métiers, *tôt*')
    a = S.cue('ambassadeurs')
    box(c, t, S.t0 + 0.4, 340, 820, 400, 160, 'Cas d\'usage', DARK, WHITE, 38)
    teams = [(90, 560, 'Équipe A'), (700, 560, 'Équipe B'), (90, 1080, 'Équipe C'), (700, 1080, 'Équipe D')]
    for k, (x, y, s) in enumerate(teams):
        at = a + k * 0.2
        card(c, t, at, x, y, 290, 180, LIGHT, 30, 'pop')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, 'user', x + 70, y + 90, 55, RED)
            icon(c, t, at + 0.15, 'user', x + 150, y + 90, 45, PL)
            icon(c, t, at + 0.2, 'user', x + 220, y + 90, 45, PL)
            small(c, s, x + 145, y + 160, 18, DARK, align='center')
    if t >= a:
        small(c, 'En rouge : un ambassadeur', 540, 790, 20, RED, align='center')
    rm = S.cue('remontent les problèmes')
    for k, (x, y, _) in enumerate(teams):
        cx = x + 145
        y1 = y + 190 if y < 800 else y - 10
        y2 = 815 if y < 800 else 990
        if y < 800:
            arrow(c, t, rm + k * 0.1, cx, y1 + 0, cx + (60 if x < 500 else -60), y2 + 20, RED, 5, 16)
        else:
            arrow(c, t, rm + k * 0.1, cx, y1, cx + (60 if x < 500 else -60), y2 - 5, RED, 5, 16)
    co = S.cue('Co-construisez')
    chip(c, t, co, 'Co-construire', 540, 1300, RED, WHITE, 36, align='center')
    cm = S.cue('Co-construisez') + 0.8
    if t >= cm:
        reveal_plain(c, t, cm, 'plutôt que livrer clés en main', 540, 1400, 30, DARK, 'Medium', 'center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Rassurer, puis *itérer*')
    a = S.cue('rassurez sur les rôles')
    card(c, t, a, 90, 540, 900, 320, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        label(c, t, a + 0.1, 'Ce qui reste humain', 140, 580, PLL, DARK, 22)
        x = 140
        for s, kw in [('La décision', 'la décision'), ('La relation', 'la relation'), ('Le jugement', 'le jugement')]:
            w = chip(c, t, S.cue(kw), s, x, 680, RED, WHITE, 32)
            x += w + 16
        ch = S.cue('ce qui change')
        if t >= ch:
            reveal_plain(c, t, ch, 'Et ce qui change : dit clairement', 140, 820, 30, DARK)
    steps = [('Mesurer', "mesurez l'usage", 'target'), ('Écouter', 'écoutez les retours', 'chat'),
             ('Itérer', 'itérez', 'gear')]
    for k, (s, kw, ic) in enumerate(steps):
        at = S.cue(kw)
        x = 90 + k * 315
        card(c, t, at, x, 940, 270, 260, RED if k == 2 else DARK, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 135, 1040, 70, WHITE)
            plain(c, s, x + 135, 1150, 34, WHITE, 'Medium', 'center')
        if k < 2:
            arrow(c, t, at + 0.3, x + 275, 1070, x + 310, 1070, DARK, 5, 14)
    ft = S.cue('et itérez') + 0.6
    if t >= ft:
        arrow(c, t, ft, 855, 1215, 855, 1270, RED, 5, 16)
        arrow(c, t, ft + 0.4, 855, 1275, 225, 1275, RED, 5, 1)
        arrow(c, t, ft + 0.8, 225, 1275, 225, 1215, RED, 5, 16)
        reveal_plain(c, t, ft + 1.0, 'Comme toute fonctionnalité', 540, 1350, 30, DARK, 'Medium', 'center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Qui *forme* les équipes, et sur quels usages ?', 'Qui forme'),
        ("Quelles *règles d'usage* écrire avant le lancement ?", "Quelles règles"),
        ('Qui sont vos *ambassadeurs* dans chaque métier ?', 'qui sont vos'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Une IA réussie est une IA *adoptée*.', 'une IA réussie'),
        ('Formez, fixez des *règles*, embarquez, *itérez*.', 'Formez, fixez'),
    ], 'Vous savez *cadrer* un projet', next_label='Saison terminée')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Dans un projet d'IA, le plus difficile n'est pas toujours la technique. "
        "C'est souvent que les équipes l'adoptent, et qu'elles s'en servent vraiment.")),
    dict(kind='content', draw=s2, name='Former les équipes', text=(
        "Commencez par former. Pas à la technique, mais à l'usage : "
        "ce que l'IA fait bien, comme résumer ou reformuler, "
        "et ce qu'elle fait mal, comme garantir un chiffre exact. "
        "Une personne formée sait quand faire confiance, et quand vérifier. Appuyez-vous sur des exemples tirés de son propre métier.")),
    dict(kind='content', draw=s3, name="Des règles d'usage", text=(
        "Fixez ensuite des règles d'usage claires. "
        "Quelles données ont le droit d'entrer dans l'outil, et lesquelles jamais. "
        "Ce qu'il faut vérifier avant d'envoyer un texte produit par l'IA. "
        "Des règles simples, écrites, connues de tous, et revues quand l'outil évolue.")),
    dict(kind='content', draw=s4, name='Embarquer les métiers', text=(
        "Embarquez les métiers tôt. Identifiez des ambassadeurs dans chaque équipe : "
        "des utilisateurs qui testent, remontent les problèmes et aident leurs collègues au quotidien. Leur parole convainc mieux qu'une campagne de communication. "
        "Co-construisez les cas d'usage avec eux, plutôt que de les livrer clés en main.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, rassurez sur les rôles. Dites clairement ce qui change dans le travail, "
        "et ce qui reste humain : la décision, la relation, le jugement. "
        "Puis mesurez l'usage, écoutez les retours et itérez, comme pour toute autre fonctionnalité.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Qui forme les équipes, et sur quels usages ? "
        "Quelles règles d'usage écrivez-vous avant le lancement ? "
        "Et qui sont vos ambassadeurs dans chaque métier ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : une IA réussie est une IA adoptée. Formez, fixez des règles, embarquez les métiers, et itérez. "
        "C'était la dernière capsule de la saison deux. Merci de l'avoir suivie jusqu'au bout, et bravo pour ce parcours. "
        "Vous savez maintenant cadrer un projet d'IA générative, de la première idée jusqu'à son adoption. "
        "À vous de jouer !")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
