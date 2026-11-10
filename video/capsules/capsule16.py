from engine import *  # noqa
from engine import _paint  # noqa

NUM = 16
TITLE = "CAS D'USAGE"
FULL_TITLE = "Trouver le bon cas d'usage"
SLUG = 'bon_cas_usage'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'

CRITERIA = [('doc', 'Beaucoup de texte'), ('clock', 'Tâche répétitive'), ('shield', "Tolère l'erreur"),
            ('user', 'Humain qui valide'), ('target', 'Valeur mesurable'), ('db', 'Données disponibles')]


def criteria_grid(c, t, S, cues, first):
    """Grille des six critères ; `first` = indice du premier critère animé dans cette scène."""
    for k, (ic, s) in enumerate(CRITERIA):
        x = 90 + (k % 3) * 310
        y = 550 + (k // 3) * 220
        if first <= k < first + 3:
            at = cues[k - first]
            card(c, t, at, x, y, 280, 200, RED, 30, 'pop')
            if prog(t, at, 0.5) > 0.4:
                icon(c, t, at + 0.1, ic, x + 140, y + 70, 60, WHITE)
                text_block(c, t, at + 0.15, s, x + 140, y + 145, 26, 'Medium', WHITE, WHITE, maxw=240,
                           align='center', max_lines=2, lh=1.2)
        elif k < first:
            rrect(c, x, y, 280, 200, 30, PLL)
            icon(c, t, None, 'check', x + 140, y + 70, 60, DARK)
            text_block(c, t, None, s, x + 140, y + 145, 26, 'Medium', DARK, DARK, maxw=240,
                       align='center', max_lines=2, lh=1.2, reveal=False)
        else:
            rrect(c, x, y, 280, 200, 30, LIGHT)
            plain(c, '?', x + 140, y + 125, 64, PL, 'Light', 'center')


def s1(c, t, S):
    opening(c, t, S, CAP, 'La meilleure idée est souvent la plus *ennuyeuse*.')
    sp = S.cue('la plus spectaculaire')
    card(c, t, sp, 90, 880, 420, 420, LIGHT, 36, 'up')
    if prog(t, sp, 0.5) > 0.4:
        icon(c, t, sp + 0.1, 'bolt', 300, 1010, 100, DARK)
        reveal_plain(c, t, sp + 0.2, 'Spectaculaire', 300, 1170, 36, DARK, 'Medium', 'center')
        en = S.cue('Ennuyeuse')
        icon(c, t, en - 0.2, 'cross', 460, 920, 50, RED)
    en = S.cue('la plus ennuyeuse')
    card(c, t, en, 570, 880, 420, 420, RED, 36, 'up')
    if prog(t, en, 0.5) > 0.4:
        for k in range(3):
            icon(c, t, en + 0.1 + k * 0.1, 'doc', 720 + k * 50, 1010 - k * 20, 80, WHITE)
        reveal_plain(c, t, en + 0.2, 'Ennuyeuse', 780, 1170, 36, WHITE, 'Medium', 'center')
    tags = [('Répétitive', 'répétitive'), ('Pleine de texte', 'pleine de texte')]
    x = 570
    for s, kw in tags:
        at = S.cue(kw)
        x += chip(c, t, at, s, x, 1340, WHITE, RED, 28) + 14


def s2(c, t, S):
    header(c, t, S, 'Les critères', 'Des cases à *cocher*')
    criteria_grid(c, t, S, [S.cue('beaucoup de texte'), S.cue('tâche répétitive'), S.cue("tolérance à l'erreur")], 0)
    ex = S.cue('Exemple')
    card(c, t, ex, 90, 1020, 900, 410, LIGHT, 36, 'up')
    if prog(t, ex, 0.5) > 0.4:
        label(c, t, ex + 0.1, 'Réclamations clients', 140, 1060, WHITE, DARK, 22)
        rc = S.cue('réclamations')
        icon(c, t, rc, 'doc', 230, 1250, 100, DARK)
        small(c, 'Réclamation', 230, 1370, 20, DARK, align='center')
        arrow(c, t, rc + 0.3, 330, 1250, 420, 1250, DARK, 6)
        box(c, t, rc + 0.5, 440, 1170, 260, 160, 'Brouillon', RED, WHITE, 34)
        arrow(c, t, rc + 0.8, 720, 1250, 800, 1250, DARK, 6)
        icon(c, t, rc + 1.0, 'user', 880, 1240, 90, DARK)
        small(c, 'Relu', 880, 1370, 20, DARK, align='center')


def s3(c, t, S):
    header(c, t, S, 'Les critères', 'Humain, *valeur*, données')
    criteria_grid(c, t, S, [S.cue('un humain'), S.cue('valeur mesurable'), S.cue('données disponibles')], 3)
    dl = S.cue('du temps gagné')
    card(c, t, dl, 90, 1020, 440, 410, LIGHT, 36, 'up')
    if prog(t, dl, 0.5) > 0.4:
        small(c, 'Délai de réponse', 140, 1080, 20, DARK)
        small(c, 'Illustratif', 140, 1110, 18, DARK, weight='Medium')
        for k, (nm, h, col) in enumerate([('Avant', 220, PL), ('Après', 110, RED)]):
            x = 180 + k * 170
            hh = h * ease(prog(t, dl + 0.2 + k * 0.4, 0.8))
            if hh > 0:
                rrect(c, x, 1360 - hh, 110, hh, 14, col)
            small(c, nm, x + 55, 1400, 20, DARK, align='center')
    ar = S.cue('archivées')
    card(c, t, ar, 550, 1020, 440, 410, LIGHT, 36, 'up')
    if prog(t, ar, 0.5) > 0.4:
        icon(c, t, ar + 0.1, 'db', 770, 1160, 100, RED)
        jt = S.cue('jeu de test')
        text_block(c, t, jt, 'Archives = *jeu de test*', 770, 1320, 32, 'Medium', DARK, RED, maxw=380,
                   align='center', max_lines=2)


def s4(c, t, S):
    header(c, t, S, 'Fausses bonnes idées', 'Ce que le LLM fait *mal*')
    rows = [('Calcul exact', 'calcul exact', 'Une formule', 'une formule'),
            ('Décision critique sans contrôle', 'décision critique', 'Une relecture humaine', 'aucune relecture'),
            ('Problème réglé par une règle', 'règle simple', 'Une règle simple', 'bloquez')]
    for k, (s, kw, alt, kw2) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 290
        card(c, t, at, 90, y, 900, 260, LIGHT, 32, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, 'cross', 165, y + 75, 50, RED)
            reveal_plain(c, t, at + 0.15, s, 220, y + 90, 36, DARK, 'Medium')
            a2 = S.cue(kw2)
            if t >= a2:
                small(c, 'Plutôt', 220, y + 185, 20, DARK)
                chip(c, t, a2, alt, 350, y + 150, WHITE, DARK, 30)
                icon(c, t, a2 + 0.2, 'check', 920, y + 180, 46, RED)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Partir du *problème*')
    nt = S.cue('Notez chaque idée')
    card(c, t, nt, 90, 550, 900, 470, LIGHT, 36, 'up')
    if prog(t, nt, 0.5) > 0.4:
        label(c, t, nt + 0.1, 'Score sur les critères', 140, 590, WHITE, DARK, 22)
        ideas = [('Réponses aux réclamations', 0.85, RED), ('Assistant pour tout', 0.45, PL),
                 ('Calcul des primes', 0.15, PL)]
        for k, (s, fr, col) in enumerate(ideas):
            y = 690 + k * 105
            plain(c, s, 140, y + 30, 30, DARK)
            bar(c, t, nt + 0.3 + k * 0.25, 140, y + 50, 800, 30, fr, col, WHITE, 0.8)
    cp = S.cue('commencez petit')
    steps = [('Un périmètre', 'un périmètre'), ('Une équipe', 'une équipe'), ('Mesure avant / après', 'une mesure')]
    for k, (s, kw) in enumerate(steps):
        at = S.cue(kw)
        x = 90 + k * 310
        box(c, t, at, x, 1070, 280, 150, s, RED if k == 2 else LIGHT, WHITE if k == 2 else DARK, 30)
        if k < 2:
            arrow(c, t, S.cue(steps[k + 1][1]) - 0.2, x + 285, 1145, x + 305, 1145, DARK, 5, 12)
    if t >= cp:
        small(c, 'Commencer petit', 90, 1060, 20, DARK)
    sm = S.cue('succès modeste')
    chip(c, t, sm, 'Un premier succès modeste', 90, 1290, PLL, DARK, 34)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Combien de fois par mois la tâche *revient* ?', 'Combien de fois'),
        ('Que coûte une *erreur*, et qui la rattrape ?', 'Que coûte'),
        ('Une *règle simple* suffirait-elle ?', 'Et une règle'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("Du texte en volume, de la *répétition*, une tolérance à l'erreur.", 'un bon cas'),
        ('Une règle ou une formule suffit ? *Gardez-la*.', 'Si une règle'),
    ], "17 · UX d'un assistant IA")


