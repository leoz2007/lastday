import math

from engine import *  # noqa
from engine import _paint  # noqa

NUM = 40
TITLE = 'AGENTS VOCAUX'
FULL_TITLE = 'Agents vocaux'
SLUG = 'agents_vocaux'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def wave(c, t, at, x, y, w, h, color, seed=0, n=None, cut=None):
    """Onde sonore stylisée : barres verticales centrées sur y, qui apparaissent de gauche à droite.
    cut = instant où l'onde s'interrompt (barres suivantes non dessinées)."""
    n = n or max(4, int(w / 22))
    step = w / n
    for k in range(n):
        a = at + k * 0.03
        if t < a:
            break
        if cut is not None and t >= cut and k >= n // 2:
            break
        p = ease(prog(t, a, 0.3))
        amp = 0.25 + 0.75 * abs(math.sin(k * 1.3 + seed) * math.cos(k * 0.45 + seed * 2))
        hh = max(10, h * amp * p)
        rrect(c, x + k * step, y - hh / 2, step * 0.55, hh, step * 0.27, color)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Au téléphone, chaque *silence* compte.')
    a = S.t0 + 0.6
    small(c, 'Appelant', 90, 860, 22, WHITE)
    wave(c, t, a, 90, 920, 360, 90, WHITE, 1)
    tr = S.cue('répond trop tard')
    small(c, 'Agent', 90, 1030, 22, WHITE)
    if t >= tr:
        p = ease(prog(t, tr, 1.0))
        rrect(c, 470, 895, 300 * p, 6, 3, RED)
        icon(c, t, tr + 0.3, 'clock', 620, 990, 56, RED)
    wave(c, t, tr + 1.0, 790, 1090, 200, 90, PL, 2)
    cs = S.cue('chaque silence')
    if t >= cs:
        reveal_plain(c, t, cs, 'Le silence se remarque', 620, 1180, 30, RED, 'Medium', 'center')
    ep = S.cue('qui écoute et qui parle')
    card(c, t, ep, 90, 1250, 900, 170, WHITE, 32, 'up')
    if prog(t, ep, 0.5) > 0.4:
        icon(c, t, ep + 0.1, 'user', 180, 1330, 56, DARK)
        reveal_plain(c, t, ep + 0.2, 'Écouter, puis parler', 250, 1350, 38, DARK, 'Medium')
        wave(c, t, ep + 0.3, 760, 1335, 180, 70, RED, 3)


def s2(c, t, S):
    header(c, t, S, 'La chaîne classique', 'Trois *maillons*')
    a = S.cue('trois maillons')
    card(c, t, a, 90, 540, 900, 380, LIGHT, 32, 'up')
    steps = [('Transcrire', 'Voix en texte', 'La reconnaissance vocale'),
             ('Modèle', 'Texte de réponse', 'Le modèle lit'),
             ('Synthèse', 'Texte en voix', 'la synthèse vocale')]
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Chaîne classique', 140, 600, 20, DARK)
        for k, (nm, sub, kw) in enumerate(steps):
            at = S.cue(kw)
            x = 130 + k * 295
            box(c, t, at, x, 650, 230, 130, nm, RED if k == 1 else WHITE, WHITE if k == 1 else DARK, 32)
            if t >= at + 0.3:
                small(c, sub, x + 115, 840, 18, DARK, align='center')
            if k < 2:
                arrow(c, t, S.cue(steps[k + 1][2]), x + 238, 715, x + 287, 715, DARK, 5, 14)
    d = S.cue("directement l'audio")
    card(c, t, d, 90, 960, 900, 360, LIGHT, 32, 'up')
    if prog(t, d, 0.5) > 0.4:
        small(c, 'Certains modèles', 140, 1020, 20, DARK)
        wave(c, t, d + 0.1, 140, 1145, 200, 100, DARK, 1)
        arrow(c, t, d + 0.4, 355, 1145, 405, 1145, DARK, 5, 14)
        box(c, t, d + 0.5, 420, 1075, 240, 140, 'Modèle audio', RED, WHITE, 30)
        arrow(c, t, d + 0.7, 675, 1145, 725, 1145, DARK, 5, 14)
        wave(c, t, d + 0.8, 740, 1145, 200, 100, RED, 4)
        st = S.cue('sans passer par le texte')
        if t >= st:
            reveal_plain(c, t, st, 'Sans passer par le texte', 540, 1280, 28, RED, 'Medium', 'center')


