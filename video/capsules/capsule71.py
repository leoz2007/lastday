from engine import *  # noqa
from engine import _paint  # noqa

NUM = 71
TITLE = 'ÉVALUER UN AGENT'
FULL_TITLE = 'Évaluer un agent'
SLUG = 'evaluer_un_agent'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def chip_row(c, t, items, x, y, size=26, gap=40, arrows=True, color=DARK):
    """items = [(texte, at, fill, fg)] sur une ligne, reliés par de petites flèches.
    Renvoie la liste des (x, largeur) de chaque pastille."""
    out = []
    cx = x
    h = size * 1.75
    for k, (s, at, fill, fg) in enumerate(items):
        w = chip_width(s, size)
        chip(c, t, at, s, cx, y, fill, fg, size)
        out.append((cx, w))
        if arrows and k < len(items) - 1:
            arrow(c, t, at + 0.15, cx + w + 6, y + h / 2, cx + w + gap - 6, y + h / 2, color, 3, 10)
        cx += w + gap
    return out


def s1(c, t, S):
    opening(c, t, S, CAP, 'Bonne réponse, *mauvais* parcours.')
    a = S.t0 + 0.6
    br = S.cue('la bonne réponse')
    ef = S.cue('effacé un fichier')
    small(c, 'Le parcours de l\'agent', 90, 860, 22, WHITE)
    chip_row(c, t, [('Chercher', a, WHITE, DARK), ('Lire', a + 0.2, WHITE, DARK),
                    ('Effacer un fichier', ef, RED if t >= ef else WHITE, WHITE if t >= ef else DARK),
                    ], 90, 900, 32, 50, color=WHITE)
    if t >= ef + 0.3:
        icon(c, t, ef + 0.3, 'cross', 860, 930, 50, RED)
    da = S.cue("dizaines d'appels")
    if t >= da - 0.1:
        small(c, 'Appels inutiles', 90, 1070, 22, WHITE)
    for k in range(30):
        x = 110 + (k % 15) * 58
        y = 1110 + (k // 15) * 56
        dot(c, t, da + k * 0.03, x, y, 16, PL)
    chip(c, t, br, 'Réponse correcte', 90, 1260, WHITE, DARK, 32)
    icon(c, t, br + 0.2, 'check', 470, 1290, 56, WHITE)
    tp = S.cue('tout le parcours')
    if t >= tp:
        reveal_plain(c, t, tp, 'On évalue tout le parcours', 990, 1420, 34, RED, 'Medium', 'right')


def s2(c, t, S):
    header(c, t, S, 'Deux niveaux', 'Le *résultat* et la *trajectoire*')
    rf = S.cue('le résultat final')
    card(c, t, rf, 90, 540, 900, 300, LIGHT, 32, 'up')
    if prog(t, rf, 0.5) > 0.4:
        small(c, '1 · Résultat final', 140, 600, 20, DARK)
        tf = S.cue('la tâche est-elle faite')
        icon(c, t, tf, 'check', 175, 690, 56, RED)
        reveal_plain(c, t, tf + 0.1, 'Tâche faite ?', 225, 702, 34, DARK, 'Medium')
        tp = S.cue('les tests passent-ils')
        icon(c, t, tp, 'check', 175, 780, 56, RED)
        reveal_plain(c, t, tp + 0.1, 'Tests au vert ?', 225, 792, 34, DARK, 'Medium')
    tr = S.cue('la trajectoire')
    card(c, t, tr, 90, 870, 900, 560, LIGHT, 32, 'up')
    if prog(t, tr, 0.5) > 0.4:
        small(c, '2 · Trajectoire', 140, 930, 20, DARK)
        ei = S.cue('étapes inutiles')
        ad = S.cue('actions dangereuses')
        steps = [('Chercher', None), ('Lire', None), ('Lire', ei), ('Supprimer', ad), ('Vérifier', None)]
        items = []
        for k, (s, flag) in enumerate(steps):
            hot = flag is not None and t >= flag
            items.append((s, tr + 0.2 + k * 0.12, RED if hot else WHITE, WHITE if hot else DARK))
        pos = chip_row(c, t, items, 140, 970, 26, 34)
        if t >= ei:
            x, w = pos[2]
            small(c, 'Inutile', x + w / 2, 1060, 18, RED, align='center')
        if t >= ad:
            x, w = pos[3]
            small(c, 'Dangereux', x + w / 2, 1060, 18, RED, align='center')
        mets = [('Coût', 'coin', 'coût'), ('Durée', 'clock', 'durée'), ('Appels', 'bolt', "nombre d'appels")]
        for k, (s, ic, kw) in enumerate(mets):
            at = S.cue(kw)
            x = 140 + k * 275
            card(c, t, at, x, 1110, 250, 270, WHITE, 28, 'pop')
            if prog(t, at, 0.5) > 0.5:
                icon(c, t, at + 0.1, ic, x + 125, 1210, 80, DARK)
                plain(c, s, x + 125, 1340, 32, DARK, 'Medium', 'center')


def s3(c, t, S):
    header(c, t, S, "Le banc d'essai", 'Isolé et *reproductible*')
    iso = S.cue('un environnement isolé')
    card(c, t, iso, 90, 540, 900, 620, LIGHT, 32, 'up')
    if prog(t, iso, 0.5) > 0.4:
        small(c, 'Environnement de test', 140, 600, 20, DARK)
        icon(c, t, iso + 0.2, 'brain', 250, 820, 110, RED)
        plain(c, 'Agent', 250, 920, 30, DARK, 'Medium', 'center')
        mp = S.cue('le même point de départ')
        if t >= mp:
            chip(c, t, mp, 'Même départ à chaque essai', 140, 1060, WHITE, DARK, 28)
        si = S.cue('simulés')
        box(c, t, si, 520, 650, 420, 150, 'Faux service de *paiement*', WHITE, DARK, 30)
        arrow(c, t, si + 0.2, 330, 790, 510, 730, DARK, 5, 14)
        cb = S.cue('une copie de la base')
        box(c, t, cb, 520, 850, 420, 150, 'Copie de la *base*', WHITE, DARK, 30)
        arrow(c, t, cb + 0.2, 330, 850, 510, 920, DARK, 5, 14)
    pr = S.cue('une erreur de')
    card(c, t, pr, 90, 1190, 900, 240, LIGHT, 32, 'up')
    if prog(t, pr, 0.5) > 0.4:
        icon(c, t, pr + 0.1, 'lock', 200, 1310, 80, DARK)
        plain(c, 'Production', 270, 1300, 36, DARK, 'Medium')
        nt = S.cue('ne touche jamais')
        reveal_plain(c, t, nt, 'Jamais touchée', 270, 1360, 30, RED, 'Medium')
        icon(c, t, nt, 'shield', 890, 1310, 90, RED)


RUNS = [1, 1, 0, 1, 1, 1, 0, 1, 0, 1]


def s4(c, t, S):
    header(c, t, S, 'La variance', 'Rejouer, puis *compter*')
    mt = S.cue('la même tâche')
    card(c, t, mt, 90, 540, 900, 330, LIGHT, 32, 'up')
    if prog(t, mt, 0.5) > 0.4:
        small(c, 'Même tâche, trois essais', 140, 600, 20, DARK)
        paths = [5, 8, 3]
        for r, n in enumerate(paths):
            y = 660 + r * 65
            for k in range(n):
                dot(c, t, mt + 0.2 + r * 0.25 + k * 0.05, 160 + k * 70, y, 14, DARK if r != 1 else PL)
            ok = r != 2
            icon(c, t, mt + 0.3 + r * 0.25 + n * 0.05, 'check' if ok else 'cross',
                 160 + n * 70 + 20, y, 44, RED if not ok else DARK)
        sp = S.cue('Un seul essai')
        if t >= sp:
            reveal_plain(c, t, sp, 'Un essai ne prouve rien', 940, 850, 26, RED, 'Medium', 'right')
    pf = S.cue('plusieurs fois')
    card(c, t, pf, 90, 900, 900, 530, LIGHT, 32, 'up')
    if prog(t, pf, 0.5) > 0.4:
        small(c, 'Dix essais (exemple illustratif)', 140, 960, 20, DARK)
        for k, ok in enumerate(RUNS):
            cx = 200 + (k % 5) * 170
            cy = 1050 + (k // 5) * 130
            at = pf + 0.3 + k * 0.12
            dot(c, t, at, cx, cy, 46, WHITE)
            icon(c, t, at + 0.1, 'check' if ok else 'cross', cx, cy, 50, DARK if ok else RED)
        sr = S.cue('sept réussites')
        if t >= sr - 0.25:
            small(c, 'Taux de réussite', 140, 1330, 20, DARK)
        bar(c, t, sr, 140, 1350, 600, 40, 0.7, RED, WHITE)
        if t >= sr + 0.4:
            plain(c, '7 / 10', 940, 1385, 40, RED, 'Medium', 'right')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Vos tâches, *vos scénarios*')
    bp = S.cue('les benchmarks publics')
    card(c, t, bp, 90, 540, 900, 380, LIGHT, 32, 'up')
    if prog(t, bp, 0.5) > 0.4:
        small(c, 'Benchmark public', 140, 600, 20, DARK)
        icon(c, t, bp + 0.2, 'target', 880, 590, 60, DARK)
        pi = S.cue('une première idée')
        chip(c, t, pi, 'Une première idée', 140, 640, WHITE, DARK, 30)
        lv = S.cue('loin des vôtres')
        chip(c, t, lv, 'Loin de vos tâches ?', 140, 730, RED, WHITE, 30)
        dv = S.cue('déjà vues')
        chip(c, t, dv, "Déjà vu à l'entraînement ?", 140, 820, RED, WHITE, 30)
    ps = S.cue('vos propres scénarios')
    card(c, t, ps, 90, 950, 900, 480, LIGHT, 32, 'up')
    if prog(t, ps, 0.5) > 0.4:
        small(c, 'Vos scénarios', 140, 1010, 20, DARK)
        rows = ['Rembourser une commande', 'Corriger un test cassé', 'Mettre à jour une fiche']
        cr = S.cue('critère de réussite')
        for k, s in enumerate(rows):
            y = 1040 + k * 120
            card(c, t, ps + 0.2 + k * 0.15, 140, y, 800, 100, WHITE, 24, 'left')
            if prog(t, ps + 0.2 + k * 0.15, 0.5) > 0.6:
                plain(c, s, 175, y + 62, 30, DARK, 'Medium')
            if t >= cr:
                chip(c, t, cr + k * 0.12, 'Critère', 760, y + 24, RED, WHITE, 26)
        cl = S.cue('cas réels')
        if t >= cl and t < cr:
            small(c, 'Tirés de cas réels', 940, 1010, 20, RED, align='right')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Qu\'est-ce qui *prouve* que la tâche est faite ?', "Qu'est-ce qui prouve"),
        ('Quelles actions sont *interdites*, même si le résultat est bon ?', 'Quelles actions'),
        ('Combien d\'*essais* par tâche, pour quel taux visé ?', "Et combien d'essais"),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Évaluez le *résultat* et le *parcours*, en environnement isolé.', 'on évalue un agent'),
        ('Rejouez chaque tâche, sur *vos* scénarios.', 'Rejouez chaque tâche'),
    ], '72 · Reward hacking')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un agent peut donner la bonne réponse et avoir échoué quand même. "
        "En route, il a peut-être effacé un fichier, ou fait des dizaines d'appels inutiles. "
        "On évalue tout le parcours, pas seulement la fin.")),
    dict(kind='content', draw=s2, name='Le résultat et la trajectoire', text=(
        "Un agent enchaîne des actions : chercher, lire, modifier, vérifier. "
        "On évalue d'abord le résultat final : la tâche est-elle faite, les tests passent-ils ? "
        "Puis la trajectoire, c'est-à-dire le chemin suivi : étapes inutiles, actions dangereuses, "
        "coût, durée, nombre d'appels.")),
    dict(kind='content', draw=s3, name='Un environnement de test isolé', text=(
        "Pour tester, il faut un environnement isolé et reproductible : "
        "le même point de départ à chaque essai. Les outils sont simulés, ou branchés sur des copies : "
        "un faux service de paiement, une copie de la base de données. "
        "Ainsi, une erreur de l'agent ne touche jamais la production.")),
    dict(kind='content', draw=s4, name='Rejouer et mesurer un taux de réussite', text=(
        "Autre piège : le même agent, sur la même tâche, ne fait pas toujours la même chose. "
        "Un seul essai ne prouve donc rien. On rejoue chaque tâche plusieurs fois, "
        "et on mesure un taux de réussite : par exemple, sept réussites sur dix essais.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, les benchmarks publics, des tests de référence partagés, donnent une première idée. "
        "Mais leurs tâches peuvent être loin des vôtres, "
        "et les modèles les ont peut-être déjà vues pendant leur entraînement. "
        "Construisez vos propres scénarios, tirés de cas réels, chacun avec son critère de réussite.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Qu'est-ce qui prouve que la tâche est faite ? "
        "Quelles actions sont interdites, même si le résultat est bon ? "
        "Et combien d'essais par tâche, pour quel taux de réussite visé ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : on évalue un agent sur son résultat et sur son parcours, dans un environnement isolé. "
        "Rejouez chaque tâche plusieurs fois, sur vos propres scénarios. "
        "Prochaine capsule : le reward hacking, quand un modèle contourne le critère qui le récompense.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
