# MA-02 — Official Clarifications & Unresolved Evidence Register
**Datum:** 05.11.2026. **WICHTIG:** Dies ist ein Register **offizieller Publikationsbelege und offener Klarstellungsanfragen**, keine Sammlung behaupteter, unveröffentlichter ENTSO-E-Freigaben. **Official owner replies obtained: 0.**

## A. Offiziell tatsächlich belegte Klarstellungen (geringer Autoritätsumfang)
|ID|Offizielle Quelle / Aussage|Status|Normativer Geltungsbereich / Grenze|MA01-Bezug|
|---|---|---|---|---|
|EV-01|O26 Titelblatt „Version for Public Consultation“, 25.02.2026|PUBLISHED_DRAFT_CONFIRMED|Nicht genehmigte IoSN-Konsultationsfassung|alle 48 SR|
|EV-02|ENTSO-E Citizen Space: 26.02.2026 eröffnet, 03.04.2026 geschlossen|CONSULTATION_CLOSED_CONFIRMED|Belegt Konsultation, **keine** Annahme|MD-01|
|EV-03|CBA4 Titelblatt: Final version approved by the European Commission; §2.5.1 proof of maturity|EXTERNAL_CBA_APPROVAL_CONFIRMED|**Nur CBA4**, keine IoSN-Freigabe; referenziert in O26 §3.4|SR-005, SR-048|
|EV-04|Webinar 27.03.2026: „IoSN Methodology Final Report“ als künftiges Deliverable|FUTURE_DELIVERABLE_MENTIONED|Kein Beleg für erschienenes/angenommenes Finaldokument|MD-01|
|EV-05|O26 S.31, S.37, S.40: Aufschlag/Storage-Enddetails angekündigt bzw. defekter Verweis|SOURCE_LIMITATIONS_CONFIRMED|Offenheit **in A**; keine bestätigte spätere Behebung|SR-038,034,044|

