from engine import *  # noqa
from engine import _paint  # noqa

NUM = 51
TITLE = 'PROPRIÉTÉ ET IA'
FULL_TITLE = 'Propriété intellectuelle'
SLUG = 'propriete_intellectuelle'
NEXT_CUE = 'prochaine capsule'
SERIES = (39, 54)
SERIES_LABEL = 'Saison 4'


def outline(c, x, y, w, h, r, color, width=5):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + w, y + h), r, r), _paint(color, width))


def s1(c, t, S):
    opening(c, t, S, CAP, 'La propriété intellectuelle, c\'est *trois questions*.')
    m = S.t0 + 0.6
    card(c, t, m, 390, 880, 300, 300, WHITE, 40, 'pop')
    if prog(t, m, 0.5) > 0.4:
        icon(c, t, m + 0.1, 'brain', 540, 1000, 90, DARK)
        plain(c, 'Modèle', 540, 1120, 30, DARK, 'Medium', 'center')
    items = [('Entrée', 'ce que vous envoyez', 'doc', 90, 960),
             ('Sortie', "ce qu'il produit", 'chat', 790, 880),
             ('Code', 'le code qu', 'code', 790, 1110)]
    for k, (s, kw, ic, x, y) in enumerate(items):
        at = S.cue(kw)
        card(c, t, at, x, y, 200, 180, RED if t >= at else WHITE, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 100, y + 70, 56, WHITE)
            plain(c, s, x + 100, y + 150, 28, WHITE, 'Medium', 'center')
        if k == 0:
            arrow(c, t, at + 0.2, 300, 1050, 380, 1040, WHITE, 6, 18)
        else:
            arrow(c, t, at + 0.2, 700, 1030 if k == 1 else 1060, 780, y + 90, WHITE, 6, 18)
    mr = S.cue('rater des risques')
    if t >= mr:
        reveal_plain(c, t, mr, 'Trois risques à traiter séparément', 540, 1390, 34, WHITE, 'Medium', 'center')


def s2(c, t, S):
    header(c, t, S, '1 · Ce que vous envoyez', 'Avez-vous *le droit* de l\'envoyer ?')
    rows = [('Document confidentiel', 'document confidentiel', 'lock'),
            ('Texte sous droits', 'texte sous droits', 'doc'),
            ('Fichier client', 'fichier client', 'user')]
    for k, (s, kw, ic) in enumerate(rows):
        at = S.cue(kw)
        y = 560 + k * 120
        card(c, t, at, 90, y, 520, 100, LIGHT, 28, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 145, y + 50, 40, DARK)
            reveal_plain(c, t, at + 0.15, s, 190, y + 61, 30, DARK, 'Medium')
    tr = S.cue('le transmettre')
    arrow(c, t, tr, 625, 710, 735, 710, DARK, 6, 18)
    card(c, t, tr + 0.2, 750, 590, 240, 240, DARK, 36, 'pop')
    if prog(t, tr + 0.2, 0.5) > 0.4:
        icon(c, t, tr + 0.3, 'brain', 870, 690, 70, WHITE)
        plain(c, 'Modèle', 870, 790, 28, WHITE, 'Medium', 'center')
    ct = S.cue('le contrat du fournisseur')
    card(c, t, ct, 90, 940, 900, 480, LIGHT, 36, 'up')
    if prog(t, ct, 0.5) > 0.4:
        label(c, t, ct + 0.1, 'Contrat du fournisseur', 140, 975, PLL, DARK, 22)
        qs = [('Vos données entraînent-elles ses modèles ?', 'entraîner ses modèles'),
              ('Combien de temps sont-elles conservées ?', 'combien de temps')]
        for j, (s, kw) in enumerate(qs):
            at = S.cue(kw)
            y = 1090 + j * 140
            card(c, t, at, 140, y, 800, 110, WHITE, 26, 'left')
            if prog(t, at, 0.5) > 0.4:
                icon(c, t, at + 0.1, 'eye' if j == 0 else 'clock', 200, y + 55, 44, RED)
                reveal_plain(c, t, at + 0.15, s, 250, y + 66, 30, DARK, 'Medium')


