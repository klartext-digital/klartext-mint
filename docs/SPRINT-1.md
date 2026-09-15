# Sprint 1: Umsetzung und Übergabe

## Umgesetzt

- Vollständiges Inventar aller 27 ursprünglichen HTML-Dateien, Hosting-/Git-Prüfung und Audit vor den Änderungen.
- Homepage: Title, Description, Einleitung und Leistungsüberschrift auf Marketing für Schweizer KMU ausgerichtet. Die Marken-H1, das Mona-Lisa-Bild, Farben, Fonts und Grundlayout bleiben erhalten.
- Neue ausgebaute `/webdesign/`-Seite: Ziel, Ablauf, Relaunch, UX, technische SEO, Performance, Inhaltspflege, Budget und FAQ. Vorhandener Kostenrechner bleibt funktionsfähig und als ungeprüfter Entwurf gekennzeichnet.
- Neuer Leitfaden `/wissen/website-kosten-schweiz/`: Kostentreiber, Website-Typen, Betriebskosten, Offertenvergleich, Budgetvorbereitung und FAQ. Keine unbelegten Preisbereiche oder erfundene Autorenschaft.
- `/wissen/` als zugänglicher Hub, Links von Homepage/Footer/Webdesign sowie Rückverweise.
- Saubere Pfade für Leistungsseiten, Über uns, Projekte, Blog und Rechtliches. Alte HTML-Adressen werden als eigenständige Weiterleitungsdateien ausgegeben. Alle Pfade stehen in URL-MAP.json.
- Ein zentraler Build erzeugt pro Seite Title, Description, Canonical, Robots, Open Graph und JSON-LD. Organisation mit bestätigter Marke/URL/Logo; keine Aussage über Rechtsform. Breadcrumbs sichtbar und als Daten. Article für den neuen Leitfaden.
- Sitemap und robots.txt aus derselben Konfiguration. Draft-Seiten nicht in die Sitemap aufnehmen. Studien bleiben dauerhaft noindex.
- Bildgrössen aus echten Dateien reserviert, Menü-/Dienstbilder bei Bedarf laden, Skripte in korrekter Reihenfolge mit defer, Hauptschrift und Hero-Bild vorladen. Der bisherige Ladeschirm ist für normale Besuche deaktiviert, seine optionale Implementierung bleibt erhalten.
- Mobile Artikelabstände und einzeiliger Navigations-CTA korrigiert. Fehlende Blog-Sprungmarke und fehlerhafte Webdesign-Verweise repariert.
- Veröffentlichung der geprüften Ausgabe über einen separaten gh-pages-Branch; Quellen und veröffentlichte Dateien bleiben getrennt. Ein optionales Workflow-Beispiel liegt in docs/.

## Was noch eine inhaltliche Bestätigung braucht

| Thema | Aktueller Umgang | Benötigte Grundlage |
|---|---|---|
| Finale Domain | Vorhandene GitHub-Pages-Adresse in Canonicals | Verbindliche Domain und bevorzugte www-Variante |
| Person | Technisch vorbereitet, keine Person veröffentlicht | Vollständiger öffentlicher Name und bestätigtes sichtbares Profil |
| Organization | Nur Marke klartext., vorhandenes Logo und URL | Weitere Angaben erst nach Bestätigung |
| GmbH / Standort / Kontakte | Bestehende Texte mit Entwurfsmarkierung; kein entsprechendes Schema | Tatsächlicher Betreiber, Rechtsform, Anschrift, erreichbare Kontakte |
| Team | Sichtbar als ungeprüft markiert | Echte Namen, Rollen, Bilder und Zustimmung |
| Referenzen / Kundenlogos / Zitate | Sichtbar markiert, keine Review-/Rating-Daten | Projektzuordnung, Rechte und nachprüfbare Aussagen; frühere Arbeitgeberprojekte separat erläutern |
| Preise / Rechner | Bestehende Werte als Entwurf; Artikel ohne Marktpreisbehauptung | Einheitliche Kalkulation, Leistungsumfang, MWST-Darstellung und freigegebene Preisbereiche |
| Formulare / Social | Bestehendes Entwurfsverhalten dokumentiert | Buchung/Newsletter tatsächlich anbinden, Zielprofile bestätigen |
| Neue Texte | Vollständige reviewbare Entwürfe | Inhaltliche Freigabe vor Indexierung |

