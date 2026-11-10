from engine import *  # noqa
from engine import _paint  # noqa

NUM = 32
TITLE = 'RAG AVANCÉ'
FULL_TITLE = 'Le RAG avancé'
SLUG = 'rag_avance'
NEXT_CUE = 'prochaine capsule'
SERIES = (29, 38)
SERIES_LABEL = 'Saison 3'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Le RAG plafonne ? Regardez la *recherche*.')
    rows = [('En démonstration', 'en démonstration', 0.85, WHITE), ('En production', 'plafonne', 0.5, PL)]
    for k, (nm, kw, f, col) in enumerate(rows):
        at = S.cue(kw)
        y = 860 + k * 120
        if t >= at - 0.2:
            small(c, nm, 90, y, 24, WHITE)
        bar(c, t, at, 90, y + 22, 900, 34, f, col, DARK, 0.8)
    steps = ['Question', 'Recherche', 'Modèle', 'Réponse']
    b = S.cue('cherche des documents')
    rc = S.cue('la recherche')
    for k, s in enumerate(steps):
        x = 90 + k * 235
        hot = k == 1 and t >= rc
        box(c, t, b + k * 0.15, x, 1170, 195, 120, s, RED if hot else WHITE, WHITE if hot else DARK, 28)
        if k < 3:
            arrow(c, t, b + k * 0.15 + 0.1, x + 199, 1230, x + 231, 1230, WHITE, 5, 12)
    nr = S.cue("n'y est pour rien")
    icon(c, t, nr, 'check', 90 + 2 * 235 + 97, 1370, 50, WHITE)
    mp = S.cue('mauvais passages')
    icon(c, t, mp, 'cross', 90 + 235 + 97, 1370, 50, RED)


def s2(c, t, S):
    header(c, t, S, 'Le RAG naïf', 'Trois causes *fréquentes*')
    # 1. découpage
    a = S.cue('Le découpage')
    card(c, t, a, 90, 540, 900, 270, LIGHT, 32, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, '1 · Découpage maladroit', 140, 600, 20, DARK)
        for j, w in enumerate([520, 480, 540, 460]):
            y = 640 + j * 40
            rrect(c, 140, y, w, 20, 10, PL)
        cut = S.cue('en deux')
        if t >= cut:
            p = ease(prog(t, cut, 0.4))
            rrect(c, 120, 699, 600 * p, 6, 3, RED)
            reveal_plain(c, t, cut + 0.2, 'Règle coupée', 940, 715, 30, RED, 'Medium', 'right')
    # 2. question floue
    q = S.cue('mal formulée')
    card(c, t, q, 90, 840, 900, 270, LIGHT, 32, 'up')
    if prog(t, q, 0.5) > 0.4:
        small(c, '2 · Question floue', 140, 900, 20, DARK)
        pr = S.cue('pour les pros')
        chip(c, t, pr, '« Et pour les pros ? »', 140, 950, WHITE, DARK, 34)
        sc = S.cue('sans contexte')
        icon(c, t, sc, 'search', 720, 980, 56, DARK)
        icon(c, t, sc + 0.3, 'cross', 820, 980, 50, RED)
        if t >= sc + 0.3:
            small(c, 'Rien de pertinent', 140, 1075, 20, RED)
    # 3. proche mais inutile
    p = S.cue('proches du sujet')
    card(c, t, p, 90, 1140, 900, 290, LIGHT, 32, 'up')
    if prog(t, p, 0.5) > 0.4:
        small(c, '3 · Proche, mais inutile', 140, 1200, 20, DARK)
        dl = S.cue('délais de résiliation')
        box(c, t, dl, 140, 1240, 330, 120, 'Délais de résiliation ?', WHITE, DARK, 28)
        ob = S.cue("conditions d'abonnement")
        arrow(c, t, ob, 480, 1300, 540, 1300, DARK, 5, 16)
        box(c, t, ob + 0.2, 555, 1240, 330, 120, "Conditions d'abonnement", PL, DARK, 28)
        icon(c, t, ob + 0.5, 'cross', 920, 1300, 40, RED)


