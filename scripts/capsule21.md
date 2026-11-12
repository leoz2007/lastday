# Capsule 21 · Multi-agents

Texte de la voix off (286 mots).

## Scène 1 · Accroche

Mettre plusieurs agents sur une tâche ne la rend pas forcément plus intelligente. Parfois, c'est juste plus cher, plus lent, et plus fragile. Avant d'en ajouter, demandez-vous ce que chacun apporte vraiment.

## Scène 2 · Les rôles des agents

Dans un système multi-agents, chaque agent a un rôle. Un agent planifie : il découpe la demande en sous-tâches. D'autres agents exécutent, chacun la sienne. Un dernier relit le résultat, et renvoie ce qui ne va pas. Par exemple, pour répondre à un appel d'offres : un plan, trois rédacteurs, un relecteur.

## Scène 3 · Quand c'est utile

C'est utile dans trois cas. Une tâche longue, qui déborderait le contexte d'un seul agent. Une tâche parallélisable : plusieurs recherches menées en même temps. Ou des expertises distinctes, chaque agent avec ses propres instructions et ses outils. Chaque agent garde alors un contexte court, centré sur sa sous-tâche.

## Scène 4 · Quand c'est inutile

Mais chaque agent ajoute des appels au modèle, donc du coût et de la latence. Les échanges entre agents ajoutent de la complexité. Et une erreur du planificateur se propage à tous les autres : elle est copiée, pas corrigée. Et quand le résultat est faux, il faut retrouver quel agent s'est trompé.

## Scène 5 · Ce que ça change côté produit

Côté produit, commencez simple. Un seul agent bien outillé, ou un workflow, règle déjà beaucoup de cas. Ajoutez un deuxième agent seulement quand vos evals montrent un vrai gain, qui justifie le coût en plus. Mesurez avant d'empiler.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Un seul agent suffirait-il ? Qui vérifie le travail des autres agents ? Et combien coûte une demande, une fois tous les appels additionnés ?

## Scène 7 · À retenir

À retenir : plusieurs agents, c'est utile pour des tâches longues, parallèles, ou très spécialisées. Sinon, commencez simple. Prochaine capsule : observabilité et traces, pour comprendre ce que fait vraiment votre système.
