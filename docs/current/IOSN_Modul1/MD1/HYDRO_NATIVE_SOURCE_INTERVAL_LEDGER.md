# MD1 — Hydro native source / interval / semantics independent from CGMES

**Source-native Ebene:** PECD/TYNDP-Hydro liefert regionalisierte/ hydrologische Energieinformationen. Es kennt **keine** PyPSA-`StorageUnit`-/Bus-/Generator-ID. Elektrische Zuordnung zu Anlagen und Hydro-Port ist eigener nachgelagerter Join.

## Hydrotypen und Datenkategorie

| Code | Source-native Semantik | Konsequenz ohne Anlagenkenntnis |
|---|---|---|
| `HRR` | Run-of-river inflow energy `MWh` | nicht stündliche Erzeugung/Dispatch |
| `HRI` | Reservoir inflow energy `MWh` | nicht automatisch schon elektrische Speicherenergie |
| `HPI` | Pondage inflow energy `MWh` | mit eigener Hydroklasse und native Intervallen |
| `HOL` | Open-loop pumped-hydro natural inflow (wenn geliefert) | Pumpstrom und natürlicher Zufluss getrennt |
| `HCL` | Closed-loop pumped-hydro TYNDP-Anlagentyp | nur bei unabhängig belegter Klasse `NO_NATURAL_INFLOW_BY_DESIGN`; `NOT_APPLICABLE` ≠ fehlende Datei mit 0 |
| `HRO` / `HPO` / `HRG` | tatsächlich generierte Energie `MWh` | **nicht** als Hydro-`inflow` deklarieren |

Die unabhängige PECD-v4.2-Spezifikation dokumentiert hydrologische Produkte typischerweise in `SZON` und wöchentlichen `MWh`. Der tatsächliche separate **TYNDP-2026-Hydro-Input** kann `WEEK`-/Tageswerte enthalten; er muss **an echten Dateibezügen** qualifiziert werden, nicht allein durch den PUG-Produktnamen.

## Unabhängiger echter Hydro-Source-Witness

Für jede bereitgestellte Datei sind ohne jedes CGMES-Netz prüfbar: `source_id`, `dataset_version`/`fv`, provider, ursprüngliche Dateibytes + SHA-256, Rechte/Revision, exakter `weather_id`/Klimahorizont, Source-Area-ID, Hydro-Tech-Code, `inflow` gegen `generation`, `native_source_unit`, `native_interval_key`, originärer `[start,end)`-UTC-Zeitbeleg, echte `energy_mwh`-Zahlen und Quell-Negativfälle. Für jede einzelne Quellstunde/-woche: keine Null-/Mittelwert- oder unzulässige Horizon-Substitution.

Für ein belegtes Originalintervall `k=[t0,t1)` und seine Source-Energie `E_z,k` ist die Dauer `h_k=(t1-t0)/3600` in *echten* UTC-Stunden zu bestimmen. Eine dokumentierte uniforme Disaggregation `P_z,k=E_z,k/h_k` kann Source-Intervallenergie erhalten, ist aber **nicht** beobachtete stündliche natürliche Wassermenge. Ein wöchentlicher Index `WEEK=53` ist kein Freibrief für genau 168h; Teilwoche, Leap-Year und DST per Originalgrenzen verifizieren.

**Getrennte spätere M1-Join-Ebene:** `hydro_area_id+hydro_tech -> existing_M0_hydro_asset+approved_storage_port` mit echten Becken-/TSO-Anteilen `B`, Nachweis `sum_a B=1` für vollständig abgebildete Source-Areas und getrennter Umrechnung `E_model=c E_source B`. Hydraulische Energie und PyPSA-Speichermodellenergie sind nicht pauschal identisch. Kein Mapping anhand elektrischer Buspunktnähe.

## Verifizierte Reader-/Quellgrenzen

`open-tyndp@71a3a9a15b77114cd79458bceabc98e1a64dd58a`: `clean_tyndp_hydro_inflows.py` nutzt Dateinamen nach `TYNDP_NODE`, `WEEK`/daily, `.ffill()`, `/168`/`/24`, `.fillna(0)`; als echte MD1-Quellqualifikation **nicht** direkt geeignet. MA3 @ `b3b9bf133d1b5c968323a31f8ac76090f1f2e182` normalisiert nur belegte Source-/Bounds-SHA256 und berechnet echte Dauer; dessen Anlagensplits gehören nachgelagert in Join.

**Quelle gefunden:** [TYNDP-2026 Downloadportal](https://2026.entsos-tyndp-scenarios.eu/download/) verlinkt separates Hydro-Inflow-ZIP; [PECD-v4.2 PUG](https://confluence.ecmwf.int/spaces/CKB/pages/540941752/Climate+and+energy+related+variables+from+the+Pan-European+Climate+Database+derived+from+reanalysis+and+climate+projections+v4.2+Product+user+guide+PUG) erläutert originale hydroenergetische Produkte. **Quellbytes nicht einsehbar**, weder reale WEEK-/DAY-Zeile noch eine regionale Energiezahl oder Originärgrenze geprüft.

**Entscheidung:** `S-HYDRO-CATALOG=PASS_STATIC_CATALOG_ONLY`; `S-HYDRO-PHYSICAL=BLOCKED_NOT_WITNESSED`; `HYDRO_BASIN_TO_M0_JOIN=BLOCKED_PREREQUISITES`, ohne diese beiden fachlich unterschiedlichen Status zu vermischen.
