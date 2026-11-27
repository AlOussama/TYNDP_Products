# ESM-C2 — Open-TYNDP Deep Scientific & Modular Reuse Audit

**Stand:** 2026-11-28 · **Status:** READ_ONLY_STATIC_AUDIT_COMPLETE / NUMERIC_QUALIFICATION_OPEN  
**Rolle:** Independent Lead Scientific Energy-System Modelling & Optimization Architect  
**Entscheidungsvorlage:** selektiver Reuse; kein allgemeiner Ersatz für die offiziellen TYNDP-Methodiken oder die M2-Implementierung.  
**Mandat:** Vertiefung von ESM-C vor der ESM-A–D-Konsolidierung. Keine Installation, kein Solverlauf, kein produktiver Codepatch, keine Änderungen an Upstream, kein Merge/PR. Ausschließlich dieser Dokumentations-Handoff auf dem vom Owner bestimmten Branch.  
**Ablage:** direkt unter docs/handoffs/ auf docs/esm-b-planning-requirements-20261127, kein separater ESM-C-Ordner.

## 0. Executive Decision Record

### 0.1 Ergebnis in einem Satz

Open-TYNDP ist eine substanzielle, wissenschaftlich wertvolle Implementierung des **zonenbasierten, sektorgekoppelten Referenzmarktmodells** und zahlreicher ENTSO-E-Datenadapter, ergänzt um einen operativen Projektvergleich und B1–B4-Postprocessing. Es ist weder eine umfassende Implementierung der offiziellen Scenario-Building-Transformation noch eine qualifizierte physische IoSN-Netzaggregation noch eine vollständige offizielle CBA-Engine. Für TYNDP_Products empfehlen wir **Reuse auf Funktions- und Datenvertragsebene**, getrennte Environment-Pins sowie eine unabhängige Methodik-/Numerik-Qualifikation.

### 0.2 Wichtigste zusätzliche Erkenntnisse gegenüber ESM-C

| ID | Befund | Evidenz | Reuse-Folge |
|---|---|---|---|
| C2-F01 | 2024 NT ist der veröffentlichte operative Referenzpfad; DE/GA ausdrücklich nicht implementiert/unterstützt. 2026 HEV/LEV sind teilweise implementierte Varianten, kein vollständig reproduzierter offizieller Prozess. | D/C | Nur exakt benannten Szenario-/Releasepfad verwenden. |
| C2-F02 | 2026 listet drei Wetterfälle je Horizont, wählt im Standardpfad jedoch den ersten Eintrag; nicht gemeinsamer Ausbau über mehrere Wetterfälle. | C | Eigene Multiweather-Investment-Schnittstelle notwendig, Solver-Core wiederverwenden. |
| C2-F03 | SB-Default beider Zyklen 168-h-Mittelung, nicht 8760 aufgelöste Stunden. 2024 Standardjahr 52 Wochen; 2026 8760 h Rohkalender. Tages-DSR/EV/Speicher und Extremwerte sind nicht durch den Default validiert. | C | Stundenpfad und Aggregation getrennt qualifizieren; keine automatische Übertragung auf IoSN. |
| C2-F04 | 2026 CBA: fix_reference_sb_to_cba erzeugt leere Korrekturtabelle; prepare_reference exportiert Eingang unverändert. | C | P0: Referenznetz/Reifegrade und PINT/TOOT-Fallbildung vor 2026-Bewertung vervollständigen. |
| C2-F05 | 2026 CBA-Gewichtung enthält weiterhin 1995/2008/2009 mit 0.233/0.367/0.400; fehlendes Label Gewicht 1, keine Renormierung über vollständig nachgewiesene Stichprobe. | C | P0: Wetteridentität, Szenario-/Projekt-/Einheitenschlüssel und vollständige Gewichte erzwingen. |
| C2-F06 | PINT/TOOT-Nutzen ist OPEX-Differenz, nicht NPV; B2 zieht ETS vom sozialen CO2-Preis ab, B3/B4 nutzen eigene Vorzeichen/Einheiten; B4-Faktor 3.6 wurde in v0.9.2 korrigiert. | C/D | Indikatorfunktionen modular übernehmen erst nach unabhängigen Unit-/Sign-Tests. |
| C2-F07 | 2024-Benchmark v0.9 und v0.9.2 sind nicht austauschbar. Publizierte CBA enthält strukturelle Abweichungen: 12 von 126 Übertragungsprojekten mit zusätzlich erschlossener RES-Kapazität, bei einzelnen bis 14 GW. | P/D | B3 und nachgelagerte B1/B2/B4 für betroffene Projekte konditionieren; nicht als Modellfehler gleicher Art wie numerische Residuen behandeln. |
| C2-F08 | CBA-Rolling-Horizon deaktiviert bestimmte globale/Jahresgrenzen und ersetzt Teile durch Referenz-Schattenpreise, SOC-Vorgaben und weitere Heuristiken. Ob alle Jahresgrenzen im zusammengesetzten Ergebnis eingehalten werden, ist nicht nachgewiesen. | C/Q | Annual-resource- und SOC-Ledger als separate Akzeptanzkriterien. |
| C2-F09 | ESM-C2 überprüft vorhandene TYNDP_Products-M2-Verträge. Zonale NTC-Daten sind kein Ersatz für physische Netzdaten, affine KVL, PST-/HVDC-Semantik, detaillierte Flussreferenzen oder Länderquoten. | C | Daten- und Dispatchadapter entwickeln; M2-Core nicht durch Open-TYNDP-Clustering ersetzen. |
| C2-F10 | Lockfiles: Open-TYNDP 1.2.4/0.8.0 (PyPSA/Linopy); Upstream PyPSA-Eur 1.4.0/0.10.1; TYNDP_Products optionaler Adapter verlangt PyPSA >=1.4,<2. | C | Getrennte Environments, neutrale Verträge; kein ungeprüftes Upgrade/Downgrade. |

### 0.3 Architekturentscheidung (Vorschlag, nicht Owner-Freigabe)

- **ACCEPT für Architektur- und Reuse-Planung:** Open-TYNDP-Adapter für PEMMDB, PECD, NTC, H2, Nachfrage und Projekt-/Indikatorverarbeitung.
- **QUALIFY_BEFORE_REUSE:** Import-/Kapazitätsfixierung, Wirtschaftlichkeits- und Ressourcengrenzen, Wetter-/Zeitachsen, Rolling-Horizon, Benchmark-Schlüssel und Datenprovenienz. Erst Dokumentationsvertrag, dann Tests.
- **HOLD für wissenschaftliche Reproduktion der offiziellen 2026-CBA und IoSN:** keine vollständigen offiziellen Referenznetze und Fallgewichte im geprüften CBA-Workflow; fehlende gemeinsame Ausbaustufe, physische Netzäquivalente und formale Prozesskriterien.
- **NO_REPLACEMENT für TYNDP_Products MA1/M2:** bestehende lokale Physik-, Länder-, Screening- und Projektionsebenen bleiben separat.
- **NO numerical acceptance:** keine Modelle installiert oder gelöst, keine Solver- und Datenkampagne, keine produktiven Änderungen vorgenommen.

## 1. Evidenzregeln, Vorgänger und Quellenautorität

### 1.1 Handoff-Kette

