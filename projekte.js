/* Filter der Projektuebersicht.

   Kein Nachladen und kein Umsortieren: die sechs Karten stehen im
   Markup, gefiltert wird ueber ein Attribut. Wer ohne JavaScript
   kommt, sieht alle Projekte — das ist der richtige Ausgangszustand,
   nicht der leere. */
(function () {
  const raster = document.getElementById('proRaster');
  if (!raster) return;
  const karten = [...raster.querySelectorAll('.pk')];
  const reiter = [...document.querySelectorAll('.pro__reiter .reiter')];
  const leer = document.getElementById('proLeer');

  const zeige = (thema) => {
    let sichtbar = 0;
    karten.forEach((k) => {
      const passt = thema === 'alle' || (k.dataset.themen || '').split(' ').includes(thema);
      k.hidden = !passt;
      if (passt) sichtbar++;
    });
    reiter.forEach((r) => {
      const ist = r.dataset.thema === thema;
      r.classList.toggle('ist', ist);
      r.setAttribute('aria-pressed', ist ? 'true' : 'false');
    });
    if (leer) leer.hidden = sichtbar > 0;
  };

  reiter.forEach((r) => r.addEventListener('click', () => zeige(r.dataset.thema)));
  if (leer) {
    const zurueck = leer.querySelector('button');
    if (zurueck) zurueck.addEventListener('click', () => zeige('alle'));
  }
})();
