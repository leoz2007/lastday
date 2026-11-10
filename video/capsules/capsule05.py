import math

from engine import *  # noqa
from engine import _paint  # noqa

NUM = 5
TITLE = 'AGENTS'
FULL_TITLE = 'Agents, tool use et MCP'
SLUG = 'agents_tool_use_mcp'
NEXT_CUE = 'prochaine capsule'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un chatbot répond. Un agent *agit*.')
    a = S.cue('Un chatbot')
    card(c, t, a, 90, 820, 430, 300, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 305, 920, 90, DARK)
        reveal_plain(c, t, a + 0.2, 'Chatbot', 305, 1060, 40, DARK, 'Medium', 'center')
    b = S.cue('Un agent')
    card(c, t, b, 560, 820, 430, 300, RED, 36, 'up')
    if prog(t, b, 0.5) > 0.4:
        icon(c, t, b + 0.1, 'bolt', 775, 920, 90, WHITE)
        reveal_plain(c, t, b + 0.2, 'Agent', 775, 1060, 40, WHITE, 'Medium', 'center')
    ag = S.cue('agit à votre place')
    for k, s in enumerate(['Ticket créé', 'Mail envoyé']):
        chip(c, t, ag + 0.2 + k * 0.3, s, 560, 1170 + k * 90, PLL, DARK, 32)


def s2(c, t, S):
    header(c, t, S, 'Tool use', 'Donner des *outils* au modèle')
    tools = [('search', 'Chercher une commande', 'chercher une commande'),
             ('doc', 'Créer un ticket', 'créer un ticket'),
             ('chat', 'Envoyer un mail', 'envoyer un mail')]
    for k, (ic, s, kw) in enumerate(tools):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 540, 280, 220, LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 610, 60, RED)
            text_block(c, t, at + 0.2, s, x + 140, 700, 28, 'Medium', DARK, RED, maxw=240,
                       align='center', max_lines=2, lh=1.15)
    ne = S.cue("n'exécute rien")
    box(c, t, ne, 90, 850, 300, 200, 'LLM', RED, WHITE, 52, 'Light', 30)
    ap = S.cue("c'est l'application")
    card(c, t, ap, 690, 850, 300, 200, LIGHT, 30)
    if prog(t, ap, 0.5) > 0.4:
        icon(c, t, ap + 0.1, 'gear', 840, 920, 60, DARK)
        plain(c, 'Application', 840, 1015, 32, DARK, 'Medium', 'center')
    dm = S.cue('Il demande')
    arrow(c, t, dm, 400, 900, 680, 900, DARK, 6)
    if t >= dm:
        small(c, 'Appel', 540, 880, 20, DARK, align='center')
    rs = S.cue('le résultat')
    arrow(c, t, rs, 680, 1000, 400, 1000, RED, 6)
    if t >= rs:
        small(c, 'Résultat', 540, 1040, 20, RED, align='center')
    pa = S.cue('paramètres')
    card(c, t, pa, 90, 1140, 900, 290, LIGHT, 32, 'up')
    if prog(t, pa, 0.5) > 0.4:
        label(c, t, pa + 0.1, "Demande d'appel", 140, 1175, PLL, DARK, 22)
        plain(c, 'outil : chercher_commande', 140, 1300, 34, DARK, 'Medium')
        plain(c, 'numéro : 4521', 140, 1360, 34, RED, 'Medium')


def s3(c, t, S):
    header(c, t, S, "La boucle d'agent", 'Observer, décider, *agir*')
    cx, cy, r = 540, 850, 230
    nodes = [('Observer', 'observe', -90), ('Décider', 'décide', 0), ('Agir', 'agit', 90), ('Vérifier', 'regarde', 180)]
    for k, (s, kw, ang) in enumerate(nodes):
        at = S.cue(kw)
        a1 = math.radians(ang + 22)
        a2 = math.radians(ang + 68)
        nxt = S.cue(nodes[(k + 1) % 4][1]) if k < 3 else S.cue('recommence')
        arrow(c, t, nxt - 0.2, cx + r * math.cos(a1), cy + r * math.sin(a1),
              cx + r * math.cos(a2), cy + r * math.sin(a2), PL, 6, 18)
    for k, (s, kw, ang) in enumerate(nodes):
        at = S.cue(kw)
        a = math.radians(ang)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        box(c, t, at, x - 125, y - 50, 250, 100, s, RED if k == 2 else LIGHT, WHITE if k == 2 else DARK, 34)
    ob = S.cue("l'objectif")
    icon(c, t, ob, 'target', cx, cy - 10, 80, RED)
    if t >= ob:
        small(c, 'Objectif', cx, cy + 70, 22, DARK, align='center')
    ex = S.cue('Par exemple')
    card(c, t, ex, 90, 1150, 900, 300, LIGHT, 32, 'up')
    steps = [('Trouver la commande', 'Trouve la commande'), ('Vérifier la livraison', 'vérifie la livraison'),
             ('Proposer un geste commercial', 'propose un geste')]
    for k, (s, kw) in enumerate(steps):
        at = S.cue(kw)
        y = 1180 + k * 85
        dot(c, t, at, 150, y + 35, 22, RED)
        if t >= at:
            plain(c, str(k + 1), 150, y + 45, 26, WHITE, 'Bold', 'center')
        reveal_plain(c, t, at + 0.1, s, 195, y + 48, 34, DARK)


