# Capsule 15 · Mémoire et personnalisation

Texte de la voix off (288 mots).

## Scène 1 · Accroche

Un LLM ne se souvient de rien. Entre deux appels, il repart de zéro. La mémoire d'un assistant, c'est l'application qui la fabrique.

## Scène 2 · L'historique renvoyé

À chaque message, l'application renvoie toute la conversation au modèle. C'est ce qui donne l'impression qu'il suit le fil. Vous écrivez : « Mon vol est mardi. » Puis : « Décale-le d'un jour. » Le modèle comprend, parce que la première phrase lui est renvoyée avec la seconde.

## Scène 3 · Résumés et préférences

Mais l'historique grossit, et la fenêtre de contexte a une limite. Alors on résume les anciens échanges en quelques lignes. On peut aussi stocker des préférences : « répondez en anglais », « je suis végétarien ». Elles sont réinjectées dans le prompt à chaque nouvelle conversation, sans que vous ayez à les répéter.

## Scène 4 · Le RAG sur l'historique

Sur des mois d'échanges, on fait du RAG : on cherche dans l'historique les passages utiles à la question, et on ne réinjecte que ceux-là. Vous demandez : « Quel hôtel m'aviez-vous conseillé à Lyon ? » L'application retrouve l'échange concerné, et seulement lui.

## Scène 5 · Ce que ça change côté produit

Côté produit, la mémoire touche aux données personnelles. Il faut le consentement de l'utilisateur, et lui montrer ce qui est retenu. Il doit pouvoir corriger, désactiver, ou tout effacer : c'est le droit à l'oubli. Et l'effacement doit aussi toucher les résumés et les index de recherche.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Que faut-il vraiment retenir, et pendant combien de temps ? Où l'utilisateur voit-il et corrige-t-il ce qui est retenu ? Et comment garantir un effacement complet ?

## Scène 7 · À retenir

À retenir : le modèle n'a pas de mémoire, c'est l'application qui en construit une. Ce qu'elle retient doit rester visible, et effaçable. Prochaine capsule : trouver le bon cas d'usage, celui où l'IA générative apporte vraiment quelque chose.
