from engine import *  # noqa
from engine import _paint  # noqa

NUM = 3
TITLE = 'PROMPTING'
FULL_TITLE = 'Prompting et system prompt'
SLUG = 'prompting_system_prompt'
NEXT_CUE = 'prochaine capsule'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un prompt est une *spécification*.')
    q = S.cue('question posée')
    chip(c, t, q, 'Résume ce mail', 90, 760, PLL, DARK, 38)
    sp = S.cue('spécification')
    card(c, t, sp, 90, 900, 900, 500, LIGHT, 36, 'up')
    if prog(t, sp, 0.5) > 0.4:
        label(c, t, sp + 0.2, 'Spec fonctionnelle', 140, 950, PLL, DARK, 22)
        for k, fr in enumerate([0.8, 0.6, 0.9, 0.5]):
            bar(c, t, sp + 0.4 + k * 0.2, 140, 1050 + k * 70, 660, 28, fr, PL, WHITE, 0.6)
    rl = S.cue('se relit')
    icon(c, t, rl, 'check', 880, 1100, 90, WHITE, bg=RED)


def s2(c, t, S):
    header(c, t, S, 'Deux niveaux', 'System prompt et *message*')
    a = S.cue('system prompt')
    card(c, t, a, 90, 560, 900, 330, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        label(c, t, a + 0.1, 'System prompt', 140, 600, RED, WHITE, 22)
        reveal_plain(c, t, S.cue("l'équipe produit"), "Écrit par l'équipe produit", 140, 720, 36, DARK)
        x = 140
        for s, kw in [('Rôle', 'le rôle'), ('Ton', 'le ton'), ('Règles', 'les règles')]:
            w = chip(c, t, S.cue(kw), s, x, 770, PLL, DARK, 34)
            x += w + 16
    tc = S.cue('toutes les conversations')
    arrow(c, t, tc, 540, 900, 540, 960, DARK, 6)
    m = S.cue('message utilisateur')
    for k in range(3):
        box(c, t, m + k * 0.35, 90 + k * 310, 980, 280, 110, f'Message {k + 1}', WHITE, DARK, 32, 'Medium', 28, 'up')
        if t >= m + k * 0.35:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90 + k * 310, 980, 370 + k * 310, 1090), 28, 28),
                        _paint(DARK, 3))
    ex = S.cue('Par exemple')
    card(c, t, ex, 90, 1160, 900, 270, WHITE, 32, 'up')
    if prog(t, ex, 0.5) > 0.5:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, 1160, 990, 1430), 32, 32), _paint(RED, 5))
        text_block(c, t, S.cue('Tu es'), "« Tu es l'assistant du service client. Tu réponds en *trois phrases* maximum. »",
                   140, 1240, 38, 'Medium', DARK, RED, maxw=800, max_lines=4)


def s3(c, t, S):
    header(c, t, S, 'Anatomie', 'Comme une *user story*')
    rows = [('Contexte', 'Un contexte', 'Client particulier, assurance habitation'),
            ('Tâche', 'tâche précise', 'Résumer la réclamation'),
            ('Contraintes', 'Des contraintes', 'Cinq lignes au plus, ton neutre'),
            ('Format', 'format de sortie', 'Motif, urgence, action proposée')]
    y = 540
    for name, kw, ex in rows:
        at = S.cue(kw)
        card(c, t, at, 90, y, 900, 165, LIGHT, 32, 'left')
        if prog(t, at, 0.5) > 0.4:
            label(c, t, at + 0.1, name, 130, y + 28, RED, WHITE, 22)
            reveal_plain(c, t, at + 0.3, ex, 130, y + 128, 34, DARK)
        y += 190
    su = S.cue('suppositions')
    chip(c, t, su, 'Sinon : des suppositions', 90, 1320, DARK, WHITE, 36)
    icon(c, t, su + 0.3, 'cross', 650, 1351, 60, RED)


