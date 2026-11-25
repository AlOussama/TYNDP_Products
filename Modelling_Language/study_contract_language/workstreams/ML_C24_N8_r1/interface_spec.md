# R1 interface and proposed extension specification
NON-NORMATIVE / RESEARCH ONLY

Executed interface: prototype/research_chain.py and independently authored contract.a / contract.b.json, external method and study JSON files, data snapshot, local_execution_manifest and method_swap_runs. These fixtures and executable validators are the authoritative finite-interface examples, not a complete versioned language schema. The original C21 is preserved as a separate compatibility validator.
Proposed versioned semantic relations (not implemented in full):
- StudyContract(id, version, domains, components, ports, assumptions, obligations, observable definitions, authority refs, evidence requests).
- TypedExpression(operator registry version, type, ordered operands/binders, scope, unit/basis, provenance); reference resolution uses typed IDs, not strings masquerading as formulas.
- MethodProfile(id, version, rule DAG, applicability, parameter declarations/bounds, override policy, external method source); StudyProfile(method ref/version/hash, binding to StudyContract, data snapshot, parameters, declared variation and decision).
- InputDataSnapshot(id, source identity, content hash, typed arrays/axes, exogenous context and observable binding); data content and authentic source evidence are different.
- Contribution(id, typed source projection, atomic coverage, lineage DAG, aggregation rule version, overlap policy); use is separate from semantic additive coverage. Reuse of a data value is not intrinsically double counting.
- EvidenceRequest(subject, obligation, verification scope, required evidence); EvidenceResult(request ref, run identity, result, method/data/contract hashes, verifier, status). Source authenticity and owner decision require independently verifiable authority, not a hash alone.
- Canonical and audit digests with declared inclusion/exclusion policies; retain raw source identity. Unknown is a distinct typed state.
Prefer reuse of CSNF relations, scope, typed sets, aggregation and expression composition before adding domain-specific operators. No CBA-specific core rule. Native SysML/KerML, GEMS and mathspec integration remains NOT_EXECUTED.