def s3(c, t, S):
    header(c, t, S, 'Recherche hybride', 'Mots clés, *sens*, puis *tri*')
    k = S.cue('Les mots clés')
    card(c, t, k, 90, 540, 440, 260, LIGHT, 32, 'up')
    if prog(t, k, 0.5) > 0.4:
        small(c, 'Mots clés', 130, 600, 20, DARK)
        nc = S.cue('numéro de contrat')
        chip(c, t, nc, 'CTR-4182', 130, 640, WHITE, DARK, 32)
        icon(c, t, nc + 0.3, 'check', 450, 668, 44, RED)
        if t >= nc:
            small(c, 'Référence exacte', 130, 760, 18, DARK)
    v = S.cue('Les vecteurs')
    card(c, t, v, 550, 540, 440, 260, LIGHT, 32, 'up')
    if prog(t, v, 0.5) > 0.4:
        small(c, 'Vecteurs · le sens', 590, 600, 20, DARK)
        ar = S.cue('arrêter mon abonnement')
        chip(c, t, ar, '« Arrêter »', 590, 640, WHITE, DARK, 28)
        rs = S.cue('à « résiliation »')
        chip(c, t, rs, '« Résilier »', 590, 715, WHITE, DARK, 28)
        if t >= rs:
            plain(c, '=', 870, 715, 56, RED, 'Medium', 'center')
            small(c, 'Même sens', 950, 600, 18, RED, align='right')
    cb = S.cue('On combine')
    box(c, t, cb, 90, 830, 900, 100, 'Recherche hybride', RED, WHITE, 34)
    rr = S.cue('le reranking')
    card(c, t, rr, 90, 960, 900, 470, LIGHT, 36, 'up')
    if prog(t, rr, 0.5) > 0.4:
        small(c, 'Reranking · un second modèle reclasse', 140, 1020, 20, DARK)
        names = ['Passage A', 'Passage B', 'Passage C', 'Passage D', 'Passage E']
        new = [2, 3, 0, 4, 1]  # nouveau rang de chaque passage
        re_ = S.cue('les reclasse')
        u = ease(prog(t, re_, 0.8))
        kp = S.cue('les plus pertinents')
        for j, nm in enumerate(names):
            at = rr + 0.2 + j * 0.1
            if t < at:
                continue
            y = lerp(1050 + j * 70, 1050 + new[j] * 70, u)
            top = new[j] < 2 and t >= kp
            rrect(c, 140, y, 600, 54, 27, RED if top else (PLL if t >= kp else PL))
            plain(c, nm, 175, y + 38, 28, WHITE if top else DARK)
        if t >= kp:
            reveal_plain(c, t, kp + 0.2, 'Gardés', 940, 1130, 30, RED, 'Medium', 'right')


