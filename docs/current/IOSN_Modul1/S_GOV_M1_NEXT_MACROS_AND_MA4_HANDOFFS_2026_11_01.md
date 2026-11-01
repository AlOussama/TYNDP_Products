# S-GOV-M1 — nächste konsolidierte Makro-Aufträge und direkte Worker-Handoffs

**Datum:** 2026-11-01
**Autorität:** [Parallelrücklauf-Konsolidierung](S_GOV_M1_CONSOLIDATED_MA1C_MA2_MA3_REVIEW_2026_11_01.md) am Commit `91f5d5f4df23188478764b2149928d3f3939a426`. Historische Ausgangsbaseline `2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994`.
**Entscheidung:** Jetzt gleichzeitig `M1-MA4F` (Fixture-/Integrationsmakro in neuem Chat) und `M1-MD1` (Real-Source-/M0-Datenqualifikation, Data-/M0-Owner) vorbereiten/ausführen. `M1-MA4R` realer End-to-End-/Abnahmemakro **erst nach** A+B. Vollständiger M2-Handoff nach independent Reviewer + S-GOV.
**Makroprinzip:** keine Mikroaufträge für einzelne Fehlermeldungen, Anlagen, Wetterjahre oder Technologien; je Makro ein vollständiger Rücklauf, ein isolierter Git-Branch, Tests und ein revisionssicherer Gateentscheid.

## 1. Auftrag M1-MA4F — Fixture Integration & Interface Reconciliation (SOFORT, SEPARATER CHAT)

**Rolle:** verantwortlicher Python-/PyPSA-/Snakemake-Integrator und Integrationsarchitekt. Dies ist ein **Ausführungsauftrag** zur vollständigen Fixture-E2E-Integration, keine weitere allgemeine Planung.

**Verbindliche erste Aktionen:**
- Überprüfe S-GOV Review `91f5d5f4...`, danach die ursprünglichen MA-1-Contracts (Basis `2c0b482...`), MA-1C Source-Gate `f366f8162e1023ff959721d5fed14ad80dcba890`, MA-2 Producer `11700baa8df8cafc6bd71b96998f8b2bca647ca0`, MA-3 Producer `b3b9bf133d1b5c968323a31f8ac76090f1f2e182`.
- Lies **vollständig** MA-2 und MA-3 Reports, Handoffs, Quellschemas, Reader/Adapter/CLI, Snakemake-Rules und Testfixtures. Lies M0 `85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md`, `90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md` am `b1e284996fa69f81651daf9150b829e6a42e4ce3` und jüngeren `95/96`-Preflight am `ba55e4a12819a88605474606888ca23ee2108584`; **M0-Produktivnetz noch nicht belegt**.
- Arbeite auf neuem, exklusivem Branch, Vorschlag `impl/iosn-m1-ma4f-fixture-integration-20261101`. Nutze `2c0b482...` als gemeinsame Ausgangsbasis und führe die beiden Producerlieferungen **gezielt** zusammen; dokumentiere alle übernommenen Blob-/Commit-IDs. Kein direktes Mergen in `main`, keine Änderung an den Original-Producer-Branches.

