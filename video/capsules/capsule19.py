from engine import *  # noqa
from engine import _paint  # noqa

NUM = 19
TITLE = "GÉRER L'ÉCHEC"
FULL_TITLE = "Gérer l'échec"
SLUG = 'gerer_echec'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Votre assistant *va échouer*.')
    a = S.cue('Votre assistant')
    dot(c, t, a, 150, 1000, 30, WHITE)
    if t >= a:
        small(c, 'Question', 150, 940, 22, WHITE, align='center')
    arrow(c, t, a + 0.2, 180, 1000, 520, 1000, WHITE, 8, 0)
    f = S.cue('forcément')
    icon(c, t, f, 'cross', 600, 1000, 70, RED)
    if prog(t, a + 0.6, 0.3) > 0:
        dot(c, t, a + 0.6, 930, 1000, 30, PL)
        small(c, 'Réponse', 930, 940, 22, WHITE, align='center')
    vi = S.cue('ce que vit')
    icon(c, t, vi, 'user', 150, 1170, 70, WHITE)
    so = S.cue('et comment')
    arrow(c, t, so, 520, 1015, 600, 1250, RED, 8, 0, 0.25)
    arrow(c, t, so + 0.25, 600, 1250, 840, 1250, RED, 8, 0, 0.25)
    arrow(c, t, so + 0.5, 840, 1250, 920, 1040, RED, 8, 24, 0.25)
    if t >= so + 0.4:
        chip(c, t, so + 0.4, 'Un parcours prévu', 720, 1290, RED, WHITE, 30, align='center')


