# Brief commun — capsules « GEN AI EN 2 MIN », saison 2 (11 à 28)

Tu écris des fichiers `video/capsules/capsuleNN.py` pour un moteur de rendu existant (`video/engine.py`, Python + skia). Public : une PO fonctionnelle senior, qui veut un vernis technique en IA générative. La saison 1 (capsules 02 à 10) existe déjà et sert de modèle.

## À lire avant d'écrire
- `video/capsules/capsule02.py`, `video/capsules/capsule05.py` et `video/capsules/capsule07.py` : modèles de structure, de ton et d'illustrations.
- `video/engine.py` : helpers disponibles (voir la liste plus bas). **Ne modifie jamais `engine.py`, ni les fichiers des autres capsules.** Si un helper te manque, définis-le dans ton propre fichier de capsule.

## Interdits
- Pas d'appel à ElevenLabs ni à aucune API, pas de `git commit` ou `git push`, pas de rendu final avec `render.py NN` sans `FAKE_TTS`.
- Seules commandes utiles : `python3 video/render.py NN --md` (compte les mots et écrit `scripts/capsuleNN.md`) et `python3 video/preview.py NN [fraction]` (planche PNG avec un alignement factice, sans appel API).

## Métadonnées du module
```python
from engine import *  # noqa
from engine import _paint  # noqa
NUM = 11
TITLE = 'HALLUCINATIONS'          # court, en capitales, ≤ 22 caractères (en-tête à droite)
FULL_TITLE = 'Hallucinations'
SLUG = 'hallucinations'           # nom de fichier, ascii, minuscules, _
NEXT_CUE = 'prochaine capsule'    # sous-chaîne prononcée dans la scène finale
SERIES = (11, 28)
SERIES_LABEL = 'Saison 2'
...
import sys as _sys  # noqa: E402
CAP = _sys.modules[__name__]
```

## Script (le texte des scènes est envoyé tel quel à la synthèse vocale)
- **280 à 300 mots au total.** Vérifie avec `python3 video/render.py NN --md`.
- Vouvoiement, phrases courtes, ton d'un pair expert et bienveillant. Zéro jargon non expliqué.
- Exactement 7 scènes, dans cet ordre :
  1. `kind='open'` : accroche, une affirmation qui surprend.
  2. à 4. `kind='content'` : trois scènes d'explication, chacune avec un exemple concret.
  5. `kind='content'` : « Côté produit, … » (ce que ça change côté produit).
  6. `kind='content'` : « Au cadrage, posez trois questions. … » (utilise le helper `questions`).
  7. `kind='end'` : « À retenir : … », puis l'annonce de la capsule suivante, qui commence par « Prochaine capsule : ». La 28 conclut la saison, sans annonce.
- **N'invente aucun chiffre présenté comme un fait** (prix, tailles, pourcentages, parts de marché). Si un ordre de grandeur aide, présente-le comme un exemple illustratif.
- **Écris les nombres en toutes lettres** dans le texte des scènes (« trois », « cent »). À l'écran, dans les illustrations, les chiffres sont permis.
- Exactitude technique : reste sur ce qui est vrai en général. Pas de nom de fournisseur ni de produit, pas d'affirmation datée.
- N'emploie que des caractères latins courants. Les guillemets « » sont permis ; pas de flèches Unicode (→) ni d'emoji : la police ne les a pas. Dessine les flèches avec `arrow()`.
- Chaque `dict` de scène porte `name=` (titre de scène pour le .md) pour les scènes de contenu.

