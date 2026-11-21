/* Mila Nagelstudio — site.js (ES module). Motion-kit for the standard effects (data-attributes),
   own code only for the brand pieces: Waterlijn mirrors, scroll-film with chapters, water ripples, circle veil, cursor-reveal. */
import { MK } from './vendor/motion-kit.js';
const g = window.gsap, ST = window.ScrollTrigger;
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const MOB = matchMedia('(max-width: 760px)').matches;
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const root = document.documentElement;
g.registerPlugin(...[ST, window.SplitText, window.DrawSVGPlugin, window.ScrambleTextPlugin].filter(Boolean));

/* ---------------- Waterlijn: mirror clone under every .wl heading (before SplitText runs) ---------------- */
const mirrors = [];
$$('.wl').forEach(w => {
  const h = $('.wl-h', w); if (!h) return;
  const m = h.cloneNode(true);
  m.classList.add('wl-m'); m.setAttribute('aria-hidden', 'true');
  ['data-split', 'data-chh', 'id'].forEach(a => m.removeAttribute(a));
  m.querySelectorAll('[id]').forEach(x => x.removeAttribute('id'));
  w.appendChild(m); mirrors.push(m);
});
/* ripple strength follows scroll velocity; .calm mirrors are still water */
const turb = $('#rimpel-t'), disp = $('#rimpel-d');
const rip = { s: 10, ts: 10, ph: 0 };
function rippleTick(dt) {
  rip.s += (rip.ts - rip.s) * 0.08; rip.ts += (8 - rip.ts) * 0.03; rip.ph += dt * 0.0004;
  if (disp) disp.setAttribute('scale', rip.s.toFixed(1));
  if (turb) turb.setAttribute('baseFrequency', `${(0.010 + Math.sin(rip.ph) * 0.002).toFixed(4)} ${(0.085 + Math.cos(rip.ph * 0.7) * 0.012).toFixed(4)}`);
}

/* ---------------- motion-kit (split, reveal, clip, parallax, horizontal, stack, count, marquee, magnetic, tilt, cursor, bg) ---------------- */
MK.init({ three: false });
const lenis = MK.lenis; window.__lenis = lenis;
if (lenis) lenis.on('scroll', e => { rip.ts = Math.min(34, 8 + Math.abs(e.velocity) * 1.6); });
else addEventListener('scroll', () => { rip.ts = 22; }, { passive: true });
if (!RM) g.ticker.add((t, dt) => rippleTick(dt));
/* mirrors fade in with their heading */
if (!RM) mirrors.forEach(m => { if (m.closest('.stage')) return; g.from(m, { opacity: 0, y: -20, duration: 1.4, ease: 'sine.out', scrollTrigger: { trigger: m.parentElement, start: 'top 85%' } }); });

/* ---------------- header ---------------- */
const hd = $('.hd'); let lastY = 0;
const onScroll = () => { const y = scrollY; hd.classList.toggle('scrolled', y > 40); hd.classList.toggle('hide', y > lastY && y > 400 && !root.classList.contains('menu-open')); lastY = y; };
addEventListener('scroll', onScroll, { passive: true }); onScroll();
const burger = $('.burger');
burger && burger.addEventListener('click', () => { const o = root.classList.toggle('menu-open'); burger.setAttribute('aria-expanded', o); o ? lenis && lenis.stop() : lenis && lenis.start(); });
$$('.btn').forEach(b => b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); b.style.setProperty('--mx', (e.clientX - r.left) + 'px'); }));

