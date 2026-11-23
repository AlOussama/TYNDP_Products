# ML-C19/01 – Anforderungen an die Canonical Semantic Normal Form
Stand 2026-11-23; Forschungsbaseline research-r1; NON-NORMATIVE. Grundlage: [ML-C18/01](https://github.com/AlOussama/TYNDP_Products/blob/5555be36f74d1d4f6e871d4503c1fc91e417e57c/Modelling_Language/study_contract_language/workstreams/ML_C18_general_contract_language_research/01_study_contract_language_requirements.md), 42 SLR-Kandidaten, sowie [ML-C18/02](https://github.com/AlOussama/TYNDP_Products/blob/5555be36f74d1d4f6e871d4503c1fc91e417e57c/Modelling_Language/study_contract_language/workstreams/ML_C18_general_contract_language_research/02_requirements_and_metrics_matrix.csv), K01–K17.

## Ziel, Entscheidungsgrenzen und Akzeptanz
CSNF repräsentiert fachliche *Verpflichtungsbedeutung* unabhängig von Schreibweise, Parser, Solver und interner Modellformulierung. Sie ist nicht das kanonische mathematische Optimierungsmodell. Der semantische Kern wird vor Syntax und Compiler untersucht. Keine neue normative IoSN-Methodik, keine D1–D6-Revision, alle MD/CL offen; G1 BLOCKED.

Abstraktionsregel: Eine zusätzliche Verpflichtung zu einer konkreten Variablen, Gleichung oder Engine ist nur zulässig, wenn eine belegte fachliche Quelle sie ausdrücklich vorschreibt. Explizite Source- und Owner-Referenzen bleiben identifizierbar. Konflikt und Unwissen dürfen nicht stillschweigend aufgefüllt werden.

| ID | Forschungsanforderung | Prüforakel / Negativgegenbeispiel | Zuordnung |
|---|---|---|---|
| NFR-01 | Determinismus für fixierte Schema-, Registry- und Regelversion | N(C) byte-identisch in zwei Ausführungen | K08,K16 |
| NFR-02 | Idempotenz N(N(C))=N(C) | Wiederholung verändert semantischen Hash nicht | K09 |
| NFR-03 | Bedeutungserhaltung bei jeder Regel | Interpretation vorher/nachher gleich im angegebenen Fragment | SLR05,08 |
| NFR-04 | Typisierte Referenzen, stabile IDs, Namespace-Auflösung | Mehrdeutige Rollenreferenz muss BLOCKED sein | SLR12–14 |
| NFR-05 | Normativitäts-, Entscheidungs- und Approval-Status erhalten | REQUIRED/PERMITTED/OWNER_TBD nicht verschmelzen | SLR05,11,36 |
| NFR-06 | Scope, Guards, A/G-Stärke und Konfliktregionen erhalten | fehlender Guard darf kein TRUE werden | SLR18,19 |
| NFR-07 | Größenart, Dimension, Einheit, Bezugsbasis und Sign erhalten | MW-Injektion ≠ MW-Verbrauch | SLR14,35 |
| NFR-08 | Zeitachse, Schrittweite, Gewichte, Szenariobaum, Informationsmenge | Stage-1 Leakage erkennen | SLR04,37,38 |
| NFR-09 | Externes Rollen-/Port-/Connect-Verhalten | Gleiches Feld ohne Carrier keine Kompatibilität | SLR12–20 |
| NFR-10 | Interne Struktur- und Implementierungsfreiheit | SOC vs Energiezustand bei gleicher Außenpflicht | SLR21–26 |
| NFR-11 | Input-/Transformation-/KPI-Semantik erhalten | N2E-Gegenfaktum und Diskontbasis nicht tilgen | SLR06–09,39 |
| NFR-12 | Source, Evidence, Provenienz und unabhängige Identitäten | zwei Quellen derselben Aussage nicht zusammenwerfen | SLR10,34,41,42 |
| NFR-13 | Getypte Komposition mit expliziten Überschreibungen | widersprüchliche Fragmente nicht last-write-wins | K13 |
| NFR-14 | Roundtrip unter klar definiertem Semantikprojektor | export/import verliert Ownerstatus => FAIL | K14 |
| NFR-15 | Schema- und Regelversion im Hash und Diff | neuer Guard ist semantischer Change | K15 |
| NFR-16 | Fehlerdiagnostik, Trace und kognitive Minimalität | Meldung mit ID/Pfad/Regel/Source/Grund | K12,K17 |
| NFR-17 | automatische E1 strikt von E2–E5 trennen | identisches Ziel ohne feasible-set-Beweis nicht E4 | K06,K09 |
| NFR-18 | Unbekanntheit konservativ bewahren | UNKNOWN/NOT_EXECUTED ≠ Null/PASS | SLR36,41 |

## Redundanzprüfung und Priorisierung
NFR01/02 sind getrennt: deterministisch kann ein nichtidempotentes Verfahren sein. NFR03/14 sind getrennt: lokale Rewrite-Soundness beweist keinen Adapter-Roundtrip. NFR05/12: fachliche Geltung einer Verpflichtung ist nicht ihre Quellenkette. NFR07/08: zeitliche Zeitintegration ist dimensionsbezogen, aber nicht auf Einheiten reduzierbar. NFR09/10: Schnittstellenstrenge und interne Offenheit sind komplementäre Pflichten. NFR17/18: Unentscheidbarkeit kann auch bei vollständig gegebenen Daten auftreten.

**Gate A – Muss für einen positiven Formalsemantikbefund:** NFR01–10, 12, 17,18. **Gate B – erforderlich für Architekturreife/Handoff:** NFR11,13–16. Keine numerische Erfüllungsquote ohne ausgeführte vollständige Fallmatrix behaupten.

## Testaufbau und Evidenzhierarchie
Für jede NFR: Baseline-Case, gleichbedeutende Umschreibung, minimale semantikändernde Mutation, Erwartung E1_EQUAL / E1_DIFFERENT / BLOCKED / UNKNOWN, Quellen-ID, Testart und Run-ID. Status: SPECIFIED, DESIGNED, SOURCE_INSPECTED, EXECUTED_SYNTHETIC, NATIVE_EXECUTED, PROVED, NOT_EXECUTED; diese Dimensionen dürfen nicht zu einem einzigen PASS verdichtet werden.

Validitätsklassen: (i) Syntaxwellformedness (erst in ML-C20 formal parserbar), (ii) Typ- und Referenzkorrektheit, (iii) lokale semantische Konsistenz, (iv) globale Erfüllbarkeit (im Allgemeinen nicht automatisch entscheidbar), (v) wissenschaftliche Implementierungskonformität (separat, ML-C21+). Nicht ermittelbar bedeutet UNKNOWN, nicht PASS.

## Versionierte Quellen
- mathspec canonical source und Tests: https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/_canonical.py ; https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/tests/test_canonical.py
- GEMS Library/Port: https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/library.md
- OMG: https://www.omg.org/spec/SysML/2.0/Language/PDF ; https://www.omg.org/spec/KerML/1.0/PDF
