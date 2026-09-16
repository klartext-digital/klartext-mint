(function () {
const svg = document.querySelector('.ag');
if (!svg) return;
const flaechen = [...svg.querySelectorAll('.ag__flaeche')];
const zeigen = (kz) => svg.setAttribute('data-aktiv', kz || '');
flaechen.forEach((f) => {
const kz = f.dataset.fuer;
f.addEventListener('pointerenter', () => zeigen(kz));
f.addEventListener('pointerdown', () => zeigen(kz));   /* Tippen */
});
svg.addEventListener('pointerleave', () => zeigen(null));
flaechen.forEach((f) => {
f.setAttribute('tabindex', '0');
f.setAttribute('role', 'button');
f.addEventListener('focus', () => zeigen(f.dataset.fuer));
f.addEventListener('blur', () => zeigen(null));
});
})();
