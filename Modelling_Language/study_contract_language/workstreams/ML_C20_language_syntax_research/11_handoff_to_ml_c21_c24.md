# ML-C20/11 – B1 versioned interface handoff
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

Protocol identifier `CSNF-AST-RESEARCH-0.1`. Input: C1–C9 role discriminators, QualifiedID, typed expression, external-port carrier/unit/sign, Scope, time/scenario information set, data source, separate Evidence REQUEST/RESULT and Authority. Only an explicitly versioned schema/registry release can be integrated. JSON Schema is a *research envelope*, not the canonical validator language standard.

C21 must consume the *typed semantic contract* independent of parser. Any future AST adapter promises `parse_A : Text -> TypedContract|Diagnostic` and `decode_B : JSON -> TypedContract|Diagnostic`, total on declared fragment or explicit BLOCKED; typed object retains sidecar SourceLedger. C22 export mapping must declare semantic/audit preservation fields. C23 supplies frozen oracle `ML-C23/research-r0.1`. C24 must not integrate until B1 signature compatibility confirmed and B2 execution evidence available. G1 BLOCKED.
