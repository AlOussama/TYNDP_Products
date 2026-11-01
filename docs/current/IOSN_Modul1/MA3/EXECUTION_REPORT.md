# M1-MA3 — Hydro Source Inflows and Original-Asset Mapping: consolidated execution report

**Date:** 2026-11-01  
**Execution scope:** complete single macro covering upstream inspection, original adapter, fail-closed five-source contract, native interval conversion, hydrological allocation, storage-port semantics, Snakemake rule, synthetic positive/negative tests, mapping and energy ledgers, integration handoff.  
**Decision:** **IMPLEMENTED_FIXTURE_ONLY__REAL_SOURCE_BLOCKED**. Source and M0 Real-Data-PASS is explicitly **NOT GRANTED**.  
**Isolated producer branch:** impl/iosn-m1-ma3-hydro-20261101  
**Base commit (immutable):** 2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994  
**External implementation studied:** open-energy-transition/open-tyndp tyndp-2026 @ 71a3a9a15b77114cd79458bceabc98e1a64dd58a  
**Independent upstream source gate:** M1-MA1C @ f366f8162e1023ff959721d5fed14ad80dcba890 — M1_SOURCE_CONTRACT_BLOCKED  
**PR:** https://github.com/AlOussama/TYNDP_Products/pull/7 (draft, no merge authorization).

## 1. Execution and immutable authorities

- Verified the M1 instruction commit and fully consulted section 5 of IOSN_M1_NEXT_MACRO_ASSIGNMENTS_AND_HANDOFFS_2026_11_01.md, the MA1 consolidated spatial/source audit, logical data contract YAML and base architecture.
- Inspected upstream Open-TYNDP's clean_tyndp_hydro_inflows.py, build_tyndp_hydro_profile.py, data/tyndp_technology_map.csv and rules/sb.smk at the exact pinned upstream SHA; inspected M0 DetailedNetworkReference logical canonical contract at 0275f48231a0794bea324b9cab34700bb0de8f5b.
- Reconciled the simultaneously completed MA1C witness: all five externally selected weather identifiers, actual Hydro source bytes/period bounds, physical basin/TSO asset fractions and a tested M0 network/sidecar remain unavailable. The M0 CAN/2.0.0 revision/projection identity bridge also requires M0 owner coordination. The independent audit has not granted any real-data readiness.
- All written Python is original implementation rather than verbatim upstream code. Open-TYNDP's SPDX MIT script licenses were inspected; physical source-data licensing is not inferred from code licensing.

## 2. Code and deliverables (all under this isolated branch)

| Path | Output and role |
|---|---|
| scripts/iosn_m1/hydro/adapter.py | SHA-verified source file reader; five exact weather IDs; intervals and UTC checks; native-MWh allocation; original-asset mapping; constrained PyPSA port semantics; dual energy ledgers and machine-readable QA; network is never mutated |
| scripts/iosn_m1/hydro/normalize_tyndp2026.py | Strict selected WS### WEEK/DAY extraction only when original period-key-to-time bounds and two physical SHA256 values are evidenced; emits normalized native intervals/provenance |
| scripts/iosn_m1/hydro/cli.py | Standalone documented reproducible command for one horizon/weather ID, enforces REAL mode M0 inputs |
| rules/iosn_m1_hydro.smk | Independent opt-in Snakemake rule with full five-source input dependencies; no default TYNDP busmap or fallback |
| schemas/iosn_m1/hydro_allocation_schema.json | Versioned basin-asset/energy conversion/store-port fields and invariant descriptions |
| schemas/iosn_m1/hydro_source_manifest_schema.json | Versioned weather selection, source/interval bounds, timezone and temporal policy requirements |
| tests/iosn_m1/hydro_fixtures.py; tests/iosn_m1/test_hydro_*.py | Fully synthetic scenarios with physics/capacity/format/security negative checks, CLI and raw TYNDP-format smoke |
| docs/current/IOSN_Modul1/MA3/HYDRO_MAPPING_REAL_SOURCE_LEDGER.csv | All five empty external Weather slots explicitly NOT_PROVIDED for HRR/HRI/HPI/HOL/HCL, never fictitious asset IDs or MWh |
| docs/current/IOSN_Modul1/MA3/INTERVAL_ENERGY_REAL_LEDGER_TEMPLATE.csv | Real-source interval-energy output schema without fabricated source rows |
| docs/current/IOSN_Modul1/MA3/SOURCE_GATE_STATUS.json | Machine-readable gates, source-count and CI references |
| docs/current/IOSN_Modul1/MA3/INPUT_CONTRACT_AND_PHYSICS.md | Source-native energy and original-M0-component contracts, equations, CLI/ports and temporal evidence |
| docs/current/IOSN_Modul1/MA3/SOURCE_REUSE_AND_LIMITATIONS.md | Upstream source-by-source adoption/rejection, licensing and source limitations |
| docs/current/IOSN_Modul1/MA3/HANDOFF_MA4.md | Non-mutating MA4 integration interface and explicit real qualification prerequisites |

