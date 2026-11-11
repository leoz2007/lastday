from engine import *  # noqa
from engine import _paint  # noqa

NUM = 52
TITLE = 'CONTRATS FOURNISSEUR'
FULL_TITLE = 'Contrats avec un fournisseur de LLM'
SLUG = 'contrats_fournisseur'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Choisir un modèle, c\'est *signer un contrat*.')
    m = S.cue('le meilleur modèle')
    card(c, t, m, 90, 860, 380, 420, WHITE, 40, 'pop')
    if prog(t, m, 0.5) > 0.4:
        icon(c, t, m + 0.1, 'brain', 280, 1010, 110, DARK)
        plain(c, 'Le modèle', 280, 1180, 32, DARK, 'Medium', 'center')
    sg = S.cue('signer un contrat')
    arrow(c, t, sg, 490, 1070, 580, 1070, WHITE, 6, 18)
    card(c, t, sg + 0.2, 600, 860, 390, 420, RED, 40, 'pop')
    if prog(t, sg + 0.2, 0.5) > 0.4:
        small(c, 'Contrat', 640, 920, 22, WHITE)
        for j, w in enumerate([300, 260, 310, 220]):
            rrect(c, 640, 960 + j * 50, w * min(1, prog(t, sg + 0.3 + j * 0.08, 0.4)), 22, 11, WHITE)
        eng = S.cue('engage votre produit')
        if t >= eng:
            p = ease(prog(t, eng, 0.6))
            c.drawLine(640, 1200, 640 + 200 * p, 1200, _paint(WHITE, 4))
            small(c, 'Signature', 640, 1240, 18, WHITE)
    lg = S.cue('pour longtemps')
    if t >= lg:
        reveal_plain(c, t, lg, 'Un engagement dans la durée', 540, 1380, 34, WHITE, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, 'Bloc 1 · Vos données', 'Où vont *vos données* ?')
    rows = [('brain', 'Entraînement ?', 'entraîner les modèles'),
            ('clock', 'Durée de conservation', 'combien de temps'),
            ('target', 'Pays de stockage', 'dans quel pays'),
            ('user', 'Sous-traitants', 'sous-traitants')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 550 + k * 130
        card(c, t, at, 90, y, 900, 110, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 165, y + 55, 48, DARK)
            reveal_plain(c, t, at + 0.15, s, 230, y + 67, 34, DARK, 'Medium')
            icon(c, t, at + 0.3, 'search', 920, y + 55, 40, RED)
    rg = S.cue('le RGPD')
    card(c, t, rg, 90, 1100, 900, 300, RED, 36, 'up')
    if prog(t, rg, 0.5) > 0.4:
        icon(c, t, rg + 0.1, 'shield', 180, 1200, 64, WHITE)
        reveal_plain(c, t, rg + 0.2, 'Données personnelles : RGPD', 250, 1215, 36, WHITE, 'Medium')
        dp = S.cue('votre DPO')
        if t >= dp:
            chip(c, t, dp, 'DPO', 140, 1280, WHITE, RED, 30)
            reveal_plain(c, t, dp + 0.3, 'Délégué à la protection des données', 270, 1322, 28, WHITE, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Bloc 2 · Le service', 'Sécurité et *disponibilité*')
    for k, (ic, s, kw) in enumerate([('lock', 'Confidentialité', 'la confidentialité'),
                                     ('shield', 'Sécurité', 'la sécurité')]):
        at = S.cue(kw)
        x = 90 + k * 460
        card(c, t, at, x, 540, 440, 160, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 80, 620, 56, DARK)
            reveal_plain(c, t, at + 0.15, s, x + 140, 632, 34, DARK, 'Medium')
    d = S.cue('si le service tombe')
    card(c, t, d, 90, 740, 900, 400, LIGHT, 36, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Disponibilité du service · illustratif', 140, 800, 20, DARK)
        for k in range(14):
            x = 160 + k * 58
            bad = k in (8, 9)
            col = RED if bad else PL
            rrect(c, x - 20, 860, 40, 120 * min(1, prog(t, d + 0.2 + k * 0.05, 0.3)), 12, col)
        if t >= d + 0.9:
            small(c, 'Panne', 160 + 8.5 * 58, 1020, 20, RED, align='center')
        sl = S.cue('souvent appelés SLA')
        if t >= sl:
            chip(c, t, sl, 'SLA', 140, 1050, DARK, WHITE, 30)
            reveal_plain(c, t, sl + 0.3, 'Engagements de niveau de service', 270, 1092, 30, DARK, 'Medium')
    a = S.cue('assistant client')
    card(c, t, a, 90, 1180, 900, 220, RED, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 180, 1290, 64, WHITE)
        text_block(c, t, a + 0.2, 'Votre assistant client en dépend', 250, 1305, 38, 'Medium', WHITE, WHITE,
                   maxw=700, max_lines=1)


def s4(c, t, S):
    header(c, t, S, 'Bloc 3 · Dans la durée', 'Changer *sans tout réécrire*')
    m = S.cue('les anciens sont retirés')
    card(c, t, m, 90, 540, 900, 260, LIGHT, 36, 'up')
    if prog(t, m, 0.5) > 0.4:
        small(c, 'Modèles', 140, 600, 20, DARK)
        rrect(c, 140, 690, 800, 6, 3, PL)
        for k, s in enumerate(['V1', 'V2', 'V3']):
            x = 200 + k * 300
            old = k == 0
            dot(c, t, m + 0.1 + k * 0.15, x, 693, 34, PL if old else (RED if k == 2 else DARK))
            plain(c, s, x, 703, 26, DARK if old else WHITE, 'Medium', 'center') if t >= m + 0.3 + k * 0.15 else None
        icon(c, t, m + 0.6, 'cross', 200, 760, 36, RED)
        pv = S.cue('quel préavis')
        if t >= pv:
            reveal_plain(c, t, pv, 'Préavis ?', 940, 770, 30, RED, 'Medium', 'right')
    pq = S.cue('Les prix et les quotas')
    card(c, t, pq, 90, 830, 900, 200, LIGHT, 36, 'up')
    if prog(t, pq, 0.5) > 0.4:
        icon(c, t, pq + 0.1, 'coin', 170, 930, 56, DARK)
        reveal_plain(c, t, pq + 0.2, 'Prix et quotas', 240, 915, 34, DARK, 'Medium')
        vl = S.cue('volumes autorisés')
        if t >= vl:
            reveal_plain(c, t, vl, 'Quotas = volumes autorisés', 240, 975, 26, DARK, 'Medium')
        bar(c, t, pq + 0.4, 680, 905, 260, 30, 0.7, RED, WHITE, 0.8)
    r = S.cue('la réversibilité')
    card(c, t, r, 90, 1060, 900, 240, LIGHT, 36, 'up')
    if prog(t, r, 0.5) > 0.4:
        small(c, 'Réversibilité', 140, 1120, 20, DARK)
        box(c, t, r + 0.1, 140, 1150, 240, 110, 'Fournisseur A', WHITE, DARK, 28)
        cf = S.cue('changer de fournisseur')
        arrow(c, t, cf, 400, 1205, 680, 1205, RED, 6, 18)
        box(c, t, cf + 0.3, 700, 1150, 240, 110, 'Fournisseur B', RED, WHITE, 28)
    rs = S.cue('qui est responsable')
    if t >= rs:
        icon(c, t, rs, 'user', 150, 1365, 40, RED)
        reveal_plain(c, t, rs + 0.1, 'Et qui est responsable en cas de problème ?', 200, 1377, 30, DARK, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Chacun *son rôle*')
    roles = [('shield', 'Juridique', 'Le juridique', RED, WHITE),
             ('coin', 'Achats', 'les achats', RED, WHITE),
             ('user', 'Vous, la PO', 'Vous, vous apportez', LIGHT, DARK)]
    for k, (ic, s, kw, fill, fg) in enumerate(roles):
        at = S.cue(kw)
        x = 90 + k * 305
        card(c, t, at, x, 550, 290, 260, fill, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 145, 640, 64, fg)
            plain(c, s, x + 145, 760, 30, fg, 'Medium', 'center')
    tr = S.cue('tranchent')
    if t >= tr:
        reveal_plain(c, t, tr, 'Négocient et tranchent', 395, 860, 28, RED, 'Medium', 'center')
    rows = [('Volumes', 'volumes'), ('Données sensibles', 'données sensibles'),
            ('Disponibilité attendue', 'disponibilité attendue')]
    yb = 900
    x = 90
    for s, kw in rows:
        x += chip(c, t, S.cue(kw), s, x, yb, PLL, DARK, 28) + 14
    co = S.cue('une couche')
    card(c, t, co, 90, 1020, 900, 380, LIGHT, 36, 'up')
    if prog(t, co, 0.5) > 0.4:
        small(c, 'Architecture', 140, 1080, 20, DARK)
        box(c, t, co + 0.1, 140, 1110, 230, 110, 'Votre produit', DARK, WHITE, 28)
        arrow(c, t, co + 0.2, 380, 1165, 430, 1165, DARK, 5, 16)
        box(c, t, co + 0.3, 440, 1110, 230, 110, 'Couche d\'accès', RED, WHITE, 28)
        arrow(c, t, co + 0.4, 680, 1150, 730, 1130, DARK, 5, 16)
        arrow(c, t, co + 0.4, 680, 1180, 730, 1260, DARK, 5, 16)
        box(c, t, co + 0.5, 740, 1090, 200, 80, 'Fourn. A', WHITE, DARK, 26)
        box(c, t, co + 0.6, 740, 1220, 200, 80, 'Fourn. B', WHITE, DARK, 26)
        ch = S.cue('pouvoir en changer')
        if t >= ch:
            reveal_plain(c, t, ch, 'Changer sans tout réécrire', 140, 1360, 30, RED, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles *données* confiez-vous, et le *DPO* est-il impliqué ?', 'Quelles données'),
        ('Et si un modèle est *retiré*, ou si les *prix* changent ?', 'Que se passe-t-il'),
        ('Comment *sortir* sans tout réécrire ?', 'Et comment sortir'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Vos *données*, son *service*, et votre *liberté d\'en sortir*.', "c'est vos données"),
        ('Le juridique et les achats *tranchent*, vous apportez les *besoins*.', 'Le juridique et les achats'),
    ], '53 · Gouvernance de l\'IA')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Choisir un fournisseur de LLM, un grand modèle de langage, ce n'est pas seulement choisir le meilleur modèle. "
        "C'est signer un contrat, et ce contrat engage votre produit pour longtemps.")),
    dict(kind='content', draw=s2, name='Vos données', text=(
        "Premier bloc : vos données. Servent-elles à entraîner les modèles du fournisseur ? "
        "Combien de temps sont-elles conservées, et dans quel pays ? Quels sous-traitants y ont accès ? "
        "Dès qu'il y a des données personnelles, le RGPD s'applique : impliquez votre DPO, "
        "le délégué à la protection des données.")),
    dict(kind='content', draw=s3, name='Sécurité et engagements de service', text=(
        "Deuxième bloc : la confidentialité, la sécurité et la disponibilité. "
        "Que garantit le fournisseur si le service tombe ? Ces engagements de service, souvent appelés SLA, "
        "fixent par exemple un niveau de disponibilité et des délais d'intervention. "
        "Votre assistant client en dépend directement.")),
    dict(kind='content', draw=s4, name='Évolution, prix et réversibilité', text=(
        "Troisième bloc : la durée. Les modèles évoluent, et les anciens sont retirés : avec quel préavis ? "
        "Les prix et les quotas, c'est-à-dire les volumes autorisés, peuvent bouger aussi. "
        "Puis la réversibilité : pouvez-vous changer de fournisseur sans tout réécrire ? "
        "Et qui est responsable en cas de problème ?")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, chacun son rôle. Le juridique et les achats négocient et tranchent. "
        "Vous, vous apportez les besoins : volumes, données sensibles, disponibilité attendue. "
        "Et prévoyez une couche qui isole le fournisseur, pour pouvoir en changer.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles données confiez-vous au fournisseur, et le DPO est-il impliqué ? "
        "Que se passe-t-il si un modèle est retiré, ou si les prix changent ? "
        "Et comment sortir sans tout réécrire ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un contrat avec un fournisseur, c'est vos données, son service, et votre liberté d'en sortir. "
        "Le juridique et les achats tranchent, vous apportez les besoins. "
        "Prochaine capsule : la gouvernance de l'IA en entreprise.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
