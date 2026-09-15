# klartext. Website

Statische HTML/CSS/JavaScript-Website. Bestehendes Premium-Design und lokale Schrift-/Animationsdateien bleiben erhalten. Sprint 1 ergänzt eine konsistente SEO-Ausgabe.

## Bearbeiten und prüfen

Die HTML-Dateien im Repo sind die Quellen. `webdesign/index.html` ist die neue Webdesign-Quelle; die alte `leistungen/websites.html` bleibt als historischer Bestand erhalten und wird bei der Ausgabe durch eine Weiterleitung ersetzt. **Nicht `_site` bearbeiten.**

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8402 --bind 127.0.0.1 --directory _site
# In einem zweiten Terminal:
python3 scripts/check.py http://127.0.0.1:8402
```

Python 3.9+ ohne zusätzliche Bibliotheken. Der Build ersetzt ausschliesslich den selbst erzeugten Ordner `_site`. Relative Links funktionieren lokal und unter dem GitHub-Pages-Projektpfad.

- Inhalte: bestehende HTML-Dateien, `webdesign/`, `wissen/`
- Bestehendes Design: `stil.css`, `marke/`, `fonts/`
- Gezielte Ergänzungen: `seo.css`, dokumentiert in `DESIGN.md`
- Metadaten und URL-Zuordnung: `scripts/build.py`
- Indexierung, Basisadresse, bestätigte Entitäten: `seo.config.json`
- Vorher-Audit: `docs/SEO-AUDIT.md`
- Übergabe und Freigaben: `docs/SPRINT-1.md`
- Generierte URL-Matrix: `docs/URL-MAP.json`

## Status: Entwurf, nicht für Suchmaschinen freigegeben

Die bestehenden Angaben zu Team, Referenzen, Firmierung, Kontakt, Standort, Preisen und Ergebnissen sind nicht pauschal als echt bestätigt. Sichtbare Hinweise markieren die betroffenen Bereiche. Keine Bewertungen, erfundenen Personen, Adressen, Geschäftszeiten, Kundenzuordnungen oder GmbH-Angaben in strukturierten Daten.

`Organization` nennt ausschliesslich die sichtbare Marke klartext., Logo und die bestehende Website-Adresse. Das bestätigt keine Rechtsform oder Registrierung. `Person` ist vorbereitet, aber deaktiviert. `WebPage`, `BreadcrumbList` und beim neuen Leitfaden `Article` sind aktiv.

`indexable: false` erzeugt auf allen Seiten `noindex, follow` und eine leere Sitemap. Dies ist absichtlich konsistent: ungeprüfte Entwurfsseiten werden nicht zur Indexierung eingereicht. `robots.txt` sperrt Crawling nicht, damit Suchmaschinen das noindex lesen können. Unter GitHub Project Pages ist nur die robots.txt am Host-Ursprung wirksam.

## Veröffentlichung mit GitHub Pages

Der geprüfte Website-Stand wird auf dem separaten Branch `gh-pages` veröffentlicht. Der Quellcode bleibt auf `main` bzw. dem Sprint-Branch. GitHub Pages verwendet `gh-pages`, Ordner `/`.

```sh
python3 scripts/publish.py
```

Das Skript baut und prüft zuerst. Es synchronisiert dann ausschliesslich eine neu erzeugte temporäre Arbeitskopie des Veröffentlichungsbranches und pusht ohne Force. Die bestehende Desktop-Arbeitskopie und andere Branches bleiben unangetastet. GitHub baut daraus die vorhandene Projektadresse; kein DNS-/Domainwechsel.

`docs/pages-workflow.example.yml` ist eine optionale spätere Alternative über GitHub Actions. Sie wurde nicht aktiviert: der vorhandenen GitHub-Anmeldung fehlt die Berechtigung zum Schreiben von Workflow-Dateien. Der funktionierende Veröffentlichungsweg benötigt diese Zusatzberechtigung nicht.

Bei einer späteren bestätigten Domain die `base_url` ändern, neu bauen, Canonicals und Weiterleitungen prüfen. Nur nach ausdrücklichem Auftrag Domain/DNS umschalten.

## Zusammenarbeit mit Claude Code

Ausgangsstand `1a7d7b0`, Sprint-Branch `codex/seo-sprint-1`. Die Desktop-Arbeitskopie wurde nicht verändert. Änderungen über Branch/Pull Request übernehmen, nicht zwei Agenten gleichzeitig dieselben Quellen überschreiben lassen. Nach jeder Änderung Build und Check ausführen und die Ausgabe auf Desktop/Handy prüfen.
