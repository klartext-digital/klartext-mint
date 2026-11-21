# Brief: Blogartikel für klartext-digital.ch (Projekt klartext-mint)

Projektordner: dieses Repo (klartext-mint). Erstellt 21.11.2026 für den Blog-Ausbau (10 Leitfäden).
Ziel: SEO der Domain stärken. Jeder Artikel beantwortet eine echte Suchfrage von KMU in der
Deutschschweiz (Schwerpunkt Region Basel und Aargau) gründlich, praktisch und belegt.

## Was du lieferst

Pro Artikel GENAU eine neue Datei `blog/<slug>/index.html`. Sonst nichts im Projekt ändern
(kein page-meta.json, kein build, kein git, keine anderen Dateien, nichts löschen).

## Vorlage (Pflicht)

1. Kopiere `blog/unternehmenswebsite-leitfaden/index.html` vollständig als Ausgangspunkt
   (Kopf, Menü, Fusszeile bleiben byte-gleich; alle Pfade `../../` stimmen, weil gleiche Tiefe).
2. Ersetze nur:
   - `<title>…</title>` durch deinen Titel (siehe unten)
   - den gesamten Inhalt zwischen `<main>` und `</main>`
   - falls im `<head>` eine description steht: durch deine Beschreibung
3. Aufbau innerhalb von `<main>` exakt nach dem Muster der Vorlage:
   - Hero-Block (`<div class="hero hero--portraet" data-hero>` … ) mit Zurück-Link
     `<a class="zurueck" href="../">…Alle Artikel…</a>`, `<h1 class="seo-h1 unter__gross unter__gross--artikel">Titel<i class="punkt">.</i></h1>`
     (H1 ohne Schlusspunkt im Text; der Punkt kommt aus `<i class="punkt">.</i>`. Endet der Titel
     mit „?“, dann KEIN punkt-Element), eine kurze `<p class="brush">`-Zeile (max. 6 Wörter),
     `<figure class="unter__motiv" data-rein><img sizes="(max-width: 1100px) 1px, 62vw" src="../../bilder/<BILD>" alt="" fetchpriority="high" decoding="async"></figure>`
     und ein Einstiegsabsatz in `unter__text`.
   - `<article class="artikel seo-prose">` mit:
     - `<p class="seo-antwort"><strong>Kurze Antwort:</strong> …</p>` (2 bis 4 Sätze, beantwortet die Suchfrage direkt)
     - 6 bis 9 `<h2>`-Abschnitte, Listen wo sinnvoll, genau eine `<p class="seo-lesetipp">`
     - einen Abschnitt `<h2>Checkliste</h2>` als `<ul>`
     - den FAQ-Block mit 4 Fragen, Markup 1:1 wie in der Vorlage (`fragen fragen--eingebettet fragen--wie-start`, `frage`, `frage__kopf`, `frage__huelle`, …)
     - `<h2>Quellen und Vertiefung</h2>` mit Links zu den Primärquellen (siehe unten)
     - `<h2>Euer nächster Schritt</h2>` mit 1 bis 2 Absätzen
     - zum Schluss eine Weiterlesen-Leiste genau wie in `blog/google-unternehmensprofil/index.html`
       (`<nav class="weiterlesen" aria-label="Weiterlesen">` mit 2 bis 3 `weiter__karte`, Art „Leitfaden“)
   - KEINEN Knopf `<a class="knopf …">` im Artikel. Kontakt läuft über Kopfleiste und Fusszeile.

## Umfang und SEO

- 1300 bis 1900 sichtbare Wörter im `<main>` (Hauptartikel `seo-fuer-kmu`: 1900 bis 2400).
- Hauptkeyword im Titel, in der H1, im ersten Absatz und in einer H2. Natürlich schreiben, kein Keyword-Stopfen.
- Nebenkeywords und Fragen in H2 und FAQ aufgreifen (so, wie Leute bei Google fragen).
- Interne Links (relativ, Ordnerform mit Schrägstrich am Ende):
  - 1 Link nach oben zum Hauptartikel des Themas
  - 2 bis 4 seitwärts zu passenden Artikeln
  - 1 bis 2 zur passenden Leistungsseite, im Fliesstext (kein Knopf)
- Regionalbezug natürlich einbauen, wo er passt (Basel, Baselland, Aargau, Deutschschweiz), nicht in jedem Absatz.

## Sprache und Stil (streng)

- Schweizer Hochdeutsch: „ss“ statt „ß“, Anführungszeichen „…“.
- Leserinnen und Leser in der Mehrzahl duzen: „ihr“, „euch“, „eure“ (klein).
- **Keine Gedankenstriche** „–“ oder „—“ im Text. Umformulieren mit Doppelpunkt, Komma, Punkt.
  Zahlenbereiche als „10 bis 15“. Bindestriche in Wörtern (E-Mail, Social-Media-Beitrag) sind ok.
