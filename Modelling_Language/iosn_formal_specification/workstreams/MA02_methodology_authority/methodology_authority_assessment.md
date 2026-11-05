# MA-02 — Methodology Authority Assessment (MD-01)
**Assessment date:** 05.11.2026 · **Verdict:** **AUTHORITY_UNCONFIRMED** · **Assurance:** Öffentlich nachgewiesene Quellenlage, **kein** regulatorisches oder ENTSO-E Sign-off.

## 1. Entscheidung
**MD-01 bleibt OPEN und ist für normative Freigabe BLOCKING.** O26 (25.02.2026) ist die **letzte im MA-02-Rechercheumfang verifizierbare direkte ENTSO-E-IoSN-Methodikfassung für TYNDP 2026**, jedoch ausdrücklich eine Konsultationsversion. Eine spätere finale/adoptierte/effective Fassung, ein offiziell publiziertes Erratum oder eine IoSN-spezifische finale Konsultationsauswertung mit Freigabebeschluss konnte zum Stichtag **nicht verifiziert** werden.

Das bedeutet **nicht**, dass eine interne Betriebsanweisung, ein unveröffentlichtes finales Dokument oder eine spätere Veröffentlichung ausgeschlossen ist. Solche Artefakte sind zum Stichtag **nicht auditierbar**. Keine Behauptung einer Genehmigung allein aus der laufenden IoSN-Berechnung ableiten.

## 2. Prüfung der fünf Autoritätsdimensionen
|Dimension|O26 25.02.2026|Nachweis und Grenze|
|---|---|---|
|Veröffentlicht|**YES**|ENTSO-E-PDF auf offizieller Download-Domain, Titelblatt S.1: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf|
|Konsultiert|**YES**|Konsultation 26.02.–03.04.2026, Status closed: https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/|
|Von zuständiger Stelle verabschiedet|**UNCONFIRMED**|Kein Version+Beschluss+Autorität-Beleg ermittelt; ENT SO-E SDC als Verfasserangabe im Entwurf ist **nicht** Annahmebeschluss|
|Für TYNDP 2026 IoSN tatsächlich maßgeblich|**UNCONFIRMED**|O26 als Arbeitsreferenz möglich, keine bestätigte Effective-Version oder Method Owner Directive|
|Historisch/ersetzt|**UNCONFIRMED**|Keine verifizierte Nachfolgeversion; eine behauptete Nicht-Ersetzung ist damit ebenfalls nicht beweisbar|

## 3. Evidenzhierarchie
1. **Rechtsrahmen:** Verordnung (EU) 2022/869 in einschlägiger geltender Fassung; sie autorisiert den Planungsprozess, ist nicht die versionierte operative IoSN-Methodik: https://eur-lex.europa.eu/eli/reg/2022/869/2026-04-29/eng.
2. **Explizit freigegebener Querverweis:** 4th ENTSO-E CBA Guideline, final EC-approved (Titelblatt), **nur** die von O26 §3.4 ausdrücklich referenzierte §2.5.1 als Eligibility-Input: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/news/2024/entso-e_4th_CBA_Guideline_240409.pdf.
3. **Primäre IoSN-Spezifikation:** O26, Konsultationsversion (keine normative Freigabe).
4. **Offizielle Begleitbelege:** Konsultation https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/, News https://www.entsoe.eu/news/2026/02/26/entso-e-releases-public-consultation-on-the-system-needs-methodology/, Webinar-Slides https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYDNP_2026_IoSN_Methodology_Public_Webinar.pdf; kein normsetzender Release.
5. **Interne MA01-MR-/SR-Ableitungen:** fachlich nachvollziehbare, ausschließlich **vorläufige** Requirements.

