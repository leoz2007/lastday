# Capsule 12 · Température et aléatoire

Texte de la voix off (285 mots).

## Scène 1 · Accroche

Posez deux fois la même question à un modèle de langage. Vous n'obtiendrez pas forcément la même réponse. Et c'est voulu.

## Scène 2 · Un tirage au sort

À chaque étape, le modèle calcule une probabilité pour chaque token possible. Puis il en tire un au sort, parmi les plus probables. Après « Le ciel est », il écrira souvent « bleu », parfois « gris ». Un tirage différent au début, et toute la suite change.

## Scène 3 · La température

La température règle ce tirage. Basse, le modèle choisit presque toujours le token le plus probable : les réponses sont stables. Haute, les choix moins probables ont leur chance : plus de variété, mais aussi plus d'écarts. Le réglage se fait dans l'appel d'API, pas dans le prompt.

## Scène 4 · Variété ou stabilité

Le bon réglage dépend de la tâche. Pour un slogan ou des idées, on veut de la variété : une température plus haute. Pour extraire un montant ou classer un email, on veut la même réponse à chaque fois : une température basse. Attention : même à zéro, la répétabilité parfaite n'est pas toujours garantie.

## Scène 5 · Ce que ça change côté produit

Côté produit, l'aléatoire change la façon de tester. Un seul essai ne prouve rien : vos evals rejouent chaque cas plusieurs fois. Et l'aléatoire devient une fonctionnalité : proposer trois variantes, ou un bouton « autre suggestion ».

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Cette tâche demande-t-elle de la créativité ou de la constance ? Deux réponses différentes à la même question sont-elles acceptables ? Et combien de fois rejoue-t-on chaque cas de test ?

## Scène 7 · À retenir

À retenir : le modèle tire ses mots au sort parmi les plus probables. La température règle ce hasard : haute pour créer, basse pour extraire et classer. Prochaine capsule : les modèles qui raisonnent avant de répondre.
