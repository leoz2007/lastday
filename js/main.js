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
import { EffectComposer } from './vendor/postprocessing/EffectComposer.js';
import { RenderPass } from './vendor/postprocessing/RenderPass.js';
import { UnrealBloomPass } from './vendor/postprocessing/UnrealBloomPass.js';
import { OutputPass } from './vendor/postprocessing/OutputPass.js';
import { ShaderPass } from './vendor/postprocessing/ShaderPass.js';
import { GLTFLoader } from './vendor/loaders/GLTFLoader.js';
import * as SkeletonUtils from './vendor/utils/SkeletonUtils.js';
import { mergeVertices, mergeGeometries } from './vendor/utils/BufferGeometryUtils.js';

// ------------------------------------------------------------
//  Constantes du monde
// ------------------------------------------------------------
const ISLAND_R = 62;        // rayon de l'île
const WALK_R = 56;          // rayon max du joueur
const PLAYER_SPEED = 6.2;
const CRYSTAL_COUNT = 5;
const MAX_HEARTS = 5;
const SAVE_KEY = 'porte-oubliee-save-v3';

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
renderer.toneMappingExposure = 1.04;
document.getElementById('game').appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0xd4e0dd, 60, 165);

const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 700);

// Post-processing : rendu HDR multisampled + bloom + sortie tone-mappée
const composerRT = new THREE.WebGLRenderTarget(window.innerWidth, window.innerHeight, {
  type: THREE.HalfFloatType, samples: 4,
});
const composer = new EffectComposer(renderer, composerRT);
composer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
composer.setSize(window.innerWidth, window.innerHeight);
composer.addPass(new RenderPass(scene, camera));
// bloom à résolution réduite : la lueur large coûte moitié moins
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth / 2, window.innerHeight / 2), 0.55, 0.5, 0.97);
composer.addPass(bloomPass);
composer.addPass(new OutputPass());
// grain de film + micro-saturation (le « polish » des sketches three.js)
const grainPass = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float uTime;
    varying vec2 vUv;
    float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7)) + uTime * 13.7) * 43758.5453); }
    void main(){
      vec4 c = texture2D(tDiffuse, vUv);
      float l = dot(c.rgb, vec3(0.299, 0.587, 0.114));
      c.rgb = mix(vec3(l), c.rgb, 1.07);
      c.rgb += (hash(vUv * vec2(1917.0, 1031.0)) - 0.5) * 0.04;
      gl_FragColor = c;
    }`,
});
composer.addPass(grainPass);

// Lumières
const hemi = new THREE.HemisphereLight(0xcfe8ff, 0x5a7a48, 0.9);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xffedc4, 1.9);
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
//  Stylisation des matériaux via injection de shader
//  (onBeforeCompile sur Lambert : vent, rim light, grain)
// ------------------------------------------------------------
const windShaders = [];
const F = n => Number(n).toFixed(3);
function stylize(mat, opts = {}) {
  mat.onBeforeCompile = (shader) => {
    shader.uniforms.uTime = { value: 0 };
    if (opts.sway) windShaders.push(shader);
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\nuniform float uTime;\nvarying vec3 vStylePos;');
    let inject = '\n  vStylePos = position;';
    if (opts.sway) {
      // ondulation type vent, plus forte vers le haut de l'objet
      inject += `
  {
    float grad = smoothstep(${F(opts.swayY[0])}, ${F(opts.swayY[1])}, position.y);
    #ifdef USE_INSTANCING
      float ph = instanceMatrix[3][0] * 0.37 + instanceMatrix[3][2] * 0.29;
    #else
      float ph = position.x * 0.6 + position.z * 0.5;
    #endif
    transformed.x += sin(uTime * 1.5 + ph) * ${F(opts.sway)} * grad;
    transformed.z += cos(uTime * 1.15 + ph * 1.3) * ${F(opts.sway * 0.7)} * grad;
  }`;
    }
    shader.vertexShader = shader.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>' + inject);
    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vStylePos;');
    if (opts.grain) {
      // grain procédural : casse les aplats de couleur
      shader.fragmentShader = shader.fragmentShader.replace('#include <color_fragment>', `#include <color_fragment>
  {
    float g1 = sin(vStylePos.x * 2.3 + sin(vStylePos.z * 1.7)) * sin(vStylePos.z * 2.1 + sin(vStylePos.x * 1.9));
    float g2 = sin(vStylePos.x * 9.7 + vStylePos.z * 7.3) * sin(vStylePos.y * 8.1 + vStylePos.x * 6.3);
    diffuseColor.rgb *= 0.965 + 0.05 * g1 + 0.022 * g2;
  }`);
    }
    if (opts.rim) {
      // lumière de contour : adoucit et arrondit les silhouettes
      const c = new THREE.Color(opts.rim);
      shader.fragmentShader = shader.fragmentShader.replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
  {
    float rimf = pow(1.0 - saturate(dot(normalize(vViewPosition), normal)), ${F(opts.rimPow || 3)});
    totalEmissiveRadiance += vec3(${F(c.r)}, ${F(c.g)}, ${F(c.b)}) * rimf * ${F(opts.rimStrength || 0.25)};
  }`);
    }
  };
  mat.customProgramCacheKey = () => 'stylize' + JSON.stringify(opts);
  return mat;
}

// ------------------------------------------------------------
//  Cel-shading façon BOTW : rampe de lumière en bandes douces
//  partagée par tous les matériaux du monde
// ------------------------------------------------------------
const toonRamp = (() => {
  const c = document.createElement('canvas');
  c.width = 4; c.height = 1;
  const ctx = c.getContext('2d');
  [112, 158, 228, 255].forEach((g, i) => {
    ctx.fillStyle = `rgb(${g},${g},${g})`;
    ctx.fillRect(i, 0, 1, 1);
  });
  const t = new THREE.CanvasTexture(c);
  t.minFilter = THREE.LinearFilter;
  t.magFilter = THREE.LinearFilter;
  t.generateMipmaps = false;
  return t;
})();
function TOON(params = {}) {
  return new THREE.MeshToonMaterial({ gradientMap: toonRamp, ...params });
}

