# Capsule 19 · Gérer l'échec

Texte de la voix off (274 mots).

## Scène 1 · Accroche

Votre assistant va échouer. Pas peut-être : forcément. La vraie question, c'est ce que vit l'utilisateur à ce moment-là, et comment il s'en sort.

## Scène 2 · Les quatre cas d'échec

Il y a quatre grands cas. Le modèle ne sait pas. Il se trompe, avec aplomb. Il refuse de répondre. Ou l'API, le service qui fait tourner le modèle, ne répond plus du tout. Chaque cas mérite sa propre réponse, pas un message d'erreur générique.

## Scène 3 · Messages honnêtes, repli et escalade

D'abord, des messages honnêtes. « Je n'ai pas trouvé cette information dans vos documents » vaut mieux qu'une réponse inventée. Ensuite, un repli : reformuler, consulter l'aide, ou parler à un conseiller. Et l'escalade vers un humain transmet la conversation, pour ne pas tout réexpliquer.

## Scène 4 · Tentatives limitées et mode dégradé

Quand l'API ne répond pas, on réessaie, mais avec une limite : par exemple trois tentatives, de plus en plus espacées. Au-delà, on bascule en mode dégradé : une réponse plus simple, une mise en file d'attente, ou le formulaire classique. Le service rend moins, mais il ne s'arrête pas.

## Scène 5 · Ce que ça change côté produit

Côté produit, l'échec se conçoit comme un parcours, avec ses écrans et ses textes. Dessinez-le dans vos maquettes, au même titre que le cas nominal, celui où tout va bien. Puis suivez-le : taux d'escalade, abandons, réponses de repli.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Que dit l'assistant quand il ne sait pas ? Vers qui escalade-t-on, et avec quel contexte ? Et que reste-t-il du service si l'API tombe ?

## Scène 7 · À retenir

À retenir : l'échec n'est pas une exception, c'est un parcours à concevoir. Messages honnêtes, repli, escalade et mode dégradé : prévoyez-les dès le départ. Prochaine capsule : workflows et chaînes de prompts, pour découper une tâche en étapes fiables.
