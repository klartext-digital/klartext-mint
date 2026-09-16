# Seitenarchitektur — verbindlich ab 16.09.2026

Entschieden nach Auftrag des Auftraggebers („triff die Entscheidung, die bei mir Sinn
macht"). Vorbild war HubSpot; übernommen wurde die **Struktur**, nicht der Massstab.

> **Fassung 2.** Die erste Fassung legte die Inhalte unter `/wissen/` zusammen, mit der
> Begründung, zwei Bereiche lohnten sich bei 14 Artikeln nicht und man baue keine
> Struktur um eine Tätigkeit, die nicht stattfindet. Der Auftraggeber hat ergänzt, dass
> laufend neue Beiträge entstehen sollen. Damit ist die zweite Hälfte der Begründung
> hinfällig — und der Schluss daraus ebenfalls. Bei stetigem Wachstum ist der Blog der
> tragende Bereich, nicht der Anhang.

## Warum es eine Entscheidung brauchte

Drei Ebenen lagen nebeneinander, aus verschiedenen Zeiten und ohne Verbindung:

| Ebene | Umfang | sichtbar in |
|---|---|---|
| Leistungsseiten (ursprünglich) | 5 Seiten, 695–1080 Wörter | nur im Klappmenü |
| Leistungsseiten (später ergänzt) | 6 Seiten, 302–695 Wörter | nur in der Fusszeile |
| Wissen | 8 Leitfäden, 446–1088 Wörter | Wissen-Übersicht |
| Blog | 6 Standpunkte, 129–152 Wörter | Blog-Übersicht |

Das Menü zeigte fünf Leistungen, die Fusszeile acht andere.

## Zielbild: zwei Ebenen

```
Startseite
├─ Leistungen ....... verkauft.      6 Seiten, alle im Menü, alle gleich gebaut
├─ Blog ............. wird gefunden. 3 Themendächer, Leitfäden + Standpunkte
├─ Projekte ......... beweist
└─ Über uns · Kontakt ... schliesst ab
```

**Abo und Projektarbeit sind keine Leistungen**, sondern zwei Arten der Zusammenarbeit.
Sie bleiben in der Section „Abo oder Projekt?" und im Klappmenü.

## Ebene 1 — Leistungen: sieben statt elf

Neun einzelne Leistungen sind zu viele fürs Menü, zwei davon tragen keine eigene Seite.
Die dünnen werden Abschnitte in einer starken Seite — dafür muss nichts erfunden werden.

| Menüpunkt | Seite | nimmt auf |
|---|---|---|
| 01 Marke & Strategie | `branding/` | `kommunikationsstrategie/` (302 W.) |
| 02 Website | `webdesign/` | — |
| 07 Website-Betreuung | `website-betreuung/` | eigene Seite statt Abschnitt, siehe unten |

**Korrektur vom 17.09.2026 — Website-Betreuung bleibt eigenständig.** Die Tabelle oben
sah ursprünglich vor, `website-betreuung/` als Abschnitt in `webdesign/` einzuarbeiten.
Das war entschieden, bevor die Überschriften der Zielseite vorlagen. `webdesign/` deckt
mit „Inhalte pflegen und Verantwortung klären", „Suchmaschinenoptimierung als technische
Grundlage" und „Danach geht die Arbeit weiter" das Thema bereits ab und ist mit 1077
Wörtern die längste Leistungsseite; 656 Wörter zusätzlich hätten eine Seite ergeben, die
Projekt, Pflege und SEO gleichzeitig sein will. Website-Betreuung ist eine laufend
nachgefragte Leistung mit eigenem Suchbegriff und steht deshalb als Eintrag 07 im Menü.

Damit hat das Menü sieben statt sechs Einträge. Die Begründung „neun sind zu viele"
bleibt gültig, sieben sind vertretbar — der Unterschied ist, dass keine Seite mit
eigener Suchnachfrage in einer anderen verschwindet.
| 03 Social Media & Content | `social-media/` | `content-creation/` (350 W.) |
| 04 Werbung | `performance-marketing/` | — |
| 05 Newsletter | `email-marketing/` | — |
| 06 SEO | `seo/` | eigene Seite: hohe Suchnachfrage, 695 Wörter vorhanden |

Das Klappmenü braucht für Eintrag 06 ein **sechstes Vorschaubild und einen sechsten
Textblock** — `bewegung.js` koppelt Liste und Vorschau über die Position im Array
(`bilder.forEach((b,k)=>b.classList.toggle('ist', k===i))`). Fehlt der Index, bleibt die
Vorschau beim Überfahren leer. Kein Fehler, aber sichtbar kaputt.

Der Menüblock steht **handgeschrieben in 41 Quelldateien**, der Build erzeugt ihn nicht.
Zwei neue Einträge heisst 41 Dateien — nur per Skript, und der Verweis-Vorsatz ist je
Datei auszulesen (`''` bei 2, `'../'` bei 31, `'../../'` bei 8 Dateien).

## Ebene 2 — Blog: ein Bereich, zwei Textsorten, drei Dächer

Adresse ist `/blog/`. Die acht Leitfäden ziehen von `/wissen/` dorthin, `/wissen/`
leitet weiter.

**Wie der Umzug technisch läuft — am 17.09.2026 an einer Kopie erprobt.** Der Schlüssel
in `page-meta.json` ist **zugleich Quellort und Route**; der Build leitet die Quelldatei
daraus ab (`ROUTES[route+'index.html'] = route`). Eine Route lässt sich also nicht
umbiegen, ohne die Datei mitzunehmen — der erste Versuch endete in einem
`FileNotFoundError`.

Die Lösung ist ein **Ordner-Umzug**: `wissen/<x>/index.html` → `blog/<x>/index.html`.
Beide liegen zwei Ebenen tief, also bleiben alle Pfade in den Dateien gültig — 475
`../../`-Verweise über acht Dateien müssen **nicht** angefasst werden. Ein Umzug in die
flache Form `blog/<x>.html` würde sie alle brechen.

Zu erledigen sind dabei: die acht `page-meta`-Schlüssel umbenennen, eingehende Verweise
umbiegen (zehn Dateien), `ALIASES` für die alten Adressen, und die Wissens-Übersicht
auflösen. Der Kartengenerator muss zusätzlich `blog/*/index.html` durchsuchen — als
Ordner wären die Leitfäden sonst unsichtbar in der Übersicht.

**Warum der Blog der tragende Bereich wird und nicht das Wissen:** Die Blog-Übersicht
ist bereits das bessere Gerüst — echte Karten mit Datum, Lesezeit, Anriss und
Kontaktblock. Die Wissens-Übersicht hat 141 Wörter und zwei Aufzählungslisten. Für ein
wachsendes Archiv ist die Blog-Seite die brauchbare Vorlage.

- **Leitfäden** — lang, zeitlos, beantworten Suchfragen. Bringen die Sichtbarkeit.
- **Standpunkte** — kurz, datiert, mit Haltung. Bringen die Unterscheidbarkeit. Das ist
  das Eigenständigste auf der Seite und bleibt erhalten.

### Drei Themendächer

```
blog/
├─ Website ............ Hauptartikel + website-kosten-schweiz, website-erstellen-lassen,
│                        website-relaunch-checkliste, website-pflege-checkliste,
│                        woran-man-eine-website-misst
├─ Marke .............. Hauptartikel + branding-kosten, kluge-marken-wachsen,
│                        marke-am-anfang, wettbewerb-gewinnen
└─ Social & Budget .... Hauptartikel + social-media-kosten, marketingbudget-kmu,
                         google-ads-budget, rhythmus-statt-kampagne, vorne-bleiben
```

Je Dach ein Hauptartikel von 1500–2500 Wörtern — nicht HubSpots 4992. Ein
Redaktionsteam gegen eine Person; der Massstab wird nicht übernommen.

## Die Wachstumsbremse: die Übersicht wächst nicht mit

**Das ist wichtiger als der Ordnername.** Die sechs Karten stehen handgeschrieben in
`blog/index.html`; `build.py` erzeugt davon nichts. Jede Karte trägt von Hand gepflegt:
Lesezeit, Datum, Titel, Anriss, Autor, Bild. Bei 6 Beiträgen geht das, bei 30 driftet es
auseinander, bei 80 stimmt nichts mehr mit den Artikeln überein.

**Regel: Ein neuer Artikel ist eine Datei. Sonst nichts.**

Der Build erzeugt daraus Übersicht, Dach-Seiten und strukturierte Daten. Die Routen
entstehen bereits automatisch (`for p in sorted((ROOT/'blog').glob('*.html'))`) — es
fehlen nur Übersicht und Metadaten.

Dafür nötig:

1. **Datum maschinenlesbar im Artikel**: `<time datetime="2026-09-16">16. September 2026</time>`.
   Heute steht es als blosser Text und zusätzlich von Hand in der Übersichtskarte.
2. **Anriss und Lesezeit** aus dem Artikel ableiten, nicht doppelt pflegen.
3. **Kartenbild** aus `page-meta.json` (`image`) — die Leitfäden haben dort bereits
   eines. Kein neues Bildmaterial nötig.
4. **Article-Schema für Blogbeiträge**: heute ist `is_article` nur für
   `wissen/website-kosten-schweiz/` und `page-meta`-Seiten wahr. Die sechs Standpunkte
   haben deshalb **keine** Artikel-Auszeichnung und alle dasselbe Vorschaubild
   (`dienst-3.jpg` als Rückfallwert).

### Datumsquelle

**Korrektur vom 17.09.2026.** Die Angabe unten, die Git-Historie sei die ehrliche
Datumsquelle, ist falsch und wurde zurückgenommen. Der Menü-Umbau vom 17.09. hat jede
Datei berührt; „zuletzt geändert" zeigt seither für alle acht Leitfäden denselben Tag.
Und bei den Standpunkten widerspricht Git der Redaktion ohnehin: Chip sagt Dez 2025,
erster Commit sagt Aug 2026. Die Chip-Daten sind die redaktionellen.

Die Leitfäden haben **kein** Datum, und es wird keines erfunden. Gemessen am 17.09.2026:
Eine Karte ohne Datum hält — die Kartenhöhe kommt aus dem Raster (`.lese` mit
`grid-template-rows:1fr auto`), die Meta-Zeile trägt dann nur die Lesezeit. Ohne
Personenzeile schrumpft der Abstand zwischen Anriss und Bild von 103 auf 45 px, statt
eine Lücke zu lassen. **Damit hängt Schritt 3 nicht mehr an Schritt 4.**

Zur Einordnung die Git-Daten, ausdrücklich nicht als Veröffentlichungsdatum:

| Gruppe | angelegt | zuletzt geändert |
|---|---|---|
| sechs Standpunkte | 12.08.2026 | 08.09.2026 |
| Leitfäden | 15.–16.09.2026 | 16.09.2026 |

Angezeigt wird „Aktualisiert", wie bei HubSpot — das ist belegbar und altert besser als
ein Veröffentlichungsdatum.

## Verlinkung: die Regel

Gemessen an HubSpots Leitfaden, Sprungmarken herausgerechnet: 34 eindeutige Ziele,
davon **50 % seitwärts auf Geschwister-Artikel**, 35 % auf Verkaufs- und Angebotsseiten,
der Rest Autor und Übersichten.

Die Verlinkung entsteht also **innerhalb** der Blogebene, nicht zwischen den Ebenen.
Daraus für jeden Artikel:

1. **nach oben** — ein Verweis auf den Hauptartikel seines Dachs
2. **seitwärts** — zwei bis vier Verweise auf Geschwister im selben Dach
3. **zur Leistung** — ein bis zwei Verweise dorthin, wo der Leser die Arbeit abgeben
   kann. Nicht mehr: der Artikel soll helfen, nicht verkaufen.

Jede Leistungsseite verweist umgekehrt auf zwei bis vier Artikel ihres Dachs.

## Was bewusst nicht übernommen wird

- **Umfang.** 4992 Wörter und 16 Bilder je Artikel sind die Leistung eines Teams.
- **Eigene Kennzahlen und Fallstudien.** „200× mehr Leads" sind HubSpots Daten.
- **Mengen-SEO.** HubSpot verkauft an Zehntausende. Hier zählen zehn bis zwanzig
  Schweizer KMU im Jahr: Suchen mit Kaufabsicht („Social Media Agentur Zürich") statt
  Reichweitenbegriffe („Social-Media-Marketing").

## Reihenfolge

1. Leistungsebene zusammenführen — sieben Seiten, ein Menü ✔ erledigt 17.09.2026
2. Übersicht vom Build erzeugen lassen — **vor** dem Umzug, sonst wird Handarbeit
   verschoben statt beseitigt
3. Leitfäden nach `/blog/`, `/wissen/` weiterleiten (je eine Zeile in `ALIASES`)
4. Datum maschinenlesbar, Article-Schema für alle Beiträge
5. „Kurze Antwort"-Kasten je Leitfaden
6. Die drei Hauptartikel schreiben
7. Erst danach Freigabe zur Indexierung

Solange `indexable:false` gilt, bringt kein Artikel Besucher. Aufräumen zuerst kostet am
wenigsten und behebt am meisten. Die Weiterleitungen sind HTML-Umleitungen, keine echten
301er — GitHub Pages kann das nicht. Auf dem Zielhosting müssen echte 301er gesetzt
werden.

## Offen, weil Entscheidung des Auftraggebers

- **Autorenzeile.** Die Blog-Karten schreiben Beiträge heute **Pia** und **Reto** zu,
  während der Build dieselben Personen als unbestätigt kennzeichnet
  („Teamdarstellung im Entwurf: Namen, Rollen und Zugehörigkeit sind noch zu
  bestätigen"). Bis das geklärt ist: keine Autorenzeile ausbauen, kein Person-Schema.
  HubSpots Autorenseite ist ein starkes Vertrauenssignal — aber nur mit echten Personen.
- **Lead-Magnet / Formularempfang.** Alle Formulare öffnen nur ein Mailprogramm
  (`action="mailto:"`); es wird nichts empfangen oder gespeichert. Eine E-Mail-Abfrage
  vor einem Download liefe ins Leere. Braucht einen kostenpflichtigen Dienst und eine
  neue Datenschutzseite — der heutige Satz „Es findet keine Übermittlung an einen Server
  dieser Website und keine Speicherung statt" wird damit falsch.
- **GmbH-Angabe** in der Fusszeile von 40 Seiten — bleibt vorerst unverändert
  (ausdrückliche Anweisung vom 16.09.2026).
