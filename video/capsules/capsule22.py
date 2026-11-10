from engine import *  # noqa
from engine import _paint  # noqa

NUM = 22
TITLE = 'OBSERVABILITÉ'
FULL_TITLE = 'Observabilité et traces'
SLUG = 'observabilite_traces'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def spark(c, t, at, x, y, w, h, vals, color, width=6, dur=1.2):
    """Courbe tracée progressivement dans le cadre (x, y, w, h). vals entre 0 et 1."""
    p = ease(prog(t, at, dur))
    if p <= 0:
        return []
    n = len(vals) - 1
    pts = [(x + w * i / n, y + h * (1 - v)) for i, v in enumerate(vals)]
    seg = p * n
    for i in range(n):
        if seg <= i:
            break
        f = min(1.0, seg - i)
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        c.drawLine(x1, y1, lerp(x1, x2, f), lerp(y1, y2, f), _paint(color, width))
    return pts


def s1(c, t, S):
    opening(c, t, S, CAP, "Sans traces, une erreur d'IA reste *un mystère*.")
    a = S.cue('se trompe')
    card(c, t, a, 90, 840, 430, 300, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 305, 940, 80, DARK)
        reveal_plain(c, t, a + 0.2, 'Réponse fausse', 305, 1070, 36, DARK, 'Medium', 'center')
        icon(c, t, a + 0.4, 'cross', 470, 890, 40, RED)
    v = S.cue("qu'a-t-il vu")
    card(c, t, v, 560, 840, 430, 300, RED, 36, 'up')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'eye', 775, 940, 80, WHITE)
        reveal_plain(c, t, v + 0.2, "Qu'a-t-il vu ?", 775, 1070, 36, WHITE, 'Medium', 'center')
    h = S.cue('au hasard')
    x = 90
    for k, s in enumerate(['Le prompt ?', 'Le document ?', 'Le modèle ?']):
        w = chip(c, t, h + k * 0.2, s, x, 1220, WHITE, DARK, 30)
        x += w + 20


