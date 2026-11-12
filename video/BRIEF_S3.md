# Brief saison 3 (capsules 29 à 38)

Applique **intégralement** `video/BRIEF_S2.md`, avec ces différences :

- `SERIES = (29, 38)` et `SERIES_LABEL = 'Saison 3'`.
- Les sujets sont plus techniques. Vise l'intuition juste, pas la formule : chaque notion est expliquée par une image ou une analogie concrète, puis reliée à une conséquence produit. Aucune équation.
- L'exactitude prime. Pas de chiffre présenté comme un fait, pas de nom de modèle, de produit ou de fournisseur. Pas d'affirmation qui dépend d'une version. En cas de doute, formule plus prudemment (« souvent », « en général »).
- Les termes anglais usuels (prefill, reranking, LoRA, quantification…) sont expliqués à leur première apparition.
- Modèles de référence à lire : `video/capsules/capsule13.py` (raisonnement), `video/capsules/capsule20.py` (workflows) et `video/capsules/capsule24.py` (coûts), en plus de ceux du brief S2.
- La 38 conclut la saison 3 : `ending(..., 'Vous maîtrisez les *coulisses*', next_label='Saison terminée')`, sans « Prochaine capsule » ; `NEXT_CUE` est une sous-chaîne de la phrase de conclusion.

Titres pour les annonces de fin :
29 · Knowledge graph et GraphRAG
30 · L'inférence, de près
31 · Optimiser l'inférence
32 · Le RAG avancé
33 · Transformers et attention
34 · Comment un modèle est entraîné
35 · Fine-tuning efficace
36 · Données synthétiques
37 · IA sur site et en périphérie
38 · Agents en production
