# ML-C18 / 13 – Language Research Decision Brief
**Datum:** 2026-11-20. **Status:** nichtnormative, konditionale Forschungsempfehlung. Baselines: GEMS `9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a`; mathspec `5f1464c334c1012cdee2947d4d55b4d1d6bef40a`; ML-C17 `c8bbedad390d0ba00604a0f499e79e9cff087138`. Requirements/metrics ML-C18/01–02 waren **vor** dem Scoring eingefroren.

## Executive research conclusion
Die drei Ansätze sind **nicht dieselbe Art von Sprache**. GEMS ist für die graphorientierte Zusammensetzung mathematischer Energiesystemmodelle stark, mathspec für klar definierte, engineübergreifende mathematische Semantik und statische Validierung; ML-C17 für source-linked fachliche Anforderungen, methodische Scopes und Owner-/Evidence-Ungewissheit, aber bisher weitgehend konzeptionell. Die **allgemeine Study Contract Language** muss eine solche fachliche Ebene bewahren und optional spezifischere Math-Specs akzeptieren. Es gibt aktuell **keinen** belastbaren Nachweis, dass GEMS, mathspec oder der bisherige Kern allein K02–K09 vollständig erfüllen. Keine pauschale Rangliste und keine verbindliche Architekturfestlegung.

## Tabelle A – Vollständiger Vergleich nach K01–K17
**Legende:** `Q/E` = Qualitätsurteil 0–5 / Evidenzklasse E0–E5. `NE` = NOT_EVALUATED. Heuristische qualitative Ordinalscores, keine statistische Messung oder additive Gesamtbewertung. Sie bewerten *Eignung für einen allgemeinen Study Contract*, nicht die allgemeine Qualität als mathematische Sprache. Details und Belege: `06_gems_mathspec_comparative_evaluation.csv`, `03`, `04`, `08`.

| Kriterium | ML-C17 | GEMS | mathspec | Entscheidende Einschränkung |
|---|---|---|---|---|
| K01 | 3/E2 | 2/E2 | 2/E2 | Whole-study scoping ML-C17 concept; tools chiefly optimization models |
| K02 | 2/E2 | 3/E2 | 2/E2 | GEMS port interface valuable; no formally enforced general A/G external contract |
| K03 | 3/E2 | 2/E2 | 2/E2 | Freedom intent vs mandatory algebra inside a shared library/spec |
| K04 | 3/E2 | 2/E2 | 3/E3 | mathspec semantics engine-independent but not study-framework-independent by itself |
| K05 | 3/E2 | 2/E2 | 2/E2 | Alternative independent files/libraries, not arbitrary algebra within a fixed spec |
| K06 | 3/E2 | 3/E2 | 3/E2 | Multiple models possible; independent scientific substitution not proven |
| K07 | 2/E2 | 2/E2 | 2/E2 | No native R1-R4 shared conformance/robustness contract shown |
| K08 | 2/E2 | 3/E2 | 4/E3 | mathspec has defined operator/reference/index AST and tested errors |
| K09 | 2/E2 | 2/E2 | 4/E3 | Existing mathspec CI passes pytest; not component scientific validation |
| K10 | 3/E2 | 3/E2 | 3/E2 | Energy examples and profiles, H2/EV cross-domain obligation needs extensions |
| K11 | 3/E2 | 3/E2 | 2/E2 | C17 data/process evidence, GEMS output Views; mathspec data assumptions |
| K12 | 2/E2 | 3/E2 | 3/E2 | Minimality and authoring cognitive effort untested |
| K13 | 3/E2 | 3/E2 | 4/E3 | GEMS Libraries/Taxonomy; mathspec given/merge/override confirmed |
| K14 | 2/E2 | 3/E2 | 4/E3 | Tool import/export and semantic roundtrips for Study Contract untested |
| K15 | 3/E2 | 3/E2 | 3/E2 | Source authority vs software versions; Owner governance external |
| K16 | 2/E2 | 3/E2 | 4/E3 | GEMS current checked workflow E2E skipped; mathspec CI tests passed |
| K17 | NE/E0 | NE/E0 | NE/E0 | No controlled independent modeler authoring task |