**Konsolidierte Pflichtausführung:**
1. Vereinheitliche `scripts/iosn_m1/__init__.py`, gemeinsame Dependency-BOM, Python/PyPSA/xarray/pandas/Geo/Snakemake-Pins und reproduzierbare Testumgebung. **Kein zufälliges Neuschreiben der qualifizierten Adapter.** Respektiere Originalmodule, repariere nur tatsächliche Integrationsdefekte.
2. Definiere einen **versionierten M0 DNR/1.0.0 Identity-Bridge** (`source_revision_id`, `operating_state_id`, `canonical_revision_id`, `projection_id`, Source-ID→PyPSA-View-ID), der ältere `network_revision_id`-Felder der Producer kontrolliert abbildet; nur mit Schema-autorisiertem Mapping, keine stillen Aliase.
3. Definiere das **Master-Input-Manifest** und zwei spezifizierte Adapter-Sichten, sodass MA-2 JSON Weather Manifest und MA-3 Hydro Manifest intern weiterhin gelesen werden können, aber die fünf echten externen `weather_id`-Slots, Horizon, UTC-Zeitachse, Source-Hash, M0-Revision und Quality-Klasse EINEN Eigentümer haben.
4. Definiere die dynamische PyPSA-Write-Allowlist und das **Target-Ownership-Ledger**: Wind/PV `Generator.p_max_pu` aus MA-2; RoR `Generator.p_max_pu` aus MA-3 **ohne Kollision**; Hydro `StorageUnit.inflow`; Store/Link-Staging nur mit explizitem M0-Port- und Owner-Zustimmungsstatus, sonst verweigern; DFT/Load nur bei existierender geprüfter Quelle und nicht-mutierendem Umgang mit M0-`loads_t.p_set`.
5. Implementiere **einen** PyPSA-Composer an einem real ausführbaren, **synthetischen DNR/1.0.0 Fixture** inklusive Sidecar, Original-IDs, Generator/Load/StorageUnit/Store/Link/Transformer/3W-Synthetic-ID und synthetischen fünf Weather-IDs; statische Fingerprints für **alle** M0-Komponententabellen vor/nach jeder Zeitreiheninjektion, NetCDF Import/Export/Roundtrip, Missing/Overwrite/Collision negative Tests.
6. Führe die MA-2- und MA-3-Tests gemeinsam unter einem konsistenten PyPSA-/Snakemake-Host aus, mindestens `pytest` und `snakemake -n`/Dry-Run, und wo für Fixture möglich vollständige Snakemake-Ausführung. Jede Testumgebung, Logs, Runtimeversion und Ausführungshash belegen. Keine reale Source behaupten, wenn die Dateien nur synthetisch sind.
7. Prüfe Speicher-/CPU-Datenvolumen für die fünf Szenarios, führe Snapshot-/UTC-/Leap-/Wirkungsgrad-/PV-MWp- und geometrische Negativfixtures zusammen und liefere **ein** konsolidiertes Integrations-/Konfliktledger. Kein Clustering, keine Netzreduktion, kein neues Wetterjahr.
8. Bei Datenmangel `MA4_FIXTURE_INTEGRATION_QUALIFIED` nur für synthetischen Scope; `REAL_SOURCE_NOT_QUALIFIED` festhalten. Gib niemals den M2-Handoff frei.

**Pflichtabgabe:** versionierte Master-Schemas/BOM, vollständiger Composer + `rules/iosn_m1_compose.smk`, integrierter MA-2/MA-3-Satz, `tests/iosn_m1/test_integrated_*.py`, nachvollziehbare Source-SHAs/Schema-Bridge, `docs/current/IOSN_Modul1/MA4F/EXECUTION_REPORT.md`, `INTEGRATION_CONFLICT_LEDGER.md`, `HANDOFF_MA4R.md`, `QA.json`, Commit und PR-Entwurf.

**Exit:** `M1_MA4F_FIXTURE_INTEGRATION_QUALIFIED` oder `M1_MA4F_REPAIRS_REQUIRED`, mit numerisch belegten Tests. **Kein** Real-Daten- oder M2-PASS.

## 2. Auftrag M1-MD1 — Consolidated Real Source + M0 DNR Witness (PARALLEL, DATEN-/M0-OWNER)

**Rolle:** Data Owner/Source Auditor und M0-Referenz-Owner mit klar getrennten Freigaben. **Kein erneuter allgemeiner Literaturreview.**

**Verbindlicher Ausgangspunkt:** MA-1C `OPEN_INPUTS_AND_EXIT_CRITERIA.md` am `f366f8162e1023ff959721d5fed14ad80dcba890`, IN-01…IN-10; M0 S-GOV-Freeze `b1e284...`, M0 M4-0 `ba55e4...`.

**Konsolidierte Pflichtausführung:**
- Stelle **ein** gebündeltes, zugriffsrechtlich zulässiges Quellpaket bereit und verifiziere: genau die fünf bereits festgelegten Weather-IDs plus Horizons; PECD Wind/PV profile bytes/region masks/tech units; Hydro `HRR/HRI/HPI/HOL/HCL` Quell-MWh-/Intervalle und Basin-/TSO-Anteile; bei Pflichtumfang Demand/DFT-Stunden und Last-ID-Splits; vollständige Quelldaten-SHA256/Lizenz/Freigabeversion/Korrekturdaten.
- M0-Owner liefert **wirklich ausgeführtes**, versioniertes `DetailedNetworkReference` mit PyPSA-Netz, Sidecar, Source-/View-/Asset-ID, Geo-/Busrollen, Originalkapazitäten, Hydro-Modellports sowie qualifizierter statischer und elektrischer M0-Referenzfähigkeit. Dokumentarischer M0-Freeze ist nicht ausreichend; Runtime-Freigabe erfolgt ausschließlich durch den M0-Owner-Prozess.
- Bestätige DNR-CAN/2.0.0 Rev-/Projection-Key-Mapping zum M1-Bridge-Contract. Reale Anlage/PECD-Profil-Assoziation und Hydro-Basin-Anteile müssen aus Quelle/TSO/zulässigen Geodaten nachvollziehbar sein, nicht aus erfundenen `nearest`-Heuristiken.
- Prüfe je Quelle tatsächliche Bytes/Intervallgrenzen, PV DC/AC-Basis, Offshore-Geo, fünf Sätze ohne Fallbacks und Datenlizenzen. Die projektintern schon gewählten Wetterjahre werden **nicht erneut gewählt**.
- Übergabe: einmaliges maschinenlesbares Source-Manifest, Real-Source-Coverage, M0-Identity-Bridge-Witness, Geo-/Hydro-Tabellen, Quelldatenhashes und eindeutiges `M1_SOURCE_CONTRACT_WITNESSED` oder `M1_SOURCE_CONTRACT_BLOCKED`. Wo tatsächliche Dateien fehlen: **ein konsolidierter Blockerbericht**, keine unbegründeten PASS-Labels.

