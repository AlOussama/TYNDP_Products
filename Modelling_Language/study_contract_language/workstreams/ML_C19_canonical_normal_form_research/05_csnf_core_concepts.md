# ML-C19/05 – Minimaler CSNF-Kern, Forschungsmodell v0.1
Stand 2026-11-23. **Nichtnormative Kernhypothese**, keine DSL, kein Serialisierungsformat, keine Engine-API.

## 9 Kandidaten-Rollenfamilien, keine Behauptung mathematischer Minimalität
| Kernrolle | Identität, Attribute, Beziehungen | Generische Pflicht |
|---|---|---|
| C1 ContractFrame | contract_id, schema_version, normalization_version, study_question, boundaries, time/scenario/counterfactual | Studienfrage, Universum und gemeinsame Bezugsbasis |
| C2 Referent | stable_id, kind, type_ref, role, measurement_type, scope_ref | ComponentRole, Port, Dataset, Process, Scenario, Resource, Owner, Source und Result als **getypte Instanzen** statt 8 getrennte Kernklassen |
| C3 TypedRelation | kind, from_ref, to_ref, role, cardinality, provenance_ref | connected_to, uses, derives_from, satisfies, verifies, member_of, supersedes, valid_for |
| C4 Predicate | typed operator tree, operands, explicit unknown semantics, dimensional annotations | Guards, Invarianten, Leistungs- und Serviceprädikate, KPI-Bedingungen; keine vordefinierten Optimierungsvariablen |
| C5 ScopedAssertion | modality, semantic_role, predicate_ref, applicability_ref, assumptions, guarantees, authority_links | REQUIRED, PROHIBITED, PERMITTED, CONDITIONALLY_REQUIRED; data assumption vs behavioural guarantee vs capability |
| C6 ObservableDefinition | target, projection, kind, quantity/unit/sign, temporal/spatial/scenario aggregation, tolerance/selection | äußerlich beobachtbarer Trace/KPI mit vollständiger Berechnungssemantik |
| C7 VariationPolicy | choice_set, status, extra_assumptions, disclosure_required, constraint_source, proof_duty | interne Freiheit, zulässige Nichtäquivalenz und Ausnahmen ohne Default |
| C8 EvidenceRecord | request/evidence/outcome discriminator, subject_ref, oracle, level, test_input, run_id, status | Nachweisanforderung von tatsächlich ausgeführter Prüfung trennen |
| C9 AuthorityRecord | source/owner/decision/provenance discriminator, immutable_source_ref, version, approval, decision_state | Quellautorität, Entscheidungsstand, Unknown, Origin-IDs, Audit Trail |

Kompakte **Value Types**, keine zusätzlichen Referentklassen: Scope=(space, time, scenario, subject, guard); QuantityType=(physical_kind, dimension, unit, reference_basis, sign, temporal_support); TimeAxis=(timezone, sampling, interval_convention, duration, weights); ScenarioInfo=(tree, probabilities, information_sets); Measure=(value, uncertainty, validity); Status=(normative, decision, verification); SourceSpan=(document, revision, clause, immutable_id). Required case profiles (energy, grid, IoSN, CBA) definieren kontrollierte Kind-Werte und Prädikate; nicht jeweils neue Kernmetaklassen.

## Kompositions- und Abhängigkeitsgraph
ContractFrame --contains--> Referents/Assertions/Policies/Observables/Evidence.
ScopedAssertion --has_predicate--> Predicate; --applies_to--> Referent/Scope; --supported_by--> AuthorityRecord.
Referent[port] --connected_to--> Referent[port] mit Carrier/Sign/Unit-Prüfung.
ObservableDefinition --observes--> Referent/Predicate; EvidenceRecord --verifies--> ScopedAssertion/ObservableDefinition.
VariationPolicy --governs--> Referent/ImplementationRole; AuthorityRecord --authorizes--> Assertion/Policy.
Process/Data Contracts sind getypte Referents + ScopedAssertions + typed input/output/derivation links, nicht zwingend neue C10/C11-Klassen.

