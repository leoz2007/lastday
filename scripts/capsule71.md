# Capsule 71 · Évaluer un agent

Texte de la voix off (297 mots).

## Scène 1 · Accroche

Un agent peut donner la bonne réponse et avoir échoué quand même. En route, il a peut-être effacé un fichier, ou fait des dizaines d'appels inutiles. On évalue tout le parcours, pas seulement la fin.

## Scène 2 · Le résultat et la trajectoire

Un agent enchaîne des actions : chercher, lire, modifier, vérifier. On évalue d'abord le résultat final : la tâche est-elle faite, les tests passent-ils ? Puis la trajectoire, c'est-à-dire le chemin suivi : étapes inutiles, actions dangereuses, coût, durée, nombre d'appels.

## Scène 3 · Un environnement de test isolé

Pour tester, il faut un environnement isolé et reproductible : le même point de départ à chaque essai. Les outils sont simulés, ou branchés sur des copies : un faux service de paiement, une copie de la base de données. Ainsi, une erreur de l'agent ne touche jamais la production.

## Scène 4 · Rejouer et mesurer un taux de réussite

Autre piège : le même agent, sur la même tâche, ne fait pas toujours la même chose. Un seul essai ne prouve donc rien. On rejoue chaque tâche plusieurs fois, et on mesure un taux de réussite : par exemple, sept réussites sur dix essais.

## Scène 5 · Ce que ça change côté produit

Côté produit, les benchmarks publics, des tests de référence partagés, donnent une première idée. Mais leurs tâches peuvent être loin des vôtres, et les modèles les ont parfois déjà vues pendant leur entraînement. Construisez vos propres scénarios, tirés de cas réels, chacun avec son critère de réussite.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Qu'est-ce qui prouve que la tâche est faite ? Quelles actions sont interdites, même si le résultat est bon ? Et combien d'essais par tâche, pour quel taux de réussite visé ?

## Scène 7 · À retenir

À retenir : on évalue un agent sur son résultat et sur son parcours, dans un environnement isolé. Rejouez chaque tâche plusieurs fois, sur vos propres scénarios. Prochaine capsule : le reward hacking, quand un modèle contourne le critère qui le récompense.
