# MA1C — Konsolidierte Handoffs für die parallelen Makros MA2 und MA3

**Source- und M0-Gate:** `M1_SOURCE_CONTRACT_BLOCKED`. Beide Makros dürfen den **kontraktgebundenen Fixture-/Adaptercode** parallel entwickeln und je ein finales Implementierungs-/Testpaket liefern, **keine** reale qualifizierte Profil-/Hydro-/M0-Integration beanspruchen. Gemeinsamer unveränderlicher Input: M1-NEXT_MACROS @ `2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994`, MA1-Logical-YAML, vorliegendes MA1C Ledger und M0-Spezifikation mit normativer DNR-Repair-Beobachtung.

## MA2 — RES / PECD v4.2 Renewable Profiles / Spatial Mapping

**Arbeitsbranch:** `impl/iosn-m1-ma2-pecd-res-20261101` (eigenständig von freigegebener gemeinsamen Baseline; keine MA1C-Dateien überschreiben).

**Auftrag:** Implementiere **ein einziges** isoliertes Makro Wind-Onshore, Wind-Offshore, Solar Utility/Rooftop. Übernimm aus Open-TYNDP `tyndp-2026` @ `71a3a9a15b77114cd79458bceabc98e1a64dd58a` nur geeignete PECD v4.2 File-/Spaltenparser, xarray-/Snakemake-Bausteine und Technologie-Crosswalk. `TYNDP_NODE`, `buses_tyndp`, `busmap_base_s_all.csv` sind **keine** CGMES-Generator-/Bus-IDs. Lege `profile_catalog`, `source_manifest`, `asset_profile_map` mit M0-`asset_id/view_id/pypsa_component_id` und Source-/Geoqualität an.

**Mindestfixtures in einem Durchlauf:** PEON+P2ON und zwei getrennte Generatoren derselben Region, PEOF+P2OF mit Offshore-Standort vs Landfall, PV-ORIG gegen regionale PV, PV DC-MWp→AC-MW/Clipping und negative fehlende Konversion, Grenzpunkt/dual masks, Composite mit belegten MW-Anteilen, M0-3W-Stern, Leap/DST/UTC, alle fünf Slot-IDs explizit mit `NOT_PROVIDED`-Verweigerung, Missing/Zero/Fallback-Verbote. Für realen Profile-Writer `generators_t.p_max_pu` ausschließlich bestehende IDs verwenden, keine `p_nom`/`bus`-Mutation. Physische Quelle `ORIG` nur wenn wirklich vorhanden. Bei Layout-Proxies die abgeleitete Qualität nicht als Anlagenpunkt ausgeben.

**Abnahme:** `M1_RES_FIXTURE_QUALIFIED` bei positiv/negativ getesteten synthetischen Fixtures, `IMPLEMENTED_FIXTURE_ONLY` falls keine echten PECD/M0-Daten. `M1_RES_REAL_DATA_QUALIFIED` nur mit G1-C/D, fünf realen Source-IDs, echten M0-Generatoren, versionierten Masken, MW-Coverage und Source-Roundtrip. **Nicht** aufgrund bestandenem Code-/Fixturetest.

**Pflichtabgabe:** `scripts/iosn_m1/res/`, `rules/iosn_m1_res.smk`, `tests/iosn_m1/test_res*.py`, Source-/Profile-/Assignment-Metadatenschemas, `docs/current/IOSN_Modul1/MA2/EXECUTION_REPORT.md`, `HANDOFF_MA4.md`, exakter Commit-/Test-/Known-Gaps-Status.

**Verbindliche MA1C-Eingänge:** [FIVE_WEATHER_ID_LEDGER.csv](FIVE_WEATHER_ID_LEDGER.csv), [PECD_SPATIAL_PRODUCT_MATRIX.md](PECD_SPATIAL_PRODUCT_MATRIX.md), [SPATIAL_ASSIGNMENT_LEDGER.csv](SPATIAL_ASSIGNMENT_LEDGER.csv), [SOURCE_STATUS_LEDGER.csv](SOURCE_STATUS_LEDGER.csv), [M0_REFERENCE_WITNESS.md](M0_REFERENCE_WITNESS.md).

## MA3 — Hydro Inflow / Basin Allocation / Original Asset Ports

