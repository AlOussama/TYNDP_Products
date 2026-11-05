# MA-01 — IoSN System Requirements Specification (SyRS)

**Revision 0.1.0, 2026-11-05 | PROVISIONAL, NOT APPROVED.** Applies only to the IoSN process described in the ENTSO-E **TYNDP 2026 IoSN Version for Public Consultation, 25 February 2026**. `MA01-SR-*` are MA-01 requirements **proposals**, not assertions that ENTSO-E has approved an implementation specification. Only `MA01-SR-*` recorded in the companion `iosn_requirements_catalogue.csv` are **active draft** requirements; original `SR-*` and `MR-*` in legacy reports are superseded. Every executed-implementation conformance verdict is **NOT_EXECUTED**.

## Requirements engineering separation and four levels

- **L1 – Methodology Requirements**: The official source's obligations (registered as `MA01-MR-001..050`, each anchored to a section and printed page). Evidence class distinguishes exact mandatory formulations from descriptive source statements, open parameters, and upstream/outside-scope weather selection.
- **L2 – System Requirements**: Tool-neutral “System shall” behaviors, data and mathematical constraints `MA01-SR-001..050`, omitting `012` and `049` which exist only as **excluded methodology coverage**. There are **48 draft system requirements**. An explicit derived behavior is not, by itself, ENTSO-E approval.
- **L3 – Required Formalisation**: What a future representation *must be able to express*, e.g. temporal axes and data contracts, two-stage process states, Kirchhoff DC equations on existing network, market-link investment candidate semantics, stage-specific admissibility, weighted expectation, and verification oracles. The identifier `MA01-FR-*` is a *capability need*, not a DSL proposal/architecture choice.
- **L4 – Verification Needs**: Requirement-specific evidence `MA01-VN-*` through inspection, data reconciliation, mathematical model inspection, reference case and/or running a solver. Defining these tests is **not** executing them. `NOT_EXECUTED` does not mean `PASS`.

## Obligation types, control and acceptance

**Methodology-mandated equations**: preserve linear expected-cost LP with CAPEX, weighted OPEX and VoLL unserved-energy cost; common investment decision across weather cases; electrical nodal balance and DC load flow where prescribed; admissible candidate bounds, two-stage investments and stage-specific sources. Different solver libraries or component taxonomies are allowed, but not a different mathematical problem. **Methodology-mandated modelling abstraction**: proposed investment **transmission** candidates as controllable DC market links irrespective of physical AC/DC; existing mesh network has *different* electrical DC-load-flow semantics.

**External selected weather years**: `MA01-SR-010`, `-011`, `-040` import scenario IDs, number, weights, time series and provenance. `MA01-MR-012` and `-049` are **not** active L2 items; Annex 6.3 PCA/K-Means/feature selection/reproduction **MUST NOT** be implemented or verified by this IoSN contract. Source-specific 2035 WS032/WS037/WS059 etc are O26-revision data, not permanent language definitions. Input validation is permitted.

**Conditions and blockers**: an `O26_DRAFT_CONSTRAINED_DERIVATION` is method-bound only if the consulted source is confirmed/applicable or a later approved revision supersedes it. A `CONDITIONAL_IF_STUDY_EXECUTED` rule becomes applicable only where its optional variant is run. Acceptance oracles with missing source parameters carry `PARTIAL_OWNER_DECISION_REQUIRED`. They cannot be turned into `PASS` by assuming internal defaults.

**Catalogue and traceability**: CSV is a reviewable exact row representation; `iosn_methodology_traceability.csv` records all **50** source-coverage IDs, including the two excluded upstream entries. `methodology_ambiguity_register.md` is the place for source owner decisions; `requirements_review.md` documents non-closure findings.

## Explicitly prohibited scope creep

Weather-year choice/PCA/K-Means, extra generic robustness layers, CBA interoperability, adoption of SysML/GEMS/CESM/INES/custom DSL, new validators/PoCs, adapter development, mandated choice of PyPSA/Antares/Sienna. No parameter is authoritative merely because a previous proof-of-concept used it.

## Requirement catalogue

### MA01-SR-001 — FUNC

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-001: IoSN identifiziert Übertragungs-, Speicher- und Offshore-Systembedarfe; keine verbindlichen Projektentscheidungen.|
|Originalfundstelle|O26 §§2.1–2.2 (S. 9–11) (O-explicit)|
|L2 Requirement statement|**Systembedarfe als methodische Opportunitäten berichten; sie dürfen nicht als bereits genehmigte Investitionsprojekte ausgegeben werden.**|
|Begründung|Unterscheidung zwischen Bedarf und konkreter Projektentscheidung schützt die Planungsaussage.|
|Input|Optimierungs-/Szenarioergebnisse|
|Output|Bedarfsregister mit Bedeutungskennzeichnung|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|KPI-Vorlage und Berichtstechnologie frei.|
|Verification Method|Inspection; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jeder veröffentlichte Datensatz trägt Kategorie Systembedarf/Projektstatus; keine stillschweigende Bauentscheidung.|
|L3 Required Formalisation|MA01-FR-001 (SEMANTIC_OUTPUT); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-001; Nachweisart: Inspection|
|Open Issues|OUTPUT-KPI|

### MA01-SR-002 — SCOPE

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-002: Eigenständige Studienhorizonte 2035, 2040, 2050; 2030 ist kein IoSN-Zieljahr.|
|Originalfundstelle|O26 §3.2 (S. 15) (O-explicit)|
|L2 Requirement statement|**Für den 2026-Methodikstand die Zieljahre 2035, 2040 und 2050 eindeutig führen und methodisch getrennt behandeln.**|
|Begründung|Verhindert unzulässige Vermischung der getrennten Studien.|
|Input|Study-Szenarien, Zieljahr|
|Output|Zieljahr-gebundene Laufmanifestdatei|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Jahrkennzeichen und Datenablage frei.|
|Verification Method|Schema; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Für diesen O26-Profilstand genau 2035/2040/2050; 2030 ist kein offizieller IoSN-Lauf.|
|L3 Required Formalisation|MA01-FR-002 (DATA_AXES); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-002; Nachweisart: Schema|
|Open Issues|Keine spezifische Entscheidung; Source-Release B-01 bleibt offen.|

