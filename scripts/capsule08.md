# Capsule 08 · Prompting, RAG ou fine-tuning

Texte de la voix off (287 mots).

## Scène 1 · Accroche

Quand un assistant répond mal, le réflexe est souvent de vouloir entraîner le modèle. C'est pourtant rarement le premier levier à actionner.

## Scène 2 · Levier un : le prompting

Premier levier : le prompting. Vous changez la consigne, le ton, le format, les exemples. C'est rapide, peu coûteux, et réversible en quelques minutes. Si le problème vient d'une consigne floue ou d'un format mal respecté, commencez toujours par là.

## Scène 3 · Levier deux : le RAG

Deuxième levier : le RAG. Il sert quand le modèle manque d'information : vos produits, vos procédures, des données qui changent souvent. Le modèle ne mémorise rien de nouveau : on lui fournit les bons passages à chaque question. Mettre à jour un document suffit pour mettre à jour la réponse.

## Scène 4 · Levier trois : le fine-tuning

Troisième levier : le fine-tuning. On réentraîne un modèle sur des centaines ou des milliers d'exemples, pour lui apprendre un style, un format ou une tâche très répétitive. C'est plus long, il faut des données de qualité, et chaque mise à jour demande un nouvel entraînement. Ce n'est pas le bon outil pour lui apprendre des faits qui changent.

## Scène 5 · Ce que ça change côté produit

Côté produit, retenez une règle simple. Un problème de comportement ? Le prompt. Un problème de connaissance ? Le RAG. Un style très constant, à grande échelle, que le prompt ne suffit pas à obtenir ? Là, le fine-tuning se discute. Et souvent, on combine les trois.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Le problème vient-il de la consigne, ou de l'information ? Les données changent-elles souvent ? Dispose-t-on d'exemples de qualité, en nombre suffisant, pour entraîner ?

## Scène 7 · À retenir

À retenir : d'abord le prompt, ensuite le RAG, et le fine-tuning en dernier recours, quand on a les données pour le faire. Prochaine capsule : la sécurité et la conformité, de la prompt injection à l'AI Act.
