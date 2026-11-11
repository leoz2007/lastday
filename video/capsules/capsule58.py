from engine import *  # noqa
from engine import _paint  # noqa

NUM = 58
TITLE = 'LE LLM HUB'
FULL_TITLE = 'Le LLM hub'
SLUG = 'llm_hub'
NEXT_CUE = 'prochaine capsule'
SERIES = (55, 65)
SERIES_LABEL = 'Saison spéciale'


def hub_card(c, t, at, x, y, w, h, fill=RED, fg=WHITE, s='LLM hub', size=34):
    """Carte du hub : un engrenage et son nom."""
    p = card(c, t, at, x, y, w, h, fill, 32, 'pop')
    if p > 0.4:
        icon(c, t, at + 0.1, 'gear', x + w / 2, y + h / 2 - 30, 70, fg)
        plain(c, s, x + w / 2, y + h / 2 + 50, size, fg, 'Medium', 'center')
    return p


def s1(c, t, S):
    opening(c, t, S, CAP, 'Entre agents et modèles, *une seule porte*.')
    a = S.cue('agents de code')
    for k in range(3):
        y = 860 + k * 170
        card(c, t, a + k * 0.12, 90, y, 230, 130, WHITE, 28, 'left')
        if prog(t, a + k * 0.12, 0.5) > 0.4:
            icon(c, t, a + k * 0.12 + 0.1, 'code', 150, y + 65, 50, DARK)
            plain(c, f'Agent {k + 1}', 190, y + 76, 28, DARK, 'Medium')
    d = S.cue('en direct')
    if t >= d and t < S.cue('une seule porte'):
        arrow(c, t, d, 330, 925, 750, 925, PL, 5, 16)
        icon(c, t, d + 0.3, 'cross', 540, 925, 44, RED)
    h = S.cue('une seule porte')
    hub_card(c, t, h, 400, 930, 280, 300)
    if t >= h:
        for k in range(3):
            y = 925 + k * 170
            arrow(c, t, h + 0.2 + k * 0.08, 330, y, 390, lerp(y, 1080, 0.6), DARK, 5, 14)
    m = S.cue('entre les agents et les modèles')
    for k, s in enumerate(['Interne', 'Externe']):
        y = 900 + k * 230
        card(c, t, m + k * 0.15, 760, y, 230, 170, LIGHT, 28, 'right')
        if prog(t, m + k * 0.15, 0.5) > 0.4:
            icon(c, t, m + k * 0.15 + 0.1, 'brain', 875, y + 65, 56, DARK)
            plain(c, s, 875, y + 140, 26, DARK, 'Medium', 'center')
        arrow(c, t, m + k * 0.15, 690, 1080, 750, y + 85, WHITE, 5, 14)
    g = S.cue('gateway')
    chip(c, t, g, 'Gateway', 540, 1350, WHITE, DARK, 30, align='center')


def s2(c, t, S):
    header(c, t, S, 'Le principe', 'Un *standard* téléphonique')
    st = S.cue('standard téléphonique')
    card(c, t, st, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, st, 0.5) > 0.4:
        icon(c, t, st + 0.1, 'user', 200, 740, 70, DARK)
        small(c, 'Agent', 200, 830, 20, DARK, align='center')
        arrow(c, t, st + 0.3, 260, 740, 400, 740, DARK, 6, 18)
        hub_card(c, t, st + 0.4, 410, 600, 260, 280, RED, WHITE, 'Un numéro', 30)
        tr = S.cue('on vous transfère')
        for k, s in enumerate(['Modèle A', 'Modèle B', 'Modèle C']):
            y = 620 + k * 95
            arrow(c, t, tr + k * 0.12, 680, 740, 760, y + 35, DARK, 5, 14)
            box(c, t, tr + k * 0.12 + 0.1, 770, y, 190, 70, s, WHITE, DARK, 26)
    ex = S.cue('Exemples à date')
    if t >= ex:
        small(c, 'Exemples à date', 90, 1010, 22, DARK)
    names = [('LiteLLM', 'LiteLLM'), ('Portkey', 'Portkey'), ('Kong AI Gateway', 'Portkey')]
    for k, (s, kw) in enumerate(names):
        at = S.cue(kw) + (0.4 if k == 2 else 0)
        y = 1040 + k * 100
        card(c, t, at, 90, y, 560, 80, WHITE if k < 2 else PLL, 22, 'left')
        if prog(t, at, 0.5) > 0.4:
            plain(c, s, 130, y + 52, 32, DARK, 'Medium')
    ev = S.cue('évolue vite')
    card(c, t, ev, 690, 1040, 300, 280, DARK, 32, 'pop')
    if prog(t, ev, 0.5) > 0.4:
        icon(c, t, ev + 0.1, 'clock', 840, 1130, 70, WHITE)
        plain(c, 'Ça évolue', 840, 1230, 30, WHITE, 'Medium', 'center')
        plain(c, 'vite', 840, 1272, 30, RED, 'Medium', 'center')


