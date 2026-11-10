from engine import *  # noqa
from engine import _paint  # noqa

NUM = 30
TITLE = 'INFÉRENCE'
FULL_TITLE = "L'inférence, de près"
SLUG = 'inference_de_pres'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'

TOKENS = ['Résum', 'ez', 'ce', 'rapport', 'trimes', 'triel']


def token_row(c, t, ats, words, x, y, fill, fg, size=32, gap=12):
    """Rangée de jetons ; ats = instant d'apparition de chaque jeton. Renvoie les centres x."""
    cx, centers = x, []
    for at, w in zip(ats, words):
        wd = chip_width(w, size)
        chip(c, t, at, w, cx, y, fill, fg, size)
        centers.append(cx + wd / 2)
        cx += wd + gap
    return centers


def timeline(c, t, at, y, read_w, n_out, x0=140, x1=940, dur_read=0.8, step=0.08):
    """Lecture (barre claire), premier token (point rouge), puis tokens un par un."""
    bar(c, t, at, x0, y - 18, read_w, 36, 1.0, PL, LIGHT, dur_read)
    ft = at + dur_read
    dx = x0 + read_w + 26
    dot(c, t, ft, dx, y, 22, RED)
    gap = (x1 - dx - 30) / max(1, n_out - 1) if n_out > 1 else 0
    for k in range(n_out):
        a = ft + 0.15 + k * step
        if t >= a:
            p = ease(prog(t, a, 0.25))
            h = 44 * p
            rrect(c, dx + 30 + k * gap - 6, y - h / 2, 12, max(2, h), 6, RED)
    return dx


def stair(c, t, at, x, y, cached, n=5, cw=58, ch=34, g=8, step=0.3):
    """Escalier de calculs : à chaque nouveau token, la rangée des calculs nécessaires."""
    for k in range(n):
        a = at + k * step
        for j in range(k + 1):
            if j == k:
                col = RED
            else:
                col = WHITE if cached else PL
            card(c, t, a + j * 0.03, x + j * (cw + g), y + k * (ch + g), cw, ch, col, 8, 'pop')


def s1(c, t, S):
    opening(c, t, S, CAP, "Le modèle lit *d'un coup*, puis écrit *pas à pas*.")
    lt = S.cue('il lit')
    card(c, t, lt, 90, 830, 900, 230, WHITE, 36, 'up')
    if prog(t, lt, 0.5) > 0.4:
        small(c, "Lire : tout d'un coup", 140, 890, 22, DARK)
        token_row(c, t, [lt + 0.4] * 6, TOKENS, 140, 940, PL, DARK, 32)
    ec = S.cue('puis écrit')
    card(c, t, ec, 90, 1090, 900, 230, WHITE, 36, 'up')
    if prog(t, ec, 0.5) > 0.4:
        small(c, 'Écrire : un morceau après l\'autre', 140, 1150, 22, DARK)
        out = ['Le', 'chiffre', "d'affaires", 'progresse']
        token_row(c, t, [ec + 0.4 + k * 0.45 for k in range(4)], out, 140, 1200, RED, WHITE, 32)
    x = 90
    for s, kw, ic in [('Les délais', 'les délais', 'clock'), ('La facture', 'la facture', 'coin')]:
        at = S.cue(kw)
        icon(c, t, at, ic, x + 30, 1390, 50, WHITE)
        w = chip(c, t, at + 0.1, s, x + 70, 1360, WHITE, DARK, 30)
        x += w + 130


def s2(c, t, S):
    header(c, t, S, 'Tokens et prefill', "Lire l'entrée *d'un coup*")
    d = S.cue('découpé en tokens')
    card(c, t, d, 90, 540, 900, 200, LIGHT, 36, 'up')
    centers = []
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Découpage en tokens · illustratif', 140, 600, 20, DARK)
        centers = token_row(c, t, [d + 0.3 + k * 0.12 for k in range(6)], TOKENS, 140, 635, WHITE, DARK, 32)
    pf = S.cue('en parallèle')
    for x in centers:
        arrow(c, t, pf, x, 760, x, 830, RED, 5, 16)
    box(c, t, S.cue('prefill'), 90, 845, 900, 120, 'Lecture du prompt (prefill)', DARK, WHITE, 36)
    pg = S.cue('la page entière')
    card(c, t, pg, 90, 1010, 900, 180, LIGHT, 32, 'up')
    if prog(t, pg, 0.5) > 0.4:
        icon(c, t, pg + 0.1, 'eye', 170, 1100, 60, RED)
        icon(c, t, pg + 0.2, 'doc', 260, 1100, 70, DARK)
        reveal_plain(c, t, pg + 0.3, 'Toute la page, en une fois', 330, 1112, 34, DARK)
    lg = S.cue('très longue entrée')
    card(c, t, lg, 90, 1230, 900, 200, LIGHT, 32, 'up')
    if prog(t, lg, 0.5) > 0.4:
        small(c, 'Temps de lecture · illustratif', 140, 1285, 20, DARK)
        plain(c, 'Entrée courte', 140, 1342, 28, DARK)
        bar(c, t, lg + 0.2, 470, 1318, 470, 30, 0.15, PL, WHITE, 0.5)
        plain(c, 'Très longue entrée', 140, 1397, 28, RED)
        bar(c, t, lg + 0.4, 470, 1373, 470, 30, 0.8, RED, WHITE, 1.0)


