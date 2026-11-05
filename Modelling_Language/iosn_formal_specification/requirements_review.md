# MA-01 — Independent Requirements Review (R1–R5)

**Datum:** 2026-11-05. **Review-Gegenstand:** 50 Fundstellen zur ENTSO-E IoSN-Methodik (Konsultationsversion 25.02.2026), 18 Prozessschritte P00–P17, 48 vorläufige toolunabhängige MA01-SR, methodische Scope-Grenze und Research PR #16. **Art:** unabhängiger Dokumenten-/Konsistenzreview, **kein** ENTSO-E Sign-off und **keine** Modell- oder Softwarekonformitätsprüfung.

## R1 — Completeness

|Finding|Schwere|Feststellung|Disposition|
|---|---|---|---|
|R1-F01|CRITICAL|Eine final genehmigte/effective Methodikversion ist nicht nachgewiesen.|MD-01 BLOCKED.|
|R1-F02|HIGH|Frühere 34-Clause-Inventur war nur partiell; Netzreduktion, Hydro/DSR, Projektkandidaten, Kosten-/Offshore-Details müssen ausdrücklich abgedeckt sein.|50 source-clause-Einträge und 18 Prozesszeilen neu erfasst; vollständiges Satz-für-Satz-Audit und Owner-Bestätigung weiterhin OPEN.|
|R1-F03|HIGH|Frühere Requirement-/PoC-Dokumente behandelten Wetterjahrauswahl als aktiven Use Case.|Bereits ausgewählte Wetterjahre als Input; 2 Annex-Fundstellen nur extern; neue aktive SyRS ohne Auswahlalgorithmus. FIXED_IN_DRAFT.|
|R1-F04|HIGH|Output-KPI, Diskontierungsblöcke, Offshore-Routing-Faktor und Speicherkosten nicht vollständig quellenabgeschlossen.|MD-02/04/05/06; exakte Akzeptanz derzeit BLOCKED.|
|R1-F05|MEDIUM|Referenzquellen PEMMDB/PECD/DFT/Starting Grid mit freizugebenden Versionen fehlen.|MD-11/14; Datenreplay OPEN.|

**R1-Bewertung:** Systematische Subsection-/Clause-Überprüfung als Draft vorhanden. Die 50 Zeilen sind **kein attestierter Anspruch**, sämtliche normativen Sätze im PDF vollständig erfasst zu haben. Annex 6.3 nur upstream.

## R2 — Correctness and Methodology Fidelity

|Finding|Schwere|Feststellung|Disposition|
|---|---|---|---|
|R2-F01|CRITICAL|Nichtantizipative Investitionsentscheidung in §3.1.1 darf nicht pro Wetterfall unabhängig sein.|MA01-SR-029; Prüfung muss generiertes Modell inspizieren.|
|R2-F02|HIGH|§3.9 trennt primäre LF-Expansion mit vermaschten DC-Flüssen und entgrenzten Interzonenkapazitäten von internen Engpassläufen und optionaler OPF-Expansion.|P10–P15 und SR-024–026 getrennt; MD-08 offen.|
|R2-F03|HIGH|§4.5.2 verlangt **steuerbare DC-Marktlinks für alle Übertragungsausbaukandidaten**, auch physisch AC; nicht gleich Bestands-DC-Netzlastfluss.|SR-018 vs SR-035 getrennt; MD-09 offen.|
|R2-F04|HIGH|§3.10 erfordert Stufen mit definierten Kandidatenmengen und separat 2040/2050 Speicher.|SR-031–034; Stage-Crossover MD-07 bleibt offen.|
|R2-F05|MEDIUM|§5.1 nennt Plexos/Antares als Veranschaulichung, nicht als Software-Mandat.|SR-047 nur technischer Nachweisbedarf, keinerlei Toolzwang.|
|R2-F06|HIGH|Wetterfall-IDs, Zonenanzahl, Kostenannahmen sind O26-versionsspezifisch; nicht allgemeine DSL-Konstanten.|Profil/Release gebunden; MD-01.|
|R2-F07|HIGH|KPI-/Kostenregeln unvollständig; willkürliche Toolstandards dürfen sie nicht ersetzen.|Offene Parameter als BLOCKED geführt.|