/* ---------------- veil: preloader (drop falls into water) + circle page transitions ---------------- */
const veil = $('#veil');
const circ = (r, x, y) => `circle(${r}% at ${x}% ${y}%)`;
function openVeil(x = 50, y = 50, delay = 0.05) {
  g.fromTo(veil, { clipPath: circ(150, x, y) }, { clipPath: circ(0, x, y), duration: RM ? 0.01 : 1.0, ease: 'power3.inOut', delay, onStart: () => root.classList.remove('veiled', 'first') });
}
if (root.classList.contains('first') && !RM) {
  try { sessionStorage.setItem('mila-seen', '1'); } catch (e) {}
  const tl = g.timeline();
  tl.from('#veil .pdrop', { y: -120, duration: 0.8, ease: 'power2.in' })
    .to('#veil .pdrop', { scaleY: 0.4, scaleX: 1.4, y: 80, opacity: 0, transformOrigin: '50% 100%', duration: 0.25 })
    .fromTo('#veil .pr', { scale: 0.2, opacity: 1, transformOrigin: '100px 150px' }, { scale: 1.6, opacity: 0, duration: 1.3, stagger: 0.14, ease: 'elastic.out(1,.6)' }, '<')
    .add(() => openVeil(50, 75, 0), '-=0.9');
} else if (root.classList.contains('veiled')) {
  const v = window.__veil || {}; openVeil(v.x ?? 50, v.y ?? 50, 0.1);
} else { try { sessionStorage.setItem('mila-seen', '1'); } catch (e) {} }
document.addEventListener('click', e => {
  const a = e.target.closest('a[href]'); if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target) return;
  const h = a.getAttribute('href'); if (!h || h.startsWith('#') || /^(https?:|tel:|mailto:)/.test(h) || !/\.html/.test(h)) return;
  e.preventDefault();
  const x = (e.clientX || innerWidth / 2) / innerWidth * 100, y = (e.clientY || innerHeight / 2) / innerHeight * 100;
  try { sessionStorage.setItem('mila-veil', JSON.stringify({ x, y })); } catch (er) {}
  root.classList.remove('menu-open');
  if (RM) { location.href = h; return; }
  g.fromTo(veil, { clipPath: circ(0, x, y) }, { clipPath: circ(150, x, y), duration: 0.75, ease: 'power2.inOut', onComplete: () => { location.href = h; } });
});
addEventListener('pageshow', e => { if (e.persisted) g.set(veil, { clipPath: circ(0, 50, 50) }); });

/* ---------------- water ripples on canvases (pointer + idle drops) ---------------- */
$$('canvas.ripples').forEach(cv => {
  if (RM) return;
  const host = cv.parentElement, ctx = cv.getContext('2d'); let W = 0, H = 0, vis = false, last = 0; const rings = [];
  const size = () => { const d = Math.min(devicePixelRatio, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * d; cv.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0); };
  size(); addEventListener('resize', size);
  new IntersectionObserver(([en]) => vis = en.isIntersecting).observe(host);
  const add = (x, y, big) => rings.push({ x, y, t: 0, max: big ? 260 : 90 + Math.random() * 60, sp: big ? 1.1 : 0.8 });
  host.addEventListener('pointermove', e => { const n = performance.now(); if (n - last < 110) return; last = n; const r = cv.getBoundingClientRect(); add(e.clientX - r.left, e.clientY - r.top, false); });
  host.addEventListener('pointerdown', e => { const r = cv.getBoundingClientRect(); add(e.clientX - r.left, e.clientY - r.top, true); });
  let idle = 0;
  g.ticker.add((t, dt) => {
    if (!vis) return;
    idle += dt; if (idle > 2600) { idle = 0; add(W * (0.45 + Math.random() * 0.45), H * (0.72 + Math.random() * 0.2), false); }
    ctx.clearRect(0, 0, W, H);
    for (let i = rings.length - 1; i >= 0; i--) {
      const r = rings[i]; r.t += dt / 1000 * r.sp; if (r.t >= 1) { rings.splice(i, 1); continue; }
      const k = 1 - Math.pow(1 - r.t, 3), a = (1 - r.t) * 0.55;
      for (let j = 0; j < 3; j++) { const rr = k * r.max * (1 - j * 0.22); if (rr <= 0) continue;
        ctx.beginPath(); ctx.ellipse(r.x, r.y, rr, rr * 0.3, 0, 0, Math.PI * 2); ctx.strokeStyle = `rgba(255,255,255,${(a * (1 - j * 0.3)).toFixed(3)})`; ctx.lineWidth = 1.2; ctx.stroke(); }
    }
  });
});

/* ---------------- scroll films (LTX clips, H.264 -g 12) ----------------
   .film: key frames every 5 s with holds (data-holds), captions .hero/.cap-step[data-i], labels/night per key.
   .pfilm: one clip, linear. Index = film-a (K1..K4) → Druppel 3D → film-b (K4..K7). */