def s3(c, t, S):
    header(c, t, S, '2 · Ce que le modèle produit', 'Une protection *incertaine*')
    g = S.cue('sont-ils protégés')
    card(c, t, g, 90, 540, 900, 440, LIGHT, 36, 'up')
    if prog(t, g, 0.5) > 0.4:
        small(c, 'Contenu généré : protégé ?', 140, 600, 20, DARK)
        icon(c, t, g + 0.2, 'doc', 230, 720, 100, DARK)
        inc = S.cue("C'est incertain")
        if t >= inc:
            plain(c, '?', 380, 755, 110, RED, 'Medium', 'center')
        py = S.cue('les pays')
        x = 470
        for s in ['Pays A', 'Pays B', 'Pays C']:
            x += chip(c, t, py + (x - 470) / 1200, s, x, 660, WHITE, DARK, 28) + 14
        ph = S.cue('la part humaine')
        if t >= ph - 0.2:
            small(c, 'Part humaine dans le résultat', 140, 860, 20, DARK)
        bar(c, t, ph, 140, 885, 800, 36, 0.6, RED, WHITE, 1.0)
        if t >= ph:
            small(c, 'Faible', 140, 955, 18, DARK)
            small(c, 'Forte', 940, 955, 18, DARK, align='right')
    rs = S.cue('ressemble trop')
    card(c, t, rs, 90, 1020, 900, 400, LIGHT, 36, 'up')
    if prog(t, rs, 0.5) > 0.4:
        small(c, 'Risque de ressemblance', 140, 1080, 20, DARK)
        ex = S.cue('une œuvre existante')
        lg = S.cue('un logo proche')
        if t >= ex:
            dot(c, t, ex, 300, 1240, 90, DARK)
            dot(c, t, ex + 0.1, 300, 1240, 40, LIGHT)
            small(c, 'Œuvre existante', 300, 1385, 18, DARK, align='center')
        if t >= lg:
            dot(c, t, lg, 780, 1240, 90, RED)
            dot(c, t, lg + 0.1, 788, 1236, 40, LIGHT)
            small(c, 'Sortie générée', 780, 1385, 18, DARK, align='center')
            small(c, 'Trop proche', 540, 1250, 22, RED, align='center')


