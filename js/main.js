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
    Math.cos(x * 0.017 - z * 0.023) * 1.2 +
    Math.sin(x * 0.21 + 1.7) * Math.cos(z * 0.19 - 0.6) * 0.35;
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
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.12;
document.getElementById('game').appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0xbfe0f2, 60, 165);

const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 700);

// Lumières
const hemi = new THREE.HemisphereLight(0xcfe8ff, 0x5a7a48, 0.9);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff2d0, 1.9);
sun.position.set(32, 52, 18);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = -30; sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30; sun.shadow.camera.bottom = -30;
sun.shadow.camera.near = 1; sun.shadow.camera.far = 160;
sun.shadow.bias = -0.0012;
sun.shadow.normalBias = 0.5;
scene.add(sun);
scene.add(sun.target);

// ------------------------------------------------------------
//  Textures générées (halos, fumée, lune, runes)
// ------------------------------------------------------------
function makeGlowTexture(inner = 'rgba(255,255,255,0.9)', mid = 'rgba(160,220,255,0.35)') {
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(32, 32, 2, 32, 32, 30);
  grad.addColorStop(0, inner);
  grad.addColorStop(0.4, mid);
  grad.addColorStop(1, 'rgba(160,220,255,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}
function makeSmokeTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(32, 32, 4, 32, 32, 30);
  grad.addColorStop(0, 'rgba(200,200,210,0.55)');
  grad.addColorStop(0.6, 'rgba(180,180,195,0.22)');
  grad.addColorStop(1, 'rgba(180,180,195,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}
function makeMoonTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(64, 64, 8, 64, 64, 62);
  grad.addColorStop(0, 'rgba(240,244,255,1)');
  grad.addColorStop(0.75, 'rgba(214,222,244,1)');
  grad.addColorStop(0.92, 'rgba(190,200,235,0.6)');
  grad.addColorStop(1, 'rgba(190,200,235,0)');
  ctx.fillStyle = grad;
  ctx.beginPath(); ctx.arc(64, 64, 62, 0, 7); ctx.fill();
  ctx.fillStyle = 'rgba(160,172,210,0.5)';
  for (const [x, y, r] of [[45, 42, 9], [82, 60, 12], [58, 88, 7], [88, 92, 5], [38, 72, 5], [70, 32, 5]]) {
    ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
  }
  return new THREE.CanvasTexture(c);
}
function makeRunesTexture() {
  const c = document.createElement('canvas');
  c.width = 128; c.height = 192;
  const ctx = c.getContext('2d');
  const grad = ctx.createLinearGradient(0, 0, 0, 192);
  grad.addColorStop(0, '#d8b258'); grad.addColorStop(0.5, '#c49a3e'); grad.addColorStop(1, '#a87f2e');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 128, 192);
  // panneaux
  ctx.strokeStyle = 'rgba(90,60,10,0.8)'; ctx.lineWidth = 5;
  ctx.strokeRect(12, 12, 104, 168);
  ctx.strokeRect(24, 24, 80, 60);
  ctx.strokeRect(24, 100, 80, 60);
  // runes
  ctx.strokeStyle = '#fff0b8'; ctx.lineWidth = 3.5; ctx.lineCap = 'round';
  ctx.shadowColor = '#ffdf8a'; ctx.shadowBlur = 6;
  ctx.beginPath();
  ctx.arc(64, 54, 16, 0, 7);
  ctx.moveTo(64, 38); ctx.lineTo(64, 70);
  ctx.moveTo(40, 118); ctx.lineTo(64, 148); ctx.lineTo(88, 118);
  ctx.moveTo(64, 148); ctx.lineTo(64, 112);
  ctx.stroke();
  return new THREE.CanvasTexture(c);
}
const glowTex = makeGlowTexture();
const smokeTex = makeSmokeTexture();

// ------------------------------------------------------------
//  Ciel : dôme en shader (jour/nuit), soleil, lune, étoiles
// ------------------------------------------------------------
const skyU = {
  uNight: { value: 0 },
  uSunDir: { value: new THREE.Vector3(32, 52, 18).normalize() },
};
{
  const skyMat = new THREE.ShaderMaterial({
    uniforms: skyU,
    side: THREE.BackSide,
    depthWrite: false,
    fog: false,
    vertexShader: `
      varying vec3 vDir;
      void main(){
        vDir = position;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: `
      uniform float uNight;
      uniform vec3 uSunDir;
      varying vec3 vDir;
      void main(){
        vec3 nd = normalize(vDir);
        float h = clamp(nd.y, -1.0, 1.0);
        vec3 dayZen = vec3(0.28, 0.58, 0.86);
        vec3 dayHor = vec3(0.86, 0.93, 0.96);
        vec3 nightZen = vec3(0.015, 0.03, 0.09);
        vec3 nightHor = vec3(0.09, 0.13, 0.26);
        float g = pow(smoothstep(-0.05, 0.6, h), 0.75);
        vec3 day = mix(dayHor, dayZen, g);
        vec3 night = mix(nightHor, nightZen, g);
        vec3 col = mix(day, night, uNight);
        float s = max(dot(nd, uSunDir), 0.0);
        col += vec3(1.0, 0.82, 0.55) * pow(s, 60.0) * (1.0 - uNight) * 0.55;
        col += vec3(1.0, 0.95, 0.8) * pow(s, 700.0) * (1.0 - uNight) * 2.4;
        // teinte chaude à l'horizon le jour
        col += vec3(0.35, 0.18, 0.05) * (1.0 - uNight) * pow(1.0 - abs(h), 6.0) * 0.5;
        gl_FragColor = vec4(col, 1.0);
      }`,
  });
  const sky = new THREE.Mesh(new THREE.SphereGeometry(420, 32, 18), skyMat);
  scene.add(sky);
}

// Étoiles
let stars;
{
  const N = 400;
  const positions = new Float32Array(N * 3);
  const srng = mulberry32(4242);
  for (let i = 0; i < N; i++) {
    const a = srng() * Math.PI * 2;
    const e = Math.asin(srng() * 0.95 + 0.05);
    const r = 400;
    positions[i * 3] = Math.cos(a) * Math.cos(e) * r;
    positions[i * 3 + 1] = Math.sin(e) * r;
    positions[i * 3 + 2] = Math.sin(a) * Math.cos(e) * r;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  stars = new THREE.Points(geo, new THREE.PointsMaterial({
    color: 0xdfe8ff, size: 1.7, sizeAttenuation: false,
    transparent: true, opacity: 0, depthWrite: false, fog: false,
  }));
  scene.add(stars);
}

// Soleil et lune (sprites)
let sunSprite, moon;
{
  sunSprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture('rgba(255,246,214,1)', 'rgba(255,214,130,0.5)'),
    transparent: true, opacity: 0.95, depthWrite: false, fog: false,
    blending: THREE.AdditiveBlending,
  }));
  sunSprite.scale.setScalar(90);
  sunSprite.position.copy(skyU.uSunDir.value).multiplyScalar(400);
  scene.add(sunSprite);

  moon = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeMoonTexture(), transparent: true, opacity: 0, depthWrite: false, fog: false,
  }));
  moon.scale.setScalar(52);
  moon.position.set(-160, 240, -300);
  scene.add(moon);
}

// ------------------------------------------------------------
//  Jour / Nuit (les Brumes de l'acte 2)
// ------------------------------------------------------------
const MOOD = {
  dayFog: new THREE.Color(0xbfe0f2), nightFog: new THREE.Color(0x121c33),
  daySun: new THREE.Color(0xfff2d0), nightSun: new THREE.Color(0x8fa8ff),
  dayHemiSky: new THREE.Color(0xcfe8ff), nightHemiSky: new THREE.Color(0x2a3a66),
  dayHemiGnd: new THREE.Color(0x5a7a48), nightHemiGnd: new THREE.Color(0x18203a),
};
let night01 = 0;      // 0 = jour, 1 = nuit
let nightTarget = 0;

function applyMood() {
  skyU.uNight.value = night01;
  waterU.uNight.value = night01;
  scene.fog.color.lerpColors(MOOD.dayFog, MOOD.nightFog, night01);
  scene.fog.near = 60 - night01 * 28;
  scene.fog.far = 165 - night01 * 70;
  hemi.intensity = 0.9 - night01 * 0.44;
  hemi.color.lerpColors(MOOD.dayHemiSky, MOOD.nightHemiSky, night01);
  hemi.groundColor.lerpColors(MOOD.dayHemiGnd, MOOD.nightHemiGnd, night01);
  sun.intensity = 1.9 - night01 * 1.2;
  sun.color.lerpColors(MOOD.daySun, MOOD.nightSun, night01);
  stars.material.opacity = night01;
  sunSprite.material.opacity = (1 - night01) * 0.95;
  moon.material.opacity = night01 * 0.98;
}

// ------------------------------------------------------------
//  Terrain low-poly facetté, coloré par altitude
// ------------------------------------------------------------
{
  const seg = 104;
  let geo = new THREE.PlaneGeometry(ISLAND_R * 2.7, ISLAND_R * 2.7, seg, seg);
  geo.rotateX(-Math.PI / 2);
  const pos0 = geo.attributes.position;
  for (let i = 0; i < pos0.count; i++) {
    pos0.setY(i, terrainH(pos0.getX(i), pos0.getZ(i)));
  }
  // géométrie non indexée -> facettes plates, une couleur par triangle
  geo = geo.toNonIndexed();
  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  const crng = mulberry32(777);
  const cWet = new THREE.Color(0xd9bd82);
  const cSand = new THREE.Color(0xf0dca4);
  const cGrassA = new THREE.Color(0x7cc457);
  const cGrassB = new THREE.Color(0x4d9b48);
  const cGrassC = new THREE.Color(0x3a7f42);
  const cDirt = new THREE.Color(0x9a8562);
  const cRock = new THREE.Color(0x939099);
  const cSnow = new THREE.Color(0xdadde5);
  const tmp = new THREE.Color();
  for (let f = 0; f < pos.count; f += 3) {
    const hAvg = (pos.getY(f) + pos.getY(f + 1) + pos.getY(f + 2)) / 3;
    const xAvg = (pos.getX(f) + pos.getX(f + 1) + pos.getX(f + 2)) / 3;
    const zAvg = (pos.getZ(f) + pos.getZ(f + 1) + pos.getZ(f + 2)) / 3;
    const n = Math.sin(xAvg * 0.6) * Math.cos(zAvg * 0.55) * 0.18;
    if (hAvg < 0.02) tmp.copy(cWet);
    else if (hAvg < 0.42 + n) tmp.copy(cWet).lerp(cSand, Math.min(1, hAvg / 0.35));
    else if (hAvg < 1.6 + n) tmp.copy(cGrassA).lerp(cGrassB, (hAvg - 0.42) / 1.2);
    else if (hAvg < 2.9 + n) tmp.copy(cGrassB).lerp(cGrassC, (hAvg - 1.6) / 1.3);
    else if (hAvg < 3.8 + n) tmp.copy(cGrassC).lerp(cDirt, (hAvg - 2.9) / 0.9);
    else if (hAvg < 4.6 + n) tmp.copy(cDirt).lerp(cRock, (hAvg - 3.8) / 0.8);
    else tmp.copy(cRock).lerp(cSnow, Math.min(1, (hAvg - 4.6) / 1.2));
    // variation par facette (aspect low-poly stylisé)
    const j = (crng() - 0.5) * 0.07;
    tmp.offsetHSL(j * 0.15, j * 0.4, j);
    for (let k = 0; k < 3; k++) {
      colors[(f + k) * 3] = tmp.r;
      colors[(f + k) * 3 + 1] = tmp.g;
      colors[(f + k) * 3 + 2] = tmp.b;
    }
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  const terrain = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true }));
  terrain.receiveShadow = true;
  scene.add(terrain);
}

// ------------------------------------------------------------
//  Océan en shader : vagues, écume au rivage, reflets
// ------------------------------------------------------------
const waterU = THREE.UniformsUtils.merge([
  THREE.UniformsLib.fog,
  { uTime: { value: 0 }, uNight: { value: 0 } },
]);
{
  const geo = new THREE.PlaneGeometry(520, 520, 56, 56);
  const mat = new THREE.ShaderMaterial({
    uniforms: waterU,
    transparent: true,
    fog: true,
    vertexShader: `
      uniform float uTime;
      varying vec2 vXZ;
      varying float vW;
      #include <fog_pars_vertex>
      void main(){
        vec3 p = position;
        float w = sin(p.x * 0.14 + uTime * 1.2) * 0.5
                + cos(p.y * 0.11 - uTime * 0.9) * 0.5
                + sin((p.x + p.y) * 0.07 + uTime * 0.6) * 0.5;
        p.z += w * 0.28;
        vW = w;
        vXZ = position.xy;
        vec4 mvPosition = modelViewMatrix * vec4(p, 1.0);
        gl_Position = projectionMatrix * mvPosition;
        #include <fog_vertex>
      }`,
    fragmentShader: `
      uniform float uTime;
      uniform float uNight;
      varying vec2 vXZ;
      varying float vW;
      #include <fog_pars_fragment>
      void main(){
        float d = length(vXZ);
        vec3 shallow = mix(vec3(0.30, 0.72, 0.80), vec3(0.07, 0.19, 0.34), uNight);
        vec3 deep    = mix(vec3(0.05, 0.35, 0.62), vec3(0.015, 0.07, 0.18), uNight);
        vec3 col = mix(shallow, deep, smoothstep(56.0, 130.0, d));
        // crêtes scintillantes
        float sp = sin(vXZ.x * 0.55 + uTime * 1.7) * cos(vXZ.y * 0.5 - uTime * 1.3);
        col += vec3(0.55, 0.75, 0.85) * smoothstep(0.86, 1.0, sp) * (0.28 - 0.18 * uNight);
        col += vW * 0.035;
        // écume qui vient lécher le rivage
        float foamBand = smoothstep(63.0, 58.5, d) * smoothstep(54.0, 57.5, d);
        float foamWave = 0.5 + 0.5 * sin(d * 1.9 - uTime * 2.2 + sin(atan(vXZ.y, vXZ.x) * 8.0) * 0.7);
        float foam = foamBand * smoothstep(0.55, 0.95, foamWave);
        col = mix(col, vec3(0.93, 0.97, 0.98), clamp(foam, 0.0, 1.0) * (0.8 - 0.55 * uNight));
        float alpha = 0.95 - smoothstep(63.0, 57.0, d) * 0.38;
        gl_FragColor = vec4(col, alpha);
        #include <fog_fragment>
      }`,
  });
  const water = new THREE.Mesh(geo, mat);
  water.rotation.x = -Math.PI / 2;
  water.position.y = 0;
  scene.add(water);
}

// ------------------------------------------------------------
//  Décor : arbres (pins, feuillus, palmiers), rochers, herbe, fleurs
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
function randSpot(minR, maxR, minH, maxH = 99) {
  for (let tries = 0; tries < 40; tries++) {
    const a = rng() * Math.PI * 2;
    const r = minR + rng() * (maxR - minR);
    const x = Math.cos(a) * r, z = Math.sin(a) * r;
    const h = terrainH(x, z);
    if (h > minH && h < maxH && !nearReserved(x, z)) return { x, z, h };
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

// Pins (3 étages de feuillage, teintes variées)
{
  const N = 60;
  const trunkGeo = new THREE.CylinderGeometry(0.2, 0.34, 2.2, 7);
  const trunkMat = new THREE.MeshLambertMaterial({ color: 0x74513a, flatShading: true });
  const leafGeo = new THREE.ConeGeometry(1.5, 2.4, 7);
  const leafMat = new THREE.MeshLambertMaterial({ color: 0xffffff, flatShading: true });
  const trunks = new THREE.InstancedMesh(trunkGeo, trunkMat, N);
  const leaves = new THREE.InstancedMesh(leafGeo, leafMat, N * 3);
  trunks.castShadow = leaves.castShadow = true;
  const leafColor = new THREE.Color();
  let li = 0, ti = 0;
  for (let i = 0; i < N; i++) {
    const s = randSpot(10, 52, 0.7);
    if (!s) continue;
    const scale = 0.8 + rng() * 1.0;
    const lean = (rng() - 0.5) * 0.09;
    dummy.rotation.set(0, rng() * Math.PI * 2, lean);
    dummy.position.set(s.x, s.h + 1.1 * scale, s.z);
    dummy.scale.setScalar(scale);
    dummy.updateMatrix();
    trunks.setMatrixAt(ti++, dummy.matrix);
    const hue = 0.3 + rng() * 0.09;
    for (let k = 0; k < 3; k++) {
      dummy.position.set(s.x - lean * k, s.h + (2.3 + k * 1.05) * scale, s.z);
      dummy.scale.setScalar(scale * (1 - k * 0.26));
      dummy.updateMatrix();
      leaves.setMatrixAt(li, dummy.matrix);
      leafColor.setHSL(hue, 0.5 + rng() * 0.15, 0.26 + k * 0.045 + rng() * 0.05);
      leaves.setColorAt(li, leafColor);
      li++;
    }
    colliders.push({ x: s.x, z: s.z, r: 0.7 * scale });
  }
  trunks.count = ti; leaves.count = li;
  scene.add(trunks, leaves);
}

// Feuillus (boules de feuillage sur tronc)
{
  const N = 26;
  const trunkGeo = new THREE.CylinderGeometry(0.16, 0.28, 1.7, 6);
  const trunkMat = new THREE.MeshLambertMaterial({ color: 0x84604a, flatShading: true });
  const blobGeo = new THREE.IcosahedronGeometry(1.0, 0);
  const blobMat = new THREE.MeshLambertMaterial({ color: 0xffffff, flatShading: true });
  const trunks = new THREE.InstancedMesh(trunkGeo, trunkMat, N);
  const blobs = new THREE.InstancedMesh(blobGeo, blobMat, N * 3);
  trunks.castShadow = blobs.castShadow = true;
  const c = new THREE.Color();
  let bi = 0, ti = 0;
  for (let i = 0; i < N; i++) {
    const s = randSpot(8, 48, 0.6);
    if (!s) continue;
    const scale = 0.75 + rng() * 0.7;
    dummy.rotation.set(0, rng() * Math.PI * 2, 0);
    dummy.position.set(s.x, s.h + 0.85 * scale, s.z);
    dummy.scale.setScalar(scale);
    dummy.updateMatrix();
    trunks.setMatrixAt(ti++, dummy.matrix);
    const hue = 0.24 + rng() * 0.14;
    for (let k = 0; k < 3; k++) {
      const ox = (rng() - 0.5) * 1.1, oz = (rng() - 0.5) * 1.1;
      dummy.position.set(s.x + ox * scale, s.h + (1.9 + rng() * 0.7) * scale, s.z + oz * scale);
      dummy.scale.setScalar(scale * (0.7 + rng() * 0.5));
      dummy.rotation.set(rng() * 3, rng() * 3, rng() * 3);
      dummy.updateMatrix();
      blobs.setMatrixAt(bi, dummy.matrix);
      c.setHSL(hue, 0.55, 0.3 + rng() * 0.14);
      blobs.setColorAt(bi, c);
      bi++;
    }
    colliders.push({ x: s.x, z: s.z, r: 0.55 * scale });
  }
  trunks.count = ti; blobs.count = bi;
  scene.add(trunks, blobs);
}

// Palmiers de plage
{
  const trunkMat = new THREE.MeshLambertMaterial({ color: 0x9a7248, flatShading: true });
  const leafMat = new THREE.MeshLambertMaterial({ color: 0x4faf52, flatShading: true });
  const cocoMat = new THREE.MeshLambertMaterial({ color: 0x6e4a2e });
  const segGeo = new THREE.CylinderGeometry(0.13, 0.18, 1.1, 6);
  const leafGeo = new THREE.SphereGeometry(1, 5, 4);
  const cocoGeo = new THREE.SphereGeometry(0.14, 6, 5);
  for (let i = 0; i < 9; i++) {
    const s = randSpot(46, 56, 0.12, 0.75);
    if (!s) continue;
    const palm = new THREE.Group();
    const lean = 0.14 + rng() * 0.12;
    const dir = rng() * Math.PI * 2;
    let px = 0, py = 0, pz = 0;
    for (let k = 0; k < 4; k++) {
      const seg = new THREE.Mesh(segGeo, trunkMat);
      const a = lean * (k + 1) * 0.55;
      px += Math.sin(a) * Math.cos(dir) * 0.9;
      pz += Math.sin(a) * Math.sin(dir) * 0.9;
      py += Math.cos(a) * 0.95;
      seg.position.set(px, py - 0.45, pz);
      seg.rotation.set(Math.sin(dir) * a, 0, -Math.cos(dir) * a);
      seg.castShadow = true;
      palm.add(seg);
    }
    for (let k = 0; k < 7; k++) {
      const leaf = new THREE.Mesh(leafGeo, leafMat);
      const la = (k / 7) * Math.PI * 2;
      leaf.scale.set(1.5, 0.05, 0.42);
      leaf.position.set(px + Math.cos(la) * 1.1, py + 0.15, pz + Math.sin(la) * 1.1);
      leaf.rotation.set(0, -la, -0.35);
      leaf.castShadow = true;
      palm.add(leaf);
    }
    for (let k = 0; k < 3; k++) {
      const coco = new THREE.Mesh(cocoGeo, cocoMat);
      coco.position.set(px + (rng() - 0.5) * 0.4, py - 0.15, pz + (rng() - 0.5) * 0.4);
      palm.add(coco);
    }
    palm.position.set(s.x, s.h, s.z);
    scene.add(palm);
    colliders.push({ x: s.x, z: s.z, r: 0.5 });
  }
}

// Rochers (teintes variées)
{
  const N = 26;
  const geo = new THREE.IcosahedronGeometry(0.9, 0);
  const mat = new THREE.MeshLambertMaterial({ color: 0xffffff, flatShading: true });
  const rocks = new THREE.InstancedMesh(geo, mat, N);
  rocks.castShadow = true;
  const c = new THREE.Color();
  let ri = 0;
  for (let i = 0; i < N; i++) {
    const s = randSpot(8, 54, 0.15);
    if (!s) continue;
    const sc = 0.5 + rng() * 1.3;
    dummy.position.set(s.x, s.h + sc * 0.3, s.z);
    dummy.scale.set(sc, sc * (0.6 + rng() * 0.5), sc);
    dummy.rotation.set(rng(), rng() * Math.PI * 2, rng());
    dummy.updateMatrix();
    rocks.setMatrixAt(ri, dummy.matrix);
    c.setHSL(0.08 + rng() * 0.55, 0.03 + rng() * 0.06, 0.5 + rng() * 0.16);
    rocks.setColorAt(ri, c);
    ri++;
    if (sc > 0.8) colliders.push({ x: s.x, z: s.z, r: sc * 0.8 });
  }
  rocks.count = ri;
  scene.add(rocks);
}

// Touffes d'herbe
{
  const N = 320;
  const geo = new THREE.ConeGeometry(0.05, 0.42, 4);
  const mat = new THREE.MeshLambertMaterial({ color: 0xffffff });
  const grass = new THREE.InstancedMesh(geo, mat, N);
  const c = new THREE.Color();
  let gi = 0;
  for (let i = 0; i < N; i++) {
    const s = randSpot(5, 52, 0.5);
    if (!s) continue;
    dummy.position.set(s.x, s.h + 0.18, s.z);
    dummy.scale.set(1, 0.7 + rng() * 0.9, 1);
    dummy.rotation.set((rng() - 0.5) * 0.4, rng() * 3, (rng() - 0.5) * 0.4);
    dummy.updateMatrix();
    grass.setMatrixAt(gi, dummy.matrix);
    c.setHSL(0.26 + rng() * 0.09, 0.5, 0.3 + rng() * 0.15);
    grass.setColorAt(gi, c);
    gi++;
  }
  grass.count = gi;
  scene.add(grass);
}

// Fleurs (tige + corolle)
{
  const N = 80;
  const stemGeo = new THREE.CylinderGeometry(0.02, 0.03, 0.34, 4);
  const stemMat = new THREE.MeshLambertMaterial({ color: 0x3f8a3c });
  const headGeo = new THREE.SphereGeometry(0.1, 6, 5);
  const headMat = new THREE.MeshLambertMaterial({ color: 0xffffff });
  const stems = new THREE.InstancedMesh(stemGeo, stemMat, N);
  const heads = new THREE.InstancedMesh(headGeo, headMat, N);
  const palette = [0xff6b8d, 0xffd166, 0xa78bfa, 0xfff6f0, 0xff9e5e, 0x7ae0ff];
  const c = new THREE.Color();
  let fi = 0;
  for (let i = 0; i < N; i++) {
    const s = randSpot(6, 50, 0.5);
    if (!s) continue;
    const sc = 0.8 + rng() * 0.7;
    dummy.rotation.set(0, 0, 0);
    dummy.position.set(s.x, s.h + 0.17 * sc, s.z);
    dummy.scale.setScalar(sc);
    dummy.updateMatrix();
    stems.setMatrixAt(fi, dummy.matrix);
    dummy.position.y = s.h + 0.38 * sc;
    dummy.scale.set(sc, sc * 0.7, sc);
    dummy.updateMatrix();
    heads.setMatrixAt(fi, dummy.matrix);
    heads.setColorAt(fi, c.setHex(palette[(rng() * palette.length) | 0]));
    fi++;
  }
  stems.count = heads.count = fi;
  scene.add(stems, heads);
}

// Lucioles (points scintillants)
let fireflies;
{
  const N = 70;
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
    map: glowTex, color: 0xfff7b0, size: 0.5, transparent: true, opacity: 0.9,
    blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  scene.add(fireflies);
}

// Pollen / poussière dorée en journée
let dust;
{
  const N = 45;
  const positions = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const s = randSpot(4, 46, 0.3) || { x: 0, z: 0, h: 1 };
    positions[i * 3] = s.x;
    positions[i * 3 + 1] = s.h + 0.8 + rng() * 2.5;
    positions[i * 3 + 2] = s.z;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  dust = new THREE.Points(geo, new THREE.PointsMaterial({
    map: glowTex, color: 0xfff2c8, size: 0.3, transparent: true, opacity: 0.45,
    blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  scene.add(dust);
}

// Nuages low-poly
const clouds = [];
{
  const mat = new THREE.MeshLambertMaterial({
    color: 0xffffff, flatShading: true, transparent: true, opacity: 0.92,
    emissive: 0x9aa8c0, emissiveIntensity: 0.25,
  });
  for (let i = 0; i < 9; i++) {
    const g = new THREE.Group();
    const n = 3 + ((rng() * 3) | 0);
    for (let k = 0; k < n; k++) {
      const puff = new THREE.Mesh(new THREE.IcosahedronGeometry(2 + rng() * 2.6, 0), mat);
      puff.position.set((rng() - 0.5) * 8, (rng() - 0.5) * 1.4, (rng() - 0.5) * 4.5);
      puff.scale.y = 0.5;
      puff.rotation.y = rng() * 3;
      g.add(puff);
    }
    g.position.set((rng() - 0.5) * 240, 36 + rng() * 16, (rng() - 0.5) * 240);
    g.userData.speed = 0.4 + rng() * 0.7;
    scene.add(g);
    clouds.push(g);
  }
}

// ------------------------------------------------------------
//  Personnages détaillés
// ------------------------------------------------------------
function makeCharacter({ shirt, pants, skin, hat, hair, backpack }) {
  const g = new THREE.Group();
  const M = (c, extra = {}) => new THREE.MeshLambertMaterial({ color: c, ...extra });
  const skinMat = M(skin);
  const shirtMat = M(shirt);
  const pantsMat = M(pants);

  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.36, 0.5, 4, 10), shirtMat);
  body.position.y = 1.05;
  const belt = new THREE.Mesh(new THREE.CylinderGeometry(0.375, 0.375, 0.12, 10), M(0x4a3628));
  belt.position.y = 0.78;
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.34, 14, 12), skinMat);
  head.position.y = 1.78;
  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.12, 6), skinMat);
  nose.position.set(0, 1.76, 0.34); nose.rotation.x = Math.PI / 2;

  // yeux : blanc + pupille
  const eyeWhiteG = new THREE.SphereGeometry(0.06, 8, 8);
  const pupilG = new THREE.SphereGeometry(0.028, 6, 6);
  const whiteM = new THREE.MeshBasicMaterial({ color: 0xf8f8f8 });
  const pupilM = new THREE.MeshBasicMaterial({ color: 0x2a2020 });
  for (const sx of [0.13, -0.13]) {
    const w = new THREE.Mesh(eyeWhiteG, whiteM); w.position.set(sx, 1.82, 0.285); w.scale.z = 0.55;
    const p = new THREE.Mesh(pupilG, pupilM); p.position.set(sx, 1.82, 0.325);
    g.add(w, p);
  }

  // cheveux
  if (hair) {
    const hairMat = M(hair);
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.36, 12, 8, 0, Math.PI * 2, 0, Math.PI * 0.55), hairMat);
    cap.position.set(0, 1.8, -0.03);
    const tuft = new THREE.Mesh(new THREE.SphereGeometry(0.1, 6, 5), hairMat);
    tuft.position.set(0.1, 2.1, 0.08);
    g.add(cap, tuft);
  }

  const armGeo = new THREE.CapsuleGeometry(0.09, 0.5, 3, 6);
  const handGeo = new THREE.SphereGeometry(0.1, 8, 6);
  const armL = new THREE.Mesh(armGeo, shirtMat); armL.position.set(0.5, 1.18, 0);
  const armR = new THREE.Mesh(armGeo, shirtMat); armR.position.set(-0.5, 1.18, 0);
  const handL = new THREE.Mesh(handGeo, skinMat); handL.position.set(0, -0.38, 0); armL.add(handL);
  const handR = new THREE.Mesh(handGeo, skinMat); handR.position.set(0, -0.38, 0); armR.add(handR);

  const legGeo = new THREE.CapsuleGeometry(0.11, 0.42, 3, 6);
  const footGeo = new THREE.BoxGeometry(0.17, 0.1, 0.3);
  const footMat = M(0x3a2c20);
  const legL = new THREE.Mesh(legGeo, pantsMat); legL.position.set(0.17, 0.38, 0);
  const legR = new THREE.Mesh(legGeo, pantsMat); legR.position.set(-0.17, 0.38, 0);
  const footL = new THREE.Mesh(footGeo, footMat); footL.position.set(0, -0.33, 0.06); legL.add(footL);
  const footR = new THREE.Mesh(footGeo, footMat); footR.position.set(0, -0.33, 0.06); legR.add(footR);

  g.add(body, belt, head, nose, armL, armR, legL, legR);

  if (backpack) {
    const pack = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.44, 0.2), M(0x8a6540));
    pack.position.set(0, 1.18, -0.37);
    const roll = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.4, 8), M(0xc8b088));
    roll.position.set(0, 1.46, -0.37); roll.rotation.z = Math.PI / 2;
    g.add(pack, roll);
  }
  if (hat) {
    const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.52, 0.07, 12), M(hat));
    brim.position.y = 1.99;
    const top = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 10), M(hat));
    top.position.y = 2.28;
    const band = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.31, 0.1, 10), M(0xd8c27a));
    band.position.y = 2.05;
    g.add(brim, top, band);
  }
  g.traverse(o => { if (o.isMesh) o.castShadow = true; });
  g.userData.limbs = { armL, armR, legL, legR };
  return g;
}

// Joueur
const player = makeCharacter({
  shirt: 0xe06848, pants: 0x35506e, skin: 0xf0c49b,
  hair: 0x5a3a22, backpack: true,
});
player.position.set(0, terrainH(0, 10), 10);
player.rotation.y = Math.PI; // face au Sage
scene.add(player);
const pState = { angle: Math.PI, bob: 0 };

// Épée de Lumière (invisible avant l'acte 2), attachée au bras droit
const sword = new THREE.Group();
{
  const blade = new THREE.Mesh(
    new THREE.BoxGeometry(0.1, 1.05, 0.03),
    new THREE.MeshLambertMaterial({ color: 0xeaf2ff, emissive: 0x6a8ae8, emissiveIntensity: 0.9 })
  );
  blade.position.y = -0.88;
  const tip = new THREE.Mesh(
    new THREE.ConeGeometry(0.07, 0.18, 4),
    blade.material
  );
  tip.position.y = -1.48; tip.rotation.x = Math.PI; tip.rotation.y = Math.PI / 4;
  const guard = new THREE.Mesh(
    new THREE.BoxGeometry(0.32, 0.06, 0.1),
    new THREE.MeshLambertMaterial({ color: 0xd8b258, emissive: 0x574010, emissiveIntensity: 0.5 })
  );
  guard.position.y = -0.32;
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex, color: 0x9fc0ff, transparent: true, opacity: 0.5,
    blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  glow.scale.set(0.7, 2.2, 1);
  glow.position.y = -0.85;
  sword.add(blade, tip, guard, glow);
  sword.visible = false;
  player.userData.limbs.armR.add(sword);
}

// Le Sage
const sage = makeCharacter({ shirt: 0x7a66c0, pants: 0x4a3f75, skin: 0xe8bd92, hat: 0x5a4a9e });
sage.position.set(4, terrainH(4, 3), 3);
sage.rotation.y = Math.PI * 0.85;
scene.add(sage);
// robe, barbe, bâton
{
  const robe = new THREE.Mesh(
    new THREE.ConeGeometry(0.62, 1.15, 10),
    new THREE.MeshLambertMaterial({ color: 0x62519f })
  );
  robe.position.y = 0.58;
  const rope = new THREE.Mesh(
    new THREE.TorusGeometry(0.4, 0.035, 6, 12),
    new THREE.MeshLambertMaterial({ color: 0xd8c27a })
  );
  rope.position.y = 0.95; rope.rotation.x = Math.PI / 2;
  const beard = new THREE.Mesh(
    new THREE.ConeGeometry(0.2, 0.55, 8),
    new THREE.MeshLambertMaterial({ color: 0xeeeeee })
  );
  beard.position.set(0, 1.48, 0.26); beard.rotation.x = 0.3;
  const staff = new THREE.Mesh(
    new THREE.CylinderGeometry(0.04, 0.05, 2.1, 6),
    new THREE.MeshLambertMaterial({ color: 0x8a6540 })
  );
  staff.position.set(0.62, 1.05, 0.1);
  const orb = new THREE.Mesh(
    new THREE.SphereGeometry(0.14, 12, 10),
    new THREE.MeshLambertMaterial({ color: 0x9feaff, emissive: 0x2fa8c8, emissiveIntensity: 1.2 })
  );
  orb.position.set(0.62, 2.15, 0.1);
  const orbGlow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex, color: 0x7de8ff, transparent: true, opacity: 0.7,
    blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  orbGlow.scale.setScalar(1.2);
  orbGlow.position.copy(orb.position);
  robe.castShadow = beard.castShadow = staff.castShadow = true;
  sage.add(robe, rope, beard, staff, orb, orbGlow);
}
colliders.push({ x: sage.position.x, z: sage.position.z, r: 0.7 });

// ------------------------------------------------------------
//  Flammes & fumée (partagées : braseros + torches du temple)
// ------------------------------------------------------------
const allFlames = []; // {group, phase} — scale flicker quand visible
function makeFlame(scale = 1) {
  const flame = new THREE.Group();
  const f1 = new THREE.Mesh(new THREE.ConeGeometry(0.34, 0.9, 8),
    new THREE.MeshLambertMaterial({ color: 0xffb03a, emissive: 0xff7a10, emissiveIntensity: 1.4, transparent: true, opacity: 0.95 }));
  f1.position.y = 0.45;
  const f2 = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.6, 8),
    new THREE.MeshLambertMaterial({ color: 0xfff0a0, emissive: 0xffc040, emissiveIntensity: 1.6 }));
  f2.position.y = 0.6;
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture('rgba(255,230,170,0.95)', 'rgba(255,160,60,0.4)'),
    transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  glow.scale.setScalar(3.2);
  glow.position.y = 0.5;
  flame.add(f1, f2, glow);
  flame.scale.setScalar(scale);
  allFlames.push({ group: flame, phase: Math.random() * 9, baseScale: scale });
  return flame;
}
// fumée
const smokes = [];
let smokeTimer = 0;
const smokeSources = []; // {x, y, z, active: () => bool}
function updateSmoke(dt) {
  smokeTimer += dt;
  if (smokeTimer > 0.22 && smokes.length < 40) {
    smokeTimer = 0;
    for (const s of smokeSources) {
      if (!s.active()) continue;
      const spr = new THREE.Sprite(new THREE.SpriteMaterial({
        map: smokeTex, transparent: true, opacity: 0.4, depthWrite: false,
      }));
      spr.position.set(s.x + (Math.random() - 0.5) * 0.3, s.y, s.z + (Math.random() - 0.5) * 0.3);
      spr.scale.setScalar(0.5);
      scene.add(spr);
      smokes.push({ spr, life: 1.6 + Math.random() * 0.6 });
      if (smokes.length >= 40) break;
    }
  }
  for (let i = smokes.length - 1; i >= 0; i--) {
    const s = smokes[i];
    s.life -= dt;
    s.spr.position.y += dt * 0.9;
    s.spr.position.x += dt * 0.15;
    s.spr.scale.addScalar(dt * 0.6);
    s.spr.material.opacity = Math.min(0.4, Math.max(0, s.life * 0.3));
    if (s.life <= 0) {
      scene.remove(s.spr);
      s.spr.material.dispose();
      smokes.splice(i, 1);
    }
  }
}

// ------------------------------------------------------------
//  Le temple ancien
// ------------------------------------------------------------
const temple = new THREE.Group();
let templeDoor, treasureRef;
{
  const stone = new THREE.MeshLambertMaterial({ color: 0xc4bba8, flatShading: true });
  const stoneDark = new THREE.MeshLambertMaterial({ color: 0x968e7a, flatShading: true });
  const gold = new THREE.MeshLambertMaterial({ color: 0xd8b258, emissive: 0x3a2a08, emissiveIntensity: 0.4 });

  const base = new THREE.Mesh(new THREE.BoxGeometry(14, 1.2, 10), stoneDark);
  base.position.y = 0.6;
  const trim = new THREE.Mesh(new THREE.BoxGeometry(14.6, 0.25, 10.6), stone);
  trim.position.y = 1.15;
  temple.add(base, trim);
  // marches
  for (let k = 0; k < 3; k++) {
    const step = new THREE.Mesh(new THREE.BoxGeometry(6.5 - k * 0.7, 0.34, 1.1), stoneDark);
    step.position.set(0, 0.17 + k * 0.34, 6.6 - k * 0.62);
    temple.add(step);
  }
  // colonnes avec base et chapiteau
  for (const sx of [-5.2, -1.8, 1.8, 5.2]) {
    const col = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.6, 5.6, 9), stone);
    col.position.set(sx, 4.2, 4.2);
    const cbase = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.4, 1.5), stoneDark);
    cbase.position.set(sx, 1.6, 4.2);
    const cap = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.35, 1.4), stoneDark);
    cap.position.set(sx, 7.15, 4.2);
    temple.add(col, cbase, cap);
  }
  const lintel = new THREE.Mesh(new THREE.BoxGeometry(13.6, 1.0, 1.7), stone);
  lintel.position.set(0, 7.75, 4.2);
  const lintelTrim = new THREE.Mesh(new THREE.BoxGeometry(13.9, 0.22, 1.9), gold);
  lintelTrim.position.set(0, 8.3, 4.2);
  temple.add(lintel, lintelTrim);
  const backWall = new THREE.Mesh(new THREE.BoxGeometry(12, 7, 1), stone);
  backWall.position.set(0, 4.7, -3.5);
  temple.add(backWall);
  for (const side of [-1, 1]) {
    const wall = new THREE.Mesh(new THREE.BoxGeometry(1, 7, 7), stone);
    wall.position.set(side * 6, 4.7, 0.2);
    temple.add(wall);
  }
  const roof = new THREE.Mesh(new THREE.BoxGeometry(13.8, 0.9, 9.8), stoneDark);
  roof.position.set(0, 8.55, 0.2);
  temple.add(roof);
  // fronton triangulaire
  const pedGeo = new THREE.CylinderGeometry(2.5, 2.5, 13.4, 3, 1);
  pedGeo.rotateZ(Math.PI / 2);
  const pediment = new THREE.Mesh(pedGeo, stone);
  pediment.scale.set(1, 1, 0.45);
  pediment.position.set(0, 9.6, 2.2);
  temple.add(pediment);
  // mousse sur la plateforme
  const mossMat = new THREE.MeshLambertMaterial({ color: 0x5a8a44, flatShading: true });
  const mrng = mulberry32(55);
  for (let k = 0; k < 8; k++) {
    const moss = new THREE.Mesh(new THREE.IcosahedronGeometry(0.3 + mrng() * 0.3, 0), mossMat);
    moss.position.set((mrng() - 0.5) * 13, 1.25, 3.2 + mrng() * 2.6);
    moss.scale.y = 0.25;
    temple.add(moss);
  }

  // porte dorée gravée de runes
  templeDoor = new THREE.Mesh(
    new THREE.BoxGeometry(3.4, 5.2, 0.5),
    new THREE.MeshLambertMaterial({ map: makeRunesTexture(), emissive: 0x553a10, emissiveIntensity: 0.35 })
  );
  templeDoor.position.set(0, 3.8, 4.2);
  temple.add(templeDoor);

  // torches de l'entrée (toujours allumées)
  for (const sx of [-3.4, 3.4]) {
    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.11, 1.6, 6),
      new THREE.MeshLambertMaterial({ color: 0x5c4530 }));
    post.position.set(sx, 2.0, 5.6);
    const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.12, 0.3, 8), stoneDark);
    cup.position.set(sx, 2.85, 5.6);
    const flame = makeFlame(0.55);
    flame.position.set(sx, 2.95, 5.6);
    temple.add(post, cup, flame);
  }

  // trésor (révélé quand la porte s'ouvre)
  treasureRef = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.9, 1),
    new THREE.MeshLambertMaterial({ color: 0xffe27a, emissive: 0xcf9d2a, emissiveIntensity: 0.9 })
  );
  treasureRef.position.set(0, 2.6, 0);
  const tGlow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture('rgba(255,240,180,0.9)', 'rgba(255,200,90,0.35)'),
    transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  tGlow.scale.setScalar(4.5);
  tGlow.position.set(0, 2.6, 0);
  temple.add(treasureRef, tGlow);

  const th = terrainH(0, -38);
  temple.position.set(0, th, -38);
  temple.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  scene.add(temple);
  colliders.push(
    { x: 0, z: -38 - 3.5, r: 6.5 },
    { x: -6, z: -38, r: 2 }, { x: 6, z: -38, r: 2 },
  );
  // fumée des torches du temple
  for (const sx of [-3.4, 3.4]) {
    smokeSources.push({ x: sx, y: th + 3.6, z: -38 + 5.6, active: () => true });
  }
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
  const innerGeo = new THREE.OctahedronGeometry(0.28, 0);
  for (let i = 0; i < CRYSTAL_COUNT; i++) {
    const [x, z] = spots[i];
    const mat = new THREE.MeshPhongMaterial({
      color: 0x9fdcff, emissive: 0x2f7fd8, emissiveIntensity: 0.6,
      shininess: 90, specular: 0xffffff,
      transparent: true, opacity: 0.85,
    });
    const m = new THREE.Mesh(geo, mat);
    const inner = new THREE.Mesh(innerGeo, new THREE.MeshBasicMaterial({ color: 0xeaffff }));
    m.add(inner);
    const h = Math.max(terrainH(x, z), 0.3);
    m.position.set(x, h + 1.2, z);
    m.castShadow = true;
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTex, color: 0x9fe0ff, transparent: true,
      opacity: 0.75, blending: THREE.AdditiveBlending, depthWrite: false,
    }));
    halo.scale.setScalar(3);
    m.add(halo);
    // anneau d'étincelles en orbite
    const sN = 8;
    const sPos = new Float32Array(sN * 3);
    for (let k = 0; k < sN; k++) {
      const a = (k / sN) * Math.PI * 2;
      sPos[k * 3] = Math.cos(a) * 0.95;
      sPos[k * 3 + 1] = (Math.random() - 0.5) * 0.5;
      sPos[k * 3 + 2] = Math.sin(a) * 0.95;
    }
    const sGeo = new THREE.BufferGeometry();
    sGeo.setAttribute('position', new THREE.BufferAttribute(sPos, 3));
    const sparkles = new THREE.Points(sGeo, new THREE.PointsMaterial({
      map: glowTex, color: 0xcfeaff, size: 0.22, transparent: true, opacity: 0.9,
      blending: THREE.AdditiveBlending, depthWrite: false,
    }));
    m.add(sparkles);
    scene.add(m);
    crystals.push({ mesh: m, sparkles, taken: false, baseY: m.position.y, phase: i * 1.3 });
  }
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
  sign.traverse(o => { if (o.isMesh) o.castShadow = true; });
  scene.add(sign);
}

// ------------------------------------------------------------
//  Braseros sacrés (acte 2)
// ------------------------------------------------------------
const braziers = [];
{
  const bowlMat = new THREE.MeshLambertMaterial({ color: 0x5c5c68, flatShading: true });
  const woodMat = new THREE.MeshLambertMaterial({ color: 0x5c3f26 });
  const emberMat = new THREE.MeshLambertMaterial({ color: 0xff8830, emissive: 0xdd4400, emissiveIntensity: 1.2 });
  const stoneMat = new THREE.MeshLambertMaterial({ color: 0x8f8f99, flatShading: true });
  for (let i = 0; i < BRAZIER_SPOTS.length; i++) {
    const [x, z] = BRAZIER_SPOTS[i];
    const h = Math.max(terrainH(x, z), 0.3);
    const g = new THREE.Group();
    const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.34, 1.0, 8), bowlMat);
    foot.position.y = 0.5;
    const bowl = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.32, 0.45, 10), bowlMat);
    bowl.position.y = 1.15;
    const wood = new THREE.Mesh(new THREE.SphereGeometry(0.32, 8, 6), woodMat);
    wood.position.y = 1.35; wood.scale.y = 0.5;
    const ember = new THREE.Mesh(new THREE.SphereGeometry(0.26, 8, 6), emberMat);
    ember.position.y = 1.36; ember.scale.y = 0.4;
    ember.visible = false;
    // cercle de pierres au sol
    for (let k = 0; k < 6; k++) {
      const a = (k / 6) * Math.PI * 2;
      const st = new THREE.Mesh(new THREE.IcosahedronGeometry(0.16 + (i + k) % 3 * 0.05, 0), stoneMat);
      st.position.set(Math.cos(a) * 1.3, 0.08, Math.sin(a) * 1.3);
      g.add(st);
    }
    const flame = makeFlame(1);
    flame.position.y = 1.45;
    flame.visible = false;
    g.add(foot, bowl, wood, ember, flame);
    g.position.set(x, h, z);
    g.traverse(o => { if (o.isMesh) o.castShadow = true; });
    scene.add(g);
    colliders.push({ x, z, r: 0.7 });
    const b = { group: g, flame, ember, lit: false, x, z };
    braziers.push(b);
    smokeSources.push({ x, y: h + 2.4, z, active: () => b.lit });
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
    emissiveIntensity: 0.7,
    transparent: true, opacity: 0.82,
  });
  const body = new THREE.Mesh(new THREE.ConeGeometry(0.55, 1.6, 8), bodyMat);
  body.position.y = 0.8; body.rotation.x = Math.PI; // pointe vers le bas
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.42, 12, 10), bodyMat);
  head.position.y = 1.75;
  const eyeMat = new THREE.MeshBasicMaterial({ color: boss ? 0xff4040 : 0x7ae8ff });
  const eyeGeo = new THREE.SphereGeometry(0.07, 6, 6);
  const e1 = new THREE.Mesh(eyeGeo, eyeMat); e1.position.set(0.15, 1.82, 0.36);
  const e2 = new THREE.Mesh(eyeGeo, eyeMat); e2.position.set(-0.15, 1.82, 0.36);
  const armGeo = new THREE.CapsuleGeometry(0.08, 0.5, 3, 6);
  const a1 = new THREE.Mesh(armGeo, bodyMat); a1.position.set(0.55, 1.2, 0.1); a1.rotation.z = -0.5;
  const a2 = new THREE.Mesh(armGeo, bodyMat); a2.position.set(-0.55, 1.2, 0.1); a2.rotation.z = 0.5;
  const aura = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex, color: boss ? 0xff6a6a : 0x8a7ae8, transparent: true,
    opacity: 0.35, blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  aura.scale.setScalar(3.4);
  aura.position.y = 1.2;
  g.add(body, head, e1, e2, a1, a2, aura);
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
    map: glowTex, color, size: 0.4, transparent: true, opacity: 1,
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
  b.ember.visible = true;
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
applyMood();

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

  // le soleil (et ses ombres) suit le joueur pour des ombres nettes
  sun.position.set(player.position.x + 30, 50, player.position.z + 17);
  sun.target.position.set(player.position.x, 0, player.position.z);
  sun.target.updateMatrixWorld();

  // sage : respiration
  sage.position.y = terrainH(sage.position.x, sage.position.z) + Math.sin(t * 1.6) * 0.03;

  // cristaux : flottement + étincelles en orbite
  for (const c of crystals) {
    if (c.taken) continue;
    c.mesh.position.y = c.baseY + Math.sin(t * 2 + c.phase) * 0.25;
    c.mesh.rotation.y = t * 1.4 + c.phase;
    c.sparkles.rotation.y = -t * 3.2;
    if (quest.stage === 'collect' &&
        player.position.distanceTo(c.mesh.position) < 1.9) {
      collectCrystal(c);
    }
  }

  // lucioles scintillent (plus visibles la nuit), pollen le jour
  fireflies.material.opacity = 0.35 + Math.sin(t * 2.2) * 0.25 + night01 * 0.5;
  fireflies.rotation.y = Math.sin(t * 0.05) * 0.02;
  dust.material.opacity = (1 - night01) * (0.3 + Math.sin(t * 1.3) * 0.15);
  dust.rotation.y = t * 0.012;

  // nuages
  for (const cl of clouds) {
    cl.position.x += cl.userData.speed * dt;
    if (cl.position.x > 140) cl.position.x = -140;
  }

  // flammes (braseros + torches) : flicker
  for (const f of allFlames) {
    if (f.group.visible) {
      f.group.scale.setScalar(f.baseScale * (1 + Math.sin(t * 13 + f.phase) * 0.12));
    }
  }
  updateSmoke(dt);

  // océan animé
  waterU.uTime.value = t;

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
      braziers[i].ember.visible = true;
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
