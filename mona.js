/* Die Mona Lisa im Kopfbereich.

   Zwei getrennte Sachen laufen hier:
   1. Der Blick folgt dem Mauszeiger. Die Augaepfel liegen als eigene
      Ebene ueber dem Bild und werden um wenige Bildpunkte verschoben.
      Die Lider bleiben stehen, sonst zuckt das Gesicht.
   2. Das Laecheln haengt am Abstand zum Knopf "Gespraech buchen".
      Es liegt in sieben vorgerechneten Stufen bereit, zwischen denen
      nur noch ueberblendet wird — im Browser wird nichts verzogen.

   Beide Werte werden geglaettet. Ohne das zappelt das Gesicht bei
   jeder Mausbewegung, und ein zappelndes Gesicht wirkt nicht
   lebendig, sondern kaputt. */
(function () {
  const bild = document.getElementById('monaBild');
  if (!bild || !window.gsap) return;

  const ziel  = document.querySelector('.nav__cta');
  const augeL = document.querySelector('#monaAugeL i');
  const augeR = document.querySelector('#monaAugeR i');
  if (!ziel || !augeL || !augeR) return;

  const STUFEN = 7;
  const muender = [];
  for (let i = 0; i < STUFEN; i++) {
    const m = document.getElementById('monaMund' + i);
    if (!m) return;
    muender.push(m);
  }

  const feinerZeiger = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const ruhig = matchMedia('(prefers-reduced-motion:reduce)').matches;

  const RADIUS = 560;      /* ab hier faengt das Laecheln an zu wachsen */
  const BILD_B = 1672;     /* Breite des Kopfbildes */
  const WEG_X = 4.5, WEG_Y = 2.0;   /* wie weit die Augaepfel hoechstens wandern */

  const z = { laune: 0, bx: 0, by: 0 };
  const setLaune = gsap.quickTo(z, 'laune', { duration: .55, ease: 'power3' });
  const setBx    = gsap.quickTo(z, 'bx',    { duration: .28, ease: 'power3' });
  const setBy    = gsap.quickTo(z, 'by',    { duration: .28, ease: 'power3' });

  let mx = null, my = null;

  const mitte = (el) => {
    const r = el.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
  };

  function messen() {
    if (mx === null) { setLaune(0); setBx(0); setBy(0); return; }
    const k = mitte(ziel);
    setLaune(gsap.utils.clamp(0, 1, 1 - Math.hypot(mx - k.x, my - k.y) / RADIUS));
    if (ruhig) { setBx(0); setBy(0); return; }
    const l = mitte(document.getElementById('monaAugeL'));
    const r = mitte(document.getElementById('monaAugeR'));
    const ax = (l.x + r.x) / 2, ay = (l.y + r.y) / 2;
    setBx(gsap.utils.clamp(-1, 1, (mx - ax) / 420));
    setBy(gsap.utils.clamp(-1, 1, (my - ay) / 340));
  }

  function zeichnen() {
    /* Ein Bildpunkt des Originals ist auf dem Schirm so viel wert: */
    const mass = bild.clientWidth / BILD_B;
    gsap.set([augeL, augeR], { x: z.bx * WEG_X * mass, y: z.by * WEG_Y * mass });

    /* Zwischen zwei benachbarten Stufen ueberblenden: die untere steht
       auf voll, die obere waechst ein. So bleibt die Mischung sauber. */
    const s = z.laune * (STUFEN - 1);
    const k = Math.min(STUFEN - 1, Math.floor(s));
    const t = s - k;
    for (let i = 0; i < STUFEN; i++) {
      muender[i].style.opacity = (i === k) ? 1 : (i === k + 1 ? t : 0);
    }
  }

  addEventListener('pointermove', (e) => {
    if (e.pointerType === 'touch') return;
    mx = e.clientX; my = e.clientY; messen();
  }, { passive: true });

  addEventListener('pointerleave', () => { mx = null; my = null; messen(); });
  addEventListener('scroll', messen, { passive: true });
  addEventListener('resize', messen);

  gsap.ticker.add(zeichnen);
  messen();
})();
