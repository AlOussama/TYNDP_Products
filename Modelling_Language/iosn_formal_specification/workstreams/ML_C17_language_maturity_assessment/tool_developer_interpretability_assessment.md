# ML-C17 — Tool-Developer Interpretability Assessment

**Art der Prüfung:** deduktives, KI-internes Implementer-Handover anhand gleicher RC01–RC12; **keine** tatsächlich unabhängig durchgeführte Entwicklerstudie, keine native Implementierung, kein Benchmark und keine Zertifizierung eines Frameworks.

## 1. Drei verschiedene Energie-Modellierungsparadigmen

**PyPSA / PyPSA-Eur:** netzwerk-/snapshotbasierte Modellierung mit Bus, Line, Link, Carrier und Storage sowie Optimierungsproblemkonstruktion, heute insbesondere Linopy. Dokumentation: https://docs.pypsa.org/latest/user-guide/network-optimization/ und https://docs.pypsa.org/latest/api/networks/optimize/ . Die Nutzung der im Tool vorhandenen Komponenten definiert nicht die IoSN-Mathematik.

**Antares Simulator:** Areas/Interconnections, MC-Zeitreihen, hydro-/betriebsbezogene Nebenbedingungen, eigene Modell- und Szenariodaten. Physische AC-/KVL-Repräsentation und steuerbare Interconnections müssen ausdrücklich voneinander getrennt werden. Dokumentation: https://antares-simulator.readthedocs.io/en/latest/user-guide/solver/02-inputs/ und https://antares-simulator.readthedocs.io/en/latest/user-guide/solver/05-model/ . Keine Behauptung vollständiger IoSN-Fähigkeiten in einer bestimmten Version.

**Sienna (PowerSystems und PowerSimulations):** typisierte Stromsystemgeräte und konfigurierbare Optimierungs- und Netzformulationsmodelle, inklusive spezifischer Sicherheitsrestriktions- und Speicher-/Hydroansätze. Dokumentation: https://sienna-platform.github.io/Sienna/SiennaDocs/docs/build/PowerSimulations/stable/tutorials/generated_security_constrained_reserves/ und https://sienna-platform.github.io/Sienna/SiennaDocs/docs/build/PowerSystems/stable/explanation/grouping_generators_into_plants/ . Eine vollständige IoSN-H2-Stage-OPF-Abbildung wurde nicht demonstriert.

## 2. Gleicher Contract — drei denkbare Entwicklungsinterpretationen

Alle Zellen sind **MAPPING_HYPOTHESIS / FRAMEWORK_NATIVE_UNCONFIRMED**. Die hier benutzten Toolobjekte sind Beispiele, keine garantiert direkt geeignete Featureliste für aktuelle Versionen.