The runtime writes **hydro_inflow.csv** (existing StorageUnit, MW), **ror_availability.csv** (existing RoR Generator, per-unit availability, not dispatch), **store_link_staged.csv** (approved auxiliary input port only, not automatically written to PyPSA), **interval_energy_ledger.csv**, **hydro_allocation_ledger.csv**, **closed_loop_policy_ledger.csv** and **qa.json**.

## 3. Physical energy contract and test evidence

For each original, actually proven source interval k = [t0,t1), elapsed h_k hours, the source input is E_zk MWh. All hydrologically evidenced asset fractions B_az must sum to one per hydro area and technology. We first check that the sum of the allocated *native* source MWh equals E_zk. Only after this source-conservation step does a documented hydraulic-to-model conversion c_az produce model-input energy E_azk = c_az B_az E_zk. An explicitly authorized uniform interval allocation yields P_azk = E_azk / h_k; the independently audited sum of P_azk times actual hourly duration must equal E_azk. Source-native and converted/electrical energy are two separately audited quantities. Hourly uniform power is **not** claimed to be observed hourly generation or measured river inflow.

**Deterministic synthetic examples exercised in GitHub Actions (not genuine PECD data):**

| Positive physics fixture | Inputs | Expected and tested behavior |
|---|---|---|
| Basin → 2 original StorageUnits | 96 MWh over 48 h; 60%/40% shares | Native MWh 57.6 + 38.4 = 96, hourly modeled MW 1.2 and 0.8; unchanged electrical bus IDs |
| Leap-year 53 native calendar intervals | Jan 1 2024 through Jan 1 2025; 52 seven-day periods and a 48h last period; 2 MW energy-equivalent | 53 genuine intervals, 8784 hourly intervals, total 17,568 MWh, last period 48h rather than 168h |
| DST spring Europe/Berlin | Native civil day with 23 elapsed UTC hours and 46 MWh | 2 MW for exactly 23 UTC hours; total 46 MWh |
| DST autumn Europe/Berlin | Native civil day with 25 elapsed UTC hours and 50 MWh | 2 MW for exactly 25 UTC hours; total 50 MWh |
| HRR / HPI / HOL / HCL | RoR Generator energy availability, pondage StorageUnit, open-loop natural PHS, closed-loop physical no-natural-inflow declaration | Correct port/capacity/capability matrix; HCL explicit NOT_APPLICABLE, **no fabricated zero-valued series** |
| Store + Link with M0-authorized auxiliary port | Pre-existing Store and auxiliary Generator on same energy bus, explicit additional attribute approval | Stage non-default generators_t.p_set input only; no network components constructed |
| Genuine zero in synthetic native file | Explicit 0 MWh in a byte-hashed source | Preserve and trace the actual zero; distinguish it from missing/unknown file |

**Negative tests** reject missing fifth weather source, duplicate weather IDs, wrong SHA, nonexistent source file, invalid region shares or asset IDs, electrical-bus-only basin matching, missing hydrological/temporal provenance, source conversion gains, capacity overflow, invalid StorageUnit discharge efficiency, missing Store/Link approval, generation-code masquerading as inflow, HCL as generic natural inflow, missing native hour, invalid timezone/DST offset, unsupported raw WS source column and unverified interval-bound hashes.

**CI witness:** Python 3.11 / pandas 3.1.0, pytest including the existing project suite plus MA3 positive/negative/CLI tests. At commit 81d5bd29021beeb00caa5bd7f7c08189d9cc1c11 GitHub Actions run 41311626884 returned **PASS — 60 tests**, and existing project demo step succeeded. Two additional temporal/generation negative tests were committed after that run; final status below must be read from the final branch CI job rather than assuming them to have passed.

**Not executed:** a real Snakemake hydro pipeline, a real M0 PyPSA network/NetCDF roundtrip, actual five physical Hydro input campaigns, real basin-to-plant coverage, real plant efficiency/Store-Link operational validation, storage dispatch or AC power flow. This restriction is deliberate and cannot be replaced by synthetic tests.

