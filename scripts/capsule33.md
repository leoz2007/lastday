# Capsule 33 · Transformers et attention

Texte de la voix off (299 mots).

## Scène 1 · Accroche

Un modèle de langage sait à qui renvoie un pronom, sans règle de grammaire écrite à la main. Dans « la cliente a rappelé le vendeur, car il avait oublié la livraison », il relie « il » au vendeur.

## Scène 2 · L'attention

Le secret s'appelle l'attention. C'est le cœur du transformer, l'architecture des grands modèles de langage. Chaque mot regarde les autres mots du texte pour préciser son sens. Prenez « avocat ». Près de « tribunal », c'est une personne. Près de « salade », c'est un fruit.

## Scène 3 · Des couches empilées

Ce regard ne se fait pas une seule fois. Un transformer empile de nombreuses couches, et chacune affine la représentation de chaque mot. En simplifiant : les premières couches captent plutôt la forme, les suivantes le sens, les plus hautes les liens dans tout le texte. À la sortie, l'avocat est une personne.

## Scène 4 · Le coût de l'attention

Mais l'attention coûte cher. Chaque token, un petit morceau de texte, regarde tous ceux qui le précèdent. Quand le texte double, le travail d'attention fait bien plus que doubler. D'où des fenêtres de contexte limitées, et des réponses plus lentes sur les longs documents.

## Scène 5 · Ce que ça change côté produit

Côté produit, plus de contexte n'est pas toujours mieux. Une information noyée au milieu d'un très long contexte peut être moins bien exploitée qu'au début ou à la fin. Envoyez les passages utiles plutôt que tout le dossier, et testez sur de vrais documents longs.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quelle longueur de contexte vos cas d'usage demandent-ils vraiment ? Quel délai est acceptable sur un long document ? Et l'information clé risque-t-elle d'être noyée au milieu ?

## Scène 7 · À retenir

À retenir : grâce à l'attention, chaque mot regarde les autres pour préciser son sens. Mais ce regard coûte cher sur les longs contextes : envoyez l'essentiel, bien placé. Prochaine capsule : comment un modèle est entraîné.
