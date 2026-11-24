# ML-C24-N4 — native reuse preflight and comparative design
NON-NORMATIVE / RESEARCH ONLY. B0 2f0297b754e3a96a2523a34d3af98782b26181f3. C22 828c87eb100646da6fcce5f8751af5f3f42c7600; P3 0e85be6d9d2a84dffd7bb2685e6548671be3ef17; P5 eaea6dd99b736f2560866abda722cde78b908bce; decision PR65 63e36207351a23f2290c25ffd865a166e03e1bc8.

Source-checked exact pins: [mathspec canonicalizer](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/_canonical.py), blob a8487b60f03839fc622834ffcaf76e1f9c99f6e9; [GEMS library](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/library.md), blob 01a5b0f5555a44fe5cd89e99c23989d6024bdefa. SysML 2.0 / KerML 1.0, Systems Modeling API 1.0 (P3 pinned design references; no native engine). Pilot release 2026-09.1 from P3, not installed or verified in this experiment.

Executed: python preflight.py under Python 3.13.5. Java 21 available, mathspec import false, GEMS and SysML CLI absent, Julia absent; local Git network DNS failed. Native parse/type/roundtrip NOT_EXECUTED; measured semantic and audit losses UNKNOWN. Do not infer inability of any standard from unavailable runtime. H0 UNRESOLVED; B3 NOT_READY; G1 BLOCKED.

## Common experiments (DESIGN_ONLY)
Use N1 RC01 and CBA fragments, N2 paired finite dataset and begin/end profiles. Preserve semantic digest and separate audit/provenance, exact source and method hashes, OWNER_TBD; native export/reimport with same oracle. No counting design sketches as coverage.

| Candidate | RC01 reuse | Paired study and external profile switch | Additional semantic profile (hypothesis) | Audit risk (unmeasured) | complexity hypothesis |
|---|---|---|---|---|---|
| SysML/KerML | typed Port, Part, Connection; Requirements/Constraints | typed case relations and expression/metadata model; imports | carrier, unit/sign, scenario and time domains, quantifier support, method rule types, variation policy | owner/source/version and run evidence identity require typed metadata and preservation tests | broad standard; tooling/profile integration |
| GEMS | port-types/fields, system connections, binding constraints | data/parameter substitution; native method-rule swap not established | study frame, paired cases, external A/G distinct from library equations, observables and method schema | library versions insufficient for owner/evidence and resolved run provenance | reuse model/port schema; external contract layer needed to test |
| mathspec | typed symbol/dimension and algebraic expression conventions | expression canonicalization and parameterized algebra; full method profiles not established | stable external port roles, explicit case/authority/evidence/variation semantics | canonical YAML alone not proof of audit identity | reuse expression AST/normalizer; wrapper/profile unknown |
No scores or loss measurements. A textual sketch, executable expression library or solver is not a native study-contract test.

## Critical review (AI-internal; not independent human review)
Unknown native behavior prevents fair ranking; compare C1-C9 using frozen P3 registry and identical inputs. Do not assume absence of capability from absent evidence. Test negative guard, basis, authority, evidence, double-count and changed method source. Record install commands, pinned dependencies, native outputs and failed mappings; estimate actual profile counts only after executable builds. N4 must not artificially hold N1/N2 gates.