**Gates:** K02–K09 sind wissenschaftliche Mindestpflichten und nicht kompensierbar. E2 und E3 bedeuten nicht E4/E5. Der bei mathspec bestehende E3-Nachweis betrifft tatsächliche ursprüngliche Sprachteests und CI, **nicht** ML-C18-RC-Durchläufe. GEMS vorhandene E2-Quellen plus externe Laufzeittools, beim geprüften SHA CI-E2E skipped. Der ML-C17 Ansatz besitzt den beabsichtigten Scope, aber keine native umfassende Grammatik/Parser-Evidenz.

## Tabelle B – Stärken, Grenzen und Zielerfüllung
| Kategorie | ML-C17 bestehender Kern | GEMS | mathspec |
|---|---|---|---|
| Wissenschaftliche Stärke | Methodikgebundene, quellengestützte Verpflichtungen/Ownerstatus; Input-Process-Output-Verification | Explizite Energienetzmodellkomposition, konkret formulierte physikalische Modelle | Eindeutige mathematische Ausdruckssemantik mit typed indices/operators |
| Technische Stärke | Nachvollziehbarer C02-Graph, strukturierte eigene Microtests, traceability | Versionierte YAML Model Libraries, bestehende Simulationstudien/E2E-Dateien, Antares/GemsPy | Pydantic/parser/AST/composition/typesetting, Repo-CI pytest success |
| Sprachliche Stärke | Trennung von Requirement/Scope/Unknown/Evidence als wissenschaftliche Bedeutung | Typisierte Ports und graphorientierte Komposition, Library/System-Trennung | Strict source checks, variable/reference/degree rules, `given`, `merge`, `override` |
| Z1 Toolagnostik | **DESIGN_INTENT, not proven** | kompatibel mit Enginefamilie, aber GEMS-spezifisches Modellformat | engineübergreifende mathspec-Bedeutung, aber mathspec-spezifische Programsemantik |
| Z2 Modelling Freedom | ausdrücklich gewollt, formal noch unzureichend | durch **alternative Libraries** möglich, gemeinsame Library bindet Algebra | durch **alternative Specs** möglich, einzelne Spec bindet Algebra |
| Z3 Multi-Model Robustness | offene Vergleichsebene, Evidence-Rollen nur teilweise | Outputs, Views und mehrere Modellbibliotheken, aber kein gebundener R3/R4-Contract | Program/expressions + comp. ermöglichen Vergleichsteile, aber kein äußerer R3/R4-Contract |
| Grenzen | Nichtgeparste S2-Grammatik, unbewiesene Minimalität, IoSN-Überhänge | kein nachgewiesener allgemeiner A/G Contract, Pflicht zur spezifischen Algebra je Library, externe Interpreter | keine native physikalische Port-/A/G-Semantik, Objective/Constraint-Bindung, Data-assumptions nicht Behaviour |
| Offene Forschungsfrage | Kann kleiner Kern wirklich UC1–3 und RC01–10 ausdrücken? | Sind semantisch gleiche Ports verschiedener Libraries unabhängig prüfbar und native parsbar? | Können mehrere mathspec-Dateien unter einem äußeren Contract interagieren, ohne die interne Form festzulegen? |