// ------------------------------------------------------------
//  Sculpture procédurale : déplace les sommets le long des
//  normales avec un bruit multi-octaves (pierre taillée, métal
//  martelé, feuillage froissé…)
// ------------------------------------------------------------
function sculpt(geo, amp, freq, seed = 0, flat = false) {
  let g = geo.index ? geo : mergeVertices(geo);
  if (!g.index) g = mergeVertices(g);
  g.computeVertexNormals();
  const pos = g.attributes.position;
  const nor = g.attributes.normal;
  const v = new THREE.Vector3(), n = new THREE.Vector3();
  for (let i = 0; i < pos.count; i++) {
    v.fromBufferAttribute(pos, i);
    n.fromBufferAttribute(nor, i);
    const d =
      Math.sin(v.x * freq + seed) * Math.sin(v.y * freq * 1.31 + seed * 2.1) * Math.sin(v.z * freq * 0.83 + seed * 3.7) +
      0.5 * Math.sin(v.x * freq * 2.71 + seed) * Math.sin(v.y * freq * 2.33) * Math.sin(v.z * freq * 3.17) +
      0.25 * Math.sin(v.x * freq * 5.3) * Math.sin(v.z * freq * 6.1);
    pos.setXYZ(i, v.x + n.x * d * amp, v.y + n.y * d * amp, v.z + n.z * d * amp);
  }
  if (flat) g = g.toNonIndexed();
  g.computeVertexNormals();
  return g;
}

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
function makeWorleyTexture() {
  // champ cellulaire de Worley tuilé (grille 8x8 jitterée)
  const S = 256, G = 8, cell = S / G;
  const wrng = mulberry32(2024);
  const pts = [];
  for (let gy = 0; gy < G; gy++) {
    for (let gx = 0; gx < G; gx++) {
      pts.push([(gx + wrng()) * cell, (gy + wrng()) * cell]);
    }
  }
  const c = document.createElement('canvas');
  c.width = c.height = S;
  const ctx = c.getContext('2d');
  const img = ctx.createImageData(S, S);
  for (let y = 0; y < S; y++) {
    const gy = Math.floor(y / cell);
    for (let x = 0; x < S; x++) {
      const gx = Math.floor(x / cell);
      let d1 = 1e9;
      for (let oy = -1; oy <= 1; oy++) {
        for (let ox = -1; ox <= 1; ox++) {
          const p = pts[((gy + oy + G) % G) * G + ((gx + ox + G) % G)];
          // distance avec enroulement (texture tuilée)
          let dx = Math.abs(p[0] - x); dx = Math.min(dx, S - dx);
          let dy = Math.abs(p[1] - y); dy = Math.min(dy, S - dy);
          const d = dx * dx + dy * dy;
          if (d < d1) d1 = d;
        }
      }
      const v = Math.min(255, Math.sqrt(d1) / (cell * 0.9) * 255);
      const i = (y * S + x) * 4;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = v;
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}
const glowTex = makeGlowTexture();
const worleyTex = makeWorleyTexture();
const smokeTex = makeSmokeTexture();

// ------------------------------------------------------------
//  Ciel : dôme en shader (jour/nuit), soleil, lune, étoiles
// ------------------------------------------------------------
const skyU = {
  uNight: { value: 0 },
  uDusk: { value: 0 },
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
      uniform float uDusk;
      uniform vec3 uSunDir;
      varying vec3 vDir;
      void main(){
        vec3 nd = normalize(vDir);
        float h = clamp(nd.y, -1.0, 1.0);
        vec3 dayZen = vec3(0.30, 0.56, 0.83);
        vec3 dayHor = vec3(0.93, 0.91, 0.84);
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
        // embrasement du crépuscule pendant la transition jour/nuit
        float horiz = pow(1.0 - abs(h), 4.0);
        col = mix(col, vec3(0.98, 0.52, 0.22), uDusk * horiz * 0.8);
        col = mix(col, vec3(0.72, 0.38, 0.42), uDusk * pow(1.0 - abs(h), 2.0) * 0.3);
        col += vec3(1.0, 0.5, 0.2) * pow(s, 8.0) * uDusk * horiz * 0.5;
        gl_FragColor = vec4(col, 1.0);
      }`,
  });
  const sky = new THREE.Mesh(new THREE.SphereGeometry(420, 32, 18), skyMat);
  scene.add(sky);
}

// Étoiles (2 couches qui scintillent en alternance)
const starLayers = [];
{
  const srng = mulberry32(4242);
  for (let layer = 0; layer < 2; layer++) {
    const N = 220;
    const positions = new Float32Array(N * 3);
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
    const pts = new THREE.Points(geo, new THREE.PointsMaterial({
      color: layer ? 0xfff4d8 : 0xdfe8ff, size: 1.4 + layer * 0.7, sizeAttenuation: false,
      transparent: true, opacity: 0, depthWrite: false, fog: false,
    }));
    scene.add(pts);
    starLayers.push(pts);
  }
}

// Étoile filante (apparaît de temps en temps la nuit)
const meteor = new THREE.Sprite(new THREE.SpriteMaterial({
  map: makeGlowTexture('rgba(255,255,255,1)', 'rgba(200,220,255,0.5)'),
  transparent: true, opacity: 0, depthWrite: false, fog: false,
  blending: THREE.AdditiveBlending,
}));
meteor.scale.set(30, 1.6, 1);
scene.add(meteor);
const meteorState = { life: 0, next: 12, vel: new THREE.Vector3() };

// Soleil et lune (sprites)
let sunSprite, moon, moon2, planet;
{
  sunSprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture('rgba(255,246,214,1)', 'rgba(255,214,130,0.5)'),
    transparent: true, opacity: 0.95, depthWrite: false, fog: false,
    blending: THREE.AdditiveBlending,
  }));
  sunSprite.scale.setScalar(90);
  sunSprite.position.copy(skyU.uSunDir.value).multiplyScalar(400);
  scene.add(sunSprite);

  // flare anamorphique horizontal
  const flare = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture('rgba(255,240,200,0.8)', 'rgba(255,210,130,0.3)'),
    transparent: true, opacity: 0.5, depthWrite: false, fog: false,
    blending: THREE.AdditiveBlending,
  }));
  flare.scale.set(240, 7, 1);
  flare.position.copy(sunSprite.position);
  scene.add(flare);
  sunSprite.userData.flare = flare;

  moon = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeMoonTexture(), transparent: true, opacity: 0, depthWrite: false, fog: false,
  }));
  moon.scale.setScalar(52);
  moon.position.set(-160, 240, -300);
  scene.add(moon);
  // halo de lune
  const moonHalo = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture('rgba(220,230,255,0.55)', 'rgba(180,200,255,0.2)'),
    transparent: true, opacity: 0, depthWrite: false, fog: false,
    blending: THREE.AdditiveBlending,
  }));
  moonHalo.scale.setScalar(130);
  moonHalo.position.copy(moon.position);
  scene.add(moonHalo);
  moon.userData.halo = moonHalo;

  // deuxième lune (P4X-731 en a deux)
  moon2 = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeMoonTexture(), color: 0xbfe8dc, transparent: true, opacity: 0.3,
    depthWrite: false, fog: false,
  }));
  moon2.scale.setScalar(24);
  moon2.position.set(230, 150, -240);
  scene.add(moon2);

  // planète géante visible à l'horizon
  const planetTex = (() => {
    const c = document.createElement('canvas');
    c.width = c.height = 256;
    const ctx = c.getContext('2d');
    const g1 = ctx.createRadialGradient(108, 100, 20, 128, 128, 126);
    g1.addColorStop(0, 'rgba(190,210,235,1)');
    g1.addColorStop(0.55, 'rgba(130,155,195,1)');
    g1.addColorStop(0.85, 'rgba(80,100,140,1)');
    g1.addColorStop(1, 'rgba(80,100,140,0)');
    ctx.fillStyle = g1;
    ctx.beginPath(); ctx.arc(128, 128, 124, 0, 7); ctx.fill();
    ctx.globalCompositeOperation = 'source-atop';
    ctx.fillStyle = 'rgba(255,255,255,0.10)';
    for (const [y, h] of [[70, 14], [110, 9], [150, 18], [196, 10]]) ctx.fillRect(0, y, 256, h);
    ctx.fillStyle = 'rgba(30,40,70,0.35)';
    ctx.beginPath(); ctx.arc(210, 190, 150, 0, 7); ctx.fill();
    return new THREE.CanvasTexture(c);
  })();
  planet = new THREE.Sprite(new THREE.SpriteMaterial({
    map: planetTex, transparent: true, opacity: 0.5, depthWrite: false, fog: false,
  }));
  planet.scale.setScalar(150);
  planet.position.set(-320, 120, 180);
  scene.add(planet);
}

// ------------------------------------------------------------
//  Jour / Nuit (les Brumes de l'acte 2)
// ------------------------------------------------------------
const MOOD = {
  dayFog: new THREE.Color(0xd4e0dd), nightFog: new THREE.Color(0x121c33),
  daySun: new THREE.Color(0xffedc4), nightSun: new THREE.Color(0x8fa8ff),
  dayHemiSky: new THREE.Color(0xcfe8ff), nightHemiSky: new THREE.Color(0x2a3a66),
  dayHemiGnd: new THREE.Color(0x5a7a48), nightHemiGnd: new THREE.Color(0x18203a),
};
let night01 = 0;      // 0 = jour, 1 = nuit
let nightTarget = 0;

const DUSK = {
  fog: new THREE.Color(0xd89a66),
  sun: new THREE.Color(0xff8c42),
  sprite: new THREE.Color(0xffb060),
};
function applyMood() {
  const dusk = Math.sin(night01 * Math.PI); // pic au milieu de la transition
  skyU.uNight.value = night01;
  skyU.uDusk.value = dusk;
  waterU.uNight.value = night01;
  waterU.uDusk.value = dusk;
  scene.fog.color.lerpColors(MOOD.dayFog, MOOD.nightFog, night01).lerp(DUSK.fog, dusk * 0.45);
  scene.fog.near = 60 - night01 * 28;
  scene.fog.far = 165 - night01 * 70;
  hemi.intensity = 0.76 - night01 * 0.32;
  hemi.color.lerpColors(MOOD.dayHemiSky, MOOD.nightHemiSky, night01);
  hemi.groundColor.lerpColors(MOOD.dayHemiGnd, MOOD.nightHemiGnd, night01);
  sun.intensity = 1.9 - night01 * 1.05;
  sun.color.lerpColors(MOOD.daySun, MOOD.nightSun, night01).lerp(DUSK.sun, dusk * 0.65);
  sunSprite.material.opacity = (1 - night01) * 0.95;
  sunSprite.material.color.set(0xffffff).lerp(DUSK.sprite, dusk);
  sunSprite.userData.flare.material.opacity = (1 - night01) * 0.45 + dusk * 0.3;
  moon.material.opacity = night01 * 0.98;
  moon.userData.halo.material.opacity = night01 * 0.5;
  moon2.material.opacity = 0.28 + night01 * 0.6;
  planet.material.opacity = 0.5 - night01 * 0.12;
  bloomPass.strength = 0.42 + night01 * 0.42; // la nuit, les lueurs ressortent plus
}

// ------------------------------------------------------------
//  Terrain lissé, dégradés continus par altitude + grain shader
// ------------------------------------------------------------
{
  const seg = 132;
  const geo = new THREE.PlaneGeometry(ISLAND_R * 2.7, ISLAND_R * 2.7, seg, seg);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  const crng = mulberry32(777);
  const cWet = new THREE.Color(0xd9bd82);
  const cSand = new THREE.Color(0xf0dca4);
  const cGrassA = new THREE.Color(0x93c96e);
  const cGrassB = new THREE.Color(0x6aab60);
  const cGrassC = new THREE.Color(0x548f58);
  const cDirt = new THREE.Color(0xa08d6a);
  const cRock = new THREE.Color(0x939099);
  const cSnow = new THREE.Color(0xdadde5);
  const tmp = new THREE.Color();
  const ss = (a, b, x) => {
    const k = Math.min(1, Math.max(0, (x - a) / (b - a)));
    return k * k * (3 - 2 * k);
  };
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), z = pos.getZ(i);
    const h = terrainH(x, z);
    pos.setY(i, h);
    // bruit doux pour des frontières organiques entre biomes
    const n = Math.sin(x * 0.5) * Math.cos(z * 0.45) * 0.22 + Math.sin(x * 0.13 + z * 0.17) * 0.28;
    const hh = h + n;
    tmp.copy(cWet)
      .lerp(cSand, ss(-0.15, 0.35, hh))
      .lerp(cGrassA, ss(0.3, 0.95, hh))
      .lerp(cGrassB, ss(0.95, 2.2, hh))
      .lerp(cGrassC, ss(2.2, 3.1, hh))
      .lerp(cDirt, ss(3.0, 3.9, hh))
      .lerp(cRock, ss(3.8, 4.6, hh))
      .lerp(cSnow, ss(4.6, 5.6, hh));
    tmp.offsetHSL((crng() - 0.5) * 0.008, 0, (crng() - 0.5) * 0.02);
    colors[i * 3] = tmp.r; colors[i * 3 + 1] = tmp.g; colors[i * 3 + 2] = tmp.b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  const terrain = new THREE.Mesh(geo,
    stylize(TOON({ vertexColors: true }), { grain: true }));
  terrain.receiveShadow = true;
  scene.add(terrain);
}

// ------------------------------------------------------------
//  Océan v3 : bathymétrie analytique portée en GLSL, trains de
//  Gerstner à déferlement limité par la profondeur, absorption
//  Beer-Lambert, écume Worley effilochée, bioluminescence
//  d'agitation la nuit, chemin de soleil scintillant
// ------------------------------------------------------------
const waterU = THREE.UniformsUtils.merge([
  THREE.UniformsLib.fog,
  { uTime: { value: 0 }, uNight: { value: 0 }, uDusk: { value: 0 }, uWorley: { value: null } },
]);
waterU.uWorley.value = worleyTex;
const BATHY_GLSL = `
  // même fonction que terrainH côté JS : l'eau connaît la vraie profondeur
  float bathy(vec2 w){
    float d = length(w);
    float island = max(0.0, 1.0 - (d / 62.0) * (d / 62.0));
    float h = sin(w.x * 0.09) * cos(w.y * 0.08) * 1.5
            + sin(w.x * 0.031 + w.y * 0.047) * 2.1
            + cos(w.x * 0.017 - w.y * 0.023) * 1.2
            + sin(w.x * 0.21 + 1.7) * cos(w.y * 0.19 - 0.6) * 0.35;
    return (h + 3.1) * island - 1.4;
  }`;
{
  const geo = new THREE.PlaneGeometry(520, 520, 110, 110);
  const mat = new THREE.ShaderMaterial({
    uniforms: waterU,
    transparent: true,
    fog: true,
    vertexShader: `
      uniform float uTime;
      varying vec2 vW;
      varying float vH;
      varying float vDepth;
      varying float vAgit;
      __BATHY__
      #include <fog_pars_vertex>
      void main(){
        vec3 p = position;
        vec2 w = vec2(p.x, -p.y); // coordonnées monde XZ
        float depth = max(0.06, -bathy(w));
        // amplitude limitée par la profondeur : les vagues cassent au rivage
        float dl = clamp(depth / 2.4, 0.0, 1.0);
        vec2 D1 = normalize(vec2(0.80, 0.60));
        vec2 D2 = normalize(vec2(-0.55, 0.78));
        vec2 D3 = normalize(vec2(0.95, -0.30));
        float A1 = 0.34 * dl, A2 = 0.19 * dl, A3 = 0.10 * dl;
        float ph1 = dot(D1, w) * 0.10 - uTime * 0.85;
        float ph2 = dot(D2, w) * 0.17 - uTime * 1.05 + 2.0;
        float ph3 = dot(D3, w) * 0.28 - uTime * 1.45 + 4.0;
        // cambrure de Gerstner, accentuée dans les hauts-fonds
        float Q = 0.55 * (1.0 + (1.0 - dl) * 1.3);
        vec2 hd = D1 * (Q * A1 * cos(ph1)) + D2 * (Q * A2 * cos(ph2)) + D3 * (Q * A3 * cos(ph3));
        p.x += hd.x; p.y -= hd.y; // retour local (y local = -z monde)
        float H = A1 * sin(ph1) + A2 * sin(ph2) + A3 * sin(ph3)
                + sin(p.x * 0.34 + uTime * 1.8) * sin(p.y * 0.29 - uTime * 1.4) * 0.035 * dl;
        p.z += H;
        vH = H;
        vDepth = depth;
        // agitation = énergie perdue au déferlement + crêtes cambrées
        vAgit = (1.0 - dl) * (0.5 + 0.5 * sin(ph1)) + max(0.0, sin(ph2)) * (1.0 - dl) * 0.6;
        vW = w;
        vec4 mvPosition = modelViewMatrix * vec4(p, 1.0);
        gl_Position = projectionMatrix * mvPosition;
        #include <fog_vertex>
      }`.replace('__BATHY__', BATHY_GLSL),
    fragmentShader: `
      uniform float uTime;
      uniform float uNight;
      uniform float uDusk;
      uniform sampler2D uWorley;
      varying vec2 vW;
      varying float vH;
      varying float vDepth;
      varying float vAgit;
      #include <fog_pars_fragment>
      void main(){
        float depth = vDepth;
        // absorption de Beer-Lambert : turquoise -> large bleu selon la profondeur
        vec3 cShallow = mix(vec3(0.46, 0.86, 0.78), vec3(0.10, 0.24, 0.38), uNight);
        vec3 cDeep    = mix(vec3(0.02, 0.23, 0.44), vec3(0.012, 0.055, 0.15), uNight);
        float absorb = exp(-depth * 0.24);
        vec3 col = mix(cDeep, cShallow, absorb);
        col += vH * (0.10 - 0.05 * uNight);
        // champ de Worley (deux échelles qui dérivent)
        float wo = texture2D(uWorley, vW * 0.045 + vec2(uTime * 0.006, uTime * 0.004)).r;
        float wo2 = texture2D(uWorley, vW * 0.012 - vec2(uTime * 0.003, 0.0)).r;
        // ligne de swash : la vague lèche le bord de lagune, bord effiloché
        float lap = sin(uTime * 0.7 + wo2 * 5.0) * 0.16 + 0.18;
        float swash = 1.0 - smoothstep(0.0, 0.6, depth - lap);
        float frayed = smoothstep(0.42, 0.8, swash + (0.5 - wo) * 1.0) * smoothstep(0.03, 0.2, swash);
        // écume de déferlement, morcelée en cellules
        float breakFoam = smoothstep(0.6, 0.92, vAgit * (0.5 + 0.7 * (1.0 - wo)));
        float foam = clamp(frayed + breakFoam * 0.85, 0.0, 1.0);
        vec3 foamCol = mix(vec3(0.97, 0.99, 1.0), vec3(0.5, 0.62, 0.78), uNight);
        col = mix(col, foamCol, foam * 0.92);
        // bioluminescence : uniquement là où l'eau est agitée, la nuit
        float pulse = 0.45 + 0.55 * sin(uTime * 1.7 + wo * 14.0);
        float biolum = clamp(breakFoam + frayed * 0.55, 0.0, 1.0) * uNight * pulse
                     * smoothstep(0.5, 0.8, wo2); // par plaques éparses
        col += vec3(0.25, 1.05, 0.78) * biolum * 0.7;
        // chemin de soleil / lune scintillant
        vec2 sunA = normalize(vec2(32.0, 18.0));
        float band = pow(max(0.0, dot(normalize(vW), sunA)), 16.0);
        float glit = sin(vW.x * 6.1 + uTime * 2.2) * sin(vW.y * 5.7 - uTime * 1.7);
        float sparkle = smoothstep(0.72, 0.97, glit);
        col += vec3(1.25, 1.02, 0.72) * sparkle * band * (1.0 - uNight) * 1.15;
        col += vec3(0.6, 0.78, 1.15) * sparkle * uNight * 0.4;
        col = mix(col, vec3(0.9, 0.45, 0.2), uDusk * 0.25);
        col += vec3(1.25, 0.5, 0.18) * sparkle * band * uDusk * 1.3;
        // transparence dans les hauts-fonds : le sable transparaît
        float alpha = mix(0.32, 0.96, smoothstep(0.0, 2.3, depth));
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
//  Banc de poissons : un seul draw call instancié, allure
//  individuelle bornée, respiration de formation, fuite
// ------------------------------------------------------------
const school = { fish: [], mesh: null, center: { a: 0.8, r: 66 }, alert: 0 };
{
  const N = 110;
  // poisson : corps fuselé + caudale, fusionnés en une géométrie
  const body = new THREE.SphereGeometry(0.5, 8, 6);
  body.applyMatrix4(new THREE.Matrix4().makeScale(1.7, 0.55, 0.28));
  const tail = new THREE.ConeGeometry(0.28, 0.5, 4);
  tail.applyMatrix4(new THREE.Matrix4()
    .multiply(new THREE.Matrix4().makeTranslation(-1.0, 0, 0))
    .multiply(new THREE.Matrix4().makeRotationZ(Math.PI / 2)));
  tail.applyMatrix4(new THREE.Matrix4().makeScale(1, 1, 0.22));
  const geo = mergeGeometries([body.toNonIndexed(), tail.toNonIndexed()]);
  geo.applyMatrix4(new THREE.Matrix4().makeScale(0.55, 0.55, 0.55));
  const mat = TOON({ color: 0xffffff });
  school.mesh = new THREE.InstancedMesh(geo, mat, N);
  const c = new THREE.Color();
  const frng = mulberry32(777);
  for (let i = 0; i < N; i++) {
    school.fish.push({
      slotA: frng() * Math.PI * 2,          // position dans la formation
      slotR: 0.5 + frng() * 4.5,
      slotY: -0.25 - frng() * 0.55,
      pace: 0.85 + frng() * 0.3,            // variation d'allure bornée
      ph: frng() * 9,
    });
    c.setHSL(0.52 + frng() * 0.08, 0.35, 0.55 + frng() * 0.2);
    school.mesh.setColorAt(i, c);
  }
  scene.add(school.mesh);
}
function updateSchool(dt, t) {
  // le centre du banc dérive le long du lagon
  school.center.a += dt * 0.03;
  const cx = Math.cos(school.center.a) * school.center.r;
  const cz = Math.sin(school.center.a) * school.center.r;
  // alerte : joueur proche ou baleine active -> compression puis fuite
  const dP = Math.hypot(player.position.x - cx, player.position.z - cz);
  const target = (dP < 12 || whale.state === 'breach') ? 1 : 0;
  school.alert += (target - school.alert) * Math.min(1, dt * (target ? 3 : 0.25));
  const spread = 1 - school.alert * 0.55;    // compression
  const burst = 1 + school.alert * 2.2;      // accélération de fuite
  const breathe = 1 + Math.sin(t * 0.5) * 0.18; // respiration de formation
  for (let i = 0; i < school.fish.length; i++) {
    const f = school.fish[i];
    const a = f.slotA + t * 0.55 * f.pace * burst;
    const r = f.slotR * spread * breathe + Math.sin(t * 1.3 + f.ph) * 0.3;
    const x = cx + Math.cos(a) * r;
    const z = cz + Math.sin(a) * r * 0.65;
    const y = f.slotY + Math.sin(t * 2.1 + f.ph) * 0.12 - school.alert * 0.5;
    dummy.position.set(x, y, z);
    dummy.rotation.set(0, -a + Math.PI, Math.sin(t * 6 * f.pace + f.ph) * 0.15);
    dummy.scale.setScalar(1);
    dummy.updateMatrix();
    school.mesh.setMatrixAt(i, dummy.matrix);
  }
  school.mesh.instanceMatrix.needsUpdate = true;
}

// ------------------------------------------------------------
//  La baleine à bosse : surfacage avec souffle, et breach
//  balistique — sortie, couronne, claque retardée, gouttelettes
//  et anneaux persistants partagent les mêmes points de contact
// ------------------------------------------------------------
const whale = { group: null, state: 'hidden', timer: 25, t: 0, kind: 'surface', n: 0, p0: new THREE.Vector3(), dir: new THREE.Vector3(), events: {} };
const seaRings = [];
{
  const g = new THREE.Group();
  const dark = TOON({ color: 0x3c4c5e });
  const belly = TOON({ color: 0x9aaab6 });
  let bodyGeo = new THREE.SphereGeometry(1, 20, 14);
  bodyGeo.applyMatrix4(new THREE.Matrix4().makeScale(3.6, 1.05, 1.15));
  bodyGeo = sculpt(bodyGeo, 0.05, 1.6, 8.8);
  const body = new THREE.Mesh(bodyGeo, dark);
  const ventral = new THREE.Mesh(new THREE.SphereGeometry(0.92, 16, 10), belly);
  ventral.scale.set(3.1, 0.8, 1.0);
  ventral.position.y = -0.32;
  // longues pectorales de mégaptère
  for (const sx of [-1, 1]) {
    const fin = new THREE.Mesh(new THREE.SphereGeometry(1, 10, 6), belly);
    fin.scale.set(1.9, 0.09, 0.5);
    fin.position.set(0.4, -0.5, sx * 1.15);
    fin.rotation.y = sx * 0.5;
    fin.rotation.z = -0.15;
    g.add(fin);
  }
  // caudale
  for (const sz of [-1, 1]) {
    const fluke = new THREE.Mesh(new THREE.SphereGeometry(1, 10, 6), dark);
    fluke.scale.set(1.1, 0.08, 0.65);
    fluke.position.set(-3.6, 0.1, sz * 0.6);
    fluke.rotation.y = sz * 0.45;
    g.add(fluke);
  }
  const dorsal = new THREE.Mesh(new THREE.ConeGeometry(0.35, 0.55, 6), dark);
  dorsal.position.set(-1.4, 1.0, 0);
  g.add(body, ventral, dorsal);
  g.traverse(o => { if (o.isMesh) o.castShadow = true; });
  g.visible = false;
  scene.add(g);
  whale.group = g;
}
function spawnSeaRing(x, z, big) {
  const m = new THREE.Mesh(
    new THREE.RingGeometry(0.85, 1.12, 40),
    new THREE.MeshBasicMaterial({
      color: 0xdff4ff, transparent: true, opacity: 0.8,
      blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide,
    })
  );
  m.rotation.x = -Math.PI / 2;
  m.position.set(x, 0.06, z);
  m.scale.setScalar(big ? 2.2 : 1);
  scene.add(m);
  seaRings.push({ m, life: 1, speed: big ? 4.5 : 2.6 });
}
function updateSeaRings(dt) {
  for (let i = seaRings.length - 1; i >= 0; i--) {
    const r = seaRings[i];
    r.life -= dt * 0.24;
    r.m.scale.addScalar(dt * r.speed);
    r.m.material.opacity = Math.max(0, r.life) * 0.8;
    if (r.life <= 0) {
      scene.remove(r.m);
      r.m.geometry.dispose(); r.m.material.dispose();
      seaRings.splice(i, 1);
    }
  }
}
function whaleStart() {
  // apparaît dans le secteur de mer que le joueur regarde probablement
  const pa = Math.atan2(player.position.z, player.position.x) + (Math.random() - 0.5) * 1.3;
  const r = 86 + Math.random() * 22;
  whale.p0.set(Math.cos(pa) * r, -5, Math.sin(pa) * r);
  whale.dir.set(-Math.sin(pa), 0, Math.cos(pa)); // tangentiel
  whale.n++;
  whale.kind = (whale.n % 3 === 0) ? 'breach' : 'surface';
  whale.state = whale.kind;
  whale.t = 0;
  whale.events = {};
  whale.group.visible = true;
}
function updateWhale(dt, t) {
  updateSeaRings(dt);
  if (whale.state === 'hidden') {
    whale.timer -= dt;
    if (whale.timer <= 0) whaleStart();
    return;
  }
  whale.t += dt;
  const g = whale.group, u = whale.t;
  if (whale.state === 'surface') {
    // arc avant peu profond : le dos crève la surface, souffle, replongée
    const k = u / 9.0;
    g.position.copy(whale.p0).addScaledVector(whale.dir, u * 1.6);
    g.position.y = -3.4 + Math.sin(Math.min(1, k) * Math.PI) * 3.9;
    g.rotation.set(0, Math.atan2(whale.dir.x, whale.dir.z) - Math.PI / 2, 0);
    g.rotation.z = Math.cos(k * Math.PI) * -0.22; // tangage le long de l'arc
    if (!whale.events.inRing && g.position.y > -1.2) {
      whale.events.inRing = true;
      spawnSeaRing(g.position.x, g.position.z, false);
    }
    if (!whale.events.blow && k > 0.42) {
      whale.events.blow = true;
      sfx.whaleBlow();
      // souffle : condensation brève au niveau de l'évent
      for (let i = 0; i < 8; i++) {
        const spr = new THREE.Sprite(new THREE.SpriteMaterial({
          map: smokeTex, transparent: true, opacity: 0.5, depthWrite: false,
        }));
        spr.position.set(g.position.x + 1.2, 0.6, g.position.z);
        spr.scale.setScalar(0.4);
        scene.add(spr);
        smokes.push({ spr, life: 1.1 + Math.random() * 0.4 });
      }
    }
    if (!whale.events.outRing && k > 0.8 && g.position.y < -1.0) {
      whale.events.outRing = true;
      spawnSeaRing(g.position.x, g.position.z, false);
    }
    if (k >= 1.15) { whale.state = 'hidden'; whale.timer = 55 + Math.random() * 45; g.visible = false; }
  } else if (whale.state === 'breach') {
    // approche accélérée puis breach mené par la gravité
    const T0 = 2.2; // montée sous-marine
    if (u < T0) {
      const k = u / T0;
      g.position.copy(whale.p0).addScaledVector(whale.dir, u * 3.0);
      g.position.y = -6.5 + k * k * 5.8; // accélération
      g.rotation.set(0, Math.atan2(whale.dir.x, whale.dir.z) - Math.PI / 2, 0);
      g.rotation.z = 0.9; // cabré vers la surface
    } else {
      const b = u - T0; // phase balistique
      const vy = 8.6;
      const y = -0.7 + vy * b - 4.9 * b * b;
      g.position.copy(whale.p0).addScaledVector(whale.dir, T0 * 3.0 + b * 2.2);
      g.position.y = y;
      const contactX = g.position.x, contactZ = g.position.z;
      if (!whale.events.exit) {
        // jaillissement : tous les effets partagent ce point de contact
        whale.events.exit = { x: contactX, z: contactZ };
        spawnBurst(new THREE.Vector3(contactX, 0.4, contactZ), 0xe8f6ff, 34, 7);
        spawnSeaRing(contactX, contactZ, false);
      }
      // roulis à travers l'apex, retombée sur le flanc
      const roll = Math.min(1, b / 1.35);
      g.rotation.z = 0.9 - roll * 1.1;
      g.rotation.x = roll * 2.3;
      if (y <= -0.6 && !whale.events.slap) {
        whale.events.slap = { x: contactX, z: contactZ };
        sfx.whaleSlap();
        // couronne primaire
        spawnBurst(new THREE.Vector3(contactX, 0.5, contactZ), 0xffffff, 60, 10);
        spawnSeaRing(contactX, contactZ, true);
        spawnSeaRing(contactX, contactZ, false);
        // claque du corps, retardée, au même point
        setTimeout(() => {
          spawnBurst(new THREE.Vector3(contactX, 0.4, contactZ), 0xdff0ff, 40, 7);
          spawnSeaRing(contactX, contactZ, true);
        }, 260);
        // brume
        for (let i = 0; i < 10; i++) {
          const spr = new THREE.Sprite(new THREE.SpriteMaterial({
            map: smokeTex, transparent: true, opacity: 0.45, depthWrite: false,
          }));
          spr.position.set(contactX + (Math.random() - 0.5) * 4, 0.8, contactZ + (Math.random() - 0.5) * 4);
          spr.scale.setScalar(1.2);
          scene.add(spr);
          smokes.push({ spr, life: 1.6 + Math.random() * 0.8 });
        }
      }
      if (y < -6) { whale.state = 'hidden'; whale.timer = 70 + Math.random() * 50; g.visible = false; }
    }
  }
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

// Pins (3 étages de feuillage arrondis, teintes variées, vent)
{
  const N = 60;
  const trunkGeo = new THREE.CylinderGeometry(0.2, 0.34, 2.2, 14, 2);
  const trunkMat = TOON({ color: 0x74513a });
  const leafGeo = sculpt(new THREE.ConeGeometry(1.5, 2.4, 22, 4), 0.09, 2.4, 3.1);
  const leafMat = stylize(TOON({ color: 0xffffff }),
    { sway: 0.07, swayY: [-1.2, 1.2] });
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
    const hue = rng() < 0.28 ? 0.44 + rng() * 0.07 : 0.3 + rng() * 0.09; // quelques pins turquoise
    for (let k = 0; k < 3; k++) {
      dummy.position.set(s.x - lean * k, s.h + (2.3 + k * 1.05) * scale, s.z);
      dummy.scale.setScalar(scale * (1 - k * 0.26));
      dummy.updateMatrix();
      leaves.setMatrixAt(li, dummy.matrix);
      leafColor.setHSL(hue, 0.42 + rng() * 0.15, 0.33 + k * 0.05 + rng() * 0.05);
      leaves.setColorAt(li, leafColor);
      li++;
    }
    colliders.push({ x: s.x, z: s.z, r: 0.7 * scale });
  }
  trunks.count = ti; leaves.count = li;
  scene.add(trunks, leaves);
}

// Feuillus (boules de feuillage rondes sur tronc, vent)
{
  const N = 26;
  const trunkGeo = new THREE.CylinderGeometry(0.16, 0.28, 1.7, 10);
  const trunkMat = TOON({ color: 0x84604a });
  const blobGeo = sculpt(new THREE.IcosahedronGeometry(1.0, 3), 0.11, 2.3, 5.7);
  const blobMat = stylize(TOON({ color: 0xffffff }),
    { sway: 0.09, swayY: [-1, 1] });
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
    const hue = rng() < 0.22 ? 0.72 + rng() * 0.08 : 0.24 + rng() * 0.14; // quelques feuillus pourpres
    for (let k = 0; k < 3; k++) {
      const ox = (rng() - 0.5) * 1.1, oz = (rng() - 0.5) * 1.1;
      dummy.position.set(s.x + ox * scale, s.h + (1.9 + rng() * 0.7) * scale, s.z + oz * scale);
      dummy.scale.setScalar(scale * (0.7 + rng() * 0.5));
      dummy.rotation.set(rng() * 3, rng() * 3, rng() * 3);
      dummy.updateMatrix();
      blobs.setMatrixAt(bi, dummy.matrix);
      c.setHSL(hue, 0.45, 0.36 + rng() * 0.14);
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
  const trunkMat = TOON({ color: 0x9a7248 });
  const leafMat = stylize(TOON({ color: 0x4faf52 }),
    { sway: 0.07, swayY: [-0.6, 0.6] });
  const cocoMat = TOON({ color: 0x6e4a2e });
  const segGeo = new THREE.CylinderGeometry(0.13, 0.18, 1.1, 9);
  const leafGeo = new THREE.SphereGeometry(1, 14, 10);
  const cocoGeo = new THREE.SphereGeometry(0.14, 8, 6);
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

// Rochers : 4 variantes haute densité sculptées (facettes anguleuses)
const rockVariantGeos = [];
{
  for (let vi = 0; vi < 4; vi++) {
    rockVariantGeos.push(sculpt(
      new THREE.IcosahedronGeometry(0.9, 2),
      0.15 + vi * 0.035, 1.7 + vi * 0.6, vi * 7.3, true
    ));
  }
  const mat = stylize(TOON({ color: 0xffffff }), { grain: true });
  const per = 8;
  const meshes = rockVariantGeos.map(g => {
    const m = new THREE.InstancedMesh(g, mat, per);
    m.castShadow = m.receiveShadow = true;
    return m;
  });
  const counts = [0, 0, 0, 0];
  const c = new THREE.Color();
  for (let i = 0; i < 26; i++) {
    const s = randSpot(8, 54, 0.15);
    if (!s) continue;
    const vi = i % 4;
    if (counts[vi] >= per) continue;
    const sc = 0.5 + rng() * 1.3;
    dummy.position.set(s.x, s.h + sc * 0.3, s.z);
    dummy.scale.set(sc, sc * (0.6 + rng() * 0.5), sc);
    dummy.rotation.set(rng(), rng() * Math.PI * 2, rng());
    dummy.updateMatrix();
    meshes[vi].setMatrixAt(counts[vi], dummy.matrix);
    c.setHSL(0.08 + rng() * 0.55, 0.03 + rng() * 0.06, 0.5 + rng() * 0.16);
    meshes[vi].setColorAt(counts[vi], c);
    counts[vi]++;
    if (sc > 0.8) colliders.push({ x: s.x, z: s.z, r: sc * 0.8 });
  }
  meshes.forEach((m, i) => { m.count = counts[i]; scene.add(m); });
}

// Champ d'herbe dense (milliers de brins qui ondulent — façon plaine d'Hyrule)
{
  const N = 6000;
  const bladeGeo = new THREE.PlaneGeometry(0.1, 0.62, 1, 2);
  bladeGeo.translate(0, 0.31, 0); // ancré au sol
  const mat = stylize(TOON({ color: 0xffffff, side: THREE.DoubleSide }),
    { sway: 0.16, swayY: [0.0, 0.55] });
  const blades = new THREE.InstancedMesh(bladeGeo, mat, N);
  blades.receiveShadow = true;
  const c = new THREE.Color();
  let bi = 0;
  for (let i = 0; i < N * 3 && bi < N; i++) {
    const a = rng() * Math.PI * 2;
    const r = Math.sqrt(rng()) * 54;
    const x = Math.cos(a) * r, z = Math.sin(a) * r;
    const h = terrainH(x, z);
    if (h < 0.45 || h > 3.4) continue;
    if ((x - 0) ** 2 + (z + 38) ** 2 < 64) continue; // pas dans le temple
    dummy.position.set(x, h - 0.02, z);
    dummy.rotation.set((rng() - 0.5) * 0.22, rng() * Math.PI, (rng() - 0.5) * 0.22);
    dummy.scale.set(0.8 + rng() * 0.6, 0.65 + rng() * 0.85, 1);
    dummy.updateMatrix();
    blades.setMatrixAt(bi, dummy.matrix);
    c.setHSL(0.25 + rng() * 0.08, 0.55 + rng() * 0.15, 0.26 + rng() * 0.13);
    blades.setColorAt(bi, c);
    bi++;
  }
  blades.count = bi;
  scene.add(blades);
}

// Touffes d'herbe (ondulent dans le vent)
{
  const N = 320;
  const geo = new THREE.ConeGeometry(0.05, 0.42, 6);
  const mat = stylize(TOON({ color: 0xffffff }),
    { sway: 0.16, swayY: [-0.21, 0.21] });
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
  const stemGeo = new THREE.CylinderGeometry(0.02, 0.03, 0.34, 6);
  const stemMat = stylize(TOON({ color: 0x3f8a3c }),
    { sway: 0.07, swayY: [-0.17, 0.17] });
  const headGeo = new THREE.SphereGeometry(0.1, 10, 8);
  const headMat = stylize(TOON({ color: 0xffffff }),
    { sway: 0.07, swayY: [-0.1, 0.1] });
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

// Feuilles portées par le vent (dérivent à travers l'île)
const windLeaves = [];
{
  const geo = new THREE.PlaneGeometry(0.13, 0.13);
  const mats = [
    TOON({ color: 0xa9cc70, side: THREE.DoubleSide, transparent: true, opacity: 0.95 }),
    TOON({ color: 0xc9df8e, side: THREE.DoubleSide, transparent: true, opacity: 0.95 }),
    TOON({ color: 0xe8c8d8, side: THREE.DoubleSide, transparent: true, opacity: 0.95 }),
  ];
  for (let i = 0; i < 34; i++) {
    const m = new THREE.Mesh(geo, mats[i % mats.length]);
    scene.add(m);
    windLeaves.push({ m, seed: rng() * 100 });
  }
}

// Papillons (voltigent le jour)
const butterflies = [];
{
  const palette = [0xffa8c8, 0xffd166, 0xa78bfa, 0x7ae0ff, 0xff9e5e];
  const wingGeo = new THREE.CircleGeometry(0.14, 8);
  for (let i = 0; i < 8; i++) {
    const s = randSpot(6, 46, 0.5) || { x: 0, z: 0, h: 1 };
    const g = new THREE.Group();
    const mat = new THREE.MeshBasicMaterial({
      color: palette[i % palette.length], side: THREE.DoubleSide,
      transparent: true, opacity: 0.95,
    });
    const wingL = new THREE.Mesh(wingGeo, mat);
    const wingR = new THREE.Mesh(wingGeo, mat);
    wingL.rotation.x = wingR.rotation.x = -Math.PI / 2;
    wingL.position.x = -0.13; wingR.position.x = 0.13;
    wingL.scale.y = wingR.scale.y = 1.4;
    const bodyB = new THREE.Mesh(
      new THREE.CapsuleGeometry(0.025, 0.14, 3, 6),
      new THREE.MeshBasicMaterial({ color: 0x3a2c30 })
    );
    bodyB.rotation.x = Math.PI / 2;
    g.add(wingL, wingR, bodyB);
    scene.add(g);
    butterflies.push({
      group: g, wingL, wingR,
      cx: s.x, cz: s.z, r: 1.5 + rng() * 2.5,
      sp: 0.5 + rng() * 0.6, ph: rng() * 9,
    });
  }
}

// Nuages moelleux
const clouds = [];
{
  const mat = TOON({
    color: 0xffffff, transparent: true, opacity: 0.92,
    emissive: 0x9aa8c0, emissiveIntensity: 0.25,
  });
  for (let i = 0; i < 9; i++) {
    const g = new THREE.Group();
    const n = 3 + ((rng() * 3) | 0);
    for (let k = 0; k < n; k++) {
      const puff = new THREE.Mesh(new THREE.SphereGeometry(2 + rng() * 2.6, 12, 9), mat);
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
  const M = (c, extra = {}) => TOON({ color: c, ...extra });
  // rim light chaude : silhouettes douces et arrondies
  const rimOpts = { rim: 0xffe4c0, rimStrength: 0.22, rimPow: 3 };
  const skinMat = stylize(M(skin), rimOpts);
  const shirtMat = stylize(M(shirt), rimOpts);
  const pantsMat = stylize(M(pants), { rim: 0xffe4c0, rimStrength: 0.15, rimPow: 3 });

  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.36, 0.5, 6, 16), shirtMat);
  body.position.y = 1.05;
  const belt = new THREE.Mesh(new THREE.CylinderGeometry(0.375, 0.375, 0.12, 16), M(0x4a3628));
  belt.position.y = 0.78;
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.34, 22, 18), skinMat);
  head.position.y = 1.78;
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.055, 8, 6), skinMat);
  nose.position.set(0, 1.75, 0.33); nose.scale.z = 1.3;

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
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.36, 18, 12, 0, Math.PI * 2, 0, Math.PI * 0.55), hairMat);
    cap.position.set(0, 1.8, -0.03);
    const tuft = new THREE.Mesh(new THREE.SphereGeometry(0.1, 10, 8), hairMat);
    tuft.position.set(0.1, 2.1, 0.08);
    g.add(cap, tuft);
  }

  const armGeo = new THREE.CapsuleGeometry(0.09, 0.5, 6, 12);
  const handGeo = new THREE.SphereGeometry(0.1, 10, 8);
  const armL = new THREE.Mesh(armGeo, shirtMat); armL.position.set(0.5, 1.18, 0);
  const armR = new THREE.Mesh(armGeo, shirtMat); armR.position.set(-0.5, 1.18, 0);
  const handL = new THREE.Mesh(handGeo, skinMat); handL.position.set(0, -0.38, 0); armL.add(handL);
  const handR = new THREE.Mesh(handGeo, skinMat); handR.position.set(0, -0.38, 0); armR.add(handR);

  const legGeo = new THREE.CapsuleGeometry(0.11, 0.42, 6, 12);
  const footGeo = new THREE.SphereGeometry(0.12, 10, 8);
  const footMat = M(0x3a2c20);
  const legL = new THREE.Mesh(legGeo, pantsMat); legL.position.set(0.17, 0.38, 0);
  const legR = new THREE.Mesh(legGeo, pantsMat); legR.position.set(-0.17, 0.38, 0);
  const footL = new THREE.Mesh(footGeo, footMat); footL.position.set(0, -0.33, 0.06); footL.scale.set(0.85, 0.55, 1.35); legL.add(footL);
  const footR = new THREE.Mesh(footGeo, footMat); footR.position.set(0, -0.33, 0.06); footR.scale.set(0.85, 0.55, 1.35); legR.add(footR);

  g.add(body, belt, head, nose, armL, armR, legL, legR);

  if (backpack) {
    const pack = new THREE.Mesh(new THREE.CapsuleGeometry(0.17, 0.24, 6, 12), M(0x8a6540));
    pack.position.set(0, 1.18, -0.37); pack.scale.set(1.15, 1, 0.7);
    const roll = new THREE.Mesh(new THREE.CapsuleGeometry(0.09, 0.26, 6, 10), M(0xc8b088));
    roll.position.set(0, 1.48, -0.37); roll.rotation.z = Math.PI / 2;
    g.add(pack, roll);
  }
  if (hat) {
    const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.52, 0.07, 18), M(hat));
    brim.position.y = 1.99;
    const top = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 16), M(hat));
    top.position.y = 2.28;
    const band = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.31, 0.1, 16), M(0xd8c27a));
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
    TOON({ color: 0xeaf2ff, emissive: 0x6a8ae8, emissiveIntensity: 1.6 })
  );
  blade.position.y = -0.88;
  const tip = new THREE.Mesh(
    new THREE.ConeGeometry(0.07, 0.18, 4),
    blade.material
  );
  tip.position.y = -1.48; tip.rotation.x = Math.PI; tip.rotation.y = Math.PI / 4;
  const guard = new THREE.Mesh(
    new THREE.BoxGeometry(0.32, 0.06, 0.1),
    TOON({ color: 0xd8b258, emissive: 0x574010, emissiveIntensity: 0.5 })
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
// la lame éclaire les alentours la nuit
const swordLight = new THREE.PointLight(0x8fb0ff, 0, 14, 1.6);
swordLight.position.set(0, 1.6, 0);
player.add(swordLight);
// traînée d'énergie du coup d'épée
const slashTrail = new THREE.Mesh(
  new THREE.TorusGeometry(1.15, 0.055, 6, 20, Math.PI * 1.1),
  new THREE.MeshBasicMaterial({
    color: 0x9fd0ff, transparent: true, opacity: 0,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide,
  })
);
slashTrail.position.set(0, 1.35, 0.55);
player.add(slashTrail);

// Le Sage
const sage = makeCharacter({ shirt: 0x55663f, pants: 0x3c4238, skin: 0xe8bd92, hair: 0xb8b8b8 });
sage.position.set(4, terrainH(4, 3), 3);
sage.rotation.y = Math.PI * 0.85;
scene.add(sage);
// robe, barbe, bâton
{
  const beard = new THREE.Mesh(
    new THREE.ConeGeometry(0.2, 0.55, 8),
    TOON({ color: 0xeeeeee })
  );
  beard.position.set(0, 1.48, 0.26); beard.rotation.x = 0.3;
  const staff = new THREE.Mesh(
    new THREE.CylinderGeometry(0.04, 0.05, 2.1, 6),
    TOON({ color: 0x8a6540 })
  );
  staff.position.set(0.62, 1.05, 0.1);
  const orb = new THREE.Mesh(
    new THREE.SphereGeometry(0.14, 12, 10),
    TOON({ color: 0x9feaff, emissive: 0x2fa8c8, emissiveIntensity: 1.2 })
  );
  orb.position.set(0.62, 2.15, 0.1);
  const orbGlow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex, color: 0x7de8ff, transparent: true, opacity: 0.7,
    blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  orbGlow.scale.setScalar(1.2);
  orbGlow.position.copy(orb.position);
  beard.castShadow = staff.castShadow = true;
  sage.add(beard, staff, orb, orbGlow);
}
colliders.push({ x: sage.position.x, z: sage.position.z, r: 0.7 });

// ------------------------------------------------------------
//  Modèles 3D animés (glTF du dépôt three.js, licence MIT)
//  Le soldat remplace les personnages procéduraux dès qu'il est
//  chargé ; en cas d'échec, le jeu garde ses personnages low-poly.
// ------------------------------------------------------------
const gltfMixers = [];
const birds = [];
function toonify(root, tint) {
  root.traverse(o => {
    if (o.isMesh) {
      const old = o.material;
      o.material = new THREE.MeshToonMaterial({
        map: old.map || null,
        color: tint !== undefined ? new THREE.Color(tint) : (old.color ? old.color.clone() : new THREE.Color(0xffffff)),
        gradientMap: toonRamp,
      });
      o.castShadow = true;
      o.frustumCulled = false; // les meshes skinnés bougent avec les os
    }
  });
}
function setSoldierAnim(sold, name) {
  if (sold.current === name || !sold.actions[name]) return;
  sold.actions[name].reset().fadeIn(0.18).play();
  if (sold.actions[sold.current]) sold.actions[sold.current].fadeOut(0.18);
  sold.current = name;
}
const gltfLoader = new GLTFLoader();

gltfLoader.load('./assets/models/Soldier.glb', (gltf) => {
  const setup = (tint, animName, timeOffset) => {
    const model = SkeletonUtils.clone(gltf.scene);
    toonify(model, tint);
    model.scale.setScalar(1.05);
    model.rotation.y = Math.PI; // le soldat du glb regarde -Z, notre avant est +Z
    const mixer = new THREE.AnimationMixer(model);
    const actions = {};
    for (const clip of gltf.animations) actions[clip.name] = mixer.clipAction(clip);
    if (actions[animName]) { actions[animName].play(); mixer.update(timeOffset); }
    gltfMixers.push(mixer);
    return { model, mixer, actions };
  };

  // --- le joueur ---
  const p = setup(undefined, 'Idle', 0);
  sword.parent.remove(sword); // récupérer la lame avant de purger le corps procédural
  for (const c of [...player.children]) player.remove(c);
  player.add(p.model, swordLight);
  let handBone = null, armBone = null, foreBone = null, spineBone = null;
  p.model.traverse(o => {
    if (!o.isBone) return;
    if (/RightHand$/.test(o.name)) handBone = o;
    if (/RightArm$/.test(o.name)) armBone = o;
    if (/RightForeArm$/.test(o.name)) foreBone = o;
    if (/Spine$/.test(o.name)) spineBone = o;
  });
  if (handBone) {
    p.model.updateMatrixWorld(true);
    handBone.add(sword);
    const ws = new THREE.Vector3();
    handBone.getWorldScale(ws);
    sword.scale.setScalar(1 / (ws.x || 1));
    sword.position.set(0, 0.08, 0.03);
    sword.rotation.set(-Math.PI / 2, 0, 0);
  } else {
    player.add(sword);
    sword.position.set(0.45, 1.6, 0);
  }
  player.userData.soldier = { ...p, armBone, foreBone, spineBone, current: 'Idle' };

  // --- Dr Vance (uniforme teinté olive, pose d'attente) ---
  const v = setup(0x92a4c0, 'Idle', 0.6);
  for (const c of [...sage.children]) sage.remove(c);
  sage.add(v.model);
  // son détecteur d'énergie flotte à côté de lui
  const orb = new THREE.Mesh(new THREE.SphereGeometry(0.12, 12, 10),
    TOON({ color: 0x9feaff, emissive: 0x2fa8c8, emissiveIntensity: 1.4 }));
  orb.position.set(0.6, 1.7, 0.25);
  const orbGlow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTex, color: 0x7de8ff, transparent: true, opacity: 0.7,
    blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  orbGlow.scale.setScalar(1.1);
  orbGlow.position.copy(orb.position);
  sage.add(orb, orbGlow);
}, undefined, (err) => console.warn('Soldier.glb indisponible, personnages procéduraux conservés', err));

// Réplicateurs : robot glTF animé (marche, coup, mort)
let robotProto = null;
gltfLoader.load('./assets/models/RobotExpressive.glb', (gltf) => {
  robotProto = gltf;
}, undefined, () => { /* fallback : entités procédurales */ });

// Oiseaux alien qui tournoient au-dessus de l'île
gltfLoader.load('./assets/models/Parrot.glb', (gltf) => {
  const tints = [0x8ae8dc, 0xd8a8f0, 0xf0d890];
  for (let i = 0; i < 3; i++) {
    const bird = SkeletonUtils.clone(gltf.scene);
    toonify(bird, tints[i]);
    const size = new THREE.Box3().setFromObject(bird).getSize(new THREE.Vector3());
    bird.scale.setScalar(1.5 / Math.max(size.x, size.y, size.z));
    const mixer = new THREE.AnimationMixer(bird);
    if (gltf.animations.length) {
      mixer.clipAction(gltf.animations[0]).play();
      mixer.update(i * 0.3);
    }
    gltfMixers.push(mixer);
    scene.add(bird);
    birds.push({ bird, phase: i * 2.1, r: 24 + i * 9, speed: 0.14 + i * 0.03, h: 11 + i * 3 });
  }
}, undefined, () => {});


// ------------------------------------------------------------
//  Flammes & fumée (partagées : braseros + torches du temple)
// ------------------------------------------------------------
const allFlames = []; // {group, phase} — scale flicker quand visible
function makeFlame(scale = 1, energy = false) {
  const flame = new THREE.Group();
  const f1 = new THREE.Mesh(new THREE.ConeGeometry(0.34, 0.9, 8),
    energy
      ? TOON({ color: 0x7fd4ff, emissive: 0x1f7fe8, emissiveIntensity: 1.5, transparent: true, opacity: 0.92 })
      : TOON({ color: 0xffb03a, emissive: 0xff7a10, emissiveIntensity: 1.4, transparent: true, opacity: 0.95 }));
  f1.position.y = 0.45;
  const f2 = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.6, 8),
    energy
      ? TOON({ color: 0xe8f8ff, emissive: 0x8fd0ff, emissiveIntensity: 1.7 })
      : TOON({ color: 0xfff0a0, emissive: 0xffc040, emissiveIntensity: 1.6 }));
  f2.position.y = 0.6;
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: energy
      ? makeGlowTexture('rgba(200,235,255,0.95)', 'rgba(90,170,255,0.4)')
      : makeGlowTexture('rgba(255,230,170,0.95)', 'rgba(255,160,60,0.4)'),
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
//  La Porte des Étoiles + DHD (hommage fan, 100 % procédural)
// ------------------------------------------------------------
const temple = new THREE.Group();      // zone de la Porte
const chevrons = [];
let symbolBand, horizonMesh;
const horizonU = { uTime: { value: 0 }, uOpen: { value: 0 } };
let horizonTarget = 0;
const templeBaseY = terrainH(0, -38);
{
  const stone = stylize(TOON({ color: 0xb9b2a2 }), { grain: true });
  const stoneDark = stylize(TOON({ color: 0x8f8878 }), { grain: true });
  const naqahdah = stylize(TOON({ color: 0x6a7180 }), { grain: true });
  const naqahdahDark = TOON({ color: 0x4a4f5c });

  // dais circulaire + marches
  const dais = new THREE.Mesh(new THREE.CylinderGeometry(6.6, 7.2, 0.7, 72), stoneDark);
  dais.position.y = 0.35;
  const daisTop = new THREE.Mesh(new THREE.CylinderGeometry(6.2, 6.6, 0.25, 72), stone);
  daisTop.position.y = 0.82;
  temple.add(dais, daisTop);
  for (let k = 0; k < 3; k++) {
    const step = new THREE.Mesh(new THREE.BoxGeometry(4.6 - k * 0.5, 0.3, 1.2), stoneDark);
    step.position.set(0, 0.15 + k * 0.3, 7.6 - k * 0.7);
    temple.add(step);
  }

  // anneau extérieur en naqahdah martelé (haute densité + sculpture)
  const ring = new THREE.Mesh(
    sculpt(new THREE.TorusGeometry(4.1, 0.52, 26, 116), 0.028, 3.4, 2.2),
    naqahdah
  );
  ring.position.y = 5.15;
  temple.add(ring);
  // 39 séparateurs de glyphes autour de la bande
  {
    const studGeo = new THREE.BoxGeometry(0.055, 0.1, 0.58);
    const studs = new THREE.InstancedMesh(studGeo, naqahdahDark, 39);
    for (let i = 0; i < 39; i++) {
      const a = (i / 39) * Math.PI * 2;
      dummy.position.set(Math.cos(a) * 3.72, 5.15 + Math.sin(a) * 3.72, 0);
      dummy.rotation.set(0, 0, a + Math.PI / 2);
      dummy.scale.setScalar(1);
      dummy.updateMatrix();
      studs.setMatrixAt(i, dummy.matrix);
    }
    studs.castShadow = true;
    temple.add(studs);
  }

  // bande de symboles (glyphes générés en canvas)
  const glyphTex = (() => {
    const c = document.createElement('canvas');
    c.width = 512; c.height = 32;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#343948';
    ctx.fillRect(0, 0, 512, 32);
    ctx.strokeStyle = '#d8b878';
    ctx.lineWidth = 2; ctx.lineCap = 'round';
    const grng = mulberry32(93);
    for (let i = 0; i < 39; i++) {
      const x0 = i * 13.1 + 2;
      ctx.beginPath();
      ctx.moveTo(x0 + grng() * 9, 4 + grng() * 24);
      ctx.lineTo(x0 + grng() * 9, 4 + grng() * 24);
      ctx.lineTo(x0 + grng() * 9, 4 + grng() * 24);
      ctx.stroke();
      if (grng() > 0.55) {
        ctx.beginPath();
        ctx.arc(x0 + 4 + grng() * 5, 8 + grng() * 16, 2.2, 0, 7);
        ctx.stroke();
      }
    }
    const t = new THREE.CanvasTexture(c);
    t.wrapS = THREE.RepeatWrapping;
    return t;
  })();
  const bandGeo = new THREE.CylinderGeometry(3.72, 3.72, 0.6, 116, 1, true);
  bandGeo.rotateX(Math.PI / 2); // axe le long de Z
  symbolBand = new THREE.Mesh(bandGeo, TOON({ map: glyphTex, emissive: 0x6a6050, emissiveIntensity: 0.35, side: THREE.DoubleSide }));
  symbolBand.position.y = 5.15;
  temple.add(symbolBand);

  const innerRing = new THREE.Mesh(new THREE.TorusGeometry(3.45, 0.16, 14, 116), naqahdahDark);
  innerRing.position.y = 5.15;
  temple.add(innerRing);

  // 9 chevrons détaillés en V (le cœur s'illumine pendant la composition)
  for (let i = 0; i < 9; i++) {
    const a = Math.PI / 2 + (i / 9) * Math.PI * 2;
    const chg = new THREE.Group();
    const back = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.68, 0.12), naqahdahDark);
    const armL = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.52, 0.15), naqahdah);
    armL.position.set(-0.13, 0.05, 0.03); armL.rotation.z = 0.4;
    const armR = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.52, 0.15), naqahdah);
    armR.position.set(0.13, 0.05, 0.03); armR.rotation.z = -0.4;
    const core = new THREE.Mesh(
      new THREE.ConeGeometry(0.15, 0.36, 3),
      TOON({ color: 0x9a6a35, emissive: 0xff7a20, emissiveIntensity: 0 })
    );
    core.position.set(0, -0.06, 0.08);
    chg.add(back, armL, armR, core);
    chg.position.set(Math.cos(a) * 4.18, 5.15 + Math.sin(a) * 4.18, 0.42);
    chg.rotation.z = a + Math.PI / 2; // pointe vers le centre
    chg.traverse(o => { if (o.isMesh) o.castShadow = true; });
    temple.add(chg);
    chevrons.push(core);
  }

  // l'horizon des événements (la « flaque » animée en shader)
  horizonMesh = new THREE.Mesh(
    new THREE.CircleGeometry(3.4, 48),
    new THREE.ShaderMaterial({
      uniforms: horizonU,
      transparent: true, side: THREE.DoubleSide, depthWrite: false,
      vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
      fragmentShader: `
        uniform float uTime; uniform float uOpen; varying vec2 vUv;
        void main(){
          vec2 p = vUv - 0.5;
          float r = length(p) * 2.0;
          if (r > 1.0 || uOpen < 0.01) discard;
          float rip = sin(r * 26.0 - uTime * 3.4) * 0.5 + 0.5;
          float rip2 = sin(p.x * 20.0 + uTime * 1.8) * sin(p.y * 18.0 - uTime * 2.2) * 0.5 + 0.5;
          vec3 deep = vec3(0.03, 0.12, 0.30);
          vec3 mid  = vec3(0.10, 0.36, 0.72);
          vec3 hi   = vec3(0.55, 0.85, 1.25);
          vec3 col = mix(mid, deep, r);
          col += hi * rip * 0.28 * (1.0 - r * 0.6);
          col += hi * rip2 * 0.18;
          col += hi * smoothstep(0.88, 1.0, r) * 1.1;
          gl_FragColor = vec4(col * uOpen, uOpen * (0.94 - r * 0.12));
        }`,
    })
  );
  horizonMesh.position.y = 5.15;
  temple.add(horizonMesh);

  // colonnes en ruine autour du dais
  for (const [cx, cz, hgt] of [[-8, -2, 3.2], [8, -1, 2.4], [-6.5, 5, 1.6], [7, 4.5, 4.0]]) {
    const col = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, hgt, 12), stone);
    col.position.set(cx, hgt / 2 + 0.2, cz);
    col.rotation.z = (cx > 0 ? -1 : 1) * 0.05;
    temple.add(col);
    colliders.push({ x: cx, z: -38 + cz, r: 0.8 });
  }

  temple.position.set(0, templeBaseY, -38);
  temple.traverse(o => { if (o.isMesh && o !== horizonMesh) { o.castShadow = true; o.receiveShadow = true; } });
  scene.add(temple);
  colliders.push({ x: -3.6, z: -38, r: 1.0 }, { x: 3.6, z: -38, r: 1.0 });
}

