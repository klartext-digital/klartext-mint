# Zusammenarbeit an klartext-mint

Hier arbeiten zwei KI-Werkzeuge: **ChatGPT/Codex** und **Claude Code**. Diese Regeln gelten für beide.

## Ein einziger Weg zur Live-Seite

Live-Adresse: https://klartext-digital.github.io/klartext-mint/

1. Quellstand ist immer `main`. Nie direkt `gh-pages` bearbeiten, nie die Pages-Quelle in den GitHub-Einstellungen ändern.
2. Arbeit auf einem eigenen Zweig beginnen, der vom aktuellen `main` abzweigt:
   ChatGPT/Codex → `codex/<thema>`, Claude Code → `claude/<thema>` oder direkt nach Absprache.
3. Nur Quelldateien bearbeiten (HTML, `stil.css`, `seo.css`, JS, `seo.config.json`). **Nie `_site/` bearbeiten** — der Ordner wird bei jedem Bau gelöscht.
4. Bauen und prüfen:
   ```sh
   python3 scripts/build.py
   python3 scripts/check.py
   ```
5. Sichtprüfung Desktop (1440 px) und Handy (390 px): keine Konsolenfehler, kein waagrechter Überlauf.
6. Übernahme nach `main` (Pull Request, nie Force-Push).
7. Veröffentlichen **nur aus `main`**: `python3 scripts/publish.py`, danach die Live-Adresse prüfen.

Nicht zwei Werkzeuge gleichzeitig auf `main`.

## Rollen

- **ChatGPT/Codex:** SEO/GEO-Strategie, Keywords, Texte, Metadaten, strukturierte Daten, neue Leistungs- und Wissensseiten.
- **Claude Code:** Design, Interaktion, Review der Änderungen, Zusammenführung, Veröffentlichung.

## Verbindliche Vorgaben des Auftraggebers

- **Ladeschirm bleibt aktiv:** beim ersten Besuch und danach bei jedem zehnten Aufruf. Nicht abschalten, auch nicht über den Build.
- **Design, Farben, Schriften:** nur mit Freigabe ändern. Kein Sandton/Beige, kein Streifenmuster.
- **Kein vollständiger Personenname auf GitHub** — weder in Dateien noch in Commits. Commits laufen auf „KLARTEXT".
- **Referenzen (Entscheid des Auftraggebers, 16.09.2026):** Alle Kunden, die er betreut hat, gelten als klartext.-Referenzen und dürfen so gezeigt werden. Keine Hinweise wie „Referenzen im Entwurf“ oder „aus früheren beruflichen Stationen“ mehr einblenden.
- **Nichts erfinden:** keine Firmenangaben, Adressen, Bewertungen, Kennzahlen oder Preise ohne Bestätigung.
- **Indexierung** (`indexable` in `seo.config.json`) bleibt `false`, bis Domain und Firmenangaben bestätigt sind.
- **Domain/DNS** nie ohne ausdrücklichen Auftrag umstellen.

## Technische Fallen

- `scripts/build.py` kopiert nur diese Ordner in die Ausgabe: `bilder fonts js kopf laune logos marke video` sowie `.js/.css/.png` im Hauptordner. Neue Asset-Ordner dort eintragen, sonst fehlen sie live.
- Neue Seiten brauchen einen Eintrag in `ROUTES` und `META` in `scripts/build.py`, sonst bekommen sie keine saubere Adresse und keine Metadaten.
- GitHub Pages cached rund 10 Minuten; zum Prüfen `?c=<zufall>` an die Adresse hängen.