## B. Offizielle Methodology-Owner-Entscheidungen erforderlich
|ID|Priorität|Offene fachliche Frage|Originalfundstelle|Betroffene MA01-SR|Erwartetes Entscheidungsartefakt|Vorgeschlagener Owner|Status|
|---|---|---|---|---|---|---|---|
|MA02-CL-001|P0|2035 Startnetz: O26 nennt CBA4 a/b/c; CBA4 §2.5.1 limitiert beim ersten mittelfristigen Studienjahr a/b. Gilt die Einschränkung für IoSN 2035 oder eine explizite 2026-study-specific Abweichung?|O26 §3.4 S.16–17; CBA4 §2.5.1 S.15|005,048|Signierter Eligibility-Crosswalk pro Studienjahr und Project-Maturity-Fall, maßgebliche CBA-/IoSN-Regel|Starting Grid Owner + Methodology Owner|OPEN; POTENTIAL_DIFFERENCE|
|MA02-CL-002|P0|Wo sind finale IoSN-Methodikfassung, Version, Freigabeakt, Stichtag, Wirksamkeitsbereich, Errata und Consultation Outcome?|O26 S.1; P26|alle 48|Final-PDF, SHA256, Beschluss, Datum, Effective Scope, Änderungsverzeichnis|ENTSO-E Methodology Owner|OPEN|
|MA02-CL-003|P0|Diskontformel, Bezugsjahr und Jahresblöcke bei fehlendem PDF-Querverweis?|O26 §4.6 S.40|027,043,044|Vollständige Formel und numerisches Referenzbeispiel|Economics Owner|OPEN|
|MA02-CL-004|P0|Verbindliche Qualitäts-/Akzeptanzschwellen für Zonen, RMSE, LODF, N-1, äquivalente Kapazitäten?|O26 §3.8 + Anh.6.1|013–023|Referenznetz und Testfälle, Sollwerte, Toleranzen|Network Reduction Owner|OPEN|
|MA02-CL-005|P1|Endgültiger einheitlicher Offshore-Wegfaktor und Kosten-Geltungsbereich?|O26 §3.11 S.30–31|038|Einheitlicher Wert/Geometrie/Kostenbeispiel|Offshore Owner|OPEN|
|MA02-CL-006|P1|Speicherkosten, Dauerklassen und Ländertrajektorien für 2040/2050?|O26 §3.10/§4.5.1 S.30/37|033,034|Parameter-Release und Beispiel|Storage Owner|OPEN|
|MA02-CL-007|P1|Exakte Transition der zwei Übertragungs-LP-Stufen, verbleibende Teilkandidaten und Speicher-Stage?|O26 §3.10 S.30|003,031,032,033|Freigabe der Stage-Transition; dimensionsrichtige Beispiele|Expansion Owner|OPEN|
|MA02-CL-008|P1|Verbindlicher LF-Modus versus zusätzlicher Dispatch; OPF optional und auf LF-Kandidaten begrenzt?|O26 §3.9 S.29|024,025,026|Lauf-/Verifikationsszenarien, was Pflicht vs optional ist|Network Expansion Owner|OPEN|
|MA02-CL-009|P1|Wahl der Input- und Umwandlungssemantik für H2/eingefrorene Elektrolyse-Last?|O26 §§3.3/3.6 S.15/18|007,008,009,050|Freigegebenes H2-Referenzprofil inkl. Einheit/Zuordnung|Hydrogen Owner|OPEN|
|MA02-CL-010|P1|KPI-Metriken, Aggregation, Kleinmengenfilter, äquivalente Optima?|O26 §§2.2,3.1.2,5.1|001,025,045,046,047|Output-Catalogue, Berechnungsdefinitionen, Testfall|Reporting & Verification Owner|OPEN|
|MA02-CL-011|P2|Wetterinput: Studie, Identitäten, Gewichte, Zeitachsen und Profile extern zu liefern; welche numerischen Toleranzen?|O26 §3.7 S.19–20|010,011,040,042|Freigegebenes Inputmanifest und Annahmetest **ohne Auswahlalgorithmus**|Weather Input Contract Owner|OPEN|
|MA02-CL-012|P1|Realprojekt-Marktlink: NTC je Richtung, Kostenzurechnung, AC-physisch/steuerbar-DC-im-Modell?|O26 §4.5.2 S.37–38|035,036|Mapping-/Equivalence-Example und dokumentierte Modellfreiräume|Market Model Owner|OPEN|
|MA02-CL-013|P1|Wie werden Projektlisten, Offshore-Targets und fachliche Eingaberevision im 2035 Startnetz legitimiert?|O26 §§3.4/3.5; Anh.6.2|005,006,048|Methodisch freigegebene Releasekennungen/Eligibilitätsregeln; Dateninventur bleibt MA-03|Starting Grid Owner|OPEN|

## C. Handhabung
- **Status OPEN** bis zitierfähiger ENTSO-E-Owner-Beschluss oder schriftliche, versionsgebundene autorisierte Klarstellung vorhanden ist. Webinar-/PR-Diskussionen nicht automatisch zu Anforderungen erheben.
- Jeder Bescheid dokumentiert: **ID, Frage, erteilende Person/Stelle, Rolle/Befugnis, Datum, Signatur/URL, exakter Wortlaut, betroffene MR/SR, Änderungsklasse und Akzeptanztest**.
- Wichtig: Der Scope des Wettermoduls beginnt bei **bereits ausgewählten** Wetterjahren; weder PCA/K-Means noch die Auswahlheuristik oder statistische Evaluierung in MA-02 integrieren.
- Es werden keine neuen Robustheits-, Software-/Spracharchitektur-, Tooladapter- oder CBA-Interoperabilitätsanforderungen eingeführt.

**Quellen:** https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf · https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/ · https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/news/2024/entso-e_4th_CBA_Guideline_240409.pdf · https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYDNP_2026_IoSN_Methodology_Public_Webinar.pdf