// Le DHD (console de composition)
let dhdGroup;
{
  const dhd = new THREE.Group();
  dhdGroup = dhd;
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.62, 1.0, 22),
    stylize(TOON({ color: 0x6a6f7c }), { grain: true }));
  base.position.y = 0.5;
  const consoleTop = new THREE.Mesh(new THREE.CylinderGeometry(1.05, 0.75, 0.32, 38), TOON({ color: 0x545968 }));
  consoleTop.position.y = 1.1;
  consoleTop.rotation.x = 0.35;
  const dome = new THREE.Mesh(new THREE.SphereGeometry(0.3, 26, 18),
    TOON({ color: 0xff8850, emissive: 0xd84a10, emissiveIntensity: 0.8 }));
  dome.position.set(0, 1.32, -0.1);
  const domeGlow = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeGlowTexture('rgba(255,190,140,0.9)', 'rgba(255,120,50,0.35)'),
    transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  domeGlow.scale.setScalar(1.6);
  domeGlow.position.copy(dome.position);
  // deux couronnes de touches à glyphes (39 au total, quelques-unes allumées)
  {
    const btnGroup = new THREE.Group();
    btnGroup.position.y = 1.1;
    btnGroup.rotation.x = 0.35;
    const btnGeo = new THREE.BoxGeometry(0.12, 0.05, 0.17);
    const brng = mulberry32(41);
    for (const [r, n] of [[0.52, 16], [0.82, 23]]) {
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2;
        const lit = brng() < 0.2;
        const b = new THREE.Mesh(btnGeo, TOON({
          color: lit ? 0xffb070 : 0x8a5a3a,
          emissive: lit ? 0xd86a20 : 0x1a0e06,
          emissiveIntensity: lit ? 1.1 : 0.3,
        }));
        b.position.set(Math.cos(a) * r, 0.17, Math.sin(a) * r);
        b.rotation.y = -a;
        btnGroup.add(b);
      }
    }
    dhd.add(btnGroup);
  }
  dhd.add(base, consoleTop, dome, domeGlow);
  dhd.scale.setScalar(1.35);
  dhd.position.set(0, terrainH(0, -30.5), -30.5);
  dhd.traverse(o => { if (o.isMesh) o.castShadow = true; });
  scene.add(dhd);
  colliders.push({ x: 0, z: -30.5, r: 0.8 });
}

