# ML-C17 — Modelling Language Maturity Assessment

**Stichtag:** 18.11.2026. **Frozen research baseline:** AlOussama/TYNDP_Products, ML-C08 Draft PR #51, Commit 8470add62fcbc7f39b1d90c0d5afdcee50ab811e. C01–C07 liegen als separate Draft-PRs vor. Nichtnormativ; AI-kritischer Review nicht personell unabhängig. **G1 BLOCKED.**

## 1. Forschungsfrage und Hauptergebnis

Eine IoSN-Spezifikationssprache soll die fachlichen Daten-, Prozess-, mathematischen und Outputverpflichtungen so präzise angeben, dass Entwickler verschiedener Energiesystemtools sie unabhängig implementieren können. Sie ist weder eine ausführbare Modellsprache noch ein Generator für das finale Energiesystemmodell. Vier Ebenen bleiben getrennt: (1) fachliche Anforderung, (2) sprachlicher Ausdruck, (3) Interpretation im Modellierungsframework, (4) Nachweis an echter Implementierung. ML-C17 prüft hauptsächlich (1) und (2), die konzeptionelle Brücke zu (3), nicht (3)/(4) in der Praxis.

**Hauptbefund:** Ein inhaltlich breit angelegtes und referenziell geschlossenes wissenschaftliches Contract-Konzept liegt vor. Die eindeutige, durchgehend formal typisierte und unabhängig lesbare **Sprache selbst** ist noch nicht vollständig spezifiziert oder validiert. Die 48 aktiven MA01-SR sind im Graph und in der Traceability vollständig referenziert, aber 48 vollständig formal ausgedrückte und durch Gegenfälle validierte Anforderungen sind **nicht nachgewiesen**. Dies ist INSUFFICIENT_EVIDENCE, kein mathematischer Unmöglichkeitsnachweis.

## 2. Maturity Model

Forschungsskala, noch keine Owner-Policy: L0 nicht beschrieben; L1 konzeptionell beschrieben; L2 fachlich/semantisch typisiert oder strukturiert; L3 konkrete vollständige formale Sprachdefinition mit nachvollziehbaren Positiv-/Negativfällen; L4 geeigneter echter Sprach-/Validierungsprototyp kontrolliert nachgewiesen; L5 für festgelegten Scope unabhängig extern geprüft. E0 keine, E1 Entwurfsdokument, E2 erneute strukturelle Prüfung, E3 lokaler Custom-Checker mit Mutation, E4 native Parser-/Formalsemantiktests, E5 unabhängiger externer Review. Qualität K0–5 und Reifegrad L0–5 sind nicht dieselbe Skala.

## 3. Reife nach zehn Dimensionen

| Dimension | Aktuell belegter Reifegrad | Evidenz/Unsicherheit | Nächste Level-Voraussetzung / Aufwand |
|---|---|---|---|
| Fachliche IoSN-Semantik | **L2** | R01 M01–M18 und P00–P17, C01 Konflikte, C08 D1–D6; Quellautorität weiter ungeklärt; E2/E1 | formale Wahrheitsbedingungen für alle RC und aufgelöste oder ausdrücklich getypte Owner-TBD; mittel bis hoch |
| Formales Sprachmodell | **L2** | C02 30 Invarianten, C02 528 Node/1323 Edge und logische Konzepte; nicht alle Math-Operatoren materialisiert; E2 | vollständige abstrakte Syntax, Typisierung und operative/denotative Operatorsemantik; hoch |
| Konkrete syntaktische Definition | **L1** | frühe R02 JSON- und C06 View-Mockups, keine gemeinsame ausreichend vollständige Grammatik; E1 | native, formal validierbare RC01–12-Fälle samt Fehlerbeispielen; mittel bis hoch |
| Typ- und Konsistenzregeln | **L2** | C02 INV01–30; C06 Custom-Checks; C17 20/20 Strukturprüfungen und 26/26 lokale Boolean-Fixtures; E2/E3 | Vollchecker für gebundene Variablen, Einheiten, Guards und mathematische Pflichtausdrücke; hoch |
| Mathematische Ausdrucksfähigkeit | **L2** | C02 M01–M18 als semantische Obligationen, C04 15+15 synthetische Arithmetik, keine native E04; E1/E3 | Operator-/Quantor-/State-/Objective-Kern, E-FEAS/E-OPT/E-OBS unter Annahmen; hoch |
| Praktische Einfachheit und Verständlichkeit | **L1** | Typzählung und S1–S3 vereinfachte Entwürfe, keine Leser-/Entwicklerstudie; E1 | ablationsbasierte Minimalitätsprüfung und tatsächliche Interpretationsmessung; mittel |
| Unabhängige Toolimplementierbarkeit | **L1** | D6-A und gedankliche PyPSA/Antares/Sienna-Interpretation, keine echten Entwickler/Native-Proben; E1 | formaler Implementer-Handover an zwei unabhängige Entwickler; hoch |
| Formale Validierungsfähigkeit | **L2** | Graph-Endpunktprüfungen, C06 135/135 und 24/24 Custom-Harness, C17 begrenzte lokale Tests; E2/E3 | einheitlicher Parser-/Typ-/Semantikchecker inkl. Mathematik und Mutanten; hoch |
| Standard-/Interoperabilitätsintegration | **L1** | dokumentierte Rollen von ReqIF/SysML/LinkML/SHACL/GEMS usw., keine native Standard-Parser-Roundtrips; E1 | zwei echte Standardparser/-serializer und bit-/semantikbezogener Diff; mittel bis hoch |
| Versionierung und Evolution | **L2** | source revision/authority und C06 8×3 Custom-Mutationen, keine praktischen Migrationen; E2/E3 | semantischer Änderungs-/Kompatibilitätsvertrag plus nachweisbare Migration/Invalidierung; mittel bis hoch |

