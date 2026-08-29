// ============================================================
//  L'ÎLE OUBLIÉE — jeu d'aventure three.js mobile-first
//
//  Acte 1 : explore l'île, parle au Sage, collecte 5 cristaux,
//           ouvre le temple ancien.
//  Acte 2 : l'Épée de Lumière, la nuit des Brumes, les spectres,
//           les 4 braseros sacrés et le Gardien des Brumes.
//
//  Sauvegarde automatique en localStorage.
// ============================================================
import * as THREE from 'three';

// ------------------------------------------------------------
//  Constantes du monde
// ------------------------------------------------------------
const ISLAND_R = 62;        // rayon de l'île
const WALK_R = 56;          // rayon max du joueur
const PLAYER_SPEED = 6.2;
const CRYSTAL_COUNT = 5;
const MAX_HEARTS = 5;
const SAVE_KEY = 'ile-oubliee-save-v2';

// ------------------------------------------------------------
//  Terrain : hauteur procédurale (île avec collines)
// ------------------------------------------------------------
function terrainH(x, z) {
  const d = Math.sqrt(x * x + z * z);
  const island = Math.max(0, 1 - (d / ISLAND_R) ** 2);
  let h =
    Math.sin(x * 0.09) * Math.cos(z * 0.08) * 1.5 +
    Math.sin(x * 0.031 + z * 0.047) * 2.1 +
    Math.cos(x * 0.017 - z * 0.023) * 1.2;
  return (h + 3.1) * island - 1.4;
}

// ------------------------------------------------------------
//  Rendu de base
// ------------------------------------------------------------
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.getElementById('game').appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87c5ea);
scene.fog = new THREE.Fog(0x9fd2ee, 55, 150);

const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 400);

// Lumières
const hemi = new THREE.HemisphereLight(0xcfe8ff, 0x4a6b3a, 0.85);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff2d0, 1.5);
sun.position.set(40, 60, 25);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.left = -70; sun.shadow.camera.right = 70;
sun.shadow.camera.top = 70; sun.shadow.camera.bottom = -70;
sun.shadow.camera.far = 200;
sun.shadow.bias = -0.0015;
scene.add(sun);

// ------------------------------------------------------------
//  Jour / Nuit (les Brumes de l'acte 2)
// ------------------------------------------------------------
const MOOD = {
  daySky: new THREE.Color(0x87c5ea), nightSky: new THREE.Color(0x0c1730),
  dayFog: new THREE.Color(0x9fd2ee), nightFog: new THREE.Color(0x182440),
  daySun: new THREE.Color(0xfff2d0), nightSun: new THREE.Color(0x8fa8ff),
  dayWater: new THREE.Color(0x2f7fc4), nightWater: new THREE.Color(0x142c48),
};
let night01 = 0;      // 0 = jour, 1 = nuit
let nightTarget = 0;
let moon;

function applyMood() {
  scene.background.lerpColors(MOOD.daySky, MOOD.nightSky, night01);
  scene.fog.color.lerpColors(MOOD.dayFog, MOOD.nightFog, night01);
  scene.fog.near = 55 - night01 * 25;
  scene.fog.far = 150 - night01 * 60;
  hemi.intensity = 0.85 - night01 * 0.55;
  sun.intensity = 1.5 - night01 * 1.1;
  sun.color.lerpColors(MOOD.daySun, MOOD.nightSun, night01);
  waterMat.color.lerpColors(MOOD.dayWater, MOOD.nightWater, night01);
  if (moon) moon.material.opacity = night01 * 0.95;
}

// ------------------------------------------------------------
//  Terrain maillé + couleurs par altitude
// ------------------------------------------------------------
{
  const seg = 110;
  const geo = new THREE.PlaneGeometry(ISLAND_R * 2.6, ISLAND_R * 2.6, seg, seg);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  const cSand = new THREE.Color(0xe6d29a);
  const cGrass1 = new THREE.Color(0x5fae4c);
  const cGrass2 = new THREE.Color(0x3f8a3c);
  const cRock = new THREE.Color(0x8d8d95);
  const tmp = new THREE.Color();
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), z = pos.getZ(i);
    const h = terrainH(x, z);
    pos.setY(i, h);
    const n = Math.sin(x * 0.7) * Math.cos(z * 0.8) * 0.15;
    if (h < 0.35 + n) tmp.copy(cSand);
    else if (h < 2.6 + n) tmp.copy(cGrass1).lerp(cGrass2, (h - 0.35) / 2.3);
    else tmp.copy(cGrass2).lerp(cRock, Math.min(1, (h - 2.6) / 1.8));
    colors[i * 3] = tmp.r; colors[i * 3 + 1] = tmp.g; colors[i * 3 + 2] = tmp.b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  const mat = new THREE.MeshLambertMaterial({ vertexColors: true });
  const terrain = new THREE.Mesh(geo, mat);
  terrain.receiveShadow = true;
  scene.add(terrain);
}

// Océan
const waterMat = new THREE.MeshLambertMaterial({ color: 0x2f7fc4, transparent: true, opacity: 0.88 });
{
  const water = new THREE.Mesh(new THREE.CircleGeometry(220, 48), waterMat);
  water.rotation.x = -Math.PI / 2;
  water.position.y = 0;
  scene.add(water);
}

// ------------------------------------------------------------
//  Décor instancié : arbres, rochers, fleurs
// ------------------------------------------------------------
const colliders = []; // {x, z, r}
const dummy = new THREE.Object3D();
const rng = mulberry32(1337);
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function randSpot(minR, maxR, minH) {
  for (let tries = 0; tries < 40; tries++) {
    const a = rng() * Math.PI * 2;
    const r = minR + rng() * (maxR - minR);
    const x = Math.cos(a) * r, z = Math.sin(a) * r;
    const h = terrainH(x, z);
    if (h > minH && !nearReserved(x, z)) return { x, z, h };
  }
  return null;
}
// zones réservées (spawn, sage, temple, braseros) où le décor ne pousse pas
const BRAZIER_SPOTS = [[34, 6], [-30, 10], [-20, -30], [26, -20]];
const reserved = [
  { x: 0, z: 10, r: 7 },   // spawn
  { x: 4, z: 3, r: 4 },    // sage
  { x: 0, z: -38, r: 12 }, // temple
  ...BRAZIER_SPOTS.map(([x, z]) => ({ x, z, r: 4 })),
];
function nearReserved(x, z) {
  return reserved.some(s => (x - s.x) ** 2 + (z - s.z) ** 2 < s.r * s.r);
}

// Arbres
{
  const N = 70;
  const trunkGeo = new THREE.CylinderGeometry(0.22, 0.34, 2.2, 6);
  const trunkMat = new THREE.MeshLambertMaterial({ color: 0x6e4a2e });
  const leafGeo = new THREE.ConeGeometry(1.5, 2.6, 7);
  const leafMat = new THREE.MeshLambertMaterial({ color: 0x2e7d36 });
  const trunks = new THREE.InstancedMesh(trunkGeo, trunkMat, N);
  const leaves = new THREE.InstancedMesh(leafGeo, leafMat, N * 2);
  trunks.castShadow = leaves.castShadow = true;
  const leafColor = new THREE.Color();
  let li = 0;
  for (let i = 0; i < N; i++) {
    const s = randSpot(10, 52, 0.6);
    if (!s) continue;
    const scale = 0.8 + rng() * 0.9;
    dummy.position.set(s.x, s.h + 1.1 * scale, s.z);
    dummy.scale.setScalar(scale);
    dummy.rotation.y = rng() * Math.PI * 2;
    dummy.updateMatrix();
    trunks.setMatrixAt(i, dummy.matrix);
    for (let k = 0; k < 2; k++) {
      dummy.position.set(s.x, s.h + (2.2 + k * 1.1) * scale, s.z);
      dummy.scale.setScalar(scale * (1 - k * 0.35));
      dummy.updateMatrix();
      leaves.setMatrixAt(li, dummy.matrix);
      leafColor.setHSL(0.32 + rng() * 0.06, 0.55, 0.3 + rng() * 0.12);
      leaves.setColorAt(li, leafColor);
      li++;
    }
    colliders.push({ x: s.x, z: s.z, r: 0.7 * scale });
  }
  leaves.count = li;
  scene.add(trunks, leaves);
}