def s4(c, t, S):
    header(c, t, S, '3 · Le code généré', 'Attention aux *licences*')
    e = S.cue('reproduire des extraits')
    card(c, t, e, 90, 540, 900, 400, LIGHT, 36, 'up')
    if prog(t, e, 0.5) > 0.4:
        small(c, 'Code généré', 140, 600, 20, DARK)
        ws = [620, 520, 640, 460, 580]
        li = S.cue('soumis à une licence')
        for j, w in enumerate(ws):
            y = 640 + j * 50
            hot = j in (1, 2) and t >= li
            rrect(c, 140, y, w * min(1, prog(t, e + 0.1 + j * 0.08, 0.4)), 26, 13, RED if hot else PL)
        if t >= li:
            chip(c, t, li, 'Licence', 960 - chip_width('Licence', 28), 700, DARK, WHITE, 28)
        cd = S.cue('conditions de réutilisation')
        if t >= cd:
            reveal_plain(c, t, cd, 'Licence = conditions de réutilisation', 140, 910, 28, DARK, 'Medium')
    pb = S.cue('publier le code')
    card(c, t, pb, 90, 980, 430, 440, LIGHT, 36, 'up')
    if prog(t, pb, 0.5) > 0.4:
        icon(c, t, pb + 0.1, 'code', 305, 1110, 80, DARK)
        text_block(c, t, pb + 0.2, 'Certaines imposent de *publier* le code dérivé', 130, 1250, 30,
                   'Medium', DARK, RED, maxw=360, max_lines=3)
    v = S.cue('vérifier')
    card(c, t, v, 560, 980, 430, 440, RED, 36, 'up')
    if prog(t, v, 0.5) > 0.4:
        icon(c, t, v + 0.1, 'search', 775, 1110, 80, WHITE)
        text_block(c, t, v + 0.2, 'Vérifier, comme tout code récupéré', 600, 1250, 30,
                   'Medium', WHITE, WHITE, maxw=360, max_lines=3)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Quatre *bonnes pratiques*')
    rows = [('doc', "Règles d'usage", "règles d'usage claires"),
            ('eye', 'Revue humaine', 'revue humaine'),
            ('db', 'Traçabilité du généré', 'traçabilité'),
            ('shield', 'Clauses contractuelles', 'clauses contractuelles')]
    for k, (ic, s, kw) in enumerate(rows):
        at = S.cue(kw)
        y = 550 + k * 140
        card(c, t, at, 90, y, 900, 120, LIGHT, 30, 'left')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, 165, y + 60, 50, DARK)
            reveal_plain(c, t, at + 0.15, s, 230, y + 72, 36, DARK, 'Medium')
    if t >= S.cue('quels outils'):
        small(c, 'Quelles données, quels outils', 960, 550 + 72, 18, DARK, align='right')
    jr = S.cue('service juridique')
    card(c, t, jr, 90, 1130, 900, 200, RED, 36, 'up')
    if prog(t, jr, 0.5) > 0.4:
        icon(c, t, jr + 0.1, 'shield', 180, 1230, 64, WHITE)
        reveal_plain(c, t, jr + 0.2, 'Le juridique tranche', 260, 1250, 44, WHITE, 'Medium')


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles *données* a-t-on le droit d\'envoyer ?', 'Quelles données'),
        ('Qui *relit* les contenus avant publication ?', 'Qui relit'),
        ('Le *juridique* a-t-il validé contrat et règles ?', 'Et le service juridique'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Trois questions : *l\'entrée*, *la sortie*, et *le code*.', 'trois questions distinctes'),
        ('Règles, *revue humaine*, traçabilité, et avis du juridique.', 'Des règles'),
    ], '52 · Contrats avec un fournisseur')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Avec l'IA générative, la propriété intellectuelle pose trois questions distinctes : "
        "ce que vous envoyez au modèle, ce qu'il produit, et le code qu'il écrit. "
        "Les mélanger, c'est rater des risques. Voici des principes généraux, pas un avis juridique.")),
    dict(kind='content', draw=s2, name='Ce que vous envoyez au modèle', text=(
        "Première question : ce que vous envoyez. Un document confidentiel, un texte sous droits, "
        "un fichier client : avez-vous le droit de le transmettre ? "
        "Lisez aussi le contrat du fournisseur : vos données peuvent-elles entraîner ses modèles ? "
        "Et combien de temps sont-elles conservées ?")),
    dict(kind='content', draw=s3, name='Ce que le modèle produit', text=(
        "Deuxième question : ce que le modèle produit. Un texte ou une image générés sont-ils protégés ? "
        "C'est incertain : la réponse varie selon les pays, et dépend de la part humaine dans le résultat. "
        "Autre risque : une sortie qui ressemble trop à une œuvre existante, comme un logo proche d'une marque connue.")),
    dict(kind='content', draw=s4, name='Le code généré', text=(
        "Troisième question : le code généré. Il peut reproduire des extraits de code existant, "
        "soumis à une licence, c'est-à-dire à des conditions de réutilisation. "
        "Certaines licences imposent, par exemple, de publier le code qui en dérive. "
        "Vos développeurs doivent donc vérifier, comme pour tout code récupéré.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, quatre bonnes pratiques. Des règles d'usage claires : quelles données, quels outils. "
        "Une revue humaine avant toute publication. Une traçabilité de ce qui est généré. "
        "Et des clauses contractuelles, avec votre service juridique : c'est lui qui tranche.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles données avez-vous le droit d'envoyer au modèle ? "
        "Qui relit les contenus générés avant publication ? "
        "Et le service juridique a-t-il validé le contrat et les règles d'usage ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : trois questions distinctes, l'entrée, la sortie, et le code. "
        "Des règles, une revue humaine, de la traçabilité, et l'avis du juridique. "
        "Prochaine capsule : les contrats avec un fournisseur de modèle de langage.")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
