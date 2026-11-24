# ML-C24-N5 — generality and modelling freedom
NON-NORMATIVE / RESEARCH ONLY. B0 2f0297b754e3a96a2523a34d3af98782b26181f3; C23 d3d5362231d81a00fd6a19501bc7187f4ad12da5; P4 4b61addb0e87205e6670e253bd65cb0428e08681; P5 eaea6dd99b736f2560866abda722cde78b908bce; decision PR65 63e36207351a23f2290c25ffd865a166e03e1bc8. Golden catalog frozen unchanged using original Git blob.

## Actual execution
Python 3.13.5, stdlib, exact Fraction arithmetic. Run python test_freedom.py. Local run 7/7 checks. This is a finite standalone oracle, not a language-chain RC suite or real-model comparison. All numerical parameters are synthetic research choices, not owner-approved.
- RC01: same signed external traces from SOC versus MWh states, half-hour step, explicit efficiency and initial/terminal state; negative overflow and grid intake check.
- RC02: individual deadline witness vs aggregate envelope on two EVs; total energy alone admits an invalid schedule.
- RC03: constant versus piecewise efficiency, both satisfy sampled external envelope, but their outputs differ; explicit synthetic LHV. This directly distinguishes conformance from mathematical equivalence.
- RC04: mass ledger vs energy inventory under an explicit fixed LHV and loss convention; incompatible basis negative.
- RC05: angle model vs cycle model with oriented 3-bus triangle, identical finite external flow set; KCL-only circulating flow fails KVL.
- RC06: integer module variable vs binary encoding, finite projected choices; fractional module rejected.
- RC07: shared first-stage variable vs scenario-indexed equalities, identical finite projection; future-information leakage rejected.

## General Assume-Guarantee semantics (design)
Assumptions define domain, boundary conditions, carrier/unit/sign/time support, exogenous inputs and permissible service requests. Guarantees constrain external projected traces and observables, not necessarily internal variables. Safety: all admissible external traces obey constraints. Capability: for every admissible request there exists a feasible response, not merely one existential witness. E5 conditional on separate evidence for each internal model. Equality of finite projected sets is not proof for continuous domain/general horizon. Need explicit evidence level, semantic scope and variation disclosure. No normative terminal/efficiency/price rule fixed in core.

## Critical review (AI-internal, not independent human audit)
Synthetic test denominators not representative of full RCs. RC02 has a tiny service domain, RC03 only samples points, RC04 is a single trace, RC05 uses equal reactances and bounded integer flows, RC07 only first stage; no independent solvers. The original RC01–10 requirements remain unchanged. RC08/09 limited evidence in N2 (not original golden suite), RC10 not executed. Full C23 18 mutations, P5 30 mutations, full SLR/NFR/K coverage and E2–E5 remain unproven. B1/B2 PARTIAL, B3 NOT_READY, G1 BLOCKED. No forced internal mathematical formulation, no architecture decision.
