"""Deterministic *synthetic* MA1 acceptance fixture, never real qualified."""
from __future__ import annotations
import argparse
import json
from hashlib import sha256
import numpy as np
from .contracts import ACBranch, HVDCTerminals, DetailedGridSnapshot, ReferenceDispatchSet, TimeSet, NormalContingencyRatings, Provenance
from .country import CountryZoneBudget
from .ma1 import execute_ma1


def synthetic_source(name):
    return Provenance("synthetic-ma1-" + name, "synthetic://m2-ma1/" + name,
                      "fixture-v1", sha256(("ma1-v1:" + name).encode()).hexdigest(),
                      synthetic=True)


def build_synthetic_fixture():
    """Two AC islands, HVDC bridge, cross-country AC mesh and operational PST."""
    branches = (
        ACBranch("d01", "d0", "d1", .1, 225),
        ACBranch("d12", "d1", "d2", .1, 400),
        ACBranch("d20", "d2", "d0", .1, 110),
        ACBranch("cross_de_fr_1", "d1", "f0", .2, 400),
        ACBranch("fr01", "f0", "f1", .1, 225),
        ACBranch("cross_fr_de_2", "f1", "d0", .2, 400),
        ACBranch("pst_de", "d0", "d2", .2, 400, "pst"),
        ACBranch("ni_trafo", "n0", "n1", .1, 225, "transformer"),
    )
    grid = DetailedGridSnapshot(
        ("d0", "d1", "d2", "f0", "f1", "n0", "n1"),
        ("DE", "DE", "DE", "FR", "FR", "NI", "NI"),
        branches, (HVDCTerminals("hvdc_de_ni", "d2", "n0"),), 100.,
        synthetic_source("grid"),
    )
    snapshots = tuple(f"202{i}-01-01T00:00:00Z" for i in range(5))
    years = tuple(f"MOCK-Y{i+1}" for i in range(5))
    time = TimeSet(snapshots, years, years, np.array([1., 2., 3., 1., 1.]),
                   ("winter", "summer", "winter", "summer", "winter"),
                   synthetic_source("time"))
    p = np.array([20., -12., -4., -1., -1., -1., -1.])
    dispatch = ReferenceDispatchSet(
        grid.bus_ids, time.snapshot_ids, np.tile(p[:, None], (1, 5)),
        {"hvdc_de_ni": np.full(5, 2.)},
        {"pst_de": np.array([0., .01, 0., .01, 0.])},
        synthetic_source("dispatch"))
    ratings = NormalContingencyRatings(
        snapshots,
        {b.identifier: np.full(5, 12.) for b in branches},
        {b.identifier: np.full(5, 18.) for b in branches},
        synthetic_source("ratings"))
    budget = CountryZoneBudget.synthetic(
        {"Germany": 2, "France": 1, "Northern Ireland": 1})
    explicit_map = {"DE": "Germany", "FR": "France", "NI": "Northern Ireland"}
    weights = {year: 1. for year in years}
    return grid, dispatch, time, ratings, budget, explicit_map, weights


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--output", required=True)
    cli.add_argument("--commit", required=True)
    opts = cli.parse_args(argv)
    if not opts.commit.strip():
        cli.error("Missing code commit SHA")
    result = execute_ma1(*build_synthetic_fixture(), protected_line_ids=("d12",))
    if result.preflight.status != "PASS" or len(result.preflight.ac_islands) != 2:
        raise SystemExit("BLOCKED: synthetic physical contract")
    manifest = result.export(opts.output, code_commit=opts.commit)
    print(json.dumps({
        "status": manifest["status"],
        "input_manifest_sha256": result.input_manifest_sha256,
        "preflight_status": result.preflight.status,
        "country_quota_counts": result.seed.quota_counts,
        "ac_island_count": len(result.preflight.ac_islands),
        "snapshot_count": len(result.reference.snapshot_ids),
        "artifacts_hashed": len(manifest["output_sha256"]),
        "real_network_qualified": False,
        "independent_reviewer_release": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
