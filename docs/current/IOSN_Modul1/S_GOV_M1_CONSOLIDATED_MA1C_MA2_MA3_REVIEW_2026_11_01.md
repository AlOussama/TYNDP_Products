# S-GOV-M1 — Konsolidierte MA-1C-/MA-2-/MA-3-Bewertung und Integrationsfreigabe

**Datum:** 2026-11-01
**Status:** `M1_PARALLEL_DELIVERIES_COMPLETE__FIXTURE_QUALIFIED__REAL_DATA_BLOCKED`
**Bewertung:** Unabhängiger Governance- und statischer Schnittstellenabgleich, **kein** neuer Produktions-/Snakemake-/PyPSA-Test, **keine** reale Datenqualifikation und **keine** Freigabe an Modul 2.
**Ausgangsauftrag:** [NEXT_MACROS vom 2026-11-01](https://github.com/AlOussama/TYNDP_Products/blob/2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994/docs/current/IOSN_M1_NEXT_MACRO_ASSIGNMENTS_AND_HANDOFFS_2026_11_01.md) @ `2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994`.

## 1. Autoritative Rückläufe: direkt am Immutable Commit geprüft

| Makro | SHA/Branch | Lieferungen | Ausführungsbeleg | Ergebnis |
|---|---|---|---|---|
| MA-1C Source & M0 Witness | `f366f8162e1023ff959721d5fed14ad80dcba890` / `research/iosn-m1-ma1c-source-witness-20261101` | 12 neue Dokument-/CSV-Ledger; keine Python-Änderungen | GitHub-Rohquellen geprüft, keine heruntergeladenen realen PECD-/Hydro-Bytes und kein reales M0-Paket | **`M1_SOURCE_CONTRACT_BLOCKED`** |
| MA-2 PECD RES | `11700baa8df8cafc6bd71b96998f8b2bca647ca0` / `impl/iosn-m1-ma2-pecd-res-20261101` | 17 neue Dateien: Reader, Zuordnung, Snakemake, Katalog, JSON-Schema, Tests, QA | **20/20 lokale Fixture-Tests laut Producerreport**; am Branch-HEAD keine bestätigte PR-Triggered-Actions-Kampagne; weder PyPSA noch Snakemake im lokalen Testhost installiert | **`M1_RES_FIXTURE_QUALIFIED__REAL_DATA_GATE_BLOCKED`** |
| MA-3 Hydro | `b3b9bf133d1b5c968323a31f8ac76090f1f2e182` / `impl/iosn-m1-ma3-hydro-20261101` | 20 neue Dateien: Hydro-Reader, Normalisierer, CLI, Snakemake, Schemas, positive/negative Tests, Ledger, Reports | GitHub Actions **41311811036** (Implementation `f4f721...`) und **41311980437** (Branch-HEAD) jeweils `success`; core-tests job `pytest -q` und Demo-Step PASS; berichtete **62 Gesamttests**, synthetische Fixtures + bestehende Tests | **`IMPLEMENTED_FIXTURE_ONLY__REAL_SOURCE_BLOCKED`** |

**Evidenzauflösung:** 20 MA-2-Tests = Producerangabe, nicht unabhängig erneut ausgeführt. Die 62 MA-3-Tests bezeichnen den gesamten CI-Pytest-Lauf, **nicht 62 eigenständige Hydro-Testfälle**. Beide Ausführungsstände sind kein Quell- oder physikalischer Realnetz-PASS. Alle drei Branches divergieren nicht von der gemeinsamen Basis: jeweils 1/13/30 Commits voraus, 0 dahinter; ungemergt.

Primärbelege:
- [MA1C Report](https://github.com/AlOussama/TYNDP_Products/blob/f366f8162e1023ff959721d5fed14ad80dcba890/docs/current/IOSN_Modul1/MA1C/CONSOLIDATED_EXECUTION_REPORT.md), [Freeze Decision](https://github.com/AlOussama/TYNDP_Products/blob/f366f8162e1023ff959721d5fed14ad80dcba890/docs/current/IOSN_Modul1/MA1C/CONTRACT_FREEZE_DECISION.md), [Inputliste](https://github.com/AlOussama/TYNDP_Products/blob/f366f8162e1023ff959721d5fed14ad80dcba890/docs/current/IOSN_Modul1/MA1C/OPEN_INPUTS_AND_EXIT_CRITERIA.md)
- [MA2 Report](https://github.com/AlOussama/TYNDP_Products/blob/11700baa8df8cafc6bd71b96998f8b2bca647ca0/docs/current/IOSN_Modul1/MA2/EXECUTION_REPORT.md), [Adapter](https://github.com/AlOussama/TYNDP_Products/blob/11700baa8df8cafc6bd71b96998f8b2bca647ca0/scripts/iosn_m1/res/adapter.py), [QA JSON](https://github.com/AlOussama/TYNDP_Products/blob/11700baa8df8cafc6bd71b96998f8b2bca647ca0/docs/current/IOSN_Modul1/MA2/SOURCE_GATE_STATUS.json)
- [MA3 Report](https://github.com/AlOussama/TYNDP_Products/blob/b3b9bf133d1b5c968323a31f8ac76090f1f2e182/docs/current/IOSN_Modul1/MA3/EXECUTION_REPORT.md), [Adapter](https://github.com/AlOussama/TYNDP_Products/blob/b3b9bf133d1b5c968323a31f8ac76090f1f2e182/scripts/iosn_m1/hydro/adapter.py), [CI run](https://github.com/AlOussama/TYNDP_Products/actions/runs/41311980437), [PR #7](https://github.com/AlOussama/TYNDP_Products/pull/7)

## 2. Positiv bewertete technische Ergebnisse

1. **Elektrische Originalauflösung:** Beide Adapter sind isolierte Zeitreihen-Compiler; sie erzeugen weder neue Generatoren noch neue Netzknoten, Stromleitungen oder Netzaggregate. MA-2 arbeitet `renewable_cf(time, existing_generator_id)`; MA-3 liefert `hydro_inflow.csv`, `ror_availability.csv`, `store_link_staged.csv` und Energie-Ledger. Die **tatsächliche Invarianz am M0-Netz** muss jedoch erst der Composer beweisen.
2. **Räumliche Quelltreue:** MA-2 prüft PECD-Version/HASH, Profil-ID, M0-Generator-ID, offshore Landfall, Geo-Quality, offiziell referenzierte Gebietsmasken, Wind-PEON/P2ON/PEOF/P2OF und PV-ORIG/Regional; kann bestehende Generatoren mit MW-gewichteten Profilen beliefern. Die verwendeten *synthetischen* Masken/Zuordnungen belegen noch keine reale Source-Geometrie. Quellauflösung bleibt unabhängig von der elektrischen Knotenauflösung.
3. **PV-Semantik:** MA-2 verlangt explizite DC-MWp- und AC-MW-Basen inklusive genehmigter Clipping-Annahme, blockiert sonst. Diese Modellierung ist eine dokumentierte Möglichkeit, **keine nachgewiesene allgemein gültige PECD→M0-Anlagenumrechnung**.
4. **Hydrologische Physik:** MA-3 hält Quell-MWh und in das Modell umgerechnete Energie getrennt; native Intervalle, Rand-/DST-/Leapstunden, HRR/HRI/HPI/HOL/HCL, echte Nulleingänge und Store-/Link-Port-Autorität werden getrennt getestet. **Energieerhaltung** gilt in den Fixtures, noch nicht auf echten Einzugsgebieten.
5. **Provenienz:** Beide Adapter schreiben Hash-/Source-/Assignment-/Energy-Audits und lehnen automatische Wetterjahr-Fallbacks, erfundene Nullwerte und unbestätigte räumliche Zuordnung ab.
6. **Branch-/Scope-Disziplin:** Kein Producer hat M0-/M2-Topologie oder die Dateien des anderen Produktivmoduls geändert. MA-1C liefert eine konsolidierte Quell-/M0-Evidenzliste statt Mikroschleifen.

## 3. Gemeinsame Blocker und präzise Integrationsbefunde

| ID | Kategorie | Befund / Konsequenz | Priorität | Owner |
|---|---|---|---|---|
| **B-01** | REAL DATA | Die **fünf extern bereits ausgewählten Wetter-IDs** sind in den zugänglichen Projektdateien nicht identifiziert, keine vollständig gehashten physischen PECD-/Hydro-/ggf. DFT-Sets für alle fünf. TYNDP-2026-Standard je Horizont nur drei befüllte WS; niemals 3→5 simulieren | **P0 für Real** | Data Owner / MA1C Follow-up |
| **B-02** | M0 | Es gibt **kein ausgeführtes reales `DetailedNetworkReference v1`** inkl. Sidecar/Identity, Standortqualität, Generator-/Hydro-ID-/Bus-/Port-Witness. M0-S-GOV-Freeze (Branch `b1e284...`) ist ausschließlich dokumentarisch; M4-0 Preflight `ba55e4...` ebenfalls keine Runtime-Freigabe | **P0 für Real** | M0 Owner |
| **B-03** | Hydro spatial | Kein nachgewiesener hydrologischer Basin-/TSO→Anlage-Anteil und keine realen nativen Intervallquellen inkl. Wirkungsgrad-/Store-Port-Semantik | **P0 für Real** | Hydro/Data Owner |
| **B-04** | RES spatial | Keine tatsächlich geprüften PECD-Masken/Profil-Bytes/Original Offshore-Anlagenstandorte/PV-MWp↔AC-MW | **P0 für Real** | PECD/Data Owner |
| **I-01** | M0 schema | Beide Adapter verwenden den älteren Schlüssel `network_revision_id`; M0-Reparaturvertrag CAN/2.0.0/DNR/1.0.0 unterscheidet `source_revision_id`, `operating_state_id`, `canonical_revision_id`, `projection_id`. **Versionierter Identity-/Revision-Bridge** muss vor Realmodus entwickelt/abgenommen werden; keine stillen Umbenennungen | **P1 vor Integration** | M1 Integrator mit M0 |
| **I-02** | Schemas | MA-2: separates JSON-Weather-Manifest, Source-Catalog, NetCDF CF; MA-3: anderes Manifest-`contract`/`source_mode`, `assets`, `allocations`, CSV/Inflow/QA. Benötigt **gemeinsames Master-Manifest** und geprüfte Adapter-Normalisierung, keine unkoordinierte Anpassung an ein Producer-Format | **P1 vor Integration** | M1 Integrator |
| **I-03** | Write policy | MA-2 RES-CF → `generators_t.p_max_pu`, MA-3 RoR → ebenfalls `generators_t.p_max_pu`, Speicher → `storage_units_t.inflow`, Store-/Link staged **nicht** freigegebenes `generators_t.p_set`. **Ein gemeinsamer Target-Ownership-/Conflict-Ledger** mit eindeutiger Generatorpartition erforderlich | **P1 vor Integration** | M1 Integrator |
| **I-04** | Package/CI | Beide Branches legen `scripts/iosn_m1/__init__.py` **mit unterschiedlichem Inhalt** neu an; MA-2 legt auch `scripts/__init__.py` an. Kombinierter Branch benötigt explizite Konfliktauflösung, Dependency-BOM und gemeinsame CI-Matrix. MA-2 wurde Python 3.13 ohne PyPSA/Snakemake lokal getestet; MA-3 GitHub Actions Python 3.11/pytest. `pyproject.toml` der Basis listet xarray/shapely/pyproj/Snakemake nicht als M1-Integrationsrequirements | **P1 vor Integration** | M1 Integrator |
| **I-05** | Runtime | Keine tatsächlichen Snakemake-Regeln beider Teiladapter zusammen gelaufen; kein NetCDF PyPSA-Composer, keine Referenznetz-Invarianz, kein M0-Source-Roundtrip, keine 5-Sets-E2E-Kampagne | **P1 für Fixture, P0 für Real** | M1 Integrator / Reviewer |
| **I-06** | Input scope | DFT-/Last-Quellen sind noch kein Implementierungsrücklauf. Der Composer muss festlegen: **bereits von M0 zulässig stündlich befülltes `loads_t.p_set` unverändert**, oder gesondert autorisierte Quellzuordnung `Load ID→Demand`. Keine scheinbare „vollständige Referenz mit Lasten“ ohne echten Lastzeitreihen-Witness | **P1 vor M2-Handoff** | M1 Lead / Demand Owner |

**Zusammenführbarkeit:** Codepfade überwiegend getrennt; aus Git-Compare zur gemeinsamen Basis `2c0b482...`: MA1C **1 Commit/12 Dateien**, MA2 **13 Commits/17 Dateien**, MA3 **30 Commits/20 Dateien**, jeweils **0 Commits hinter Basis**. **Nicht** unkontrolliert `main` mergen: erstmal isolierter MA4-F-Integratorbranch; `scripts/iosn_m1/__init__.py` und Schemas/Deps bewusst abstimmen. MA-3 PR #7 bleibt Draft. MA-2 hat zum Prüfzeitpunkt keinen PR im Repository, aber veröffentlichten Branch.

## 4. Modulgrenzen und verbindliche Architekturentscheidung

- M0 liefert ein versioniertes `DetailedNetworkReference`-/Sidecar-Paket. **M0-Originalnetz und technische Stammdaten sind unveränderlich.**
- M1 integriert nur dynamische, quellentreu zugeordnete Daten an **vorhandenen** Generator-/Load-/StorageUnit-/Store-Port-IDs, mit strengem Target-Ownership-Ledger.
- Ein wetterseitig regionales PECD-Windprofil darf mehreren unterschiedlichen elektrischen Generatoren zugewiesen werden; das ist **keine Netzaggregation**, darf aber nicht als standortgenaue Wetterauflösung bezeichnet werden.
- Ein TYNDP-/PECD-Hydrogebiet ist **nicht** der elektrische Originalbus oder ein Ersatz für den hydrologischen Anlagenort.
- **MA4 Composer soll erst Snapshot-Index, Target-Key und Vorhanden-Profil-Overwrite prüfen und dann dynamische Whitelist-Attribute schreiben**; ausschließlich der Composer darf PyPSA-Netze materialisieren.
- Alle fünf extern festgelegten Weather-IDs werden **unverändert** verwendet; kein neues Ranking, keine neue Jahresauswahl oder Stundenreduktion.
- Eine bereits bestandene Syntax-/Fixture-/NetCDF-Readerprüfung ist **nicht** Real-Input-, Snakemake- oder elektrische Netzqualifikation.
- Kein Beginn einer M2-Netzaggregation auf Basis ungeprüfter M1-Inputnetze.

## 5. Governance-Freigaben und nächste Makros

**Freigabe A — `M1-MA4F` FIXTURE INTEGRATION & INTERFACE RECONCILIATION: JETZT, NEUER INTEGRATIONSCHAT.** Als ein Makro beide Adapter auf einem eigenen Branch mit korrektem DNR-Bridge, Master-Manifest, eindeutigen Schreibrechten, reproduzierbarer BOM und echtem gemeinsamen PyPSA-/Snakemake-Fixture-Netz integrieren; positive und negative E2E-Tests, NetCDF-Roundtrip, vollständige Statik-Fingerprints. Dieser Macro darf `MA4_FIXTURE_INTEGRATION_QUALIFIED` ausgeben, **aber niemals** `REAL_DATA_READY` ohne G1C/D/E.

**Freigabe B — `M1-MD1` PHYSICAL DATA & M0 RUN-RELEASE WITNESS: PARALLEL, DATA-/M0-OWNER.** Genau **ein** gebündeltes Paket gemäß MA1C `OPEN_INPUTS_AND_EXIT_CRITERIA.md` (IN-01…IN-10) mit fünf bereits gewählten IDs/Horizonten, echten PECD-/Hydro-/DFT-Dateien, Rechte/Hashes, Regionengeometrie, Plant-Geo/PV-MWp/AC, Basin-/TSO-Anteilen und M0-DNR-Paket. M0-Betriebsfreigabe/PoC bleibt separate M0-Governance; kein Ersatz durch M1. Ein Reviewer prüft Bytes und Gates G1-C/D/E, gibt `M1_SOURCE_CONTRACT_WITNESSED` oder `BLOCKED` aus. Bei Inputmangel nur Report, **kein wiederholtes Auftragskarussell**.

**Freigabe C — `M1-MA4R` FULL REAL-SOURCE CAMPAIGN + FINAL ACCEPTANCE: NACH A UND B.** Ein gemeinsames, versioniert gepinntes M0-/MA2-/MA3-/DFT-Paket, fünf Wetterdatensätze pro tatsächlich erforderlichem Horizont, räumliche und zeitliche Profilzuordnung, realer NetCDF-/Statik-/MWh-/CF-/Coverage-Witness. Danach **separater unabhängiger R-M1-MA4 Reviewer** am endgültigen Producer-SHA. Nur mit Reviewer-PASS und S-GOV-M1-Freigabe `M1_DETAILED_REFERENCE_READY_FOR_M2` behaupten.

**M0-Vorbedingung:** M0 `ARCHITECTURE_FROZEN_FOR_IMPLEMENTATION_PLANNING` und `M4_0_STATIC_PREFLIGHT_COMPLETE` sind **keine** echten CGMES-PyPSA-Netze. M0-Realisierung/Release wird vom M0-Owner separat entschieden, nicht vom MA4F-Worker. Zeitreihen-Integrationsfixture darf M0-DNR mit synthetischem Sidecar testen, muss aber dessen nicht reale Evidenzklasse beibehalten.

**Aktuelle S-GOV-Klassifikation:** `M1_PARALLEL_MACROS_DELIVERED__FIXTURE_LEVEL_PARTIAL_PASS__PHYSICAL_SOURCE_BLOCKED`. Keine Freigabe des Real-Data-MA4R, keine M2-Übergabe, kein Merge von Draft-PR #6/#7 als Produktiv-PASS.
