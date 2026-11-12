from engine import *  # noqa
from engine import _paint  # noqa

NUM = 4
TITLE = 'RAG'
FULL_TITLE = 'RAG et embeddings'
SLUG = 'rag_embeddings'
NEXT_CUE = 'prochaine capsule'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un LLM ne connaît pas vos *clients*.')
    a = S.cue('vos contrats')
    for k, (s, kw) in enumerate([('Contrats', 'vos contrats'), ('Procédures', 'vos procédures')]):
        at = S.cue(kw)
        box(c, t, at, 90, 820 + k * 200, 380, 150, s, LIGHT, DARK, 36, 'Medium', 30, 'left')
    llm = S.t0 + 0.6
    box(c, t, llm, 650, 900, 340, 220, 'LLM', RED, WHITE, 56, 'Light', 40)
    if t < S.cue('RAG'):
        for k in range(2):
            icon(c, t, a + 0.3 + k * 0.4, 'cross', 560, 895 + k * 200, 50, PL)
    rg = S.cue('RAG')
    for k in range(2):
        arrow(c, t, rg + k * 0.2, 480, 895 + k * 200, 640, 1010, RED, 7)
    bd = S.cue('bons documents')
    chip(c, t, bd, 'les bons documents, au bon moment', 90, 1300, PLL, DARK, 36)


def s2(c, t, S):
    header(c, t, S, 'Étape 1 · Découper', 'Des *morceaux* de documents')
    a = S.t0 + 0.4
    card(c, t, a, 90, 560, 330, 520, LIGHT, 30, 'up')
    if t >= a + 0.2:
        icon(c, t, a + 0.2, 'doc', 255, 650, 80, DARK)
        for j in range(6):
            bar(c, t, a + 0.3, 130, 740 + j * 50, 250, 20, 0.9 - (j % 3) * 0.15, PL, WHITE, 0.4)
        small(c, 'Guide client', 255, 1050, 22, DARK, align='center')
    d = S.cue('on découpe')
    for j in range(4):
        y = 560 + j * 135
        arrow(c, t, d + j * 0.15, 440, 820, 520, y + 55, DARK, 4, 14)
        card(c, t, d + 0.2 + j * 0.15, 540, y, 450, 110, LIGHT, 26, 'left')
        if t >= d + 0.4 + j * 0.15:
            bar(c, t, d + 0.4 + j * 0.15, 570, y + 30, 230, 18, 0.95, PL, WHITE, 0.3)
            bar(c, t, d + 0.4 + j * 0.15, 570, y + 62, 230, 18, 0.6, PL, WHITE, 0.3)
    ch = S.cue('chunks')
    label(c, t, ch, 'Chunks', 540, 1110, RED, WHITE)
    src = S.cue('sa source')
    for j in range(4):
        chip(c, t, src + j * 0.12, f'p. {12 + j * 7}', 830, 560 + j * 135 + 28, WHITE, DARK, 26, 'Bold', 14)
    ex = S.cue('deux cents pages')
    box(c, t, ex, 90, 1200, 900, 140, '200 pages = des *centaines* de passages', LIGHT, DARK, 36, 'Medium', 30, 'up')
    if t >= src:
        small(c, 'Exemple illustratif', 90, 1390, 22, DARK)


