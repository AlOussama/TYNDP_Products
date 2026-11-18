# ML-C17 — Minimal Viable IoSN Contract Language (semantische Hypothese)

**Ziel:** kleinster plausibler, fachlich voll Ausdruck-fähiger **spezifikationsorientierter** Sprachkern. Keine Serialisierung, DSL, AST-Framework-, Runtime- oder Standardsfestlegung und kein automatisch generierter ausführbarer Modellcode. Der Begriff „viable“ bedeutet hier **prüfbaren Entwicklungskandidaten**, nicht bereits bewiesene fachliche Vollständigkeit.

## 1. Grundprinzipien

Ein gültiger Contract ist ein **source-linked, typed, scoped, versionierter Satz fachlicher Assertions** mit explizitem Anwendungsbereich, erlaubter Implementierungsfreiheit, Anforderungen an Daten/Prozesse/Mathematik/Outputs und konkreten Prüforakel-Anfragen. Wo Methodik-/Ownerentscheidungen fehlen, muss ein typed Unknown den Status erhalten und reale Freigabe blockieren. Eine Implementation darf eigene Variablen, Algorithmen, numerische Solver oder interne Modellkomponenten wählen; die fachliche Semantik darf nicht verloren gehen.

## 2. Vorschlag minimaler S2-Semantikkern

| Rollengruppe | Verpflichtende Felder/Werte | Warum nicht entfallen |
|---|---|---|
| SourceAssertion + Authority | source/version/clause/claim, status, ResearchProfile, conflict_refs | D1/D2/O26 und MD-01 |
| Requirement | unveränderte ID/text_ref, source_ref, normstatus, required/conditional, scope | 48 MA01-SR, kein erfundener 49. SR |
| Scope + Predicate | Y, externes CY, scenario/variant, UTC interval Δt, space, carrier, stage, guard TRUE/FALSE/UNKNOWN | RC01/11; Anwendungsbedingungen |
| EnergyObjectRole | PhysicalBranch / ControllableMarketLink / Storage / Converter / ExogenousH2, TopologyRef | RC03/04/06/07 |
| DataDefinition + DataInstanceRef | Grain, unit, axes, source release, provenance, data quality/Unknown | 87 B01-D; 20 process-only ohne neue SR |
| ProcessStep + TransformSpec | P00–P17, 38 T, consumes/produces, dependency/quality predicate | RC08/P14/P16, Spec ≠ execution |
| MathematicalRule | typed decision, parameter, set, quantifier, constraint/objective, equivalence projection, allowed freedom | M01–M18; nicht bloßer Gleichungstext |
| ResultDefinition | RawResult, DerivedMetric definition/formula, SystemNeed, project approval distinction | RC09, B01-D081 |
| VerificationRequest | case, oracle/ref or Unknown, evidenceRequest, six scoped atomic statuses, actual evidence identity as separate type | RC10/P15 |
| Unknown | reason, owner, required_for, source, scope, resolves_by, blocking_policy | 21 MD/CL offen ohne erfundene Werte |

**Leichtgewichtige Relationsfamilien:** DERIVED_FROM, REFINES, APPLIES_TO, CONSUMES/PRODUCES (je eigene Richtung), DEPENDS_ON, VERIFIES, REQUIRES_EVIDENCE/HAS_EVIDENCE (getrennt), BLOCKED_BY. Der genaue Grammatikumfang kann eine Tagged Union verwenden; diese Gruppierung ist **keine** bewiesene minimale Anzahl einzelner Klassen/Relationen.

### Nicht zulässige semantische Vereinfachung

PHYSICAL_BRANCH/KVL ≠ MARKET_LINK/NTC; Requirement ≠ source draft; Definition ≠ reale Dateninstanz; spec ≠ execution; Request ≠ Evidence; NOT_EXECUTED ≠ FAIL; CONDITIONAL ≠ NOT_APPLICABLE; native Algebra ≠ wissenschaftlich äquivalente Eigenschaft.

## 3. Illustrative Abstract-Contract-Notation (keine ausführbare DSL)

~~~text
contract ResearchProfile:IoSN_D1_D6 @ semantic_revision="research"
 source O26:2026-02-25 authority=CONSULTATION_DRAFT
 decision D2: status=RESEARCH_DECISION scope=Y{2035,2040,2050}
 requirement MA01-SR-010: external CY={CY1,CY2,CY3,CY4,CY5}
   parameter w[CY] : symbolic dimensionless owner=TBD
   invariant forall y in Y, c in CY: weight[y,c] == w[c]
   not_required: forall c,d: w[c] == w[d]
   conflict_ref: O26_draft_three_weather_cases
   verification: test_ref=R04-T-SR-010 oracle=TBD evidence=NOT_EXECUTED

 requirement MA01-SR-029:
   decision invest[y,k,stage] information_time=BEFORE_WEATHER
   invariant forall c: projected_native_invest[y,k,stage,c] == invest[y,k,stage]
   freedom: native index replication allowed only with equality-coupling

 requirement MA01-SR-018:
   asset PHYSICAL_BRANCH: physical_DC_mesh=true, KCL=true, KVL=true
   freedom: angle|cycle|PTDF if equivalence_projection and assumptions proven

 requirement MA01-SR-035:
   asset CONTROLLABLE_MARKET_LINK: directional_NTC_bounds=true
   physical_technology: AC_OR_DC_AS_SOURCE
   not_required: physical_mesh_KVL_on_market_link

 requirement MA01-SR-026:
   applies_if: P15_guard TRUE|FALSE|UNKNOWN
   if FALSE and witnessed_not_invoked: NOT_APPLICABLE
   if UNKNOWN: BLOCKED
   if TRUE: x_OPF <= x_LF_portfolio ; verification_required=true
~~~

Das ist **didaktische Semantik**; keine tatsächlich geparste, vollständige Grammatik. Eine zukünftige Syntax darf nur dann als gleichwertig gelten, wenn positive und negative Fälle plus Quellen-/Unit-/Scope-Regressionen erhalten bleiben.

## 4. Die noch fehlende formale Ausgestaltung

1. Abstraktes getyptes Expressionsystem: Binder/Index, Quantor, Dimension/Unit, phasenabhängige Variable, Constraint, Objective und Zeit-Nachfolger.
2. Formaler Gültigkeitsbegriff: kompletter Contract vs Unknown mit Status und Pflicht zur blockierenden Auswertung.
3. Versionierte Source-/Profil-/Migrationstupel und rekursives Invalidieren alter Testzeugnisse.
4. Prüfer für 48 SR / 18 P / M01–M18 und Negativmutationen; genauer Umfang muss dokumentiert werden.
5. Zwei voneinander getrennte externe Toolentwickler-Interpretationen und mindestens zwei native Standard-Parser-Slices; **später**, keine sofortige normative Auswahl.
6. E-FEAS-/E-OPT-/E-OBS-Projektionsnachweise auf synthetischen Mini-Modellen, keine volle IoSN-Optimierung.

**Konditionale Empfehlung:** S2 als gemeinsames semantisches Evaluationsobjekt entwickeln. A, B und C bleiben technische Implementations- und Austauschoptionen; die S2-Kernsemantik präjudiziert **keine** davon. Ohne nachgewiesene semantische Vollständigkeit nicht als „minimal complete“ freigeben. **G1 BLOCKED.**