def s4(c, t, S):
    header(c, t, S, 'Question et découpage', 'Réécrire, *découper*, filtrer')
    r = S.cue('réécrire la question')
    card(c, t, r, 90, 540, 900, 330, LIGHT, 36, 'up')
    if prog(t, r, 0.5) > 0.4:
        small(c, 'Décomposer la question', 140, 600, 20, DARK)
        cq = S.cue('comparez les offres')
        box(c, t, cq, 140, 640, 360, 190, '« Comparez les offres A et B »', WHITE, DARK, 30)
        dr = S.cue('deux recherches')
        arrow(c, t, dr, 510, 700, 580, 680, DARK, 5, 16)
        arrow(c, t, dr, 510, 770, 580, 790, DARK, 5, 16)
        box(c, t, dr + 0.2, 595, 640, 345, 80, 'Recherche : offre A', RED, WHITE, 28)
        box(c, t, dr + 0.35, 595, 750, 345, 80, 'Recherche : offre B', RED, WHITE, 28)
    d = S.cue('par section')
    card(c, t, d, 90, 910, 900, 520, LIGHT, 36, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Un morceau par section', 140, 970, 20, DARK)
        rrect(c, 140, 1000, 520, 56, 28, DARK)
        plain(c, 'Section : Résiliation', 170, 1039, 28, WHITE)
        for j, w in enumerate([500, 460, 480]):
            rrect(c, 140, 1080 + j * 36, w, 18, 9, PL)
        x = 140
        for s, kw in [('Date', 'la date'), ('Produit', 'le produit'), ('Droits', "droits d'accès")]:
            x += chip(c, t, S.cue(kw), s, x, 1200, PLL, DARK, 28) + 14
        f = S.cue('On filtre')
        if t >= f:
            small(c, 'Filtre', 720, 1030, 20, DARK)
        keep = [True, False, True, False]
        vg = S.cue('en vigueur')
        for j, ok in enumerate(keep):
            cx, cy = 760 + (j % 2) * 120, 1110 + (j // 2) * 130
            col = DARK if t < vg else (RED if ok else PL)
            icon(c, t, f + 0.1 + j * 0.1, 'doc', cx, cy, 70, col)
        dv = S.cue('droit de voir')
        if t >= dv:
            reveal_plain(c, t, dv, 'En vigueur et autorisés', 140, 1340, 30, RED, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Mesurer la recherche *à part*')
    cols = [('Recherche', 'Bons passages en tête ?', "D'abord", 0.55, RED),
            ('Réponse', 'Réponse juste ?', 'Ensuite seulement', 0.8, PL)]
    for k, (nm, q, kw, f, col) in enumerate(cols):
        at = S.cue(kw)
        x = 90 + k * 460
        card(c, t, at, x, 540, 440, 380, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, f'{k + 1} · {nm}', x + 40, 600, 22, RED if k == 0 else DARK)
            icon(c, t, at + 0.1, 'search' if k == 0 else 'chat', x + 220, 700, 80, DARK)
            text_block(c, t, at + 0.2, q, x + 40, 810, 30, 'Medium', DARK, RED, maxw=360, max_lines=2)
            bar(c, t, at + 0.4, x + 40, 870, 360, 26, f, col, WHITE, 0.6)
    if t >= S.cue("D'abord") + 0.6:
        small(c, 'Scores illustratifs', 90, 970, 20, DARK)
    rp = S.cue('vous retouchez le prompt')
    card(c, t, rp, 90, 1010, 900, 180, LIGHT, 32, 'left')
    if prog(t, rp, 0.5) > 0.4:
        icon(c, t, rp + 0.1, 'cross', 170, 1100, 54, DARK)
        reveal_plain(c, t, rp + 0.2, 'Retoucher le prompt', 240, 1112, 36, DARK)
    pb = S.cue('vient de la recherche')
    card(c, t, pb, 90, 1230, 900, 180, RED, 32, 'left')
    if prog(t, pb, 0.5) > 0.4:
        icon(c, t, pb + 0.1, 'check', 170, 1320, 54, WHITE)
        reveal_plain(c, t, pb + 0.2, 'Corriger la recherche', 240, 1332, 36, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Cherche-t-on des *références exactes*, du *sens*, ou les deux ?', 'Vos utilisateurs'),
        ('Quelles *métadonnées*, notamment pour les droits ?', 'Quelles métadonnées'),
        ('Comment mesure-t-on la *recherche* seule ?', 'Et comment'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Un bon RAG, c'est d'abord une bonne *recherche*.", 'un bon RAG'),
        ('Hybride, reclassée, filtrée, et *mesurée à part*.', 'Hybride'),
    ], '33 · Transformers et attention')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un RAG, qui cherche des documents avant de répondre, brille en démonstration, puis plafonne en production. "
        "Souvent, le modèle n'y est pour rien : c'est la recherche qui lui donne les mauvais passages.")),
    dict(kind='content', draw=s2, name='Pourquoi un RAG naïf plafonne', text=(
        "Trois causes reviennent souvent. Le découpage coupe une règle en deux. "
        "La question est mal formulée, comme « et pour les pros ? », sans contexte. "
        "Ou des passages proches du sujet, mais inutiles, prennent la place des bons : "
        "on demande les délais de résiliation, on obtient les conditions d'abonnement.")),
    dict(kind='content', draw=s3, name='Recherche hybride et reranking', text=(
        "Première réponse : la recherche hybride. Les mots clés retrouvent les références exactes, comme un numéro de contrat. "
        "Les vecteurs, qui comparent le sens, relient « arrêter mon abonnement » à « résiliation ». On combine les deux. "
        "Puis le reranking : un second modèle relit les meilleurs candidats, les reclasse, "
        "et garde les plus pertinents.")),
    dict(kind='content', draw=s4, name='Réécrire la question, mieux découper', text=(
        "Deuxième réponse : réécrire la question, ou la décomposer. « Comparez les offres A et B » devient deux recherches. "
        "Troisième : découper par section, avec titres et métadonnées, comme la date, le produit ou les droits d'accès. "
        "On filtre alors les documents en vigueur, que l'utilisateur a le droit de voir.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, mesurez la recherche séparément de la réponse. "
        "D'abord : les bons passages sont-ils dans les premiers résultats ? Ensuite seulement : la réponse est-elle juste ? "
        "Sinon, vous retouchez le prompt alors que le problème vient de la recherche.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Vos utilisateurs cherchent-ils des références exactes, du sens, ou les deux ? "
        "Quelles métadonnées faut-il, notamment pour les droits d'accès ? "
        "Et comment mesure-t-on la recherche seule ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un bon RAG, c'est d'abord une bonne recherche. "
        "Hybride, reclassée, filtrée, et mesurée à part de la réponse. "
        "Prochaine capsule : les transformers et l'attention, au cœur des modèles.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
