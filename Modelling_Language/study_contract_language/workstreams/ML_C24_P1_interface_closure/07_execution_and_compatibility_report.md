# P1 execution and gate report

Run ID: `P1-V8-20261123-r0.1`; executor: isolated JavaScript/V8 tool context, exact engine version not reported. Input `data/rc01_positive_candidate_b.json` and the negative original C21 input (pinned source copy). Inline bridge run: **15/15 synthetic checks pass**; typed RC01 returns `BLOCKED`, because `OWNER_TBD` is retained and explicitly surfaced. No hidden promotion to `APPROVED`. C21 Python validator execution in the same runtime: NOT_EXECUTED. Candidate A full parser: NOT_EXECUTED. All other RCs: NOT_EXECUTED.

**B1_PARTIAL**, not B1_MET. Schema migration coverage is a restricted fragment and semantic equivalence of registries is unproven. B2_NOT_MET; G1_BLOCKED.
