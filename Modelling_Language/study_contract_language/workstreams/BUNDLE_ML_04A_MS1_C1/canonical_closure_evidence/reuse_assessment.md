# Measured reuse and necessary extension assessment

**NON-NORMATIVE / RESEARCH ONLY**. Scope: pinned public mathspec Program, tested commit 0a61f8415a45a365fc14ef3c5a71dfa87a5b01c4.

- Nine arithmetic node families from C1: Constant, ParameterReference, ExpressionReference, Negate, Add, Multiply, Divide, Power, Sum.
- Four additional expression node families admitted with restrictions: Join (closed lookup/group sum), Translate (explicit nonnegative offset and edge), WindowSum (constant bounded width and edge), Cases (all regions checked).
- Twelve condition-node branches handled: BooleanLiteral (only synthetic masks), ParameterDefined (bool only), ParameterComparison (dimensionless exact integer literal), ExpressionComparison (compatible quantity and explicit alignment), ConditionReference, And, Or, Not, DimensionPosition, DimensionComparison (integer label), JoinedCondition (closed lookup), CountComparison. Static native reuse, no general truth/evaluator implementation.
- Native condition syntax, relation declarations, index resolution, case-region typing, AST traversal and canonical YAML are used directly. No independent mathematical parser, persisted AST or normalizer. Quantity validation, lexical admission, finite support checks, profile/role context and audit are additional domain-specific functions, not native replacements.
- No complete M0/M2/M3 code-equivalent comparison; no quantified LOC savings, global minimality or ablation claim. M0 remains the comparison reference; legacy M2 mapping remains an original gate criterion until owner revises it. No removal of existing implementations.

## Why certain restrictions are necessary
Float preimage collision was established in PR #87. Integer-token admission rejects decimals/exponents before native loading, including tiny exponents that round to zero. Native Mask folds constants, so literal booleans in authored conditions are rejected to preserve static review of branches; native Cases are accepted where all regions survive the bounded profile. Dense keys and every used grouping must have explicit support; zero-filled shift and clipped/wrapped window require explicit policy. These are conservative research restrictions, not proof that each exclusion is globally necessary. Native constraints/variables/dual/objective are excluded from external-observable profile; solver formulations remain independent.

## Concrete remaining scope
RC01/04: physical chronology, initial/terminal authority, time duration and complete ledger. RC02/07: nonvacuity, service capability and information/nonanticipativity. RC03: general conversion authority and direction/sign transitions. RC05: arbitrary topology, empty groups and physical reactance; current equal-coefficient triangle only. RC06: integer data and module types supported, full investment contract not materialized. RC08/09: actual method binding and contribution/event policy. RC10: evidence lifecycle and equivalence claims. No new original full A/B paths.
