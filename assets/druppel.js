/* «Druppel» — Three.js r170. A drop of waterlelie lacquer (MeshPhysicalMaterial, transmission + clearcoat) falls into a water plane
   (128×128, CPU ripple from the impact point), the water rings, the drop flattens and morphs into a glossy almond nail tip.
   Water reflects the scene via CubeCamera + RoomEnvironment. Drag rotates. DPR ≤ 2, paused off-screen, reduced-motion = final frame.
   canvas[data-druppel="scroll"] — driven by its section scroll;  canvas[data-druppel="pick"] — morphed tip, colour via 'druppel:color' event. */
import * as T from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const g = window.gsap, ST = window.ScrollTrigger;
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const LILY = '#A8325A';

function shapes(geo) {
  const p = geo.attributes.position, n = p.count, drop = new Float32Array(n * 3), tip = new Float32Array(n * 3), ball = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i);
    ball[i * 3] = x * 0.66; ball[i * 3 + 1] = y * 0.74; ball[i * 3 + 2] = z * 0.66; // falling drop: round
    // resting drop (sessile): soft round dome on top, wider flattened base sitting on the water (no point)
    const up = Math.max(0, y), dn = Math.max(0, -y);
    const w = 0.7 * (1 + 0.16 * dn - 0.06 * up);
    drop[i * 3] = x * w; drop[i * 3 + 1] = y >= 0 ? y * 0.78 : -Math.min(dn * 0.62, 0.3) - dn * dn * 0.04; drop[i * 3 + 2] = z * w;
    // almond nail tip: long, softly pointed top, thin and curved shell
    const ff = 1 - 0.62 * Math.pow(up, 1.15), xx = x * 0.62 * ff;
    tip[i * 3] = xx; tip[i * 3 + 1] = y * 1.35; tip[i * 3 + 2] = z * 0.2 + 0.32 * (xx * xx) / 0.4 - 0.05;
  }
  return { drop, tip, ball };
}

