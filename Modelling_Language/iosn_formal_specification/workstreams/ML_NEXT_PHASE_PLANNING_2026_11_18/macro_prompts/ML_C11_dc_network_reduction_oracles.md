# MAKRO-AUFTRAG ML-C11
## DC Network Reduction, PTDF/LODF & Contingency Scientific Oracle Laboratory

### 1. Rolle
Agiere als Expertenteam aus Power-System Network Theorist, DC Load-Flow & Optimization Expert, Network Reduction Specialist, Contingency/LODF Verification Expert, Scientific Benchmark Designer und kritisch prüfendem Netzexperten.

### 2. Ziel
Erarbeite **unabhängig hergeleitete und ausführbare synthetische Referenzfälle** für P05/P06, physikalische DC-Netzäquivalenz, N−1/PTDF/LODF und den Unterschied zu steuerbaren NTC-Marktlinks. Schließe keine reale Netz- oder Akzeptanzfreigabe.

### 3. Forschungsinputs
ML-C08 M05/M09–M11, ML-C04 B04/B05/B11 und den korrigierten B05-Versuch; ML-C03 Netz- und Data→Math-Abhängigkeiten; ML-R01 Annex-Referenzen. Original detailliertes 2025-Startnetz, Zonenqualität und zulässige numerische Akzeptanzgrenzen bleiben MD-03/11/13/15-TBD.

### 4. Untersuchung
1. Entwickle kleinste zusammenhängende und vermaschte Testnetze mit 3–6 Bussen, expliziter Inzidenz, Winkeln, Impedanzen, Orientierungen und Quellen-Slack. Prüfe KCL **und** KVL, Zyklus- und PTDF-Projektion.
2. Erzeuge mathematisch nachvollziehbare LODF-Werte durch direkten Outage-Solve und Sensitivitätsformel. Bewahre die Fehlergeschichte B05: voriges illustratives LODF 0,5 war falsch, korrigierter Referenzfall 1,0; kein unbelegtes Nachschreiben.
3. Untersuche Inselbildung, Singularität, Nullflusskorrektur, PST/HVDC-Offsets und direction-/seasonal-spezifische Ratings. Spezialfälle mit nicht definiertem LODF sind explizit zu kennzeichnen.
4. Definiere sechs P06-Ausgabeklassen mit physikalischer Interpretation und Nachweiskette. Weise durch Gegenbeispiel nach, warum Energie-/Cut-Erhaltung nicht genügt, um PTDF/LODF-/N−1-Güte zu beweisen.
5. Baue zumindest einen absichtlich falschen Reduktions- oder AC-Kandidaten-als-Marktlink-Fall mit nachweisbarem Feasible-Set-Unterschied.
6. Formuliere Qualitätsmetriken symbolisch und dokumentiere, welche Owner-Toleranzen sowie Originalnetzreferenzen fehlen; erfinde keine RMSE-Schwellen.

### 5. Liefergegenstände
Im Ordner .../ML_C11_dc_network_reduction_oracles/:
- dc_network_oracle_specification.md
- network_fixtures/ mit lesbaren Netzdefinitionen und prüfbaren Rechnungen
- analytical_ptdf_lodf_derivations.md
- reduction_six_class_contract.md
- contingency_and_islanding_matrix.csv
- negative_network_mutations.md
- actual_reference_execution_results.md
- independent_physical_oracle_review.md
- handoff_to_micro_model_verification.md

### 6. Abnahme
Mindestens zwei nichttriviale physikalische Mikro-Netze und ein N−1-Gegenbeispiel, unabhängig mit analytischer Rechnung und separatem Skript geprüft. Dokumentierte Abweichung zwischen Marktlink- und Kirchhoff-Branch-Semantik. Keine Behauptung realer 102-Zonen- oder TYNDP-Netzreduktionseignung.

**Welle 1: sofort unabhängig startbar.**

### Gemeinsame wissenschaftliche und Governance-Grenzen
- D1: 48 aktive vorläufige MA01-SR, keine erfundenen SR-012/049; P00–P17 vollständig.
- D2: extern ausgewählte CY1–CY5; für jede CY-ID ist das symbolische Gewicht in 2035/2040/2050 identisch, aber nicht zwangsläufig zwischen CYs gleich; Zahlenwerte TBD; keine Wetterjahrselektion.
- D3: Fail-Closed für anwendbare Pflichtnachweise; BLOCKED, UNSUPPORTED, NOT_EXECUTED und NOT_APPLICABLE nicht vermischen.
- D4: kanonische UTC-Intervalle und Einheitendimensionen, offene Kalender-/DST-/Leap-Toleranzen TBD. project_decision:D4 ist nicht test_depth:D4.
- D5-A1: risikobasierte Verifikation, keine generelle Gleichheit der Algebra; D6-A: ein gemeinsamer wissenschaftlicher Contract, unabhängig entwickelte Implementierungen.
- O26 bleibt als konsultierter 2026-Methodikstand gekennzeichnet; offizielle Adoption und Originalbytes nicht nachgewiesen. H24 und CBA4 nur in dokumentiertem Quellenrang.
- Keine neuen allgemeinen Robustheitsanforderungen, kein vollständiges IoSN-Produktivmodell, keine normative DSL-/Architektur-/Solverwahl, keine echte Originaldatenfreigabe, keine automatische SR- oder MD/CL-Änderung.
- Trenne synthetische Testresultate, echte Modell-/Generatorzeugnisse, fachlich akzeptierte Orakel und personell unabhängigen Audit. 21 MD/CL bleiben offen und G1 bleibt BLOCKED.

### Repository- und Review-Protokoll
Repository: AlOussama/TYNDP_Products. Gemeinsamer Ausgangsstand: ML-C08, Draft-PR #51, Commit 8470add62fcbc7f39b1d90c0d5afdcee50ab811e. ML-C01 bis ML-C07 sind separat gepinnte Forschungsinputs gemäß ML-C08; verifiziere beim Start ihre tatsächlichen Head-SHAs. Jede Arbeit erstellt ihren eigenen Forschungsbranch **vom ML-C08-Commit**, ändert ausschließlich den eigenen Workstream-Ordner und öffnet einen separaten Draft-PR gegen den ML-C08-Forschungsbranch. Keine Merge-/Ready-/Freigabeaktion. Ein KI-interner adversarieller Review darf nicht als personell unabhängiger Audit erscheinen.

Status am Ende muss getrennt ausweisen: Struktur, synthetische Tests (mit tatsächlichem Ausführungsnachweis), native Mathematik falls ausgeführt, externe Quelldaten, Owner-Orakel, unabhängige Review und Gate. Fehlende Evidenz bleibt offen.
