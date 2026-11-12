# Capsule 56 · Modèles et inférence

Texte de la voix off (296 mots).

## Scène 1 · Accroche

Pour un agent de code, le meilleur modèle n'est pas celui qui gagne les classements publics. C'est celui qui appelle ses outils sans se tromper, des dizaines de fois.

## Scène 2 · L'appel d'outils et les familles de modèles

L'appel d'outils, en anglais tool calling, c'est la capacité du modèle à demander une action précise, avec les bons paramètres : lire un fichier, lancer les tests. Testez-le sur vos propres tâches. Les familles à suivre changent chaque trimestre : à date, par exemple Qwen Coder.

## Scène 3 · Le serveur d'inférence

Le modèle a besoin d'un serveur d'inférence : le logiciel qui le fait tourner et répond aux requêtes. En production, partagé par des équipes, on prend par exemple vLLM, à date. Pour essayer sur un poste local, Ollama suffit. Restaurant d'un côté, cuisine familiale de l'autre.

## Scène 4 · Dimensionner les GPU

Pour dimensionner les GPU, ces processeurs graphiques, regardez quatre facteurs. Leur mémoire, la VRAM. La taille du contexte : le KV cache, où le modèle garde ce qu'il a déjà lu, grossit vite quand l'agent accumule les fichiers. Le nombre d'utilisateurs simultanés. Et la quantification, qui compresse le modèle.

## Scène 5 · Ce que ça change côté produit

Côté produit, suivez trois mesures. Le délai avant le premier token, le TTFT ; un token est un morceau de mot. Les tokens par seconde par utilisateur. Et le débit global du serveur. Car un agent fait souvent des dizaines, voire des centaines d'appels par tâche, en ordre de grandeur : chaque seconde se multiplie.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Le modèle réussit-il l'appel d'outils sur vos propres tâches ? Combien d'utilisateurs simultanés, avec quelle taille de contexte ? Et quel délai avant le premier token est acceptable ?

## Scène 7 · À retenir

À retenir : choisissez le modèle sur l'appel d'outils, pas sur les classements. Dimensionnez les GPU selon la mémoire, le contexte et les utilisateurs, puis mesurez délai et débit. Prochaine capsule : le harness, l'agent de code.
