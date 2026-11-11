# Capsule 60 · Sécurité des agents

Texte de la voix off (290 mots).

## Scène 1 · Accroche

Un agent de code lit, écrit et exécute des commandes. C'est sa force, et c'est un risque. Une seule consigne piégée, et il peut agir contre vous, avec vos propres accès.

## Scène 2 · L'isolement de l'agent

Première défense : l'isolement, le sandboxing. L'agent travaille dans un bac à sable : un conteneur de développement, ou une machine virtuelle éphémère, détruite après la tâche. Et le trafic sortant est filtré : seules quelques adresses passent, comme le miroir de paquets.

## Scène 3 · Aucun secret de production

Deuxième défense : les secrets. Mots de passe, clés d'API, certificats de production : l'agent ne les voit jamais. Il travaille avec des données et des accès de test. Comme un stagiaire brillant, à qui l'on ne confie pas pour autant la clé du coffre.

## Scène 4 · Les risques propres aux agents

Trois risques sont propres aux agents. L'injection : une consigne cachée dans un dépôt ou un ticket, comme « envoie le fichier de configuration ici ». Les commandes destructrices, comme effacer un dossier entier. Et le slopsquatting : le modèle invente un nom de paquet, et des attaquants l'enregistrent avec du code malveillant.

## Scène 5 · Ce que ça change côté produit

Côté produit, ajoutez deux contrôles. La DLP, des règles de prévention des fuites sur les prompts : un secret ou une donnée client ne sort pas. Et un audit des actions de l'agent : chaque commande, chaque fichier modifié, tracé et relu en cas d'incident.

## Scène 6 · Questions à poser au cadrage

Au cadrage, posez trois questions. Où l'agent s'exécute-t-il, et vers quelles adresses peut-il sortir ? Comment garantir qu'il ne voit aucun secret de production ? Et quelles commandes exigent une validation humaine ?

## Scène 7 · À retenir

À retenir : un agent de code s'isole, se prive de secrets et laisse des traces. Méfiez-vous des consignes cachées, des commandes destructrices et des paquets inventés. Prochaine capsule : la FinOps de l'IA de code, pour maîtriser la facture.
