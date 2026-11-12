from engine import *  # noqa
from engine import _paint  # noqa

NUM = 54
TITLE = 'ESTIMER ET PLANIFIER'
FULL_TITLE = 'Estimer et planifier un projet IA'
SLUG = 'estimer_planifier'
NEXT_CUE = 'vous savez maintenant industrialiser'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un projet IA, ça se *planifie dans l\'incertitude*.')
    cl = S.cue('un projet classique')
    ia = S.cue('personne ne sait')
    rows = [('Projet classique', cl, 0.55, 0.65, WHITE), ('Projet IA', ia, 0.3, 0.9, RED)]
    for k, (s, at, a, b, col) in enumerate(rows):
        y = 880 + k * 230
        if t >= at:
            small(c, s, 90, y, 24, WHITE)
        bar(c, t, at, 90, y + 30, 900, 60, 0, col, PL, 0.6)
        if t >= at:
            p = ease(prog(t, at + 0.2, 0.7))
            mid = (a + b) / 2
            x0 = 90 + 900 * lerp(mid, a, p)
            x1 = 90 + 900 * lerp(mid, b, p)
            rrect(c, x0, y + 30, max(60, x1 - x0), 60, 30, col)
    if t >= ia:
        small(c, 'Qualité atteignable · fourchette illustrative', 90, 1240, 20, WHITE)
    pi = S.cue("planifier l'incertitude")
    if t >= pi:
        chip(c, t, pi, "Planifier l'incertitude", 540, 1300, WHITE, RED, 36, align='center')


def s2(c, t, S):
    header(c, t, S, 'Itérations courtes', 'Un objectif *mesuré* à chaque tour')
    it = S.cue('itérations courtes')
    card(c, t, it, 90, 540, 900, 620, LIGHT, 36, 'up')
    ob = S.cue('quatre-vingts pour cent')
    if prog(t, it, 0.5) > 0.4:
        small(c, 'Qualité mesurée sur les evals · illustratif', 140, 600, 20, DARK)
        base, top = 1060, 660
        rrect(c, 140, base, 800, 4, 2, DARK)
        vals = [0.35, 0.55, 0.7, 0.85]
        for k, v in enumerate(vals):
            x = 200 + k * 200
            at = it + 0.3 + k * 0.25
            h = (base - top) * v * ease(prog(t, at, 0.5))
            hit = v >= 0.8 and t >= ob
            if t >= at:
                rrect(c, x, base - h, 120, h, 16, RED if hit else PL)
                small(c, f'Itér. {k + 1}', x + 60, base + 40, 18, DARK, align='center')
        if t >= ob:
            y = base - (base - top) * 0.8
            p = ease(prog(t, ob, 0.5))
            rrect(c, 140, y - 2, 800 * p, 5, 2, RED)
            small(c, 'Objectif : 80 %', 140, y - 16, 20, RED)
    ev = S.cue('ces tests automatiques')
    if t >= ev:
        reveal_plain(c, t, ev, 'Evals : des tests automatiques sur des cas réels', 540, 1220, 28, DARK,
                     'Medium', 'center')
    cn = S.cue('on continue')
    chip(c, t, cn, 'Progrès : on continue', 90, 1280, RED, WHITE, 28)
    ch = S.cue("on change d'approche")
    w = chip_width("Sinon : on change d'approche", 28)
    chip(c, t, ch, "Sinon : on change d'approche", 990 - w, 1280, DARK, WHITE, 28)


