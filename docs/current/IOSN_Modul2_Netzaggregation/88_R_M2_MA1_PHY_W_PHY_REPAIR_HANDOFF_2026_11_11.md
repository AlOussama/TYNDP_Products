# W-PHY Repair Handoff — R-M2-MA1-PHY Independent Review 2026-11-11

**Worker role only:** W-PHY; **Reviewer role remains separate:** R-PHY.  
**Decision to repair:** `REPAIRS_REQUIRED` (four independent P1 findings, no discovered P0).  
**Scope:** `src/tyndp_reduce/iosn_official/contracts.py`, `physical.py` and worker-side tests only. **No** M0, M1, weather-selection, main merge, real-network or MA2 runtime release.

## Frozen starting points

- Original integrated code-freeze `0254d867a34b66ec7b56c90225605d29ea328916`, documented PR #13 head `70e92ba9e62a320e58227ce9c2f03fad266f44bf`.
- Independent scientific tests, unchanged: [`test_r_phy_independent_20261111.py`](https://github.com/AlOussama/TYNDP_Products/blob/c0dd75de1285296da420fd0eb77d29f60efd7d92/tests/iosn_official/test_r_phy_independent_20261111.py).
- Full review: [87](87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md); [Findings JSON](R_M2_MA1_PHY_FINDINGS_20261111.json); [independent CI](https://github.com/AlOussama/TYNDP_Products/actions/runs/43077807614).

## Single consolidated repair macro

1. Create a **distinct worker branch**, e.g. `work/iosn-m2-ma1-phy-repairs-20261111`, from the integrated PR #13 code/head; pin parent SHA; do not push changes to the independent R-PHY review branch.
2. **PHY-R01:** eliminate live caller-owned mutable sequences from every frozen input/cache contract. Use defensive canonical tuples with type/element checks or explicit rejection, and verify fingerprint cannot be externally changed after validation. Preserve SHA and array semantics.
3. **PHY-R02:** enforce strictly boolean `HVDCTerminals.lossless`, with `False` still `REJECTED_COMPONENT`. Strings `"False"`, integers `0/1`, null/unknown flags must fail closed.
4. **PHY-R03:** enforce strictly boolean `ACBranch.in_service` before `active_branches`; check related flags including `incomplete_110kv_ties` and `Provenance.synthetic`. No implicit truthiness for topology or synthetic/real status.
5. **PHY-R04:** reject NaN, infinity and unsafe large finite `atol_mw` tolerances before any sparse solve; explicitly preserve a bounded non-overridable island-balance/KCL acceptance criterion. Document scientifically justified tolerance and numerically test an unbalanced 2-bus network.
6. Run package regression and independent 10-bus three-island cycle-space oracle, 1001-bus sparse case, five-snapshot original fixture and repeat all negative attacks. Do **not** delete, relax or alter the independent review tests to turn defects into artificial passes.
7. Publish worker branch, implementation commit SHA, worker-side tests, CI run/job links, diff summary and evidence manifest. Request a **new independent R-PHY re-review** of that exact repair SHA; no self-approval, no forced `ACCEPT_SYNTHETIC`.

### Reviewer acceptance gate

R-PHY must replay the four originally strict XFAIL attack cases against **the repair SHA**. On a correct repair, the strict-XFAIL wrappers in the frozen reviewer test source will become XPASS (red by design); the reviewer, **not** the worker, then removes/reclassifies the markers on a distinct re-review evidence branch, records the transition to ordinary PASS, repeats all regression/numerical checks, and issues a new decision. Each source/test change must be traced by commit.

### Still blocked after code repair

Real-Europe/37-country/102-zone input source bytes, exact provenance hashes and TSO/PyPSA tap/PST/HVDC-loss/contingency semantics remain separate `BLOCKED_DATA` and `BLOCKED_INTEGRATION` gates. R-CLU is a distinct independent review. Code repair alone never authorizes real network, merge or MA2 runtime.
