# SPDX-License-Identifier: MIT
# Include from the project Snakefile: include: "rules/iosn_m1_res.smk"
# Do not use the Open-TYNDP TYNDP_NODE busmap or compose_network rule.
import csv
import json
from pathlib import Path

RES = config["iosn_m1_res"]
RES_MANIFEST = json.loads(Path(RES["weather_manifest"]).read_text(encoding="utf-8"))
RES_WEATHER = RES_MANIFEST["selected_weather_ids"]
RES_HORIZONS = [str(h) for h in RES_MANIFEST["planning_horizons"]]
if len(RES_WEATHER) != 5 or len(set(RES_WEATHER)) != 5 or not RES_HORIZONS:
    raise ValueError("MA2 requires exactly five externally selected weather IDs and explicit horizons")


def res_source_files(wc):
    # Actual raw input dependencies, not only the source CSV catalog.
    catalog = Path(RES["source_catalog"])
    with catalog.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    files = [catalog.parent / row["file_path"] for row in rows
             if row["planning_horizon"] == wc.horizon and row["weather_id"] == wc.weather_id]
    if not files:
        raise ValueError(f"No PECD inputs catalogued for {wc.horizon}/{wc.weather_id}")
    return sorted(set(map(str, files)))


rule iosn_m1_res_all:
    input:
        expand(RES["output_dir"] + "/{horizon}/{weather_id}/renewable_cf.nc",
               horizon=RES_HORIZONS, weather_id=RES_WEATHER),
        expand(RES["output_dir"] + "/{horizon}/{weather_id}/qa.json",
               horizon=RES_HORIZONS, weather_id=RES_WEATHER),


rule iosn_m1_res_compile:
    input:
        weather=RES["weather_manifest"],
        catalog=RES["source_catalog"],
        asset=lambda wc: RES["m0_res_registry"].format(horizon=wc.horizon),
        m0=lambda wc: RES["m0_reference_manifest"].format(horizon=wc.horizon),
        crosswalk=RES["technology_crosswalk"],
        assignments=RES["asset_profile_map"],
        raw=res_source_files,
    output:
        cf=RES["output_dir"] + "/{horizon}/{weather_id}/renewable_cf.nc",
        sources=RES["output_dir"] + "/{horizon}/{weather_id}/source_ledger.csv",
        mapping=RES["output_dir"] + "/{horizon}/{weather_id}/assignment_ledger.csv",
        profiles=RES["output_dir"] + "/{horizon}/{weather_id}/profile_catalog.csv",
        qa=RES["output_dir"] + "/{horizon}/{weather_id}/qa.json",
    params:
        geometry=("--geometry-registry " + RES["geometry_registry"] if RES.get("geometry_registry") else ""),
    threads: 1
    resources:
        mem_mb=2500
    shell:
        """
        python -m scripts.iosn_m1.res.run \
          --weather-manifest {input.weather:q} \
          --source-catalog {input.catalog:q} \
          --m0-assets {input.asset:q} \
          --m0-reference-manifest {input.m0:q} \
          --technology-crosswalk {input.crosswalk:q} \
          --assignment-map {input.assignments:q} \
          {params.geometry} \
          --horizon {wildcards.horizon:q} --weather-id {wildcards.weather_id:q} \
          --output-cf {output.cf:q} \
          --output-source-ledger {output.sources:q} \
          --output-assignment-ledger {output.mapping:q} \
          --output-profile-catalog {output.profiles:q} \
          --output-qa {output.qa:q}
        """
