# ML-C22/01 – Reuse-first interoperability obligations
ML-C22 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
CSNF base 2f0297b754e3a96a2523a34d3af98782b26181f3; mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce. OMG SysML 2.0, KerML 1.0, Systems Modeling API 1.0; pilot 2026-09.1 is IMPLEMENTATION, not normative. G1 BLOCKED.

Null hypothesis H0: existing standard language with a small, controlled extension encodes all relevant external study obligations with fewer total effective costs than a separate syntax. Compare against A minimal own kernel, B SysML/KerML CSNF, C federated mappings; H0 is the sufficiency claim of the standard-profile option, not a separate parser implementation.

Mapping contract requires identity, type, scope, guarded assumptions, guarantees, physical quantities (kind+carrier+unit+basis+sign), observables and KPI computation basis, VariationPolicy, Owner/Authority, independent Evidence REQUEST/RESULT and SourceSpan. Evaluate E1 structural matching and audit identity **separately**. An implementation with external profile/sidecar may be valid, but any dependence on it counts as extension burden; absent data never silently defaulted.

Controls: same RC01–RC10 and C23 frozen oracles; versioned source pins, explicit mapping cardinality, semantics before syntax, loss classification ObligationLoss / OwnerStatusLoss / SourceAuditLoss / ObservableLoss / VariationLoss / EvidenceLoss. No language architecture decision until B2 comparative evidence.
