# subset semantic specification

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

See minimal_mathspec_subset.yaml: 20 explicitly enumerated candidate construct families; selected executable subset is smaller than static native experiment. These are families, not a count of grammar productions. Inclusion follows requirement and RC dependency, not syntactic convenience. No claim of proven global minimality.

### S01 — dimensions / unordered domains (KEEP_RESTRICTED)
Original/target mapping: Index domain labels, not units; exact finite nonempty support; qualified CSNF identity retained. Need: SLR-04,13,17,28; NFR-08, RC01,RC02,RC05,RC07. Evidence: native+finite. Relative integration effort: Low native; adapter identity/support. Alternative: Own typed domain.

### S02 — ordered dimensions (KEEP_WITH_ADAPTER)
Original/target mapping: ordered:true supports native indexing; data order and physical chronology explicit; preserve binder order. Need: SLR-17,37,38; R07, RC01,RC04,RC07. Evidence: native static shift only. Relative integration effort: Medium: time semantics. Alternative: R1 time domain.

### S03 — relations (KEEP_WITH_ADAPTER)
Original/target mapping: Keys/roles and at/sum(by) are index relations, not contract relation authority; coverage/cardinality checked. Need: C3,SLR-13,28,38, RC05,RC07. Evidence: source reviewed; join execution deferred. Relative integration effort: Medium. Alternative: CSNF Relation.

### S04 — parameters (KEEP_WITH_ADAPTER)
Original/target mapping: ParameterReference as bound data only; INPUT vs OBSERVABLE vs METHOD_PARAMETER; complete support. Need: C6,SLR-06,20,29, RC01-RC09. Evidence: native+finite. Relative integration effort: Medium: binding and data type. Alternative: R1 observable registry.

### S05 — named expressions / mathematical symbols (KEEP_NATIVE)
Original/target mapping: Native names and expression references with checked dimensions; qualified identity outside. Need: C4,SLR-08,09,31, RC01-RC09. Evidence: native+finite. Relative integration effort: Low. Alternative: own expression AST.

### S06 — indexed expressions / broadcasting (KEEP_RESTRICTED)
Original/target mapping: Only declared complete Cartesian axes in executed subset; join, sparse support deferred. Need: NFR-04,07,08; R00, RC01-RC09. Evidence: native+finite. Relative integration effort: Medium: support. Alternative: own indexed AST.

### S07 — arithmetic +,-,*,/,** (KEEP_RESTRICTED)
Original/target mapping: Exact integer literal subset, rational observations, same units/basis for +; nonzero divisor; bounded integral exponent. Need: SLR-08,14,16,35; R04,R06, RC01,RC03,RC04,RC08,RC09. Evidence: native+finite. Relative integration effort: Medium: quantity semantics. Alternative: R1 arithmetic.

### S08 — comparisons (KEEP_WITH_ADAPTER)
Original/target mapping: Native conditions statically checked; executed adapter compares typed expression pairs; no native data execution. Need: C4,C5,SLR-15,19; NFR-06, RC01-RC07. Evidence: native static and separate comparator. Relative integration effort: Medium. Alternative: CSNF assertion.

### S09 — AND OR NOT / masks (KEEP_WITH_SEMANTIC_EXTENSION)
Original/target mapping: Native absent-as-false not Bool3; external complete guard supports, truth semantics and Unknown block. Need: SLR-18,36; NFR-06,18; R03,R05,R11, RC01,RC02,RC07. Evidence: static; narrow binary guard execution. Relative integration effort: High general Bool3. Alternative: existing R1 typed guards.

### S10 — sum (KEEP_RESTRICTED)
Original/target mapping: Dense finite typed summation; explicit axis; nonempty support, weights outside core, relation-based reductions deferred. Need: SLR-09,16,31; R04,R12, RC05,RC08,RC09. Evidence: native+finite. Relative integration effort: Low/medium. Alternative: own sum AST.

