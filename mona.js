/* Die Mona Lisa im Kopfbereich.

   Zwei getrennte Sachen laufen hier, und sie kommen aus zwei
   verschiedenen Quellen:

   1. Der Blick folgt dem Mauszeiger. Die Iris liegt als eigene Ebene
      ueber einer Lederhaut-Platte und ist auf die Lidspalte
      beschnitten. Es wandert also NUR die Iris — bewegte man das ganze
      Auge, saehe es aus wie Rutschen statt wie Blicken. Beim Seitenblick
      wird die Iris zusaetzlich schmaler, weil sich der Augapfel dreht.

   2. Das Lachen haengt am Abstand zum Knopf "Gespraech buchen". Es
      besteht aus neun echten Zwischenbildern zwischen zwei Aufnahmen
      derselben Person. Deshalb gibt es Zaehne, gehobene Wangen und
      zusammengekniffene Augen — das laesst sich nicht rechnen, das muss
      fotografiert sein.

   Sobald sie zu lachen beginnt, uebernehmen die Lachbilder auch die
   Augen. Die Blick-Ebene blendet darum frueh aus, sonst laegen zwei
   verschiedene Augen uebereinander. */
(function () {
  const bild = document.getElementById('monaBild');
  if (!bild || !window.gsap) return;

  const ziel   = document.querySelector('.nav__cta');
  const blickL = document.getElementById('blickL');
  const blickR = document.getElementById('blickR');
  if (!ziel || !blickL || !blickR) return;

  const irisL = blickL.querySelector('.iris');
  const irisR = blickR.querySelector('.iris');

  const STUFEN = 9;
  const lachen = [];
  for (let i = 0; i < STUFEN; i++) {
    const el = document.getElementById('lachen' + i);
    if (!el) return;
    lachen.push(el);
  }

  const feinerZeiger = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const ruhig = matchMedia('(prefers-reduced-motion:reduce)').matches;

  const RADIUS = 560;      /* ab hier faengt das Lachen an zu wachsen */
  const BILD_B = 1672;     /* Breite des Grundbildes */
  const WEG_X = 3.0, WEG_Y = 1.6;   /* Ausschlag der Iris in Bildpunkten */
  const UEBERGABE = 0.22;  /* ab hier uebernehmen die Lachbilder die Augen */

  const z = { laune: 0, bx: 0, by: 0 };
  const setLaune = gsap.quickTo(z, 'laune', { duration: .55, ease: 'power3' });
  const setBx    = gsap.quickTo(z, 'bx',    { duration: .30, ease: 'power2' });
  const setBy    = gsap.quickTo(z, 'by',    { duration: .30, ease: 'power2' });

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
    const l = mitte(blickL), r = mitte(blickR);
    const ax = (l.x + r.x) / 2, ay = (l.y + r.y) / 2;
    setBx(gsap.utils.clamp(-1, 1, (mx - ax) / 420));
    setBy(gsap.utils.clamp(-1, 1, (my - ay) / 340));
  }

  function zeichnen() {
    const mass = bild.clientWidth / BILD_B;   /* ein Bildpunkt auf dem Schirm */

    /* Zwischen zwei benachbarten Lachstufen ueberblenden: die untere
       steht auf voll, die obere waechst ein. */
    const s = z.laune * (STUFEN - 1);
    const k = Math.min(STUFEN - 1, Math.floor(s));
    const t = s - k;
    for (let i = 0; i < STUFEN; i++) {
      lachen[i].style.opacity = (i === k) ? 1 : (i === k + 1 ? t : 0);
    }

    const sicht = gsap.utils.clamp(0, 1, 1 - z.laune / UEBERGABE);
    blickL.style.opacity = blickR.style.opacity = sicht;
    if (sicht > 0) {
      /* Beim Seitenblick verkuerzt sich die Iris — sie steht dann
         schraeg zur Blickrichtung des Betrachters. */
      const quer = 1 - 0.13 * Math.abs(z.bx);
      gsap.set([irisL, irisR], {
        x: z.bx * WEG_X * mass, y: z.by * WEG_Y * mass,
        scaleX: quer, transformOrigin: '50% 50%'
      });
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

  window.__z = z; window.__zeichnen = zeichnen;   /* nur fuer Prueffotos */
})();
