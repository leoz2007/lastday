from engine import *  # noqa
from engine import _paint  # noqa

NUM = 12
TITLE = 'TEMPÉRATURE'
FULL_TITLE = 'Température et aléatoire'
SLUG = 'temperature_aleatoire'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def vbars(c, t, at, x, y_base, vals, bw=60, gap=24, hmax=260, hi=0, names=None, size=24):
    """Histogramme vertical qui pousse depuis la base. hi = indice mis en rouge."""
    for k, v in enumerate(vals):
        p = ease(prog(t, at + k * 0.08, 0.6))
        if p <= 0:
            continue
        bx = x + k * (bw + gap)
        h = max(8, hmax * v * p)
        rrect(c, bx, y_base - h, bw, h, 12, RED if k == hi else PL)
        if names:
            small(c, names[k], bx + bw / 2, y_base + 40, size, DARK, align='center', upper=False)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Même question, *autre* réponse.')
    a = S.cue('la même question')
    box(c, t, a, 290, 840, 500, 120, 'Un slogan pour l\'appli ?', WHITE, DARK, 34)
    r = S.cue('pas forcément')
    arrow(c, t, r, 440, 975, 300, 1070, WHITE, 6)
    arrow(c, t, r + 0.2, 640, 975, 780, 1070, WHITE, 6)
    for k, (s, x) in enumerate([('« Simple, rapide, à vous. »', 90), ('« Votre temps compte. »', 560)]):
        at = r + 0.3 + k * 0.3
        card(c, t, at, x, 1090, 430, 170, LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, f'Réponse {"AB"[k]}', x + 40, 1140, 20, DARK)
            reveal_plain(c, t, at + 0.1, s, x + 40, 1210, 28, DARK)
    v = S.cue("Et c'est")
    chip(c, t, v, "C'est voulu", 540, 1320, RED, WHITE, 36, align='center')


