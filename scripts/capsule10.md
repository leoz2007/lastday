# Capsule 10 · Sorties structurées et intégration

Texte de la voix off (300 mots).

## Scène 1 · Accroche

Pour une application, une belle phrase ne sert à rien. Elle a besoin de champs, de valeurs, bref de données qu'elle peut traiter.

## Scène 2 · Les sorties structurées

D'où les sorties structurées. Au lieu d'un texte libre, on demande au modèle un JSON : un format simple, fait de champs et de valeurs. Par exemple, pour une réclamation : le motif, le niveau d'urgence, et le service concerné. L'application lit ces champs, et peut créer un ticket automatiquement.

## Scène 3 · Le schéma

Pour que ce soit fiable, on fournit un schéma. Il décrit chaque champ : son nom, son type, les valeurs autorisées. L'urgence, par exemple, ne peut être que basse, moyenne ou haute. Plusieurs fournisseurs proposent un mode qui force la réponse à respecter le schéma : on parle de contraindre la sortie. Mais l'application doit quand même vérifier ce qu'elle reçoit.

## Scène 4 · L'appel depuis l'application

Concrètement, appeler un LLM, c'est un appel d'API, comme pour n'importe quel service web. L'application envoie le system prompt, le message et le schéma. Elle reçoit la réponse, la valide, puis l'enregistre ou l'affiche. Et elle prévoit le cas d'erreur : délai dépassé, réponse invalide, nouvelle tentative.

## Scène 5 · Ce que ça change côté produit

Côté produit, le schéma devient un contrat d'interface entre le modèle et l'application. Il se spécifie avec le métier, comme un formulaire : quels champs, quelles valeurs, et que faire si une information manque. C'est là que votre regard fonctionnel compte le plus.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quels champs l'application attend-elle exactement ? Que fait-on si le modèle ne trouve pas une information ? Et qui est prévenu quand la réponse est invalide ?

## Scène 7 · À retenir

À retenir : le schéma est un contrat d'interface. On le spécifie, on le valide, et on gère les erreurs. C'était la dernière capsule de la série. Vous avez maintenant les bases pour cadrer un projet d'IA générative, et pour poser les bonnes questions.
