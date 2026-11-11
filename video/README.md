# Capsules « GEN AI EN 2 MIN »

Capsules vidéo verticales (1080×1920, 30 fps) pour donner un vernis technique en IA générative à une PO fonctionnelle :

- saison 1 : capsules 02 à 10 (la capsule 01 existait déjà) ;
- saison 2 : capsules 11 à 28. Dans chaque module, `SERIES = (11, 28)` et `SERIES_LABEL = 'Saison 2'`. Le brief de rédaction commun est dans `video/BRIEF_S2.md`.
- saison 3 : capsules 29 à 38, sujets plus techniques (GraphRAG, inférence, RAG avancé, attention, entraînement, LoRA, données synthétiques, IA sur site, agents en production). `SERIES = (29, 38)`, brief dans `video/BRIEF_S3.md`.
- saison 4 : capsules 39 à 54, industrialisation (text-to-SQL, agents vocaux, context engineering, embeddings, extraction en masse, agents sur ordinateur, petits modèles, POC vers production, LLMOps, A/B testing, guardrails, red teaming, propriété intellectuelle, contrats, gouvernance, planification). `SERIES = (39, 54)`, brief dans `video/BRIEF_S4.md`.
- saison spéciale : capsules 55 à 65, déployer des agents de code IA « on premise » (souveraineté, modèles et inférence, harness, LLM hub, contexte et outils, sécurité, FinOps, observabilité, qualité, gouvernance, adoption). `SERIES = (55, 65)`, brief dans `video/BRIEF_SPE.md`. Par exception, les noms d'outils y sont cités, comme exemples à date.
- saison 5 : capsules 66 à 75, sujets avancés (Mixture of Experts, lois d'échelle, interprétabilité, calibration, bases vectorielles, évaluer un agent, reward hacking, spec-driven development, interopérabilité des agents, calcul confidentiel). `SERIES = (66, 75)`, brief dans `video/BRIEF_S5.md`.

| Fichier | Contenu |
|---|---|
| `out/capsuleNN_*.mp4` | vidéos finales |
| `scripts/capsuleNN.md` | texte de la voix off, scène par scène |
| `video/engine.py` | moteur commun : palette, polices, helpers d'animation, habillage, sous-titres, synthèse vocale ElevenLabs, rendu et encodage |
| `video/capsules/capsuleNN.py` | une capsule : script (7 scènes) et illustrations animées |
| `video/audio/capsuleNN.mp3` + `.json` | voix générée et alignement temporel par caractère (mis en cache) |
| `video/fonts/` | Montserrat Light, Medium et Bold (depuis `@fontsource/montserrat`, woff2 converti en TTF) |

## Régénérer une capsule

```bash
pip install skia-python numpy fonttools brotli   # sous Linux, skia a aussi besoin de libegl1
python3 video/render.py 04            # rend out/capsule04_*.mp4 (et réécrit scripts/capsule04.md)
python3 video/qa.py 04                # contrôles ffprobe + 5 images extraites du MP4 final
python3 video/preview.py 04           # planche d'aperçu sans appel API (alignement factice)
python3 video/render.py 04 --md       # compte les mots du script
python3 video/preview.py 04 0.55      # aperçu au milieu de chaque scène
```

- **La voix n'est jamais régénérée** si `video/audio/capsuleNN.mp3` et `.json` existent déjà. Le rendu ne coûte donc aucun crédit. Pour une nouvelle voix (par exemple après une modification du texte), supprimez ces deux fichiers et lancez le rendu avec `ELEVENLABS_API_KEY` dans l'environnement. Si le texte ne correspond plus à l'audio en cache, le moteur le signale et garde l'audio existant.
- Voix : « Julien - Friendly French Tech Explainer » (`VuE88ydpXAhBTNxFI7WF`), modèle `eleven_v4`, endpoint `text-to-speech/{voice}/with-timestamps`, sortie mp3 44,1 kHz 192 kbit/s.
- Calage : chaque scène démarre 0,15 s avant son premier mot, et chaque animation se déclenche sur le mot prononcé (`S.cue("mot")`). Les sous-titres viennent de l'alignement mot à mot. Il n'y a aucune déformation temporelle.
- Encodage : une vidéo par scène (frames skia en BGRA envoyées à ffmpeg avec `-pix_fmt bgra`), concaténation en `-c copy`, puis ajout de l'audio en `-c:v copy` (AAC 192k, `+faststart`). La vidéo dure la voix plus 1,5 s (0,5 s avant, 1 s après).

## Ce qui n'a pas pu être vérifié

- **`reference/render.py` n'existe pas** dans le dépôt, ni dans son historique. Le gabarit a donc été reconstruit d'après la description écrite (palette, polices, mise en page, éléments permanents). Il peut différer de la capsule 01 sur des détails : positions exactes, tailles, courbes d'animation, style de la barre de progression.
- **La voix n'a pas été écoutée.** La prononciation des sigles (LLM, RAG, MCP, JSON, API, DPO, RGPD, AI Act) et les intonations n'ont pas été contrôlées à l'oreille. Seul l'alignement renvoyé par l'API a été vérifié : le texte aligné est identique au texte envoyé.
- La concordance entre sous-titres et voix repose sur cet alignement. Il n'y a pas eu de transcription indépendante de l'audio.
- La documentation ElevenLabs n'était pas accessible depuis l'environnement (domaine bloqué). Le choix du modèle repose sur la liste `/v1/models` de l'API, où `eleven_v4` est disponible.
- Sur les images extraites, le rouge mesuré est d'environ (245, 71, 93) pour (248, 72, 94) attendu. L'écart vient de la conversion en yuv420p.
- Les exemples à l'écran (découpage en tokens, tarifs, scores, numéros de page) sont illustratifs et signalés comme tels quand c'est utile. Ce ne sont pas des mesures.
- Pour le RGPD et l'AI Act, les scripts restent sur des principes généraux. Ils ne remplacent pas un avis juridique.
- Saison 2 : les scènes ont été rédigées par plusieurs agents à partir du même brief, puis relues une à une sur planche d'aperçu avant la génération des voix. La lecture humaine des formulations reste recommandée.
- Les exemples à l'écran de la saison 2 (montants, dates, « art. 3 », noms fictifs pseudonymisés dans la capsule 22) sont illustratifs.