const doorSpot = new THREE.Vector3(0, 0, -29.2); // point d'interaction devant le DHD
let dialT = 0;              // séquence de composition
let dialChevrons = 0;
let kawooshDone = false, voiceShown = false;
// lumière de la Porte (s'embrase au kawoosh)
const templeLight = new THREE.PointLight(0x66c8ff, 0, 22, 1.6);
templeLight.position.set(0, 5.2, 0);
temple.add(templeLight);
let templeLightTarget = 0;

// ------------------------------------------------------------
//  Cristaux (acte 1)
// ------------------------------------------------------------
const crystals = [];
{
  const spots = [
    [30, 18], [-26, 24], [-34, -18], [24, -30], [8, 42],
  ];
  const geo = sculpt(new THREE.OctahedronGeometry(0.55, 2), 0.05, 4.2, 1.3, true);
  const innerGeo = new THREE.OctahedronGeometry(0.28, 1);
  for (let i = 0; i < CRYSTAL_COUNT; i++) {
    const [x, z] = spots[i];
    const mat = new THREE.MeshPhongMaterial({
      color: 0xffc890, emissive: 0xe85a10, emissiveIntensity: 1.2,
      shininess: 90, specular: 0xffffff,
      transparent: true, opacity: 0.88,
    });
    const m = new THREE.Mesh(geo, mat);
    const inner = new THREE.Mesh(innerGeo, new THREE.MeshBasicMaterial({ color: 0xfff0d8 }));
    m.add(inner);
    // pilier de lumière visible de loin
    const beamTex = (() => {
      const c = document.createElement('canvas');
      c.width = 16; c.height = 128;
      const ctx = c.getContext('2d');
      const grad = ctx.createLinearGradient(0, 128, 0, 0);
      grad.addColorStop(0, 'rgba(255,190,120,0.55)');
      grad.addColorStop(0.5, 'rgba(255,190,120,0.18)');
      grad.addColorStop(1, 'rgba(255,190,120,0)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 16, 128);
      return new THREE.CanvasTexture(c);
    })();
    const beam = new THREE.Mesh(
      new THREE.CylinderGeometry(0.32, 0.5, 11, 10, 1, true),
      new THREE.MeshBasicMaterial({
        map: beamTex, transparent: true, side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending, depthWrite: false,
      })
    );
    beam.position.y = 5.2;
    m.add(beam);
    const h = Math.max(terrainH(x, z), 0.3);
    m.position.set(x, h + 1.2, z);
    m.castShadow = true;
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTex, color: 0xffc088, transparent: true,
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
      map: glowTex, color: 0xffe0b8, size: 0.22, transparent: true, opacity: 0.9,
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
    TOON({ color: 0x7a5734 }));
  const board = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.5, 0.08),
    TOON({ color: 0x9c7648 }));
  board.position.y = 0.7;
  const sign = new THREE.Group();
  sign.add(post, board);
  sign.position.set(-2.5, terrainH(-2.5, 8) + 0.7, 8);
  sign.rotation.y = 0.5;
  sign.traverse(o => { if (o.isMesh) o.castShadow = true; });
  scene.add(sign);
}