Diese Level sind **maximal durch den jeweiligen Behauptungsumfang gestützte Forschungslevel**. Insbesondere L2 ist kein L3-Syntaxnachweis, auch wenn einzelne lokale Custom-Checks durchgeführt wurden.

## 4. Fünf voneinander unabhängige Reifeobjekte

| Objekt | Ergebnis |
|---|---|
| Wissenschaftliches Contract-Konzept | **L2 – semantisch strukturiert**, Autoritätsentscheidungen offen |
| Konkrete formal definierte Sprache | **L1 – Syntax/Operatorsemantik unvollständig** |
| Sprachvalidierungswerkzeuge | **L2 – begrenzte strukturelle und Custom-Validierung** |
| Eignung für zwei unabhängige native Toolimplementierungen | **L1 – reine Implementierbarkeitshypothese** |
| Normative Freigabereife | **NOT_EVALUATED / G1_BLOCKED** |

## 5. K1–K10: entscheidende Befunde

**K1:** Die 528/1323 Graphdatensätze sind keine 528 Sprachkonstrukte. 15 materialisierte NODE-Typen/14 Relationstypen bilden nur einen Teil des späteren Matheausdrucksraums ab. **K2:** 48/48 IDs sind tracebar, die Anzahl voller formaler Sprachrepräsentationen ist nicht belegt. **K3:** D2, UTC/Delta t, Assetrollen und P15 sind konzeptionell klar; Owner-TBD und Formalausdruck müssen sauber getrennt werden. **K4/K5:** Frameworkneutralität plausibel, aber nicht implementer-validiert. **K6:** mathematische Invarianten bekannt, getypte vollständige algebra-unabhängige Operatorsemantik fehlt. **K7:** Referenzielle Fehler und einige lokale Semantikfehler erkennbar, aber kein globaler DSL-Validator. **K8:** Versionstupel beschrieben, kein nachgewiesener Migrationsprozess. **K9:** Standards können Teilfunktionen abdecken, derzeit kein echtes verlustfreies Austausch-Experiment. **K10:** Source/Evidence/G1 getrennt, Freigaben nicht erfolgt.

## 6. F1–F12 — ausdrücklich beantwortet

| Frage | Ergebnis |
|---|---|
| F1 Reife | multidimensional L1–L2, **kein einziger sinnvoller Gesamtlevel** |
| F2 Metamodell | geeigneter Traceability-Forschungsgraph; Minimalität nicht bewiesen; vollständige Math-Expression nicht materialisiert |
| F3 Ausdruck | 48 SR referenziell; formales FULL = **INSUFFICIENT_EVIDENCE** |
| F4 Implementer-Lesbarkeit | Kernpflichten nachvollziehbar, Lücken und Owner-TBD erzeugen Fragen; unabhängiger Handover fehlt |
| F5 Toolunabhängigkeit | als Contract-Ziel logisch erhalten; praktisch an PyPSA/Antares/Sienna unbestätigt |
| F6 Fehlende Konstrukte | Quantor/Index/Timing, getypte Math/Projection, Zeit/Carrier, Guard, Stage und Status/KPI |
| F7 Vereinfachung | Fixture/Capability/Governance aus Sprachkern in Profile prüfbar; Physik-/Evidence-Typen nicht zusammenwerfen |
| F8 Standards | ReqIF: SR-Austausch; SysML/KerML: typisierte Systemrelationen; LinkML/JSON Schema/SHACL: strukturierte Daten/Validierung; mathspec/GEMS: Math-Kandidaten; BPMN/DMN: Prozess-/Entscheidungssicht; alles IoSN-spezifisch zu verifizieren |
| F9 A/B/C | A Profile/Resolver, B typed core/Migrationskopplung, C federated Views/Mappings; **kein belastbarer Gewinner** |
| F10 Kern | kleinster **plausibler** S2-Semantikkern, noch nicht minimalitätsbewiesen |
| F11 Forschung | vollständige Sprache + Negativtests, native Standardparser-Slices, minimality Ablation, echte Implementerinterpretation |
| F12 Später | Owner-Methodik-/Datenfreigabe, echte native Implementierung, Solver-/Tooltest, unabhängige Zertifizierung, G1 |

## 7. Neun Abschlusskategorien

CURRENT_LANGUAGE_MATURITY = L1–L2 je Dimension.
SCIENTIFIC_EXPRESSIVENESS = CONCEPTUALLY_BROAD; FULL_FORMAL_INSUFFICIENT_EVIDENCE.
SIMPLICITY_AND_MINIMALITY = NOT_DEMONSTRATED.
ENERGY_TOOL_SUITABILITY = PLAUSIBLE_DESIGN; NATIVE_HANDOVER_NOT_TESTED.
FORMAL_VALIDATION_READINESS = STRUCTURAL_PLUS_LOCAL_CUSTOM_ONLY.
REMAINING_LANGUAGE_GAPS = typed math/guards/state/output/versions (siehe Gap CSV).
RECOMMENDED_MINIMAL_LANGUAGE_CORE = CONDITIONAL_S2_RESEARCH_HYPOTHESIS.
ARCHITECTURE_DECISION_READINESS = ADR_DEFERRED.
NEXT_RESEARCH_STEPS = formalise, falsify, compare, handover (siehe Roadmap).

**Keine Architekturauswahl, keine neue Methodik, D1–D6 unverändert, alle 21 MD/CL offen, G1 BLOCKED.**
