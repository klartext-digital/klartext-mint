/* Häufige Fragen: Filter nach Thema, dazu Tastatur- und Tippbedienung.

   Das Aufklappen selbst macht das Stylesheet (Schweben und
   Tastaturfokus). Hier steht nur, was CSS nicht kann: das Filtern und
   das Umschalten per Klick — denn auf einem Handy gibt es kein
   Schweben, und mit der Tastatur muss man eine Frage festhalten
   koennen, statt sie nur zu streifen. */
(function () {
  const wurzel = document.querySelector('.fragen');
  if (!wurzel) return;

  const reiter = [...wurzel.querySelectorAll('.reiter')];
  const fragen = [...wurzel.querySelectorAll('.frage')];

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
        /* Eine ausgeblendete Frage darf nicht offen bleiben — sonst
           steht sie beim Zurueckschalten aufgeklappt da. */
        if (f.hidden) zu(f);
      });
    });
  });

  function zu(f) {
    f.classList.remove('offen');
    f.querySelector('.frage__kopf').setAttribute('aria-expanded', 'false');
  }

  fragen.forEach((f) => {
    const kopf = f.querySelector('.frage__kopf');
    kopf.addEventListener('click', () => {
      const offen = f.classList.toggle('offen');
      kopf.setAttribute('aria-expanded', offen ? 'true' : 'false');
    });
  });
})();
