# Capsule 31 · Optimiser l'inférence

Texte de la voix off (295 mots).

## Scène 1 · Accroche

Un même assistant peut souvent répondre plus vite et coûter moins cher, à qualité presque égale. Tout se joue à l'inférence, le moment où le modèle calcule ses réponses.

## Scène 2 · Quantification et distillation

Première piste : alléger le modèle. La quantification stocke ses poids, les nombres appris à l'entraînement, avec moins de précision, comme une photo compressée. Le modèle devient plus léger, souvent plus rapide, avec parfois une légère perte de qualité. La distillation, elle, entraîne un petit modèle à imiter un grand, sur une seule tâche, par exemple classer des tickets.

## Scène 3 · Batching et cache de prompt

Deuxième piste : mieux utiliser le matériel. Le batching, ou traitement par lots, regroupe plusieurs requêtes pour les calculer ensemble. Le serveur en traite davantage, mais chacune attend un peu. Le cache de prompt réutilise le calcul d'un début de prompt identique, comme de longues consignes répétées à chaque appel.

## Scène 4 · Le décodage spéculatif

Troisième piste : le décodage spéculatif. Un petit modèle rapide propose plusieurs mots d'avance. Le grand modèle les vérifie d'un coup, garde ceux qu'il aurait écrits, et corrige au premier écart. Quand le petit devine bien, la réponse arrive plus vite, en général sans perte de qualité.

## Scène 5 · Ce que ça change côté produit

Côté produit, chaque optimisation est un compromis entre délai, coût et qualité. Mesurez toujours son effet sur vos evals, avant et après. Un modèle plus rapide qui se trompe davantage sur vos cas critiques n'est pas un gain.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Qu'est-ce qui compte le plus ici : le délai, le coût ou la qualité ? Quelle perte de qualité est acceptable, et sur quels cas ? Et quelles evals rejoue-t-on après chaque optimisation ?

## Scène 7 · À retenir

À retenir : alléger le modèle, regrouper les requêtes, réutiliser le calcul, l'inférence s'optimise. Mais chaque gain se vérifie sur vos evals. Prochaine capsule : le RAG avancé, pour retrouver les bons passages.