## Gabarit visuel (le moteur dessine déjà l'en-tête, la barre de progression, le pied et les sous-titres)
- Zone de contenu : x de 90 à 990, y d'environ 520 à 1450 maximum. **Rien sous y = 1460** : les sous-titres occupent 1500 à 1720.
- Scène 1 : `opening(c, t, S, CAP, 'Titre avec *accent*')`, 3 lignes max à 96 px, puis une illustration entre y ≈ 820 et 1440. Fond Dark Grey, texte blanc.
- Scènes 2 à 5 : `header(c, t, S, 'Étiquette', 'Titre avec *accent*')` (2 lignes max à 80 px ; le titre finit vers y ≈ 500), puis l'illustration à partir de y ≈ 540.
- Scène 6 : `questions(c, t, S, 'Trois *questions* à poser', [(texte_court_avec_*accent*, mot_clé), ...])`. Chaque question tient en 2 lignes max : reformule-la plus courte qu'à l'oral si besoin.
- Scène 7 : `ending(c, t, S, CAP, [(texte, mot_clé), (texte, mot_clé)], 'NN · Titre suivant')`. Deux cartes, trois maximum, chacune de 3 lignes max. Pour la 28 : `ending(..., 'Vous savez *cadrer* un projet', next_label='Saison terminée')`.
- **Chaque scène a une vraie illustration animée** du concept (schéma, flux, barres, cartes, nuage de points, chronologie…), pas seulement du texte. Une idée par écran, beaucoup de blanc.
- Palette uniquement : `RED` (accent unique, mots clés), `DARK` (texte), `WHITE`, `LIGHT` (cartes), `PL` et `PLL` (barres, pastilles, progressions ; **jamais comme couleur de texte**). Pas de dégradé, pas de transparence. Le texte apparaît par glissement sous masque (les helpers le font déjà).
- Texte sur fond rouge : blanc. Texte sur `PL`/`PLL` : `DARK`. Sur fond Dark Grey : blanc, ou rouge pour l'accent.
- Animations déclenchées sur le mot prononcé : `S.cue('sous-chaîne')` renvoie l'instant où elle est prononcée dans la scène (insensible à la casse, première occurrence ; `nth=2` pour la deuxième). **La sous-chaîne doit exister telle quelle dans le texte de la scène**, sinon c'est une KeyError. `S.t0` est le début de la scène.

## Helpers d'`engine.py` (signatures abrégées ; `at` = instant d'apparition)
- `text_block(c,t,at,s,x,y,size,weight,color,accent,maxw,align,max_lines)` : texte multi-lignes, `*accent*` en rouge, `y` = ligne de base.
- `reveal_plain(c,t,at,s,x,y,size,color,weight,align)` : une ligne. `plain(...)` : une ligne sans animation.
- `small(c,s,x,y,size,color,align=)` : petites capitales Bold.
- `label(c,t,at,s,x,y,bg,fg,size)` : pastille d'étiquette.
- `card(c,t,at,x,y,w,h,fill,r,mode)` avec `mode` = `'pop'`, `'up'`, `'left'` ou `'right'`. `box(...)` : carte avec texte centré.
- `chip(c,t,at,s,x,y,fill,fg,size)` : renvoie la largeur ; `chip_width(s,size)`.
- `bar(c,t,at,x,y,w,h,frac,fill,bg)` : barre qui se remplit.
- `arrow(c,t,at,x1,y1,x2,y2,color,width,head)` ; `dot(c,t,at,x,y,r,color)` ; `rrect(c,x,y,w,h,r,color)`.
- `check_row(...)` ; `icon(c,t,at,kind,cx,cy,s,color,bg=None)` avec `kind` parmi doc, search, gear, user, chat, db, shield, check, cross, clock, coin, lock, brain, bolt, code, eye, target.
- `prog`, `ease`, `back`, `clamp`, `lerp`, `font(weight,size)`, `text_width(s,font)`.
- Textes dans `box`/`chip` : vise une largeur de texte inférieure à celle de la carte. `text_block` lève une erreur au-delà de `max_lines`.

## Contrôle obligatoire avant de rendre
1. `python3 video/render.py NN --md` : entre 280 et 300 mots.
2. `python3 video/preview.py NN` (fin de chaque scène), puis `python3 video/preview.py NN 0.55` (milieu des scènes). Ouvre les PNG avec l'outil Read (`video/build/capsuleNN/preview_sheet.png`) et vérifie : aucun débordement, aucun chevauchement entre éléments ou avec les sous-titres, chaque scène illustrée, texte lisible.
3. Corrige, puis relance jusqu'à ce que ce soit propre.
4. Relis le script pour l'exactitude technique.