## 4. Hydro technology and output semantics

- HRR: original RoR Generator may receive an **approved availability signal** via generators_t.p_max_pu (only from technically qualified source available-energy semantics; never imply dispatch), or an existing genuine energy-state unit when modeled that way.
- HRI/HPI: distinct reservoir/pondage class; genuine natural inflow mapped to an already existing StorageUnit state-of-charge inflow, not generated MWh.
- HOL: natural inflow to an **open-loop** pumped storage energy state, separately from pumping energy and link efficiency.
- HCL: existing **closed-loop** pumped storage treated as NO_NATURAL_INFLOW_BY_DESIGN only with independent technology evidence; absence is recorded as a classification, not as a 0 MWh source file.
- HRO/HPO/HRG: generation-energy output codes do not qualify as generic inflow to StorageUnit.
- Store/Link: existing Store has no native inflow attribute; additional approved pre-existing injection Generator port with generators_t.p_set is staged only and requires MA4/M0 original topology and additional allowlist approval.
- Source basin/TSO association uses approved hydrological allocation, never electrical bus coordinates or TYNDP bus identifiers to infer basin membership.

## 5. Acceptance matrix and blockers

| Gate | Result | Authority |
|---|---|---|
| Immutable assignment/MA1 source and Open-TYNDP code review | PASS_STATIC | Direct verified source documents/SHAs |
| Hydro reader, interval energy algorithm, type/port logic | IMPLEMENTED | Producer files and positive/negative tests |
| Fixture-based energy, DST/leap, five artificial weather-set interface | PASS_FIXTURE | GitHub Actions pytest witness (see section 3) |
| Static network core unchanged during MA3 | PASS_BY_ISOLATION_ONLY | No MA3 code mutates any network; real M0 before/after fingerprint remains MA4 NOT_EXECUTED |
| G1-C actual M0 DNR plus sidecar, original asset crosswalk, component support | BLOCKED_NOT_PROVIDED | Independent MA1C |
| G1-E real hydro source native intervals, semantics and hydrological mapping | BLOCKED_NOT_PROVIDED | Independent MA1C |
| Exact five externally chosen weather datasets and physical source SHA256 | BLOCKED_NOT_PROVIDED | Independent MA1C |
| Corrected Hydro dataset version and data-use license | NOT_VERIFIED | No physical source archive |
| M0 CAN/2.0.0 canonical_revision_id/projection_id handshake | OPEN_INTERFACE_HOLD | MA1C independent M0 review |
| Real Store/Link source port and source-energy conversion witness | BLOCKED_NOT_PROVIDED | No approved M0/Hydro plant model |
| Real-data Hydro qualification / E2E into MA4 | **NOT_GRANTED** | All physical preconditions required |
| Actual Snakemake run / PyPSA NetCDF roundtrip / loadflow | NOT_EXECUTED | No source inputs and outside standalone adapter scope |

### Consolidated external input gate (one package)

1. Deliver the exact five already-selected project weather IDs and horizons together with physical Hydro files (original and normalized), byte SHA256, version/correction/license, exact source WS columns, native timestamps with authoritative interval-bounds witness.
2. Deliver physical hydro area/TSO/basin registry, original M0 component IDs/capabilities, asset shares per area/tech, and energy/water-to-model unit conversion and evidence, including open/closed pumped hydro identification.
3. Deliver actual M0 DetailedNetworkReference (PyPSA + sidecar + all identity/quality ledgers) and approved Store/Link port models, and resolve the M0 CAN/2.0.0 canonical/projection revision-key translation to MA3's MA1 contract.
4. With this one source package, run the five scenario campaigns, verify full source-native and original-asset MWh closure, nonmutation, actual PyPSA time-series injection policy and independent MA4 review. No Real-Data-PASS or M2 handoff before these facts exist.

## 6. Final producer decision

The full MA3 implementation macro is **delivered and fixture-functional** on its own branch. This satisfies the implementable code/Snakemake/schema/ledger/test preparation scope while the source witness is missing. The **real physical source acceptance remains blocked** in accordance with both MA1 and the independent MA1C gate. No weather years were selected, no synthetic profile was presented as original PECD, no missing inflow was replaced with a fabricated zero, and no original M0 network topology or static component was changed.

**Producer disposition:** IMPLEMENTED_FIXTURE_ONLY__REAL_SOURCE_BLOCKED. **Next responsible owner:** MA4 integration owner *after* MA1C real-source and M0 owner approvals, as specified by HANDOFF_MA4.md.
