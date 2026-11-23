# ML-C19/08 – Äquivalenzstufen E1–E5 und Modelling Freedom
Stand 2026-11-23, CSNF-R0. Grundsatz: sprachlich gleiche Darstellung, gleiche äußere Pflicht, gleiches beobachtbares Verhalten und äquivalente Optimierungsformulierung sind **unterschiedliche** Aussagen.

| Stufe | Aussage und expliziter Kontext | automatisierbar? | Negativbeispiel |
|---|---|---|---|
| E1 Syntactic Normalisation Equivalence | gleiche kanonische Strukturen unter identischer Schema/Rule/Registry-Version, im erlaubten Rewritefragment | Ja, wenn beide typkorrekt sind | 1 MW Injection vs Consumption |
| E2 Contract Semantic Equivalence | gleiche Pflichten, Normativitäten, Guards, Scope, Owners/Authority-relevanten Status; ggf. E2_obligation ≠ E2_audit | eingeschränkt (definierte endliche Logik), sonst proof obligation | REQUIRED vs PERMITTED; gleiche Pflichten mit unterschiedlichen Authoritäten ≠ auditidentisch |
| E3 Observational Equivalence | gleiche externe Trace/Output-Projektionen O im Scope S mit festgelegter Zeit-/Szenario-/Tol.-Semantik | Messbar auf begrenzten Fällen; universell oft nicht entscheidbar | ein optimales Beispiel hat gleiche Kosten, andere Verfügbarkeit |
| E4 Mathematical Formulation Equivalence | gleiche projections von feasible sets und Ziele/Präferenz unter H, inkl. Randbedingungen | nur mit separatem mathematischen Beweis oder begrenzten Benchmarks | KCL-only vs KCL+KVL; unterschiedliche Integer-Granularität |
| E5 Permitted Structural Non-Equivalence | M1 und M2 erfüllen denselben äußeren C, obwohl interne Strukturen/F1/F2 nicht äquivalent sind | Konformität prüfen, Nichtäquivalenz offenlegen; kein E4 erforderlich | verschiedene Units, ungenehmigte zusätzliche Datenannahme |

E5 ist terminologisch kein universelles mathematisches Äquivalenzverhältnis. Eine zulässige Modellabweichung bedeutet nicht, dass die Resultate numerisch identisch sind; gemeinsame Ergebnisdefinitionen erlauben ausdrücklich Robustheits-/Sensitivitätsunterschiede.

## Variationskategorien und nicht heimliche Modellrestriktion
Frei: interne Zustandskoordinaten (SOC vs MWh), Variable-/Constraintbezeichnungen, Primal/Dual-/PTDF-/Angle-Formen bei erfüllter fachlicher Netzpflicht, Modellbibliotheken, Algorithmen, Solver, Datenstrukturen, interne Modellkomposition, approximative numerische Verfahren **wenn** definierte Toleranzen und Nachweise erfüllt sind.
Bedingt frei: räumliche/zeitliche Aggregation, diskrete vs stetige Ausbauentscheidungen, nichtlineare vs lineare Umwandlungskennlinien, technische Reserve-/Availability-Approximation; nur nach expliziter VariationPolicy und Disclosure, erforderlichen Bounds und Evidence.
Nicht frei: Carrier, Port-Sign, aktiver Scope, verbindliche Energie-/Massenbilanz, KVL wenn fachlich REQUIRED, Informationszeitpunkt, Methodikquelle, Qualitätsanforderung, Transparenz/Provenienz, genehmigte KPIs und Vergleichsbaselines.

## Aggregation und generische Komponenten-Contracts
Ein aggregierter EV-Envelope erfüllt nicht automatisch jede individuelle Abfahrtsdeadline; for-all request / exists dispatch (Quantorenfolge) ist zu prüfen. Ein 3-Bus-Strommodell mit identischem KCL, aber verletztem KVL ist nicht E3/E4 für Branchflows. Bei H2 kann MWh_LHV und kg nur mit festgelegtem Heizwert und Referenzbasis gemappt werden. Ein Batteriemodell mit SOC und eines mit MWh-State können E2 der **fachlichen** Vertragsspezifikation teilen, ohne E4 für sämtliche internen Lösungsmengen zu erfüllen.

## Ergebnisvergleich und Multi-Model Robustness
ComparisonContract muss gemeinsam festlegen: study ID, model IDs/Abhängigkeit, input/scenario snapshots, ObservableDefinitions, Gewichtung, Bezugsjahr, Toleranzen, Auswahl aus Mehrfachoptima, Variationsregister, R1–R4-Prüfprotokoll, Evidence und Entscheidungsschwellen. Kein E4-Label aus gleichen KPIs vergeben; keine strukturelle Varianz als Solverdifferenz umetikettieren. Unterschiedliche Implementierungen dürfen bei demselben Outer Contract verschiedene wissenschaftlich plausible Ergebnisverteilungen liefern; Robustheit ist gerade der Gegenstand der Untersuchung.

## Zentrale Prüflogik
Static normalization -> E1 label, mandatory type/unit/ref/status checks.
Contract obligation comparison -> E2_proved, E2_different oder E2_unknown.
Result/projection comparison -> E3_sample_checked mit Scope und Datensatz; niemals universal ohne Beweis.
Math proof -> E4_proved_under_H separat; sonst E4_not_proved.
Conformance -> C_pass / C_fail / C_inconclusive; E5_permitted nur wenn VariationPolicy, Disclosure und Evidence erfüllt.
**NOT_EXECUTED** und **OWNER_TBD** sperren positives wissenschaftliches Nachweisvotum, werden nicht mit FAIL gleichgesetzt.

## Quellen
[mathspec canonical](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/_canonical.py), [GEMS Library](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/library.md), [SysML Part 1](https://www.omg.org/spec/SysML/2.0/Language/PDF), [ML-C18 RC/07](https://github.com/AlOussama/TYNDP_Products/blob/5555be36f74d1d4f6e871d4503c1fc91e417e57c/Modelling_Language/study_contract_language/workstreams/ML_C18_general_contract_language_research/07_reference_case_language_experiments.md).
