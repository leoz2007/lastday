# Capsule 29 · Knowledge graph et GraphRAG

Texte de la voix off (298 mots).

## Scène 1 · Accroche

Un RAG classique retrouve des passages qui se ressemblent. Il ne sait pas suivre un lien d'un document à l'autre. C'est ce que permet un graphe de connaissances.

## Scène 2 · Des entités et des relations

Un graphe de connaissances, ou knowledge graph, relie des entités par des relations typées. Des entités : un client, un contrat, un produit, un fournisseur. Des relations : le client a signé le contrat, qui couvre le produit, qui dépend du fournisseur. Chaque lien a un sens précis, qu'on peut suivre.

## Scène 3 · Extraire le graphe des documents

Ce graphe peut être extrait de vos documents par un LLM. Il repère les entités, puis propose les relations. La phrase « ce client a signé le contrat de maintenance » donne deux entités et un lien. Mais l'extraction se trompe parfois : un nom mal reconnu, un lien oublié. Elle se vérifie.

## Scène 4 · GraphRAG : suivre les liens

GraphRAG combine recherche dans le graphe et génération. Question : quels clients sont touchés si ce fournisseur fait défaut ? Le système part du fournisseur, suit les liens vers ses produits, les contrats, puis les clients, et transmet ces faits au modèle, qui répond. Un RAG vectoriel, qui cherche par proximité de sens, ramènerait seulement des extraits semblables.

## Scène 5 · Ce que ça change côté produit

Côté produit, réservez le graphe aux questions qui suivent des liens : dépendances, impacts. Pour retrouver une clause, un RAG classique suffit souvent. Prévoyez les coûts : construire le graphe, le tenir à jour, contrôler l'extraction. Et choisissez entités et relations avec le métier.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Vos questions suivent-elles des liens ? Quelles entités et relations comptent pour le métier ? Et qui met le graphe à jour quand les documents changent ?

## Scène 7 · À retenir

À retenir : un graphe de connaissances relie des entités par des relations typées. GraphRAG suit ces liens pour répondre aux questions qui croisent plusieurs documents. Prochaine capsule : l'inférence, de près.
