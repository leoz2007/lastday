from engine import *  # noqa
from engine import _paint  # noqa

NUM = 39
TITLE = 'TEXT-TO-SQL'
FULL_TITLE = 'Vos données en langage naturel'
SLUG = 'donnees_langage_naturel'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'

REGIONS = [('Nord', 0.8), ('Sud', 0.55), ('Est', 0.65), ('Ouest', 0.4)]


def s1(c, t, S):
    opening(c, t, S, CAP, 'Une question en français, *un tableau* en retour.')
    q = S.cue("chiffre d'affaires par région")
    chip(c, t, q, '« Chiffre d\'affaires par région ? »', 90, 840, WHITE, DARK, 32)
    tb = S.cue("un tableau s'affiche")
    arrow(c, t, tb, 300, 920, 300, 985, WHITE, 6, 18)
    card(c, t, tb, 90, 1000, 900, 230, WHITE, 32, 'up')
    if prog(t, tb, 0.5) > 0.4:
        for k, (nm, f) in enumerate(REGIONS):
            y = 1035 + k * 46
            small(c, nm, 140, y + 21, 20, DARK)
            bar(c, t, tb + 0.2 + k * 0.1, 290, y, 650, 26, f, RED, PLL, 0.7)
    rq = S.cue('requête SQL')
    card(c, t, rq, 90, 1260, 900, 170, PLL, 32, 'up')
    if prog(t, rq, 0.5) > 0.4:
        icon(c, t, rq + 0.1, 'code', 170, 1345, 56, DARK)
        reveal_plain(c, t, rq + 0.2, 'SELECT région, SUM(montant)', 240, 1330, 30, DARK, 'Medium')
        reveal_plain(c, t, rq + 0.35, 'FROM ventes GROUP BY région', 240, 1385, 30, DARK, 'Medium')


