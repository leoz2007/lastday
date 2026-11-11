from engine import *  # noqa
from engine import _paint  # noqa

NUM = 42
TITLE = 'EMBEDDINGS'
FULL_TITLE = 'Les embeddings au-delà du RAG'
SLUG = 'embeddings_au_dela_rag'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'

# trois grappes de points (dx, dy) autour de centres
CLUSTER = [(-60, -30), (-20, 40), (30, -50), (50, 20), (-40, 10), (10, 0), (60, -10)]


def s1(c, t, S):
    opening(c, t, S, CAP, 'Les embeddings ne servent *pas qu\'au* RAG.')
    a = S.t0 + 0.6
    centers = [(250, 1000), (720, 960), (480, 1250)]
    for g, (cx, cy) in enumerate(centers):
        for k, (dx, dy) in enumerate(CLUSTER):
            dot(c, t, a + g * 0.2 + k * 0.04, cx + dx * 1.2, cy + dy * 1.2, 14, PL)
    words = [('Classer', 'classer', 0), ('Regrouper', 'regrouper', 1), ('Doublons', 'doublons', 2)]
    for s, kw, g in words:
        at = S.cue(kw)
        cx, cy = centers[g]
        for k, (dx, dy) in enumerate(CLUSTER):
            dot(c, t, at + k * 0.03, cx + dx * 1.2, cy + dy * 1.2, 14, WHITE if g != 1 else RED)
        chip(c, t, at + 0.2, s, cx, cy + 100, WHITE, DARK, 28, align='center')
    mc = S.cue('bien moins cher')
    if t >= mc:
        icon(c, t, mc, 'coin', 860, 1350, 50, RED)
        reveal_plain(c, t, mc + 0.1, 'Souvent moins cher', 810, 1362, 28, WHITE, 'Medium', 'right')


def s2(c, t, S):
    header(c, t, S, 'Rappel', 'Une liste de nombres *pour le sens*')
    ln = S.cue('une liste de nombres')
    card(c, t, ln, 90, 540, 900, 230, LIGHT, 32, 'up')
    if prog(t, ln, 0.5) > 0.4:
        chip(c, t, ln + 0.1, '« Colis pas arrivé »', 130, 580, WHITE, DARK, 28)
        arrow(c, t, ln + 0.4, 480, 610, 540, 610, DARK, 5, 14)
        chip(c, t, ln + 0.6, '0,12  -0,48  0,91  ...', 555, 580, PLL, DARK, 28)
        small(c, 'Valeurs illustratives', 130, 720, 18, DARK)
    pl = S.cue('des listes proches')
    card(c, t, pl, 90, 800, 900, 630, LIGHT, 32, 'up')
    if prog(t, pl, 0.5) > 0.4:
        small(c, 'Proches par le sens', 140, 860, 20, DARK)
        # axes
        rrect(c, 140, 1380, 800, 4, 2, PL)
        rrect(c, 140, 890, 4, 494, 2, PL)
        cl = S.cue("« Mon colis n'est pas arrivé »")
        dot(c, t, cl, 360, 1060, 22, RED)
        chip(c, t, cl + 0.2, 'Colis pas arrivé', 400, 980, WHITE, DARK, 26)
        lv = S.cue('« livraison jamais reçue »')
        dot(c, t, lv, 420, 1130, 22, RED)
        chip(c, t, lv + 0.2, 'Livraison jamais reçue', 460, 1110, WHITE, DARK, 26)
        cc = S.cue('côte à côte')
        dot(c, t, cc, 820, 1300, 22, DARK)
        if t >= cc + 0.2:
            small(c, 'Facture erronée', 800, 1350, 18, DARK, align='right')
        mm = S.cue('sans mot commun')
        if t >= mm:
            reveal_plain(c, t, mm, 'Aucun mot commun', 180, 1330, 28, RED, 'Medium')