**R2-Bewertung:** Zentrale methodische Mathematik und Modellabstraktion erhalten, keine methodisch unbelegte Wahl eines Komponentenframeworks. Details und Zahlen teilweise unbestätigt.

## R3 — Solution Neutrality

|Finding|Schwere|Feststellung|Disposition|
|---|---|---|---|
|R3-F01|HIGH|Legacy ADR und LRC-Matrix könnte verbindliche Architekturauswahl suggerieren.|Historisch markiert; neue MA-01-SyRS trifft keine Wahl zwischen SysML/CESM/GEMS/INES/DSL.|
|R3-F02|HIGH|Toolneutralität bedeutet **nicht** Freiheit, LP-Zielfunktion oder Netzphysik zu ändern.|Solver-/Bibliothekswahl frei, Gleichungsklasse und Domain-Link-Semantik quellengebunden.|
|R3-F03|MEDIUM|POC-spezifische JSON-Struktur darf nicht zum vorgeschriebenen Datenformat werden.|Legacy PoC ist nicht normative Implementierung.|
|R3-F04|MEDIUM|Keine CBA-Interoperation, generische Robustheitslayer oder Wetterjahrauswahl im MA-01.|Scope und Ausschlüsse explizit.|

**R3-Bewertung:** Vorläufige Anforderungen sind tool-/implementierungsneutral; Interoperabilität mehrerer realer Modelle ist **nicht** nachgewiesen.

## R4 — Verifiability

|Finding|Schwere|Feststellung|Disposition|
|---|---|---|---|
|R4-F01|CRITICAL|Legacy PoC: positive/negative synthetische Tests eines publizierten Wettermanifests, **keine** Modellvalidierung.|Alle MA-01 L4-Nachweise NOT_EXECUTED; alte Tests nicht als SyRS-PASS übertragen.|
|R4-F02|HIGH|Ergebnisgleiche Investitionen beweisen keine gültige Nichtantizipativität des generierten Optimierungsmodells.|SR-029 prüft LP-Bindung; adversarial counterexample erst später.|
|R4-F03|HIGH|RMSE/LODF/N-1 und KPI-Orakel brauchen offizielle Parameter und Referenzdaten.|MD-03/04/13; BLOCKED.|
|R4-F04|HIGH|Multiple optimale Portfolios dürfen nicht blind als nichtkonform gelten.|MD-15/17: mathematische Feasibility, Zielwert-/KPI-Äquivalenz erforderlich.|
|R4-F05|MEDIUM|Zeittoleranzen, optionale OPF, H2-Freeze und Speicherrestriktionen brauchen konkrete Fixture-/Oracle-Freigabe.|MD-06–12,15; NOT_EXECUTED.|

**R4-Bewertung:** Nachweisbedarfe sind spezifiziert, aber 0/48 MA-01-Anforderungen auf Implementierungsebene erfolgreich getestet. Testdefinition ≠ Testdurchführung ≠ Nachweis vollständiger Systemkonformität.

## R5 — Consistency

|Finding|Schwere|Feststellung|Disposition|
|---|---|---|---|
|R5-F01|CRITICAL|Legacy SR-005 / UC-01 / Roadmap Gate2 widersprechen der externen Wetterjahrauswahl.|Neue MA01-IDs aktive Draft-Baseline, alte SR/UC/Gate nur historisch.|
|R5-F02|HIGH|Entwurfswort “robust” darf keine Minimax-/CVaR-Pflicht erzeugen.|Wettergewichtete Erwartung + gemeinsame Investitionen, keine generische Robustheitsanforderung.|
|R5-F03|HIGH|DC-Lastfluss und kontrollierbarer DC-Marktlink bezeichnen unterschiedliche physikalische/marktliche Rollen.|L3 und SR-018/035 strikt getrennt.|
|R5-F04|MEDIUM|Frühe Architektur-/PoC-Berichte bleiben im Repository, sind aber historisch.|Kennzeichnung in README/Legacy-Dokumenten; keine Codeänderung.|
|R5-F05|HIGH|PASS eines Inputschemas darf nicht automatisch vollständigen IoSN-Vertragsstatus bedeuten.|Explizite Evidence-Layer und BLOCKED/NOT_EXECUTED.|

