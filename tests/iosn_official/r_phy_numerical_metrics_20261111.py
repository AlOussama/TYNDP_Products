"""Machine-readable numerical residuals for the independent R-PHY witness.

A separate dense KCL/cycle-space-KVL oracle is used only on ten buses.
Production reference uses the library's sparse factorisation.
"""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from tyndp_reduce.iosn_official.physical import ac_topology, reference_flows
from test_r_phy_independent_20261111 import independent_case, cycle_space_flow


def main():
    grid, dispatch, time, ratings = independent_case()
    a_sparse, b, island, n_islands = ac_topology(grid)
    solved = reference_flows(grid, dispatch, time)
    a = a_sparse.toarray()
    cycles = null_space(a)
    all_oracle_diffs = []
    all_kvl_residuals = []
    for t in range(len(time.snapshot_ids)):
        phase = np.array([
            dispatch.pst_phase_rad[branch.identifier][t] if branch.kind == "pst"
            else branch.phase_shift_rad for branch in grid.active_branches
        ], dtype=float)
        oracle = cycle_space_flow(grid, solved.nodal_net_mw[:, t], phase)
        all_oracle_diffs.append(np.max(np.abs(oracle - solved.flow_mw[:, t])))
        kvl = cycles.T @ (solved.flow_mw[:, t] / b + phase)
        all_kvl_residuals.append(float(np.max(np.abs(kvl))))
    balance = np.stack([
        np.sum(solved.nodal_net_mw[island == k, :], axis=0)
        for k in range(n_islands)
    ])
    out = {
        "case": "R-PHY-independent-10bus-3island-5cycle-2hvdc-2pst",
        "synthetic": True,
        "buses": len(grid.bus_ids),
        "active_ac_branches": len(grid.active_branches),
        "islands": int(n_islands),
        "independent_cycles": int(cycles.shape[1]),
        "hvdc_links": len(grid.hvdc),
        "pst_branches": sum(branch.kind == "pst" for branch in grid.active_branches),
        "snapshots": len(time.snapshot_ids),
        "reference_input_sha256": solved.input_sha256,
        "max_abs_kcl_residual_mw": float(np.max(np.abs(a @ solved.flow_mw - solved.nodal_net_mw))),
        "max_abs_island_balance_mw": float(np.max(np.abs(balance))),
        "max_abs_cycle_space_oracle_delta_mw": float(max(all_oracle_diffs)),
        "max_abs_cycle_kvl_residual_rad": float(max(all_kvl_residuals)),
        "real_network_qualified": False,
    }
    path = Path(sys.argv[1])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
