import skia

from engine import *  # noqa
from engine import _paint  # noqa

NUM = 14
TITLE = 'MULTIMODAL'
FULL_TITLE = 'Multimodal : images, PDF, voix'
SLUG = 'multimodal_images_pdf_voix'
NEXT_CUE = 'prochaine capsule'
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'


# ---------------------------------------------------------------- pictos locaux
def pic(c, t, at, kind, cx, cy, s=80, color=DARK):
    """Pictos complémentaires : photo, screen, mic, table, pdf."""
    p = back(prog(t, at, 0.4))
    if p <= 0:
        return
    c.save()
    c.translate(cx, cy)
    c.scale(p * s / 100, p * s / 100)
    st = _paint(color, 8)
    fl = _paint(color)
    if kind == 'photo':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-46, -36, 46, 36), 10, 10), st)
        path = skia.Path()
        path.moveTo(-34, 26); path.lineTo(-10, -4); path.lineTo(6, 14); path.lineTo(18, 2); path.lineTo(36, 26)
        path.close()
        c.drawPath(path, fl)
        c.drawCircle(22, -16, 8, fl)
    elif kind == 'screen':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-48, -38, 48, 24), 8, 8), st)
        c.drawLine(0, 24, 0, 40, st)
        c.drawLine(-22, 42, 22, 42, st)
        c.drawLine(-30, -18, 10, -18, st)
        c.drawLine(-30, 0, 24, 0, st)
    elif kind == 'mic':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-16, -46, 16, 10), 16, 16), st)
        path = skia.Path()
        path.addArc(skia.Rect(-32, -22, 32, 26), 0, 180)
        c.drawPath(path, st)
        c.drawLine(0, 26, 0, 44, st)
        c.drawLine(-18, 44, 18, 44, st)
    elif kind == 'pdf':
        path = skia.Path()
        path.moveTo(-32, -42); path.lineTo(14, -42); path.lineTo(32, -24); path.lineTo(32, 42)
        path.lineTo(-32, 42); path.close()
        c.drawPath(path, st)
        for yy in (-10, 8, 26):
            c.drawLine(-18, yy, 18, yy, st)
    elif kind == 'table':
        c.drawRect(skia.Rect(-46, -36, 46, 36), st)
        c.drawLine(-46, -12, 46, -12, st)
        c.drawLine(-46, 12, 46, 12, st)
        c.drawLine(-15, -36, -15, 36, st)
        c.drawLine(15, -12, 15, 36, st)
    c.restore()


def s1(c, t, S):
    opening(c, t, S, CAP, 'Un modèle qui *regarde* vos documents.')
    items = [('photo', 'Photo', 'Une photo'), ('pdf', 'PDF scanné', 'un PDF scanné'),
             ('screen', 'Capture', "une capture d'écran")]
    for k, (ic, s, kw) in enumerate(items):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 840, 280, 240, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            pic(c, t, at + 0.1, ic, x + 140, 930, 80, RED)
            reveal_plain(c, t, at + 0.2, s, x + 140, 1040, 32, DARK, 'Medium', 'center')
    td = S.cue('tout devient')
    for k in range(3):
        x = 90 + k * 310 + 140
        arrow(c, t, td + k * 0.1, x, 1100, 540 + (k - 1) * 60, 1220, WHITE, 5, 16)
    box(c, t, td + 0.4, 290, 1240, 500, 150, 'Une entrée du modèle', RED, WHITE, 36)


