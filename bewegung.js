gsap.registerPlugin(ScrollTrigger);
function bezier(x1, y1, x2, y2) {
const A = (a, b) => 1 - 3 * b + 3 * a;
const B = (a, b) => 3 * b - 6 * a;
const C = (a) => 3 * a;
const calc = (t, a, b) => ((A(a, b) * t + B(a, b)) * t + C(a)) * t;
const slope = (t, a, b) => 3 * A(a, b) * t * t + 2 * B(a, b) * t + C(a);
return (x) => {
if (x <= 0) return 0;
if (x >= 1) return 1;
let t = x;
for (let i = 0; i < 6; i++) {
const s = slope(t, x1, x2);
if (s === 0) break;
t -= (calc(t, x1, x2) - x) / s;
}
return calc(t, y1, y2);
};
}
const KURVE = bezier(0.44, 0, 0.56, 1);             // Interaktion
const KURVE_REIN = bezier(0.23, 0.52, 0.42, 0.97);  // Einblendung
const T_FARBE = 0.4, T_FLAECHE = 0.3, T_BILD = 0.6;
const T_REIN = 0.74, WEG_REIN = 20, SKALA_REIN = 0.9;
const lenis = new Lenis({ lerp: 0.1, wheelMultiplier: 1, syncTouch: false });
window.__lenis = lenis;
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);
lenis.on('scroll', ScrollTrigger.update);
document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach((a) => {
a.addEventListener('click', (e) => {
const ziel = document.querySelector(a.getAttribute('href'));
if (!ziel) return;
e.preventDefault();
lenis.scrollTo(ziel, { offset: -110 });
});
});
function zeileHalten(el, dauerMs) {
const ziel = el.getBoundingClientRect().top;
const ende = performance.now() + dauerMs;
const halten = (jetzt) => {
const versatz = el.getBoundingClientRect().top - ziel;
if (Math.abs(versatz) > 0.5) {
lenis.scrollTo(lenis.animatedScroll + versatz, { immediate: true });
}
if (jetzt < ende) requestAnimationFrame(halten);
};
requestAnimationFrame(halten);
}
(function knopfPunkte() {
document.querySelectorAll('.knopf').forEach((k) => {
if (k.querySelector('.knopf__punkt')) return;
if ([...k.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) {
const t = document.createElement('span');
while (k.firstChild) t.appendChild(k.firstChild);
k.appendChild(t);
}
for (let i = 0; i < 3; i++) {
const s = document.createElement('span');
s.className = 'knopf__punkt';
s.setAttribute('aria-hidden', 'true');
k.insertBefore(s, k.firstChild);
}
});
})();
(function reveals() {
const UNSCHAERFE = 12;
const rein = (ziele, ausloeser, verzug = 0) => {
gsap.fromTo(ziele,
{ y: WEG_REIN, scale: SKALA_REIN, opacity: 0, filter: 'blur(' + UNSCHAERFE + 'px)' },
{
y: 0, scale: 1, opacity: 1, filter: 'blur(0px)',
duration: T_REIN, ease: KURVE_REIN, delay: verzug,
clearProps: 'transform,opacity,filter',
scrollTrigger: { trigger: ausloeser, start: 'top 92%' },
});
};
document.querySelectorAll('[data-rein]').forEach((el) => rein(el, el));
document.querySelectorAll('[data-rein-zeilen]').forEach((block) => {
const zeilen = [...block.children];
zeilen.forEach((z) => (z.style.display = 'block'));
rein(zeilen, block);            // ein Auslöser, keine Staffel
});
})();
(function handschrift() {
if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
const einwickeln = (el) => {
const da = el.querySelector('.brush__t');
if (da) return da;
const t = document.createElement('span');
t.className = 'brush__t';
while (el.firstChild) t.appendChild(el.firstChild);
el.appendChild(t);
return t;
};
const schreiben = (el, verzug = 0) => {
const mittig = getComputedStyle(el).textAlign === 'center';
gsap.fromTo(einwickeln(el),
{ clipPath: mittig ? 'inset(0% 50% 0% 50%)' : 'inset(0% 100% 0% 0%)' },
{ clipPath: 'inset(0% 0% 0% 0%)', duration: 0.85, ease: KURVE_REIN,
delay: verzug, clearProps: 'clipPath',
scrollTrigger: { trigger: el, start: 'top 90%' } });
};
const leben = (el, i) => {
const t = einwickeln(el);
gsap.fromTo(t, { y: -2.5 },
{ y: 2.5, duration: 3.4 + (i % 3) * 0.9, ease: 'sine.inOut',
repeat: -1, yoyo: true, delay: i * 0.4 });
gsap.fromTo(t, { x: -1.6 },
{ x: 1.6, duration: 4.7 + (i % 4) * 0.8, ease: 'sine.inOut',
repeat: -1, yoyo: true, delay: i * 0.55 });
};
const driften = (el, von, bis, wo) => {
gsap.fromTo(el, { y: von },
{ y: bis, ease: 'none',
scrollTrigger: wo || { trigger: el, start: 'top bottom', end: 'bottom top', scrub: 0.6 } });
};
[...document.querySelectorAll('p.brush')]
.filter((el) => !el.closest('.nav'))
.forEach((el, i) => {
schreiben(el);
leben(el, i);
const w = i % 2 ? 11 : 17;
driften(el, w, -w);
});
const heroWort = document.querySelector('h1 .brush');
if (heroWort) {
schreiben(heroWort, 0.4);
leben(heroWort, 2);
driften(heroWort, 0, -18,
{ trigger: '.buehne', start: 'top top', end: 'bottom top', scrub: 0.6 });
}
})();
(function dropdown() {
const wurzel = document.querySelector('.ndd');
if (!wurzel) return;
const ausloeser = wurzel.querySelector('.ndd__ausloeser');
const panel = document.querySelector('.ndd__panel');
const zeilen = [...document.querySelectorAll('.ndd__liste a')];
const bilder = [...document.querySelectorAll('.ndd__bild img')];
const saetze = [...document.querySelectorAll('.ndd__satz')];
const fuss = document.querySelector('.ndd__fuss');
const leiste = document.querySelector('.nav');
if (!panel || !leiste) return;
let aufTimer = null, zuTimer = null, offen = false;
const aufAb = () => { if (aufTimer) { clearTimeout(aufTimer); aufTimer = null; } };
const zuAb = () => { if (zuTimer) { clearTimeout(zuTimer); zuTimer = null; } };
const ursprungSetzen = () => {
const bezug = document.querySelector('.nav__pille');
const a = ausloeser.getBoundingClientRect();
const p = bezug.getBoundingClientRect();
panel.style.setProperty('--ndd-x', Math.round(a.left - p.left + a.width / 2) + 'px');
const breite = Math.min(1120, p.width);
const links = Math.max(p.left, p.right - breite);
panel.style.setProperty('--ndd-links', Math.round(links) + 'px');
panel.style.setProperty('--ndd-breite', Math.round(p.right - links) + 'px');
};
const setze = (auf) => {
if (auf === offen) return;
offen = auf;
if (auf) ursprungSetzen();
wurzel.classList.toggle('ist', auf);
leiste.classList.toggle('auf', auf);
panel.setAttribute('aria-hidden', String(!auf));
ausloeser.setAttribute('aria-expanded', String(auf));
[...zeilen, fuss].forEach((el) => el && el.setAttribute('tabindex', auf ? '0' : '-1'));
};
ausloeser.addEventListener('pointerenter', () => {
zuAb();
if (offen) return;
aufAb();
aufTimer = setTimeout(() => setze(true), 70);    // Verweilzeit
});
ausloeser.addEventListener('pointerleave', () => { aufAb(); baldZu(); });
function baldZu() { zuAb(); zuTimer = setTimeout(() => setze(false), 180); }
panel.addEventListener('pointerenter', () => { if (offen) zuAb(); });
panel.addEventListener('pointerleave', () => { if (offen) baldZu(); });
ausloeser.addEventListener('focus', () => { zuAb(); setze(true); });
leiste.addEventListener('focusout', (e) => {
if (!leiste.contains(e.relatedTarget)) setze(false);
});
addEventListener('keydown', (e) => { if (e.key === 'Escape' && offen) setze(false); });
addEventListener('resize', () => { if (offen) ursprungSetzen(); });
const zeige = (i) => {
bilder.forEach((b, k) => b.classList.toggle('ist', k === i));
saetze.forEach((s, k) => s.classList.toggle('ist', k === i));
};
zeilen.forEach((z, i) => {
z.addEventListener('pointerenter', () => zeige(i));
z.addEventListener('focus', () => zeige(i));
});
[...zeilen, fuss].forEach((el) => el && el.addEventListener('click', () => setze(false)));
setze(false);
})();
(function leistungen() {
const zeilen = [...document.querySelectorAll('#lzliste .lz')];
if (!zeilen.length) return;
const zu = (lz) => {
const h = lz.querySelector('.lz__huelle');
h.style.height = h.scrollHeight + 'px';
requestAnimationFrame(() => { h.style.height = '0px'; });
lz.classList.remove('ist');
lz.querySelector('.lz__kopf').setAttribute('aria-expanded', 'false');
};
const auf = (lz) => {
const h = lz.querySelector('.lz__huelle');
h.style.height = h.querySelector('.lz__leib').offsetHeight + 'px';
lz.classList.add('ist');
lz.querySelector('.lz__kopf').setAttribute('aria-expanded', 'true');
const fertig = (e) => {
if (e.propertyName !== 'height') return;
if (lz.classList.contains('ist')) h.style.height = 'auto';
h.removeEventListener('transitionend', fertig);
};
h.addEventListener('transitionend', fertig);
};
zeilen.forEach((lz) => {
const kopf = lz.querySelector('.lz__kopf');
kopf.addEventListener('click', () => {
const offen = lz.classList.contains('ist');
zeilen.forEach((a) => { if (a.classList.contains('ist')) zu(a); });
if (!offen) auf(lz);
zeileHalten(kopf, 460);
});
});
const liste = document.querySelector('#lzliste');
if (liste && matchMedia('(hover:hover) and (pointer:fine)').matches) {
const waehle = (e) => {
if (e.pointerType === 'touch') return;
const y = e.clientY;
let ziel = zeilen.find((lz) => {
const r = lz.getBoundingClientRect();
return y >= r.top && y <= r.bottom;
});
if (!ziel) {
let kleinster = Infinity;
zeilen.forEach((lz) => {
const r = lz.getBoundingClientRect();
const d = y < r.top ? r.top - y : y - r.bottom;
if (d < kleinster) { kleinster = d; ziel = lz; }
});
}
if (!ziel || ziel.classList.contains('ist')) return;
zeilen.forEach((a) => { if (a.classList.contains('ist')) zu(a); });
auf(ziel);
};
liste.addEventListener('pointerenter', waehle, { passive: true });
liste.addEventListener('pointermove', waehle, { passive: true });
liste.addEventListener('pointerleave', () => {
zeilen.forEach((a) => { if (a.classList.contains('ist')) zu(a); });
});
}
})();
(function vollbreiteBloecke() {
if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
const ecke = parseFloat(getComputedStyle(document.documentElement)
.getPropertyValue('--r-seite')) || 56;
document.querySelectorAll('[data-zug]').forEach((block) => {
const sekt = block.parentElement;
const stand = { t: 0 };
const zeichne = () => {
const breite = block.getBoundingClientRect().width;
const rand = parseFloat(getComputedStyle(document.documentElement)
.getPropertyValue('--pad')) || 40;
const maxw = parseFloat(getComputedStyle(document.documentElement)
.getPropertyValue('--maxw')) || 1520;
const einzug = Math.max(24, Math.max(rand, (breite - maxw) / 2) - 40);
block.style.clipPath = 'inset(0 ' + (einzug * stand.t).toFixed(1) +
'px round ' + ecke + 'px)';
};
zeichne();
gsap.to(stand, {
t: 1, ease: 'none', onUpdate: zeichne,
scrollTrigger: { trigger: sekt, start: 'bottom bottom',
end: 'bottom top+=25%', scrub: 0.5 },
});
addEventListener('resize', zeichne);
});
})();
(function videoReferenzen() {
const DATEN = [
{ zitat: 'Sie haben aus groben Ideen eine Marke gemacht, die klar und selbstbewusst wirkt.',
rolle: 'Geschäftsführung', firma: 'Nordlicht', film: 'video/testimonial-01' },
{ zitat: 'Zum ersten Mal erklärt uns jemand nicht nur, was gemacht wird, sondern warum.',
rolle: 'Marketing', firma: 'Volta', film: 'video/testimonial-02' },
{ zitat: 'Schnell, direkt, ohne Agentur-Nebel — und das Team kann alles selbst pflegen.',
rolle: 'Gründung', firma: 'Meridian', film: 'video/testimonial-03' },
];
const film = document.getElementById('vrefVideo');
const zitat = document.getElementById('vrefZitat');
const rolle = document.getElementById('vrefRolle');
const firma = document.getElementById('vrefFirma');
const chips = [...document.querySelectorAll('#vrefChips button')];
if (!film || !chips.length) return;
const sanft = matchMedia('(prefers-reduced-motion: reduce)').matches;
let ist = -1;
const setze = (i) => {
if (i === ist) return;
ist = i;
const d = DATEN[i];
chips.forEach((c, k) => c.classList.toggle('ist', k === i));
gsap.to([zitat, '.vref__wer'], {
opacity: 0, y: 12, duration: T_FLAECHE, ease: KURVE,
onComplete: () => {
zitat.textContent = '«' + d.zitat + '»';
rolle.textContent = d.rolle; firma.textContent = d.firma;
gsap.to([zitat, '.vref__wer'], { opacity: 1, y: 0, duration: T_FARBE, ease: KURVE });
},
});
gsap.to(film, {
opacity: 0, duration: T_FLAECHE, ease: KURVE,
onComplete: () => {
film.poster = d.film + '-poster.jpg';
film.src = d.film + '.mp4';
if (!sanft) film.play().catch(() => {});
gsap.to(film, { opacity: 1, duration: T_BILD, ease: KURVE });
},
});
};
chips.forEach((c, i) => c.addEventListener('click', () => setze(i)));
ScrollTrigger.create({
trigger: '.vref', start: 'top 90%', once: true,
onEnter: () => { film.preload = 'auto'; if (!sanft) film.play().catch(() => {}); },
});
setze(0);
})();
(function faelle() {
const FAELLE = [
{ titel: 'Eine klare Markenidentität für eine junge Energieplattform',
jahr: '2025', dauer: '6 Wochen', pillen: ['Branding', 'Website', '3D'],
bild: 'bilder/fall-1.jpg', link: 'arbeiten/nordlicht.html' },
{ titel: 'Ein Auftritt, der komplexe Technik verständlich macht',
jahr: '2024', dauer: '9 Wochen', pillen: ['Branding', 'Content', 'Social Media'],
bild: 'bilder/fall-2.jpg', link: 'arbeiten/volta.html' },
{ titel: 'Vom Nischenprodukt zur Marke mit Haltung',
jahr: '2024', dauer: '12 Wochen', pillen: ['Strategie', 'Website', 'Performance'],
bild: 'bilder/fall-3.jpg', link: 'arbeiten/meridian.html' },
];
const inhalt = document.getElementById('fallInhalt');
const bild = document.getElementById('fallBild');
const liste = [...document.querySelectorAll('#fallListe li')];
if (!inhalt) return;
let ist = -1;
const setze = (i) => {
if (i === ist) return;
ist = i;
const f = FAELLE[i];
liste.forEach((li, k) => li.classList.toggle('ist', k === i));
gsap.to(inhalt, {
opacity: 0, y: 14, duration: T_FLAECHE, ease: KURVE,
onComplete: () => {
inhalt.querySelector('[data-feld="titel"]').textContent = f.titel;
inhalt.querySelector('[data-feld="jahr"]').textContent = f.jahr;
inhalt.querySelector('[data-feld="dauer"]').textContent = f.dauer;
inhalt.querySelector('[data-feld="pillen"]').innerHTML =
f.pillen.map((p) => `<span>${p}</span>`).join('');
inhalt.querySelector('[data-feld="link"]').href = f.link;
gsap.to(inhalt, { opacity: 1, y: 0, duration: T_FARBE, ease: KURVE });
},
});
gsap.to(bild, {
opacity: 0, scale: 1.04, duration: T_FLAECHE, ease: KURVE,
onComplete: () => {
bild.src = f.bild;
gsap.to(bild, { opacity: 1, scale: 1, duration: T_BILD, ease: KURVE });
},
});
};
document.querySelectorAll('.fall__ausloeser').forEach((t, i) => {
ScrollTrigger.create({ trigger: t, start: 'top 60%', end: 'bottom 60%',
onToggle: (s) => s.isActive && setze(i) });
});
liste.forEach((li, i) => li.addEventListener('click', () => setze(i)));
setze(0);
})();
(function lamellen() {
const feld = document.getElementById('lamellen');
if (!feld) return;
const streifen = [...feld.querySelectorAll('.lamelle')];
const waehle = (s) => {
if (s.classList.contains('ist')) return;
streifen.forEach((x) => {
const ist = x === s;
x.classList.toggle('ist', ist);
x.setAttribute('aria-pressed', ist ? 'true' : 'false');
});
};
streifen.forEach((s) => {
s.addEventListener('pointerenter', () => waehle(s));
s.addEventListener('focus', () => waehle(s));
s.addEventListener('click', () => waehle(s));
});
})();
(function preise() {
const knoepfe = [...document.querySelectorAll('#schalter button')];
if (!knoepfe.length) return;
const setze = (takt) => {
knoepfe.forEach((k) => k.classList.toggle('ist', k.dataset.takt === takt));
document.body.classList.toggle('langtakt', takt === 'lang');
};
knoepfe.forEach((k) => k.addEventListener('click', () => setze(k.dataset.takt)));
const start = knoepfe.find((k) => k.classList.contains('ist'));
if (start) setze(start.dataset.takt);
})();
(function akkordeon() {
const zeilen = [...document.querySelectorAll('#faq .fr')];
if (!zeilen.length) return;
const zu = (fr) => {
const h = fr.querySelector('.fr__huelle');
h.style.height = h.scrollHeight + 'px';
requestAnimationFrame(() => { h.style.height = '0px'; });
fr.classList.remove('ist');
fr.querySelector('.fr__kopf').setAttribute('aria-expanded', 'false');
};
const auf = (fr) => {
const h = fr.querySelector('.fr__huelle');
h.style.height = h.querySelector('.fr__leib').offsetHeight + 'px';
fr.classList.add('ist');
fr.querySelector('.fr__kopf').setAttribute('aria-expanded', 'true');
const fertig = (e) => {
if (e.propertyName !== 'height') return;
if (fr.classList.contains('ist')) h.style.height = 'auto';
h.removeEventListener('transitionend', fertig);
};
h.addEventListener('transitionend', fertig);
};
zeilen.forEach((fr) => {
const kopf = fr.querySelector('.fr__kopf');
kopf.addEventListener('click', () => {
const offen = fr.classList.contains('ist');
zeilen.forEach((a) => { if (a.classList.contains('ist')) zu(a); });
if (!offen) auf(fr);
zeileHalten(kopf, 340);   /* Aufklappen dauert jetzt .3s, nicht .46s */
});
});
})();
(function bildhover() {
document.querySelectorAll('.fall__bild').forEach((w) => {
const img = w.querySelector('img');
if (!img) return;
w.addEventListener('pointerenter', () => gsap.to(img, { scale: 1.06, duration: T_BILD, ease: KURVE }));
w.addEventListener('pointerleave', () => gsap.to(img, { scale: 1, duration: T_BILD, ease: KURVE }));
});
})();
(function termin() {
const kal = document.getElementById('kal');
const form = document.getElementById('fm');
if (!kal || !form) return;
const MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
'August', 'September', 'Oktober', 'November', 'Dezember'];
const ZEITEN = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'];
const raster = document.getElementById('kalRaster');
const monatFeld = document.getElementById('kalMonat');
const slotFeld = document.getElementById('kalSlots');
const slots = document.getElementById('slots');
const zusammen = document.getElementById('fmGewaehlt');
const pfeile = [...kal.querySelectorAll('.kal__pfeil')];
const heute = new Date(); heute.setHours(0, 0, 0, 0);
const frueh = new Date(heute); frueh.setDate(frueh.getDate() + 1);
const spaet = new Date(heute); spaet.setMonth(spaet.getMonth() + 3);
let monat = new Date(heute.getFullYear(), heute.getMonth(), 1);
let tag = null, zeit = null;
const gleich = (a, b) => a && b && a.getTime() === b.getTime();
const lesbar = (d) => d.getDate() + '. ' + MONATE[d.getMonth()] + ' ' + d.getFullYear();
const melden = () => {
const fertig = tag && zeit;
zusammen.textContent = fertig
? lesbar(tag) + ' um ' + zeit + ' Uhr'
: tag ? lesbar(tag) + ' — noch eine Uhrzeit wählen'
: 'Noch kein Termin gewählt';
zusammen.classList.toggle('ist', !!fertig);
};
const zeichneSlots = () => {
slots.innerHTML = '';
ZEITEN.forEach((z) => {
const b = document.createElement('button');
b.type = 'button'; b.textContent = z;
b.classList.toggle('ist', z === zeit);
b.disabled = !tag;
b.addEventListener('click', () => {
zeit = z;
[...slots.children].forEach((x) => x.classList.toggle('ist', x === b));
melden();
});
slots.appendChild(b);
});
};
const zeichne = () => {
monatFeld.textContent = MONATE[monat.getMonth()] + ' ' + monat.getFullYear();
const versatz = (new Date(monat.getFullYear(), monat.getMonth(), 1).getDay() + 6) % 7;
const letzter = new Date(monat.getFullYear(), monat.getMonth() + 1, 0).getDate();
raster.innerHTML = '';
for (let i = 0; i < versatz; i++) {
const l = document.createElement('span'); l.className = 'kal__leer';
raster.appendChild(l);
}
for (let d = 1; d <= letzter; d++) {
const datum = new Date(monat.getFullYear(), monat.getMonth(), d);
const wochenende = datum.getDay() === 0 || datum.getDay() === 6;
const b = document.createElement('button');
b.type = 'button'; b.className = 'kal__tag';
b.innerHTML = '<span class="kal__bg" aria-hidden="true"></span>'
+ '<span class="kal__t">' + d + '</span>'
+ '<span class="kal__t kal__t--neu" aria-hidden="true">' + d + '</span>';
b.disabled = wochenende || datum < frueh || datum > spaet;
if (gleich(datum, heute)) b.classList.add('heute');
if (gleich(datum, tag)) b.classList.add('ist');
b.addEventListener('click', () => {
tag = datum; zeit = null;
zeichne(); zeichneSlots(); melden();
});
raster.appendChild(b);
}
pfeile[0].disabled = monat <= new Date(heute.getFullYear(), heute.getMonth(), 1);
pfeile[1].disabled = monat >= new Date(spaet.getFullYear(), spaet.getMonth(), 1);
};
pfeile.forEach((p) => p.addEventListener('click', () => {
monat = new Date(monat.getFullYear(), monat.getMonth() + (+p.dataset.schritt), 1);
zeichne();
}));
form.addEventListener('submit', (e) => {
e.preventDefault();
const w = (n) => (form.elements[n].value || '').trim();
if (!form.reportValidity()) return;
const zeilen = [
'Name: ' + w('name'),
'Unternehmen: ' + w('firma'),
'E-Mail: ' + w('mail'),
'Telefon: ' + w('tel'),
'Wunschtermin: ' + (tag && zeit ? lesbar(tag) + ', ' + zeit + ' Uhr' : 'offen'),
'', w('text') || '',
];
location.href = 'mailto:hallo@klartext-digital.ch'
+ '?subject=' + encodeURIComponent('Anfrage über die Website — ' + w('name'))
+ '&body=' + encodeURIComponent(zeilen.join('\n'));
});
zeichne(); zeichneSlots(); melden();
})();
(() => {
const graf = document.querySelector('.wiewir__bild');
const bild = graf && graf.querySelector('.ag');
if (!bild) return;
const glatt = (p) => p * p * (3 - 2 * p);
gsap.matchMedia().add(
'(min-width: 900px) and (prefers-reduced-motion: no-preference)',
() => {
let D = 0, A = 0, hoch = 0;
const messen = () => {
D = Math.round(innerHeight * 0.85);
A = Math.round(D / 1.5);
hoch = Math.round(bild.getBoundingClientRect().height * 0.105);
graf.style.marginBottom = A + 'px';
};
messen();
const st = ScrollTrigger.create({
trigger: graf,
start: () => 'center center+=' + (hoch + D / 6),
end: () => '+=' + D,
invalidateOnRefresh: true,
onRefreshInit: messen,
onUpdate: (self) => gsap.set(bild, { y: A * glatt(self.progress) }),
onLeave: () => gsap.set(bild, { y: A }),
onLeaveBack: () => gsap.set(bild, { y: 0 }),
});
return () => {
st.kill();
graf.style.marginBottom = '';
gsap.set(bild, { clearProps: 'y' });
};
},
);
})();
(() => {
const knopf = document.getElementById('hoch');
if (!knopf) return;
const pruefe = () => knopf.classList.toggle('ist', scrollY > innerHeight * 1.5);
pruefe();
lenis.on('scroll', pruefe);
addEventListener('resize', pruefe);
knopf.addEventListener('click', () => lenis.scrollTo(0, { duration: 1.1 }));
})();
addEventListener('load', () => ScrollTrigger.refresh());
