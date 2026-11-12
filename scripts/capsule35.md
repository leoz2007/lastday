# Capsule 35 · Fine-tuning efficace (LoRA)

Texte de la voix off (299 mots).

## Scène 1 · Accroche

Pour spécialiser un modèle, inutile de le réentraîner en entier. On peut le figer, et n'entraîner qu'une petite pièce ajoutée.

## Scène 2 · Le fine-tuning complet

Le fine-tuning, ou ajustement fin, consiste à poursuivre l'entraînement d'un modèle sur vos exemples. En version complète, on modifie tous ses paramètres, ces réglages internes. C'est lourd : beaucoup de calcul, et une copie entière du modèle à stocker pour chaque variante.

## Scène 3 · LoRA : geler et ajouter

LoRA, une méthode d'adaptation légère, et les méthodes proches font autrement. Le modèle est gelé : on entraîne seulement de petites pièces ajoutées, appelées adaptateurs. Un adaptateur pèse une fraction du modèle : il se stocke et s'échange facilement. On en garde un par client ou par tâche, sur le même modèle de base.

## Scène 4 · Ce que ça apprend, ou pas

Ce que ça apprend bien : un style, un format de sortie, un vocabulaire métier, une tâche répétitive. Par exemple, rédiger des comptes rendus de sinistre toujours structurés pareil. Ce que ça apprend mal : les faits qui changent, comme des tarifs ou un stock. Ça, c'est le rôle du RAG, pas du fine-tuning.

## Scène 5 · Ce que ça change côté produit

Côté produit, tout repose sur les données : des exemples de qualité, représentatifs, relus par le métier. Deux risques : le surapprentissage, quand le modèle récite ses exemples au lieu de généraliser, et la perte de capacités générales. Mesurez-les avec vos evals, avant et après.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Le besoin porte-t-il sur la forme, ou sur des faits qui changent ? Avez-vous des exemples relus et représentatifs ? Et le modèle visé le permet-il : poids ouverts, c'est-à-dire téléchargeables, ou offre de fine-tuning du fournisseur ?

## Scène 7 · À retenir

À retenir : LoRA gèle le modèle et entraîne une petite pièce ajoutée, légère et échangeable. Idéal pour le style et le format. Pour les faits, préférez le RAG. Prochaine capsule : les données synthétiques, quand un modèle génère vos exemples.
