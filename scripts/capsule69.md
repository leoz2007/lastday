# Capsule 69 · Calibration et incertitude

Texte de la voix off (293 mots).

## Scène 1 · Accroche

Un modèle qui vous dit « je suis sûr » n'a pas forcément raison. Les modèles de langage peuvent être trop sûrs d'eux. La vraie question : sa confiance annoncée correspond-elle à son taux de bonnes réponses ?

## Scène 2 · Être bien calibré

Être bien calibré, c'est avoir raison à peu près aussi souvent que sa confiance l'annonce. Pensez à un météorologue : quand il annonce soixante-dix pour cent de pluie, il devrait pleuvoir environ sept fois sur dix. Un modèle trop sûr de lui annonce beaucoup, et se trompe plus souvent qu'annoncé.

## Scène 3 · Le piège de la confiance en mots

Piège classique : la confiance exprimée en mots. « Je suis certain », ou « probablement », ne sont pas des mesures fiables. Ce sont des mots générés, comme le reste de la réponse, pas la lecture d'une jauge interne.

## Scène 4 · De meilleurs signaux

Il existe de meilleurs indices. Les probabilités des tokens, ces morceaux de mots, quand elles sont disponibles. L'accord entre plusieurs réponses à la même question : si elles divergent, méfiance. La vérification par les sources. Ou un second modèle, chargé de vérifier.

## Scène 5 · Ce que ça change côté produit

Côté produit, mesurez la calibration sur vos propres cas : comparez la confiance annoncée au taux de bonnes réponses. Puis fixez des seuils : sous le seuil, on escalade vers un humain. Vous pouvez aussi afficher le doute, et trier les cas pour la relecture.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Quel signal de confiance utilise-t-on, et est-il mesuré sur nos cas ? Quel seuil déclenche le passage à un humain ? Et comment montre-t-on le doute à l'utilisateur ?

## Scène 7 · À retenir

À retenir : un modèle bien calibré a raison aussi souvent qu'il l'annonce, et un « je suis sûr » ne prouve rien. Mesurez sur vos cas, puis fixez vos seuils. Prochaine capsule : les bases vectorielles, pour retrouver vite ce qui se ressemble.
