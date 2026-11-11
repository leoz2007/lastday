# Capsule 39 · Vos données en langage naturel

Texte de la voix off (294 mots).

## Scène 1 · Accroche

Vous tapez « chiffre d'affaires par région ce trimestre », et un tableau s'affiche. Personne n'a écrit de requête. C'est le text-to-SQL : votre question devient une requête SQL, le langage des bases de données.

## Scène 2 · Le circuit

D'abord, l'utilisateur pose sa question. Le modèle écrit la requête, sans toucher aux données. Puis l'application l'exécute sur la base et affiche le résultat, en tableau ou en graphique. Le modèle rédige ; c'est l'application qui agit, et qui garde la main.

## Scène 3 · Décrire le schéma et le vocabulaire

Le modèle doit connaître le schéma : les tables, les colonnes, leurs liens. Et surtout votre vocabulaire métier. Qu'est-ce qu'un « client actif » ? Un achat dans l'année ? Une connexion ce mois-ci ? Si personne ne l'a défini, le modèle choisit à votre place.

## Scène 4 · Les risques

Le premier risque : une requête syntaxiquement juste, c'est-à-dire bien écrite, mais fausse sur le fond. Le chiffre a l'air sérieux, mais les avoirs ont été oubliés. Ajoutez les ambiguïtés, les droits d'accès, et les requêtes lourdes, qui ralentissent toute la base.

## Scène 5 · Ce que ça change côté produit

Côté produit, quatre parades. Un accès en lecture seule, avec les droits de l'utilisateur, pas ceux de l'application. Montrez la requête, ou son interprétation en clair : « ventes hors avoirs, depuis le début du trimestre ». Et une couche sémantique : des définitions validées, que le modèle réutilise au lieu d'inventer.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quels termes métier faut-il définir et faire valider ? Quels droits s'appliquent à chaque utilisateur ? Et quelles questions types, avec leurs résultats attendus, serviront d'evals, ces tests qui vérifient les réponses ?

## Scène 7 · À retenir

À retenir : le modèle écrit la requête, mais votre base et vos définitions disent la vérité. Lecture seule, droits appliqués, requête visible, et des evals pour vérifier. Prochaine capsule : les agents vocaux, quand l'assistant écoute et parle.
