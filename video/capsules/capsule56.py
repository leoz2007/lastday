from engine import *  # noqa
from engine import _paint  # noqa

NUM = 56
TITLE = 'MODÈLES ET INFÉRENCE'
FULL_TITLE = 'Modèles et inférence'
SLUG = 'modeles_inference'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'

FAMILIES = ['Qwen Coder', 'Devstral', 'GLM', 'DeepSeek', 'Kimi', 'gpt-oss']


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def s1(c, t, S):
    opening(c, t, S, CAP, 'Les classements ne *suffisent pas*.')
    cl = S.cue('classements publics')
    card(c, t, cl, 90, 830, 420, 400, WHITE, 36, 'up')
    if prog(t, cl, 0.5) > 0.4:
        small(c, 'Classement public', 130, 885, 20, DARK)
        for k, (h, col) in enumerate([(150, PL), (210, DARK), (110, PL)]):
            x = 150 + k * 110
            rrect(c, x, 1150 - h * ease(prog(t, cl + 0.2 + k * 0.1, 0.5)), 80, h * ease(prog(t, cl + 0.2 + k * 0.1, 0.5)), 12, col)
        icon(c, t, cl + 0.9, 'cross', 440, 900, 40, RED)
    ap = S.cue('appelle ses outils')
    card(c, t, ap, 550, 830, 440, 400, WHITE, 36, 'up')
    if prog(t, ap, 0.5) > 0.4:
        small(c, "Appels d'outils", 590, 885, 20, RED)
        for k in range(4):
            y = 940 + k * 70
            dot(c, t, ap + 0.2 + k * 0.15, 620, y + 20, 16, DARK)
            rrect(c, 650, y + 10, 220 * ease(prog(t, ap + 0.25 + k * 0.15, 0.4)) + 1, 20, 10, PL)
            icon(c, t, ap + 0.4 + k * 0.15, 'check', 920, y + 20, 34, RED)
    dz = S.cue('des dizaines de fois')
    if t >= dz:
        reveal_plain(c, t, dz, 'Sans erreur, des dizaines de fois', 540, 1320, 36, WHITE, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, "L'appel d'outils", 'Le *bon outil*, les *bons paramètres*')
    a = S.cue('demander une action')
    card(c, t, a, 90, 540, 900, 330, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, "Ce que le modèle demande · exemple", 140, 600, 20, DARK)
        lf = S.cue('lire un fichier')
        box(c, t, lf, 140, 640, 700, 90, 'lire_fichier( "src/paiement.py" )', WHITE, DARK, 30)
        icon(c, t, lf + 0.4, 'check', 900, 685, 44, RED)
        lt = S.cue('lancer les tests')
        box(c, t, lt, 140, 750, 700, 90, 'lancer_tests( "paiement" )', WHITE, DARK, 30)
        icon(c, t, lt + 0.4, 'check', 900, 795, 44, RED)
    tv = S.cue('vos propres tâches')
    chip(c, t, tv, 'Testez sur vos propres tâches', 90, 900, RED, WHITE, 32)
    f = S.cue('Les familles')
    card(c, t, f, 90, 1020, 900, 400, LIGHT, 36, 'up')
    if prog(t, f, 0.5) > 0.4:
        small(c, 'Familles à suivre · exemples à date', 140, 1080, 20, DARK)
        e = S.cue('chaque trimestre')
        items = []
        for k, s in enumerate(FAMILIES):
            at = e + 0.3 + k * 0.12
            items.append((s, at, RED if k == 0 else WHITE, WHITE if k == 0 else DARK))
        flow_chips(c, t, items, 140, 1115, 800, 32, 18)
        tr = S.cue('chaque trimestre')
        if t >= e:
            icon(c, t, e, 'clock', 160, 1360, 40, DARK)
            reveal_plain(c, t, e, 'Le paysage change chaque trimestre', 200, 1372, 28, DARK, 'Medium')
        _ = tr


