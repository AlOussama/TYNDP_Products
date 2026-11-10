# BUNDLE-01R C — Requirements Change Proposal (HOLD, no normative changes)

**Proposal version:** `B01R-RCP-0.1-DRAFT` · **Status:** `CHANGE_NOT_AUTHORIZED` · **Original MA01 baseline:** PR #17 `a86bbeb8377ac1c9a5c77d900ad287691397e506` · **Original MA02:** PR #18.

## Controlled change disposition

|Item|Scope|Trigger/required evidence|Current disposition|
|---|---|---|---|
|RCP-01|All 48 MA01-SR; source validity|Approved 2026 IoSN release/version, original bytes/hash/effective dates, authoritative A/B clauses or explicit no-change approval|**ON_HOLD / 0 verified deltas**|
|RCP-02|Input-related L2/L3 requirements|Owner-validated exact frozen run data, source identity, unit/calendar/zone/technical grain and acceptance tests|**ON_HOLD**, no data assertions promoted|
|RCP-03|L3 mathematical semantics and L4 tests|Qualified reference cases for equivalence grid, market links, LP stage/finance, H2/storage/OPF/KPI and numerical acceptance|**ON_HOLD**, not syntactically sufficient|
|RCP-04|20 process-only objects|Domain/Requirements owner disposition as direct SR obligation versus controlled process support input|**OPEN_ALLOCATION**, not an automatic new SR|
|RCP-05|MA01-MR-012 and -049|Verify only selected-case input/scope; no upstream PCA/K-Means requirement|**NO_SCOPE_EXPANSION**, preserve existing out-of-scope classification|
|RCP-06|MD-/CL-specific clarifications (21)|Only an authorized owner decision with study-year scope, alternative chosen, example, signed artifact|**OPEN**; do not rewrite SR text|

### Required edit control if authorized later

A signed, versioned change request must cite exact old/new text, MR source clauses, original SR, impacts on inputs/processes/L3/L4, baseline revision, test data and numeric oracles, decisions and approvers; update new MA01 branch and release only after independent review. Never overwrite the existing MA01 baseline silently.

**All current 48 SR are left byte-for-byte unchanged.** There is no authorized new requirement, suppression of an SR or superseding IoSN methodology at this stage. No modelling-language or tool adapter choice is made.