// Rochers
{
  const N = 26;
  const geo = new THREE.IcosahedronGeometry(0.9, 0);
  const mat = new THREE.MeshLambertMaterial({ color: 0x8f9099, flatShading: true });
  const rocks = new THREE.InstancedMesh(geo, mat, N);
  rocks.castShadow = true;
  for (let i = 0; i < N; i++) {
    const s = randSpot(8, 54, 0.15);
    if (!s) continue;
    const sc = 0.5 + rng() * 1.3;
    dummy.position.set(s.x, s.h + sc * 0.3, s.z);
    dummy.scale.set(sc, sc * (0.6 + rng() * 0.5), sc);
    dummy.rotation.set(rng(), rng() * Math.PI * 2, rng());
    dummy.updateMatrix();
    rocks.setMatrixAt(i, dummy.matrix);
    if (sc > 0.8) colliders.push({ x: s.x, z: s.z, r: sc * 0.8 });
  }
  scene.add(rocks);
}

// Fleurs
{
  const N = 90;
  const geo = new THREE.ConeGeometry(0.12, 0.25, 5);
  const mat = new THREE.MeshLambertMaterial({ color: 0xffffff });
  const flowers = new THREE.InstancedMesh(geo, mat, N);
  const palette = [0xff6b8d, 0xffd166, 0xa78bfa, 0xffffff, 0xff9e5e];
  const c = new THREE.Color();
  for (let i = 0; i < N; i++) {
    const s = randSpot(6, 50, 0.5);
    if (!s) continue;
    dummy.position.set(s.x, s.h + 0.14, s.z);
    dummy.scale.setScalar(0.8 + rng() * 0.8);
    dummy.updateMatrix();
    flowers.setMatrixAt(i, dummy.matrix);
    flowers.setColorAt(i, c.setHex(palette[(rng() * palette.length) | 0]));
  }
  scene.add(flowers);
}

// Lucioles (points scintillants)
let fireflies;
{
  const N = 60;
  const positions = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const s = randSpot(5, 50, 0.4) || { x: 0, z: 0, h: 1 };
    positions[i * 3] = s.x;
    positions[i * 3 + 1] = s.h + 1 + rng() * 2;
    positions[i * 3 + 2] = s.z;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  fireflies = new THREE.Points(geo, new THREE.PointsMaterial({
    color: 0xfff7b0, size: 0.22, transparent: true, opacity: 0.9,
    blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  scene.add(fireflies);
}

// Nuages
const clouds = [];
{
  const mat = new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.85 });
  for (let i = 0; i < 8; i++) {
    const g = new THREE.Group();
    const n = 3 + ((rng() * 3) | 0);
    for (let k = 0; k < n; k++) {
      const puff = new THREE.Mesh(new THREE.SphereGeometry(2 + rng() * 2.4, 8, 6), mat);
      puff.position.set((rng() - 0.5) * 7, (rng() - 0.5) * 1.5, (rng() - 0.5) * 4);
      puff.scale.y = 0.55;
      g.add(puff);
    }
    g.position.set((rng() - 0.5) * 220, 34 + rng() * 14, (rng() - 0.5) * 220);
    g.userData.speed = 0.4 + rng() * 0.6;
    scene.add(g);
    clouds.push(g);
  }
}

// Lune (visible la nuit)
{
  moon = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture(), color: 0xeef2ff, transparent: true,
    opacity: 0, depthWrite: false,
  }));
  moon.scale.setScalar(26);
  moon.position.set(-70, 75, -90);
  scene.add(moon);
}

// ------------------------------------------------------------
//  Personnages
// ------------------------------------------------------------
function makeCharacter({ shirt, pants, skin, hat }) {
  const g = new THREE.Group();
  const M = c => new THREE.MeshLambertMaterial({ color: c });

  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.42, 0.85, 10), M(shirt));
  body.position.y = 1.0;
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.34, 12, 10), M(skin));
  head.position.y = 1.75;
  const eyeMat = new THREE.MeshBasicMaterial({ color: 0x222222 });
  const eyeGeo = new THREE.SphereGeometry(0.045, 6, 6);
  const e1 = new THREE.Mesh(eyeGeo, eyeMat); e1.position.set(0.13, 1.8, 0.29);
  const e2 = new THREE.Mesh(eyeGeo, eyeMat); e2.position.set(-0.13, 1.8, 0.29);

  const armGeo = new THREE.CapsuleGeometry(0.09, 0.5, 3, 6);
  const armL = new THREE.Mesh(armGeo, M(shirt)); armL.position.set(0.48, 1.15, 0);
  const armR = new THREE.Mesh(armGeo, M(shirt)); armR.position.set(-0.48, 1.15, 0);
  const legGeo = new THREE.CapsuleGeometry(0.11, 0.42, 3, 6);
  const legL = new THREE.Mesh(legGeo, M(pants)); legL.position.set(0.17, 0.38, 0);
  const legR = new THREE.Mesh(legGeo, M(pants)); legR.position.set(-0.17, 0.38, 0);

  g.add(body, head, e1, e2, armL, armR, legL, legR);
  if (hat) {
    const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.46, 0.46, 0.06, 12), M(hat));
    brim.position.y = 1.98;
    const top = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.55, 10), M(hat));
    top.position.y = 2.25;
    g.add(brim, top);
  }
  g.traverse(o => { if (o.isMesh) o.castShadow = true; });
  g.userData.limbs = { armL, armR, legL, legR };
  return g;
}

// Joueur
const player = makeCharacter({ shirt: 0xd95a3c, pants: 0x35506e, skin: 0xf0c49b });
player.position.set(0, terrainH(0, 10), 10);
player.rotation.y = Math.PI; // face au Sage
scene.add(player);
const pState = { angle: Math.PI, bob: 0 };

// Épée de Lumière (invisible avant l'acte 2), attachée au bras droit
const sword = new THREE.Group();
{
  const blade = new THREE.Mesh(
    new THREE.BoxGeometry(0.09, 1.05, 0.045),
    new THREE.MeshLambertMaterial({ color: 0xdfe9ff, emissive: 0x5a7ad8 })
  );
  blade.position.y = -0.85;
  const guard = new THREE.Mesh(
    new THREE.BoxGeometry(0.3, 0.06, 0.09),
    new THREE.MeshLambertMaterial({ color: 0xc9a24a, emissive: 0x3a2a08 })
  );
  guard.position.y = -0.3;
  sword.add(blade, guard);
  sword.visible = false;
  player.userData.limbs.armR.add(sword);
}

