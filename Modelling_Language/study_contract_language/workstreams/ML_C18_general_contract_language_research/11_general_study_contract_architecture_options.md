# ML-C18 / 11 – Minimal General Study Contract Architecture Options

**Status:** vergleichende Forschungsarchitektur, 2026-11-20; **keine DSL-/Parser-/Softwarearchitekturentscheidung**. A/B/C-Bezeichnungen unten sind neue Architekturhypothesen und mit ML-C17 Architektur A/B/C nur auf Konzeptebene verwandt. Anforderungen und Metriken ML-C18/01–02 sind das vorrangige normative *Forschungsprüfschema*, nicht eine normative Branchenbaseline.

## 1 Minimaler fachlicher Bedeutungsvertrag (keine implizite Algebra)
Kernfrage F1/F15: Kann ein Contract für *Studie, Teileigenschaften und Beobachtung* mit einer kleinen Mengenstruktur beschrieben werden, während ausführbare mathematische Specs optional und austauschbar bleiben?

Die minimale vorgeschlagene Rollenstruktur umfasst **sechs bis neun semantische Rollenfamilien** (nicht bewiesene Anzahl):
1. `StudyContext`: Zweck, Scope (System, Zeit, Raum, Szenarien, Vergleichsvarianten, referenzierter Studienfall) und explizite source authority.
2. `Rule`: getypte Aussage mit `subject`, `predicate`, `guard`, `status` (required/prohibited), SourceAssertion; verschiedene Prädikatprofile (physics, data, process, service) optional.
3. `Interface`: Component role, Port (carrier, connection, flow direction, unit/sign, time), typed relationships und beobachtbarer Dienst. Interface/behaviour als spezialisiertes Rule-Profil, nicht eigenständige Optimierungs-Model Library.
4. `VariationPolicy`: permitted/implementation-defined and disclosure obligations plus equivalence vs allowed non-equivalence classification.
5. `Observable` / `ResultMetric`: codierte Bedeutung, Einheit, Aggregation, Projektion, Vergleichsbasis.
6. `VerificationRequest`: Predicate/Oracle/Claim/EvidenceIdentity/TestOutcome/Limit mit getrennten Status.
7. `DecisionStatus` / `AuthorityReference`: source/version/owner/TBD blocking, policy applicability.
8. optional `DataFlow/TransformationReference`, falls Input-Verarbeitung und Ergebnisprovenienz sonst nicht semantisch geschlossen werden können.
9. optional `ComparisonPlan`: R1–R4, Input harmonization, study alternatives, independence ledger, result-ranking rules.

**Hypothese nicht mit Datenklassenanzahl verwechseln.** Implementation kann Entity-Types, Tagged Unions, Records oder Profile verwenden. Nicht alles muss in einer einzigen Dateisprache erscheinen. Die erforderliche `Unit/Carrier/Time`-Semantik ist dagegen Querschnittsvoraussetzung, egal wie sie kodiert wird.

## 2 Ebenen A–E des Auftrags und sparsame Zusammenfassung
| Ausgangsebene | Minimal nötige Semantik | Mögliche Implementierung | Kann entfallen? |
|---|---|---|---|
| A Generic Study Contract | Context+Rules+Data+Output/Evidence | Kern | **Nein** für volle Study Specification |
| B Component Behaviour | Interface + Guard/Guarantee/Capability + Ledger | optional wiederverwendbares fachliches Component-Profil auf Kernregeln | Für rein ökonomische Studien ohne Komponentenverhalten ja; generische Sprache muss es aufnehmen können |
| C Modelling Freedom | VariationPolicy + categorized declaration | in den Rules und Profilen verwendbar | Nein für Ziel Z2, aber keine eigene Dateisprache nötig |
| D Multi-Model Comparison | ComparisonPlan + shared Observables + provenance | separates Studienprofil, gebunden an Kern | Für Single-model Studien optional; für Z3 nötig |
| E Mathematical Specification | optional volle formal-algebraische Spec | GEMS-/mathspec-Adapter/Subspec | **Nicht verpflichtend**; Einsatz nur bei explizit erforderlicher mathematischer Präzisierung |

