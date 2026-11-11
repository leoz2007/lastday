# Capsule 63 · Qualité et cycle de développement

Texte de la voix off (298 mots).

## Scène 1 · Accroche

Un agent qui écrit plus de code ne rend pas forcément votre équipe plus rapide. Il peut aussi produire plus de corrections, plus de relectures, et plus de dette. Pour le savoir, il faut mesurer.

## Scène 2 · Des évals maison sur vos dépôts

D'abord, construisez des évals maison : des tâches réelles tirées de vos dépôts, avec leurs tests. Par exemple, cinquante tickets déjà résolus, rejoués par chaque modèle candidat. Un essai sur votre route, pas sur circuit. Changer de modèle devient une décision objective.

## Scène 3 · Des garde-fous dans l'intégration continue

Ensuite, des garde-fous dans l'intégration continue, la CI, qui vérifie chaque modification. Les tests doivent passer. L'analyse statique de sécurité, le SAST, cherche les failles dans le code. La revue humaine reste obligatoire. Et les demandes de fusion, les PR, ouvertes par un agent ont leurs règles : étiquette visible, périmètre limité.

## Scène 4 · Mesurer l'impact : les métriques DORA

Puis mesurez l'impact avec les métriques DORA, des indicateurs de performance de la livraison logicielle. Rien à voir avec le règlement européen du même nom. À quelle fréquence déploie-t-on ? En combien de temps une modification arrive-t-elle en production ? Quelle part des déploiements échoue ? Et en combien de temps rétablit-on le service ?

## Scène 5 · Ce que ça change côté produit

Côté produit, ajoutez deux mesures. Le taux de reprise, ou rework : la part du code d'agent réécrite peu après. Et la dette générée : du code dupliqué ou obscur, que l'équipe devra porter. Comparez avant et après l'agent, sur plusieurs mois.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Sur quelles tâches de nos dépôts évaluer les modèles ? Quelles règles pour les demandes de fusion d'un agent ? Et quelles mesures suivre, avant et après ?

## Scène 7 · À retenir

À retenir : choisissez vos modèles avec des évals maison, sur vos dépôts. Gardez tests, SAST et revue humaine en CI, et mesurez l'impact avec DORA, le rework et la dette. Prochaine capsule : la gouvernance et la conformité.