def s4(c, t, S):
    header(c, t, S, 'MCP', 'Une *prise universelle*')
    m = S.cue('Model Context Protocol')
    box(c, t, m, 390, 820, 300, 200, 'MCP', RED, WHITE, 60, 'Light', 36)
    if t >= m + 0.3:
        small(c, 'Standard ouvert', 540, 1060, 22, DARK, align='center')
    asst = S.cue('plusieurs assistants')
    for k in range(2):
        y = 640 + k * 300
        box(c, t, asst + k * 0.2, 90, y, 230, 200, f'Assistant {"AB"[k]}', LIGHT, DARK, 32)
        arrow(c, t, asst + 0.3 + k * 0.2, 330, y + 100, 380, 920 - 40 + k * 80, DARK, 5, 16)
    tl = S.cue('des outils et des données')
    tools = [('CRM', 'db'), ('Documents', 'doc'), ('Agenda', 'clock')]
    crm = S.cue('Votre CRM')
    for k, (s, ic) in enumerate(tools):
        y = 600 + k * 200
        at = tl + k * 0.2
        arrow(c, t, at + 0.2, 700, 880 + k * 40, 750, y + 80, DARK, 5, 16)
        card(c, t, at, 760, y, 230, 160, LIGHT, 28)
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 875, y + 60, 50, RED if t >= crm and k < 2 else DARK)
            plain(c, s, 875, y + 135, 28, DARK, 'Medium', 'center')
    un = S.cue('une fois')
    chip(c, t, un, 'Décrit une fois, réutilisé partout', 90, 1290, PLL, DARK, 34)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "Où l'humain *valide*-t-il ?")
    ld = S.cue('Lire des données')
    box(c, t, ld, 90, 560, 520, 120, 'Lire des données', LIGHT, DARK, 34, 'Medium', 30, 'left')
    chip(c, t, ld + 0.4, 'Automatique', 650, 585, PLL, DARK, 32)
    acts = [('Rembourser', 'rembourser'), ('Supprimer', 'supprimer'), ('Écrire à un client', 'écrire à un client')]
    for k, (s, kw) in enumerate(acts):
        at = S.cue(kw)
        box(c, t, at, 90, 720 + k * 140, 520, 120, s, LIGHT, DARK, 34, 'Medium', 30, 'left')
    cf = S.cue('confirmation')
    card(c, t, cf, 650, 720, 340, 400, RED, 32, 'up')
    if prog(t, cf, 0.5) > 0.4:
        icon(c, t, cf + 0.1, 'user', 820, 840, 90, WHITE)
        text_block(c, t, cf + 0.2, 'Validation humaine', 820, 1010, 34, 'Medium', WHITE, WHITE,
                   maxw=280, align='center', max_lines=2)
    tr = S.cue('tracée')
    card(c, t, tr, 90, 1180, 900, 260, LIGHT, 32, 'up')
    if prog(t, tr, 0.5) > 0.4:
        label(c, t, tr + 0.1, 'Journal', 140, 1210, PLL, DARK, 22)
        for k, s in enumerate(['Agent · lecture commande', 'Conseillère · remboursement validé']):
            icon(c, t, tr + 0.3 + k * 0.3, 'clock', 165, 1300 + k * 70, 40, RED)
            reveal_plain(c, t, tr + 0.3 + k * 0.3, s, 210, 1312 + k * 70, 30, DARK)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Quelles actions l'agent peut-il faire *seul* ?", 'Quelles actions'),
        ('Lesquelles exigent une *validation humaine* ?', 'Lesquelles'),
        ('Que se passe-t-il si un outil *échoue* en plein milieu ?', 'Et que se passe'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un agent : un modèle, des *outils* et une *boucle*.', 'un agent, c'),
        ('Plus il agit, plus la *validation humaine* compte.', 'Plus il peut'),
    ], '06 · Évaluation (evals)')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un chatbot vous répond. Un agent, lui, agit à votre place. "
        "Et pour le produit, cette différence change tout : les droits, les risques, la validation.")),
    dict(kind='content', draw=s2, name='Le tool use', text=(
        "Le tool use, c'est donner des outils au modèle. "
        "On lui décrit des fonctions : chercher une commande, créer un ticket, envoyer un mail. "
        "Le modèle n'exécute rien lui-même. Il demande d'appeler un outil, avec des paramètres. "
        "Et c'est l'application qui exécute, puis lui renvoie le résultat.")),
    dict(kind='content', draw=s3, name="La boucle d'agent", text=(
        "Un agent enchaîne ces étapes en boucle. Il observe, décide, agit, regarde le résultat, "
        "puis recommence jusqu'à atteindre l'objectif. "
        "Par exemple : « Trouve la commande du client, vérifie la livraison, et propose un geste commercial. » "
        "Trois outils, plusieurs tours, sans intervention humaine entre chaque étape : c'est sa force, et son risque.")),
    dict(kind='content', draw=s4, name='Le MCP', text=(
        "Le MCP, pour Model Context Protocol, est un standard ouvert pour brancher des outils et des données sur un modèle. "
        "C'est une sorte de prise universelle : on décrit un outil une fois, et plusieurs assistants compatibles peuvent l'utiliser. "
        "Votre CRM ou votre base documentaire deviennent accessibles sans refaire l'intégration pour chaque assistant.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, la vraie question devient : où l'humain valide-t-il ? "
        "Lire des données peut être automatique. "
        "Mais rembourser, supprimer ou écrire à un client mérite une confirmation. "
        "Chaque action doit aussi être tracée, pour savoir qui a fait quoi.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles actions l'agent a-t-il le droit de faire seul ? "
        "Lesquelles exigent une validation humaine ? "
        "Et que se passe-t-il si un outil échoue en plein milieu ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un agent, c'est un modèle, des outils et une boucle. "
        "Plus il peut agir, plus les points de validation humaine comptent. "
        "Prochaine capsule : comment évaluer un assistant, comme on fait une recette.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
