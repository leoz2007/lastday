# Capsule 24 · Maîtriser les coûts en production

Texte de la voix off (293 mots).

## Scène 1 · Accroche

Le même assistant, à qualité égale, peut coûter bien moins cher. Tout se joue dans quelques choix : quel modèle, quel contexte, et combien de fois on l'appelle.

## Scène 2 · Le bon modèle, un contexte court

Premier levier : choisir le modèle par tâche. Un petit modèle pour classer, un grand pour les cas difficiles. Deuxième levier : raccourcir les prompts et le contexte. Chaque token envoyé se paie, à chaque appel. Par exemple, envoyer trois extraits pertinents plutôt que tout le contrat.

## Scène 3 · Cache et longueur des réponses

Troisième levier : la mise en cache. Une question fréquente, comme les horaires d'ouverture, peut recevoir une réponse déjà calculée. Certains fournisseurs proposent aussi un cache de prompt : la partie fixe, répétée à chaque appel, est facturée moins cher. Quatrième levier : limiter la longueur des réponses, car la sortie coûte souvent plus cher que l'entrée.

## Scène 4 · Quotas et traitement par lots

Cinquième levier : des quotas par utilisateur. Un plafond d'appels par jour protège des abus et des boucles qui s'emballent. Sixième levier : le traitement par lots, quand le temps réel n'est pas nécessaire. Pour résumer les tickets de la veille, on regroupe les demandes et on les traite la nuit, souvent à moindre coût.

## Scène 5 · Ce que ça change côté produit

Côté produit, suivez le coût par utilisateur, pas seulement la facture globale. Souvent, une poignée d'usages pèse très lourd : c'est là qu'on agit en premier. Et prévoyez une alerte quand le budget du mois approche de sa limite.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quel coût par utilisateur votre modèle économique peut-il supporter ? Quelles demandes peuvent attendre un traitement par lots ? Et qui est alerté si la facture dérape ?

## Scène 7 · À retenir

À retenir : le coût se pilote, levier par levier. Mesurez-le par utilisateur, et agissez d'abord sur les usages qui pèsent le plus. Prochaine capsule : open source ou propriétaire, comment choisir son modèle.
