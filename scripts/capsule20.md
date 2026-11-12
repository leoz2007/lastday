# Capsule 20 · Workflows et chaînes de prompts

Texte de la voix off (295 mots).

## Scène 1 · Accroche

Un seul prompt géant fait souvent moins bien que quatre petits prompts enchaînés. Découper une tâche, c'est rendre chaque étape simple, testable et réparable.

## Scène 2 · La chaîne de prompts

Prenez une réclamation client. Première étape : extraire les faits, le client, la commande, le problème. Deuxième étape : classer la demande. Troisième : rédiger une réponse. Quatrième : vérifier cette réponse avant l'envoi. Chaque étape a un seul travail, et sa sortie devient l'entrée de la suivante.

## Scène 3 · Un prompt et des tests par étape

Chaque étape a son propre prompt, court et précis. Et surtout, ses propres tests. Si la classification se trompe, vous le voyez tout de suite, à cet endroit précis. Avec un prompt unique, l'erreur se cache dans la masse, et on ne sait pas quoi corriger. Avec des étapes, vous en corrigez une sans casser les autres.

## Scène 4 · Workflow codé ou agent libre

Un workflow codé suit un chemin fixé à l'avance : toujours les mêmes étapes, dans le même ordre. C'est prévisible, et plus simple à tester. Un agent libre choisit lui-même ses étapes : il est plus souple, mais moins prévisible. Quand le chemin est connu, préférez le workflow.

## Scène 5 · Ce que ça change côté produit

Côté produit, les passages entre étapes deviennent des points de contrôle. On vérifie par exemple que l'extraction est complète, et que la catégorie existe bien. Ce sont des règles simples, écrites dans le code, pas confiées au modèle. En cas de doute, on s'arrête, on réessaie, ou on passe la main à un humain.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quelles étapes peut-on séparer clairement ? Comment teste-t-on chacune d'elles ? Et que fait-on quand un contrôle échoue entre deux étapes ?

## Scène 7 · À retenir

À retenir : découpez une tâche complexe en étapes simples, chacune avec son prompt et ses tests. Un chemin connu mérite un workflow, pas un agent. Prochaine capsule : les systèmes multi-agents, quand plusieurs agents travaillent ensemble.