def s3(c, t, S):
    header(c, t, S, 'Jalons', 'Trois *jalons*')
    steps = [('Faisabilité', 'Petit échantillon', 'la faisabilité', 'search'),
             ('Pilote', 'Quelques utilisateurs', 'un pilote', 'user'),
             ('Production', 'Par vagues', 'mise en production progressive', 'bolt')]
    rrect(c, 225, 640, 630 * ease(prog(t, S.cue('trois jalons'), 1.2)), 8, 4, PL) \
        if t >= S.cue('trois jalons') else None
    for k, (s, sub, kw, ic) in enumerate(steps):
        at = S.cue(kw)
        x = 225 + k * 315
        dot(c, t, at, x, 644, 34, RED if k == 2 else DARK)
        if t >= at:
            plain(c, str(k + 1), x, 656, 32, WHITE, 'Medium', 'center')
        card(c, t, at + 0.1, x - 135, 720, 270, 380, LIGHT, 32, 'up')
        cx = x
        if prog(t, at + 0.1, 0.5) > 0.4:
            icon(c, t, at + 0.2, ic, cx, 830, 70, RED if k == 2 else DARK)
            plain(c, s, cx, 950, 32, DARK, 'Medium', 'center')
            small(c, sub, cx, 1010, 18, DARK, align='center')
    vg = S.cue('par vagues')
    if t >= vg:
        small(c, 'Utilisateurs servis', 720, 1160, 18, DARK)
        for j, f in enumerate([0.15, 0.4, 1.0]):
            bar(c, t, vg + j * 0.25, 720, 1190 + j * 60, 270, 36, f, RED, LIGHT, 0.6)
    sq = S.cue('en surveillant la qualité')
    if t >= sq:
        icon(c, t, sq, 'eye', 130, 1250, 60, DARK)
        reveal_plain(c, t, sq + 0.1, 'Qualité surveillée', 180, 1262, 32, DARK, 'Medium')


