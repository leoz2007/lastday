from engine import *  # noqa
from engine import _paint  # noqa

NUM = 43
TITLE = 'EXTRACTION EN MASSE'
FULL_TITLE = 'Extraction en masse'
SLUG = 'extraction_masse'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def mini_doc(c, t, at, x, y, w, h, color):
    """Petit document stylisé qui apparaît en zoom."""
    p = back(prog(t, at, 0.35))
    if p <= 0:
        return
    c.save()
    c.translate(x + w / 2, y + h / 2)
    c.scale(p, p)
    rrect(c, -w / 2, -h / 2, w, h, 8, color)
    c.restore()


def grow_bar(c, t, at, x, base, w, hmax, frac, color):
    """Barre verticale qui pousse depuis sa base."""
    p = ease(prog(t, at, 0.6))
    if p <= 0:
        return
    h = max(w / 2, hmax * frac * p)
    rrect(c, x, base - h, w, h, 10, color)


def s1(c, t, S):
    opening(c, t, S, CAP, 'Une facture, facile. *Dix mille*, un métier.')
    one = S.cue('Une facture')
    icon(c, t, one + 0.3, 'doc', 210, 1000, 130, WHITE)
    if t >= one + 0.4:
        small(c, '1 facture', 210, 1130, 22, WHITE, align='center')
    dm = S.cue('Dix mille')
    for r in range(4):
        for k in range(7):
            mini_doc(c, t, dm + (r * 7 + k) * 0.03, 420 + k * 82, 860 + r * 75, 60, 62,
                     RED if (r, k) == (1, 4) else PL)
    if t >= dm + 0.5:
        small(c, '10 000 factures', 420, 1180, 22, WHITE)
    x = 90
    for s, kw in [('Schéma', 'un schéma'), ('Lots', 'des lots'), ('Contrôles', 'des contrôles'),
                  ('Budget', 'un budget')]:
        hot = s == 'Budget'
        chip(c, t, S.cue(kw), s, x, 1290, RED if hot else WHITE, WHITE if hot else DARK, 32)
        x += chip_width(s, 32) + 24


def s2(c, t, S):
    header(c, t, S, 'Schéma de sortie', 'Une *fiche identique* par document')
    a = S.cue('un schéma de sortie fixe')
    card(c, t, a, 90, 540, 900, 560, LIGHT, 36, 'up')
    if prog(t, a, 0.5) > 0.4:
        icon(c, t, a + 0.1, 'doc', 160, 610, 50, DARK)
        small(c, 'Fiche · champs et formats', 210, 620, 22, DARK)
    rows = [('Numéro', 'FA-2031', 'numéro de facture'),
            ('Date', '12/03/2025', 'la date'),
            ('Montant HT', '1 240,00', 'montant hors taxes'),
            ('Fournisseur', 'Non trouvé', 'le fournisseur')]
    for k, (nm, val, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 680 + k * 100
        if t >= at - 0.1:
            reveal_plain(c, t, at, nm, 140, y + 50, 32, DARK)
        miss = k == 3
        w = chip_width(val, 30)
        chip(c, t, at + 0.2, val, 940 - w, y, PLL if miss else WHITE, DARK, 30)
        if miss and t >= at + 0.4:
            small(c, 'Valeur prévue si absent', 940, y + 88, 16, RED, align='right')
    v = S.cue('le code vérifie')
    card(c, t, v, 90, 1140, 900, 200, RED, 32, 'left')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'code', 180, 1240, 60, WHITE)
        reveal_plain(c, t, v + 0.2, 'Fiche complète ?', 260, 1255, 40, WHITE)
        icon(c, t, S.cue('enregistrer'), 'check', 900, 1240, 56, WHITE)


