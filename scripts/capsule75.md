# Capsule 75 · Calcul confidentiel

Texte de la voix off (296 mots).

## Scène 1 · Accroche

Vos données sont souvent chiffrées sur le disque, et sur le réseau. Mais pendant le calcul, elles sont en général en clair, dans la mémoire de la machine.

## Scène 2 · Les trois états de la donnée

Une donnée connaît trois états : au repos, stockée ; en transit, sur le réseau ; et en cours d'usage, pendant le calcul. Les deux premiers sont souvent bien protégés. Le calcul confidentiel s'attaque au troisième : protéger la donnée pendant qu'on la traite.

## Scène 3 · Enclaves et attestation

Première approche : les enclaves matérielles, des zones isolées du processeur ou du GPU, le processeur graphique. Même l'hébergeur ne peut pas lire ce qui s'y passe. Et l'attestation apporte une preuve : c'est bien le bon code, dans la bonne enclave, avant d'y envoyer vos données.

## Scène 4 · Chiffrement homomorphe et apprentissage fédéré

Deuxième approche, le chiffrement homomorphe : calculer directement sur des données chiffrées. Prometteur, mais encore très coûteux, et limité pour les grands modèles. Troisième, l'apprentissage fédéré : on entraîne le modèle là où sont les données, et seules les mises à jour circulent.

## Scène 5 · Ce que ça change côté produit

Côté produit, c'est utile pour utiliser un modèle chez un tiers avec des données sensibles. Mais il y a des limites : un coût, de la performance en moins, plus de complexité, et une confiance à accorder au fabricant du matériel. Le juridique et la sécurité tranchent.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quelles données faut-il protéger pendant le calcul ? Quelle preuve d'attestation l'hébergeur fournit-il ? Et quel surcoût, quelle lenteur, êtes-vous prêts à accepter ?

## Scène 7 · À retenir

À retenir : le calcul confidentiel protège la donnée aussi pendant son traitement. C'est un outil puissant, avec un coût, à valider avec le juridique et la sécurité. C'était la dernière capsule de la saison cinq. Merci de l'avoir suivie avec tant de curiosité. Vous voyez maintenant sous le capot de l'IA générative. À vous de jouer !
