# Capsule 22 · Observabilité et traces

Texte de la voix off (256 mots).

## Scène 1 · Accroche

Quand un assistant se trompe, la première question est simple : qu'a-t-il vu, exactement ? Sans traces, impossible de répondre. On devine, et on corrige au hasard.

## Scène 2 · La trace

Une trace, c'est l'enregistrement de chaque appel au modèle. On y garde le prompt, le contexte fourni, la réponse, les outils appelés, la durée et le coût. C'est la boîte noire de votre assistant, un peu comme dans un avion.

## Scène 3 · Comprendre une erreur

Prenons une réponse fausse sur un délai de rétractation. On ouvre la trace. Le bon document n'était pas dans le contexte : c'est la recherche qui a échoué, pas le modèle. Sans trace, on aurait réécrit le prompt pour rien.

## Scène 4 · Les tableaux de bord

En regroupant les traces, on construit des tableaux de bord. Quatre courbes à suivre : la qualité, le coût, la latence et le taux d'échec. Si le coût double un mardi, vous voyez quand, et vous retrouvez les appels en cause.

## Scène 5 · Ce que ça change côté produit

Côté produit, attention : les traces contiennent souvent des données personnelles, comme des noms, des adresses, des numéros de contrat. Masquez ou anonymisez-les avant de les stocker, limitez qui peut les lire, et fixez une durée de conservation. Une trace utile n'a pas besoin d'un nom.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Que doit-on enregistrer à chaque appel ? Qui a le droit de lire les traces ? Et combien de temps les garde-t-on ?

## Scène 7 · À retenir

À retenir : tracez chaque appel, pour comprendre au lieu de deviner. Et protégez ces traces comme des données sensibles. Prochaine capsule : les retours utilisateurs, pour savoir ce que vos utilisateurs pensent vraiment.