def s3(c, t, S):
    header(c, t, S, "Serveur d'inférence", 'Faire *tourner* le modèle')
    sv = S.cue("serveur d'inférence")
    box(c, t, sv, 90, 540, 900, 110, 'Le logiciel qui répond aux requêtes', DARK, WHITE, 32)
    pr = S.cue('En production')
    card(c, t, pr, 90, 690, 520, 520, LIGHT, 36, 'up')
    if prog(t, pr, 0.5) > 0.4:
        label(c, t, pr + 0.1, 'Production', 130, 720, RED, WHITE, 22)
        icon(c, t, pr + 0.2, 'db', 350, 880, 90, DARK)
        for k in range(5):
            x = 170 + k * 90
            icon(c, t, pr + 0.4 + k * 0.08, 'user', x, 1020, 44, DARK)
            arrow(c, t, pr + 0.5 + k * 0.08, x, 990, 350 + (x - 350) * 0.3, 945, PL, 4, 12)
        v = S.cue('vLLM')
        x = 130
        for k, s in enumerate(['vLLM', 'SGLang']):
            w = chip(c, t, v + k * 0.2, s, x, 1090, WHITE, DARK, 28)
            x += w + 14
        if t >= v:
            small(c, 'Exemples à date', 130, 1180, 18, DARK)
    lo = S.cue('poste local')
    card(c, t, lo, 640, 690, 350, 520, LIGHT, 36, 'up')
    if prog(t, lo, 0.5) > 0.4:
        label(c, t, lo + 0.1, 'Poste local', 680, 720, PLL, DARK, 22)
        icon(c, t, lo + 0.2, 'code', 815, 880, 90, DARK)
        icon(c, t, lo + 0.3, 'user', 815, 1020, 44, DARK)
        ol = S.cue('Ollama')
        chip(c, t, ol, 'Ollama', 680, 1090, WHITE, DARK, 28)
        if t >= ol:
            small(c, 'Exemple à date', 680, 1180, 18, DARK)
    cu = S.cue("Restaurant d'un côté")
    if t >= cu:
        icon(c, t, cu, 'user', 130, 1320, 50, RED)
        reveal_plain(c, t, cu + 0.1, 'Restaurant contre cuisine familiale', 180, 1333, 32, DARK, 'Medium')


