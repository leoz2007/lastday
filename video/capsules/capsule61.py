from engine import *  # noqa
from engine import _paint  # noqa

NUM = 61
TITLE = 'FINOPS IA DE CODE'
FULL_TITLE = "FinOps de l'IA de code"
SLUG = 'finops_ia_code'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def gpu(c, t, at, cx, cy, s=100, color=DARK):
    """Picto de carte graphique : un boîtier, deux ventilateurs, des connecteurs."""
    p = back(prog(t, at, 0.4))
    if p <= 0:
        return
    c.save()
    c.translate(cx, cy)
    c.scale(p * s / 100, p * s / 100)
    st = _paint(color, 7)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-50, -30, 50, 26), 8, 8), st)
    c.drawCircle(-22, -2, 14, st)
    c.drawCircle(22, -2, 14, st)
    for k in range(4):
        c.drawLine(-36 + k * 20, 26, -36 + k * 20, 40, st)
    c.restore()


def s1(c, t, S):
    opening(c, t, S, CAP, "Le coût de l'IA se *cache*.")
    items = [('gpu', 'Des GPU qui dorment', 'qui dorment'),
             ('loop', 'Des boucles qui tournent', 'qui tournent'),
             ('eye', "Des équipes sans l'addition", "jamais l'addition")]
    for k, (ic, s, kw) in enumerate(items):
        at = S.cue(kw)
        y = 830 + k * 150
        card(c, t, at, 90, y, 900, 130, WHITE, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            if ic == 'gpu':
                gpu(c, t, at + 0.1, 170, y + 65, 70, DARK)
            elif ic == 'loop':
                icon(c, t, at + 0.1, 'gear', 170, y + 65, 56, DARK)
            else:
                icon(c, t, at + 0.1, ic, 170, y + 65, 56, DARK)
            reveal_plain(c, t, at + 0.2, s, 240, y + 78, 36, DARK)
            if k == 1:
                chip(c, t, at + 0.4, '?', 900, y + 40, RED, WHITE, 30)
    f = S.cue('La FinOps')
    card(c, t, f, 90, 1300, 900, 130, RED, 30, 'up')
    if prog(t, f, 0.5) > 0.4:
        icon(c, t, f + 0.1, 'coin', 170, 1365, 56, WHITE)
        reveal_plain(c, t, f + 0.2, 'FinOps : piloter les coûts au grand jour', 240, 1378, 34, WHITE)


def s2(c, t, S):
    header(c, t, S, 'Acheter ou louer', 'GPU à vous, ou *paiement à l\'usage*')
    a = S.cue('Avec vos GPU')
    card(c, t, a, 90, 560, 430, 640, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        gpu(c, t, a + 0.1, 170, 640, 70, DARK)
        plain(c, 'Sur site', 240, 652, 32, DARK, 'Medium')
        small(c, 'TCO · coût total', 130, 730, 18, DARK)
        rows = [('Investissement', "l'investissement", 120), ('Énergie', "l'énergie", 80),
                ('Exploitation', "l'exploitation", 100)]
        y = 1100
        for s, kw, h in rows:
            at = S.cue(kw)
            p = ease(prog(t, at, 0.6))
            if p > 0:
                rrect(c, 130, y - h * p, 120, h * p, 8, RED if s == 'Investissement' else PL)
                if p > 0.8:
                    plain(c, s, 266, y - h / 2 + 9, 24, DARK, 'Medium')
            y -= h + 6
        ar = S.cue("même à l'arrêt")
        if t >= ar:
            reveal_plain(c, t, ar, "Coûte même à l'arrêt", 305, 1150, 26, RED, 'Medium', 'center')
    b = S.cue('à l\'usage, au token')
    card(c, t, b, 560, 560, 430, 640, LIGHT, 32, 'up')
    if prog(t, b, 0.5) > 0.4:
        icon(c, t, b + 0.1, 'coin', 640, 640, 60, DARK)
        plain(c, 'Cloud', 700, 652, 32, DARK, 'Medium')
        small(c, 'Au token consommé', 600, 730, 18, DARK)
        for k in range(12):
            dot(c, t, b + 0.3 + k * 0.08, 640 + (k % 4) * 90, 820 + (k // 4) * 90, 24, PL)
        rl = S.cue('quand il roule')
        if t >= rl:
            reveal_plain(c, t, rl, "Ne coûte qu'à l'usage", 775, 1150, 26, RED, 'Medium', 'center')
    n = S.cue('Aucun prix universel')
    card(c, t, n, 90, 1240, 900, 170, RED, 30, 'up')
    if prog(t, n, 0.5) > 0.4:
        icon(c, t, n + 0.1, 'cross', 170, 1325, 50, WHITE)
        reveal_plain(c, t, n + 0.2, 'Aucun prix universel :', 240, 1312, 34, WHITE)
        reveal_plain(c, t, n + 0.35, 'calculez avec vos chiffres', 240, 1362, 34, WHITE)


def s3(c, t, S):
    header(c, t, S, 'Mesurer et répartir', 'Des tokens, *par équipe*')
    m = S.cue('mesurez les tokens')
    card(c, t, m, 90, 560, 900, 470, LIGHT, 32, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'Tokens par tâche · illustratif', 140, 620, 20, DARK)
        rows = [('Correction de bug', 'correction de bug', 0.18, PL),
                ('Refonte', 'une refonte', 0.85, RED)]
        for j, (s, kw, f, col) in enumerate(rows):
            at = S.cue(kw)
            y = 660 + j * 110
            if t >= at:
                plain(c, s, 140, y + 30, 28, DARK)
            bar(c, t, at, 140, y + 50, 800, 34, f, col, WHITE)
        small(c, 'Par équipe', 140, 920, 20, DARK)
        x = 140
        for k, (s, f) in enumerate([('A', 0.5), ('B', 0.8), ('C', 0.3)]):
            at = S.cue('chaque équipe') + k * 0.15
            plain(c, s, x, 990, 30, DARK, 'Medium') if t >= at else None
            bar(c, t, at, x + 40, 962, 200, 36, f, PL, WHITE)
            x += 270
    sb = S.cue("c'est le showback")
    card(c, t, sb, 90, 1070, 430, 340, WHITE, 32, 'pop')
    if prog(t, sb, 0.5) > 0.4:
        outline(c, 90, 1070, 430, 340, 32, PL)
        icon(c, t, sb + 0.1, 'eye', 305, 1170, 70, DARK)
        plain(c, 'Showback', 305, 1280, 36, DARK, 'Medium', 'center')
        small(c, 'Rendre visible', 305, 1340, 20, DARK, align='center')
    cb = S.cue("c'est le chargeback")
    card(c, t, cb, 560, 1070, 430, 340, RED, 32, 'pop')
    if prog(t, cb, 0.5) > 0.4:
        icon(c, t, cb + 0.1, 'coin', 775, 1170, 70, WHITE)
        plain(c, 'Chargeback', 775, 1280, 36, WHITE, 'Medium', 'center')
        small(c, 'Refacturer', 775, 1340, 20, WHITE, align='center')


def s4(c, t, S):
    header(c, t, S, 'Utilisation des GPU', 'Un GPU qui dort *coûte*')
    u = S.cue("taux d'utilisation")
    card(c, t, u, 90, 560, 900, 560, LIGHT, 32, 'up')
    ex = S.cue('Exemple illustratif')
    nu = S.cue('la nuit')
    if prog(t, u, 0.5) > 0.4:
        small(c, 'Utilisation sur 24 h · illustratif', 140, 620, 20, DARK)
        base = 1000
        for h in range(24):
            day = 9 <= h < 18
            f = 0.9 if day else 0.12
            at = ex + h * 0.04
            p = ease(prog(t, at, 0.5))
            x = 150 + h * 33
            # cadre : capacité payée
            if t >= u + 0.2:
                outline(c, x, base - 300, 24, 300, 6, PL, 3)
            if p > 0:
                col = DARK if day else (RED if t >= nu else PL)
                rrect(c, x, base - 300 * f * p, 24, 300 * f * p, 6, col)
        for h, s in [(0, '0 h'), (9, '9 h'), (18, '18 h'), (23, '24 h')]:
            if t >= u + 0.2:
                small(c, s, 162 + h * 33, 1050, 18, DARK, align='center')
        if t >= nu:
            reveal_plain(c, t, nu, 'Payé, mais inutilisé', 540, 1095, 28, RED, 'Medium', 'center')
    y = 1160
    for k, (s, kw) in enumerate([('Partager entre équipes', 'partager les GPU'),
                                 ('Tâches de nuit', 'lancer la nuit')]):
        at = S.cue(kw)
        card(c, t, at, 90 + k * 460, y, 440, 240, RED if k == 1 else WHITE, 30, 'pop')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if k == 1 else DARK
            if k == 0:
                outline(c, 90, y, 440, 240, 30, PL)
            icon(c, t, at + 0.1, 'user' if k == 0 else 'clock', 310 + k * 460, y + 80, 60, fg)
            plain(c, s, 310 + k * 460, y + 180, 30, fg, 'Medium', 'center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Des *garde-fous* sur les coûts')
    b = S.cue('un budget mensuel')
    card(c, t, b, 90, 560, 900, 400, LIGHT, 32, 'up')
    al = S.cue('Des alertes')
    if prog(t, b, 0.5) > 0.4:
        small(c, 'Budget mensuel · équipe A', 140, 620, 20, DARK)
        f = 0.6 + 0.25 * ease(prog(t, al, 1.2))
        bar(c, t, b + 0.2, 140, 680, 800, 60, f, RED if t >= al + 0.8 else PL, WHITE, 1.0)
        mx = 140 + 800 * 0.8
        if t >= al:
            rrect(c, mx - 3, 660, 6, 100, 3, DARK)
            small(c, 'Alerte · 80 %', mx, 800, 18, DARK, align='center')
            icon(c, t, al + 0.8, 'bolt', 900, 870, 50, RED)
        if t >= b + 0.3:
            small(c, '100 %', 940, 800, 18, DARK, align='right')
    p = S.cue('un plafond par session')
    card(c, t, p, 90, 1000, 900, 250, LIGHT, 32, 'up')
    bo = S.cue('un agent qui boucle')
    if prog(t, p, 0.5) > 0.4:
        small(c, 'Session', 140, 1060, 20, DARK)
        for k in range(8):
            dot(c, t, bo + k * 0.12, 170 + k * 70, 1150, 20, PL if k < 6 else RED)
        if t >= p + 0.2:
            rrect(c, 700, 1090, 6, 120, 3, DARK)
        if t >= bo + 1.0:
            chip(c, t, bo + 1.0, 'Stop', 760, 1120, RED, WHITE, 30)
    v = S.cue('sa consommation')
    card(c, t, v, 90, 1290, 900, 130, RED, 30, 'left')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'eye', 170, 1355, 56, WHITE)
        reveal_plain(c, t, v + 0.2, 'Chacun voit sa consommation', 240, 1368, 36, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Des *GPU à nous*, ou le paiement à l\'usage ?', 'Des GPU à nous'),
        ('Qui *voit* le coût, et qui le *paie* ?', 'Qui voit'),
        ('Quel *plafond* par session et par équipe ?', 'quel plafond'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Comparez le *coût total* des GPU au coût à l\'usage, avec vos chiffres.', 'comparez le coût'),
        ('Mesurez les tokens, montrez le coût, posez des *plafonds*.', 'Mesurez les tokens'),
    ], "62 · Observabilité des agents")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Le coût d'un agent de code ne se lit pas sur une seule facture. "
        "Il se cache dans des GPU, les processeurs graphiques, qui dorment ; des boucles qui tournent ; "
        "des équipes qui ne voient jamais l'addition. "
        "La FinOps pilote ces coûts au grand jour.")),
    dict(kind='content', draw=s2, name="Coût total de possession ou paiement à l'usage", text=(
        "Premier arbitrage : acheter ou louer. Avec vos GPU, "
        "vous payez le coût total de possession, le TCO : l'investissement, l'énergie, l'exploitation. "
        "Dans le cloud, vous payez à l'usage, au token. "
        "Une voiture achetée coûte même à l'arrêt ; un taxi, seulement quand il roule. "
        "Aucun prix universel : calculez avec vos chiffres.")),
    dict(kind='content', draw=s3, name='Tokens par tâche, showback et chargeback', text=(
        "Ensuite, mesurez les tokens par développeur et par tâche. "
        "Une correction de bug en consomme peu, une refonte bien plus. "
        "Puis montrez le coût à chaque équipe : c'est le showback. "
        "Ou refacturez-le : c'est le chargeback. "
        "Comme un compteur d'eau par appartement.")),
    dict(kind='content', draw=s4, name="Le taux d'utilisation des GPU", text=(
        "Sur site, suivez le taux d'utilisation des GPU. "
        "Des GPU payés qui dorment la nuit, c'est de l'argent immobilisé. "
        "Exemple illustratif : chargés le jour, presque vides la nuit. "
        "Deux pistes : partager les GPU entre équipes, "
        "ou lancer la nuit les tâches non urgentes.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, posez des garde-fous : un budget mensuel par équipe ; "
        "des alertes, par exemple à quatre-vingts pour cent ; "
        "un plafond par session, pour qu'un agent qui boucle s'arrête à temps. "
        "Et montrez à chacun sa consommation , pour changer les habitudes.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Des GPU à nous, ou le paiement à l'usage ? "
        "Qui voit le coût, et qui le paie ? "
        "Et quel plafond par session et par équipe ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : comparez le coût total de vos GPU au coût à l'usage, avec vos chiffres. "
        "Mesurez les tokens, montrez le coût, posez budgets, alertes et plafonds. "
        "Prochaine capsule : l'observabilité des agents.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