- Kurze, klare Sätze, konkrete Beispiele aus dem KMU-Alltag (Treuhand, Handwerk, Praxis, Gastro …).
- Kein Marketing-Geschwurbel, keine Superlative, keine Füllsätze („In der heutigen digitalen Welt…“).
- Haltung erlaubt, aber begründet.

## Nichts erfinden (streng)

- Keine Zahlen, Studien, Prozentwerte, Preise oder Zitate ohne überprüfte Quelle.
- Keine Aussagen über Kunden, Projekte, Ergebnisse oder Team von Klartext Digital. Keine Personennamen.
- Rechtliche Aussagen (Schweiz: UWG, DSG, Markenrecht) nur mit Link auf fedlex.admin.ch, edoeb.admin.ch,
  ige.ch o. ä. und vorsichtig formuliert („klärt im Zweifel mit einer Fachperson“).
- Plattform-Fakten (Google, Meta, LinkedIn, Gmail …) nur aus offiziellen Hilfeseiten/Dokumentation.
- **Jede Quelle selbst aufrufen (WebFetch/WebSearch) und prüfen**, dass die Seite existiert und die Aussage
  stützt. Lieber weniger Quellen als eine falsche. Bevorzugt deutsche Fassungen offizieller Seiten.

## Bestehende Artikel (für Links; Pfad relativ von blog/<slug>/ aus: `../<slug>/`)

| Slug | Titel | Thema |
|---|---|---|
| unternehmenswebsite-leitfaden | Die Unternehmenswebsite: der Leitfaden | Hauptartikel Website |
| website-kosten-schweiz | Website-Kosten Schweiz | Website |
| website-erstellen-lassen | Website erstellen lassen: Was muss vorher klar sein? | Website |
| website-relaunch-checkliste | Website-Relaunch: Was darf beim Wechsel nicht verloren gehen? | Website |
| website-pflege-checkliste | Website-Pflege: Checkliste | Website |
| website-die-arbeitet | Woran man eine Website misst (neu, wird gerade geschrieben) | Website/Kennzahlen |
| seo-fuer-kmu | SEO für KMU (neu, Hauptartikel SEO & Google) | SEO |
| lokale-seo | Lokale SEO (neu) | SEO |
| vorne-bleiben | Laufende SEO: bei Google vorne bleiben (neu) | SEO |
| google-unternehmensprofil | Google-Unternehmensprofil: So richtet ihr es richtig ein | SEO lokal |
| in-chatgpt-gefunden-werden | In ChatGPT gefunden werden: Wie funktioniert GEO? | KI-Suche |
| ki-im-marketing | KI im Marketing (neu) | KI |
| newsletter-kmu | Newsletter für KMU (neu) | E-Mail |
| rhythmus-statt-kampagne | Redaktionsplan Social Media (neu) | Social Media |
| social-media-kosten | Was kostet Social-Media-Betreuung? | Social Media |
| marketingbudget-kmu | Marketingbudget für KMU: Was muss in den Plan? | Budget |
| google-ads-budget | Google-Ads-Budget: Wie viel wofür einplanen? | Google Ads |
| branding-kosten | Was kostet ein Branding? | Marke |
| wettbewerb-gewinnen | Positionierung (neu) | Marke |
| marke-am-anfang | Markenaufbau beim Start (neu) | Marke |
| kluge-marken-wachsen | Markensystem und Corporate Design (neu) | Marke |

Hauptartikel je Thema: Website → `unternehmenswebsite-leitfaden`, SEO/Google/KI-Suche → `seo-fuer-kmu`,
Marke → `branding-kosten`, Social/E-Mail/Budget → `marketingbudget-kmu`.

## Leistungsseiten (Pfad von blog/<slug>/ aus)

`../../seo/` SEO · `../../webdesign/` Webdesign · `../../website-betreuung/` Website-Betreuung ·
`../../social-media/` Social Media · `../../email-marketing/` Newsletter & E-Mail ·
`../../performance-marketing/` Google & Meta Ads · `../../branding/` Branding · `../../marketing-abo/` Marketing im Abo

## Rückmeldung an mich (pro Artikel)

- Slug, Titel für `<title>` (inkl. „ | Klartext Digital“, gesamt höchstens 60 Zeichen)
- Meta-Beschreibung (120 bis 155 Zeichen, ohne Gedankenstrich)
- Kartentitel (label), ca. 40 bis 60 Zeichen
- Wortzahl im `<main>`
- Liste der Quellen-URLs, jeweils mit „geprüft: ja“
- Hinweise auf Aussagen, bei denen du unsicher bist

## Nach dem Schreiben (Einbau)

- Eintrag in `page-meta.json`: `title`, `description`, `label`, `"article": true`, `image`, optional `rang` (Reihenfolge in der Übersicht).
- Titelbild braucht WebP-Fassungen in `bild-varianten.json`.
- Build, Check, Sichtprüfung 320 bis 1920 px, Quellen-Links per curl prüfen (Facebook-Hilfe blockt Abrufe, im Browser prüfen).
- Vor dem Publizieren: `grep 'class="knopf' blog/*/index.html` im `<main>` muss leer sein, keine „–“/„—“.