// Le Sage
const sage = makeCharacter({ shirt: 0x6d5aa8, pants: 0x4a3f75, skin: 0xe8bd92, hat: 0x54468f });
sage.position.set(4, terrainH(4, 3), 3);
sage.rotation.y = Math.PI * 0.85;
scene.add(sage);
// barbe + bâton
{
  const beard = new THREE.Mesh(
    new THREE.ConeGeometry(0.2, 0.5, 8),
    new THREE.MeshLambertMaterial({ color: 0xe8e8e8 })
  );
  beard.position.set(0, 1.45, 0.24); beard.rotation.x = 0.25;
  const staff = new THREE.Mesh(
    new THREE.CylinderGeometry(0.04, 0.05, 2.1, 6),
    new THREE.MeshLambertMaterial({ color: 0x8a6540 })
  );
  staff.position.set(0.62, 1.05, 0.1);
  const orb = new THREE.Mesh(
    new THREE.SphereGeometry(0.13, 10, 8),
    new THREE.MeshLambertMaterial({ color: 0x7de8ff, emissive: 0x2fa8c8 })
  );
  orb.position.set(0.62, 2.15, 0.1);
  sage.add(beard, staff, orb);
}
colliders.push({ x: sage.position.x, z: sage.position.z, r: 0.7 });

// ------------------------------------------------------------
//  Le temple ancien
// ------------------------------------------------------------
const temple = new THREE.Group();
let templeDoor, treasureRef;
{
  const stone = new THREE.MeshLambertMaterial({ color: 0xb8b0a0 });
  const stoneDark = new THREE.MeshLambertMaterial({ color: 0x8f8878 });
  const base = new THREE.Mesh(new THREE.BoxGeometry(14, 1.2, 10), stoneDark);
  base.position.y = 0.6;
  temple.add(base);
  const steps = new THREE.Mesh(new THREE.BoxGeometry(6, 0.6, 2.4), stoneDark);
  steps.position.set(0, 0.3, 6.0);
  temple.add(steps);
  for (const sx of [-5.2, -1.8, 1.8, 5.2]) {
    const col = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.65, 6, 10), stone);
    col.position.set(sx, 4.2, 4.2);
    temple.add(col);
  }
  const lintel = new THREE.Mesh(new THREE.BoxGeometry(13.4, 1.1, 1.6), stone);
  lintel.position.set(0, 7.6, 4.2);
  temple.add(lintel);
  const backWall = new THREE.Mesh(new THREE.BoxGeometry(12, 7, 1), stone);
  backWall.position.set(0, 4.7, -3.5);
  temple.add(backWall);
  for (const side of [-1, 1]) {
    const wall = new THREE.Mesh(new THREE.BoxGeometry(1, 7, 7), stone);
    wall.position.set(side * 6, 4.7, 0.2);
    temple.add(wall);
  }
  const roof = new THREE.Mesh(new THREE.BoxGeometry(13.5, 0.9, 9.5), stoneDark);
  roof.position.set(0, 8.5, 0.2);
  temple.add(roof);

  // porte dorée
  templeDoor = new THREE.Mesh(
    new THREE.BoxGeometry(3.4, 5.2, 0.5),
    new THREE.MeshLambertMaterial({ color: 0xc9a24a, emissive: 0x3a2a08 })
  );
  templeDoor.position.set(0, 3.8, 4.2);
  temple.add(templeDoor);

  // trésor (révélé quand la porte s'ouvre)
  treasureRef = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.9, 1),
    new THREE.MeshLambertMaterial({ color: 0xffe27a, emissive: 0xcf9d2a })
  );
  treasureRef.position.set(0, 2.6, 0);
  temple.add(treasureRef);

  const th = terrainH(0, -38);
  temple.position.set(0, th, -38);
  temple.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  scene.add(temple);
  colliders.push(
    { x: 0, z: -38 - 3.5, r: 6.5 },
    { x: -6, z: -38, r: 2 }, { x: 6, z: -38, r: 2 },
  );
}
const doorSpot = new THREE.Vector3(0, 0, -38 + 6.5); // point d'interaction devant la porte
let doorOpenAnim = 0;

// ------------------------------------------------------------
//  Cristaux (acte 1)
// ------------------------------------------------------------
const crystals = [];
{
  const spots = [
    [30, 18], [-26, 24], [-34, -18], [24, -30], [8, 42],
  ];
  const geo = new THREE.OctahedronGeometry(0.55, 0);
  for (let i = 0; i < CRYSTAL_COUNT; i++) {
    const [x, z] = spots[i];
    const mat = new THREE.MeshLambertMaterial({
      color: 0x7fd8ff, emissive: 0x2f7fd8, transparent: true, opacity: 0.95,
    });
    const m = new THREE.Mesh(geo, mat);
    const h = Math.max(terrainH(x, z), 0.3);
    m.position.set(x, h + 1.2, z);
    m.castShadow = true;
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({
      map: makeGlowTexture(), color: 0x9fe0ff, transparent: true,
      opacity: 0.75, blending: THREE.AdditiveBlending, depthWrite: false,
    }));
    halo.scale.setScalar(3);
    m.add(halo);
    scene.add(m);
    crystals.push({ mesh: m, taken: false, baseY: m.position.y, phase: i * 1.3 });
  }
}
function makeGlowTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(32, 32, 2, 32, 32, 30);
  grad.addColorStop(0, 'rgba(255,255,255,0.9)');
  grad.addColorStop(0.4, 'rgba(160,220,255,0.35)');
  grad.addColorStop(1, 'rgba(160,220,255,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}

// Panneau indicateur au spawn
{
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 1.4, 6),
    new THREE.MeshLambertMaterial({ color: 0x7a5734 }));
  const board = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.5, 0.08),
    new THREE.MeshLambertMaterial({ color: 0x9c7648 }));
  board.position.y = 0.7;
  const sign = new THREE.Group();
  sign.add(post, board);
  sign.position.set(-2.5, terrainH(-2.5, 8) + 0.7, 8);
  sign.rotation.y = 0.5;
  scene.add(sign);
}

// ------------------------------------------------------------
//  Braseros sacrés (acte 2)
// ------------------------------------------------------------
const braziers = [];
{
  const bowlMat = new THREE.MeshLambertMaterial({ color: 0x555560 });
  const woodMat = new THREE.MeshLambertMaterial({ color: 0x5c3f26 });
  for (let i = 0; i < BRAZIER_SPOTS.length; i++) {
    const [x, z] = BRAZIER_SPOTS[i];
    const h = Math.max(terrainH(x, z), 0.3);
    const g = new THREE.Group();
    const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.3, 1.0, 8), bowlMat);
    foot.position.y = 0.5;
    const bowl = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.35, 0.45, 10), bowlMat);
    bowl.position.y = 1.15;
    const wood = new THREE.Mesh(new THREE.SphereGeometry(0.32, 8, 6), woodMat);
    wood.position.y = 1.35; wood.scale.y = 0.5;
    // flamme (cachée tant que non allumé)
    const flame = new THREE.Group();
    const f1 = new THREE.Mesh(new THREE.ConeGeometry(0.34, 0.9, 8),
      new THREE.MeshLambertMaterial({ color: 0xffb03a, emissive: 0xff7a10, transparent: true, opacity: 0.95 }));
    f1.position.y = 1.85;
    const f2 = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.6, 8),
      new THREE.MeshLambertMaterial({ color: 0xfff0a0, emissive: 0xffc040 }));
    f2.position.y = 2.0;
    const glow = new THREE.Sprite(new THREE.SpriteMaterial({
      map: makeGlowTexture(), color: 0xffb050, transparent: true,
      opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false,
    }));
    glow.scale.setScalar(4);
    glow.position.y = 1.9;
    flame.add(f1, f2, glow);
    flame.visible = false;
    g.add(foot, bowl, wood, flame);
    g.position.set(x, h, z);
    g.traverse(o => { if (o.isMesh) o.castShadow = true; });
    scene.add(g);
    colliders.push({ x, z, r: 0.7 });
    braziers.push({ group: g, flame, lit: false, x, z });
  }
}
function litCount() { return braziers.filter(b => b.lit).length; }