### MA01-SR-003 — PROCESS

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-003: Separate Expansion-Optimierungen für die drei Zieljahre; 2035-Grenznetz als Ausgangspunkt.|
|Originalfundstelle|O26 §§3.1.1, 3.10 (S. 13–14, 30) (O-explicit)|
|L2 Requirement statement|**Für jeden Zieljahrfall eigenständige, methodisch definierte Expansionsrechnungen durchführen.**|
|Begründung|Trennung der Studienjahre bewahrt publizierte Vergleichbarkeit.|
|Input|Zieljahr- und Modellinputs|
|Output|Expansionsläufe mit Start-/Endzustand|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Aufruf-/Workflowtechnik frei.|
|Verification Method|RunTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jeder Lauf weist Zieljahr, LP-Sequenz und getrennten Endstatus auf; keine unbewiesene Investitionsverkettung.|
|L3 Required Formalisation|MA01-FR-003 (PROCESS_STAGE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-003; Nachweisart: RunTest|
|Open Issues|CAND-STAGES|

### MA01-SR-004 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-004: Szenariokonforme PEMMDB-, PECD- und Planungsdaten als Modelleingang.|
|Originalfundstelle|O26 §§3.1.2, 4 (S. 14, 32) (O-descriptive)|
|L2 Requirement statement|**Szenario- und technoökonomische Referenzdaten mit Herkunft, Zieljahr und Einheiten übernehmen.**|
|Begründung|Der Optimierungsinput ist ohne Herkunftskontrolle nicht nachvollziehbar.|
|Input|PEMMDB, PECD, Szenariopaket|
|Output|Quellversioniertes Eingabedatenmanifest|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|ETL- und Speicherformate frei.|
|Verification Method|DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Kein ungekennzeichneter Quellmix; alle Referenzsätze jahres- und einheitengültig.|
|L3 Required Formalisation|MA01-FR-004 (DATA_SCHEMA); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-004; Nachweisart: DataAudit|
|Open Issues|DATA-VERSION|

### MA01-SR-005 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-005: Startnetz an Grenzen als 2035-Netz auf Basis 2025 und qualifizierter Projekte.|
|Originalfundstelle|O26 §3.4; Anhang 6.2 (S. 16–17, 52–56) (O-explicit)|
|L2 Requirement statement|**Das für 2035 vorgeschriebene Startnetz aus 2025-Bestand und nach Zulässigkeitsregeln berücksichtigten Projekten aufbauen.**|
|Begründung|Anderes Startnetz verändert den gesamten Netzausbaubedarf.|
|Input|2025-Bestandsnetz, Projekte, Zulässigkeitsstatus|
|Output|2035-Referenznetzdaten|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Graphformat frei; Projektberechtigung nicht frei.|
|Verification Method|SourceAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jedes berücksichtigte/ausgeschlossene Projekt ist mit Eignungskriterium und Netzbeitrag nachweisbar.|
|L3 Required Formalisation|MA01-FR-005 (NETWORK_BASE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-005; Nachweisart: SourceAudit|
|Open Issues|GRID-ELIG|

### MA01-SR-006 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-006: Offshore-RES-Ziele der Mitgliedstaaten als exogene feste Größen; Offshore-Hybridprojekte im Startnetz.|
|Originalfundstelle|O26 §3.5 (S. 18) (O-explicit)|
|L2 Requirement statement|**Nationale Offshore-RES-Ziele und qualifizierte Offshore-Hybride als fest vorgegebene Referenzdaten abbilden.**|
|Begründung|Nicht genehmigte Offshore-Entscheidungsfreiheit verzerrt Bedarfsermittlung.|
|Input|Offshore-Zielwerte, Projektliste|
|Output|Festes Offshore-Baselineprofil|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Modellkomponenten frei; Zielwerte nicht optimieren.|
|Verification Method|DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Exogenwerte und Projektidentitäten stimmen mit gültiger Quellenrevision überein.|
|L3 Required Formalisation|MA01-FR-006 (CAPACITY_FIXED); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-006; Nachweisart: DataAudit|
|Open Issues|OFFSHORE-TARGET|

### MA01-SR-007 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-007: Strom- und Wasserstoffbetrieb samt P2G/H2-Rückverstromung sektorgekoppelt abbilden und betreiben.|
|Originalfundstelle|O26 §§3.3, 3.6 (S. 15, 18) (O-explicit)|
|L2 Requirement statement|**Strom-H2-Umwandlung und betriebliche Kopplung über Elektrolyse und H2-Rückverstromung mit getrennten Energiebilanzen repräsentieren.**|
|Begründung|Fehlende Umwandlung eliminiert einen modellrelevanten Flexibilitätsmechanismus.|
|Input|Elektrizitäts- und H2-Daten, Umwandlungsparameter|
|Output|Gekoppeltes Betriebsmodell|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Knoten-/Portobjekttypen und Solver frei.|
|Verification Method|MathTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Beide Energieträgerbilanzen und Umwandlungsrichtungen sind vollständig und algebraisch konsistent.|
|L3 Required Formalisation|MA01-FR-007 (MULTICARRIER_BALANCE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-007; Nachweisart: MathTest|
|Open Issues|H2-DETAIL|

### MA01-SR-008 — SCOPE

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-008: Entwicklung der H2-Übertragungsinfrastruktur ist im vorliegenden Strom-Expansionsmodell vorgegeben.|
|Originalfundstelle|O26 §3.6 (S. 18) (O-descriptive)|
|L2 Requirement statement|**Die vorgegebene H2-Netzentwicklung als Szenarioannahme übernehmen, ohne eigenständige H2-Netzausbauentscheidung in die IoSN-Expansion aufzunehmen.**|
|Begründung|Verhindert nicht spezifizierte Verlagerung von Investitionsfreiheiten zwischen Sektoren.|
|Input|Exogenes H2-Netz|
|Output|H2-Netzrestriktionen|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Datenstruktur für H2-Netz frei.|
|Verification Method|ModelInspection; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Keine als frei entscheidbare H2-Pipeline-Ausbauvariable in den vorgesehenen Stromexpansionsstufen.|
|L3 Required Formalisation|MA01-FR-008 (INVESTMENT_ELIGIBILITY); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-008; Nachweisart: ModelInspection|
|Open Issues|H2-DETAIL|

### MA01-SR-009 — PROCESS

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-009: Wasserstoff-Sensitivität mit eingefrorenem H2-Dispatch auf Basis stündlicher Elektrolyselast aus Prä-Expansion.|
|Originalfundstelle|O26 §3.6 (S. 18) (O-explicit)|
|L2 Requirement statement|**Die methodisch beschriebene Sensitivität mit eingefrorenem H2-Dispatch gegenüber der Expansion nachweisbar getrennt berechnen.**|
|Begründung|Die Sensitivität soll H2-Einfluss auf elektrische Systembedarfe isolieren.|
|Input|Vor-Expansion-Elektrolysezeitreihe, elektrisches Modell|
|Output|H2-Freeze-Sensitivität|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Numerische Betriebslösung frei, Freeze-Semantik nicht.|
|Verification Method|RunTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Eingefrorene Stundenwerte bleiben identisch und Laufstatus ist getrennt berichtet.|
|L3 Required Formalisation|MA01-FR-009 (SENSITIVITY_RULE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-009; Nachweisart: RunTest|
|Open Issues|H2-SENS|

### MA01-SR-010 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-010: Je Zieljahr drei ausgewählte Wetterfälle und Gewichte als Eingaben; IDs/Anteile sind publiziert.|
|Originalfundstelle|O26 §3.7 (S. 19–20) (O-explicit)|
|L2 Requirement statement|**Bereits extern ausgewählte Wetterjahre/Wetterszenarien mit Anzahl, Identitäten, Studienjahrzuordnung und Gewichten als Input übernehmen und auf formale Konsistenz prüfen; keine Auswahlentscheidung treffen.**|
|Begründung|Rechenlauf benötigt Eingabeszenarien, nicht deren upstream Entstehung.|
|Input|Externes Auswahlmanifest, Quelle und Zeitreihenverweise|
|Output|Validiertes Wetter-Inputmanifest|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Dateiformat frei; Auswahlverfahren bleibt ausdrücklich extern.|
|Verification Method|Schema+DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Eindeutige IDs, für O26 die drei publizierten Fälle je Zieljahr, Gewichte endlich/nichtnegativ und Summe 1 (Toleranz freizugeben); keine PCA-/K-Means-Prüfung.|
|L3 Required Formalisation|MA01-FR-010 (WEATHER_INPUT_ONLY); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-010; Nachweisart: Schema+DataAudit|
|Open Issues|SOURCE-RELEASE|

### MA01-SR-011 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-011: Klimasensitive Nachfrage, RES und Hydroprofile als mit Wetterfall verknüpfte Eingaben.|
|Originalfundstelle|O26 §§3.7, 4.2 (S. 19, 34) (O-explicit)|
|L2 Requirement statement|**Wetter- und Zieljahr-indizierte RES-, Last- und Hydrozeitreihen mit konsistenter Zeitachse, Raumbezug, Einheiten und Quellprovenienz übernehmen.**|
|Begründung|Eine fehlerhafte zeitliche Zuordnung verändert die Systembilanz.|
|Input|Externes Wettermanifest, PECD/DFT/RES/Hydro-Reihen|
|Output|Zeitachsenkonformer Inputdatensatz|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|ETL frei; Auswahl und Gewichtserzeugung nicht.|
|Verification Method|DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jede erforderliche Reihe referenziert genau definierten Zieljahr-Wetter-Zonen-Schnitt; keine verdeckte Zeitschrittverschiebung.|
|L3 Required Formalisation|MA01-FR-011 (TIMESERIES_ALIGNMENT); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-011; Nachweisart: DataAudit|
|Open Issues|TIME-AXIS|

### MA01-SR-013 — NETWORK

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-013: Zonale Netzabbildung für TYNDP 2026 mit 102 genannten Zonen (Tabelle 3).|
|Originalfundstelle|O26 §3.8.1 (S. 23–27) (O-explicit-2026)|
|L2 Requirement statement|**Die für diesen O26-Studienstand angegebene zonale Geographie einschließlich zonaler Identitäten/Zuordnung abbilden.**|
|Begründung|Zonenauflösung bestimmt lokalisierte Engpässe.|
|Input|O26-Zonendefinition, Netztopologie|
|Output|Zonenregister und Knotenzuordnung|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Zonenidentifikator-Format frei.|
|Verification Method|Inspection; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Das O26-Referenzprofil dokumentiert die 102 Zonen und alle abweichenden versionsbedingten Definitionen.|
|L3 Required Formalisation|MA01-FR-013 (ZONAL_GEOGRAPHY); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-013; Nachweisart: Inspection|
|Open Issues|ZONE-GEOGRAPHY|

### MA01-SR-014 — NETWORK

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-014: Clustering muss kritische/engpassrelevante Leitungen, homogene Austauschrichtungen und Rechenaufwand abwägen.|
|Originalfundstelle|O26 §3.8.1 (S. 23–24) (O-descriptive)|
|L2 Requirement statement|**Für die Netzclusterbildung methodisch relevante Engpass- und Austauschmerkmale heranziehen und Entscheidungen protokollieren.**|
|Begründung|Unabhängige Nachbildung erfordert mehr als eine fertige Busmap.|
|Input|Kritische Leitungen, Lastflüsse und Netzgraph|
|Output|Clustering-Evidenz|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Algorithmische Optimierungsimplementierung frei innerhalb der Methode.|
|Verification Method|MethodReview; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Engpasskriterien und Zone-Zuordnung nachvollziehbar; numerische Qualitätsfreigabe derzeit BLOCKED.|
|L3 Required Formalisation|MA01-FR-014 (CLUSTER_CRITERIA); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-014; Nachweisart: MethodReview|
|Open Issues|ZONAL-QUALITY|

### MA01-SR-015 — NETWORK

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-015: Kritische 225/400-kV-Leitungen durch stündliche Überlastung und jährliche Überlastungsenergie identifizieren.|
|Originalfundstelle|O26 Anhang 6.1 (S. 45) (O-explicit)|
|L2 Requirement statement|**Kritische Leitungen unter Einbeziehung stündlicher Überlastungs- und jährlicher Überlastungsenergiekennzahlen identifizieren.**|
|Begründung|Priorisierte Engpässe steuern die Netzaggregation.|
|Input|Detaillierte Leitungsflüsse und Ratings|
|Output|Kritische-Leitungen-Liste|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Numerische Vektor-/Matrixbibliothek frei.|
|Verification Method|Data+MathTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jede Markierung enthält Stundenbelege, Bezugsrating und gewählte Aggregationskonvention.|
|L3 Required Formalisation|MA01-FR-015 (CONGESTION_METRIC); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-015; Nachweisart: Data+MathTest|
|Open Issues|GRID-INPUT|

### MA01-SR-016 — NETWORK

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-016: Zusammenhängende Knoten je Cluster; Größenverhältnis und PECD-Kohärenz als weitere Qualitätsaspekte.|
|Originalfundstelle|O26 §3.8.1 (S. 24) (O-descriptive)|
|L2 Requirement statement|**Geographisch/elektrisch zulässige, zusammenhängende Netzcluster und Zuordnung sämtlicher relevanter Knoten sicherstellen.**|
|Begründung|Disconnected Cluster verfälschen elektrotechnische Äquivalenz.|
|Input|Netzgraph, Zonenvorgaben|
|Output|Verbundenes Clusterregister|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Clusterungsalgorithmus frei.|
|Verification Method|GraphTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jeder abgebildete Knoten ist genau einer gültigen Zone zugeordnet, jede Zone graphisch zusammenhängend.|
|L3 Required Formalisation|MA01-FR-016 (GRAPH_PARTITION); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-016; Nachweisart: GraphTest|
|Open Issues|ZONAL-QUALITY|

### MA01-SR-017 — NETWORK

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-017: Äquivalente Impedanzen und Nullbilanz-Flusskorrekturen über Fehler-minimierende Optimierung ermitteln.|
|Originalfundstelle|O26 §3.8.2; Anhang 6.1 (S. 27, 48–49) (O-explicit)|
|L2 Requirement statement|**Äquivalente Impedanzen und Referenzflusskorrekturen des reduzierten Netzes methodenkonform herleiten.**|
|Begründung|Equivalent-Grid-Fehler können Ausbausignale systematisch verschieben.|
|Input|Detaillierte Netzimpedanzen und Referenzlastflüsse|
|Output|Impedanz-/Flusskorrekturparameter|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Algorithmische/solvertechnische Umsetzung frei bei gleicher mathematischer Methodik.|
|Verification Method|MathTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Rekonstruierbarer Abgleich Detailed vs Reduced; genaue Fehlertoleranz mangels freigegebenem Oracle BLOCKED.|
|L3 Required Formalisation|MA01-FR-017 (EQUIVALENT_GRID); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-017; Nachweisart: MathTest|
|Open Issues|ZONAL-ORACLE|

### MA01-SR-018 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-018: Vermaschungsregeln des reduzierten Netzes unter DC-Approximation abbilden.|
|Originalfundstelle|O26 §3.8.2; Anhang 6.1 (S. 27, 49) (O-explicit)|
|L2 Requirement statement|**Vermaschte elektrische Lastflussbeziehungen nach der vorgeschriebenen DC-Näherung in das reduzierte Stromnetz übernehmen.**|
|Begründung|Die Maschenphysik ist Teil des methodischen Lastflussmodells.|
|Input|Zonen-/Leitungstopologie, Impedanzen|
|Output|Kirchhoff-konforme Maschenrestriktionen|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Variable-/Gleichungscodierung frei; physikalische Gleichungsklasse nicht.|
|Verification Method|GeneratedModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Erzeugtes Optimierungsmodell erfüllt Fluss-/Winkelkopplung auf Bestandsleitungen; keine Verwechslung mit Markt-Links.|
|L3 Required Formalisation|MA01-FR-018 (DC_NETWORK_EQUATIONS); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-018; Nachweisart: GeneratedModelTest|
|Open Issues|MESH-CONVENTION|

### MA01-SR-019 — NETWORK

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-019: Äquivalente N-1-Kapazitäten mit detaillierten Lastflüssen und LODF ableiten.|
|Originalfundstelle|O26 §3.8.2; Anhang 6.1 (S. 27, 49–51) (O-explicit)|
|L2 Requirement statement|**Methodisch abgeleitete äquivalente N-1-Übertragungskapazitäten und LODF-Bezüge des reduzierten Netzes bereitstellen.**|
|Begründung|Überdimensionierte Grenzwerte verschleiern kritische Engpässe.|
|Input|Detaillierte Netzanalyse und LODF|
|Output|Äquivalente Sicherheitskapazitäten|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Numerische Lösung frei, Sicherheitsszenario-Semantik nicht.|
|Verification Method|ReferenceTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Vergleichbar zu referenzierten Detailnetzfällen; quantitative Schwellen BLOCKED bis Methodikentscheid.|
|L3 Required Formalisation|MA01-FR-019 (N_MINUS_ONE_CAPACITY); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-019; Nachweisart: ReferenceTest|
|Open Issues|CAP-ORACLE|

### MA01-SR-020 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-020: Je Interzonenverbindung vier Kapazitätswerte: Sommer/Winter je Richtung.|
|Originalfundstelle|O26 §3.8.3 (S. 28) (O-explicit)|
|L2 Requirement statement|**Für jede relevante reduzierte Interzonen-Verbindung die vier Sommer/Winter- und Hin-/Rückrichtungs-Kapazitäten führen.**|
|Begründung|Eine symmetrische Einheits-NTC würde methodische Unterschiede verlieren.|
|Input|Zeitabschnitte, N-1-Analysen|
|Output|Vierdimensionierte Übertragungslimits|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Tabellen-/Arrayrepräsentation frei.|
|Verification Method|Schema+DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Für jede Verbindung sind zwei Jahreszeiten mal zwei Richtungen eindeutig vollständig.|
|L3 Required Formalisation|MA01-FR-020 (DIRECTIONAL_SEASONAL_CAP); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-020; Nachweisart: Schema+DataAudit|
|Open Issues|CAP-ORACLE|

### MA01-SR-021 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-021: Sechs Reduktionsoutputs: No-load-Flüsse, Maschenbeziehungen, HVDC-Einfluss, Kapazitäten, Impedanzen, PST-Einfluss.|
|Originalfundstelle|O26 §3.8.3 (S. 28) (O-explicit)|
|L2 Requirement statement|**Alle sechs von der Methodik genannten Kategorien von Netzreduktionsparametern konsistent ausgeben.**|
|Begründung|Vollständige Datenklassen sind Voraussetzung für spätere Nachrechnung.|
|Input|Netzreduktionsrechenlauf|
|Output|Reduktionsdaten mit sechs Parameterklassen|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Format frei.|
|Verification Method|Schema; bisher **NOT_EXECUTED**|
|Acceptance Criteria|No-load flows, Mesh Relations, HVDC Impact, Capacities, Impedances, PST Impact vollständig oder explizit methodisch nicht anwendbar.|
|L3 Required Formalisation|MA01-FR-021 (REDUCED_NETWORK_OUTPUT); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-021; Nachweisart: Schema|
|Open Issues|Keine spezifische Entscheidung; Source-Release B-01 bleibt offen.|

### MA01-SR-022 — VERIFICATION

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-022: Clustering-Iterationen mit RMSE-Priorität, Kapazitätsqualität und methodischen Sonderfällen dokumentieren.|
|Originalfundstelle|O26 Anhang 6.1 (S. 45–51) (O-descriptive)|
|L2 Requirement statement|**Netzreduktionsgüte an Quellenkennzahlen (u.a. Fluss-RMSE und Kapazitätsverhalten) ausweisen; bei unklaren Schwellen keine implizite Qualitätsfreigabe vergeben.**|
|Begründung|Abbildung des Graphen allein belegt keine elektrische Güte.|
|Input|Detail-/Aggregatnetz-Ergebnisse|
|Output|Qualitäts-/Abweichungsbericht|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Metrik-Implementierung frei, Methodikschwelle nicht zu erfinden.|
|Verification Method|ReferenceTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Kennzahlen und Referenzfälle berechnet; endgültiges PASS abhängig von freigegebenem Grenzwert.|
|L3 Required Formalisation|MA01-FR-022 (NETWORK_QUALITY); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-022; Nachweisart: ReferenceTest|
|Open Issues|ZONAL-QUALITY|

### MA01-SR-023 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-023: PEMMDB/PECD-Netz- und Lastdaten zonal aufteilen und Generatorkapazitäten sowie Profile reconciliieren.|
|Originalfundstelle|O26 §3.8.4 (S. 28–29) (O-explicit)|
|L2 Requirement statement|**PEMMDB-/PECD-/DFT-Daten zonal nach methodischer Netzabbildung disaggregieren und Quelle→Zone-Mapping nachvollziehbar dokumentieren.**|
|Begründung|Unkontrollierte Quellenverschiebung verändert zonale Grenzkosten.|
|Input|Quellassets, Zeitreihen und Busmap|
|Output|Zonale Markt- und Zeitreihen|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|ETL-/Dateisystem frei.|
|Verification Method|Reconciliation; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Aggregierte Mengen lassen sich auf Quellenbestände und Profile rückführen; Abweichungstoleranzen freizugeben.|
|L3 Required Formalisation|MA01-FR-023 (ZONAL_ALLOCATION); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-023; Nachweisart: Reconciliation|
|Open Issues|ALLOC-TOLERANCE|

### MA01-SR-024 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-024: Primäre Expansion im LF-Modus mit Maschenphysik, aber unbegrenzten Interzonen-Kapazitätsgrenzen.|
|Originalfundstelle|O26 §3.9 (S. 29) (O-explicit)|
|L2 Requirement statement|**Die primäre Leitungsexpansion in der methodisch vorgesehenen LF-Variante mit Maschenrestriktionen und unbeschränkten Interzonen-Kapazitätsgrenzen lösen.**|
|Begründung|LF-basierte Systembedarfe sind nicht OPF-Ausbauoptionen.|
|Input|Elektrisches Modell und Marktdaten|
|Output|LF-Baseline-Expansionslösung|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|LP-Solver frei, LF-Modus nicht optional.|
|Verification Method|GeneratedModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Modus LF und Kirchhoff-Beziehungen belegt; keine endlichen Netzkapazitäts-Restriktionen, wo Quelle LF-Infinity vorschreibt.|
|L3 Required Formalisation|MA01-FR-024 (LF_EXPANSION_PROFILE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-024; Nachweisart: GeneratedModelTest|
|Open Issues|LF-SEMANTICS|

### MA01-SR-025 — PROCESS

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-025: Dispatch mit und ohne IoSN-Portfolio zur Wirkung interner Netzengpässe.|
|Originalfundstelle|O26 §3.9 (S. 29) (O-explicit)|
|L2 Requirement statement|**Den zusätzlichen Dispatchvergleich mit und ohne Portfolio unter internen Netzrestriktionen getrennt von der LF-Baseline durchführen.**|
|Begründung|Vergleich misst Betriebseffekte des vorgeschlagenen Ausbaus.|
|Input|LF-Portfolio, internes Netz|
|Output|Zwei Vergleichs-Dispatchläufe|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Dispatchtechnik frei.|
|Verification Method|RunTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Beide Fälle verwenden dieselben exogenen Inputkonventionen; Portfoliowirkung separat ausgewiesen.|
|L3 Required Formalisation|MA01-FR-025 (DISPATCH_PAIR); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-025; Nachweisart: RunTest|
|Open Issues|KPI-REPORT|

### MA01-SR-026 — PROCESS

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-026: Zusätzliche OPF-Expansion ist fakultativ; wenn durchgeführt, Kandidatenportfolio durch LF-Portfolio begrenzt.|
|Originalfundstelle|O26 §3.9 (S. 29) (O-conditional)|
|L2 Requirement statement|**Eine optionale OPF-Expansion ausschließlich als gekennzeichnete Zusatzanalyse ausführen und ihre Kandidatenexpansion auf LF-Portfolio begrenzen.**|
|Begründung|Verhindert falsche Bewertung von OPF als ursprüngliche Systembedarfsbaseline.|
|Input|LF-Kandidatenportfolio, internes OPF-Netz|
|Output|Optionales OPF-Portfolio|
|Verbindlichkeit / Status|CONDITIONAL_IF_STUDY_EXECUTED; PROPOSED_NOT_APPROVED|
|Implementation Freedom|OPF-Implementierung frei; Kapazitätsdeckel verbindlich falls genutzt.|
|Verification Method|GeneratedModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Falls OPF durchgeführt, ist zulässige Kandidatenmenge nicht größer als LF-basierte; sonst NOT_APPLICABLE.|
|L3 Required Formalisation|MA01-FR-026 (OPTIONAL_OPF_CONDITION); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-026; Nachweisart: GeneratedModelTest|
|Open Issues|OPF-CAP|

### MA01-SR-027 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-027: Ziel: Investitionskosten + wahrscheinlichkeitgewichtete Betriebskosten + VoLL×nicht versorgte Energie.|
|Originalfundstelle|O26 §3.1.1 (S. 12–14) (O-explicit-math)|
|L2 Requirement statement|**Investition, nach Wetterfallwahrscheinlichkeiten gewichtete Betriebskosten und Bewertung nicht versorgter Energie im vorgeschriebenen Optimierungsziel abbilden.**|
|Begründung|Erhaltung der Zielfunktion ist entscheidend für Bedarfsaussagen.|
|Input|CAPEX, OPEX, Wettergewichte, VoLL, ENS|
|Output|Objektivfunktion und Kostendekomposition|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Solver/Modell-Datensätze frei; Zielstruktur nicht frei.|
|Verification Method|MathTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Generated LP contains all cost blocks with consistent units/weights; discount convention BLOCKED.|
|L3 Required Formalisation|MA01-FR-027 (EXPECTED_COST_OBJECTIVE); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-027; Nachweisart: MathTest|
|Open Issues|ECON-DISCOUNT|

### MA01-SR-028 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-028: Knotenleistungsbilanz, DC-Netzfluss/Kirchhoff, technische Betriebsgrenzen und Policy-Constraints.|
|Originalfundstelle|O26 §3.1.1 (S. 13) (O-explicit-math)|
|L2 Requirement statement|**Elektrische Leistungsbilanz, zulässige DC-Flussgesetze, Betriebsschranken und relevante Policy-Restriktionen methodenkonform kodieren.**|
|Begründung|Vollständige Balance und Nebenbedingungen definieren die zulässige Lösungsmenge.|
|Input|Topologie, Anlagen, Grenzwerte, Politikszenario|
|Output|Gleichungs-/Restriktionssystem|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Indexierung/Gleichungsbibliothek frei.|
|Verification Method|GeneratedModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jede vorgeschriebene Gleichungsfamilie im generierten Modell nachweisbar; keine ungeklärte Default-Annahme.|
|L3 Required Formalisation|MA01-FR-028 (CONSTRAINT_FAMILIES); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-028; Nachweisart: GeneratedModelTest|
|Open Issues|BALANCE-DETAIL|

### MA01-SR-029 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-029: Nichtantizipativität: dieselbe Investitionsentscheidung über alle Wetterfälle je Zieljahr.|
|Originalfundstelle|O26 §3.1.1 (S. 12–14) (O-explicit-math)|
|L2 Requirement statement|**Je Zieljahr für jeden Investitionskandidaten dieselbe Investitionsentscheidung über sämtliche Wetterfälle erzwingen.**|
|Begründung|Wetterrealisationen dürfen keine ex-post-Investitionsentscheidung auslösen.|
|Input|Kandidaten, Wetterfallindex|
|Output|Nichtantizipative Investitionsrestriktionen|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Gemeinsame Variable oder Gleichheitsrestriktion frei.|
|Verification Method|GeneratedModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Pro Zieljahr/Kandidat keine frei voneinander variierenden s-spezifischen Ausbauentscheidungen.|
|L3 Required Formalisation|MA01-FR-029 (NONANTICIPATIVITY); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-029; Nachweisart: GeneratedModelTest|
|Open Issues|Keine spezifische Entscheidung; Source-Release B-01 bleibt offen.|

### MA01-SR-030 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-030: Lineare Investitionskandidaten durch 0 ≤ Ausbau ≤ zulässigem Maximum begrenzt.|
|Originalfundstelle|O26 §3.1.1 (S. 13) (O-explicit-math)|
|L2 Requirement statement|**Jeden zulässigen Ausbauumfang linear zwischen null und kandidatenbezogenem Höchstwert beschränken.**|
|Begründung|Fehlende Begrenzung erzeugt nicht physische Investitionsmöglichkeiten.|
|Input|Kandidatenregister und Obergrenzen|
|Output|Ausbau-Schranken|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|LP-Variablenkodierung frei.|
|Verification Method|GeneratedModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Alle Kandidaten durch 0 ≤ x ≤ x_max gebunden; keine ungeprüften negativen/unbeschränkten x.|
|L3 Required Formalisation|MA01-FR-030 (INVESTMENT_BOUNDS); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-030; Nachweisart: GeneratedModelTest|
|Open Issues|Keine spezifische Entscheidung; Source-Release B-01 bleibt offen.|

### MA01-SR-031 — PROCESS

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-031: Expansionsstufe 1 als LP über reale Onshore-/Offshore-Übertragungskandidaten.|
|Originalfundstelle|O26 §3.10 (S. 30) (O-explicit)|
|L2 Requirement statement|**Die erste vorgeschriebene LP-Investitionsstufe auf die laut O26 zulässigen realen Übertragungskandidaten beschränken.**|
|Begründung|Verbindliche Stufenreihenfolge verhindert Kandidaten-Misclassification.|
|Input|Reale On-/Offshore-Kandidaten|
|Output|Stage-1-Lösung und Kandidatenliste|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Interner Solver-Aufruf frei.|
|Verification Method|Run+ModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Kein konzeptioneller/theoretischer Kandidat in Stage 1, Portfolio und Solverstatus dokumentiert.|
|L3 Required Formalisation|MA01-FR-031 (TWO_STAGE_FIRST); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-031; Nachweisart: Run+ModelTest|
|Open Issues|CAND-STAGES|

### MA01-SR-032 — PROCESS

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-032: Expansionsstufe 2 als LP mit verbleibenden realen, konzeptionellen Onshore- und theoretischen Offshore-Kandidaten.|
|Originalfundstelle|O26 §3.10 (S. 30) (O-explicit)|
|L2 Requirement statement|**In der zweiten LP-Stufe nur verbleibende reale, konzeptionelle und theoretische Kandidaten mit korrekter Stage-1-Anrechnung zulassen.**|
|Begründung|Kandidatenstufen beeinflussen das Investitionsergebnis.|
|Input|Stage 1, übrige Kandidaten|
|Output|Stage-2-Portfolio|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|LP-Repräsentation frei; Stufenlogik nicht.|
|Verification Method|Run+ModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Stage-1-Investitionen nachvollziehbar übernommen; Kandidatenfilter und zulässige Stufen offen dokumentiert.|
|L3 Required Formalisation|MA01-FR-032 (TWO_STAGE_SECOND); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-032; Nachweisart: Run+ModelTest|
|Open Issues|CAND-STAGES|

### MA01-SR-033 — SCOPE

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-033: Speicherausbau separat nur 2040 und 2050, 2035 exogener Szenariobestand; Ländertrajektorien begrenzen Ausbau.|
|Originalfundstelle|O26 §3.10 (S. 30) (O-explicit)|
|L2 Requirement statement|**Endogene Speicherinvestitionen ausschließlich in 2040/2050 erlauben; 2035 nur szenariobasierten Speicherbestand verwenden.**|
|Begründung|Verhindert methodisch nicht autorisierte frühe Speicherinvestition.|
|Input|Speicherkapazitäten und Zieljahr|
|Output|Horizonspezifische Speicherrestriktionen|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Speicherkomponente frei.|
|Verification Method|GeneratedModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Kein speicherbezogener Ausbaufreiheitsgrad 2035, 2040/2050 mit zulässigen Länderkappen.|
|L3 Required Formalisation|MA01-FR-033 (STORAGE_HORIZONS); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-033; Nachweisart: GeneratedModelTest|
|Open Issues|STORAGE-DETAIL|

### MA01-SR-034 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-034: Mindestens zwei Speichergrößen/-dauern; standardisierte Batterie-Modellannahme als Stellvertreter für Speicherbedarf.|
|Originalfundstelle|O26 §4.5.1 (S. 37) (O-explicit)|
|L2 Requirement statement|**Mindestens zwei Speicherdauer-/Flexibilitätsklassen unter der dokumentierten generischen Speicherproxy-Annahme unterscheiden.**|
|Begründung|Der Proxy ist kein Beschluss über Batterietechnologie der Projekte.|
|Input|Speicherdauer, Energie-/Leistungsgrößen und Kosten|
|Output|Speicherkandidaten-Proxy|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Komponententyp frei; Methodikklassen erhalten.|
|Verification Method|Schema+ModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Mindestens zwei unterschiedliche Dauerklassen, konkrete Technologieaussage als Proxy markiert; Endkosten offen.|
|L3 Required Formalisation|MA01-FR-034 (STORAGE_PROXY); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-034; Nachweisart: Schema+ModelTest|
|Open Issues|STORAGE-DETAIL|

### MA01-SR-035 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-035: Alle Übertragungs-Investitionskandidaten unabhängig von physischer AC/DC-Technologie als steuerbare DC-Markt-Links mit NTC-Effekt.|
|Originalfundstelle|O26 §4.5.2 (S. 37) (O-explicit-method)|
|L2 Requirement statement|**Sämtliche Übertragungs-Investitionskandidaten als steuerbare DC-Markt-Links mit NTC-Wirkung modellieren – auch bei physischer AC-Technologie.**|
|Begründung|Entscheidend ist Markt-/Flusssteuerbarkeit, nicht physische Leitungsart.|
|Input|Kandidaten, NTC-Endpunkte/Richtungen|
|Output|Separater steuerbarer Kandidaten-Linktyp|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Native Modellklasse frei; Marktlink-Semantik nicht.|
|Verification Method|GeneratedModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Kein Kandidat allein wegen physischer AC-Bauart als vermaschte elektrische Bestandsleitung kodiert.|
|L3 Required Formalisation|MA01-FR-035 (CONTROLLABLE_MARKET_LINK); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-035; Nachweisart: GeneratedModelTest|
|Open Issues|CAND-MAPPING|

### MA01-SR-036 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-036: Direkte/indirekte NTC-Zuwächse, Kosten interner Verstärkung, Anschlussknoten/RDFID und Projektmetadaten.|
|Originalfundstelle|O26 §4.5.2 (S. 37–38) (O-explicit)|
|L2 Requirement statement|**Richtungsbezogene NTC-Zuwächse und kandidatenbezogene Kostenträger, Netzeinbindungen und Identitäten eindeutig erhalten.**|
|Begründung|Schlechte Richtungszuordnung verändert Ausbaudimension und Kosten.|
|Input|Projektmetadaten und bidirektionale NTC|
|Output|Kandidatenmatrix mit NTC-Richtung/Geografie/Kosten|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Datenformat frei.|
|Verification Method|DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Beide Richtungen sind getrennt definiert; Anschlusspunkt und Herkunft des CAPEX geprüft.|
|L3 Required Formalisation|MA01-FR-036 (DIRECTIONAL_NTC_IMPACT); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-036; Nachweisart: DataAudit|
|Open Issues|CAND-MAPPING|

### MA01-SR-037 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-037: Theoretische Offshore-Kandidaten: geographisch/regional geprüft; Standard 525-kV-VSC-HVDC 2 GW mit Tabelle-4-Kosten.|
|Originalfundstelle|O26 §4.5.3 (S. 38–39) (O-explicit-2026)|
|L2 Requirement statement|**Für theoretische Offshore-VSC-Verbindungen die O26-Referenztechnologie und source-spezifische Kostenannahmen versionieren und einhalten.**|
|Begründung|Technologieparameter sind für Längen-/Investitionskostenvergleich notwendig.|
|Input|Offshore-Geometrie, Technologietabelle 4|
|Output|Offshore-Kandidaten mit 525kV/2GW Referenz|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Komponentennamen frei; vorgeschriebene Referenzeigenschaften nicht.|
|Verification Method|DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Referenzkandidat entspricht expliziter Quelle; Kostenquellen verfügbar, Ausnahmen gekennzeichnet.|
|L3 Required Formalisation|MA01-FR-037 (OFFSHORE_COST_REFERENCE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-037; Nachweisart: DataAudit|
|Open Issues|OFFSHORE-COST|

### MA01-SR-038 — METHOD

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-038: Theoretische Offshore-Längen/Kosten mit einheitlichem Meer-Nutzungsfaktor 10–15 % erhöhen; exakter Wert offen.|
|Originalfundstelle|O26 §3.11 (S. 30–31) (O-explicit-open)|
|L2 Requirement statement|**Den methodisch vorgesehenen einheitlichen 10–15%-Umwegfaktor bei theoretischen Offshore-Kandidaten als unaufgelösten Methodenparameter führen; kein definitiver Wert ohne Freigabe.**|
|Begründung|Die Konsultationsfassung benennt ausdrücklich noch keinen endgültigen Wert.|
|Input|Theoretische Offshorerouten, Methodenentscheidung|
|Output|Versionierter Routing-/Kostenfaktor|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Rechenimplementierung frei, Parameterwahl owner-owned.|
|Verification Method|MethodReview; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Faktor innerhalb O26-Band; formelles PASS für finalen Wert erst nach zuständiger Entscheidung.|
|L3 Required Formalisation|MA01-FR-038 (OFFSHORE_ROUTE_FACTOR); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-038; Nachweisart: MethodReview|
|Open Issues|SEA-FACTOR|

### MA01-SR-039 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-039: PEMMDB liefert Erzeugung, Speicher, DSR/P2X, fixe Austausche, technische und variable Kosten sowie Reserven.|
|Originalfundstelle|O26 §4.1 (S. 33–34) (O-descriptive)|
|L2 Requirement statement|**PEMMDB-Produktions-, Speicher-, DSR/P2X- und Netzmarktinformationen mit gültigem Szenariobezug übernehmen.**|
|Begründung|Systemumfassende Bilanz benötigt konsistente Marktannahmen.|
|Input|PEMMDB-Quellen|
|Output|Versionierter PEMMDB-Input|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Importtechnologie frei.|
|Verification Method|DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Alle verwendeten Datengruppen und Auslassungen mit Release, Einheit und Zeitpunkt identifiziert.|
|L3 Required Formalisation|MA01-FR-039 (SCENARIO_MARKET_DATA); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-039; Nachweisart: DataAudit|
|Open Issues|DATA-VERSION|

### MA01-SR-040 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-040: PECD v4.2-Profile für Wind, Solar, temperaturabhängige Last, Hydro als externen Dateninput nutzen.|
|Originalfundstelle|O26 §4.2 (S. 34) (O-descriptive)|
|L2 Requirement statement|**PECD-Klimareihen in publiziertem Versions- und Wetterfallbezug als bereits aufbereitete Daten übernehmen.**|
|Begründung|Provenienz macht klimabezogene Sensitivität prüfbar.|
|Input|Externe PECD v4.2-Datenreferenzen|
|Output|PECD-Zeitreiheninput|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Datencontainers frei; Selektion bleibt extern.|
|Verification Method|DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|PECD-Version und zugehörige ausgewählte Wetterfall-ID/Zeitschema eindeutig; keine eigenständige Wetterauswahl.|
|L3 Required Formalisation|MA01-FR-040 (CLIMATE_INPUT); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-040; Nachweisart: DataAudit|
|Open Issues|DATA-VERSION|

### MA01-SR-041 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-041: Fünf Hydroklassen und zugehörige Zuflüsse, Speicher- und Pumpgrenzen unterscheiden.|
|Originalfundstelle|O26 §4.3 (S. 35) (O-explicit)|
|L2 Requirement statement|**Die fünf methodisch geforderten Wasserkraftbetriebs-/Ressourcenklassen mit Zeitverlauf und Restriktionen unterscheidbar abbilden.**|
|Begründung|Generisches Speicherobjekt ohne Hydrosemantik erfüllt Methode nicht zwangsläufig.|
|Input|Hydro-Inflow, Speicherstände, Pump-/Erzeugungsdaten|
|Output|Klassenbezogene Hydrorestriktionen|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Energiespeicher-Objektmodell frei.|
|Verification Method|ModelInspection; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Fünf Kategorien in Modell und Datenkennzeichnung, je Kategorie passende zeitliche Grenzbedingungen.|
|L3 Required Formalisation|MA01-FR-041 (HYDRO_CLASSES); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-041; Nachweisart: ModelInspection|
|Open Issues|HYDRO-PROFILE|

### MA01-SR-042 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-042: DFT-Stundenlast inkl. EV/HP; implizite DSR außerhalb des Markts von expliziter industrieller DSR unterscheiden.|
|Originalfundstelle|O26 §4.4 (S. 35–36) (O-explicit)|
|L2 Requirement statement|**Stündliche DFT-Nachfragereihen inkl. EV/HP und Unterscheidung impliziter vs expliziter DSR korrekt übertragen.**|
|Begründung|Entgegengesetzte DSR-Behandlung verzerrt verfügbar flexible Nachfrage.|
|Input|DFT-Nachfrage und DSR-Datentabellen|
|Output|Load- und DSR-Profile|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Native Last-/Flexibilitätsobjekte frei.|
|Verification Method|Data+ModelTest; bisher **NOT_EXECUTED**|
|Acceptance Criteria|EV/HP-Profile korrekt zeitindiziert; implizite DSR nicht als frei dispatchbare Marktfunktion reklassifiziert.|
|L3 Required Formalisation|MA01-FR-042 (DFT_DSR_SEMANTICS); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-042; Nachweisart: Data+ModelTest|
|Open Issues|DSR-SEMANTICS|

### MA01-SR-043 — METHOD

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-043: WACC 4 % für benannte Transmission-/Batteriekandidaten; wirtschaftliche Lebensdauer 25 Jahre für Transmission.|
|Originalfundstelle|O26 §4.6 (S. 39–40) (O-explicit)|
|L2 Requirement statement|**WACC-/Investitionslebensdauerannahmen und ihre Anwendungsgruppen gemäß §4.6 der Quellenrevision erhalten.**|
|Begründung|CAPEX-Umrechnung verändert Kostenvergleich der Kandidaten.|
|Input|Technologieklasse, Lebensdauer, WACC|
|Output|Ökonomische Parameterregister|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Rechenroutine frei; Methodikzahlen nicht.|
|Verification Method|DataAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|4% WACC und 25 Jahre wo O26 explizit benannt; sonst keine pauschalisierten Annahmen.|
|L3 Required Formalisation|MA01-FR-043 (ECONOMIC_PARAMETER_PROFILE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-043; Nachweisart: DataAudit|
|Open Issues|ECON-VINTAGE|

### MA01-SR-044 — METHOD

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-044: Diskontierung bis 2026 mit in Quelle beschädigter Referenz zur Blockjahreslogik.|
|Originalfundstelle|O26 §4.6 (S. 40) (O-open)|
|L2 Requirement statement|**Diskontierung und Bezugsjahr 2026 explizit abbilden und defekte Querverweise als blockierte Methodenentscheidung behandeln.**|
|Begründung|Voreilige Default-Blockzuordnung wäre nicht quellengedeckt.|
|Input|Kostentabellen und Zeitblöcke|
|Output|Diskontierungsprofil mit Freigabestatus|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Numerische Umsetzung frei nach Klärung.|
|Verification Method|MethodReview; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Grundkonvention dokumentiert, aber vollständiges PASS nur mit geklärtem §4.6-Blockbezug.|
|L3 Required Formalisation|MA01-FR-044 (DISCOUNT_PROFILE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-044; Nachweisart: MethodReview|
|Open Issues|ECON-DISCOUNT|

### MA01-SR-045 — OUTPUT

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-045: Unrealistisch kleine Ausbauwerte nachgelagert filtern; Schwelle nicht genannt.|
|Originalfundstelle|O26 §§3.1.2, 3.10 (S. 14, 30) (O-explicit-open)|
|L2 Requirement statement|**Sehr kleine Investitionsanteile beim Postprocessing nach einer formell freizugebenden methodischen Schwelle kennzeichnen/filtern.**|
|Begründung|Undokumentierter Schwellenwert ändert ausgewiesene Systembedarfe.|
|Input|Ausbaulösung und Filterkonvention|
|Output|Gefiltertes Bedarfsregister|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Postprocessing-Engine frei.|
|Verification Method|OutputAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Filter angewandt nur, wenn Schwelle offiziell freigegeben; sonst Bericht mit BLOCKED-Filterstatus.|
|L3 Required Formalisation|MA01-FR-045 (SMALL_EXPANSION_FILTER); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-045; Nachweisart: OutputAudit|
|Open Issues|FILTER-THRESHOLD|

### MA01-SR-046 — OUTPUT

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-046: Infrastructure-Gaps-Bericht, ONDP-Ergebnisse und Methodiktransparenz sind erwartete Outputs.|
|Originalfundstelle|O26 §2.2 (S. 9–11) (O-explicit)|
|L2 Requirement statement|**Methodisch vorgesehene Infrastructure-Gaps- und Offshore-ONDP-Ergebnisse samt zugehöriger Herkunft und Rechendefinition bereitstellen.**|
|Begründung|Mehrdeutige Kennzahlen verhindern Vergleichbarkeit.|
|Input|LF-/Zusatzläufe, Kandidaten, KPI-Definitionen|
|Output|Systembedarfsberichte und Outputmanifest|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Berichtformat frei; Outputsemantik nicht.|
|Verification Method|OutputAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Alle Pflichtoutputfamilien und Studienjahr-/Szenariolinien dokumentiert; KPI-Endorakel noch offen.|
|L3 Required Formalisation|MA01-FR-046 (NEEDS_REPORTING); PARTIAL_OWNER_DECISION_REQUIRED|
|L4 Verification Need|MA01-VN-046; Nachweisart: OutputAudit|
|Open Issues|OUTPUT-KPI|

### MA01-SR-047 — VERIFICATION

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-047: Dreiknoten-Plexos/Antares-Sanity-Check ist Beispiel der Vergleichbarkeit, keine universelle Zertifizierung.|
|Originalfundstelle|O26 §5.1 (S. 41–44) (O-descriptive)|
|L2 Requirement statement|**Das im Quelltext gezeigte Plexos/Antares-Beispiel nicht als Pflicht zur Verwendung dieser Tools behandeln; toolunabhängige Evidenz zu Gleichungs- und Ergebnissemantik vorsehen.**|
|Begründung|Beispielsoftware ist kein normativer Modellierungstool-Contract.|
|Input|Generiertes Modell, Prüfdaten, Bericht|
|Output|Quellen- und Tool-unabhängiger Nachweisstatus|
|Verbindlichkeit / Status|D_VERIFICATION_CONTROL; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Test- und Toolauswahl frei.|
|Verification Method|IndependentReview; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Keine Verpflichtung zur Benutzung der Beispielsoftware; überprüfbare Modellabdeckung und Ausführungsstatus.|
|L3 Required Formalisation|MA01-FR-047 (VERIFICATION_EVIDENCE); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-047; Nachweisart: IndependentReview|
|Open Issues|VERIF-ORACLE|

### MA01-SR-048 — DATA

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-048: Publizierte Startnetz-Projektliste mit NTC-Richtungen und Status als referenzierter Datensatz.|
|Originalfundstelle|O26 Anhang 6.2 (S. 52–56) (O-data)|
|L2 Requirement statement|**Die im Methodik-Anhang aufgeführten Referenznetzprojekte mit eindeutiger ID und quellenspezifischem Status in die Startnetzentscheidung einbeziehen.**|
|Begründung|Referenzprojektfehler schlagen auf Investitionsfreiraum durch.|
|Input|Annex-6.2-Projektliste, §3.4-Eignungsregel|
|Output|Versionierte Referenzprojektliste|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Importtechnik frei.|
|Verification Method|SourceAudit; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jedes vorhandene Projekt nach Identität, NTC-Orientierung und Inklusion/Exklusion zurückführbar.|
|L3 Required Formalisation|MA01-FR-048 (STARTING_GRID_REGISTER); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-048; Nachweisart: SourceAudit|
|Open Issues|GRID-ELIG|

### MA01-SR-050 — MODEL

|Attribut|Spezifikation|
|---|---|
|L1 Methodology Requirement|MA01-MR-050: Mehrere Stromzonen je Marktzone mit zonalen Preisvariablen, H2-Zonen, Offshore-Hubs und Sektorkopplung.|
|Originalfundstelle|O26 §3.3 (S. 15) (O-explicit)|
|L2 Requirement statement|**Die beschriebene Mehrzonen-Strom-/H2-Topologie einschließlich Interzonenfluss, zonalem Preis und Offshore-Hubs funktional repräsentieren.**|
|Begründung|Zonales Aggregat darf betroffene H2-/Offshore-Pfade nicht verschwinden lassen.|
|Input|Zonennetze, Offshore-Hubs, Konvertierungsknoten|
|Output|Sektorübergreifende Zonen- und Bilanztopologie|
|Verbindlichkeit / Status|O26_DRAFT_CONSTRAINED_DERIVATION; PROPOSED_NOT_APPROVED|
|Implementation Freedom|Native Bus/Hub/Link-Klassen frei.|
|Verification Method|ModelInspection; bisher **NOT_EXECUTED**|
|Acceptance Criteria|Jeder erforderliche Sektor-/Zonentyp und jede Umwandlungsverbindung in Modell und Output referenzierbar.|
|L3 Required Formalisation|MA01-FR-050 (MULTIZONE_COUPLING); FORMALISABLE_SUBJECT_TO_SOURCE_APPROVAL|
|L4 Verification Need|MA01-VN-050; Nachweisart: ModelInspection|
|Open Issues|H2-DETAIL|


## Domain-level acceptance logic

**PASS** must have an approved and applicable method-profile, exact obligation-to-generated-model mapping, independent test oracle and executed evidence. **FAIL** means observed violation of an approved obligation. **BLOCKED** covers source authority, missing KPI/discount/marine factor, unresolved tests or any unexecuted test critical to release. No complete, final conformance assertion is made by MA-01.
