/* Lumbre Hotel & Spa — lógica de la página.
   Sin dependencias ni llamadas externas. Todo texto dinámico se escribe con textContent (nunca innerHTML). */
(() => {
  'use strict';

  const I18N = window.LUMBRE_I18N || { es: {} };
  const doc = document.documentElement;
  doc.classList.add('js');

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- Datos del hotel ---------- */
  const LANGS = ['es', 'en', 'pt', 'fr'];
  const RATES = { EUR: 1, USD: 1.08, MXN: 19.8, GBP: 0.85, BRL: 6.2, COP: 4550 }; // aproximados, base EUR
  const ROOMS = { standard: { rate: 120, cap: 2 }, deluxe: { rate: 190, cap: 3 }, penthouse: { rate: 340, cap: 6 } };
  const EXTRAS = { breakfast: 18, spa: 45, transfer: 60, parking: 15, late: 30 };
  const PROMO_CODES = ['LUMBRE10'];
  const WEEKEND_RATE = 0.15, LONG_STAY = 0.10, PROMO = 0.10, TAX = 0.10;
  const MAX_NIGHTS = 30, MAX_MONTHS_AHEAD = 18;

  const EURO_ZONE = ['ES', 'FR', 'PT', 'DE', 'IT', 'NL', 'BE', 'IE', 'AT', 'GR', 'FI', 'LU'];
  const REGION_CUR = { MX: 'MXN', US: 'USD', GB: 'GBP', BR: 'BRL', CO: 'COP' };
  const REGION_LANG = { ES: 'es', MX: 'es', CO: 'es', AR: 'es', CL: 'es', PE: 'es', US: 'en', GB: 'en', CA: 'en', IE: 'en', AU: 'en', BR: 'pt', PT: 'pt', FR: 'fr', BE: 'fr' };
  const TZ_REGION = {
    'Europe/Madrid': 'ES', 'Atlantic/Canary': 'ES', 'Europe/Paris': 'FR', 'Europe/Lisbon': 'PT', 'Europe/London': 'GB', 'Europe/Dublin': 'IE',
    'Europe/Berlin': 'DE', 'Europe/Rome': 'IT', 'Europe/Amsterdam': 'NL', 'Europe/Brussels': 'BE', 'Europe/Vienna': 'AT', 'Europe/Athens': 'GR',
    'America/Mexico_City': 'MX', 'America/Monterrey': 'MX', 'America/Tijuana': 'MX', 'America/Cancun': 'MX', 'America/Merida': 'MX', 'America/Chihuahua': 'MX',
    'America/Hermosillo': 'MX', 'America/Mazatlan': 'MX', 'America/Bogota': 'CO', 'America/Sao_Paulo': 'BR', 'America/Bahia': 'BR', 'America/Fortaleza': 'BR',
    'America/Manaus': 'BR', 'America/Recife': 'BR', 'America/Argentina/Buenos_Aires': 'AR', 'America/Santiago': 'CL', 'America/Lima': 'PE',
    'America/New_York': 'US', 'America/Chicago': 'US', 'America/Denver': 'US', 'America/Los_Angeles': 'US', 'America/Phoenix': 'US', 'America/Anchorage': 'US',
    'Pacific/Honolulu': 'US', 'America/Toronto': 'CA', 'America/Vancouver': 'CA', 'Australia/Sydney': 'AU', 'Australia/Melbourne': 'AU'
  };

  const state = { lang: 'es', cur: 'EUR', region: null, consent: null, firstVisit: true, step: 1, promo: false, lastTotal: 0, lumi: { key: 'lumi.s1', vars: null }, quote: null };
  const loadedAt = performance.now();

  /* ---------- Cookies ---------- */
  const Cookies = {
    get(name) {
      const row = document.cookie.split('; ').find(r => r.startsWith(name + '='));
      if (!row) return null;
      try { return decodeURIComponent(row.slice(name.length + 1)); } catch { return null; }
    },
    set(name, value, days) {
      let c = `${name}=${encodeURIComponent(value)}; Max-Age=${Math.round(days * 86400)}; Path=/; SameSite=Lax`;
      if (location.protocol === 'https:') c += '; Secure';
      document.cookie = c;
    },
    del(name) { document.cookie = `${name}=; Max-Age=0; Path=/; SameSite=Lax`; }
  };
  const CK_CONSENT = 'lumbre_consent', CK_PREFS = 'lumbre_prefs';

  /* ---------- Región, idioma y moneda ---------- */
  function detect() {
    let region = null;
    try { region = TZ_REGION[Intl.DateTimeFormat().resolvedOptions().timeZone] || null; } catch { /* sin zona horaria */ }
    const navLangs = (navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || 'es']).map(String);
    if (!region) {
      for (const l of navLangs) {
        const m = /^[a-z]{2,3}-([A-Z]{2})$/i.exec(l);
        if (m) { region = m[1].toUpperCase(); break; }
      }
    }
    const browserLang = navLangs.map(l => l.slice(0, 2).toLowerCase()).find(l => LANGS.includes(l));
    const lang = browserLang || REGION_LANG[region] || 'en';
    const cur = REGION_CUR[region] || (EURO_ZONE.includes(region) ? 'EUR' : (region ? 'USD' : 'EUR'));
    return { region, lang, cur };
  }

  function loadPrefs() {
    const c = Cookies.get(CK_CONSENT);
    state.consent = (c === 'all' || c === 'necessary') ? c : null;
    const det = detect();
    let saved = null;
    if (state.consent === 'all') {
      try { saved = JSON.parse(Cookies.get(CK_PREFS) || 'null'); } catch { saved = null; }
    }
    // Nunca confiamos en el contenido de la cookie: solo valores de la lista blanca.
    const okSaved = saved && typeof saved === 'object';
    state.region = det.region;
    state.lang = okSaved && LANGS.includes(saved.lang) ? saved.lang : det.lang;
    state.cur = okSaved && Object.prototype.hasOwnProperty.call(RATES, saved.cur) ? saved.cur : det.cur;
    state.firstVisit = !okSaved;
  }

  function savePrefs() {
    if (state.consent === 'all') Cookies.set(CK_PREFS, JSON.stringify({ lang: state.lang, cur: state.cur, region: state.region }), 180);
    else Cookies.del(CK_PREFS);
  }

  /* ---------- i18n y formato ---------- */
  function t(key, vars) {
    const dict = I18N[state.lang] || {};
    let s = Object.prototype.hasOwnProperty.call(dict, key) ? dict[key] : (I18N.es[key] ?? key);
    if (vars) s = s.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? String(vars[k]) : m));
    return s;
  }
  function locale() {
    const tag = state.region ? `${state.lang}-${state.region}` : state.lang;
    try { return Intl.NumberFormat.supportedLocalesOf(tag)[0] || state.lang; } catch { return state.lang; }
  }
  function money(eur) {
    const v = Math.round(eur * RATES[state.cur]);
    try { return new Intl.NumberFormat(locale(), { style: 'currency', currency: state.cur, maximumFractionDigits: 0 }).format(v); }
    catch { return `${v} ${state.cur}`; }
  }
  function nightsLabel(n) { return t(n === 1 ? 'night.one' : 'night.other', { n }); }
  function regionName() {
    if (!state.region) return null;
    try { return new Intl.DisplayNames([state.lang], { type: 'region' }).of(state.region); } catch { return state.region; }
  }
  function langName() {
    try { return new Intl.DisplayNames([state.lang], { type: 'language' }).of(state.lang); } catch { return state.lang; }
  }

  function splitWords(el, text) {
    el.textContent = '';
    el.setAttribute('aria-label', text);
    text.split(' ').forEach((word, i, arr) => {
      const s = document.createElement('span');
      s.className = 'w';
      s.setAttribute('aria-hidden', 'true');
      s.style.setProperty('--i', i);
      s.textContent = word;
      el.append(s, i < arr.length - 1 ? ' ' : '');
    });
  }

  function applyI18n() {
    doc.lang = state.lang;
    document.title = t('meta.title');
    $$('[data-i18n]').forEach(el => {
      const text = t(el.dataset.i18n);
      if (el.hasAttribute('data-split')) splitWords(el, text); else el.textContent = text;
    });
    $$('[data-i18n-attr]').forEach(el => {
      el.dataset.i18nAttr.split(';').forEach(pair => {
        const [attr, key] = pair.split(':').map(x => x.trim());
        if (attr && key) el.setAttribute(attr, t(key));
      });
    });
    $$('[data-price]').forEach(el => { el.textContent = money(Number(el.dataset.price)); });
    $('#prefsLabel').textContent = `${state.lang.toUpperCase()} · ${state.cur}`;
    $('#langSel').value = state.lang;
    $('#curSel').value = state.cur;
    const rn = regionName();
    $('#regionNote').textContent = rn ? t('prefs.region', { region: rn }) : t('prefs.region.unknown');
    renderLumi(false);
    renderQuote(false);
    // Los errores visibles se vuelven a evaluar para traducirlos.
    $$('.field.invalid').forEach(f => { const el = $('input, select, textarea', f); const fn = el && fieldValidators.get(el); if (fn) fn(); });
    if (!$('#quoteSuccess').hidden) renderSuccess();
  }

  /* ---------- Fechas ---------- */
  const pad = n => String(n).padStart(2, '0');
  const iso = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  function parseDate(str) {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(str || '');
    if (!m) return null;
    const d = new Date(+m[1], +m[2] - 1, +m[3]);
    return (d.getFullYear() === +m[1] && d.getMonth() === +m[2] - 1 && d.getDate() === +m[3]) ? d : null;
  }
  function today() { const n = new Date(); return new Date(n.getFullYear(), n.getMonth(), n.getDate()); }
  function addDays(d, n) { const x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function maxDate() { const d = today(); d.setMonth(d.getMonth() + MAX_MONTHS_AHEAD); return d; }
  const nightsBetween = (a, b) => Math.round((b - a) / 864e5);

  /* ---------- Mensajes de campo ---------- */
  const fieldValidators = new Map();
  function fieldOf(el) { return el.closest('.field'); }
  function msgOf(el) { const f = fieldOf(el); return f ? $('.field-msg', f) : null; }
  function setError(el, key, vars) {
    const f = fieldOf(el), m = msgOf(el);
    if (f) { f.classList.remove('valid'); f.classList.remove('invalid'); void f.offsetWidth; f.classList.add('invalid'); }
    el.setAttribute('aria-invalid', 'true');
    if (m) { m.className = 'field-msg'; m.textContent = t(key, vars); }
    return false;
  }
  function setOk(el, mark = true) {
    const f = fieldOf(el), m = msgOf(el);
    if (f) { f.classList.remove('invalid'); f.classList.toggle('valid', mark && el.value.trim() !== ''); }
    el.removeAttribute('aria-invalid');
    if (m) { m.className = 'field-msg'; m.textContent = ''; }
    return true;
  }
  function clearField(el) {
    const f = fieldOf(el), m = msgOf(el);
    if (f) f.classList.remove('invalid', 'valid');
    el.removeAttribute('aria-invalid');
    if (m) { m.className = 'field-msg'; m.textContent = ''; }
  }
  function bind(el, fn) {
    fieldValidators.set(el, fn);
    el.addEventListener('blur', () => { if (el.value !== '' || fieldOf(el).classList.contains('invalid')) fn(); });
    el.addEventListener('input', () => { if (fieldOf(el).classList.contains('invalid')) fn(); });
    el.addEventListener('change', () => fn());
  }

  /* ---------- Validadores ---------- */
  const EMAIL_RE = /^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$/i;
  const NAME_RE = /^[\p{L}][\p{L}\p{M}'’ .-]{1,79}$/u;
  const EMAIL_TYPOS = {
    'gmial.com': 'gmail.com', 'gmai.com': 'gmail.com', 'gnail.com': 'gmail.com', 'gmail.con': 'gmail.com', 'gmail.co': 'gmail.com', 'gmal.com': 'gmail.com',
    'hotmial.com': 'hotmail.com', 'hotmal.com': 'hotmail.com', 'hotmail.con': 'hotmail.com', 'hotmail.co': 'hotmail.com',
    'outlok.com': 'outlook.com', 'outlook.con': 'outlook.com', 'yaho.com': 'yahoo.com', 'yahoo.con': 'yahoo.com', 'icloud.con': 'icloud.com'
  };

  function vName(el) {
    const v = el.value.trim().replace(/\s+/g, ' ');
    if (!v) return setError(el, 'v.required');
    if (!NAME_RE.test(v)) return setError(el, 'v.name');
    return setOk(el);
  }
  function vEmail(el) {
    const v = el.value.trim();
    if (!v) return setError(el, 'v.required');
    const [local, domain] = [v.slice(0, v.lastIndexOf('@')), v.slice(v.lastIndexOf('@') + 1).toLowerCase()];
    const tld = domain.slice(domain.lastIndexOf('.') + 1);
    if (v.length > 254 || local.length > 64 || !EMAIL_RE.test(v) || v.includes('..') || local.startsWith('.') || local.endsWith('.') || !/^[a-z]{2,}$/i.test(tld)) {
      return setError(el, 'v.email');
    }
    setOk(el);
    const fix = EMAIL_TYPOS[domain];
    if (fix) { // aviso no bloqueante con corrección en un clic
      const m = msgOf(el), suggestion = `${local}@${fix}`;
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'linklike'; b.textContent = t('v.emailTypo', { s: suggestion });
      b.addEventListener('click', () => { el.value = suggestion; vEmail(el); el.focus(); });
      m.className = 'field-msg is-hint'; m.textContent = ''; m.append(b);
    }
    return true;
  }
  function vPhone(el) {
    const raw = el.value.trim();
    if (!raw) { clearField(el); return true; }
    if (!/^[+\d][\d\s().-]*$/.test(raw)) return setError(el, 'v.phone');
    const digits = raw.replace(/\D/g, '');
    if (digits.length < 7 || digits.length > 15) return setError(el, 'v.phone');
    return setOk(el);
  }
  function vMessage(el) {
    const v = el.value.trim();
    if (!v) return setError(el, 'v.required');
    if (v.length < 10) return setError(el, 'v.msgMin');
    return setOk(el);
  }
  function vInt(el, min, max, key) {
    const n = Number(el.value);
    if (el.value.trim() === '' || !Number.isInteger(n) || n < min || n > max) return setError(el, key);
    return setOk(el, false);
  }
  function vDates(ci, co, only) {
    const a = parseDate(ci.value), b = parseDate(co.value);
    let ok = true;
    if (only !== 'out') {
      if (!ci.value) ok = setError(ci, 'v.required');
      else if (!a) ok = setError(ci, 'v.dateInvalid');
      else if (a < today()) ok = setError(ci, 'v.checkinPast');
      else if (a > maxDate()) ok = setError(ci, 'v.tooFar');
      else setOk(ci, false);
    }
    if (only !== 'in') {
      if (!co.value) ok = setError(co, 'v.required');
      else if (!b) ok = setError(co, 'v.dateInvalid');
      else if (a && b <= a) ok = setError(co, 'v.checkoutBefore');
      else if (a && nightsBetween(a, b) > MAX_NIGHTS) ok = setError(co, 'v.maxStay');
      else setOk(co, false);
    }
    return ok;
  }
  // Fechas enlazadas: límites nativos (min/max) + corrección automática de la salida.
  function linkDates(ci, co, onChange) {
    ci.min = iso(today()); ci.max = iso(maxDate());
    const sync = () => {
      const a = parseDate(ci.value);
      const base = a && a >= today() ? a : today();
      co.min = iso(addDays(base, 1)); co.max = iso(addDays(base, MAX_NIGHTS));
      const b = parseDate(co.value);
      if (a && a >= today() && (!b || b <= a)) co.value = iso(addDays(a, 1));
    };
    ci.addEventListener('change', () => { sync(); vDates(ci, co); onChange && onChange(); });
    co.addEventListener('change', () => { vDates(ci, co); onChange && onChange(); });
    ci.addEventListener('blur', () => { if (ci.value) vDates(ci, co, 'in'); });
    co.addEventListener('blur', () => { if (co.value) vDates(ci, co, 'out'); });
    fieldValidators.set(ci, () => vDates(ci, co, 'in'));
    fieldValidators.set(co, () => vDates(ci, co, 'out'));
    sync();
  }

  /* ---------- Anti-spam ---------- */
  function looksAutomated(form) {
    const hp = $('.hp input', form);
    return !!(hp && hp.value !== '');
  }
  function tooFast() { return performance.now() - loadedAt < 2500; }
  function inCooldown(key) {
    try {
      const last = Number(sessionStorage.getItem(key) || 0);
      return Date.now() - last < 20000;
    } catch { return false; }
  }
  function markSent(key) { try { sessionStorage.setItem(key, String(Date.now())); } catch { /* almacenamiento bloqueado */ } }

  /* ---------- Mascota ---------- */
  const lumiEl = $('#lumi'), bubbleEl = $('#lumiBubble'), mouthEl = $('#lumiMouth');
  const MOUTH = { happy: 'M50 70q10 8 20 0', sad: 'M50 75q10 -7 20 0', wow: 'M54 70q6 9 12 0q-6 -5 -12 0' };
  function renderLumi(animate = true) {
    const v = state.lumi.vars;
    bubbleEl.textContent = t(state.lumi.key, v && v.roomKey ? { room: t(v.roomKey) } : v);
    if (animate && !reduceMotion) { bubbleEl.classList.remove('pop'); void bubbleEl.offsetWidth; bubbleEl.classList.add('pop'); }
  }
  function lumi(key, mood = 'hop', vars = null) {
    state.lumi = { key, vars };
    mouthEl.setAttribute('d', mood === 'sad' ? MOUTH.sad : mood === 'party' ? MOUTH.wow : MOUTH.happy);
    lumiEl.classList.remove('hop', 'sad', 'party'); void lumiEl.getBoundingClientRect(); lumiEl.classList.add(mood);
    renderLumi();
  }

  /* ---------- Presupuesto ---------- */
  const qf = $('#quoteForm');
  const q = {
    ci: $('#q-checkin'), co: $('#q-checkout'), adults: $('#q-adults'), children: $('#q-children'), promo: $('#q-promo'),
    name: $('#q-name'), email: $('#q-email'), phone: $('#q-phone'), notes: $('#q-notes'), consent: $('#q-consent')
  };
  const roomValue = () => (qf.elements.room.value in ROOMS ? qf.elements.room.value : 'deluxe');
  const extrasChosen = () => $$('input[name="extras"]:checked', qf).map(i => i.value).filter(v => v in EXTRAS);

  function computeQuote() {
    const a = parseDate(q.ci.value), b = parseDate(q.co.value);
    const adults = Number(q.adults.value), children = Number(q.children.value);
    if (!a || !b || b <= a || a < today() || a > maxDate()) return null;
    const nights = nightsBetween(a, b);
    if (nights > MAX_NIGHTS) return null;
    if (!Number.isInteger(adults) || adults < 1 || adults > 6 || !Number.isInteger(children) || children < 0 || children > 4) return null;

    const room = roomValue(), rate = ROOMS[room].rate;
    let base = 0, weekend = 0;
    for (let i = 0; i < nights; i++) {
      const day = addDays(a, i).getDay();
      base += rate;
      if (day === 5 || day === 6) weekend += rate * WEEKEND_RATE;
    }
    const lines = [{ label: `${t('room.' + room)} × ${nightsLabel(nights)}`, amount: base }];
    if (weekend) lines.push({ label: t('sum.weekend'), amount: weekend });
    let extras = 0;
    for (const x of extrasChosen()) {
      let amount = EXTRAS[x];
      if (x === 'breakfast') amount *= nights * (adults + children * 0.5);
      else if (x === 'spa') amount *= adults;
      else if (x === 'parking') amount *= nights;
      extras += amount;
      lines.push({ label: t('x.' + x), amount });
    }
    const stay = base + weekend;
    const longStay = nights >= 7 ? -stay * LONG_STAY : 0;
    if (longStay) lines.push({ label: t('sum.longstay'), amount: longStay, neg: true });
    const promo = state.promo ? -(stay + extras + longStay) * PROMO : 0;
    if (promo) lines.push({ label: t('sum.promo'), amount: promo, neg: true });
    const net = stay + extras + longStay + promo;
    const tax = net * TAX;
    lines.push({ label: t('sum.tax'), amount: tax });
    return { nights, room, adults, children, lines, total: net + tax, longStay: !!longStay };
  }

  const sumList = $('#sumList'), sumTotal = $('#sumTotal'), sumPerNight = $('#sumPerNight');
  let tweenId = 0;
  function tweenTotal(from, to) {
    cancelAnimationFrame(tweenId);
    if (reduceMotion || from === to) { sumTotal.textContent = money(to); return; }
    const t0 = performance.now(), dur = 550;
    const frame = now => {
      const p = clamp((now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      sumTotal.textContent = money(from + (to - from) * e);
      if (p < 1) tweenId = requestAnimationFrame(frame);
    };
    tweenId = requestAnimationFrame(frame);
  }
  function renderQuote(animate = true) {
    const quote = computeQuote();
    state.quote = quote;
    sumList.textContent = '';
    if (!quote) {
      const li = document.createElement('li'); li.className = 'empty'; li.textContent = t('sum.empty'); sumList.append(li);
      cancelAnimationFrame(tweenId); sumTotal.textContent = '—'; sumPerNight.textContent = ''; state.lastTotal = 0;
      return;
    }
    quote.lines.forEach((line, i) => {
      const li = document.createElement('li'), l = document.createElement('span'), v = document.createElement('span');
      if (line.neg) li.className = 'neg';
      li.style.animationDelay = `${i * 40}ms`;
      l.textContent = line.label; v.textContent = (line.neg ? '−' : '') + money(Math.abs(line.amount));
      li.append(l, v); sumList.append(li);
    });
    sumPerNight.textContent = t('sum.perNight', { price: money(quote.total / quote.nights) });
    if (animate && quote.total !== state.lastTotal) {
      tweenTotal(state.lastTotal, quote.total);
      sumTotal.classList.remove('bump'); void sumTotal.offsetWidth; sumTotal.classList.add('bump');
    } else { cancelAnimationFrame(tweenId); sumTotal.textContent = money(quote.total); }
    state.lastTotal = quote.total;
  }

  function vCapacity() {
    const room = roomValue(), guests = Number(q.adults.value) + Number(q.children.value), msg = $('#roomMsg');
    if (guests > ROOMS[room].cap) { msg.className = 'field-msg group-msg'; msg.textContent = t('v.capacity', { room: t('room.' + room), n: ROOMS[room].cap }); return false; }
    msg.textContent = ''; return true;
  }
  function applyPromo(silent) {
    const code = q.promo.value.trim().toUpperCase(), m = msgOf(q.promo);
    q.promo.value = code;
    if (!code) { state.promo = false; clearField(q.promo); renderQuote(); return true; }
    if (!/^[A-Z0-9]{4,20}$/.test(code) || !PROMO_CODES.includes(code)) { state.promo = false; setError(q.promo, 'v.promoBad'); renderQuote(); return false; }
    const was = state.promo; state.promo = true; setOk(q.promo);
    m.className = 'field-msg is-ok'; m.textContent = t('v.promoOk');
    renderQuote();
    if (!was && !silent) lumi('lumi.promo', 'party');
    return true;
  }
  function vConsent() {
    if (!q.consent.checked) return setError(q.consent, 'v.consent');
    const f = fieldOf(q.consent); f.classList.remove('invalid'); msgOf(q.consent).textContent = ''; q.consent.removeAttribute('aria-invalid');
    return true;
  }

  function validateStep(n) {
    if (n === 1) {
      const r = [vDates(q.ci, q.co), vInt(q.adults, 1, 6, 'v.adults'), vInt(q.children, 0, 4, 'v.children')];
      return r.every(Boolean);
    }
    if (n === 2) {
      const promoOk = q.promo.value.trim() === '' ? true : applyPromo(true);
      return [vCapacity(), promoOk].every(Boolean);
    }
    const r = [vName(q.name), vEmail(q.email), vPhone(q.phone), vConsent()];
    return r.every(Boolean);
  }

  const stepEls = $$('.step', qf), barItems = $$('#stepsBar li');
  const prevBtn = $('#prevBtn'), nextBtn = $('#nextBtn'), submitBtn = $('#submitBtn');
  function showStep(n, focus = true) {
    const back = n < state.step;
    state.step = n;
    stepEls.forEach(s => { const on = Number(s.dataset.step) === n; s.hidden = !on; s.classList.toggle('back', on && back); });
    barItems.forEach((li, i) => { li.classList.toggle('is-on', i + 1 === n); li.classList.toggle('is-done', i + 1 < n); if (i + 1 === n) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current'); });
    prevBtn.hidden = n === 1; nextBtn.hidden = n === 3; submitBtn.hidden = n !== 3;
    lumi('lumi.s' + n, 'hop');
    if (focus) { const first = $('input:not([type="hidden"]):not([tabindex="-1"]), select, textarea', stepEls[n - 1]); if (first) first.focus({ preventScroll: true }); }
  }
  function failStep() {
    lumi('lumi.error', 'sad');
    const bad = $('.field.invalid input, .field.invalid select, .field.invalid textarea', stepEls[state.step - 1]);
    if (bad) bad.focus();
  }

  let lastRef = '', lastName = '';
  function makeRef() {
    const A = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789', buf = new Uint8Array(6);
    crypto.getRandomValues(buf);
    return 'LMB-' + Array.from(buf, b => A[b % A.length]).join('');
  }
  function renderSuccess() {
    const qt = state.quote;
    if (!qt) return;
    $('#okText').textContent = t('ok.text', { name: lastName, nights: nightsLabel(qt.nights), room: t('room.' + qt.room), total: money(qt.total) });
    $('#refCode').textContent = lastRef;
  }

  function initQuote() {
    const start = addDays(today(), 14);
    q.ci.value = iso(start); q.co.value = iso(addDays(start, 3));
    linkDates(q.ci, q.co, () => {
      renderQuote();
      if (state.quote && state.quote.longStay && state.step === 1) lumi('lumi.longstay', 'party');
    });
    bind(q.adults, () => vInt(q.adults, 1, 6, 'v.adults'));
    bind(q.children, () => vInt(q.children, 0, 4, 'v.children'));
    bind(q.name, () => vName(q.name));
    bind(q.email, () => vEmail(q.email));
    bind(q.phone, () => vPhone(q.phone));
    fieldValidators.set(q.promo, () => applyPromo(true));
    fieldValidators.set(q.consent, vConsent);
    q.consent.addEventListener('change', vConsent);

    $$('.stp', qf).forEach(btn => btn.addEventListener('click', () => {
      const input = document.getElementById(btn.dataset.for);
      const next = clamp((Number(input.value) || 0) + Number(btn.dataset.delta), Number(input.min), Number(input.max));
      input.value = String(next);
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }));
    qf.addEventListener('change', e => {
      if (e.target.name === 'room' || e.target.name === 'extras' || e.target === q.adults || e.target === q.children) {
        renderQuote();
        if (state.step === 2 || $('#roomMsg').textContent) vCapacity();
      }
    });
    $('#promoApply').addEventListener('click', () => applyPromo(false));
    q.promo.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); applyPromo(false); } });

    nextBtn.addEventListener('click', () => { if (validateStep(state.step)) showStep(state.step + 1); else failStep(); });
    prevBtn.addEventListener('click', () => showStep(state.step - 1));
    // Enter en los pasos 1 y 2 avanza en lugar de enviar.
    qf.addEventListener('keydown', e => {
      if (e.key === 'Enter' && state.step < 3 && e.target.tagName !== 'TEXTAREA' && e.target.tagName !== 'BUTTON') { e.preventDefault(); nextBtn.click(); }
    });

    qf.addEventListener('submit', e => {
      e.preventDefault();
      for (let s = 1; s <= 3; s++) {
        if (!validateStep(s)) { if (s !== state.step) showStep(s, false); validateStep(s); failStep(); return; }
      }
      const quote = computeQuote();
      if (!quote) { showStep(1); failStep(); return; }
      if (tooFast()) { setError(q.consent, 'v.tooFast'); return; }
      if (inCooldown('lumbre_q')) { setError(q.consent, 'v.cooldown'); return; }
      state.quote = quote;
      if (!looksAutomated(qf)) markSent('lumbre_q'); // a un bot se le muestra éxito sin registrar nada

      // Aquí iría el envío real (fetch a tu servidor). Los datos personales no se guardan en el navegador.
      lastRef = makeRef();
      lastName = q.name.value.trim().split(/\s+/)[0];
      renderSuccess();
      qf.hidden = true; $('#stepsBar').hidden = true;
      const ok = $('#quoteSuccess'); ok.hidden = false; ok.focus({ preventScroll: true });
      lumi('lumi.success', 'party');
      confetti();
    });

    $('#newQuote').addEventListener('click', () => {
      [q.name, q.email, q.phone, q.notes].forEach(el => { el.value = ''; clearField(el); });
      q.consent.checked = false;
      $('#quoteSuccess').hidden = true; qf.hidden = false; $('#stepsBar').hidden = false;
      showStep(1);
    });

    $$('[data-pick-room]').forEach(btn => btn.addEventListener('click', () => {
      const r = $(`input[name="room"][value="${CSS.escape(btn.dataset.pickRoom)}"]`, qf);
      if (r) { r.checked = true; renderQuote(); vCapacity(); }
      goTo('#presupuesto');
      if (qf.hidden) $('#newQuote').click();
      lumi('lumi.room', 'party', { roomKey: 'room.' + roomValue() });
    }));

    // Tarjetas de experiencias: añaden o quitan un extra del presupuesto.
    const syncChips = () => $$('[data-add-extra]').forEach(b => {
      const box = $(`input[name="extras"][value="${CSS.escape(b.dataset.addExtra)}"]`, qf);
      const on = !!(box && box.checked);
      b.classList.toggle('is-added', on); b.setAttribute('aria-pressed', String(on));
    });
    $$('[data-add-extra]').forEach(btn => btn.addEventListener('click', () => {
      const key = btn.dataset.addExtra, box = $(`input[name="extras"][value="${CSS.escape(key)}"]`, qf);
      if (!box) return;
      box.checked = !box.checked;
      renderQuote(); syncChips();
      const on = box.checked;
      toast(() => t(on ? 'exp.added' : 'exp.removed', { item: t('x.' + key) }), () => t('nav.quote'), e => { e.stopPropagation(); hideToast(); goTo('#presupuesto'); });
      if (on) lumi('lumi.s2', 'party');
    }));
    qf.addEventListener('change', e => { if (e.target.name === 'extras') syncChips(); });
    syncChips();
  }

  function goTo(sel) { const el = $(sel); if (el) el.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' }); }

  /* ---------- Formulario rápido del hero ---------- */
  function initHero() {
    const hf = $('#heroForm'), ci = $('#h-checkin'), co = $('#h-checkout'), guests = $('#h-guests');
    ci.value = q.ci.value; co.value = q.co.value;
    linkDates(ci, co);
    hf.addEventListener('submit', e => {
      e.preventDefault();
      if (!vDates(ci, co)) { const bad = $('.field.invalid input', hf); if (bad) bad.focus(); return; }
      q.ci.value = ci.value; q.ci.dispatchEvent(new Event('change', { bubbles: true }));
      q.co.value = co.value; q.co.dispatchEvent(new Event('change', { bubbles: true }));
      const g = clamp(Number(guests.value) || 2, 1, 6);
      q.adults.value = String(g); q.children.value = '0';
      // Sugiere la habitación más pequeña en la que cabe el grupo.
      const fit = Object.keys(ROOMS).find(k => ROOMS[k].cap >= g) || 'penthouse';
      if (ROOMS[roomValue()].cap < g) $(`input[name="room"][value="${fit}"]`, qf).checked = true;
      if (qf.hidden) $('#newQuote').click();
      showStep(1, false);
      renderQuote();
      goTo('#presupuesto');
    });
  }

  /* ---------- Contacto ---------- */
  function initContact() {
    const cf = $('#contactForm'), name = $('#c-name'), email = $('#c-email'), msg = $('#c-msg');
    bind(name, () => vName(name)); bind(email, () => vEmail(email)); bind(msg, () => vMessage(msg));
    // Botones "Consultar" / "Quiero ir": preparan el mensaje y llevan al formulario.
    $$('[data-ask]').forEach(btn => btn.addEventListener('click', () => {
      msg.value = t('ask.msg', { item: t(btn.dataset.ask) });
      vMessage(msg);
      goTo('#contacto');
      setTimeout(() => name.focus({ preventScroll: true }), reduceMotion ? 0 : 700);
    }));
    cf.addEventListener('submit', e => {
      e.preventDefault();
      const ok = [vName(name), vEmail(email), vMessage(msg)].every(Boolean);
      if (!ok) { const bad = $('.field.invalid input, .field.invalid textarea', cf); if (bad) bad.focus(); return; }
      if (tooFast()) { setError(msg, 'v.tooFast'); return; }
      if (inCooldown('lumbre_c')) { setError(msg, 'v.cooldown'); return; }
      if (!looksAutomated(cf)) markSent('lumbre_c');
      const first = name.value.trim().split(/\s+/)[0];
      // Aquí iría el envío real (fetch a tu servidor).
      cf.reset(); [name, email, msg].forEach(clearField);
      toast(() => t('toast.contact', { name: first }));
    });
  }

  /* ---------- Avisos ---------- */
  const toastEl = $('#toast');
  let toastTimer = 0, toastText = null, toastActionText = null;
  function toast(textFn, actionFn, onAction) {
    toastText = textFn; toastActionText = actionFn || null;
    $('#toastText').textContent = textFn();
    const act = $('#toastAction');
    act.hidden = !actionFn; act.textContent = actionFn ? actionFn() : ''; act.onclick = onAction || null;
    toastEl.classList.remove('out'); toastEl.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(hideToast, 9000);
  }
  function hideToast() {
    clearTimeout(toastTimer);
    if (toastEl.hidden) return;
    toastEl.classList.add('out');
    setTimeout(() => { toastEl.hidden = true; toastEl.classList.remove('out'); }, reduceMotion ? 0 : 300);
  }
  function retranslateToast() {
    if (toastEl.hidden || !toastText) return;
    $('#toastText').textContent = toastText();
    if (toastActionText) $('#toastAction').textContent = toastActionText();
  }

  /* ---------- Preferencias (idioma / moneda) ---------- */
  function initPrefs() {
    const btn = $('#prefsBtn'), pop = $('#prefsPop');
    const open = v => { pop.hidden = !v; btn.setAttribute('aria-expanded', String(v)); if (v) $('#langSel').focus(); };
    btn.addEventListener('click', e => { e.stopPropagation(); open(pop.hidden); });
    document.addEventListener('click', e => { if (!pop.hidden && !pop.contains(e.target)) open(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !pop.hidden) { open(false); btn.focus(); } });
    $('#langSel').addEventListener('change', e => { if (LANGS.includes(e.target.value)) { state.lang = e.target.value; savePrefs(); applyI18n(); retranslateToast(); } });
    $('#curSel').addEventListener('change', e => { if (e.target.value in RATES) { state.cur = e.target.value; savePrefs(); applyI18n(); retranslateToast(); } });
    return open;
  }

  /* ---------- Cookies (banner) ---------- */
  function initCookies() {
    const banner = $('#cookieBanner'), panel = $('#ckPanel'), prefs = $('#ckPrefs');
    const setMode = config => { panel.hidden = !config; $('#ckSave').hidden = !config; $('#ckConfig').hidden = config; };
    const decide = value => {
      state.consent = value;
      Cookies.set(CK_CONSENT, value, 180);
      savePrefs();
      banner.hidden = true;
    };
    $('#ckAccept').addEventListener('click', () => decide('all'));
    $('#ckNecessary').addEventListener('click', () => decide('necessary'));
    $('#ckConfig').addEventListener('click', () => { setMode(true); prefs.focus(); });
    $('#ckSave').addEventListener('click', () => decide(prefs.checked ? 'all' : 'necessary'));
    $('#openCookies').addEventListener('click', () => { prefs.checked = state.consent === 'all'; setMode(true); banner.hidden = false; prefs.focus(); });
    if (!state.consent) { setMode(false); banner.hidden = false; }
  }

  /* ---------- Menú móvil ---------- */
  function initMenu() {
    const btn = $('#menuBtn'), nav = $('#mainNav'), header = $('#siteHeader');
    const open = v => { nav.classList.toggle('open', v); header.classList.toggle('menu-open', v); btn.setAttribute('aria-expanded', String(v)); };
    btn.addEventListener('click', () => open(!nav.classList.contains('open')));
    nav.addEventListener('click', e => { if (e.target.closest('a')) open(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { open(false); btn.focus(); } });
    matchMedia('(min-width: 941px)').addEventListener('change', () => open(false));
  }

  /* ---------- Animaciones ---------- */
  function initReveal() {
    const els = $$('.reveal');
    els.forEach(el => { if (el.dataset.delay) el.style.transitionDelay = `${Number(el.dataset.delay) || 0}ms`; });
    if (reduceMotion || !('IntersectionObserver' in window)) { els.forEach(el => el.classList.add('in')); return; }
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (!en.isIntersecting) return;
      en.target.classList.add('in'); io.unobserve(en.target);
      // El retardo solo sirve para la entrada: después se quita para que el hover responda al instante.
      setTimeout(() => { en.target.style.transitionDelay = ''; }, 1100 + (Number(en.target.dataset.delay) || 0));
    }), { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    els.forEach(el => io.observe(el));
  }

  function initCounters() {
    const els = $$('[data-count]');
    const fmt = (v, dec) => v.toLocaleString(locale(), { minimumFractionDigits: dec, maximumFractionDigits: dec });
    const run = el => {
      const to = Number(el.dataset.count), dec = Number(el.dataset.decimals || 0);
      if (reduceMotion) { el.textContent = fmt(to, dec); return; }
      const t0 = performance.now(), dur = 1400;
      const frame = now => { const p = clamp((now - t0) / dur), e = 1 - Math.pow(1 - p, 4); el.textContent = fmt(to * e, dec); if (p < 1) requestAnimationFrame(frame); };
      requestAnimationFrame(frame);
    };
    if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
    const io = new IntersectionObserver(entries => entries.forEach(en => { if (en.isIntersecting) { run(en.target); io.unobserve(en.target); } }), { threshold: 0.6 });
    els.forEach(el => io.observe(el));
  }

  function initTilt() {
    if (reduceMotion || !finePointer) return;
    $$('.tilt').forEach(card => {
      card.addEventListener('pointermove', e => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.setProperty('--ry', `${(x * 7).toFixed(2)}deg`);
        card.style.setProperty('--rx', `${(-y * 7).toFixed(2)}deg`);
      });
      card.addEventListener('pointerleave', () => { card.style.setProperty('--ry', '0deg'); card.style.setProperty('--rx', '0deg'); });
    });
  }

  function initMarquee() {
    const track = $('.marquee-track');
    if (!track || reduceMotion) return;
    $$('.quote-card', track).forEach(card => { const c = card.cloneNode(true); c.setAttribute('aria-hidden', 'true'); track.append(c); });
  }

  function initScroll() {
    const bar = $('#progressBar'), header = $('#siteHeader'), hero = $('.hero'), sc = $('#showcase'), frame = $('.showcase-frame');
    const caps = $$('.sc-cap');
    let ticking = false, stage = -1;
    const update = () => {
      ticking = false;
      const y = window.scrollY, vh = window.innerHeight, max = doc.scrollHeight - vh;
      bar.style.transform = `scaleX(${max > 0 ? clamp(y / max) : 0})`;
      header.classList.toggle('scrolled', y > 24);
      if (!reduceMotion && y < vh * 1.3) hero.style.setProperty('--sy', y.toFixed(1));

      const r = sc.getBoundingClientRect(), total = r.height - vh;
      if (r.top < vh && r.bottom > 0) {
        const enter = clamp(1 - r.top / vh), leave = clamp(r.bottom / vh), edge = Math.min(enter, leave);
        const p = clamp(-r.top / total);
        frame.style.setProperty('--scale', reduceMotion ? '1' : (0.84 + 0.16 * edge).toFixed(4));
        frame.style.setProperty('--rad', reduceMotion ? '0px' : `${(32 * (1 - edge)).toFixed(1)}px`);
        frame.style.setProperty('--dusk', clamp((p - 0.22) / 0.2).toFixed(3));
        frame.style.setProperty('--night', clamp((p - 0.58) / 0.2).toFixed(3));
        frame.style.setProperty('--p', reduceMotion ? '0' : p.toFixed(3));
        const s = p < 0.36 ? 0 : p < 0.7 ? 1 : 2;
        if (s !== stage) { stage = s; caps.forEach(c => c.classList.toggle('is-on', Number(c.dataset.stage) === s)); }
      }
    };
    const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    update();
  }

  function confetti() {
    if (reduceMotion) return;
    const c = $('#confetti'), ctx = c.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2);
    const W = window.innerWidth, H = window.innerHeight;
    c.width = W * dpr; c.height = H * dpr; ctx.scale(dpr, dpr); c.hidden = false;
    const colors = ['#0F5F66', '#E9B95C', '#F3EBDD', '#D9603B', '#7FC8C4'];
    const parts = Array.from({ length: 150 }, () => ({
      x: W / 2 + (Math.random() - 0.5) * 220, y: H * 0.6, vx: (Math.random() - 0.5) * 16, vy: -Math.random() * 17 - 6,
      s: Math.random() * 8 + 5, r: Math.random() * 6.28, vr: (Math.random() - 0.5) * 0.4, c: colors[(Math.random() * colors.length) | 0], round: Math.random() < 0.3
    }));
    const t0 = performance.now();
    const frame = now => {
      const el = now - t0;
      ctx.clearRect(0, 0, W, H);
      for (const p of parts) {
        p.vy += 0.42; p.vx *= 0.99; p.x += p.vx; p.y += p.vy; p.r += p.vr;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.globalAlpha = clamp(1 - (el - 1900) / 900); ctx.fillStyle = p.c;
        if (p.round) { ctx.beginPath(); ctx.arc(0, 0, p.s / 2.4, 0, 6.29); ctx.fill(); } else ctx.fillRect(-p.s / 2, -p.s / 3, p.s, p.s * 0.66);
        ctx.restore();
      }
      if (el < 2800) requestAnimationFrame(frame); else { ctx.clearRect(0, 0, W, H); c.hidden = true; }
    };
    requestAnimationFrame(frame);
  }

  /* ---------- Arranque ---------- */
  loadPrefs();
  initMarquee();
  initQuote();
  initHero();
  initContact();
  const openPrefs = initPrefs();
  initCookies();
  initMenu();
  applyI18n();
  initReveal();
  initCounters();
  initTilt();
  initScroll();

  if (state.firstVisit && state.region) {
    setTimeout(() => toast(
      () => t('toast.geo', { region: regionName(), lang: langName(), cur: state.cur }),
      () => t('toast.change'),
      e => { e.stopPropagation(); hideToast(); openPrefs(true); }
    ), 1800);
  }
})();
