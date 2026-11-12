# Capsule 58 · Le LLM hub

Texte de la voix off (298 mots).

## Scène 1 · Accroche

Vos agents de code ne devraient pas appeler un modèle en direct. Tout passe par une seule porte : le LLM hub, aussi appelé gateway. C'est le point d'entrée unique entre les agents et les modèles.

## Scène 2 · Le principe et des exemples à date

Le principe ressemble à un standard téléphonique : un seul numéro, puis on vous transfère vers le bon modèle, interne ou externe. Exemples à date : LiteLLM, Portkey, parmi d'autres. Le paysage évolue vite.

## Scène 3 · Clés virtuelles, quotas et limitation de débit

Première fonction : les clés virtuelles. Chaque équipe a la sienne, jamais la clé réelle du fournisseur. À chaque clé, un quota, par exemple un budget par mois. Et une limitation de débit, le rate limiting : un plafond de requêtes par minute, pour qu'un agent emballé ne bloque pas les autres.

## Scène 4 · Routage, bascule de secours, traduction et cache

Ensuite, le routage : chaque demande part vers le bon modèle, et bascule sur un modèle de secours si le premier tombe. C'est le fallback. Il traduit aussi les formats d'API d'un fournisseur vers un autre, et inversement. Enfin, il met les prompts en cache : déjà vus, ils coûtent moins cher.

## Scène 5 · Ce que ça change côté produit

Côté produit, c'est votre point de contrôle. C'est là qu'on branche la FinOps, le suivi des coûts par équipe. L'observabilité : qui appelle quel modèle. Et la DLP, la prévention des fuites de données : un prompt qui contient un secret ne sort pas.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quel quota et quel débit pour chaque équipe ? Vers quel modèle de secours basculer en cas de panne ? Et quelles règles de fuite de données appliquer aux prompts ?

## Scène 7 · À retenir

À retenir : le LLM hub est la porte unique entre vos agents et vos modèles. Clés, quotas, routage, secours, traduction et cache : tout se règle à un seul endroit. Prochaine capsule : contexte et outils, pour ouvrir votre système d'information à l'agent.
