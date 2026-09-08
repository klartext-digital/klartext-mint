/* Die drei Kreise der Arbeitsweise-Grafik.

   Im Ruhezustand steht nur der Kern da, vergroessert. Faehrt man ueber
   einen Kreis, ruecken die Koerper auf ihre normale Groesse zurueck und
   die vier Begriffe dieses Kreises blenden mit ihren Leitungen ein.

   Warum ueber ein Attribut am SVG und nicht mit :hover im Stylesheet:
   In SVG gibt es keinen Weg, vom ueberfahrenen Kreis zurueck zu seinem
   Zweig zu greifen — die beiden sind Geschwister in verschiedenen
   Gruppen. Ein Attribut an der Wurzel loest das in einer Zeile. */
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

  /* Mit der Tastatur: die drei Flaechen sind anfahrbar. */
  flaechen.forEach((f) => {
    f.setAttribute('tabindex', '0');
    f.setAttribute('role', 'button');
    f.addEventListener('focus', () => zeigen(f.dataset.fuer));
    f.addEventListener('blur', () => zeigen(null));
  });
})();
