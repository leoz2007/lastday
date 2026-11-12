# Capsule 66 · Mixture of Experts

Texte de la voix off (292 mots).

## Scène 1 · Accroche

Un modèle peut avoir énormément de paramètres, ses réglages appris, et n'en faire travailler qu'une petite partie pour chaque mot. C'est le principe du Mixture of Experts, ou mélange d'experts.

## Scène 2 · Des experts et un routeur

Imaginez un grand hôpital. Plutôt qu'un seul généraliste, il compte de nombreux spécialistes, et un accueil oriente chaque patient. Dans le modèle, les experts sont des sous-réseaux. L'aiguilleur, le routeur, choisit pour chaque token, un morceau de mot, seulement quelques experts. Les autres restent au repos.

## Scène 3 · Moins de calcul par token

Résultat : la taille totale du modèle peut être très grande, mais seule une fraction travaille pour chaque token. Comparez avec un modèle dense, où tout s'active à chaque fois : à taille totale égale, il calcule bien plus. Le mélange d'experts répond donc souvent plus vite, et moins cher.

## Scène 4 · Mémoire et experts peu lisibles

Mais attention : même au repos, tous les experts doivent tenir en mémoire. Il faut donc beaucoup de mémoire GPU, celle des processeurs graphiques. Et les experts ne sont pas forcément des thèmes lisibles, comme le droit ou la cuisine. Leur spécialité émerge de l'entraînement, souvent difficile à interpréter.

## Scène 5 · Ce que ça change côté produit

Côté produit, cette architecture joue sur la vitesse et le coût d'inférence, c'est-à-dire de chaque réponse. Pour un hébergement sur site, dimensionnez la mémoire sur la taille totale, pas sur la part active. Et ne jugez pas sur l'architecture : évaluez sur vos propres tâches.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quelle vitesse et quel coût par réponse visez-vous ? Hébergé sur site, le modèle tient-il en mémoire ? Et l'avez-vous testé sur vos propres tâches ?

## Scène 7 · À retenir

À retenir : un routeur n'active que quelques experts par token, donc moins de calcul. Mais tous les experts restent en mémoire : dimensionnez et testez en conséquence. Prochaine capsule : les lois d'échelle, et le calcul au moment de répondre.
