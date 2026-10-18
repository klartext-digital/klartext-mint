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
    const finde = (y) => {
      const sichtbar = fragen.filter((f) => !f.hidden);
      if (!sichtbar.length) return null;

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
      return ziel;
    };

    /* 18.10.2026: Tempo statt Wartezeit. Die Schwelle von 110 ms galt fuer
       JEDE Bewegung und fuehlte sich deshalb traege an. Gegen das Flackern
       (13.10.: beim schnellen Hoch und Runter gingen gestreifte Fragen
       reihenweise gelb auf und zu) reicht es, das DURCHFAHREN zu erkennen:
       Wer gezielt auf eine Frage zeigt, bewegt die Maus langsamer als
       1,5 px pro ms - die Frage oeffnet sofort. Wer schneller darueber
       faehrt, oeffnet nur die Frage, auf der der Zeiger stehen bleibt,
       60 ms nach der letzten Bewegung. */
    const SCHNELL = 1.5;
    let zx = 0, zy = 0, zt = 0, tempo = 0, uhr = 0;
    addEventListener('pointermove', (e) => {
      /* Erstes Signal nach einer Ruhepause: das Tempo ist noch
         unbekannt (der Vergleich laege beim letzten Halt). Dann
         entscheidet das naechste Signal, 8 bis 16 ms spaeter. */
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

    /* 18.10.2026, Dusan: "bei den FAQs ist ein verzoegerter Hover-Effekt ...
       ich moechte, dass es schnell ist wie vorher, wie bei den Leistungen".
       Die Verweilschwelle von 110 ms (13.10., gegen Flackern) ist wieder
       raus: die Frage unter dem Zeiger oeffnet sofort, wie bei den
       Leistungszeilen. Das Flackern von damals kam vor allem von der
       langen Federbewegung (505 ms, mehrere liefen uebereinander); die
       Bewegung ist jetzt kurz und ohne Ueberschwingen. */

    /* Auch beim Eintreten sofort greifen, nicht erst nach der
       ersten Bewegung innerhalb der Liste. */
    liste.addEventListener('pointerenter', waehle, { passive: true });
    liste.addEventListener('pointermove', waehle, { passive: true });

    liste.addEventListener('pointerleave', () => { clearTimeout(uhr); setze(null); });
  }

  /* ── Tippen und Tastatur ────────────────────────────────────── */
  fragen.forEach((f) => {
    f.querySelector('.frage__kopf').addEventListener('click', () => {
      setze(f.classList.contains('offen') ? null : f);
    });
  });
})();
