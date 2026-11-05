> **MA-01 LEGACY / HISTORICAL ONLY — NOT AN ACTIVE REQUIREMENTS CATALOGUE (2026-11-05).** This research artifact predates MA-01. Sole active provisional source-derived system requirements: [iosn_requirements_catalogue.csv](iosn_requirements_catalogue.csv), with [source baseline](methodology_source_baseline.md), [process specification](iosn_process_specification.md), [scope change impact](scope_and_change_impact.md). Weather-year selection/PCA/K-Means/reproduction is **EXTERNAL / OUT OF SCOPE**, only already-selected weather inputs and consistency checks are in scope. Any old MR/SR/UC/VC/LRC/test/architecture recommendation is superseded and **not normative**. Retained as non-normative historical research; no architectural/tool decision is made here.

---

# 05 — Existing languages and standards: critical capability and role review

**Assessment date 2026-11-04.** Coverage denotes documented **capability in principle**, not tested interoperability. Sources below are standards bodies and project primary documentation. See `06_language_capability_matrix.csv` for requirement-by-requirement classification. Symbols: **N** native, **E** extension, **C** combined with another language, **P** partial, **0** outside scope, **?** not verified. Native support for algebra **never** means IoSN workflow or methodology support is native.

## Systems engineering

### SysML v2 / KerML
- **Role:** formal systems engineering language for model elements, requirements, constraints, actions, verification and trace relationships. Official OMG specifications: https://www.omg.org/spec/SysML/ (SysML v2 adopted; use v2.0 as inspected basis). Check exact current OMG release before production.
- **Strength:** trace graph MR→SR→verification, process activities, semantic API and extension by domain libraries.
- **Boundary:** no out-of-box IoSN carrier semantics, PECD time/calendar interpretation, representative-weather choice, equivalent-grid calculations or complete LP model validation. A SysML v2 model alone is not a runnable IoSN engine.
- **License/opening:** OMG standard documentation and its licensed tooling are distinct; tool compatibility/licensing must be vetted separately.