## 4. Unabhängige Querverweisprüfung: 2035 Eligibility
- **O26 §3.4, S.16–17:** 2035-Startnetz aus 2025-Bestand sowie Projekten, mit geplanter Inbetriebnahme bis spätestens 2035 und Verweis auf Reifekriterien **a, b und c** der CBA4.
- **CBA4 §2.5.1, S.15:** „first study year of the mid-term horizon“ soll auf **a/b** basieren, spätere Mid-term-/Long-term-Horizonte können **c** einschließen.
- **Auditfeststellung MA02-CL-001:** **Potenzielle Auslegungsdifferenz**, kein erwiesener Normwiderspruch. CBA4 beschreibt eine CBA-Referenznetzlogik, O26 ein IoSN-Startnetz 2035. Für 2035 ist deshalb **nachzuweisen**, ob O26 bewusst eine study-specific Ausnahme festlegt, und ob 2035 in CBA4 überhaupt als „first mid-term“ einzustufen wäre. Ohne Methodology-Owner-Bestätigung keine Ableitung „c immer zulässig“ oder „c immer verboten“.
- **Betroffene IDs:** MA01-MR-005, MA01-MR-048, MA01-SR-005, MA01-SR-048; fachlicher Sign-off: Starting Grid/CBA reference owner, danach Methodology Owner.

## 5. Bekannte Quellenoffenheiten (nicht erst durch eine Nachfolgefassung entstanden)
- **O26 §4.6, S.40**: kaputter Link „Error! Reference source not found.“ für Diskontierungszeitblöcke. **MD-02**, MA01-SR-027/043/044.
- **O26 §3.11, S.31**: einheitlicher Offshore-Routenfaktor im Bereich 10–15 %, Endwert für Finalfassung angekündigt. **MD-05**, MA01-SR-038.
- **O26 §4.5.1, S.37**: Kosten-/Speicherannahmen ausdrücklich unvollständig. **MD-06**, MA01-SR-033/034.
- **O26 §§3.8/3.9**, Annex 6.1: Netzreduktionsorakel und LF/optional OPF-Konsistenz müssen freigegeben werden. **MD-03/08**.
- **O26 §2.2 / §§3.1.2,3.10**: KPI- und Kleinmengenfilter ohne vollständige Abnahmeparameter. **MD-04**.

## 6. Zusätzliche Governance-Evidenz und Zurückhaltung
- Der 2025 veröffentlichte Scope-Konsultationsreport erwägt wegen früher Berechnungsstarts erst TYNDP 2028 für spätere Feedback-Umsetzung; die 2026er eigentliche IoSN-Konsultation lässt Änderungen für 2026 **falls prozessual möglich** offen. Beides ist **keine verbindliche Release-/Change-Entscheidung**.
- Die Webinar-Folien vom 27.03.2026 führen den „IoSN Methodology Final Report“ als geplantes Deliverable und Q4 2026–early 2027 als Ergebnisfenster. Erwartete Lieferung ist **kein** Veröffentlichungs- oder Annahmenachweis.
- Die am 09.09.2026 erklärte Freeze-Situation bei TYNDP-Inputdaten (https://tyndp.entsoe.eu/news/review-and-update-your-tyndp-2026-project-information) beweist **keinen** Methodology Release.

## 7. Entscheidungsdatensatz MD-01
|Feld|Ergebnis|
|---|---|
|Decision ID|MD-01|
|Status|OPEN / BLOCKER P0|
|Working baseline|O26, Version for Public Consultation, 25.02.2026|
|Approved authoritative version|NOT_VERIFIED|
|Effective date for TYNDP 2026|NOT_VERIFIED|
|Authority / named signatory|NOT_VERIFIED|
|Adoption resolution|NOT_VERIFIED|
|Official errata / response outcome|NOT_VERIFIED|
|Affected requirements|**alle 48 aktiven MA01-SR**|
|Normative release verdict|**NO-GO: AUTHORITY_UNCONFIRMED**|
|Permitted use|Draft-Anforderungsanalyse, kontrollierte Weiterprüfung, keine Behauptung IoSN-Konformität|
|Next evidence required|Owner-signed decision including approved version/filename/URL/SHA256, adopting authority, date/effective scope, annex status, change log and open-issue decisions|

**Sign-off:** **REQUIRED / NOT OBTAINED**. Dieses Dokument ist eine unabhängig erstellte Recherchebewertung, keine Entscheidung der ENTSO-E.