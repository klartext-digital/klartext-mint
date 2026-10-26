(function () {
const rahmen = document.getElementById('schaerfe');
const buehne = rahmen && rahmen.closest('.buehne');
if (!rahmen || !buehne) return;
if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
const RUHE = { x: 72, y: 33 };               // Gesicht, in % des Bildes
const jetzt = { x: RUHE.x, y: RUHE.y };
const ziel  = { x: RUHE.x, y: RUHE.y };
let laeuft = false;
function setze() {
rahmen.style.setProperty('--mx', jetzt.x.toFixed(2) + '%');
rahmen.style.setProperty('--my', jetzt.y.toFixed(2) + '%');
}
function schritt() {
jetzt.x += (ziel.x - jetzt.x) * 0.18;
jetzt.y += (ziel.y - jetzt.y) * 0.18;
setze();
if (Math.abs(ziel.x - jetzt.x) > 0.02 || Math.abs(ziel.y - jetzt.y) > 0.02) {
requestAnimationFrame(schritt);
} else {
laeuft = false;
}
}
function los() {
if (!laeuft) { laeuft = true; requestAnimationFrame(schritt); }
}
buehne.addEventListener('pointermove', (e) => {
if (e.pointerType !== 'mouse') return;
const r = rahmen.getBoundingClientRect();
ziel.x = ((e.clientX - r.left) / r.width) * 100;
ziel.y = ((e.clientY - r.top) / r.height) * 100;
los();
});
buehne.addEventListener('pointerleave', () => {
ziel.x = RUHE.x; ziel.y = RUHE.y; los();
});
setze();
})();
