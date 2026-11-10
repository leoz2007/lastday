# Capsule 04 · RAG et embeddings

Texte de la voix off (286 mots).

## Scène 1 · Accroche

Un LLM ne connaît pas vos clients. Il ne connaît ni vos contrats, ni vos procédures. Le RAG sert justement à lui donner les bons documents, au bon moment.

## Scène 2 · Étape un : découper

Première étape : on découpe les documents du client en petits morceaux de quelques paragraphes. On les appelle des chunks. Chaque morceau garde sa source : le nom du document et la page. Par exemple, un guide de deux cents pages peut devenir plusieurs centaines de passages.

## Scène 3 · Étape deux : les embeddings

Deuxième étape : chaque passage est transformé en embedding. C'est une liste de nombres qui représente le sens du texte. Deux passages qui parlent de la même chose ont des embeddings proches, même avec des mots différents. « Résilier mon contrat » et « mettre fin à mon abonnement » se retrouvent côte à côte.

## Scène 4 · Étape trois : retrouver et citer

Troisième étape : quand l'utilisateur pose une question, on la transforme elle aussi en embedding. La base vectorielle retrouve les passages les plus proches. On les envoie au modèle avec la question, et on lui demande de répondre uniquement à partir de ces passages, en citant ses sources.

## Scène 5 · Ce que ça change côté produit

Côté produit, la qualité dépend d'abord des documents. Des sources obsolètes ou contradictoires donnent de mauvaises réponses, même avec un excellent modèle. Les citations, elles, permettent à l'utilisateur de vérifier, et à vous de comprendre une erreur.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quelles sources sont fiables, et qui les met à jour ? Qui a le droit de voir quel document ? Que doit répondre l'assistant quand rien de pertinent n'est trouvé ?

## Scène 7 · À retenir

À retenir : le RAG, c'est découper, retrouver, puis répondre en citant. Le modèle ne sait que ce qu'on lui montre. Prochaine capsule : passer d'un chatbot qui parle à un agent qui agit.
