from engine import *  # noqa
from engine import _paint  # noqa

NUM = 47
TITLE = 'LLMOPS ET VERSIONING'
FULL_TITLE = 'LLMOps et versioning'
SLUG = 'llmops_versioning'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'

INGR = ['Prompt', 'Modèle', 'Documents', 'Outils', 'Paramètres']


def s1(c, t, S):
    opening(c, t, S, CAP, "Le code n'a pas bougé. *L'assistant*, si.")
    a = S.cue("personne n'a touché")
    card(c, t, a, 90, 830, 900, 130, WHITE, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'code', 160, 895, 56, DARK)
        reveal_plain(c, t, a + 0.2, 'Code inchangé', 230, 908, 36, DARK)
        icon(c, t, a + 0.4, 'check', 920, 895, 50, DARK)
    ig = S.cue('un ingrédient')
    md = S.cue('le modèle lui-même')
    pos = [(90, 1020), (400, 1020), (710, 1020), (245, 1170), (555, 1170)]
    for k, (nm, (x, y)) in enumerate(zip(INGR, pos)):
        hot = k == 1 and t >= md
        box(c, t, ig + k * 0.12, x, y, 280, 120, nm, RED if hot else PL, WHITE if hot else DARK, 32)
    lo = S.cue('LLMOps')
    chip(c, t, lo, 'LLMOps : exploiter en production', 540, 1340, WHITE, DARK, 30, align='center')