## Freigabe-Mechanik

`seo.config.json`:

- `base_url`: bestehende funktionierende Basisadresse; bei bestätigter Domain aktualisieren.
- `indexable`: bleibt false, bis die Veröffentlichung für Suchmaschinen freigegeben ist.
- `approved_paths`: explizite Liste freigegebener kanonischer Pfade, beispielsweise `""`, `"webdesign/"`, `"wissen/"`, `"wissen/website-kosten-schweiz/"`. Nur diese Seiten werden bei indexable=true indexierbar und Teil der Sitemap. Keine stillschweigende Freigabe anderer Seiten.
- `organization_verified`: bezieht sich aktuell ausschliesslich auf Marke, URL und Logo. Nicht als GmbH-/Handelsregister-Bestätigung interpretieren.
- `person`: nach Bestätigung Objekt mit `verified: true`, `name` und `visible_text`. Der vollständige Name muss auch im sichtbaren Über-uns-Quelltext stehen. Kein erfundener Beruf, Titel, sameAs oder Mitarbeiterbestand.

Beispiel ohne echte Personendaten:

```json
{"verified": true, "name": "BESTÄTIGTER ÖFFENTLICHER NAME", "visible_text": "BESTÄTIGTER ÖFFENTLICHER NAME"}
```

## Technische Grenzen

- GitHub Pages liefert die alten HTML-Dateien zunächst mit HTTP 200 und HTML-Sofortweiterleitung aus, nicht als echte serverseitige 301. Canonical und funktionierender Link sind enthalten. Beim späteren Zielhost 301-Regeln anhand der URL-Matrix setzen.
- robots.txt unter `/klartext-mint/` ist nicht die robots.txt des Hosts. Das noindex im HTML bleibt der wirksame Schutz vor Indexierung dieses Entwurfs.
- Die Sitemap ist im Draft-Modus absichtlich leer. Keine Anmeldung einer leeren/ungeprüften Sitemap bei Suchmaschinen erfolgt.
- Keine behaupteten Core-Web-Vitals-Scores. Labortests und echte Felddaten über LCP, INP und CLS stehen nach endgültigem Hosting und Freigabe an.
- Layout wurde im vorhandenen Codex-Browser geprüft; das verlangte Claude-in-Chrome-Werkzeug stand nicht zur Verfügung.
- Veröffentlichung unter der bestehenden GitHub-Pages-Adresse über gh-pages. Keine Domainumschaltung. Der GitHub-Anmeldung fehlt Workflow-Schreibzugriff; der alternative Veröffentlichungsweg verwendet keine zusätzlichen Berechtigungen.

## Grundlagen

- [Google: Organization](https://developers.google.com/search/docs/appearance/structured-data/organization)
- [Google: Canonicalisierung](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Google: robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [GitHub: eigene Pages-Workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

## Durchgeführte Prüfungen

- Alle 50 erzeugten HTML-Dateien inklusive Weiterleitungen per HTTP: 200.
- Titles, Description, genau ein Canonical, Robots, JSON-LD, Breadcrumb-Reihenfolge, lokale Links, Bild-/Script-/Stylesheet-Pfade und Sprungmarken geprüft.
- Release-Probe in isolierter Testkopie mit anderer Basisadresse und Unterpfad: freigegebene URLs werden korrekt in die Sitemap aufgenommen.
- Person-Ausgabe mit sichtbarem Testprofil geprüft; unsichtbare Person wird beim Build abgelehnt. Studien können nicht zur Indexierung freigegeben werden.
- Desktop (1440 px) und Handy (390 px): Homepage, Webdesign und Kostenartikel geprüft. Keine horizontale Überbreite im Dokument.
- FAQ öffnet, Rechner reagiert auf Shop-Auswahl, Inhaltsverzeichnis springt zum Ziel. Keine Fehler/Warnungen in der Browserkonsole der geprüften Seiten.
- Die gewollten Scroll-Einblendungen erfordern zum visuellen Prüfen einen tatsächlichen Seitenbesuch/Scroll; ein einzelner sofortiger Vollseitenscreenshot erfasst sonst noch unsichtbare Einblendungen.