def s3(c, t, S):
    header(c, t, S, 'Classer et regrouper', 'Par *proximité*')
    cl = S.cue('classer')
    card(c, t, cl, 90, 540, 900, 400, LIGHT, 32, 'up')
    if prog(t, cl, 0.5) > 0.4:
        small(c, '1 · Classer avec des exemples', 140, 600, 20, DARK)
        ex = S.cue('déjà étiquetés')
        a_pts = [(220, 720), (260, 780), (200, 820), (300, 740)]
        b_pts = [(620, 700), (680, 760), (640, 820), (720, 720)]
        for k, (x, y) in enumerate(a_pts):
            dot(c, t, ex + k * 0.05, x, y, 16, RED)
        for k, (x, y) in enumerate(b_pts):
            dot(c, t, ex + 0.2 + k * 0.05, x, y, 16, DARK)
        if t >= ex + 0.3:
            small(c, 'Livraison', 250, 890, 18, RED, align='center')
            small(c, 'Facture', 670, 890, 18, DARK, align='center')
        nt = S.cue('Un nouveau ticket')
        dot(c, t, nt, 420, 760, 18, PL)
        pr = S.cue("l'étiquette des plus proches")
        arrow(c, t, pr, 400, 760, 320, 750, RED, 4, 12)
        if t >= pr + 0.4:
            dot(c, t, pr + 0.4, 420, 760, 18, RED)
            reveal_plain(c, t, pr + 0.4, 'Livraison', 940, 770, 32, RED, 'Medium', 'right')
    rg = S.cue('regrouper')
    card(c, t, rg, 90, 970, 900, 460, LIGHT, 32, 'up')
    if prog(t, rg, 0.5) > 0.4:
        small(c, '2 · Regrouper en thèmes', 140, 1030, 20, DARK)
        centers = [(250, 1190), (530, 1150), (800, 1210)]
        for g, (cx, cy) in enumerate(centers):
            for k, (dx, dy) in enumerate(CLUSTER):
                dot(c, t, rg + 0.3 + g * 0.1 + k * 0.03, cx + dx * 0.9, cy + dy * 0.9, 12, PL)
        th = S.cue('révèle un thème')
        names = [('Retards', 'les retards'), ('Plantages', "l'application qui plante"), ('Prix', None)]
        for g, (nm, kw) in enumerate(names):
            at = S.cue(kw) if kw else th + 0.2
            if kw is None and t < at:
                continue
            cx, cy = centers[g]
            chip(c, t, at, nm, cx, cy + 90, RED if g < 2 else WHITE, WHITE if g < 2 else DARK, 26,
                 align='center')
        cs = S.cue('clustering')
        if t >= cs:
            small(c, 'Clustering', 940, 1030, 20, RED, align='right')