function make(cv) {
  const mode = cv.dataset.druppel || 'scroll';
  let R;
  try { R = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { cv.closest('.dr-canvas').parentElement.classList.add('no-webgl'); document.documentElement.classList.add('no-webgl'); return; }
  R.setPixelRatio(Math.min(devicePixelRatio, 2)); R.toneMapping = T.ACESFilmicToneMapping; R.toneMappingExposure = 1.05;
  const S = new T.Scene(), C = new T.PerspectiveCamera(32, 1, 0.1, 100);
  const pm = new T.PMREMGenerator(R); S.environment = pm.fromScene(new RoomEnvironment(), 0.035).texture;
  const DARK = mode === 'scroll';
  S.fog = new T.Fog(DARK ? 0x0B1A1E : 0xd6e0df, DARK ? 8 : 5, DARK ? 19 : 12);

  /* water */
  const SEG = 128, wgeo = new T.PlaneGeometry(mode === 'pick' ? 30 : 16, mode === 'pick' ? 30 : 16, SEG, SEG); wgeo.rotateX(-Math.PI / 2);
  const cubeRT = new T.WebGLCubeRenderTarget(256, { generateMipmaps: true, minFilter: T.LinearMipmapLinearFilter });
  const cubeCam = new T.CubeCamera(0.05, 40, cubeRT); cubeCam.position.set(0, -0.6, 0); S.add(cubeCam);
  const wmat = new T.MeshPhysicalMaterial({ color: DARK ? 0x2a4a50 : 0xb8cacb, metalness: DARK ? 0.35 : 0.15, roughness: 0.06, envMap: cubeRT.texture, envMapIntensity: 1.25, clearcoat: 1, clearcoatRoughness: 0.05, transparent: true, opacity: 0.94 });
  const water = new T.Mesh(wgeo, wmat); S.add(water);
  const wbase = wgeo.attributes.position.array.slice();

  /* drop / tip */
  const geo = new T.SphereGeometry(1, 96, 72); const { drop, tip, ball } = shapes(geo);
  const mat = new T.MeshPhysicalMaterial({ color: new T.Color(LILY), roughness: 0.03, metalness: 0, transmission: 0.72, thickness: 0.45, ior: 1.52, attenuationColor: new T.Color('#7d1f3b'), attenuationDistance: 0.9, clearcoat: 1, clearcoatRoughness: 0.01, specularIntensity: 1, envMapIntensity: 1.4 });
  const obj = new T.Mesh(geo, mat); S.add(obj);
  /* meniscus: thin bright ring where the drop meets the water */
  const men = new T.Mesh(new T.TorusGeometry(0.8, 0.07, 16, 96), new T.MeshPhysicalMaterial({ color: 0xdfe9ea, roughness: 0.05, transmission: 0.6, thickness: 0.3, clearcoat: 1, transparent: true, opacity: 0.85 }));
  men.rotation.x = Math.PI / 2; men.scale.set(1, 1, 0.35); S.add(men);
  const key = new T.DirectionalLight(0xffffff, 1.6); key.position.set(-4, 6, 3); S.add(key);
  S.add(new T.HemisphereLight(0xe5ebe8, 0x0b1a1e, 0.6));
  const rim = new T.PointLight(0xE58AA6, DARK ? 30 : 0, 12); rim.position.set(3, 2.5, -2); S.add(rim);
  const fill = new T.PointLight(0xE8C25E, DARK ? 8 : 0, 10); fill.position.set(-2, 1, 4); S.add(fill);

  const st = { p: mode === 'pick' ? 1 : 0, yaw: 0, drag: 0, vis: true, t: 0, splash: -10 };
  const col = { c: new T.Color(LILY) };
  function size() { const w = cv.clientWidth || 1, h = cv.clientHeight || 1; R.setSize(w, h, false); C.aspect = w / h;
    const narrow = C.aspect < 1;
    if (mode === 'pick') { C.position.set(4.4, 3.3, 6.8); C.lookAt(0, 1.2, 0); }
    else { C.position.set(narrow ? 0 : 0.4, narrow ? 2.2 : 1.9, narrow ? 9.5 : 7.4); C.lookAt(narrow ? 0 : 0.4, narrow ? 2.0 : 1.25, 0); }
    if (mode === 'scroll') { obj.position.x = narrow ? 0 : 1.45; st.s0 = narrow ? 0.75 : 1.05; }
    C.updateProjectionMatrix(); }
  size(); addEventListener('resize', size);

  /* scroll drive */
  if (mode === 'scroll') {
    const sec = cv.closest('section');
    ST.create({ trigger: sec, start: 'top top', end: 'bottom bottom', scrub: true, onUpdate: s => { st.p = s.progress; steps(s.progress); } });
    const lis = [...sec.querySelectorAll('.dr-steps li')];
    function steps(p) { const k = p < 0.3 ? 0 : p < 0.5 ? 1 : p < 0.82 ? 2 : 3; lis.forEach((l, i) => l.classList.toggle('on', i <= k)); }
  } else {
    addEventListener('druppel:color', e => { g.to(col.c, { r: new T.Color(e.detail).r, g: new T.Color(e.detail).g, b: new T.Color(e.detail).b, duration: 0.9, ease: 'sine.inOut' }); st.splash = st.t; });
  }
  /* drag to rotate */
  let down = null;
  cv.addEventListener('pointerdown', e => { down = e.clientX; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointermove', e => { if (down === null) return; st.drag += (e.clientX - down) * 0.012; down = e.clientX; });
  cv.addEventListener('pointerup', () => down = null); cv.addEventListener('pointercancel', () => down = null);
  new IntersectionObserver(([en]) => st.vis = en.isIntersecting).observe(cv);

  const sm = x => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);
  const pa = geo.attributes.position; let frame = 0;
  function render(time) {
    st.t = time / 1000;
    const p = st.p;
    // phases: fall 0–.3 · impact/ripple .3–.5 · morph .5–.82 · mirror .82–1
    const fall = sm(p / 0.16), morph = sm((p - 0.45) / 0.35);
    // rings: start already moving (continuing film-a's drop), new burst when the drop settles at p≈.16
    const impactAge = mode === 'scroll' ? 2.2 + p * 26 : st.t - st.splash;
    let amp = mode === 'scroll' ? 0.13 * (1 - sm((p - 0.5) / 0.4)) : 0.045 + 0.06 * Math.max(0, 1 - (st.t - st.splash) / 3);
    if (RM) amp = 0;
    // water ripple (CPU) — rings from the impact point
    const wa = wgeo.attributes.position, ix = obj.position.x;
    for (let i = 0; i < wa.count; i++) {
      const x = wbase[i * 3], z = wbase[i * 3 + 2], d = Math.hypot(x - ix, z);
      const front = impactAge * 1.4 + st.t * 0.6;
      const h = amp > 0.0005 ? amp * Math.sin(d * 4.2 - front * 3) * Math.exp(-d * 0.38) * (d < impactAge * 1.6 + 1.5 ? 1 : 0) : 0;
      wa.setY(i, h + 0.006 * Math.sin(x * 1.3 + st.t * 0.6) * Math.cos(z * 1.1 + st.t * 0.4) * (RM ? 0 : 1));
    }
    wa.needsUpdate = true; wgeo.computeVertexNormals();
    // object shape
    for (let i = 0; i < pa.count; i++) {
      const k = i * 3;
      const fx = mode === 'scroll' ? fall : 1, ax = ball[k] + (drop[k] - ball[k]) * fx, ay = ball[k + 1] + (drop[k + 1] - ball[k + 1]) * fx, az = ball[k + 2] + (drop[k + 2] - ball[k + 2]) * fx;
      pa.setXYZ(i, ax + (tip[k] - ax) * morph, ay + (tip[k + 1] - ay) * morph, az + (tip[k + 2] - az) * morph);
    }
    pa.needsUpdate = true; geo.computeVertexNormals();
    if (mode === 'scroll') {
      const squash = p > 0.12 && p < 0.3 ? Math.sin(sm((p - 0.12) / 0.18) * Math.PI) * 0.22 : 0;
      const s0 = st.s0 || 1;
      obj.scale.set(s0 * (1 + squash * 0.6), s0 * (1 - squash) * (1 + 0.1 * (1 - fall)), s0 * (1 + squash * 0.6));
      obj.position.y = 1.9 * (1 - fall) + 0.3 * s0 * fall - squash * 0.15 + morph * 0.9 * s0;
      men.position.set(obj.position.x, 0.01, 0); const mv = fall * (1 - morph); men.visible = mv > 0.02;
      men.scale.set(s0 * (1 + squash * 0.6), s0 * (1 + squash * 0.6), 0.35); men.material.opacity = 0.85 * mv;
      obj.rotation.z = morph * 0.35; obj.rotation.x = -morph * 0.25;
      obj.rotation.y = st.drag + morph * 0.6 + (RM ? 0 : Math.sin(st.t * 0.4) * 0.15 * morph);
    } else {
      obj.scale.set(1.25, 1.08, 1.25); obj.position.set(0, 1.3 + Math.sin(st.t * 0.9) * 0.05, 0); men.visible = false;
      obj.rotation.set(-0.3, st.drag + st.t * 0.35, 0.25);
    }
    mat.color.copy(col.c);
    if (frame++ % 3 === 0) { water.visible = false; cubeCam.update(R, S); water.visible = true; }
    R.render(S, C);
  }
  if (RM) { st.p = 1; render(0); return; }
  R.setAnimationLoop(t => { if (st.vis) render(t); });
}

export function initDruppel() { document.querySelectorAll('canvas[data-druppel]').forEach(cv => { try { make(cv); } catch (e) { console.warn('druppel', e); document.documentElement.classList.add('no-webgl'); } }); }