def s3(c, t, S):
    header(c, t, S, 'Décodage et cache KV', 'Écrire *token par token*')
    p = S.cue('produit un token')
    out = ['Le', 'chiffre', "d'affaires", 'progresse']
    ats = [p, S.cue('puis le suivant'), S.cue('puis le suivant', 2), S.cue('puis le suivant', 2) + 0.5]
    token_row(c, t, ats, out, 90, 545, RED, WHITE, 34, 16)
    dp = S.cue('dépend de ceux')
    if t >= dp:
        reveal_plain(c, t, dp, 'Chacun dépend des précédents', 90, 690, 30, DARK, 'Medium')
    ck = S.cue('garde en mémoire')
    card(c, t, ck, 90, 740, 900, 620, LIGHT, 36, 'up')
    if prog(t, ck, 0.5) > 0.4:
        small(c, 'Sans cache', 140, 805, 20, DARK)
        small(c, 'Avec cache KV', 590, 805, 20, RED)
        small(c, 'Calculs à chaque nouveau token', 140, 850, 18, DARK)
        stair(c, t, ck + 0.3, 140, 890, False)
        kv = S.cue('le cache KV')
        stair(c, t, kv, 590, 890, True)
        if t >= kv + 1.2:
            leg = [(RED, 'Nouveau calcul'), (PL, 'Calcul refait'), (WHITE, 'Gardé en mémoire')]
            for j, (col, s) in enumerate(leg):
                y = 1170 + j * 52
                rrect(c, 140, y, 58, 34, 8, col)
                plain(c, s, 220, y + 28, 28, DARK)
        rt = S.cue('recalculerait tout')
        if t >= rt:
            icon(c, t, rt, 'bolt', 610, 1260, 50, RED)
            text_block(c, t, rt + 0.1, 'Le cache évite de *tout refaire*', 660, 1250, 30, 'Medium',
                       DARK, RED, maxw=290, max_lines=2)


