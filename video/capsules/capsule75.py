from engine import *  # noqa
from engine import _paint  # noqa

NUM = 75
TITLE = 'CALCUL CONFIDENTIEL'
FULL_TITLE = 'Calcul confidentiel'
SLUG = 'calcul_confidentiel'
NEXT_CUE = 'Vous voyez maintenant'
SERIES = (66, 75)
SERIES_LABEL = 'Saison 5'


def s1(c, t, S):
    opening(c, t, S, CAP, 'Chiffrées partout, *sauf* pendant le calcul.')
    stages = [('Disque', 'sur le disque', 'lock', WHITE, DARK),
              ('Réseau', 'sur le réseau', 'lock', WHITE, DARK),
              ('Calcul', 'en clair', 'eye', RED, WHITE)]
    for k, (s, kw, ic, fill, fg) in enumerate(stages):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 900, 280, 320, fill, 32, 'pop')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 1020, 80, fg)
            plain(c, s, x + 140, 1160, 36, fg, 'Medium', 'center')
        if k < 2:
            arrow(c, t, S.cue(stages[k + 1][1]) - 0.2, x + 284, 1060, x + 306, 1060, WHITE, 5, 12)
    lab = [('Chiffré', 0, 'sur le disque'), ('Chiffré', 1, 'sur le réseau'), ('En clair', 2, 'en clair')]
    for s, k, kw in lab:
        at = S.cue(kw) + 0.3
        if t >= at:
            reveal_plain(c, t, at, s, 90 + k * 310 + 140, 1300, 30, RED if k == 2 else WHITE,
                         'Medium', 'center')
    mm = S.cue('dans la mémoire')
    if t >= mm:
        reveal_plain(c, t, mm, 'Dans la mémoire de la machine', 865, 1390, 26, WHITE, 'Medium', 'right')


def s2(c, t, S):
    header(c, t, S, 'Trois états', 'Protéger aussi la donnée *en usage*')
    cols = [('Au repos', 'au repos', 'db', 'Stockée'),
            ('En transit', 'en transit', 'chat', 'Sur le réseau'),
            ('En usage', "en cours d'usage", 'gear', 'Pendant le calcul')]
    for k, (s, kw, ic, sub) in enumerate(cols):
        at = S.cue(kw)
        x = 90 + k * 310
        card(c, t, at, x, 560, 280, 470, LIGHT, 32, 'up')
        if prog(t, at, 0.5) > 0.4:
            icon(c, t, at + 0.1, ic, x + 140, 680, 70, DARK)
            plain(c, s, x + 140, 820, 34, DARK, 'Medium', 'center')
            small(c, sub, x + 140, 870, 18, DARK, align='center')
    bp = S.cue('bien protégés')
    for k in range(2):
        bar(c, t, bp + k * 0.15, 90 + k * 310 + 40, 940, 200, 36, 1.0, PL, WHITE, 0.6)
        icon(c, t, bp + 0.4 + k * 0.15, 'lock', 90 + k * 310 + 140, 1080, 50, DARK)
    if t >= bp:
        bar(c, t, bp, 660, 940, 200, 36, 0.15, PL, WHITE, 0.4)
        icon(c, t, bp + 0.4, 'eye', 760, 1080, 50, RED)
    cc = S.cue('Le calcul confidentiel')
    arrow(c, t, cc, 760, 1260, 760, 1160, RED, 6, 18)
    card(c, t, cc, 90, 1270, 900, 160, RED, 32, 'up')
    if prog(t, cc, 0.5) > 0.4:
        icon(c, t, cc + 0.1, 'shield', 170, 1350, 60, WHITE)
        reveal_plain(c, t, cc + 0.2, 'Calcul confidentiel', 240, 1335, 38, WHITE)
        pt = S.cue('pendant qu')
        if t >= pt:
            reveal_plain(c, t, pt, 'Protéger la donnée pendant son traitement', 240, 1390, 26, WHITE,
                         'Medium')


