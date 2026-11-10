from engine import *  # noqa
from engine import _paint  # noqa

NUM = 10
TITLE = 'SORTIES STRUCTURÉES'
FULL_TITLE = 'Sorties structurées et intégration'
SLUG = 'sorties_structurees_integration'
NEXT_CUE = 'dernière capsule'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Une application ne lit pas des *phrases*.')
    a = S.cue('belle phrase')
    card(c, t, a, 90, 820, 430, 330, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Texte libre', 130, 880, 22, DARK)
        for j, fr in enumerate([0.95, 0.8, 0.9, 0.6]):
            bar(c, t, a + 0.1 + j * 0.1, 130, 910 + j * 50, 350, 22, fr, PL, WHITE, 0.4)
        icon(c, t, a + 0.8, 'cross', 470, 1100, 50, RED)
    ch = S.cue('de champs')
    fields = [('motif', 'de champs'), ('urgence', 'de valeurs'), ('service', 'peut traiter')]
    for k, (s, kw) in enumerate(fields):
        box(c, t, S.cue(kw), 560, 820 + k * 115, 430, 95, s, RED, WHITE, 34, 'Medium', 26, 'left')


def json_line(c, t, at, key, val, y, x=140, size=34, last=False):
    p = ease(prog(t, at, 0.4))
    if p <= 0:
        return
    k = f'"{key}" : '
    fk = font('Medium', size)
    c.save()
    c.clipRect(skia.Rect(x - 10, y - size * 1.1, 1000, y + size * 0.4))
    yy = y + (1 - p) * size * 1.2
    plain(c, k, x, yy, size, DARK)
    plain(c, f'"{val}"' + ('' if last else ','), x + text_width(k, fk), yy, size, RED)
    c.restore()


def s2(c, t, S):
    header(c, t, S, 'Sorties structurées', 'Un *JSON* plutôt qu\'un texte')
    j = S.cue('un JSON')
    card(c, t, j, 90, 540, 900, 460, LIGHT, 36, 'up')
    if prog(t, j, 0.5) > 0.4:
        plain(c, '{', 130, 620, 40, DARK)
        json_line(c, t, S.cue('le motif'), 'motif', 'retard de livraison', 720)
        json_line(c, t, S.cue("le niveau d'urgence"), 'urgence', 'haute', 810)
        json_line(c, t, S.cue('le service concerné'), 'service', 'logistique', 900, last=True)
        if t >= S.cue('le service concerné') + 0.3:
            plain(c, '}', 130, 975, 40, DARK)
    if t >= j:
        small(c, 'Exemple de réclamation', 90, 1050, 22, DARK)
    lt = S.cue("L'application lit")
    arrow(c, t, lt, 540, 1080, 540, 1150, DARK, 6)
    tk = S.cue('créer un ticket')
    card(c, t, tk, 90, 1170, 900, 200, WHITE, 32, 'up')
    if prog(t, tk, 0.5) > 0.4:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, 1170, 990, 1370), 32, 32), _paint(RED, 5))
        icon(c, t, tk + 0.1, 'check', 180, 1270, 70, RED)
        plain(c, 'Ticket créé · Logistique · Urgence haute', 250, 1283, 32, DARK)


def s3(c, t, S):
    header(c, t, S, 'Le schéma', 'Chaque champ est *décrit*')
    a = S.cue('un schéma')
    card(c, t, a, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        cols = [('Nom', 140, 'son nom'), ('Type', 400, 'son type'), ('Valeurs', 620, 'valeurs autorisées')]
        for s, x, kw in cols:
            if t >= S.cue(kw):
                small(c, s, x, 610, 22, RED)
        rows = [('motif', 'texte', 'libre'), ('urgence', 'liste', 'basse, moyenne, haute'), ('service', 'liste', 'six services')]
        for k, (n, ty, v) in enumerate(rows):
            y = 700 + k * 80
            reveal_plain(c, t, S.cue('son nom') + k * 0.15, n, 140, y, 32, DARK)
            reveal_plain(c, t, S.cue('son type') + k * 0.15, ty, 400, y, 32, DARK)
            reveal_plain(c, t, S.cue('valeurs autorisées') + k * 0.15, v if k != 2 else 'liste fermée', 620, y, 30, DARK)
    u = S.cue('basse')
    x = 90
    for s, kw in [('basse', 'basse'), ('moyenne', 'moyenne'), ('haute', 'ou haute')]:
        w = chip(c, t, S.cue(kw), s, x, 990, RED, WHITE, 34)
        x += w + 16
    w = chip(c, t, S.cue('ou haute') + 0.4, 'très urgent', x + 20, 990, PLL, DARK, 34)
    icon(c, t, S.cue('ou haute') + 0.6, 'cross', x + 20 + w + 40, 1020, 50, RED)
    ct = S.cue('contraindre')
    box(c, t, ct, 90, 1120, 900, 120, 'API : réponse *contrainte* au schéma', LIGHT, DARK, 34, 'Medium', 30, 'left')
    v = S.cue('vérifier')
    card(c, t, v, 90, 1270, 900, 140, RED, 30, 'up')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'check', 170, 1340, 60, WHITE)
        plain(c, "L'application vérifie quand même", 230, 1352, 34, WHITE)