**Arbeitsbranch:** `impl/iosn-m1-ma3-hydro-20261101` (getrennt von MA2 und MA1C).

**Auftrag:** Ein kompletter Hydro-Inflow-/Zeit-/Energie-/Port-Adapter. Untersuche `clean_tyndp_hydro_inflows.py` und `build_tyndp_hydro_profile.py` aus festem Open-TYNDP-Commit, aber **übernimm nicht** deren unbewiesene `168h`/`24h`-Division, `ffill`, `fillna(0)` oder TYNDP-Zone als Originalanlage. Typisiere `HRR/HRI/HPI/HOL/HCL` und negative `HRO/HPO/HRG`-Generation. `closed-loop HCL` nicht durch erfundenes Null-Inflow-File qualifizieren. Für jedem nativen Quellintervall berechne aus echten Grenzen `P_MW=E_MWh/Δh` und prüfe volle Energieerhaltung. Basin/TSO-/Hydroasset-Anteile nur aus belegter Herkunft; PyPSA-`StorageUnit`/`Generator`/`Store+Link`-Port nur mit M0-Freigabe.

**Mindestfixtures in einem Durchlauf:** Tages-/Wochenenergie, 53. bzw. letzte Teilwoche, Leap/DST/UTC, Region→mehrere Speicher mit `B`-Erhaltung, negative nicht zuordenbare Basin/Asset-IDs und falsche Wirkungsgrade, HRI/HPI/HOL/HRR/HCL-Typport, Closed-Loop ohne natürliche Source, fehlendes vs echtes Null-Inflow, unpassendes Source-WS, fünf Slot-IDs ohne Fallback, Original-M0-Static-ID-Invarianz.

**Abnahme:** `M1_HYDRO_FIXTURE_QUALIFIED` für echte getestete synthetische Einheiten-/Energiekonstrukte; ohne G1-C/E maximal `IMPLEMENTED_FIXTURE_ONLY`/`BLOCKED_MISSING_SOURCE`. `M1_HYDRO_REAL_DATA_QUALIFIED` erst bei fünf realen Hydroquellensets, tatsächlichen Anlagensplits/M0-Ports, Source-Intervalle und MWh-Closure.

**Pflichtabgabe:** `scripts/iosn_m1/hydro/`, `rules/iosn_m1_hydro.smk`, `tests/iosn_m1/test_hydro*.py`, versioniertes `hydro_allocation_schema`, `interval_energy_ledger`, `docs/current/IOSN_Modul1/MA3/EXECUTION_REPORT.md`, `HANDOFF_MA4.md`, Commit + Gate-/Test-/Blocker-Bericht.

**Verbindliche MA1C-Eingänge:** [HYDRO_SOURCE_INTERVAL_LEDGER.md](HYDRO_SOURCE_INTERVAL_LEDGER.md), [M0_REFERENCE_WITNESS.md](M0_REFERENCE_WITNESS.md), [M0_INTERFACE_CROSSWALK.csv](M0_INTERFACE_CROSSWALK.csv), [FIVE_WEATHER_ID_LEDGER.csv](FIVE_WEATHER_ID_LEDGER.csv), [SOURCE_STATUS_LEDGER.csv](SOURCE_STATUS_LEDGER.csv).

## Gemeinsame M0-Owner- und Real-Data-Eskalation (genau einmal)

Beide Worker prüfen dieselbe [OPEN_INPUTS_AND_EXIT_CRITERIA.md](OPEN_INPUTS_AND_EXIT_CRITERIA.md). Ein gebündeltes M0-DNR+Sidecar+Source-Manifest+fünf-WetterIDs+PECD/Hydro-Byte- und Regionsmaskenpaket genügt als spätere E2E-Requalifikationsbasis; kein gesplittetes Nachfragen nach jeder Region oder jedem Klima-WS. Bei M0-CAN/2.0.0 vs M1-`network_revision_id` expliziten `canonical_revision_id`/`projection_id`-Handshake verlangen; keine eigenmächtige Umdefinition.

**MA4 bleibt nachgelagert** und benötigt reale, positiv qualifizierte MA2-/MA3-Outputs sowie das echte M0-Netz und falls Pflicht entsprechende Load-/DFT-Evidenz. Kein M2-Netzreduktions-/Clustering-Code in MA2 oder MA3.
