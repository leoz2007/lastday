# Capsule 02 · Tokens et fenêtre de contexte

Texte de la voix off (300 mots).

## Scène 1 · Accroche

Un modèle de langage ne lit pas des mots. Il lit des tokens. Et chaque token se paie.

## Scène 2 · Le token

Un token, c'est un morceau de texte : un mot court, une syllabe, parfois un signe. Le mot « chat » tient en un seul token. Un mot long comme « anticonstitutionnellement » est découpé en plusieurs morceaux. Les tokens sont aussi l'unité de facturation : on paie ce qu'on envoie au modèle, et ce qu'il répond. La réponse coûte souvent plus cher.

## Scène 3 · La fenêtre de contexte

La fenêtre de contexte, c'est la mémoire de travail du modèle pour un échange. La consigne, l'historique, les documents et la réponse doivent y tenir ensemble. Ce qui dépasse est tronqué ou refusé. Le modèle ne se souvient de rien entre deux appels : l'application lui renvoie, à chaque fois, ce dont il a besoin.

## Scène 4 · Pourquoi ne pas tout envoyer

Pourquoi ne pas tout envoyer ? D'abord, même une grande fenêtre a une limite. Ensuite, chaque token envoyé se paie et rallonge le temps de réponse. Enfin, noyé dans un long contexte, le modèle peut rater l'information utile. Imaginez cent pages de contrat pour une seule question : mieux vaut lui donner les trois paragraphes qui comptent.

## Scène 5 · Ce que ça change côté produit

Côté produit, le token devient une donnée de conception. Il pèse sur le coût par utilisateur, le temps de réponse, et ce que l'assistant garde d'une longue conversation. Il faut choisir quoi résumer, quoi oublier, et quoi aller chercher.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quel volume de texte entre et sort à chaque appel ? Combien d'appels par jour, pour combien d'utilisateurs ? Que fait-on quand un document dépasse la fenêtre ?

## Scène 7 · À retenir

À retenir : le token est l'unité de coût et de limite. La fenêtre de contexte est une mémoire de travail, pas une archive. Prochaine capsule : écrire un prompt comme une vraie spécification fonctionnelle.
