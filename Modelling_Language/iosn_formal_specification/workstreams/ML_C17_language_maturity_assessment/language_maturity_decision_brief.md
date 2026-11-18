# ML-C17 — Language Maturity Decision Brief

**Für die Projektleitung, nichtnormativer Research Decision Support, 18.11.2026.** Source frozen ML-C08 PR #51 @ 8470add62fcbc7f39b1d90c0d5afdcee50ab811e; separater ML-C17 Branch. Keine Methodik-, Data-, Sprach- oder Toolfreigabe. **D1–D6 unverändert, alle 21 MD-/CL-Ownerfragen offen, Gate G1 BLOCKED.**

## 1. Neun verpflichtende Abschlussvoten

| Thema | Urteil | Nachweis und Konsequenz |
|---|---|---|
| CURRENT_LANGUAGE_MATURITY | **L1–L2 je Dimension**, nicht als Gesamtzahl zusammenführbar | Fach-/Meta-/Typkonzept L2; konkrete Syntax/Usability/Independent Implementability L1 |
| SCIENTIFIC_EXPRESSIVENESS | **CONCEPTUAL_PARTIAL; FULL_FORMAL_INSUFFICIENT_EVIDENCE** | 48/48 Requirements referenziell, 0 native vollständige SR-Ausdrucksnachweise; M01–M18 logisch, Operator-/Projection-Semantik offen |
| SIMPLICITY_AND_MINIMALITY | **MINIMALITY_NOT_PROVEN** | 528 NODE,1323 EDGE = Instanzgraph, nicht Sprachumfang; 15 NODE-Typen/14 Prädikate; S1/S2/S3 vorgeschlagen, keine Ablation durchgeführt |
| ENERGY_TOOL_SUITABILITY | **DESIGN_PLAUSIBLE / ACTUAL_HANDOVER_NOT_TESTED** | gleiche Pflichten in PyPSA, Antares und Sienna konzeptionell interpretierbar; native Capability/Implementation kann offen oder UNSUPPORTED bleiben |
| FORMAL_VALIDATION_READINESS | **PARTIAL_STATIC_CUSTOM_ONLY** | 20/20 C17 Source-Strukturchecks, 26/26 atomare Boolean-Micro-Fixtures; C06 135/135 und 24/24 prior Custom-Harness, keine native Standardparser-/Math-Validator-Evidenz |
| REMAINING_LANGUAGE_GAPS | **P0 TYPED_MATH_GUARDS_OUTPUTS + P1 INTEROP_EVOLUTION** | 24 Gap-Register-Einträge getrennt nach Sprachdesign, Owner, Daten, Tool und experimenteller Evidenz |
| RECOMMENDED_MINIMAL_LANGUAGE_CORE | **CONDITIONAL_S2_SEMANTIC_CORE** | source-linked Requirements, typed Scope/Case, Rollen/Carrier, Data/Transform, Math/Equivalence, Outputs, Oracle/Evidence/Unknown; keine verbindliche DSL |
| ARCHITECTURE_DECISION_READINESS | **ADR_DEFERRED** | A modular, B integrated, C federated: gleiche custom C06 Ergebnisse; keine native semantische/Usability-/Migrationsdifferenzierung |
| NEXT_RESEARCH_STEPS | **TARGETED_LANGUAGE_RESEARCH_FIRST** | Typ-/Operatorsprache, RC-/Mutations-Harness, zwei echte Standardslices, unabhängiger Implementer-Handover, Versiondiff/Ablation |

## 2. Architekturvarianten: entscheidungsrelevante Unterschiede, keine Rangfolge

**A — Modulare Registry:** unabhängige fachliche Profile und kleinere Autorendomänen, aber Cross-Profile-Resolver, Versionstupel, Nachschlagen und potenziell höhere Leselast. **B — Integriertes typisiertes Metamodell:** zentrale Konsistenz/Operatorbibliothek und geringe semantische Fragmentierung, aber AST-Evolution und Änderungskopplung. **C — Föderierte Standard-Views:** Wiederverwendung von ReqIF/SysML/LinkML/SHACL/mathspec/GEMS/BPMN usw. im jeweiligen Stärkebereich; aber echte Adapter, Verlustfreiheit und genau eine semantische Autorität erforderlich. S2 als gemeinsamer abstrakter Semantikkern ist mit A, B und C vereinbar und **keine Auswahl B**.

Die Ordinalscores der CSV sind **konzeptionelle Qualitätsannahmen** und nicht addierbar. Sie wurden getrennt von Evidenzstärke erhoben. Keine Gesamtwertung oder Gewichtung, weil eine gute K1-Einfachheit niemals Verletzungen von K2/K3/K6/K7 kompensieren darf.

## 3. Entscheidungsfragen

**Darf eine Spracharchitektur jetzt verbindlich ausgewählt werden? Nein.** Ein konkreter S2-Contract muss mindestens dieselben 48 SR und 12 RC in einer wirklichen formal getypten Grammatik darstellen und negative Bedeutungsverlustbeispiele korrekt erkennen. Für die später in Frage kommenden Standards sind mindestens zwei native Parser-/Serializer-Roundtrips einschließlich einer bewusst verlustbehafteten Negativprobe notwendig. Ein qualifiziert unabhängiger Implementer sollte aus dem Contract die scientific obligations ableiten können, ohne nichtdokumentierte Fachannahmen.

**Was kann vor den Ownerfreigaben weiter erforscht werden?** Die Grammatik, Typ-/Guard-/Unit-Regeln, die mathematische Ausdruckssprache, synthetic negative cases, semantische Changes und nativen Standardslices mit klaren Forschungsprofilen. Reale IoSN-Daten, Solver-End-to-End und Toolzertifizierung sind weder Voraussetzung noch Bestandteil des gegenwärtigen Sprachreifeschritts.

**Was bleibt Owner-/Data-/Toolsache?** MD-01 effective Methodology, D2 numerische Gewichte/Casequellen, MD-07 Stage-F_y, MD-12 Zeitachsen-/Toleranzdetails, Netz-/N−1-/H2-Provenienz und KPI B01-D081, Realdaten, echte Solvermodelle und Native-Frameworkunterstützung. Die Sprache muss explizite TBD und BLOCKED Semantik haben statt erfundene Defaults.

## 4. Bedingte Forschungspräferenz

**S2 – Minimal Complete Scientific Contract als zu testende Designhypothese.** Beginne mit einer klein gehaltenen kanonischen **Bedeutungsdefinition**, nicht einem vorentschiedenen zentralen Technologie-B-AST. Führe A/B/C über denselben 12er-Referenzfallkatalog und die gleiche SR-Traceability. Erweise vollständige fachliche Ausdruckskraft mit Negativfällen, ehe über die physische Architektur, DSL oder Standards entschieden wird.

Das ist **kein** normativer Architektur-, Sprach-, Methodik- oder Datenbeschluss. Die interne kritische Gegenprüfung ist kein personell unabhängiger Audit. **G1 bleibt BLOCKED.**