def s2(c, t, S):
    header(c, t, S, 'Quatre cas', 'Échouer de *quatre* façons')
    cases = [('Ne sait pas', 'search', 'ne sait pas'), ('Se trompe', 'cross', 'se trompe'),
             ('Refuse', 'lock', 'refuse'), ('API muette', 'clock', 'ne répond plus')]
    for k, (s, ic, kw) in enumerate(cases):
        at = S.cue(kw)
        x = 90 + (k % 2) * 460
        y = 560 + (k // 2) * 270
        card(c, t, at, x, y, 440, 240, LIGHT, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 220, y + 90, 64, RED)
            plain(c, s, x + 220, y + 195, 36, DARK, 'Medium', 'center')
    g = S.cue('Chaque cas')
    card(c, t, g, 90, 1130, 900, 170, LIGHT, 32, 'up')
    if prog(t, g, 0.5) > 0.4:
        plain(c, 'Une erreur est survenue.', 540, 1230, 38, DARK, 'Medium', 'center')
        p = ease(prog(t, g + 0.4, 0.5))
        if p > 0:
            rrect(c, 250, 1213, 580 * p, 8, 4, RED)
    if t >= g + 0.8:
        reveal_plain(c, t, g + 0.8, 'À chaque cas, sa réponse', 540, 1380, 36, RED, 'Medium', 'center')


def s3(c, t, S):
    header(c, t, S, 'Repli et escalade', 'Dire *vrai*, puis proposer')
    a = S.cue('messages honnêtes')
    card(c, t, a, 90, 540, 900, 230, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 165, 610, 50, RED)
        text_block(c, t, a + 0.2, "« Je n'ai pas trouvé cette information dans vos *documents*. »",
                   220, 630, 34, 'Medium', DARK, RED, maxw=730, max_lines=3)
    opts = [('Reformuler', 'reformuler'), ("Consulter l'aide", "consulter l'aide"),
            ('Parler à un conseiller', 'parler à un conseiller')]
    flow_chips(c, t, [(s, S.cue(kw), RED if k == 2 else PLL, WHITE if k == 2 else DARK)
                      for k, (s, kw) in enumerate(opts)], 90, 820, 900, 32)
    es = S.cue("l'escalade")
    card(c, t, es, 90, 980, 900, 420, LIGHT, 36, 'up')
    if prog(t, es, 0.5) > 0.4:
        label(c, t, es + 0.1, 'Escalade', 140, 1015, PLL, DARK, 22)
        box(c, t, es + 0.2, 140, 1110, 240, 160, 'Assistant', DARK, WHITE, 32)
        card(c, t, es + 0.4, 690, 1110, 250, 160, WHITE, 28, 'pop')
        if prog(t, es + 0.4, 0.5) > 0.4:
            icon(c, t, es + 0.5, 'user', 815, 1170, 56, RED)
            plain(c, 'Conseiller', 815, 1250, 28, DARK, 'Medium', 'center')
    tc = S.cue('transmet la conversation')
    arrow(c, t, tc, 395, 1190, 675, 1190, RED, 6)
    icon(c, t, tc + 0.3, 'doc', 535, 1140, 46, DARK)
    if t >= tc + 0.3:
        reveal_plain(c, t, tc + 0.4, 'Contexte transmis', 535, 1345, 30, DARK, 'Medium', 'center')


def s4(c, t, S):
    header(c, t, S, 'Côté technique', 'Réessayer, puis *dégrader*')
    a = S.cue('on réessaie')
    card(c, t, a, 90, 540, 900, 300, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Tentatives limitées', 140, 600, 22, DARK)
    tr = S.cue('trois tentatives')
    xs = [190, 370, 660]
    for k, x in enumerate(xs):
        at = (a + 0.4) if k == 0 else tr + 0.3 * k
        if k > 0:
            arrow(c, t, at - 0.15, xs[k - 1] + 50, 700, x - 50, 700, PL, 5, 0)
        dot(c, t, at, x, 700, 40, DARK)
        icon(c, t, at + 0.15, 'cross', x, 700, 44, WHITE)
        if t >= at:
            small(c, f'Essai {k + 1}', x, 785, 20, DARK, align='center')
    sp = S.cue('espacées')
    if t >= sp:
        icon(c, t, sp, 'clock', 515, 665, 40, RED)
        small(c, 'Attente plus longue', 515, 752, 18, RED, align='center')
    ad = S.cue('Au-delà')
    arrow(c, t, ad, 900, 740, 900, 880, RED, 6)
    box(c, t, ad + 0.2, 90, 890, 900, 120, 'Mode dégradé', RED, WHITE, 40, 'Medium', 32, 'up')
    opts = [('Réponse simple', 'plus simple'), ("File d'attente", "file d'attente"),
            ('Formulaire classique', 'formulaire')]
    for k, (s, kw) in enumerate(opts):
        at = S.cue(kw)
        box(c, t, at, 90 + k * 307, 1050, 286, 150, s, LIGHT, DARK, 30)
    st = S.cue("ne s'arrête pas")
    chip(c, t, st, 'Le service rend moins, mais continue', 90, 1250, DARK, WHITE, 32)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "L'échec est un *parcours*")
    a = S.cue('un parcours')
    box(c, t, a, 90, 680, 250, 120, 'Question', DARK, WHITE, 32)
    ec = S.cue('ses écrans')
    arrow(c, t, ec, 300, 810, 410, 880, RED, 6, 18)
    box(c, t, ec + 0.2, 420, 840, 250, 120, 'Repli', PLL, DARK, 32)
    ma = S.cue('maquettes')
    arrow(c, t, ma, 680, 900, 730, 900, RED, 6, 18)
    box(c, t, ma + 0.2, 740, 840, 250, 120, 'Humain', RED, WHITE, 32)
    no = S.cue('cas nominal')
    arrow(c, t, no, 350, 710, 730, 630, DARK, 6, 18)
    box(c, t, no + 0.2, 740, 560, 250, 120, 'Réponse', LIGHT, DARK, 32)
    if t >= no + 0.3:
        small(c, 'Cas nominal', 545, 605, 20, DARK, align='center')
        small(c, 'Échec', 300, 900, 20, RED, align='center')
    su = S.cue('suivez-le')
    card(c, t, su, 90, 1030, 900, 380, LIGHT, 36, 'up')
    if prog(t, su, 0.5) > 0.4:
        label(c, t, su + 0.1, 'À suivre', 140, 1065, PLL, DARK, 22)
    ms = [("Taux d'escalade", "taux d'escalade", 0.3), ('Abandons', 'abandons', 0.18),
          ('Réponses de repli', 'réponses de repli', 0.4)]
    for k, (s, kw, fr) in enumerate(ms):
        at = S.cue(kw)
        y = 1170 + k * 75
        reveal_plain(c, t, at, s, 140, y + 12, 30, DARK)
        bar(c, t, at + 0.1, 520, y - 12, 420, 26, fr, RED, WHITE, 0.6)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Que dit l'assistant quand il *ne sait pas* ?", 'Que dit'),
        ('Vers qui *escalader*, avec quel contexte ?', 'Vers qui'),
        ("Que reste-t-il du service si l'*API tombe* ?", 'Et que reste'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("L'échec est un *parcours* à concevoir.", "l'échec n'est"),
        ('Honnêteté, *repli*, *escalade* et mode dégradé.', 'Messages honnêtes'),
    ], '20 · Workflows et chaînes de prompts')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Votre assistant va échouer. Pas peut-être : forcément, un jour ou l'autre. "
        "La vraie question, c'est ce que vit l'utilisateur à ce moment-là, et comment il s'en sort.")),
    dict(kind='content', draw=s2, name="Les quatre cas d'échec", text=(
        "Il y a quatre grands cas. Le modèle ne sait pas. Il se trompe, avec aplomb. Il refuse de répondre, parfois à tort. "
        "Ou l'API, le service qui fait tourner le modèle, ne répond plus du tout. "
        "Chaque cas mérite sa propre réponse, pas un message d'erreur générique.")),
    dict(kind='content', draw=s3, name='Messages honnêtes, repli et escalade', text=(
        "D'abord, des messages honnêtes. « Je n'ai pas trouvé cette information dans vos documents » "
        "vaut toujours mieux qu'une réponse inventée. "
        "Ensuite, un repli : reformuler, consulter l'aide, ou parler à un conseiller. "
        "Et l'escalade vers un humain transmet la conversation, pour ne pas tout réexpliquer.")),
    dict(kind='content', draw=s4, name='Tentatives limitées et mode dégradé', text=(
        "Quand l'API ne répond pas, on réessaie, mais avec une limite : par exemple trois tentatives, "
        "de plus en plus espacées. "
        "Au-delà, on bascule en mode dégradé : une réponse plus simple, une mise en file d'attente, "
        "ou le formulaire classique. Le service rend moins, mais il ne s'arrête pas.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, l'échec se conçoit comme un parcours, avec ses écrans et ses textes. "
        "Dessinez-le dans vos maquettes, au même titre que le cas nominal, celui où tout va bien. "
        "Puis suivez-le en production : taux d'escalade, abandons, réponses de repli.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Que dit l'assistant quand il ne sait pas ? "
        "Vers qui escalade-t-on, et avec quel contexte ? "
        "Et que reste-t-il du service si l'API tombe ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : l'échec n'est pas une exception, c'est un parcours à concevoir. "
        "Messages honnêtes, repli, escalade et mode dégradé : prévoyez-les dès le départ. "
        "Prochaine capsule : workflows et chaînes de prompts, pour découper une tâche en étapes fiables.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