def s4(c, t, S):
    header(c, t, S, 'Exemples et cas limites', "Montrer plutôt qu'*expliquer*")
    a = S.cue('réponses modèles')
    for k in range(3):
        x = 90 + k * 160
        card(c, t, a + k * 0.2, x, 580, 140, 220, LIGHT, 24, 'up')
        if t >= a + k * 0.2 + 0.2:
            for j, fr in enumerate([0.9, 0.6, 0.75]):
                bar(c, t, a + k * 0.2 + 0.2, x + 20, 620 + j * 50, 100, 18, fr, PL, WHITE, 0.4)
    if t >= a:
        small(c, 'Exemples', 90, 850, 22, DARK)
    st = S.cue('le style')
    arrow(c, t, st, 590, 690, 690, 690, DARK, 6)
    card(c, t, st + 0.2, 720, 560, 270, 260, WHITE, 28, 'pop')
    if t >= st + 0.3:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(720, 560, 990, 820), 28, 28), _paint(RED, 5))
        for j, fr in enumerate([0.9, 0.6, 0.75]):
            bar(c, t, st + 0.4, 750, 610 + j * 60, 210, 22, fr, RED, PLL, 0.5)
        small(c, 'Même structure', 720, 850, 22, RED)
    cl = S.cue('cas limites')
    label(c, t, cl, 'Cas limite', 90, 960, PLL, DARK)
    hp = S.cue('périmètre')
    box(c, t, hp, 90, 1050, 900, 120, 'Question *hors périmètre*', LIGHT, DARK, 36, 'Medium', 30, 'left')
    arrow(c, t, hp + 0.5, 540, 1180, 540, 1240, DARK, 6)
    box(c, t, hp + 0.8, 90, 1260, 900, 120, '« Je transmets à un conseiller. »', WHITE, DARK, 36, 'Medium', 30, 'left')
    if t >= hp + 1.1:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, 1260, 990, 1380), 30, 30), _paint(RED, 4))
    im = S.cue('improvisera')
    if t >= im:
        reveal_plain(c, t, im, "Non écrit = improvisé", 90, 1450, 32, RED, 'Medium')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Le system prompt est un *livrable*')
    a = S.cue('se versionne')
    x = 90
    for k, v in enumerate(['v1', 'v2', 'v3']):
        box(c, t, a + k * 0.25, x + k * 310, 600, 280, 140, v, LIGHT if k < 2 else RED,
            DARK if k < 2 else WHITE, 44, 'Light', 30)
        if k < 2:
            arrow(c, t, a + k * 0.25 + 0.2, x + k * 310 + 285, 670, x + k * 310 + 305, 670, DARK, 5, 14)
    for k, (s, kw) in enumerate([('Relu', 'se relit'), ('Testé', 'se teste')]):
        at = S.cue(kw)
        card(c, t, at, 90 + k * 460, 790, 440, 120, LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, 'check', 160 + k * 460, 850, 60, RED)
            reveal_plain(c, t, at + 0.1, s, 220 + k * 460, 863, 38, DARK)
    ph = S.cue('Une phrase modifiée')
    card(c, t, ph, 90, 970, 900, 440, LIGHT, 36, 'up')
    if prog(t, ph, 0.5) > 0.4:
        small(c, 'Une phrase modifiée', 140, 1040, 22, DARK)
        for j in range(5):
            bar(c, t, ph + 0.2, 140, 1070 + j * 40, 800, 20, 1.0 if j != 2 else 0.7,
                RED if j == 2 else PLL, PLL, 0.3)
        tt = S.cue("tout l'assistant")
        small(c, "Impact sur tout l'assistant", 140, 1330, 22, DARK)
        bar(c, t, tt, 140, 1350, 800, 30, 1.0, RED, PLL, 0.8)
    rc = S.cue('une recette')
    icon(c, t, rc, 'check', 940, 1030, 70, WHITE, bg=RED)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Qui *rédige et valide* le system prompt ?', 'Qui rédige'),
        ('Quels sujets sont *interdits*, et que répond-on alors ?', 'Quels sont les sujets'),
        ('Comment *teste*-t-on une nouvelle version avant de la déployer ?', 'Comment teste'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le prompt est une *spec* : contexte, tâche, contraintes, format, exemples.', 'le prompt est'),
        ('Le system prompt se gère comme un *livrable*.', 'se gère'),
    ], '04 · RAG et embeddings')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un prompt n'est pas une question posée à une machine. "
        "C'est une spécification fonctionnelle. Et comme toute spec, elle se relit, se discute et se valide.")),
    dict(kind='content', draw=s2, name='System prompt et message utilisateur', text=(
        "Il y a deux niveaux. Le system prompt, écrit par l'équipe produit, fixe le rôle, le ton et les règles, "
        "pour toutes les conversations. Le message utilisateur, lui, change à chaque échange. "
        "Par exemple : « Tu es l'assistant du service client. Tu réponds en trois phrases maximum. »")),
    dict(kind='content', draw=s3, name="L'anatomie d'un bon prompt", text=(
        "Un bon prompt ressemble à une user story bien écrite. "
        "Un contexte : qui est l'utilisateur, quel est le métier. Une tâche précise, avec un seul objectif. "
        "Des contraintes : la longueur, le ton, ce qu'il ne faut jamais faire. "
        "Et le format de sortie attendu. Sans ces éléments, le modèle comble les trous avec des suppositions.")),
    dict(kind='content', draw=s4, name='Exemples et cas limites', text=(
        "Le levier le plus efficace, c'est souvent l'exemple. "
        "Montrez au modèle deux ou trois réponses modèles : il en reprend le style et la structure. "
        "Pensez aussi aux cas limites. Que répondre si la question sort du périmètre ? "
        "Si vous ne l'écrivez pas, le modèle improvisera.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, le system prompt devient un livrable. Il a un responsable, il se versionne, se relit et se teste, comme du code. "
        "Une phrase modifiée peut changer le comportement de tout l'assistant. "
        "Chaque changement mérite donc une recette.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Qui rédige et valide le system prompt ? "
        "Quels sont les sujets interdits, et que répond-on dans ce cas ? "
        "Comment teste-t-on une nouvelle version avant de la déployer ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le prompt est une spécification. Contexte, tâche, contraintes, format et exemples. "
        "Et le system prompt se gère comme un livrable. "
        "Prochaine capsule : brancher un LLM sur les données du client, avec le RAG.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