// ------------------------------------------------------------
//  Spectres & Gardien (acte 2)
// ------------------------------------------------------------
const enemies = [];
function makeSpectre(boss = false) {
  const g = new THREE.Group();
  const bodyMat = new THREE.MeshLambertMaterial({
    color: boss ? 0xd8b8c8 : 0xc4bcf2,
    emissive: boss ? 0x8a2a3a : 0x4a3f9a,
    transparent: true, opacity: 0.82,
  });
  const body = new THREE.Mesh(new THREE.ConeGeometry(0.55, 1.6, 8), bodyMat);
  body.position.y = 0.8; body.rotation.x = Math.PI; // pointe vers le bas
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.42, 10, 8), bodyMat);
  head.position.y = 1.75;
  const eyeMat = new THREE.MeshBasicMaterial({ color: boss ? 0xff4040 : 0x7ae8ff });
  const eyeGeo = new THREE.SphereGeometry(0.07, 6, 6);
  const e1 = new THREE.Mesh(eyeGeo, eyeMat); e1.position.set(0.15, 1.82, 0.36);
  const e2 = new THREE.Mesh(eyeGeo, eyeMat); e2.position.set(-0.15, 1.82, 0.36);
  const armGeo = new THREE.CapsuleGeometry(0.08, 0.5, 3, 6);
  const a1 = new THREE.Mesh(armGeo, bodyMat); a1.position.set(0.55, 1.2, 0.1); a1.rotation.z = -0.5;
  const a2 = new THREE.Mesh(armGeo, bodyMat); a2.position.set(-0.55, 1.2, 0.1); a2.rotation.z = 0.5;
  g.add(body, head, e1, e2, a1, a2);
  if (boss) {
    const crown = new THREE.Mesh(
      new THREE.CylinderGeometry(0.3, 0.42, 0.35, 6, 1, true),
      new THREE.MeshLambertMaterial({ color: 0x8a8a95, emissive: 0x2a2a35, side: THREE.DoubleSide })
    );
    crown.position.y = 2.15;
    g.add(crown);
    g.scale.setScalar(2.1);
  }
  return { group: g, mats: [bodyMat] };
}
function spawnSpectre(x, z, boss = false) {
  const { group, mats } = makeSpectre(boss);
  group.position.set(x, Math.max(terrainH(x, z), 0.05) + 0.55, z);
  scene.add(group);
  const e = {
    group, mats, boss,
    hp: boss ? 6 : 1,
    speed: boss ? 3.4 : 2.6,
    aggro: boss ? 40 : 11,
    phase: Math.random() * 6.28,
    home: { x, z },
    dying: null, dead: false,
  };
  enemies.push(e);
  return e;
}
let bossRef = null;
function spawnEnemies() {
  for (const b of braziers) {
    if (b.lit) continue;
    spawnSpectre(b.x + 2.5, b.z + 1.5);
    spawnSpectre(b.x - 2, b.z - 2.5);
  }
  spawnSpectre(12, -12);
  spawnSpectre(-10, -20);
}
function spawnBoss() {
  bossRef = spawnSpectre(0, -26, true);
  toast('Le Gardien des Brumes apparaît !');
  sfx.boss();
}

// ------------------------------------------------------------
//  Particules d'effets (collecte, combat, victoire)
// ------------------------------------------------------------
const bursts = [];
function spawnBurst(pos, color, count = 26, speed = 5) {
  const positions = new Float32Array(count * 3);
  const vels = [];
  for (let i = 0; i < count; i++) {
    positions[i * 3] = pos.x; positions[i * 3 + 1] = pos.y; positions[i * 3 + 2] = pos.z;
    const a = Math.random() * Math.PI * 2;
    const b = Math.random() * Math.PI - Math.PI / 2;
    const v = speed * (0.4 + Math.random() * 0.6);
    vels.push(new THREE.Vector3(
      Math.cos(a) * Math.cos(b) * v,
      Math.sin(b) * v + 2,
      Math.sin(a) * Math.cos(b) * v
    ));
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const mat = new THREE.PointsMaterial({
    color, size: 0.28, transparent: true, opacity: 1,
    blending: THREE.AdditiveBlending, depthWrite: false,
  });
  const pts = new THREE.Points(geo, mat);
  scene.add(pts);
  bursts.push({ pts, vels, life: 1 });
}
function updateBursts(dt) {
  for (let i = bursts.length - 1; i >= 0; i--) {
    const b = bursts[i];
    b.life -= dt * 0.9;
    const pos = b.pts.geometry.attributes.position;
    for (let k = 0; k < b.vels.length; k++) {
      const v = b.vels[k];
      v.y -= 9 * dt;
      pos.setXYZ(k, pos.getX(k) + v.x * dt, pos.getY(k) + v.y * dt, pos.getZ(k) + v.z * dt);
    }
    pos.needsUpdate = true;
    b.pts.material.opacity = Math.max(0, b.life);
    if (b.life <= 0) {
      scene.remove(b.pts);
      b.pts.geometry.dispose(); b.pts.material.dispose();
      bursts.splice(i, 1);
    }
  }
}

// ------------------------------------------------------------
//  Audio (WebAudio, zéro asset)
// ------------------------------------------------------------
let actx = null;
function audioInit() {
  if (!actx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC) actx = new AC();
  }
  if (actx && actx.state === 'suspended') actx.resume();
}
function tone(freq, dur = 0.15, type = 'sine', vol = 0.18, delay = 0) {
  if (!actx) return;
  const t0 = actx.currentTime + delay;
  const o = actx.createOscillator();
  const g = actx.createGain();
  o.type = type; o.frequency.value = freq;
  g.gain.setValueAtTime(0, t0);
  g.gain.linearRampToValueAtTime(vol, t0 + 0.015);
  g.gain.exponentialRampToValueAtTime(0.001, t0 + dur);
  o.connect(g); g.connect(actx.destination);
  o.start(t0); o.stop(t0 + dur + 0.05);
}
const sfx = {
  blip: () => tone(620, 0.07, 'square', 0.06),
  collect: () => { tone(660, 0.12, 'sine', 0.2); tone(880, 0.14, 'sine', 0.18, 0.09); tone(1320, 0.2, 'sine', 0.14, 0.18); },
  quest: () => { tone(523, 0.15, 'triangle', 0.16); tone(659, 0.15, 'triangle', 0.16, 0.12); tone(784, 0.25, 'triangle', 0.16, 0.24); },
  door: () => { tone(120, 0.7, 'sawtooth', 0.12); tone(90, 0.9, 'sawtooth', 0.1, 0.15); },
  swing: () => { tone(300, 0.07, 'sawtooth', 0.09); tone(190, 0.09, 'sawtooth', 0.07, 0.04); },
  hit: () => { tone(520, 0.06, 'square', 0.14); tone(260, 0.1, 'square', 0.1, 0.04); },
  hurt: () => { tone(140, 0.22, 'sawtooth', 0.2); tone(90, 0.3, 'sawtooth', 0.16, 0.08); },
  brazier: () => { tone(220, 0.25, 'triangle', 0.16); tone(330, 0.3, 'sine', 0.14, 0.12); tone(440, 0.4, 'sine', 0.12, 0.24); },
  boss: () => { tone(80, 0.6, 'sawtooth', 0.22); tone(60, 0.8, 'sawtooth', 0.18, 0.2); tone(110, 0.5, 'square', 0.1, 0.4); },
  victory: () => {
    const notes = [523, 659, 784, 1047, 784, 1047, 1319];
    notes.forEach((n, i) => tone(n, 0.22, 'triangle', 0.18, i * 0.14));
  },
};

