# R-M2-API – Independent MA1 Implementation and Interface Reconciliation

**Projekt:** AlOussama/TYNDP_Products  
**Review-Datum:** 2026-11-11  
**Rolle:** unabhängiger wissenschaftlich-technischer Software-Architekturreviewer  
**Entscheidung:** **RECOMMEND_A_CANONICAL_WITH_LIMITED_ADAPTER / OWNER_GATE_REQUIRED**  
**Qualifikation:** **INDEPENDENT_SYNTHETIC_API_REPLAY_PASS / REAL_DATA_NOT_QUALIFIED / MA2_NOT_AUTHORIZED**  
**Charakter:** Architektur-, Datenvertrags- und Kompatibilitätsreview; keine MA2-Implementierung und keine automatische Merge-Freigabe.

## 1. Prüfgegenstände, Identität und Unabhängigkeit

| Kennzeichen | Verbindlicher Commit | Quellort | Status bei Review |
|---|---|---|---|
| A | [70e92ba9e62a320e58227ce9c2f03fad266f44bf](https://github.com/AlOussama/TYNDP_Products/commit/70e92ba9e62a320e58227ce9c2f03fad266f44bf) | src/tyndp_reduce/iosn_official; tests/iosn_official | PR #13 offen; MA1-Code umgesetzt |
| B | [88374dd38792146ca55fa3fe2d4b35dac842c0b9](https://github.com/AlOussama/TYNDP_Products/commit/88374dd38792146ca55fa3fe2d4b35dac842c0b9) | src/tyndp_reduce/m2; tests/test_m2_* | Alternative separat; nicht gemergt |
| MA2-Ziel | [Dokument 85](85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md) | globales x/c0; affine KVL; gekoppelte Länder-Suche; MA3-Handoff | Technische Zieldefinition, keine Owner-Freigabe |
| Review-Ausführung | [418b8ba8b71afdd5808ada87fcb6fb981a3cc5e2](https://github.com/AlOussama/TYNDP_Products/commit/418b8ba8b71afdd5808ada87fcb6fb981a3cc5e2) | review/iosn-m2-r-api-20261111 | getrennte Testinstanz auf beiden unveränderten Quellständen |

**Quellintegrität:** Git-Blob-Vergleich des Testbranches mit beiden Originalcommits: 14/14 A-Code- und A-Testdateien unverändert, 11/11 kopierte B-Code-/Testdateien byteidentisch (Git-Blob-SHA identisch). Die B-Kopie dient **nur** als isolierter Review-Testträger, nicht als Integrationsfreigabe oder Produktionsimport. Beide ursprünglichen Branches, main sowie M0/M1/Wetterjahrauswahl sind unverändert.

**Methodikstatus:** Ausgangspunkt ist die ENTSO-E-Konsultationsfassung zur IoSN-Methodik vom 25.02.2026, veröffentlicht zur Konsultation am 26.02.2026; es wird weder ein veröffentlichter proprietärer Solver noch eine offizielle Reproduktion von Clustering oder Optimierung behauptet. Siehe [ENTSO-E-Konsultationshinweis](https://www.entsoe.eu/news/2026/02/26/entso-e-releases-public-consultation-on-the-system-needs-methodology/) und den projektspezifischen Methodikabgleich 80/81/85.

**Review-Grenzen:** Keine vollständigen europäischen Original-Lastflussstunden, keine reale verlustbehaftete Gerätequalifikation, kein externer PyPSA-Realnetzvergleich, keine MA2-x/c0-Implementierung. Die bei Erstellung von Dokument 82/83/84 bestehenden R-PHY-/R-CLU-Gates sind hier nicht automatisch aufgehoben.

## 2. Vergleichsmatrix auf Datei- und Funktionsebene

Die Links sind durch die exakten SHAs eingefroren: [A-Dateibaum](https://github.com/AlOussama/TYNDP_Products/tree/70e92ba9e62a320e58227ce9c2f03fad266f44bf/src/tyndp_reduce/iosn_official), [B-Dateibaum](https://github.com/AlOussama/TYNDP_Products/tree/88374dd38792146ca55fa3fe2d4b35dac842c0b9/src/tyndp_reduce/m2).

| Thema | A-Datei/Funktion | B-Datei/Funktion | Klassifikation und MA2-Folge |
|---|---|---|---|
| Domänenverträge | contracts.py: Provenance, ACBranch, HVDCTerminals, DetailedGridSnapshot, TimeSet, ReferenceDispatchSet, NormalContingencyRatings | contracts.py: Evidence, Bus, ACBranch, HVDCTerminalPair, TimePoint, TimeSet, HVDCDispatch, PSTDispatch, ReferenceDispatchSet, Ratings | **Nicht binär/API-kompatibel**; B hat explizite Bus- und Terminalobjekte, A native Matrix-/Schedule-Eingaben und strikte UTC-/Fünf-Jahre-Regeln |
| Vorprüfung | preflight.py: preflight, PreflightLedger.require_pass | preflight.py: preflight_ledger, save_ledger_once | **Fachlich ähnlich, andere Ergebnis- und Fehlerverträge**; A liefert typisiertes Ledger, B JSON-Dict, B benötigt realen beobachteten AC-Flow-Witness |
| Referenzphysik | physical.py: ac_topology, reference_flows | physical.py: SparseACReference.__init__/solve, ReferenceFlowCache.payload/write_once | **Gleichwertiger gemeinsamer lossless-DC-Kern in Prüffällen**; A berechnet vollständige Arrays und NPZ, B einmalige Faktorobjekt-Haltung und JSON-Cache |
| HVDC | contracts.HVDCTerminals + physical.reference_flows | contracts.HVDCTerminalPair/HVDCDispatch + SparseACReference.solve | **Nicht verlustsemantisch gleich**; A nur symmetrischer, verlustloser Transfer; B separate p0/p1 inkl. p0+p1 kleiner/gleich 0 |
| PST/Trafo | ACBranch.phase_shift_rad + pst_phase_rad-Schedule | PSTDispatch; ACBranch.tap_ratio-Guard | **Teilweise inkompatibel**; A erlaubt feste Trafo-Winkeloffsets, B nicht; B weist nicht-einheitlichen Trafo-Tap explizit ab |
| Länder | country.py: load_official_country_budget, resolve_country_ids, validate_country_feasibility, validate_busmap | country.py: load_official_budget, validate_country_feasibility, assert_country_zones | **Konvertierbar mit expliziter Country-Normalisierung**; beide 37/102 und NI/UK separat, A verlangt injektive Raw-ID→Original-Label-Abbildung |
| Screening | screen.py: screen_annual_overload, weighted_edge_costs | screening.py: screen_annual_overload, protect_congested_union | **Abweichende Eligibility/Policies**: A explizite 225/400-Screeningklasse einschließlich 380→400, B nur nominal exakt 225 oder 400 |
| Erstcluster | seed.py: quota_seed, SeedResult | country.py: country_quota_busmap | **Nicht algorithmisch identisch**; A kumuliert nach Kontraktion Grenzkosten dynamisch, B verwendet statische Kruskal-Kantenrangfolge |
| Zonenoperatoren | operators.py: build_oriented_projection, OrientedProjection.verify/aggregate/counterflow_ledger | projection.py: build_oriented_projection, OrientedProjection.verify/counterflow_diagnostic | **Physisch äquivalente Identität**, inkompatible Typ-/ID-Schemata; A liefert zusätzlich A_d, namentliche Zonen/Schnitte und Branch-/Bus-IDs |
| Pipeline | ma1.py: execute_ma1, MA1Result.export | Kein allgemeiner execute_ma1-Orchestrator; Komposition in fixture_witness.generate | **A deutlich näher am dokumentierten MA2-Eingangsvertrag**; B benötigt einen Produktions-Orchestrator, vollständiges Manifest und numerischen Exportadapter |
| Reproduzierbarkeit | fixture_evidence.py, 15 MA1-Dateien mit NPZ/CSV/JSON/Manifest, Code- und Input-SHA | fixture_witness.py, sechs JSON-Dateien, Hash-/Write-once-Mechanik | **Beide synthetisch reproduzierbar, Output inkompatibel**; B-Checksum-/Write-once-Konzept nutzbar, A numerisch sparsamer |
| Testabdeckung | tests/iosn_official/test_ma1_physical, clustering, integration, fixture_evidence | tests/test_m2_physical, country, witness | **Komplementär**; A komplette Pipeline/Export, B u.a. großer Chain-/Country-Test und negative Terminalfälle |

Gemeinsame korrekte Grundlagen in den geprüften Fällen: gerichtete Inzidenz A_d, f = diag(Sbase/x)(A_d^T theta - phi), A_d f = p_net, separate Referenzwinkel und MW-Bilanz je tatsächlich elektrischer AC-Insel, HVDC niemals als passiver AC-Zweig, länderreine verbundene Zonen und A_z Gamma = P A_d. Ein solcher Kurzschluss auf gleichem DC-Sonderfall beweist **keine** Gleichwertigkeit für abweichende Gerätesemantik.

## 3. Reproduzierbare unabhängige Tests

**Prüflauf:** [GitHub Actions 43078255397](https://github.com/AlOussama/TYNDP_Products/actions/runs/43078255397), Job parity, SHA 418b8ba8b71afdd5808ada87fcb6fb981a3cc5e2. Status SUCCESS.

| Test | Ergebnis | Begründung |
|---|---|---|
| Unabhängiges 3-Bus-Dreieck mit PST und Dense-Oracle | A=B=Dense, max. Abweichung gegen Dense in Runner 0 MW | Gemeinsame Vorzeichen-/PST- und Maschensemantik |
| Zwei AC-Inseln, HVDC-Brücke | A=B; 20/10/15 MW | Kein unsichtbarer Country-/Global-Slack |
| Drei elektrisch gekoppelte Länder, harte Quote, Projektion | A=B, Zonenschnitte 5/10 MW | Quoten und orientierte KCL kompatibel |
| Island-Imbalance | Beide weisen zurück | Fail-closed ohne künstliche Bilanzkompensation |
| 380-kV-Branch mit expliziter 400-kV-Klasse | A inkludiert; B lässt Branch ohne Fehler weg | **Bestätigter Screening-Vertragsunterschied** |
| Nichtmonotone fünf UTC-Snapshots | A weist zurück; B akzeptiert | **Bestätigter Zeitachsen-Vertragsunterschied** |
| Nicht-synthetischer Fall ohne beobachtete AC-Flüsse | A berechnet; B verweigert | **Bestätigter Qualifikations-Gate-Unterschied** |
| HVDC mit 1 MW Verlust (p0=-10, p1=+9) | B kann getrennte Terminalwirkungen; A weist lossy-Gerät zurück | **Bestätigter Physik-Umfangunterschied**, nicht Qualitätsentscheidung |
| Feste Trafo-Phasenverschiebung | A-Vertrag akzeptiert; B-Vertrag kennt Feld nicht | **Bestätigter Modellkonflikt** |
| Vermaschter 4-Bus/K4 mit gleichen Detailflüssen, gleichen Landquoten und Original-Edge-Weights | A bildet {v0,v1}/{v2,v3}: Zonenschnitt 10 MW; B bildet {v0,v1,v2}/{v3}: 5 MW | **Zwei zulässige, aber verschiedene Heuristiken**; MA2 muss Schnittliste/Zielwerte pro Kandidat konsistent neu berechnen |
| Sparse-Kette, 500 Busse/499 Branches, fünf Snapshots | A=B innerhalb 1e-8 MW | Kein Dichte-Inverse-Pfad im gemeinsamen Prüffall; **kein** europäischer Skalennachweis |

**Neue unabhängige Tests: 11/11 PASS. Bestehende vollständige A- und B-spezifische Regressionen auf byteidentischen Quellständen: 58/58 PASS.** Beide ursprünglichen CLI-Fixture-Erzeuger PASS. Vorheriger Teststand: [Run 43077732881](https://github.com/AlOussama/TYNDP_Products/actions/runs/43077732881) mit 9/9 + 58/58.

500-Bus-Laufdiagnose auf einem gemeinsamen GitHub-Linuxrunner, nur illustrativ: A ca. 2,644 ms, B ca. 9,921 ms; die zwei A-Arrays f/p zusammen 39.960 Bytes, der B-JSON-Cache 80.453 Bytes. Sie enthalten nicht genau denselben Metadatenumfang. Kein belastbarer Laufzeitvorteil für Europa, keine Performance-SLA und keine Hochrechnung aus einer Einzelmessung.

**Repro im freigegebenen isolierten Review-Branch:**

~~~sh
git checkout review/iosn-m2-r-api-20261111
python -m pip install -e ".[test]"
python -m pytest -vv -s tests/review/test_r_m2_api_parity.py
python -m pytest -q tests/iosn_official tests/test_m2_country.py tests/test_m2_physical.py tests/test_m2_witness.py
python -m tyndp_reduce.iosn_official.fixture_evidence --output /tmp/r-api-a-repro --commit 418b8ba8b71afdd5808ada87fcb6fb981a3cc5e2
python -m tyndp_reduce.m2.fixture_witness --output /tmp/r-api-b-repro
~~~

Verzeichnisse für die Fixture-Erzeuger müssen neu sein. Testkopien der B-Implementierung liegen **nur auf dem Review-Branch**. Prüfscript: [tests/review/test_r_m2_api_parity.py](https://github.com/AlOussama/TYNDP_Products/blob/418b8ba8b71afdd5808ada87fcb6fb981a3cc5e2/tests/review/test_r_m2_api_parity.py).

## 4. Kompatibilitäts- und Finding-Register

| ID / Priorität | Nachweis und Risiko | Maßnahme/Status |
|---|---|---|
| R-API-P1-01 | **B: 380-kV-Nennspannung beim Screening still ausgelassen**, obwohl eine explizite 400-kV-Klassifikation fachlich erforderlich sein kann; Grenz-/Cluster-Risiko | **REPRODUCED**; A-Screeningklasse kanonisch; B-Adapter nur mit explizitem Mapping oder harter Abweisung |
| R-API-P1-02 | **Zeitachsen:** A strenges UTC/Sortierung/fünf IDs, B für Fixture verkürzt und ohne strikten chronologischen Check | **REPRODUCED**; MA2 benötigt streng monotonisierte, im Eingangsmanifest eingefrorene originale Zeitachse, kein stilles Sortieren |
| R-API-P1-03 | **HVDC-Losses:** B p0/p1 asymmetrisch, A nur verlustlos; direkte Umkodierung verändert Netzeinspeisungen | **REPRODUCED**; lossless als gemeinsames Pflichtprofil; lossy nur nach separatem Semantik-, Leistungsbilanz- und Source-Gate |
| R-API-P1-04 | **Feste Trafo-Phase:** A hat phase_shift_rad; B keinen entsprechenden Parameter | **REPRODUCED**; B-Konverter muss ablehnen oder explizit mit validierter Gleichung erweitert werden |
| R-API-P1-05 | **Observed-flow-Witness:** B fordert für Nicht-Fixtures exakte Nähe der beobachteten AC-Ströme zur verlustlosen DC-Rechnung (1e-6 MW); A nicht | **REPRODUCED**; unabhängige beobachtete Flüsse als getrennte Qualitätsdiagnose, niemals unkommentiert als DC-Identität fordern; reale Kalibrierung bleibt offen |
| R-API-P1-06 | **Andere Clustering-Heuristik bei gleichen Kosten:** K4-Zonenschnitt 10 vs. 5 MW; RMSE auf wechselnder Linkmenge nicht ohne feste Monitore vergleichbar | **REPRODUCED**; Candidate-Version, vollständiger globaler Refit und konsistente Monitor-Metrik verpflichtend; beide Greedy-Heuristiken sind nur Seeds |
| R-API-P1-07 | **Critical-line-Protection:** A execute_ma1 hat optionales protected_line_ids=(); B schützt in der Fixture automatische Union aus Jahresüberlastungen, aber ohne allgemein verfügbaren Orchestrator | **STATIC_FINDING**; vor produktiver MA2-Nutzung festgelegte Schutzpolicy und Ledger als Pflicht-Preflight; keine stillschweigende Null-Protection |
| R-API-P1-08 | **Europaweite Memory/IO:** Beide materialisieren LxT- und NxT-Matrizen; B zusätzlich JSON-Listen; A speichert ein NPZ-Gesamtobjekt | **DESIGN_RISK**; Speicherbudget, Block-/Stream- und Sparse-Replay-Gate vor Realnetz; 500-Bus-Test ist kein Nachweis |
| R-API-P1-09 | **Trafo-Tap-Provenienz:** B lehnt tap_ratio !=1 ab; A akzeptiert nur bereits normierte Ersatz-x und hat keinen Tap-Feldeingang | **STATIC_FINDING**; Originalgerät-/Normierungsnachweis beim Upstream-Vertrag oder fail closed |
| R-API-P2-01 | **Zonenschlüssel:** A namentliche Country::NNN, B ganze 0..Z-1-Indizes; gleiche Zonennummer bedeutet keine gleiche Physik | **STATIC_FINDING**; stabile kanonische Label-/Orientierungs- und ZonePair-Konversion, eindeutige Shape-/Source-Hashes |
| R-API-P2-02 | **Output:** A 15 Artefakte (inkl. NPZ/CSV), B sechs JSON; nicht kompatibel | **STATIC_FINDING**; A Export als MA2-Eingang, B Cache-Check und Write-once-Konzepte selektiv übernehmen |
| R-API-P2-03 | **Export-Atomizität:** A exportiert in neue Directory, schreibt jedoch mehrere Dateien sequenziell; Fehler kann partiellen Ordner hinterlassen. B schützt einzelne Dateien mit open(x), nicht komplette Run-Transaktion | **STATIC_FINDING**; staging-directory, manifestierte Hashprüfung, erst dann atomic rename/READY-Marker |
| R-API-P2-04 | **Country-ID-Normalisierung:** A fordert injektive Raw-ID-Mapping-Relation, B erwartet bereits kanonische Country-Labels | **STATIC_FINDING**; upstream explizites Mapping mit NI/UK-Unterscheidung; dokumentierte Aliasfälle separat entscheiden |
| R-API-P2-05 | **Topology in_service:** A kann inaktive AC-Zweige speichern und beim Solve filtern; B lehnt inaktive ACBranch ab | **STATIC_FINDING**; kein implizites Entfernen aus Input-Fingerprint; aktiven Topologiestand versionieren |
| R-API-P2-06 | **Wiederholte Referenzrechnung:** A-Preflight ruft reference_flows und execute_ma1 anschließend erneut auf; B hält SparseACReference-Faktoren in einem Objekt | **STATIC_FINDING**; Cache/Faktor-Reuse innerhalb A-Pipeline möglich, ohne externen Contract zu brechen |
| R-API-P2-07 | **Metadaten:** B Evidence.target_year und signierte JSON-Content-Hashes; A erweiterte Provenienz, expliziten Code- und Rating-Content-Hash | **KOMPLEMENTÄR**; beides im kanonischen versionierten MA2-Manifest referenzieren |

**Schweregrad:** P1 = vor Vertragseinfrieren und Start einer unkontrollierten MA2-Implementierung zu entscheiden oder mit validiertem Gate abzuschirmen; P2 = dokumentierter Adapter-/Qualifizierungsbedarf. Kein aktueller Beleg für numerisch falsche gemeinsame DC-Gleichungen in den elf geprüften Fällen. Zugleich keine Freigabe des Realnetzbetriebs.

## 5. Optionenentscheidung

| Kriterium | Option A – iosn_official kanonisch | Option B – m2 kanonisch | Option C – A-Kanonik plus begrenzte Adapter |
|---|---|---|---|
| Bestehender Handoff 85 und MA2-Result-Vertrag | Direkt verwendbar | Handoff/Export erheblich zu revidieren | Direkt verwendbar; B nur gekapselt |
| Physikalisch gemeinsamer lossless DC-Kern | PASS im unabhängigen Test | PASS im unabhängigen Test | PASS im unabhängigen Test |
| Fünf fixe Jahre, UTC, 380-kV-Semantik | Günstigere Ausgangsbasis | P1-Reparaturen erforderlich | A als strenge Grenze |
| B-spezifische Vorteile | Keine direkte B-Funktion | Signed-HVDC, JSON-Checksum, Faktor-Reuse | Selektive Übernahme nach Gate |
| Komplettheit MA1→MA2 | execute_ma1 + typisierter Result + Export vorhanden | Produktions-Orchestrator und A-Export fehlen | A als verbindlicher MA2Input, B-Witness-Konverter optional |
| Risiko zweier konkurrierender Source-of-Truths | Gering | Hoch bei bestehendem Handoff 85 | Niedrig nur bei **einseitigem** und versioniertem Adapter |
| Grobe Engineering-Schätzung nur Interface-/Testmigration (keine Realnetz-, x/c0-, MA3-Arbeit) | 2–4 Personentage | 8–14 Personentage | 4–7 Personentage |

**Eindeutige Empfehlung: Option C mit A als alleiniger kanonischer MA2-API.** C bedeutet **nicht** eine Fusion beider Implementierungen. Eine dokumentierte, schmale B→A-Adapter-/QA-Grenze übernimmt nur nachweislich kompatible Fähigkeiten; B bleibt als unabhängiger numerischer Regressionsträger und für spätere Gerätenerweiterungen erhalten. Die naheliegende Alternative A ohne Adapter ist technisch ebenfalls vertretbar, verschenkt aber die geprüften positiven B-Witness- und Terminalideen. B als Kanonik würde für das vorliegende MA2-Ziel zusätzliche Änderungen an Datensemantik, Prüfprotokoll und Export erzwingen, ohne einen entsprechenden Vorteil für globalen x/c0-Fit oder gekoppelte Suche nachzuweisen.

Die angegebenen Aufwände sind **unsichere Schätzungen für die Schnittstellenreconciliation**, keine durchgemessenen Arbeitszeiten und keine Prognose für Realnetzskalierung.

## 6. Minimaler Integrations-/Migrationsplan

1. **Gate D-API (Owner):** A-C/canonical und MA2-Frozen-Input beschließen oder andere Option ausdrücklich wählen. Bis dahin keine MA2-Implementierungsfreigabe.
2. **A-API v1 einfrieren:** <code>execute_ma1</code>, <code>MA1Result</code>, <code>DetailedGridSnapshot</code>, <code>TimeSet</code>, <code>ReferenceFlowCache</code>, <code>OrientedProjection</code>, SHA- und Outputschema versionieren. Keine direkte Änderung der originalen A/B-Branches aus diesem Review.
3. **Dünner B→A-Konverter als separater optionaler Namespace:** exakt reindizierte Busse/Branches/Snapshots, geprüfte Source-SHA, UTC- und Fünf-Jahre-Vertrag, explizites Country-Label-Mapping, ZoneID-Konvertierung. Nur <code>tap_ratio=1</code>, verlustlose HVDC-Terminals <code>p0=-p1</code> und von A vollständig darstellbare PST/Trafo-Parameter zulassen. Bei realen lossy/unknown Devices zwingend <code>UNSUPPORTED_SEMANTICS</code> statt plausibilisiertem Ausgabefluss.
4. **Zusatz-QA ohne Wechsel der Kanonik:** B-JSON-Content-Hash/Write-once-Konzept als optionales Witness-/Audit-Modul; beobachtete AC-Flüsse nur getrennt mit definierter Toleranz und zugehöriger Source-Evidence, nicht als stiller Ersatz für den unabhängigen Referenzsolver.
5. **Schutz- und Exporthärtung:** Schutzpolicy explizit manifestieren, 225/400-Klassifizierung und 220/380-Provenienz prüfen, sämtliches Result inklusive normal/emergency-Rating-Content hash-binden; atomare, nicht überschreibbare Run-Publikation. Keine Breaking-API-Änderung am bisherigen execute_ma1 ohne separate Version.
6. **Länderkopplung/Skalierung:** vorher fixierter numerischer Speicher- und CPU-Test für mindestens eine große sparse, mehrinselige Fixture; Zeitblock-/Memorybudget für LxT vor MA2-Realnetz festlegen. A_d/P/Gamma/A_z pro Kandidat vollständig neu und mit G05 nachprüfen; Kontingenten und Country-Label-Zuordnungen nicht abkürzen.
7. **Re-Review und Handoff-Revision:** alle unabhängigen R-API-Testfälle plus R-PHY/R-CLU-Gates; erst danach angepassten Handoff 85 auf Owner-freigegebenem Branch publizieren. Kein Merge, keine automatische MA2-/MA3-Runtime- oder Realnetzfreigabe.

## 7. Verbindlicher vorgeschlagener MA2-Eingangsvertrag: M2.MA2Input.v1

**Eingang ist genau ein A-kompatibles, geprüftes und inhaltlich eingefrorenes MA1-Run-Manifest.** B-Objekte dürfen die Grenze nur über einen explizit versionierten validierenden Adapter passieren.

| Feld/Artefakt | Vertrag |
|---|---|
| **code_identity** | A-Implementierungs-SHA + API-Schema + optional B-Adapter-SHA und Source-Tree-Hashes; niemals beweglicher Branch als identitätsstiftender Code |
| **source_manifest** | Grid-SHA, Dispatch-/TimeSet-/Ratings-Content-SHA, CountryBudget-SHA, Country-Resolver-Ledger, Gerätedaten-/Base-MVA-/Unit-Provenienz |
| **original_graph** | Vollständiger globaler AC-Inzidenzgraph A_d, konsistente aktive Topologie, echte AC-Islands, HVDC nur signierte Terminalaktionen, keine Länder-Slacks |
| **five_year_time_axis** | Fünf externe eindeutige Wetterjahr-IDs unverändert, strenge UTC-Chronologie, Dauer/Season/Dispatch/Rating-Zeilen auf denselben Snapshots, versionierter Hash; kein Weather-Year-Resampling |
| **frozen_operational_reference** | Ein unveränderlicher ReferenceFlowCache MW (branch_ids, bus_ids, snapshot_ids, island IDs, f_detail, p_net) mit SHA und KCL-Witness; niemals pro Kandidat neu dispatchen |
| **neutral_calibration_input** | Separat gelieferter und gehashter neutraler Dispatch mit HVDC=0 und PST neutral, physikalisch AC-island-balanced; nicht aus operationalem Cache durch Nullstellen ohne Bilanzprüfung erzeugen |
| **country_quotas** | Original-37/102 nur für offiziell vollständige Geografie; NI und UK getrennt; synthetische Quoten als SYNTHETIC_BUDGET markiert; <code>k_c</code> für alle Kandidaten unveränderlich |
| **baseline_busmap** | Vollständige Country-pure, AC-connected, exact-quota SeedResult-Busmap; keine ungeschützte kritische AC-Leitung internalisieren; Dokumentation der Schutzpolicy |
| **candidate_projection** | Für **jeden** Kandidaten aus Originalnetz rebuild: P(z), Gamma(z), A_z(z), A_d und benannte sortierte ZonePairs, Orientierungs-/KCL-Test <code>A_z Gamma = P A_d</code>, <code>p_z=P p_detail</code>, <code>f_target=Gamma f_detail</code> |
| **calibration_contract** | Globale positive Ersatzreaktanzen <code>x_e>0</code>; für jede tatsächliche zonale AC-Island Gauge, Sparse-Solver ohne dichte Europa-Inverse, Rang-/Konditions-/Identifizierbarkeits-Witness, bei Bäumen/degenerierten Loops <code>UNIDENTIFIABLE</code> statt falscher x-Fits |
| **affine_c0_contract** | <code>f_eq(t)=H_eq(x)p_z(t)+c0</code>, <code>A_z c0=0</code> und **im implementierten reduzierten Simulationsmodell** <code>C^T diag(x)(f_eq(t)-c0)=0</code>; c0 nicht bloßer Plotoffset. Inselübergreifende DC-Verbindungen bleiben exogene Terminallasten |
| **frozen_splits** | Hashfixierter TRAIN/SELECTION/HOLDOUT-Blocksplit aus den fünf **bereits** gewählten Jahres-ID-/Stunden-Mengen; Fit TRAIN, Accept/Reject SELECTION, HOLDOUT nur abschließendes unabhängiges Replay |
| **objective_monitoring** | Fixe, topologieunabhängig definierte Monitorgruppen und Vergleichsmetriken vor Suchstart; Linkzahl/Schnittlistenwechsel kennzeichnen; MW-RMSE, MAE, P95/P99, kritische Branch-Capture, Land-/Border-Fairness |
| **search_contract** | Cross-country AC-gekoppelte Boundary-Moves, balancierte Swaps und Multi-Country-Moves; Quoten/Connectedness/Schutz vor Fit; nach jedem zulässigen Kandidaten voller europäischer x/c0-Refit und Selection-Accept/Rollback |
| **gate_ledger** | G05–G08, Input-/Result-/Split-/Candidate-SHA, Solver-Status, Validitäts-/KCL-/KVL-/Gauge-/Rangresiduen, deterministische Seed-/TieBreak-/Tolerance-Werte als explizite I-Entscheidungen |
| **release_flags** | unabhängiger R-NUM und MA1 R-PHY/R-CLU-Review separat; <code>real_qualified=false</code> ohne vollständigen Original-Datenwitness und G12; MA3 N-1-Vierfachkapazitäten bleiben nachgelagert |

**Normative MA2-Fail-Closed-Bedingungen:** unbekanntes Gerät, mehrdeutiger 380/220-kV-Screening-Status, fehlende Phasen-/Terminaldaten, unbilanzierte AC-Islands, ungültiger SHA/Zeiten/Rating-Einheiten, Country-Mixing, geschluckter kritischer AC-Branch, Kandidat ohne vollständiges Rebuild, negative/undefinierte x, nichtidentifizierbare Baumparameter, fehlendes c0/KVL-Residual, veränderte Splits oder verschlossener Holdout während Selection. Kein stiller Übergang von SYNTHETIC_TESTS_PASS auf REAL_QUALIFIED.

## 8. Erforderliche Owner-Entscheidungen

| Entscheidungs-ID | Optionen | Empfehlung und Konsequenz |
|---|---|---|
| **OD-M2-API-01** Canonical | A allein / B allein / C: **A kanonisch + begrenzter Adapter** | **C**; verbindliches MA2-Ziel bleibt execute_ma1/MA1Result/A-Export; keine Fusion |
| **OD-M2-API-02** HVDC-Semantik MA2-v1 | Strict lossless / signed-losses mit vollständig unabhängig validierten Terminalverlusten | **Strict lossless zunächst**, explizit lossy als gesondertes späteres Device-Gate, nicht als unerkannte Injektion |
| **OD-M2-API-03** Observed AC witness | B-artige harte 1e-6-MW-Gleichheit / separate diagnostische Modellabweichungs-QA | **Separate QA** mit fixierter Toleranz und Source-Witness; kein Ersatz für lossless Modellgleichungen |
| **OD-M2-API-04** Screening/Schutz | Nur nominal-exakt / explizite Klassenzuordnung und auditierten Protected-Union-Contract | **Explizite Klassenzuordnung** und verpflichtende dokumentierte Schutzpolicy |
| **OD-M2-API-05** Publikations-/Freigabegrenze | Bericht und Tests allein / sofort MA2 entwickeln oder mergen | **Nur Bericht, Tests und Owner-Gate**; kein main-Merge, kein MA2-Runtime-Go |

Diese Optionen sind **Empfehlungen, nicht bereits bestätigte Owner-Entscheidungen**. Jede Freigabe muss explizit auf GitHub protokolliert werden. Ein zukünftiger Integrationsplan ist keine Merge-Erlaubnis.

## 9. Schlussbewertung und Folgegates

- **TEST_EVIDENCE:** PASS_SYNTHETIC, unabhängige A/B-Parität 11/11, A+B-Regression 58/58, Fixture-Replay beider Implementierungen bestanden.
- **API_COMPATIBILITY:** NOT_DIRECTLY_COMPATIBLE; definierte lossless-Adapterteilmenge vorhanden; P1-Inkompatibilitäten nachgewiesen.
- **RECOMMENDATION:** A als alleiniger MA2-Canon, B nur mit versionierter kleiner Adapter-/QA-Schicht; A und B bleiben eingefrorene separate Entwicklungsstände.
- **OWNER_GATE:** REQUIRED vor Veröffentlichung eines revidierten MA2-Handoffs als autorisiert.
- **MA2_G06–G08, MA3_N-1, REAL_G12:** NOT_RUN / NOT_AUTHORIZED / BLOCKED_REAL_DATA.
- **MERGE:** NO_MERGE; auch Review-Branch nicht automatisch nach A, B oder main mergen.

Dieser Review vergibt weder die separat einzuholende R-PHY-/R-CLU-/R-NUM-Freigabe noch eine Realnetz- oder MA2-Implementierungsfreigabe.
