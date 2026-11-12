from engine import *  # noqa
from engine import _paint  # noqa

NUM = 17
TITLE = 'UX ASSISTANT IA'
FULL_TITLE = "UX d'un assistant IA"
SLUG = 'ux_assistant_ia'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


def text_lines(c, t, at, x, y, widths, color=PL, h=24, gap=50, stagger=0.08):
    """Lignes de texte schématiques (barres arrondies) qui s'allongent."""
    for k, w in enumerate(widths):
        p = ease(prog(t, at + k * stagger, 0.5))
        if p > 0 and w * p > h:
            rrect(c, x, y + k * gap, w * p, h, h / 2, color)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Une bonne réponse ne suffit *pas*.')
    a = S.cue('bonne réponse')
    card(c, t, a, 240, 980, 600, 200, WHITE, 36, 'pop')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 320, 1080, 60, RED)
        text_lines(c, t, a + 0.2, 390, 1030, [380, 330, 220], PL, 22, 42)
    items = [('Attente', "l'attente", 90, 850), ('Sources', 'les sources', None, 850),
             ('Doutes', 'les doutes', 90, 1250), ('Correction', 'corriger', None, 1250)]
    for k, (s, kw, x, y) in enumerate(items):
        at = S.cue(kw)
        w = chip_width(s, 36)
        xx = x if x is not None else 990 - w
        chip(c, t, at, s, xx, y, RED if k == 3 else WHITE, WHITE if k == 3 else DARK, 36)
        # trait de liaison vers la bulle
        cx = xx + w / 2
        y1 = y + 63 if y < 1000 else y
        y2 = 980 if y < 1000 else 1180
        if t >= at + 0.1:
            arrow(c, t, at + 0.1, cx, y1 + (8 if y < 1000 else -8), cx, y2 + (-6 if y < 1000 else 6),
                  PL, 5, 0)


def s2(c, t, S):
    header(c, t, S, 'Les sources', "Montrer d'où ça *vient*")
    a = S.cue('Première règle')
    card(c, t, a, 90, 540, 900, 330, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'chat', 165, 605, 50, DARK)
        small(c, 'Réponse', 215, 615, 22, DARK)
        text_block(c, t, a + 0.2, 'Remboursable sous *30 jours*.', 140, 710, 40, 'Medium',
                   DARK, RED, maxw=800, max_lines=1)
    so = S.cue('affichez la source')
    icon(c, t, so, 'doc', 165, 800, 40, RED)
    chip(c, t, so + 0.1, 'Politique de remboursement · art. 3', 210, 772, WHITE, DARK, 28)
    ps = S.cue('peu sûr')
    card(c, t, ps, 90, 930, 900, 330, LIGHT, 36, 'up')
    if prog(t, ps, 0.5) > 0.4:
        label(c, t, ps + 0.1, 'À vérifier', 140, 965, RED, WHITE, 22)
        text_block(c, t, ps + 0.2, "Je n'ai pas trouvé de règle pour les *soldes*.", 140, 1090, 38,
                   'Medium', DARK, RED, maxw=800, max_lines=2)
    ta = S.cue('peu sûr') + 0.8
    if t >= ta - 0.2:
        small(c, 'Confiance', 140, 1213, 22, DARK)
        bar(c, t, ta, 330, 1192, 610, 28, 0.35, RED, WHITE, 0.6)


