# ML-C20/07 – RC01–RC10 authoring variants (conceptual fixtures)
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

**Evidence warning:** Two sketch representations per case are *intended* to carry the same outer obligation only when all profile field definitions exist and are validated; provided `contractPredicate(...)` delegates exact physical expression to a not-yet-frozen profile. Consequently no E1/ E2 result or parser coverage is claimed. Negative mutation is adversarial; source citations from ML-C19/11 are research references rather than approved domain clauses. Detailed evaluator oracles live in C23 draft PR #56.

### RC01: battery external grid injection
**Contract oracle:** port battery.grid carrier electricity kind active_power unit MW sign INJECTION; guarantee bounds -3..4 MW; ledger delta MWh; source SRC_B; owner OWNER_TBD
**Positive implementation alternatives:** battery.grid connectedTo BUS_A; external ledger 2MW*0.5h=1MWh.
**Mutation:** 2 MW*0.5h=2MWh; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC01" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC01:frame" { study_kind: "battery external grid injection"; }
  authority "RC01:SRC": SOURCE { immutable_ref: "ML-C19/11:RC01"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC01:P1" = contractPredicate("RC01:external");
  assert "RC01:A1" REQUIRED SAFETY_GUARANTEE predicate "RC01:P1" scope "RC01:scope" guard true authority ["RC01:SRC"] decision OWNER_TBD;
  observe "RC01:O1" from "RC01:port" { semantics: "port battery.grid carrier electricity kind active_power unit MW sign INJECTION; guarantee bounds -3..4 MW; ledger delta MWh; source SRC_B; owner OWNER_TBD"; }
  evidence "RC01:V1": REQUEST for "RC01:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC01:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "battery external grid injection"
  },
  "referents": [
    {
      "id": "RC01:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC01:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC01:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC01:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC01:P1",
      "scope": "RC01:scope",
      "guard": true,
      "authority_refs": [
        "RC01:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC01:O1",
      "subject": "RC01:port",
      "semantics": "port battery.grid carrier electricity kind active_power unit MW sign INJECTION; guarantee bounds -3..4 MW; ledger delta MWh; source SRC_B; owner OWNER_TBD"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC01:V1",
      "role": "REQUEST",
      "subject_ref": "RC01:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC01:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC01",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC02: individual EV departure guarantee
**Contract oracle:** port fleet.grid carrier electricity kind active_power unit MW sign CONSUMPTION; guarantee forall vehicles departure_energy; source SRC_EV
**Positive implementation alternatives:** fleet service quantifier forall vehicle exists feasible dispatch.
**Mutation:** aggregate MWh okay but vehicle deadline missed; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC02" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC02:frame" { study_kind: "individual EV departure guarantee"; }
  authority "RC02:SRC": SOURCE { immutable_ref: "ML-C19/11:RC02"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC02:P1" = contractPredicate("RC02:external");
  assert "RC02:A1" REQUIRED SAFETY_GUARANTEE predicate "RC02:P1" scope "RC02:scope" guard true authority ["RC02:SRC"] decision OWNER_TBD;
  observe "RC02:O1" from "RC02:port" { semantics: "port fleet.grid carrier electricity kind active_power unit MW sign CONSUMPTION; guarantee forall vehicles departure_energy; source SRC_EV"; }
  evidence "RC02:V1": REQUEST for "RC02:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC02:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "individual EV departure guarantee"
  },
  "referents": [
    {
      "id": "RC02:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC02:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC02:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC02:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC02:P1",
      "scope": "RC02:scope",
      "guard": true,
      "authority_refs": [
        "RC02:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC02:O1",
      "subject": "RC02:port",
      "semantics": "port fleet.grid carrier electricity kind active_power unit MW sign CONSUMPTION; guarantee forall vehicles departure_energy; source SRC_EV"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC02:V1",
      "role": "REQUEST",
      "subject_ref": "RC02:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC02:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC02",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC03: electrolyser electricity/H2 interfaces
**Contract oracle:** port el.grid carrier electricity kind active_power unit MW sign CONSUMPTION; port el.h2 carrier hydrogen kind mass_flow unit kg/h; source SRC_EL
**Positive implementation alternatives:** two typed ports and approved heating_value_basis.
**Mutation:** kg/h compared to MW directly; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC03" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC03:frame" { study_kind: "electrolyser electricity/H2 interfaces"; }
  authority "RC03:SRC": SOURCE { immutable_ref: "ML-C19/11:RC03"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC03:P1" = contractPredicate("RC03:external");
  assert "RC03:A1" REQUIRED SAFETY_GUARANTEE predicate "RC03:P1" scope "RC03:scope" guard true authority ["RC03:SRC"] decision OWNER_TBD;
  observe "RC03:O1" from "RC03:port" { semantics: "port el.grid carrier electricity kind active_power unit MW sign CONSUMPTION; port el.h2 carrier hydrogen kind mass_flow unit kg/h; source SRC_EL"; }
  evidence "RC03:V1": REQUEST for "RC03:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC03:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "electrolyser electricity/H2 interfaces"
  },
  "referents": [
    {
      "id": "RC03:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC03:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC03:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC03:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC03:P1",
      "scope": "RC03:scope",
      "guard": true,
      "authority_refs": [
        "RC03:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC03:O1",
      "subject": "RC03:port",
      "semantics": "port el.grid carrier electricity kind active_power unit MW sign CONSUMPTION; port el.h2 carrier hydrogen kind mass_flow unit kg/h; source SRC_EL"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC03:V1",
      "role": "REQUEST",
      "subject_ref": "RC03:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC03:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC03",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC04: H2 storage mass conservation
**Contract oracle:** port h2store.mass carrier hydrogen kind mass_flow unit kg/h; guarantee conservation of kg inventory; source SRC_HS
**Positive implementation alternatives:** mass ledger under explicit leakage basis.
**Mutation:** 1 kg silently treated as 1 MWh; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC04" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC04:frame" { study_kind: "H2 storage mass conservation"; }
  authority "RC04:SRC": SOURCE { immutable_ref: "ML-C19/11:RC04"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC04:P1" = contractPredicate("RC04:external");
  assert "RC04:A1" REQUIRED SAFETY_GUARANTEE predicate "RC04:P1" scope "RC04:scope" guard true authority ["RC04:SRC"] decision OWNER_TBD;
  observe "RC04:O1" from "RC04:port" { semantics: "port h2store.mass carrier hydrogen kind mass_flow unit kg/h; guarantee conservation of kg inventory; source SRC_HS"; }
  evidence "RC04:V1": REQUEST for "RC04:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC04:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "H2 storage mass conservation"
  },
  "referents": [
    {
      "id": "RC04:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC04:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC04:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC04:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC04:P1",
      "scope": "RC04:scope",
      "guard": true,
      "authority_refs": [
        "RC04:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC04:O1",
      "subject": "RC04:port",
      "semantics": "port h2store.mass carrier hydrogen kind mass_flow unit kg/h; guarantee conservation of kg inventory; source SRC_HS"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC04:V1",
      "role": "REQUEST",
      "subject_ref": "RC04:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC04:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC04",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC05: DC electric KCL and KVL
**Contract oracle:** referent branch role physical_branch; guarantee KCL_AND_KVL under DC assumptions; source SRC_GRID
**Positive implementation alternatives:** angle or PTDF implementation allowed with required KVL trace.
**Mutation:** only KCL required; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC05" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC05:frame" { study_kind: "DC electric KCL and KVL"; }
  authority "RC05:SRC": SOURCE { immutable_ref: "ML-C19/11:RC05"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC05:P1" = contractPredicate("RC05:external");
  assert "RC05:A1" REQUIRED SAFETY_GUARANTEE predicate "RC05:P1" scope "RC05:scope" guard true authority ["RC05:SRC"] decision OWNER_TBD;
  observe "RC05:O1" from "RC05:port" { semantics: "referent branch role physical_branch; guarantee KCL_AND_KVL under DC assumptions; source SRC_GRID"; }
  evidence "RC05:V1": REQUEST for "RC05:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC05:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "DC electric KCL and KVL"
  },
  "referents": [
    {
      "id": "RC05:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC05:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC05:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC05:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC05:P1",
      "scope": "RC05:scope",
      "guard": true,
      "authority_refs": [
        "RC05:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC05:O1",
      "subject": "RC05:port",
      "semantics": "referent branch role physical_branch; guarantee KCL_AND_KVL under DC assumptions; source SRC_GRID"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC05:V1",
      "role": "REQUEST",
      "subject_ref": "RC05:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC05:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC05",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC06: expansion admissibility
**Contract oracle:** guarantee discrete modules when source requires; disclose continuum approximation; source SRC_INV
**Positive implementation alternatives:** module count integer 0 or 1 on approved profile.
**Mutation:** 0.3 module built as physical asset; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC06" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC06:frame" { study_kind: "expansion admissibility"; }
  authority "RC06:SRC": SOURCE { immutable_ref: "ML-C19/11:RC06"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC06:P1" = contractPredicate("RC06:external");
  assert "RC06:A1" REQUIRED SAFETY_GUARANTEE predicate "RC06:P1" scope "RC06:scope" guard true authority ["RC06:SRC"] decision OWNER_TBD;
  observe "RC06:O1" from "RC06:port" { semantics: "guarantee discrete modules when source requires; disclose continuum approximation; source SRC_INV"; }
  evidence "RC06:V1": REQUEST for "RC06:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC06:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "expansion admissibility"
  },
  "referents": [
    {
      "id": "RC06:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC06:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC06:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC06:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC06:P1",
      "scope": "RC06:scope",
      "guard": true,
      "authority_refs": [
        "RC06:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC06:O1",
      "subject": "RC06:port",
      "semantics": "guarantee discrete modules when source requires; disclose continuum approximation; source SRC_INV"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC06:V1",
      "role": "REQUEST",
      "subject_ref": "RC06:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC06:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC06",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC07: stage information-set condition
**Contract oracle:** guarantee stage1 decision equal across unrevealed scenarios; source SRC_SCEN
**Positive implementation alternatives:** scenario-indexed or single-shared x pre-revelation.
**Mutation:** stage-1 depends on future scenario; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC07" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC07:frame" { study_kind: "stage information-set condition"; }
  authority "RC07:SRC": SOURCE { immutable_ref: "ML-C19/11:RC07"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC07:P1" = contractPredicate("RC07:external");
  assert "RC07:A1" REQUIRED SAFETY_GUARANTEE predicate "RC07:P1" scope "RC07:scope" guard true authority ["RC07:SRC"] decision OWNER_TBD;
  observe "RC07:O1" from "RC07:port" { semantics: "guarantee stage1 decision equal across unrevealed scenarios; source SRC_SCEN"; }
  evidence "RC07:V1": REQUEST for "RC07:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC07:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "stage information-set condition"
  },
  "referents": [
    {
      "id": "RC07:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC07:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC07:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC07:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC07:P1",
      "scope": "RC07:scope",
      "guard": true,
      "authority_refs": [
        "RC07:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC07:O1",
      "subject": "RC07:port",
      "semantics": "guarantee stage1 decision equal across unrevealed scenarios; source SRC_SCEN"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC07:V1",
      "role": "REQUEST",
      "subject_ref": "RC07:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC07:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC07",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC08: cost KPI basis and weights
**Contract oracle:** observe total_system_cost kind currency unit EUR basis real_2025 discount explicit; source SRC_KPI
**Positive implementation alternatives:** solver objective or postprocess ledger same contract KPI.
**Mutation:** omit temporal weight or double-count CAPEX; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC08" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC08:frame" { study_kind: "cost KPI basis and weights"; }
  authority "RC08:SRC": SOURCE { immutable_ref: "ML-C19/11:RC08"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC08:P1" = contractPredicate("RC08:external");
  assert "RC08:A1" REQUIRED SAFETY_GUARANTEE predicate "RC08:P1" scope "RC08:scope" guard true authority ["RC08:SRC"] decision OWNER_TBD;
  observe "RC08:O1" from "RC08:port" { semantics: "observe total_system_cost kind currency unit EUR basis real_2025 discount explicit; source SRC_KPI"; }
  evidence "RC08:V1": REQUEST for "RC08:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC08:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "cost KPI basis and weights"
  },
  "referents": [
    {
      "id": "RC08:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC08:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC08:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC08:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC08:P1",
      "scope": "RC08:scope",
      "guard": true,
      "authority_refs": [
        "RC08:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC08:O1",
      "subject": "RC08:port",
      "semantics": "observe total_system_cost kind currency unit EUR basis real_2025 discount explicit; source SRC_KPI"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC08:V1",
      "role": "REQUEST",
      "subject_ref": "RC08:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC08:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC08",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC09: CBA counterfactual / unknown method owner
**Contract oracle:** frame baseline BASE and project P with shared exogenous snapshot; owner OWNER_TBD; source SRC_CBA
**Positive implementation alternatives:** integrated CBA or external postprocess, no N2E authority claim.
**Mutation:** counterfactual data drift or owner approval invented; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC09" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC09:frame" { study_kind: "CBA counterfactual / unknown method owner"; }
  authority "RC09:SRC": SOURCE { immutable_ref: "ML-C19/11:RC09"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC09:P1" = contractPredicate("RC09:external");
  assert "RC09:A1" REQUIRED SAFETY_GUARANTEE predicate "RC09:P1" scope "RC09:scope" guard true authority ["RC09:SRC"] decision OWNER_TBD;
  observe "RC09:O1" from "RC09:port" { semantics: "frame baseline BASE and project P with shared exogenous snapshot; owner OWNER_TBD; source SRC_CBA"; }
  evidence "RC09:V1": REQUEST for "RC09:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC09:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "CBA counterfactual / unknown method owner"
  },
  "referents": [
    {
      "id": "RC09:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC09:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC09:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC09:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC09:P1",
      "scope": "RC09:scope",
      "guard": true,
      "authority_refs": [
        "RC09:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC09:O1",
      "subject": "RC09:port",
      "semantics": "frame baseline BASE and project P with shared exogenous snapshot; owner OWNER_TBD; source SRC_CBA"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC09:V1",
      "role": "REQUEST",
      "subject_ref": "RC09:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC09:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC09",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.

### RC10: multi-model variation + evidence
**Contract oracle:** compare two model implementations by shared KPI + sources + variation, evidence NOT_EXECUTED; source SRC_MULTI
**Positive implementation alternatives:** two independent model internals with same obligations and disclosed variation.
**Mutation:** declare E4 from identical cost; evidence NOT_EXECUTED->PASS; expected DIFFERENT/BLOCKED, not E1_EQUAL.
Candidate A sketch (illustrates syntax, NOT parse-tested; `contractPredicate` is profile-defined and the full physical equation remains in profile registry):
```text
contract "RC10" schema "C20-research-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "RC10:frame" { study_kind: "multi-model variation + evidence"; }
  authority "RC10:SRC": SOURCE { immutable_ref: "ML-C19/11:RC10"; revision: "research-r0"; decision: OWNER_TBD; }
  predicate "RC10:P1" = contractPredicate("RC10:external");
  assert "RC10:A1" REQUIRED SAFETY_GUARANTEE predicate "RC10:P1" scope "RC10:scope" guard true authority ["RC10:SRC"] decision OWNER_TBD;
  observe "RC10:O1" from "RC10:port" { semantics: "compare two model implementations by shared KPI + sources + variation, evidence NOT_EXECUTED; source SRC_MULTI"; }
  evidence "RC10:V1": REQUEST for "RC10:A1" { status: NOT_EXECUTED; }
}
```
Candidate B structured snippet (design sketch, not complete type-checkable reference):
```json
{
  "frame": {
    "id": "RC10:frame",
    "schema": "C20-research-0.1",
    "ruleset": "CSNF-R0",
    "registry": "energy-r0",
    "question": "multi-model variation + evidence"
  },
  "referents": [
    {
      "id": "RC10:port",
      "kind": "external_port"
    }
  ],
  "relations": [],
  "predicates": [
    {
      "id": "RC10:P1",
      "expr": {
        "op": "contractPredicate",
        "args": [
          "RC10:external"
        ]
      }
    }
  ],
  "assertions": [
    {
      "id": "RC10:A1",
      "modality": "REQUIRED",
      "semantic_role": "SAFETY_GUARANTEE",
      "predicate_ref": "RC10:P1",
      "scope": "RC10:scope",
      "guard": true,
      "authority_refs": [
        "RC10:SRC"
      ],
      "decision": "OWNER_TBD"
    }
  ],
  "observables": [
    {
      "id": "RC10:O1",
      "subject": "RC10:port",
      "semantics": "compare two model implementations by shared KPI + sources + variation, evidence NOT_EXECUTED; source SRC_MULTI"
    }
  ],
  "variations": [],
  "evidences": [
    {
      "id": "RC10:V1",
      "role": "REQUEST",
      "subject_ref": "RC10:A1",
      "status": "NOT_EXECUTED"
    }
  ],
  "authorities": [
    {
      "id": "RC10:SRC",
      "role": "SOURCE",
      "immutable_ref": "ML-C19/11:RC10",
      "decision_state": "OWNER_TBD"
    }
  ]
}
```
**Equivalence limit:** Under a common normalized typed AST and full approved profile semantics only, these *intended* encodings share obligation meaning. Until complete profile and resolver checks, E1=NOT_EXECUTED. Owner-TBD and source links must remain preserved; both syntaxes currently share the same unresolved owner.
