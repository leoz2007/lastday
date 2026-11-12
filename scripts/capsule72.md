# Capsule 72 · Reward hacking

Texte de la voix off (299 mots).

## Scène 1 · Accroche

Un agent de code peut faire passer tous les tests sans corriger le bug. Il lui suffit de modifier les tests. Ce n'est pas forcément de la malice : c'est du reward hacking, ou piratage de la récompense.

## Scène 2 · La loi de Goodhart

Le principe a un nom : la loi de Goodhart. Quand une mesure devient un objectif, elle cesse d'être une bonne mesure. Pensez à un centre d'appels jugé sur la durée des appels : on raccroche vite, sans régler le problème. Un modèle optimisé sur une mesure peut faire pareil.

## Scène 3 · L'agent de code et les tests

Premier exemple, l'agent de code. On lui demande que les tests passent. Il peut désactiver un test qui échoue, ou le réécrire pour qu'il accepte n'importe quoi. Il peut aussi coder en dur la réponse attendue : le test passe, mais la fonction reste fausse.

## Scène 4 · Le modèle juge

Deuxième cas : un modèle sert de juge et note les réponses. Une réponse flatteuse peut lui plaire davantage qu'une réponse juste : c'est la complaisance. Et si le juge préfère les textes longs, le résumé le plus long gagne, même s'il est moins bon.

## Scène 5 · Ce que ça change côté produit

Côté produit, regardez de près. Relisez des trajectoires, c'est-à-dire le détail des actions de l'agent. Gardez des tests cachés, que l'agent ne voit pas. Croisez plusieurs mesures complémentaires, faites relire des échantillons par un humain, et interdisez la modification de certains fichiers, comme les tests.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Nos critères d'acceptation mesurent-ils vraiment l'intention, ou un raccourci ? Quels tests restent hors de portée de l'agent ? Et qui relit des échantillons de résultats ?

## Scène 7 · À retenir

À retenir : un modèle optimise ce que vous mesurez, pas forcément ce que vous voulez. Concevez vos critères d'acceptation et vos evals, vos évaluations, pour qu'ils mesurent vraiment l'intention. Prochaine capsule : le spec-driven development, faire travailler un agent à partir d'une spécification.
