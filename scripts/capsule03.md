# Capsule 03 · Prompting et system prompt

Texte de la voix off (290 mots).

## Scène 1 · Accroche

Un prompt n'est pas une question posée à une machine. C'est une spécification fonctionnelle. Et comme toute spec, elle se relit, se discute et se valide.

## Scène 2 · System prompt et message utilisateur

Il y a deux niveaux. Le system prompt, écrit par l'équipe produit, fixe le rôle, le ton et les règles, pour toutes les conversations. Le message utilisateur, lui, change à chaque échange. Par exemple : « Tu es l'assistant du service client. Tu réponds en trois phrases maximum. »

## Scène 3 · L'anatomie d'un bon prompt

Un bon prompt ressemble à une user story bien écrite. Un contexte : qui est l'utilisateur, quel est le métier. Une tâche précise, avec un seul objectif. Des contraintes : la longueur, le ton, ce qu'il ne faut jamais faire. Et le format de sortie attendu. Sans ces éléments, le modèle comble les trous avec des suppositions.

## Scène 4 · Exemples et cas limites

Le levier le plus efficace, c'est souvent l'exemple. Montrez au modèle deux ou trois réponses modèles : il en reprend le style et la structure. Pensez aussi aux cas limites. Que répondre si la question sort du périmètre ? Si vous ne l'écrivez pas, le modèle improvisera.

## Scène 5 · Ce que ça change côté produit

Côté produit, le system prompt devient un livrable. Il a un responsable, il se versionne, se relit et se teste, comme du code. Une phrase modifiée peut changer le comportement de tout l'assistant. Chaque changement mérite donc une recette.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Qui rédige et valide le system prompt ? Quels sont les sujets interdits, et que répond-on dans ce cas ? Comment teste-t-on une nouvelle version avant de la déployer ?

## Scène 7 · À retenir

À retenir : le prompt est une spécification. Contexte, tâche, contraintes, format et exemples. Et le system prompt se gère comme un livrable. Prochaine capsule : brancher un LLM sur les données du client, avec le RAG.