// ------------------------------------------------------------
//  État de la quête + UI
// ------------------------------------------------------------
// stages : intro → collect → temple → opening → braziers → boss → dawn → done
const quest = { stage: 'intro', collected: 0, startTime: 0, priorMs: 0 };
let hearts = MAX_HEARTS;
let invulnUntil = 0;
let attackT = 0;

const ui = {
  banner: document.getElementById('questBanner'),
  counter: document.getElementById('counter'),
  counterTxt: document.getElementById('counterTxt'),
  actionBtn: document.getElementById('actionBtn'),
  attackBtn: document.getElementById('attackBtn'),
  hearts: document.getElementById('hearts'),
  dialogue: document.getElementById('dialogue'),
  dlgSpeaker: document.getElementById('dlgSpeaker'),
  dlgText: document.getElementById('dlgText'),
  toast: document.getElementById('toast'),
  joy: document.getElementById('joy'),
  joyStick: document.getElementById('joyStick'),
};

function setBanner(html) { ui.banner.innerHTML = html; }
function toast(msg) {
  ui.toast.textContent = msg;
  ui.toast.style.opacity = '1';
  ui.toast.style.transform = 'translate(-50%,-70%)';
  setTimeout(() => {
    ui.toast.style.opacity = '0';
    ui.toast.style.transform = 'translate(-50%,-50%)';
  }, 1600);
}
function renderHearts() {
  ui.hearts.textContent = '❤️'.repeat(hearts) + '🖤'.repeat(MAX_HEARTS - hearts);
}
function brazierBanner() {
  setBanner(`🔥 Rallume les <b>braseros sacrés</b> — ${litCount()} / ${braziers.length}`);
}
function bossBanner() {
  const hp = bossRef && !bossRef.dead ? bossRef.hp : 0;
  setBanner(`⚔️ Terrasse le <b>Gardien des Brumes</b> ! ${'🔺'.repeat(Math.max(hp, 0))}`);
}
function playMs() {
  return quest.priorMs + (quest.startTime ? performance.now() - quest.startTime : 0);
}

// ------------------------------------------------------------
//  Sauvegarde (localStorage)
// ------------------------------------------------------------
function saveGame(stage) {
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify({
      v: 2,
      stage,
      taken: crystals.map((c, i) => c.taken ? i : -1).filter(i => i >= 0),
      lit: braziers.map((b, i) => b.lit ? i : -1).filter(i => i >= 0),
      playMs: playMs(),
    }));
  } catch (e) { /* stockage indisponible : on joue sans sauvegarde */ }
}
function loadSave() {
  try {
    const s = JSON.parse(localStorage.getItem(SAVE_KEY));
    return (s && s.v === 2 && s.stage && s.stage !== 'done') ? s : null;
  } catch (e) { return null; }
}
function clearSave() {
  try { localStorage.removeItem(SAVE_KEY); } catch (e) { /* ignore */ }
}

// ------------------------------------------------------------
//  Dialogues
// ------------------------------------------------------------
const DIALOGUES = {
  sageIntro: {
    speaker: 'Le Sage',
    lines: [
      "Ah… un visiteur ! Cela faisait bien longtemps.",
      "Cette île cache un temple ancien, mais sa porte est scellée depuis des siècles.",
      "Jadis, cinq cristaux de lumière alimentaient son mécanisme. Une tempête les a dispersés aux quatre coins de l'île…",
      "Rapporte-moi les 5 cristaux, et je te confierai la clé du temple. Bonne chance, voyageur !",
    ],
    onEnd: () => {
      quest.stage = 'collect';
      if (!quest.startTime) quest.startTime = performance.now();
      ui.counter.style.display = 'flex';
      setBanner("🔍 Retrouve les <b>5 cristaux</b> dispersés sur l'île");
      sfx.quest();
      toast('Nouvelle quête !');
      saveGame('collect');
    },
  },
  sageWait: {
    speaker: 'Le Sage',
    lines: ["Les cristaux brillent la nuit comme le jour… Ouvre l'œil, ils ne sont jamais loin des sentiers."],
  },
  sageDone: {
    speaker: 'Le Sage',
    lines: [
      "Par les anciens… tu les as tous retrouvés !",
      "Voici la clé du temple. Il se dresse au nord de l'île, derrière la colline.",
      "Va, et découvre ce que nos ancêtres y ont laissé…",
    ],
    onEnd: () => {
      quest.stage = 'temple';
      setBanner("🗝️ Ouvre la <b>porte du temple</b>, au nord de l'île");
      sfx.quest();
      toast('Clé du temple obtenue !');
      saveGame('temple');
    },
  },
  sageAfter: {
    speaker: 'Le Sage',
    lines: ["Le temple t'attend au nord. La clé ne sert qu'une fois, fais-en bon usage !"],
  },
  templeVoice: {
    speaker: 'Une Voix Ancienne',
    lines: [
      "Tu saisis l'Épée de Lumière, endormie depuis mille ans…",
      "Mais prends garde, voyageur : en brisant le sceau, tu as libéré les Brumes.",
      "La nuit tombe sur l'île. Des spectres rôdent déjà entre les arbres…",
      "Rallume les 4 braseros sacrés pour affaiblir les Brumes… puis terrasse leur Gardien !",
    ],
    onEnd: () => { startAct2(); },
  },
  sageNight: {
    speaker: 'Le Sage',
    lines: [
      "Les Brumes… je les croyais légende. Ton épée est leur seule faiblesse !",
      "Rallume les braseros, petit. Leur flamme sacrée affaiblit les spectres. Et reviens me voir si ton courage vacille.",
    ],
  },
  sageBoss: {
    speaker: 'Le Sage',
    lines: ["Le Gardien des Brumes garde le temple. Frappe-le sans relâche — chaque coup de ton épée le rapproche du néant !"],
  },
};

let activeDialogue = null;
let dlgIndex = 0;
function openDialogue(key) {
  activeDialogue = DIALOGUES[key];
  dlgIndex = 0;
  ui.dlgSpeaker.textContent = activeDialogue.speaker;
  ui.dlgText.textContent = activeDialogue.lines[0];
  ui.dialogue.style.display = 'block';
  ui.actionBtn.style.display = 'none';
  sfx.blip();
}
function advanceDialogue() {
  if (!activeDialogue) return;
  dlgIndex++;
  if (dlgIndex < activeDialogue.lines.length) {
    ui.dlgText.textContent = activeDialogue.lines[dlgIndex];
    sfx.blip();
  } else {
    ui.dialogue.style.display = 'none';
    const cb = activeDialogue.onEnd;
    activeDialogue = null;
    if (cb) cb();
  }
}
ui.dialogue.addEventListener('pointerdown', e => { e.stopPropagation(); advanceDialogue(); });

// ------------------------------------------------------------
//  Progression de l'acte 2
// ------------------------------------------------------------
function startAct2() {
  quest.stage = 'braziers';
  nightTarget = 1;
  sword.visible = true;
  ui.hearts.style.display = 'flex';
  ui.attackBtn.style.display = 'flex';
  renderHearts();
  spawnEnemies();
  brazierBanner();
  sfx.quest();
  toast("L'Épée de Lumière est à toi !");
  saveGame('braziers');
}

