# SPDX-License-Identifier: MIT
# One immutable M0 input network per (horizon,weather_id). The composer owns all PyPSA writes.
# Snakemake 9.13.3; include MA2 and MA3 rules in Snakefile.iosn_m1_ma4f.
COMPOSE = config["iosn_m1_compose"]
COMPOSE_RES = config["iosn_m1_res"]
COMPOSE_HYDRO = config["iosn_m1_hydro"]


rule iosn_m1_compose:
    input:
        master=COMPOSE["master_manifest"],
        bridge=COMPOSE["identity_bridge"],
        network=COMPOSE["m0_network"],
        sidecar=COMPOSE["m0_sidecar"],
        m0manifest=COMPOSE["m0_reference_manifest"],
        resmanifest=COMPOSE_RES["weather_manifest"],
        rescatalog=COMPOSE_RES["source_catalog"],
        hydromanifest=COMPOSE_HYDRO["manifest"],
        hydroassets=COMPOSE_HYDRO["assets"],
        hydroalloc=COMPOSE_HYDRO["allocations"],
        rescf=COMPOSE_RES["output_dir"] + "/{horizon}/{weather_id}/renewable_cf.nc",
        resqa=COMPOSE_RES["output_dir"] + "/{horizon}/{weather_id}/qa.json",
        hydro="results/iosn_m1/hydro/{horizon}/{weather_id}",
    output:
        network=COMPOSE["output_dir"] + "/{horizon}/{weather_id}/detailed_reference_{horizon}_{weather_id}.nc",
        qa=COMPOSE["output_dir"] + "/{horizon}/{weather_id}/qa.json",
    threads: 1
    resources:
        mem_mb=2500
    shell:
        r"""
        python -m scripts.iosn_m1.compose \
          --m0-network {input.network:q} --m0-sidecar {input.sidecar:q} \
          --m0-reference-manifest {input.m0manifest:q} \
          --bridge-path {input.bridge:q} --master-path {input.master:q} \
          --res-manifest-path {input.resmanifest:q} --res-catalog {input.rescatalog:q} \
          --hydro-manifest-path {input.hydromanifest:q} \
          --hydro-assets {input.hydroassets:q} --hydro-allocations {input.hydroalloc:q} \
          --res-cf {input.rescf:q} --res-qa {input.resqa:q} \
          --hydro-dir {input.hydro:q} --hydro-qa {input.hydro:q}/qa.json \
          --horizon {wildcards.horizon:q} --weather-id {wildcards.weather_id:q} \
          --output-network {output.network:q} --output-qa {output.qa:q}
        """
