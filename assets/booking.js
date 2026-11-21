/* Mila Nagelstudio — 4-step demo booking (behandeling+kleur+afwerking → dag/tijd → gegevens → bevestiging).
   Adapted from golden-fingers/booking.js. Nothing is sent or booked; only the form draft is kept in localStorage (try/catch).
   Colour choice is sent to the 3D Druppel via the 'druppel:color' event. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var wiz = $('#wizard'); if (!wiz) return;
  var pad = function (n) { return ('0' + n).slice(-2); };
  var DAYS = ['zo', 'ma', 'di', 'wo', 'do', 'vr', 'za'];
  var DAYS_L = ['zondag', 'maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag'];
  var MON = ['jan', 'feb', 'mrt', 'apr', 'mei', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'];
  var MON_L = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'];
  var KEY = 'mila-afspraak-concept';
  var st = { step: 1, dienst: null, kleur: null, afw: 'glans', day: null, time: null };
  var knames = {}, afnames = {};
  $$('input[name=kleur]', wiz).forEach(function (r) { knames[r.value] = r.dataset.n; });
  $$('input[name=afw]', wiz).forEach(function (r) { afnames[r.value] = r.dataset.n; });
  var steps = $$('.wstep', wiz), bar = $$('.wbar li', wiz);
  var names = {};
  $$('input[name=dienst]', wiz).forEach(function (r) { names[r.value] = r.dataset.n; });

  /* preselect via ?dienst= */
  try {
    var q = new URLSearchParams(location.search).get('dienst');
    if (q && names[q]) { st.dienst = q; $('input[name=dienst][value="' + q + '"]', wiz).checked = true; }
    var qk = new URLSearchParams(location.search).get('kleur');
    if (qk && knames[qk]) { st.kleur = qk; var rk = $('input[name=kleur][value="' + qk + '"]', wiz); rk.checked = true; setTimeout(function () { dispatchEvent(new CustomEvent('druppel:color', { detail: rk.dataset.c })); }, 1200); }
  } catch (e) {}

  /* draft (form fields only) */
  var form = $('#gegevens');
  try {
    var d = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (d) ['naam', 'tel', 'mail', 'opm'].forEach(function (k) { if (d[k] && form.elements[k]) form.elements[k].value = d[k]; });
  } catch (e) {}
  form.addEventListener('input', function () {
    try {
      localStorage.setItem(KEY, JSON.stringify({ naam: form.elements.naam.value, tel: form.elements.tel.value, mail: form.elements.mail.value, opm: form.elements.opm.value }));
    } catch (e) {}
  });

  function scrollTop() {
    var y = wiz.getBoundingClientRect().top + scrollY - (innerWidth < 980 ? 150 : 90);
    if (Math.abs(wiz.getBoundingClientRect().top) < 120) return;
    if (window.__lenis) window.__lenis.scrollTo(y, { duration: .9 }); else scrollTo({ top: y, behavior: 'smooth' });
  }
  function go(n, init) {
    st.step = n;
    steps.forEach(function (s, i) { var on = i + 1 === n; s.hidden = !on; s.classList.toggle('enter', on); });
    bar.forEach(function (li, i) {
      li.classList.toggle('done', i + 1 < n); li.classList.toggle('cur', i + 1 === n);
      var b = $('button', li); b.disabled = !(i + 1 < n) || n === 4; if (i + 1 === n) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current');
    });
    summary();
    if (init) return;
    var h = $('h2', steps[n - 1]); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
    scrollTop();
  }
  bar.forEach(function (li, i) { $('button', li).addEventListener('click', function () { if (i + 1 < st.step && st.step !== 4) go(i + 1); }); });

  /* ---------- step 1 ---------- */
  $$('input[name=dienst]', wiz).forEach(function (r) { r.addEventListener('change', function () { st.dienst = r.value; $('#e1').textContent = ''; summary(); }); });
  $$('input[name=kleur]', wiz).forEach(function (r) { r.addEventListener('change', function () { st.kleur = r.value; dispatchEvent(new CustomEvent('druppel:color', { detail: r.dataset.c })); summary(); }); });
  $$('input[name=afw]', wiz).forEach(function (r) { r.addEventListener('change', function () { st.afw = r.value; summary(); }); });
  $('#n1').addEventListener('click', function () { if (!st.dienst) { $('#e1').textContent = 'Kies eerst een behandeling.'; return; } go(2); });

  /* ---------- step 2: 14-day strip + deterministic example slots ---------- */
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var dayEls = $('#days'), slotEls = $('#slots');
  function iso(dt) { return dt.getFullYear() + '-' + pad(dt.getMonth() + 1) + '-' + pad(dt.getDate()); }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0); }
  function dateOf(isoS) { var p = isoS.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  for (var i = 0; i < 14; i++) {
    var dt = new Date(today); dt.setDate(today.getDate() + i);
    var b = document.createElement('button'); b.type = 'button'; b.className = 'day'; b.dataset.d = iso(dt);
    b.setAttribute('aria-pressed', 'false');
    b.setAttribute('aria-label', (i === 0 ? 'vandaag, ' : i === 1 ? 'morgen, ' : '') + DAYS_L[dt.getDay()] + ' ' + dt.getDate() + ' ' + MON_L[dt.getMonth()]);
    b.innerHTML = '<small>' + (i === 0 ? 'vandaag' : DAYS[dt.getDay()]) + '</small><b>' + dt.getDate() + '</b><small>' + MON[dt.getMonth()] + '</small>';
    dayEls.appendChild(b);
  }
  function slots() {
    slotEls.innerHTML = '';
    if (!st.day) { slotEls.innerHTML = '<p class="empty">Kies eerst een dag, dan zie je de tijden.</p>'; return; }
    var now = new Date(), isToday = st.day === iso(today), n = 0;
    for (var m = 9 * 60; m <= 17 * 60; m += 30) {
      var t = pad(Math.floor(m / 60)) + ':' + pad(m % 60);
      var past = isToday && (m <= now.getHours() * 60 + now.getMinutes() + 30);
      var busy = past || dateOf(st.day).getDay() === 0 || hash(st.day + 'T' + t) % 10 < 3;
      var b = document.createElement('button'); b.type = 'button'; b.className = 'slot'; b.textContent = t; b.dataset.t = t;
      b.setAttribute('aria-pressed', st.time === t ? 'true' : 'false');
      if (busy) { b.disabled = true; b.setAttribute('aria-label', t + ' — bezet'); } else n++;
      slotEls.appendChild(b);
    }
    if (!n) { var p = document.createElement('p'); p.className = 'empty'; p.textContent = 'Geen voorbeeldtijden op deze dag — kies een andere dag.'; slotEls.appendChild(p); }
  }
  dayEls.addEventListener('click', function (e) {
    var b = e.target.closest('.day'); if (!b) return;
    st.day = b.dataset.d; st.time = null;
    $$('.day', dayEls).forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
    $('#e2').textContent = ''; slots(); summary();
  });
  slotEls.addEventListener('click', function (e) {
    var b = e.target.closest('.slot'); if (!b || b.disabled) return;
    st.time = b.dataset.t;
    $$('.slot', slotEls).forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
    $('#e2').textContent = ''; summary();
  });
  slots();
  $('#b2').addEventListener('click', function () { go(1); });
  $('#n2').addEventListener('click', function () { if (!st.day || !st.time) { $('#e2').textContent = 'Kies een dag en een tijd.'; return; } go(3); });

  /* ---------- step 3: gegevens with validation ---------- */
  function fieldErr(name, msg) {
    var f = form.elements[name], wrap = f.closest('.fld'), e = $('.ferr', wrap);
    e.textContent = msg || ''; wrap.classList.toggle('bad', !!msg); f.setAttribute('aria-invalid', !!msg);
    return !msg;
  }
  function validTel(v) { var s = v.replace(/[\s\-().]/g, ''); return /^(\+31|0031|0)[1-9]\d{8}$/.test(s); }
  function validate() {
    var ok1 = fieldErr('naam', form.elements.naam.value.trim().length < 2 ? 'Vul je naam in.' : '');
    var ok2 = fieldErr('tel', validTel(form.elements.tel.value) ? '' : 'Vul een geldig telefoonnummer in.');
    return ok1 && ok2;
  }
  ['naam', 'tel'].forEach(function (k) { form.elements[k].addEventListener('blur', function () { if (form.elements[k].value) validate(); }); });
  $('#b3').addEventListener('click', function () { go(2); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!validate()) { var bad = $('.fld.bad input', form); if (bad) bad.focus(); return; }
    st.naam = form.elements.naam.value.trim();
    receipt(); go(4);
  });

  /* ---------- step 4: receipt + .ics ---------- */
  function niceDay(isoS) { var dt = dateOf(isoS); return DAYS_L[dt.getDay()] + ' ' + dt.getDate() + ' ' + MON_L[dt.getMonth()]; }
  function receipt() {
    $('#r-dienst').textContent = names[st.dienst] + (st.afw ? ' · ' + afnames[st.afw] : '');
    $('#r-kleur').textContent = st.kleur ? knames[st.kleur] : 'in overleg';
    $('#r-dag').textContent = niceDay(st.day);
    $('#r-tijd').textContent = st.time;
    $('#r-naam').textContent = st.naam;
  }
  var icsB = $('#ics'); if (icsB) icsB.addEventListener('click', function () {
    var dt = dateOf(st.day), hm = st.time.split(':');
    dt.setHours(+hm[0], +hm[1]);
    var end = new Date(dt.getTime() + 60 * 60000);
    var f = function (x) { return x.getFullYear() + pad(x.getMonth() + 1) + pad(x.getDate()) + 'T' + pad(x.getHours()) + pad(x.getMinutes()) + '00'; };
    var n = new Date(), stamp = n.getUTCFullYear() + pad(n.getUTCMonth() + 1) + pad(n.getUTCDate()) + 'T' + pad(n.getUTCHours()) + pad(n.getUTCMinutes()) + pad(n.getUTCSeconds()) + 'Z';
    var ics = [
      'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//ITty Company//Mila Nagelstudio ontwerpvoorstel//NL', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
      'BEGIN:VEVENT', 'UID:' + stamp + '-' + hash(st.day + st.time + st.naam) + '@mila-nagelstudio.demo', 'DTSTAMP:' + stamp,
      'DTSTART:' + f(dt), 'DTEND:' + f(end),
      'SUMMARY:Afspraak Mila Nagelstudio (demo)',
      'LOCATION:Waterloostraat 27\\, 4901 EM Oosterhout',
      'DESCRIPTION:' + names[st.dienst] + '. Ontwerpvoorstel: er is niets geboekt en niets verstuurd. Bel +31 6 43619068 of boek via Salonkee om echt af te spreken.',
      'END:VEVENT', 'END:VCALENDAR'
    ].join('\r\n');
    var url = URL.createObjectURL(new Blob([ics], { type: 'text/calendar;charset=utf-8' }));
    var a = document.createElement('a'); a.href = url; a.download = 'afspraak-mila-demo.ics'; a.setAttribute('download', a.download);
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  });
  $('#nieuw').addEventListener('click', function () {
    st.dienst = null; st.kleur = null; st.day = null; st.time = null;
    $$('input[name=dienst], input[name=kleur]', wiz).forEach(function (r) { r.checked = false; });
    $$('.day', dayEls).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
    slots(); go(1);
  });

  /* ---------- summary «Jouw afspraak» ---------- */
  function summary() {
    var a = $('#aside');
    $('#s-dienst').textContent = st.dienst ? names[st.dienst] : '';
    $('#s-kleur').textContent = st.kleur ? knames[st.kleur] : '';
    $('#s-afw').textContent = afnames[st.afw] || '';
    $('#s-dag').textContent = st.day ? niceDay(st.day) : '';
    $('#s-tijd').textContent = st.time || '';
    var any = st.dienst || st.kleur || st.day || st.time;
    $('.empty', a).hidden = !!any; $('dl', a).hidden = !any;
  }
  go(1, true);
})();
