# ML-C21/07 – Executed synthetic cases and remaining gaps
ML-C21 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 ML-C19 2f0297b754e3a96a2523a34d3af98782b26181f3; Python 3.13.5 stdlib-only local synthetic fragment. No C20 syntax parser, solver, GEMS/mathspec native tests or SysML pilot. G1 BLOCKED.

The module `tools/test_csnf_validator.py` contains 31 executed stdlib tests including deterministic/idempotent normalization, AND nesting/order, explicit kW/MW and minute/hour, Owner-TBD, source multiset, audit-only differences, KCL/KVL discrimination, injection/consumption, REQUIRED/PERMITTED, fake PASS, incompatible H2, port incompatibility, ambiguous IDs/refs, information leakage finite snapshots and forced SOC restriction. Actual local command: `python -m unittest -v test_csnf_validator.py` in the `tools` directory.

| Golden RC | Scoped mutation oracle | Current evidence |
|---|---|---|
| RC01 | energy integration requires known duration; sign direction must remain | TIME_INTEGRATION_DURATION_MISSING or E1_DIFFERENT |
| RC02 | per-vehicle deadline service quantifier | NOT_EXECUTED; no fleet service solver |
| RC03 | electricity MW vs H2 mass/energy basis | UNIT_OR_CONVERSION_BASIS / PORT_CARRIER_MISMATCH |
| RC04 | H2 mass vs H2 energy without approved LHV | UNIT_OR_CONVERSION_BASIS |
| RC05 | KCL-only versus KCL+KVL | E1_DIFFERENT (not generic E4 failure proof) |
| RC06 | discrete investment module contract | NOT_EXECUTED; no integrality oracle |
| RC07 | synthetic stage-1 decision depends on future revelation | INFORMATION_LEAKAGE |
| RC08 | cost KPI price basis or missing duration | PRICE_BASIS_MISSING / TIME_INTEGRATION_DURATION_MISSING |
| RC09 | CBA owner/TBD and baseline mutation | OWNER_UNRESOLVED BLOCKED only; no N2E method judgement |
| RC10 | source identity/evidence status and extra assumptions | AUDIT_DIFFERENT / UNSUPPORTED_PASS; full model comparison NOT_EXECUTED |

These do **not** constitute two independently implemented energy models per RC nor a full positive+negative matrix for ten cases. RC02/06, full RC09, physical network feasibility, EV service quantifiers and all native parsers remain NOT_EXECUTED.
