# Numeric boundary

Only source integer tokens 0..2^53−1, no decimal, exponent notation or implicit numeric defaults, then native Constant is verified. Rationals via integer division or exact external Fraction binding. Explicit nonzero literal or declared and checked nonzero divisor; positive constant integer power 1..8. Unknown, missing and nonfinite rejected, not coerced. No approximate tolerances in this scope. Native normalization can change tree structure; tests must show roundtrip safety, not general equivalence. Domain proof beyond finite binding is deferred.
