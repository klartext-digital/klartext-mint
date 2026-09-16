# Zusammenarbeit an klartext-mint

Hier arbeiten zwei KI-Werkzeuge: **ChatGPT/Codex** und **Claude Code**. Diese Regeln gelten für beide.

## Ein einziger Weg zur Live-Seite

Öffentlich erreichbare Vorschau: https://klartext-digital.github.io/klartext-mint/

**Produktivstart pausiert (Auftraggeber, 16.09.2026):** Die GitHub-Vorschau darf weiter aktualisiert werden. Die finale Domain darf noch nicht live gehen. Der Agenturname könnte sich ändern. Keine Domain-Umschaltung, Indexfreigabe oder Sitemap-Einreichung ohne neuen ausdrücklichen Auftrag. `scripts/release_policy.py` begrenzt Bauen, Prüfen und Publizieren auf diese Vorschau mit `noindex`. Diese Sperre nicht allein aufgrund vollständiger Firmenangaben entfernen. Namenswechsel erst nach bestätigtem neuen Namen; siehe `docs/NAMENSWECHSEL.md`.

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
- **Indexierung** (`indexable` in `seo.config.json`) bleibt `false`, bis ein neuer ausdrücklicher Auftrag den Produktivstart freigibt. Domain- oder Firmenbestätigung allein genügt nicht.
- **Domain/DNS** nie ohne ausdrücklichen Auftrag umstellen.

## Seitenarchitektur — vor jeder neuen Seite lesen

**`docs/ARCHITEKTUR.md` ist verbindlich** (entschieden am 16.09.2026). Die Seite hat
**zwei Ebenen**: Leistungen verkaufen, Wissen wird gefunden. Mehr nicht.

- **Keine neue Seite ohne Platz im Menü.** Es sind zuletzt sechs Seiten entstanden, die
  nur in der Fusszeile standen — das Klappmenü zeigte fünf Leistungen, die Fusszeile
  acht andere. Wer eine Seite anlegt, trägt sie im selben Zug ins Klappmenü ein
  (`ndd__liste`, handgeschrieben in **38 der 41** Quelldateien — ohne Menü sind nur
  `laune.html`, `marke.html`, `takt.html`; der Pfad-Vorsatz hängt an der Tiefe:
  2× `''`, 28× `'../'`, 8× `'../../'`) **und** ergänzt Vorschaubild und
  Textblock — `bewegung.js` koppelt beides über die Position im Array, sonst bleibt die
  Vorschau beim Überfahren leer.
- **Kein dritter Inhaltsbereich.** Leitfäden und Standpunkte liegen beide unter
  `/blog/`, sortiert nach drei Themendächern. `/wissen/` leitet dorthin weiter.
- **Ein neuer Artikel ist eine Datei. Sonst nichts.** Die Übersicht in
  `blog/index.html` erzeugt seit 17.09.2026 der Build (`blog_karten_html()` in
  `scripts/build.py`) aus den Dateien in `blog/` — Lesezeit, Datum, Anriss, Person
  und Bild. Im Quelltext steht nur das leere Raster `lesegitter` mit einem Hinweis.
  **Was dort von Hand hineingeschrieben wird, verwirft der Build bei jedem Lauf**
  — lautlos. Genau das war bis zum 17.09.2026 der Fall: sechs alte Karten standen
  noch in der Quelle und hatten live keine Wirkung. Personenzuordnung kommt aus
  `blog-autoren.json`, nicht aus dem Markup.
- **Datum maschinenlesbar** im Artikel (`<time datetime="…">`), nicht als blosser Text
  und nicht zusätzlich in der Übersichtskarte. Keine Veröffentlichungsdaten erfinden —
  Quelle ist die Git-Historie, angezeigt wird „Aktualisiert".
- **Jede Leistungsseite ist vollständig gebaut:** Zurück-Knopf, Nummer, Abschluss mit
  „Weiter"-Block und Kontaktblock. Seiten, die nach dem Text einfach aufhören, gelten
  als unfertig.
- **Verlinkungsregel je Artikel:** einer nach oben zum Hauptartikel, zwei bis vier
  seitwärts zu Geschwistern, ein bis zwei zur passenden Leistung.

## Technische Fallen

- `scripts/build.py` kopiert nur diese Ordner in die Ausgabe: `bilder fonts js kopf laune logos marke video` sowie `.js/.css/.png` im Hauptordner. Neue Asset-Ordner dort eintragen, sonst fehlen sie live.
- Neue Ordnerseiten in `page-meta.json` aufnehmen; der Build übernimmt Routen und Metadaten daraus. Bestehende Legacy-Dateien bleiben über `ROUTES` und `META` in `scripts/build.py` zugeordnet.
- GitHub Pages cached rund 10 Minuten; zum Prüfen `?c=<zufall>` an die Adresse hängen.