def s3(c, t, S):
    header(c, t, S, 'Traitement par lots', 'Des lots, et des *reprises*')
    a = S.cue('par lots')
    fails = S.cue('Certains échouent')
    for k in range(6):
        x = 90 + (k % 3) * 310
        y = 540 + (k // 3) * 180
        at = a + k * 0.15
        card(c, t, at, x, y, 280, 150, LIGHT, 28, 'up')
        if prog(t, at, 0.5) > 0.4:
            small(c, f'Lot {k + 1}', x + 30, y + 50, 20, DARK)
            if t >= at - 0.25:
                small(c, '500 docs', x + 250, y + 50, 16, DARK, align='right')
            bar(c, t, at + 0.2, x + 30, y + 85, 220, 26, 0.7 if k == 2 else 1.0, PL, WHITE, 0.8)
            if k == 2:
                dot(c, t, fails, x + 240, y + 98, 26, RED)
                icon(c, t, fails + 0.1, 'cross', x + 240, y + 98, 26, WHITE)
    steps = [('Échec noté', 'doc', "On note l'échec"), ('Relance auto', 'gear', 'on relance'),
             ('Mis de côté', 'user', 'de côté')]
    for k, (s, ic, kw) in enumerate(steps):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 920, 280, 230, LIGHT, 30, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 1000, 64, DARK)
            plain(c, s, x + 140, 1110, 30, DARK, 'Medium', 'center')
        if k < 2:
            arrow(c, t, S.cue(steps[k + 1][2]), x + 284, 1035, x + 306, 1035, DARK, 5, 12)
    r = S.cue('tout recommencer')
    card(c, t, r, 90, 1190, 900, 180, RED, 32, 'up')
    if prog(t, r, 0.5) > 0.4:
        icon(c, t, r + 0.1, 'cross', 180, 1280, 54, WHITE)
        reveal_plain(c, t, r + 0.2, 'Jamais tout recommencer', 250, 1294, 40, WHITE)