// ------------------------------------------------------------
//  Obélisques de défense lantiens (acte 2)
//  (nom interne « braziers » conservé pour les sauvegardes)
// ------------------------------------------------------------
const braziers = [];
{
  const stoneMat = stylize(TOON({ color: 0x7a7f8c }), { grain: true });
  for (let i = 0; i < BRAZIER_SPOTS.length; i++) {
    const [x, z] = BRAZIER_SPOTS[i];
    const h = Math.max(terrainH(x, z), 0.3);
    const g = new THREE.Group();
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.5, 1.1), stoneMat);
    plinth.position.y = 0.25;
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.4, 2.4, 4, 4), stoneMat);
    shaft.position.y = 1.7; shaft.rotation.y = Math.PI / 4;
    for (const cy of [0.9, 2.55]) {
      const collar = new THREE.Mesh(new THREE.TorusGeometry(0.36 - (cy > 2 ? 0.09 : 0), 0.05, 8, 4), stoneMat);
      collar.position.y = cy; collar.rotation.x = Math.PI / 2; collar.rotation.z = Math.PI / 4;
      g.add(collar);
    }
    const groove = new THREE.Mesh(new THREE.BoxGeometry(0.07, 2.0, 0.47),
      TOON({ color: 0x9fd8ff, emissive: 0x2f8fd8, emissiveIntensity: 0.35 }));
    groove.position.y = 1.65;
    // cristal sommital
    const ember = new THREE.Mesh(new THREE.OctahedronGeometry(0.34, 0),
      TOON({ color: 0x9fe4ff, emissive: 0x2f8fd8, emissiveIntensity: 0.5, transparent: true, opacity: 0.95 }));
    ember.position.y = 3.25;
    const flame = makeFlame(0.9, true);
    flame.position.y = 3.15;
    flame.visible = false;
    const light = new THREE.PointLight(0x55baff, 0, 11, 1.8);
    light.position.y = 3.2;
    for (let k = 0; k < 5; k++) {
      const a = (k / 5) * Math.PI * 2;
      const st = new THREE.Mesh(new THREE.IcosahedronGeometry(0.15 + ((i + k) % 3) * 0.05, 1), stoneMat);
      st.position.set(Math.cos(a) * 1.2, 0.08, Math.sin(a) * 1.2);
      g.add(st);
    }
    g.add(plinth, shaft, groove, ember, flame, light);
    g.position.set(x, h, z);
    g.traverse(o => { if (o.isMesh) o.castShadow = true; });
    scene.add(g);
    colliders.push({ x, z, r: 0.7 });
    braziers.push({ group: g, flame, ember, light, lit: false, x, z });
  }
}
function litCount() { return braziers.filter(b => b.lit).length; }