function lightBrazier(b) {
  if (b.lit) return;
  b.lit = true;
  b.flame.visible = true;
  spawnBurst(new THREE.Vector3(b.x, b.group.position.y + 1.8, b.z), 0xffb050, 30, 5);
  sfx.brazier();
  if (litCount() >= braziers.length) {
    quest.stage = 'boss';
    spawnBoss();
    bossBanner();
    saveGame('boss');
  } else {
    brazierBanner();
    toast(`Brasero ${litCount()} / ${braziers.length}`);
    saveGame('braziers');
  }
}

function doAttack() {
  if (quest.stage !== 'braziers' && quest.stage !== 'boss') return;
  if (attackT > 0 || activeDialogue) return;
  attackT = 0.38;
  sfx.swing();
  const p = player.position;
  const fx = Math.sin(pState.angle), fz = Math.cos(pState.angle);
  for (const e of enemies) {
    if (e.dead || e.dying !== null) continue;
    const dx = e.group.position.x - p.x, dz = e.group.position.z - p.z;
    const d = Math.hypot(dx, dz);
    const reach = e.boss ? 3.4 : 2.7;
    const inFront = d > 0.01 && (dx / d * fx + dz / d * fz) > 0.15;
    if (d < 1.6 || (d < reach && inFront)) damageEnemy(e);
  }
}
function damageEnemy(e) {
  e.hp--;
  sfx.hit();
  spawnBurst(e.group.position.clone().add(new THREE.Vector3(0, 1.2, 0)),
    e.boss ? 0xff8080 : 0xbfb8ff, 18, 4);
  // recul
  const dx = e.group.position.x - player.position.x;
  const dz = e.group.position.z - player.position.z;
  const d = Math.hypot(dx, dz) || 1;
  e.group.position.x += dx / d * 1.2;
  e.group.position.z += dz / d * 1.2;
  if (e.boss) bossBanner();
  if (e.hp <= 0) {
    e.dying = 0.6;
    if (e.boss) {
      quest.stage = 'dawn';
      nightTarget = 0;
      setBanner('🌅 Les Brumes se dissipent…');
      toast('Le Gardien est vaincu !');
      sfx.victory();
      setTimeout(finalVictory, 3200);
    }
  }
}
function damagePlayer(e) {
  const now = performance.now();
  if (now < invulnUntil || quest.stage === 'dawn' || quest.stage === 'done') return;
  invulnUntil = now + 1300;
  hearts--;
  renderHearts();
  sfx.hurt();
  // recul du joueur
  const dx = player.position.x - e.group.position.x;
  const dz = player.position.z - e.group.position.z;
  const d = Math.hypot(dx, dz) || 1;
  let nx = player.position.x + dx / d * 2.4;
  let nz = player.position.z + dz / d * 2.4;
  const dc = Math.hypot(nx, nz);
  if (dc > WALK_R) { nx = nx / dc * WALK_R; nz = nz / dc * WALK_R; }
  player.position.x = nx; player.position.z = nz;
  if (hearts <= 0) {
    hearts = MAX_HEARTS;
    renderHearts();
    player.position.set(0, terrainH(0, 10), 10);
    toast('Les Brumes t\'ont repoussé au campement…');
  }
}

function finalVictory() {
  quest.stage = 'done';
  clearSave();
  const secs = Math.round(playMs() / 1000);
  const m = Math.floor(secs / 60), s = secs % 60;
  document.getElementById('victoryText').textContent =
    `Cristaux retrouvés, braseros rallumés, Gardien des Brumes terrassé : tu as sauvé l'Île Oubliée en ${m > 0 ? m + ' min ' : ''}${s} s. Les anciens chanteront ton nom !`;
  const pos = player.position;
  for (let i = 0; i < 5; i++) {
    setTimeout(() => {
      spawnBurst(new THREE.Vector3(
        pos.x + (Math.random() - 0.5) * 6, pos.y + 2 + Math.random() * 3, pos.z + (Math.random() - 0.5) * 6
      ), [0xffe27a, 0xff9e5e, 0x9fe0ff, 0xa78bfa, 0x8be29b][i], 34, 7);
    }, i * 300);
  }
  setTimeout(() => document.getElementById('victory').classList.add('show'), 1500);
}

// ------------------------------------------------------------
//  Contrôles : joystick tactile + clavier + drag caméra
// ------------------------------------------------------------
const input = { x: 0, z: 0 };           // vecteur joystick (-1..1)
const keys = {};
let camYaw = 0;                          // caméra derrière le joueur au départ
let camPitch = 0.32;

let joyTouchId = null, camTouchId = null;
let joyOrigin = { x: 0, y: 0 };
const JOY_RADIUS = 48;

function onTouchStart(e) {
  audioInit();
  for (const t of e.changedTouches) {
    if (activeDialogue) { advanceDialogue(); continue; }
    const isLeft = t.clientX < window.innerWidth * 0.5;
    if (isLeft && joyTouchId === null) {
      joyTouchId = t.identifier;
      joyOrigin = { x: t.clientX, y: t.clientY };
      ui.joy.style.display = 'block';
      ui.joy.style.left = (t.clientX - 60) + 'px';
      ui.joy.style.top = (t.clientY - 60) + 'px';
      ui.joyStick.style.transform = 'translate(-50%,-50%)';
    } else if (camTouchId === null) {
      camTouchId = t.identifier;
      camLast = { x: t.clientX, y: t.clientY };
    }
  }
}
let camLast = { x: 0, y: 0 };
function onTouchMove(e) {
  for (const t of e.changedTouches) {
    if (t.identifier === joyTouchId) {
      let dx = t.clientX - joyOrigin.x;
      let dy = t.clientY - joyOrigin.y;
      const len = Math.hypot(dx, dy);
      if (len > JOY_RADIUS) { dx = dx / len * JOY_RADIUS; dy = dy / len * JOY_RADIUS; }
      ui.joyStick.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
      input.x = dx / JOY_RADIUS;
      input.z = dy / JOY_RADIUS;
    } else if (t.identifier === camTouchId) {
      const dx = t.clientX - camLast.x;
      const dy = t.clientY - camLast.y;
      camLast = { x: t.clientX, y: t.clientY };
      camYaw -= dx * 0.008;
      camPitch = THREE.MathUtils.clamp(camPitch + dy * 0.005, 0.08, 0.9);
    }
  }
  e.preventDefault();
}
function onTouchEnd(e) {
  for (const t of e.changedTouches) {
    if (t.identifier === joyTouchId) {
      joyTouchId = null;
      input.x = 0; input.z = 0;
      ui.joy.style.display = 'none';
    } else if (t.identifier === camTouchId) {
      camTouchId = null;
    }
  }
}
const cv = renderer.domElement;
cv.addEventListener('touchstart', onTouchStart, { passive: false });
cv.addEventListener('touchmove', onTouchMove, { passive: false });
cv.addEventListener('touchend', onTouchEnd);
cv.addEventListener('touchcancel', onTouchEnd);

// Souris (desktop) : drag pour la caméra
let mouseDown = false, mouseLast = { x: 0, y: 0 };
cv.addEventListener('mousedown', e => {
  audioInit();
  if (activeDialogue) { advanceDialogue(); return; }
  mouseDown = true; mouseLast = { x: e.clientX, y: e.clientY };
});
window.addEventListener('mousemove', e => {
  if (!mouseDown) return;
  camYaw -= (e.clientX - mouseLast.x) * 0.006;
  camPitch = THREE.MathUtils.clamp(camPitch + (e.clientY - mouseLast.y) * 0.004, 0.08, 0.9);
  mouseLast = { x: e.clientX, y: e.clientY };
});
window.addEventListener('mouseup', () => { mouseDown = false; });