def s4(c, t, S):
    header(c, t, S, 'Contrôle qualité', 'Un *seuil*, une file de *revue*')
    a = S.cue('indice de confiance')
    card(c, t, a, 90, 540, 900, 480, LIGHT, 36, 'up')
    vals = [0.9, 0.82, 0.35, 0.95, 0.88, 0.42, 0.78, 0.92]
    base, hmax, thr = 960, 320, 0.6
    sd = S.cue('Sous un seuil')
    ech = S.cue('un échantillon au hasard')
    if prog(t, a, 0.5) > 0.4:
        small(c, 'Confiance par champ · illustratif', 140, 600, 20, DARK)
        for k, v in enumerate(vals):
            x = 160 + k * 100
            low = v < thr and t >= sd
            grow_bar(c, t, a + 0.2 + k * 0.08, x, base, 60, hmax, v, RED if low else PL)
            if k in (1, 6):
                dot(c, t, ech, x + 30, base - hmax * v - 30, 16, DARK)
        if t >= sd:
            p = ease(prog(t, sd, 0.5))
            yy = base - hmax * thr
            rrect(c, 140, yy - 3, 800 * p, 6, 3, DARK)
            if p > 0.8:
                small(c, 'Seuil', 940, yy - 18, 18, DARK, align='right')
    fr = S.cue('file de revue')
    card(c, t, fr, 90, 1060, 440, 360, RED, 32, 'up')
    if prog(t, fr, 0.5) > 0.4:
        icon(c, t, fr + 0.1, 'user', 310, 1170, 90, WHITE)
        plain(c, 'File de revue', 310, 1300, 34, WHITE, 'Medium', 'center')
        if t >= S.cue('un humain tranche'):
            small(c, 'Un humain tranche', 310, 1360, 18, WHITE, align='center')
    card(c, t, ech, 550, 1060, 440, 360, LIGHT, 32, 'up')
    if prog(t, ech, 0.5) > 0.4:
        icon(c, t, ech + 0.1, 'eye', 770, 1170, 90, DARK)
        plain(c, 'Échantillon relu', 770, 1300, 34, DARK, 'Medium', 'center')
        if t >= S.cue('dit vrai'):
            small(c, "L'indice dit-il vrai ?", 770, 1360, 18, RED, align='center')


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'La précision *champ par champ*')
    rows = [('Moyenne', 0.9, DARK, 'moyenne excellente'), ('Numéro', 0.97, PL, 'la date'),
            ('Date', 0.96, PL, 'la date'), ('Montant HT', 0.94, PL, 'la date'),
            ('Fournisseur', 0.62, RED, 'le fournisseur')]
    for k, (nm, f, col, kw) in enumerate(rows):
        at = S.cue(kw) + (0.15 * (k - 1) if kw == 'la date' else 0)
        y = 560 + k * 86
        if t >= at - 0.1:
            reveal_plain(c, t, at, nm, 90, y + 36, 30, RED if k == 4 else DARK)
        bar(c, t, at + 0.1, 360, y + 10, 630, 32, f, col, LIGHT, 0.8)
        if k == 0:
            rrect(c, 90, y + 66, 900, 3, 1, LIGHT)
    if t >= S.cue('le fournisseur') + 0.6:
        small(c, 'Précision illustrative', 90, 1010, 20, DARK)
    pi = S.cue('faites un pilote')
    card(c, t, pi, 90, 1060, 900, 370, LIGHT, 36, 'up')
    if prog(t, pi, 0.5) > 0.4:
        small(c, 'Pilote · quelques centaines de documents', 140, 1120, 20, DARK)
        for k in range(10):
            mini_doc(c, t, pi + 0.2 + k * 0.05, 140 + k * 46, 1160, 34, 42, PL)
        cd = S.cue('le coût et le délai')
        for k, (ic, s) in enumerate([('coin', 'Coût réel'), ('clock', 'Délai réel')]):
            x = 140 + k * 410
            card(c, t, cd + k * 0.2, x, 1250, 390, 140, RED if k == 0 else WHITE, 30, 'pop')
            if prog(t, cd + k * 0.2, 0.5) > 0.4:
                fg = WHITE if k == 0 else DARK
                icon(c, t, cd + k * 0.2 + 0.1, ic, x + 80, 1320, 56, fg)
                plain(c, s, x + 140, 1333, 34, fg, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quels *champs*, quel format, et si un champ manque ?', 'Quels champs'),
        ('Quel *seuil* envoie un document en revue humaine ?', 'Quel seuil'),
        ('Quel *coût* et quel *délai*, mesurés sur un pilote ?', 'Et quels coût'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ("En masse, l'extraction devient une *chaîne de production*.", 'en masse'),
        ('Schéma fixe, *reprises*, seuils et *relecture humaine*.', 'Un schéma fixe'),
    ], '44 · Agents qui utilisent un ordinateur')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Une facture, un modèle l'extrait sans peine. Dix mille factures, c'est un autre métier : "
        "il faut un schéma, des lots, des contrôles, et un budget estimé avant de lancer.")),
    dict(kind='content', draw=s2, name='Un schéma de sortie fixe', text=(
        "D'abord, un schéma de sortie fixe : les champs, leur format, et ce qu'on écrit quand un champ manque. "
        "Par exemple : le numéro de facture, la date, le montant hors taxes, le fournisseur. "
        "Chaque document produit la même fiche, et le code vérifie qu'elle est complète avant de l'enregistrer.")),
    dict(kind='content', draw=s3, name='Lots et reprises sur erreur', text=(
        "Ensuite, on traite par lots, par exemple cinq cents documents à la fois. "
        "Certains échouent : fichier illisible, délai dépassé. "
        "On note l'échec, on relance automatiquement, puis, après quelques essais, on met le document de côté. "
        "Une erreur ne doit jamais obliger à tout recommencer.")),
    dict(kind='content', draw=s4, name='Seuils de confiance et revue humaine', text=(
        "Puis la qualité. Chaque champ reçoit un indice de confiance, issu par exemple de contrôles de cohérence. "
        "Sous un seuil fixé, le document part dans une file de revue, où un humain tranche. "
        "Au-dessus, on relit quand même un échantillon au hasard, pour vérifier que l'indice dit vrai.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, mesurez la précision champ par champ. "
        "Une moyenne excellente peut cacher un champ faible : la date est presque toujours juste, le fournisseur, beaucoup moins. "
        "Et avant de tout lancer, faites un pilote sur quelques centaines de documents : "
        "vous estimez le coût et le délai réels.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels champs, dans quel format, et que faire quand ils manquent ? "
        "Quel seuil de confiance envoie un document en revue humaine ? "
        "Et quels coût et délai prévoir, d'après le pilote ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : en masse, l'extraction devient une chaîne de production. "
        "Un schéma fixe, des reprises sur erreur, des seuils et une relecture humaine. "
        "Prochaine capsule : les agents qui utilisent un ordinateur, comme vous.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