## Explizite Diskriminatoren, die nicht wegreduziert werden dürfen
- Normativity: REQUIRED, PROHIBITED, PERMITTED, IMPLEMENTATION_DEFINED, CONDITIONAL. Entscheidung: APPROVED, PROPOSED, OWNER_TBD, REJECTED, SUPERSEDED, UNKNOWN. Evidenz: NOT_EXECUTED, PASS, FAIL, INCONCLUSIVE, NOT_APPLICABLE, BLOCKED. Statusdomänen **nicht** gleichsetzen.
- Assumption(kind=ENVIRONMENT/DATA/TECHNICAL) vs Guarantee(kind=SAFETY/SERVICE/CAPABILITY); eine Servicefähigkeit kann ein Für-alle-Forderungen/Es-gibt-Reaktionsgarantie sein und ist nicht durch bloßes Nichtverletzen von Grenzen belegt.
- Observable-Definition vs real beobachteter Wert; EvidenceRequest vs EvidenceResult; Modellvariante vs Referenzprofil; externe Verpflichtung vs interne Implementierungsentscheidung.

## Minimale Speicherbeispielprojektion (abstrakt, keine YAML-Grammatik)
Frame S: time=hourly; horizon=48 intervals; BUS_A electricity; scenario set known.
Referent battery: role=electrical_storage; referent port:grid: p_active [MW], positive injects into BUS_A.
Assertion A1 REQUIRED safety: -3 MW <= p_grid(t) <= 4 MW for all valid t.
Assertion A2 REQUIRED behavioural: battery energy ledger after losses and initial/terminal conditions, defined **at externally verifiable functional level**; domain guarantee needs a trace witness or a formally akzeptierte Abstraktion.
Variation V1 PERMITTED: arbitrary internal coordinates/constraint structure; must provide ledger projection and battery-role conformance evidence. NOT permitted: implicit energy creation.
Observable O1: p_grid(t) [MW] signed, O2: ledger deltaE [MWh], O3: availability and initial/terminal witness.
Authority R1: method clause + version + Owner decision; Unknowns remain links.
Zwei getrennte Quell-IDs mit gleichlautender Pflicht bleiben zwei AuthorityRecords; fachlich identische Assertion kann gemeinsame Statement-Bedeutung haben, jedoch separate Authorities.

## Bewertung durch wissenschaftliche Ablation, zu testen
C1 entfernen: unklare Referenz- und Scope-Basis RC09. C2 entfernen: keine stabilen Komponenten-/Datentypen RC03. C3 entfernen: keine Connections/Traceability RC05. C4 entfernen: nur Prosa, kein strukturprüfbarer Guard RC07. C5 entfernen: keine Normativität/A-G RC01. C6 entfernen: gleiche Zielzahlen ohne KPI-Projektionssemantik RC08. C7 entfernen: Variation irrtümlich E4 RC10. C8 entfernen: Behauptung ohne Evidenzbeziehung RC10. C9 entfernen: Owner_TBD/Quelle fällt weg RC09. Diese 9 Witnesses sprechen für funktionale Unersetzbarkeit der **Unterscheidungen**, nicht für 9 notwendige Klassen. C9 könnte als generischer getypter Referent und C3-Rela­tion kodiert werden; dies spart Klassen, aber keinen semantischen Inhalt. Reduktionsziel in ML-C20: Typzahl vs Regel-/Validator-Komplexität vs Autorenfehler getrennt messen.

## Grenzen
Vollständigkeit bezieht sich auf SLR01–42 als Forschungskandidaten und RC01–10, nicht alle möglichen Energiesystemwissenschaften. Ein Modell kann konform sein, ohne denselben Optimierungs-Feasible-Set wie ein zweites zu besitzen. Das Metamodell ist nur mit konkret definierter Regelsignatur und Validation implementierbar; kein implementierter CSNF-Parser wird hier behauptet.