### ReqIF
- **Role:** OMG Requirements Interchange Format v1.2 (https://www.omg.org/spec/ReqIF/). Interchange of structured requirements, attributes and links, not process solver or mathematical rules.
- **Strength:** exchange with existing requirements tools and change trace.
- **Boundary:** semantic rules and test oracles require complementary languages; importing ReqIF is not equivalent to executing requirement tests.

## Energy models and typed exchange

### GEMS / Antares
- **Role:** graph-based mathematical energy-system specification with model entities and equations; https://github.com/AntaresSimulatorTeam/GEMS ; available interpreters include Antares/GemsPy as described by project.
- **Strength:** explicit algebra for model equations, balance, period/scenario dimensions; useful for O26 §3.1.1 reference class if compatibility checked.
- **Boundary:** no established native end-to-end O26 preprocessing, change governance, system requirements, weather selection, complete postprocessing acceptance. Project converter compatibility is not proof of 1:1 equivalence.
- **Status/licensing:** public source; MPL-2.0 indicated by repository; re-check pinned commit and license before adoption.

### G-PST Common Energy System Model (CESM)
- **Role:** LinkML-based multi-carrier **data/metamodel** and translation hub; https://github.com/G-PST/CommonEnergySystemModel ; schema `model/cesm_v0.1.0.yaml`; MIT; public README explicitly calls project early phase.
- **Strength:** `Balance`, `Unit`, `Storage`, `Commodity`, `Link`, conversions, method identifiers; useful building blocks for SR-010 and LRC-02/06/13.
- **Boundary:** energy-model representation is not an authoritative description of ENTSO-E §3.7 PCA, §3.8 network reduction or §3.9 LF/OPF sequencing, nor proof of correct translated implementation. Typed schemas alone cannot ensure port reference integrity and feasible solution equivalence in every exporter.

### INES / ines-spec
- **Role:** typed model-exchange schema and scenario/time-series context for infrastructure energy-system data; https://github.com/ines-tools/ines-spec ; MIT project. Use pinned tag/branch for any evaluated integration.
- **Strength:** multi-carrier data description and ETL mappings.
- **Boundary:** adapter conversion losses and method support may require explicit capability gates. Not a complete IoSN normative requirements/execution contract.

### SiennaSchemas
- **Role:** schema infrastructure for PowerSystems/Sienna data records (topology, system data, time series and some planning entities), https://github.com/Sienna-Platform/SiennaSchemas ; BSD-style open source as documented project. Earlier review identifies versions below 1.0; **exact latest stable version not independently pinned**.
- **Strength:** typed time-series and system components.
- **Boundary:** native O26 weather selection, policy stages, H2 assumptions and methodology conformance have **not been demonstrated**. Distinguish schema from capabilities of Sienna.jl modelling libraries.

### energy-models/mathspec
- **Role:** optimisation model **algebra/specification** in YAML. https://github.com/energy-models/mathspec ; reviewed README: dimensions, parameters, variables, constraints, objective; checks and rendering to math; **no solver** in mathspec itself. Version indicated 0.2.x as of Oct 2026; version must be pinned.
- **Strength:** clean candidate for **mathematical obligation profile** O26 §3.1.1 (LP/index checks), if expression grammar supports required constraints.
- **Boundary:** not full input data, ETL, zoning or system acceptance standard. Do not confuse with DynamicalSystemsGroup/MSML. License check per repository release (README SPDX uses CC-BY-4.0 for some docs; package license must be verified separately).

### DynamicalSystemsGroup/MSML (Mathematical Specification Mapping Library)
- **Role:** JSON block/space/wiring specification, linked reports/visualisation; optional Python function execution. https://github.com/DynamicalSystemsGroup/MSML .
- **Strength:** traceable mechanisms, composition and documentation; may cover workflow structures with custom semantics.
- **Boundary:** optional executable simulation wiring is not established as an IoSN two-stage LP description/validator. Do not infer full energy-specificity or cross-tool conformance. **Naming caveat:** user also names BlockScience/MSML; DSG repository README was accessible, BlockScience repository contents not independently verified for this review.

### CIM/CGMES, OEO
- **CIM/CGMES:** IEC/ENTSO-E grid exchange profile, https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/ ; CGMES 3.0 is a relevant published profile. Good network identifiers/topology/electrical attributes; **not** complete scenario investment LP, H2 preprocessing, or acceptance contract.
- **Open Energy Ontology (OEO):** https://openenergyplatform.org/ontology/ ; renewable energy vocabulary identities/ontology; valuable semantic URI layer but not solver constraints or acceptance. Exact ontology revision and IRIs must be pinned.

## Formal data / process / verification languages

|Candidate|Primary purpose|Native strengths|Missing pieces for IoSN|Standards/open status|
|---|---|---|---|---|
|JSON or YAML + formally defined semantics|Serialization of one contract document|Readable and portable|Syntax alone no semantics, algebra, signatures or tests|YAML 1.2 / JSON RFC 8259; openness good|
|JSON Schema 2020-12|Typed JSON validation|Shapes, types, required, enums, numerical bounds|Cross-record conservation, external references, solver LP correctness|https://json-schema.org/specification |
|LinkML|Schema meta-language / generators|Typed models, identifier references, generated JSON Schema/SHACL/Pydantic|Full runtime/domain semantics and method algorithms require profiles|https://linkml.io/linkml/ |
|SHACL|RDF graph validation|Cross-references and value/graph shapes|Optimisation process/test execution; need RDF mapping|W3C Recommendation https://www.w3.org/TR/shacl/ |
|OCL|Object-model declarative invariants|Pre/postconditions and collection constraints|Tool coverage, energy semantics, optimisation algorithm verification|OMG https://www.omg.org/spec/OCL/ |
|BPMN 2.0.2|Process sequence|Dependency, gates, handoff/workflow states|Physical rules and time series algebra|OMG https://www.omg.org/spec/BPMN/ |
|DMN|Decision tables/expressions|Conditional eligibility, candidate filters|PCA/KMeans optimisation, LP solver and general physics|OMG https://www.omg.org/spec/DMN/ ; recent v1.6 standard / v1.7 beta in 2026 require precise pin|
|PyPSA, Antares, Sienna (not languages in this matrix)|Potential **target implementations**|Engines can express portions of requirements|Need actual adapter/conformance tests; cannot equate tool features with formal method profile|Use per-tool pinned release and test|

## Comparative conclusions (not a predetermined choice)
- If the contract's main object is **requirement→proof**, SysML v2 is strongest at trace semantics but costs energy-domain extension.
- If the main object is **typed energy data**, CESM/INES/SiennaSchemas give reusable components but cannot independently certify O26's process and prescribed equations.
- If the main object is **explicit normative mathematics**, GEMS and mathspec have relevant expression facilities; they do not by themselves specify weather-algorithm and output evidence lifecycle.
- A **controlled combination** may minimise new semantic invention, but only if cross-layer identifiers, version, precedence, schema composition and failure rules are documented. Without one canonical registry, stacking standards makes ambiguity worse.
- No studied single candidate has evidence for full end-to-end IoSN coverage. This is an **evidence-limited conclusion**, not a proof of impossibility.

## Source register
|ID|Primary reference|Nature / inspected aspect|
|---|---|---|
|T-01|https://www.omg.org/spec/SysML/|OMG SysML v2 specification portal, KerML relation|
|T-02|https://www.omg.org/spec/ReqIF/|OMG requirements exchange|
|T-03|https://github.com/AntaresSimulatorTeam/GEMS|GEMS project, model algebra and interpreters|
|T-04|https://github.com/G-PST/CommonEnergySystemModel|CESM README/schema v0.1.0, MIT, early-phase|
|T-05|https://github.com/ines-tools/ines-spec|INES data specification|
|T-06|https://github.com/Sienna-Platform/SiennaSchemas|Sienna schema types|
|T-07|https://github.com/energy-models/mathspec|mathspec README, mathematical spec|
|T-08|https://github.com/DynamicalSystemsGroup/MSML|MSML README, JSON wiring|
|T-09|https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/|CGMES profiles|
|T-10|https://openenergyplatform.org/ontology/|Energy ontology|
|T-11|https://json-schema.org/specification|JSON Schema 2020-12|
|T-12|https://linkml.io/linkml/|LinkML documentation|
|T-13|https://www.w3.org/TR/shacl/|W3C SHACL|
|T-14|https://www.omg.org/spec/BPMN/ and https://www.omg.org/spec/DMN/|BPMN/DMN|
|T-15|https://www.omg.org/spec/OCL/|OCL|

### Evidence caution
Project README and portal claims are **not** benchmarked behavior. No formal PLEXOS/Antares/Sienna or SysML v2 tooling was executed for this review. Versions/licensing not individually confirmed are marked unverified rather than guessed. Re-run matrix on precise tagged releases before standard selection.