def s4(c, t, S):
    header(c, t, S, 'Le temps caché', 'Ce qu\'on *sous-estime* souvent')
    md = S.cue('sous-estime souvent')
    rows = [('Modèle et prompt', md, 0.2, PL),
            ('Données', S.cue('Les données'), 0.55, RED),
            ('Evals', S.cue('Les evals'), 0.45, RED),
            ('Intégration', S.cue("L'intégration"), 0.6, RED),
            ('Conformité', S.cue('la conformité'), 0.4, RED)]
    small(c, 'Temps du projet · illustratif', 90, 570, 20, DARK) if t >= md else None
    for k, (s, at, f, col) in enumerate(rows):
        y = 610 + k * 150
        card(c, t, at, 90, y, 900, 125, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            plain(c, s, 130, y + 75, 32, DARK, 'Medium')
            bar(c, t, at + 0.2, 470, y + 45, 480, 36, f, col, WHITE, 0.7)
    subs = [('Trouver, nettoyer, droits', 'les nettoyer', 1), ('Cas de test', 'les cas de test', 2),
            ('Systèmes existants', 'systèmes existants', 3), ('Juridique, sécurité', 'juridique, sécurité', 4)]
    for s, kw, k in subs:
        at = S.cue(kw)
        if t >= at:
            small(c, s, 130, 610 + k * 150 + 108, 16, RED)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Des *fourchettes* et des *critères*')
    f = S.cue('en fourchettes')
    card(c, t, f, 90, 540, 900, 330, LIGHT, 36, 'up')
    if prog(t, f, 0.5) > 0.4:
        df = S.cue('dates fermes')
        small(c, 'Date ferme', 140, 600, 20, DARK)
        icon(c, t, df, 'cross', 900, 640, 36, RED)
        if t >= f + 0.2:
            dot(c, t, f + 0.2, 540, 650, 18, PL)
        small(c, 'Fourchette', 140, 730, 20, RED)
        dm = S.cue('entre deux et quatre mois')
        bar(c, t, dm - 0.2, 140, 760, 800, 10, 0, RED, PL, 0.1)
        if t >= dm:
            p = ease(prog(t, dm, 0.6))
            rrect(c, 540 - 200 * p, 745, 400 * p + 1, 40, 20, RED)
            small(c, '2 mois', 340, 830, 18, DARK, align='center')
            small(c, '4 mois', 740, 830, 18, DARK, align='center')
    cr = S.cue('critères de décision')
    if t >= cr:
        small(c, 'À chaque jalon', 90, 930, 22, DARK)
    opts = [('Continuer', 'continuer,', 'check', LIGHT, DARK), ('Ajuster', 'ajuster', 'gear', LIGHT, DARK),
            ('Arrêter', 'ou arrêter', 'cross', LIGHT, DARK)]
    for k, (s, kw, ic, fill, fg) in enumerate(opts):
        at = S.cue(kw)
        x = 90 + k * 305
        card(c, t, at, x, 960, 290, 220, fill, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 145, 1040, 60, RED)
            plain(c, s, x + 145, 1140, 32, fg, 'Medium', 'center')
    su = S.cue('aussi un succès')
    card(c, t, su, 90, 1220, 900, 180, RED, 36, 'up')
    if prog(t, su, 0.5) > 0.4:
        reveal_plain(c, t, su + 0.1, 'Arrêter tôt, c\'est aussi un succès', 540, 1328, 38, WHITE, 'Medium', 'center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelle *qualité* rend le projet utile, mesurée comment ?', 'Quel niveau'),
        ('A-t-on prévu le temps des *données*, des *evals*, de la conformité ?', 'Avons-nous prévu'),
        ('Quels *critères* pour continuer, ajuster ou arrêter ?', 'Et quels critères'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Planifiez *l'incertitude*.", "planifiez l'incertitude"),
        ('Itérations courtes, *evals*, jalons, et *fourchettes*.', 'Des itérations courtes'),
    ], 'Vous savez *industrialiser*', next_label='Saison terminée')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un projet IA ne s'estime pas comme un projet classique. "
        "Au départ, personne ne sait quelle qualité vous atteindrez réellement. "
        "Il faut donc apprendre à planifier l'incertitude.")),
    dict(kind='content', draw=s2, name='Des itérations courtes, mesurées', text=(
        "Travaillez par itérations courtes, de quelques semaines par exemple. "
        "Chacune vise un objectif de qualité mesuré sur les evals, ces tests automatiques sur des cas réels. "
        "Par exemple : quatre-vingts pour cent de bonnes réponses. "
        "Si la qualité progresse, on continue ; sinon, on change d'approche.")),
    dict(kind='content', draw=s3, name='Trois jalons', text=(
        "Posez trois jalons. D'abord, la faisabilité, sur un petit échantillon de cas. "
        "Puis un pilote, avec quelques utilisateurs réels. "
        "Enfin, une mise en production progressive, par vagues, en surveillant la qualité.")),
    dict(kind='content', draw=s4, name='Le temps souvent sous-estimé', text=(
        "Prévoyez du temps pour ce qu'on sous-estime souvent. Le modèle et le prompt vont vite. "
        "Les données, beaucoup moins : les trouver, les nettoyer, obtenir les droits. "
        "Les evals : construire les cas de test. L'intégration aux systèmes existants. "
        "Et la conformité : juridique, sécurité, gouvernance.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, parlez aux sponsors en fourchettes, pas en dates fermes : "
        "entre deux et quatre mois, par exemple. Et fixez d'avance des critères de décision à chaque jalon : "
        "continuer, ajuster, ou arrêter. Arrêter tôt un projet qui ne tient pas, c'est aussi un succès.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel niveau de qualité rend le projet utile, et comment le mesure-t-on ? "
        "Avons-nous prévu le temps des données, des evals et de la conformité ? "
        "Et quels critères pour continuer, ajuster ou arrêter ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : planifiez l'incertitude. Des itérations courtes, mesurées sur les evals, des jalons, "
        "et des fourchettes plutôt que des promesses. "
        "C'était la dernière capsule de la saison quatre. Merci de l'avoir suivie, et bravo pour ce parcours. "
        "Du prototype à la gouvernance, vous savez maintenant industrialiser l'IA générative. À vous de jouer !")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
