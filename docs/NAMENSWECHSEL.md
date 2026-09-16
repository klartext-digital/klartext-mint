# Namensentscheidung und Startpause

Stand: 16. September 2026. Der Auftraggeber erwägt wegen ähnlicher Agenturnamen einen Namenswechsel. Noch kein neuer Name bestätigt. Keine Aussage zur rechtlichen Verfügbarkeit geprüft oder getroffen.

## Verbindlicher Zwischenstand

- GitHub-Vorschau darf weiter aktualisiert werden; sie ist öffentlich erreichbar und trägt `noindex`.
- Finale Domain nicht mit der Website verbinden. Keine Indexfreigabe und keine Sitemap bei Google einreichen.
- Google-Inhaberbestätigung für klartext-digital.ch bleibt bestehen. Sie veröffentlicht keine Website.
- Bestehenden Namen, Referenzen und Gestaltung vorerst erhalten.

## Nach bestätigter Namensentscheidung gemeinsam umstellen

1. Namen, Schreibweise, Wortmarke und gegebenenfalls neue Domain bestätigen.
2. Wortmarken und Bilddateien in `marke/`, `logos/`, Social Cards sowie sichtbare Marken-/Kontakttexte inventarisieren.
3. Titel, Beschreibungen und strukturierte Daten in `page-meta.json`, `scripts/build.py` und den HTML-Quellen anpassen. Der Markenname steht derzeit an mehreren Stellen; diese sind noch nicht zentralisiert.
4. Erst bestätigte E-Mail-Adressen, Firmierung und öffentliche Betreiberangaben übernehmen. Keine Adressen aus einem neuen Namen ableiten.
5. Domain, Canonicals, Sitemap, Weiterleitungen und Search-Console-Property auf den dann freigegebenen Zielhost abstimmen. Alte Domain nicht automatisch weiterleiten.
6. Vorschau vollständig bauen, Links und Darstellung prüfen. `release_policy.py` erst mit ausdrücklichem Startauftrag auf den bestätigten Veröffentlichungsweg umstellen.

Ein neuer Name erfordert keine neue Seitenarchitektur: Leistungs- und Wissensadressen sind bereits vom Agenturnamen unabhängig.
