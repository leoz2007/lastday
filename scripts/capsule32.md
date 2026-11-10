# Capsule 32 · Le RAG avancé

Texte de la voix off (298 mots).

## Scène 1 · Accroche

Un RAG, qui cherche des documents avant de répondre, brille en démonstration, puis plafonne en production. Souvent, le modèle n'y est pour rien : c'est la recherche qui lui donne les mauvais passages.

## Scène 2 · Pourquoi un RAG naïf plafonne

Trois causes reviennent souvent. Le découpage coupe une règle en deux. La question est mal formulée, comme « et pour les pros ? », sans contexte. Ou des passages proches du sujet, mais inutiles, prennent la place des bons : on demande les délais de résiliation, on obtient les conditions d'abonnement.

## Scène 3 · Recherche hybride et reranking

Première réponse : la recherche hybride. Les mots clés retrouvent les références exactes, comme un numéro de contrat. Les vecteurs, qui comparent le sens, relient « arrêter mon abonnement » à « résiliation ». On combine les deux. Puis le reranking : un second modèle relit les meilleurs candidats, les reclasse, et garde les plus pertinents.

## Scène 4 · Réécrire la question, mieux découper

Deuxième réponse : réécrire la question, ou la décomposer. « Comparez les offres A et B » devient deux recherches. Troisième : découper par section, avec titres et métadonnées, comme la date, le produit ou les droits d'accès. On filtre alors les documents en vigueur, que l'utilisateur a le droit de voir.

## Scène 5 · Ce que ça change côté produit

Côté produit, mesurez la recherche séparément de la réponse. D'abord : les bons passages sont-ils dans les premiers résultats ? Ensuite seulement : la réponse est-elle juste ? Sinon, vous retouchez le prompt alors que le problème vient de la recherche.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Vos utilisateurs cherchent-ils des références exactes, du sens, ou les deux ? Quelles métadonnées faut-il, notamment pour les droits d'accès ? Et comment mesure-t-on la recherche seule ?

## Scène 7 · À retenir

À retenir : un bon RAG, c'est d'abord une bonne recherche. Hybride, reclassée, filtrée, et mesurée à part de la réponse. Prochaine capsule : les transformers et l'attention, au cœur des modèles.