| RC | PyPSA / PyPSA-Eur | Antares | Sienna | Zusätzliche Info/Kategorie |
|---|---|---|---|---|
| RC01 | Y×CY-Snapshot, external weight manifest, keine Wetterselektion | MC-Läufe/Areazugehörigkeit, CY-ID und shared w separat abbilden | Zeitreihen-/Scenario-/Forecast-Container auf eindeutige CY-ID binden | DATEN: externe CY-IDs und Werte; OWNER: Gewichtsnorm |
| RC02 | Linopy-investment Decision ohne CY oder repliziert mit Gleichheitskopplung | Unterscheide Portfolioentscheidung von MC-Dispatch und fixiere diese fachlich | investment vs dispatch separate Entscheidungszeitpunkte in Formulation | SPRACHE: Quantor/InformationStage; TOOL: native Formulierungswahl |
| RC03 | Line + KCL/KVL/Schlupf-Inseln; Flow versus controllable Link | physikalische Interconnection und Kirchhoff-Regeln gesondert modellieren | Netzgerät plus PowerFlowFormulation und KCL/KVL-Witness | DATEN: Topologie/PTDF/PST und CONTINGENCY; TOOL: angle/cycle |
| RC04 | steuerbarer Link + directional NTC statt passiver Line | candidate Marktlink-Wirkung mit AC/DC-Attribut nicht verwechseln | direktionale Transfer-/Interface-Restriktionen und Investmentwirkung | DATEN: NTC candidate map; SPRACHE: typed model_role |
| RC05 | mehrere getrennte Optimierungs-/Transformläufe für S1/S2/S3 | klarer Prozessmanager für fixe S1/zulässige S2 Entscheidungen | Mehrstufen-Programmkonstrukt und Transferidentität explizit | OWNER: MD-07, Kosten F_y; TOOL: Sequenzmanager |
| RC06 | Store/StorageUnit zu MW/MWh-States und Zeitauflösung | Hydro/Storage-Zustände und zeitliche Randbedingungen prüfen | Storage/State/Power-Problemmodell für jeweiligen Scope | OWNER: efficiency, boundary; SPRACHE: State-DeltaTime |
| RC07 | Carrier-nodes/converter Link/ports, explizite externe H2 Infrastruktur | H2-Infrastruktur und Strom-H2 bilanziell nur mit deklarierter Basis | Konverter-/Portobjekt, getrennte Energieeinheiten und PreExpansion-Provenienz | DATEN: PreExpansion H2; OWNER: LHV/HHV |
| RC08 | Preprocessing außerhalb Optimierung, Netzreduktionswitness | Input-/Outputnetz je Quellen- und Modellversion abbilden | Network conversion/crosswalk plus QualityOracle getrennt | DATEN: detailliertes Netz; SPRACHE: TransformSpec≠Execution |
| RC09 | raw Optimierungsergebnisse vs KPI Reports, SystemNeed≠Project | Runs/area results separat von Reporting ableiten | ResultStore und Metric-Definition/Filter/B01-D081 | OWNER: Outputformel/Schwelle; SPRACHE: Status/Provenienz |
| RC10 | Linopy model constraints/rows als spätere E04-Evidence | Report von Modell-/Scenario-/Solve-IDs und Oracle | Formula/Constraint-Status und nachvollziehbare Proof-Request-IDs | SPRACHE: sechs Teststatus und Oracle-/Evidence-Trennung |
| RC11 | separater optionaler OPF-Run mit LF-x als cap | OPF-Option und LF-Grenzen anhand Szenario-/Portfolio-Ref | OPF-Probleminstanz mit TRUE/FALSE/UNKNOWN-Guard | OWNER: OPF on/off; SPRACHE: evidenced N/A |
| RC12 | Daten-/Code-/Scenario-/Run-Versionen und Contract-Refs | Versionierte Studie, Source-ID und gespeicherte Ergebnisbasis | Gerät/Formulation/Result-Versionstupel mit SourceManifest | GOV: Autorität; SPRACHE: semantische Änderung und Zeugeninvalidierung |

## 3. Zwingend für alle unabhängigen Implementierungen aus dem Contract lesbar

1. Objektrollen: PhysicalBranch vs ControllableMarketLink; Converter/Storage/H2Carrier/Generator/Load und unzulässige endogene H2-Pipelines.
2. Scope und Entscheidungsinformation: Y getrennt, fünf *extern ausgewählte* CY, fallidentischer Vektor w[c] über Y, Investition vor CY, Dispatch mit CY, Zeitschnitt in UTC/Delta t, Raum und Carrier.
3. mathematische Behauptungen: KCL/KVL bei physikalischen Netzstrukturen, directional NTC bei Kandidatenmarktlinks, Investitionsgrenzen, erwartungswertgewichtete Betriebskosten, E/P Speicherzustandsentwicklung, Strom-H2-Umrechnung, LF-Mesh, OPF-Guard und Stufenbindung.
4. Prozesse: P00–P17 und verknüpfte 38 TransformSpec-Rollen, einschließlich P14 unabhängiger PreExpansion-H2-Run, P16 raw→KPI, P17 Evidenz.
5. Outputs und Nachweise: RawResult, Formel/Owner-Status für DerivedMetric, SystemNeed ungleich freigegebenes Projekt, sechs voneinander unabhängige Teststatus plus tatsächliche Evidence vs bloße Request.

