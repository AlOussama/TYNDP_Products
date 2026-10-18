# TYNDP Products — IoSN / PyPSA Research

Research artifacts for ENTSO-E TYNDP 2026 Identification of System Needs (IoSN) network reduction, PyPSA implementations, technology-specific PTDF, merit-order GSKs, N-1/LODF security and flow-based market coupling.

## Scientific scope

- **Method A:** full-dispatch overload-energy clustering (IoSN-near).
- **Method B:** RES-and-load structural line-loading clustering (research extension).
- Exact spatial aggregation: `p_z = P p_d`, `f_z = Gamma f_d`, `A_z Gamma = P A_d`.
- Technology-specific zonal PTDF: `H_z^(k) = Gamma H_d R_k`.
- Equivalent reactance, structural zero-balance flow offsets, and N-1 transfer-capacity estimation.
- Woodbury/dual-LODF analyses and FBMC CNEC/GSK/RAM connections.

## Artifact-import status

**Important:** This initial repository commit only establishes the project index. The previously generated binary reports, code archives and test artifacts **have not yet been uploaded to GitHub**. They are available in the conversation's attached download package and require a filesystem-enabled Git upload.

A reproducibility claim must distinguish synthetic unit tests from an unperformed real-network PyPSA integration test.

## Planned structure

```text
docs/
  methodology/
  implementation/
  archive/
src/
tests/
examples/
results/
artifacts/
provenance/
```

The latest authoritative reports for the current analysis are titled:
- `IOSN_2026_Band_I_Wissenschaftliche_Methodik` (PDF/DOCX/Markdown)
- `IOSN_2026_Band_II_PyPSA_Implementierung` (PDF/DOCX/Markdown)
- `IOSN_TYNDP2026_Wissenschaftlicher_Gesamtbericht_revidiert.pdf`

The complete chat-generated collection must be imported without silently relabelling synthetic results as ENTSO-E evidence.