window.addEventListener('keydown', e => {
  keys[e.code] = true;
  if (e.code.startsWith('Arrow') || e.code === 'Space') e.preventDefault();
  if ((e.code === 'KeyE' || e.code === 'Space' || e.code === 'Enter')) {
    audioInit();
    if (activeDialogue) advanceDialogue();
    else if (currentInteract) doInteract();
  }
  if (e.code === 'KeyF') { audioInit(); doAttack(); }
});
window.addEventListener('keyup', e => { keys[e.code] = false; });

function keyboardInput() {
  let x = 0, z = 0;
  if (keys.KeyW || keys.KeyZ || keys.ArrowUp) z -= 1;
  if (keys.KeyS || keys.ArrowDown) z += 1;
  if (keys.KeyA || keys.KeyQ || keys.ArrowLeft) x -= 1;
  if (keys.KeyD || keys.ArrowRight) x += 1;
  if (x || z) {
    const l = Math.hypot(x, z);
    input.x = x / l; input.z = z / l;
    return true;
  }
  return false;
}

// ------------------------------------------------------------
//  Interactions contextuelles
// ------------------------------------------------------------
let currentInteract = null; // { label, action }
function updateInteractables() {
  if (activeDialogue || ['opening', 'dawn', 'done'].includes(quest.stage)) {
    currentInteract = null; ui.actionBtn.style.display = 'none'; return;
  }
  const p = player.position;
  let next = null;

  const dSage = p.distanceTo(sage.position);
  if (dSage < 3.2) {
    if (quest.stage === 'intro') next = { label: '💬 Parler', action: () => openDialogue('sageIntro') };
    else if (quest.stage === 'collect' && quest.collected < CRYSTAL_COUNT) next = { label: '💬 Parler', action: () => openDialogue('sageWait') };
    else if (quest.stage === 'collect') next = { label: '💬 Parler', action: () => openDialogue('sageDone') };
    else if (quest.stage === 'temple') next = { label: '💬 Parler', action: () => openDialogue('sageAfter') };
    else if (quest.stage === 'braziers') next = { label: '💬 Parler', action: () => openDialogue('sageNight') };
    else if (quest.stage === 'boss') next = { label: '💬 Parler', action: () => openDialogue('sageBoss') };
  }

  if (!next && quest.stage === 'temple') {
    const dDoor = Math.hypot(p.x - doorSpot.x, p.z - doorSpot.z);
    if (dDoor < 4.5) next = { label: '🗝️ Ouvrir', action: openTemple };
  }

  if (!next && quest.stage === 'braziers') {
    for (const b of braziers) {
      if (b.lit) continue;
      if (Math.hypot(p.x - b.x, p.z - b.z) < 2.8) {
        next = { label: '🔥 Allumer', action: () => lightBrazier(b) };
        break;
      }
    }
  }

  currentInteract = next;
  if (next) {
    ui.actionBtn.textContent = next.label;
    ui.actionBtn.style.display = 'flex';
  } else {
    ui.actionBtn.style.display = 'none';
  }
}
function doInteract() {
  if (currentInteract) currentInteract.action();
}
ui.actionBtn.addEventListener('pointerdown', e => { e.stopPropagation(); e.preventDefault(); audioInit(); doInteract(); });
ui.attackBtn.addEventListener('pointerdown', e => { e.stopPropagation(); e.preventDefault(); audioInit(); doAttack(); });

function openTemple() {
  if (quest.stage !== 'temple') return;
  quest.stage = 'opening';
  sfx.door();
  setBanner('🏛️ La porte du temple s\'ouvre…');
  ui.actionBtn.style.display = 'none';
}

function collectCrystal(c) {
  c.taken = true;
  quest.collected++;
  ui.counterTxt.textContent = `${quest.collected} / ${CRYSTAL_COUNT}`;
  spawnBurst(c.mesh.position.clone(), 0x9fe0ff, 30, 6);
  sfx.collect();
  scene.remove(c.mesh);
  if (quest.collected >= CRYSTAL_COUNT) {
    setBanner('✅ Tous les cristaux ! Retourne voir le <b>Sage</b>');
    sfx.quest();
    toast('5 / 5 cristaux !');
  } else {
    toast(`Cristal ${quest.collected} / ${CRYSTAL_COUNT}`);
  }
  saveGame('collect');
}

// ------------------------------------------------------------
//  Mise à jour des spectres
// ------------------------------------------------------------
function updateEnemies(dt, t) {
  const p = player.position;
  const frozen = !!activeDialogue || ['dawn', 'done'].includes(quest.stage);
  for (let i = enemies.length - 1; i >= 0; i--) {
    const e = enemies[i];
    if (e.dead) continue;
    const g = e.group;
    if (e.dying !== null) {
      e.dying -= dt;
      const op = Math.max(0, e.dying / 0.6);
      for (const m of e.mats) m.opacity = op * 0.82;
      g.position.y += dt * 1.5;
      if (e.dying <= 0) {
        e.dead = true;
        scene.remove(g);
      }
      continue;
    }
    if (!frozen) {
      const dx = p.x - g.position.x, dz = p.z - g.position.z;
      const d = Math.hypot(dx, dz);
      if (d < e.aggro) {
        const s = e.speed * dt;
        if (d > 0.01) {
          g.position.x += dx / d * s;
          g.position.z += dz / d * s;
          g.rotation.y = Math.atan2(dx, dz);
        }
        if (d < (e.boss ? 2.0 : 1.2)) damagePlayer(e);
      } else {
        g.position.x += Math.sin(t * 0.5 + e.phase) * dt * 0.5;
        g.position.z += Math.cos(t * 0.4 + e.phase) * dt * 0.5;
      }
      const dc = Math.hypot(g.position.x, g.position.z);
      if (dc > WALK_R) {
        g.position.x = g.position.x / dc * WALK_R;
        g.position.z = g.position.z / dc * WALK_R;
      }
    }
    g.position.y = Math.max(terrainH(g.position.x, g.position.z), 0.05) + 0.55 + Math.sin(t * 2.4 + e.phase) * 0.15;
  }
}

// ------------------------------------------------------------
//  Boucle de jeu
// ------------------------------------------------------------
const clock = new THREE.Clock();
let started = false;

