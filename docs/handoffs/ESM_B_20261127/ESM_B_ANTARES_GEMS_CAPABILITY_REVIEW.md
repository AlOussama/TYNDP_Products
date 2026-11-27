# ESM-B – Antares & GEMS Scientific Capability Review

**Stichtag:** 27.11.2026 · **Version:** 0.1 · **Status:** Independent source/implementation/CI review; scoped evidence; keine Produktions- oder Owner-Freigabe.  
**Zweck:** fachlich-technische Übergabe an den zentralen ESM-Vergleich (ESM-A/C/D/…); Bewertung unabhängig von einer Produktpräferenz.  
**Ablage:** separater Dokumentationsbranch, Basis main @ 1595d6d38e77804760612621657721b3699d2fea; keine Änderungen an IoSN-Code, Daten oder bestehenden Berichten. ESM-A ist bewusst nur über seinen eigenen gepinnten Branch referenziert.  
**Scope:** klassische Antares-Simulation, GEMS-Schema/Modelle, Antares Modeler und Hybridmodus, GemsPy, Xpansion, PyPSA-to-GEMS und Legacy-Konverter.  
**Arbeitsmodus:** öffentliche Quellen und GitHub read-only geprüft, außer der nachträglich ausdrücklich autorisierten Anlage dieses Branches und dieses Dokuments. Keine Installation, kein Download von Realnetzstudien, keine Antares-/PyPSA-/Xpansion-Solverkampagne. Kleine unabhängige LP-Orakel mit bereits vorhandenem SciPy/HiGHS ausgeführt; keine Engine-Reproduktion.

## 0. Executive Summary / Entscheidungsvorlage

**Befund B-01:** Antares ist heute nicht mehr sinnvoll als bloßes NTC-Strommarktprogramm zu bewerten. Die Kombination aus klassischem Simulator, komponentenbasierter GEMS-Sprache, zwei Interpretern und Xpansion bildet eine ernsthafte modulare Alternative für chronologische Markt-, Adequacy- und stochastische Investitionsstudien. Die einzelnen Schichten haben jedoch unterschiedliche mathematische Fähigkeiten, Ausführungsmodi und Versionsverträge.

**B-02:** GEMS ist eine deklarative LP/MILP-Modellierungs- und Austauschschicht, kein vollständiges sektorales Datenmodell und kein physikalischer AC-Netzsolver. Komponenten, Ports, Zeit-/Szenarioindizes, lineare Nebenbedingungen und Kosten sind vorhanden. Neue EV-, Wärme-, H2-, Prozess- und Flexibilitätsmodelle benötigen zumeist Modellbibliotheken und geprüfte Datenadapter, nicht zwingend eine Interpreteränderung. Nichtlineare AC-/Gas-/Wärmenetzphysik wird dadurch nicht automatisch verfügbar.

**B-03:** Xpansion implementiert stochastische Master-/Subproblem-Optimierung und einen Trajectory-Workflow mit jährlichen Studien, verzweigtem Szenariobaum, Ausbau-/Rückbauvariablen und diskontierten Kosten. Die Frage nach Mehrperiodenfähigkeit ist deshalb differenziert mit JA für Xpansion-Trajectory und NEIN für die automatische Übersetzung von PyPSA investment_periods zu beantworten. Nichtantizipativität und Asset-Vintages sind explizite Modellierungsaufgaben. Ganzzahlige Recourse ist nicht mit gewöhnlichen LP-Benders-Cuts gleichzusetzen.

**B-04:** Der aktuelle PyPSA-Konverter registriert Lines und Transformers und formuliert winkelbasierte DC-Netzgleichungen einschließlich modularer Kapazitäten. Ältere GEMS-Dokumentation, die Transformers ausschließt, ist hier veraltet. Der Konverter ist dennoch kein allgemeiner PyPSA-Eur-Übersetzer. Multiport-Links, Process-Komponenten, Rampen, Link-UC, zusätzliche Linopy-Nebenbedingungen und verschiedene weitere Attribute werden nicht oder nicht sicher übertragen. Nichtzyklische Speicher, Generator-UC, ungleiche Snapshot-Weights und Investitionsperioden werden zumindest teilweise aktiv abgewehrt. Besonders kritisch: fehlende Abwehr bei semantisch relevanten ignorierten Attributen.

**B-05:** Konkrete Codebefunde erfordern eine fail-closed Preflight-Schicht vor jeder produktiven Konversion: (i) StorageUnit verwendet p_max_pu auch als Ladeobergrenze; (ii) Transformer-Phasenschiebung fehlt, obwohl PyPSA 1.3.0 sie in KVL berücksichtigt; (iii) Lines/Transformers fehlen in der Auswahl der Xpansion-Investitionsvariablen und im exportierten Decomposition-Config; (iv) inaktive passive Zweige/Speicher und Multiports können unbemerkt das Optimierungsproblem ändern; (v) die PyPSA-Version in COMPATIBILITY.md stimmt nicht mit pyproject.toml überein. Siehe §5 und §8. Keine dieser Feststellungen ist ein Beweis, dass alle Studien fehlerhaft sind; sie definiert die zulässige Subdomäne.

**B-06:** Ein erfolgreicher CI-Status ist keine vollständige Abdeckung. Der tatsächlich eingesehene E2E-Log am Konverter-HEAD vom 20.11.2026 zeigt zwei Läufe mit jeweils genau fünf bestandenen Hybridtests. Weitere, wissenschaftlich wertvolle Testdefinitionen existieren in end_2_end_tests.py und tests/e2e_2_stage_stochastic/, sind aber durch diesen konkreten CI-Log nicht als ausgeführt belegt. Insbesondere keine pauschale Freigabe für Line/PST-, Speicher- oder ungleichgewichtete Investitionsfälle.

**Empfehlung:** Für den ESM-Gesamtvergleich Antares/GEMS **als eigenständige Referenzfamilie beibehalten**. Priorität: (A) Antares classic + Xpansion für probabilistische Strommarkt-/Bedarfsstudien; (B) GEMS/GemsPy als modellbasierte zweite Engine für kontrollierte LP/MILP-Fälle; (C) selektiver PyPSA-Import mit Capability-/Loss-Ledger und unabhängigen Orakeln; (D) physische Netzplanung über eigenständigen AC-/Redispatch-/DSO-/Gasnetz-Workflow. Kein Big-Bang-Fork, keine unqualifizierte Migration aller PyPSA-Eur-Modelle, keine automatische Ablösung des vorhandenen IoSN-Moduls.

## 1. Bewertungsvertrag und Quellenbasis

### 1.1 Capability und Evidenz sind orthogonal

| Capability | Bedeutung |
|---|---|
| NATIVE | Funktionskern/Modell ist in betrachteter Komponente vorhanden. |
| CONFIGURATION | vorhandene Formulierung kann durch definierte Daten, Restriktionen oder Moduswahl aktiviert werden. |
| MODEL_EXTENSION | zusätzliche deklarative GEMS-Modelle/Portverträge oder deren mathematische Kombination erforderlich; keine neue Engine vorausgesetzt. |
| ENGINE_EXTENSION | Parser, Interpreter, Solverkopplung, Zeit-/Informationsstruktur oder Konverterlogik muss geändert werden; genaue Schicht benennen. |
| EXTERNAL_COUPLING | separater fachlicher Solver/Workflow mit qualifiziertem Schnittstellenvertrag notwendig. |
| NOT_SUPPORTED | betrachteter Pfad kann Funktion im eingefrorenen Stand nicht übertragen/ausführen. |
| UNVERIFIED | Quellenlage oder Scope reichen nicht zur positiven oder negativen Feststellung. |

Evidenzkennzeichen: **D** = Dokumentation gelesen; **C** = konkrete Implementierung oder mathematisches YAML geprüft; **T** = vorhandene Testdefinition mit prüfbarer Assertion gelesen; **CI** = ausgeführter externer Lauf im passenden Commit/Job-Log belegt; **O** = eigenes unabhängiges mathematisches Orakel ausgeführt, nicht betroffene Engine; **R** = eigene Reproduktion durch betroffene Engines (hier nirgends vergeben). Ein CI-Gesamtstatus ohne Testspezifikation ist lediglich BUILD/CI-Evidenz, nicht CI für jedes Feature. NATIVE/D allein ist keine Produktionsfreigabe. Status, Zeitgrenze, Solverprofil und Artefaktprovenienz getrennt.

### 1.2 Eingefrorene Quell-/Versionsmatrix

Default-Branch-HEADs und Release-Tag-Commits unabhängig über GitHub API ermittelt. Die nachfolgenden Detailbefunde beziehen sich, sofern nicht anders angegeben, auf den HEAD-Pin. Release-Tags sind keine automatische Aussage, dass alle HEAD-Funktionen im Release enthalten sind.

