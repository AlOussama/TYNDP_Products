# Frozen bridge versions

Source: `C20-research-0.1|CSNF-R0|energy-r0`.
Target: `CSNF-C21-0.1|CSNF-R0|energy-c21-0.1`.
Adapter: `ML-C24-P1-bridge-r0.1`.

Explicit schema migration is an **experiment**, not evidence of semantically identical source/target operator registries. Every unknown version hard-fails. No owner status inference. Full migration approval and registry equivalence: NOT_PROVED. Port externality is materialized as `external=true`. Predicate and projector ASTs are preserved as typed, deeply copied structures; C21 ignores them unless additional checks are run first.