def s3(c, t, S):
    header(c, t, S, "L'attente", 'Montrer que ça *avance*')
    st = S.cue('streaming')
    card(c, t, st, 90, 540, 900, 230, LIGHT, 36, 'up')
    if prog(t, st, 0.5) > 0.4:
        small(c, 'Streaming', 140, 600, 22, RED)
        u = clamp((t - st - 0.4) / 3.0)
        words = [110, 150, 80, 130, 100, 170, 90, 140, 120, 100, 150]
        x, y = 140, 630
        for j, wd in enumerate(words):
            if u < j / len(words):
                break
            if x + wd > 940:
                x, y = 140, y + 46
            rrect(c, x, y, wd, 26, 13, RED if j == 0 else PL)
            x += wd + 14
    steps = [('Je cherche dans vos contrats', 'Je cherche'), ('Je compare les dates', 'Je compare'),
             ('Je rédige', 'Je rédige')]
    ta = S.cue('tâche longue')
    card(c, t, ta, 90, 820, 900, 400, LIGHT, 36, 'up')
    if prog(t, ta, 0.5) > 0.4:
        small(c, 'Étapes affichées', 140, 880, 22, DARK)
    for k, (s, kw) in enumerate(steps):
        at = S.cue(kw)
        y = 920 + k * 95
        nxt = S.cue(steps[k + 1][1]) if k < 2 else S.cue('voit que')
        if t >= nxt:
            dot(c, t, nxt, 165, y + 40, 30, RED)
            icon(c, t, nxt, 'check', 165, y + 40, 40, WHITE)
        else:
            dot(c, t, at, 165, y + 40, 30, PLL)
            icon(c, t, at, 'clock', 165, y + 40, 34, DARK)
        reveal_plain(c, t, at + 0.1, s, 220, y + 52, 34, DARK)
    ar = S.cue('arrêter')
    card(c, t, ar, 90, 1270, 300, 110, DARK, 30, 'pop')
    if prog(t, ar, 0.5) > 0.4:
        rrect(c, 135, 1307, 36, 36, 6, WHITE)
        plain(c, 'Arrêter', 195, 1337, 34, WHITE)
    if t >= ar + 0.3:
        reveal_plain(c, t, ar + 0.3, "L'utilisateur garde la main", 430, 1337, 32, DARK)


