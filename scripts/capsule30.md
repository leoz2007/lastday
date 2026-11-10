# Capsule 30 · L'inférence, de près

Texte de la voix off (297 mots).

## Scène 1 · Accroche

Un modèle ne lit pas et n'écrit pas au même rythme. Il lit tout votre texte d'un coup, puis écrit morceau par morceau. Ce détail explique les délais, et la facture.

## Scène 2 · Les tokens et la lecture du prompt

D'abord, le texte est découpé en tokens, des morceaux de mots. Vient ensuite la lecture du prompt, le prefill, ou préremplissage. Le modèle traite toute l'entrée d'un coup, en parallèle, comme un lecteur qui verrait la page entière. Mais une très longue entrée prend quand même du temps.

## Scène 3 · Le décodage et le cache KV

Puis vient la génération, ou décodage. Le modèle produit un token, puis le suivant, puis le suivant. Chacun dépend de ceux d'avant : impossible de les calculer en parallèle. Pour aller plus vite, il garde en mémoire ses calculs déjà faits : c'est le cache KV. Sans lui, chaque token recalculerait tout.

## Scène 4 · Deux mesures : premier token et débit

D'où deux mesures : le délai avant le premier token, puis le débit, en tokens par seconde. Une longue entrée allonge surtout le délai initial : pour résumer cent pages, l'attente est au début. Une longue sortie allonge le temps total : pour un long courrier, l'attente est dans l'écriture.

## Scène 5 · Ce que ça change côté produit

Côté produit, la sortie est en général facturée plus cher que l'entrée. Une raison : l'entrée est lue en bloc, alors que chaque token de sortie demande sa propre étape de calcul. Deux réflexes : afficher la réponse au fil de l'eau, et demander des réponses courtes.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quel délai avant le premier mot l'utilisateur accepte-t-il ? Les réponses doivent-elles être longues ? Et la réponse peut-elle s'afficher au fil de l'eau ?

## Scène 7 · À retenir

À retenir : le modèle lit l'entrée d'un coup, puis écrit token par token. L'entrée pèse surtout sur le délai initial, la sortie sur le temps total. Prochaine capsule : optimiser l'inférence, pour répondre plus vite et moins cher.