- [ESM-A – fachliche Anforderungen](https://github.com/AlOussama/TYNDP_Products/blob/docs/esm-a-planning-requirements-20261127/docs/handoffs/ESM_A_20261127/ESM_A_PLANNING_PROCESS_REQUIREMENTS.md), zuvor verifizierter Blob beb9ba62152624daa44b12e64e7b50ba0a58ad59. ESM-A ist Anforderungsbasis, C2 keine neue Prozessautorität.
- [ESM-B – Antares/GEMS](https://github.com/AlOussama/TYNDP_Products/blob/docs/esm-b-planning-requirements-20261127/docs/handoffs/ESM_B_20261127/ESM_B_ANTARES_GEMS_CAPABILITY_REVIEW.md), unveränderter Vergleichsbericht.
- [ESM-C – vorangegangener PyPSA-/Open-TYNDP-Audit](https://github.com/AlOussama/TYNDP_Products/blob/08e0d5c7fc8999c23bd68248a126402b1060d51f/docs/handoffs/ESM_C_PYPSA_OPEN_TYNDP_CAPABILITY_REVIEW.md), Commit 08e0d5c7fc8999c23bd68248a126402b1060d51f, Blob f9b52f217ad153ffd885b0f79d233351b9923049. C2 ergänzt, überschreibt nicht. Allgemeine Sektorkopplungs-, FBMC-, Unit-Commitment- und Power-Agent-Befunde aus C bleiben erhalten.
- [ESM-D/weitere regionale Arbeiten](https://github.com/AlOussama/TYNDP_Products/tree/docs/esm-b-planning-requirements-20261127): spätere Konsolidierung; keine ungeprüfte Behauptung über deren Status.

### 1.2 Evidenzstufen

D = Dokumentation/Hersteller- oder Projektbeschreibung; C = tatsächlich statisch im Quellcode, in der Konfiguration oder in einem Lockfile festgestellt; T = vorhandener Test mit relevantem Assert geprüft (Test nicht erneut ausgeführt); P = publizierte numerische Ergebnisse Dritter; R = hier numerisch reproduziert; Q = analytische Schlussfolgerung, Risiko oder offener Qualifikationspunkt. Für C2 gilt **R = 0**. P beweist weder R noch offizielle Akzeptanz. Quellcode mit TODO ist keine Implementierung der TODO-Funktion. Ein Workflow-Rule-Name, eine Tabelle in einem README oder eine Modellierungsoption allein ist kein Nachweis aktiver Constraints.

Capability-Klassen: NATIVE (Kernfunktion), CONFIGURATION (bestehende Funktion durch Daten/Optionen), MODEL_EXTENSION (zusätzliche Constraints/Komponenten), ENGINE_EXTENSION (Änderung der Engine), EXTERNAL_COUPLING (separater Prozess/Engine), NOT_SUPPORTED (im geprüften Prozess nicht implementiert), UNVERIFIED (Evidenz reicht nicht). Reuse-Entscheide separat: REUSE_AS_IS, WRAP, ADAPT, NEW, NOT_APPLICABLE. Stets mit Scope und Qualifikation.

### 1.3 Offizielle Referenzquellen

| Quelle | Status/Verwendung |
|---|---|
| [ENTSO-E/ENTSOG Scenario Building 2024](https://2024.entsos-tyndp-scenarios.eu/) | Vergleichszyklus, Methodik/Daten; 2024 NT nicht DE/GA gleichsetzen. |
| [ENTSO-E/ENTSOG Scenario Building 2026](https://2026.entsos-tyndp-scenarios.eu/) | Zyklusbezogene Szenario-/Datenquelle; Datenschnappschüsse getrennt behandeln. |
| [2026 Scenario Input Consultation](https://consultations.entsoe.eu/tyndp/2026-scenarios-input/consult_view/) | Konsultationsstand, nicht ohne weiteres finaler Modellvertrag. |
| [TYNDP 2024 CBA Implementation Guidelines](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2024/foropinion/CBA_Implementation_Guidelines.pdf) | Fassung zur Stellungnahme 09.04.2025; Referenz für CBA 2024, kein Rückschluss auf finale Billigung dieses Dokuments. |
| [TYNDP 2026 Identification of System Needs Methodology for Consultation](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf) | 25.02.2026 Konsultationsentwurf; §3.1, §3.8, Netz-/Wetter-/Ausbauvertrag, Tabellen der Modellzonen. |
| [TYNDP 2026 CBA Implementation Guidelines for public consultation](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2026/Draft_TYNDP_2026_CBA_ImpG_for_PC.pdf) | 16.12.2025 Entwurf; insbesondere §3.1–3.5 und Referenznetz, p.45. |
| [OET Open-TYNDP Methodology](https://open-tyndp.openenergytransition.org/methodology/) | Projektbeschreibung, Modellannahmen und Abweichungen; nicht amtliche Methode. |
| [OET Open-TYNDP Results](https://open-tyndp.openenergytransition.org/results/) | Publizierte Benchmarkdarstellungen und Abweichungen; P-Evidenz. |
| [Zenodo v0.9, DOI 10.5281/zenodo.22921182](https://doi.org/10.5281/zenodo.22921182) | Archivierte externe Rechenergebnisse; Datenarchiv nicht heruntergeladen. |

Offizielle PDF-Quellen für die benannten Anforderungen geöffnet und einschlägige Seiten visuell geprüft; vollständige formale Gegenprüfung aller CBA-Indikatoren, Annex-Versionen und etwaiger später finalisierter Methodikstände nicht vorgenommen. 2026-Statements gelten daher **gegen den bezeichneten Entwurf**, nicht als Feststellung einer amtlichen finalen Konformität.

## 2. Versions- und Fork-Audit

### 2.1 Immutable Pins

| Bezeichnung | Referenz | Status |
|---|---|---|
| O24 | [Open-TYNDP v0.9.2 / c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727](https://github.com/open-energy-transition/open-tyndp/commit/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727) | Release vom 24.11.2026; 2024-Modell; publizierte Release-Notes nennen B4-Faktorfix. |
| O26 | [Open-TYNDP master / 31f5a6fe65613fb86015026aae4a823ee825e1e9](https://github.com/open-energy-transition/open-tyndp/commit/31f5a6fe65613fb86015026aae4a823ee825e1e9) | 27.11.2026 14:01 UTC, Entwicklungsstand TYNDP 2026. Kein bestätigtes v0.10-Release zum Abrufzeitpunkt. |
| E | [PyPSA-Eur / ec79876d2b484fd1e65abc71835444c6bacb0874](https://github.com/PyPSA/pypsa-eur/commit/ec79876d2b484fd1e65abc71835444c6bacb0874) | v2026.11.1; neuer Upstream, nicht blind die Parent-Version. |
| P | [PyPSA / 345091197e7783f1987f6aa8e80ff0dcd726640c](https://github.com/PyPSA/PyPSA/commit/345091197e7783f1987f6aa8e80ff0dcd726640c) | ESM-C-Pin; native FBMC im HEAD, nicht im geprüften v1.4.0-Release. |
| Linopy | [4e78d4ea58858b2ecd9e8fb0afe7bc439e4c79c1](https://github.com/PyPSA/linopy/commit/4e78d4ea58858b2ecd9e8fb0afe7bc439e4c79c1) | ESM-C-Pin; Environment-Versionen davon getrennt. |
| TYNDP_Products M2 | [feature/iosn-m2-ma1-rp1-integration-20261111](https://github.com/AlOussama/TYNDP_Products/tree/feature/iosn-m2-ma1-rp1-integration-20261111) | direkt geprüfte Branch-Dateien mit Blob-Pins in §9; keine Aussage über Merge- oder Release-Freigabe. |

Lizenz: Open-TYNDP-Code MIT gemäß Repository/Dateikopf; PyPSA-Eur/PyPSA-Code MIT gemäß ESM-C. Daten, Drittanbieter-Exceldateien, veröffentlichte Ergebnisarchive und abgeleitete Datensätze besitzen eigene Nutzungs-/Provenienzbedingungen. Kein Transfer der MIT-Lizenz auf externe Daten angenommen.

### 2.2 Ancestry statt bloßer Vergleich zweier Ordner

| Vergleich | Ahead/Behind (Open-TYNDP gegenüber Vergleich) | Merge Base | Ergebnis |
|---|---:|---|---|
| O24 → O26 | 227/6 | 8d3c85958896e845088cda01db16e05b91f68399 | divergiert; API-Dateiliste 300 = mögliche API-Grenze; kein linearer Upgradepfad |
| E → O24 | 753/166 | 0cbacfc29c19073357e81bfc7f5266236388addf | 256 gemeldete Dateien; Soft-Fork, eigene Historie |
| E → O26 | 900/92 | 12c29818bf47f7e2732361b09050e13cec568011 | 268 gemeldete Dateien |
| OET PyPSA-Eur-Parent → O26 | 757/0 | ddb66caf3efefb661b03d4689279b9b54cc6cca7 | separater tatsächlicher Parent-Pfad, aus ESM-C |

Vergleiche: [O24...O26](https://github.com/open-energy-transition/open-tyndp/compare/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727...31f5a6fe65613fb86015026aae4a823ee825e1e9); [Merge Base O26](https://github.com/PyPSA/pypsa-eur/commit/12c29818bf47f7e2732361b09050e13cec568011). Tree API meldete 578 Pfade O24 und 599 O26 ohne Trunkierung. Die Compare API liefert für manche Python-/Snakemake-Dateien keine aussagekräftige Additions-/Deletionszahl trotz geänderter Pfade. **Keine exhaustive semantische Prüfung aller geänderten Dateien behauptet.** Aktive Modellpfade und ausgewählte tatsächlich gelesene Funktionen haben Vorrang.

### 2.3 Environment-Vertrag

| Linux-64-Pin | O24 | O26 | E |
|---|---:|---:|---:|
| Python | 3.13.15 | 3.14.7 | 3.13.18 |
| PyPSA | 1.2.4 | 1.2.4 | 1.4.0 |
| Linopy | 0.8.0 | 0.8.0 | 0.10.1 |
| atlite | 0.6.1 | 0.6.1 | 0.8.0 |
| HiGHS | 1.15.1 | 1.15.1 | 1.15.1 |
| Gurobi | 13.0.3 | 14.0.0 | 14.0.0 |

Quellen: [envs/open-tyndp_linux-64.pin.txt](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/envs/open-tyndp_linux-64.pin.txt), [envs/open-tyndp_linux-64.pin.txt](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/envs/open-tyndp_linux-64.pin.txt), [Upstream Linux-Pin](https://github.com/PyPSA/pypsa-eur/tree/ec79876d2b484fd1e65abc71835444c6bacb0874/envs). Tabellenwerte aus expliziten Paket-Pins, **keine lauffähige Installation**. M2 optionaler PyPSA-Adapter siehe §9. Kein automatischer Zugriff auf aktuelle PyPSA-HEAD-FBMC/andere neue APIs durch Open-TYNDP.

### 2.4 Semantisches Delta O24 → O26

| Änderung | O24 | O26 | Wissenschaftlicher Effekt |
|---|---|---|---|
| Szenariokatalog | NT; DE/GA nicht unterstützt | NT+, HEV/LEV unvollständig | keine gemeinsame Szenariotransformation |
| Zeitachse | 52-Wochen-/Klimajahrpfad | 8760 h, WS-ID je Horizont | Klima-ID nicht Kalenderjahr; Persistenz/Weighting ändern |
| Netzdaten | Referenz-NTC und historische Korrekturen/Offshore | Referenz-Topologie und NTC-Overlay pro Jahr | NTC-Zeitstände prüfen, nicht physische KVL |
| Nachfrage | überwiegend exogene Endnachfrage | neue EV-/Prosumer-/Wärme-/Synfuel-Adapter | mehr explizite Flexibilität, aber Risiko Doppelzählung |
| H2 | 2024-Daten und teilweise MM-Abgleich | Z1/Z2, SRES/DRES, P2G-Splits, Importprofile | zusätzliche Bus-/Link- und Jahresverträge |
| Brennstoff | importiertes H2 und fossile Ketten | Synfuel-MWh_H2-Basis und Biogen-CO2-Budget | Energie-/CO2-Umrechnung, gemeinsames Budget |
| CBA-Referenz | teilweise Korrekturregeln für 2024 | leere Korrektur und Passthrough | 2026-HOLD |
| Benchmarking | 2024-Tabellen, OET-Ergebnisse publiziert | neue Mapping-/Aggregationspfade, alte CBA-Jahreslabels | neue Qualifikation statt Übertragung |

Neue Dateien u.a. [scripts/build_tyndp_electricity_ntc.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/build_tyndp_electricity_ntc.py), [scripts/sb/build_tyndp_demand.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_demand.py), [scripts/sb/build_tyndp_ev_fleets.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_ev_fleets.py), [scripts/sb/build_tyndp_cop_profiles.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_cop_profiles.py), [scripts/sb/build_tyndp_hybrid_heating.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_hybrid_heating.py), [scripts/sb/build_tyndp_nuclear_profiles.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_nuclear_profiles.py), [scripts/sb/build_tyndp_p2g_shares.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_p2g_shares.py), [scripts/sb/build_tyndp_synfuels.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_synfuels.py); PEMMDB-Skript umbenannt; frühere H2-Demand-, Offshore-Hub- und Trajektorien-Skripte aus O24 nicht in gleicher Form vorhanden. Migration detailliert in [doc/migration_tyndp_2026.md:299–310](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/doc/migration_tyndp_2026.md#L299-L310).

## 3. Tatsächlicher Scenario-Building-Prozess

### 3.1 Rekonstruktion des Workflows

Input authority & versions → Datenretrieval und Konvertierung → PyPSA-Bus-/Link-/Generator-/Store-Tabellen und exogene Lasten → Aufbereitung der Referenz-NTC und Kapazitäts-/Verfügbarkeitsdaten → sektorale Komponenten → Zeitaggregation → Bestands-/Brownfield-Logik, Kosten, Emissionen, Anpassungen → konsistente NC-Falldatei → Linopy-Modellerzeugung + Extra-Constraints → Dispatch/ggf. Restinvestition → Statistik/Benchmark.

Relevante Entry Points: [rules/sb.smk](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/rules/sb.smk), [scripts/compose_network.py:77–136](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/compose_network.py#L77-L136), [scripts/prepare_sector_network.py:10009–10156](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L10009-L10156), [scripts/solve_network.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/solve_network.py). Der Compose-Pfad schreibt n.meta einschließlich Konfigurations-/Wildcard-Informationen. Das ist gute Grundlage für Reproduzierbarkeit, aber kein vollständiges Hash-Manifest der Rohdaten und nicht automatisch Nachweis, welche externen Dateien tatsächlich verwendet wurden.

Die Auswahl im Konfigurationsblock allein beweist nicht die Fixierung jedes Assets. Insbesondere das myopic/Brownfield-Verhalten verlangt den Vergleich der **effektiven** p_nom_extendable/e_nom_extendable/s_nom_extendable und investitionsbezogenen Bounds vor und nach compose/solve. Manche sektorale Objekte werden erst extendable angelegt und später mit PEMMDB-Kapazitäten überschrieben. Ohne NC-Inspektion und Solve-Manifest bleibt der gesamte Freiheitsgradvektor UNVERIFIED. Das ist keine Behauptung, dass NT grundsätzlich ein Ausbauproblem wäre.

### 3.2 Effektive Standardprofile (statischer Quellcode)

| Parameter/Funktion | O24 NT | O26 NT+ | Einstufung |
|---|---|---|---|
| Planungshorizonte | 2030, 2040 | 2030, 2035, 2040, 2050 | CONFIGURATION C |
| Foresight | myopic gesetzt; NT-Doku Dispatch | myopic gesetzt, TODO; Referenz-Dispatch | C/D; tatsächliche Restinvestitionen Q |
| Generator/Store extendable_carriers | leere Listen | leere Listen | C; andere Komponententypen/Funktionen separat |
| Rohzeitachse | 2009, 52 Wochen, 8736 h im Standard | 2009-Koordinate, ganzes Jahr 8760 h | C; keine Klimaidentität aus Jahr ableiten |
| Zeitauflösung | 168H Default, 1H optional | temporal.averaging: 168h Default, false für unaggregiert | C |
| Stromnetz | administrative/bidding-zone NTC | administrative/bidding-zone NTC | C; kein physisches DC-/AC-Netz |
| PEMMDB/PECD/hydro | aktiviert | aktiviert | C; Inputqualität Q |
| DSR | aktiviert | aktiviert | C; temporale Semantik Q |
| Heizung (allgemeines PyPSA-Eur-Heizmodell) | false | false; separate TYNDP-Hybridfunktion dennoch aufgerufen | C |
| Industrie/Agriculture | false/false | false/false | C; keine expliziten Prozessketten |
| Transport | true, EV-Anteil im generischen Pfad null, exogene Nachfrage | true, zusätzliche explizite TYNDP-Fleets | C |
| Biomasse/Schifffahrt/Luftfahrt/Fossil | true | true | C; spezifische Mengen-/Anteilannahmen |
| Gas-Netztopologie | false | false, Distribution ebenfalls false | C; EU-Sammel-/Brennstoffbilanz |
| CO2-Netz/spatial | false/false | false/false | C |
| H2-Netz | TYNDP true, Zonen-Option anders | TYNDP true, Z1/Z2 | C |
| synthetische Kraftstoffe | allgemeine Optionen begrenzt | synfuel e-liquids + sng aktiv | C |
| Import | H2 | H2, e-liquids, sng | C |
| Wärmepumpen/Strom-Demand in Standard | im exogenen Lastprofil, nicht eigener Hybridpfad | zusätzlich Hybrid-Wärme und Prosumer-Abgrenzung | C |
| Offshore | TYNDP-Hub-/Crossborder-Abgleich | netzdatenbasierte Offshore-Nodes/Links | C |
| CO2-Preis EUR/t | 113.4 / 147 | 97.47 / 197.51 / 297.54 / 502.74 | C; jeweils auf genannte Horizonte |
| Nutzungsoptionen | DE/GA ausdrücklich nicht unterstützt | HEV/LEV unvollständig | D/C; nicht als voll qualifiziert |
| Bemessung | keine endogene Pkw-/Gebäude-/Industrie-Transformation | keine endogene Pkw-/Gebäude-/Industrie-Transformation | NOT_SUPPORTED im Standard-SB |

Belege: [config/config.tyndp.yaml:14–140](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/config/config.tyndp.yaml#L14-L140), [config/config.tyndp.yaml:219–340](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/config/config.tyndp.yaml#L219-L340), [doc/scenarios.md:24–32](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/doc/scenarios.md#L24-L32), [doc/sb.md:8–125](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/doc/sb.md#L8-L125), [config/config.tyndp.yaml:14–178](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/config/config.tyndp.yaml#L14-L178), [config/config.tyndp.yaml:237–344](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/config/config.tyndp.yaml#L237-L344), [doc/sb.md:99–139](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/doc/sb.md#L99-L139), [config/scenarios.tyndp.yaml:10–41](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/config/scenarios.tyndp.yaml#L10-L41). Die Zahl 8736 ist 52×168 für den Standard O24, kein pauschaler Befund für alle Klimajahres-/Leap-Day-Einstellungen.

### 3.3 Wetter- und Aggregationsvertrag: harte Abgrenzung

O26-Konfiguration enthält je Jahr drei WS-IDs:

| Horizon | in Config gelistete WS-IDs | Standardauswahl im Code |
|---:|---|---|
| 2030 | 003, 021, 029 | 003 |
| 2035 | 032, 037, 059 | 032 |
| 2040 | 065, 071, 077 | 065 |
| 2050 | 091, 092, 106 | 091 |

Die Auswahl erfolgt mit Index [0] in [rules/sb.smk:130–139](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/rules/sb.smk#L130-L139) bzw. [scripts/sb/_helpers.py:862–895](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/_helpers.py#L862-L895). Mehrere WS in einer Liste sind damit **nicht** gleichzeitig als Betriebsstufen im selben Investitionsmodell aktiv. Ein explizit umkonfigurierter Einzelfall je WS ist konzeptionell möglich; unabhängige Runs sind nicht gemeinsam gekoppelt. Die offiziell im IoSN-Entwurf verwendeten drei Fälle/gewichteten Betriebssituationen verlangen ein gemeinsames x (siehe §8); die CBA-Wetterjahre/Methodikgewichte sind wiederum ein anderer Vertrag.

Die 168-h-Aggregation bildet Mittelwerte und entsprechende Snapshot-Gewichte. Sie erlaubt eine schnelle strukturelle Näherung, ersetzt aber nicht die Chronologie: 2 h mit Nachfrage [0, 2 MW] und Supply-Cap 1 MW haben 1 MWh ENS im zweiten Schritt; der Mittelwert [1 MW] über 2 h zeigt 0 ENS. Ebenso können Intraday-Laden/Entladen, Ladeanschluss und tägliche DSR-Budgets verschwinden oder verschärft werden. Insbesondere die Kalendergruppierung eines einzelnen 168-h-Snapshots repräsentiert keinen vollständigen täglichen Constraint-Satz.

**Akzeptanzregel:** Für jeden Solve Schlüssel (cycle, variant, horizon, weather_id, calendar, hours, weights, aggregation, source hash). Explizite Angabe, ob ausschließlich WS[0], Ensemble einzelner Runs oder gemeinsame Investition. Energie, Peak, Min/Max, Rampen, EENS und Speicher-Kontinuität getrennt vergleichen. Keine Validierung von Stundenflexibilität aus Wochenmittelwerten.

### 3.4 Szenariovarianten 2026

HEV/LEV konfigurieren u.a. ±10 % bei Fuel/CO2 relativ zu NT+ und schalten Benchmarking ab. Demand-/H2-Importpreis-Abweichungen fehlen teilweise; der Gas-Demand-Pfad nutzt die NT+-Vorlage, mit dokumentierter fehlender HEV-/LEV-Unterstützung. Die Konsultationsdokumente und spätere Datenversionen sind zudem nicht identisch. **Keine Vollständigkeitsbehauptung für HEV/LEV**. Die Migration dokumentiert noch mehrere offene Annahmen ([doc/migration_tyndp_2026.md:299–310](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/doc/migration_tyndp_2026.md#L299-L310)). Empfohlen: HORIZON×VARIANT×WS Source-of-Truth-Tabelle, pro Parameter Unterschied gegen NT+ und dokumentierter Gleichheitsgrund, statt bloßer globaler Prozentänderung.

## 4. Datenherkunft und tatsächliche Adapter

### 4.1 Cycle-/Snapshot-Matrix

| Datenquelle | Repräsentation und Verwendung | Prüfbedarf |
|---|---|---|
| 2024 Scenario inputs / PEMMDB 2.5 / PECD 3.1 | TYNDP-NT-Lasten, Kapazitäten, Wetterprofile | Datenhash und Lizenz, Input-/Output-Felder trennen |
| 2026 TYNDP Inputs | versioniertes Archiv: 2026-08-21, 2026-10-07, 2026-11-11; latest im gepinnten Register ist 11-11 | 08-21 enthält CBA-Korrekturen, nicht ungeprüft für SB; primary als not-supported markiert |
| PECD | 4.2.1 und 4.2.1+pre-built.0.1, IE00 2040 Windkorrektur | Dateihash, exakte Wetter-/Technologie-Mapping-Version |
| TYNDP CBA projects | weiterhin 2024-Projekt-Archiv in O26 Register, Zyklusbezeichnung zwingend | 2026-Projekt-/Referenzdaten nicht aus 2024 übernehmen |
| 2024 publizierte Outputs | v0.9-Resultatarchiv inkl. ausgewählter NC-Netze | exogene Kalibrierfelder vs unabhängige Vergleichsoutputs trennen |
| Costs / technology-data | annuitisierte CAPEX, Fuel, CO2, technische Parameter, teilweise Offsite-Imports | Kostenbasisjahr, LHV/HHV, Währung, Preis-/Technologieversion |
| PyPSA-Eur Spatial / demand input | unterstützende Geo-/Sektor-/Importdaten | nicht als amtliche physische Netz-/Sektorparameter deklarieren |

Quelle: [data/tyndp_versions.csv:64–95](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/data/tyndp_versions.csv#L64-L95); 2024 [data/tyndp_versions.csv](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/data/tyndp_versions.csv). Keine Roharchive heruntergeladen; keine Zeile daraus als unabhängig verifiziertes Anlagen- oder Flussdatum behandelt.

### 4.2 Funktionsverträge und Qualitätsfallen

| Adapter | Source → Output | Konkreter statischer Befund | Qualifikation |
|---|---|---|---|
| build_tyndp_network | offizielle Nodes/Links → PyPSA-Bus-/Link-Dateien | Onshore/Offshore, H2-Z1/Z2, Import/Bottleneck; Topologie nach Referenzjahr | stabile IDs, Kategorie, Zone, Endpunkte; keine Zuordnung physischer Stationen ohne Mapping |
| apply_tyndp_electricity_ntc | NTC je Horizont → feste Link-Leistung | vorhandene Link-Schnittmenge überschrieben, neue Links angelegt; keine explizite Löschung fehlender Links innerhalb dieser Funktion | fehlt ≠ null ≠ nicht in Betrieb; stale-link-Test; gesondert Richtung/Einheit |
| build_tyndp_pemmdb_data | Excel, Kapazität, availability, power plant params → PEMMDB-Tabelle/Profiles | Aggregation doppelter Bands (p_nom/p_max Summe, andere Attribute first), Filtern nach WS, Einheiten/Pumpen-Korrekturen | heterogene η/Kosten/Rampen nicht durch first unbemerkt homogenisieren |
| PECD conversion | Wetter-/Technologieprofil → p_max_pu | Standard fill_gaps_method zero | missing-data ledger, expliziter Ersatz/Abbruch; zero nicht automatisch tatsächliche Nichtverfügbarkeit |
| build_tyndp_demand | 2026 Excel/Zeitschema → typisierte Lastzeitreihen | market, prosumer, BTM, EV, H2, thermal, synfuel; korrigiert/dedupliziert Spalten; drop zero sum | Identität und Strom-/H2-/Wärmeeinheit; zero-sum darf nicht positive/negative Werte auslöschen |
| build_tyndp_h2_imports | Preis, Kapazität oder Profile → Importdaten | Maximalprofil→p_nom, normiertes p_max_pu; fehlende Profile prüfen | 0-Max, NaN, negative Kapazität, Zeitbasis, Preis-/Energiebasis |
| build_tyndp_h2_network | H2-Link-Excel → Netz | H2-Zonen/Verbindungen | Richtungsgrenzen, Endpunkte, Preis, keine Druck-/Linepack-Ableitung |
| build_tyndp_p2g_shares | Elektrolysekapazität/Zuordnung → Z2-Shares | Teilkapazitäten normiert je Strombus | Summe=1, Nullnenner und fehlende Zonen abweisen |
| build_tyndp_gas_demand | EU27 Supply Tool → jährlicher Gasbedarf MWh | final methane + district-heating gas; TWh×10^6 | system boundary; Nicht-EU27 nicht repräsentiert; keine stillschweigende 0 |
| build_tyndp_synfuels | GWh_H2/kt CO2 → MWh_H2/tCO2 | annual limits und import price auf H2-Basis | einheitliche Umrechnung/Cap, keine MWh-fuel-Doppelumrechnung |
| build_tyndp_ev_fleets | Bestände/Anteile/Stationen/Profile → Fixed/Commuter/Non-Commuter, market/prosumer | flexible Flotte 50:50, share mapping, normalize driving demand | Fleet/zone/segment sum, Charge power basis und SOC prüfen |
| build_tyndp_hybrid_heating / COP | hybride Last und COP, Fuel-Choice → Wärmeprofile | O26, gekoppelte Komponenten | COP>0, LHV/HHV und fehlende Nachfrageknoten |
| build_tyndp_nuclear_profiles | Marktergebnis-/Maintenance-Information → Verfügbarkeit | O26 zusätzliche Inputangleichung | nicht als unabhängige Outputvalidierung ausweisen |

Primärquellen: [scripts/build_tyndp_network.py:6–18](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/build_tyndp_network.py#L6-L18), [scripts/build_tyndp_electricity_ntc.py:43–95](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/build_tyndp_electricity_ntc.py#L43-L95), [scripts/sb/_helpers.py:55–155](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/_helpers.py#L55-L155), [scripts/sb/build_tyndp_pemmdb_data.py:105–200](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_pemmdb_data.py#L105-L200), [scripts/sb/build_tyndp_pemmdb_data.py:245–562](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_pemmdb_data.py#L245-L562), [scripts/sb/build_tyndp_demand.py:67–256](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_demand.py#L67-L256), [scripts/sb/build_tyndp_demand.py:284–382](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_demand.py#L284-L382), [scripts/sb/build_tyndp_h2_imports.py:44–86](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_h2_imports.py#L44-L86), [scripts/sb/build_tyndp_h2_imports.py:89–175](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_h2_imports.py#L89-L175), [scripts/sb/build_tyndp_p2g_shares.py:45–70](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_p2g_shares.py#L45-L70), [scripts/sb/build_tyndp_gas_demand.py:36–77](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_gas_demand.py#L36-L77), [scripts/sb/build_tyndp_synfuels.py:43–125](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_synfuels.py#L43-L125), [scripts/sb/build_tyndp_ev_fleets.py:156–320](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_ev_fleets.py#L156-L320). Bewertung der möglichen Fehlermodi ist Q, nicht Beleg, dass ein veröffentlichter konkreter Datensatz fehlerhaft ist.

### 4.3 Kalibrierung ist nicht Validierung

OET beschreibt für 2024 den Abgleich von Referenz-NTC und weiteren nicht vollständig verfügbaren Parametern mit Marktergebnisdaten. Die offizielle Referenz stammt aus mehreren Modellen; beobachtete Maximalflüsse dürfen nicht als allgemeingültiger Beweis für thermische/NTC-Grenzen verstanden werden. Auch Maintenance-/Demand-Anpassung aus den Zieloutputs kann deren Nähe erhöhen, ohne die freie Prognosefähigkeit zu belegen.

Erforderliche Provenienzklassen: A_INPUT_OFFICIAL, B_INPUT_DERIVED, C_CALIBRATED_ON_OUTPUT, D_ASSUMED, E_HOLDOUT_OUTPUT. Vergleichsmetrik pro Klasse. Parameter fitted aus offizieller Serie nicht im selben Holdout als unabhängig validiert werten.

## 5. Mathematische Rekonstruktion des aktiven Marktmodells

### 5.1 Generischer Vertrag (PyPSA/Linopy, nicht neue Engine)

Sei t ein Snapshot, Δt_t die Zeitdauer, b ein Bus, k eine Technologie, s ein Wetterfall, y ein Horizont. Elektrische Leistungen MW_el, H2/Gas MW_LHV bzw. ausdrücklich deklarierte andere Basis; Speicher MWh, CO2 t, Kosten EUR. Vorzeichen: q_l,t = Link-Eingangsleistung am bus0; output j = η_l,j,t q_l,t. PyPSA-Portflüsse sind am Eingang positiv, am Ausgang entsprechend negativ. In den folgenden Gleichungen sind Einspeisungen in die Busbilanz positiv.

Fixiertes Marktmodell: min Σ_t Δt_t [Σ_g c_g,t p_g,t + Σ_l c_l,t q_l,t + c_ENS ENS_t + weitere aktive Betriebs-/Speicher-/Startkosten]. Für tatsächlich extendable Kapazitäten ergänzt PyPSA Investitionskosten; ob solche Freiheitsgrade verbleiben, ist per Modellmanifest festzustellen.

Für jeden Bus:
Σ lokale Erzeugung + Σ ausgehende Speicherentladung + Σ eingehende Konversions-/Transportleistungen − Σ Link-Verbrauch − Σ Speicherladung − d + ENS = 0.
Für fixierten Generator: p_nom·p_min_pu,t ≤ p_g,t ≤ p_nom·p_max_pu,t. Ramps, min load, availability gemäß aktiver Parametrierung. Für einen gerichteten NTC-Link: 0 ≤ q_ij,t ≤ NTC_ij,y; wenn Verlust η<1, Empfang ηq. Separate Richtung j→i ggf. separat begrenzt. Kein Winkel/Impedanzterm aus NTC herleitbar.

Store: e_t = α_t e_(t−1) + Δt_t(η_ch q_ch,t − q_dis,t/η_dis − d_storage,t), sofern q_dis als Ausgangsleistung definiert; in PyPSA Store/Link-Semantik am richtigen Port umrechnen. 0 ≤ e ≤ E, min SOC zeitabhängig, ggf. zyklisch. StorageUnit mit max_hours und eigener Ladung/Entladung/Inflows/Spill separat behandeln. Die Gleichungen sind rekonstruierter Vertrag, kein exportiertes Linopy-Matrix-Dump.

### 5.2 Stromerzeugung, Brennstoffe, DSR

- Konventionelle Anlagen mit PEMMDB-Kapazität und technischen Attributen; fuel-to-power Links und Generatoren. Bei Link η_el ist p_el = η_el q_fuel; Fuel-Cost auf Eingangsenergie, CO2 aus Fuel-/CO2-Port. Ein direkt in EUR/MWh_el deklarierter Kostenkoeffizient darf nicht nochmals durch η dividiert werden.
- RES: p ≤ capacity·profile. Kein impliziter Strom-/H2-Doppelzugriff auf dieselbe dedizierte Anlage. Curtailment = verfügbare minus erzeugte Energie nach eindeutiger Port-/Carrier-Semantik.
- DSR: Für Generatoren carrier=dsr, P>0, pemmdb_hours<24 setzt Code je normalisiertem Kalendertag d:
  Σ_(t∈d) w_generator,t p_t ≤ P·h_pemmdb.
  Bei h≥24 keine zusätzliche tägliche Grenze. Kein allgemeines Shift-/Rebound-Modell; DSR-Dispatch kann Nachfrageersatz repräsentieren, nicht automatisch verschobene Energie. Bei 168-h-Snapshot wird nur dessen Label-Tag gebildet. Bei Rolling-Horizon über Tagesschnitt muss kumulierte bereits committed DSR-Aktivierung abgezogen werden; im gelesenen Helper wird nur aktueller Fenstersatz gruppiert. Das erzeugt einen strukturellen Prüfbedarf, keinen nachgewiesenen Fehler eines konkreten Ergebnisses.
- Unit commitment: PyPSA-Core grundsätzlich fähig (ESM-C); nicht als automatisch aktive ganzzahlige UC aller OET-Assets zählen. Exakte aktive committable flags, Ramps, outage/maintenance, min up/down und Kosten im Fall prüfen. Keine deterministische Adequacy-Proxy mit probabilistischer ERAA/LOLE gleichsetzen.

Quellen: [scripts/prepare_sector_network.py:1315–1428](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L1315-L1428), [scripts/solve_network.py:1275–1330](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/solve_network.py#L1275-L1330), [scripts/solve_network.py:1333–1422](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/solve_network.py#L1333-L1422).

### 5.3 H2: tatsächlich aktive Komponenten

| Baustein | O26-Implementierung | Formel / Bedeutung | Offene Grenze |
|---|---|---|---|
| Elektrolyse | electricity node → H2-Z1/Z2, zunächst extendable und später Kapazitätsfixierung | h=η_el·q, q≤P_in | finaler Fixed-/Extendable-Manifest; ob PEMMDB MW_el oder output MW_H2 |
| P2G splits | Z2-Teile normiert aus Input | P_i,j = P_i·share_i,j; Σ_j share=1 | fallback/NaN/fehlende Zonen |
| DRES/SRES | dedizierte bzw. zugeordnete Erzeuger-/Elektrolysepfade | Energie der zugeordneten RES nicht doppelt bilanziert | getrennte Bus- und shared-capacity-Regeln tatsächlich prüfen |
| SMR / blue H2 | Gasverbrauch, H2-output, CO2-Abgabe bzw. Capture-Port | h=η_SMR q_gas; CO2_vent+CO2_captured aus deklarierten Intensitäten | LHV/HHV, capture energy, leakage, ramp |
| H2-Rückverstromung | fuel cell/turbine Links zum Strombus | p_el=η_fc h_in | länder-/zonenbezogene Auswahl, kein automatisches Druckmodell |
| Transport | gerichtete H2-Links mit fixer Kapazität | h_ij≤P_ij, bilanziert mit η | kein Druck, Kompressorfluss, Linepack, Hydraulik |
| H2 storage | Store + separater Charger/Discharger | unabhängige P_charge/P_discharge/E, zyklische SOC | Jahresgrenzen, Terminalzustand, Energiebasis |
| H2 import | statische oder normierte zeitvariable Kapazität, Preis | h_import ≤ Pmax·a_t | max=0, missing/zero, absolute Jahresgrenzen |
| H2 final demand | Last an relevanten Zonen | Σ Einspeisung = demand + Verbräuche | fehlende Zonen mit Warnung; kein Beweis zusätzlicher Jahresgleichheit |

Quellen: [scripts/prepare_sector_network.py:1890–2034](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L1890-L2034), [scripts/prepare_sector_network.py:2850–3054](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L2850-L3054), [scripts/prepare_sector_network.py:3756–3908](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L3756-L3908), [scripts/prepare_sector_network.py:4031–4247](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L4031-L4247), [scripts/prepare_sector_network.py:4312–4518](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L4312-L4518), [scripts/prepare_sector_network.py:10009–10156](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L10009-L10156).

Wesentlich: Z1/Z2-/P2G-/DRES-Adapter sind qualitativ mehr als ein generisches Link-Beispiel und wiederverwendbar. H2-NTC- bzw. Transportmodell ist dagegen keine Rohrnetzphysik, keine ENTSOG-Voll-CBA und kein integriertes AC/H2-Drucknetz. Die SB-Doku beschreibt jährliche H2-Bilanzen; ein zusätzlicher, separat zu jedem Land modellierter Jahresgleichheits-Constraint jenseits der Bus-/Kapazitäts-/Importbilanz wurde nicht vollständig nachgewiesen (UNVERIFIED). Kein Beweis einer nationalen Jahresbalance durch einen Satz im README.

### 5.4 Methan, Biomasse, Synfuel und CO2

O26 gas_network=false: attach_gas_load dividiert jährliche MWh durch 8760; aggregiert EU-Last ohne räumliches Gasnetz, erstellt exogene Demand-Busse/Loads und Fuel-Link mit CO2-Port. Dies ist ein einheitlicher Fuel-Pool-/Nachfragevertrag, kein zeitlich aufgelöstes Gasnetz. Bei O24 8736 h oder anderen Zeitachsen ist tatsächliche annualisierte Energie gegen Ziel zu prüfen. [scripts/prepare_sector_network.py:5235–5300](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L5235-L5300).

Synfuels: O26 führt die EU-Sammelbusse für e-liquids und sng in MWh_H2-Basis. Produktionslink von H2-Z2 verwendet eine biogene CO2-Inputport-Kopplung; nachfolgende Links konvertieren in die tatsächlichen Fuel-Busse mit deklarierter η. Die konfigurierte Nachfrage fixiert den entsprechenden Abfluss (min=max auf normierter Reihe); Importgrenzen und Preise stammen aus H2-Basis. §5.1-Portkonvention konsequent anwenden. Zusätzlicher SB-Constraint:
Σ_(l∈synfuel,t) Δt_t q_l,t·(−efficiency2_l) ≤ Q_biogenic_CO2 (t).
Dies begrenzt verwendetes biogenes CO2. Einheit des Limits und Zeitgewicht muss gemeinsam verifiziert sein.

Quellen: [scripts/prepare_sector_network.py:4520–4600](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L4520-L4600), [scripts/sb/build_tyndp_synfuels.py:43–125](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_synfuels.py#L43-L125), [scripts/solve_network.py:1226–1249](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/solve_network.py#L1226-L1249). Der separate CBA-Hook enthält in den gelesenen Zeilen keine entsprechende synfuel-Constraint-Injektion ([scripts/cba/solve_cba_network.py:81–129](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/cba/solve_cba_network.py#L81-L129)). Daher **Constraint-Parität SB–CBA nicht belegt**. Prüfen, ob Limit anderweitig erhalten/ersetzt wurde; CBA-Entwicklung noch offen, keine Behauptung, dass schon publizierte 2026-Werte verletzt sind.

Biomasse-/Biogaspotenziale, Schifffahrt/Luftfahrt und übrige Fuel-Annahmen teilweise vorgegeben/erzwungen; Systemgrenzen pro Sektor dokumentieren. Endogene Fuel-Choice nicht gleich endogene Industrie-, Pkw- oder Gebäudebestandsentwicklung. Keine CO2-Pipeline-/geographische Abscheidungsmodellierung bei CO2 network/spatial=false.

### 5.5 Elektromobilität O26: neue explizite Flotten

Statisch nachgewiesen: Segment- und Zone-Shares, EV ETM DATA (Bestand und TWh), FLEX_SHARE, MISC_PARAMETERS, CHARGING STATIONS; Aufteilung in Fixed sowie Commuter und Non-Commuter je zur Hälfte der flexiblen Flotte. p_nom fixed = max(fixed demand)/η_charge; flexible P_charge = N_flex·units·charge_rate; P_discharge = N_flex·share_V2G·units·discharge_rate; E = N_flex·capacity_kWh/1000. Driving Profile normiert über Jahresindex; availability und minimum SOC je Segment/Fleet/Tagtyp.

Komponenten: separater Bus je Fleet, Charger-Link vom market bus bzw. node+RETE (Prosumer), Last als Driving Demand; bei DSM flexibler zyklischer Store, e_min_pu; bei V2G zusätzlicher Rückspeise-Link, dessen Eingangs-P_nom auf discharge_p_nom/η_discharge gesetzt wird. Die Rückspeisevergütung/Nutzungsentgelt wird auf Eingangsleistungsbasis umgerechnet.

Vertrag für flexible Fleet: E_min,t ≤ e_t ≤ E; e_t = e_prev + Δt(η_c p_charge − p_V2G,input − d_drive); 0≤p_charge≤a_t P_charge; 0≤p_V2G,grid≤a_t P_discharge; terminal cyclic wenn aktiv. Fixed ohne Store: p_grid = d_fixed/η_c. Schaltlogik dsm/v2g, gleichzeitiges Laden/Entladen, Preiszeichen, SOC-Minimum, Anschlussgrenzen und doppelte Prosumer-/Market-Last sind explizite Prüfobjekte. Bei fehlendem grid bus werden Fleets ausgefiltert; Jahresenergie dieser entfernten Flotten muss im Ledger erscheinen. Reindex darf keine NaN in solverrelevanten Reihen belassen.

Quellen: [scripts/sb/build_tyndp_ev_fleets.py:156–242](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_ev_fleets.py#L156-L242), [scripts/sb/build_tyndp_ev_fleets.py:246–320](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_ev_fleets.py#L246-L320), [scripts/prepare_sector_network.py:3197–3307](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L3197-L3307). Reuse-Klasse MODEL_EXTENSION/CONFIGURATION, Evidenz C. Nicht: vollständiges Verkehrsmodell mit endogenem Pkw-Bestand, Netzanschlussverteilung je realem DSO-Feeder, Trip-level individuelles Optimieren, explizite Alterung oder garantierte Reservelieferung. O24 keine gleichwertige explizite TYNDP-Fleet-Komponente im Standard-NT-Pfad.

### 5.6 Prosumer, BTM und Wärme/Kälte

O26 Prosumer: RETE-Busse und gerichtete Netzverbindungen, grundsätzlich unbeschränkte Kapazitäten, η=1, wheeling costs; BTM-Lasten und Prosumer-Fleets von market load getrennt. Diese Differenzierung modelliert Energie-/Marktgrenzen und Gebühren, keine MV/LV-Leitungs-, Trafo-, Phasenspannungs- oder Hosting-Capacity-Physik. Quelle [scripts/prepare_sector_network.py:3371–3505](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L3371-L3505).

O26 Hybridwärme: separate Demand-Busse je Fuel-Typ, elektrisch betriebene HP und Fuel-Boiler konkurrieren um Wärmebereitstellung. HP nutzt ungewöhnliche Portorientierung: negative p0 auf Heat-Bus, η=1/COP zum Stromverbrauch. Bei positiver Wärmeleistung Q ist p_el=Q/COP; z.B. Q=6 MW_th,COP=3 → 2 MW_el Verbrauch. Boiler Q=η_b·q_gas bzw. H2; CH4-CO2-Port. Kapazitäten in dieser Funktion unbeschränkt, keine endogene Gebäude-/HP-Investition. Fehlende Wärmebus-/Lastzuordnung wird protokolliert. Migration nennt H2-Boiler-Wirkungsgradfrage (1/1.08 vs Dashboard-Anzeige 1.08); Heizwertbasis und Quelle prüfen, nicht pauschal einen physikalisch unzulässigen Wirkungsgrad behaupten. [scripts/prepare_sector_network.py:5303–5425](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L5303-L5425), [scripts/prepare_sector_network.py:10166–10389](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/prepare_sector_network.py#L10166-L10389), [doc/migration_tyndp_2026.md:299–310](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/doc/migration_tyndp_2026.md#L299-L310).

**Kälte:** Keine eigenständige explizite Kälte-/Kältenetz-/Kältespeicherkette im geprüften TYNDP-Default nachgewiesen; Kühlung kann Teil exogener Strom-/Endnachfrage sein. Keine belastbare Aussage über Anteil ohne Datenzerlegung. Allgemeines PyPSA-Eur-/Core-Potenzial nicht gleich aktive OET-Konfiguration. Gebäudezustandsmodell/thermischer Komfort, individuelle Wärmespeicher-/Sanierungsentscheidungen und industrielle Prozessflexibilität im OET-NT+-Profil NOT_SUPPORTED bzw. UNVERIFIED, sofern nur geerbte Optionen ohne aktiven Pfad vorhanden sind.

### 5.7 Capability-Matrix (Open-TYNDP-spezifisch)

| Fähigkeit | O24 Standard | O26 Standard | Qualifikationsniveau |
|---|---|---|---|
| Zonal dispatch, multi-carrier KCL | NATIVE/CONFIGURATION | NATIVE/CONFIGURATION | C/D |
| TYNDP-spezifische NTC, PEMMDB, PECD | MODEL_EXTENSION | MODEL_EXTENSION | C |
| physische nodale AC/DC-Netzoptimierung | NOT_SUPPORTED in diesem NTC-Profil | NOT_SUPPORTED in diesem NTC-Profil | C/Q |
| H2-Zonal network, fuel chain, storage | CONFIGURATION/MODEL_EXTENSION | MODEL_EXTENSION, erweitert | C |
| Endogener Netzausbau über alle Wetterfälle | NOT_SUPPORTED | NOT_SUPPORTED im Standardpfad | C |
| DSR daily energy cap | MODEL_EXTENSION | MODEL_EXTENSION | C; Aggregation/RH Q |
| EV V1G/V2G TYNDP-explizit | NOT_SUPPORTED Standard | MODEL_EXTENSION | C; Parameterflags und Zeitauflösung Q |
| Prosumer market split | begrenzt | MODEL_EXTENSION | C |
| Physisches Verteilnetz | NOT_SUPPORTED | NOT_SUPPORTED | C |
| Hybrid-Wärmepumpe CH4/H2 | nicht im Standard | MODEL_EXTENSION | C |
| Explizite Kälte, Industrie/Building Stock | NOT_SUPPORTED/UNVERIFIED | NOT_SUPPORTED/UNVERIFIED | C/Q |
| Gas-Pipeline/Druck/Linepack | NOT_SUPPORTED | NOT_SUPPORTED | C |
| Synfuels + biogenic CO2 cap | eingeschränkt | MODEL_EXTENSION | C; CBA-Parität Q |
| vollständige UC/ERAA | UNVERIFIED / EXTERNAL_COUPLING | UNVERIFIED / EXTERNAL_COUPLING | C/D/Q |
| FBMC | NOT_SUPPORTED als aktiver TYNDP-NTC-Pfad | NOT_SUPPORTED als aktiver TYNDP-NTC-Pfad | C; neuere Core-Fähigkeiten getrennt |
| SoS-CBA-Kalibrierung | UNVERIFIED | UNVERIFIED | Q |
| Projekt-B1–B4 | MODEL_EXTENSION | MODEL_EXTENSION geerbt, Referenzmigration offen | C/P (P nur O24) |
| B5–B9/physische Netzindikatoren/vollständige CBA | NOT_SUPPORTED/EXTERNAL_COUPLING | NOT_SUPPORTED/EXTERNAL_COUPLING | C/Q |
| formale IoSN M2 | EXTERNAL_COUPLING | EXTERNAL_COUPLING | C |

## 6. CBA: forensische Prozess- und Gleichungsrekonstruktion

### 6.1 DAG und Fallidentität

Der CBA-Workflow ist nicht bloß ein weiteres Scenario-Building. Gelesene Rule-/Funktionskette:
clean_projects → clean_tyndp_indicators → simplify_sb_network → fix_reference_sb_to_cba → prepare_reference → prepare weights → solve_cba_msv_extraction → prepare_rolling_horizon → prepare_project → getrennte Reference-/Project-Dispatches → make_indicators → average_indicators → Benchmarkplots.

[rules/cba.smk](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/rules/cba.smk); O24 [scripts/cba/clean_projects.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/clean_projects.py), [scripts/cba/simplify_sb_network.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/simplify_sb_network.py), [scripts/cba/fix_reference_sb_to_cba.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/fix_reference_sb_to_cba.py), [scripts/cba/prepare_reference.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_reference.py), [scripts/cba/prepare_project.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_project.py). Die sechs vorkonfigurierten Projekt-IDs (O24 t335,t339,t1106,s1001,s1013,s1035; O26 t225,t339 und s1001/s1013/s1035, t1106 entfernt) sind Default-Auswahl, nicht vollständiger Projektbestand. Publizierter CBA-Satz größer. PINT/TOOT nicht aus Projektnamen, sondern Fallregister und Referenzmitgliedschaft ermitteln.

Verbindlicher Fallkey vorgeschlagen:
cycle, methodology_version, project_id, horizon, variant, weather_id, method, reference_case_id, with_without, grid_hash, capacity_hash, temporal_hash, fuel/CO2 price hash, SoS_calibration_id, dataset_hashes, code/environment_pins, constraints_manifest, solver_status, output_hash. Kein Vergleich ohne gleiche Kontrollvariablen oder explizit dokumentierte Änderung.

### 6.2 SB → CBA Vereinfachung

O24:
1. Vereinfacht Carrier-/Busstruktur, fusioniert ausgewählte Busse und entfernt Self-loops/Load-Shedding-Objekte.
2. Setzt bestimmte primary-fuel generator capacities auf ∞ (p_nom und p_nom_opt); Matching über Carrier-String kann potenziell zu breit sein.
3. Splittet bidirektionale DC-Links in gerichtete Links; Rückrichtung erhält teilweise Null-Länge/Null-CAPEX, um Kostendoppelzählung zu vermeiden.
4. Friert optimierte Kapazitäten für Betriebsproblem ein; hurdle costs und weitere Regeln.
5. Prüft/patcht Referenzkapazitäten über 2024-Regeln.

Quellen [scripts/cba/simplify_sb_network.py:34–139](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/simplify_sb_network.py#L34-L139), [scripts/cba/simplify_sb_network.py:142–197](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/simplify_sb_network.py#L142-L197), [scripts/cba/simplify_sb_network.py:253–279](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/simplify_sb_network.py#L253-L279). Diese Transformationen verändern die physische/ökonomische Modellstruktur. Sie sind nicht universell äquivalent, insbesondere hinsichtlich bidirektionalem shared cap, Verlusten, Primärressourcen, CAPEX und Last-/Prosumer-Grenzen. Für jeden Transformationsschritt vor/nach Energie-/Kapazitäts-/Kostenledger.

### 6.3 Referenznetz und PINT/TOOT

Sei R_y der gültige Referenzfall im Jahr y, K_p die projektbezogene Änderung der gerichteten Transfergrenzen/Anlagen. Für PINT R_without=R_y, R_with=R_y⊕K_p. Für TOOT R_with=R_y, R_without=R_y⊖K_p. In beiden Fällen muss die Menge der übrigen Projekte konstant sein. Es handelt sich nicht um das isolierte Delta einer beliebigen Leitung aus einem frei gewählten Netz.

O24 clean_projects: Annex-/Methodenmapping, Grenzkorrekturen, unklare oder kapazitätslose Projekte filtern, PINT-Default für nicht klassifizierte Einträge, Storage-Methodenzuordnung nach Referenzstatus; unterstützt custom PINT-/Generator-Definitionen, nicht alle Varianten gleichermaßen. [scripts/cba/clean_projects.py:865–1014](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/clean_projects.py#L865-L1014).

O24 prepare_reference: kapazitative Anpassung gerichteter Links, max(0,current+delta); fehlender negativer Link bzw. fehlende Busse werden mit Warnung übersprungen; referenzbezogene Korrekturen abhängig vom Jahr (insb. 2035/2040) und vorherigem Patch-Status. [scripts/cba/prepare_reference.py:33–79](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_reference.py#L33-L79), [scripts/cba/prepare_reference.py:116–152](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_reference.py#L116-L152). Nicht bewiesen ist, dass sämtliche offiziellen TOOT-Projekte und ihre Interaktionen in jedem Referenzfall korrekt enthalten sind. Referenzledger vor/nach und gegen offizielle Projektstatusliste notwendig.

O24 prepare_project: TOOT subtrahiert; negative_toot_capacity default zero (Clamping), alternativ break; fehlende Links können übersprungen werden. PINT addiert oder legt neue Links an. Bei bestehenden custom generators hauptsächlich p_nom ändern, nicht automatisch alle anderen Attribute. Storage- und Generator-Erweiterung gesondert. [scripts/cba/prepare_project.py:149–242](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_project.py#L149-L242), [scripts/cba/prepare_project.py:313–552](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_project.py#L313-L552). Negative Kapazität nach Subtraktion ist für den wissenschaftlichen Vertrag ein **Daten-/Referenzkonflikt**, nicht stillschweigend 0. Reuse-Adapter soll fail-closed sein, außer dokumentierter Owner-Ausnahme.

O26 **kritischer Unterschied**: [scripts/cba/fix_reference_sb_to_cba.py:1–43](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/cba/fix_reference_sb_to_cba.py#L1-L43) beschreibt und erzeugt eine leere Korrekturtabelle, weil Referenzgrid pro Horizont als passend angenommen wird. [scripts/cba/prepare_reference.py:1–38](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/cba/prepare_reference.py#L1-L38) ist expliziter Placeholder; lädt und exportiert das Netzwerk, ohne TOOT/PINT-/Reference-Corrections anzuwenden. Diese Annahme kann für einzelne Fälle korrekt sein, ist aber keine validierte Referenzkonstruktion. Das 2026-CBA-Register enthält weiterhin Altzyklusdaten und in der Migration benannte offene Referenznetz-/Projektfragen. **HOLD** unabhängig davon, ob einzelne Modelle erfolgreich lösen würden.

Offizieller Prozessvergleich: 2026-Konsultationsentwurf, §3.5/p.45: Referenznetze je Horizont, Reifegrad-/Inbetriebnahmekriterien, projektspezifische Mitgliedschaft. Daraus folgt die Notwendigkeit eines year-/project-/case-spezifischen Referenzregisters. OET-Passthrough ersetzt nicht diesen Vertrag.

### 6.4 SoS, Preisbasis, Kosten und Storage-CAPEX

2024 CBA-Config: 2030/2040; soziale CO2-Preise (low/central/high) 126/238/315 bzw. 339/628/662 EUR/t; beide CBA-Läufe H2/AC load shedding cost 300; HiGHS simplex; 168 Snapshots + 1 Overlap; Storage discount 7%, lifetime default 25y; cyclic battery/CAES; Reservoir-Boundary-Carrier. O26 behält 2030/2040 und die 2024-bezogenen Preise/Weatherlabels, erweitert u.a. cyclic um home battery. [config/config.tyndp.yaml:431–536](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/config/config.tyndp.yaml#L431-L536), [config/config.tyndp.yaml:451–556](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/config/config.tyndp.yaml#L451-L556).

Diese Settings sind eine konkret konfigurierte Rechenannahme, **kein Nachweis** der offiziellen Security-of-Supply-Kalibrierung, VOLL-Werte oder Vollständigkeit des Preisbasisjahres. ENS/Load shedding darf nicht als frei verfügbare günstige Erzeugung den Nutzen systematisch abschneiden. SoS-Kalibrierung, adequacy baseline, monetäre VOLL-Semantik, ENS/MWh und Fallgewicht müssen explizit sein; keine ERAA-Aussage aus einem 300-€/MWh-Proxy.

Storage-CAPEX aus Annuität und jährlichen Kosten pro Energie-/Leistungsgröße; Transmission-CAPEX u.a. Leitungslänge/Technologiekosten, nicht automatisch offizielle projektindividuelle Kostenschätzung. [scripts/cba/_helpers.py:17–102](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/_helpers.py#L17-L102). B1 bleibt OPEX, die Wirtschaftlichkeit benötigt separaten Cashflow mit CAPEX, O&M, Zeitprofil, Diskontierung/Restwert, ohne Doppelzählung. Beispiel NPV = Σ_y δ_y(Σ monetisierte kompatible jährliche Benefits_y − incremental annual costs_y) − initial capex; bei annuitisierten Kosten nicht zusätzlich initial CAPEX doppelt abziehen.

### 6.5 Marginal Storage Values und Rolling Horizon

O24 Algorithmus:
- Perfekt vorausblickender Referenzsolve, Speicherung von Dualwerten der Energiebilanzen (mu_energy_balance); Extraktion ohne Duals nicht erlaubt.
- Nichtzyklische Langzeit-Speicher erhalten initialen SOC aus letztem Perfect-Foresight-Snapshot, sofern zuvor cyclic.
- Bestimmte globale Grenzen (CO2 sequestration limit, unsustainable biomass) entfernt.
- Jahressummenlimits e_sum_min/e_sum_max deaktiviert, indem **has_e_sum_min = isfinite(e_sum_min)** als Maske benutzt wird; für diese Objekte werden beide Grenzen auf ±∞ gesetzt und has_volume_limit markiert. Ob der angekündigte per-window energy budget tatsächlich an jedem relevanten Objekt aktiviert wird, muss separat im erzeugten Constraint-Manifest nachgewiesen werden. Maximum-only-Limits sind durch diese Maske nicht erfasst.
- Zeitabhängige Speicher-Marginalkosten aus Referenzduals, ggf. Resampling; apply_msv_to_network gibt frühzeitig zurück, wenn stores_t.mu_energy_balance leer ist, selbst wenn StorageUnit-Duals relevant sein könnten. Kein Beweis für jeden Speicher.
- Weitere Biomasse-Marginalpreise; ausgewählte Reservoir-SOC-Boundaries auf PF-Trajektorie.
- RH-Fenster W=168, O=1, Startabstand W−O=167; bei jedem Fenster k initial SOC aus vorherigem Snapshot start−1. Überlappende Snapshots erneut optimiert, Ergebnisse zusammenfügen. Fallback solver, Statuscheck, Dispose Model. Das ist nicht exakt 7-tägiges Kalenderraster.

Quellen: [scripts/cba/solve_cba_msv_extraction.py:60–140](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/solve_cba_msv_extraction.py#L60-L140), [scripts/cba/prepare_rolling_horizon.py:29–42](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_rolling_horizon.py#L29-L42), [scripts/cba/prepare_rolling_horizon.py:153–172](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_rolling_horizon.py#L153-L172), [scripts/cba/prepare_rolling_horizon.py:175–227](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_rolling_horizon.py#L175-L227), [scripts/cba/prepare_rolling_horizon.py:230–323](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_rolling_horizon.py#L230-L323), [scripts/cba/prepare_rolling_horizon.py:325–408](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_rolling_horizon.py#L325-L408), [scripts/cba/prepare_rolling_horizon.py:425–465](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_rolling_horizon.py#L425-L465), [scripts/cba/solve_cba_network.py:135–228](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/solve_cba_network.py#L135-L228).

Fachlich: Schattenpreis λ_ref,t einer Storage-energy-balance ist lokale marginale Bewertung im Referenzproblem. Übertragung als Preisvektor in einen anderen Fall ist eine Approximation; λ hängt von Netz, Preisen, Grenzen, Szenario und aktiven Constraints ab. Ein Projekt kann genau die aktiven Grenzen ändern. Ein mit Referenz-MSV und Boundary-SOC geführtes Projektproblem ist nicht notwendigerweise exakt der neue PF-Optimumsfall. Kumulative Jahresressource, Strom-/H2-Bilanz und Speichergrenzen auch im verketteten Ergebnis prüfen. Fallback und Status ok ersetzen keine unabhängige Kontrolle des Termination Condition/Residuals aller Fenster.

Prüfbedarf:
- eindeutige committed snapshots (keine doppelt gezählten Overlap-Stunden), SOC-Rekursion über Übergänge;
- jährliche min/max volume limits mit max-only, min-only, equality, both, ∞, fehlend getrennt;
- tägliches DSR-Budget über Fensterränder; Lade-/Entladeverluste und zyklische Kurzzeitspeicher;
- Schattenpreiszeichen/-Einheit EUR/MWh, Snapshotgewichte, Resampling und Ergebnis-OPEX ohne ökonomische Doppelzählung;
- gleiche End-SOC-/Boundary-Regel in with/without; Sensitivität gegenüber W/O und projektindividuellen MSV;
- explizites Ledger für jede in RH aufgehobene, ersetzte oder nicht erneut hinzugefügte Restriktion, speziell biogenes CO2 in O26;
- separat reporting cost vs objective proxy cost (z.B. Schattenpreis als Hilfskosten).

P0/P1-Status: qualifikationsbedürftig. Kein Ergebnis, dass die veröffentlichten O24-Fälle tatsächlich alle diese Fehler aufweisen. Keine Solver-Reproduktion.

### 6.6 Indikatoren: exakt gelesene Implementierung, sign conventions

Definiere with-project als w, without-project als o, unabhängig von PINT/TOOT. Für positive benefits B1=OPEX_o−OPEX_w. Die Funktionen ermitteln die Reihenfolge aus method. Fälschlich übergebene method-Strings dürfen nicht in einen Else-TOOT-Fall fallen; Adapter muss enum validieren.

| Indikator | Codeformel/Einheit | Abgrenzung und Prüfbedarf |
|---|---|---|
| B1 | (OPEX_o−OPEX_w)/10^6 EURmillion/Jahr | PyPSA stats opex, capex separat; remove_noisy_costs setzt statische marginal_cost_original/capital_cost_original zurück; keine automatische vollständige Sozialwohlfahrt bei Nachfrageelastizität, keine NPV; temporäre Storage-MSV-Kosten/Doppelzählung prüfen. |
| B2a physical | (E_CO2,w−E_CO2,o)/1000 kt/Jahr | positive Mehr-Emission, negative Reduktion; power-sector-Auswahl, nicht systemweite Lebenszyklusbilanz. |
| B2a monetary | (E_CO2,o−E_CO2,w)·(c_soc−c_ETS)/10^6 EURmillion/Jahr | ETS bereits in OPEX berücksichtigt vorausgesetzt; low/central/high; keine doppelte CO2-Bepreisung. |
| B3a RES capacity | Σ G_RES,w − Σ G_RES,o [MW] | zusätzliche projektinduzierte RES muss explizit im with-Fall liegen; sonst strukturell 0. |
| B3 RES generation | (E_RES,w−E_RES,o)/1000 GWh/Jahr | Statistik nach Carrier, Port-/Bus-Abgrenzung erforderlich. |
| B3 curtailed | (Curt_w−Curt_o)/1000 GWh/Jahr | Code nennt Feld annual_avoided_curtailment, liefert aber with-minus-without-Differenz der Curtailment-Statistik. Bei positiver Curtailment-Größe bedeutet negativ eine Reduktion. Nicht blind als positive avoided quantity interpretieren; Export-Sign gegen amtliche Zielkonvention prüfen. |
| B4a–f | (E_pollutant,w−E_pollutant,o)/1000 t/Jahr bei kg Ausgangssumme | NOx,NH3,SOx,PM2.5,PM10,NMVOC; negative Reduktion. Fuel energy×kg/MWh, Bio-Faktoren getrennt; missing factor fail, manche numerisch fehlenden Felder zuvor fillna(0); keine Lebenszyklusemissionen. |

Belege: [scripts/cba/make_indicators.py:78–150](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/make_indicators.py#L78-L150), [scripts/cba/make_indicators.py:248–315](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/make_indicators.py#L248-L315), [scripts/cba/make_indicators.py:316–410](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/make_indicators.py#L316-L410), [scripts/cba/make_indicators.py:411–500](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/make_indicators.py#L411-L500), [scripts/cba/make_indicators.py:554–640](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/make_indicators.py#L554-L640), [scripts/cba/make_indicators.py:645–760](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/make_indicators.py#L645-L760). O24 und O26 verwenden gleichartig benannte B1–B4-Funktionen; O24 hier im Detail gelesen; keine vollständige Byte-/Verhaltensgleichheit aller O26-Calls behauptet.

**B4-Releasefix:** kg/GJ-Faktoren ×3.6 → kg/MWh. [Release v0.9.2](https://github.com/open-energy-transition/open-tyndp/releases/tag/v0.9.2). Publizierte v0.9-Werte nicht unverändert als v0.9.2-Ergebnis behandeln. 100 MWh Fuel ×2 kg/GJ ×3.6=720 kg=0.72 t; ohne Faktor 0.20 t. Das ist ein analytisches Unit-Orakel, keine numerische Reproduktion des Projektarchivs. Im average_indicators-Header existieren B4-Einheitsbezeichnungen kg/year, während der konkrete Indikator ton/year liefert; tatsächliche CSV-Units werden aus Eingangszeilen gelesen. Daher kein blindes Umrechnen anhand eines Konstantennamens; Einheiten pro Key erzwingen.

**B1-Monotonie:** Für exakt gleiche Zielfunktion und sonst gleiche zulässige Nebenbedingungen gilt bei bloßer PINT-Kapazitätserweiterung und global optimalem Solve J_w ≤ J_o (erweiterte zulässige Menge). Nicht ohne weiteres für RH, veränderte SOC-/MSV-Policies, PINT-Koppelanlagen, fixierte RES-Mehrinvestitionen oder reporting cost mit abweichender Zielfunktion. Negative B1 dann untersuchen, nicht automatisch numerischer Bug.

B5–B9 und physikalische/Resilienz-/Umwelt-/Systemstabilitätsbewertungen nicht als durch diese B1–B4-Kette implementiert zählen. Ein positiver B1 oder B1+B2 ersetzt keine vollständige Wohlfahrts-/Investitionsentscheidung.

### 6.7 Aggregation der Wetterfälle: konkrete 2026-Lücke

O24 weights 1995 0.233 / 2008 0.367 / 2009 0.400. O26 hat Variablen in wscenario umbenannt, enthält weiterhin dieselben Jahreszahlen. Es sucht ws-String im Dateipfad, default weight=1 wenn kein bekanntes Label; sammelt Werte und berechnet gewichtete Summe ohne explizite Renormierung. Bei fehlender Wetterzeile, Duplikat oder falschem Label kann daher ein formal numerischer Wert entstehen, der kein valides gewichtetes Mittel ist. O26-Migrationsdoku: bisherige 2024-Kalendernamen wechseln die Snapshots, nicht notwendigerweise die zugrunde liegenden 2026-Profile.

Quellen [scripts/cba/average_indicators.py:38–149](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/average_indicators.py#L38-L149), [scripts/cba/average_indicators.py:30–155](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/cba/average_indicators.py#L30-L155), [doc/migration_tyndp_2026.md:299–310](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/doc/migration_tyndp_2026.md#L299-L310). P0: neue cycle-specific WeightTable mit Schlüssel (cycle,horizon,weather_id), genau vollständiger erwarteter Satz und Σ weight=1; nicht aus Dateinamen oder Default 1. Doppelte project/method/indicator/subindex/units-Schlüssel ablehnen. min/max der ausgewählten Verteilung getrennt von low/central/high CO2-Preisvariante. Für 2026-CBA nur CBA-autorisierte Gewichte verwenden; die IoSN-Entwurfsgewichte aus §8 sind **kein Ersatz**.

## 7. Publizierte Benchmarks: Aussagekraft, Grenzen, Verbesserung

### 7.1 Was tatsächlich veröffentlicht ist

[OET Results](https://open-tyndp.openenergytransition.org/results/) und [Methodology](https://open-tyndp.openenergytransition.org/methodology/) dokumentieren Vergleich mit 2024 NT, u.a. CY2009, Horizonte 2030/2040; CBA unter Klimajahren 1995/2008/2009. Die Vergleichsoutputs sind gemäß Projektbeschreibung aus mehreren Modellen gebildet (fünf, Ausreißerbehandlung); kein eins-zu-eins Vergleich mit einer identischen einzelnen Solverinstanz. [Zenodo DOI 10.5281/zenodo.22921182](https://doi.org/10.5281/zenodo.22921182) veröffentlicht v0.9 am 23.09.2026: Ressourcen- und Ergebnisarchive insgesamt ca. 7.3 GB, B1–B4-Tabellen für Transmissions-/Storage-Projekte und sechs ausgewählte gelöste NC-Netze. Archiv-Metadaten wurden geprüft, **Archive nicht heruntergeladen**, daher keine unabhängige MAE/RMSE pro Projekt oder Coverage-Rekonstruktion.

Archivangaben: resources ca.3.4 GB, MD5 dceb6b46154ddfe1a2d3e18daf5cceb5; results ca.3.9 GB, MD5 c87c4613e5e7c5ea01e58466099c0cf3. MD5 aus Archivmetadaten, nicht durch eigenen Download nachgerechnet. Für spätere Reproduktion SHA256 zusätzlich bilden, Daten-/Lizenzbedingungen prüfen.

Wichtig: v0.9 ist nicht v0.9.2. Die Änderung der Emissionseinheiten betrifft B4. Diagramme der Website sind keine automatisch neue Rechenkampagne unter v0.9.2 oder O26. Ergebnisgrafiken visuell geprüft, nicht alle Einzelwerte aus Abbildungen extrahiert; wegen Auflösung und fehlenden Rohdaten keine ungesicherten quantitativen Fehlerwerte erfunden.

### 7.2 Dokumentierte Abweichungen und Ursachen

| Vergleich | Beobachtung laut OET | Einordnung |
|---|---|---|
| Erzeugung/Installed capacity | weitreichende Übereinstimmung durch Nutzung vorgegebener Inputs; Unterschiede aus Netz-/Tech-Mapping | teils Inputkontrolle, keine unabhängige Modellvalidierung |
| Nuklearproduktion | teilweise höhere Erzeugung; fehlende/andere Maintenance- und Outage-Inputs | explizit Input-Gap, O26 neuer Profiladapter |
| H2-to-power | niedriger als amtliche Referenz in Teilen | OET endogenes H2-Preis-/Fuel-Cost-Verhalten vs andere externe Annahmen |
| H2 domestic/import | Abweichungen zwischen Produktion und Import | Kosten/Capacity/Verfügbarkeitsdaten und Systemgrenze |
| RES-Profile | Abweichungen in CF und Erzeugung | Daten-/Wetterversion, Technologie-/Offgrid-Scope |
| Geographische Abdeckung | fehlende Länder/Nodes in Teilinputs; Gasdaten EU27 | Coverage-Gap statt Nullbedarf |
| Solar thermal | kleiner Beitrag in amtlichen Erzeugungswerten, etwa 0.3/0.5% laut OET | nicht explizit modellierte Technologie/Scope |
| CBA RES unlocking | 12/126 Übertragungsprojekte mit zusätzlicher erschlossener RES-Kapazität, in einzelnen Fällen bis 14 GW, nicht automatisch modelliert | strukturelles B3a-Gap mit Einfluss auf B1/B2/B4; getrennte Projektkohorte |

Primärquelle: OET [Ergebnisse](https://open-tyndp.openenergytransition.org/results/). Kein eigenständiger Nachweis dieser Zahlen aus den amtlichen Exceldateien; als publizierter Projektbefund P kennzeichnen. B3a nahe null ist bei fixierten Erzeugungskapazitäten mathematisch erwartbar, kein Beweis geringer tatsächlicher Nutzen. Bei RES-unlocking-Projekten muss die zusätzliche, projektbedingt zulässige Erzeugungskapazität mit gleicher Annahme im with-Fall modelliert werden; Kosten-/Wohlfahrts-/Emissionsrechnung anschließend erneut durchführen.

### 7.3 Metriken im Quellcode

O24 make_benchmark und O26 entsprechende Funktionen: sMPE, sMAPE, sMdAPE, RMSLE, growth error, missing counts. Symmetric percentage denominator (|model|+|ref|)/2+eps; RMSLE über logarithmische Verhältnisse, Behandlung negativer/nahe null Werte kritisch. Growth verwendet Endpunkte/Epsilon; keine vollständige Zeitreihenvalidierung. O26 aggregiert zu Reference-Zones, bei additiven Kennzahlen Summe, Preise teilweise ungewichtetes Mittel. Zeit-/Scope-Matching ist Teil des Skripts; Aggregation kann Peaks, zeitliche Verschiebung und kompensierende Fehler verdecken.

Quellen [scripts/sb/make_benchmark.py:191–402](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/sb/make_benchmark.py#L191-L402), [scripts/sb/make_benchmark.py:36–84](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/make_benchmark.py#L36-L84), [scripts/sb/make_benchmark.py:176–442](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/make_benchmark.py#L176-L442), [scripts/sb/make_benchmark.py:638–670](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/make_benchmark.py#L638-L670). Kein allgemeiner amtlicher Pass/Fail-Toleranzvertrag in den geprüften Metrikfunktionen. Coverage/Missing nicht aus gemittelter Fehlerrate ableiten.

Empfohlene zweite Ebene (neu, nicht Owner-festgelegt):
- Key-Matching vor Metriken; N_expected, N_matched, N_missing, N_duplicate, N_excluded mit Grund pro Carrier/Zone/WS/Horizon/Indicator.
- MAE, RMSE, signed bias, absolute Energie-/Leistungsresiduen; Kapazitäts- und Energy conservation vor wirtschaftlichem Fit.
- last-/energiebasierte Preise vs ungewichtete Preisstatistik getrennt.
- ENS, Peak, Stunden mit Engpass, SOC-Verläufe und Grenzfälle separat; kein RMSLE auf signed B1/B2/B4 ohne klaren Transformationsvertrag.
- CBA: sign accuracy (nur oberhalb materiality threshold), absolute Fehler, normierte Fehler mit Referenz-Nennerregel, Rangkorrelation, separate Kohorten PINT/TOOT, Storage/Transmission, RES unlock ja/nein.
- Kalibrierte Felder und holdout outputs getrennt. Keine Toleranz aus nachträglichem Blick auf Testdaten als unabhängigen Nachweis behaupten.
- Alle Kennzahlen aus versionierten Roh-/Ergebnisdateien mit unabhängiger Statistikfunktion reproduzieren; v0.9, v0.9.2 und O26 separat.

### 7.4 Performance ist berichtet, nicht reproduziert

OET-Website berichtet u.a. SB 2030 ca.897 s/29.3 GB, 2040 ca.2559 s/29.6 GB; MSV 619/769 s bei ca.30.7 GB; Reference-RH 915/1306 s bei ca.5.8 GB. Dies sind indikative Angaben des Projekts (P). Ohne gesicherte Hardware, exakten Solver-/Parallelitäts-/Zeitauflösungs- und Lizenzvertrag keine extrapolierte Aussage über eigene Laufzeit oder Antares-Vergleich. Für ESM-F später identische Problemgröße, Hardware, Threads, Toleranzen, Warm start, Infeasibility/Retry, I/O und Modellaufbau getrennt messen.

## 8. IoSN: formale Abgrenzung und Wiederverwendung

### 8.1 Anforderungen des offiziellen 2026-Konsultationsentwurfs

Der [IoSN-Methodikentwurf](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf) beschreibt in §3.1, §3.8, pp.12–14,20,25–27 einen gemeinsamen Ausbau-/Betriebsvergleich über Wetterfälle, physisch kalibrierte aggregierte Netze und eine Kandidaten-/Filterkette. Zusammengefasst als eigenständiger mathematischer Zielvertrag:

min_(x≥0,y_s) C_inv(x) + Σ_s π_s C_op,s(y_s)  
subject to 0≤x≤x_max, für alle s: A_s y_s + B_s x = d_s bzw. ≤ Grenzen, KCL/KVL/Netzrestriktionen, Ressourcen und Kandidatenlogik.

x ist ein **gemeinsamer** Vektor, y_s wetterspezifisch. Ein getrennt optimiertes x_s, anschließend Mittelwert oder Auswahl von x_s, ist im Allgemeinen nicht gleich diesem Erwartungswertproblem; es ist auch kein Minimax, solange nicht ausdrücklich anderer Zieloperator vorgegeben.

Entwurfsgewichte (nur IoSN, je Horizont):

| Horizont | WS | π |
|---:|---|---|
| 2035 | 032,037,059 | 0.24,0.43,0.33 |
| 2040 | 065,071,077 | 0.20,0.40,0.40 |
| 2050 | 091,092,106 | 0.23,0.57,0.20 |

Methodik unterscheidet reale Projekte/Kandidaten, weitere konzeptionelle/theoretische Optionen (inklusive Offshore) und Filter-/Auswertungsschritte. Modellzonen sind physisch und geographisch zu qualifizieren (Tabellen insgesamt 102 Zonen). M2-Netzäquivalente müssen Flüsse gegen das detaillierte Original abgleichen; Impedanzen, Flow corrections und N-1-abgeleitete Äquivalentkapazitäten sind nicht durch NTC-Summen oder Längencluster substituierbar. Offizielle Angaben sind **Entwurfsstand**, keine Behauptung finaler Norm.

### 8.2 Open-TYNDP-Gap zum IoSN-Prozess

| IoSN-Baustein | OET-Fit | Entscheidung |
|---|---|---|
| Szenario-/Kapazitäts-/Profilinput | hoch, viele Adapter tatsächlich vorhanden | WRAP/ADAPT |
| Stündlicher sektoraler Dispatch | strukturell geeignet mit Stundenoption; default 168h | QUALIFY, separate Operationsinstanz |
| Gemeinsames Ausbau-x über 3 WS | Standard wählt ersten, NT+ weitgehend Dispatch | MODEL_EXTENSION/NEW orchestration; kein Engine-Neubau |
| Ausbaukandidaten-Reife, Grenzen, CAPEX und zwei Schritte | keine vollständige Prozessimplementierung festgestellt | ADAPT ProjectRegistry, NEW method orchestration |
| Geographische 102-Zonen-Länderquoten | administrative NTC-Topologie ≠ kalibrierte M2-Cluster | EXTERNAL_COUPLING zu TYNDP_Products |
| physikalische AC-equivalent x und affine Flow corrections c0 | NTC-Link-Ketten, keine nachgewiesene M2-Gleichwertigkeit | bestehende M2-Physik behalten |
| N-1 / äquivalente thermische Kapazität | nicht aus OET-NTC ableitbar | M2/physische Engine |
| HVDC/PST-Semantik | Transport-Links, teils Offshore | explizites Mapping, keine automatische PST-Gleichwertigkeit |
| Identifizierter system need / CandidateFilter | nicht vollständiger Prozess in OET | NEW/ADAPT M2+Investments |
| CBA-Projektbewertung nach IoSN | O24 separat nützlich, O26 Referenz-HOLD | selektiver, fallgebundener Reuse |

Die **fünf externen Screening-Jahre in bestehender M2-Implementierung** sind nicht die drei IoSN-Markt-Wetterfälle. Separate Zeitachsen, Gewichte, Quellen und mathematische Funktionen. Kein Gleichsetzen von 102 Aggregationszonen mit bloßer Anzahl von Bidding-Zones.

### 8.3 Physischer Vertrag zum gekoppelten Modell

Für detaillierte bzw. äquivalente AC-Kanten:
f_l,t = b_l(θ_from,t−θ_to,t−φ_l,t)+c0_l,t, mit konsistentem per-unit-/MW-Bezug, b=1/x auf definierter Basis. KCL über AC-Teilnetz plus **explizite** externe HVDC-Terminalinjektionen. PST Phase/Regelplan ist nicht gleich ein frei dispatchbarer Transportlink. Für jede AC-Insel muss die Summe der Injektionen ausgeglichen sein, Referenzwinkel je Insel. Bei Verlusten gesonderte Terminalwerte. Der genaue affine-KVL-/c0-Vertrag aus autorisierter M2-Methodik ist maßgebend, diese Gleichung nur Schnittstellen-Illustration.

Ein OET-Dispatch p_z,t auf Zonen kann höchstens Ziel für disaggregierte Last-/Erzeugungsinjektionen sein. Er identifiziert nicht eindeutig Busvektor p_b,t oder detailed branch flows. Erforderlich: S (Bus→Zone Aggregation), D (zonale Leistung→Bus Zuordnung) mit S·D=I für zulässige Verteilung; Einheiten, Erzeugungs-/Lastgruppen, Grenze, Inselfälle, HVDC/PST-Schedules separat. Disaggregation nicht aus zonalen Nettoflüssen allein. Fehlende Ortsdaten → BLOCKED_DATA, nicht erfundene Busverteilung.

## 9. Konkrete Modular-Reuse-Entscheidung für TYNDP_Products

### 9.1 Vorhandener lokaler Code, tatsächlich eingesehen

Die folgenden Dateien wurden auf feature/iosn-m2-ma1-rp1-integration-20261111 direkt gelesen. Branch kann sich ändern; Blob-SHAs sind Evidenz der gelesenen Version. Kein neuer Governance-Gate-Status, keine Behauptung eines Merges in main.

| Lokale Datei / Blob | Relevanter Vertrag | Entscheidung |
|---|---|---|
| [src/tyndp_reduce/iosn_official/contracts.py](https://github.com/AlOussama/TYNDP_Products/blob/feature/iosn-m2-ma1-rp1-integration-20261111/src/tyndp_reduce/iosn_official/contracts.py) / ba9d6e641c085fe92608f0d67276a60c7969c258 | ACBranch, HVDCTerminals, DetailedGridSnapshot; IDs/Endpunkte/Länder; PST-Schedule, lossy HVDC rejected | REUSE_AS_IS; OET verlustbehaftete Links nicht ungeprüft in Vertrag pressen |
| [src/tyndp_reduce/iosn_official/ma1.py](https://github.com/AlOussama/TYNDP_Products/blob/feature/iosn-m2-ma1-rp1-integration-20261111/src/tyndp_reduce/iosn_official/ma1.py) / 8808cdd55d144d0fefb432445810ae12fd91378b | execute_ma1, Preflight, country budget, Flussreferenz, Screening, quota seed, Projektion, Hashes | REUSE_AS_IS als vorhandene M2-Stufe |
| [src/tyndp_reduce/iosn_official/physical.py](https://github.com/AlOussama/TYNDP_Products/blob/feature/iosn-m2-ma1-rp1-integration-20261111/src/tyndp_reduce/iosn_official/physical.py) / 0a82d35b6a6607c79b2cfa6ee6117b47cfedade1 | AC-KVL, PST/phase, HVDC signed terminal injections, island balance | REUSE_AS_IS; Referenz nicht aus zonalem NTC-Flow approximieren |
| [src/tyndp_reduce/iosn_official/screen.py](https://github.com/AlOussama/TYNDP_Products/blob/feature/iosn-m2-ma1-rp1-integration-20261111/src/tyndp_reduce/iosn_official/screen.py) / 675047a1fa6d1dc01c72d2e74bdd5ad4353e05a3 | 225/400kV, duration weighted overload, 5 externe Jahre, explizite Ratings | REUSE_AS_IS; IoSN-Wetterfälle separat |
| [src/tyndp_reduce/pypsa_adapter.py](https://github.com/AlOussama/TYNDP_Products/blob/feature/iosn-m2-ma1-rp1-integration-20261111/src/tyndp_reduce/pypsa_adapter.py) / 62c54669f5413598f9f5d231c6ebea7e9b4ca914 | bewusst enger 1.4+-Adapter; keine volle Transformer/PST-/Storage/Link/HVDC-Unterstützung | ADAPT dünne typed bridge, bestehende physikalische Verträge nicht umgehen |
| [src/tyndp_reduce/fbmc_bridge.py](https://github.com/AlOussama/TYNDP_Products/blob/feature/iosn-m2-ma1-rp1-integration-20261111/src/tyndp_reduce/fbmc_bridge.py) / 64fd02c61045a0e61d3a867d1437acb816aff89d | PTDF/GSK/CNEC/FBMC research bridge, Sensitivitätsscreen | getrennt qualifizieren; nicht amtlichen FBMC-Prozess behaupten |
| [pyproject.toml](https://github.com/AlOussama/TYNDP_Products/blob/feature/iosn-m2-ma1-rp1-integration-20261111/pyproject.toml) | optional pypsa>=1.4,<2 | separate OET-1.2.4-Umgebung; kein globaler Pin-Wechsel |

Die lokale Quellcodeprüfung adressiert spezifische Integrationsgrenzen, nicht die vollständige MA1/MA2-Review- und Freigabehistorie. Die Governance-/Handoff-Pfade auf einigen zusätzlich abgefragten Branches konnten über die verwendeten Pfade nicht gelesen werden; keine Aussage über jüngste Owner-Gates daraus abgeleitet. Bereits freigegebene lokale Methodikentscheidungen haben Vorrang.

### 9.2 Module: nachgewiesene Funktion, I/O, Reuse

| Reuse-ID | Originalfunktion/Modul | Grenzvertrag | Entscheidung |
|---|---|---|---|
| R01 | [scripts/build_tyndp_network.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/build_tyndp_network.py) + [scripts/sb/_helpers.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/_helpers.py) | Nodes/Links/cycle → zonale IDs und gerichtete NTC | WRAP; normalize IDs, categories, directions |
| R02 | [scripts/build_tyndp_electricity_ntc.py:43–95](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/build_tyndp_electricity_ntc.py#L43-L95) | (network,horizon,NTC frame) → Link-capacity overlay | ADAPT, stale entries/zero/absent und idempotence |
| R03 | [scripts/sb/build_tyndp_pemmdb_data.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_pemmdb_data.py) | input XLSX→asset/availability/cost table | WRAP; schema+energy basis, lineage, duplicate aggregation |
| R04 | PECD profile converters / [scripts/sb/build_tyndp_demand.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_demand.py) | scenario weather/demand→indexed series | WRAP/ADAPT, strict timestamp/coverage/no implicit zeros |
| R05 | [scripts/sb/build_tyndp_h2_network.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_h2_network.py), [scripts/sb/build_tyndp_h2_imports.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_h2_imports.py) | H2-zone transport/import | WRAP, not pipe physics |
| R06 | [scripts/sb/build_tyndp_p2g_shares.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_p2g_shares.py) + H2 attach functions | split & component graph | ADAPT, normalization/capacity freeze |
| R07 | [scripts/sb/build_tyndp_ev_fleets.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_ev_fleets.py) + add_ev_tyndp | fleet table/drive/availability/SOC→components | WRAP/ADAPT, energy+boundary manifest |
| R08 | [scripts/sb/build_tyndp_cop_profiles.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_cop_profiles.py), [scripts/sb/build_tyndp_hybrid_heating.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_hybrid_heating.py) + attach | COP, fuel, heat service | ADAPT, port sign/heating basis, no unlimited-cap extrapolation |
| R09 | [scripts/sb/build_tyndp_gas_demand.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_gas_demand.py), [scripts/sb/build_tyndp_synfuels.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/build_tyndp_synfuels.py) | annual methane/synfuel/CO2 budgets | ADAPT, explicit annual ledger, input basis |
| R10 | [scripts/solve_network.py:1275–1330](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/solve_network.py#L1275-L1330) DSR | Linopy calendar-day cap | ADAPT, actual Δt/day split and remaining budget |
| R11 | [scripts/cba/clean_projects.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/clean_projects.py), [scripts/cba/_helpers.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/_helpers.py) | ProjectRegistry, cost and method mapping | WRAP/ADAPT, schema/year/reifegrad, exceptions ledger |
| R12 | [scripts/cba/prepare_project.py:149–242](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_project.py#L149-L242) | PINT/TOOT transformation | ADAPT, strict reversible delta/no clamp without decision |
| R13 | [scripts/cba/prepare_reference.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/cba/prepare_reference.py) | reference network | NOT_APPLICABLE as 2026 production module; NEW ReferenceCaseBuilder; O24 rules reusable with review |
| R14 | [scripts/cba/prepare_rolling_horizon.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/prepare_rolling_horizon.py), [scripts/cba/solve_cba_network.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/solve_cba_network.py) | MSV/SOC/rolling optimizer | ADAPT, annual/committed ledger, exact solver status |
| R15 | [scripts/cba/make_indicators.py](https://github.com/open-energy-transition/open-tyndp/blob/c3ef9aaccbf2ac11f19c4a6b1bb4a60ec81c3727/scripts/cba/make_indicators.py) | solved with/without→IndicatorSet | ADAPT, units/scope/sign/ETS/original costs/RES unlocking |
| R16 | [scripts/cba/average_indicators.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/cba/average_indicators.py) | weather aggregation | NEW small pure weighted aggregation kernel, reuse schema/plots only |
| R17 | [scripts/sb/make_benchmark.py](https://github.com/open-energy-transition/open-tyndp/blob/31f5a6fe65613fb86015026aae4a823ee825e1e9/scripts/sb/make_benchmark.py) | match, metrics, plots | WRAP/ADAPT, independent coverage and robust signed metrics |
| R18 | [src/tyndp_reduce/iosn_official/ma1.py](https://github.com/AlOussama/TYNDP_Products/blob/feature/iosn-m2-ma1-rp1-integration-20261111/src/tyndp_reduce/iosn_official/ma1.py) | physical aggregation stage | REUSE_AS_IS from own repo, not OET replacement |
| R19 | PyPSA/Linopy multiweather investment | common x + per-s operating variables | NEW model orchestration using existing engine; no engine rewrite unless tests show need |
| R20 | whole OET Snakemake pipeline | reproducible cycle-bound benchmark | WRAP as external benchmark workflow, not canonical TYNDP_Products API |

Snakemake-centric scripts can assume global config, wildcards, working directory, pandas IO, n.config/n.params, and in-place mutation. A function existing in Python does not imply stable public API or side-effect-free behavior. Extract wrapper, not wholesale copy: explicit input/output, version pin, dependency set, logging/provenance, failure taxonomy and license. Use native helpers where contracts match; no general-purpose new ESOM framework needed.

### 9.3 Vorgeschlagene Zielarchitektur

ASCII-Sicht (keine Implementierung):

Official data + version manifest
  → Open-TYNDP-derived typed import/normalization adapters
  → immutable Canonical ScenarioBundle / ProjectRegistry / WeatherSet
  → (A) OET ReferenceMarketCase runner (pinned 1.2.4/0.8)
  → (B) TYNDP_Products physical M2 (MA1/MA2, country quotas, AC/PST/HVDC)
  → (C) IoSN common-investment multiweather adapter (qualified PyPSA/Linopy version)
  → (D) CBA ReferenceCaseBuilder and paired market runner + optional physical network assessment
  → independent Indicator/Evidence layer
  → published comparable results and audit manifest.

**Separation of concerns:** A is reference/zonal dispatch, B is physical reduction, C is expansion process, D is project counterfactual. Coupling through immutable contracts. Same codebase optional, same Python environment not required. No writing physical constraints directly into OET's NTC-only network without proved operator mapping.

### 9.4 Minimal data/API specification (proposal)

| Data contract | Required fields/invariants |
|---|---|
| DatasetManifest | source_uri, cycle, release/retrieval date, file SHA256, schema/unit map, license, derivation class, code pin |
| ScenarioKey | cycle, horizon, variant, weather_id, authoritative method revision, model role (SB/IoSN/CBA) |
| TimeAxis | UTC or explicitly named local/calendar, snapshots unique ordered, Δt positive, weather_id independent of year, leap policy, committed indices, weights by purpose |
| WeatherSet | exact expected IDs, positive normalized weights, allowed horizon, method source, no duplicate |
| AssetCatalog | immutable asset_id, carrier, zone/node, input/output ports+units, capacity_fixed/extendable, bounds, technical params, commissioning, retirement, source fields |
| DispatchEnvelope | p_min/p_max, p_set, efficiencies, ramp basis, storage initial/terminal/availability/min SOC, annual/daily energy budgets |
| MarketTopology | nodes by type, directed link_id, from/to, NTC, loss/efficiency convention, date validity, source, no inference of x/PST/ratings |
| PhysicalBridge | DetailedGridSnapshot, S/D maps, AC/HVDC/PST types, ratings, phase schedules, loss treatment, references, island balances |
| ProjectRegistry | project_id, cycle/year, status/reifegrad, commissioning date, capacity delta per direction/asset, storage P/E, RES unlock, CAPEX/OPEX assumptions, method |
| ReferenceCase | hash of exact project membership and topology, base ScenarioKey, case transformations ledger, SoS calibration ID |
| IndicatorRow | pair_id, indicator, subindex, value, unit, sign convention, scope, source, weather, coverage, solver status, source/result hashes |

Candidate minimal pure APIs (names intentionally new proposals, not existing upstream APIs):
- read_official_scenario(manifest, key) → ScenarioBundle
- build_market_case(bundle, profile, strict=True) → MarketCase + TransformationLedger
- build_reference_case(bundle, project_registry, methodology) → ReferenceCase
- apply_project_delta(reference, project, method) → CasePair (canonical with/without)
- run_market_case(case, env_pin, solver_spec) → ResultManifest
- extract_zonal_dispatch(result, mapping_contract) → ZonalDispatch
- build_m2_inputs(detailed_grid, dispatch, disaggregation, source_refs) → typed local contracts or BLOCKED_DATA
- assemble_multiweather_problem(investments, weather_cases, weight_table) → ModelContract
- calculate_indicators(case_pair, results, policy) → IndicatorRows
- aggregate_indicators(rows, weather_set) → weighted rows + coverage ledger.

Function names in proposal have no implication that these already exist. Implementation only after Owner authorization. Stages independently testable and consumable by other project chats.

### 9.5 Power-Agent Reuse-First

ESM-C already audited PowerSkills, PowerMCP/PowerIO, PowerWF, PowerAgentBench with pins. C2 preserves those contracts instead of re-reviewing the entire libraries:
- PowerSkills: reuse independent review, provenance, source pinning and test-plan rules; no claim it supplies official TYNDP equations.
- PowerMCP/PowerIO: use schema-based retrieval/normalization, explicit units and immutable artifact manifests; no verified connector that automatically yields authoritative PEMMDB/CGMES/IoSN mappings. New adapters qualify as ADAPT; avoid new general transport/schema layers.
- PowerWF: orchestrate per ScenarioKey/WeatherSet/CasePair, stop on missing data or failed solver; preserve role separation, no authorization creep.
- PowerAgentBench: independent analytic/mathematical oracles in §10, evidence taxonomy, per-stage acceptance, no result synthesis before actual run.
- Prior ESM-C pin audit is source; C2 does not claim updated independent tests of all Power-Agent modules. This is a recommended integration path, not installed or executed.

## 10. Qualification campaign design (specification only)

No execution. Synthetic expected values below are analytic test oracles. Acceptance tolerances are proposals, not official or Owner-approved numerical limits. For exact identities: no missing/duplicate keys, exact units, expected branch membership. For small LPs: primal feasibility ≤1e−7 in appropriately scaled units, objective/known variables abs/rel ≤1e−6 suggested; tolerate alternative optima by checking objective/residual/observable invariant rather than all variable values. Solver tolerances and conditioning must be declared. Use larger system tolerance only after error budget analysis.

| ID | Fixture / falsifier | Independent expected result / acceptance | Stage |
|---|---|---|---|
| Q01 | O24/O26 lockfile manifest | exact versions and cycle; mismatched PyPSA/Linopy reject; no implicit upgrade | intake |
| Q02 | dataset absent, explicit zero, repeated source file | distinguish absence from zero; duplicate or hash mismatch fail | input |
| Q03 | NTC two directions 80/20 MW, later link absent vs zero | directed bounds preserved; absent reject or explicit retirement; no stale 80 MW | R01/02 |
| Q04 | PEMMDB aggregate P=60+40 MW, η differing | P=100; energy/cost/efficiency equivalence checked or retain separate bands; first-row η not assumed exact | R03 |
| Q05 | PECD one missing hour vs observed zero | missing mask distinct, no silent 0; imputed values provenance | R04 |
| Q06 | 2 h demand [0,2] MW, capacity 1 MW | hourly ENS=1 MWh, mean-block ENS=0; reject equivalence claim | aggregation |
| Q07 | simple P2G 100 MW, shares 0.4/0.6 | 40+60=100; missing/zero denominator reject; verify capacity on input or output basis | R06 |
| Q08 | electrolyser q=10 MW_el, η=0.7, Δt=1 h | H2=7 MWh_H2; no double conversion; cost basis explicitly input/output | H2 |
| Q09 | import profile [0,10,5] MW | max=10, a=[0,1,0.5]; all-zero profile safely explicit zero capacity | H2 |
| Q10 | H2 charge 10 MWh, η_c=.9, η_d=.8 | ΔSOC=9, max grid/output energy=7.2 MWh for empty terminal | H2/storage |
| Q11 | EV 100 vehicles, capacity 50 kWh, flex=.6, V2G share .5 | flexible E=3 MWh; commuter/non-commuter 30/30 vehicles, fixed 40; driving energy sum preserved | R07 |
| Q12 | fixed EV 4 MWh driving, charge η=.8 | electricity 5 MWh, no battery shifting | R07 |
| Q13 | V2G P_grid=1.8 MW, η=.9, a=1 | input cap 2 MW, grid output cap1.8, SOC−2 MWh in hour | R07 |
| Q14 | flexible EV SOC_min 1 MWh, availability0, driving demand2, initial SOC2 | infeasible without allowed slack/additional charge; explicit infeasibility not negative SOC | R07 |
| Q15 | 6 MW_th heat, COP3 vs boiler η=.9 | HP consumes2 MW_el, boiler 6.6667 MW_fuel; heat balance and positive CO2 coefficient | R08 |
| Q16 | 87,600 MWh annual methane; 8760h vs 8736h | 10 MW for full year, 87,360 MWh on truncated axis before documented renorm; do not silently label annual target satisfied | R09 |
| Q17 | synfuel 4 MWh_H2, 0.25 t/MWh_H2 biogenic coefficient | consumed CO2=1 t; cap0.9 infeasible/production curtailed; same cap active in CBA if required | R09/14 |
| Q18 | DSR P10 MW, h=2h, two 12h windows in same calendar day | true daily cap20 MWh; per-window resets could allow40; merged committed trace ≤20 | R10/14 |
| Q19 | DSR 10 MW×2h/day across 168h aggregate | correct weekly energy budget140 MWh if all seven days represented; label-day-only cap20 not equivalent; still cannot reconstruct individual days | R10 |
| Q20 | weather cases p=.25/.75, costs 40/80 | expectation70; missing case or duplicate reject; unknown label cannot silently get weight1 | R16 |
| Q21 | multiweather common investment x, I=6/MW, benefit_s=10/MW with probability .5 and0 otherwise, 0≤x≤1 | expected net benefit−1/MW → shared x=0; separate optimal x_s=(1,0) inconsistent with shared decision | R19 |
| Q22 | PINT existing NTC80, delta20; TOOT with100 remove20 | with100/without80 for both canonical pairs; inverse operation exact | R12 |
| Q23 | TOOT remove90 from80 | fail-closed expected; no silent clamp to0 without authorized correction | R12/13 |
| Q24 | year-specific reference membership, projects P1/P2, P1 test | with/without differ only P1 and explicitly coupled RES; unrelated P2 unchanged | R13 |
| Q25 | reference project absent from both due passthrough | TOOT rejected; PINT only if actual membership valid | R13 |
| Q26 | 4 h storage, W=3,O=1, initial E=2, net flows [-1,+2,-1,0] MWh | states [1,3,2,2], each snapshot committed once; no overlap double count | R14 |
| Q27 | annual max10 MWh, split windows dispatch6+6 | reject 12>10; maximum-only and min-only independent tests | R14 |
| Q28 | MSV provided only for StorageUnit, empty Store table | still process applicable duals or fail explicit; no silent omission | R14 |
| Q29 | fixed simple LP PINT adds free capacity, J_o=100,J_w=70 | B1=30 monetary units, objective monotonic if same nested feasible set; with method TOOT same sign | R15 |
| Q30 | E_CO2,o=200t,E_CO2,w=100t, social200,ETS80 EUR/t | B2 physical−0.1 kt, benefit12,000 EUR=0.012 MEUR; no ETS double counting | R15 |
| Q31 | curtailment without20 MWh, with5 MWh | with−without=−15 MWh; positive avoided curtailment=+15; explicit field/sign mapping | R15 |
| Q32 | 100 MWh fuel, 2 kg/GJ pollutant | 720kg=0.72t; v0.9.2 conversion test; direction with/without verified | R15 |
| Q33 | RES unlocked project with+50 MW and without0 additional | B3a=50 MW, not 0; compare B1/2/4 after same paired solve | R12/15 |
| Q34 | two reference items [100,−100], model[0,0] | total signed bias0 but MAE100; no aggregate-only validation | R17 |
| Q35 | missing benchmark bus, duplicated price key, negative signed indicator | coverage fails; safe MAE/sign, no inappropriate RMSLE | R17 |
| Q36 | 3 physical buses, 2 zones, HVDC nonzero between AC islands, PST phase known | S·D=I on supported zonal vectors, correct terminal signs, physical residual independently verified; OET NTC not inferred x | R18 |
| Q37 | lossy HVDC offered to existing lossless-only M2 contract | explicit reject/approved contract extension; no forced lossless conversion | R18 |
| Q38 | local country quota across islands and edge cutoff | existing M2 official/synthetic tests independent of OET; preserve quota/connectivity, 37/102 when real authorized data available | R18 |
| Q39 | CBA-B1 reporting cost with MSV proxy included vs excluded | independent cost decomposition, declared physical cost not arbitrary shadow proxy | R14/15 |
| Q40 | failed RH middle window then fallback fails | stop, no complete result/hash/pass; record condition for each window | R14 |

Positive/negative cases required; Q21 distinguishes different mathematical problems, not merely API behavior. Q36–Q38 do not pretend real physical-grid datasets are available. Q16 is input accounting, not an instruction to renormalize every annual variable identically. Q19 only tests energy envelope, not exact equivalence of weekly means to chronological days.

### 10.1 Ordered future qualification stages

1. **PRE:** data source, cycle/methodology authority, licenses, locked environments, project-reference tables, all relevant input/expected test manifests. No solver until accepted.
2. **U:** pure adapters, units, identities, time axes, project delta/sign, no silent filtering. Q01–Q05,Q07,Q09,Q11–Q13,Q15–Q16,Q20,Q22–Q25,Q30–Q32,Q34–Q35,Q37.
3. **S:** small deterministic LP/MILP as needed, independent analytic oracle, Q06/Q08/Q10/Q14/Q17–Q19/Q21/Q26–Q29/Q33/Q36/Q38–Q40.
4. **R24:** reproduce specified 2024-NT case at published v0.9; separate v0.9.2 B4 test and compare corrected output; no assertion of acceptance until raw archive inspected. Test one PINT, TOOT, storage and RES-unlock exemplar; status, weather, complete constraints, costs.
5. **R26:** first qualify 2026 SB at exact WS and full hourly/aggregated pair; complete CBA reference and 2026 WeatherSet before any official CBA comparison.
6. **IoSN:** common-investment 3-weather cases and detailed M2 physical data when authorized; never extrapolate from zonal NTC results.
7. **Independent scientific review:** separate reviewer sees pins, fixtures, formulas, manifests and raw results, validates no circular input fitting. Owner gate.

All stages above are proposed, not executed or delegated.

## 11. Prioritized Gap-/Risk Register

Severity P0 = blocks named scientific claim/release, P1 = must qualify before module reuse beyond documented scope, P2 = improvement/benchmark design. Not all P0 block every individual module.

| ID | Severity | Observation / hypothesis | Blocking scope | Closure artifact |
|---|---|---|---|---|
| G01 | P0 | O26 ref correction empty and prepare_reference passthrough (C) | official 2026 CBA | authoritative reference membership/year/project delta ledger |
| G02 | P0 | O26 old 1995/2008/2009 weather weights and label/default issue (C) | 2026 CBA | cycle-specific WeatherSet, normalized full coverage, Q20 |
| G03 | P0 | no common-x multiweather process in standard (C) | IoSN 2026 | formal model and Q21, same x across scenarios |
| G04 | P0 | physical topology/flow equivalence absent from NTC (C) | M2/IoSN physical proof | typed detailed-grid bridge, independent physical oracles |
| G05 | P0 | HEV/LEV demand/import/gas gaps (D/C) | full 2026 scenarios | complete variant input and validation matrix |
| G06 | P0 | v0.9 published vs v0.9.2 B4 unit fix (D/C) | B4 reproduction claim | paired pin+recalculated units, archive result manifest |
| G07 | P1 | weekly means & day group interaction (C/Q) | temporal flexibility/ENS | hourly benchmark, conservation and chronological bounds |
| G08 | P1 | RH per-window resource/DSR/SOC and year bounds (C/Q) | annual feasibility/benefits | committed ledgers, Q18/26/27/28 |
| G09 | P1 | SB/CBA synfuel CO2-cap parity unverified (C/Q) | O26 CBA H2/fuels | active constraint manifest for both cases |
| G10 | P1 | RES unlocking omitted for subset (P/D) | affected CBA projects | project-specific RES delta and renewed B1–4 |
| G11 | P1 | TOOT default clamp/missing link warning (C) | reference/project correctness | strict delta/error audit Q22–25 |
| G12 | P1 | existing cost/statistic conventions & MSV proxy (C/Q) | SEW/NPV interpretation | objective vs reporting cost decomposition, Q29/39 |
| G13 | P1 | fill_gaps_method zero, dedup/aggregation/drop filters (C/Q) | data completeness | coverage/provenance, zero/missing/schema test |
| G14 | P1 | H2 boiler basis, gas time normalization, P2G allocation (D/C/Q) | sectoral balance | unit-basis table, Q07/15/16 |
| G15 | P1 | dependency mismatch (C) | integration runtime | independent env pins, immutable interchange |
| G16 | P1 | no numeric R, archives not inspected (limitation) | any model acceptance | authorized test run with raw manifests |
| G17 | P1 | possible benchmark circularity via output-derived calibration (D/Q) | independent accuracy claim | split calibration/holdout and parameter lineage |
| G18 | P2 | full fork delta not exhaustively audited | upgrade impact | function-level semantic diff, compare API limitation overcome |
| G19 | P2 | chart results alone lack robust signed metrics/coverage | comparative study | independent MAE/RMSE/sign/case-cohort metrics |
| G20 | P1 | incomplete formal B5–B9, SoS/ERAA/stability etc. | full CBA | appropriate independent network/adequacy/stability workflows |

## 12. Owner-facing work packages (ready for authorization; no implementation)

**C2-W1 DATA CONTRACT (parallelizable with W2):** extract only existing OET adapters via thin wrapper; pin O24/O26 and dataset versions. Output schemas + source map + fixture cases Q01–Q05/Q07/Q09/Q11/Q13/Q15/Q16. Acceptance: no silent gaps, unit/id/time invariants; no solver; stop if license or authority absent.

**C2-W2 REFERENCE CASE CONTRACT:** compare 2024 ReferenceCaseBuilder behavior to official reference requirements and 2026 draft. Implement only if authorized: ProjectRegistry and strict canonical with/without. Q22–Q25, Q33. Stop on unresolved project maturity or missing source. No 2026 claimed compliant CBA until G01/G02 closed.

**C2-W3 OPERATIONS / NUMERICAL CONTRACT:** after authorization, separate minimal hourly LPs, annual resource/SOC/MSV/DSR and unit oracles. Q06/Q08/Q10/Q14/Q17–Q19/Q26–Q28/Q40. Do not require commercial solver for basic fixtures. No large network campaign until fixture gate.

**C2-W4 INDICATOR QUALIFICATION:** code-level independent B1/B2/B3/B4 formulas, units, scope, weights; Q20,Q29–Q35,Q39. Compare v0.9 vs v0.9.2 on designated raw published case after permission. Stop on incompatible dataset or sign.

**C2-W5 IoSN BRIDGE:** existing M2 is authority for physical semantics. Bind zonal schedules to documented disaggregation and detailed grid only when actual data available. Formulate common-x LP with independent weather-operations; Q21/Q36–Q38. Distinguish M2 five screening years vs IoSN three market WS. No replacing existing M2 via generic clustering.

**C2-W6 CROSS-ECOSYSTEM CONSOLIDATION:** ESM-A process needs × ESM-B Antares/GEMS × ESM-C/C2 PyPSA/OET × ESM-D regional/eGon. Compare reusable capability, not branding. Same model/data/time/scenario/constraints and benchmark acceptance. Independent scientific review then Owner decision.

## 13. Final handoff and limitations

### 13.1 Scope achieved

- Version/branch ancestry and environment pins O24/O26/E rechecked; relevant active config, SB data and component paths, reference-builder/CBA transform, RH and B1–4 calculations examined.
- Published 2024 benchmark source, archive metadata, explanatory deviations and metric implementation reviewed; 2026 migration gaps distinguished.
- Direct TYNDP_Products M2 and adapter files inspected, Blob IDs listed; proposed reusable APIs and 20 module decisions with qualification gates.
- 40 analytic benchmark specifications, 20 prioritized gaps, six staged future work packages.
- C2 supplements ESM-C with concrete model/process evidence, not repetition of generic PyPSA capabilities.

### 13.2 Limitations to preserve in downstream chats

- R=0: no installation, solver run, numerical test execution, complete NetCDF/LP matrix inspection, or large raw-data/Zenodo download. Published numerical output is P only; no independent MAE/RMSE or exhaustive official project-by-project reproduction.
- API compare file cap and missing meaningful line-change statistics; selected functions actually read, not exhaustive 300-file diff. Some exact active optional component/constraint combinations and full scenario-input coverage remain UNVERIFIED.
- 2026 official IoSN/CBA methodology sources are cited consultation drafts; no confirmation of any later final approval. Full official requirements cross-check beyond inspected sections remains open.
- OET charts/metadata reviewed, not all individual graph values digitized; no invented metrics. O24-v0.9/0.9.2 and O26 must not be mixed.
- M2 code checked on named integration branch, not asserted merged into main or current Owner-approved; additional governance paths inaccessible in this pass. No automatic transfer of OET NTC to physical M2.
- Power-Agent prior C evidence reused, no full new independent audit of every related tool. Data licenses require explicit validation.
- Proposed architecture, tests/tolerances, priorities and work packages are review recommendations, not preempted Owner decisions. No upstream or model-code changes, no solver campaign, no PR/merge.

### 13.3 Downstream decision recommendation

**Open-TYNDP should be a primary reuse and reference-model source for European TYNDP scenario inputs, market dispatch and selected CBA subfunctions.** Use it in its exact cycle-bound environment as an external reference, extract narrowly defined data/indicator adapters, and retain TYNDP_Products physical and method-authority contracts. Build only the missing glue: strict provenance, reference-case formation, weather-case orchestration with shared investments, verified data mapping, and independent acceptance tests. Do not interpret absence of a full official workflow as a reason to develop a new optimization engine.

**ESM-C2 status: HANDOFF_READY / STATIC_REUSE_DECISION_READY / OFFICIAL_TYNDP_2026_CBA_HOLD / IOSN_NUMERIC_QUALIFICATION_OPEN.**
