# klartext. – Audit vor Sprint 1

Stand: 15.09.2026. Geprüfter Commit: `1a7d7b0` (lokal und origin/main identisch). Quelle: vollständige statische Bestandsaufnahme aller 27 HTML-Dateien plus Browserprüfung der bestehenden Homepage. Keine Search-Console-Daten oder belastbaren Nutzerdaten zur Ladezeit vorhanden.

## Wichtigste Befunde

- P0: Das gesamte Repo ist ein deklarierter Entwurf. 26 Inhalts-/Demoseiten mit noindex; Takt-Test ohne H1. Indexierung bleibt bis zur Bestätigung von Domain und Fakten gesperrt.
- P0: Kundenlogos und Projektzuordnung teilweise aus früherer Beschäftigung (vom Nutzer bestätigt). Team, Testimonials, GmbH, Zürich, Telefonnummer, Öffnungszeiten, Antwortversprechen und Preise sind nicht verifiziert. Keine Übernahme in Organization/Person/Review-Schema.
- P0: Preiswiderspruch zwischen Homepage (8’000–25’000 CHF) und Rechner (2’499–20’000 CHF). Keine belastbare Marktpreisaussage ableitbar.
- P1: Keine Canonicals, keine strukturierten Daten, keine Sitemap, keine robots.txt. HTML-Seiten und index.html werden intern explizit verlinkt.
- P1: Titles vielfach lang und auf Zürich ausgerichtet; Beschreibungen teilweise mitten im Wort abgeschnitten.
- P1: Homepage hat genau eine sinnvolle Marken-H1, aber die Einleitung nennt nicht Schweizer KMU. Diese H1 bleibt zur Designwahrung bestehen; Einleitung und passende H2 übernehmen die Zielgruppen-Einordnung.
- P1: Webdesignseite bisher kurze Leistungsbeschreibung. Wissensartikel und Wissensübersicht fehlen.
- P1: Ladeschirm verdeckt den Inhalt mindestens 1,15 Sekunden, bei Problemen bis 8 Sekunden. Zahlreiche Bilder ohne Breite/Höhe; Menüvorschaubilder werden sofort geladen.
- P2: Lokale Fonts bereits mit font-display:swap; lokale GSAP/Lenis-Dateien. Statische Inhalte sind ohne JavaScript auslesbar.
- P2: Videos bis 5,65 MB, grosse Homepage mit vielen interaktiven Bereichen. Echte Core Web Vitals benötigen Messungen; aus Dateigrössen folgt kein belastbarer Score.
- P2: Formulare öffnen nur ein Mailprogramm, Social-Links zeigen auf Startseite; keine echte Newsletter-/Buchungsintegration.

## Hosting und Grenzen

GitHub Pages unter https://klartext-digital.github.io/klartext-mint/. Keine bestätigte Produktivdomain, keine CNAME-Datei. Domain/DNS bleiben unverändert. robots.txt ist nur am Host-Ursprung wirksam; /klartext-mint/robots.txt steuert den GitHub-Pages-Host nicht. Für den aktuellen Entwurf gelten deshalb HTML-noindex-Tags. GitHub Pages unterstützt keine frei konfigurierbaren serverseitigen 301-Regeln; alte HTML-Adressen benötigen Canonical plus HTML-Weiterleitung und später gegebenenfalls echte 301 beim Zielhost.

## Vollständiges Seiteninventar

| Datei | Bisheriger Title | H1 | Bilder ohne Grössen |
|---|---|---:|---:|
| arbeiten/aesthetics-medical.html | Aesthetics Medical  /  Social Media  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| arbeiten/grand-casino-baden.html | Grand Casino Baden  /  Social Media  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| arbeiten/index.html | Arbeiten  /  KLARTEXT. Werbeagentur Zürich | 1 | 11 |
| arbeiten/meridian.html | Meridian  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| arbeiten/nordlicht.html | Nordlicht  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| arbeiten/red-bull.html | Red Bull × Grand Casino Baden  /  KLARTEXT. Werbeagentur Zürich | 1 | 19 |
| arbeiten/volta.html | Volta  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| blog/index.html | Blog  /  KLARTEXT. Werbeagentur Zürich | 1 | 17 |
| blog/kluge-marken-wachsen.html | Warum kluge Marken schneller wachsen  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| blog/marke-am-anfang.html | Wie viel Marke braucht ein Start?  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| blog/rhythmus-statt-kampagne.html | Rhythmus schlägt Kampagne  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| blog/vorne-bleiben.html | Der echte Grund, warum Marken vorne bleiben  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| blog/website-die-arbeitet.html | Woran man eine Website misst  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| blog/wettbewerb-gewinnen.html | Wie grosse Marken den Wettbewerb gewinnen  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| index.html | Werbeagentur Zürich  /  Branding, Social Media, Websites, Ads  /  KLARTEXT. | 1 | 49 |
| laune.html | Laune folgt dem Zeiger | 1 | 8 |
| leistungen/branding.html | Branding und Markenstrategie  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| leistungen/email-marketing.html | E-Mail Marketing und Newsletter  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| leistungen/index.html | Leistungen  /  KLARTEXT. Werbeagentur Zürich | 1 | 10 |
| leistungen/performance.html | Performance Marketing mit Google Ads, Meta, TikTok und LinkedIn  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| leistungen/social-media.html | Social Media Betreuung für Instagram, TikTok und LinkedIn  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| leistungen/websites.html | Website erstellen lassen in Zürich  /  KLARTEXT. Werbeagentur Zürich | 1 | 6 |
| marke.html | Marke  /  KLARTEXT. | 1 | 12 |
| recht/datenschutz.html | Datenschutz  /  KLARTEXT. Werbeagentur Zürich | 1 | 5 |
| recht/impressum.html | Impressum  /  KLARTEXT. Werbeagentur Zürich | 1 | 5 |
| takt.html | Bildtakt messen | 0 | 0 |
| ueber-uns.html | Über uns  /  KLARTEXT. Werbeagentur Zürich | 1 | 11 |
