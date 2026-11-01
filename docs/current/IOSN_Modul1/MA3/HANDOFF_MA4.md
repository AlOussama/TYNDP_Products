# M1-MA3 → MA4 — Integration Handoff and gate limitations

**Producer branch:** impl/iosn-m1-ma3-hydro-20261101. **Contract:** IOSN-M1-MA3/1.0.0. **Status:** IMPLEMENTED_FIXTURE_ONLY; REAL-DATA BLOCKED.

MA4 shall not start real Hydro integration until MA1C G1-C/E are evidenced: actual M0 DetailedNetworkReference plus sidecar and identity/capability ledger; five externally selected weather IDs; real regional/day/week Hydro file bytes and checksums, original interval boundaries, hydro basin/TSO shares and approved storage ports. The published MA1C report at commit f366f8162e1023ff959721d5fed14ad80dcba890 explicitly classifies the source gate as M1_SOURCE_CONTRACT_BLOCKED.

## Interface checklist for integration owner

1. Review final MA3 producer SHA, input schemas and SOURCE_REUSE_AND_LIMITATIONS. Cross-check against the actual M0 owner export version: CAN/2.0.0 canonical_revision_id and projection_id must be reconciled with MA1 network_revision_id, without silent field coercion.
2. Run the source SHA and selected exact WS-column checks, verify all **five** external weather datasets and every required Hydro region/tech pairing; do not reuse the three conventional TYNDP weather columns as five.
3. Verify per native source interval: source_energy_mwh == allocated_native_mwh, and per source×existing asset interval: model_energy_mwh == integrated_model_mwh (after separately evidenced conversion). Enforce complete UTC hour coverage, explicit temporal uniformity policy, real native bounds (especially 53rd/partial weeks), no missing/zero fallbacks.
4. Join hydro_inflow.csv **only** to existing StorageUnit.inflow, ror_availability.csv **only if evidenced** to existing Generator.p_max_pu. Check no pre-existing dynamic profile overwrites, unchanged Generator.p_nom/bus, source ID ledger and capacity/semantic validity. Do not infer dispatch from RoR availability.
5. store_link_staged.csv is **not an automatic allowed dynamic attribute**. Obtain M0 owner approval for the pre-existing auxiliary Generator on the Store energy bus, the discharging/charging Link topology and efficiency convention, power capacity and generators_t.p_set policy. Verify time-series conflicts before applying any staged port.
6. HCL with documented NO_NATURAL_INFLOW_BY_DESIGN is a classified absence, **not** 0 MW of invented natural water. Carry closed_loop_policy_ledger separately into the integration ledger.
7. MA4 is responsible for complete static original-network fingerprints before/after, PyPSA NetCDF roundtrip, full five-horizon/weather output acceptance, actual load/PF eligibility and independent review. MA3 never writes or imports the final composited network.

**No MA4/M2 release:** M1_HYDRO_REAL_DATA_QUALIFIED is blocked while these real input gates are missing. MA2 and MA3 must remain isolated; no worker-cherry-pick/merge prior to integration-owner review. This is a single consolidated missing-source gate, not a request for repeated micro-iterations.