**Nicht** festlegen: dieselben nativen Variablennamen, Solver, Modellcode, eine spezifische LP-Algebra, Framework-Datenklassen oder starre Pipeline-Technik. Wissenschaftlich äquivalente Formulierungen benötigen deklarierten semantischen Projektion- und Annahmewitness, keine syntaktische Identität.

## 4. Alle erforderlichen Zusatzinformationen nach Ursachen klassifizieren

| Klasse | konkrete Rückfrage | Contract-Bewertung |
|---|---|---|
| CONTRACT_DETERMINED | x nicht unabhängig je CY; P15 Guard UNKNOWN blockiert | logisch schon eindeutig; native Sprachsyntax dennoch nicht formell durchgeprüft |
| EXTERNAL_DATA | Netzimpedanzen, CY-Zeitreihen, exogene H2-Infrastruktur, NTC-Impact und Originalsource | kein Sprachdefizit; reale Quelle später zu qualifizieren |
| TOOL_IMPLEMENTER_FREEDOM | angle/cycle/PTDF, native Objektklassen, Solver, Datenformat | zulässig bei Erhalt aller Invarianten und Beobachtungen |
| OWNER_TBD | MD-01, MD-07 F_y, MD-12 Zeitdetails, H2 LHV/HHV, KPI B01-D081 | Unknown mit Verantwortlichem/Scope/Blockade, nicht frei zu erraten |
| LANGUAGE_GAP | quantifiziertes before-CY, typed equations, Stage-Transfer, MetricDef und Equivalence Projection | echte Sprachentwicklungsaufgabe |
| TOOL_LIMITATION | gewählter Solver/Framework kann konkrete IoSN-Funktion nicht nativ darstellen | Adapter-/Erweiterungs-/UNSUPPORTED-Frage im Tool, nicht per se Sprache ungeeignet |

## 5. Gezielt auf Interpretationsrisiken geprüfte Beispiele

- **PyPSA:** physikalische Line irrtümlich als frei steuerbarer Link modelliert; ein CY-Index auf Investition erlaubt separate Investitionen je Wetterfall.
- **Antares:** ein technologisch AC geplantes Candidate-Asset erhält versehentlich die KVL-Rolle statt directional NTC; mehrere Monte-Carlo-Ziehungen werden fälschlich als fünf feste Case-IDs und gemeinsame Investitionsentscheidung interpretiert.
- **Sienna:** vorhandene Geräteklasse wird mit vollständiger mathematischer Pflicht gleichgesetzt; tatsächlich ausgewählte Problem-/Netzformulation aktiviert nur einen Teil der Contract-Restriktionen.
- **Frameworkübergreifend:** identischer optimaler Kostenwert genügt nicht zur E-FEAS-Äquivalenz; zwei unterschiedliche kostenoptimale Portfolios können trotzdem vertragskonform sein.

## 6. Unabhängiges Handover als fehlendes Experiment

Zwei voneinander unabhängige und vom Sprachentwurf getrennte Entwickler erhalten die identische *nativ parsebare* S2-Spezifikation, alle 12 RCs und keine versteckten Implementierungsdetails. Jeder erfasst Vertragslesart, mathematische Pflicht, unbeantwortete Fachentscheidung, erlaubte interne Freiheit und späteren Witness. Danach klassifizierte Differenzen anhand K3/K5, ohne Ownerentscheidungen zu simulieren. **NOT_EXECUTED**: In ML-C17 gab es nur diese KI-interne Rollenprüfung, keine tatsächlichen menschlichen Probanden.

**Urteil:** ENERGY_TOOL_SUITABILITY = CONCEPTUALLY_PLAUSIBLE / IMPLEMENTER_VALIDATION_NOT_EVALUATED. **G1 BLOCKED.**