function tick() {
  requestAnimationFrame(tick);
  const dt = Math.min(clock.getDelta(), 0.05);
  const t = clock.elapsedTime;

  // --- clavier actif seulement quand le joystick tactile est relâché ---
  if (joyTouchId === null) {
    input.x = 0; input.z = 0;
    keyboardInput();
  }

  // --- déplacement joueur ---
  const mag = Math.min(1, Math.hypot(input.x, input.z));
  const moving = mag > 0.12 && !activeDialogue && quest.stage !== 'done';
  if (moving) {
    // direction relative à la caméra (avant = s'éloigner de la caméra)
    const sin = Math.sin(camYaw), cos = Math.cos(camYaw);
    const dx = input.x * cos + input.z * sin;
    const dz = -input.x * sin + input.z * cos;
    const targetAngle = Math.atan2(dx, dz);
    let da = targetAngle - pState.angle;
    while (da > Math.PI) da -= Math.PI * 2;
    while (da < -Math.PI) da += Math.PI * 2;
    pState.angle += da * Math.min(1, dt * 12);
    player.rotation.y = pState.angle;

    const speed = PLAYER_SPEED * mag;
    let nx = player.position.x + Math.sin(pState.angle) * speed * dt;
    let nz = player.position.z + Math.cos(pState.angle) * speed * dt;

    // limites de l'île
    const dCenter = Math.hypot(nx, nz);
    if (dCenter > WALK_R) { nx = nx / dCenter * WALK_R; nz = nz / dCenter * WALK_R; }

    // collisions simples (cercles)
    for (const c of colliders) {
      const ddx = nx - c.x, ddz = nz - c.z;
      const d = Math.hypot(ddx, ddz);
      const minD = c.r + 0.45;
      if (d < minD && d > 0.001) {
        nx = c.x + ddx / d * minD;
        nz = c.z + ddz / d * minD;
      }
    }

    player.position.x = nx;
    player.position.z = nz;
    pState.bob += dt * speed * 1.6;
  }

  // hauteur du terrain (ne pas descendre dans l'eau)
  const groundY = Math.max(terrainH(player.position.x, player.position.z), 0.05);
  player.position.y += (groundY - player.position.y) * Math.min(1, dt * 14);

  // animation des membres (+ coup d'épée)
  const limbs = player.userData.limbs;
  const swing = moving ? Math.sin(pState.bob * 4) * 0.55 : 0;
  limbs.armL.rotation.x = swing;
  limbs.legL.rotation.x = -swing;
  limbs.legR.rotation.x = swing;
  if (attackT > 0) {
    attackT -= dt;
    const k = 1 - Math.max(attackT, 0) / 0.38;
    limbs.armR.rotation.x = -Math.sin(k * Math.PI) * 2.3;
  } else {
    limbs.armR.rotation.x = -swing;
  }

  // clignotement d'invulnérabilité
  player.visible = performance.now() > invulnUntil || Math.floor(t * 12) % 2 === 0;

  // sage : respiration
  sage.position.y = terrainH(sage.position.x, sage.position.z) + Math.sin(t * 1.6) * 0.03;

  // cristaux : flottement
  for (const c of crystals) {
    if (c.taken) continue;
    c.mesh.position.y = c.baseY + Math.sin(t * 2 + c.phase) * 0.25;
    c.mesh.rotation.y = t * 1.4 + c.phase;
    if (quest.stage === 'collect' &&
        player.position.distanceTo(c.mesh.position) < 1.9) {
      collectCrystal(c);
    }
  }

  // lucioles scintillent (plus visibles la nuit)
  fireflies.material.opacity = 0.5 + Math.sin(t * 2.2) * 0.35 + night01 * 0.3;
  fireflies.rotation.y = Math.sin(t * 0.05) * 0.02;

  // nuages
  for (const cl of clouds) {
    cl.position.x += cl.userData.speed * dt;
    if (cl.position.x > 130) cl.position.x = -130;
  }

  // flammes des braseros
  for (let i = 0; i < braziers.length; i++) {
    const b = braziers[i];
    if (b.lit) b.flame.scale.setScalar(1 + Math.sin(t * 13 + i * 2) * 0.12);
  }

  // ouverture de la porte
  if (quest.stage === 'opening') {
    doorOpenAnim += dt;
    templeDoor.position.y = Math.max(3.8 - doorOpenAnim * 1.4, -1.6);
    if (templeDoor.position.y <= -1.55 && templeDoor.visible) {
      templeDoor.visible = false; // une seule fois
      openDialogue('templeVoice');
    }
  }
  // trésor qui tourne
  treasureRef.rotation.y = t * 0.8;
  treasureRef.position.y = 2.6 + Math.sin(t * 1.5) * 0.15;

  // spectres
  updateEnemies(dt, t);

  // transition jour/nuit
  if (Math.abs(night01 - nightTarget) > 0.001) {
    night01 += Math.sign(nightTarget - night01) * Math.min(dt * 0.25, Math.abs(nightTarget - night01));
    applyMood();
  }

  updateBursts(dt);
  updateInteractables();

  // --- caméra 3e personne ---
  const camDist = 7.5;
  const target = new THREE.Vector3(
    player.position.x, player.position.y + 1.6, player.position.z
  );
  const desired = new THREE.Vector3(
    target.x + Math.sin(camYaw) * Math.cos(camPitch) * camDist,
    target.y + Math.sin(camPitch) * camDist,
    target.z + Math.cos(camYaw) * Math.cos(camPitch) * camDist
  );
  const minY = Math.max(terrainH(desired.x, desired.z), 0) + 0.7;
  if (desired.y < minY) desired.y = minY;
  camera.position.lerp(desired, started ? Math.min(1, dt * 6) : 1);
  camera.lookAt(target);
  started = true;

  renderer.render(scene, camera);
}
tick();

// ------------------------------------------------------------
//  Restauration d'une sauvegarde
// ------------------------------------------------------------
function applySave(s) {
  quest.priorMs = s.playMs || 0;
  quest.startTime = performance.now();
  const inAct2 = s.stage === 'braziers' || s.stage === 'boss';
  const takenAll = s.stage !== 'collect';

  for (let i = 0; i < crystals.length; i++) {
    if (takenAll || s.taken.includes(i)) {
      crystals[i].taken = true;
      scene.remove(crystals[i].mesh);
    }
  }
  quest.collected = crystals.filter(c => c.taken).length;
  ui.counter.style.display = 'flex';
  ui.counterTxt.textContent = `${quest.collected} / ${CRYSTAL_COUNT}`;

  if (s.stage === 'collect') {
    quest.stage = 'collect';
    setBanner(quest.collected >= CRYSTAL_COUNT
      ? '✅ Tous les cristaux ! Retourne voir le <b>Sage</b>'
      : "🔍 Retrouve les <b>5 cristaux</b> dispersés sur l'île");
  } else if (s.stage === 'temple') {
    quest.stage = 'temple';
    setBanner("🗝️ Ouvre la <b>porte du temple</b>, au nord de l'île");
  } else if (inAct2) {
    // porte déjà ouverte
    templeDoor.visible = false;
    night01 = 1; nightTarget = 1;
    applyMood();
    sword.visible = true;
    ui.hearts.style.display = 'flex';
    ui.attackBtn.style.display = 'flex';
    renderHearts();
    for (const i of (s.lit || [])) {
      braziers[i].lit = true;
      braziers[i].flame.visible = true;
    }
    spawnEnemies();
    if (s.stage === 'boss') {
      quest.stage = 'boss';
      spawnBoss();
      bossBanner();
    } else {
      quest.stage = 'braziers';
      brazierBanner();
    }
  }
}

// ------------------------------------------------------------
//  UI : démarrage, rejouer, redimensionnement
// ------------------------------------------------------------
setBanner("🌴 Bienvenue ! Va parler au <b>Sage</b> au chapeau violet");

const pendingSave = loadSave();
const continueBtn = document.getElementById('continueBtn');
if (pendingSave) continueBtn.style.display = 'inline-block';

function closeIntro() {
  document.getElementById('intro').classList.add('hide');
  setTimeout(() => document.getElementById('intro').style.display = 'none', 700);
}
document.getElementById('startBtn').addEventListener('click', () => {
  audioInit();
  clearSave();
  sfx.quest();
  closeIntro();
});
continueBtn.addEventListener('click', () => {
  audioInit();
  if (pendingSave) applySave(pendingSave);
  sfx.quest();
  closeIntro();
});
document.getElementById('replayBtn').addEventListener('click', () => {
  clearSave();
  location.reload();
});

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// iOS : re-layout après rotation
window.addEventListener('orientationchange', () => {
  setTimeout(() => window.dispatchEvent(new Event('resize')), 300);
});

// Accès debug (tests automatisés) — sans effet sur le jeu
window.__game = {
  player, quest, crystals, sage, doorSpot, braziers, enemies,
  doAttack, getHearts: () => hearts, getNight: () => night01,
};