def s3(c, t, S):
    header(c, t, S, 'Étape 2 · Embeddings', 'Le *sens* en nombres')
    e = S.cue('embedding')
    box(c, t, e, 90, 560, 330, 120, 'Un passage', LIGHT, DARK, 34)
    arrow(c, t, e + 0.3, 430, 620, 510, 620, DARK, 6)
    nb = S.cue('liste de nombres')
    chip(c, t, nb, '0,12   0,87   0,33   …', 530, 590, PLL, DARK, 34)
    # espace des sens
    pr = S.cue('proches')
    card(c, t, pr - 0.3, 90, 760, 900, 680, LIGHT, 36)
    import random
    rnd = random.Random(4)
    if t >= pr - 0.1:
        for k in range(26):
            x, y = 140 + rnd.random() * 800, 800 + rnd.random() * 600
            if 520 < x < 960 and 980 < y < 1160:
                continue
            dot(c, t, pr - 0.1 + k * 0.02, x, y, 9, PL)
    r1, r2 = S.cue('« Résilier'), S.cue('« mettre fin')
    dot(c, t, r1, 600, 1050, 18, RED)
    dot(c, t, r2, 660, 1110, 18, RED)
    if t >= r1:
        chip(c, t, r1 + 0.1, 'Résilier mon contrat', 330, 960, WHITE, DARK, 30)
    if t >= r2:
        chip(c, t, r2 + 0.1, 'Mettre fin à mon abonnement', 300, 1160, WHITE, DARK, 30)
    cc = S.cue('côte à côte')
    if t >= cc:
        p = ease(prog(t, cc, 0.6))
        c.drawCircle(630, 1080, 80 * p, _paint(RED, 4))


