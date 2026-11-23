# ML-C20/03 – Two independent surface candidates
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

## A Compact declarative text C-SCN
Purpose: energy modelers edit external obligations in compact named blocks, explicit QIDs and typed expressions. Pros: low textual redundancy, readable role/port/guarantee declarations; costs: custom grammar, reference resolver, diagnostics, potential surprises in expression operator precedence (mitigated by prefix typed calls). Subject to developer familiarity and K17 human tests.

## B Structured typed document JSON
Purpose: leverage existing parser and schema tooling and leave semantic validation in common typed AST. Pros: familiar machine-readable tree, broad validators, easier generation/diffs; costs: repetitive syntax, highly verbose source refs, JSON lacks comments and cannot enforce physical validity through JSON Schema. Structured syntax is not 'CSNF' by itself; AST mapping remains the semantic authority.

## Full RC01 illustration of equivalence intention
Text candidate:
```text
contract "urn:study:RC01" schema "C20-0.1" rules "CSNF-R0" registry "energy-r0" {
  frame "urn:study:RC01:frame" { question: "Grid-connected storage behaviour"; }
  referent "urn:study:RC01:battery.grid": Port { carrier: electricity; kind: active_power; unit: MW; sign: INJECTION; direction: BIDIRECTIONAL; connection: "BUS_A"; }
  authority "urn:study:RC01:S1": SOURCE { immutable_ref: "ML-C19/11:RC01"; decision: OWNER_TBD; }
  predicate "urn:study:RC01:p-bound" = forall(t, between(port("urn:study:RC01:battery.grid", t), quantity(-3, MW), quantity(4, MW)));
  assert "urn:study:RC01:A1" REQUIRED SAFETY_GUARANTEE predicate "urn:study:RC01:p-bound" scope "urn:study:RC01:all-times" guard true authority ["urn:study:RC01:S1"] decision OWNER_TBD;
  observe "urn:study:RC01:O1" from "urn:study:RC01:battery.grid" { kind: active_power; unit: MW; temporal: interval; }
  variation "urn:study:RC01:V1" on "urn:study:RC01:battery" { allowed: ["SOC_state","MWh_state"]; disclosure: true; }
  evidence "urn:study:RC01:E1": REQUEST for "urn:study:RC01:A1" { status: NOT_EXECUTED; }
}
```
The `forall` quantifier's domain, authority to choose -3/+4 bounds, terminal conditions and available request profiles are mandatory profile/schema references not yet instantiated in this snippet. The sample shows formatting, **not an executable, complete RC01**. Candidate B uses identical nine role arrays as in `schema/contract_document.schema.json`, with source ID `urn:study:RC01:S1` and evidence status `NOT_EXECUTED`; a full cross-encoding sample is part of RC examples file.

## Controls for candidate comparison
Case material equal, type/authority complete, no syntax-inferred physics, no fabricated default. Compare 42 SLR coverage, parser status, AST loss, edit/token counts, authors' median task time, error/ambiguity, diagnostic quality. Current comparison is qualitative DESIGN ONLY.