def s3(c, t, S):
    header(c, t, S, 'Clés et quotas', 'Une *clé* par équipe')
    k0 = S.cue('clés virtuelles')
    card(c, t, k0, 90, 540, 900, 470, LIGHT, 36, 'up')
    q = S.cue('un quota')
    if prog(t, k0, 0.5) > 0.4:
        small(c, 'Clé virtuelle · quota mensuel illustratif', 140, 600, 20, DARK)
        rows = [('Équipe Paiement', 0.45), ('Équipe Mobile', 0.7), ('Équipe Data', 0.95)]
        for j, (s, f) in enumerate(rows):
            y = 640 + j * 115
            icon(c, t, k0 + 0.2 + j * 0.12, 'lock', 175, y + 45, 44, RED if j == 2 else DARK)
            reveal_plain(c, t, k0 + 0.25 + j * 0.12, s, 225, y + 30, 28, DARK, 'Medium')
            bar(c, t, q + j * 0.15, 225, y + 55, 700, 30, f, RED if j == 2 else PL, WHITE)
        re = S.cue('jamais la clé réelle')
        if t >= re:
            reveal_plain(c, t, re, 'Jamais la vraie clé du fournisseur', 540, 985, 28, RED, 'Medium', 'center')
    rl = S.cue('rate limiting')
    card(c, t, rl, 90, 1050, 900, 380, LIGHT, 36, 'up')
    if prog(t, rl, 0.5) > 0.4:
        label(c, t, rl + 0.1, 'Limite de débit', 140, 1085, PLL, DARK, 22)
        small(c, 'Requêtes par minute · exemple', 940, 1120, 18, DARK, align='right')
        lim = 140 + 9 * 60
        em = S.cue('agent emballé')
        for k in range(13):
            x = 170 + k * 60
            over = k >= 9
            dot(c, t, rl + 0.3 + k * 0.08, x, 1240, 18, (RED if t >= em else PL) if over else DARK)
        if t >= rl + 0.4:
            rrect(c, lim - 3, 1190, 6, 100, 3, DARK)
            small(c, 'Plafond', lim, 1325, 18, DARK, align='center')
        if t >= em:
            chip(c, t, em, 'Refusé, attendez', 690, 1335, RED, WHITE, 26)


