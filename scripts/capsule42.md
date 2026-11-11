# Capsule 42 · Les embeddings au-delà du RAG

Texte de la voix off (299 mots).

## Scène 1 · Accroche

Les embeddings ne servent pas qu'à chercher des documents pour un RAG. Ils savent aussi classer, regrouper, repérer des doublons, souvent pour bien moins cher qu'un appel à un modèle de langage.

## Scène 2 · Rappel : un embedding

Petit rappel. Un embedding est une liste de nombres qui représente le sens d'un texte. Deux textes au sens proche obtiennent des listes proches. « Mon colis n'est pas arrivé » et « livraison jamais reçue » se retrouvent côte à côte, sans mot commun.

## Scène 3 · Classer et regrouper

Premier usage : classer. Un nouveau ticket est comparé à des exemples déjà étiquetés, et prend l'étiquette des plus proches. Deuxième usage : regrouper. Des centaines de retours clients forment des grappes, c'est le clustering : chaque grappe révèle un thème, comme les retards ou l'application qui plante.

## Scène 4 · Doublons, recommandation, inhabituel

Troisième usage : les doublons. Deux fiches produit presque identiques sont très proches : on les signale. Quatrième : recommander des contenus proches de ce qu'un utilisateur a lu. Cinquième : repérer l'inhabituel, un message loin de tout ce qu'on voit d'ordinaire, comme une fraude ou un nouveau problème.

## Scène 5 · Ce que ça change côté produit

Côté produit, c'est souvent bien moins cher qu'un appel au modèle pour chaque élément : on calcule l'embedding une fois, puis on compare. Mais « proche » n'est pas toujours votre sens métier. « Résilier » et « s'abonner » parlent du même sujet, et peuvent sembler proches, alors que l'intention est opposée.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Sur quels exemples étiquetés valide-t-on la proximité ? Quel seuil décide qu'on parle de doublon, ou d'inhabituel ? Et qui relit les cas proches du seuil ?

## Scène 7 · À retenir

À retenir : un embedding mesure une proximité de sens, vite et à faible coût. Validez-la sur vos exemples, et choisissez vos seuils avant de lui faire confiance. Prochaine capsule : l'extraction en masse, pour traiter des milliers de documents.
