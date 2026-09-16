(function leseband() {
const spur = document.getElementById('leseband');
if (!spur) return;
const band = spur.closest('.leseband');
const leiste = band && band.querySelector('.leseband__leiste');
const lauf = leiste && leiste.querySelector('.leseband__lauf');
spur.addEventListener('wheel', (e) => {
if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) e.stopPropagation();
}, { passive: true });
const zeichne = () => {
if (!leiste || !lauf) return;
const weite = spur.scrollWidth - spur.clientWidth;
if (weite < 4) { leiste.style.display = 'none'; return; }
leiste.style.display = '';
const voll = leiste.clientWidth;
const breit = Math.max(48, voll * (spur.clientWidth / spur.scrollWidth));
lauf.style.setProperty('--breit', breit + 'px');
lauf.style.setProperty('--weg', (spur.scrollLeft / weite) * (voll - breit) + 'px');
};
spur.addEventListener('scroll', zeichne, { passive: true });
addEventListener('resize', zeichne);
zeichne();
addEventListener('load', zeichne);
let zeiger = null, startX = 0, startLinks = 0, weg = 0;
const bewege = (e) => {
if (e.pointerId !== zeiger) return;
const d = e.clientX - startX;
if (Math.abs(d) > weg) weg = Math.abs(d);
if (weg > 6) spur.classList.add('zieht');
spur.scrollLeft = startLinks - d;
};
const loslassen = (e) => {
if (e.pointerId !== zeiger) return;
zeiger = null;
spur.classList.remove('zieht');
removeEventListener('pointermove', bewege);
removeEventListener('pointerup', loslassen);
removeEventListener('pointercancel', loslassen);
};
spur.addEventListener('pointerdown', (e) => {
if (e.button !== 0 || e.pointerType === 'touch') return;  // Touch kann der Browser selbst
zeiger = e.pointerId; startX = e.clientX; startLinks = spur.scrollLeft; weg = 0;
addEventListener('pointermove', bewege);
addEventListener('pointerup', loslassen);
addEventListener('pointercancel', loslassen);
});
spur.addEventListener('click', (e) => {
if (weg > 6) { e.preventDefault(); e.stopPropagation(); }
weg = 0;
}, true);
spur.addEventListener('dragstart', (e) => e.preventDefault());
})();
