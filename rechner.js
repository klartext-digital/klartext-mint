/* Kostenrechner für Websites.

   Bewusst eine Frage: der Aufbau der Seite (Auftraggeber 27.11.2026,
   Sprachen-Frage entfernt). Alles andere —
   eigenes Design, Inhalte aus Briefing und Onboarding, technische
   Suchmaschinen-Grundlage — gehört bei uns immer dazu und ist deshalb
   keine Option, die man abwählen kann.

   Ausgegeben wird ein Startwert ("ab CHF ..."), keine Spanne mit
   erfundener Obergrenze: Was oben draufkommt, entscheidet das
   Gespräch, nicht ein Rechner. */
(function () {
  const R = document.getElementById('rechner');
  if (!R) return;

  const PREISE = {
    art: { landingpage: 3000, mehrseitig: 4990, shop: 6990 }
  };

  const chf = (n) => (Math.round(n) + '').replace(/\B(?=(\d{3})+(?!\d))/g, '\u2019');
  const wahl = (g) => R.querySelector('input[name="' + g + '"]:checked');

  /* Zahl weich hochzählen statt springen lassen */
  let laeuft = null;
  function zeigeWert(ziel) {
    const feld = R.querySelector('#rSpanne');
    const start = +feld.dataset.wert || ziel;
    const t0 = performance.now(), dauer = 420;
    if (laeuft) cancelAnimationFrame(laeuft);
    (function schritt(t) {
      const p = Math.min(1, (t - t0) / dauer);
      const e = 1 - Math.pow(1 - p, 3);
      feld.textContent = 'ab CHF ' + chf(start + (ziel - start) * e);
      if (p < 1) laeuft = requestAnimationFrame(schritt);
      else feld.dataset.wert = ziel;
    })(t0);
  }

  function rechne() {
    const art = wahl('art');
    const artWert = art ? art.value : 'mehrseitig';
    const summe = PREISE.art[artWert];

    const posten = [[art ? art.dataset.wort : '', PREISE.art[artWert]]];

    zeigeWert(summe);

    /* Bei nur einem Posten wiederholt die Liste den Startwert — dann
       bleibt sie leer. Sie erklaert erst etwas, sobald mehr als eine
       Angabe zusammenkommt. */
    const liste = R.querySelector('#rPosten');
    liste.innerHTML = posten.length > 1 ? posten.map(function (p) {
      return '<li><span>' + p[0] + '</span><b>+ CHF ' + chf(p[1]) + '</b></li>';
    }).join('') : '';

    const zeilen = posten.map((p) => '\u2022 ' + p[0]).join('\n');
    R.querySelector('#rAnfrage').href = 'mailto:hallo@klartext-digital.ch?subject=' +
      encodeURIComponent('Anfrage Website') + '&body=' +
      encodeURIComponent('Guten Tag\n\nüber den Rechner auf eurer Seite habe ich folgende Auswahl getroffen:\n\n' +
        zeilen + '\n\nStartwert: ab CHF ' + chf(summe) + ' zuzüglich MWST\n\nFreundliche Grüsse\n');
  }

  R.addEventListener('change', rechne);
  rechne();
})();