function film(sec) {
  const stage = $('.stage', sec), v = $('video', stage), poster = $('.poster', stage);
  const src = (MOB && sec.dataset.filmM) ? sec.dataset.filmM : sec.dataset.film;
  if (MOB && sec.dataset.filmM) poster.src = poster.src.replace('-0.webp', '-m-0.webp');
  const load = () => { if (v.src) return; v.src = src; v.load(); v.addEventListener('loadeddata', () => v.classList.add('ready'), { once: true }); };
  if (v.getAttribute('preload') === 'auto') load(); else ST.create({ trigger: sec, start: 'top 250%', once: true, onEnter: load });
  const unlock = () => { v.play().then(() => v.pause()).catch(() => {}); removeEventListener('touchstart', unlock); };
  addEventListener('touchstart', unlock, { passive: true });
  const isMain = sec.classList.contains('film');
  const st = { p: 0, cur: 0, vis: false };
  ST.create({ trigger: sec, start: 'top top', end: 'bottom bottom', onUpdate: s => st.p = s.progress });
  new IntersectionObserver(([en]) => st.vis = en.isIntersecting).observe(sec);
  const H = (sec.dataset.holds || '').split(',').filter(Boolean).map(Number), N = H.length;
  const TOT = H.reduce((a, b) => a + b, 0) + (N - 1);
  function mapKeys(p, dur) {
    let u = p * TOT;
    for (let i = 0; i < N; i++) {
      if (u <= H[i]) return { t: Math.min(i * 5, dur - 0.05), ch: i };
      u -= H[i]; if (i === N - 1) break;
      if (u <= 1) { const e = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; return { t: Math.min((i + e) * 5, dur - 0.05), ch: u < 0.5 ? i : i + 1 }; }
      u -= 1;
    }
    return { t: dur - 0.05, ch: N - 1 };
  }
  let ch = -1; const chap = isMain ? chapters(sec) : null;
  const bar = $('.sbar i', stage), ph = $('.ph', stage);
  if (ph && !RM) g.to(ph, { opacity: 0, y: -60, filter: 'blur(6px)', ease: 'none', scrollTrigger: { trigger: sec, start: '55% top', end: 'bottom bottom', scrub: true } });
  g.ticker.add(() => {
    if (!st.vis) return;
    const dur = v.duration || (isMain ? 15 : 5);
    let target;
    if (isMain) { const m = mapKeys(st.p, dur); target = m.t; if (m.ch !== ch) { ch = m.ch; chap(ch, m.t); } }
    else target = st.p * (dur - 0.05);
    st.cur += (target - st.cur) * (RM ? 1 : 0.16);
    if (bar) bar.style.transform = `scaleX(${st.p})`;
    if (v.readyState >= 1 && !v.seeking && Math.abs(v.currentTime - st.cur) > 0.035) { try { v.currentTime = st.cur; } catch (e) {} }
  });
}
function chapters(sec) {
  const stage = $('.stage', sec), laag = $('.laag', stage), tc = $('.tc', stage);
  const caps = {}; $$('[data-i]', stage).forEach(el => caps[el.dataset.i] = el);
  const depth = $('.depth', stage), dot = $('.dot', stage), hint = $('.scrollhint', stage);
  const splits = {}; Object.entries(caps).forEach(([i, el]) => { const h = $('[data-chh]', el); if (h && window.SplitText) splits[i] = new SplitText(h, { type: 'lines', mask: 'lines' }); });
  const labels = (sec.dataset.labels || '').split('|'), night = (sec.dataset.night || '').split(',').map(Number);
  const base = sec.classList.contains('fb') ? 15 : 0, calmAt = labels.findIndex(l => l.startsWith('Laag 05'));
  const isA = !!$('.hero', stage);
  const half = sec.classList.contains('fb') ? 0.5 : 0;
  ST.create({ trigger: sec, start: 'top top', end: 'bottom bottom', onUpdate: s => { if (dot) dot.style.top = (half + s.progress * 0.5) * 100 + '%'; } });
  let prev = 0, init = false;
  return c => {
    if (!init) { init = true; if (c === 0 && isA) return; }
    stage.classList.toggle('night', !!night[c]);
    if (depth) depth.classList.toggle('on', isA ? c > 0 : !(labels[c] || '').startsWith('Waterloostraat'));
    if (hint) hint.style.opacity = c === 0 ? '' : 0;
    if (laag && labels[c]) RM || !g.plugins.scrambleText ? laag.textContent = labels[c] : g.to(laag, { duration: 0.8, scrambleText: { text: labels[c], chars: '0123456789/', speed: 0.6 } });
    if (tc) tc.textContent = `00:${String(base + c * 5).padStart(2, '0')}`;
    $$('.wl-m', stage).forEach(m => m.classList.toggle('calm', c === calmAt));
    if (c === calmAt) rip.ts = 0;
    const out = caps[prev], inn = caps[c];
    if (out && out !== inn) g.to(out, { opacity: 0, y: -40, filter: 'blur(8px)', duration: RM ? 0 : 0.6, ease: 'power2.in', onComplete: () => { out.classList.remove('on'); out.style.visibility = 'hidden'; } });
    if (inn && inn !== out) {
      g.killTweensOf(inn); inn.classList.add('on'); inn.style.visibility = 'visible';
      g.fromTo(inn, { opacity: 0, y: 0, filter: 'blur(0px)' }, { opacity: 1, duration: RM ? 0 : 0.5, delay: RM ? 0 : 0.25 });
      const sp = splits[c];
      if (sp && !RM) g.fromTo(sp.lines, { yPercent: 110, filter: 'blur(6px)' }, { yPercent: 0, filter: 'blur(0px)', duration: 1.1, stagger: 0.09, ease: 'power2.out', delay: 0.3 });
      const rest = $$('.tag, p, .row, .wl-m', inn);
      if (!RM) g.fromTo(rest, { opacity: 0, y: 24 }, { opacity: (i, el) => el.classList.contains('wl-m') ? 0.26 : 1, y: 0, duration: 1, stagger: 0.08, ease: 'sine.out', delay: 0.45 });
    }
    prev = c;
  };
}
$$('.film, .pfilm').forEach(film);
/* hero intro (index first screen) */
if (!RM) { const h = $('.film .hero'); if (h) { h.classList.add('on'); g.from($$('.chip, .wl, .lead, .row, .rating', h), { opacity: 0, y: 40, filter: 'blur(6px)', duration: 1.3, stagger: 0.12, ease: 'power2.out', delay: root.classList.contains('first') ? 1.6 : 0.5 }); } }
$$('.pfilm .ph').forEach(ph => { if (!RM) g.from(ph.children, { opacity: 0, y: 40, filter: 'blur(6px)', duration: 1.2, stagger: 0.12, ease: 'power2.out', delay: 0.5 }); });