Vereinfachungshypothese: **3 semantische Schichten**: (I) Study/Roles/External Obligations, (II) Variation/Verification/Observables, (III) optional Math/Tool Profiles. Diese sind *konzeptionelle Schichten*, kein Beschluss für drei Parser oder ein Monorepo.

## 3 Drei alternative Architekturen ohne Vorentscheidung
| | A – Modular Contract Registry | B – Integrated Typed Semantic Core | C – Federated Standards / Profiles |
|---|---|---|---|
| Fachliche Wahrheit | registry IDs, source/authority ledger, referenzierte Profile | konsistentes typed graph/AST für Study, Rules, Ports, Variation | gemeinsame Ontologie/Identifiers, fachliche Bedeutung in mehreren Views |
| Study+component | getrennte Study-, Interface-, Data-, Output-Profile | integrierte Rule-/Interface-/Observable-Knoten | SysML/ReqIF/JSON-schema/Semantic Views plus math adapters |
| GEMS-Reuse | Port-/Topology-View aus Modellbibliotheken adaptieren | GEMS-Adapter mappt native Library Ports auf externe typed Interface | GEMS als optionaler ausführbarer Komponenten-View |
| mathspec-Reuse | mathspec-typed MathProfile bei Bedarf, kein Kern | mathspec als optional typed subtree / invariant renderer | mathspec als mathematischer Fach-View |
| Benefits | Inkrementeller, kleiner Autoren-Scope und parallele Verantwortliche | Ein Ort für Type/Unit/Guard-Checks, weniger Semantikdrift | maximale Standardwiederverwendung im jeweiligen Kompetenzfeld |
| Costs | cross-profile joins, version tuple und Referenzfehler | AST-Versionsmigration, große Implementationskopplung | bidirektionale Adapter, semantische Verlustkontrolle, authority arbitration |
| Freedom | leicht austauschbare Math-Profile, wenn Registry-Facts unabhängig | kontrollierte Erweiterbarkeit ohne Zwang zur Variablenstruktur | Bibliothek-/Spec-Views leicht austauschbar, wenn Kernsemantik unverändert |
| Failure mode | references join wrong versions, lokale Checks übersehen Cross-Profile Widerspruch | interne DSL erstarrt zu einem Universalmodell | semantisch nicht rückholbare View-Exporte, doppelte Authorities |
| Reviewstatus | TEST_REQUIRED | TEST_REQUIRED | TEST_REQUIRED |

Eine *vierter Minimalalternative* – einen vollständigen mathematischen Modellstandard allein als Study Contract verwenden – ist ein relevanter Nullvergleich (Option D). Sie wäre **dann** geeignet, wenn die Studie tatsächlich nur eine feste mathematische Spezifikation verlangt und Varianten auf Engine-R1/R2 beschränkt sind. Bei verpflichtendem Z2/Z3 und zugelassenen verschiedenartigen Modellstrukturen müsste D um äußere Contract-Schicht ergänzt werden. Dies ist keine Abwertung von GEMS oder mathspec.

## 4 Präzision ohne Implementation Lock-in
**Required behaviour** kann als zeitbezogene Menge von Input-/Output-Historien plus Verlust- und Dienstwitness formuliert werden. Ein Satz von `p_grid(t)`-Grenzen allein ist bei Energieumwandlung kein hinreichender Batteriespeicher- oder H2-Vertrag; zusätzlich benötigt ein Contract Energie-/Stoffbilanzen, Anfang-/Endzustands- und Wirkungsgradsemantik und gegebenenfalls Mindest-Servicefähigkeit. Statt bestimmter `soc`-Variable könnten Validatoren eine verifizierbare Bilanzprojektion/Witness anfordern. Gleichwertige physikalische Verpflichtungen sind verbindlich; algebraische Darstellung ist flexibel.

