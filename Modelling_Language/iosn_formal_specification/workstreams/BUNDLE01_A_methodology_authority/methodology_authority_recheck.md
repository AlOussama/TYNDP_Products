# BUNDLE-01 / Workstream A — Methodology Authority Recheck

**Stichtag:** 2026-11-10 · **Vergleichsgrundlage:** MA-01 PR #17 (`a86bbeb8377ac1c9a5c77d900ad287691397e506`), MA-02 PR #18 (`1c32643a578ec7a6531cf9d314a343dfb9c7fa5d`) · **Status:** `AUTHORITY_UNCONFIRMED`, **NOT_NORMATIVE**.

## Befund und Statusdimensionen

|Autoritätsaspekt|Beleg|Urteil|
|---|---|---|
|Methodikdokument, Inhalt und Datum|O26, Titelblatt: „Version for Public Consultation“, 25.02.2026, 65 Seiten; https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf|**PUBLISHED_DRAFT_CONFIRMED**|
|Konsultationszeitraum|ENTSO-E Citizen Space: eröffnet 26.02., geschlossen 03.04.2026; https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/|**CONSULTATION_COMPLETED**|
|Formeller Genehmigungsakt|Keine versionierte, von zuständigem IoSN-Methodikowner bestätigte Entscheidung vorgelegt oder bei aktueller Öffentlichkeitsrecherche eindeutig gefunden|**UNCONFIRMED**|
|Maßgebliche Revision, Gültigkeitsbeginn und Anwendungsbereich|Keine offiziell belegte Effective-Directive für TYNDP-2026-IoSN|**UNCONFIRMED**|
|Ausdrücklich erlassene IoSN-Korrekturen, Konsultationsauswertung|Kein im Recheck positiv belegbares Release/Erratum mit referenzierter Dokumentfassung|**UNCONFIRMED**, keine Nichtexistenzbehauptung|
|SHA-256 des tatsächlichen offiziellen PDF-Binärartefakts|Offizieller PDF-Pfad als lesbares Dokument überprüft; Download von Binärbytes in Prüf-Laufzeit fehlgeschlagen|**NOT_COMPUTED**; kein fingierter Hash|
|MA01-Requirements-Reconciliation|48 aktive MA01-SR und 50 MA01-MR; keine belegte zweite Revision zum direkten Delta-Vergleich|**0 verifizierte A→B-Änderungen**, **nicht** „0 tatsächliche Änderungen“|
|Scope Wetterjahrauswahl|MA01-MR-012/049 als `UPSTREAM_ONLY`; bereits gewählte Wetterjahre sind nur Input|Auswahlalgorithmus weiterhin **außerhalb des IoSN**|

**Wichtige Abgrenzung:** Die separat von der Europäischen Kommission genehmigte 4th ENTSO-E CBA Guideline und die im Juni 2026 öffentlich publizierten **Draft Scenarios** sind weder eine Genehmigung noch eine Nachfolgerevision der IoSN-Methodik. CBA4 §2.5.1 bleibt ein O26-Querverweis zur Startnetz-Projektreife.

## Evidenz- und Suchspur am Stichtag

- Offizielle ENTSO-E-Konsultationsseite und Mitteilung vom 26.02.2026: https://www.entsoe.eu/news/2026/02/26/entso-e-releases-public-consultation-on-the-system-needs-methodology/
- Offizielle PDF (Titelblatt; Inputdata §§4.1–4.6; §3.4 / Annex 6.2; §3.7 / Annex 6.3).
- ENTSO-E TYNDP-Hub, News und offizielle ENTSO-E-Webseiten nach „TYNDP 2026 Identification of System Needs methodology final/approved/erratum/consultation outcome“.
- Aktuelle TYNDP-2026-Datenstände: https://2026.entsos-tyndp-scenarios.eu/download/; 09.09.2026 Projekt-Update-Hinweis https://tyndp.entsoe.eu/news/review-and-update-your-tyndp-2026-project-information; Datenfreeze **kein** Methodikfreigabebeleg.
- Resultat ist eine zeitpunktbezogene **Negativverifikation**, keine Vollständigkeits- oder Nichtexistenzgarantie für interne/ungelistete ENTSO-E-Unterlagen.

## Querverweis: ungeklärte Eligibility für 2035

**MA02-CL-001 / P0.** O26 §3.4 S.16–17 nennt CBA4-Reifekriterien a/b/c; CBA4 §2.5.1 S.15 unterscheidet das erste Jahr des mittelfristigen Horizonts. Der Vergleich ist **eine potenzielle Auslegungsdifferenz, kein nachgewiesener Normwiderspruch**. Freizugeben ist ein versionierter Jahr×Projekt×Reifegrad-Crosswalk, gemeinsam bestätigt von Starting-Grid- und IoSN-Methodology-Owner (MA01-MR/SR-005,048).

## Änderungs- und Freigabedisposition

1. **Keine** Veränderung der 48/48 MA01-SR, der 50 MA01-MR oder der bisherigen MA02-Matrizen: sie bleiben vorläufig.
2. **Kein methodischer Delta erfunden:** `VERSION_B=NOT_VERIFIED`; O26→B textuelle und normative Differenz `NOT_ASSESSABLE`; nicht „UNCHANGED“.
3. 20 MD aus dem bestehenden Register plus MA02-CL-001 weiterhin offen; neue Owner-Antworten wurden **nicht** eingeholt.
4. Sign-off durch ENTSO-E Methodology Owner, fachliche Domain Owner, Release-Governance und unabhängige QA **nicht erfolgt**.
5. G1-Normativgate: `AUTHORITY_UNCONFIRMED / BLOCKED`. Zulässig: vorläufige Input-/Requirement-Analyse; unzulässig: normative IoSN-Contract-Implementierung.

## Lieferpflicht für einen späteren echten Versionsvergleich

Für jede freigegebene Revision B: Original-PDF-Bytes; kanonische URL; Dokumenttitel/Version; SHA-256; Herausgeber, Entscheider und Annahmeakt; Veröffentlichungs- und Wirksamkeitsdatum; Gültigkeitsbereich; Annex-/Errata-Liste; Änderungsverzeichnis; source-clause Crosswalk auf **alle** 50 MA01-MR und 48 MA01-SR, inklusive betroffener Verifikationsorakel. Method Owner muss die unveränderten Bereiche **positiv** attestieren. Keine Freigabe aus bloßer Dateinamens- oder Versionsähnlichkeit.