**Exit:** G1-C/D/E inklusive tatsächlicher Physik-/Raum-/Revisionsbelege; Real-Data-Scope und Data Access dokumentiert. Ohne diese Freigabe darf MA4R nicht als vollständige reale Qualifikation starten.

## 3. Auftrag M1-MA4R — Full Real Source Campaign & Independent Acceptance (NACH MA4F + MD1)

**Rolle:** eigener MA4R-Integrationschat mit echtem Datenzugang; danach separater unabhängiger `R-M1-MA4`-Reviewer.

**Verbindliche Inputs:** MA4F freigegebener Producer-Code/Fixture-E2E-Commit, MD1 vollständiges Real-Source-Paket/Source-Decision, qualifiziertes M0-DNR/Sidecar. Kein Rückgriff auf imaginäre PECD-WS.

**Konsolidierte Pflichtausführung:**
- Exakte fünf vorselektierte Wetterdatensätze und tatsächliche Planungshorizonte für RES, Hydro und gemäß Zielscope Lasten in das **unveränderte M0-Netz** integrieren, mit vollständiger Originalbus-/Generator-/Speicher-ID-Provenienz.
- Onshore PEON/P2ON, Offshore PEOF/P2OF, PV ORIG/Regional, MWp↔MW_AC, hydrologische Basin-Zuordnung/energetische Source-/Plant-Closure und gültige UTC-Zeitachse real qualifizieren. Keine metrisch unbelegte höhere Wetterauflösung behaupten.
- Vollständige NetCDF-Outputs pro `(horizon,weather_id)`, Quell-zu-Netz-Integritätsbelege, MW-Coverage, ursprüngliche Statische-Tabellen-Fingerprints, Import/Export-Hashes, kombinierte Tests, Speicher-/Laufzeitdaten. Falls verifizierte bilanzierten Betriebsfälle vorhanden, PF separat qualifizieren; bloße `p_max_pu` ist kein Dispatch.
- Vollständigen Producer-Commit publizieren, **unabhängigen Reviewer** getrennt beauftragen. Erst nach überprüfbarem Reviewer-PASS und S-GOV-Entscheidung `M1_DETAILED_REFERENCE_READY_FOR_M2`.

**Exit:** `M1_REAL_REFERENCE_READY_FOR_INDEPENDENT_REVIEW` (Producer), dann `R_M1_ACCEPTED`/begrenzte Findings (Reviewer), dann `S_GOV_M1_M2_RELEASED` oder `BLOCKED` (Owner). Ein Status allein ersetzt nicht die andere Autorität.

## 4. Governance und Ausführung ohne Mikroiterationen

- **S-GOV in diesem Chat:** überprüft nur Makro-Rückläufe am fixierten Commit, entscheidet Merge-/M2-Gates; implementiert nicht heimlich parallel zu einem Worker.
- **MA4F neuer Chat jetzt:** vollständige Fixture-Integration mit real installierter PyPSA-/Snakemake-Runtime auf eigenem Branch. Codeänderungen bleiben auf Adapter-/Composer-Ebene; kein PyPSA-Core-Fork.
- **MD1 parallel:** M0-/Datenowner liefert ein Paket; falls keine reale Datenquelle verfügbar ist, dokumentierter `BLOCKED`-Rücklauf und Fortführung nur von Fixture-Arbeiten.
- **MA4R und unabhängiger R:** erst nach Gatenachweisen; echte Referenzfreigabe in diesem Governance-Chat.
- **Kein Main-Merge von MA-2/MA-3 ohne Integrationsreview.** MA3-PR #7 ist Draft, MA2 noch ohne PR; finalen Aggregationscode M2 separat halten.
