# ADR-C1-COMP-01 — Select M3-Hybrid for further research development

**Status: SELECTED FOR FURTHER RESEARCH DEVELOPMENT. NON-NORMATIVE / RESEARCH ONLY.**

Decision criterion: achieve all original requirements with minimum additional implementation, integration and maintenance burden. A combined option is explicitly permitted by the requested research decision. This records the actual engineering direction rather than leaving the development choice unresolved. It is not approval of individual study methods, proof of scientific conformance, or authorization for production.

## Decision

Select **M3-Hybrid**: native pinned mathspec Canonical Specification and public typed Program are the single mathematical authority; retain and adapt existing R1/R2 external-contract, quantity, configurable method/profile, governance, provenance and verification functionality where applicable. M0 remains frozen comparison and fallback. M2 is limited to evidenced, fail-closed legacy migration/interoperability, not the primary development architecture. Do not maintain two authoritative mathematical normal forms. Existing code remains intact pending actual ablation and later approval of removal.

## Evidence and tradeoffs

On identical derived RC fragments, M3's static boundary and bounded finite consumer succeeded for 10/10; the native-to-legacy predicate target succeeded on 3/10 (legacy owner BLOCKED retained), the unchanged profile Engine numerically evaluated 2/10. The two shared numerical cases agree exactly; three legacy M0/M2 projections have equal semantic and audit digests. These are different evidence depths and uneven maturity, not general architecture pass rates. Additional EX08 preintegrated costs agree; EXPOW supports data-dependent integer exponent in legacy profile while the current M3 admission rejects it. ABL09 shows mathematically consistent output with invalid scenario probabilities accepted by the M3 finite maths but rejected by original profile and independent oracle. ABL11 shows existing exogeneity checks. The R1 outer control preserves request/response quantifier structure, Unknown guard and service evidence blocker. Both original R1 timing profiles retain identical exact numeric outcomes across R1 and MS1 consumer. ABL06 reveals current M2 audit-source mapping loss; underlying legacy CSNF can preserve source if explicitly mapped. ABL08 reveals M3 current semantic hash overdistinguishes documentation-only changes. Both need exact source admission (ABL07) and typed context (ABL01–05). No general equivalence proof.

M0 retains the strongest representation independence but requires extensions to general mathematical constructs already available natively. M2 retains existing representation and profile infrastructure but requires a wider translation and target math extension. A greenfield M3 rewrite would unnecessarily recreate existing domain semantics. M3-H retains the mathematical simplicity advantage while reusing demonstrated nonmathematical features. This is a qualitative incremental architecture judgment, not a measured total effort estimate. Raw source line counts are reported only as inspected file metrics, not savings. The actual hybrid integration is still to be completed in C2/C3.

## Consequences

- Pin the bounded v0.2 native boundary and package v0.1 as C2 working interfaces at the tested C1 baseline. Changes only through explicit versioned, regression-tested extension. No claim that all constructs are frozen/final.
- C2 independently closes external obligations and method bindings. Reuse actual old checks instead of rewriting by default. Add dynamic integer-power admission with positive/base/domain proof; preserve exact source and dimensional typing. Reuse weight role and exogeneity validation, contribution lineage, method source/owner rules and output bindings. Separate canonical bytes, semantic projection and audit identity.
- C3 integrates both original language paths, eliminates extension bypass and completes the original A/B materialisations. M2 translations remain optional interop, not mandatory intermediate in the selected architecture.
- C4 proves all original requirements and preserves 58 identities / 116 paths / 105 traceability IDs, comparable evidence and model freedom; decides scientific acceptance and later deprecation. Reopen this engineering choice only on concrete falsifying evidence, not another broad language survey.

The prior Option F applies to insufficient evidence for **final scientific approval**, not to the now-resolved development direction. Original gates C1-A1–A4 and B1–B3 are not promoted; MS-G6 remains NOT_READY for final scientific acceptance. Original OWNER_TBD and no 04B release unchanged.

Evidence: tested commit 8802240fc162e6da0aea22800a5331d7623635f7, CI 45995179530, job 140492665768; comparison_results.json, ablation_results.json and architecture_comparison.csv.
