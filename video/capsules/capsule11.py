from engine import *  # noqa
from engine import _paint  # noqa

NUM = 11
TITLE = 'HALLUCINATIONS'
FULL_TITLE = 'Hallucinations'
SLUG = 'hallucinations'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un LLM peut se tromper avec *aplomb*.')
    a = S.cue('une réponse fausse')
    card(c, t, a, 90, 840, 900, 230, WHITE, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 190, 955, 80, DARK)
        small(c, 'Réponse du modèle', 270, 920, 22, DARK)
        reveal_plain(c, t, a + 0.2, 'Le contrat a été signé le 12 mai 2019.', 270, 990, 34, DARK)
    ap = S.cue('aplomb')
    rows = [('Assurance', ap, 1.0, RED), ('Vérification', S.cue('il se trompe'), 0.0, PL)]
    for k, (nm, at, fr, col) in enumerate(rows):
        y = 1130 + k * 130
        if t >= at:
            small(c, nm, 90, y, 24, WHITE)
            bar(c, t, at, 90, y + 25, 760, 40, fr, col, PL if fr else LIGHT, 0.8)
    icon(c, t, S.cue('il se trompe') + 0.4, 'cross', 930, 1305, 60, RED, bg=WHITE)


def s2(c, t, S):
    header(c, t, S, 'Le mécanisme', 'Il prédit le *plausible*')
    a = S.cue('base de faits')
    card(c, t, a, 90, 540, 900, 150, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'db', 170, 615, 60, DARK)
        reveal_plain(c, t, a + 0.2, 'Pas de base de faits consultée', 250, 630, 34, DARK)
        icon(c, t, a + 0.5, 'cross', 930, 615, 44, RED)
    m = S.cue('mot après mot')
    if t >= m:
        small(c, 'Suites plausibles après « Il est né le »', 90, 760, 22, DARK)
    cands = [('12 mars', 0.75), ('3 juin', 0.55), ('28 mai', 0.4)]
    for k, (s, fr) in enumerate(cands):
        at = m + 0.2 + k * 0.2
        y = 790 + k * 80
        if t >= at:
            plain(c, s, 90, y + 42, 32, DARK)
        bar(c, t, at, 300, y + 14, 690, 36, fr, RED if k == 0 else PL, PLL, 0.7)
    d = S.cue('date crédible')
    card(c, t, d, 90, 1060, 900, 130, WHITE, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        outline(c, 90, 1060, 900, 130, 32, RED)
        plain(c, 'Né le 12 mars 1974', 540, 1140, 40, DARK, 'Medium', 'center')
    p = S.cue('Plausible ne veut')
    w = chip(c, t, p, 'Plausible', 90, 1240, RED, WHITE, 34)
    icon(c, t, p + 0.2, 'check', 90 + w + 50, 1270, 44, RED)
    x2 = 560
    w2 = chip(c, t, p + 0.5, 'Vrai ?', x2, 1240, DARK, WHITE, 34)
    icon(c, t, p + 0.7, 'cross', x2 + w2 + 50, 1270, 44, RED)
    h = S.cue('hallucination')
    if t >= h:
        reveal_plain(c, t, h, 'Hallucination', 540, 1410, 44, RED, 'Medium', 'center')


def s3(c, t, S):
    header(c, t, S, 'Les zones à risque', 'Quand le risque *grimpe*')
    zones = [('target', 'Question *précise*', 'très précise'),
             ('search', 'Sujet *rare*', 'sujet rare'),
             ('clock', 'Info *récente*', 'information récente')]
    for k, (ic, s, kw) in enumerate(zones):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 560, 280, 260, LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 650, 70, RED)
            text_block(c, t, at + 0.2, s, x + 140, 770, 30, 'Medium', DARK, RED, maxw=250,
                       align='center', max_lines=2)
    pr = S.cue('un chiffre')
    x = 90
    for s, kw in [('Un chiffre', 'un chiffre'), ('Une date', 'une date'), ('Une référence', 'une référence')]:
        w = chip(c, t, S.cue(kw), s, x, 860, PLL, DARK, 30)
        x += w + 16
    ex = S.cue('Exemple classique')
    card(c, t, ex, 90, 990, 900, 400, LIGHT, 36, 'up')
    if prog(t, ex, 0.5) > 0.4:
        label(c, t, ex + 0.1, 'Exemple fictif', 140, 1030, PLL, DARK, 22)
        icon(c, t, ex + 0.2, 'doc', 190, 1190, 80, DARK)
        reveal_plain(c, t, ex + 0.3, '« Selon l\'article L. 9999-1', 270, 1170, 34, DARK)
        reveal_plain(c, t, ex + 0.45, 'du code du travail… »', 270, 1220, 34, DARK)
    n = S.cue("n'existe pas")
    chip(c, t, n, 'Numéro inexistant', 270, 1280, RED, WHITE, 32)


