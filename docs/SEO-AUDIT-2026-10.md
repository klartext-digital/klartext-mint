# SEO- und GEO-Audit, Oktober 2026

Stand: 14.10.2026. Geprüft: alle 38 gebauten Seiten der Vorschau (Titel, Beschreibung,
H1/H2, Wortzahl, Bilder, strukturierte Daten), dazu eine Websuche zu Konkurrenz und
Suchbegriffen. Kein SEO-Werkzeug angebunden (Ahrefs/Semrush): Suchvolumen sind
Einschätzungen, keine Messwerte. Die Seite ist noch nicht indexiert, es gibt also
keine Rankings und keine Search-Console-Daten.

## Zusammenfassung

Technisch solide: saubere Adressen, Canonicals, Brotkrumen, FAQ- und Artikel-Daten,
schnelle statische Seiten, ausführliche Leistungsseiten (700 bis 1200 Wörter) und
neun Ratgeber. **Das grösste Hindernis ist nicht die Seite, sondern der fehlende
Livegang**: Unter klartext-digital.ch steht die Hostinger-Parkseite. Danach zählen
drei Dinge am meisten: Google-Profil bestätigen und Bewertungen sammeln,
Bing anmelden (ChatGPT sucht über Bing), und Platzhalter durch echte Belege ersetzen.

## Umgesetzt am 14.10.2026

| Punkt | Wirkung |
|---|---|
| Standortsatz im sichtbaren Text von Startseite und 9 Leistungsseiten | Region stand vorher nur im Titel, nie im Text |
| Steckbrief `Service` je Leistungsseite (Leistung + Anbieter + Einzugsgebiet) | Google/KI verknüpfen Leistung, Firma und Region |
| Öffnungszeiten im Steckbrief und in `llms.txt` | gleich wie Google-Profil |
| Beschreibungen über 160 Zeichen gekürzt (Social Media, Webdesign, SEO, Leitfaden) | werden bei Google nicht mehr abgeschnitten |
| Firmenname einheitlich „Klartext Digital“ | Markenkonsistenz für KI-Suchen |

## Befunde (offen)

| Seite | Befund | Schwere | Empfehlung |
|---|---|---|---|
| ganze Seite | Domain zeigt Parkseite, Vorschau `noindex` | Kritisch | Livegang (Auftrag Dusan) |
| ganze Seite | Banner „Entwurf · Texte, Namen und Zahlen sind Platzhalter“ | Kritisch beim Livegang | vor Livegang entfernen |
| Startseite, Über uns | Kundenstimmen und Team als „noch nicht bestätigt“ markiert | Hoch | nur echte Zitate/Personen zeigen, sonst entfernen; erfundene Belege schaden bei Google und KI |
| projekte/nordlicht, volta, meridian | je ~120 Wörter, keine Kundendaten prüfbar | Hoch | bestätigen, dass es echte Projekte sind, und ausbauen; sonst entfernen |
| 6 Kurz-Beiträge im Blog | 119 bis 142 Wörter, „dünner Inhalt“ | Mittel | ausbauen auf 600+ Wörter oder beim Livegang auf `noindex` |
| leistungen/, projekte/ | Übersichten mit ~90 Wörtern | Niedrig | je 2 bis 3 Sätze Einleitung |
| Fusszeile | Social-Links zeigen auf `#` | Mittel | echte Profile verlinken, dann `sameAs` im Steckbrief |
| Bilder | `alt=""` auf Leistungskarten | Pass | sind Schmuckbilder mit Text darüber, korrekt so |

## Suchbegriffe (Einschätzung, ohne Volumendaten)

| Suchbegriff | Schwierigkeit | Chance | Absicht | Zielseite |
|---|---|---|---|---|
| Marketingagentur Pratteln | leicht | hoch | kaufen | Startseite + Google-Profil |
| Werbeagentur Pratteln | leicht | hoch | kaufen | Startseite + Google-Profil |
| Webdesign Pratteln / Muttenz / Liestal | leicht | hoch | kaufen | Webdesign |
| Marketingagentur Baselland | mittel | hoch | kaufen | Startseite |
| Webdesign Basel | schwer | mittel | kaufen | Webdesign |
| Marketingagentur Basel | schwer | mittel | kaufen | Startseite |
| Social Media Agentur Basel | mittel | mittel | kaufen | Social Media |
| Google Ads Agentur Basel | mittel | mittel | kaufen | Performance |
| SEO Agentur Basel | schwer | mittel | kaufen | SEO |
| Marketingagentur Aargau | mittel | mittel | kaufen | später Regionsseite |
| Webdesign Aarau / Baden | mittel | mittel | kaufen | später Regionsseite |
| Was kostet eine Website Schweiz | mittel | hoch | informieren | Ratgeber vorhanden |
| Social Media Betreuung Kosten | mittel | hoch | informieren | Ratgeber vorhanden |
| Google Ads Budget KMU | mittel | mittel | informieren | Ratgeber vorhanden |
| In ChatGPT gefunden werden / GEO für KMU | leicht | hoch | informieren | **fehlt**: neuer Ratgeber |
| Google Unternehmensprofil einrichten | mittel | mittel | informieren | **fehlt**: neuer Ratgeber |
| Marketing outsourcen KMU | mittel | mittel | vergleichen | Marketing im Abo |

## Konkurrenz (Stichprobe aus der Websuche)

| Anbieter | Ort | Auffällig |
|---|---|---|
| Frascati GmbH | Oberwil BL | „für Basel und die ganze Nordwestschweiz“, **Festpreis ab CHF 2'900**, in Verzeichnissen (GoodFirms) gelistet |
| Gutzwiller Kommunikation und Design | Aarau | bietet **GEO** und Google-Profil-Betreuung ausdrücklich an |
| diffrent digital AG | Pratteln | direkter Nachbar, Grafik + Web |
| Kopf & Stift | Deutschland | eigene Landingpage „Webdesign Basel“ |

Lehre: Lokale Konkurrenten punkten mit **Verzeichniseinträgen** und **transparenten
Preisen**. GEO wird im Aargau schon verkauft, ein eigener GEO-Ratgeber ist ein
Unterscheidungsmerkmal.

## Massnahmenplan

**Diese Woche (schnell)**
1. Google-Profil per Video bestätigen, sobald das Briefkastenschild hängt (Dusan)
2. Kundenstimmen, Team und die drei Kurzprojekte prüfen: echt oder raus (Dusan entscheidet)
3. Social-Profile anlegen bzw. verlinken (Instagram, LinkedIn-Unternehmensseite)

**Beim Livegang**
4. Entwurfs-Banner entfernen, `indexable` freigeben, Sitemap einreichen
5. Bing Webmaster Tools (Import aus Search Console), IndexNow
6. Website im Google-Profil eintragen

**Dieses Quartal**
7. Verzeichnisse mit identischen Angaben: local.ch, search.ch, Sortlist, GoodFirms, Clutch
8. ✔ 14.10.2026: Ratgeber „In ChatGPT gefunden werden“ unter /blog/in-chatgpt-gefunden-werden/ (Dach Website, verlinkt von SEO-Seite und Hauptartikel)
9. ✔ 15.10.2026: Ratgeber unter /blog/google-unternehmensprofil/ (eigenes Motiv gbp-profil.jpg)
10. Bewertungen: nach jedem Projekt um eine Google-Bewertung bitten
11. Zwei echte Fallstudien mit Zahlen (z. B. Grand Casino Baden)
12. Erwähnungen: Gewerbeverein Pratteln, Wirtschaftskammer Baselland, Kundenseiten
