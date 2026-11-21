# Livegang auf klartext-digital.ch

Neu geschrieben am 21.11.2026 (vorher: Hostinger-Variante vom 15.10.2026).
**Startet nur mit ausdrücklichem Auftrag „Livegang“ vom Auftraggeber.**

## Ausgangslage (gemessen 21.11.2026)

- **DNS zeigt bereits auf GitHub Pages:** A `@` → 185.199.108.153 / .109 / .110 / .111,
  `www` → CNAME `klartext-digital.github.io`. **Am DNS muss nichts geändert werden.**
- **Mail:** MX `smtp.google.com` (Google Workspace). MX-, SPF- und
  google-site-verification-Einträge **nie anfassen**.
- Auf der Domain läuft heute die „Bald“-Seite aus dem Repo `klartext-digital/klartext-bald`
  (GitHub Pages, Quelle `main`, CNAME `klartext-digital.ch`, noindex).
- Diese Seite (`klartext-mint`) läuft als Vorschau unter
  https://klartext-digital.github.io/klartext-mint/ (Quelle `gh-pages`, noindex).
- Der Livegang ist im Code vorbereitet, aber gesperrt: `scripts/release_policy.py`
  öffnet erst bei `"launch_approved": true` in `seo.config.json`. Dann schreibt der
  Build die Datei `CNAME`, lässt `schrifttest.html` weg, und `check.py` prüft
  Indexierung und Canonicals gegen die echte Domain. Probelauf am 21.11.2026: PASS,
  41 Seiten in der Sitemap.

## Vorher klären

- [ ] Ausdrücklicher Auftrag „Livegang“
- [ ] Sechs kurze Blogbeiträge (je rund 120 bis 140 Wörter): `kluge-marken-wachsen`,
      `marke-am-anfang`, `rhythmus-statt-kampagne`, `vorne-bleiben`,
      `website-die-arbeitet`, `wettbewerb-gewinnen`. Empfehlung: zum Start **nicht**
      in `approved_paths` aufnehmen (bleiben erreichbar, aber noindex), bis sie
      ausgebaut sind. Dünne Seiten ziehen die Bewertung der ganzen Domain runter.
- [ ] Ausgeblendet bleiben (Abschnitt `ausblenden` in `seo.config.json`):
      Kundenlogos, Referenzvideos, Team
- [ ] MWST-Nummer da? Dann ins Impressum (`recht/impressum.html`)

## 1. Schalter umlegen (ein Commit auf `claude/livegang`)

In `seo.config.json`:

```json
"base_url": "https://klartext-digital.ch/",
"indexable": true,
"launch_approved": true,
"production_host": "GitHub Pages",
"approved_paths": [ ... ]
```

`approved_paths` = alle Routen ausser `marke.html`, `laune.html`, `takt.html` (und
ausser den dünnen Beiträgen, falls so entschieden). Liste erzeugen:

```sh
python3 -c "import json;m=json.load(open('docs/URL-MAP.json'));p='https://klartext-digital.github.io/klartext-mint/';print(json.dumps(sorted({v[len(p):] for v in m.values() if v.startswith(p)}-{'marke.html','laune.html','takt.html'}),ensure_ascii=False,indent=2))"
```

(Vor dem Umstellen ausführen, solange die URL-Map noch die Vorschau-Adressen enthält.)

Dann `python3 scripts/build.py` und `python3 scripts/check.py`. Kontrolle:
`_site/CNAME` enthält `klartext-digital.ch`, `robots` = `index, follow` auf den
freigegebenen Seiten, Canonicals und Sitemap zeigen auf `https://klartext-digital.ch/…`.
Pull Request, zusammenführen, `main` ziehen.

## 2. Domain von der „Bald“-Seite übernehmen

GitHub lässt eine Domain nur in **einem** Repo zu. Reihenfolge:

1. Im Repo `klartext-bald` die Domain lösen:
   `gh api -X PUT repos/klartext-digital/klartext-bald/pages -F cname=null`
   (oder Settings → Pages → Custom domain leeren). Die Datei `CNAME` dort danach löschen,
   sonst trägt der nächste Push die Domain wieder ein.
2. Sofort `python3 scripts/publish.py` in `klartext-mint` (schreibt `CNAME` nach gh-pages).
3. Domain im Pages-Setting von `klartext-mint` bestätigen und HTTPS erzwingen:
   `gh api -X PUT repos/klartext-digital/klartext-mint/pages -f cname=klartext-digital.ch`
   und danach `-F https_enforced=true` (das Zertifikat kann bis etwa eine Stunde brauchen).

