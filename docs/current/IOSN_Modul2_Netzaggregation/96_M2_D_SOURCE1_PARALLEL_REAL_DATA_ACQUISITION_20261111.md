# M2-D-SOURCE1 — Parallel Reference Grid/Data Acquisition & Qualification Macro

**Projekt:** AlOussama/TYNDP_Products. **Rolle:** unabhängiger Grid Data Lead; vier getrennte Worker D0–D3 mit später separatem R-DATA (D4). **Status:** sofort ausführbar für Quellenzugriff, Provenienz und zulässige Testwitnesses; kein Realnetz-PASS vor tatsächlicher Datenqualifikation.

## 1. Verbindliche Quellen

- [D-REAL Quelleninventar 88](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/88_M2_D_REAL_SOURCE_INVENTORY_2026_11_11.md)
- [D-REAL Gap-/DR01–DR17-Katalog 89](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/89_M2_D_REAL_GAP_GATES_AND_WITNESS_2026_11_11.md)
- [Readiness 90](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/90_M2_D_REAL_READINESS_MATRIX_2026_11_11.json)
- [Originale D0–D4-Handoffs 92](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/92_M2_D_REAL_ACQUISITION_HANDOFFS_2026_11_11.md)
- [MA1 PR #13](https://github.com/AlOussama/TYNDP_Products/pull/13), [MA2 Vertrag 85](85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md)

## 2. Ausführung (parallel)

**D0 — TSO Starting Grid/Provenance:** Ermittele und beantrage nur lizenzkonform die echten versionierten 2025 AC/DC-Detailnetzdaten und autorisierten IoSN-2035-Startnetzänderungen; Geräte-/Branch-IDs, Base, Trafos/PST/HVDC, 110-kV-Ties, Limits und Owner-Rechte. Nicht behaupten, ein Szenario-Download sei das TSO-Detailnetz. Ergebnis: `source_manifest.json` (Originalbytes SHA-256), `topology_check.json`, Gerätefähigkeit, nötige Access-Requests. Gate `SOURCE_BYTES_VERIFIED` oder `BLOCKED`.

**D1 — Offener Real-Topologiepilot:** Recherchiere/ladet eine explizit gepinnte öffentlich lizenzierte PyPSA-Eur OSM-v0.6-Basis oder gleichwertige reale Topologie, prüfe Originalbytes/Hashes/Lizenz, extrahiere kleinstes geeignetes zweiländriges **AC-gekoppeltes vermaschtes** Teilnetz mit echten IDs/Units und Geräte-/Topologie-Inventar. Test nur physikalische Topologie und gegebenenfalls Parameter auf Model 2-Input. Keine erfundenen Marktflüsse/5 Jahre. Gate `PARTIAL_REAL_TOPOLOGY_WITNESS` oder `BLOCKED`, nicht `REAL_IOSN`.

**D2 — Dispatch/neutraler Kalibrierzustand/Zeit:** Hole vom zuständigen Owner die exakt fünf bereits festgelegten Wetterjahr-IDs, echten UTC-Snapshots, Stundenlängen, saisonale Zuordnung und getrennt belegte nodale Dispatch-/HVDC-/PST-/Asset-MW-Bilanzen mit originalem physischem Flussoracle. Erzeuge nur einen **eigenen physikalisch bilanzierten** HVDC=0/PST=neutral-Kalibrierzustand, kein simples Control-Zero ohne korrekte Redispatchbilanz. Gate `OPERATIONAL_AND_NEUTRAL_BALANCED` oder `BLOCKED`.

**D3 — Kontingenzen/TSO-Exceptions:** Erlange autorisierte LODF/N-1-Monitore/Outages, Sommer-/Winter- und Normal-/Notfalllimits und explizite TSO-Ausnahmen. Unterlasse die Gleichsetzung von 99,5%/1%/130%-Methodik-Sonderfällen mit TSO-Exemptions. Gate `VALIDATED_SECURITY_DATA` oder `BLOCKED`.

Vier Worker dürfen parallel arbeiten, da sie unterschiedliche Quellen beschaffen. D1 ist nicht von vertraulichen D0-Quellen abhängig. Quellen- und Lizenzgrenzen explizit respektieren. Lokale, untracked, private, Cloud- oder TSO-Daten sind **nicht** aus GitHub-Abwesenheit als nicht existent zu behaupten; aber konkrete Originalbytes müssen für jedes Gate tatsächlich eingesehen/gehasht werden.

## 3. Integration und unabhängige Gate-Validierung

Mapping auf die M2-Verträge `DetailedGridSnapshot`, `CountryZoneBudget`, `TimeSet`, `ReferenceDispatchSet`, `NormalContingencyRatings`, vorgeschlagenes `SecurityData`. Führe die 17 DR-Prüfungen aus; prüfe Originalbytes-Hash, IDs, Country NI/UK, AC-/HVDC-Semantik, Einheiten, Zeit-/Islands-Balance, Rating-/Security-Scope, Neutralfälle. Fehlende Felder `BLOCKED_DATA`.

D4 — **unabhängiger** R-DATA erhält die fixierten Original-Inputmanifeste erst nach D0–D3; eigener SHA/Quellenzugriff/Run/Re-Review, Status nur `REAL_TOPOLOGY_ONLY`, `REAL_MA1_WITNESS`, `REAL_MA2_CALIBRATION_WITNESS`, `REAL_MA3_SECURITY_WITNESS` oder `BLOCKED` mit Scope. D4 darf Proxies nicht zum TSO-validierten Status hochstufen.

## 4. Liefergegenstände und Verbotene Operationen

Einziger konsolidierter Datenstatusbericht, D0–D3 Subreports, original SHA-/Lizenz-/Accessmanifeste, Parser-/Einheitenledger, getestete Source-Checks, Geräte-/Country-/Zeit-/N-1-Gaps, expliziter R-DATA-Folgehandoff. Schreib nur **nicht vertrauliche** Manifeste auf einen neuen Dokumentationsbranch; restricted Rohdateien nie in öffentliches Git, keine Credential-Links. Kein M0-/CGMES-Parser, kein M1-/PECD-Reader, keine Wetterjahrwahl, kein PR-13-Merge, kein MA2-/MA3-Runtime-GO.