def s2(c, t, S):
    header(c, t, S, 'Les ingrédients', 'Plusieurs ingrédients *qui bougent*')
    kws = ['le prompt', 'sa version', 'les documents', 'les outils', 'des paramètres']
    labs = ['Prompt', 'Modèle et version', 'Documents', 'Outils', 'Paramètres']
    a = S.cue('Un assistant dépend')
    card(c, t, a, 620, 690, 370, 260, DARK, 36, 'pop')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 805, 790, 80, WHITE)
        plain(c, 'Assistant', 805, 900, 34, WHITE, 'Medium', 'center')
    for k, (lab, kw) in enumerate(zip(labs, kws)):
        at = S.cue(kw)
        y = 560 + k * 110
        box(c, t, at, 90, y, 400, 90, lab, LIGHT, DARK, 30, 'Medium', 26, 'left')
        arrow(c, t, at + 0.2, 500, y + 45, 610, lerp(y + 45, 820, 0.6), DARK, 5, 14)
    ex = S.cue('Par exemple')
    card(c, t, ex, 90, 1140, 900, 290, LIGHT, 36, 'up')
    if prog(t, ex, 0.5) > 0.4:
        small(c, 'Un seul ingrédient change', 140, 1200, 20, DARK)
        md = S.cue('mise à jour des documents')
        icon(c, t, md, 'doc', 200, 1310, 80, DARK)
        chip(c, t, md + 0.2, 'v2', 250, 1240, RED, WHITE, 26)
        tr = S.cue('suffit à changer')
        arrow(c, t, tr, 320, 1310, 440, 1310, DARK, 6, 18)
        icon(c, t, tr + 0.2, 'chat', 510, 1310, 70, RED)
        reveal_plain(c, t, tr + 0.3, 'Réponse différente', 570, 1325, 34, RED, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Versionner ensemble', 'Une *recette* numérotée')
    r = S.cue('recette numérotée')
    card(c, t, r, 90, 540, 470, 560, LIGHT, 36, 'up')
    vd = S.cue('Version douze')
    if prog(t, r, 0.5) > 0.4:
        if t >= vd:
            chip(c, t, vd, 'Version 12', 130, 570, RED, WHITE, 30)
        vers = ['v7', 'v3', 'v21', 'v4', 'v2']
        for k, nm in enumerate(INGR):
            at = vd + 0.3 + k * 0.15
            y = 690 + k * 80
            if t >= at:
                reveal_plain(c, t, at, nm, 130, y + 34, 30, DARK)
                chip(c, t, at + 0.1, vers[k], 520 - chip_width(vers[k], 24), y, PL, DARK, 24)
    nv = S.cue('ce numéro de version')
    small(c, 'Journal des réponses', 600, 575, 20, DARK) if t >= nv else None
    for k in range(4):
        at = nv + 0.1 + k * 0.15
        y = 610 + k * 120
        card(c, t, at, 600, y, 390, 100, LIGHT, 28, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, 'chat', 650, y + 50, 44, DARK)
            rrect(c, 700, y + 40, 140, 20, 10, PL)
            chip(c, t, at + 0.2, 'v12', 860, y + 26, RED, WHITE, 24)
    cs = S.cue('conteste')
    card(c, t, cs, 90, 1140, 900, 290, LIGHT, 36, 'up')
    if prog(t, cs, 0.5) > 0.4:
        small(c, 'Une réponse contestée', 140, 1200, 20, DARK)
        icon(c, t, cs + 0.1, 'user', 190, 1320, 70, DARK)
        arrow(c, t, cs + 0.3, 250, 1320, 340, 1320, DARK, 5, 16)
        qc = S.cue('quelle combinaison')
        chip(c, t, qc, 'v12', 355, 1294, RED, WHITE, 30)
        rj = qc + 0.8
        arrow(c, t, rj, 470, 1320, 560, 1320, DARK, 5, 16)
        box(c, t, rj + 0.2, 575, 1260, 370, 120, 'Rejouée à l\'identique', RED, WHITE, 30)


def s4(c, t, S):
    header(c, t, S, 'Évaluer et déployer', 'Tester, puis déployer *peu à peu*')
    steps = [('Changement', 'Chaque changement'), ('Evals', 'les evals'), ('Déploiement', 'progressivement')]
    for k, (s, kw) in enumerate(steps):
        at = S.cue(kw)
        x = 90 + k * 310
        box(c, t, at, x, 560, 280, 120, s, RED if k == 1 else LIGHT, WHITE if k == 1 else DARK, 30)
        if k < 2:
            arrow(c, t, at + 0.3, x + 284, 620, x + 306, 620, DARK, 5, 12)
    pp = S.cue('une petite part')
    pd = S.cue('puis davantage')
    card(c, t, pp, 90, 730, 900, 330, LIGHT, 36, 'up')
    if prog(t, pp, 0.5) > 0.4:
        small(c, 'Part du trafic (illustratif)', 140, 790, 20, DARK)
        rows = [('Étape 1', 0.05, pp + 0.2), ('Étape 2', 0.3, pd), ('Étape 3', 1.0, pd + 0.5)]
        for k, (nm, f, at) in enumerate(rows):
            y = 830 + k * 70
            if t >= at - 0.25:
                plain(c, nm, 140, y + 32, 26, DARK)
            bar(c, t, at, 290, y + 8, 650, 34, f, RED, WHITE, 0.7)
    qb = S.cue('la qualité baisse')
    card(c, t, qb, 90, 1100, 900, 330, LIGHT, 36, 'up')
    if prog(t, qb, 0.5) > 0.4:
        small(c, 'Retour arrière', 140, 1160, 20, DARK)
        box(c, t, qb + 0.2, 560, 1210, 330, 120, 'Version 13', PL, DARK, 32)
        icon(c, t, qb + 0.5, 'cross', 935, 1270, 40, RED)
        vp = S.cue('version précédente')
        arrow(c, t, vp, 550, 1270, 470, 1270, RED, 6, 18)
        box(c, t, vp + 0.3, 140, 1210, 320, 120, 'Version 12', RED, WHITE, 32)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Un modèle peut *être retiré*')
    rg = S.cue('un registre des versions')
    card(c, t, rg, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, rg, 0.5) > 0.4:
        small(c, 'Registre des versions', 140, 600, 20, DARK)
        cols = [('Version', 140), ('Date', 330), ('Motif', 520), ('Evals', 740)]
        for nm, x in cols:
            small(c, nm, x, 650, 18, DARK)
        for k, (v, f) in enumerate([('v11', 0.7), ('v12', 0.82), ('v13', 0.55)]):
            at = rg + 0.3 + k * 0.2
            y = 680 + k * 80
            if t >= at:
                chip(c, t, at, v, 140, y, RED if k == 1 else PL, WHITE if k == 1 else DARK, 24)
                rrect(c, 330, y + 12, 140, 20, 10, PL)
                rrect(c, 520, y + 12, 180, 20, 10, PL)
                bar(c, t, at + 0.1, 740, y + 10, 200, 24, f, RED if k == 1 else DARK, WHITE, 0.6)
    fo = S.cue('Surveillez votre fournisseur')
    card(c, t, fo, 90, 980, 900, 450, LIGHT, 36, 'up')
    if prog(t, fo, 0.5) > 0.4:
        small(c, 'Calendrier (illustratif)', 140, 1040, 20, DARK)
        plain(c, 'Modèle actuel', 140, 1110, 28, DARK)
        bar(c, t, fo + 0.2, 140, 1130, 640, 36, 1.0, PL, WHITE, 0.8)
        rt = S.cue('le retirer')
        if t >= rt:
            rrect(c, 790, 1110, 6, 210, 3, RED)
            reveal_plain(c, t, rt, 'Retrait', 940, 1150, 28, RED, 'Medium', 'right')
        mg = S.cue('Prévoyez la migration')
        if t >= mg - 0.25:
            plain(c, 'Nouveau modèle', 140, 1230, 28, DARK)
        bar(c, t, mg, 420, 1250, 520, 36, 1.0, RED, WHITE, 0.8)
        ev = S.cue('avec ses evals')
        chip(c, t, ev, 'Evals', 430, 1320, DARK, WHITE, 26)
        if t >= ev:
            reveal_plain(c, t, ev + 0.2, 'Migrer avant', 940, 1360, 28, RED, 'Medium', 'right')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Qu'est-ce qui est *versionné*, et qui peut le modifier ?", "Qu'est-ce qui"),
        ('Quelles *evals* bloquent un déploiement ?', 'Quelles evals'),
        ('Que fait-on si le modèle est *retiré* ?', 'Et que fait-on'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un assistant, ce sont des ingrédients *versionnés ensemble*.', 'un assistant'),
        ('Evals avant tout changement, déploiement progressif, *retour arrière*.', 'Chaque changement'),
    ], "48 · A/B testing d'un assistant")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Votre assistant a changé de comportement, et personne n'a touché au code. "
        "Pourtant, un ingrédient a bougé : un prompt, un document, ou le modèle lui-même. "
        "Bienvenue dans le LLMOps, l'art d'exploiter des modèles de langage en production.")),
    dict(kind='content', draw=s2, name='Les ingrédients d\'un assistant', text=(
        "Un assistant dépend de plusieurs ingrédients : le prompt, le modèle et sa version, "
        "les documents qu'il consulte, les outils qu'il appelle, "
        "et des paramètres, comme la température, qui règle la part de hasard. "
        "Chacun évolue de son côté. Par exemple, une mise à jour des documents suffit à changer une réponse sur les tarifs.")),
    dict(kind='content', draw=s3, name='Versionner ensemble', text=(
        "La parade : versionner ces ingrédients ensemble, comme une recette numérotée. "
        "Version douze : tel prompt, tel modèle, tels documents, tels outils. "
        "Avec chaque réponse, on enregistre ce numéro de version. "
        "Si un client conteste une réponse, on sait quelle combinaison l'a produite, et on peut la rejouer.")),
    dict(kind='content', draw=s4, name='Evals, déploiement progressif, retour arrière', text=(
        "Chaque changement passe d'abord par les evals, des tests automatiques sur des cas représentatifs. "
        "S'ils sont bons, on déploie progressivement : une petite part du trafic, puis davantage si tout va bien. "
        "Et si la qualité baisse, on revient en arrière, vers la version précédente.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, tenez un registre des versions : la date, le motif, le résultat des evals. "
        "Surveillez votre fournisseur : il peut faire évoluer un modèle, ou le retirer. "
        "Prévoyez la migration comme un changement à part entière, avec ses evals et son calendrier.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Qu'est-ce qui est versionné, et qui peut le modifier ? "
        "Quelles evals bloquent un déploiement ? "
        "Et que fait-on le jour où le modèle est retiré ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un assistant, c'est une combinaison d'ingrédients, versionnés ensemble. "
        "Chaque changement passe par les evals, se déploie progressivement, et peut revenir en arrière. "
        "Prochaine capsule : l'A/B testing, pour comparer deux versions sur de vrais utilisateurs.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
