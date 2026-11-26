# modelling freedom report

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

| Required example | External obligations | Independent check/proof boundary | Internal variation |
|---|---|---|---|
| Battery RC01 | P sign, dt, I=-P·dt when charging, energy ledger/loss, bounds/terminal authority | 2 MW × 1/2 h = 1 MWh; SOC=19/40 × 4 MWh = 19/10; 2 MWh rejected; terminal still OWNER_TBD | SOC vs energy state; state mapping not a solver variable mandate |
| EV RC02 | Each individual deadline/service, connection and non-vacuous request support | [1,1] satisfies two 1 MWh requests, [0,2] fails despite same aggregate; no fleet-wide feasibility proof | Individual vs aggregated plus verified individual witness |
| Electrolysis RC03 | LHV-labelled carrier conversion envelope 3/5–4/5 | at 1 MW, 21 vs 18 kg/h with 1/30 MWh/kg meet envelope, 30 fails; distinct outputs | constant vs piecewise/variable efficiency allowed if envelope and capability proven |
| DC grid RC05 | KCL and KVL with common orientation, topology/reactance scope | triangle f=(-1,-1,2), b=(-3,0,3), sum f=0; circulation f+(1,1,1) preserves KCL but violates KVL | angle vs cycle/PTDF; equal reactance finite case is not general proof |
| Stochastic RC07 | decisions equal on same pre-revelation information set | shared a=b on declared pair; different value fails; all-false guard or unknown blocked | shared first-stage var vs scenario-indexed with nonanticipativity |
| RC04/06 | mass ledger; integer modules | explicit single step and integer domain; not complete temporal proof | hidden representation free |

The finite native observation consumer accepts or rejects selected projected witnesses; original pinned test_freedom.py additionally tests synthetic alternative formulations. Neither establishes universal conformance of a real model. RC01's terminal authority, RC02's complete individual request enumeration, RC03's full admissible conversion domain, RC05's general topology proof and RC07's policy/partition completeness are still open. RC10 remains a contract-level governance/evidence requirement. E4 and E5 not promoted.
