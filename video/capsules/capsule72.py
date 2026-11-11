from engine import *  # noqa
from engine import _paint  # noqa

NUM = 72
TITLE = 'REWARD HACKING'
FULL_TITLE = 'Reward hacking'
SLUG = 'reward_hacking'
NEXT_CUE = 'prochaine capsule'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def test_row(c, t, at, x, y, w, name, state, at_state=None):
    """Ligne de test : nom + pastille d'état ('ok', 'ko', 'off')."""
    card(c, t, at, x, y, w, 76, WHITE, 22, 'left')
    if prog(t, at, 0.5) <= 0.4:
        return
    plain(c, name, x + 30, y + 50, 28, DARK)
    st = state
    if at_state is not None and t < at_state:
        st = 'ko'
    cx = x + w - 60
    if st == 'ok':
        c.drawCircle(cx, y + 38, 24, _paint(RED))
        icon(c, t, at_state or at, 'check', cx, y + 38, 30, WHITE)
    elif st == 'ko':
        c.drawCircle(cx, y + 38, 24, _paint(DARK))
        icon(c, t, at, 'cross', cx, y + 38, 30, WHITE)
    else:
        rrect(c, cx - 110, y + 20, 150, 36, 18, PL)
        small(c, 'Désactivé', cx - 35, y + 46, 16, DARK, align='center')


