# Capsule 62 · Observabilité des agents

Texte de la voix off (295 mots).

## Scène 1 · Accroche

Un agent de code peut échouer en silence. Par exemple, il tourne vingt minutes, enchaîne des dizaines d'appels, puis rend un résultat faux. Personne ne sait pourquoi. L'observabilité, c'est voir ce que fait l'agent, étape par étape.

## Scène 2 · Tracer les sessions de bout en bout

D'abord, tracez chaque session de bout en bout. Une trace, c'est le carnet de bord de l'agent : la demande, chaque appel au modèle, chaque appel d'outil, puis le résultat. Comme le suivi d'un colis. Des outils existent, à date, comme OpenTelemetry ou Langfuse ; le paysage évolue vite.

## Scène 3 · Latence, erreurs d'outils et boucles

Suivez ensuite trois signaux. La latence : combien de temps attend le développeur. Le taux d'erreur des appels d'outils, les tool calls : un outil qui échoue fait dérailler la tâche. Et le nombre de boucles par tâche : un agent qui relance dix fois le même test tourne en rond.

## Scène 4 · Journaliser les prompts, conformément au RGPD

Les prompts contiennent parfois des données personnelles. Journalisez-les en conformité avec le RGPD, le règlement européen sur la protection des données : une durée de conservation définie, des accès restreints, et une piste d'audit, qui dit qui a lu quoi. Sur les détails, le juridique tranche.

## Scène 5 · Ce que ça change côté produit

Côté produit, l'observabilité est une fonctionnalité, pas un bonus. Prévoyez des tableaux de bord par équipe. Des alertes, aussi : par exemple, au-delà de cinq boucles sur la même étape, l'agent s'arrête et prévient. Et reliez chaque trace à son coût.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Que faut-il tracer, et combien de temps le garder ? Qui peut lire les prompts journalisés ? Et à partir de combien de boucles l'agent doit-il s'arrêter ?

## Scène 7 · À retenir

À retenir : tracez chaque session, et suivez latence, erreurs d'outils et boucles. Journalisez les prompts avec une durée de conservation, des accès restreints et une piste d'audit. Prochaine capsule : la qualité et le cycle de développement.
