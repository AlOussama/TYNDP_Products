# SPDX-License-Identifier: MIT
# Optional isolated subworkflow: include from the M1 orchestration Snakefile.
# Mandatory external config. No replacement weather scenarios, regions or M0 assets.
import json
from pathlib import Path

hydro_cfg = config["iosn_m1_hydro"]


def hydro_source_inputs(wildcards):
    manifest = json.loads(Path(hydro_cfg["manifest"]).read_text(encoding="utf-8"))
    source_root = Path(hydro_cfg["source_root"])
    # Materialize EVERY one of the five selected weather files as tracked inputs.
    return [str(source_root / source["path"])
            for source in manifest["sources"]
            if str(source["planning_horizon"]) == str(wildcards.horizon)]


rule iosn_m1_hydro:
    input:
        manifest=hydro_cfg["manifest"],
        allocations=hydro_cfg["allocations"],
        assets=hydro_cfg["assets"],
        snapshots=lambda wc: hydro_cfg["snapshots"][str(wc.horizon)][wc.weather_id],
        source_files=hydro_source_inputs,
    output:
        directory("results/iosn_m1/hydro/{horizon}/{weather_id}")
    params:
        root=hydro_cfg["source_root"],
        extra=hydro_cfg.get("m0_network_flags", ""),
    log:
        "logs/iosn_m1/hydro_{horizon}_{weather_id}.log"
    shell:
        r"""
        python -m scripts.iosn_m1.hydro.cli \
          --manifest {input.manifest:q} \
          --allocations {input.allocations:q} \
          --assets {input.assets:q} \
          --snapshots {input.snapshots:q} \
          --source-root {params.root:q} \
          --planning-horizon {wildcards.horizon:q} \
          --weather-id {wildcards.weather_id:q} \
          --output-dir {output:q} {params.extra} \
          > {log:q} 2>&1
        """
