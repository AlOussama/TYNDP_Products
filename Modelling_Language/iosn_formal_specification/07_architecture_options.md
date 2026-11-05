> **MA-01 LEGACY / HISTORICAL ONLY — NOT AN ACTIVE REQUIREMENTS CATALOGUE (2026-11-05).** This research artifact predates MA-01. Sole active provisional source-derived system requirements: [iosn_requirements_catalogue.csv](iosn_requirements_catalogue.csv), with [source baseline](methodology_source_baseline.md), [process specification](iosn_process_specification.md), [scope change impact](scope_and_change_impact.md). Weather-year selection/PCA/K-Means/reproduction is **EXTERNAL / OUT OF SCOPE**, only already-selected weather inputs and consistency checks are in scope. Any old MR/SR/UC/VC/LRC/test/architecture recommendation is superseded and **not normative**. Retained as non-normative historical research; no architectural/tool decision is made here.

---

# 07 — Architecture options: comparative study (not a premise)

## Constraints inherited from SyRS
The solution must deliver (i) single governed normative semantic authority; (ii) stable trace graph; (iii) typed inputs/transformations/outputs; (iv) method-specific obligatory math when published in O26; (v) tool-neutral verification; (vi) no invented source rules; (vii) manageable release governance. These arise from SR-001–021 / LRC-01–17, **not from former A/A+/B/B+ designs**.

## Options and architecture boundaries

### L1 — SysML v2 as canonical system specification
~~~mermaid
flowchart LR
  O[Signed IoSN source] --> S[SysML v2 canonical model]
  S --> D[IoSN domain profile]
  D --> T[Tool adapters and evidence]
  S --> V[Verification Cases]
~~~
**Pros:** unified stakeholder/system requirement types, constraint/verification relationships, traceability. **Cons:** MBSE onboarding, ecosystem licence/tool support, domain-specific timeseries/schema/solver validators still needed; interpretation of imported data and complex LP not solved automatically.

### L2 — Independent IoSN DSL, serialized as YAML/JSON
~~~mermaid
flowchart LR
  O[Source] --> DSL[One IoSN grammar + semantic specification]
  DSL --> C[Parser / IR / validators]
  C --> A[Tool adapters]
  C --> E[Verification tests]
~~~
**Pros:** narrow, energy-expert friendly terminology; potentially simple canonical artifact. **Cons:** full ownership of syntax + normative semantics + validators + migrations + security/QA. YAML is merely the syntax; rejecting undefined implicit defaults is mandatory.

### L3 — Extend an energy-system metamodel
~~~mermaid
flowchart LR
  O[Source] --> CESM[Extended CESM / INES / GEMS profile]
  CESM --> M[Model data/math]
  CESM --> P[Added method/workflow/test contracts]
~~~
**Pros:** reuse existing typed energy model and converters. **Cons:** mismatch between *system model exchange* and methodology/requirements language; might force a particular graph or algebra; extension governance depends on upstream project.

### L4 — A modular IoSN contract with one canonical registry
~~~mermaid
flowchart LR
  O[Signed sources] --> R[Canonical IoSN requirement and obligation registry]
  R --> IN[Data profile]
  R --> PRE[Method/transform profile]
  R --> MOD[Energy semantic + conditional math profile]
  R --> OUT[Output/KPI profile]
  R --> V[Verification/evidence profile]
  IN --> AD[Independent tool adapters]
  PRE --> AD
  MOD --> AD
  OUT --> AD
  AD --> V
~~~
**Pros:** apply mature specialised tools with explicit semantics/validation per module; mathematical precision only where needed. **Cons:** composition cost, dual sources of truth risk, migration burden, conflicting identifiers/versions unless one registry, precedence and conflict rules exist.

## Comparative tradeoffs
|Criterion|L1 SysML v2|L2 Own DSL|L3 Extend energy model|L4 Modular registry|
|---|---|---|---|---|
|Trace / requirements|Strong native base|Designed by project|Extension needed|Registry/ReqIF or SysML profile|
|Input/semantics|Requires profile|Designed by project|Strong energy base|LinkML/CESM + ontology|
|Preprocessing|Activity/extension|Native custom rules|Extension|Method profile / typed transformations|
|Mandatory LP equations|Constraint/profile needed|Native custom expressiveness|Depends on GEMS vs CESM|Optional mathematical subprofile|
|Verification tests|Native case relation; execution external|Validator engineering|Major extension|Dedicated evidence/test profile|
|Single semantic authority|Possible with disciplined model|Possible by design|Upstream+project conflicts risk|Possible with canonical registry **only**|
|Energy expert accessibility|Requires MBSE training|Potentially best|Good energy model familiarity|More formats; curated human-facing view|
|Version/governance|OMG tooling + local profile|Full in-house burden|Upstream dependency|Multi-profile compatibility burden|
|Freedom of solver/internal structures|Good if model profile neutral|Good if grammar neutral|May inherit assumptions|Good if data and method separated|
|Vendor/ecosystem risk|Tool licence and adoption|One bespoke maintainer|Metamodel maturity|Adapters and cross-standard dependencies|
|Immediate demonstrator effort|Higher for SysML tools|Low if tiny; high if complete|Medium|Medium; use existing schema+small semantics|
|Strongest objection|Tooling overhead unrelated to IoSN|Reinventing standards|Mixes model and methodology|Multiple incompatible sources of truth|

## Critical countertests before selecting
1. **L1 falsification:** represent O26 §3.7, §3.8 and §3.1.1 as genuinely editable/testable SysML v2 concepts; measure external validation effort.
2. **L2 falsification:** show why LinkML + JSON Schema + lightweight semantic rules cannot meet signed SyRS; if it can, a full bespoke parser is not justified.
3. **L3 falsification:** independently demonstrate CESM/GEMS/INES can encode the *complete* weather/PCA, network reduction and acceptance semantics without abusing entity types.
4. **L4 falsification:** intentionally add conflicting IDs, units or formula revisions across modules; validator **must fail closed**, never choose silently.

## Conditional result after comparison
**Working direction for a pilot:** L4, the **modular single-registry contract**, with JSON Schema / LinkML for typed data and small explicit semantic predicates, plus an *optional obligation-bound mathematical profile*. A small IoSN-specific **profile/namespace** is likely unavoidable; a wholly new general-purpose energy modelling DSL is **not shown necessary**. This is a **PROPOSED, reversible** position: L1 is preferable where an MBSE toolchain is already mature; L3 is preferable if a mature upstream metamodel demonstrably covers end-to-end method semantics; L2 might win for simple, tightly governed projects.

## Non-negotiable semantic precedence rules for any selected option
1. Source PDF or superseding approved text is **legal/methodological authority**; signed contract artifact is the **only implementer-facing normative technical interpretation**. An unapproved contract may not supersede the method owner.
2. `requirement_id` + `source_version` uniquely identify obligation; profile versions and target horizon govern applicability.
3. Missing or contradictory mandatory semantic rules → `UNRESOLVED` or `FAIL`, **never fallback to tool defaults**.
4. Validation status separated: schema, domain rules, tool execution evidence, formal/human review.
5. No silent component/parameter loss in adapters; declare and block unsupported obligations.
6. Separate **mandatory math** from **implementation internals**; requirement must point to explicit O26 rule before math is forced.