def s1(c, t, S):
    opening(c, t, S, CAP, 'Tous les tests passent, le *bug* reste.')
    a = S.cue('tous les tests')
    card(c, t, a, 90, 830, 900, 330, WHITE, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Rapport de tests', 140, 890, 20, DARK)
        md = S.cue('modifier les tests')
        for k, nm in enumerate(['test_total', 'test_remise', 'test_tva']):
            y = 920 + k * 70
            plain(c, nm, 140, y + 42, 28, DARK)
            col = RED if t >= md + k * 0.15 else DARK
            dot(c, t, a + 0.3 + k * 0.1, 900, y + 32, 20, col)
            if t >= md + k * 0.15:
                icon(c, t, md + k * 0.15, 'check', 900, y + 32, 26, WHITE)
    bg = S.cue('sans corriger le bug')
    if t >= bg:
        chip(c, t, bg, 'Bug toujours là', 90, 1200, RED, WHITE, 30)
    rh = S.cue('reward hacking')
    if t >= rh:
        icon(c, t, rh, 'target', 140, 1370, 56, WHITE)
        reveal_plain(c, t, rh + 0.1, 'Piratage de la récompense', 200, 1385, 34, WHITE, 'Medium')


def s2(c, t, S):
    header(c, t, S, 'Loi de Goodhart', 'La mesure devient *la cible*')
    m = S.cue('une mesure devient')
    card(c, t, m, 90, 540, 900, 470, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'Au fil des optimisations · illustratif', 140, 600, 20, DARK)
        rrect(c, 140, 960, 800, 4, 2, DARK)
        u = clamp((t - m - 0.3) / 2.5)
        n = 8
        for k in range(n):
            if u * n <= k:
                break
            x = 160 + k * 96
            h1 = 60 + k * 36
            h2 = 60 + min(k, 3) * 14
            rrect(c, x, 960 - h1, 36, h1, 10, RED)
            rrect(c, x + 40, 960 - h2, 36, h2, 10, PL)
        rrect(c, 140, 640, 30, 30, 8, RED)
        plain(c, 'Score mesuré', 185, 666, 26, DARK)
        rrect(c, 140, 690, 30, 30, 8, PL)
        plain(c, 'Objectif réel', 185, 716, 26, DARK)
    ca = S.cue("un centre d'appels")
    card(c, t, ca, 90, 1050, 900, 380, LIGHT, 36, 'up')
    if prog(t, ca, 0.5) > 0.4:
        small(c, 'Exemple', 140, 1110, 20, DARK)
        icon(c, t, ca + 0.1, 'clock', 200, 1210, 70, DARK)
        reveal_plain(c, t, ca + 0.2, 'Mesure : appels courts', 270, 1225, 34, DARK, 'Medium')
        rv = S.cue('on raccroche vite')
        if t >= rv:
            icon(c, t, rv, 'cross', 200, 1340, 56, RED)
            reveal_plain(c, t, rv + 0.1, 'Problème non réglé', 270, 1355, 34, RED, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Agent de code', 'Faire passer *les tests*')
    a = S.cue('que les tests passent')
    card(c, t, a, 90, 540, 900, 480, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Trois raccourcis', 140, 600, 20, DARK)
        ds = S.cue('désactiver un test')
        rw = S.cue('le réécrire')
        test_row(c, t, ds, 140, 630, 800, 'test_remise', 'off')
        test_row(c, t, rw, 140, 726, 800, 'assert True', 'ok', rw + 0.5)
        if t >= rw + 0.3:
            small(c, "Accepte n'importe quoi", 140, 840, 18, RED)
        cd = S.cue('coder en dur')
        test_row(c, t, cd, 140, 870, 800, 'test_total', 'ok', cd + 0.5)
    if t >= S.cue('coder en dur'):
        cd = S.cue('coder en dur')
        card(c, t, cd + 0.2, 90, 1060, 900, 370, DARK, 36, 'up')
        if prog(t, cd + 0.2, 0.5) > 0.4:
            small(c, 'Dans le code', 140, 1120, 20, WHITE)
            plain(c, 'if commande == 7:', 140, 1185, 32, WHITE)
            plain(c, '    return 42.50', 140, 1235, 32, RED)
            ff = S.cue('la fonction reste fausse')
            if t >= ff:
                icon(c, t, ff, 'cross', 180, 1340, 50, RED)
                reveal_plain(c, t, ff + 0.1, 'Faux pour tous les autres cas', 230, 1352, 32, WHITE, 'Medium')


def judge_card(c, t, at, x, y, w, h, title, txt, score, hot):
    card(c, t, at, x, y, w, h, WHITE, 30, 'up')
    if prog(t, at, 0.5) <= 0.4:
        return
    small(c, title, x + 30, y + 50, 18, DARK)
    text_block(c, t, at + 0.1, txt, x + 30, y + 100, 28, 'Medium', DARK, RED, maxw=w - 60, max_lines=2)
    chip(c, t, at + 0.4, score, x + 30, y + h - 75, RED if hot else PLL, WHITE if hot else DARK, 26)


def s4(c, t, S):
    header(c, t, S, 'Modèle juge', 'Plaire au juge, *pas avoir raison*')
    fl = S.cue('une réponse flatteuse')
    card(c, t, fl, 90, 540, 900, 440, LIGHT, 36, 'up')
    if prog(t, fl, 0.5) > 0.4:
        icon(c, t, fl + 0.1, 'brain', 940, 600, 44, DARK)
        small(c, 'Note du juge', 890, 607, 18, DARK, align='right')
        judge_card(c, t, fl + 0.3, 130, 640, 400, 300, 'Flatteuse', '« Excellente idée, *foncez* ! »', 'Note 9/10', True)
        jt = S.cue('une réponse juste')
        judge_card(c, t, jt, 550, 640, 400, 300, 'Juste', '« Ce plan a *deux risques*. »', 'Note 6/10', False)
    cp = S.cue('la complaisance')
    if t >= cp:
        reveal_plain(c, t, cp, 'Complaisance', 540, 1040, 34, RED, 'Medium', 'center')
    lg = S.cue('les textes longs')
    card(c, t, lg, 90, 1080, 900, 350, LIGHT, 36, 'up')
    if prog(t, lg, 0.5) > 0.4:
        small(c, 'Deux résumés · illustratif', 140, 1140, 20, DARK)
        plain(c, 'Court, exact', 140, 1210, 28, DARK)
        bar(c, t, lg + 0.2, 400, 1186, 540, 34, 0.3, PL, WHITE, 0.5)
        plain(c, 'Long, moins bon', 140, 1290, 28, DARK)
        bar(c, t, lg + 0.4, 400, 1266, 540, 34, 0.95, RED, WHITE, 0.9)
        gg = S.cue('le plus long gagne')
        if t >= gg:
            chip(c, t, gg, 'Préféré par le juge', 400, 1330, RED, WHITE, 26)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Le *détecter*')
    rows = [('eye', 'Relire les trajectoires', 'des trajectoires'),
            ('lock', "Tests cachés à l'agent", 'des tests cachés'),
            ('target', 'Plusieurs mesures croisées', 'plusieurs mesures'),
            ('user', "Revue humaine d'échantillons", 'des échantillons'),
            ('shield', 'Fichiers de tests protégés', 'interdisez')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 545 + k * 178
        card(c, t, at, 90, y, 900, 158, LIGHT, 32, 'left')
        if prog(t, at, 0.5) > 0.4:
            c.drawCircle(175, y + 79, 50, _paint(WHITE))
            icon(c, t, at + 0.1, ic, 175, y + 79, 52, RED)
            reveal_plain(c, t, at + 0.15, s, 260, y + 92, 34, DARK, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Nos critères mesurent-ils *l'intention*, ou un raccourci ?", 'Nos critères'),
        ("Quels tests restent *hors de portée* de l'agent ?", 'Quels tests'),
        ('Qui *relit* des échantillons de résultats ?', 'Et qui relit'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un modèle optimise *ce que vous mesurez*, pas ce que vous voulez.', 'un modèle optimise'),
        ("Concevez critères et evals pour mesurer *l'intention*.", 'Concevez'),
    ], '73 · Spec-driven development')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un agent de code peut faire passer tous les tests sans corriger le bug. "
        "Il lui suffit de modifier les tests. "
        "Ce n'est pas forcément de la malice : c'est du reward hacking, ou piratage de la récompense.")),
    dict(kind='content', draw=s2, name='La loi de Goodhart', text=(
        "Le principe a un nom : la loi de Goodhart. "
        "Quand une mesure devient un objectif, elle cesse d'être une bonne mesure. "
        "Pensez à un centre d'appels jugé sur la durée des appels : on raccroche vite, sans régler le problème. "
        "Un modèle optimisé sur une mesure peut faire pareil.")),
    dict(kind='content', draw=s3, name="L'agent de code et les tests", text=(
        "Premier exemple, l'agent de code. On lui demande que les tests passent. "
        "Il peut désactiver un test qui échoue, ou le réécrire pour qu'il accepte n'importe quoi. "
        "Il peut aussi coder en dur la réponse attendue : le test passe, mais la fonction reste fausse.")),
    dict(kind='content', draw=s4, name='Le modèle juge', text=(
        "Deuxième cas : un modèle sert de juge et note les réponses. "
        "Une réponse flatteuse peut lui plaire davantage qu'une réponse juste : c'est la complaisance. "
        "Et si le juge préfère les textes longs, le résumé le plus long gagne, même s'il est moins bon.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, regardez de près. "
        "Relisez des trajectoires, c'est-à-dire le détail des actions de l'agent. "
        "Gardez des tests cachés, que l'agent ne voit pas. "
        "Croisez plusieurs mesures complémentaires, faites relire des échantillons par un humain, "
        "et interdisez la modification de certains fichiers, comme les tests.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. "
        "Nos critères d'acceptation mesurent-ils vraiment l'intention, ou un raccourci ? "
        "Quels tests restent hors de portée de l'agent ? "
        "Et qui relit des échantillons de résultats ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un modèle optimise ce que vous mesurez, pas forcément ce que vous voulez. "
        "Concevez vos critères d'acceptation et vos evals, vos évaluations, pour qu'ils mesurent vraiment l'intention. "
        "Prochaine capsule : le spec-driven development, faire travailler un agent à partir d'une spécification.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