Zwischen Schritt 1 und 2 zeigt die Domain wenige Minuten eine GitHub-404. Die Mail ist nicht betroffen.

## 3. Am selben Tag prüfen

- [ ] `https://klartext-digital.ch/` 200; `http://` und `www.` leiten mit 301 auf `https://klartext-digital.ch/`
- [ ] Alte Vorschau `https://klartext-digital.github.io/klartext-mint/` leitet auf die Domain
- [ ] Unbekannte Adresse liefert 404 mit eigener Fehlerseite
- [ ] `robots.txt`, `sitemap.xml`, `llms.txt` an der Wurzel erreichbar
- [ ] Sichtprüfung Computer und Handy (1440 / 390), keine Konsolenfehler
- [ ] Test-Mail an hallo@ kommt an
- [ ] Prüfen mit `?c=<zufall>`: GitHub Pages cached rund 10 Minuten

## 4. Anmelden und einreichen

- [ ] Search Console (Domain-Property bestätigt): Sitemap `https://klartext-digital.ch/sitemap.xml`
      einreichen, Startseite und Leistungsseiten per URL-Prüfung zur Indexierung beantragen
- [ ] Bing Webmaster Tools: aus Search Console importieren, Sitemap
- [ ] Google-Unternehmensprofil und Bing Places: Website eintragen
- [ ] Rich-Results-Test für Startseite und eine Leistungsseite
- [ ] PageSpeed Insights (Handy) für Startseite und eine Fallstudie, Werte hier eintragen

## 5. Danach

- Verzeichniseinträge nach `~/Desktop/02_KLARTEXT/Marke/Verzeichniseintraege.md`
- Neue Profile als `same_as` in `seo.config.json`
- Indexierung erst nach einigen Tagen bewerten; „Gefunden, nicht indexiert“ ist eine
  Warteschlange, kein Fehler. Ein guter Lighthouse-Wert heisst nicht „bei Google drin“.

## SEO-Prüfung „als wäre sie online“ (21.11.2026)

Testbau mit `base_url` klartext-digital.ch, alles freigegeben ausser Gestaltungsstudien.

**In Ordnung:**
- 41 Seiten, alle mit genau einem H1, Beschreibung, eigenem Canonical und strukturierten Daten
- Keine doppelten Titel oder Beschreibungen ausser der Testseite `schrifttest.html` (fällt beim Livegang weg)
- Alle Bilder mit Alt-Attribut, keine kaputten internen Links
- Firmendaten (ProfessionalService): Name, Adresse Pratteln, UID, E-Mail, Einzugsgebiet, Instagram
- `robots.txt` erlaubt Suchmaschinen und KI-Suchdienste, `llms.txt` mit Firmenangaben und Leistungen

**Behoben am 21.11.2026 (Ladezeit, gemessen Handy, 1,6 Mbit/s, 4-fach gedrosselte CPU):**

| Seite | LCP vorher | LCP nachher |
|---|---|---|
| Grand Casino Baden | 6,8 s | 3,4 s |
| PLÜ | 3,8 s | 2,4 s |
| Blog Website-Kosten | 3,5 s | 2,1 s |
| Red Bull, Layout-Springen (CLS) | 0,119 | 0,003 |
| Startseite, Datenmenge | 1,98 MB | 1,44 MB |

Massnahmen: Hintergründe als WebP, WebP-Fassungen für 23 Bilder mit gemessenen `sizes`,
Titelbild nicht mehr lazy, Pfadzeile einzeilig. Der Testserver komprimiert nicht;
GitHub Pages liefert CSS und HTML gzip-komprimiert aus, echte Werte liegen darunter.

**Offen (Empfehlung):**
- Die sechs kurzen Blogbeiträge ausbauen oder zum Start noindex lassen (siehe oben)
- Titel knapp über 60 Zeichen: Startseite (61), Leistungen (61), `vorne-bleiben` (62); unkritisch
- Logo in den Firmendaten ist SVG; ein PNG ab 112 × 112 px ist für Google sicherer
- Einige Originalfotos (z. B. `gcb-haus.jpg` 1280 px, `dienst-*` 1200 px) sind für
  Retina-Bildschirme bei voller Breite zu klein; nur mit grösseren Originalen lösbar
