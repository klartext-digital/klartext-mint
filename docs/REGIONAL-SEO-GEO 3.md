# Regionale Sichtbarkeit: SEO und GEO

Stand: 14. Oktober 2026. Entscheid des Auftraggebers: **regional starten**, Fokus
**Basel, Baselland, Aargau**, Sitz Lohagstrasse 15, 4133 Pratteln. National später.

Grundregel: Ein Punkt gilt erst als erledigt, wenn der **Nachweis** vorliegt
(Search Console, Bing Webmaster Tools, Live-Abruf). „Code eingebaut“ ist kein Nachweis.

## 1. Fundament

| Punkt | Status | Nachweis / Voraussetzung |
|---|---|---|
| Fusszeile, Über uns, Impressum auf Pratteln statt Zürich | erledigt 14.10. | Vorschau, alle 38 Seiten |
| Seitentitel und Beschreibungen regional (siehe `KEYWORD-MAP.csv`) | erledigt 14.10. | Vorschau-Quelltext |
| Steckbrief `ProfessionalService` mit Adresse und Einzugsgebiet (Quelle: `seo.config.json` → `business`) | erledigt 14.10. | Rich-Results-Test nach Livegang |
| `llms.txt` für KI-Suchen | erledigt 14.10. | wirkt erst an der Wurzel von klartext-digital.ch |
| Telefonnummer (Fusszeile zeigt Platzhalter) | **offen: Dusan** | Nummer bestätigen oder Feld entfernen |
| Geschäftszeiten: Website Mo–Fr 08:30–18:00, Google-Profil Mo–Fr 08:00–20:00 | **offen: Dusan** | eine Angabe für beide Orte festlegen |
| „in Gründung“ entfernen, UID und Handelsregister ins Impressum, `legalName` ins Schema | wartet auf HR-Eintrag | Zefix-Eintrag |
| **Livegang auf klartext-digital.ch** (DNS, `indexable`, Sitemap) | **wartet auf ausdrücklichen Auftrag** | MX-Einträge (Google Workspace) nie anfassen |

## 2. Google (lokal)

| Punkt | Status | Nachweis |
|---|---|---|
| Google-Unternehmensprofil angelegt (Konto dusan@klartext-digital.ch) | erledigt 14.10. | Status „Bestätigung erforderlich“ |
| Profil per Video bestätigen (Briefkastenschild) | offen: Dusan, sobald Schild hängt | Profil „Bestätigt“ |
| Website-Adresse im Profil eintragen | nach Livegang | |
| Nebenkategorien: Marketingbüro, Werbeagentur, Webdesigner | offen | |
| Bewertungen echter Kunden einholen (Link aus dem Profil) | nach Bestätigung | Anzahl im Profil |
| Sitemap einreichen, Hauptseiten zur Indexierung beantragen | nach Livegang | Search Console: Seitenindexierung |

## 3. Bing und KI-Suchen (GEO)

ChatGPT sucht über Bing, Gemini und die KI-Übersichten über Google, Perplexity
über einen eigenen Index plus Bing. Ohne Bing-Eintrag findet ChatGPT die Seite kaum.

| Punkt | Status | Nachweis |
|---|---|---|
| Bing Webmaster Tools: Import aus der Search Console | nach Livegang; Anmeldung macht Dusan | Bing: indexierte Seiten |
| IndexNow für schnelle Meldung neuer Seiten | nach Livegang | |
| Identische Angaben in Verzeichnissen: local.ch, search.ch, LinkedIn-Unternehmensseite, Instagram-Bio | offen | gleicher Name, gleiche Adresse überall |
| Zefix / Moneyhouse | automatisch nach HR-Eintrag | |
| `sameAs` im Schema mit den echten Profil-Links | sobald Profile existieren | Fusszeilen-Links zeigen heute auf `#` |
| Erwähnungen Dritter: Kundenseiten („Website von Klartext Digital“), regionale Medien, Wirtschaftskammer Baselland, Gewerbeverein Pratteln | offen | Liste der Fundstellen |
| Echte Fallstudien mit Zahlen aus der Region | offen | |

## 4. Regionale Seiten (Vorschlag, braucht Freigabe)

Das Google-Profil in Pratteln trägt in der Kartensuche für Basel und Baselland. Für den
**Aargau** reicht es nicht: dort braucht es eine eigene Seite mit echtem Bezug
(Referenzen aus dem Aargau, z. B. Grand Casino Baden). Je eine Seite pro Region nur mit
eigenem Inhalt, keine austauschbaren Ortsseiten. Laut `ARCHITEKTUR.md` braucht jede neue
Seite einen Platz im Menü, darum erst nach Freigabe.

## 5. Monatliche Messung

Jeden Monat dieselben Prüfungen, Ergebnisse unten anhängen:

1. Search Console und Bing: indexierte Seiten, Klicks, Impressionen
2. Position für die Hauptbegriffe: Marketingagentur Basel, Marketingagentur Baselland,
   Marketingagentur Aargau, Webdesign Basel, Webdesign Aargau, Social Media Agentur Basel,
   SEO Agentur Basel, Google Ads Agentur Basel, Werbeagentur Pratteln, Marketingagentur Pratteln
3. KI-Test, dieselben Fragen an ChatGPT, Perplexity und Gemini; notieren, ob klartext genannt wird:
   - Welche Marketingagentur in der Region Basel empfiehlst du für ein KMU?
   - Gute Webdesign-Agentur im Aargau?
   - Wer macht Social Media für Firmen in Baselland?
   - Marketingagentur in Pratteln?
4. Google-Profil: Aufrufe, Anrufe, Routen, Bewertungen

### Messprotokoll

| Monat | Indexiert (G / B) | Top-Begriffe | KI nennt klartext | Bewertungen |
|---|---|---|---|---|
| Okt. 2026 | 0 / 0 (Domain zeigt Parkseite) | keine | nein | 0 |
