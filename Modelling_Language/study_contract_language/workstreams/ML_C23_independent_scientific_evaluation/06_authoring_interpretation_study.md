# ML-C23/06 – Blind authoring and interpretation study (PROTOCOL ONLY)
Version: ML-C23 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
Common baseline: 2f0297b754e3a96a2523a34d3af98782b26181f3 (ML-C19 draft PR #55). External: mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce; OMG SysML 2.0 / KerML 1.0 / API 1.0. No independent human audit. G1 BLOCKED.

## Human sample / responsibilities
Target at least two independent energy-system modelers and two software/formal-language reviewers; recruitment, conflicts and consent to be documented. No participant has been recruited; HUMAN_TEST_STATUS=NOT_EXECUTED. Assign blinded A/B/C/H0 order by preregistered counterbalance; separate novice/expert skill level and prior SysML experience. Do not simulate humans with LLM answers or report fabricated time.

## Tasks and outcomes
Task 1 encode RC01 battery port, source/owner and ledger; Task 2 RC05 physical branch and KCL+KVL; Task 3 RC07 scenario InfoSet; Task 4 RC08 cost KPI; Task 5 RC09 Owner-TBD; Task 6 repair a deliberately incorrect specimen. Participants receive the same semantics and allowed references; clock start/stop, edit counts, incorrect obligations, ambiguous guards, missing source links, diagnostic resolution time and confidence must be recorded separately. Blind reviewers infer semantics and flag unresolved questions; use exact match to fixed oracle with a category `UNRESOLVED`.

## Analysis
Report median/IQR times per task and expertise, defect count/type, agreement (raw and optionally kappa where applicable), disambiguation questions, usability observations and missing-data counts. Any unbalanced design or incomplete recruiting blocks comparative claim. Pre-register exclusions and retain anonymized evidence references, no invented empirical figures.