## Tabelle C – Wiederverwendbare Fähigkeiten und bewusst vermiedene Einschränkungen
| Fähigkeit | GEMS | mathspec | Unser Kern | Direkt reuse? | Adaptieren / nicht übernehmen / Freiheit erhalten |
|---|---|---|---|---|---|
| Study-/Model-Kopplung | Graph-System + versionierte Modellbibliotheken | Mathematisch typisierte Spec mit eigenständiger Engine | Source-linked Study/Requirement/Verification-Konzept | Adapter / externe Schema-Referenzen | Gemeinsamen Studienzweck und Model-Library-Bindings entkoppeln; **vermeiden:** Kein kompletter GEMS/mathspec Modellgraph als Pflichtkern |
| Getypte externe Ports | Port types, port fields, binding constraints | Relations können Topologie mathematisch codieren | EnergyObjectRole; keine vollgetypte Port-Behavior-Semantik | GEMS-Ports als Designvorbild | PortCarrier+Unit+Direction+Sign+Time und Verhaltens-Guards; **vermeiden:** Porttyp ≠ Energiebilanzbeweis |
| Fachliches Verhalten und A/G | Constraints/Binds als konkrete Mathematik | Conditions, assumptions (für Daten), Constraints | Rules/Scope/Unknown semantisch skizziert | Partial semantic patterns | Externe Garantien, Servicefähigkeiten, Witnesses getrennt von Datenannahmen; **vermeiden:** mathspec data assumptions nicht als A/G umbenennen |
| Modellierungsfreiheit | Verschiedene model libraries möglich | Verschiedene Specs/Fragments möglich | AllowedFreedom Forschungsbegriff | Getrennte Alternativmodelle | VariationPolicy mit Erlaubnismengen/Disclosure/EquivalenceLabel; **vermeiden:** Gemeinsame Variablen-/Constraintfamilien nicht vorgeben |
| Typ-/Indexsemantik | Zeit-/Szenario-Entfaltung, dokumentierte Grammatik | Dimensions, relations, typed operators AST | Typed scopes als S2-Hypothese | mathspec semantic principles | Carrier/Unit/Time als unabhängige Pflichtsemantik; **vermeiden:** Nicht alle mathematischen Operatoren in Kern importieren |
| Kompakter Formal Validator | Interpreterabhängige Validierung und Taxonomy checks | Pydantic strict schema, resolution, negative unit tests | Custom source/structural checks, kein universeller parser | Fehlermeldungs-/Testmechanik mathspec | Contract-owned static Rule/Unit/Guard/Ref checks + negative suite; **vermeiden:** Parser PASS ist nicht wissenschaftliche Konformität |
| Multi-Model Vergleich | Views/Catalog und native component outputs | Named expressions/typeset/math programs | RawResult/MetricDefinition/Evidence identities | Canonical Observable mapping | KPI Projection, unit, aggregation, base and variance attribution; **vermeiden:** Gleicher Spaltenname ersetzt keine KPI-Definition |
| Komposition | Versionierte Libraries, Taxonomy | given, merge, override, rename, macros | A/B/C profilesource registry, typed relation | mathspec composition patterns | Explicit overrides, owner precedence, source provenance, conflict detection; **vermeiden:** Override darf REQUIRED nicht stillschweigend ändern |
| Absence/TBD | GEMS data configs versioned | missing: absent/0/refused, optional where | OwnerTBD/NOT_EXECUTED/STATUS getrennt | mathspec missing-data semantics | Domain-specific typed unknown/status ledger; **vermeiden:** TBD ≠ zero ≠ N/A |
| R1-R4 Robustheit | Engine-/Solver-abhängige Simulationsresultate | Eine mathematische Spec für mehrere Engines, mehrere Specs möglich | IoSN C17 evidence framework, noch kein Robustheit-Protokoll | GEMS+mathspec als optionale Implementierungsprofiles | Unabhängigkeits-/Variation-/KPI-Register und alternative Modellfamilien; **vermeiden:** Gemeinsame Library nicht als unabhängiger Modellnachweis |

Technisch genaue Wiederverwendungsentscheidung mit Status, SHA, SLR und Next proof: `09_reuse_opportunities_and_design_gaps.csv`.