def s4(c, t, S):
    header(c, t, S, 'Deux mesures', 'Le *premier token*, puis le *débit*')
    a = S.cue('le délai avant le premier token')
    card(c, t, a, 90, 540, 900, 300, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Un appel, dans le temps', 140, 600, 20, DARK)
        dx = timeline(c, t, a + 0.2, 690, 260, 12)
        if t >= a + 1.0:
            small(c, 'Délai avant le 1er token', 140, 770, 18, DARK)
        db = S.cue('le débit')
        if t >= db:
            small(c, 'Débit : tokens par seconde', 940, 770, 18, RED, align='right')
    ex = [('Résumer 100 pages', 'cent pages', 620, 3, "Attente au début", 'au début'),
          ('Rédiger un long courrier', 'long courrier', 100, 16, "Attente dans l'écriture", "dans l'écriture")]
    for k, (s, kw, rw, n, lab, kw2) in enumerate(ex):
        at = S.cue(kw)
        y = 880 + k * 280
        card(c, t, at, 90, y, 900, 250, LIGHT, 36, 'up')
        if prog(t, at, 0.5) > 0.4:
            plain(c, s, 140, y + 65, 30, DARK)
            timeline(c, t, at + 0.2, y + 130, rw, n, dur_read=0.4 + rw / 800, step=0.06)
            a2 = S.cue(kw2)
            if t >= a2:
                reveal_plain(c, t, a2, lab, 140, y + 210, 28, RED, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Pourquoi la sortie *coûte plus*')
    e = S.cue('lue en bloc')
    card(c, t, e, 90, 540, 430, 330, LIGHT, 32, 'up')
    if prog(t, e, 0.5) > 0.4:
        small(c, 'Entrée', 140, 600, 20, DARK)
        rrect(c, 140, 630, 330, 130, 20, WHITE)
        for k in range(6):
            card(c, t, e + 0.2, 160 + k * 50, 660, 40, 70, PL, 8, 'pop')
        small(c, '1 passe, en parallèle', 140, 820, 18, DARK)
    so = S.cue('sa propre étape')
    card(c, t, so, 560, 540, 430, 330, LIGHT, 32, 'up')
    if prog(t, so, 0.5) > 0.4:
        small(c, 'Sortie', 610, 600, 20, RED)
        for k in range(6):
            card(c, t, so + 0.2 + k * 0.2, 630 + k * 50, 730 - k * 18, 40, 30, RED, 8, 'pop')
        small(c, '1 étape par token', 610, 820, 18, RED)
    pr = S.cue('facturée plus cher')
    card(c, t, pr, 90, 910, 900, 230, LIGHT, 32, 'up')
    if prog(t, pr, 0.5) > 0.4:
        small(c, 'Prix par token · illustratif', 140, 970, 20, DARK)
        plain(c, 'Entrée', 140, 1030, 28, DARK)
        bar(c, t, pr + 0.2, 330, 1006, 610, 30, 0.25, PL, WHITE, 0.5)
        plain(c, 'Sortie', 140, 1095, 28, RED)
        bar(c, t, pr + 0.4, 330, 1071, 610, 30, 0.8, RED, WHITE, 0.8)
    fl = S.cue("au fil de l'eau")
    card(c, t, fl, 90, 1180, 520, 250, LIGHT, 32, 'up')
    if prog(t, fl, 0.5) > 0.4:
        small(c, "Au fil de l'eau", 140, 1240, 20, DARK)
        u = clamp((t - fl - 0.3) / 2.0)
        for j, w in enumerate([420, 360, 300]):
            ww = clamp(u * 3 - j) * w
            if ww > 0:
                rrect(c, 140, 1275 + j * 45, max(20, ww), 20, 10, RED if j == 2 else PL)
    ct = S.cue('réponses courtes')
    card(c, t, ct, 640, 1180, 350, 250, RED, 32, 'up')
    if prog(t, ct, 0.5) > 0.4:
        icon(c, t, ct + 0.1, 'target', 815, 1265, 60, WHITE)
        plain(c, 'Réponses courtes', 815, 1375, 30, WHITE, 'Medium', 'center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Quel *délai avant le premier mot* l'utilisateur accepte-t-il ?", 'Quel délai'),
        ('Les réponses doivent-elles être *longues* ?', 'Les réponses'),
        ("La réponse peut-elle s'afficher *au fil de l'eau* ?", 'Et la réponse'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Le modèle lit *d'un coup*, puis écrit *token par token*.", 'le modèle lit'),
        ("L'entrée pèse sur le *délai initial*, la sortie sur le *temps total*.", "l'entrée pèse"),
    ], "31 · Optimiser l'inférence")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle ne lit pas et n'écrit pas au même rythme. "
        "Il lit tout votre texte d'un coup, puis écrit morceau par morceau. "
        "Ce détail explique les délais, et la facture.")),
    dict(kind='content', draw=s2, name='Les tokens et la lecture du prompt', text=(
        "D'abord, le texte est découpé en tokens, des morceaux de mots. "
        "Vient ensuite la lecture du prompt, le prefill, ou préremplissage. "
        "Le modèle traite toute l'entrée d'un coup, en parallèle, comme un lecteur qui verrait la page entière. "
        "Mais une très longue entrée prend quand même du temps.")),
    dict(kind='content', draw=s3, name='Le décodage et le cache KV', text=(
        "Puis vient la génération, ou décodage. "
        "Le modèle produit un token, puis le suivant, puis le suivant. "
        "Chacun dépend de ceux d'avant : impossible de les calculer en parallèle. "
        "Pour aller plus vite, il garde en mémoire ses calculs déjà faits : c'est le cache KV. "
        "Sans lui, chaque token recalculerait tout.")),
    dict(kind='content', draw=s4, name='Deux mesures : premier token et débit', text=(
        "D'où deux mesures : le délai avant le premier token, puis le débit, en tokens par seconde. "
        "Une longue entrée allonge surtout le délai initial : pour résumer cent pages, l'attente est au début. "
        "Une longue sortie allonge le temps total : pour un long courrier, l'attente est dans l'écriture.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, la sortie est en général facturée plus cher que l'entrée. "
        "Une raison : l'entrée est lue en bloc, alors que chaque token de sortie demande sa propre étape de calcul. "
        "Deux réflexes : afficher la réponse au fil de l'eau, et demander des réponses courtes.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel délai avant le premier mot l'utilisateur accepte-t-il ? "
        "Les réponses doivent-elles être longues ? "
        "Et la réponse peut-elle s'afficher au fil de l'eau ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le modèle lit l'entrée d'un coup, puis écrit token par token. "
        "L'entrée pèse surtout sur le délai initial, la sortie sur le temps total. "
        "Prochaine capsule : optimiser l'inférence, pour répondre plus vite et moins cher.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
