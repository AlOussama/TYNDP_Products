> **MA-01 LEGACY / HISTORICAL ONLY — NOT AN ACTIVE REQUIREMENTS CATALOGUE (2026-11-05).** This research artifact predates MA-01. Sole active provisional source-derived system requirements: [iosn_requirements_catalogue.csv](iosn_requirements_catalogue.csv), with [source baseline](methodology_source_baseline.md), [process specification](iosn_process_specification.md), [scope change impact](scope_and_change_impact.md). Weather-year selection/PCA/K-Means/reproduction is **EXTERNAL / OUT OF SCOPE**, only already-selected weather inputs and consistency checks are in scope. Any old MR/SR/UC/VC/LRC/test/architecture recommendation is superseded and **not normative**. Retained as non-normative historical research; no architectural/tool decision is made here.

---

# 06 — Interpretation protocol for Language Capability × IoSN Requirement Matrix

The accompanying CSV covers 17 [LRC] capabilities across 17 technologies or standard categories. This **is not a weighted ranking**, because categories have different native purposes.

|Code|Meaning|Proof standard|
|---|---|---|
|0|Not a feature of the candidate|Documented source claim; for final standard pin version and test with an IoSN instance|
|N|Native support in stated primary role|Documented source claim; for final standard pin version and test with an IoSN instance|
|E|Support through domain extension/profile|Documented source claim; for final standard pin version and test with an IoSN instance|
|C|Support with another standard|Documented source claim; for final standard pin version and test with an IoSN instance|
|P|Partial support / insufficient for full requirement|Documented source claim; for final standard pin version and test with an IoSN instance|
|?|Not evidenced|Documented source claim; for final standard pin version and test with an IoSN instance|

**Ratings are a qualitative desk assessment:** `N` only denotes that the relevant *general capability* is native, never that it contains ENTSO-E's IoSN-specific algorithm. `E` and `C` denote a plausible extension/composition, **not an implemented extension**. `P` means a capability exists but would fail to capture the entire LRC criterion. `0` means not designed for that aspect. `?` is lack of reliable evidence; it must not be silently counted as `0`.

Selected evidence-backed distinctions:
- LRC-07 mathematical obligation profiles: GEMS and mathspec **N** for algebra, SysML v2 **C**, CESM **P**, bare YAML/JSON **0**. Mathematical expression does not prove solver conformance.
- LRC-12 sequencing: BPMN/SysML v2 **N** for process representation, mathematical languages need external workflow.
- LRC-02 typed data: CESM/INES/SiennaSchemas/JSON Schema/LinkML **N**; bare serialization **0** because no validation semantics.
- LRC-10 test objects: native SysML v2 verification models **N**, JSON Schema/SHACL **N** for structure/graph shapes only. Neither proves that the implementing optimizer enforced equations.
- LRC-15 change trace: native ReqIF exchange, SysML v2 requirements relations; governance evidence still outside notation.

**To promote a cell from candidate assessment to verified capability:** provide standard version/tag, an IoSN fixture, exact schema or language expression, validator or importer command, acceptance results, limitations, and a test report. Missing such a fixture means no certification of the row.

## Added LRC columns 18–21
The revised CSV explicitly considers detailed hydro/demand resource class semantics, economic vintage and annualization, reference-grid + directional NTC candidate contracts, and offshore siting/economic policy. Codes `N/E/C/P/0` remain **unverified candidate capability classifications**, not actual tool acceptance. `N` for a network schema means it natively models network data, **not** that it natively models the ENTSO-E expansion method.
