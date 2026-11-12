from engine import *  # noqa
from engine import _paint  # noqa

NUM = 50
TITLE = 'RED TEAMING'
FULL_TITLE = 'Red teaming'
SLUG = 'red_teaming'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Attaquez votre assistant *avant les autres*.')
    a = S.cue('attaquez votre propre assistant')
    card(c, t, a, 390, 980, 300, 300, WHITE, 150, 'pop')
    icon(c, t, a + 0.2, 'chat', 540, 1130, 120, DARK)
    eq = S.cue('une équipe joue')
    pos = [(150, 900), (150, 1360), (930, 900), (930, 1360)]
    for k, (x, y) in enumerate(pos):
        at = eq + k * 0.15
        icon(c, t, at, 'user', x, y, 70, RED)
        tx = 400 if x < 540 else 680
        ty = 1050 if y < 1130 else 1210
        arrow(c, t, at + 0.3, x + (50 if x < 540 else -50), y, tx, ty, WHITE, 5, 16)
    fl = S.cue('les failles')
    dot(c, t, fl, 690, 1020, 26, RED)
    if t >= fl:
        reveal_plain(c, t, fl + 0.2, 'Faille trouvée', 540, 1450 - 20, 30, WHITE, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, 'Ce qu\'on cherche', 'Quatre types de *failles*')
    items = [('Contourner les règles', 'Contourner les règles', '« Jouons un rôle... »', 'shield'),
             ('Extraire des données', 'Extraire des données', 'Le system prompt', 'lock'),
             ('Contenu interdit', 'contenu interdit', 'Ce qui doit rester bloqué', 'cross'),
             ('Action non voulue', 'action non voulue', 'Remboursement non validé', 'bolt')]
    for k, (nm, kw, ex, ic) in enumerate(items):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        y = 540 + (k // 2) * 450
        card(c, t, at, x, y, 440, 420, LIGHT, 36, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, f'{k + 1}', x + 40, y + 60, 24, RED)
            icon(c, t, at + 0.1, ic, x + 220, y + 150, 90, RED)
            text_block(c, t, at + 0.2, nm, x + 220, y + 270, 34, 'Medium', DARK, RED,
                       maxw=380, align='center', max_lines=2)
            ext = S.cue(['jeu de rôle', 'system prompt', 'contenu interdit', 'un remboursement'][k])
            if t >= ext:
                text_block(c, t, ext, ex, x + 220, y + 360, 24, 'Medium', RED, RED,
                           maxw=380, align='center', max_lines=1)


def s3(c, t, S):
    header(c, t, S, 'Qui attaque', 'Une équipe *mixte*')
    rows = [('Sécurité', 'La sécurité', 'Les attaques techniques', 'lock'),
            ('Métier', 'Le métier', 'Ce qui serait grave chez vous', 'target'),
            ('Profils variés', 'des profils variés', 'Des détours inattendus', 'user')]
    for k, (nm, kw, ex, ic) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 230
        card(c, t, at, 90, y, 900, 200, LIGHT if k < 2 else RED, 36, 'left')
        if prog(t, at, 0.5) > 0.4:
            fg = DARK if k < 2 else WHITE
            icon(c, t, at + 0.1, ic, 190, y + 100, 80, RED if k < 2 else WHITE)
            reveal_plain(c, t, at + 0.2, nm, 280, y + 85, 40, fg, 'Medium')
            reveal_plain(c, t, at + 0.4, ex, 280, y + 145, 28, fg, 'Medium')
    ox = S.cue('Mélangez les regards')
    if t >= ox:
        x = 90
        for s in ['Regards mélangés', 'Plus de failles trouvées']:
            x += chip(c, t, ox + (0 if s == 'Regards mélangés' else 0.2), s, x, 1270, DARK, WHITE, 30) + 14


def s4(c, t, S):
    header(c, t, S, 'Après l\'attaque', 'Chaque faille devient *un test*')
    steps = [('Consigner', 'est consignée'), ('Corriger', 'On la corrige'), ('Test permanent', 'cas de test permanent')]
    for k, (s, kw) in enumerate(steps):
        at = S.cue(kw)
        x = 90 + k * 310
        box(c, t, at, x, 560, 280, 120, s, RED if k == 2 else LIGHT, WHITE if k == 2 else DARK, 30)
        if k < 2:
            arrow(c, t, at + 0.3, x + 284, 620, x + 306, 620, DARK, 5, 12)
    cs = S.cue('est consignée')
    card(c, t, cs, 90, 730, 900, 280, LIGHT, 36, 'up')
    if prog(t, cs, 0.5) > 0.4:
        small(c, "Fiche d'attaque", 140, 790, 20, DARK)
        for k, (nm, kw) in enumerate([('Demande exacte', 'la demande exacte'), ('Réponse obtenue', 'la réponse obtenue'),
                                      ('Gravité', 'la gravité')]):
            at = S.cue(kw)
            y = 820 + k * 60
            if t >= at:
                reveal_plain(c, t, at, nm, 140, y + 36, 28, DARK)
                bar(c, t, at + 0.1, 440, y + 14, 500 if k < 2 else 300, 26, 1.0, RED if k == 2 else PL, WHITE, 0.6)
    ev = S.cue('dans les evals')
    card(c, t, ev, 90, 1050, 900, 380, LIGHT, 36, 'up')
    if prog(t, ev, 0.5) > 0.4:
        small(c, 'Evals : la liste de tests grandit', 140, 1110, 20, DARK)
        for k in range(12):
            x = 140 + (k % 6) * 135
            y = 1150 + (k // 6) * 95
            new = k >= 10
            at = ev + 0.2 + k * 0.05 if not new else ev + 1.0 + (k - 10) * 0.2
            card(c, t, at, x, y, 115, 75, RED if new else PL, 20, 'pop')
            if prog(t, at, 0.4) > 0.5:
                icon(c, t, at, 'check', x + 57, y + 37, 34, WHITE if new else DARK)
        rv = S.cue('ne revient pas')
        if t >= rv:
            reveal_plain(c, t, rv, 'Une faille corrigée reste surveillée', 140, 1395, 28, RED, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'À refaire à *chaque changement*')
    a = S.cue("pas un examen unique")
    card(c, t, a, 90, 540, 900, 560, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Vie de l\'assistant', 140, 600, 20, DARK)
        rrect(c, 140, 760, 800, 8, 4, PL)
        evs = [('Nouveau modèle', 'nouveau modèle'), ('Nouvel outil', 'nouvel outil'),
               ('Nouvelle source', 'nouvelle source')]
        for k, (nm, kw) in enumerate(evs):
            at = S.cue(kw)
            x = 250 + k * 280
            dot(c, t, at, x, 764, 18, DARK)
            if t >= at:
                text_block(c, t, at + 0.1, nm, x, 690, 26, 'Medium', DARK, RED, maxw=240,
                           align='center', max_lines=1)
            icon(c, t, at + 0.3, 'bolt', x, 870, 60, RED)
            if t >= at + 0.3:
                small(c, 'Red teaming', x, 960, 18, RED, align='center')
    tc = S.cue('le temps de corriger')
    card(c, t, tc, 90, 1140, 900, 290, RED, 36, 'up')
    if prog(t, tc, 0.5) > 0.4:
        icon(c, t, tc + 0.1, 'clock', 180, 1285, 70, WHITE)
        reveal_plain(c, t, tc + 0.2, 'Du temps pour corriger', 260, 1270, 38, WHITE, 'Medium')
        lc = S.cue('date de lancement')
        if t >= lc:
            reveal_plain(c, t, lc, 'avant la date de lancement', 260, 1330, 30, WHITE, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles *failles* seraient les plus graves pour nous ?', 'Quelles failles'),
        ("Qui compose l'*équipe d'attaque* ?", 'Qui compose'),
        ('Quels *changements* relancent une campagne ?', 'Et quels changements'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Attaquez votre assistant *avant les autres*.', 'attaquez votre assistant'),
        ('Chaque faille trouvée devient un *test permanent*.', 'Chaque faille'),
    ], '51 · Propriété intellectuelle')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Avant la mise en production, attaquez votre propre assistant. "
        "C'est le red teaming, l'équipe rouge : une équipe joue les attaquants, "
        "pour trouver les failles avant les vrais. "
        "Mieux vaut que ce soit vous qui les découvriez.")),
    dict(kind='content', draw=s2, name='Quatre types de failles', text=(
        "On cherche quatre types de failles. Contourner les règles, par exemple avec un jeu de rôle. "
        "Extraire des données, ou le system prompt, ces consignes cachées qui guident l'assistant. "
        "Obtenir un contenu interdit. "
        "Ou déclencher une action non voulue, comme un remboursement que personne n'a validé.")),
    dict(kind='content', draw=s3, name='Une équipe mixte', text=(
        "L'équipe doit être mixte. La sécurité connaît les attaques techniques. "
        "Le métier sait ce qui serait grave dans votre contexte. "
        "Et des profils variés, qui ne sont pas experts, pensent à des détours que les experts oublient. "
        "Mélangez les regards : chacun voit des failles différentes.")),
    dict(kind='content', draw=s4, name='Chaque faille devient un test', text=(
        "Chaque attaque réussie est consignée : la demande exacte, la réponse obtenue, la gravité. "
        "On la corrige, en changeant le prompt, un guardrail ou un droit d'accès. Puis on la transforme en cas de test permanent, dans les evals. "
        "Ainsi, une faille corrigée ne revient pas sans qu'on le voie.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, le red teaming n'est pas un examen unique. "
        "Refaites-le à chaque changement important : nouveau modèle, nouvel outil, nouvelle source de données. "
        "Car un changement peut rouvrir une faille, ou en créer une nouvelle. "
        "Et prévoyez le temps de corriger avant la date de lancement.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles failles seraient les plus graves pour nous ? "
        "Qui compose l'équipe d'attaque ? "
        "Et quels changements déclenchent une nouvelle campagne ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : attaquez votre assistant avant que d'autres ne le fassent. "
        "Chaque faille trouvée est corrigée, puis devient un test permanent. "
        "Prochaine capsule : la propriété intellectuelle, et les questions qu'elle pose à l'IA générative.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