/* finale: LTX clip (dawn → fog → dusk) scrubbed while the finale scrolls in — the film runs to the end of every page */
$$('[data-finfilm]').forEach(box => {
  const v = $('video', box); if (!v || RM) return;
  ST.create({ trigger: box.parentElement, start: 'top 160%', once: true, onEnter: () => { v.src = MOB ? box.dataset.finfilmM : box.dataset.finfilm; v.preload = 'auto'; v.load(); v.addEventListener('loadeddata', () => v.classList.add('ready'), { once: true }); } });
  const st = { t: 0, cur: 0 };
  ST.create({ trigger: box.parentElement, start: 'top bottom', end: 'bottom bottom', onUpdate: s => st.t = s.progress });
  g.ticker.add(() => { if (!v.duration) return; st.cur += (st.t * (v.duration - 0.05) - st.cur) * 0.14; if (!v.seeking && Math.abs(v.currentTime - st.cur) > 0.035) v.currentTime = st.cur; });
});

/* diensten: four compositions — mask iris (pin), drifting word band, rotating arch, growing arch */
if (!RM) {
  $$('.sv-mask').forEach(sec => { const pin = $('.sv-pin', sec), img = $('.sv-img', sec), t = $('.sv-t', sec);
    g.timeline({ scrollTrigger: { trigger: sec, start: 'top top', end: '+=120%', pin: pin, scrub: 1 } })
      .fromTo(img, { clipPath: 'circle(14% at 70% 55%)' }, { clipPath: 'circle(80% at 60% 50%)', ease: 'none' })
      .fromTo($('img', img), { scale: 1.35 }, { scale: 1, ease: 'none' }, 0)
      .from(t.children, { y: 60, opacity: 0, stagger: 0.08, ease: 'power2.out' }, 0.25); });
  $$('.band-word span').forEach(w => g.fromTo(w, { xPercent: 0 }, { xPercent: -45, ease: 'none', scrollTrigger: { trigger: w.closest('section'), start: 'top bottom', end: 'bottom top', scrub: true } }));
  $$('.kl-arch').forEach(a => g.fromTo(a, { rotate: -6, yPercent: 8 }, { rotate: 4, yPercent: -8, ease: 'none', scrollTrigger: { trigger: a.closest('section'), start: 'top bottom', end: 'bottom top', scrub: true } }));
  $$('.ar-img').forEach(a => g.fromTo(a, { scale: 0.72, borderRadius: '50% 50% 50% 50%' }, { scale: 1, borderRadius: '300px 300px 24px 24px', ease: 'none', scrollTrigger: { trigger: a, start: 'top 95%', end: 'center 50%', scrub: true } }));
}