## F1–F15 – ausdrückliche Forschungsantworten
| Frage | Evidenzgebundene Antwort / Grenze |
|---|---|
| **F1** | Minimal: versionierter StudyContext, Rule+Guard+Source, Component Interface/Behavior, VariationPolicy, Observable, Verification/Evidence, DecisionStatus; Data/Process/Comparison als Profile. 6–9 Rollenfamilien sind **ungetestete** Designhypothese. |
| **F2** | Extern verpflichtend: Ports inkl. Carrier/Unit/Sign/Point/Time, verbindliche Betriebs- und physikalische Energie-/Stoffbilanzen, Services/Verfügbarkeiten, Initial-/Terminal-Verhalten, Assume-Guarantee Guards und Prüfwitnesses. |
| **F3** | Interne State-Coordinates, Variablen-/Constraintfamilien, Linearisierungsansatz soweit physikalisch erlaubt, Granularität innerhalb nachgewiesener Außenfähigkeit, Algorithmen, Engines und Solver. |
| **F4** | GEMS: versionierte Graph-/Model Libraries, Port-Felder, Binding Constraints und Output-Kataloge; mathspec: strict typed mathematical spec, operators, indexes, compositional grammar, tests+CI. |
| **F5** | Eine normierende GEMS-Model-Library oder ein gemeinsames konkretes mathspec variables/constraints/objective-Schema würde unnötig alle Modelle auf festgelegte Algebra festlegen; Engine-spezifische stage/solver settings ebenso. |
| **F6** | GEMS: Komponentengraph und Port-/Library-Konzepte; mathspec: language/engine boundary, typed indices, named conditions, absence, composition, strict static validation, typesetting; C17 source/owner status. |
| **F7** | Ein versionierter AußencContract `C` mit gemeinsamen Required Behaviors und unabhängigen `M_i -> C`-Mappings. Nachweise der individuellen guarantees und definierte VariationPolicy, nicht identische interne Algebra. |
| **F8** | R2 nachweisbare Feasible-/Objective-Projektion unter begründeten Annahmen; R3 ausdrücklich erlaubte strukturelle Nichtäquivalenz mit individuelles A/G Conformance und erklärbaren Ergebnisunterschieden. |
| **F9** | Identische KPI-Definitionen, System-/Kosten-/Zeit-/Szenario-/Einheitenbasis, sign, inflation, aggregation, counterfactual und geprüfte Outputprojektionen, mit eindeutiger Evidenz und missing status. |
| **F10** | R1 Residuen/Mehrfachoptima; R2 Implementationsabweichungen; R3 structure effects; R4 Ergebnis- und Maßnahmenrankingstabilität; nur innerhalb des registrierten Modellspektrums, nicht als Wahrheitsbeweis. |
| **F11** | C17 SourceAssertion, Requirement, Scope/Applicability, Data-/Process-/ResultDefinition, VerificationRequest, Unknown und typed provenance relations sind generell nutzbar. |
| **F12** | IoSN SR-, P00–P17-, CY1–CY5-, Netzwerk-/Investitionsregeln in Profile, Graphinstanzen nicht zu Grammatikklassen machen; ergänzen typed Port/G/A, VariationPolicy und ComparisonContract. |
| **F13** | Nicht nachgewiesen. Beide Sprachen lassen alternative Modelle/Specs zu, aber native general Study Contract/structured permitted freedoms/R3/R4 werden in geprüften Quellen nicht als vollständiger Parser-Workflow belegt. |
| **F14** | Eine *eigenständige äußere Bedeutungsschicht* ist vorläufig fachlich plausibel, eine neue eigenständige DSL/Parser-Implementierung noch **nicht** begründet. Adapter zu bestehenden Systemen zunächst prüfen. |
| **F15** | Forschungspräferenz: kleiner semantic interface/Rules/Scope/Observables/Variation/Verification-Kern mit optionalem Math-Profil und getrennten A/B/C-Architekturimplementierungen; ADR erst nach native RCs und unabhängiger Interpretation. |