// ------------------------------------------------------------
//  Spectres & Gardien (acte 2)
// ------------------------------------------------------------
const enemies = [];
// ombre douce projetée au sol sous chaque spectre (ils flottent)
const blobShadowTex = (() => {
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(32, 32, 2, 32, 32, 30);
  grad.addColorStop(0, 'rgba(10,14,26,0.5)');
  grad.addColorStop(0.7, 'rgba(10,14,26,0.22)');
  grad.addColorStop(1, 'rgba(10,14,26,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
})();
const blobShadowGeo = new THREE.PlaneGeometry(1.7, 1.7);
blobShadowGeo.rotateX(-Math.PI / 2);
function makeSpectre(boss = false) {
  const g = new THREE.Group();
  const bodyMat = stylize(TOON({
    color: boss ? 0xd8b8c8 : 0xc4bcf2,
    emissive: boss ? 0x8a2a3a : 0x4a3f9a,
    emissiveIntensity: 0.7,
    transparent: true, opacity: 0.82,
  }), { rim: boss ? 0xff7060 : 0x9fd8ff, rimStrength: 0.9, rimPow: 2.5 });
  const body = new THREE.Mesh(new THREE.ConeGeometry(0.55, 1.6, 16), bodyMat);
  body.position.y = 0.8; body.rotation.x = Math.PI; // pointe vers le bas
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.42, 18, 14), bodyMat);
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
      TOON({ color: 0x8a8a95, emissive: 0x2a2a35, side: THREE.DoubleSide })
    );
    crown.position.y = 2.15;
    g.add(crown);
    g.scale.setScalar(2.1);
  }
  return { group: g, mats: [bodyMat] };
}
function setEnemyAnim(e, name) {
  if (!e.actions || e.current === name || !e.actions[name]) return;
  e.actions[name].reset().fadeIn(0.15).play();
  if (e.actions[e.current]) e.actions[e.current].fadeOut(0.15);
  e.current = name;
}
function spawnSpectre(x, z, boss = false) {
  const blob = new THREE.Mesh(blobShadowGeo, new THREE.MeshBasicMaterial({
    map: blobShadowTex, transparent: true, depthWrite: false,
  }));
  if (boss) blob.scale.setScalar(2.1);
  scene.add(blob);
  const e = {
    blob, boss,
    hp: boss ? 6 : 1,
    speed: boss ? 3.4 : 2.6,
    aggro: boss ? 40 : 11,
    phase: Math.random() * 6.28,
    home: { x, z },
    dying: null, dead: false, punchT: 0,
  };
  if (robotProto) {
    // Réplicateur : robot glTF animé
    const group = new THREE.Group();
    const model = SkeletonUtils.clone(robotProto.scene);
    toonify(model, boss ? 0xd8887a : 0x9fb0c4);
    const size = new THREE.Box3().setFromObject(model).getSize(new THREE.Vector3());
    model.scale.setScalar((boss ? 4.2 : 1.95) / (size.y || 1));
    group.add(model);
    group.position.set(x, Math.max(terrainH(x, z), 0.05), z);
    scene.add(group);
    const mixer = new THREE.AnimationMixer(model);
    const actions = {};
    for (const clip of robotProto.animations) actions[clip.name] = mixer.clipAction(clip);
    if (actions.Death) {
      actions.Death.setLoop(THREE.LoopOnce);
      actions.Death.clampWhenFinished = true;
    }
    if (actions.Punch) actions.Punch.setLoop(THREE.LoopOnce);
    e.current = 'none';
    e.actions = actions;
    e.mixer = mixer;
    gltfMixers.push(mixer);
    setEnemyAnim(e, 'Idle');
    const mats = [];
    model.traverse(o => { if (o.isMesh) mats.push(o.material); });
    e.group = group; e.mats = mats; e.isRobot = true;
  } else {
    const { group, mats } = makeSpectre(boss);
    group.position.set(x, Math.max(terrainH(x, z), 0.05) + 0.55, z);
    scene.add(group);
    e.group = group; e.mats = mats; e.isRobot = false;
  }
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
  toast("Le Réplicateur Alpha apparaît !");
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
  chevron: () => { tone(160, 0.1, 'square', 0.16); tone(80, 0.2, 'sawtooth', 0.14, 0.05); },
  whaleBlow: () => { tone(900, 0.5, 'sawtooth', 0.03); tone(1400, 0.4, 'sawtooth', 0.02, 0.05); },
  whaleSlap: () => { tone(65, 0.9, 'sawtooth', 0.2, 0.1); tone(48, 1.3, 'sawtooth', 0.16, 0.2); },
  travel: () => {
    tone(520, 0.3, 'sine', 0.16); tone(400, 0.3, 'sine', 0.15, 0.18);
    tone(300, 0.35, 'sine', 0.15, 0.36); tone(210, 0.5, 'sine', 0.14, 0.55);
    tone(70, 2.2, 'sawtooth', 0.2, 0.2); tone(105, 1.8, 'sawtooth', 0.12, 0.4);
  },
  gate: () => { tone(50, 1.5, 'sawtooth', 0.26); tone(75, 1.2, 'sawtooth', 0.2, 0.1); tone(320, 0.5, 'sine', 0.15, 0.15); tone(150, 0.9, 'triangle', 0.12, 0.35); },
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
  setBanner(`⚡ Réactive les <b>obélisques lantiens</b> — ${litCount()} / ${braziers.length}`);
}
function bossBanner() {
  const hp = bossRef && !bossRef.dead ? bossRef.hp : 0;
  setBanner(`⚔️ Détruis le <b>Réplicateur Alpha</b> ! ${'🔺'.repeat(Math.max(hp, 0))}`);
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
    speaker: 'Dr Vance',
    lines: [
      "Dr Elias Vance, archéologue du SGC. Mon équipe est repartie par la Porte juste avant la tempête de naquadah…",
      "…et cette tempête a grillé le DHD. Sans lui, impossible de composer une adresse : nous sommes coincés sur P4X-731.",
      "Ses 5 cristaux de contrôle ont été éjectés et dispersés sur l'île. Ils émettent une lueur orange, tu ne peux pas les rater.",
      "Rapporte-les-moi, et je te montrerai comment composer l'adresse de la Terre !",
    ],
    onEnd: () => {
      quest.stage = 'collect';
      if (!quest.startTime) quest.startTime = performance.now();
      ui.counter.style.display = 'flex';
      setBanner("🔍 Retrouve les <b>5 cristaux du DHD</b> dispersés sur l'île");
      sfx.quest();
      toast('Nouvelle mission !');
      saveGame('collect');
    },
  },
  sageWait: {
    speaker: 'Dr Vance',
    lines: ["Cherche les lueurs orange et leurs piliers de lumière… Les cristaux sont tombés près des sentiers, des plages et des collines."],
  },
  sageDone: {
    speaker: 'Dr Vance',
    lines: [
      "Excellent travail ! Voilà… les cristaux sont réinstallés, le DHD répond.",
      "Va au DHD, au nord — la Porte des Étoiles se dresse juste derrière. Pose la main sur le dôme central : l'adresse de la Terre se composera.",
      "J'espère seulement que la Porte n'a rien… attiré pendant la panne.",
    ],
    onEnd: () => {
      quest.stage = 'temple';
      setBanner("🖐 Va au <b>DHD</b>, au nord, et compose l'adresse de la Terre");
      sfx.quest();
      toast('DHD réparé !');
      saveGame('temple');
    },
  },
  sageAfter: {
    speaker: 'Dr Vance',
    lines: ["Le DHD est au nord, juste devant la Porte. Pose la main sur le dôme central, le reste est automatique !"],
  },
  templeVoice: {
    speaker: 'Alerte du DHD',
    lines: [
      "⚠ VORTEX ENTRANT INSTABLE — signature d'énergie inconnue détectée…",
      "Une nuée de RÉPLICATEURS a traversé l'horizon avant la fermeture du vortex !",
      "Leur nuée brouille l'atmosphère : une nuit artificielle tombe sur P4X-731…",
      "Protocole lantien : réactive les 4 obélisques de défense, et détruis leur Alpha avec la lame ancienne apparue près du dais !",
    ],
    onEnd: () => { startAct2(); },
  },
  sageNight: {
    speaker: 'Dr Vance',
    lines: [
      "Des Réplicateurs ! Ces machines dévorent toute technologie… Les obélisques lantiens brouillent leur cohésion — réactive-les tous les quatre !",
      "Cette lame ancienne canalise l'énergie : c'est la seule arme qui perce leur carapace. Reviens me voir si ton courage vacille.",
    ],
  },
  sageBoss: {
    speaker: 'Dr Vance',
    lines: ["Le Réplicateur Alpha bloque la Porte ! Sa carapace cède sous la lame ancienne — frappe sans relâche, puis franchis l'horizon !"],
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
  // le vortex s'est effondré après l'incursion de l'Entité
  horizonTarget = 0;
  templeLightTarget = 0.5;
  dialChevrons = 0;
  sword.visible = true;
  ui.hearts.style.display = 'flex';
  ui.attackBtn.style.display = 'flex';
  renderHearts();
  spawnEnemies();
  brazierBanner();
  sfx.quest();
  toast('La lame ancienne est à toi !');
  saveGame('braziers');
}

