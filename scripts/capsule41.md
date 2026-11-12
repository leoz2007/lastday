# Capsule 41 · Context engineering

Texte de la voix off (298 mots).

## Scène 1 · Accroche

Le prompt que vous écrivez n'est souvent qu'une petite partie de ce que le modèle lit. À chaque appel, sa fenêtre de contexte se remplit de bien d'autres choses. Les concevoir, c'est le context engineering : l'ingénierie du contexte.

## Scène 2 · Ce qui entre dans la fenêtre

Qu'y a-t-il dans cette fenêtre ? Les instructions, la description des outils disponibles, la mémoire et un résumé de l'historique, les documents récupérés, quelques exemples, et l'état de la tâche en cours. Pour un assistant de service client : la politique de remboursement, l'outil de commande, et le dossier du client.

## Scène 3 · Ni trop peu, ni trop

Trop peu de contexte, et le modèle devine : il invente un délai de livraison qu'on ne lui a pas donné. Trop de contexte, et il se noie : l'information utile est perdue au milieu, et chaque appel coûte plus cher. Il faut donc ordonner, résumer, élaguer.

## Scène 4 · Pour un agent, étape par étape

Pour un agent, le contexte change à chaque étape. Il appelle un outil, reçoit un long résultat, puis un autre. Sans tri, la fenêtre se remplit vite. On garde l'essentiel : le résultat utile, un résumé des étapes passées, et l'objectif, toujours en tête.

## Scène 5 · Ce que ça change côté produit

Côté produit, traitez le contexte comme une spécification. Ce qui entre, dans quel ordre, sous quelle forme : écrivez-le, versionnez-le. Puis testez-le avec les evals, vos questions et leurs réponses attendues. Retirer un document, ou résumer l'historique, peut changer les réponses.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. De quoi le modèle a-t-il vraiment besoin, pour chaque tâche ? Que résume-t-on, et que retire-t-on, quand la conversation s'allonge ? Et quelles evals vérifient qu'un changement de contexte ne dégrade rien ?

## Scène 7 · À retenir

À retenir : le modèle ne sait que ce que vous mettez dans sa fenêtre. Choisissez, ordonnez, résumez, et testez ce contexte comme une spécification. Prochaine capsule : les embeddings au-delà du RAG, pour classer, regrouper et comparer.