def s4(c, t, S):
    header(c, t, S, 'Étape 3 · Retrouver', 'Chercher, puis *citer*')
    q = S.cue('pose une question')
    box(c, t, q, 90, 560, 380, 150, 'Question', LIGHT, DARK, 38)
    bv = S.cue('base vectorielle')
    arrow(c, t, bv - 0.2, 480, 635, 600, 635, DARK, 6)
    card(c, t, bv, 610, 560, 380, 150, LIGHT, 30)
    if t >= bv + 0.2:
        icon(c, t, bv + 0.1, 'db', 690, 635, 60, RED)
        plain(c, 'Base', 750, 625, 32, DARK)
        plain(c, 'vectorielle', 750, 665, 32, DARK)
    pp = S.cue('plus proches')
    arrow(c, t, pp - 0.2, 800, 720, 800, 780, DARK, 6)
    for k in range(3):
        x = 90 + k * 310
        card(c, t, pp + k * 0.15, x, 800, 280, 140, WHITE, 26, 'up')
        if t >= pp + k * 0.15 + 0.2:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, 800, x + 280, 940), 26, 26), _paint(RED, 4))
            bar(c, t, pp + k * 0.15 + 0.2, x + 30, 840, 220, 18, 0.9, PL, PLL, 0.3)
            bar(c, t, pp + k * 0.15 + 0.2, x + 30, 880, 220, 18, 0.6, PL, PLL, 0.3)
            small(c, f'Source {k + 1}', x + 140, 990, 20, DARK, align='center')
    m = S.cue('au modèle')
    arrow(c, t, m - 0.2, 280, 1010, 280, 1070, DARK, 6)
    box(c, t, m, 90, 1080, 380, 150, 'LLM', RED, WHITE, 48, 'Light', 30)
    arrow(c, t, m + 0.3, 480, 1155, 600, 1155, DARK, 6)
    card(c, t, m + 0.4, 610, 1080, 380, 150, LIGHT, 30)
    if t >= m + 0.6:
        plain(c, 'Réponse', 640, 1140, 34, DARK)
    ci = S.cue('en citant')
    for k in range(2):
        chip(c, t, ci + k * 0.2, f'[{k + 1}]', 640 + k * 90, 1160, RED, WHITE, 26, 'Bold', 14)
    u = S.cue('uniquement')
    if t >= u:
        reveal_plain(c, t, u, 'Uniquement à partir des passages', 90, 1320, 34, RED)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "La qualité vient des *documents*")
    o = S.cue('obsolètes')
    for k, (s, kw) in enumerate([('Sources obsolètes', 'obsolètes'), ('Sources contradictoires', 'contradictoires')]):
        at = S.cue(kw)
        box(c, t, at, 90, 560 + k * 150, 560, 120, s, LIGHT, DARK, 34, 'Medium', 30, 'left')
    mr = S.cue('mauvaises réponses')
    arrow(c, t, mr, 660, 695, 740, 695, DARK, 6)
    box(c, t, mr + 0.2, 750, 600, 240, 190, 'Mauvaise *réponse*', WHITE, DARK, 32)
    if t >= mr + 0.4:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(750, 600, 990, 790), 30, 30), _paint(RED, 4))
    ex = S.cue('excellent modèle')
    chip(c, t, ex, 'même avec un excellent modèle', 90, 880, PLL, DARK, 30)
    ci = S.cue('Les citations')
    card(c, t, ci, 90, 1000, 900, 420, LIGHT, 36, 'up')
    if prog(t, ci, 0.5) > 0.4:
        label(c, t, ci + 0.1, 'Citations', 140, 1040, RED, WHITE, 22)
        bar(c, t, ci + 0.2, 140, 1130, 500, 22, 1.0, PL, WHITE, 0.4)
        bar(c, t, ci + 0.2, 140, 1170, 380, 22, 1.0, PL, WHITE, 0.4)
        chip(c, t, ci + 0.5, '[1] guide.pdf · p. 12', 680, 1160, WHITE, RED, 26, 'Bold', 14)
        v = S.cue('vérifier')
        icon(c, t, v, 'eye', 190, 1320, 60, RED)
        reveal_plain(c, t, v, "L'utilisateur vérifie", 240, 1332, 32, DARK)
        e = S.cue('une erreur')
        icon(c, t, e, 'search', 620, 1320, 50, RED)
        reveal_plain(c, t, e, "Vous déboguez", 670, 1332, 32, DARK)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles sources sont *fiables*, et qui les met à jour ?', 'Quelles sources'),
        ('Qui a le *droit de voir* quel document ?', 'Qui a le droit'),
        ("Que répond l'assistant quand *rien de pertinent* n'est trouvé ?", "Que doit répondre"),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le RAG : *découper*, *retrouver*, puis répondre en *citant*.', 'le RAG'),
        ("Le modèle ne sait que ce qu'on lui *montre*.", 'ne sait que'),
    ], '05 · Agents, tool use et MCP')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un LLM ne connaît pas vos clients. Il ne connaît ni vos contrats, ni vos procédures. "
        "Le RAG sert justement à lui donner les bons documents, au bon moment.")),
    dict(kind='content', draw=s2, name='Étape un : découper', text=(
        "Première étape : on découpe les documents du client en petits morceaux de quelques paragraphes. "
        "On les appelle des chunks. Chaque morceau garde sa source : le nom du document et la page. "
        "Par exemple, un guide de deux cents pages peut devenir plusieurs centaines de passages.")),
    dict(kind='content', draw=s3, name='Étape deux : les embeddings', text=(
        "Deuxième étape : chaque passage est transformé en embedding. "
        "C'est une liste de nombres qui représente le sens du texte. "
        "Deux passages qui parlent de la même chose ont des embeddings proches, même avec des mots différents. "
        "« Résilier mon contrat » et « mettre fin à mon abonnement » se retrouvent côte à côte.")),
    dict(kind='content', draw=s4, name='Étape trois : retrouver et citer', text=(
        "Troisième étape : quand l'utilisateur pose une question, on la transforme elle aussi en embedding. "
        "La base vectorielle retrouve les passages les plus proches. "
        "On les envoie au modèle avec la question, et on lui demande de répondre uniquement à partir de ces passages, en citant ses sources.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, la qualité dépend d'abord des documents. "
        "Des sources obsolètes ou contradictoires donnent de mauvaises réponses, même avec un excellent modèle. "
        "Les citations, elles, permettent à l'utilisateur de vérifier, et à vous de comprendre une erreur.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles sources sont fiables, et qui les met à jour ? "
        "Qui a le droit de voir quel document ? "
        "Que doit répondre l'assistant quand rien de pertinent n'est trouvé ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le RAG, c'est découper, retrouver, puis répondre en citant. "
        "Le modèle ne sait que ce qu'on lui montre. "
        "Prochaine capsule : passer d'un chatbot qui parle à un agent qui agit.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
