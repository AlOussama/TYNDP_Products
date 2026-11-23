# ML-C21/02 – Parser-independent validator architecture
ML-C21 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 ML-C19 2f0297b754e3a96a2523a34d3af98782b26181f3; Python 3.13.5 stdlib-only local synthetic fragment. No C20 syntax parser, solver, GEMS/mathspec native tests or SysML pilot. G1 BLOCKED.

```text
Typed CSNF fixture --> structural/type/reference checks (R00,R01,R08,R10,R11)
                   --> deterministic finite rewrites (R02–R07,R09,R12,R13)
                   --> canonical semantic/audit projections + rule trace
                   --> E1 fragment comparison or diagnostic BLOCKED/ERROR
                   -X-> universal E2/E3/E4/E5 conclusion
Future C20 syntax parser --adapter--> exact same typed CSNF interface (NOT_INTEGRATED)
```
Versioned signature: `validate(dict)->list[Diagnostic{code,path,severity,detail}]`; `normalize(dict)->(dict, trace)|CSNFError`; `compare_e1(a,b)->{e1,audit_equal,e2,e3,e4,e5}`. `AUTHORITIES` remain independent records, not copied into untyped string comments. Canonical JSON textual encoding is a *hash input* for this experimental fragment and only comparable under equal pins. No assertion that all semantically equivalent formulas normalize to identical hashes.
