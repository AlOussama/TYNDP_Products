# SPDX-License-Identifier: MIT
"""Run MA3 on an externally supplied five-weather source catalog."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .adapter import execute, read_snapshots, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--allocations", type=Path, required=True)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--snapshots", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--planning-horizon", required=True)
    parser.add_argument("--weather-id", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--m0-network", default=None)
    parser.add_argument("--m0-sidecar", default=None)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = execute(
        manifest,
        pd.read_csv(args.allocations, keep_default_na=False, dtype=str),
        pd.read_csv(args.assets, keep_default_na=False, dtype=str),
        read_snapshots(args.snapshots),
        args.source_root,
        str(args.planning_horizon),
        args.weather_id,
        network_path=args.m0_network,
        sidecar_path=args.m0_sidecar,
    )
    write_outputs(result, args.output_dir)
    print(json.dumps(result["qa"], sort_keys=True))


if __name__ == "__main__":
    main()
