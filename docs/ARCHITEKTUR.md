# Seitenarchitektur — verbindlich ab 16.09.2026

Entschieden nach Auftrag des Auftraggebers („triff die Entscheidung, die bei mir Sinn macht").
Vorbild war HubSpot; übernommen wurde die **Struktur**, nicht der Massstab.

## Warum es eine Entscheidung brauchte

Auf der Seite lagen drei Ebenen nebeneinander, die aus verschiedenen Zeiten stammten
und nichts voneinander wussten:

| Ebene | Umfang | sichtbar in |
|---|---|---|
| Leistungsseiten (ursprünglich) | 5 Seiten, 695–1080 Wörter | nur im Klappmenü |
| Leistungsseiten (später ergänzt) | 6 Seiten, 302–695 Wörter | nur in der Fusszeile |
| Wissen | 8 Artikel, 446–1088 Wörter | Wissen-Übersicht |
| Blog | 6 Beiträge, 129–152 Wörter | Blog-Übersicht |

Das Menü zeigte fünf Leistungen, die Fusszeile acht andere. Wer „Leistungen" anklickte,
sah die SEO-Seite nie — obwohl sie mit 695 Wörtern so umfangreich ist wie Branding.

## Zielbild: zwei Ebenen

```
Startseite
├─ Leistungen ....... verkauft.   6 Seiten, alle im Menü, alle gleich gebaut
├─ Wissen ........... wird gefunden.   3 Themendächer, Leitfäden + Standpunkte
├─ Projekte ......... beweist
└─ Über uns · Kontakt ... schliesst ab
```

**Abo und Projektarbeit sind keine Leistungen**, sondern zwei Arten der Zusammenarbeit.
Sie bleiben in der Section „Abo oder Projekt?" auf der Startseite und im Klappmenü.

## Ebene 1 — Leistungen: sechs statt elf

Neun einzelne Leistungen sind zu viele fürs Menü, und zwei davon tragen keine eigene
Seite. Deshalb gruppiert. Die dünnen Seiten werden zu Abschnitten in einer starken
Seite, statt schwache Einzelseiten zu bleiben — es muss dafür nichts erfunden werden.

| Menüpunkt | Seite | nimmt auf |
|---|---|---|
| 01 Marke & Strategie | `branding/` | `kommunikationsstrategie/` (302 W.) |
| 02 Website | `webdesign/` | `website-betreuung/` (670 W.) als Abschnitt + Verweis |
| 03 Social Media & Content | `social-media/` | `content-creation/` (350 W.) |
| 04 Werbung | `performance-marketing/` | — |
| 05 Newsletter | `email-marketing/` | — |
| 06 SEO | `seo/` | eigene Seite: hohe Suchnachfrage, 695 Wörter vorhanden |

Aufgelöste Adressen bekommen Weiterleitungen. Das Klappmenü braucht für Eintrag 06
ein sechstes Vorschaubild und einen sechsten Textblock — sonst zeigt es beim
Überfahren nichts an (`bewegung.js` koppelt über die Position im Array).

## Ebene 2 — Wissen: ein Bereich, zwei Textsorten

**Der Blog wird nicht gelöscht, aber er wird kein eigener Bereich.** Zwei
Inhaltsbereiche nebeneinander sind bei 14 Artikeln nicht zu rechtfertigen; sie waren
genau die dritte Ebene, die das Durcheinander erzeugt hat.

Adresse bleibt `/wissen/`. `/blog/` leitet dorthin weiter.

- **Leitfäden** — lang, zeitlos, beantworten Suchfragen. Bringen die Sichtbarkeit.
- **Standpunkte** — kurz, datiert, mit Haltung. Bringen die Unterscheidbarkeit.
  Das ist das Eigenständigste, was auf der Seite steht, und bleibt erhalten.

### Drei Themendächer

```
wissen/
├─ Website ............ Hauptartikel + website-kosten-schweiz, website-erstellen-lassen,
│                        website-relaunch-checkliste, website-pflege-checkliste
├─ Social Media ....... Hauptartikel + social-media-kosten
└─ Werbung & Budget ... Hauptartikel + marketingbudget-kmu, google-ads-budget,
                         branding-kosten
```

Je Dach ein Hauptartikel von 1500–2500 Wörtern — nicht HubSpots 5000. Ein
Redaktionsteam gegen eine Person; der Massstab wird nicht übernommen.

### Die sechs Standpunkte und ihr Dach

| Beitrag | Wörter | Dach | verweist auf |
|---|---|---|---|
| Warum kluge Marken schneller wachsen | 129 | Marke | `branding/` |
| Wie viel Marke braucht ein Start? | 152 | Marke | `branding/`, `branding-kosten` |
| Wie grosse Marken den Wettbewerb gewinnen | 143 | Marke | `branding/` |
| Rhythmus schlägt Kampagne | 141 | Social Media | `social-media/`, `marketing-abo/` |
| Der echte Grund, warum Marken vorne bleiben | 132 | Social Media | `marketing-abo/` |
| Woran man eine Website misst | 135 | Website | `webdesign/`, `website-kosten-schweiz` |

## Verlinkung: die Regel

Gemessen an HubSpots Leitfaden (34 eindeutige Ziele, Sprungmarken herausgerechnet):
**50 % der Verweise gehen seitwärts auf Geschwister-Artikel**, 35 % auf Verkaufs- und
Angebotsseiten, der Rest auf Autor und Übersichten.

Die Verlinkung entsteht also **innerhalb** der Wissensebene, nicht zwischen den Ebenen.
Daraus die Regel für jeden neuen Artikel:

1. **nach oben** — ein Verweis auf den Hauptartikel des Dachs
2. **seitwärts** — zwei bis vier Verweise auf Geschwister im selben Dach
3. **hinauf zur Leistung** — ein bis zwei Verweise dorthin, wo der Leser die Arbeit
   abgeben kann. Nicht mehr: der Artikel soll helfen, nicht verkaufen.

Jede Leistungsseite verweist umgekehrt auf zwei bis vier Artikel ihres Dachs.

## Was bewusst nicht übernommen wird

- **Umfang.** 4992 Wörter und 16 Bilder je Artikel sind die Leistung eines
  Redaktionsteams.
- **Eigene Kennzahlen und Fallstudien.** „200× mehr Leads" sind HubSpots Daten.
  Ohne freigegebene Projektzahlen wird nichts dergleichen behauptet.
- **Mengen-SEO.** HubSpot verkauft Software an Zehntausende. Hier zählen zehn bis
  zwanzig Schweizer KMU im Jahr, also Suchen mit Kaufabsicht
  („Social Media Agentur Zürich") statt Reichweitenbegriffe („Social-Media-Marketing").

## Reihenfolge

1. Leistungsebene zusammenführen — sechs Seiten, ein Menü
2. Wissensebene zusammenführen — Standpunkte nach `/wissen/`, `/blog/` weiterleiten
3. Autor und Aktualisierungsdatum ergänzen (sichtbar und in den strukturierten Daten)
4. „Kurze Antwort"-Kasten je Leitfaden
5. Die drei Hauptartikel schreiben
6. Erst danach Freigabe zur Indexierung

Solange `indexable:false` gilt, bringt kein Artikel Besucher. Aufräumen zuerst kostet
am wenigsten und behebt am meisten.

## Offen, weil Entscheidung des Auftraggebers

- **Lead-Magnet / Formularempfang.** Alle Formulare öffnen heute nur ein Mailprogramm
  (`action="mailto:"`), es wird nichts empfangen oder gespeichert. Eine E-Mail-Abfrage
  vor einem Download würde ins Leere laufen. Braucht einen kostenpflichtigen Dienst
  und eine neue Datenschutzseite — der heutige Satz „Es findet keine Übermittlung an
  einen Server dieser Website und keine Speicherung statt" wird damit falsch.
- **Autorenname.** Der Vorname steht bereits sichtbar auf der Seite („Gründer"). Eine
  Autorenzeile unter Artikeln ist trotzdem eine eigene Freigabe.
- **GmbH-Angabe** in der Fusszeile von 40 Seiten — bleibt vorerst unverändert
  (ausdrückliche Anweisung vom 16.09.2026).