def s4(c, t, S):
    header(c, t, S, 'Intégration', "Un appel d'*API*")
    a = S.cue("appel d'API")
    box(c, t, a, 90, 540, 330, 140, 'Application', LIGHT, DARK, 34)
    box(c, t, a + 0.3, 660, 540, 330, 140, 'API du modèle', DARK, WHITE, 34)
    for x in (255, 825):
        if t >= a + 0.5:
            c.drawLine(x, 690, x, 1060, _paint(PL, 4))
    e = S.cue("L'application envoie")
    arrow(c, t, e, 260, 760, 815, 760, DARK, 6)
    x = 285
    for s, kw in [('System prompt', 'le system prompt'), ('Message', 'le message'), ('Schéma', 'le schéma')]:
        w = chip(c, t, S.cue(kw), s, x, 785, PLL, DARK, 24, 'Bold', 12)
        x += w + 10
    r = S.cue('Elle reçoit')
    arrow(c, t, r, 820, 920, 265, 920, RED, 6)
    if t >= r:
        small(c, 'Réponse JSON', 540, 960, 22, RED, align='center')
    va = S.cue('la valide')
    box(c, t, va, 90, 1000, 330, 100, 'Valider', RED, WHITE, 32)
    en = S.cue("l'enregistre")
    box(c, t, en, 90, 1120, 330, 100, 'Enregistrer, afficher', LIGHT, DARK, 30)
    er = S.cue("le cas d'erreur")
    label(c, t, er, "Cas d'erreur", 480, 1010, PLL, DARK, 22)
    for k, (s, kw) in enumerate([('Délai dépassé', 'délai dépassé'), ('Réponse invalide', 'réponse invalide'),
                                 ('Nouvelle tentative', 'nouvelle tentative')]):
        chip(c, t, S.cue(kw), s, 480, 1090 + k * 85, DARK if k < 2 else RED, WHITE, 30)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', "Le schéma, un *contrat d'interface*")
    a = S.cue("contrat d'interface")
    box(c, t, a, 90, 580, 260, 140, 'Modèle', DARK, WHITE, 34)
    box(c, t, a + 0.2, 730, 580, 260, 140, 'Application', LIGHT, DARK, 34)
    card(c, t, a + 0.4, 400, 560, 280, 180, RED, 30)
    if prog(t, a + 0.4, 0.5) > 0.4:
        icon(c, t, a + 0.5, 'doc', 540, 630, 60, WHITE)
        plain(c, 'Schéma', 540, 715, 30, WHITE, 'Medium', 'center')
    f = S.cue('comme un formulaire')
    card(c, t, f, 90, 820, 900, 470, LIGHT, 36, 'up')
    if prog(t, f, 0.5) > 0.4:
        label(c, t, f + 0.1, 'Spécifié avec le métier', 140, 860, PLL, DARK, 22)
        rows = [('Quels champs ?', 'quels champs'), ('Quelles valeurs ?', 'quelles valeurs'),
                ('Info manquante ?', 'une information manque')]
        for k, (s, kw) in enumerate(rows):
            at = S.cue(kw)
            y = 950 + k * 105
            reveal_plain(c, t, at, s, 140, y + 50, 32, DARK)
            if t >= at:
                rrect(c, 480, y + 8, 460, 60, 18, WHITE)
                if k == 2:
                    plain(c, '"non trouvé"', 500, y + 50, 30, RED)
    rg = S.cue('regard fonctionnel')
    chip(c, t, rg, 'Votre regard fonctionnel compte ici', 90, 1340, DARK, WHITE, 32)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ("Quels *champs* l'application attend-elle exactement ?", 'Quels champs'),
        ('Que fait-on si une *information manque* ?', 'Que fait-on'),
        ('Qui est prévenu quand la réponse est *invalide* ?', 'qui est prévenu'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Le schéma est un *contrat d'interface*.", 'le schéma est'),
        ('On le spécifie, on le *valide*, on gère les *erreurs*.', 'On le spécifie'),
    ], 'Vous avez les bases pour *cadrer*', next_label='Série terminée')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Pour une application, une belle phrase ne sert à rien. "
        "Elle a besoin de champs, de valeurs, bref de données qu'elle peut traiter.")),
    dict(kind='content', draw=s2, name='Les sorties structurées', text=(
        "D'où les sorties structurées. Au lieu d'un texte libre, on demande au modèle un JSON : "
        "un format simple, fait de champs et de valeurs. "
        "Par exemple, pour une réclamation : le motif, le niveau d'urgence, et le service concerné. "
        "L'application lit ces champs, et peut créer un ticket automatiquement.")),
    dict(kind='content', draw=s3, name='Le schéma', text=(
        "Pour que ce soit fiable, on fournit un schéma. Il décrit chaque champ : son nom, son type, les valeurs autorisées. "
        "L'urgence, par exemple, ne peut être que basse, moyenne ou haute. "
        "Plusieurs fournisseurs proposent un mode qui force la réponse à respecter le schéma : on parle de contraindre la sortie. "
        "Mais l'application doit quand même vérifier ce qu'elle reçoit.")),
    dict(kind='content', draw=s4, name="L'appel depuis l'application", text=(
        "Concrètement, appeler un LLM, c'est un appel d'API, comme pour n'importe quel service web. "
        "L'application envoie le system prompt, le message et le schéma. "
        "Elle reçoit la réponse, la valide, puis l'enregistre ou l'affiche. "
        "Et elle prévoit le cas d'erreur : délai dépassé, réponse invalide, nouvelle tentative.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, le schéma devient un contrat d'interface entre le modèle et l'application. "
        "Il se spécifie avec le métier, comme un formulaire : quels champs, quelles valeurs, "
        "et que faire si une information manque. C'est là que votre regard fonctionnel compte le plus.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels champs l'application attend-elle exactement ? "
        "Que fait-on si le modèle ne trouve pas une information ? "
        "Et qui est prévenu quand la réponse est invalide ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le schéma est un contrat d'interface. On le spécifie, on le valide, et on gère les erreurs. "
        "C'était la dernière capsule de la série. Vous avez maintenant les bases pour cadrer un projet d'IA générative, "
        "et pour poser les bonnes questions.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
