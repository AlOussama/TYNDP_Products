# Handoff — MD1 → bestehender S-GOV-M1-Chat

**Projekt:** `AlOussama/TYNDP_Products`  
**Makro:** `M1-MD1 Consolidated Real Source & M0 Reference Witness`  
**Quelle/Autorität:** S-GOV `03fa261850da8c940283668741bb7a17c46bd769` §2, S-GOV-Konsolidierungsbericht; MA1C `f366f8162e1023ff959721d5fed14ad80dcba890`, M0 CAN/2.0.0 DNR/1.0.0 `b1e284996fa69f81651daf9150b829e6a42e4ce3`, M0 M4-0 `ba55e4a12819a88605474606888ca23ee2108584`.  
**MD1-Finalentscheidung:** `M1_SOURCE_CONTRACT_BLOCKED` und `MA4R_REAL_INPUT_NOT_RELEASED`.

## Verbindliche Korrektur zum Datenfluss

**PECD/TYNDP und CGMES/M0 sind zwei unabhängige Datenströme.** Native PECD-Wind-/PV-/Hydro-Source-QA (Regionscode, Raster, CF/MWh, Zeit, Weather-ID, SHA, Version/Rechte) ist netzunabhängig. M0 liefert separat elektrische Topologie, Generatoren/Lasten/Hydroports und Sidecar. Source→M0-Asset/Basin→Port-Mapping liegt **ausschließlich im M1-Join**. Die fehlende M0-Datei ist kein PECD-Sourcedefekt, blockiert aber den realen M1-Join und damit MA4R.

## Ausgeführte Evidenz und Gates

- Quellen/Unterlagen: fixierte M1-/M0-Owner-Commits, MA1C-Inputliste IN-01…IN-10, MA2-/MA3-Reports/Schemas/Adapter, Open-TYNDP 2026 `71a3a9a15b77114cd79458bceabc98e1a64dd58a`, offizielle ECMWF PECD-v4.2-PUG/CDS und TYNDP-2026-Download-/CC-BY-4.0-Erklärung. Statische Katalogprüfung `PASS_STATIC`.
- Real native data: **0/5** festgelegte Projekt-IDs im zugänglichen Manifest; **0** echte PECD-Wind-/PV-Sourcebytes, **0** echte Hydro-Inflow-Dateien/native Bounds, **0** tatsächlich geladene PECD-fractional-NetCDF-Masken, **0** Source-Byte-SHA256; `S-PECD-PHYSICAL=BLOCKED`, `S-HYDRO-PHYSICAL=BLOCKED`. Öffentliche ZIP-Links sind vorhanden, in dieser Auditumgebung nicht als Binärdatei gelesen.
- Reales M0: CAN/2.0.0/DNR/1.0.0-Freeze ist dokumentarisch, M4-0 nur statischer Preflight. **0** reale qualifizierte M0-DNR-Netze samt Sidecar/Originalanlage/Geo-/Hydroport. `N-M0-PHYSICAL=BLOCKED`.
- M1 Join: keine realen originalen Anlagen-/Geo-/hydrologischen Zuteilungen; `J-M1=BLOCKED`. Legacy-Producer `network_revision_id` ≠ vollständiger DNR-Handshake aus `canonical_revision_id`, `projection_id`, `reference_id`.
- **Zusätzliches konkretes Integrationsrisiko:** MA2 Source-Reader nur CSV/ISO, offizielle ORIG-PV-Quelle ggf. NetCDF; GeoJSON-Polygone nicht unmittelbar identisch mit offiziellen PECD fractional NetCDF-Masken. Kein Verlust-/Verfeinerungs-Fallback. Aufgabe der MA4F-/RES-Integration, **nicht** MD1-Code.
- Weder Produktion, Tests an echten Daten, CGMES-Topologie, PyPSA-Stammdaten noch Wetterjahrwahl verändert; kein Main-Merge.

## S-GOV-Anweisung und Entscheid

**Nicht MA4R oder M2 freigeben.** MA4F darf Fixture-E2E unabhängig weiterarbeiten; seine spätere vollständige positive Fixture-QA ist keine Real-Data-Source-Freigabe. Für den nächsten gebündelten Owner-Release exakt [BLOCKER_REGISTER.csv](BLOCKER_REGISTER.csv) mit BMD1-01..09 (plus bedingte Scope-Items) abarbeiten: tatsächliche fünf IDs/Horizons, offizielle source-native Wind/PV/Hydro-/Maskenfiles mit SHA256/Freigabeversion, separat echtes M0 DNR/Sidecar/Identity, hydrologische Asset-Anteile und M0 Geo-/PV-Portbasis, dokumentierter DNR-Bridge-/Format-Handshake. Danach **ein** echter fünf-Sets-Qualifikationslauf und unabhängiger Reviewer.

**Übergabe:** MD1 Source-/Hydro-/M0-/Join-Ledgers, maschinenlesbarer `QUALIFICATION_REPORT.json`, einziges konsolidiertes `BLOCKER_REGISTER.csv`, `MA4R_RELEASE_DECISION.md`. Ein SRC-native-PASS kann bei späterer Nachreichung eigenständig erteilt werden, ohne M0 als PECD-Provider darzustellen. Die Gesamtklasse bleibt bis zur vollständigen M1-Real-Input-Qualifikation `BLOCKED`.
