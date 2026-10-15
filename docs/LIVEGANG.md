# Livegang auf klartext-digital.ch

Vorbereitet am 15.10.2026. **Startet nur mit ausdrücklichem Auftrag von Dusan.**
Ziel: an einem Tag sauber live, ohne dass Mail (Google Workspace) unterbricht.

## Vorher klären

- [ ] Ausdrücklicher Auftrag „Livegang“
- [ ] Hostinger: Webhosting-Paket für klartext-digital.ch vorhanden? (Domain ist dort, heute nur Parkseite)
- [ ] Platzhalter entschieden: Team, Kundenstimme, Projekte Nordlicht/Volta/Meridian (siehe `SEO-AUDIT-2026-10.md`)
- [ ] Handelsregistereintrag da? Sonst bleibt „(in Gründung)“ stehen, UID folgt später

## 1. Build auf die Produktivdomain umstellen

1. `scripts/release_policy.py`: Produktivdomain `https://klartext-digital.ch/` als erlaubtes Ziel ergänzen (heute nur die GitHub-Vorschau).
2. `seo.config.json`:
   - `base_url` → `https://klartext-digital.ch/`
   - `indexable` → `true`
   - `approved_paths` → alle Seiten ausser `marke.html`, `laune.html`, `takt.html`
   - `verification.bing` → Code aus den Bing Webmaster Tools (falls Meta-Tag-Methode)
3. Bauen und prüfen (`build.py`, `check.py`). Kontrolle:
   - Entwurfs-Hinweis unten rechts ist weg (fällt automatisch mit `indexable`)
   - `robots` = `index, follow` auf den freigegebenen Seiten
   - `sitemap.xml` enthält alle freigegebenen Seiten
   - Canonicals zeigen auf `https://klartext-digital.ch/…`

## 2. Hochladen zu Hostinger

Inhalt von `_site/` in `public_html/`, dazu die `.htaccess` unten.

```apache
# HTTPS und ohne www: alles auf https://klartext-digital.ch
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\. [NC]
RewriteRule ^ https://klartext-digital.ch%{REQUEST_URI} [L,R=301]

# Alte .html-Adressen und /wissen/ leiten die Seiten selbst weiter (Build).
# Fehlende Seiten: eigene 404 mit echtem Status 404.
ErrorDocument 404 /404.html

# Caching: Bilder/Schriften lange, HTML kurz
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/css "access plus 1 week"
  ExpiresByType application/javascript "access plus 1 week"
  ExpiresByType text/html "access plus 10 minutes"
</IfModule>
```

## 3. DNS bei Hostinger

- **Nur** A-Record (und www) auf das Hosting zeigen lassen.
- **MX-, SPF- und google-site-verification-Einträge NIE anfassen.** Sonst ist hallo@ tot.
- SSL-Zertifikat in Hostinger aktivieren (kann Stunden dauern).
- Prüfen mit `curl --resolve`, nicht mit normalem curl (lokaler DNS-Cache zeigt die alte Parkseite).

## 4. Am selben Tag prüfen

- [ ] `https://klartext-digital.ch/` 200, `http://` und `www.` leiten mit 301 weiter
- [ ] Unbekannte Adresse liefert 404 mit Fehlerseite
- [ ] Alle Seiten auf Computer und Handy (Sichtprüfung)
- [ ] Test-Mail an hallo@ kommt an (Mail unberührt)
- [ ] `robots.txt`, `sitemap.xml`, `llms.txt` an der Wurzel erreichbar

## 5. Anmelden und einreichen

- [ ] Search Console (Domain-Property ist bestätigt): Sitemap einreichen, Startseite und Leistungsseiten per URL-Prüfung zur Indexierung beantragen
- [ ] Bing Webmaster Tools: Import aus Search Console, Sitemap
- [ ] Google-Unternehmensprofil: Website eintragen
- [ ] Rich-Results-Test für Startseite und eine Leistungsseite
- [ ] PageSpeed messen (Startseite, Handy), Ladeschirm-Wirkung festhalten

## 6. Danach

- Verzeichniseinträge nach `~/Desktop/02_KLARTEXT/Marke/Verzeichniseintraege.md`
- Profil-Links als `sameAs` in den Steckbrief (seo.config.json)
- Indexierung erst nach einigen Tagen bewerten; „Gefunden, nicht indexiert“ ist eine Warteschlange, kein Fehler