function lightBrazier(b) {
  if (b.lit) return;
  b.lit = true;
  b.flame.visible = true;
  b.ember.material.emissiveIntensity = 2.2;
  spawnBurst(new THREE.Vector3(b.x, b.group.position.y + 3.2, b.z), 0x7fd4ff, 30, 5);
  sfx.brazier();
  if (litCount() >= braziers.length) {
    quest.stage = 'boss';
    spawnBoss();
    bossBanner();
    saveGame('boss');
  } else {
    brazierBanner();
    toast(`Obélisque ${litCount()} / ${braziers.length}`);
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
    if (e.isRobot) {
      e.dying = 1.9;
      setEnemyAnim(e, 'Death');
    } else {
      e.dying = 0.6;
    }
    if (e.boss) {
      quest.stage = 'dawn';
      nightTarget = 0;
      dialChevrons = 9;
      horizonTarget = 1;
      templeLightTarget = 3.0;
      setBanner('🌀 La Porte est ouverte — <b>franchis l\'horizon</b> pour rentrer !');
      toast("L'Alpha est détruit !");
      sfx.victory();
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
    toast("Les Réplicateurs t'ont repoussé au campement…");
  }
}

let traveling = false;
function startTravel() {
  if (traveling || quest.stage !== 'dawn') return;
  traveling = true;
  sfx.travel();
  const w = document.getElementById('wormhole');
  w.style.display = 'flex';
  requestAnimationFrame(() => w.classList.add('on'));
  setTimeout(finalVictory, 2600);
  setTimeout(() => { w.classList.remove('on'); }, 3300);
  setTimeout(() => { w.style.display = 'none'; }, 3900);
}

function finalVictory() {
  quest.stage = 'done';
  clearSave();
  const secs = Math.round(playMs() / 1000);
  const m = Math.floor(secs / 60), s = secs % 60;
  document.getElementById('victoryText').textContent =
    `Cristaux du DHD récupérés, obélisques réactivés, Réplicateurs détruits… et tu as franchi l'horizon des événements en ${m > 0 ? m + ' min ' : ''}${s} s. Bon retour sur Terre !`;
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
    if (dDoor < 3.5) next = { label: '🖐 Composer', action: openTemple };
  }

  if (!next && quest.stage === 'braziers') {
    for (const b of braziers) {
      if (b.lit) continue;
      if (Math.hypot(p.x - b.x, p.z - b.z) < 2.8) {
        next = { label: '⚡ Activer', action: () => lightBrazier(b) };
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
  setBanner('🌀 Composition en cours… <b>chevrons en verrouillage</b>');
  ui.actionBtn.style.display = 'none';
}

function collectCrystal(c) {
  c.taken = true;
  quest.collected++;
  ui.counterTxt.textContent = `${quest.collected} / ${CRYSTAL_COUNT}`;
  spawnBurst(c.mesh.position.clone(), 0xffb060, 30, 6);
  sfx.collect();
  scene.remove(c.mesh);
  if (quest.collected >= CRYSTAL_COUNT) {
    setBanner('✅ Tous les cristaux ! Retourne voir le <b>Dr Vance</b>');
    sfx.quest();
    toast('5 / 5 cristaux !');
  } else {
    toast(`Cristal du DHD ${quest.collected} / ${CRYSTAL_COUNT}`);
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
      if (e.isRobot) {
        // l'animation Death joue ; fondu sur la fin
        if (e.dying < 0.7) {
          const op = Math.max(0, e.dying / 0.7);
          for (const m of e.mats) { m.transparent = true; m.opacity = op; }
          e.blob.material.opacity = op;
        }
      } else {
        const op = Math.max(0, e.dying / 0.6);
        for (const m of e.mats) m.opacity = op * 0.82;
        e.blob.material.opacity = op;
        g.position.y += dt * 1.5;
      }
      if (e.dying <= 0) {
        e.dead = true;
        scene.remove(g);
        scene.remove(e.blob);
        if (e.mixer) {
          const mi = gltfMixers.indexOf(e.mixer);
          if (mi >= 0) gltfMixers.splice(mi, 1);
        }
      }
      continue;
    }
    if (e.punchT > 0) e.punchT -= dt;
    if (!frozen) {
      const dx = p.x - g.position.x, dz = p.z - g.position.z;
      const d = Math.hypot(dx, dz);
      if (d < e.aggro) {
        const s = e.speed * dt;
        if (d > 0.01 && e.punchT <= 0) {
          g.position.x += dx / d * s;
          g.position.z += dz / d * s;
        }
        g.rotation.y = Math.atan2(dx, dz);
        if (e.isRobot) setEnemyAnim(e, e.punchT > 0 ? 'Punch' : (e.boss ? 'Running' : 'Walking'));
        if (d < (e.boss ? 2.4 : 1.4)) {
          if (e.isRobot && e.punchT <= 0) { e.punchT = 0.9; setEnemyAnim(e, 'Punch'); }
          damagePlayer(e);
        }
      } else {
        if (e.isRobot) setEnemyAnim(e, 'Idle');
        g.position.x += Math.sin(t * 0.5 + e.phase) * dt * 0.5;
        g.position.z += Math.cos(t * 0.4 + e.phase) * dt * 0.5;
      }
      const dc = Math.hypot(g.position.x, g.position.z);
      if (dc > WALK_R) {
        g.position.x = g.position.x / dc * WALK_R;
        g.position.z = g.position.z / dc * WALK_R;
      }
    }
    const gnd = Math.max(terrainH(g.position.x, g.position.z), 0.05);
    g.position.y = e.isRobot ? gnd : gnd + 0.55 + Math.sin(t * 2.4 + e.phase) * 0.15;
    e.blob.position.set(g.position.x, gnd + 0.05, g.position.z);
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

  // hauteur du terrain (ne pas descendre dans l'eau) + dais de la Porte
  let groundY = Math.max(terrainH(player.position.x, player.position.z), 0.05);
  const dGate = Math.hypot(player.position.x, player.position.z + 38);
  if (dGate < 6.5) groundY = Math.max(groundY, templeBaseY + 0.95);
  player.position.y += (groundY - player.position.y) * Math.min(1, dt * 14);

  // mixers des modèles glTF (avant les overrides d'os)
  for (const m of gltfMixers) m.update(dt);
  // oiseaux qui tournoient
  for (const b of birds) {
    const a = t * b.speed + b.phase;
    b.bird.position.set(Math.cos(a) * b.r, b.h + Math.sin(t * 0.9 + b.phase) * 1.5, Math.sin(a) * b.r);
    b.bird.rotation.y = -a;
  }

  // animation du personnage (soldat glTF s'il est chargé, sinon membres procéduraux)
  const soldier = player.userData.soldier;
  if (soldier) {
    setSoldierAnim(soldier, moving ? (mag > 0.75 ? 'Run' : 'Walk') : 'Idle');
    if (attackT > 0) {
      attackT -= dt;
      const k = 1 - Math.max(attackT, 0) / 0.38;
      const sw = Math.sin(k * Math.PI);
      // frappe : le torse pivote, le bras se lève puis fauche, l'avant-bras suit
      if (soldier.spineBone) soldier.spineBone.rotation.y += sw * 0.5;
      if (soldier.armBone) soldier.armBone.rotation.x -= sw * 1.7;
      if (soldier.foreBone) soldier.foreBone.rotation.x -= sw * 0.7;
      slashTrail.material.opacity = sw * 0.85;
      slashTrail.rotation.z = 1.4 - k * 2.8;
    } else {
      slashTrail.material.opacity = 0;
    }
  } else {
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

  // lumières dynamiques
  swordLight.intensity = sword.visible ? night01 * 2.3 : 0;
  for (let i = 0; i < braziers.length; i++) {
    const b = braziers[i];
    b.light.intensity = b.lit ? 1.7 * (1 + Math.sin(t * 11 + i * 2.1) * 0.18) : 0;
  }
  templeLight.intensity += (templeLightTarget - templeLight.intensity) * Math.min(1, dt * 1.5);

  // étoiles qui scintillent (en alternance)
  starLayers[0].material.opacity = night01 * (0.75 + Math.sin(t * 2.3) * 0.25);
  starLayers[1].material.opacity = night01 * (0.75 + Math.cos(t * 1.7) * 0.25);

  // étoile filante occasionnelle
  if (meteorState.life > 0) {
    meteorState.life -= dt;
    meteor.position.addScaledVector(meteorState.vel, dt);
    meteor.material.opacity = Math.max(0, Math.min(1, meteorState.life * 2)) * night01;
    if (meteorState.life <= 0) meteorState.next = t + 7 + Math.random() * 9;
  } else if (night01 > 0.7 && t > meteorState.next) {
    meteorState.life = 1.4;
    const a = Math.random() * Math.PI * 2;
    meteor.position.set(Math.cos(a) * 220, 200 + Math.random() * 120, Math.sin(a) * 220);
    meteorState.vel.set((Math.random() - 0.5) * 180, -70, (Math.random() - 0.5) * 180);
    meteor.material.rotation = Math.atan2(-meteorState.vel.y, meteorState.vel.x);
  }

  // feuilles portées par le vent
  for (const lf of windLeaves) {
    const s = lf.seed;
    const x = -55 + (((s * 17.3) + t * (2.0 + (s % 1))) % 110);
    const z = -55 + ((s * 31.7) % 110) + Math.sin(t * 0.6 + s) * 4;
    const y = Math.max(terrainH(x, z), 0.1) + 0.9
      + Math.sin(t * 1.4 + s) * 0.7 + Math.sin(t * 3.1 + s * 2) * 0.2;
    lf.m.position.set(x, y, z);
    lf.m.rotation.set(t * 2.1 + s, t * 1.5 + s * 2, t * 1.2 + s * 3);
    lf.m.visible = Math.hypot(x, z) < 58 && lf.m.position.distanceToSquared(camera.position) > 3;
  }

  // papillons (le jour)
  const bfVisible = night01 < 0.6;
  for (const bf of butterflies) {
    // jamais collé à l'objectif de la caméra
    bf.group.visible = bfVisible && bf.group.position.distanceToSquared(camera.position) > 5;
    if (!bf.group.visible) continue;
    const a = t * bf.sp + bf.ph;
    const x = bf.cx + Math.cos(a) * bf.r;
    const z = bf.cz + Math.sin(a * 0.8) * bf.r;
    bf.group.position.set(x, Math.max(terrainH(x, z), 0.1) + 1.1 + Math.sin(t * 1.9 + bf.ph) * 0.4, z);
    bf.group.rotation.y = -a + Math.PI / 2;
    const flap = 0.25 + 0.75 * Math.abs(Math.sin(t * 16 + bf.ph));
    bf.wingL.scale.x = flap; bf.wingR.scale.x = flap;
  }

  // océan, banc de poissons, baleine
  waterU.uTime.value = t;
  updateSchool(dt, t);
  updateWhale(dt, t);
  grainPass.uniforms.uTime.value = t;
  for (const s of windShaders) s.uniforms.uTime.value = t;

  // franchir l'horizon des événements une fois la Porte rouverte
  if (quest.stage === 'dawn' && !traveling &&
      Math.abs(player.position.x) < 2.6 &&
      Math.abs(player.position.z + 38) < 1.3) {
    startTravel();
  }

  // séquence de composition de la Porte
  if (quest.stage === 'opening') {
    dialT += dt;
    symbolBand.rotation.z = Math.sin(dialT * 0.85) * 2.6;
    const lit = Math.min(7, Math.floor(dialT / 0.8));
    if (lit > dialChevrons) { dialChevrons = lit; sfx.chevron(); }
    if (dialT > 6.0 && !kawooshDone) {
      kawooshDone = true;
      horizonTarget = 1;
      templeLightTarget = 3.0;
      sfx.gate();
      spawnBurst(new THREE.Vector3(0, templeBaseY + 5.2, -36.5), 0x9fd8ff, 40, 8);
      spawnBurst(new THREE.Vector3(0, templeBaseY + 5.2, -35), 0xd8f0ff, 30, 10);
    }
    if (dialT > 8.0 && !voiceShown) {
      voiceShown = true;
      openDialogue('templeVoice');
    }
  }
  // chevrons + horizon des événements
  for (let i = 0; i < chevrons.length; i++) {
    chevrons[i].material.emissiveIntensity +=
      ((i < dialChevrons ? 1.9 : 0) - chevrons[i].material.emissiveIntensity) * Math.min(1, dt * 8);
  }
  horizonU.uOpen.value += (horizonTarget - horizonU.uOpen.value) * Math.min(1, dt * 2.2);
  horizonU.uTime.value = t;

  // spectres
  updateEnemies(dt, t);

  // transition jour/nuit
  if (Math.abs(night01 - nightTarget) > 0.001) {
    night01 += Math.sign(nightTarget - night01) * Math.min(dt * 0.25, Math.abs(nightTarget - night01));
    applyMood();
  }

  updateBursts(dt);
  updateInteractables();

  // --- caméra 3e personne avec anti-occlusion ---
  const target = new THREE.Vector3(
    player.position.x, player.position.y + 1.6, player.position.z
  );
  // si un arbre/rocher bloque la ligne de vue, la caméra se rapproche
  const dirX = Math.sin(camYaw), dirZ = Math.cos(camYaw);
  let maxXZ = 7.5 * Math.cos(camPitch);
  for (const c of colliders) {
    const rx = c.x - target.x, rz = c.z - target.z;
    const tproj = rx * dirX + rz * dirZ;
    if (tproj < 0.6 || tproj > maxXZ + c.r + 1.3) continue;
    const px = rx - dirX * tproj, pz = rz - dirZ * tproj;
    const occR = c.r + 1.3; // approx. du feuillage autour du tronc
    if (px * px + pz * pz < occR * occR) {
      maxXZ = Math.min(maxXZ, Math.max(1.8, tproj - occR - 0.2));
    }
  }
  const camDist = maxXZ / Math.max(0.3, Math.cos(camPitch));
  const desired = new THREE.Vector3(
    target.x + Math.sin(camYaw) * Math.cos(camPitch) * camDist,
    target.y + Math.sin(camPitch) * camDist,
    target.z + Math.cos(camYaw) * Math.cos(camPitch) * camDist
  );
  let minY = Math.max(terrainH(desired.x, desired.z), 0) + 0.7;
  // ne pas passer sous le dais de la Porte
  if (Math.hypot(desired.x, desired.z + 38) < 7.4) {
    minY = Math.max(minY, templeBaseY + 1.8);
  }
  if (desired.y < minY) desired.y = minY;
  camera.position.lerp(desired, started ? Math.min(1, dt * 6) : 1);
  // la caméra ne traverse jamais le sol, même en plein déplacement interpolé
  const camFloor = Math.max(terrainH(camera.position.x, camera.position.z), 0) + 0.6;
  if (camera.position.y < camFloor) camera.position.y = camFloor;
  camera.lookAt(target);
  started = true;

  composer.render();
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
      ? '✅ Tous les cristaux ! Retourne voir le <b>Dr Vance</b>'
      : "🔍 Retrouve les <b>5 cristaux du DHD</b> dispersés sur l'île");
  } else if (s.stage === 'temple') {
    quest.stage = 'temple';
    setBanner("🖐 Va au <b>DHD</b>, au nord, et compose l'adresse de la Terre");
  } else if (inAct2) {
    // la Porte s'est refermée après l'incursion
    templeLightTarget = 0.5;
    night01 = 1; nightTarget = 1;
    applyMood();
    sword.visible = true;
    ui.hearts.style.display = 'flex';
    ui.attackBtn.style.display = 'flex';
    renderHearts();
    for (const i of (s.lit || [])) {
      braziers[i].lit = true;
      braziers[i].flame.visible = true;
      braziers[i].ember.material.emissiveIntensity = 2.2;
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
setBanner("🪐 Bienvenue sur P4X-731 ! Va parler au <b>Dr Vance</b>");

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
  composer.setSize(window.innerWidth, window.innerHeight);
  bloomPass.setSize(window.innerWidth / 2, window.innerHeight / 2);
});
// iOS : re-layout après rotation
window.addEventListener('orientationchange', () => {
  setTimeout(() => window.dispatchEvent(new Event('resize')), 300);
});

// Accès debug (tests automatisés) — sans effet sur le jeu
window.__game = {
  player, quest, crystals, sage, doorSpot, braziers, enemies,
  _dhd: dhdGroup, camera, butterflies,
  doAttack, getHearts: () => hearts, getNight: () => night01,
  setCam: (yaw, pitch) => { camYaw = yaw; camPitch = pitch; },
  debugGate: (open) => { dialChevrons = open ? 9 : 0; horizonTarget = open ? 1 : 0; templeLightTarget = open ? 3 : 0.5; },
  startTravel,
  whaleNow: (kind) => { whale.timer = 0; whale.n = kind === 'breach' ? 2 : 0; },
  whale, school,
  // Exporte chaque asset héros en .glb (bibliothèque d'assets du jeu)
  exportAssets: async () => {
    const { GLTFExporter } = await import('./vendor/exporters/GLTFExporter.js');
    const exporter = new GLTFExporter();
    const clean = (obj) => {
      const c = obj.clone(true);
      const kill = [];
      c.traverse(o => {
        if (o.isSprite || o.isPoints || o.isLight ||
            (o.material && o.material.isShaderMaterial)) kill.push(o);
      });
      kill.forEach(o => o.parent && o.parent.remove(o));
      return c;
    };
    const items = {
      porte_des_etoiles: clean(temple),
      dhd: clean(window.__game._dhd),
      obelisque_lantien: clean(braziers[0].group),
      cristal_dhd: clean(crystals[0].mesh),
      rocher: new THREE.Mesh(rockVariantGeos[0], TOON({ color: 0x8f9099 })),
    };
    const out = {};
    for (const [name, obj] of Object.entries(items)) {
      const buf = await exporter.parseAsync(obj, { binary: true });
      let bin = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.length; i += 8192) {
        bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 8192));
      }
      out[name] = btoa(bin);
    }
    return out;
  },
};