def s2(c, t, S):
    header(c, t, S, 'Le circuit', 'Le modèle *rédige*, l\'application *exécute*')
    rows = [('user', '1 · La question', 'pose sa question'),
            ('brain', '2 · Le modèle écrit', 'écrit la requête'),
            ('db', "3 · L'application exécute", "l'exécute")]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 550 + k * 220
        card(c, t, at, 90, y, 900, 190, LIGHT, 32, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 175, y + 95, 64, RED)
            reveal_plain(c, t, at + 0.2, s, 250, y + 80, 34, DARK, 'Medium')
            if k == 0:
                small(c, '« CA par région ? »', 250, y + 135, 20, DARK)
            elif k == 1:
                st = S.cue('sans toucher aux données')
                if t >= st:
                    small(c, 'Sans toucher aux données', 250, y + 135, 20, RED)
                chip(c, t, at + 0.3, 'SELECT ...', 760, y + 65, WHITE, DARK, 28)
            else:
                af = S.cue('affiche le résultat')
                if t >= af:
                    small(c, 'Tableau ou graphique', 250, y + 135, 20, DARK)
                for j, h in enumerate([60, 100, 80, 120]):
                    hh = h * ease(prog(t, af + j * 0.1, 0.5))
                    if hh > 0:
                        rrect(c, 780 + j * 45, y + 160 - hh, 30, hh, 8, RED if j == 3 else PL)
    gm = S.cue("c'est l'application qui agit")
    card(c, t, gm, 90, 1220, 900, 170, RED, 32, 'up')
    if prog(t, gm, 0.5) > 0.4:
        icon(c, t, gm + 0.1, 'gear', 180, 1305, 60, WHITE)
        reveal_plain(c, t, gm + 0.2, "L'application garde la main", 250, 1318, 38, WHITE, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Schéma et vocabulaire', 'Décrire la base et *vos mots*')
    sc = S.cue('le schéma')
    card(c, t, sc, 90, 540, 900, 350, LIGHT, 32, 'up')
    if prog(t, sc, 0.5) > 0.4:
        small(c, 'Le schéma', 140, 600, 20, DARK)
        tables = [('Clients', 'id, nom'), ('Ventes', 'date, montant'), ('Régions', 'id, nom')]
        tb = S.cue('les tables')
        co = S.cue('les colonnes')
        li = S.cue('leurs liens')
        for k, (nm, cols) in enumerate(tables):
            x = 140 + k * 290
            box(c, t, tb + k * 0.15, x, 640, 230, 110, nm, WHITE, DARK, 32)
            if t >= co + k * 0.1:
                small(c, cols, x + 115, 800, 20, DARK, align='center')
            if k < 2:
                arrow(c, t, li + k * 0.2, x + 238, 695, x + 282, 695, RED, 5, 14)
    vm = S.cue('vocabulaire métier')
    card(c, t, vm, 90, 920, 900, 510, LIGHT, 32, 'up')
    if prog(t, vm, 0.5) > 0.4:
        small(c, 'Vocabulaire métier', 140, 980, 20, DARK)
        ca = S.cue('« client actif »')
        chip(c, t, ca, '« Client actif »', 540, 1010, RED, WHITE, 38, align='center')
        opts = [("Un achat dans l'année ?", "Un achat dans l'année"), ('Une connexion ce mois-ci ?', 'Une connexion')]
        for k, (s, kw) in enumerate(opts):
            at = S.cue(kw)
            x = 140 + k * 430
            arrow(c, t, at, 540, 1085, x + 190, 1150, DARK, 5, 14)
            box(c, t, at + 0.2, x, 1160, 380, 130, s, WHITE, DARK, 30)
        ch = S.cue('choisit à votre place')
        if t >= ch:
            icon(c, t, ch, 'cross', 180, 1365, 40, RED)
            reveal_plain(c, t, ch + 0.1, 'Non défini : le modèle devine', 230, 1377, 32, RED, 'Medium')


def s4(c, t, S):
    header(c, t, S, 'Les risques', 'Bien écrite, mais *fausse*')
    sj = S.cue('syntaxiquement juste')
    card(c, t, sj, 90, 540, 900, 380, LIGHT, 32, 'up')
    if prog(t, sj, 0.5) > 0.4:
        small(c, '1 · Juste dans la forme', 140, 600, 20, DARK)
        box(c, t, sj + 0.2, 140, 640, 360, 170, 'Requête bien écrite', WHITE, DARK, 32)
        icon(c, t, sj + 0.4, 'check', 320, 865, 40, RED)
        fo = S.cue('fausse sur le fond')
        arrow(c, t, fo, 510, 725, 570, 725, DARK, 5, 16)
        box(c, t, fo + 0.2, 580, 640, 360, 170, 'Chiffre faux', RED, WHITE, 34)
        av = S.cue('avoirs ont été oubliés')
        if t >= av:
            reveal_plain(c, t, av, 'Les avoirs oubliés', 940, 875, 28, RED, 'Medium', 'right')
    risks = [('chat', 'Ambiguïtés', 'les ambiguïtés'), ('lock', "Droits d'accès", "les droits d'accès"),
             ('clock', 'Requêtes lourdes', 'les requêtes lourdes')]
    for k, (ic, s, kw) in enumerate(risks):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 950, 280, 230, LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 1030, 60, DARK)
            text_block(c, t, at + 0.2, s, x + 140, 1130, 28, 'Medium', DARK, RED, maxw=240,
                       align='center', max_lines=2)
    rl = S.cue('les requêtes lourdes')
    if t >= rl - 0.25:
        small(c, 'Charge de la base', 90, 1250, 22, DARK)
    bar(c, t, rl, 90, 1280, 900, 40, 0.95, RED, PLL, 1.2)
    if t >= rl + 1.0:
        reveal_plain(c, t, rl + 1.0, 'Tout le monde ralentit', 990, 1385, 30, RED, 'Medium', 'right')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Quatre *parades*')
    items = [('lock', 'Lecture seule', 'lecture seule'), ('user', "Droits de l'utilisateur", "droits de l'utilisateur")]
    for k, (ic, s, kw) in enumerate(items):
        at = S.cue(kw)
        x = 90 + k * 460
        card(c, t, at, x, 540, 440, 200, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 70, 640, 52, RED)
            text_block(c, t, at + 0.2, s, x + 120, 630, 30, 'Medium', DARK, RED, maxw=300, max_lines=2)
    ic_ = S.cue('son interprétation')
    card(c, t, ic_, 90, 770, 900, 250, LIGHT, 32, 'up')
    if prog(t, ic_, 0.5) > 0.4:
        small(c, 'Montrer ce qui a été compris', 140, 830, 20, DARK)
        icon(c, t, ic_ + 0.1, 'eye', 180, 930, 60, DARK)
        hv = S.cue('hors avoirs')
        text_block(c, t, hv, '« Ventes *hors avoirs*, depuis le début du trimestre »', 250, 905, 32,
                   'Medium', DARK, RED, maxw=690, max_lines=2)
    cs = S.cue('couche sémantique')
    card(c, t, cs, 90, 1050, 900, 380, LIGHT, 32, 'up')
    if prog(t, cs, 0.5) > 0.4:
        small(c, 'Couche sémantique', 140, 1110, 20, DARK)
        dv = S.cue('définitions validées')
        defs = ['Client actif', "Chiffre d'affaires", 'Trimestre']
        for j, s in enumerate(defs):
            y = 1140 + j * 88
            at = cs + 0.2 + j * 0.15
            if t >= at:
                rrect(c, 140, y, 640, 70, 35, PLL)
                reveal_plain(c, t, at, s, 175, y + 47, 30, DARK, 'Medium')
            dot(c, t, dv + j * 0.15, 860, y + 35, 30, RED)
            icon(c, t, dv + j * 0.15 + 0.1, 'check', 860, y + 35, 32, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quels *termes métier* faut-il définir et faire valider ?', 'Quels termes'),
        ('Quels *droits* pour chaque utilisateur ?', 'Quels droits'),
        ('Quelles questions types, avec *résultats attendus*, pour les evals ?', 'Et quelles questions'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le modèle *écrit* la requête ; vos *définitions* disent la vérité.', 'le modèle écrit'),
        ('Lecture seule, droits appliqués, requête *visible*, evals.', 'Lecture seule'),
    ], '40 · Agents vocaux')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Vous tapez « chiffre d'affaires par région ce trimestre », et un tableau s'affiche. "
        "Personne n'a écrit de requête. C'est le text-to-SQL : votre question devient une requête SQL, "
        "le langage des bases de données.")),
    dict(kind='content', draw=s2, name='Le circuit', text=(
        "D'abord, l'utilisateur pose sa question. "
        "Le modèle écrit la requête, sans toucher aux données. "
        "Puis l'application l'exécute sur la base et affiche le résultat, en tableau ou en graphique. "
        "Le modèle rédige ; c'est l'application qui agit, et qui garde la main.")),
    dict(kind='content', draw=s3, name='Décrire le schéma et le vocabulaire', text=(
        "Le modèle doit connaître le schéma : les tables, les colonnes, leurs liens. "
        "Et surtout votre vocabulaire métier. Qu'est-ce qu'un « client actif » ? "
        "Un achat dans l'année ? Une connexion ce mois-ci ? "
        "Si personne ne l'a défini, le modèle choisit à votre place.")),
    dict(kind='content', draw=s4, name='Les risques', text=(
        "Le premier risque : une requête syntaxiquement juste, c'est-à-dire bien écrite, mais fausse sur le fond. "
        "Le chiffre a l'air sérieux, mais les avoirs ont été oubliés. "
        "Ajoutez les ambiguïtés, les droits d'accès, et les requêtes lourdes, qui ralentissent toute la base.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, quatre parades. Un accès en lecture seule, avec les droits de l'utilisateur, "
        "pas ceux de l'application. Montrez la requête, ou son interprétation en clair : "
        "« ventes hors avoirs, depuis le début du trimestre ». "
        "Et une couche sémantique : des définitions validées, que le modèle réutilise au lieu d'inventer.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels termes métier faut-il définir et faire valider ? "
        "Quels droits s'appliquent à chaque utilisateur ? "
        "Et quelles questions types, avec leurs résultats attendus, serviront d'evals, "
        "ces tests qui vérifient les réponses ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le modèle écrit la requête, mais votre base et vos définitions disent la vérité. "
        "Lecture seule, droits appliqués, requête visible, et des evals pour vérifier. "
        "Prochaine capsule : les agents vocaux, quand l'assistant écoute et parle.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