**Freedom policy** enthält Wahlbereich, Dokumentation, Äquivalenzstatus und `additional_assumption` inkl. Auswirkung. Eine ausdrücklich erlaubte Variation darf `Required` nicht überschreiben. Systematisch testbar an RC01,RC02,RC03 und RC05.

**Modellvergleich** braucht gemeinsame Output-Bedeutung, nicht nur Spaltennamen: Einheiten, Aggregation, Zeit-/Szenariogewichte, Kostenbasis, Counterfactual und Observable projection. Zusätzlich getrennt Audit/Verification und Robustness-Report. Ein GEMS-katalogbasierter Output und eine mathspec `expression` dürfen denselben Shared Output befüllen, wenn Provenienz und Ableitung nachweisbar stimmen.

## 5 Sprach- und Validator-/Adapter-Grenzen
| Prüfklasse | Kern statisch? | Konkrete Zuständigkeit |
|---|---|---|
| Schema/Grammar/Reference | ja, nach Definition | generischer Contract-Validator |
| Unit, carrier, direction, scope/guard, version graph | ja, soweit formalisiert | generischer Validator + Fachprofile |
| Bewiesene physikalische Balance/Existenz von Servicewitness | teilweise; allgemeine dynamische Garantie nicht entscheidbar | synthetische Prüfung, bounded formal reasoning, native model proof |
| Konkrete Solver-/Model Library-Gleichung | ausdrücklich nicht im Pflichtkern | GEMS/mathspec/pypsa/etc. |
| Data preprocessing execution, source qualification | nein | Data Governance/ETL-evidence |
| Scientific validity, independent review | nein | fachliche Owner-/Reviewerrollen plus empirische Validierung |

## 6 Vergleichsentscheidungsregel
Keine gewichtete Summe ordinaler K01–K17-Werte. **Nicht kompensierbare Gates**: K02 external components, K03 freedom, K04 toolagnostic, K05 formulation, K06 diversity, K07 multimodel, K08 precise meaning, K09 checkability. Ein Kontrakt darf bei fehlenden Fällen `INSUFFICIENT_EVIDENCE` melden; definitive Ablehnung nur bei nachgewiesenem Konflikt. K16 Tooling maturity und K12 Minimality sind wichtig, können keine Verletzung der wissenschaftlichen Gates kompensieren.

**Vergleichbares Experiment für A/B/C/D:** Gleicher RC01 Storage mit zwei alternativen Zustandsmodellen, RC03 H2 mit Umwandlungsbasis, RC05 Angle/Cycle/PTDF, RC09 N2E CBA und RC10 multimodel. Darstelle die gleichen äußeren Rules und bewusst nichtäquivalente Optionen; synthetischer negativer Counterexample muss vom Core aufgefangen werden. Miss: mapped SLR coverage, semantischen Verlust, Zahl unnötiger interner Vorgaben, ungeklärte Rückfragen, erfolgreiche Parser-/Roundtrips, Aufwand menschlicher Autoren. Nur nach nativen Tests (mind. zwei externe Standardslices und zwei unabhängige Modellierer) ist ADR/Language decision readiness neu zu bestimmen.

## 7 Entscheidungsvotum
**ARCHITECTURE_DECISION_READINESS = DEFERRED**, **MINIMAL_GENERAL_CORE = 6–9 ROLE FAMILIES (UNPROVEN HYPOTHESIS)**, GEMS und mathspec **als wiederverwendbare optionale mathematische/graphbasierte Profile**, nicht stillschweigend zur normativen gemeinsamen Modellbibliothek erheben. Parser/Serializer/Serialisierung offen. Kein Merge oder Owner-Signoff. IoSN Gate G1 bleibt BLOCKED.