def s2(c, t, S):
    header(c, t, S, 'La trace', "Tout ce qu'a vu *chaque appel*")
    a = S.cue("l'enregistrement")
    card(c, t, a, 90, 540, 900, 720, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        label(c, t, a + 0.1, 'Trace · exemple illustratif', 140, 570, PLL, DARK, 22)
    rows = [('chat', 'Prompt', '« Résume ce dossier »', 'le prompt'),
            ('doc', 'Contexte', '3 documents fournis', 'le contexte fourni'),
            ('chat', 'Réponse', 'Résumé en 5 lignes', 'la réponse'),
            ('gear', 'Outils', 'recherche_documents', 'les outils appelés'),
            ('clock', 'Durée', '2,4 s', 'la durée'),
            ('coin', 'Coût', '0,01 €', 'le coût')]
    for k, (ic, key, val, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 670 + k * 95
        icon(c, t, at, ic, 165, y, 44, RED)
        if t >= at:
            small(c, key, 215, y + 9, 22, DARK)
        reveal_plain(c, t, at + 0.15, val, 450, y + 12, 32, DARK)
    b = S.cue('boîte noire')
    chip(c, t, b, "La boîte noire de l'assistant", 90, 1300, RED, WHITE, 34)


def s3(c, t, S):
    header(c, t, S, 'Comprendre une erreur', 'Trouver la *vraie cause*')
    q = S.cue('réponse fausse')
    steps = [('Question du client', q, True), ('Recherche de documents', S.cue("n'était pas dans le contexte"), False),
             ('Appel au modèle', S.cue('pas le modèle'), True), ('Réponse fausse', q, False)]
    o = S.cue('On ouvre la trace')
    if t >= o:
        c.drawLine(130, 610, 130, 610 + (1080 - 610) * ease(prog(t, o, 1.0)), _paint(PL, 6))
    for k, (s, at, ok) in enumerate(steps):
        y = 560 + k * 150
        st = o + k * 0.2
        dot(c, t, st, 130, y + 60, 22, DARK)
        bad = (not ok) and t >= at
        card(c, t, st, 190, y, 800, 120, RED if (k == 1 and bad) else LIGHT, 30, 'left')
        if prog(t, st, 0.5) > 0.4:
            fg = WHITE if (k == 1 and bad) else DARK
            plain(c, s, 240, y + 72, 34, fg)
            if k == 1 and bad:
                icon(c, t, at, 'cross', 920, y + 60, 44, WHITE)
            elif k != 1 and t >= at + 0.2:
                if ok:
                    icon(c, t, at + 0.2, 'check', 920, y + 60, 44, RED)
                else:
                    icon(c, t, at + 0.2, 'cross', 920, y + 60, 44, RED)
    if t >= o:
        small(c, 'Délai de rétractation', 190, 545, 20, DARK)
    pr = S.cue('pour rien')
    card(c, t, pr, 90, 1180, 900, 230, DARK, 32, 'up')
    if prog(t, pr, 0.5) > 0.4:
        icon(c, t, pr + 0.1, 'target', 190, 1295, 70, RED)
        text_block(c, t, pr + 0.2, 'Corriger la *recherche*, pas le prompt', 270, 1280, 38, 'Medium',
                   WHITE, RED, maxw=680, max_lines=2)


def s4(c, t, S):
    header(c, t, S, 'Tableaux de bord', 'Quatre *courbes* à suivre')
    a = S.cue('tableaux de bord')
    series = [('Qualité', 'la qualité', [0.6, 0.65, 0.62, 0.7, 0.72, 0.7, 0.75], DARK),
              ('Coût', 'le coût', [0.25, 0.28, 0.26, 0.85, 0.3, 0.27, 0.29], RED),
              ('Latence', 'la latence', [0.4, 0.45, 0.42, 0.5, 0.44, 0.41, 0.43], DARK),
              ("Taux d'échec", "taux d'échec", [0.2, 0.18, 0.22, 0.2, 0.15, 0.17, 0.14], DARK)]
    md = S.cue('double un mardi')
    for k, (nm, kw, vals, col) in enumerate(series):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        y = 540 + (k // 2) * 330
        card(c, t, min(at, a + 0.3 + k * 0.15), x, y, 440, 300, LIGHT, 30, 'pop')
        if t >= min(at, a + 0.3 + k * 0.15) + 0.2:
            small(c, nm, x + 30, y + 50, 22, DARK)
            pts = spark(c, t, at, x + 40, y + 90, 360, 170, vals, col)
            if k == 1 and t >= md and pts:
                px, py = pts[3]
                dot(c, t, md, px, py, 18, RED)
                chip(c, t, md + 0.2, 'Mardi', px + 30, py - 10, RED, WHITE, 24)
    if t >= a + 0.5:
        small(c, 'Courbes illustratives', 90, 1225, 20, DARK)
    ap = S.cue('les appels en cause')
    card(c, t, ap, 90, 1260, 900, 150, LIGHT, 32, 'up')
    if prog(t, ap, 0.5) > 0.4:
        icon(c, t, ap + 0.1, 'search', 170, 1335, 56, RED)
        reveal_plain(c, t, ap + 0.2, 'Du pic à la trace en cause', 240, 1350, 36, DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Des traces *sensibles*')
    dp = S.cue('données personnelles')
    an = S.cue('anonymisez')
    card(c, t, dp, 90, 540, 900, 340, LIGHT, 32, 'up')
    if prog(t, dp, 0.5) > 0.4:
        label(c, t, dp + 0.1, 'Extrait de trace', 140, 570, PLL, DARK, 22)
        rows = [('Nom', 'Camille Martin', '[NOM]', 'noms'), ('Adresse', '12 rue des Lilas', '[ADRESSE]', 'adresses'),
                ('Contrat', 'n° 48213', '[CONTRAT]', 'numéros de contrat')]
        for k, (key, val, mask, kw) in enumerate(rows):
            at = S.cue(kw)
            y = 680 + k * 70
            if t >= at:
                small(c, key, 140, y + 10, 22, DARK)
            if t < an + k * 0.2:
                reveal_plain(c, t, at, val, 400, y + 12, 32, RED)
            else:
                chip(c, t, an + k * 0.2, mask, 400, y - 22, PL, DARK, 26)
    items = [('lock', 'Accès limité', 'limitez qui'), ('clock', 'Durée de conservation', 'durée de conservation')]
    for k, (ic, s, kw) in enumerate(items):
        at = S.cue(kw)
        x = 90 + k * 460
        card(c, t, at, x, 930, 440, 270, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 220, 1020, 70, RED)
            text_block(c, t, at + 0.2, s, x + 220, 1130, 32, 'Medium', DARK, RED, maxw=380,
                       align='center', max_lines=2)
    nb = S.cue("n'a pas besoin")
    card(c, t, nb, 90, 1260, 900, 140, RED, 32, 'up')
    if prog(t, nb, 0.5) > 0.4:
        icon(c, t, nb + 0.1, 'shield', 170, 1330, 56, WHITE)
        reveal_plain(c, t, nb + 0.2, "Utile, sans nom", 240, 1345, 38, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Que doit-on *enregistrer* à chaque appel ?', 'Que doit-on'),
        ('Qui a le droit de *lire* les traces ?', 'Qui a le droit'),
        ('Combien de *temps* les garde-t-on ?', 'Et combien'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Tracez *chaque appel* : comprendre plutôt que deviner.', 'tracez'),
        ('Protégez les traces comme des *données sensibles*.', 'Et protégez'),
    ], '23 · Retours utilisateurs')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Quand un assistant se trompe, la première question est simple : qu'a-t-il vu, exactement ? "
        "Sans traces, impossible de répondre. On devine, et on corrige au hasard.")),
    dict(kind='content', draw=s2, name='La trace', text=(
        "Une trace, c'est l'enregistrement de chaque appel au modèle. "
        "On y garde le prompt, le contexte fourni, la réponse, les outils appelés, la durée et le coût. "
        "C'est la boîte noire de votre assistant, un peu comme dans un avion.")),
    dict(kind='content', draw=s3, name='Comprendre une erreur', text=(
        "Prenons une réponse fausse sur un délai de rétractation. On ouvre la trace. "
        "Le bon document n'était pas dans le contexte : c'est la recherche qui a échoué, pas le modèle. "
        "Sans trace, on aurait réécrit le prompt pour rien.")),
    dict(kind='content', draw=s4, name='Les tableaux de bord', text=(
        "En regroupant les traces, on construit des tableaux de bord. "
        "Quatre courbes à suivre : la qualité, le coût, la latence et le taux d'échec. "
        "Si le coût double un mardi, vous voyez quand, et vous retrouvez les appels en cause.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, attention : les traces contiennent souvent des données personnelles, "
        "comme des noms, des adresses, des numéros de contrat. "
        "Masquez ou anonymisez-les avant de les stocker, limitez qui peut les lire, "
        "et fixez une durée de conservation. Une trace utile n'a pas besoin d'un nom.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Que doit-on enregistrer à chaque appel ? "
        "Qui a le droit de lire les traces ? "
        "Et combien de temps les garde-t-on ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : tracez chaque appel, pour comprendre au lieu de deviner. "
        "Et protégez ces traces comme des données sensibles. "
        "Prochaine capsule : les retours utilisateurs, pour savoir ce que vos utilisateurs pensent vraiment.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
