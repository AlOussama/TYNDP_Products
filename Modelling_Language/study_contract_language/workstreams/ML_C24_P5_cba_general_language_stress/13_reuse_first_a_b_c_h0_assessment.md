# Reuse-first A/B/C/H0 architecture assessment – controlled CBA lens

| Candidate | Why plausible | Specific unproven risk | Current admissible vote |
|---|---|---|---|
| A stand-alone general CSNF core | C1–C9 graph + independent typed projections can express outer obligations in design | Candidate A parser, full quantifier/operator semantics and validators incomplete | DESIGN_PLAUSIBLE_NOT_VERIFIED |
| B SysML v2/KerML profile | Native system boundaries/part/port/requirement structure may represent C1–C5; metadata for C6–C9 | No native profile run, no quantified retained authority/evidence or end-to-end cost comparison | H0_UNRESOLVED |
| C federated CSNF | May retain local CBA/solver/spec formats and use shared semantic/audit comparison | No native import/export, paired project scope or audit roundtrip measured | NOT_VALIDATED |
| H0 small existing standard profile suffices | Potentially avoids new language/parser | No executable proof of complete generic CBA operators/profile, version-safe roundtrip and authoring effort | UNRESOLVED |

Reuse candidates (from pinned source inspection, **not native execution**): [mathspec canonicalisation](https://github.com/energy-models/mathspec/tree/5f1464c334c1012cdee2947d4d55b4d1d6bef40a) for expression parsing, selective rewrite and stable textual canonicalisation; [GEMS](https://github.com/AntaresSimulatorTeam/GEMS/tree/c463e30b610443c1f59b20074bb7acffa2844cce) for component/port/connection relations; [SysML v2/KerML](https://www.omg.org/spec/SysML/2.0) for typed system/requirement structures. A GEMS connection is not necessarily a behavioural contract; mathspec algebraic normalisation is not feasible-set equivalence; a SysML requirements link is not CBA evidence.

A CBA-specific syntax or an obligatory CBA equation is **not recommended** on current evidence. The reuse-first experimental sequence should be: demonstrate typed profile in extant language -> measure semantic/audit loss -> measure additional operator count -> only then compare new-core costs. Without B1/B2 comparative evidence there is no ranked winner.
