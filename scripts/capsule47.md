# Capsule 47 · LLMOps et versioning

Texte de la voix off (300 mots).

## Scène 1 · Accroche

Votre assistant a changé de comportement, et personne n'a touché au code. Pourtant, un ingrédient a bougé : un prompt, un document, ou le modèle lui-même. Bienvenue dans le LLMOps, l'art d'exploiter des modèles de langage en production.

## Scène 2 · Les ingrédients d'un assistant

Un assistant dépend de plusieurs ingrédients : le prompt, le modèle et sa version, les documents qu'il consulte, les outils qu'il appelle, et des paramètres, comme la température, qui règle la part de hasard. Chacun évolue de son côté. Par exemple, une mise à jour des documents suffit à changer une réponse sur les tarifs.

## Scène 3 · Versionner ensemble

La parade : versionner ces ingrédients ensemble, comme une recette numérotée. Version douze : tel prompt, tel modèle, tels documents, tels outils. Avec chaque réponse, on enregistre ce numéro de version. Si un client conteste une réponse, on sait quelle combinaison l'a produite, et on peut la rejouer.

## Scène 4 · Evals, déploiement progressif, retour arrière

Chaque changement passe d'abord par les evals, des tests automatiques sur des cas représentatifs. S'ils sont bons, on déploie progressivement : une petite part du trafic, puis davantage si tout va bien. Et si la qualité baisse, on revient en arrière, vers la version précédente.

## Scène 5 · Ce que ça change côté produit

Côté produit, tenez un registre des versions : la date, le motif, le résultat des evals. Surveillez votre fournisseur : il peut faire évoluer un modèle, ou le retirer. Prévoyez la migration comme un changement à part entière, avec ses evals et son calendrier.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Qu'est-ce qui est versionné, et qui peut le modifier ? Quelles evals bloquent un déploiement ? Et que fait-on le jour où le modèle est retiré ?

## Scène 7 · À retenir

À retenir : un assistant, c'est une combinaison d'ingrédients, versionnés ensemble. Chaque changement passe par les evals, se déploie progressivement, et peut revenir en arrière. Prochaine capsule : l'A/B testing, pour comparer deux versions sur de vrais utilisateurs.
