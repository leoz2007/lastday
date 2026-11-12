from engine import *  # noqa
from engine import _paint  # noqa

NUM = 34
TITLE = 'ENTRAÎNEMENT'
FULL_TITLE = 'Comment un modèle est entraîné'
SLUG = 'entrainement_modele'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def lines(c, t, at, x, y, widths, color, gap=40, h=20):
    """Lignes de texte schématiques qui apparaissent l'une après l'autre."""
    for j, w in enumerate(widths):
        if t >= at + j * 0.1:
            p = ease(prog(t, at + j * 0.1, 0.4))
            rrect(c, x, y + j * gap, max(h, w * p), h, h / 2, color)


def s1(c, t, S):
    opening(c, t, S, CAP, "Un modèle apprend d'abord à *deviner la suite*.")
    a = S.cue('deviner la suite')
    reveal_plain(c, t, a - 0.3, 'Le chat dort sur le ...', 90, 880, 46, WHITE, 'Light')
    cands = [('canapé', 0.62, RED), ('lit', 0.26, PL), ('toit', 0.08, PL)]
    for k, (s, f, col) in enumerate(cands):
        y = 960 + k * 100
        at = a + 0.2 + k * 0.2
        if t >= at:
            plain(c, s, 90, y + 40, 34, RED if k == 0 else WHITE, 'Medium')
        bar(c, t, at, 300, y + 12, 690, 36, f, col, WHITE, 0.8)
    if t >= a + 1.0:
        small(c, 'Probabilités · illustratif', 990, 1290, 20, WHITE, align='right')
    e = S.cue('Encore et encore')
    for k in range(9):
        icon(c, t, e + k * 0.06, 'doc', 120 + k * 60, 1380, 44, WHITE)
    ass = S.cue("L'assistant")
    chip(c, t, ass, "L'assistant : après", 990 - chip_width("L'assistant : après", 30), 1350, RED, WHITE, 30)


def s2(c, t, S):
    header(c, t, S, 'Étape 1', 'Le *préentraînement*')
    v = S.cue("d'immenses volumes")
    for k in range(10):
        i, j = k % 5, k // 5
        icon(c, t, v + k * 0.06, 'doc', 140 + i * 75, 600 + j * 95, 56, DARK)
    arrow(c, t, v + 0.6, 530, 650, 640, 650, DARK, 6, 18)
    p = S.cue('prédire le token suivant')
    card(c, t, v + 0.7, 660, 545, 330, 210, RED, 32, 'pop')
    if prog(t, v + 0.7, 0.5) > 0.4:
        icon(c, t, v + 0.8, 'brain', 825, 615, 70, WHITE)
        if t >= p:
            reveal_plain(c, t, p, 'Token suivant ?', 825, 715, 30, WHITE, 'Medium', 'center')
    x = 90
    for s, kw in [('La langue', 'la langue'), ('Des faits', 'des faits'), ('Des raisonnements', 'de raisonner')]:
        w = chip(c, t, S.cue(kw), s, x, 820, PLL, DARK, 32)
        x += w + 16
    cu = S.cue('date de coupure')
    card(c, t, cu, 90, 960, 900, 470, LIGHT, 36, 'up')
    if prog(t, cu, 0.5) > 0.4:
        small(c, 'Ce que le modèle connaît', 140, 1020, 20, DARK)
        bar(c, t, cu + 0.2, 140, 1150, 560, 40, 1.0, PL, WHITE, 0.8)
        rrect(c, 720, 1150, 220, 40, 20, WHITE)
        if t >= cu + 0.8:
            rrect(c, 707, 1100, 6, 140, 3, RED)
            reveal_plain(c, t, cu + 0.8, 'Date de coupure', 710, 1300, 30, RED, 'Medium', 'center')
            icon(c, t, cu + 1.1, 'cross', 830, 1080, 44, DARK)
            small(c, 'Après : inconnu', 830, 1370, 20, DARK, align='center')
            small(c, 'Avant : appris', 420, 1370, 20, DARK, align='center')


def s3(c, t, S):
    header(c, t, S, 'Étape 2', "L'ajustement aux *instructions*")
    ex = S.cue('des exemples de questions')
    card(c, t, ex, 90, 540, 900, 300, LIGHT, 36, 'up')
    if prog(t, ex, 0.5) > 0.4:
        label(c, t, ex + 0.1, "Exemple d'entraînement", 140, 570, PLL, DARK, 22)
        icon(c, t, ex + 0.2, 'user', 170, 680, 50, DARK)
        reveal_plain(c, t, ex + 0.3, 'Résume ce mail en une phrase.', 220, 692, 32, DARK)
        br = S.cue('bonnes réponses')
        icon(c, t, br, 'check', 170, 775, 50, RED)
        reveal_plain(c, t, br + 0.1, 'Bonne réponse rédigée', 220, 787, 32, RED, 'Medium')
    q = S.cue('suivre une consigne')
    box(c, t, q, 90, 900, 900, 100, 'Demande : « Résume ce mail »', DARK, WHITE, 32)
    pr = S.cue('prolonger le texte')
    rows = [('Avant', pr, 'cross', DARK, [600, 520, 640]),
            ('Après', S.cue('à répondre'), 'check', RED, [480, 300])]
    for k, (nm, at, ic, col, ws) in enumerate(rows):
        x = 90 + k * 460
        card(c, t, at, x, 1050, 440, 380, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, nm, x + 40, 1110, 22, col)
            icon(c, t, at + 0.2, ic, x + 380, 1100, 44, col)
            lines(c, t, at + 0.2, x + 40, 1160, [w * 0.55 for w in ws], PL if k == 0 else RED)
            small(c, 'Prolonge le texte' if k == 0 else 'Répond', x + 40, 1390, 20, col)


