/* Häufige Fragen: Themenfilter und das Öffnen beim Überfahren.

   Warum das nicht im Stylesheet steht: Zwischen zwei Kaesten liegen
   20 Punkte Luecke. Mit :hover verliert der Kasten dort den Zeiger und
   klappt zu — beim Wandern durch die Liste flackert es dauernd auf und
   zu. Deshalb entscheidet die LISTE, welche Frage offen ist:

     Zeiger im offenen Kasten          -> bleibt offen
     Zeiger in einem anderen Kasten    -> der uebernimmt
     Zeiger in der Luecke              -> die naechstgelegene Frage,
                                          und das ist fast immer die
                                          bereits offene
     Zeiger verlaesst die Liste        -> alles zu

   Dadurch gibt es keinen Zustand mehr, in dem zwischen zwei Zeilen
   alles geschlossen ist. */
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

  /* ── Filter nach Thema ──────────────────────────────────────── */
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

  /* ── Öffnen beim Überfahren ─────────────────────────────────── */
  if (schweben) {
    const waehle = (e) => {
      if (e.pointerType === 'touch') return;
      const sichtbar = fragen.filter((f) => !f.hidden);
      if (!sichtbar.length) return;
      const y = e.clientY;

      /* 1 · Steht der Zeiger in einem Kasten? Der gewinnt. */
      let ziel = sichtbar.find((f) => {
        const r = f.getBoundingClientRect();
        return y >= r.top && y <= r.bottom;
      });

      /* 2 · Sonst: der naechstgelegene. In der Luecke neben der
             offenen Frage ist das sie selbst — deshalb bleibt sie
             stehen, statt zuzuklappen. */
      if (!ziel) {
        let kleinster = Infinity;
        sichtbar.forEach((f) => {
          const r = f.getBoundingClientRect();
          const d = y < r.top ? r.top - y : y - r.bottom;
          if (d < kleinster) { kleinster = d; ziel = f; }
        });
      }
      if (ziel && !ziel.classList.contains('offen')) setze(ziel);
    };
    /* Auch beim Eintreten sofort greifen, nicht erst nach der
       ersten Bewegung innerhalb der Liste. */
    liste.addEventListener('pointerenter', waehle, { passive: true });
    liste.addEventListener('pointermove', waehle, { passive: true });

    liste.addEventListener('pointerleave', () => setze(null));
  }

  /* ── Tippen und Tastatur ────────────────────────────────────── */
  fragen.forEach((f) => {
    f.querySelector('.frage__kopf').addEventListener('click', () => {
      setze(f.classList.contains('offen') ? null : f);
    });
  });
})();