## Review-Abnahme gegen MA-01-Gates

|Gate|Disposition|
|---|---|
|Aktueller Methodikstand eindeutig oder Blocker|**Erfüllt mit BLOCKER MD-01**|
|Relevante Prozesskette systematisch geprüft|**Vorläufig erfüllt**; Detailvollständigkeit ungeprüft|
|Wetterauswahl nur externe Eingabe|**Erfüllt** in neuer SyRS; Altunterlagen historisch|
|L1→L2→L3→L4 traceability|**Erfüllt strukturell** 50 L1, 48 L2 + 2 extern|
|Anforderung/Architektur getrennt|**Erfüllt**|
|Bindende Mathematik und Toolfreiheit unterscheidbar|**Erfüllt**|
|Offene Entscheidungen erfasst|**20 OPEN**, keine künstliche Schließung|
|Kritischer unabhängiger Review|**R1–R5 dokumentiert**|
|Widerspruchsfreier aktiver Katalog|**MA01-SR allein aktiv**; historische Materialmarkierung vorausgesetzt|
|Handoff und Abhängigkeiten|**Dokumentiert**, Nachfolgearbeit nicht gestartet|

## Schlussdisposition

**PROVISIONAL / BLOCKED FOR NORMATIVE RELEASE.** Die Dokumentenbaseline ist für methodische Prüfung und Scope-Governance verwendbar. Ohne genehmigten Quellenstand, zusätzliche methodische Parameter/Orakel, betroffene Dataset-Versionsnachweise und echte Modellprüfungen kann keine vollständige IoSN-Systemkonformität bescheinigt werden.


## Nachgeprüftes Repository-/Struktur-QA (2026-11-05)

Die Dokumentstruktur wurde nach dem Commit auf dem MA-01-Branch erneut aus GitHub gelesen und mit einer unabhängigen tabellarischen Prüfung abgeglichen. Der Vergleich gegen den Ausgangsbranch research/iosn-formal-specification-2026-11-04 ergibt:

|Prüfgröße|Beobachtung|Urteil|
|---|---:|---|
|Zehn spezifizierte MA-01-Deliverables vorhanden|10/10|PASS dokumentarisch|
|Quellenbaseline MA01-MR, eindeutige IDs|50/50|PASS strukturell|
|Aktive MA01-SR (21 Katalogspalten), eindeutige IDs|48/48|PASS strukturell|
|Traceability-Einträge (12 Spalten), eindeutige MA01-MR|50/50|PASS strukturell|
|L1-Fundstellen mit aktiven SR-Verweisen|48|PASS strukturell|
|Ausdrücklich externe Wetterauswahl-Fundstellen ohne SR|2 (MA01-MR-012, MA01-MR-049)|PASS Scope|
|Prozessmatrix-Schritte und Spalten|18 Schritte / 13 Spalten|PASS strukturell|
|CSV-Spalten- und SR-Verweisfehler|0|PASS strukturell|
|Historische Markdown-Berichte mit direktem Legacy-Banner|13/13|PASS Scope|
|Historische CSV-Kataloge mit Status-Spalte HISTORICAL_NON_ACTIVE|3/3|PASS Scope|
|Git-Diff auf MA-01-Arbeitsverzeichnis beschränkt|27/27 Dateien|PASS Scope|
|Änderungen an bestehender Implementierung oder PoC-Code|0|PASS Scope|
|Ausgeführte MA-01-Modell-, LP- oder KPI-Konformitätstests|0|**NOT_EXECUTED**|
|Fachlich bestätigte finale IoSN-Methodikversion|keine|**BLOCKED MD-01**|

**Grenze des QA:** Eine gültige CSV-Struktur und fehlerfreie Verweiskette beweisen weder vollständige, korrekte Extraktion aller PDF-Formulierungen noch die Güte eines Energiesystemmodells. Der unabhängige Fachreview und die autoritativen Methodikentscheidungen sind deshalb weiterhin als externe Freigabegates offen.
