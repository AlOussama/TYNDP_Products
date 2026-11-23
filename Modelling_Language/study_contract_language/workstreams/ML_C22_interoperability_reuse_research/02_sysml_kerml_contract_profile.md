# ML-C22/02 – Minimal SysML 2.0 / KerML 1.0 external Contract Profile (design)
ML-C22 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
CSNF base 2f0297b754e3a96a2523a34d3af98782b26181f3; mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce. OMG SysML 2.0, KerML 1.0, Systems Modeling API 1.0; pilot 2026-09.1 is IMPLEMENTATION, not normative. G1 BLOCKED.

## Native building blocks (standard)
- KerML Type, Feature, Membership/Relationships, Namespace, Multiplicity for stable identity and reference structure. Owner/vendor metadata is **not intrinsically equivalent** to C9 Authority: profile meaning must be defined.
- SysML PartDefinition/Usage and PortDefinition/Usage for component types/instances and external interface points; Connection/Interface definitions and usages for physical connection *topology*, but not every graph edge is a Kirchhoff constraint.
- RequirementDefinition/Usage with assumedConstraint/requiredConstraint and corresponding ConstraintDefinition/Usage for scoped A/G; an environmental data assumption is not automatically an external guarantee.
- VerificationCase / RequirementVerificationMembership for verification intent/linkage. Verified link is NOT executed positive evidence.
- Quantity/Units libraries and typed Features where applicable; energy conversion, H2 mass/HHV/LHV, signed injections and time information sets need *explicit controlled profile semantics*.

## Minimal CSNF extensions (all profiled/metadata, not alleged SysML built-ins)
`StudyFrame`: question/boundary/time/scenario/counterfactual + schema/registry pins. `EnergyPortProfile`: carrier, physical_kind, dimension, unit, basis, sign, direction, time support and connection_point. `ContractObligation`: modality REQUIRED/PROHIBITED/PERMITTED/IMPLEMENTATION_DEFINED, decision OWNER_TBD etc, scope/guard and source IDs. `ServiceGuarantee`: quantifier ordering and admissible demands. `ObservableProfile`: KPI price/cost/aggregation/tolerance/selection. `VariationDeclaration`: internal formulation freedom/disclosure. `EvidenceProfile`: request/result discriminator, run/status and proof level. `AuthorityIdentity`: immutable source/owner/approval chain.

## Model-freedom invariant
A PartUsage representing a battery role is **not** required to contain SOC, battery energy variables, internal power balance constraints or a solver. Angle/flow/PTDF and different storage state parametrizations can map to the same outer Contract, subject to source-approved physical guarantees and evidence. Profile tags must be stable across interchange through API/XMI; assertion is untested without native roundtrip.

Standard references: https://www.omg.org/spec/SysML/2.0; https://www.omg.org/spec/KerML/1.0; https://www.omg.org/spec/SystemsModelingAPI/1.0. Pilot: https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation/releases/tag/2026-09.1. No profile is claimed standards-certified.