def s4(c, t, S):
    header(c, t, S, 'Étape 3', 'Les *préférences* humaines')
    cp = S.cue('comparent deux réponses')
    ch = S.cue('choisissent la meilleure')
    for k, nm in enumerate(['Réponse A', 'Réponse B']):
        x = 90 + k * 540
        at = cp + k * 0.25
        card(c, t, at, x, 560, 360, 400, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            win = k == 1 and t >= ch
            if win:
                outline(c, x, 560, 360, 400, 32, RED)
            small(c, nm, x + 40, 620, 22, RED if win else DARK)
            lines(c, t, at + 0.2, x + 40, 670, [280, 240, 270, 200, 250], PL)
            if win:
                dot(c, t, ch, x + 180, 890, 36, RED)
                icon(c, t, ch + 0.1, 'check', x + 180, 890, 40, WHITE)
    icon(c, t, cp + 0.3, 'user', 540, 720, 80, DARK)
    if t >= cp + 0.3:
        small(c, 'Personne', 540, 800, 20, DARK, align='center')
    arrow(c, t, ch, 540, 830, 610, 880, RED, 5, 16)
    pf = S.cue('apprend à préférer')
    card(c, t, pf, 90, 1020, 900, 410, LIGHT, 36, 'up')
    if prog(t, pf, 0.5) > 0.4:
        icon(c, t, pf + 0.1, 'brain', 190, 1130, 80, RED)
        reveal_plain(c, t, pf + 0.2, 'Le modèle préfère', 270, 1145, 40, DARK, 'Medium')
        x = 140
        for s, kw in [('Utile', 'utiles'), ('Claire', 'claires'), ('Prudente', 'prudentes')]:
            w = chip(c, t, S.cue(kw), s, x, 1260, RED, WHITE, 36)
            x += w + 20


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Trois *conséquences*')
    rows = [('clock', 'Connaissances datées', 'sont datées', 'Fournir les documents', 'fournissez-lui'),
            ('eye', 'Biais hérités', 'des biais', 'Tester sur vos publics', 'testez-le'),
            ('gear', 'Change avec la version', "d'une version", 'Relancer les evals', 'relancez vos evals')]
    for k, (ic, s, kw, act, kw2) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 290
        card(c, t, at, 90, y, 900, 250, LIGHT, 32, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 170, y + 85, 60, DARK)
            reveal_plain(c, t, at + 0.2, s, 240, y + 100, 38, DARK, 'Medium')
            a2 = S.cue(kw2)
            if t >= a2:
                arrow(c, t, a2, 240, y + 175, 300, y + 175, RED, 5, 16)
                chip(c, t, a2 + 0.2, act, 320, y + 148, RED, WHITE, 30)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("L'usage dépend-il d'*informations récentes* ?", 'Votre usage'),
        ('Quels *biais* pourraient toucher vos utilisateurs ?', 'Quels biais'),
        ('Qui relance les *evals* quand le modèle change ?', 'qui relance'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Prédire la suite, suivre des instructions, *préférer* les bonnes réponses.', 'en trois temps'),
        ('Connaissances *datées*, comportement qui change avec les versions.', 'Ses connaissances'),
    ], '35 · Fine-tuning efficace')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Avant de savoir répondre à vos questions, un modèle a appris une seule chose : deviner la suite d'un texte. "
        "Encore et encore, sur d'immenses volumes de textes. L'assistant poli ne vient qu'après.")),
    dict(kind='content', draw=s2, name='Le préentraînement', text=(
        "Première étape : le préentraînement. Le modèle lit d'immenses volumes de textes, "
        "et s'entraîne à prédire le token suivant, le petit morceau de texte qui vient ensuite. "
        "Il en tire la langue, des faits, des façons de raisonner. "
        "Mais ses connaissances s'arrêtent à une date de coupure. Ce qui s'est passé ensuite, il ne le sait pas.")),
    dict(kind='content', draw=s3, name="L'ajustement aux instructions", text=(
        "Deuxième étape : l'ajustement aux instructions. On lui montre des exemples de questions, "
        "avec de bonnes réponses rédigées. Il apprend à suivre une consigne, "
        "à répondre au lieu de simplement prolonger le texte. C'est là qu'il devient un assistant.")),
    dict(kind='content', draw=s4, name='Les préférences humaines', text=(
        "Troisième étape : apprendre des préférences humaines. Des personnes comparent deux réponses à la même question, "
        "et choisissent la meilleure. Au fil de très nombreuses comparaisons, le modèle apprend à préférer "
        "les réponses jugées utiles, claires et prudentes.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, trois conséquences. Ses connaissances sont datées : pour l'actualité, fournissez-lui les documents. "
        "Il hérite des biais de ses données : testez-le sur vos propres publics. "
        "Et son comportement peut changer d'une version à l'autre : relancez vos evals à chaque changement de modèle.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Votre usage dépend-il d'informations récentes ? "
        "Quels biais hérités des données pourraient toucher vos utilisateurs ? "
        "Et qui relance les evals quand le modèle change ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un modèle apprend en trois temps. Prédire la suite, suivre des instructions, "
        "préférer les bonnes réponses. Ses connaissances sont datées, et son comportement change avec les versions. "
        "Prochaine capsule : le fine-tuning efficace, pour adapter un modèle sans tout réentraîner.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