def s4(c, t, S):
    header(c, t, S, 'Les parades', 'Quatre *garde-fous*')
    a = S.cue('Fournir des sources')
    card(c, t, a, 90, 540, 300, 170, LIGHT, 30, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'db', 240, 600, 50, RED)
        plain(c, 'Vos documents', 240, 680, 28, DARK, 'Medium', 'center')
    r = S.cue('avec le RAG')
    arrow(c, t, r, 400, 625, 580, 625, DARK, 6)
    if t >= r:
        small(c, 'RAG', 490, 600, 20, DARK, align='center')
    box(c, t, r + 0.3, 590, 540, 400, 170, 'Modèle', DARK, WHITE, 38)
    d = S.cue('Autoriser le doute')
    card(c, t, d, 90, 750, 900, 150, PLL, 30, 'left')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Consigne', 130, 800, 20, DARK)
        reveal_plain(c, t, d + 0.2, '« Sinon, dites que vous ne savez pas. »', 130, 860, 34, DARK)
    ci = S.cue('Exiger des citations')
    card(c, t, ci, 90, 940, 900, 230, LIGHT, 30, 'up')
    if prog(t, ci, 0.5) > 0.4:
        small(c, 'Réponse', 130, 990, 20, DARK)
        for k, (w, ref) in enumerate([(560, '1'), (420, '2')]):
            y = 1020 + k * 60
            bar(c, t, ci + 0.2 + k * 0.15, 130, y, w, 28, 1.0, PL, PL, 0.4)
            chip(c, t, ci + 0.5 + k * 0.2, f'[{ref}]', 130 + w + 20, y - 10, RED, WHITE, 26)
        small(c, 'Chaque affirmation pointe vers sa source', 130, 1145, 20, DARK)
    v = S.cue('vérification automatique')
    card(c, t, v, 90, 1210, 900, 180, RED, 30, 'up')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'check', 180, 1300, 70, WHITE)
        reveal_plain(c, t, v + 0.2, 'Contrôle : la réponse', 260, 1285, 34, WHITE)
        reveal_plain(c, t, v + 0.35, "s'appuie sur les sources", 260, 1335, 34, WHITE)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Réduire et *mesurer*')
    m = S.cue('on le mesure')
    card(c, t, m, 90, 540, 900, 380, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        label(c, t, m + 0.1, 'Evals · chiffres illustratifs', 140, 575, PLL, DARK, 22)
    e = S.cue('Vos evals')
    vals = [('V1', 0.9), ('V2', 0.55), ('V3', 0.3)]
    for k, (nm, fr) in enumerate(vals):
        y = 670 + k * 75
        if t >= e + k * 0.3:
            plain(c, nm, 140, y + 30, 30, DARK)
        bar(c, t, e + k * 0.3, 230, y + 6, 700, 32, fr, RED if k == 2 else PL, WHITE, 0.7)
    if t >= e:
        small(c, 'Réponses inventées sur des cas réels', 140, 895, 20, DARK)
    s = S.cue('affiche les sources')
    card(c, t, s, 90, 970, 900, 190, WHITE, 32, 'up')
    if prog(t, s, 0.5) > 0.4:
        outline(c, 90, 970, 900, 190, 32, LIGHT, 5)
        icon(c, t, s + 0.1, 'chat', 170, 1050, 60, DARK)
        bar(c, t, s + 0.2, 240, 1015, 600, 26, 1.0, PL, PL, 0.4)
        chip(c, t, s + 0.4, 'Source : contrat.pdf, p. 4', 240, 1065, PLL, DARK, 28)
    j = S.cue('je ne sais pas')
    card(c, t, j, 90, 1200, 900, 190, RED, 32, 'up')
    if prog(t, j, 0.5) > 0.4:
        icon(c, t, j + 0.1, 'chat', 170, 1295, 60, WHITE)
        reveal_plain(c, t, j + 0.2, '« Je ne trouve pas cette information.', 240, 1280, 30, WHITE)
        reveal_plain(c, t, j + 0.35, 'Voici qui contacter. »', 240, 1328, 30, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Que coûte une *réponse fausse* ici ?', 'Que coûte'),
        ('Sur quelles *sources* le modèle s\'appuie-t-il ?', 'Sur quelles sources'),
        ('Que fait l\'assistant quand il *ne trouve pas* ?', "que fait l'assistant"),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un LLM prédit du *plausible*, il ne vérifie pas.', 'un LLM prédit'),
        ('Sources, citations et evals *réduisent* le risque.', 'Les sources'),
    ], '12 · Température et aléatoire')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle de langage peut donner une réponse fausse, avec un aplomb parfait. "
        "Et il ne sait pas qu'il se trompe.")),
    dict(kind='content', draw=s2, name='Pourquoi il invente', text=(
        "Pourquoi ? Un LLM ne consulte pas une base de faits. "
        "Il prédit, mot après mot, la suite la plus plausible. "
        "Demandez-lui la date de naissance d'un inconnu : il peut produire une date crédible, au bon format. "
        "Plausible ne veut pas dire vrai. On appelle ça une hallucination.")),
    dict(kind='content', draw=s3, name='Les situations à risque', text=(
        "Le risque grimpe dans trois situations. Une question très précise : un chiffre, une date, une référence. "
        "Un sujet rare, peu présent dans ses données d'entraînement. "
        "Ou une information récente, postérieure à son entraînement. "
        "Exemple classique : la citation d'un article de loi, avec un numéro qui n'existe pas.")),
    dict(kind='content', draw=s4, name='Les parades', text=(
        "Plusieurs parades existent. Fournir des sources : avec le RAG, le modèle répond à partir de vos documents. "
        "Autoriser le doute, avec une consigne claire : si l'information manque, dites que vous ne savez pas. "
        "Exiger des citations, pour vérifier chaque affirmation. "
        "Et ajouter une vérification automatique, qui contrôle que la réponse s'appuie sur les sources.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, on ne supprime pas le risque : on le réduit, et on le mesure. "
        "Vos evals comptent les réponses inventées sur des cas réels. "
        "L'interface affiche les sources et rend le doute acceptable : "
        "un « je ne sais pas » vaut mieux qu'une erreur sûre d'elle.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Que coûte une réponse fausse dans ce cas d'usage ? "
        "Sur quelles sources le modèle doit-il s'appuyer ? "
        "Et que fait l'assistant quand il ne trouve pas la réponse ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un LLM prédit du texte plausible, il ne vérifie pas. "
        "Les sources, les citations et les evals réduisent le risque. "
        "Prochaine capsule : la température, ou pourquoi la même question ne donne pas toujours la même réponse.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