def s3(c, t, S):
    header(c, t, S, 'Latence', 'Répondre *à temps*, se taire *à temps*')
    la = S.cue('La latence')
    card(c, t, la, 90, 540, 900, 400, LIGHT, 32, 'up')
    if prog(t, la, 0.5) > 0.4:
        small(c, 'Le délai avant la réponse', 140, 600, 20, DARK)
        small(c, 'Appelant', 140, 660, 18, DARK)
        wave(c, t, la + 0.2, 140, 710, 300, 70, DARK, 1)
        small(c, 'Agent', 140, 800, 18, DARK)
        rl = S.cue('trop longue')
        g = ease(prog(t, la + 0.6, 0.8))
        gx = 460
        gw = lerp(60, 320, ease(prog(t, rl, 0.8))) if t >= rl else 60
        if g > 0:
            rrect(c, gx, 755, gw * g, 8, 4, RED if t >= rl else PL)
        wave(c, t, la + 1.2, gx + gw + 20, 850, 940 - gx - gw - 20, 70, PL, 2)
        rp = S.cue('répète ou raccroche')
        if t >= rp:
            icon(c, t, rp, 'cross', 900, 710, 44, RED)
            reveal_plain(c, t, rp + 0.1, 'Il répète, ou raccroche', 140, 905, 28, RED, 'Medium')
    tp = S.cue('tours de parole')
    card(c, t, tp, 90, 970, 900, 450, LIGHT, 32, 'up')
    if prog(t, tp, 0.5) > 0.4:
        small(c, 'Tours de parole', 140, 1030, 20, DARK)
        it = S.cue("s'il interrompt")
        small(c, 'Agent', 140, 1090, 18, DARK)
        wave(c, t, tp + 0.2, 140, 1140, 760, 70, PL, 2, cut=it + 0.4)
        small(c, 'Appelant', 140, 1230, 18, DARK)
        if t >= it:
            wave(c, t, it, 480, 1280, 420, 70, DARK, 5)
            arrow(c, t, it + 0.3, 470, 1250, 470, 1170, RED, 5, 14)
        cd = S.cue('corriger une date')
        if t >= cd:
            reveal_plain(c, t, cd, "L'agent s'arrête net", 140, 1380, 30, RED, 'Medium')


