# Capsule 73 · Spec-driven development

Texte de la voix off (298 mots).

## Scène 1 · Accroche

Avec un agent de code, la meilleure instruction n'est pas un message. C'est un document. Le spec-driven development, ou développement piloté par la spécification, fait travailler l'agent à partir d'une spécification écrite, plutôt que de demandes au fil de l'eau.

## Scène 2 · La spécification

Tout part de la spécification, la spec. Elle dit le quoi et le pourquoi : le besoin, les utilisateurs, les règles. Elle fixe surtout les critères d'acceptation, les conditions vérifiables d'une fonctionnalité terminée. Par exemple : un client peut annuler sa commande tant qu'elle n'est pas expédiée.

## Scène 3 · L'enchaînement des étapes

Vient ensuite le plan technique, qui décrit le comment : l'architecture, les données, les choix. Il est découpé en petites tâches. L'agent les implémente une par une, puis on vérifie le résultat contre les critères. Entre chaque étape, un humain valide avant de continuer.

## Scène 4 · Une spec versionnée

La spécification est versionnée avec le code, dans le même dépôt. Elle devient la référence : quand une question se pose, on relit la spec, pas l'historique d'une conversation. Un nouvel arrivant, humain ou agent, sait d'où vient chaque choix.

## Scène 5 · Ce que ça change côté produit

Côté produit, la PO est au centre : la qualité de la spec conditionne la qualité du code. Mais attention aux limites. Une spec trop vague produit du code plausible, mais faux. Et une spec figée vieillit : quand le besoin change, mettez-la à jour d'abord, puis laissez l'agent suivre.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Nos critères d'acceptation sont-ils vraiment vérifiables ? Qui valide le plan et les tâches avant que l'agent code ? Et qui tient la spec à jour quand le besoin change ?

## Scène 7 · À retenir

À retenir : avec un agent de code, la spécification guide le travail, étape par étape. Précise et tenue à jour, elle conditionne la qualité du code. Prochaine capsule : l'interopérabilité des agents, quand des agents de systèmes différents travaillent ensemble.