def s4(c, t, S):
    header(c, t, S, 'Dimensionner les GPU', 'Tout tient dans *la mémoire*')
    v = S.cue('la VRAM')
    card(c, t, v, 90, 540, 900, 420, LIGHT, 36, 'up')
    gr = S.cue('grossit vite')
    us = S.cue('utilisateurs simultanés')
    qz = S.cue('compresse le modèle')
    if prog(t, v, 0.5) > 0.4:
        small(c, "VRAM d'un GPU · illustratif", 140, 600, 20, DARK)
        x0, w0, y0, h0 = 140, 800, 640, 90
        outline(c, x0, y0, w0, h0, 20, DARK, 5)
        wp = lerp(0.42, 0.26, ease(prog(t, qz, 0.8))) * w0
        rrect(c, x0 + 8, y0 + 8, wp * ease(prog(t, v + 0.2, 0.6)), h0 - 16, 14, PL)
        kv = lerp(0.08, 0.38, ease(prog(t, gr, 1.2))) * w0
        if t >= gr - 1.5:
            rrect(c, x0 + 14 + wp, y0 + 8, kv, h0 - 16, 14, RED)
        if t >= v + 0.4:
            plain(c, 'Poids du modèle', 140, 790, 26, DARK)
        if t >= gr - 1.5:
            plain(c, 'KV cache : ce qui est déjà lu', 940, 790, 26, RED, 'Medium', 'right')
        if t >= us:
            for k in range(5):
                icon(c, t, us + k * 0.1, 'user', 170 + k * 70, 880, 40, DARK)
            small(c, 'Un cache par requête en cours', 940, 890, 18, DARK, align='right')
    rows = [('Mémoire', 'leur mémoire'), ('Contexte', 'taille du contexte'),
            ('Utilisateurs', 'utilisateurs simultanés'), ('Quantification', 'la quantification')]
    for k, (s, kw) in enumerate(rows):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        y = 1000 + (k // 2) * 200
        card(c, t, at, x, y, 440, 170, RED if k == 1 else LIGHT, 30, 'pop')
        if prog(t, at, 0.5) > 0.4:
            fg = WHITE if k == 1 else DARK
            plain(c, str(k + 1), x + 50, y + 100, 48, fg, 'Bold')
            plain(c, s, x + 110, y + 98, 34, fg, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Mesurer *délai* et *débit*')
    a = S.cue('premier token')
    card(c, t, a, 90, 540, 900, 380, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Un appel, dans le temps', 140, 600, 20, DARK)
        x0, y = 140, 690
        bar(c, t, a + 0.2, x0, y - 18, 240, 36, 1.0, PL, WHITE, 0.6)
        dot(c, t, a + 0.8, x0 + 266, y, 22, RED)
        tp = S.cue('tokens par seconde')
        for k in range(12):
            at = tp + k * 0.08
            if t >= at:
                h = 44 * ease(prog(t, at, 0.25))
                rrect(c, x0 + 310 + k * 42, y - h / 2, 14, max(2, h), 7, RED)
        if t >= a + 0.8:
            small(c, 'TTFT : délai avant le 1er token', 140, 770, 18, DARK)
        if t >= tp:
            small(c, 'Tokens par seconde, par utilisateur', 940, 820, 18, RED, align='right')
        dg = S.cue('débit global')
        if t >= dg:
            small(c, 'Débit global : tout le serveur', 140, 880, 18, DARK)
    ap = S.cue('centaines')
    card(c, t, ap, 90, 960, 900, 440, LIGHT, 36, 'up')
    if prog(t, ap, 0.5) > 0.4:
        small(c, 'Appels par tâche · ordre de grandeur', 140, 1020, 20, DARK)
        for k in range(60):
            x = 160 + (k % 15) * 54
            y = 1080 + (k // 15) * 54
            dot(c, t, ap + 0.2 + k * 0.025, x, y, 16, RED if k % 15 == 14 else PL)
        ms = S.cue('par tâche')
        if t >= ms:
            reveal_plain(c, t, ms, 'Chaque seconde se multiplie', 540, 1370, 34, RED, 'Medium', 'center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Le modèle réussit-il l'*appel d'outils* sur vos tâches ?", 'Le modèle réussit'),
        ('Combien d\'*utilisateurs simultanés*, quel contexte ?', 'Combien'),
        ('Quel *délai* avant le premier token est acceptable ?', 'Et quel délai'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Choisissez sur l'*appel d'outils*, pas sur les classements.", 'choisissez le modèle'),
        ('Dimensionnez la *mémoire*, mesurez délai et *débit*.', 'Dimensionnez'),
    ], "57 · Le harness, l'agent de code")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Pour un agent de code, le meilleur modèle n'est pas celui qui gagne les classements publics. "
        "C'est celui qui appelle ses outils sans se tromper, des dizaines de fois.")),
    dict(kind='content', draw=s2, name="L'appel d'outils et les familles de modèles", text=(
        "L'appel d'outils, en anglais tool calling, c'est la capacité du modèle à demander une action précise, "
        "avec les bons paramètres : lire un fichier, lancer les tests. Testez-le sur vos propres tâches. "
        "Les familles à suivre changent chaque trimestre : à date, par exemple Qwen Coder.")),
    dict(kind='content', draw=s3, name="Le serveur d'inférence", text=(
        "Le modèle a besoin d'un serveur d'inférence : le logiciel qui le fait tourner et répond aux requêtes. "
        "En production, partagé par des équipes, on prend par exemple vLLM, à date. "
        "Pour essayer sur un poste local, Ollama suffit. "
        "Restaurant d'un côté, cuisine familiale de l'autre.")),
    dict(kind='content', draw=s4, name='Dimensionner les GPU', text=(
        "Pour dimensionner les GPU, ces processeurs graphiques, regardez quatre facteurs. Leur mémoire, la VRAM. "
        "La taille du contexte : le KV cache, où le modèle garde ce qu'il a déjà lu, "
        "grossit vite quand l'agent accumule les fichiers. "
        "Le nombre d'utilisateurs simultanés. Et la quantification, qui compresse le modèle.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, suivez trois mesures. Le délai avant le premier token, le TTFT ; "
        "un token est un morceau de mot. Les tokens par seconde par utilisateur. "
        "Et le débit global du serveur. Car un agent fait souvent des dizaines, voire des centaines "
        "d'appels par tâche, en ordre de grandeur : chaque seconde se multiplie.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Le modèle réussit-il l'appel d'outils sur vos propres tâches ? "
        "Combien d'utilisateurs simultanés, avec quelle taille de contexte ? "
        "Et quel délai avant le premier token est acceptable ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : choisissez le modèle sur l'appel d'outils, pas sur les classements. "
        "Dimensionnez les GPU selon la mémoire, le contexte et les utilisateurs, "
        "puis mesurez délai et débit. "
        "Prochaine capsule : le harness, l'agent de code.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
