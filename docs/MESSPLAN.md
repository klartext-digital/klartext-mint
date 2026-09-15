# Messplan

## Heute tatsächlich implementiert

`messung.js`, `anfrage.js` und `kostenplan.js` lösen lokale `klartext:interaction`-Ereignisse aus. Es gibt keinen aktiven Analytics-Adapter, keine Analytics-Cookies und keinen Versand dieser Ereignisse. Die vorhandenen Speicherzugriffe des Ladeschirms bleiben davon unabhängig bestehen.

| Ereignis | Bedeutung | Kein Nachweis für |
|---|---|---|
| abo_explore / project_explore | Einstieg in ein Angebot | Anfrage |
| *_inquiry | Klick zum passenden Anfrageweg | Anfrageeingang |
| briefing_prepared | Besucher hat ein Briefing erzeugt | Versand oder Zustellung |
| mail_open | Klick zum Mailprogramm | Versand oder Zustellung |
| budget_calculated | Berechnung mit eigenen Beträgen | Budget oder Kaufabsicht |

Ereignisse enthalten nur einen festgelegten Namen, den Seitenpfad und beim Briefing `abo`, `projekt` oder `team`. Keine Freitexte, E-Mail-Adressen, eingegebenen Beträge, URL-Parameter oder Personennamen. Künftige Adapter müssen diese Begrenzung beibehalten.

## Für echte Messung noch erforderlich

1. Analytics-Konto/Anbieter festlegen und Zugang herstellen.
2. Datenschutz und erforderliche Einwilligungssteuerung mit tatsächlich verwendeten Diensten abstimmen.
3. Adapter erst nach entsprechender Freigabe laden. Bei einer Google-Integration Basic Consent Mode berücksichtigen: vor Zustimmung keine Übertragung.
4. Empfangendes Formular-Backend oder Terminbuchung anschliessen und Zustellung testen.
5. Erst eine bestätigte Zustellung darf als `lead_received` gezählt werden. Mailto-Klicks bleiben Hilfssignale.
6. Interne Tests auswertbar kennzeichnen und aus Geschäftsberichten ausschliessen.

## Rhythmus nach Produktivstart

Wöchentlich: Indexierungsfehler, wichtige Zielseiten, Anfragen und Zustellung. Monatlich: Suchanfragen nach Cluster, qualifizierte Anfragen nach Abo/Projekt/Team und daraus folgende Massnahmen. Vor Änderungen Ausgangswerte dokumentieren.

## Quellen

- [Google: Consent Mode](https://support.google.com/analytics/answer/10000067)
- [Google: Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [Google: AI-Funktionen und Websites](https://developers.google.com/search/docs/appearance/ai-features) — keine spezielle zusätzliche Schema-Art für AI-Zitate notwendig.