## Abschließendes 12-teiliges Votum
| Entscheidungsdimension | Ergebnis / Status |
|---|---|
| `GENERAL_STUDY_CONTRACT_REQUIREMENTS` | **PROPOSED / 42 SLR CANDIDATES**; notwendige fachliche Pflicht + Output- und Serviceprojektion, nicht normativ |
| `GEMS_LANGUAGE_STRENGTHS_AND_LIMITATIONS` | **STRONG_MODEL_COMPOSITION; OUTER_CONTRACT_PARTIAL**; Library-/Port-Reuse, A/G extern |
| `MATHSPEC_LANGUAGE_STRENGTHS_AND_LIMITATIONS` | **STRONG_FORMAL_MATH; OUTER_CONTRACT_PARTIAL**; AST/validation gut belegt, Mathematik je Spec festgeschrieben |
| `EXISTING_CONTRACT_GENERALIZABILITY` | **CONCEPTUAL_PARTIAL**, generische Source/Scope/Rule/Verification, noch nicht technisch vollständig |
| `COMPONENT_BEHAVIOUR_CONTRACT_SUITABILITY` | **DESIGN_PLAUSIBLE / NOT_NATIVE_VALIDATED**, Energie-/Stoff-/Service-Witness nötig |
| `MODELLING_FREEDOM_PRESERVATION` | **POLICY_DEFINED_HYPOTHESIS**, Unterschiede zwischen R2 und R3 ausdrücklich bewahren |
| `MULTI_MODEL_ROBUSTNESS_SUITABILITY` | **PROTOCOL_PREPARED / RESULT_NOT_MEASURED**, R1–R4, no automatic validity |
| `REUSABLE_GEMS_AND_MATHSPEC_CAPABILITIES` | **SOURCE_MAPPED / ADAPTER_TEST_OPEN**, konkret in 09 |
| `DESIGN_LIMITATIONS_TO_AVOID` | **IDENTIFIED**, kein Pflichtmodell, keine Toolvariablen, kein bloßer Port mit Blackbox |
| `MINIMAL_GENERAL_LANGUAGE_CORE` | **6–9 ROLE FAMILIES RESEARCH_HYPOTHESIS**, keine bewiesene Untergrenze |
| `ARCHITECTURE_DECISION_READINESS` | **DEFERRED / INSUFFICIENT_EVIDENCE**, keine DSL-/Architecture ADR |
| `PRIORITISED_NEXT_RESEARCH_STEPS` | **P0 NATIVES + NEGATIVES + UNIT/PORT SEMANTICS; P1 REUSE/ROUNDTRIP; P2 AUTHORS/ADR**, Details 14 |

## Bedingte Forschungsempfehlung
Vorläufig bevorzugte **Test-Hypothese** ist eine schlanke, toolneutrale *fachliche Außensemantik* mit generischen Context/Rules/Ports/Observables/Variation/Verification und optionalen, austauschbaren GEMS-/mathspec-Mathematik-/Engineprofilen. Damit ist **nicht** entschieden, ob diese Semantik in einer neuen DSL, als GEMS-/mathspec-Erweiterung, als integriertes Metamodell oder als föderierte Standardsicht implementiert werden soll.

**Falsifizierende Entscheidungsbedingung:** Wenn ein einzelner bestehender Standard durch eine minimal kontrollierte Erweiterung gleiche RC01–10 / UC1–3 / K02–K09-Vollabdeckung, semantische Roundtrips und nachweisbar erhaltene Strukturvariation bei geringerem Autoren- und Governanceaufwand demonstriert, soll **dieser** Standard wiederverwendet werden statt eine neue DSL zu entwickeln. Umgekehrt rechtfertigen dokumentierte irreduzible Ebenengrenzen eine separate äußere Contract-Bedeutung, **nicht automatisch einen neuen Parser**.

## Governance
`D1–D6 = UNCHANGED`; `MD/CL = OPEN`; `IoSN Gate G1 = BLOCKED`. Keine normative CBA-Methodik angenommen; N2E authoritative source `NOT_IDENTIFIED`. Ein KI-interner kritischer Review ist keine unabhängige personelle Freigabe.