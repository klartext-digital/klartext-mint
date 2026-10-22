(function () {
const wurzel = document.documentElement;
if (!wurzel.classList.contains('laedt')) {
const tot = document.getElementById('lader');
if (tot && tot.parentNode) tot.parentNode.removeChild(tot);
return;
}
const l = document.getElementById('lader');
if (!l) { wurzel.classList.remove('laedt'); return; }
const fuell = l.querySelector('.lader__fuell');
const zahl  = l.querySelector('.lader__zahl:not(.lader__zahl--geist)');
const wort  = l.querySelector('.lader__wort');
const SAETZE = [
'Gutes Marketing braucht Zeit.',
'Schnell ist nicht immer gut.',
'Wer alle meint, erreicht niemanden.',
'Auffallen ist kein Zufall.',
'Eine Marke entsteht nicht über Nacht.',
'Klarheit schlägt Lautstärke.',
'Wer nichts zu sagen hat, sagt es meist laut.',
'Reichweite ohne Haltung verpufft.'
];
let vorher = -1;
try { vorher = parseInt(sessionStorage.getItem('kt-satz'), 10); } catch (e) {}
let i = Math.floor(Math.random() * SAETZE.length);
if (i === vorher) i = (i + 1) % SAETZE.length;
try { sessionStorage.setItem('kt-satz', i); } catch (e) {}
wort.textContent = SAETZE[i];
const sanft = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
const MINDEST = sanft ? 400 : 1150;
const start = Date.now();
try { if (window.gsap) gsap.globalTimeline.pause(); } catch (e) {}
let geladen = false, gezeigt = 0, fertig = false;
window.addEventListener('load', function () { geladen = true; });
function bilderAnteil() {
const b = document.images;
let n = 0, gesamt = 0;
for (let k = 0; k < b.length; k++) {
if (b[k].loading === 'lazy') continue;
gesamt++;
if (b[k].complete) n++;
}
return gesamt ? n / gesamt : 1;
}
let letzt = start;
const uhr = setInterval(function () {
const jetzt = Date.now();
const dt = Math.max(1, jetzt - letzt); letzt = jetzt;
const t = jetzt - start;
const echt   = .75 * bilderAnteil() + .25 * (geladen ? 1 : 0);
const deckel = t / MINDEST;
const ziel   = Math.min(echt, deckel, 1);
const k = 1 - Math.pow(.84, dt / 25);
gezeigt += (ziel - gezeigt) * k;
if (ziel >= 1 && gezeigt > .99) gezeigt = 1;
fuell.style.width = (gezeigt * 100).toFixed(2) + '%';
zahl.textContent = Math.round(gezeigt * 100) + '%';
if (gezeigt >= 1) schluss();
}, 25);
const notaus = setTimeout(function () {
gezeigt = 1;
fuell.style.width = '100%';
zahl.textContent = '100%';
schluss();
}, 7000);
function schluss() {
if (fertig) return;
fertig = true;
clearInterval(uhr);
clearTimeout(notaus);
l.classList.add('lader--weg');
setTimeout(function () {
wurzel.classList.remove('laedt');
if (l.parentNode) l.parentNode.removeChild(l);
try { if (window.gsap) gsap.globalTimeline.play(); } catch (e) {}
try { if (window.ScrollTrigger) ScrollTrigger.refresh(); } catch (e) {}
}, sanft ? 200 : 620);
}
})();