def s2(c, t, S):
    header(c, t, S, 'Le tirage', 'Un tirage parmi les *probables*')
    a = S.cue('une probabilité')
    card(c, t, a, 90, 540, 900, 560, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Après « Le ciel est »', 140, 610, 22, DARK)
        small(c, 'Probabilités illustratives', 940, 610, 20, DARK, align='right')
    words = ['bleu', 'gris', 'clair', 'vert']
    vals = [0.62, 0.25, 0.1, 0.03]
    g = S.cue('parfois')
    hi = 1 if t >= g else (0 if t >= S.cue('« bleu »') else -1)
    vbars(c, t, a + 0.3, 200, 990, vals, bw=120, gap=70, hmax=320, hi=hi, names=words, size=28)
    ts = S.cue('au sort')
    if t >= ts:
        ring(c, 830, 760, 40, DARK, 6)
        p = ease(prog(t, ts, 1.0))
        ang = p * 6.28 * 2
        c.drawLine(830, 760, 830 + 30 * math.cos(ang), 760 + 30 * math.sin(ang), _paint(RED, 8))
    su = S.cue('toute la suite')
    for k, (s, x) in enumerate([('bleu, idéal pour sortir', 90), ('gris, prévoyez un parapluie', 560)]):
        at = su + k * 0.3
        card(c, t, at, x, 1150, 430, 250, WHITE, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            outline(c, x, 1150, 430, 250, 30, RED if k else PL)
            small(c, f'Suite {"AB"[k]}', x + 40, 1205, 20, RED if k else DARK)
            text_block(c, t, at + 0.1, 'Le ciel est ' + s + '…', x + 40, 1270, 30, 'Medium', DARK,
                       RED, maxw=360, max_lines=3)


def s3(c, t, S):
    header(c, t, S, 'La température', 'Le réglage du *hasard*')
    b = S.cue('Basse')
    hh = S.cue('Haute')
    cards = [('Basse', b, [0.95, 0.15, 0.06, 0.03], 'Stable, prévisible'),
             ('Haute', hh, [0.55, 0.45, 0.38, 0.3], 'Varié, plus d\'écarts')]
    for k, (nm, at, vals, cap) in enumerate(cards):
        x = 90 + k * 460
        card(c, t, at, x, 540, 440, 470, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            label(c, t, at + 0.1, f'Température {nm.lower()}', x + 40, 570, RED if k else PLL,
                  WHITE if k else DARK, 22)
            vbars(c, t, at + 0.2, x + 60, 900, vals, bw=60, gap=25, hmax=230, hi=0)
            reveal_plain(c, t, at + 0.6, cap, x + 40, 970, 28, DARK)
    # curseur
    sl = S.cue('Le réglage se fait')
    y = 1090
    if t >= S.t0 + 0.4:
        small(c, 'Basse', 90, y - 20, 22, DARK)
        small(c, 'Haute', 990, y - 20, 22, DARK, align='right')
        rrect(c, 90, y, 900, 24, 12, PLL)
        if t < hh:
            u = 0.12
        else:
            u = lerp(0.12, 0.88, ease_io(prog(t, hh, 1.2)))
        rrect(c, 90, y, max(24, 900 * u), 24, 12, PL)
        c.drawCircle(90 + 900 * u, y + 12, 30, _paint(RED))
    card(c, t, sl, 90, 1200, 900, 190, DARK, 32, 'up')
    if prog(t, sl, 0.5) > 0.4:
        icon(c, t, sl + 0.1, 'code', 190, 1295, 70, WHITE)
        reveal_plain(c, t, sl + 0.2, "Dans l'appel d'API :", 290, 1280, 34, WHITE)
        reveal_plain(c, t, sl + 0.35, 'temperature = 0.2', 290, 1335, 34, RED)


def s4(c, t, S):
    header(c, t, S, 'Selon la tâche', 'Variété ou *stabilité*')
    cols = [('Variété', 'de la variété', 'Température haute', RED, WHITE,
             [('Un slogan', 'un slogan'), ('Des idées', 'des idées')]),
            ('Stabilité', 'la même réponse', 'Température basse', DARK, WHITE,
             [('Extraire un montant', 'extraire un montant'), ('Classer un email', 'classer un email')])]
    for k, (nm, kw, tl, fill, fg, items) in enumerate(cols):
        x = 90 + k * 460
        at = S.cue(kw)
        card(c, t, at, x, 540, 440, 160, fill, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            plain(c, nm, x + 220, 615, 40, fg, 'Medium', 'center')
            small(c, tl, x + 220, 665, 20, fg, align='center')
        for j, (s, kw2) in enumerate(items):
            box(c, t, S.cue(kw2), x, 740 + j * 140, 440, 115, s, LIGHT, DARK, 30, 'Medium', 28, 'left')
    # gros plan : plusieurs tirages
    v = S.cue('à chaque fois')
    card(c, t, v, 90, 1030, 900, 170, WHITE, 30, 'up')
    if prog(t, v, 0.5) > 0.4:
        outline(c, 90, 1030, 900, 170, 30, LIGHT, 5)
        small(c, 'Cinq essais, même email', 130, 1080, 20, DARK)
        for j in range(5):
            chip(c, t, v + 0.2 + j * 0.12, 'Facturation', 130 + j * 168, 1105, PLL, DARK, 22, padx=12)
    at = S.cue('Attention')
    card(c, t, at, 90, 1240, 900, 160, RED, 30, 'up')
    if prog(t, at, 0.5) > 0.4:
        reveal_plain(c, t, at + 0.2, 'Même à zéro, une réponse', 140, 1305, 34, WHITE)
        reveal_plain(c, t, at + 0.35, 'identique n\'est pas garantie', 140, 1355, 34, WHITE)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Tester *plusieurs* fois')
    e = S.cue('rejouent')
    card(c, t, S.cue('Un seul essai'), 90, 540, 900, 440, LIGHT, 36, 'up')
    if prog(t, S.cue('Un seul essai'), 0.5) > 0.4:
        label(c, t, S.cue('Un seul essai') + 0.1, 'Evals · chaque cas rejoué', 140, 575, PLL, DARK, 22)
    res = [[1, 1, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 1, 1]]
    for k, row in enumerate(res):
        y = 700 + k * 95
        if t >= e + k * 0.3:
            plain(c, f'Cas {k + 1}', 140, y + 12, 32, DARK)
        for j, ok in enumerate(row):
            at = e + k * 0.3 + j * 0.1
            x = 360 + j * 110
            dot(c, t, at, x, y, 34, RED if ok else DARK)
            icon(c, t, at + 0.1, 'check' if ok else 'cross', x, y, 40, WHITE)
    f = S.cue('une fonctionnalité')
    for k in range(3):
        at = f + 0.2 + k * 0.2
        x = 90 + k * 310
        card(c, t, at, x, 1030, 280, 200, WHITE, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            outline(c, x, 1030, 280, 200, 30, PL, 5)
            small(c, f'Variante {k + 1}', x + 30, 1080, 20, RED)
            for j, w in enumerate([210, 160, 190]):
                rrect(c, x + 30, 1110 + j * 36, w - k * 20, 20, 10, PLL)
    a = S.cue('autre suggestion')
    chip(c, t, a, 'Autre suggestion', 540, 1290, RED, WHITE, 36, align='center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Cette tâche demande-t-elle de la *créativité* ou de la *constance* ?', 'Cette tâche'),
        ('Deux réponses *différentes* sont-elles acceptables ?', 'Deux réponses'),
        ('Combien de fois *rejoue-t-on* chaque cas de test ?', 'combien de fois'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le modèle *tire au sort* parmi les mots probables.', 'le modèle tire'),
        ('Haute pour *créer*, basse pour *extraire* et classer.', 'La température'),
    ], '13 · Les modèles qui raisonnent')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Posez deux fois la même question à un modèle de langage. "
        "Vous n'obtiendrez pas forcément la même réponse. Et c'est voulu.")),
    dict(kind='content', draw=s2, name='Un tirage au sort', text=(
        "À chaque étape, le modèle calcule une probabilité pour chaque token possible. "
        "Puis il en tire un au sort, parmi les plus probables. "
        "Après « Le ciel est », il écrira souvent « bleu », parfois « gris ». "
        "Un tirage différent au début, et toute la suite change.")),
    dict(kind='content', draw=s3, name='La température', text=(
        "La température règle ce tirage. "
        "Basse, le modèle choisit presque toujours le token le plus probable : les réponses sont stables. "
        "Haute, les choix moins probables ont leur chance : plus de variété, mais aussi plus d'écarts. "
        "Le réglage se fait dans l'appel d'API, pas dans le prompt.")),
    dict(kind='content', draw=s4, name='Variété ou stabilité', text=(
        "Le bon réglage dépend de la tâche. Pour un slogan ou des idées, on veut de la variété : "
        "une température plus haute. "
        "Pour extraire un montant ou classer un email, on veut la même réponse à chaque fois : une température basse. "
        "Attention : même à zéro, la répétabilité parfaite n'est pas toujours garantie.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, l'aléatoire change la façon de tester. "
        "Un seul essai ne prouve rien : vos evals rejouent chaque cas plusieurs fois. "
        "Et l'aléatoire devient une fonctionnalité : proposer trois variantes, ou un bouton « autre suggestion ».")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Cette tâche demande-t-elle de la créativité ou de la constance ? "
        "Deux réponses différentes à la même question sont-elles acceptables ? "
        "Et combien de fois rejoue-t-on chaque cas de test ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le modèle tire ses mots au sort parmi les plus probables. "
        "La température règle ce hasard : haute pour créer, basse pour extraire et classer. "
        "Prochaine capsule : les modèles qui raisonnent avant de répondre.")),
]

import math  # noqa: E402
import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
