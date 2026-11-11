# Brief saison spéciale (capsules 55 à 65) : agents de code IA « on premise »

Thème : déployer des agents de code IA dans une entreprise sous contrainte de souveraineté. On parle du modèle, du serveur d'inférence, de l'agent (harness), de la gateway, des outils, de la sécurité, de la FinOps, de l'observabilité, de la qualité, de la gouvernance et de l'adoption. Le public reste une PO fonctionnelle senior, entourée d'équipes de développement et d'une équipe plateforme.

Applique **intégralement** `video/BRIEF_S2.md`, avec ces différences :

- `SERIES = (55, 65)` et `SERIES_LABEL = 'Saison spéciale'`.
- **Exception sur les noms** : les noms d'outils, de familles de modèles et de fournisseurs sont permis quand le sujet l'exige (vLLM, SGLang, Ollama, LiteLLM, Bedrock, Vertex, Azure, Claude Code, Qwen Coder…). Présente-les toujours comme des exemples « à date », et précise que le paysage évolue vite. À l'oral, cite-en peu (deux ou trois par capsule au plus) ; mets les autres à l'écran, sur des cartes ou des pastilles. N'affirme rien sur les performances relatives d'un produit.
- **Chiffres** : tout chiffre (nombre d'appels par tâche, tailles, prix, débits) est un ordre de grandeur ou un exemple illustratif, jamais un fait mesuré. Nombres en toutes lettres à l'oral.
- **Sigles** : chaque sigle est expliqué à sa première apparition (GPU, VRAM, TTFT, KV cache, MCP, DLP, SAST, CI, TCO, DORA…). Attention, il y a deux « DORA » différents : les métriques DORA (indicateurs de performance des équipes de livraison logicielle, en 63) et le règlement européen DORA (résilience opérationnelle numérique du secteur financier, en 64). Ne les confonds pas.
- **Droit** (AI Act, RGPD, licences) : principes généraux exacts, aucun article cité, et rappel que le juridique tranche.
- Ton : toujours pédagogique, avec une analogie ou un exemple concret par notion, et la conséquence pour le produit et le cadrage.
- Modèles de capsules à lire, en plus de ceux du brief S2 : `video/capsules/capsule30.py`, `capsule37.py`, `capsule38.py` et `capsule44.py`.
- La 65 conclut la saison : `ending(..., 'Vous savez *déployer* un agent de code', next_label='Saison terminée')`, sans « Prochaine capsule » ; `NEXT_CUE` est une sous-chaîne de la phrase de conclusion.

Titres pour les annonces de fin (`TITLE` d'en-tête : 22 caractères au plus, en capitales) :
55 · Le modèle de souveraineté
56 · Modèles et inférence
57 · Le harness, l'agent de code
58 · Le LLM hub
59 · Contexte et outils
60 · Sécurité des agents
61 · FinOps de l'IA de code
62 · Observabilité des agents
63 · Qualité et cycle de développement
64 · Gouvernance et conformité
65 · Exploitation et adoption