def s4(c, t, S):
    header(c, t, S, 'Corriger', 'Garder la *main*')
    a = S.cue('Troisième règle')
    card(c, t, a, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        label(c, t, a + 0.1, 'Brouillon de mail', 140, 575, PLL, DARK, 22)
        r = S.cue('raccourcit')
        sh = ease(prog(t, r, 0.8))
        widths = [780, 740, 760 * (1 - sh), 690 * (1 - sh), 480]
        ys = [660, 715, 770, 825, 880]
        for k, (w, y) in enumerate(zip(widths, ys)):
            p = ease(prog(t, a + 0.2 + k * 0.08, 0.5))
            yy = y - (110 * sh if k == 4 else 0)
            if w * p > 24:
                rrect(c, 140, yy, w * p, 24, 12, RED if (k == 4 and sh > 0.5) else PL)
        if sh > 0.5:
            label(c, t, r + 0.5, 'Raccourci par vous', 140, 830, RED, WHITE, 22)
    acts = [('Régénérer', 'Régénérer'), ('Éditer la question', 'éditer sa question'),
            ('Modifier', 'modifier directement')]
    x = 90
    for s, kw in acts:
        x += chip(c, t, S.cue(kw), s, x, 980, DARK, WHITE, 32) + 18
    pl = S.cue('pouce levé')
    for k, (s, ic) in enumerate([('Utile', 'check'), ('Pas utile', 'cross')]):
        at = pl + k * 0.3
        xx = 90 + k * 460
        card(c, t, at, xx, 1110, 440, 140, LIGHT, 30, 'pop')
        if prog(t, at, 0.5) > 0.4:
            dot(c, t, at + 0.1, xx + 75, 1180, 36, RED if k == 0 else DARK)
            icon(c, t, at + 0.1, ic, xx + 75, 1180, 44, WHITE)
            plain(c, s, xx + 135, 1192, 34, DARK)
    rp = S.cue('retour précieux')
    icon(c, t, rp, 'db', 130, 1340, 50, RED)
    if t >= rp:
        reveal_plain(c, t, rp + 0.1, 'Un signal pour améliorer', 180, 1352, 34, DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "L'état vide *guide*")
    a = S.cue('premier écran')
    card(c, t, a, 90, 540, 900, 880, LIGHT, 40, 'up')
    cols = [('Je sais faire', 'check', 'sait faire', ['Résumer', 'Comparer', 'Rédiger'], RED),
            ('Je ne fais pas', 'cross', 'ne fait pas', ['Signer', 'Décider à votre place'], DARK)]
    for k, (ttl, ic, kw, items, col) in enumerate(cols):
        at = S.cue(kw)
        x = 130 + k * 420
        card(c, t, at, x, 590, 400, 400, WHITE, 30, 'pop')
        if prog(t, at, 0.5) > 0.4:
            dot(c, t, at + 0.1, x + 55, 650, 28, col)
            icon(c, t, at + 0.1, ic, x + 55, 650, 34, WHITE)
            plain(c, ttl, x + 100, 662, 32, DARK)
            for j, s in enumerate(items):
                reveal_plain(c, t, at + 0.3 + j * 0.2, s, x + 40, 760 + j * 70, 30, DARK, 'Medium')
    sg = S.cue('suggestions cliquables')
    if t >= sg:
        small(c, 'Suggestions', 130, 1050, 22, DARK)
    rc = S.cue('Résumer un contrat')
    chip(c, t, sg + 0.1, 'Résumer un contrat', 130, 1075, RED if t >= rc else PLL,
         WHITE if t >= rc else DARK, 30)
    chip(c, t, sg + 0.3, 'Trouver une clause', 130 + chip_width('Résumer un contrat', 30) + 16,
         1075, PLL, DARK, 30)
    card(c, t, a + 0.4, 130, 1260, 820, 110, WHITE, 55, 'pop')
    if prog(t, a + 0.4, 0.5) > 0.6:
        plain(c, 'Posez votre question', 185, 1326, 30, DARK, 'Medium')
        dot(c, t, a + 0.5, 895, 1315, 34, RED)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Comment voit-on *d'où vient* une réponse ?", "Comment l'"),
        ("Que voit l'utilisateur pendant l'*attente* ?", 'Que voit'),
        ('Comment *corriger* une réponse fausse ?', 'Et comment'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Rendez visibles les *sources*, l\'*attente* et les limites.', "L'interface"),
        ("Laissez toujours l'utilisateur *corriger*.", "Et l'utilisateur"),
    ], '18 · Copilote ou autopilote')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Une bonne réponse ne suffit pas. Ce qui l'entoure compte autant, parfois plus : l'attente, les sources, "
        "les doutes, et la façon de corriger une erreur.")),
    dict(kind='content', draw=s2, name="Rendre visibles les sources et l'incertitude", text=(
        "Première règle : rendre visibles les sources et l'incertitude. "
        "Quand l'assistant s'appuie sur vos documents, affichez la source, avec un lien vers le passage cité : "
        "« Politique de remboursement, article trois ». "
        "Et quand il est peu sûr, il doit le dire, au lieu de prendre partout le même ton assuré.")),
    dict(kind='content', draw=s3, name="Gérer l'attente", text=(
        "Deuxième règle : gérer l'attente. Le streaming affiche la réponse au fil de l'eau, mot après mot. "
        "Pour une tâche longue, affichez les étapes : « Je cherche dans vos contrats », "
        "« Je compare les dates », « Je rédige ». "
        "L'utilisateur voit que ça avance, et peut arrêter en route si ça part mal.")),
    dict(kind='content', draw=s4, name='Permettre de corriger', text=(
        "Troisième règle : permettre de corriger. Régénérer une réponse, éditer sa question, "
        "ou modifier directement le texte produit. "
        "Par exemple, l'utilisateur raccourcit lui-même un brouillon de mail, au lieu de tout redemander. "
        "Et un pouce levé ou baissé vous donne un retour précieux.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, posez les attentes dès le premier écran. "
        "L'état vide n'est jamais vraiment vide : il dit ce que l'assistant sait faire, et ce qu'il ne fait pas. Cela évite bien des déceptions. "
        "Et des suggestions cliquables, comme « Résumer un contrat », aident à démarrer.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Comment l'utilisateur sait-il d'où vient une réponse ? "
        "Que voit-il pendant l'attente ? "
        "Et comment corrige-t-il une réponse fausse ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : une bonne réponse ne suffit pas. "
        "L'interface rend visibles les sources, l'attente et les limites. "
        "Et l'utilisateur doit toujours pouvoir corriger. "
        "Prochaine capsule : copilote ou autopilote, quel niveau d'automatisation choisir, et selon quels critères.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
