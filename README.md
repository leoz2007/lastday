# 🏝️ L'Île Oubliée

Un jeu d'aventure 3D **mobile-first** en [three.js](https://threejs.org/), sans build, sans dépendance externe : ouvre `index.html` et joue.

| Acte 1 — le jour | Acte 2 — les Brumes |
|---|---|
| ![Acte 1](docs/screenshot.png) | ![Acte 2](docs/screenshot-night.png) |

## 🎮 L'histoire

**Acte 1.** Échoué·e sur une île mystérieuse, tu pars à la rencontre du **Sage** au chapeau violet. Il te confie une quête : retrouver les **5 cristaux de lumière** dispersés par la tempête, puis ouvrir la porte du **temple ancien** au nord de l'île.

**Acte 2 — Les Brumes de l'Île.** En brisant le sceau du temple, tu saisis l'**Épée de Lumière**… et tu libères les Brumes. La nuit tombe, des **spectres** rôdent. Rallume les **4 braseros sacrés**, survis à leurs assauts (5 ❤️, tu réapparais au campement si tu tombes), puis terrasse le **Gardien des Brumes** pour ramener l'aube.

## 📱 Contrôles

| Plateforme | Déplacement | Caméra | Action | Attaque |
|---|---|---|---|---|
| **Mobile** | joystick virtuel (pouce gauche) | glisser sur la moitié droite | bouton contextuel 💬 / 🗝️ / 🔥 | bouton ⚔️ |
| **Desktop** | ZQSD / WASD / flèches | clic-glisser | `E`, `Espace` ou `Entrée` | `F` |

## 💾 Sauvegarde

La progression est **sauvegardée automatiquement** (localStorage) à chaque étape : cristaux collectés, clé obtenue, braseros allumés, boss. Au retour, un bouton **« ▶ Continuer l'aventure »** reprend la partie là où tu l'as laissée.

## 🚀 Lancer le jeu

Le jeu utilise des modules ES, il faut donc le servir en HTTP (pas de `file://`) :

```bash
# n'importe quel serveur statique fait l'affaire
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

Ou active simplement **GitHub Pages** sur ce dépôt (Settings → Pages → branche) : aucune étape de build n'est nécessaire.

## 🛠️ Sous le capot

- **Zéro asset externe** : three.js est vendorisé (`js/vendor/`), les sons sont synthétisés en WebAudio, les textures (halos) générées en canvas.
- **Île procédurale** : terrain déformé par bruit sinusoïdal, colorié par altitude (sable → herbe → roche), océan, nuages animés, lucioles.
- **Perf mobile** : `InstancedMesh` pour les ~70 arbres, rochers et fleurs ; pixel ratio plafonné à 2 ; une seule lumière à ombres (1024²) ; brouillard pour limiter le draw distance.
- **Gameplay** : machine à états de quête (8 étapes sur 2 actes), dialogues, collisions par cercles, caméra 3ᵉ personne avec orbite tactile, particules de collecte/combat/victoire.
- **Acte 2** : cycle jour → nuit interpolé (ciel, brouillard, lumières, océan, lune), spectres avec IA de poursuite et recul, combat à l'épée avec fenêtre de frappe et invulnérabilité temporaire, boss à 6 points de vie, retour de l'aube scripté.
- **Tactile soigné** : joystick dynamique (apparaît sous le pouce), multi-touch (marcher + tourner la caméra en même temps), `safe-area-inset` pour les encoches, blocage du zoom/scroll.

## 📂 Structure

```
index.html            # page, HUD, styles, import map
js/main.js            # tout le jeu (~800 lignes commentées)
js/vendor/            # three.js r160 (module ES minifié)
```

Amuse-toi bien ! ⛵