### S11 — at / shift / sum_back (DEFER_PENDING_EVIDENCE)
Original/target mapping: Keep native index semantics as candidate; physical boundaries and relation coverage not implied; no execution of shift/at/window in consumer. Need: SLR-17,37,38, RC01,RC04,RC07. Evidence: native static shift; at/sum_back source. Relative integration effort: Medium/high. Alternative: explicit boundary values.

### S12 — cases (DEFER_PENDING_EVIDENCE)
Original/target mapping: Native disjoint regions; need prove applicability and absence semantics; not prioritized authoring branch. Need: SLR-18,19,36, RC01,RC03,RC07. Evidence: source only. Relative integration effort: Medium. Alternative: external guard and method rule.

### S13 — assumptions (KEEP_WITH_ADAPTER)
Original/target mapping: Native data requirement; trace predicate encoding only; not modal contract assumption/guarantee. Need: C5,SLR-18,19,24, RC01-RC09. Evidence: native static. Relative integration effort: Medium. Alternative: CSNF A/G.

### S14 — constraints (REPLACE_BY_EXISTING_CONTRACT_CONCEPT)
Original/target mapping: Native solver-facing constraints require variable involvement; contract obligation expressed without specifying solver decisions. Need: SLR-08,21,26; C5, RC01-RC07. Evidence: source; excluded executable subset. Relative integration effort: High if misused. Alternative: CSNF Assertion.

### S15 — variables / given:variables (EXCLUDE_FROM_SUBSET)
Original/target mapping: Decision variables not abstract observables; do not silently reinterpret. Need: SLR-21,26,29, RC01-RC07. Evidence: source and absence in native probes. Relative integration effort: Avoid solver coupling. Alternative: parameters+ObservableBinding.

### S16 — macros (DEFER_PENDING_EVIDENCE)
Original/target mapping: Closed native templates, no arbitrary Python; validate expansion/capture/version; not needed in executed fragment. Need: NFR-13; R10, RC08,RC09. Evidence: source only. Relative integration effort: Medium. Alternative: profile composition.

### S17 — fragments/given/merge/override/rename (KEEP_WITH_ADAPTER)
Original/target mapping: Native composition candidate; external source, trust, namespace, precedence and permitted override. Need: NFR-13; SLR-11,24,42; R10, RC08-RC10. Evidence: source only; no native composition proof. Relative integration effort: High governance. Alternative: CSNF composition.

### S18 — canonical serialization (KEEP_WITH_ADAPTER)
Original/target mapping: Canonical math YAML leaf via public API, versioned identity and retained source/audit; not E2-E5. Need: NFR-01,02,03,14,15,17; R00,R02,R04,R09, RC01-RC09. Evidence: native roundtrip. Relative integration effort: Medium. Alternative: CSNF mathematical normalization.

### S19 — objective / bounds / solver domain / dual (EXCLUDE_FROM_SUBSET)
Original/target mapping: Optimization objective, variable bounds, dual semantics not required to state external obligations. Need: SLR-21,26,39, RC06,RC08,RC10. Evidence: not adopted. Relative integration effort: Avoid solver coupling. Alternative: metric/selection policy.

### S20 — arbitrary extension / Python (EXCLUDE_FROM_SUBSET)
Original/target mapping: Closed native registry; no unregistered operator or raw AST extension. Need: NFR-04,16, all. Evidence: native rejected. Relative integration effort: Avoid unsafe semantics. Alternative: typed versioned extension only.

## Contract adapter invariants
The experiment uses native to_spec then canonical export/reimport and visits public typed nodes only; explicit closed node allowlist. The finite arithmetic consumer deliberately accepts no variables/objective and no private parser imports. Exact Fraction arithmetic on known complete numeric data, no implicit default or absent-as-zero, unknown/empty guard support blocks. Data type checks are evaluated on the admitted finite support, not a sound static physical type system for all expressions/guards. Integer literal restriction and exponent bound are experiment scope, not new normative limits. Native grammar supports more; excluded functionality is not evidence of impossibility. Every identifier mapping must be collision-free. Production design must preserve original qualified identifiers, rational literal precision, ordered binders, original source bytes, and parse errors with source locations. Unused expressions and all guard roots require static checking before any data-dependent evaluation.
