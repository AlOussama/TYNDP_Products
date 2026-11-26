# Restricted candidate

See validated_mathspec_subset.yaml for all 20 families and native source evidence from MS1. This implementation only admits the nine bounded arithmetic nodes plus dense domain declarations and external typed comparisons. Native conditions, relations, cases, temporal operators, macros, fragment merge and solver constructs are not admitted. This sacrifices expressiveness to prevent unvalidated branches; reference-driven extension required in C2, not a global-minimality claim.