def s3(c, t, S):
    header(c, t, S, 'Enclave matérielle', 'Un *coffre* dans le processeur')
    sv = S.cue('enclaves matérielles')
    card(c, t, sv, 90, 540, 900, 500, LIGHT, 32, 'up')
    if prog(t, sv, 0.5) > 0.4:
        small(c, 'Serveur de l\'hébergeur', 140, 600, 20, DARK)
        rrect(c, 140, 640, 520, 360, 24, WHITE)
        small(c, 'Processeur ou GPU', 170, 690, 18, DARK)
        zi = S.cue('zones isolées')
        card(c, t, zi, 200, 730, 400, 230, RED, 28, 'pop')
        if prog(t, zi, 0.5) > 0.4:
            icon(c, t, zi + 0.1, 'lock', 300, 845, 70, WHITE)
            plain(c, 'Enclave', 380, 860, 38, WHITE, 'Medium')
        hb = S.cue("Même l'hébergeur")
        icon(c, t, hb, 'user', 830, 760, 70, DARK)
        if t >= hb:
            small(c, 'Hébergeur', 830, 860, 18, DARK, align='center')
        arrow(c, t, hb + 0.2, 770, 790, 680, 820, DARK, 4, 12)
        icon(c, t, hb + 0.5, 'cross', 830, 940, 50, RED)
    at_ = S.cue("l'attestation")
    card(c, t, at_, 90, 1070, 900, 360, LIGHT, 32, 'up')
    if prog(t, at_, 0.5) > 0.4:
        small(c, 'Attestation · une preuve avant d\'envoyer', 140, 1130, 20, DARK)
        items = [('Le bon code', 'le bon code'), ('La bonne enclave', 'la bonne enclave')]
        for k, (s, kw) in enumerate(items):
            a = S.cue(kw)
            y = 1190 + k * 90
            icon(c, t, a, 'check', 170, y + 30, 44, RED)
            reveal_plain(c, t, a + 0.1, s, 220, y + 45, 32, DARK)
        vd = S.cue("avant d'y envoyer")
        arrow(c, t, vd, 560, 1280, 700, 1280, DARK, 5, 16)
        chip(c, t, vd + 0.2, 'Vos données', 720, 1250, RED, WHITE, 30)


def s4(c, t, S):
    header(c, t, S, 'Autres approches', 'Calculer *sans voir*')
    h = S.cue('chiffrement homomorphe')
    card(c, t, h, 90, 540, 900, 400, LIGHT, 32, 'up')
    if prog(t, h, 0.5) > 0.4:
        small(c, 'Chiffrement homomorphe', 140, 600, 20, DARK)
        d = S.cue('données chiffrées')
        icon(c, t, d, 'lock', 200, 700, 56, DARK)
        reveal_plain(c, t, d + 0.1, 'Données chiffrées', 140, 790, 26, DARK, 'Medium')
        arrow(c, t, d + 0.3, 400, 700, 480, 700, DARK, 5, 14)
        icon(c, t, d + 0.4, 'gear', 540, 700, 60, RED)
        reveal_plain(c, t, d + 0.5, 'Calcul', 540, 790, 26, DARK, 'Medium', 'center')
        arrow(c, t, d + 0.6, 600, 700, 680, 700, DARK, 5, 14)
        icon(c, t, d + 0.7, 'lock', 790, 700, 56, DARK)
        reveal_plain(c, t, d + 0.8, 'Résultat chiffré', 790, 790, 26, DARK, 'Medium', 'center')
        co = S.cue('très coûteux')
        if t >= co:
            small(c, 'Coût · illustratif', 140, 860, 18, DARK)
        bar(c, t, co, 400, 838, 540, 32, 0.9, RED, WHITE, 0.8)
    f = S.cue('apprentissage fédéré')
    card(c, t, f, 90, 970, 900, 460, LIGHT, 32, 'up')
    if prog(t, f, 0.5) > 0.4:
        small(c, 'Apprentissage fédéré', 140, 1030, 20, DARK)
        sites = [(220, 'Site A'), (540, 'Site B'), (860, 'Site C')]
        ld = S.cue('là où sont les données')
        for k, (x, s) in enumerate(sites):
            icon(c, t, ld + k * 0.1, 'db', x, 1110, 56, DARK)
            if t >= ld + k * 0.1:
                small(c, s, x, 1190, 18, DARK, align='center')
        mj = S.cue('mises à jour')
        for k, (x, s) in enumerate(sites):
            arrow(c, t, mj + k * 0.1, x, 1210, 540 + (x - 540) * 0.2, 1290, RED, 4, 12)
        icon(c, t, mj + 0.4, 'brain', 540, 1345, 60, RED)
        if t >= mj + 0.4:
            small(c, 'Modèle commun', 620, 1350, 18, DARK)
            small(c, 'Les données restent sur place', 140, 1410, 18, DARK)


