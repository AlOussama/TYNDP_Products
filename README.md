# TYNDP Products — IoSN Network Reduction Research

Research prototype covering ENTSO-E TYNDP 2026 Identification of System Needs (IoSN), PyPSA spatial aggregation, technology-specific PTDF/GSK, merit-order references, N-1 security and flow-based market coupling.

## Tutorials and reproducible comparisons

Start with the **[step-by-step tutorial index](docs/TUTORIALS.md)** (German). It covers installing the package, running clustering A/B, PTDF-reference and F0 comparisons, N-1/LODF security, FBMC/GSK sensitivity, and optional real-network PyPSA preparation. A dedicated CLI creates ranked comparison tables from the synthetic demonstration's CSV.

## Start here

- [Scientific methodology, Band I](docs/current/IOSN_2026_Band_I_Wissenschaftliche_Methodik.md)
- [PyPSA implementation and validation, Band II](docs/current/IOSN_2026_Band_II_PyPSA_Implementierung.md)
- [Research audit and open gaps](docs/REPOSITORY_AUDIT.md)
- [Source package](src/tyndp_reduce/), [tests](tests/), [examples](examples/)
- [Synthetic results](results/synthetic/), [historic reports](docs/archive/), [historic artifacts](artifacts/)

## Core methodology

1. **Method A:** dispatch-based annual overload-energy clustering (close to published IoSN description).
2. **Method B:** RES/load-driven line-loading clustering (independent scientific extension).
3. Sparse node/line aggregation `p_z=P p_d`, `f_z=Gamma f_d` and `A_z Gamma=P A_d`.
4. Technology-specific PTDF `H_z^k=Gamma H_d R_k`, equal/capacity/merit-order reference distribution, structural no-load flows.
5. Equivalent reactance calibration, statistical IoSN-near N-1 proxy, analytical CNEC/PTDF/LODF projection and conservative security derating.
6. FBMC bridge for GSKs, CNEC and RAM analyses.

## Install and test

```bash
python -m pip install -e ".[test]"
pytest -q
python run_demo.py --output results/example_run
```

Install `.[pypsa]` for the optional real-network PyPSA adapter. **Integration against an actual TYNDP network is not verified.** The provided CSVs are synthetic test outputs, not ENTSO-E observations.

This repository retains previous publications/artifact versions as archival evidence; `docs/current/` and `src/` are the canonical entry points.