def s2(c, t, S):
    header(c, t, S, 'Les entrées', "Plusieurs *types* d'entrées")
    rows = [('photo', 'Photo', 'une photo'), ('pdf', 'Document scanné', 'un document scanné'),
            ('screen', "Capture d'écran", "une capture d'écran"), ('mic', 'Voix', 'La voix')]
    md = S.cue('le modèle traite')
    box(c, t, S.cue('Multimodal'), 760, 600, 230, 380, 'Modèle', RED, WHITE, 36)
    tr = S.cue('transcrite')
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 120
        card(c, t, at, 90, y, 420, 100, LIGHT, 28, 'left')
        if prog(t, at, 0.5) > 0.4:
            pic(c, t, at + 0.1, ic, 150, y + 50, 50, RED)
            reveal_plain(c, t, at + 0.15, s, 200, y + 62, 30, DARK)
        if k < 3:
            arrow(c, t, at + 0.4, 520, y + 50, 750, 640 + k * 90, DARK, 5, 16)
    # voix : transcription intermédiaire
    y = 560 + 3 * 120
    arrow(c, t, tr - 0.1, 520, y + 50, 560, y + 50, DARK, 5, 14)
    chip(c, t, tr, 'Texte', 570, y + 20, PLL, DARK, 30)
    arrow(c, t, tr + 0.3, 690, y + 50, 750, 930, DARK, 5, 14)
    # l'image découpée en morceaux = tokens
    dc = S.cue('découpée')
    card(c, t, dc - 0.2, 90, 1080, 900, 360, LIGHT, 36, 'up')
    if prog(t, dc - 0.2, 0.5) > 0.4:
        gap = 4 + 14 * ease(prog(t, dc + 0.2, 0.6))
        for i in range(3):
            for j in range(3):
                col = RED if (i + j) % 3 == 0 else PL
                rrect(c, 150 + j * (80 + gap), 1140 + i * (80 + gap), 80, 80, 10, col)
        arrow(c, t, md - 0.3, 470, 1260, 560, 1260, DARK, 5, 16)
        for k in range(9):
            col = RED if (k // 3 + k % 3) % 3 == 0 else PL
            x = 590 + (k % 5) * 75
            yy = 1170 + (k // 5) * 90
            dot(c, t, md + k * 0.06, x + 25, yy + 25, 25, col)
        if t >= md + 0.6:
            small(c, 'Morceaux = tokens', 590, 1400, 22, DARK)


def s3(c, t, S):
    header(c, t, S, 'Exemples', 'Lire, extraire, *décrire*')
    ex = [('doc', 'Constat amiable', 'constat', [('Véhicules', 'véhicules'), ('Date', 'la date'), ('Lieu', 'le lieu')]),
          ('pdf', 'Facture PDF', 'facture', [('Montant', 'le montant'), ('Fournisseur', 'le fournisseur'),
                                              ('Échéance', "l'échéance")]),
          ('screen', "Capture d'erreur", "capture d'écran", [('Description du problème', 'il décrit')])]
    for k, (ic, s, kw, fields) in enumerate(ex):
        at = S.cue(kw)
        y = 550 + k * 300
        card(c, t, at, 90, y, 900, 270, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            if ic == 'doc':
                icon(c, t, at + 0.1, 'doc', 180, y + 135, 90, RED)
            else:
                pic(c, t, at + 0.1, ic, 180, y + 135, 90, RED)
            label(c, t, at + 0.15, s, 290, y + 40, WHITE, DARK, 22)
            x = 290
            for fs, fk in fields:
                fa = S.cue(fk)
                w = chip(c, t, fa, fs, x, y + 140, RED if fk == 'il décrit' else WHITE,
                         WHITE if fk == 'il décrit' else DARK, 30)
                x += w + 16


def s4(c, t, S):
    header(c, t, S, 'Les limites', 'Ce qui *coince* encore')
    fl = S.cue('floue')
    card(c, t, fl, 90, 550, 440, 400, LIGHT, 32, 'up')
    if prog(t, fl, 0.5) > 0.4:
        # photo « floue » : contours dédoublés
        pic(c, t, fl + 0.1, 'photo', 300, 700, 130, PL)
        pic(c, t, fl + 0.1, 'photo', 318, 690, 130, DARK)
        reveal_plain(c, t, fl + 0.3, 'Photo floue', 310, 880, 32, DARK, 'Medium', 'center')
    tb = S.cue('tableaux complexes')
    card(c, t, tb, 550, 550, 440, 400, LIGHT, 32, 'up')
    if prog(t, tb, 0.5) > 0.4:
        pic(c, t, tb + 0.1, 'table', 770, 700, 130, DARK)
        icon(c, t, S.cue('mal lus'), 'cross', 880, 620, 60, RED)
        reveal_plain(c, t, tb + 0.3, 'Tableau complexe', 770, 880, 32, DARK, 'Medium', 'center')
    co = S.cue('coûte des tokens')
    card(c, t, co, 90, 990, 900, 440, LIGHT, 36, 'up')
    if prog(t, co, 0.5) > 0.4:
        label(c, t, co + 0.1, 'Coût en tokens', 140, 1030, PLL, DARK, 22)
        gr = S.cue('grande')
        rows = [('Petite image', 0.3, co + 0.3, PL), ('Grande image', 0.85, gr, RED)]
        for k, (nm, fr, at, col) in enumerate(rows):
            y = 1130 + k * 110
            plain(c, nm, 140, y + 30, 30, DARK)
            bar(c, t, at, 140, y + 50, 800, 30, fr, col, WHITE, 0.8)
        vol = S.cue('gros volume')
        if t >= vol:
            small(c, 'Proportions illustratives', 140, 1395, 20, DARK)
            for k in range(3):
                icon(c, t, vol + k * 0.12, 'coin', 790 + k * 60, 1385, 44, RED)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Photographier, puis *vérifier*')
    ph = S.cue('photographie')
    card(c, t, ph, 90, 560, 300, 400, LIGHT, 32, 'up')
    if prog(t, ph, 0.5) > 0.4:
        rrect(c, 170, 610, 140, 240, 24, DARK)
        rrect(c, 182, 630, 116, 190, 10, WHITE)
        pic(c, t, ph + 0.1, 'photo', 240, 725, 60, RED)
        reveal_plain(c, t, ph + 0.2, 'Photo', 240, 920, 30, DARK, 'Medium', 'center')
    ve = S.cue('écran de vérification')
    arrow(c, t, ve - 0.2, 400, 760, 470, 760, DARK, 6)
    card(c, t, ve, 480, 560, 510, 400, LIGHT, 32, 'up')
    if prog(t, ve, 0.5) > 0.4:
        label(c, t, ve + 0.1, 'Champs extraits', 520, 590, PLL, DARK, 20)
        co = S.cue('corrige')
        fields = [('Date', '12/03'), ('Montant', '480 €'), ('Lieu', 'Lyon')]
        for k, (nm, v) in enumerate(fields):
            y = 670 + k * 70
            rrect(c, 520, y, 430, 54, 14, WHITE)
            small(c, nm, 540, y + 36, 20, DARK)
            plain(c, v, 930, y + 38, 28, RED if (k == 1 and t >= co) else DARK, 'Medium', 'right')
        if t >= co:
            icon(c, t, co, 'user', 545, 905, 40, DARK)
        va = S.cue('avant de valider')
        chip(c, t, va, 'Valider', 780, 880, RED, WHITE, 28)
    gd = S.cue('guidez')
    label(c, t, gd, 'Guider la prise de vue', 90, 1030, PLL, DARK, 22)
    tips = [('Cadrage', 'cadrage'), ('Lumière', 'lumière'), ('Une page à la fois', 'une page')]
    x = 90
    for s, kw in tips:
        at = S.cue(kw)
        w = chip_width(s, 34)
        card(c, t, at, x, 1110, w + 40, 220, LIGHT, 28, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, 'check', x + (w + 40) / 2, 1180, 50, RED)
            reveal_plain(c, t, at + 0.2, s, x + (w + 40) / 2, 1285, 34, DARK, 'Medium', 'center')
        x += w + 70


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quels *documents réels*, et de quelle qualité ?', 'Quels documents'),
        ('Qui *vérifie* les champs extraits ?', 'Qui vérifie'),
        ('Quel *coût par document*, fois le volume ?', 'Et combien'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Un modèle multimodal lit aussi *images*, *PDF* et voix transcrite.', 'un modèle multimodal'),
        ("La *qualité de l'entrée* fait la qualité de la sortie.", 'La qualité'),
    ], '15 · Mémoire et personnalisation')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Un modèle d'IA ne lit plus seulement du texte. Il regarde aussi. "
        "Une photo, un PDF scanné, une capture d'écran : tout devient une entrée possible.")),
    dict(kind='content', draw=s2, name="Plusieurs types d'entrées", text=(
        "Multimodal veut dire : plusieurs types d'entrées. "
        "Une photo, un document scanné, une capture d'écran. "
        "La voix aussi : le plus souvent, elle est d'abord transcrite en texte. "
        "Et l'image est découpée en petits morceaux, que le modèle traite comme des tokens.")),
    dict(kind='content', draw=s3, name='Trois exemples concrets', text=(
        "Trois exemples. Un assuré photographie son constat amiable : le modèle en extrait les véhicules, "
        "la date et le lieu. Une facture en PDF : il récupère le montant, le fournisseur et l'échéance. "
        "Une capture d'écran d'erreur : il décrit le problème pour le support.")),
    dict(kind='content', draw=s4, name='Les limites', text=(
        "Mais il y a des limites. Une photo floue ou mal cadrée produit des erreurs, parfois avec beaucoup d'assurance. "
        "Les tableaux complexes, avec des cellules fusionnées, sont souvent mal lus. "
        "Et une image coûte des tokens, d'autant plus qu'elle est grande : sur un gros volume, la facture grimpe.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, la saisie change : l'utilisateur photographie au lieu de remplir un formulaire. "
        "Mais prévoyez un écran de vérification, où il relit les champs extraits et les corrige avant de valider. "
        "Et guidez la prise de vue : cadrage, lumière, une page à la fois.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quels documents réels allez-vous recevoir, et de quelle qualité ? "
        "Qui vérifie les champs extraits avant de les utiliser ? "
        "Et combien coûte le traitement d'un document, multiplié par votre volume ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : un modèle multimodal lit aussi des images, des PDF et de la voix transcrite. "
        "La qualité de l'entrée fait la qualité de la sortie. "
        "Prochaine capsule : mémoire et personnalisation, ou comment un assistant se souvient de vous.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