def s5(c, t, S):
    header(c, t, S, 'Côté produit', 'Un modèle chez un tiers, *protégé*')
    u = S.cue('chez un tiers')
    card(c, t, u, 90, 540, 900, 230, LIGHT, 32, 'up')
    if prog(t, u, 0.5) > 0.4:
        icon(c, t, u + 0.1, 'doc', 180, 640, 60, DARK)
        small(c, 'Données sensibles', 180, 730, 18, DARK, align='center')
        arrow(c, t, u + 0.3, 260, 640, 450, 640, DARK, 5, 16)
        icon(c, t, u + 0.4, 'lock', 520, 640, 60, RED)
        small(c, 'Enclave', 520, 730, 18, RED, align='center')
        arrow(c, t, u + 0.5, 590, 640, 760, 640, DARK, 5, 16)
        icon(c, t, u + 0.6, 'brain', 840, 640, 60, DARK)
        small(c, 'Modèle chez un tiers', 840, 730, 18, DARK, align='center')
    lim = [('Coût', 'un coût'), ('Performance', 'performance'),
           ('Complexité', 'complexité'), ('Confiance dans le fabricant', 'fabricant')]
    li = S.cue('des limites')
    if t >= li:
        small(c, 'Les limites', 90, 830, 20, DARK)
    pos = [(90, 860), (500, 860), (90, 970), (500, 970)]
    for k, (s, kw) in enumerate(lim):
        at = S.cue(kw)
        x, y = pos[k]
        chip(c, t, at, s, x, y, PLL, DARK, 32)
    j = S.cue('Le juridique')
    card(c, t, j, 90, 1150, 900, 230, RED, 32, 'up')
    if prog(t, j, 0.5) > 0.4:
        icon(c, t, j + 0.1, 'shield', 180, 1265, 70, WHITE)
        reveal_plain(c, t, j + 0.2, 'Le juridique et la sécurité', 260, 1250, 38, WHITE)
        reveal_plain(c, t, j + 0.35, 'tranchent', 260, 1310, 38, WHITE)


def s6(c, t, S):
    questions(c, t, S, 'Trois *questions* à poser', [
        ('Quelles données protéger *pendant le calcul* ?', 'Quelles données'),
        ("Quelle *preuve d'attestation* l'hébergeur fournit-il ?", "Quelle preuve"),
        ('Quel *surcoût* et quelle lenteur accepter ?', 'Quel surcoût'),
    ])


def s7(c, t, S):
    ending(c, t, S, CAP, [
        ('Le calcul confidentiel protège la donnée *pendant le traitement*.', 'le calcul confidentiel'),
        ('Un outil puissant, avec un *coût*, à valider avec le juridique.', 'un outil puissant'),
    ], 'Vous voyez sous le *capot*', next_label='Saison terminée')


SCENES = [
    dict(kind='open', draw=s1, text=(
        "Vos données sont souvent chiffrées sur le disque, et sur le réseau. "
        "Mais pendant le calcul, elles sont en général en clair, dans la mémoire de la machine.")),
    dict(kind='content', draw=s2, name='Les trois états de la donnée', text=(
        "Une donnée connaît trois états : au repos, stockée ; en transit, sur le réseau ; "
        "et en cours d'usage, pendant le calcul. Les deux premiers sont souvent bien protégés. "
        "Le calcul confidentiel s'attaque au troisième : protéger la donnée pendant qu'on la traite.")),
    dict(kind='content', draw=s3, name='Enclaves et attestation', text=(
        "Première approche : les enclaves matérielles, des zones isolées du processeur ou du GPU, "
        "le processeur graphique. Même l'hébergeur ne peut pas lire ce qui s'y passe. "
        "Et l'attestation apporte une preuve : c'est bien le bon code, dans la bonne enclave, "
        "avant d'y envoyer vos données.")),
    dict(kind='content', draw=s4, name='Chiffrement homomorphe et apprentissage fédéré', text=(
        "Deuxième approche, le chiffrement homomorphe : calculer directement sur des données chiffrées. "
        "Prometteur, mais encore très coûteux, et limité pour les grands modèles. "
        "Troisième, l'apprentissage fédéré : on entraîne le modèle là où sont les données, "
        "et seules les mises à jour circulent.")),
    dict(kind='content', draw=s5, name='Ce que ça change côté produit', text=(
        "Côté produit, c'est utile pour utiliser un modèle chez un tiers avec des données sensibles. "
        "Mais il y a des limites : un coût, de la performance en moins, plus de complexité, "
        "et une confiance à accorder au fabricant du matériel. "
        "Le juridique et la sécurité tranchent.")),
    dict(kind='content', draw=s6, name='Questions à poser au cadrage', text=(
        "Au cadrage, posez trois questions. Quelles données faut-il protéger pendant le calcul ? "
        "Quelle preuve d'attestation l'hébergeur fournit-il ? "
        "Et quel surcoût, quelle lenteur, êtes-vous prêts à accepter ?")),
    dict(kind='end', draw=s7, text=(
        "À retenir : le calcul confidentiel protège la donnée aussi pendant son traitement. "
        "C'est un outil puissant, avec un coût, à valider avec le juridique et la sécurité. "
        "C'était la dernière capsule de la saison cinq. "
        "Merci de l'avoir suivie avec tant de curiosité. "
        "Vous voyez maintenant sous le capot de l'IA générative. À vous de jouer !")),
]

import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
