# Capsule 11 · Hallucinations

Texte de la voix off (299 mots).

## Scène 1 · Accroche

Un modèle de langage peut donner une réponse fausse, avec un aplomb parfait. Et il ne sait pas qu'il se trompe.

## Scène 2 · Pourquoi il invente

Pourquoi ? Un LLM ne consulte pas une base de faits. Il prédit, mot après mot, la suite la plus plausible. Demandez-lui la date de naissance d'un inconnu : il peut produire une date crédible, au bon format. Plausible ne veut pas dire vrai. On appelle ça une hallucination.

## Scène 3 · Les situations à risque

Le risque grimpe dans trois situations. Une question très précise : un chiffre, une date, une référence. Un sujet rare, peu présent dans ses données d'entraînement. Ou une information récente, postérieure à son entraînement. Exemple classique : la citation d'un article de loi, avec un numéro qui n'existe pas.

## Scène 4 · Les parades

Plusieurs parades existent. Fournir des sources : avec le RAG, le modèle répond à partir de vos documents. Autoriser le doute, avec une consigne claire : si l'information manque, dites que vous ne savez pas. Exiger des citations, pour vérifier chaque affirmation. Et ajouter une vérification automatique, qui contrôle que la réponse s'appuie sur les sources.

## Scène 5 · Ce que ça change côté produit

Côté produit, on ne supprime pas le risque : on le réduit, et on le mesure. Vos evals comptent les réponses inventées sur des cas réels. L'interface affiche les sources et rend le doute acceptable : un « je ne sais pas » vaut mieux qu'une erreur sûre d'elle.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Que coûte une réponse fausse dans ce cas d'usage ? Sur quelles sources le modèle doit-il s'appuyer ? Et que fait l'assistant quand il ne trouve pas la réponse ?

## Scène 7 · À retenir

À retenir : un LLM prédit du texte plausible, il ne vérifie pas. Les sources, les citations et les evals réduisent le risque. Prochaine capsule : la température, ou pourquoi la même question ne donne pas toujours la même réponse.