/* index: four arches, four motions — iris, slow parallax, counter-parallax + zoom, rising mask */
if (!RM) {
  const T = el => ({ trigger: el, start: 'top bottom', end: 'bottom top', scrub: true });
  $$('.dimg.m1').forEach(a => g.fromTo(a, { clipPath: 'circle(18% at 50% 60%)' }, { clipPath: 'circle(75% at 50% 50%)', ease: 'none', scrollTrigger: { trigger: a, start: 'top 95%', end: 'center 45%', scrub: true } }));
  $$('.dimg.m2 img').forEach(i => g.fromTo(i, { yPercent: -14 }, { yPercent: 6, ease: 'none', scrollTrigger: T(i.parentElement) }));
  $$('.dimg.m3 img').forEach(i => g.fromTo(i, { yPercent: 8, scale: 1.25 }, { yPercent: -10, scale: 1.05, ease: 'none', scrollTrigger: T(i.parentElement) }));
  $$('.dimg.m4').forEach(a => g.fromTo(a, { clipPath: 'inset(100% 0% 0% 0% round 160px 160px 18px 18px)' }, { clipPath: 'inset(0% 0% 0% 0% round 160px 160px 18px 18px)', ease: 'none', scrollTrigger: { trigger: a, start: 'top 95%', end: 'center 50%', scrub: true } }));
  $$('.hero-drop').forEach(d => g.to(d, { yPercent: 140, scale: 0.6, opacity: 0, ease: 'none', scrollTrigger: { trigger: d.closest('section'), start: 'top top', end: '12% top', scrub: true } }));
}

/* ---------------- DrawSVG water circles / lines ---------------- */
if (!RM && g.plugins.drawSVG) $$('svg.rings, svg.hoe-line, svg.route, svg.ar-line').forEach(s => {
  g.from($$('.dr', s), { drawSVG: '50% 50%', duration: 1.8, stagger: 0.18, ease: 'sine.inOut', scrollTrigger: { trigger: s, start: 'top 85%' } });
  if (s.classList.contains('rings')) g.from($$('.dr', s), { scale: 0.6, transformOrigin: '50% 50%', duration: 2, stagger: 0.18, ease: 'elastic.out(1,.6)', scrollTrigger: { trigger: s, start: 'top 85%' } });
});

/* ---------------- 4,5 rating (real Salonkee number) ---------------- */
$$('.n45').forEach(el => { if (RM) return; const o = { v: 0 }; g.to(o, { v: 4.5, duration: 2, ease: 'power2.out', scrollTrigger: { trigger: el, start: 'top 90%' }, onUpdate: () => el.textContent = o.v.toFixed(1).replace('.', ',') }); });

/* ---------------- ScrambleText phone ---------------- */
$$('.scr').forEach(el => { if (RM || !g.plugins.scrambleText) return; g.from(el, { duration: 1.6, scrambleText: { text: el.dataset.scr, chars: '0123456789+ ', revealDelay: 0.3 }, scrollTrigger: { trigger: el, start: 'top 90%' } }); });

/* ---------------- cursor-reveal: water turns clear under the cursor ---------------- */
$$('.reveal-cur').forEach(sec => {
  const sharp = $('.rv-bg .sharp', sec); if (!sharp) return;
  const r = { r: 0, x: 50, y: 50 };
  const apply = () => { sharp.style.setProperty('--r', r.r + 'px'); sharp.style.setProperty('--x', r.x + '%'); sharp.style.setProperty('--y', r.y + '%'); };
  if (matchMedia('(hover:hover)').matches && !RM) {
    sec.addEventListener('pointermove', e => { const b = sec.getBoundingClientRect(); g.to(r, { x: (e.clientX - b.left) / b.width * 100, y: (e.clientY - b.top) / b.height * 100, r: 220, duration: 0.6, ease: 'power2.out', onUpdate: apply }); });
    sec.addEventListener('pointerleave', () => g.to(r, { r: 0, duration: 0.8, onUpdate: apply }));
  } else if (!RM) {
    g.to(r, { r: 170, duration: 1, onUpdate: apply, scrollTrigger: { trigger: sec, start: 'top 60%' } });
    g.to(r, { x: 80, y: 40, duration: 6, yoyo: true, repeat: -1, ease: 'sine.inOut', onUpdate: apply });
  }
});

/* ---------------- 3D Druppel (Three.js) ---------------- */
if ($('canvas[data-druppel]')) import('./druppel.js').then(m => m.initDruppel()).catch(e => { console.warn('druppel', e); root.classList.add('no-webgl'); });

addEventListener('load', () => ST.refresh());
