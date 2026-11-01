# MD1 — Verbindliche Entscheidung zur Real-Data-Freigabe für MA4R

**MD1-Entscheidung:** `M1_SOURCE_CONTRACT_BLOCKED`  
**MA4R-Real-Data-Gate:** `MA4R_REAL_INPUT_NOT_RELEASED`.  
**Keine** `M1_SOURCE_CONTRACT_WITNESSED`- oder `CONDITIONAL`-Behauptung: Bislang weder eine begrenzte reale PECD-/Hydro-Teilmenge mit tatsächlichem Byte-/Daten-/Zeitwitness noch das reale M0-Paket.

## Was real sofort verwendbar ist

| Subsystem | Quelle/Artefakt | Nutzbar ab jetzt | Status |
|---|---|---|---|
| PECD-native Source | Offizieller v4.2-PUG, CDS-Produktliste, TYNDP 2026 Download-URL, Open-TYNDP 2026 CSV-/Reader-Schemas | **statische Schemaprüfung, Sourcebeschaffung**; kein reales Wind/PV-Szenario als qualifizierte M1-Zeitreihe | `CATALOG_ONLY` |
| Hydro-native Source | TYNDP Hydro-Download-URL, v4.2 Semantik/Technologiemap, MA3-Normalizer | **statische Schema- und Intervallprüfung**; keine echte MW-/MWh-Zeitreihe | `CATALOG_ONLY` |
| M0-CGMES | CAN/2.0.0/DNR/1.0.0-Design, M4-0 Toolchain-/RunRelease-Policy | Normative Implementierungsgrundlage; **kein** reales M0-Referenznetz | `DESIGN_ONLY` |
| MA2/MA3 | getrennte Code- und positive/negative Fixtureprüfungen am fixierten Producer-SHA | rein synthetische Vorqualifikation unter MA4F | `FIXTURE_ONLY` |
| M1 Asset Join | Contract/Blocker/negative Szenarien | kein realer Join, kein qualifiziertes M0→PECD-Mapping | `BLOCKED` |
| MA4R / M2 | vollständig reale Referenz | **nicht nutzbar / nicht freigegeben** | `BLOCKED` |

## Unabhängige Source- und Netz-Gates

Ein erfolgreicher PECD-Source-Download und seine Byte-/Zeit-/Region-/Versionsprüfung könnte zunächst `S-PECD-PHYSICAL=PASS` erhalten, auch wenn M0 fehlt. Hydro-Dateien analog `S-HYDRO-PHYSICAL=PASS`. Ein späteres M0-DNR kann getrennt `N-M0-PHYSICAL=PASS` erreichen. Erst ein nachweisbarer Join mit identischen Revisions-/Profilschlüsseln und hydrologischem/technologischem Mapping erteilt `J-M1=PASS`. Für MD1-Gesamtfreigabe müssen **alle anwendbaren Pflichtgates** positiv sein. Dadurch wird die Nutzerkorrektur (Datenquellen sind unabhängig) normativ abgebildet, ohne die integrierte MA4R-Anforderung zu verwässern.

## Release-Voraussetzungen als *ein einziges* Paket

- exakt fünf zuvor festgelegte `weather_id` inklusive Horizons/Quellentscheidung und alle dafür nötigen echten PECD-/Hydro-/ggf. DFT-Dateien (separat katalogisiert, keine Wahl/Ersatz-ID);
- unabhängige source-native Profile-/Masken-/Intervallbyte-SHA256 sowie PUG/Korrektur-/Lizenz-Konformität, Datenqualitäts- und Coverage-QA;
- separat von M0-Owner tatsächlich erzeugter DNR/1.0.0-PyPSA-/Sidecar-/Identity-/Geo-/Hydro-Port-Package und eigene positive M0-Capability;
- explizite, quellbelegte M1-Source→Asset-/Basin→Port-Zuordnung inklusive PV-MWp/AC- und Offshore-Witness, vollständiger `canonical_revision_id+projection_id+reference_id`-Handshake und Sourceformat-/Masken-Interop;
- positive MA4F Fixture-Integration als **separate** Produktionsvoraussetzung, anschließender voller MA4R-E2E-Lauf mit statischer M0-Invarianz, NetCDF-Roundtrip, fünf-Set-Source-/Energy-Coverage und unabhängiger M1-Abnahme.

Siehe **einziges** [BLOCKER_REGISTER.csv](BLOCKER_REGISTER.csv) und [S_GOV_M1_HANDOFF.md](S_GOV_M1_HANDOFF.md). Keine weiteren Mikroschleifen. MD1 gibt MA4R nicht frei und verändert weder M0 noch MA2/MA3 oder M2.