def s4(c, t, S):
    header(c, t, S, 'Transcription', 'Mal *entendu*, mal compris')
    items = [('Noms propres', 'Les noms propres'), ('Chiffres', 'les chiffres'),
             ('Accents', 'les accents'), ('Bruit', "le bruit d'une voiture")]
    for k, (s, kw) in enumerate(items):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        y = 560 + (k // 2) * 130
        box(c, t, at, x, y, 440, 100, s, LIGHT, DARK, 32)
    tm = S.cue('« Treize mai »')
    card(c, t, tm, 90, 850, 900, 330, LIGHT, 32, 'up')
    if prog(t, tm, 0.5) > 0.4:
        small(c, "Ce que l'appelant dit, ce qui est transcrit", 140, 910, 20, DARK)
        wave(c, t, tm + 0.1, 140, 1000, 160, 70, DARK, 1)
        box(c, t, tm + 0.2, 320, 950, 260, 100, 'Treize mai', WHITE, DARK, 34)
        sz = S.cue('« seize mai »')
        arrow(c, t, sz, 590, 1000, 650, 1000, DARK, 5, 14)
        box(c, t, sz + 0.2, 665, 950, 260, 100, 'Seize mai', RED, WHITE, 34)
        cj = S.cue('change de jour')
        if t >= cj:
            icon(c, t, cj, 'clock', 360, 1120, 40, RED)
            reveal_plain(c, t, cj + 0.1, 'Rendez-vous déplacé', 400, 1132, 28, RED, 'Medium')
    tf = S.cue('un texte faux')
    card(c, t, tf, 90, 1210, 900, 200, RED, 32, 'up')
    if prog(t, tf, 0.5) > 0.4:
        icon(c, t, tf + 0.1, 'brain', 180, 1310, 64, WHITE)
        text_block(c, t, tf + 0.2, 'Le modèle raisonne sur un texte faux', 250, 1300, 34, 'Medium',
                   WHITE, WHITE, maxw=700, max_lines=2)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'La voix, *là où elle aide*')
    uses = [('gear', 'Mains occupées', 'les mains'), ('chat', 'Téléphone', 'au téléphone'),
            ('user', 'Accessibilité', "l'accessibilité")]
    for k, (ic, s, kw) in enumerate(uses):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 540, 280, 220, LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 615, 60, RED)
            plain(c, s, x + 140, 715, 28, DARK, 'Medium', 'center')
    rf = S.cue('reformulation')
    card(c, t, rf, 90, 800, 900, 330, LIGHT, 32, 'up')
    if prog(t, rf, 0.5) > 0.4:
        small(c, 'Reformuler pour confirmer', 140, 860, 20, DARK)
        mr = S.cue('le mardi seize')
        icon(c, t, mr, 'chat', 180, 960, 56, DARK)
        text_block(c, t, mr, '« Vous voulez donc *mardi seize, à dix heures* ? »', 250, 950, 32,
                   'Medium', DARK, RED, maxw=680, max_lines=2)
        ou = S.cue('« Oui.')
        if t >= ou:
            chip(c, t, ou, 'Oui', 250, 1040, RED, WHITE, 30)
    hu = S.cue('vers un humain')
    card(c, t, hu, 90, 1160, 900, 230, LIGHT, 32, 'up')
    if prog(t, hu, 0.5) > 0.4:
        icon(c, t, hu + 0.1, 'bolt', 180, 1275, 56, DARK)
        arrow(c, t, hu + 0.3, 240, 1275, 700, 1275, RED, 6, 18)
        reveal_plain(c, t, hu + 0.3, 'Transfert', 470, 1250, 28, RED, 'Medium', 'center')
        dot(c, t, hu + 0.6, 800, 1275, 70, RED)
        icon(c, t, hu + 0.7, 'user', 800, 1270, 60, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Comment l'appelant est-il *informé*, et donne-t-il son *accord* ?", 'Comment'),
        ('Enregistre-t-on les appels ? Que deviennent ces *données* ?', 'Enregistre-t-on'),
        ('Quel *délai de réponse* paraîtra naturel ?', 'Et quel délai'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('En vocal, la *vitesse* compte autant que la justesse.', 'en vocal'),
        ('*Confirmez* ce qui a été compris, prévoyez un *humain*.', 'Confirmez'),
    ], '41 · Context engineering')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Au téléphone, un assistant peut tout savoir, et pourtant échouer : il répond trop tard. "
        "Dans une conversation, chaque silence se remarque. "
        "Un agent vocal, c'est un assistant qui écoute et qui parle.")),
    dict(kind='content', draw=s2, name='La chaîne classique', text=(
        "La chaîne classique compte trois maillons. La reconnaissance vocale transcrit la parole en texte. "
        "Le modèle lit ce texte et rédige la réponse. Puis la synthèse vocale la lit à voix haute. "
        "Certains modèles, eux, traitent directement l'audio, sans passer par le texte.")),
    dict(kind='content', draw=s3, name='Latence et tours de parole', text=(
        "La latence, c'est le délai avant la réponse. En conversation, elle est critique : "
        "trop longue, l'appelant répète ou raccroche. "
        "Il faut aussi gérer les tours de parole : savoir quand l'autre a fini, "
        "et s'arrêter net s'il interrompt, par exemple pour corriger une date.")),
    dict(kind='content', draw=s4, name='Les erreurs de transcription', text=(
        "Autre fragilité : la transcription. Les noms propres, les chiffres, les accents, "
        "le bruit d'une voiture : tout peut être mal entendu. "
        "« Treize mai » devient « seize mai », et le rendez-vous change de jour. "
        "Le modèle raisonne ensuite sur un texte faux, sans le savoir.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, misez sur la voix quand les mains sont occupées, au téléphone, "
        "ou pour l'accessibilité. Prévoyez une reformulation pour confirmer : "
        "« Vous voulez donc le mardi seize, à dix heures ? » « Oui. » "
        "Et un transfert vers un humain quand ça coince.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Comment l'appelant est-il informé qu'il parle à une machine, "
        "et donne-t-il son accord ? Enregistre-t-on les appels, et que deviennent ces données personnelles ? "
        "Et quel délai de réponse vos appelants trouveront-ils naturel ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : en vocal, la vitesse compte autant que la justesse. "
        "Confirmez ce que vous avez compris, et prévoyez toujours une sortie vers un humain. "
        "Prochaine capsule : le context engineering, l'art de choisir ce que le modèle voit.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
