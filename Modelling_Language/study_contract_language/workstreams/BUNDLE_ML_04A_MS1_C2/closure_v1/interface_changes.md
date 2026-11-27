# ICR-005 — Targeted C2 closure, no architecture reopening
- Interface finite_consumer delegates to CompleteFinite; old public package and mathspec authority unchanged. Added only admitted missing node evaluation and explicit conditional execution.
- WS_B.methods separates check_static from validate, adds explicit SUM_RANGE and bool/int parameter validation; original four profiles and existing C2 tests retained.
- New closure_v1 metadata, obligations, graph, ledger, identity, definition. R1 original table/quantity, monetary conversion and N7 contribution checks reused; R1 partition validation extracted faithfully into r1_reuse.py. No original R1/C1 source modified.
- Definition 0.1, instance 0.1 and closure package 0.2 are new research interfaces; previous root package 0.1 remains a tested historical interface. Preserve source-specific pins and strict fail-closed fields. No implicit backward migration.
- Scientific decision: no new broad architecture comparison; source and scope-specific unimplemented features recorded as explicit remaining blockers. No C3 until gate decision authorizes it.
