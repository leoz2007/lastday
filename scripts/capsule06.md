# Capsule 06 · Évaluation (evals)

Texte de la voix off (285 mots).

## Scène 1 · Accroche

Un assistant qui réussit trois exemples en démo ne prouve rien. Sans évaluation, vous ne savez pas s'il marche vraiment, ni s'il marchera encore demain.

## Scène 2 · Le jeu de tests

Une évaluation commence par un jeu de tests : une liste de questions réelles, avec pour chacune la réponse attendue, ou les critères d'une bonne réponse. C'est l'équivalent de vos critères d'acceptation. Par exemple, cinquante questions de clients, dont dix pièges : hors sujet, ambiguës ou malveillantes.

## Scène 3 · Des critères et un score

Avec un LLM, la même question peut produire deux réponses différentes. On ne vérifie donc pas un texte exact, mais des critères : la réponse est-elle juste, complète, fidèle aux sources, polie ? On mesure un taux de réussite sur tout le jeu, pas une impression sur un exemple.

## Scène 4 · Le LLM-as-judge

Pour noter des centaines de réponses, on utilise souvent un autre modèle comme juge : c'est le LLM-as-judge. On lui donne la question, la réponse et une grille de notation précise. Mais un juge se calibre : on compare régulièrement ses notes à celles d'experts humains, sur un échantillon.

## Scène 5 · Ce que ça change côté produit

Côté produit, les evals deviennent votre recette continue. À chaque changement de prompt, de documents ou de modèle, on relance le jeu de tests. Si le score baisse, on ne met pas en production. Et les erreurs vues en production enrichissent le jeu de tests.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Qui écrit les cas de test et les réponses attendues ? Quel score minimum faut-il atteindre pour passer en production ? Et qui, côté métier, valide le juge ?

## Scène 7 · À retenir

À retenir : pas de mise en production sans jeu de tests. Des critères, un score, et une recette relancée à chaque changement. Prochaine capsule : choisir son modèle, entre qualité, coût et temps de réponse.
