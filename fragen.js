(function () {
const wurzel = document.querySelector('.fragen');
if (!wurzel) return;
const liste  = wurzel.querySelector('.fragen__liste');
const reiter = [...wurzel.querySelectorAll('.reiter')];
const fragen = [...wurzel.querySelectorAll('.frage')];
const schweben = matchMedia('(hover:hover) and (pointer:fine)').matches;
function setze(ziel) {
fragen.forEach((f) => {
const offen = f === ziel;
f.classList.toggle('offen', offen);
f.querySelector('.frage__kopf').setAttribute('aria-expanded', offen ? 'true' : 'false');
});
}
reiter.forEach((r) => {
r.addEventListener('click', () => {
const thema = r.dataset.thema;
reiter.forEach((x) => {
const ist = x === r;
x.classList.toggle('ist', ist);
x.setAttribute('aria-pressed', ist ? 'true' : 'false');
});
fragen.forEach((f) => {
f.hidden = thema !== 'alle' && f.dataset.thema !== thema;
});
setze(null);
});
});
if (schweben) {
const finde = (y) => {
const sichtbar = fragen.filter((f) => !f.hidden);
if (!sichtbar.length) return null;
let ziel = sichtbar.find((f) => {
const r = f.getBoundingClientRect();
return y >= r.top && y <= r.bottom;
});
if (!ziel) {
let kleinster = Infinity;
sichtbar.forEach((f) => {
const r = f.getBoundingClientRect();
const d = y < r.top ? r.top - y : y - r.bottom;
if (d < kleinster) { kleinster = d; ziel = f; }
});
}
return ziel;
};
const SCHNELL = 1.5;
let zx = 0, zy = 0, zt = 0, tempo = 0, uhr = 0;
addEventListener('pointermove', (e) => {
const dt = e.timeStamp - zt;
tempo = dt > 50 ? Infinity : Math.hypot(e.clientX - zx, e.clientY - zy) / Math.max(1, dt);
zx = e.clientX; zy = e.clientY; zt = e.timeStamp;
}, { passive: true, capture: true });
const waehle = (e) => {
if (e.pointerType === 'touch') return;
clearTimeout(uhr);
const ziel = finde(e.clientY);
if (!ziel || ziel.classList.contains('offen')) return;
if (tempo < SCHNELL) { setze(ziel); return; }
uhr = setTimeout(() => {
const z = finde(zy);
if (z && !z.classList.contains('offen')) setze(z);
}, 60);
};
liste.addEventListener('pointerenter', waehle, { passive: true });
liste.addEventListener('pointermove', waehle, { passive: true });
liste.addEventListener('pointerleave', () => { clearTimeout(uhr); setze(null); });
}
fragen.forEach((f) => {
f.querySelector('.frage__kopf').addEventListener('click', () => {
setze(f.classList.contains('offen') ? null : f);
});
});
})();
