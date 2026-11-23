# Cross-workstream diff (verified pinned sources)

NON-NORMATIVE. Fixed B0 `2f0297b754e3a96a2523a34d3af98782b26181f3`. ML-C20 `b81edeb7551aa786e0d309ccd5bc2271d244e450`; ML-C21 `cad6d30edf32476ee5e915dbea7566127cbffa5f`.

| Difference | Type | Resolution / limit |
|---|---|---|
| frame.schema C20-research-0.1 -> CSNF-C21-0.1 | Version | Explicit opt-in mapping for one frozen version only; registry equivalence NOT_PROVED |
| frame.registry energy-r0 -> energy-c21-0.1 | Version/semantics | Explicit mapping tested structurally; physical equivalence NOT_PROVED |
| authority.decision_state -> decision | Type/status | Explicit same-domain mapping with source-side audit copy, no default |
| referent.external_port -> port | Type/semantics | Only typed external_port accepted; marker external=true and source referent type kept |
| observable semantics prose vs typed projector | Type gap | Prose rejected; restricted typed projection checked |
| contractPredicate placeholder | Predicate gap | Rejected; bounded typed AST support only |
| quantified guarantees | Formal gap | forall/exists syntax and typed domain checked; runtime quantifier truth NOT_PROVED |
| C23 golden RC01–10 | Oracle gap | C23 remains pre-registered conceptual baseline; full executable suite pending |
| C22 SysML/GEMS/mathspec | Native gap | No native execution in this P1 scope |

The original negative C21 RC01 fixture is copied unaltered as a pinned reproduction input; it is deliberately incompatible with strict typed mapping.
