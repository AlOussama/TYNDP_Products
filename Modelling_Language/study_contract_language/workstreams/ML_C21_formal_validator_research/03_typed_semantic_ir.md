# ML-C21/03 – Independent typed semantic IR fragment
ML-C21 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 ML-C19 2f0297b754e3a96a2523a34d3af98782b26181f3; Python 3.13.5 stdlib-only local synthetic fragment. No C20 syntax parser, solver, GEMS/mathspec native tests or SysML pilot. G1 BLOCKED.

`frame{id,schema,ruleset,registry,time?,scenario?,imports?}`; 8 role collections `referents, relations, predicates, assertions, observables, variations, evidences, authorities` correspond C2–C9, and `frame` is C1. `referent.kind='port'` contains `quantity:{carrier,kind,unit,value,sign,basis?}`; relations have typed from/to refs; assertions carry modality, decision, semantic_role, predicate_ref, scope, Bool3 guard and authority_refs; evidences carry REQUEST/RESULT, run ID and status; authorities have immutable_ref and decision. Frame contains explicit time duration and optional synthetic stage1 scenario values.

Roles are **structurally typed at selected fields**, not complete AST+quantifier modelling. Scenario finite value check is a *specific synthetic anti-leakage oracle*, not proof of universal nonanticipativity. Context sources `ML-C19/05,06,07`. Any integration from C20 must map without default and pass B1 compatibility tests.
