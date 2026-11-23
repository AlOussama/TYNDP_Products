# ML-C21/04 – R00–R13 implemented fragment / excluded transformations
ML-C21 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 ML-C19 2f0297b754e3a96a2523a34d3af98782b26181f3; Python 3.13.5 stdlib-only local synthetic fragment. No C20 syntax parser, solver, GEMS/mathspec native tests or SysML pilot. G1 BLOCKED.

| Rule | Implemented/check scope | Synthetic test | Excluded scope |
|---|---|---|---|
| R00 | Partial structural and version validation | ERROR missing C1/C2..C9 sections or wrong pins | no surface syntax parser |
| R01 | Strict qualified ID reference check | ERROR unresolved refs, ambiguous/duplicate ID | no alias resolution |
| R02 | Sort explicitly unordered role collections by stable ID | idempotence/role permutation | arbitrary ordered lists not sorted |
| R03 | Guard pure AND/OR order normalize | Boolean commutation test | no arithmetic commutativity |
| R04 | Flatten pure nested AND/OR | Boolean association test | no associativity for floating math |
| R05 | Preserve NOT structure / typed guards | guard structure and arity check | no De Morgan |
| R06 | Exact Decimal-based explicit unit conversions | kW/MW equality, H2 mass->energy block | registry covers only 5 kind pairs |
| R07 | Explicit minutes->hours for duration | 30min equals 0.5h | no timezone, DST, irregular series |
| R08 | Physical connection carrier/kind compatibility only | wrong-port carrier blocked | no orientation/sign inversion rewrite |
| R09 | Preserve source multiset and assertion identifiers | two sources retained and audit diff | no safe body dedup |
| R10 | Reject implicit imports/compositions | unauthorised import error | no authorized composition implementation |
| R11 | No implicit defaults | Owner-TBD preserved; no price basis default | no approved default expansion |
| R12 | Normalize typed observable unit when valid | MWh/currency basis validation | no KPI aggregation proof |
| R13 | Evidence status and request/result retained | fake PASS blocked; NOT_EXECUTED preserved | no external evidence ingestion |

Pipeline is deterministic and finite on a validated acyclic fixture with bounded arrays; E1 uses the versioned serialization and a scope-specific `semantic_projection`. Explicit decimal factors avoid floating rounding in selected unit conversions. Idempotence tested for a finite factory fixture; *global* Church-Rosser/termination, arbitrary operator soundness and critical-pair resolution are NOT_PROVED. R02 sorts only top-level role collections; nested `VariationPolicy.allowed` list intentionally keeps its order pending unordered/ordered annotation. R06 converts only kind-specific approved exact constants; R08 prohibits suspicious connections but performs no sign-adjustment rewrite. No default invents Owner approval or hidden mathematical equation.
