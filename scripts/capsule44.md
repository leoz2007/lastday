# Capsule 44 · Agents qui utilisent un ordinateur

Texte de la voix off (284 mots).

## Scène 1 · Accroche

Certains agents utilisent un ordinateur comme vous : ils regardent l'écran, puis cliquent et tapent au clavier. C'est utile quand le logiciel n'a pas d'API, c'est-à-dire pas de porte d'entrée prévue pour d'autres programmes.

## Scène 2 · Une boucle : voir, décider, agir

Le principe est une boucle. L'agent reçoit une capture d'écran. Le modèle l'analyse et choisit une action : cliquer, saisir un texte, faire défiler. Puis une nouvelle capture montre le résultat. Exemple : ressaisir des commandes dans un vieux logiciel de gestion.

## Scène 3 · Plus lent, plus fragile, plus cher

Mais c'est plus lent, plus fragile et plus cher qu'une intégration classique. Là où une API répond en une requête, l'agent enchaîne parfois des dizaines de gestes, chacun avec une capture et un appel au modèle. Et un bouton déplacé ou une fenêtre inattendue suffisent à le perdre.

## Scène 4 · Les risques

Les risques sont réels. Une action involontaire : supprimer au lieu d'archiver. Une injection : un texte malveillant, affiché à l'écran, donne des ordres à l'agent, comme « envoyez ce fichier à cette adresse ». Et l'agent agit avec tous les accès du compte qu'il utilise.

## Scène 5 · Ce que ça change côté produit

Côté produit, posez des garde-fous. Un environnement isolé, séparé de vos systèmes. Des comptes dédiés, aux droits minimaux. Une validation humaine avant toute action sensible, comme payer ou envoyer. Des traces de chaque action, pour comprendre après coup. Et quand une API existe, préférez-la.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Existe-t-il une API, même partielle, pour ce logiciel ? Quelles actions exigent une validation humaine ? Et de quels droits minimaux l'agent a-t-il besoin ?

## Scène 7 · À retenir

À retenir : un agent qui utilise un ordinateur ouvre les logiciels sans API, mais il reste lent, fragile et exposé. Isolez-le, limitez ses droits, faites valider les actions sensibles. Prochaine capsule : les petits modèles spécialisés, rapides et économes.
