"""One-shot M2-MA1 pipeline: physical reference, screen and country-pure seed.

The pipeline consumes an already assembled reference grid and five externally
chosen weather years. It neither reads CGMES/PECD nor chooses weather years.
The only numerical dispatch is a GLOBAL AC graph solve with explicit islands.
MA2's x/c0 fit and iterative re-clustering are OUT OF SCOPE.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import csv
import json
import numpy as np
from scipy.sparse import save_npz

from .contracts import (
    DetailedGridSnapshot, ReferenceDispatchSet, TimeSet,
    NormalContingencyRatings, ReferenceFlowCache, digest_object,
)
from .country import CountryZoneBudget, resolve_country_ids
from .preflight import preflight, PreflightLedger
from .physical import reference_flows
from .screen import screen_annual_overload, weighted_edge_costs, AnnualScreen
from .seed import quota_seed, SeedResult
from .operators import build_oriented_projection, OrientedProjection


@dataclass(frozen=True)
class MA1Result:
    preflight: PreflightLedger
    reference: ReferenceFlowCache
    screen: AnnualScreen
    seed: SeedResult
    projection: OrientedProjection
    resolved_country_of_bus: tuple[str, ...]
    input_manifest_sha256: str
    gate_statuses: dict[str, str]

    def export(self, output_directory: str | Path, *, code_commit: str) -> dict:
        """Atomically named, non-overwritten evidence directory for MA2.

        A brand-new directory is required to prevent accidental replacement
        of an existing reference or a previous independent test result.
        """
        directory = Path(output_directory)
        directory.mkdir(parents=True, exist_ok=False)
        outputs: list[str] = []

        def write_json(filename: str, obj):
            (directory / filename).write_text(
                json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)
                + "\n", encoding="utf-8")
            outputs.append(filename)

        def write_csv(filename: str, header, rows):
            with (directory / filename).open("w", newline="", encoding="utf-8") as stream:
                out = csv.writer(stream, lineterminator="\n")
                out.writerow(header)
                out.writerows(rows)
            outputs.append(filename)

        write_json("preflight_ledger.json", self.preflight.to_dict())
        write_json("gate_ledger.json", self.gate_statuses)
        write_json("merge_ledger.json", list(self.seed.merge_ledger))
        write_json("counterflow_ledger.json",
                   list(self.projection.counterflow_ledger(self.reference)))
        write_json("reference_flow_manifest.json", self.reference.to_manifest())
        write_csv("country_quotas.csv", ("country_label", "zone_count"),
                  sorted(self.seed.quota_counts.items()))
        write_csv("busmap.csv", ("bus_id", "country_label", "zone_id"),
                  zip(self.reference.bus_ids, self.resolved_country_of_bus,
                      self.seed.zone_of_bus))
        write_csv(
            "annual_criticality.csv",
            ("year_id", "line_id", "voltage_kv", "overload_MWh",
             "overload_hours", "observation_hours"),
            ([row[k] for k in
              ("year_id", "line_id", "voltage_kv", "overload_MWh",
               "overload_hours", "observation_hours")]
             for row in self.screen.rows),
        )
        write_csv("zone_cuts.csv", ("zone0", "zone1"), self.projection.cut_pairs)
        np.savez_compressed(
            directory / "global_reference_flows.npz",
            branch_ids=np.array(self.reference.branch_ids, dtype=str),
            bus_ids=np.array(self.reference.bus_ids, dtype=str),
            snapshot_ids=np.array(self.reference.snapshot_ids, dtype=str),
            flow_mw=self.reference.flow_mw,
            nodal_net_mw=self.reference.nodal_net_mw,
            island_of_bus=np.array(self.reference.island_of_bus, dtype=int),
        )
        outputs.append("global_reference_flows.npz")
        for name, matrix in (
            ("P", self.projection.P),
            ("Gamma", self.projection.Gamma),
            ("A_z", self.projection.A_z),
            ("A_d", self.projection.A_d),
        ):
            save_npz(directory / f"operator_{name}.npz", matrix)
            outputs.append(f"operator_{name}.npz")

        hashes = {
            filename: sha256((directory / filename).read_bytes()).hexdigest()
            for filename in sorted(outputs)
        }
        grid_is_synthetic = self.preflight.source_provenance["grid"]["synthetic"]
        manifest = {
            "status": ("MA1_SYNTHETIC_CONTRACT_PASS_ONLY" if grid_is_synthetic else
                       "MA1_CONTRACT_PASS_NOT_REAL_QUALIFIED"),
            "code_commit": code_commit,
            "input_manifest_sha256": self.input_manifest_sha256,
            "reference_input_sha256": self.reference.input_sha256,
            "output_sha256": hashes,
            "real_network_qualified": False,
            "independent_reviewer_release": False,
            "calibration_equivalent_x_c0": "NOT_IN_MA1",
            "source_versions": self.preflight.source_provenance,
            "units": {"flow": "MW", "energy": "MWh", "phase": "rad",
                      "reactance": "p.u. on grid.base_mva"},
        }
        write_json("manifest.json", manifest)
        return manifest


def execute_ma1(
    grid: DetailedGridSnapshot,
    dispatch: ReferenceDispatchSet,
    time: TimeSet,
    ratings: NormalContingencyRatings,
    budget: CountryZoneBudget,
    explicit_country_map: dict[str, str],
    explicit_year_weights: dict[str, float],
    *,
    protected_line_ids=(),
) -> MA1Result:
    ledger = preflight(
        grid, dispatch, time, ratings,
        country_label_map=explicit_country_map,
    )
    ledger.require_pass()
    labels = resolve_country_ids(grid, explicit_country_map, budget)
    reference = reference_flows(
        grid, dispatch, time, neutral_calibration=False,
    )
    annual = screen_annual_overload(grid, reference, time, ratings)
    edge_costs = weighted_edge_costs(annual, grid, explicit_year_weights)
    seed = quota_seed(
        grid, labels, budget, merge_cost_by_branch=edge_costs,
        protected_line_ids=protected_line_ids,
    )
    projection = build_oriented_projection(grid, seed.zone_of_bus)
    projection.verify(reference)
    pz, fcut = projection.aggregate(reference)
    if not np.allclose(projection.A_z @ fcut, pz, atol=1e-7):
        raise AssertionError("G05 zonal Kirchhoff invariant failed")

    # Hash actual rating arrays as well as declared provenance: a stale upstream
    # source hash must not make two different limit sets share a run identity.
    rating_digest = sha256(b"MA1:normal-and-contingency-MW:v1")
    for branch_id in sorted(ratings.normal_mw):
        for label, table in (("normal", ratings.normal_mw),
                             ("contingency", ratings.contingency_mw)):
            rating_digest.update(label.encode("utf-8"))
            rating_digest.update(branch_id.encode("utf-8"))
            rating_digest.update(table[branch_id].tobytes())
    fingerprint = digest_object({
        "grid_sha256": ledger.grid_sha256,
        "ratings_content_sha256": rating_digest.hexdigest(),
        "reference_input_sha256": reference.input_sha256,
        "rating_source_sha256": ratings.provenance.source_sha256,
        "quota_source_sha256": budget.source_sha256,
        "country_labels": list(labels),
        "year_weights": explicit_year_weights,
        "protected_line_ids": sorted(protected_line_ids),
        "screened_line_ids": annual.screened_line_ids,
        "zone_of_bus": seed.zone_of_bus,
    })
    gates = {
        "G01_provenance_time_balance": "PASS_CONTRACT",
        "G02_country_budget_exact": ("PASS_SYNTHETIC_FIXTURE" if not budget.official
                                      else "PASS_CONTRACT"),
        "G03_ac_connected_and_hvdc": "PASS",
        "G04_225_400_annual_mwh": "PASS",
        "G05_oriented_aggregation_and_kcl": "PASS",
        "G11_part_devices": "PASS_LOSSLESS_DC_EQUIVALENT_ONLY",
        "real_input_and_independent_review": "BLOCKED_DATA_AND_REVIEW",
    }
    return MA1Result(ledger, reference, annual, seed, projection, labels,
                     fingerprint, gates)