def s4(c, t, S):
    header(c, t, S, 'Trois autres usages', 'Doublons, *voisins*, intrus')
    db = S.cue('les doublons')
    card(c, t, db, 90, 540, 900, 270, LIGHT, 32, 'up')
    if prog(t, db, 0.5) > 0.4:
        small(c, '3 · Doublons', 140, 600, 20, DARK)
        fi = S.cue('fiches produit')
        box(c, t, fi, 140, 640, 300, 120, 'Chaise chêne clair', WHITE, DARK, 28)
        box(c, t, fi + 0.2, 470, 640, 300, 120, 'Chaise en chêne, clair', WHITE, DARK, 28)
        sg = S.cue('on les signale')
        if t >= sg:
            chip(c, t, sg, 'Doublon ?', 800, 670, RED, WHITE, 28)
    rc = S.cue('recommander')
    card(c, t, rc, 90, 840, 900, 270, LIGHT, 32, 'up')
    if prog(t, rc, 0.5) > 0.4:
        small(c, '4 · Recommander', 140, 900, 20, DARK)
        lu = S.cue('a lu')
        icon(c, t, lu, 'doc', 200, 1010, 70, RED)
        small(c, 'Lu', 200, 1080, 18, RED, align='center')
        for k in range(3):
            arrow(c, t, lu + 0.2 + k * 0.1, 250, 1010, 380 + k * 170, 1010, PL if k else DARK, 4, 12)
            icon(c, t, lu + 0.4 + k * 0.1, 'doc', 420 + k * 170, 1010, 60, DARK)
        if t >= lu + 0.6:
            small(c, 'Contenus proches', 590, 1080, 18, DARK, align='center')
    ih = S.cue("l'inhabituel")
    card(c, t, ih, 90, 1140, 900, 290, LIGHT, 32, 'up')
    if prog(t, ih, 0.5) > 0.4:
        small(c, "5 · Repérer l'inhabituel", 140, 1200, 20, DARK)
        for k, (dx, dy) in enumerate(CLUSTER):
            dot(c, t, ih + 0.2 + k * 0.03, 330 + dx, 1310 + dy * 0.8, 12, PL)
        lt = S.cue('loin de tout')
        dot(c, t, lt, 720, 1270, 18, RED)
        arrow(c, t, lt + 0.2, 420, 1320, 690, 1280, RED, 4, 12)
        fr = S.cue('une fraude')
        if t >= fr:
            reveal_plain(c, t, fr, 'Fraude ? Nouveau problème ?', 940, 1390, 28, RED, 'Medium', 'right')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Pas cher, mais *à valider*')
    mc = S.cue('bien moins cher')
    card(c, t, mc, 90, 540, 900, 380, LIGHT, 32, 'up')
    if prog(t, mc, 0.5) > 0.4:
        small(c, 'Coût pour traiter un gros volume (illustratif)', 140, 600, 20, DARK)
        rows = [('Un appel au modèle par élément', 0.92, PL, mc + 0.2),
                ('Embeddings, puis comparaison', 0.15, RED, S.cue('une fois'))]
        for k, (s, f, col, at) in enumerate(rows):
            y = 650 + k * 120
            if t >= at - 0.25:
                small(c, s, 140, y + 20, 20, DARK)
            bar(c, t, at, 140, y + 40, 800, 36, f, col, WHITE, 0.8)
    sm = S.cue('votre sens métier')
    card(c, t, sm, 90, 950, 900, 480, LIGHT, 32, 'up')
    if prog(t, sm, 0.5) > 0.4:
        small(c, '« Proche » pour le modèle', 140, 1010, 20, DARK)
        rs = S.cue('« Résilier »')
        box(c, t, rs, 140, 1050, 340, 120, 'Résilier', WHITE, DARK, 34)
        ab = S.cue("« s'abonner »")
        box(c, t, ab, 600, 1050, 340, 120, "S'abonner", WHITE, DARK, 34)
        ps = S.cue('sembler proches')
        if t >= ps:
            plain(c, '=', 540, 1130, 60, DARK, 'Medium', 'center')
        op = S.cue('opposée')
        if t >= op:
            icon(c, t, op, 'cross', 540, 1110, 60, RED)
            reveal_plain(c, t, op + 0.1, 'Intentions opposées', 540, 1290, 34, RED, 'Medium', 'center')
        mm = S.cue('même sujet')
        if t >= mm:
            small(c, 'Même sujet', 540, 1380, 20, DARK, align='center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Sur quels *exemples étiquetés* valide-t-on la proximité ?', 'Sur quels'),
        ('Quel *seuil* pour un doublon, ou pour l\'inhabituel ?', 'Quel seuil'),
        ('Qui *relit* les cas proches du seuil ?', 'Et qui relit'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un embedding mesure une *proximité de sens*, à faible coût.', 'un embedding mesure'),
        ('Validez sur *vos exemples*, choisissez vos *seuils*.', 'Validez-la'),
    ], '43 · Extraction en masse')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Les embeddings ne servent pas qu'à chercher des documents pour un RAG. "
        "Ils savent aussi classer, regrouper, repérer des doublons, "
        "souvent pour bien moins cher qu'un appel à un modèle de langage.")),
    dict(kind='content', draw=s2, name='Rappel : un embedding', text=(
        "Petit rappel. Un embedding est une liste de nombres qui représente le sens d'un texte. "
        "Deux textes au sens proche obtiennent des listes proches. "
        "« Mon colis n'est pas arrivé » et « livraison jamais reçue » se retrouvent côte à côte, "
        "sans mot commun.")),
    dict(kind='content', draw=s3, name='Classer et regrouper', text=(
        "Premier usage : classer. Un nouveau ticket est comparé à des exemples déjà étiquetés, "
        "et prend l'étiquette des plus proches. Deuxième usage : regrouper. "
        "Des centaines de retours clients forment des grappes, c'est le clustering : "
        "chaque grappe révèle un thème, comme les retards ou l'application qui plante.")),
    dict(kind='content', draw=s4, name='Doublons, recommandation, inhabituel', text=(
        "Troisième usage : les doublons. Deux fiches produit presque identiques sont très proches : on les signale. "
        "Quatrième : recommander des contenus proches de ce qu'un utilisateur a lu. "
        "Cinquième : repérer l'inhabituel, un message loin de tout ce qu'on voit d'ordinaire, "
        "comme une fraude ou un nouveau problème.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, c'est souvent bien moins cher qu'un appel au modèle pour chaque élément : "
        "on calcule l'embedding une fois, puis on compare. "
        "Mais « proche » n'est pas toujours votre sens métier. "
        "« Résilier » et « s'abonner » parlent du même sujet, et peuvent sembler proches, "
        "alors que l'intention est opposée.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Sur quels exemples étiquetés valide-t-on la proximité ? "
        "Quel seuil décide qu'on parle de doublon, ou d'inhabituel ? "
        "Et qui relit les cas proches du seuil ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un embedding mesure une proximité de sens, vite et à faible coût. "
        "Validez-la sur vos exemples, et choisissez vos seuils avant de lui faire confiance. "
        "Prochaine capsule : l'extraction en masse, pour traiter des milliers de documents.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
