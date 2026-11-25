# Integrated method swap — finite slice, PARTIAL
NON-NORMATIVE / RESEARCH ONLY

Four actual runs: A/B × undiscounted/discounted. Shared context and data, unchanged runtime code, no rebuild during switch. Method rules differ structurally (discounting operations, not merely parameter values). Data and method identities are canonical hashes; source/audit identities are separate. No normative CBA indicator validation.
Independent hand-derived oracle: weighted increments 27.5 and 55; undiscounted = 82.5; discounted = 27.5/1.1 + 55/1.1^2 = 775/11 ≈ 70.454545. Both syntax inputs agree exactly. See prototype/method_swap_runs.json for exact outputs, hashes, and typed graphs.
Research chain SHA256 efba3de1c73dd0030bfa0d8de3de9e19623c32cd4de180548e711d0e07b92e90; C21 SHA256 b59c7f1c4570df2ac3141fb75a1c0d3432d8259ffa3ebee142a2470988f4adc1.
Canonical graph 54deb1a88bf4bc154123be910cd2669a20aa04945730aeac4571de73ae502ca4.
Canonical data b32b54462e0f9420599fb998a6c437bebe7ca95ae232200124ef04c395768341.
Methods 21f06441b7bd1aaaa95a6c367cd3da8e241b0c0f5a49dc2cc522a1a4040590b8 and e808c2afc1ca7a5ef8df6cd1cf272aeb212566f9df9259b3b7de029455c5f038.
Audit A-undiscounted e7010aa518090447106729b057dd361f950ae25667c7ca335830f480e4395d7d; A-discounted 607f3a6810d5225e1a0377870ed8a7220d9b66f491ecf0c59364f02e9063a487; B-undiscounted 33e39347143cdf3702273fb0e45a263d9c15042237e38499858ae3e4c4d30eac; B-discounted 7e7ff4fc29b51e82c2b889a44e1588c10a479fcb396167e520ae94bc1f747c37.
## Limit
The method AST is not lowered through the full CSNF/C21 chain. Some profile scopes and dependencies are restricted; no full unit/price-year/currency algebra or authorized override. Shared-context equality is over the declared context, not authenticated underlying sources. Guards are not fully carried into C21 or enforced as method applicability. Ledger coverage is declared rather than derived from expression lineage. Accordingly the integrated-method-swap gate is PARTIAL, not MET. The two profiles are illustrative and not approved ENTSO-E methods.