SCENES = [
    dict(kind='open', draw=s1, text=(
        "La meilleure idée d'IA n'est pas la plus spectaculaire. "
        "C'est souvent la plus ennuyeuse : une tâche répétitive, pleine de texte, que personne n'aime faire.")),
    dict(kind='content', draw=s2, name='Les critères : texte, répétition, erreur', text=(
        "Un bon candidat coche plusieurs cases. D'abord, beaucoup de texte à lire ou à écrire. "
        "Ensuite, une tâche répétitive, faite des centaines de fois. "
        "Et une tolérance à l'erreur : un brouillon imparfait reste utile. "
        "Exemple : préparer les réponses aux réclamations clients, qu'un conseiller relit avant envoi.")),
    dict(kind='content', draw=s3, name='Les critères : humain, valeur, données', text=(
        "Trois autres critères. Un humain dans la boucle, qui relit et valide. "
        "Une valeur mesurable : du temps gagné, un délai raccourci, moins de relances. "
        "Et des données disponibles, pour construire et tester. "
        "Si vos réclamations passées sont archivées, vous tenez déjà votre jeu de test.")),
    dict(kind='content', draw=s4, name='Les fausses bonnes idées', text=(
        "Attention aux fausses bonnes idées. Le calcul exact : un montant de remboursement se calcule "
        "avec une formule, pas avec un LLM. "
        "La décision critique sans contrôle : accorder un crédit, ou refuser un sinistre, sans aucune relecture. "
        "Et le besoin qu'une règle simple résout : si un champ obligatoire est vide, bloquez le formulaire.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, partez du problème métier, pas de la technologie. "
        "Notez chaque idée sur ces critères, puis commencez petit : un périmètre, une équipe, "
        "une mesure avant et après. "
        "Un premier succès modeste convainc plus qu'une démonstration brillante.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Combien de fois par mois cette tâche revient-elle ? "
        "Que coûte une erreur, et qui la rattrape ? "
        "Et une règle simple suffirait-elle ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un bon cas d'usage combine du texte en volume, de la répétition, "
        "et une tolérance à l'erreur. Si une règle ou une formule suffit, gardez-la. "
        "Prochaine capsule : l'UX d'un assistant IA, ou comment le rendre utile et digne de confiance.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
