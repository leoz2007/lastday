# Capsule 59 · Contexte et outils

Texte de la voix off (299 mots).

## Scène 1 · Accroche

Un agent de code brillant, mais sans accès à votre système d'information, code à l'aveugle. Il ne connaît ni vos tickets, ni votre architecture, ni vos API internes. Il faut lui ouvrir des portes, une par une.

## Scène 2 · Des serveurs MCP internes

Ces portes, ce sont souvent des serveurs MCP internes. Rappel : MCP est un standard pour brancher des outils sur un modèle, comme une prise universelle. Un serveur pour Git, un pour les tickets, un pour la documentation, un pour la CMDB, le référentiel des composants du système d'information, et d'autres pour vos API internes.

## Scène 3 · Recherche et RAG sur le code et la documentation

Ensuite, la recherche. Le code et la documentation d'architecture sont trop grandes pour tout donner au modèle. On indexe, puis on retrouve les passages utiles : c'est le RAG, la génération augmentée par recherche. Exemple : l'agent retrouve la règle de nommage des services avant d'en créer un.

## Scène 4 · Un miroir de paquets plutôt qu'Internet

Puis les paquets, ces bibliothèques que le code télécharge. L'agent ne doit pas sortir librement sur Internet. Il passe par un miroir interne, une copie contrôlée des dépôts publics, comme Artifactory ou Nexus, exemples à date. Seuls les paquets validés y entrent.

## Scène 5 · Ce que ça change côté produit

Côté produit, une règle : chaque accès suit les droits du développeur. L'agent agit au nom de quelqu'un, jamais avec un super compte. Si Julie ne voit pas les tickets de la paie, son agent non plus. Et chaque connecteur a un propriétaire, qui le maintient.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quels systèmes l'agent doit-il lire, et lesquels modifier ? Quelle documentation est assez fiable pour être indexée ? Et comment les droits du développeur passent-ils à l'agent ?

## Scène 7 · À retenir

À retenir : un agent n'est utile que s'il voit votre système d'information. Des serveurs MCP, une recherche sur le code, un miroir de paquets, toujours avec les droits du développeur. Prochaine capsule : la sécurité des agents.
