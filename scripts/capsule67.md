# Capsule 67 · Lois d'échelle et calcul à l'inférence

Texte de la voix off (286 mots).

## Scène 1 · Accroche

Pour mieux répondre, on peut agrandir un modèle. Mais un même modèle peut aussi répondre mieux, simplement en prenant plus de temps pour réfléchir. C'est le calcul à l'inférence.

## Scène 2 · Les lois d'échelle

D'abord, les lois d'échelle, en anglais scaling laws. On observe que les performances progressent de façon assez prévisible quand on augmente trois ingrédients : les données, les paramètres, ces réglages appris par le modèle, et le calcul d'entraînement. Comme une recette qu'on agrandit, le résultat suit une tendance.

## Scène 3 · Des rendements décroissants

Mais les rendements sont décroissants. Chaque nouveau gain coûte plus cher : il faut souvent multiplier les moyens pour progresser encore un peu. Et prudence : ce sont des tendances observées, pas des lois physiques. Elles peuvent changer.

## Scène 4 · Le calcul à l'inférence

D'où une autre piste : dépenser plus de calcul au moment de répondre, l'inférence. Le modèle peut réfléchir plus longtemps, faire plusieurs essais puis garder le meilleur, ou vérifier sa réponse, comme un élève qui relit sa copie. C'est utile sur les tâches difficiles, beaucoup moins sur les simples.

## Scène 5 · Ce que ça change côté produit

Côté produit, plus de réflexion veut dire plus de délai et plus de coût par requête, à mettre en balance avec la qualité. Choisissez l'effort selon la tâche : léger pour trier un courriel, plus poussé pour analyser un contrat. Et mesurez le gain sur vos évals, vos tests de référence.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quelles tâches sont vraiment difficiles ? Quel délai et quel coût par requête acceptez-vous ? Et le gain est-il mesuré sur vos évals ?

## Scène 7 · À retenir

À retenir : plus de données, de paramètres et de calcul améliorent les modèles, avec des rendements décroissants. Réfléchir plus longtemps aide sur les tâches difficiles, à un coût : dosez l'effort. Prochaine capsule : l'interprétabilité, pour regarder à l'intérieur d'un modèle.
