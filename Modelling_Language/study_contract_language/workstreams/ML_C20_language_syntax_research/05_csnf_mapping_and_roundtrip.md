# ML-C20/05 – Syntax-to-AST-to-CSNF lowering and reverse projection
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

```text
CandidateA text --parse_A--> AST_A --type/resolve--> TypedContract
CandidateB JSON --decode_B--> AST_B --type/resolve--> TypedContract
TypedContract --lower(versioned_ruleset, registries)--> CSNF semantic graph + AuditLedger
CSNF --canonical_surface(candidate, fixed renderer version)--> representation
```
## Lossless map conditions
C1 frame -> frame; C2 referents -> typed nodes; C3 relation -> typed edges; C4 predicate -> typed expression AST; C5 assertion -> guarded modality+A/G; C6 observable -> typed projection with temporal/price basis; C7 variation -> explicit choices/disclosure/proof; C8 evidence -> REQUEST or RESULT with unchanged status; C9 authority -> independent source/owner/decision/provenance IDs. All normalized IDs must maintain source-span and alias history in a sidecar ledger. Audit equality includes individual authority multiplicity, revisions, decision states, evidence status/run IDs. Semantic E1 is assessed only under same `schema|ruleset|registry` pins.

## Roundtrip contract
Define `semantic_projection` and `audit_projection` independently. For each legal input, require `semantic_projection(parse(render(lower(parse(x))))) == semantic_projection(lower(parse(x)))` and the equivalent audit projection. Raw comments: only explicitly designated domain-meaning comments are modeled as typed doc/source clauses; arbitrary formatting comments remain in raw SourceLedger and are not semantically compared. SourceSpan byte offset + URI/version are saved; canonical rendering need not reconstruct the exact original whitespace. Migrations require explicit adapter version and controlled diff; no last-write-wins.

## Error taxonomy
UNRESOLVED_REFERENCE, AMBIGUOUS_ALIAS, WRONG_KIND, UNIT_DIMENSION, CARRIER_SIGN, GUARD_UNKNOWN, STAGE_INFO_LEAK, SOURCE_MISSING, OWNER_TBD, EVIDENCE_NOT_EXECUTED, POLICY_CONFLICT, ROUNDTRIP_LOSS. Severity FAIL_STATIC / BLOCKED / INCONCLUSIVE and actual E1 verdict separated. None is a universal E2–E5 proof. Until parser and adapter run: ROUNDTRIP_NOT_EXECUTED.