| ID | Repository / Branch / HEAD (vollständiger SHA) | Letztes veröffentlichtes Release, Datum, Tag-Commit | Lizenz |
|---|---|---|---|
| S1 | [Antares_Simulator / develop](https://github.com/AntaresSimulatorTeam/Antares_Simulator/tree/b5a88640fd3ecc74ed7be67b61f2e78c7850a05b) · b5a88640fd3ecc74ed7be67b61f2e78c7850a05b | [v10.2.1](https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases/tag/v10.2.1), 25.11.2026 · 3101a616bff678fdbb868aa0be1b458188703da1 | MPL-2.0 laut COPYING.txt (GitHub-Metadaten NOASSERTION) |
| S2 | [GEMS / main](https://github.com/AntaresSimulatorTeam/GEMS/tree/c463e30b610443c1f59b20074bb7acffa2844cce) · c463e30b610443c1f59b20074bb7acffa2844cce | [v0.6.0](https://github.com/AntaresSimulatorTeam/GEMS/releases/tag/v0.6.0), 28.10.2026 · 902ae0801f42bb5143b3f0f05fc318cc8d39ce9c | MPL-2.0 |
| S3 | [GemsPy / main](https://github.com/AntaresSimulatorTeam/GemsPy/tree/77100798fd4cc7fbb2889fc278b257d58c1f08bb) · 77100798fd4cc7fbb2889fc278b257d58c1f08bb | [v0.4.0](https://github.com/AntaresSimulatorTeam/GemsPy/releases/tag/v0.4.0), 20.11.2026 · identischer HEAD | MPL-2.0 |
| S4 | [antares-xpansion / develop](https://github.com/AntaresSimulatorTeam/antares-xpansion/tree/9b509da96e1feeed6a99f80cc9b661cc515bdef7) · 9b509da96e1feeed6a99f80cc9b661cc515bdef7 | [v1.9.0](https://github.com/AntaresSimulatorTeam/antares-xpansion/releases/tag/v1.9.0), 29.06.2026 · 41d073700a38652ee88262a591a1fe603b0c3e87 | Apache-2.0 |
| S5 | [PyPSA-to-GEMS-Converter / main](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/tree/44d73886cf17040550508e88735e451e59a06d5c) · 44d73886cf17040550508e88735e451e59a06d5c | [v0.0.2](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/releases/tag/v0.0.2), 20.09.2026 · 4f2c92ef60eba19f3bb48992f5eef15f29248efe | MPL-2.0 |
| S6 | [AntaresLegacyModels-to-GEMS-Converter / main](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter/tree/ee7d3403ac61886c2e4e51526fc06bec2331d929) · ee7d3403ac61886c2e4e51526fc06bec2331d929 | [v0.5.2](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter/releases/tag/v0.5.2), 18.11.2026 · c5fce0da70c2cee391a32408e3728ae91735c087 | MPL-2.0 |
| S7 | [PyPSA v1.3.0 / Quellreferenz](https://github.com/PyPSA/PyPSA/tree/0209b0ed0a29e7e373b92883e88999dac4dc85a1) · 0209b0ed0a29e7e373b92883e88999dac4dc85a1 | vom Konverter-Package gepinnt; nicht als neuester PyPSA-Release behauptet | MIT (PyPSA-Projekt; Lizenzdatei für Distribution separat prüfen) |
| S8 | [ESM-A, unabhängiger Anforderungskatalog](https://github.com/AlOussama/TYNDP_Products/blob/955c92af93de08ae54eca6c4dcfe8d73e0401fd4/docs/handoffs/ESM_A_20261127/ESM_A_PLANNING_PROCESS_REQUIREMENTS.md) | 27.11.2026, 955c92af93de08ae54eca6c4dcfe8d73e0401fd4 | projektinterner Vertrag |
| S9 | [TYNDP_Products README](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/README.md) | dokumentierte IoSN-Aggregation, FBMC/GSK, N-1; synthetische Ergebnisse nicht Realnetzfreigabe | Bestandsprojekt |

### 1.3 Abhängigkeiten, Kompatibilität, Versionskonflikte

| Schicht | Konkreter Vertrag / Befund | Konsequenz |
|---|---|---|
| Simulator | [COPYING.txt](https://github.com/AntaresSimulatorTeam/Antares_Simulator/blob/b5a88640fd3ecc74ed7be67b61f2e78c7850a05b/COPYING.txt), [vcpkg.json](https://github.com/AntaresSimulatorTeam/Antares_Simulator/blob/b5a88640fd3ecc74ed7be67b61f2e78c7850a05b/vcpkg.json): Sirius ≥1.9, Boost, yaml-cpp, ANTLR4, Arrow/Parquet; C++/OR-Tools MPSolver-Schnittstelle im Code. Manifest version-string 10.2.0, Release 10.2.1 gesondert. | Binär- und Buildprofil separat pinnen; nicht aus Git-Tag auf vorhandenen lokalen Solver schließen. |
| GEMS | [COMPATIBILITY.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/COMPATIBILITY.md), [dependencies.json](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/dependencies.json): v0.6.0 ↔ Simulator 10.2.0/GemsPy 0.2.0; dokumentierte Zeile v0.6.1 ↔ 10.2.0/0.3.0, aber letzter API-Release v0.6.0. | Kein Nachweis der vollständigen Kompatibilität von GEMS-HEAD mit GemsPy 0.4.0 und Simulator 10.2.1. |
| GemsPy | [pyproject.toml](https://github.com/AntaresSimulatorTeam/GemsPy/blob/77100798fd4cc7fbb2889fc278b257d58c1f08bb/pyproject.toml): Python ≥3.11, Linopy ≥0.9.0, xarray ≥2025.3, highspy ≥1.14, NumPy, Pydantic, Pandas, Arrow, ANTLR. HiGHS default, Gurobi/Xpress optionale separate Lizenzen. | Python/solver/lockfile separat; keine automatische Gleichheit mit Antares C++-Interpreter. |
| Xpansion | [antares-version.json](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/antares-version.json), [vcpkg.json](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/vcpkg.json): Simulator 10.2.0, OR-Tools-RTE 9.13-rte1.3, Coin CBC 2.10.7/CLP 1.17, TBB, MPI u.a.; Manifest noch 1.8.0 trotz letztem Release 1.9.0. | Keine Versionsgleichsetzung; CLI-, Solver- und MPS-Vertrag prüfen. |
| PyPSA-Konverter | [COMPATIBILITY.md](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/COMPATIBILITY.md) nennt 0.0.2/1.2.4/10.1.1 und teils 0.0.1; [pyproject.toml](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/pyproject.toml) pinnt 0.0.2, PyPSA **1.3.0**, antares-craft 0.17.1, Python ≥3.11,<3.15, dev-GemsPy 0.1.3; [dependencies.json](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/dependencies.json) Modeler 10.1.1, Xpansion 1.9.0. Auch Release-Tag v0.0.2 pyproject und wesentliche Dispatch-Branching-Logik stichprobenartig geprüft. | **Versionsdrift**: Paket/Lock/CI vor README bevorzugen. Kein Universalstack aus allen neuesten Releases. |
| Legacy-Konverter | [COMPATIBILITY.md](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter/blob/ee7d3403ac61886c2e4e51526fc06bec2331d929/COMPATIBILITY.md), [pyproject.toml](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter/blob/ee7d3403ac61886c2e4e51526fc06bec2331d929/pyproject.toml): 0.5.2, Simulator 10.2.0, craft 0.17.1, GemsPy 0.3.0, time-series-generation 0.1.9, study-version 1.0.20. | Separater Validierungspfad, nicht mit PyPSA-Konverter-Stack vermischen. |

MPL-2.0 erlaubt Nutzung und Modifikation; bei Verteilung modifizierter MPL-Dateien deren Quelltext-/Notice-Pflichten beachten. Apache-2.0 für Xpansion und MIT-Bausteine separat behandeln. Proprietäre Solver und externe Daten/Studien benötigen eigene Rechte. Keine rechtliche Gesamtlizenzfreigabe oder SBOM-/CVE-Audit durchgeführt.

### 1.4 Organisationsinventar (35 öffentliche Repositories entdeckt)

[AntaresSimulatorTeam](https://github.com/AntaresSimulatorTeam) API-Inventar, nicht bloß die fünf vorgegebenen URLs. Folgende Gruppen wurden auf Relevanz gesichtet:

| Gruppe | Repositories | Bewertung |
|---|---|---|
| Rechenkern/Schema | Antares_Simulator, GEMS, GemsPy, antares-xpansion | primäre Tiefenprüfung |
| Konverter/Build | PyPSA-to-GEMS-Converter, AntaresLegacyModels-to-GEMS-Converter, antares_craft, antares-study-version, antares-timeseries-generation, antares-water-values | erste zwei vertieft; craft/TS/Version über Abhängigkeiten; eigenständige Water-Values-Implementierung noch nicht geprüft |
| Studien/Evidenz | Antares_Simulator_Tests_NR, Antares_Simulator_Tests, Antares_Simulator_Examples, simulator-cucumber-tests, SimTest, NonRegTests | Kandidaten für Legacy-Regression; Inventar, keine exhaustive Ausführung oder unabhängige Testabdeckung |
| Orchestrierung/GUI/Daten | AntaREST, antares-launcher, GEMS-ViewsBuilder, antares-doc, antares-desktop (Repositoryname antares_desktop), antares-datamanager-generator, antares-datamanager-back, antares-datamanager-front, antares_data_collection, antares-web-installer, antarest-python-client, Antares_Data_Organizer | Datenzugriff, Ausgabe, Workflow, keine zusätzliche mathematische Fähigkeit allein aus Namen abgeleitet |
| Build/Infrastruktur | antares-vcpkg-registry, cache, .github, Antares-AI-Plugins | potenziell ergänzend, nicht fachlicher Solver |
| archiviert | sirius-solver, antares-deps, or-tools | historische Abhängigkeiten; nicht als aktuelle eigenständige Entwicklung verwenden |

RTE-spezifische Entwicklung: Copyright-/Projektbezug in Simulator und GEMS-YAML; Andromède-Modellbibliothek im Originalrepo (siehe §4). Weiterführende RTE-interne Modelle, reale Studien und vollständige Produktionsketten nicht öffentlich verifiziert. Das gesamte öffentliche Organisationsinventar wurde erhoben; **kein Zeile-für-Zeile-Audit aller 35 Repositories**. Kernrepos und ausgewählte Schnittstellen, Modelle und Tests nach wissenschaftlicher Relevanz geprüft.

## 2. Architektur- und Datenvertrag: sechs verschiedene Ebenen

    Antares legacy study (areas, links, thermal, hydro, STS, binding constraints)
          |                         |
          | legacy conversion       | classic MC dispatch
          v                         v
    GEMS libraries + instantiated system + series + scenario/optim config
          |                         |
          | standalone C++           | Python
          v                         v
    antares-modeler             GemsPy (gems_craft + gems_runner / Linopy)
          |                         |
          +---- LP/MILP/MPS + decomposition/coupling ----+
                                                       v
                                          Xpansion Benders / trajectory
    PyPSA network + explicit unsupported-feature ledger -> scoped GEMS conversion
    Independent AC/DC security and DSO/gas validation <- canonical dispatch/capacity contract

1. **Classic Antares**: strukturierte Datenverträge für Zonen, Verbindungen, Erzeugungscluster, Wasserkraft, Speicher, Szenarien und Binding Constraints. Wirtschaftlichkeits-/Adequacy-Modus, zeitliche Blockstruktur. Kein freier Komponenteninterpreter im klassischen Pfad.
2. **GEMS**: sprach- und modellbezogene YAML-Dateien, Bibliotheken, Parameter, Variablen, Port-Typen und Port-Felder, Gleichungen, Kosten, Szenarien, Kalender und Optimierungskonfiguration. Nicht mit einem Solver verwechseln.
3. **Antares Modeler**: C++-Interpreter, standalone über antares-modeler; Hybrid über antares-solver. [Interpreter-Dokumentation](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/overview/gems-interpreters/antares-simulator.md), [Modeler.cpp](https://github.com/AntaresSimulatorTeam/Antares_Simulator/blob/b5a88640fd3ecc74ed7be67b61f2e78c7850a05b/src/modeler/modeler/Modeler.cpp#L147-L390): SystemLinearProblemBuilder, komponentenbezogene Filler, LP/MIP-Build, MPS-Export und Master/Subproblem-Aufbau. Dokumentation ausdrücklich teilweise under construction.
4. **GemsPy**: gems_craft (Parsing, Validation, Komponenten-/Systeminstanziierung), gems_runner (Vektorisierung, Linopy, Solver, Ausgaben). [optimization.py](https://github.com/AntaresSimulatorTeam/GemsPy/blob/77100798fd4cc7fbb2889fc278b257d58c1f08bb/src/gems_runner/simulation/optimization.py): tatsächlicher Linopy-Modellbau mit Komponenten-, Zeit-, Szenarioachsen, Zugriff auf Variablen, LP-Export, Objective-Konstante und Status. [session.py](https://github.com/AntaresSimulatorTeam/GemsPy/blob/77100798fd4cc7fbb2889fc278b257d58c1f08bb/src/gems_runner/session/session.py) unterstützt frontal, sequential, parallel-subproblems und Benders-Konfiguration; letzteres erzeugt keine normale SimulationTable. [runner.py](https://github.com/AntaresSimulatorTeam/GemsPy/blob/77100798fd4cc7fbb2889fc278b257d58c1f08bb/src/gems_runner/simulation/runner.py) ruft externe Xpansion-Binaries auf. Daher ist Benders in GemsPy keine unabhängige vollständige Python-Benders-Engine. End-to-end-Verfügbarkeit der aktuellen Kombination separat nachweisen.
5. **Xpansion**: Benders, Kandidaten, Investment Master, strukturierte MPS/LP-Probleme und Gewichte; Trajectory-Workflow (siehe §3).
6. **Konverter**: PyPSAStudyConverter übersetzt Daten und ausgewählte Modellsemantik, nicht beliebige ausgeführte Linopy-Modelle. Legacy-Konverter übersetzt klassische Antares-Studien über craft/templates und bietet Hybridmodus; kein Garant für identische Ergebnisse.

**Hybrid-Sondergrenze:** [GEMS hybrid limitations](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/interoperability/hybrid/limitations.md): Horizont/Zeitreihen müssen zum Legacy-Studienfenster passen; MILP-Modus für integer/binary; klassische MC-Jahre separat, daher keine allgemeinen szenariounabhängigen Entscheidungsvariablen im normalen Hybridbetrieb. Spezielle Xpansion-Problemgenerierung ist davon zu unterscheiden. Ein Hybrid-Export ist nicht automatisch ein gemeinsam gelöstes stochastisches Extensive Form.

## 3. Wissenschaftliche Modellmatrix

### 3.1 Toolneutrale Referenzformulierung

Notation: i Anlage, n Bus/Zone, l Zweig, t Zeitintervall, s Szenario, k Investitionsknoten; w_t [h], π_s Wahrscheinlichkeiten mit Summe 1. Kapazität X [MW/MWh], Dispatch p [MW], Energie e [MWh], Kosten in EUR. Die folgende Formulierung ist der unabhängige wissenschaftliche Maßstab, nicht ein behauptetes bitgenaues Abbild aller Antares-Modi.

Deterministischer Betrieb: min Σ_t w_t (c_g p_g + VOLL·ENS + c_spill·spill + c_start·u + …) bei Knotenbilanz, Kapazitätsgrenzen, Speicher-/Rampen-/UC-Restriktionen. Für elastische Nachfrage zusätzlich Nutzenfunktion (Wohlfahrt); Fixlast-Kostenminimum entspricht nicht automatisch jeder CBA-Nutzenrechnung.

Two-stage: min_{X∈𝒳} CᵀX + Σ_s π_s Q_s(X), Q_s(X)=min_{y_s} q_sᵀy_s, A_s y_s ≥ b_s−B_sX. X vor Szenariorealisierung, y_s Recourse. Benders-Master mit η_s und Schnitten η_s ≥ Q_s(X̄)+g_sᵀ(X−X̄); LP-Recourse, gültige Dualinformation und LB/UB-Gaps erforderlich. Integer-Master möglich; MILP-Recourse braucht andere nachgewiesene Verfahren. Infeasible Recourse, Lastabwurfpenalty, Kostenkonstanten und Gewichtung explizit.

Mehrperiodiger Ausbau: für Baumknoten k, X_k = X_parent + ΔX_k^+−ΔX_k^-; min Σ_k [P(k)·diskontierte CAPEX/Rückbau + w_k·(FOM·X_k + Q_k(X_k))]. Nichtantizipativität durch gemeinsame Vorgängerknoten oder Gleichheitsrestriktionen für Entscheidungen vor Informationsaufdeckung. Lifetime/Vintage, Bauzeit und Restwert als eigene Verträge. Dies ist von mehreren getrennten Zieljahrstudien zu unterscheiden.

Adequacy: EENS_n = Σ_s π_s Σ_t w_t ENS_{n,t,s}; LOLE_n = Σ_s π_s Σ_t w_t 1(ENS_{n,t,s}>ε). Ausfallstichproben und Wetterkorrelationen müssen unabhängig vom wirtschaftlichen Recourse korrekt erzeugt werden. Gleichverteilung nur wenn Studienvertrag dies erlaubt. Keine Gleichsetzung LOLE mit N-1.

NTC: −F^- ≤ f_l ≤ F^+, Knotenbilanz. Nodal DC: f_l=(θ_i−θ_j−φ_l)/x_l, KCL und KVL; eine Winkelreferenz je AC-Insel. PTDF/FBMC: Σ_z NP_z=0, H^z=H^nodal GSK, H^z NP ≤ RAM (alternativ Referenzoffset explizit), je CNEC/Orientierung/Zeit/Szenario. N-1/LODF nur unter gültigen Topologie-/Inselannahmen; NTC-Transport ≠ DC ≠ AC. DC-Approximation vernachlässigt Q, Spannungsbeträge, I²R-Verluste und nichtlineare Grenzen.

Storage: e_t=(1−λ_t)^{w_t}e_{t−1}+w_t(η_c p_c−p_d/η_d+inflow−spill). Lade- und Entladegrenzen separat; SOC-Ende zyklisch, fest, Zielband oder Terminalwert. Gleichzeitiges Laden/Entladen nur zulassen, wenn bewusst Teil des relaxierten Modells. UC: z_t binär/ganzzahlig, z_t−z_{t−1}=u_t−v_t, Pmin z_t≤p_t≤Pmax z_t, Mindestlauf-/Stillstandzeiten, Start-/Stop-Rampen, Initialstatus/elapsed time; Cluster-UC unterscheidet sich von Einzelblock-UC.

### 3.2 Implementierung und Grenzen je Schicht

Kürzel in Matrix: K = classic; M = standalone Antares Modeler; P = GemsPy; X = Xpansion; V = PyPSA-Konverter. Vollständige Statuscodes gelten jeweils für die genannte Funktion, nicht die gesamte Prozesszertifizierung. Für M/P bedeutet MODEL_EXTENSION, dass lineare Formulierbarkeit plausibel ist, nicht dass ein fertiges Modell validiert wurde.

| Capability / ESM-A-Bezug | K | M/P | X | V | Evidenz / wissenschaftliche Grenze |
|---|---|---|---|---|---|
| Deterministischer Dispatch, KCL, lineare Grenzkosten R013 | NATIVE | NATIVE | CONFIGURATION (Recourse) | NATIVE (Subset) | D/C/T, Hybrid-CI ausgewählte Fälle; exakte Objective-Konstanten prüfen |
| Monte-Carlo-Wetter/Ausfälle R009/011 | NATIVE | CONFIGURATION (bereitgestellte Zeit-/Szenariodaten), Generator der Stichproben EXTERNAL_COUPLING | CONFIGURATION (Recourse-Gewichte) | CONFIGURATION (bestehende PyPSA-Szenarien) | Legacy [outputs](https://antares-doc.readthedocs.io/en/latest/reference/outputs/); GEMS scenario builder; keine allgemeine neue Ausfallmodellbibliothek nachgewiesen |
| LOLE/EENS R011 | NATIVE (klassischer Adequacy-Ausgabepfad) | MODEL_EXTENSION/EXTERNAL_COUPLING (Auswertung) | CONFIGURATION (Adequacy-Kriterium) | EXTERNAL_COUPLING | D/C für Grundmechanismus; Threshold/gewichtete Statistik und Konvergenz qualifizieren |
| Two-stage / gemeinsame Kapazität R010 | EXTERNAL_COUPLING (X) | NATIVE für szenarioindizierte Extensive-Form in P, M Master/Subproblem-Build; X-Kopplung | NATIVE | NATIVE im begrenzten Investitionspfad | C/T; gleiche vs ungleiche Gewichte unterscheiden; keine allgemeine Stochastikfreigabe |
| Benders LP-Recourse R010/040 | EXTERNAL_COUPLING | M: NATIVE Build, EXTERNAL_COUPLING Solve; P: EXTERNAL_COUPLING BendersRunner | NATIVE | CONFIGURATION | C/T; kein Nachweis echter Integer-Recourse |
| Mehrperiodige Investitionspfade R003/004/007/040 | EXTERNAL_COUPLING | MODEL_EXTENSION/EXTERNAL_COUPLING | NATIVE (Trajectory) | NOT_SUPPORTED für investment_periods | C/D; separate Lifetime-, Vintage- und Nichtantizipativitätsprüfung |
| Investitionskosten und Kandidaten R003/044 | EXTERNAL_COUPLING | CONFIGURATION / MODEL_EXTENSION | NATIVE | NATIVE teilweise (p_nom/e_nom) | C; passive-only Xpansion-Routing-Lücke, CAPEX-FOM-Semantik |
| UC (Integer, Start/Stop, min up/down) R014 | NATIVE/CONFIGURATION (Modi, Cluster) | NATIVE (legacy thermal / UC-Tutorial, LP/MIP-Konfiguration) | NOT_SUPPORTED für gewöhnliche LP-Benders-Recourse mit ganzzahligen Betriebsvariablen; externe/relaxierte Alternative | NOT_SUPPORTED | C/D/T; Generator committable explizit abgewiesen, Link committable nicht sicher abgewehrt |
| Rampen R014 | CONFIGURATION (Ramping-Matrix) | CONFIGURATION/MODEL_EXTENSION | CONFIGURATION bei linearer Recourse | NOT_SUPPORTED für Standardexport | C: LinearProblemMatrixRamping.cpp; Register lässt Rampen aus |
| STS / Reservoirs / Hydro R015 | NATIVE | NATIVE (basic/legacy/pypsa) | CONFIGURATION | CONFIGURATION (zyklischer Subset) | C/T; Legacy Hydro Preallocation ≠ monolithische Jahresoptimierung, Speicherladegrenze-Befund |
| Saisonal übergreifende Zeitkopplung R008/015/041 | CONFIGURATION/UNVERIFIED je Block-/Hydrovertrag | CONFIGURATION (voller Horizont/Frontal) oder MODEL_EXTENSION (Terminalbedingungen) | MODEL_EXTENSION/EXTERNAL_COUPLING bei Kopplung über Subprobleme | NOT_SUPPORTED für ungleiche Snapshot-Weights; cyclic only | Keine automatische SOC-Fortschreibung über unabhängige Wochen |
| NTC und kontrollierbare Links R016 | NATIVE | NATIVE | CONFIGURATION | NATIVE für 2 Ports | D/C; Richtungs-/Verlustsemantik prüfen, Link ist nicht passive AC-Leitung |
| KVL/Kirchhoff/Loop flows R017 | CONFIGURATION (Binding Constraints) | NATIVE im pypsa_models library für line/transformer ohne PST | CONFIGURATION | NATIVE eingeschränkt | D/C/T; externe Koeffizienten bei classic; O: Dreieck |
| PTDF/FBMC/RAM/CNEC R018 | CONFIGURATION über Binding Constraints | MODEL_EXTENSION (lineare globale Portrestriktionen) | CONFIGURATION/EXTERNAL_COUPLING | NOT_SUPPORTED als automatische extra_constraints | D/C; Datenaufbereitung und GSK/Referenz-RAM extern; kein EU-Marktkopplungsprodukt nachgewiesen |
| PST R017 | CONFIGURATION (affine KL-Binding Constraints) | MODEL_EXTENSION für φ, Bereich/variable Phase | CONFIGURATION (passende lineare Recourse) | NOT_SUPPORTED im aktuellen Mapping | C/O; PyPSA v1.3.0 KVL enthält Phase, GEMS-Konverter-YAML nicht |
| AC-PF/AC-OPF/Verluste/Q/V R020 | EXTERNAL_COUPLING | EXTERNAL_COUPLING oder ENGINE_EXTENSION für echten NLP/AC | EXTERNAL_COUPLING | NOT_SUPPORTED | D/C; q-Ports/Spannungsmetadaten sind kein AC-OPF |
| SCLOPF/N-1 R021 | CONFIGURATION (vorgerechnete lineare Sicherheitsconstraints) / EXTERNAL_COUPLING | MODEL_EXTENSION + EXTERNAL_COUPLING | CONFIGURATION (gültige lineare Grenzen) | NOT_SUPPORTED als allgemeine SCLOPF-Übertragung | Keine automatische Kontingenz- und Inselvalidierung |
| Redispatch und Reserve R022/023 | CONFIGURATION (Reserve und Markt-Näherung) / EXTERNAL_COUPLING | MODEL_EXTENSION + AC EXTERNAL_COUPLING | CONFIGURATION bei linearer Kopplung | NOT_SUPPORTED für zusätzliche Restriktionen | Redispatch getrennt vom Marktmodell, keine automatische Geräterealisierung |
| CO2/primäre Energie R043 | CONFIGURATION (Binding Constraints/Parameter) | NATIVE / MODEL_EXTENSION (Port-Summen und Budget) | CONFIGURATION | NATIVE eingeschränkt | C/T; Generatoren, Stores/StorageUnits, nur primary_energy/co2/<=,==; kein allgemeiner Emissionsvertrag |
| EV V1G/V2G, Wärme/Kälte, Gas/H2 R027–034 | CONFIGURATION für voraggregierte Nachfrage/Storage-Proxies, sonst EXTERNAL_COUPLING | MODEL_EXTENSION, H2 electrolyser NATIVE | CONFIGURATION sofern lineares Modell/Recourse | CONFIGURATION nur zulässige 2-Port-/Storage-Abstraktion | siehe §4 |
| DSO, TSO-DSO, Stabilität R035–039 | EXTERNAL_COUPLING | MODEL_EXTENSION für lineare Envelopes, EXTERNAL_COUPLING für Physik | EXTERNAL_COUPLING / CONFIGURATION validierter Cuts | NOT_SUPPORTED als Vollmodelltransfer | keine automatische AC/DSO-/DAE-Simulation |
| Repräsentativtage/-wochen R041 | CONFIGURATION nur quellenkonforme Zeit-/Wetterstudien; kein allgemeines Cluster-SOC | MODEL_EXTENSION/CONFIGURATION, weights explizit | CONFIGURATION mit bewiesener Gewichts- und Kopplungssemantik | NOT_SUPPORTED für weights≠1 | kein implizites Ersetzen von w_t durch Szenariogewicht |

### 3.3 Classic Antares: entscheidende Details

- [Offizielle Optimierungsformulierung](https://antares-doc.readthedocs.io/en/latest/reference/optimization-problem/), [Optimization config](https://antares-doc.readthedocs.io/en/latest/reference/config-optimization/), [UC-Modi](https://antares-doc.readthedocs.io/en/latest/reference/config-advanced-parameters/): hydro-thermal Dispatch auf Wochen/Tagesblöcken; schnelle/genauere Relaxations-/Heuristikpfade nicht mit globalem MILP gleichsetzen. MILP-Modus und aktivierte Mindestleistung, min up/down, Rampen, Reserve separat ausweisen.
- [LinearProblemMatrix.cpp](https://github.com/AntaresSimulatorTeam/Antares_Simulator/blob/b5a88640fd3ecc74ed7be67b61f2e78c7850a05b/src/solver/optimisation/LinearProblemMatrix.cpp#L15-L56) konstruiert Binding, Hydro, Stock, Start-up, Rampen und Reserve-Gruppen; [Ramping](https://github.com/AntaresSimulatorTeam/Antares_Simulator/blob/b5a88640fd3ecc74ed7be67b61f2e78c7850a05b/src/solver/optimisation/LinearProblemMatrixRamping.cpp) mit Rate- und Variationsgruppen. Constraint-Dateien AreaBalance, ExchangeBalance, MinDownTime, NbDispUnitsMinBoundSinceMinUpTime, ShortTermStorageLevel u.a. im Tree identifiziert; nicht jede einzelne Gleichung vollständig auditiert.
- Hydro-Management monthly/daily sowie LP-Solverpfade im Quellbaum. [Hydro-heuristic](https://antares-doc.readthedocs.io/en/latest/reference/hydro-heuristic/) beschreibt Jahres-/Monats-/Tageszuordnung; Wasserwerte, Inflows, Reservoirgrenzen und Block-Endbedingungen getrennt prüfen. Stochastic inflow ≠ automatisch stochastischer optimaler Reservoirpolicy.
- [Flow models](https://antares-doc.readthedocs.io/en/latest/reference/flow-models/) und [Binding constraints](https://antares-doc.readthedocs.io/en/latest/tutorials/set-binding-constraint/): klassische Links ohne passende Zusatzrestriktionen haben keine erzwungene KVL. KVL und passive Loop-Flows können als Cᵀ diag(x) (f−f0)=0 eingegeben werden; PST als affine Korrektur. Lineare FB-Constraints auf Link-/Clustergrößen konfigurierbar, PTDF/GSK/RAM/CNEC-Berechnung und Datenhorizont extern. Quadratische Flow-Neuverteilung im Output ist nicht nachträglich ein AC-OPF oder ein Beweis korrekten Marktclearing.
- MC-Ausgabe mc-ind/mc-all mit gewichteter Aggregation, Stunden-/Tages-/Wochen-/Monats-/Jahresebene. Wetter- und Ausfallstichproben mit identischen Seeds/Playlist und korrelierten Daten für CBA-/Adequacy-Paare einfrieren. MC-Stichproben sind keine automatisch gemeinsamen Investments.

### 3.4 Xpansion und GemsPy: stochastische und zeitliche Architektur

[Annual investment theory](https://antares-doc.readthedocs.io/en/latest/reference/xpansion-theory/): annualisierte CAPEX, gewichtete Summe von Recourse-LPs, klassische Wochenprobleme, diskrete Kandidaten/zusätzliche Constraints. [BendersBase.cpp](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/src/cpp/benders/benders_core/BendersBase.cpp#L38-L248) prüft optimalen Master/Subproblem-Status, LB/UB, absolute/relative Gaps und Master-Integrität; [SubproblemWorker.cpp](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/src/cpp/benders/benders_core/SubproblemWorker.cpp#L15-L109) skaliert Objective mit slave_weight, fixiert Masterkopien per Bounds und liest LP-reduced-cost-Subgradienten. Das ist Codeevidenz für gewöhnliche Benders-Schnitte, kein allgemeines integer L-shaped Verfahren.

[Trajectory theory](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/docs/reference/trajectory-investment/index.md), [merge-master contract](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/docs/reference/trajectory-investment/merge-master.md), [TrajectoryInvestmentDriver](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/src/python/antares_xpansion/trajectory/driver_trajectory.py) und [MergeMasterMPS.cpp](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/src/cpp/benders/merge_master_mps/MergeMasterMPS.cpp): Zusammenführung jährlicher Masterprobleme, Elternknoten, Kandidatenkosten, initiale Kapazitäten, zusätzliche Trajectory-Constraints, Gewichtsmerge, Resolution. D/C, Testdateien trajectory_cleanup/input_translation entdeckt; keine eigene Ausführung. Dokumentation erlaubt zusätzliche Gleichheitsbedingungen über Kinderknoten für Nichtantizipativität vor Szenarioaufdeckung. Vollständige automatische Lifetime-/Vintage-, Bauzeit- und Restwertabbildung nicht nachgewiesen. [Adequacy criterion](https://github.com/AntaresSimulatorTeam/antares-xpansion/blob/9b509da96e1feeed6a99f80cc9b661cc515bdef7/docs/reference/inputs/adequacy-criterion.md): zonale maximale erwartete Verlustlaststunden mit explizitem ENS-Schwellenwert; nicht mit beliebiger ERAA-Kalibrierung gleichsetzen.

GemsPy [vectorized_builder.py#L395-L405](https://github.com/AntaresSimulatorTeam/GemsPy/blob/77100798fd4cc7fbb2889fc278b257d58c1f08bb/src/gems_runner/simulation/vectorized_builder.py#L395-L405): Expectation = Summe über scenario / Anzahl scenario, also ungewichteter Mittelwert; anderer Szenariooperator nicht implementiert. Nichtuniforme Gewichtung über explizite vorgegebene Koeffizienten oder externen gewichteten Master nur nach Modell-/Dekompositionsprüfung. [optim_config validation](https://github.com/AntaresSimulatorTeam/GemsPy/blob/77100798fd4cc7fbb2889fc278b257d58c1f08bb/src/gems_craft/optim_config/validation.py#L262-L316) untersagt Heuristik in Benders und exakte integer/binary in Subproblemen. [linearize.py](https://github.com/AntaresSimulatorTeam/GemsPy/blob/77100798fd4cc7fbb2889fc278b257d58c1f08bb/src/gems_runner/simulation/linearize.py#L113-L186) schützt vor nichtlinearen Variablenoperationen: Parameterfunktionen ≠ generischer NLP-Solver. Eine deklarativ ausdrückbare nichtlineare Formel bedeutet nicht ausführbare AC-Physik.

## 4. Bibliotheken und sektorale Detailanalyse

### 4.1 Verifizierte Modellbibliotheken, kein bloßes Marketing

GEMS HEAD enthält genau vier zentrale YAML-Bibliotheken im libraries-Verzeichnis. Versionen aus YAML-Headern bzw. explizitem Kompatibilitätsvertrag, nicht allein Release-Nummer:

| Bibliothek | Inhalt / Version | Reuse-Einschätzung |
|---|---|---|
| [basic_models_library.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/libraries/basic_models_library.yml) | 1.1.0 (COMPATIBILITY noch 1.0.1); bus mit ENS/spillage, load, link, renewable, generator, storage, emission_constraint, harte/weiche Energiegrenze | ADAPT für generische Dispatch- und Sektorknoten; Port-/Einheiten-/SOC-Konvention einfrieren |
| [antares_legacy_models.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/libraries/antares_legacy_models.yml) | 2.4.0; area, load, link, renewable, miscellaneous_generation, thermal, short_term_storage, long_term_storage | REUSE_AS_IS für unterstützte Legacy-Formulierungen nach Äquivalenztest; kein pauschaler Ersatz von Classic |
| [pypsa_models.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/libraries/pypsa_models.yml) | Kompatibilitätsmatrix 2.0.1; im Konverter tatsächlich eingebettete Library 2.0.1 separat geprüft | WRAP/ADAPT; Hash/Versionsgleichheit beider Kopien vor Verwendung prüfen; nicht stillschweigend aktuellste Bibliothek substituieren |
| [andromede_models.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/libraries/andromede_models.yml) | 1.0.0, RTE; flexible_load und electrolyser | REUSE_AS_IS für dokumentierten einfachen linearen Fall, ADAPT für echte Lastverschiebung/H2 |

Andromède-Details aus YAML: flexible_load: min_load≤load≤max_load, Kosten Σ(max_load−load)·marginal_flexibility_cost; keine explizite Rebound-/Gesamtenergie-/Prozesszustandsrestriktion. Elektrolyseur: 0≤power≤p_max(t,s), elektrische Portinjektion −power, H2-Port +η·power, konstante η. Keine Mindestlast, Rampen, Warmstart, Degradation, Wasser, Druck, Wärme-/O2-Kopplung oder Endnutzung im Modell selbst. Genau diese Trennung ist für sektorale Bewertung entscheidend.

Legacy-Konverter 0.5.2 beschreibt auch separate Investment-Candidates-Library 1.0.0, Hybrid-Ports für ENS-/spillage-Bounds, ausgelassene deaktivierte Thermal-/STS-Cluster, ViewsBuilder. [GEMS legacy-equivalence test source](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/tests/e2e_tests/test_antares_legacy_models_equivalence.py) identifiziert; keine pauschale Legacy→GEMS-Äquivalenz. Laut S6-Kompatibilität: Hybridkonversion kann scheitern, wenn konvertierte Objekte in Binding Constraints referenziert sind; Hybridrunner-Ausgabe ab 10.2.0 nicht gleich mc-ind/mc-all. Daten-/Resultatadapter daher separat qualifizieren.

### 4.2 Sektormatrix: Formulierung, vorhandener Reuse und verbleibende Lücke

Alle vorgeschlagenen zusätzlichen Gleichungen sind unabhängige Modellvorschläge, nicht als bereits vorhandene GEMS-Dateien ausgegeben. GEMS-Sprachniveau kann solche linearen Gleichungen ausdrücken; beide Interpreter und jede verwendete Dekomposition müssen dafür qualifiziert werden.

| Sektor/Funktion | Mathematischer Vertrag | Bestehender Reuse / Einstufung | Erforderliche Erweiterung / Falsifikator |
|---|---|---|---|
| EV unflexibel | vorgegebene p_EV(t,n,s), Jahresenergie und Spitzen aus Mobilität | classic load CONFIGURATION; GEMS load NATIVE | räumliche Ladeorte, Wetter/Temperatur, Fahrtenergie extern; keine Verschiebung |
| V1G | 0≤c_t≤a_t P_ch, e_t=e_prev+η_c w_t c_t−drive_t, SOC-Abfahrtsziel e_t≥e_req, e bounds | GEMS Storage/Load/Link ADAPT → MODEL_EXTENSION; PyPSA Store+Link-Subset nur wenn alle Mobilitätsrestriktionen erhalten | plug-in availability, Fahrtenergie, initial/terminal/route windows, Nutzerrestriktionen. Kein Laden bei a_t=0; Abfahrt muss erreichbar bleiben |
| V2G | zusätzlich d_t≤a_t P_dis, SOC-Abzug d/η_d, ggf. binary exclusivity, Durchsatzkosten | MODEL_EXTENSION; MILP-Recourse/Dekomposition gesondert | Fahrzeug-/Netzanschlussgrenze, V1G/V2G-Abgrenzung, keine doppelte Kapazität für Reserve; Negativfall simultanes Laden/Entladen |
| Wärmepumpe | q_heat=COP(t,s)·p_el, COP>0 als Zeitparameter, Wärmebedarfsbilanz | 2-Port Link mit zeitabhängiger Effizienz CONFIGURATION, GEMS MODEL_EXTENSION für echte HP; kein spezielles HP-Modell in vier geprüften Bibliotheken | Temperaturabhängigkeit, Vorlauftemperatur, Grenzlast, Backup, Defrost; variable COP abhängig von Entscheidungszustand → piecewise/ENGINE_EXTENSION |
| Thermischer Speicher | H_t=(1−λ)^Δt H_prev+η_c Q_inΔt−Q_outΔt/η_d, power/energy | generic Store/Storage CONFIGURATION/ADAPT | Speicherdauer, saisonale Kopplung, Terminalwert, Verlustmodell; bei Temperatur-/Schichtung physisch extern |
| Gebäude | C_th(T_t−T_prev)/Δt=UA(T_out−T_prev)+Q_HP+Q_solar+Q_internal, Komfortband | MODEL_EXTENSION (1R1C/mehrere lineare Zustände) | Wärmelast aus Gebäudezustand nicht gleichzeitig als fixe gleiche Last; initial T, Komfort/Belegung, Kalibrierung; B2G/Building-Engine extern |
| Wärmenetz | Knotenwärmebilanz, Verlust/Fluss/Leistung, Pumpstrom | MODEL_EXTENSION für Energieflussmodell; EXTERNAL_COUPLING für hydraulisch-thermische Netzphysik | Temperatur/Druck, Transportverzögerung, Netz-/Anschlusskosten, Rohrdimension/Abwärmestandort |
| Kälte | q_cold=EER(t)·p_el, Kältespeicher und Komfort/Prozessgrenzen | MODEL_EXTENSION / 2-Port CONFIGURATION | reversible HP, Wärmeabfuhr, gemeinsame Kapazität, ggf. multiport; keine Doppelzählung |
| H2-Elektrolyse | q_H2=η_el·p_el; bei LHV in MW_H2; Wasserverbrauch, Rampen/Min-Last bei Bedarf | Andromède electrolyser NATIVE für konstantes η, zweipoliger Link CONFIGURATION | echte technische Dynamik, H2/O2/Wärme als gemeinsam gekoppelte Ausgänge; MODEL_EXTENSION, Multiport-Konverter NOT_SUPPORTED |
| H2-Speicher/Rückverstromung | inventory, Lade-/Entladeverluste, Brennstoffzelle/Turbine, H2-Knotenbilanz | Store/Link CONFIGURATION (Subset) / MODEL_EXTENSION | LHV/HHV/ kg↔MWh konsistent, Druck/Kavernen-/Kompressorgrenzen, endogene Leistung/Energie |
| Gas/H2-Pipelines | zeitabhängige Kapazität, Richtung, Druck-/Verdichtungsrelation, linepack | MODEL_EXTENSION für transport-/inventory-Näherung; EXTERNAL_COUPLING für nichtlineare Hydraulik, Druck/linepack-Validierung | getrennte Carrier; Umstellung mit disjunkter Nutzung, Bau-/Umstellzeit, Leitungsidentität, Druck/Kompressorstrom; kein Weymouth-Solver verifiziert |
| Industrie/DSM | qmin≤q≤qmax, Produkt-/Energieerfüllung Σ_t q_t≥E_req, Produktionsspeicher, Rebound, Shift-Fenster, Opportunitätskosten | Andromède flexible_load NATIVE als Absenkproxy, MODEL_EXTENSION für zeitgekoppelte Flexibilität | Verzicht ≠ Shift. Gegenbeispiel: ohne Energieerhaltung verschwinden Produktions-/Lastmengen |
| CHP, e-fuels, CCS, Prozessketten | ein gemeinsamer Aktivitätsfluss a, Ports F_k=ν_k a (Input/Output mit Vorzeichen), ggf. Polytop für Wärme/Strom | GEMS MODEL_EXTENSION ohne zwingend neue Engine für fest-lineare Koeffizienten; V NOT_SUPPORTED multiport/process | mehrere unabhängige Links sind kein Ersatz für gemeinsame Ausbeute/Capacity; Rohstoff-/CO2-/H2-Massenbilanz |
| Verteilnetze | AC-OPF/branch flow: V², P,Q, Strom/Thermik, Trafo, Anschluss/Topologie | EXTERNAL_COUPLING für AC/unbalanced; MODEL_EXTENSION für validierte LinDistFlow/Polytope | Längs-/Quergradienten, Spannungsband, Q, Rückspeisung, simultane P/Q-Grenze; Line DC-KVL allein unzureichend |
| TSO-DSO | Knoten-/Trafoübergabe P,Q, Flex-Envelopes H_t p≤h_t plus SOC-/Energie-Zeitkopplung, aggregiertes Kostenmodell | MODEL_EXTENSION/EXTERNAL_COUPLING | disaggregierbarer Flexibilitätsnachweis, nicht doppelt verfügbare Flexibilität; AC-/DSO-Rückprüfung, Mapping je Netzanschluss |

**Folgerung:** Die eigentliche GEMS-Mehrleistung besteht in frei definierbaren Modellen, nicht in einem komplett vorhandenen PyPSA-Eur-Sektorportfolio. Für lineare Sektoren ist der Aufwand häufig Library+Converter+Tests, für nonlinear/hydraulisch/elektrische Netzphysik dagegen externe Fachengine. Eine separate Modellbibliothek für EV, Gebäude, Wärme/H2, Industrie und DSO-Envelopes ist sinnvoll, sofern Wiederverwendung des bestehenden PyPSA-Fachmodells zuvor geprüft wird.

## 5. PyPSA-Interoperabilität: konkreter Code-/Mathematikreview

### 5.1 Primäre Quellen und Datenfluss

Autoritative Konverterquelle ist die tatsächliche, gepinnte [COMPATIBILITY.md](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/COMPATIBILITY.md) zusammen mit:
- [pypsa_converter.py#L29-L193](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/src/pypsa_converter.py#L29-L193) (deepcopy vor solve, Szenario-/Investmentrouting, Solverbeschränkung, Hybridfenster);
- [pypsa_preprocessor.py#L53-L88](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/src/pypsa_preprocessor.py#L53-L88), [L161-L287](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/src/pypsa_preprocessor.py#L161-L287) (Checks, Fixierung, Carrier, Winkelreferenzen, dependent values);
- [pypsa_register.py#L27-L188](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/src/pypsa_register.py#L27-L188), [L215-L258](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/src/pypsa_register.py#L215-L258) (Whitelist der Attribute/Ports, CO2);
- [gems_model_builder.py](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/src/gems_model_builder.py), [gems_study_writer.py](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/src/gems_study_writer.py) (Instanzen, Port-Verbindungen, Zeitreihen, System/Parameter, Expansion-Weights);
- [eingebettetes pypsa_models.yml v2.0.1](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/resources/pypsa_models/pypsa_models.yml), [optim-config.yml](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/resources/optim-config.yml).
- Original PyPSA 1.3.0: [optimization/constraints.py, KVL](https://github.com/PyPSA/PyPSA/blob/0209b0ed0a29e7e373b92883e88999dac4dc85a1/pypsa/optimization/constraints.py#L1578-L1660), [StorageUnits](https://github.com/PyPSA/PyPSA/blob/0209b0ed0a29e7e373b92883e88999dac4dc85a1/pypsa/optimization/constraints.py#L2022-L2095).

Pipeline: unoptimiertes PyPSA Network → deepcopy → Szenarien normalisieren → Limitations prüfen → Namen/Carrier/Cap bounds/abhängige Werte → statische/dynamische Tabellen (Pandas→Polars) → Komponententyp-Whitelist → GEMS-Komponenten und Port-Connections → systems/input + model-libraries + data-series + parameters, ggf. optim-config und Xpansion/Hybrid-Studie. Identitäten werden umbenannt; stabile reversible ID-Map erforderlich (Präfix/Whitespace-Kollisionen prüfen). Keine Übernahme eines beliebigen n.model oder extra_functionality-Callbacks. Nicht aus vorhandenem netCDF auf Vorhandensein aller bei solve injizierten Constraints schließen.

### 5.2 Converter-Kompatibilitätsmatrix

S = syntaktisch exportierbar; M = mathematische Äquivalenz unter angegebenen Voraussetzungen; Solver = nachgewiesener/erwarteter Zielpfad; Numerik: T = Testdefinition; CI nur wo Log verifiziert; O = unabhängiges Orakel, keine Engine. REJECT = tatsächlich Codeabwehr, DROP = ignoriert/semantischer Verlust, HOLD = keine Freigabe. Bei M=conditional keine allgemeine Äquivalenz.

| Feature | S / tatsächliches Verhalten | M / Einstufung | Solver / Numerik |
|---|---|---|---|
| Bus/Load/Generator mit fixen Kapazitäten, linearen Kosten | ja; p_set für Load, p_min/max für Gen; fixe bounds; Gen-p_set nicht registriert | CONFIGURATION für reine ED, Gen-p_set nur wenn unbenutzt | Modeler HiGHS/andere passende LP; T; ausgewählte Hybrid-CI |
| Generator-UC | REJECT committable=True | NOT_SUPPORTED | GEMS thermal kann UC, V nicht |
| Generator-Rampen, Start/Stop-/Standby-Kosten, min up/down | DROP bzw. UC-Block nur für Gen | NOT_SUPPORTED | T der normalen ED beweist nichts |
| Generator/Link/Store/StorageUnit p_nom/e_nom extendable | ja, min/max; nicht extendable fixiert und capital_cost=0 | CONFIGURATION für zulässige einzelne Periode und lineare Kapazität; Objective-Konstanten/Cost-Basis prüfen | Investmentpfad nur coin/xpress; T; separate CI-Abdeckung offen |
| p_nom_mod/e_nom_mod, FOM/overnight/discount/lifetime | DROP (bei diesen Komponenten) | NOT_SUPPORTED | keine automatische Vintage-/Modulübersetzung |
| Link 2 Ports | bus0, bus1, efficiency, p_min/max, linear cap/cost | CONFIGURATION; Vorzeichen, negative flows, time/scenario-efficiency, losses, Carrier-Nachweis | LP, T |
| Multiport Link (bus2,3,… / efficiency2,3,…) | **DROP**, export akzeptiert potentiell | NOT_SUPPORTED, MODEL_EXTENSION + Converter ENGINE_EXTENSION | O CHP; fail-closed erforderlich |
| Process | DROP | NOT_SUPPORTED | keine Modellabbildung |
| Link committable/ramp/quadratic | DROP (Gen-UC-Guard schützt nicht Link) | NOT_SUPPORTED | Negativtests verpflichtend |
| Stores | e_nom, e_min/max, standing_loss, p, linear cost; cyclic zwingend | CONFIGURATION für zyklischen 1-h-Fall; e_set/Initial-/Periodenlogik nicht allgemein | T; Store mit separaten Links für power caps |
| StorageUnits | SOC, charge/discharge, max_hours, efficiencies, inflow/spill, cyclic; p_min_pu registriert, aber Modell nutzt p_max_pu auch für Laden | **HOLD** für asymmetrische Ladegrenze; CONFIGURATION nur nach expliziter Prüfung | O 2-h-Gegenbeispiel; T der üblichen Speicherfälle |
| nichtzyklischer SOC/Store | REJECT via Check | NOT_SUPPORTED | kein Terminal-/Initialvertrag |
| inactive Gen/Load/Link | REJECT, nicht einfach entfernt | NOT_SUPPORTED als ungefilterter Export | ValueError |
| inactive Line/Trafo/Store/StorageUnit | DROP active flag | NOT_SUPPORTED ohne kontrolliertes Preprocessing | Geänderte Topologie/Kapazität möglich |
| Lines/Transformers fix | ja x_pu bzw. x_pu_eff, Winkelport, bounds, s_max_pu | NATIVE eingeschränkt; AC-Inseln, taps, x≠0, base units prüfen | Modeler LP; T triangle, transformer; keine Ausführung dieser Testdatei im geprüften CI-Log |
| Line-/Trafo-Modularität | ja n_mod integer und s_nom_opt, s_nom_mod | NATIVE für direkte Formulierung, x konstant; parallele Netzverstärkung nicht automatisch x-Änderung | Modeler MILP T; **Xpansion-Autorouting/optim-config Lücke** |
| PST fixed/optimisable phase_shift | DROP | NOT_SUPPORTED; direkter Konflikt mit PyPSA 1.3.0 KVL | O 3-Bus; physikalisches Falsifikationsgate |
| s_nom_set | Dokumentation sagt behandelt; Code fixiert nur nicht extendable auf s_nom, explizite s_nom_set-Umsetzung im gelesenen Register/Preprocessor nicht gefunden | UNVERIFIED/HOLD wenn gesetzt | isolierter Test erforderlich |
| AC/DC Subnetze, Shunt | Topologiemetadaten teilweise ignoriert, shunt DROP | NOT_SUPPORTED für AC-PF bzw. DC-resistive/passive Sonderfälle nicht freigeben | keine Q/V-Lösung; H2 bus wird nur abstrakter Energieknoten |
| GlobalConstraint CO2 primary_energy <= oder == | ja Constraint-Objekt, emission_port contributors | CONFIGURATION für geprüften Scope, Generator p·emission_factor/η, zyklische Stores/SU netto 0; fehlende Carrier→null/0 Risiko | T und gesonderter scenario-factor-Test vorhanden; keine allgemeine CO2-Eur-Gleichheit |
| sonstige GlobalConstraints, tech capacity, budget, transmission volume, carrier growth | andere type/carrier REJECT über assert bzw. nicht registriert | NOT_SUPPORTED | zusätzlicher Modell-/Konvertervertrag |
| Snapshot weightings ≠1 | REJECT über Python assert | NOT_SUPPORTED | repräsentative Tage/Wochen nicht gleich Szenariogewichte |
| Investment periods | REJECT über Python assert | NOT_SUPPORTED | Xpansion Trajectory separat, kein automatisches Mapping |
| mehrere Szenarien, operative Studie, gleiche Gewichte | ja, Hybrid bei Vielfachen 168, GEMS systems bleibt | CONFIGURATION | CI 2/3/6 gleiche und unterschiedliche Profile |
| operative Studie, ungleiche Szenariogewichte | REJECT ValueError | NOT_SUPPORTED im Defaultpfad; GemsPy Expectation ungewichtet | CI negativer Test |
| investive Studie, ungleiche Szenariogewichte | schreibt yearly-weights, gemeinsame Kapazitätsvariablen | CONFIGURATION für geprüfte Typen; Gewichtsnormierung/Mapping, LP-Recourse | T two-stage objective/capacity; tatsächlicher Lauf dieser Datei offen |
| extra_functionality, n.model Linopy constraints, custom slack/reserve/CHP coupling/SCLOPF | keine allgemeine Übersetzung | NOT_SUPPORTED | expliziter Constraint-Registry nötig; O cap omitted |
| Kosten-/Solverstatus-/Dualgleichheit | output objective verfügbar; nicht alle Mappings | UNVERIFIED allgemeine Gleichheit | LP/MILP, degeneracy, objective constant, MIP gap, solver tolerance separat |

### 5.3 Kritische Befunde mit Priorität

| ID | Prio | Codebefund / Konsequenz | Minimaler Fix/Check (Entwurf, nicht implementiert) |
|---|---|---|---|
| G01 | P0 | Multiport/Process: Register nur bus0/bus1, keine Process-Registrierung. Erfolgreicher Export kann Wärme-/CO2-/H2-Produktfluss löschen. | UnsupportedFeatureLedger: jeden nichtleeren bus_k/efficiency_k, Process sowie custom variables/constraints aktiv ablehnen. Multiport-Modell mit gemeinsamen Aktivitätsvariablen und n-Ports ergänzen. |
| G02 | P0 | StorageUnit p_min_pu wird zwar registriert, [YAML L575–606](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/resources/pypsa_models/pypsa_models.yml#L570-L611) nutzt p_max_pu für p_store und p_dispatch. Für p_min_pu=−0.2, p_max_pu=1 wird eine Ladegrenze vergrößert. | Ladeobergrenze −p_min_pu·P, negative Vorzeichen und zeitvariable Grenzen prüfen; asymmetrischen Kleinstfall vor Fix und nach Fix testen. |
| G03 | P0 | PST: [YAML L401–413](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/resources/pypsa_models/pypsa_models.yml#L401-L413) f=(θ0−θ1)/x_eff, keine φ. PyPSA v1.3.0 explizit Cᵀ(xf+φ)=0. COMPATIBILITY nennt φ für DC-LOPF irrelevant, was für gepinnten PyPSA falsch ist. | Nonzero/optimisable phase sofort reject; später affine PST-Formel, radians/degrees/tap/Referenzzeichen und fix/variable Fälle qualifizieren. |
| G04 | P0 | [converter.py L29–39, L107–145] Lines/Transformers in _EXTENDABLE_CAPACITY_FLAGS auskommentiert. [optim-config.yml] nur generator/link/storage_unit/store. Branch-only investments werden nicht zum Xpansion-Workflow geroutet; bei gemischten Investments ist korrekte Master-Zuordnung der passiven Variablen nicht belegt. | separates CapType-Inventar inklusive Line/Transformer; Master/Recourse-Indexaudit. Direkte monolithische Modeler-MILP von Xpansion-Benders unterscheiden. |
| G05 | P0 | Inaktive passive Zweige/Speicher werden laut Mapping nicht gefiltert, Gen/Load/Link lösen ValueError aus. Damit kann Konverter Netzinseln/Dispatch verändern. | alle active/period availability explizit validieren; korrekt löschen oder reject unter Provenienz, Topologie-Neuberechnung. |
| G06 | P0 | zusätzliche Linopy-Constraints, nicht registrierte UC/Rampen/Dispatch-/SOC-Sets/Prozessgrenzen nicht serialisiert. | SolveSpecification mit erlaubtem Constraint-Registry und kompletter Model-Manifest-Differenz; unzulässige callback/constraints fail-closed. |
| G07 | P1 | Checks für investment_periods, snapshot_weightings, GlobalConstraint type/carrier via assert statt dokumentiertem ValueError; assert deaktivierbar. Fehlende Carrier werden teils auf null/0 abgebildet; Float-Sentinels/Clamping können mathematische Bounds verändern. | unbedingte explizite Exceptions; fehlende Werte und infinities typisieren, Range- und Cost-Audit; keine stillen Nullen. |
| G08 | P1 | fix-capacity helper nullt capital_cost bei nicht extendable, PyPSA Objective-Kostenterm/constant und FOM-Semantik müssen abgeglichen werden. | canonical objective decomposition (sunk, CAPEX incremental/absolute, FOM, OPEX, penalties, probability); keine Gleichheit allein über Gesamtwert. |
| G09 | P1 | Slack-Fallback in _add_bus_theta_bounds fixiert, wenn keine Slack-Busse gefunden werden, nur ersten AC-Bus global; Multi-Island/Szenario-Topologie und inactive flags nicht allgemein nachgewiesen. | pro zusammenhängender AC-Komponente/Topologie genau eine Gauge; kontrollierbare Links verbinden Winkel nicht. Gauged KVL und physische Flüsse getrennt testen. |
| G10 | P1 | GEMS- und Converter-Dokumentation version stale; CI-Testcollection enthält nur fünf Hybridfälle (siehe §6). | release-lock manifest, pytest collection audit; alle relevanten E2E-Dateien explizit ausführen; versionierte Regression. |
| G11 | P1 | Für operative mehrere Szenarien gleiche Gewichte vorgeschrieben; Hybrid-Studie nur bei T mod 168=0. Converter akzeptiert sonst systems-Export, aber kein Hybridartefakt. | Ausführungsprofil als Ergebnisfeld, erwarteter Pfad muss existieren; gewichtete expectation, 169-h-Gegenprobe. |
| G12 | P1 | Library bus enthält q-ports/Voltage-Metadaten, Register verbindet aktive Leistung, line/transformer verwenden DC angle. | Keine irreführenden AC-Claims; Netze nach AC/DC/HVDC/Sektoren getrennt kennzeichnen. |

P0 bedeutet Blocker für betroffenen Conversion-Scope, nicht automatisch für reine GEMS-/Classic-Studien. G03 ist durch Gegenüberstellung des gepinnten Quellcodes stärker als veraltete COMPATIBILITY-Behauptung. G04/G09 sind statische Routing-/Robustheitsbefunde; exakte Laufzeitwirkung an Fixtures noch nicht reproduziert.

### 5.4 Was von PyPSA-Eur tatsächlich wiederverwendbar ist

[GEMS PyPSA-Eur-Tutorial](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/getting-started/quick-start/pypsa-eur.md) konfiguriert FR, einen Cluster, planning_horizons [2050], minimalen electricity-Fall und kurzes Wetterfenster 2013-01-01 bis 2013-01-03 (end exclusive; Dokument nennt drei Tage, konkrete Konfiguration prüfen). Es verwendet GemsPy und eine spezielle Docker-Umgebung; [test_pypsa_eur_tutorial.py](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/tests/e2e_tests/test_pypsa_eur_tutorial.py) enthält Objective-Vergleich, kann fehlendes Network überspringen. Das ist **ein kleiner elektrischer Tutorial-Scope**, keine nachgewiesene full-sector EU-Network-Konversion, keine vollständige Reproduktion sämtlicher Snakemake-Constraints. Der konkrete PyPSA-Eur-Commit/Config/NetCDF/Notebook-Run ist nicht eingefroren und wurde hier nicht ausgeführt.

| PyPSA-Eur-Teilmodell | Urteil |
|---|---|
| einzelne Zieljahr-Stromstudie, Unit Weights, fix/linear Generatoren, NTC oder geprüfte passive Zweige | bevorzugter Positivkandidat nach Preflight |
| Netz- und Kapazitätsdatensätze, Wetterprofile, Kostenannahmen, räumliches Mapping | REUSE als Input, nicht automatisch als identische Optimierung |
| einfache 2-Port HP/Electrolyser/FuelCell und zyklischer Store | selektiv möglich, Einheiten/efficiencies/costs und alle zusätzlichen Constraints auditieren |
| EV-/Gebäude-Flexibilität, CHP/e-fuels/CCS mit mehreren Ports, CO2-Netze | GEMS Modell-/Konvertererweiterung oder explizit erzeugtes äquivalentes Teilmodell; nicht blind exportieren |
| zeitaggregiert, myopic/perfect-foresight multi-period, Vintage/Lifetime, custom policy/global constraints | nicht verlustfrei durch aktuellen Standardkonverter |
| voll integrierte PyPSA-Eur-Sektorstudie | HOLD bis tatsächliches Network + solve rules + alle Zusatzconstraints + solver results eingefroren und getestet sind |

PyPSA-Eur-Workflow und ein exportiertes PyPSA-Network sind verschiedene Artefakte. Optimierungsregeln in Snakemake/Python, postprocessing, Zusatzconstraints und Vorannahmen müssen als eigene Inputs in den gemeinsamen StudySpec gelangen. Kein Ersatz durch Umkodieren eines multiport Link in unabhängige 2-Port-Links ohne beweisbare gemeinsame Aktivität.

## 6. Vorhandene Tests und tatsächlich beobachtete CI-Evidenz

| Quelle | Testinhalt / beobachteter Stand | Aussagegrenze |
|---|---|---|
| [Converter end_2_end_tests.py](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/tests/e2e/end_2_end_tests.py) | T: Objective+constant Vergleich rel_tol 1e-6 für Generator/Load/Link, Emissionen, Store, StorageUnit; triangle, line_lp, line_milp, transformer_fixed/LP/modular, scigrid_de | Dateiname beginnt nicht mit test_; im überprüften Job nicht gesammelt. Testdefinition ist kein ausgeführter PASS. |
| [Converter two-stage tests](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/tests/e2e_2_stage_stochastic/test_2_stage_stochastic_study.py) | T: equal/unequal scenario weights, PyPSA CBC vs Xpansion, objective + constant, zwei Generator-Kapazitäten, OPTIMAL, weights sum=1; Binary prerequisite skip | in separatem Verzeichnis, nicht Teil des verifizierten CI-Befehls. Kein Nachweis tatsächlichen Laufs am HEAD. |
| [Hybrid comparison tests](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/blob/44d73886cf17040550508e88735e451e59a06d5c/tests/e2e/test_hybrid_study_comparison.py) | T/CI: equal 2/3/6 scenarios, verschiedene Szenariozeitreihen, reject unequal operational weights. PyPSA/GemsPy/Xpansion-Objective, rel_tol=1e-6. MPS-Rewrite über HiGHS für Coin orphan theta bounds im Testhelper. | keine vollständige Dispatch-/Residual-/UC-/Sektorgleichheit. Workaround selbst dokumentieren, kein stilles Produktions-MPS-Rewrite. |
| [Konverter Tests Run 44798819978](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/actions/runs/44798819978), [Job 136505721414](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter/actions/runs/44798819978/job/136505721414) | HEAD 44d738…, 20.11.2026, Ubuntu, Python 3.14.10; Unit- und E2E-Jobs erfolgreich. Log: zweimal uv run pytest tests/e2e/ -v -s …, jeweils collected 5 items, 5 passed, 16 warnings (10.64s/9.04s). Schritte bezeichnet Modeler 10.1.1 bzw. Xpansion 1.9.0, beide Binaries geladen. | **Nicht als zwei unabhängige vollwertige Test-Suites ausgeben**: identischer Testbefehl und gleiche 5 Tests. Zahl tatsächlich geprüfter unterschiedlicher Fälle = fünf, nicht zehn. |
| [GEMS UC/Investment Tutorial tests](https://github.com/AntaresSimulatorTeam/GEMS/tree/c463e30b610443c1f59b20074bb7acffa2844cce/tests/e2e_tests) | T: legacy equivalence, hybrid, UC, Investment mit/ohne Batterie, PyPSA-Eur; [Investment assertions](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/tests/e2e_tests/test_doc_tutorial_three_investment.py) gegen gespeicherte Objectives 517984.66667 und 493124.14493 EUR plus Kapazitäten | kein am GEMS-HEAD beobachteter vollständiger Testlauf; API nur Updatecheck erfolgreich |
| [GemsPy stochastic functional tests](https://github.com/AntaresSimulatorTeam/GemsPy/blob/77100798fd4cc7fbb2889fc278b257d58c1f08bb/tests/e2e/functional/test_stochastic.py) | T: szenariodependente/independente Thermal-Modelle, Modellzähl-/Strukturassertionen; [CI Run 45434431337](https://github.com/AntaresSimulatorTeam/GemsPy/actions/runs/45434431337) success am Release/HEAD | einzelne Tests/solver logs nicht vollständig auditiert |
| [Simulator Ubuntu CI](https://github.com/AntaresSimulatorTeam/Antares_Simulator/actions/runs/46017053853) und [Windows CI](https://github.com/AntaresSimulatorTeam/Antares_Simulator/actions/runs/46017054057) | HEAD b5a886… success (auch clang/sanitizer etc.) | Build-/CI-Status, keine spezifische Featurefreigabe |
| [Xpansion Ubuntu push build](https://github.com/AntaresSimulatorTeam/antares-xpansion/actions/runs/44288540229) success; [scheduled Ubuntu full build](https://github.com/AntaresSimulatorTeam/antares-xpansion/actions/runs/44990820152) failure; [Windows scheduled](https://github.com/AntaresSimulatorTeam/antares-xpansion/actions/runs/44983017039) failure | HEAD 9b509d…; Ubuntu failure im Configure-Schritt beobachtet | kein wissenschaftliches Versagen abgeleitet, Ursache nicht abschließend untersucht; Release- und Buildprofil vor Ausführung pinnen |

Keine upstream CI-Daten erzeugt, keine Testlogs als eigener Reproduktionsnachweis ausgegeben. Wichtig: Testcollection-Lücke zuerst beheben bzw. externen CI-Nachweis für genaue Testfälle beschaffen.

## 7. Prozess-Eignungsmatrix gegenüber ESM-A

Quelle für Prozessdefinition, Requirements R001–R050 und regulatorische Statusabgrenzung ist S8. Zusätzlich offizielle [IoSN-2026-Konsultation](https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/), [CBA-2026-Konsultation](https://consultations.entsoe.eu/tyndp/tyndp-2026-cba-imp-public-consultation/), [ERAA-Methodikrevision](https://www.entsoe.eu/eraa/methodology-revision/), [NEP 2037/2045](https://www.netzentwicklungsplan.de/nep-aktuell/netzentwicklungsplan-20372045-2025). Keine Behauptung, dass Drafts bereits verbindliche Finalmethodik darstellen. Die Einstufung bezieht sich auf die Funktion im Workflow, nicht auf formale regulatorische Konformität.

| ESM-A-Profil | Geeignete Antares/GEMS-Schicht | Capability / Eignung | Entscheidende fehlende Evidenz/Ergänzung |
|---|---|---|---|
| PR01 EU-Szenarien | GEMS/GemsPy mit externen Daten-/Sektormodellen | MODEL_EXTENSION / mittel | R001–009, R027–034/R043: Nachfrage-/Technologie-/Policy-Daten und Multi-Sektor-Kohärenz; kein fertiges Scenario Building |
| PR02 Strom-IoSN 2024 | classic + Xpansion | NATIVE/CONFIGURATION / hoch für definiertes Markt-/Investitionsproblem | exogene Erzeugungsannahmen, Kandidaten, NTC, Gewichte, offizielle Methodik; keine Projekt-CBA automatisch |
| PR03 Strom-IoSN 2026 | Xpansion + GEMS/Hybrid + externes TYNDP-Reduktions-/Netzmodul | CONFIGURATION/MODEL_EXTENSION/EXTERNAL_COUPLING / hoch für Kern, bedingt gesamt | R010/R017–019/R029: gemeinsame wettergewichtete Kapazität, Multi-Zonen, H2/Offshore, echte CNEC/PTDF/GSK; Investitions-/Kandidatenvertrag |
| PR04 Strom-CBA | classic/Xpansion für paarige Marktberechnung | CONFIGURATION + EXTERNAL_COUPLING / hoch für Market Core | R024–026/044/049 PINT/TOOT, Referenznetz/Reife, Projektgruppen, SEW/Verluste/SoS/andere Indikatoren separat; keine Doppelzählung |
| PR05 H2-CBA/IGI | GEMS H2 transport + Xpansion, Gasphysik extern | MODEL_EXTENSION/EXTERNAL_COUPLING / bedingt | R027–029, H2-/Gasnetze, Interlinkage, Stressfälle, Druck/Umstellung, Gegenfaktuale |
| PR06 ERAA | classic Monte Carlo, Xpansion/EVA-Modell | NATIVE/CONFIGURATION für Risiko, MODEL_EXTENSION/EXTERNAL_COUPLING für vollständige EVA / hoch für Kern | R011/045/049: korrelierte Stichproben, Konvergenz, wirtschaftliche Entry/Exit, genaue ERAA-Version |
| PR07 DE Szenariorahmen | externe Scenario-/Spatial-Daten, GEMS Modell | EXTERNAL_COUPLING / unterstützend | genehmigter Rahmen ist exogen; keine freie Erzeugungsoptimierung als Ersatz |
| PR08 DE NEP Strom | classic/GEMS Markt, TYNDP/AC-Redispatch extern | CONFIGURATION + EXTERNAL_COUPLING / hoch für Marktsimulation, nicht Gesamt-NEP | R017–023: physische AC/N-1-/NOVA- und Maßnahmenprüfung |
| PR09 DE NEP Gas/H2 | lineares GEMS-Netz + externer Gas-/H2-Solver | MODEL_EXTENSION/EXTERNAL_COUPLING / bedingt | R027/028, Druck/Kompressoren/linepack, Umstellung, Spitzenlast |
| PR10 SES/Langfristszenarien | GEMS/GemsPy + Xpansion trajectory | MODEL_EXTENSION/CONFIGURATION / strategisch interessant, bedingt | R003–007/027–037/043/044: sektorale Vollmodelle, vintages, Policy, Lebensdauer, Restwert und Regionalisierung |
| PR11 National Adequacy | classic MC | NATIVE/CONFIGURATION / hoch für Kern | deutsche/europäische Szenariokopplung, Stichproben/EV/Flex-Verträge, regulatorische Methodik |
| PR12 Netzreserve | Marktbaseline + AC-Redispatch/Reserve | EXTERNAL_COUPLING / unterstützend | R020–023, standortwirksame Reserve und Kontingenzen, kein NTC-Ersatz |
| PR13 Systemstabilität | externe AC/Dynamics/FlexPlan-Familie | EXTERNAL_COUPLING / nicht selbständig geeignet | R038/039, keine DAE- oder Frequenz-/Spannungsstabilitäts-Engine nachgewiesen |
| PR14 DSO/TSO-DSO | GEMS Flex-Envelopes + AC-DSO, gemeinsame Investitionslogik | MODEL_EXTENSION/EXTERNAL_COUPLING / bedingt | R035–037, räumlich-zeitliche Disaggregation, Q/V/Netzrestriktion und Doppelanrechnungsvermeidung |
| PR15 Wärmeplanung | GEMS Wärmebilanz + Building-/Wärmenetz-/GIS-Workflow | MODEL_EXTENSION/EXTERNAL_COUPLING / unterstützend | R032/033/037/050, Versorgungsgebiete, Netz-/Gebäudeeignung, lokales Potenzial/Investitionskosten |

Vollständige Traceability in Gruppen (alle ESM-A-IDs erfasst; methodische Einstufung, kein Rechtsnachweis):

| Requirements | Status für den integrierten Antares/GEMS-Workflow | Haupt-Gate |
|---|---|---|
| R001, R046 | CONFIGURATION + ENGINE_EXTENSION (Adapter-Preflight) | Source/StudyManifest, keine Defaults; G01–12 |
| R002, R004, R005 | CONFIGURATION; Brownfield und GF explizit | Asset-Bestand, Exogenität, Kostenbasis |
| R003, R006, R007, R040, R044 | NATIVE Xpansion/T*-Subset + MODEL_EXTENSION | Trajectory, Information Sets, Lifetime, Restwert; Gegenfaktualkosten |
| R008, R009, R041 | CONFIGURATION / EXTERNAL_COUPLING | Zeit-/Wetter-/Szenariokorrelation, SOC, Gewichte |
| R010, R012 | NATIVE LP-Benders / MODEL_EXTENSION für Risikoziele | gemeinsame x, gewichtetes Q, CVaR gesondert |
| R011, R045, R049 | NATIVE MC / MODEL_EXTENSION für EVA / CONFIGURATION für Sensitivitäten | LOLE/EENS/Seed/CI, EVA- und Konvergenzvertrag |
| R013, R014, R015, R016 | NATIVE / CONFIGURATION im jeweiligen passenden Pfad | ED/UC, Rampen/SOC/NTC; V nur Subset |
| R017, R018, R019 | CONFIGURATION / EXTERNAL_COUPLING | KVL/PST, PTDF/RAM, TYNDP-Aggregation; G03/G09 |
| R020, R021, R022, R023 | EXTERNAL_COUPLING; lineare Schnittrestriktionen CONFIGURATION | AC/N-1/Redispatch/Reserve-Replay |
| R024, R025, R026 | EXTERNAL_COUPLING + CONFIGURATION | gepaarte CBA/Gegenfaktuale, vollständige Indikatoren |
| R027, R028, R029 | MODEL_EXTENSION / EXTERNAL_COUPLING, Elektrolyse NATIVE | H2/Gas/Umstellung/Kompressor/LHV |
| R030, R031, R032, R033, R034 | MODEL_EXTENSION, einzelne Komponenten CONFIGURATION | EV-/Wärme-/Kälte-/Industrie-Flexibilitätsvertrag |
| R035, R036, R037, R047, R050 | MODEL_EXTENSION / EXTERNAL_COUPLING | DSO-Envelopes, physische Netz-/Raumzuordnung, Wärmegebiete |
| R038, R039, R048 | EXTERNAL_COUPLING | Stabilitäts-/Surrogat-Gültigkeit, unabhängige Replays |
| R042 | CONFIGURATION / NEW QA-Adapter | Benchmarks unten, eigener Engine-Nachweis fehlt |
| R043 | CONFIGURATION / MODEL_EXTENSION | CO2-Kohärenz, Multi-Carrier-/Policy-Vertrag |

## 8. Positive und negative Cross-Engine-Benchmarks

### 8.1 Minimalfälle und eigene mathematische Orakel

**Eigene Ausführung:** vorhandenes SciPy 1.17.0, scipy.optimize.linprog(method="highs"), kleine explizit aufgestellte LP-Matrizen, keine Bibliothek installiert. Alle nachfolgend mit O markierten LP-Arme lieferten Solverstatus 0 (optimal). Weder Antares, GemsPy, PyPSA noch Xpansion wurden ausgeführt. Damit sind die Sollwerte unabhängig numerisch kontrolliert, nicht die Konverterfehler zur Laufzeit reproduziert. Variablen/Einheiten in MW/MWh/EUR, Zeitschritt 1h, soweit nicht anders angegeben. Alle Daten synthetisch; bei degenerierten Flüssen nur zulässige Mengen bzw. Objective vergleichen.

| ID / Bezug | Eingaben / mathematisches Orakel | Sollwert / Negativarm | Geplanter Cross-Engine-Pfad |
|---|---|---|---|
| B01-P ED, ESM-A B01 | 2 Busse A/B, L_B=100, Gen_A cap100 c10, Gen_B cap100 c50, Link 60 lossless | O: p_A=60, p_B=40, f=60, J=2600 | PyPSA vs V→Modeler/P, classic NTC |
| B02-P KVL, ESM-A B02 | Dreieck AB, AC, BC mit identischer x, caps 100/30/100, A günstig c10, C teuer c50, L_C=100 | O: p_A=45, p_C=55, f_AB=15,f_AC=30,f_BC=15, J=3200 | PyPSA v1.3 vs V→Modeler, GEMS classic-binding KVL separat |
| B02-N Transport statt KVL | identischer Fall ohne f_AB−f_AC+f_BC=0 | O: p_A=100, f_AB=70,f_AC=30,f_BC=70, J=1000; KVL residual 110 MW (nach Division durch gemeinsames x) | FAIL, auch wenn beide Solver optimal melden |
| B03-P/N asymmetrischer StorageUnit, G02 | 2h, L=(0,10), Gen max10 je h, c=(0,50), cyclic lossless, max_hours=1, P=10, p_min_pu=−0.2, p_max_pu=1. Keine anderen Energien. | O korrekt max charge2: c0=d1=2, J=400; bei charge cap10: c0=d1=10, J=0. | V→Modeler/P muss korrekt 400 oder explizit REJECT liefern; 0 FAIL |
| B04-P/N two-stage weight, ESM-A B04 | gemeinsames k∈[0,10], CAPEX30/MW, low D=2, high D=10, free supply bis k, ENS100/MWh, π=(.9,.1) | O k=2, ENS=(0,8), J=140. Bei fälschlich gleichen Gewichten k=10, J=300. Gleichgewichtete Bewertung ist anderes Problem. | PyPSA direct vs Xpansion weighted, Benders vs Extensive Form; operation-only unequal weights REJECT |
| B05-N Multiport CHP, G01 | fuel activity a≤100 c10, Strom=0.4a, Wärme=0.5a; Demand E=40,H=50; unabhängiger Wärmeerzeuger c50 | O original a=100, boiler=0, J=1000; wenn Wärmeport ignoriert boiler=50, J=3500. | Preflight reject vor Mapping; Multiport-Erweiterung muss beide Portbilanzen erhalten |
| B06-P/N global CO2 oder extra constraint | 1 bus, demand100, dirty c10, clean c50; dirty ≤40 (1 t/MWh, budget40) | O p_dirty40, clean60, J3400; ohne Constraint J1000, dirty100. | CO2 primary_energy-Positivfall; mathematisch gleiche extra_functionality als Negativfall, nicht aus .nc rekonstruieren |
| B07-N PST, G03 | B02 mit affine cycle f_AB−f_AC+f_BC=15 MW (definierter Vorzeichenvertrag φ_AC/x=15, andere φ=0, x gleich) | O mit PST p_A=52.5,p_C=47.5, flows 22.5/30/22.5, J2900; φ ignoriert J3200. | PyPSA KVL vs V, REJECT oder nach Fix Sollwert; PST-Winkel in rad prüfen |
| B08-N inactive line/Storage | B02 mit AC inactive; AB,BC je100, C load100; kein Phantomzweig | analytisch p_A=100 über AB+BC, J1000; bei aktiver AC fälschlich J3200. Separate inaktive Batterie im B03-Setup: J500, keine SOC/dispatch decision. | Preflight/Topology-Manifest, nicht bloß Objective |
| B09-P/N Unit Commitment, ESM-A B09 | 2h, D=(0,1), unit G cap2, min stable1, start100, marginal0, initial off; alternative OPEX60/MWh. | analytisch UC: alt=1, J60; relaxed economic dispatch G=1, J0. Zusätzliche min-up/ramp-Fixtures. | Classic MILP und GEMS UC, V Generator committable REJECT, Link-UC nicht still ignorieren |
| B10-N snapshot weights / SOC | 2h mit Δt=(2,1)h; feste p=(1,−2)MW, lossless, SOC zyklisch | analytisch Energie ΔE=0, bei weights=1 ΔE=−1 MWh; unzulässiger Export ablehnen | V explicit reject auch Python -O; GEMS explizite Dauer-Koeffizienten prüfen |
| B11-P/N MC LOLE/EENS | 2 scenarios, weights .75/.25, ENS low=(0,0), high=(0,4) MW, 1h, ε=0.1 MW | analytisch LOLE=.25 h, EENS=1 MWh; ungewichtet .5 h /2 MWh | Classic weighted playlist, independent reducer |
| B12-P/N multiperiod trajectory, ESM-A B11 | k0=0, two periods 2030/2040, demand 1 then 2, cost build=1/MW each, no retire, availability exact, common build | analytisch build=(1,1), installed=(1,2), CAPEX2; independent per-year build (1,2) doubles previously installed; branches with same parent require pre-information equality | Xpansion annual+trajectory, independent LP; V investment_periods REJECT |
| B13-N AC/DSO, ESM-A B10 | 2-bus radial, voltage/reactive restriction nonbinding in DC but violated by AC; same feasible P balance, explicit Q/V/impedance, fixture numeric values to be frozen at next gate | expected fail of AC validation despite LP optimum; not yet numeric fixture | external pandapower/PowerModels/OpenDSS; no DC→AC PASS |
| B14-N incomplete time horizon | 169 snapshots, ≥2 scenarios; ordinary converter writes systems but no companion full-week Hybrid study | code-derived expected no hybrid, V must report not runnable for requested hybrid path | contract/file existence/length check |
| B15-N passive-only expansion | meshed/radial capacity expansion only Line/Transformer with positive capex, gen capacities fixed | code-derived _has_extendable_capacity false, despite nominal decision variable in YAML; reject Xpansion claim | direct Modeler LP/MILP vs Xpansion route artifact assertion; mixed capacity case also required |

B13 explicitly design-only: complete AC fixture still missing, not claimed executed. B09/B10/B11/B12 analytical, B14/B15 source-derived, B01–B07 independent LP calculations as described. For B03, time-zero SOC gauge may have multiple optima, objective and energy delta/charging decisive. Negative arms deliberately violate one model-contract dimension; they are not tool runs.

### 8.2 Reproducible small LP oracle definitions (executed)

The following compact Python reconstructs the executed independent matrices. Input order is explicit; no converter or solver installation. This block is report documentation, not a change to production code.

    import scipy
    import numpy as np
    from scipy.optimize import linprog
    print(scipy.__version__)
    def lp(c, eq, rhs, ub=None, br=None, bounds=None):
        r = linprog(c, A_eq=eq, b_eq=rhs, A_ub=ub, b_ub=br,
                    bounds=bounds, method="highs")
        assert r.status == 0
        print(round(r.fun, 8), np.round(r.x, 8))
        return r
    # ED: gA, gB, fAB
    lp([10,50,0], [[1,0,-1],[0,1,1]], [0,100],
       bounds=[(0,100),(0,100),(0,60)])
    # KCL and optionally KVL: gA, gC, fAB, fAC, fBC
    for rhs in (0, None, 15):
        A = [[1,0,-1,-1,0],[0,0,1,0,-1],[0,1,0,1,1]]
        b = [0,0,100]
        if rhs is not None:
            A += [[0,0,1,-1,1]]
            b += [rhs]
        lp([10,50,0,0,0], A,b,
           bounds=[(0,100),(0,100),(-100,100),(-30,30),(-100,100)])
    # Storage: g0,g1,charge0,discharge1,e0,e1
    for cmax in (2,10):
        lp([0,50,0,0,0,0],
           [[1,0,-1,0,0,0],[0,1,0,1,0,0],
            [0,0,-1,0,1,-1],[0,0,0,1,-1,1]], [0,10,0,0],
           bounds=[(0,10),(0,10),(0,cmax),(0,10),(0,10),(0,10)])
    # CHP: a,heat backup
    for eta_h in (.5,0):
        lp([10,50],[[.4,0],[eta_h,1]],[40,50],
           bounds=[(0,100),(0,50)])
    # CO2/callback: dirty,clean
    for cap in (40,100):
        lp([10,50],[[1,1]],[100],[[1,0]],[cap],[(0,100),(0,100)])
    # Investment: k,ENS_low,ENS_high
    for w in (.9,.5):
        lp([30,100*w,100*(1-w)],None,None,
           [[-1,-1,0],[-1,0,-1]],[-2,-10],[(0,10),(0,2),(0,10)])

### 8.3 Abnahmevertrag, bevor Ergebnisgleichheit behauptet wird

1. StudySpec-ID + canonical source SHA + data hash, library hash, converter/interpreter/solver pins, objective basis, t/s weights, clocks/units, exact active topology, investment and information structure, exact custom constraints. Reject missing/unsupported.
2. Structural diff: components/ports per canonical ID, mapped bounds and coefficients, constraint counts and sparsity normalized (elimination allowed only with certificate), MPS/LP objective constants, integer domains, scenario/clock dimensions. Feasible sets must be equivalent modulo declared auxiliary variables.
3. Solver: both optimal (or same appropriately certified infeasible/unbounded status); LP tolerances documented, MIP incumbent/gap both; no pass on timeout. Default proposed small-case tolerance abs objective 1e-5 EUR, rel 1e-6, power/energy residual ≤1e-6 max(1, scale) in units, KVL radians with pu-base, integer violation ≤1e-6. Final project gate may tighten/change these proposed tolerances.
4. Compare objective decomposition, capacities, balances/flows/SOC/CO2/ENS, not only scalar objective. Degenerate primal solutions: compare objective, feasibility, agreed invariant quantities, and reference optima sets; duals only for matching LP basis/conventions and appropriate degeneracy analysis, not MILP price equivalence.
5. Independent replay of original physical topology and all constraints. Separate EENS/LOLE, scenario weights, outage mapping, AC/DSO feasibility. Negative cases must fail closed with typed cause, not produce misleading optimal output.
6. Evidence states: NOT_RUN / UNSUPPORTED / INPUT_REJECTED / ENGINE_FAILURE / COMPARED / NUMERICAL_PASS / PHYSICALLY_VALIDATED / INDEPENDENT_REPRODUCED / OWNER_ACCEPTED. "compared" alone is not PASS. For synthetic test campaign propose ≤15 cases × ≤3 engines, one thread, small problems and ≤60 s per solve; no large real-world campaign authorized.

## 9. Reuse-first, Power-Agent-Workflow und Architekturvarianten

### 9.1 Power-Agent-Projektregeln

Owner-supplied Library rules consulted: 01_CHATGPT_PROJEKTHINWEISE_POWER_AGENT_V1.md (17.11.2026), 02_ARCHITEKTUR_UND_WORKFLOW_ENTSCHEIDUNGEN_V1.md, 04_MASTER_PROMPT_POWER_AGENT_REUSE_FUER_ALLE_PROJEKTE_V1.md (einschlägige Retrieval-Auszüge) und PowerAgent_Wissensbasis_Architekturreview_2026-11-17.md (Auszüge). Vorrang Wissenschaft → Originalquellen → Reuse → Vertrag → unabhängige Tests. GitHub-AGENTS.md aus S1–S5 gelesen bzw. relevante Auszüge gelesen, Repo-Root-Sichtung; Zielrepo main enthält keine AGENTS.md/CURRENT_*-Dateien im geprüften Tree, README und ESM-A-Handoff geprüft. Keine fremden Skill-Anweisungen als Ausführungsfreigabe behandelt. Power-Agent-Organisation neu inventarisiert: genau sechs öffentliche Repositories, folgende aktuelle HEADs bestätigt.

| Quelle/Pin | Konkreter Reuse-Befund | Entscheidung und Grenze |
|---|---|---|
| [PowerWF](https://github.com/Power-Agent/PowerWF/tree/a3c437146e7263a45db940edc5e4c66a4cd170cf) a3c437146e7263a45db940edc5e4c66a4cd170cf | [cross_engine_validation/workflow.py](https://github.com/Power-Agent/PowerWF/blob/a3c437146e7263a45db940edc5e4c66a4cd170cf/cross_engine_validation/workflow.py), [test](https://github.com/Power-Agent/PowerWF/blob/a3c437146e7263a45db940edc5e4c66a4cd170cf/tests/test_cross_engine_validation.py): identical detached StudySpec, two independent endpoints, explicit failures, raw results, comparator callback. Fake endpoints test isolation, not real solvers. Grid Impact Evaluation and Electricity Market Expert README, B2G-Agent role model read. | ADAPT: energy-system StudySpec and objective/constraint comparator (not trajectory RMSE). Use separate engine result artifacts and owner gates. Workflow license/API check before code reuse; no copying now. |
| [PowerAgentBench](https://github.com/Power-Agent/PowerAgentBench/tree/77fe638482af94dd20ce28bfa4301658660d283d) 77fe638482af94dd20ce28bfa4301658660d283d | README and [steady_state_agentic.py](https://github.com/Power-Agent/PowerAgentBench/blob/77fe638482af94dd20ce28bfa4301658660d283d/poweragentbench/steady_state_agentic.py): independent DC PF, island penalty, budgets, deterministic baseline, PTDF/LODF; RestoreBench for AC. | ADAPT benchmark method; NEW energy-system LP/MILP/CO2/SOC/Benders/FBMC cases; existing benchmark not general cross-engine sector equivalence. |
| [PowerSkills](https://github.com/Power-Agent/PowerSkills/tree/636102954ff9522e7b161cbb2e3863746afa78cc) 636102954ff9522e7b161cbb2e3863746afa78cc | [PyPSA SKILL](https://github.com/Power-Agent/PowerSkills/blob/636102954ff9522e7b161cbb2e3863746afa78cc/powerskills-tool/skills/pypsa/SKILL.md) ladder load→inspect→PF→dispatch→investment; operations/contingency/DER playbooks catalog; Egret, OpenDSS, pandapower, potpourri as future cross-checks. | ADAPT escalation; no installation, no tool-side changes. For pure sector model, use balances before electrical PF. MIT per README, exact files verify before copying. |
| [PowerMCP](https://github.com/Power-Agent/PowerMCP/tree/10dbd9a8ef81bbf0e1c790ba4faca25e7f1af336) 10dbd9a8ef81bbf0e1c790ba4faca25e7f1af336 | updated pin since 18.11; README and [PyPSA adapter README](https://github.com/Power-Agent/PowerMCP/blob/10dbd9a8ef81bbf0e1c790ba4faca25e7f1af336/PyPSA/README.md) provide inspect/solve/optimization tools, PyPSA >=0.35.2,<2. PowerIO listed; pandapower and OpenDSS candidates. Antares/GEMS native adapter not established. | WRAP direct libraries first; only use MCP if needed. PowerIO is not proof of sector/temporal/port/constraint preservation. MIT per README; current live adapter code not exhaustively audited. |
| [PowerFM](https://github.com/Power-Agent/PowerFM/tree/4c6e9b3dd1e035d7abf8c526b2947380b6667fa3) 4c6e9b3dd1e035d7abf8c526b2947380b6667fa3 | optional ML screening/warm-start research, no need to evaluate further for mathematical converter equivalence | NOT_APPLICABLE to current core; optional later only with OOD/physical validation |
| [power-agent.github.io](https://github.com/Power-Agent/power-agent.github.io/tree/9e47948d155278c5dc7ccb059ff8ac887b2ab7a8) 9e47948d155278c5dc7ccb059ff8ac887b2ab7a8 | community/navigation | NOT_APPLICABLE as mathematical authority |

PowerMCP README/source interface existence is not deployment readiness; no MCP invocation or external solver run. No hidden benchmark oracle files used. Proposed G0 authority and pins → G1 exact formulation + unsupported ledger → G2 adapter/unit tests → G3 independent structural/LP/MILP comparisons → G4 real-data scenario test (separate approval) → G5 AC/DSO/gas replay → G6 independent reviewer → G7 Owner gate/release. Role split: specification/implementation/review/owner; reviewer must independently execute if R claimed.

### 9.2 Reuse-/Gap-Matrix for implementation planning

| Source | Reuse target | Missing work / risk | Decision |
|---|---|---|---|
| S1 classic | MC adequacy, zonal dispatch, hydro, binding constraints | time/UC/MC profile, version pins, explicit network physics separation; MPL | REUSE_AS_IS + WRAP |
| S2 library | bus/link/GEN/storage/thermal/emissions/electrolyser | sectoral states, multiport, semantics/units, compatibility and MPL | ADAPT |
| S3 GemsPy | programmatic construction, LP export/inspect, frontal solves | expectation weighting, solver profiles, independent result contract; MPL | WRAP/ADAPT |
| S4 Xpansion | weighted stochastic investment, candidate and trajectory merge | lifetime/lead time/NA, Recourse restrictions, failed scheduled build profile; Apache-2.0 | REUSE_AS_IS + WRAP after qualification |
| S5 converter | existing .nc→system/series/port mapping and model library | G01–G12, silent drops, version drift, testcollection, model equivalence; MPL | WRAP fail-closed first; ADAPT only targeted gaps |
| S6 legacy converter | historical study reuse, existing hybrid components | binding-constraint/reference compatibility, output contract, exact model versions; MPL | WRAP |
| S9 TYNDP_Products | aggregation, technology PTDF/GSK, N-1, FBMC bridge, weather-year methodology | real-source scope and physical replay; no new authority or merge | REUSE_AS_IS within validated scope, ADAPT interfaces |
| PowerWF / Bench | cross-engine state machine, deterministic comparator, resource budget | domain-specific objective/constraints and physical oracles, licensing | ADAPT |
| Missing adapter | typed StudySpec, loss ledger, result normalization, CBA paired run | no existing one-stop workflow proven | NEW thin modules; no new optimization engine |
| External network engines | AC/PF/Redispatch, DSO/hydraulics, stability | choose from separate ESM reviews; do not assume installed/validated | EXTERNAL_COUPLING / WRAP |

### 9.3 Architecture options for the final comparison

| Variant | Design | Strengths | Limitations / effort |
|---|---|---|---|
| A Classic-first | Legacy Antares market + Xpansion; TYNDP network/FBMC adapters; external detailed grid; fixed sector inputs | high reuse, MC/hydro, recognizable planning workflow; small implementation scope | sector flexibility largely external/aggregated; no general multiport or fully integrated DSO |
| B GEMS-first | Canonical GEMS library and system, GemsPy / Modeler alternative execution, Xpansion investment, Legacy import | modular sector models and two interpreter paths; declarative contracts; extensible LP/MILP | must build/validate missing sector models, weights, compatibility and data tooling; risk of premature migration |
| C PyPSA-first + selective GEMS bridge | canonical PyPSA/PyPSA-Eur inputs/solve rules, fail-closed V conversion for subset, independent GEMS execution/compare, Xpansion separate | immediate reuse of sector workflow and data; falsifiable cross-engine reference; no wholesale rewriting | conversion loss risk, custom constraint adapter, multi-period and multiport gap, separate solver/version maintenance |
| D Federated process-based | shared StudySpec/Asset/Time/Scenario/Network/Constraint/Result contracts, independent classic/GEMS/PyPSA/other process engines, detailed grid validation as separate modules | matches ESM-A; preserves specialization, avoids format lock-in and false equivalence | requires disciplined semantic interfaces and independent comparison; no magical single optimum across sectors |

**Recommendation for next gate:** D as overall architecture candidate, **A + C as low-risk pilot tracks** (pure electric scoped subset); B as strategic research track only where GEMS portability and flexibility demonstrate measurable benefit. Keep PyPSA, GEMS YAML and physical network models as explicit engine-specific representations, not three competing canonical truths. Prefer reuse of upstream libraries, thin data adapters and targeted contributions rather than a fork. Final selection awaits ESM-C/D and independent comparative benchmark results; this is not an Owner architecture freeze.

Proposed contracts: StudySpec (process/methodology/draft status, snapshot durations, scenario probability/info), AssetIdentityMap (canonical IDs, existing/candidate, lifetime and location), PortContract (carrier, MW/MWh/kg, LHV/HHV, sign, conversion), NetworkConstraintSet (topology SHA, AC/DC/HVDC, x/base/phase, PTDF/GSK/CNEC/RAM), TimeSeriesManifest (clock, missing/assumed, units), OptimizationContract (variables, domains, bounds, objective/constant, custom constraints, decomposition), ConversionLedger (supported/mapped/rejected/assumed with source path), ResultBundle (raw + canonical, status, residuals, dual validity, engine/version/data pins), CounterfactualPair (baseline/project/allowed diff, common seeds), ACValidationBundle (P/Q/V/θ, contingencies, redispatch, disaggregation). No "missing→0" rule.

## 10. Open risks, decisions, and next authorized steps

- **HOLD for general PyPSA-Eur conversion:** G01–G06 must be fail-closed; no silent approximation. Qualify version matrix and CI collection G07–G12. Only admit feature-by-feature positive tests with explicit negatives.
- **HOLD for exact sector-coupled production parity:** no actual full PyPSA-Eur case/solve-rule manifest, no complete GEMS sector library for EV/building/heat/cooling/industrial/multiport, no end-to-end AC/DSO or gas/H2 physical replay. Linear abstractions may be qualified separately.
- **HOLD for combined latest-version stack:** upstream compatibility pin differs from newest releases. Converter test profile (PyPSA 1.3.0, Antares 10.1.1, Xpansion 1.9.0, converter-dev GemsPy 0.1.3) is a starting point, not a universal lockfile. GemsPy 0.4.0 and Antares 10.2.1 need separate version-matched tests.
- **HOLD for full CI assertion:** observed CI E2E only five hybrid cases, not the broader test definitions. Pin and run exact tests in next authorized campaign; inspect full unit tests, Benders and Legacy equivalence logs as separate tasks.
- **Xpansion Trajectory:** meaningful native architecture; test merged master, scenario node weights, nonanticipativity, candidate availability, retirement, discount, lead times and out-of-sample; do not assume support for arbitrary PyPSA multi-period or integer recourse.
- **Classic / Modeler / GemsPy distinction:** preserve weekly vs frontal horizon, stochastic information and solver semantics. No forced monolithic optimization when process requires separate market/physical runs. No new installation authorized.
- **Sources limitations:** no exhaustive audit of every branch, file, third-party library, solver license or RTE-internal production model; auxiliary organization repositories discovery only; several exact release-tag files not examined beyond reported spot checks. No independent Antares/GEMS/PyPSA execution. Public process fit derived against ESM-A pinned review, not new full legal review. Tiny LP oracles are the only own numeric results.
- **Chosen without explicit user instruction:** source authority = current upstream default HEAD for technical review and published tag separately; base branch = main pinned above, not ESM-A branch (independent handoff, ESM-A linked); folder convention follows ESM-A. Proposed tolerances, P0/P1 priority, pilot variants and test budget are recommendations, not approvals.

### 10.1 Next tasks (not executed)

1. ESM-B-R1: independently reproduce B01–B07 with exact version stack, both direct and converted cases, compare full normalized LP/MPS and physical residuals. Record all rejected features and collect test evidence for the actual test names.
2. ESM-B-V1: read-only design of fail-closed PyPSA converter adapter and explicit allowlist; fixture-based review of IDs, active, snapshot durations, caps, costs, multiport/Process, UC, PST, extra Linopy constraints. Only after owner gate implement targeted fixes or contribute upstream.
3. ESM-B-X1: scoped Xpansion two-stage weighted and trajectory tests; distinguish direct Modeler capacity expansion from Xpansion routing; verify LP recourse and master coupling. Annual/weather/investment periods separately.
4. ESM-B-S1: compare only necessary sector models with the PyPSA-Eur/Open-TYNDP/eGon reviews; prioritize shared model equations and data, no duplicated generic engine.
5. Central ESM gate: combine ESM-A requirement IDs with ESM-B/C/D evidence per function; require explicit decision and objective evaluation criteria (correctness, data quality, solver maturity, operational scale, reuse/licensing, extension effort). No weighted scoring until test evidence comparable.

## 11. Handoff verdict

**ESM-B SOURCE_REVIEW_COMPLETE_WITH_SCOPED_EVIDENCE / ENGINE_REPRODUCTION_NOT_RUN / GENERAL_CONVERSION_HOLD / OWNER_DECISION_PENDING.**

Use classic Antares for its qualified market and adequacy strengths; qualify Xpansion for weighted investment and trajectory; retain GEMS/GemsPy as a serious alternative modelling layer, not a turnkey sector-integrated replacement. The decisive work is proving semantics at the interfaces, not replacing all existing models. For the central ESM architecture, prefer process-specific engines plus shared contracts, positive/negative benchmarks, and explicit physical network validation.