def s4(c, t, S):
    header(c, t, S, 'Routage et secours', 'Router, *basculer*, traduire')
    r = S.cue('le routage')
    card(c, t, r, 90, 540, 900, 400, LIGHT, 36, 'up')
    fb = S.cue('fallback')
    if prog(t, r, 0.5) > 0.4:
        box(c, t, r + 0.1, 130, 680, 180, 110, 'Demande', WHITE, DARK, 28)
        arrow(c, t, r + 0.3, 320, 735, 400, 735, DARK, 6, 18)
        hub_card(c, t, r + 0.4, 410, 610, 200, 250, RED, WHITE, 'Hub', 28)
        tb = S.cue('si le premier tombe')
        arrow(c, t, r + 0.6, 620, 700, 700, 650, PL if t >= tb else DARK, 5, 14)
        box(c, t, r + 0.7, 710, 590, 240, 110, 'Modèle A', WHITE, DARK, 28)
        if t >= tb:
            icon(c, t, tb, 'cross', 925, 600, 36, RED)
        arrow(c, t, fb - 0.3, 620, 780, 700, 830, RED, 5, 14)
        box(c, t, fb - 0.2, 710, 770, 240, 110, 'Secours B', RED, WHITE, 28)
        if t >= fb:
            small(c, 'Fallback', 830, 915, 18, RED, align='center')
    tf = S.cue('formats')
    card(c, t, tf, 90, 980, 900, 210, LIGHT, 36, 'up')
    if prog(t, tf, 0.5) > 0.4:
        small(c, "Format d'API · exemples à date", 140, 1035, 20, DARK)
        chip(c, t, tf + 0.2, 'OpenAI', 140, 1075, WHITE, DARK, 30)
        arrow(c, t, tf + 0.4, 360, 1100, 640, 1100, DARK, 6, 18)
        arrow(c, t, S.cue('inversement'), 640, 1140, 360, 1140, RED, 6, 18)
        chip(c, t, tf + 0.5, 'Anthropic', 950 - chip_width('Anthropic', 30), 1075, WHITE, DARK, 30)
    ca = S.cue('en cache')
    card(c, t, ca, 90, 1230, 900, 200, DARK, 36, 'up')
    if prog(t, ca, 0.5) > 0.4:
        icon(c, t, ca + 0.1, 'bolt', 180, 1330, 64, RED)
        reveal_plain(c, t, ca + 0.2, 'Cache : déjà vu, moins cher', 250, 1320, 36, WHITE, 'Medium')
        small(c, 'Exemple : un même début de prompt', 250, 1375, 20, WHITE)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Le *point de contrôle*')
    pc = S.cue('point de contrôle')
    hub_card(c, t, pc, 380, 560, 320, 280, RED, WHITE, 'LLM hub', 34)
    rows = [('coin', 'FinOps', 'Coûts par équipe', 'la FinOps'),
            ('eye', 'Observabilité', 'Qui appelle quoi', "L'observabilité"),
            ('shield', 'DLP', 'Fuites bloquées', 'la DLP')]
    for k, (ic, s, ex, kw) in enumerate(rows):
        at = S.cue(kw)
        x = 90 + k * 310
        arrow(c, t, at, 540, 850, x + 140, 960, DARK, 5, 14)
        card(c, t, at + 0.1, x, 970, 280, 300, LIGHT if k < 2 else DARK, 32, 'up')
        if prog(t, at + 0.1, 0.5) > 0.4:
            fg = DARK if k < 2 else WHITE
            icon(c, t, at + 0.2, ic, x + 140, 1060, 70, RED if k == 2 else fg)
            plain(c, s, x + 140, 1170, 32, fg, 'Medium', 'center')
            small(c, ex, x + 140, 1225, 18, fg, align='center')
    sc = S.cue('contient un secret')
    if t >= sc:
        reveal_plain(c, t, sc, 'Un secret dans un prompt ? Bloqué.', 540, 1360, 32, RED, 'Medium', 'center')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quel *quota* et quel débit par équipe ?', 'Quel quota'),
        ('Quel *modèle de secours* en cas de panne ?', 'Vers quel modèle'),
        ('Quelles *règles de fuite* sur les prompts ?', 'Et quelles règles'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le hub est la *porte unique* entre agents et modèles.', 'le LLM hub est'),
        ('Clés, quotas, secours, cache : tout se *règle ici*.', 'Clés, quotas'),
    ], '59 · Contexte et outils')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Vos agents de code ne devraient pas appeler un modèle en direct. "
        "Tout passe par une seule porte : le LLM hub, aussi appelé gateway. "
        "C'est le point d'entrée unique entre les agents et les modèles.")),
    dict(kind='content', draw=s2, name='Le principe et des exemples à date', text=(
        "Le principe ressemble à un standard téléphonique : un seul numéro, puis on vous transfère "
        "vers le bon modèle, interne ou externe. "
        "Exemples à date : LiteLLM, Portkey, parmi d'autres. Le paysage évolue vite.")),
    dict(kind='content', draw=s3, name='Clés virtuelles, quotas et limitation de débit', text=(
        "Première fonction : les clés virtuelles. Chaque équipe a la sienne, "
        "jamais la clé réelle du fournisseur. À chaque clé, un quota, par exemple un budget par mois. "
        "Et une limitation de débit, le rate limiting : un plafond de requêtes par minute, "
        "pour qu'un agent emballé ne bloque pas les autres.")),
    dict(kind='content', draw=s4, name='Routage, bascule de secours, traduction et cache', text=(
        "Ensuite, le routage : chaque demande part vers le bon modèle, "
        "et bascule sur un modèle de secours si le premier tombe. C'est le fallback. "
        "Il traduit aussi les formats d'API d'un fournisseur vers un autre, et inversement. "
        "Enfin, il met les prompts en cache : déjà vus, ils coûtent moins cher.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, c'est votre point de contrôle. C'est là qu'on branche la FinOps, "
        "le suivi des coûts par équipe. L'observabilité : qui appelle quel modèle. "
        "Et la DLP, la prévention des fuites de données : un prompt qui contient un secret ne sort pas.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quel quota et quel débit pour chaque équipe ? "
        "Vers quel modèle de secours basculer en cas de panne ? "
        "Et quelles règles de fuite de données appliquer aux prompts ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le LLM hub est la porte unique entre vos agents et vos modèles. "
        "Clés, quotas, routage, secours, traduction et cache : tout se règle à un seul endroit. "
        "Prochaine capsule : contexte et outils, pour ouvrir votre système d'information à l'agent.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
