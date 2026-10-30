# R-M0-CGMES-CONTRACTS-1 — 10 Requirements / Anforderungsvertrag

**Stand:** 2026-10-30 · **Dokumentstatus:** fachliche Spezifikation, nicht implementiert · **Contract-ID:** IOSN-M0-REQ/1.0.0  
**Verbindliche Projektbasis:** [Commit 1595d6d38e77804760612621657721b3699d2fea](https://github.com/AlOussama/TYNDP_Products/tree/1595d6d38e77804760612621657721b3699d2fea)  
**Gegenstücke:** [30_CANONICAL_DATA_CONTRACT.md](30_CANONICAL_DATA_CONTRACT.md), [50_VALIDATION_CONTRACT.md](50_VALIDATION_CONTRACT.md).

## 1. Auftrag, Status und Geltungsgrenzen

Modul 0 ist ein **backendunabhängiger Import-, Normalisierungs-, Mapping-, Export- und Qualitätsvertrag** zwischen CIM/CGMES-Daten und einem **unveränderten detaillierten** AC-/HVDC-Netz in tabellarischer, anschließend PyPSA-kompatibler Form. Unterstützt werden symmetrische stationäre Übertragungsnetze (positive sequence), mindestens Ein-IGM- und gekoppelte Mehr-IGM-/CGM-Eingaben. Die nachgelagerte Netzreduktion in Modul 1, Wetter-/PACD-Aufbereitung, Dispatch und Netzoptimierung sind **keine** Aufgaben von Modul 0.

### 1.1 Festgestellter Repository-Zustand (am Basiscommit gelesen)

- `README.md`: Methoden A/B und Reduktion sind Forschungsprototyp; reale TYNDP-Netzintegration ausdrücklich nicht nachgewiesen.
- `docs/REPOSITORY_AUDIT.md`: Branch/PST/HVDC sowie reale PyPSA-Integration und Quellenprovenienz sind offene Qualifikationen. Synthetische Ergebnisse sind keine Realnetzevidenz.
- `docs/current/IOSN_2026_Band_II_PyPSA_Implementierung.md`: Das detaillierte Originalnetz `n_d` ist **unveränderliche elektrische Evidenzquelle**. Modul 1 benötigt Bus-ID, AC-Insel, orientierte Leitungen/Transformatoren, effektive Impedanzen, Spannungsebenen, Status, Grenzwerte, PST-/HVDC-Typen und dokumentierte Basen. Die hochaufgelösten Eingabereihen und Reduktions-Busmaps sind **separate** Objekte.
- Zusätzlich geprüft: `src/tyndp_reduce/pypsa_adapter.py` ist ein absichtlich enger **eininseliges, nur aus Leitungen bestehendes** DC-Modell-Adapter. Er weist Transformatoren, Links/HVDC, Speicher und Phasenschieber zurück; `pyproject.toml` nennt `pypsa>=1.4,<2` als optionale Dependency. **Modul-0-Konformität impliziert keine sofortige Kompatibilität dieses bestehenden Modul-1-Adapters.** Der Übergang benötigt ein benanntes Capability-Gate (REQ-038).

### 1.2 Normative Einordnung und Versionsdisziplin

CGMES **2.4.15** bezeichnet den historischen ENTSO-E-Anwendungsprofilstand von 2014; CGMES **3.0** verweist auf IEC TS 61970-600-1/-2:2021. „2.4.15“ und „2.4“ werden in späteren ENTSO-E/IEC-Dokumenten nicht uneingeschränkt synonym verwendet; deshalb sind vollständige *profile URI, model version, profile release, producer, Datei-Hash* aus den gelieferten Headern zu speichern, nicht aus einem Dateinamen zu erraten [C1–C3].

| Profil | 2.4.15 | 3.0 | Zweck im Modul 0 |
|---|---|---|---|
| EQ | Pflicht für Equipment-Import | Pflicht | Equipment, Terminals, Connectivity |
| SSH | Pflicht für betrieblichen Zustandsimport | Pflicht | Betrieb, Schalter, P/Q, Tap-Positionen |
| TP | importieren/abgleichen, wenn geliefert; sonst aus EQ/SSH ableiten | analog | TopologicalNodes und Netztopologie |
| SV | optional beim unsolved Import, erforderlich für SV-Referenzvergleich | analog | berechnete Referenzspannungen/-Terminalflüsse, **keine** Stammdaten |
| EQ_BD / EQBD | bei Mehr-IGM/Boundary soweit vom Exchange benötigt | in IEC-2021 *deprecated*; für neue Exchanges Core-EQ, EQBD befristet als Übergangspfad nach passender Exchange-Policy | Grenzmodell und Authority-Abgleich |
| TP_BD / TPBD | bei entsprechendem 2.4.15-Boundary-Set | **nicht** als 3.0-Pflichtprofil fingieren | historische Boundary-Topologie |
| GL | optionaler ergänzender Import; Pflicht der *Prüfung*, falls geliefert | analog | `Location`/`PositionPoint`/CRS |
| DL, DY, SC, OP | nur referenziert/erhalten, sofern vorhanden; außerhalb Kernmodellierung | 3.0 ggf. `OP`/`SC`-Sicht | keine dynamische bzw. Kurzschluss-Simulation; verlustfreier unveränderter Pass-through in Modus 1 |

**Profil-Vollständigkeit ist use-case-abhängig.** Unsolved EQ+SSH kann zulässig sein, sofern Topologie deterministisch ableitbar ist; ein „solved“ Status oder AC-LF-Vergleich darf ohne geeignete TP/SV-Basis nicht behauptet werden. Für eine konkrete Austauschlieferung sind die tatsächlichen, versionsspezifischen ENTSO-E/IEC-Validierungsregeln und Boundary-Verträge verbindlich, nicht allein diese Tabelle [C1–C4]. Versionen dürfen nicht unkontrolliert in einer Exchange-Assembly vermischt werden.

### 1.3 Architektur und Qualitätsgates

`CGMES/RDF-Backend (extern) → Raw-Graph mit Referenzen → Canonical Tables v1 → mathematische elektrische Mappings → Detailed PyPSA View + Sidecar → Modul 1`.  
Reverse: `PyPSA Delta + Canonical + Raw-Graph → profilbewusster Export-Patcher (Modus 1)` bzw. `PyPSA + explizite Konstruktionsvorgaben → neuer CGMES-Graph (Modus 2)`. Backend-Auswahl ist **nicht** Teil dieser Entscheidung.

Gates: **G0** Profil-/Datei-/Modell-Scope; **G1** Objekt-/FK- und Boundary-Integrität; **G2** elektrische Parameter, Topologie, Basen; **G3** PyPSA-Eignung je Modellierungsklasse; **G4** Exportfähigkeit/Loss-Manifest; **G5** optionale stationäre Referenzprüfung. Failure-Policy: **BLOCK** vor Übergabe bei fehlendem kritischem Netz-/Identity-Feld, sonst `CONDITIONAL` mit quantifiziertem, explizit quittiertem Downgrade. Jede Annahme ist objekt- und attributbezogen zu protokollieren.

## 2. Prüffähiger Anforderungskatalog

**Interpretation:** MUSS ist ein Freigabegate der jeweiligen Capability; SOLL ist begründungsbedürftig abweichbar; OPTIONAL wird nur bei expliziter Aktivierung geschuldet; AUSSERHALB DES SCOPES erzeugt keine Implementierungspflicht. **T-xx** bezeichnet den *später zu implementierenden, derzeit nicht ausgeführten* Nachweis in [50_VALIDATION_CONTRACT.md](50_VALIDATION_CONTRACT.md). Die angegebenen Akzeptanzkriterien sind normativ **für diese Modul-0-Spezifikation**, nicht offiziell von ENTSO-E vorgegebene Konformitätstoleranzen.

### A. Austausch, Profilsemantik, Provenienz

| ID | Klasse | Anforderung | Akzeptanzkriterium für MUSS | Testnachweis |
|---|---|---|---|---|
| REQ-001 | MUSS | 2.4.15 und 3.0 als explizite getrennte Profiladapter | Zwei Profilfamilien mit realen Version-/URI-Metadaten unterscheidbar; unbekanntes Profil blockt profilabhängige Interpretation | T-01 |
| REQ-002 | MUSS | EQ/SSH auswerten, TP/SV bedarfsabhängig verarbeiten | Equipment und Betriebszustand getrennt; TP/SV als gelieferte/abgeleitete/nicht-verfügbare Quelle markiert | T-01, T-02 |
| REQ-003 | MUSS | Einzel-IGM sowie mehrere IGMs/CGM zusammenführen | Assembly mit Cross-Model-Referenzen und separaten MAS/Authority-Bezügen; keine Objektverdoppelung | T-03 |
| REQ-004 | MUSS | 2.4.15 EQ_BD/TP_BD bzw. 3.0-Boundary-Semantik unterscheiden | Versionsgerechte Boundary-FK-Validierung; kein fiktives 3.0-TPBD verlangt | T-03 |
| REQ-005 | MUSS | Datei-/Graph-/Modell-/Profil-Metadaten speichern | Version, Source-URI, Profil, Header-MD, Hash, Import-Run, Authority auf jedes Quellobjekt rückführbar | T-01, T-04 |
| REQ-006 | MUSS | Original-mRID und unveränderliche interne ID getrennt führen | Eindeutiger Namespace; gleiche Quellidentität profilübergreifend vereint, konfligierende Kollision BLOCK | T-04 |
| REQ-007 | MUSS | Keine stillschweigende Verwerfung unbekannter Attribute | Opaque-Attribut-/Referenz-Ledger und Objektbezug oder expliziter unvermeidbarer Verlust mit BLOCK/Quittierung | T-04, T-21 |
| REQ-008 | MUSS | Deterministische, idempotente Reimporte und Update-Regeln | Gleiche Input-Hashes+Config liefern identische Objekt-IDs/Werte; Delta-Änderungen atomar; keine impliziten Deletes | T-05 |
| REQ-009 | MUSS | Backendunabhängiges kanonisches Format | Keine Backend-Klassentypen in Tabellen; identischer Fachgraph aus zwei Backend-Abbildungen gleich canonicalisiert | T-06 |
| REQ-010 | MUSS | Profile/Graphen ohne Verfälschung erhalten für Export 1 | Nicht veränderte semantische Tripel/Referenzen bleiben erhalten; Originalgraph bzw. verlässliche verlustfreie Kopie ist vorhanden | T-21 |
| REQ-011 | SOLL | GL-/DL-Informationen zur Wiederverwendung bewahren | — | T-11, T-21 |
| REQ-012 | OPTIONAL | Weitergabe zusätzlicher SC/OP/DY-Attribute als opake Daten | — | T-21 |

### B. Topologie, Geografie und Betriebszustände

| ID | Klasse | Anforderung | Akzeptanzkriterium für MUSS | Testnachweis |
|---|---|---|---|---|
| REQ-013 | MUSS | Terminal-, ConnectivityNode-, TopologicalNode-Beziehungen führen | Jeder aktive Port genau einem gültigen topologischen Bus pro Zustand zugeordnet oder BLOCK | T-07 |
| REQ-014 | MUSS | Switch-Open, NormalOpen, Terminal-Connected, Equipment-inService getrennt behandeln | Varianten mit offen/geschlossen/out-of-service ergeben erwartete Inseln; keine implizite Kurzschlussbrücke | T-07 |
| REQ-015 | MUSS | TP gegen aus EQ/SSH hergeleitete Topologie prüfen | Abweichung wird objektbezogen gemeldet; Override nur über explizite, versionierte Policy | T-08 |
| REQ-016 | MUSS | Elektrische Inseln vollständig und deterministisch ableiten | Aktive AC-Knoten haben genau eine Insel; isolierte Knoten identifiziert; HVDC verbindet nicht AC-synchron | T-09 |
| REQ-017 | MUSS | VoltageLevel/Substation/Country-Zuordnung erhalten | Für alle freigegebenen AC-Busse eindeutiger Country-Registry-Code (ISO 3166-1 alpha-2 oder explizit genehmigte Erweiterung); Herkunft belegt | T-10 |
| REQ-018 | MUSS | Geopositionen plus CRS und Zuordnungstyp modellieren | Positionswerte nur mit deklariertem CRS; fehlend/mehrdeutig explizit; keine stillschweigende Koordinatenannahme | T-11 |
| REQ-019 | SOLL | Geometrie von Leitungszügen und mehreren PositionPoints erhalten | — | T-11 |
| REQ-020 | SOLL | Optionale Substation-Zentroiden nur als abgeleitete Approximation | — | T-11 |

### C. Geräte, elektrische Parameter und Grenzen

| ID | Klasse | Anforderung | Akzeptanzkriterium für MUSS | Testnachweis |
|---|---|---|---|---|
| REQ-021 | MUSS | ACLineSegment und EquivalentBranch elektrisch getrennt repräsentieren | Je gültigem aktiven Zweig eindeutige Endports, orientierte Serien-/Shuntwerte, Equipmentklasse | T-12 |
| REQ-022 | MUSS | 2- und 3-Wicklungstransformatoren abbilden | Alle Wicklungen erhalten; 3W-Sternknoten/Ersatzäste eindeutig, reproduzierbar rückführbar | T-13 |
| REQ-023 | MUSS | Ratio-/Phase-Tap-Changer mit Regel- und Positionsinformation | Tap-Seite, Schritt, Neutral, Position, Shift, Limits; ggf. fehlerhafte Kombination BLOCK | T-14 |
| REQ-024 | MUSS | Erzeugung, Last und externe Einspeisung differenzieren | Geräteidentität, Status, Anschluss, P/Q, Technologie/Quellklasse, Steuer-/Q-Grenzen wo geliefert | T-15 |
| REQ-025 | MUSS | Lineare/nichtlineare und diskrete Shunts semantisch erhalten | g/b und Abschnitts-/Schaltzustand nachvollziehbar; vereinfachte Äquivalente als solche markiert | T-16 |
| REQ-026 | MUSS | HVDC-Terminals, Converter und DC-Branches erhalten | AC-Port(s), DC-Port-/Verbindungsschema, Kontrollmodus und Verluste/Unknowns getrennt | T-17 |
| REQ-027 | MUSS | Einheiten- und Basisumrechnung prüfbar | Ω/S, kV, MW/Mvar/MVA, pu-Basen ohne unbenannte Skalierung; repräsentative Rückrechnung | T-12, T-13, T-18 |
| REQ-028 | MUSS | Geräte-Status und netzbetriebliche Grenzwerte nicht verwechseln | InService-/Switch-/Grenzwerte unabhängig; Limits mit Terminal, Richtung, Dauer, Gültigkeit, Quelle | T-19 |
| REQ-029 | MUSS | Permanente und temporäre Grenzwerte getrennt speichern | Normal-/Notfall-, Dauer-, saison-/szenariobezogene Grenzen nicht zu einem undokumentierten `s_nom` verschmolzen | T-19 |
| REQ-030 | MUSS | Fehlende, widersprüchliche, null/singuläre Parameter abfangen | Keine numerisch unzulässigen aktiven Zweige im freigegebenen Modell; Default nie als Quelle ausgegeben | T-18 |
| REQ-031 | MUSS | Verschiedene P/Q-, Branch- und DC-Vorzeichen nachweisbar konvertieren | KCL- und Endportbilanz-/Verlustvorzeichen stimmen in Prüffällen | T-15, T-17 |
| REQ-032 | SOLL | Soweit verfügbar Generator-Regelziele und Capability-Curves mitgeben | — | T-15 |
| REQ-033 | OPTIONAL | Zusätzliche feine Technologieklassifikation über kontrolliertes Vokabular | — | T-15 |

### D. PyPSA, Update/Export, Qualität und Betriebsmodell

| ID | Klasse | Anforderung | Akzeptanzkriterium für MUSS | Testnachweis |
|---|---|---|---|---|
| REQ-034 | MUSS | Lesbare versionierte Mapping-Policies (YAML) | Schema-/Rule-ID, Version, Eingangsprofil, Feld-/Statusregeln, explizite Parameter, Defaults/Fehlerrouten | T-06 |
| REQ-035 | MUSS | Mathematische Umformungen **nicht** als ungeprüfte YAML-Formeln | YAML selektiert geprüfte `function_id`; Tests für komplexe Admittanz, p.u., Tap, Topologie | T-12–T-18 |
| REQ-036 | MUSS | Kanonische Werte mit Quality-/Origin-Status | Jedes abgebildete elektrische Attribut trägt SOURCE/DERIVED/DEFAULT/MISSING und Provenienz | T-04, T-18 |
| REQ-037 | MUSS | PyPSA-kompatible detaillierte *View* erzeugen | Busse, aktive passive AC-Branches, Generator/Load/Shunt und vereinfachte Links mit aktiven, stabilen IDs | T-20 |
| REQ-038 | MUSS | Fähigkeitsgrenze zum vorhandenen Modul-1-Adapter kennzeichnen | Unsupported Transformator/PST/HVDC/Mehrinsel führt `UNSUPPORTED_FOR_REDUCTION_ADAPTER` oder separater Qualifikation, **nicht** zu stiller Ausblendung | T-20 |
| REQ-039 | MUSS | Originalnetz von Zeitreihen und Reduktionsprodukten trennen | Detailnetz versioniert und unveränderlich; Wetter-/Dispatch-/Busmaps erzeugen keine Mutationen darin | T-20 |
| REQ-040 | MUSS | Exportmodus 1: Identitätsstabile graphbasierte Aktualisierung | Nur zulässige Änderungen als semantischer Delta-Patch; unveränderte IDs/Relationen/Tripel erhalten | T-21 |
| REQ-041 | MUSS | Exportmodus 2: CGMES-Neuerzeugung nur bei ausreichenden Daten | Fehlende erforderliche CIM-Objekte, Authority oder Header-Metadaten ⇒ BLOCK bzw. unvollständiges Artefakt ausdrücklich **nicht export-ready** | T-22 |
| REQ-042 | MUSS | Unterschiedliche Verlustverträge pro Exportmodus | Feldgenaue Support-Matrix `EXACT/APPROX/NONRECONSTRUCTIBLE` plus Loss-Manifest je Export | T-21, T-22 |
| REQ-043 | MUSS | Export- und Importqualifikation getrennt ausweisen | IMPORT_READY, PYPSA_READY, UPDATE_EXPORT_READY, CREATE_EXPORT_READY als unabhängige Gate-Ergebnisse | T-21–T-24 |
| REQ-044 | MUSS | Atomare Export-Transaktionen und reproduzierbare Reports | Kein Teil-Commit nach Blocker; Hashes, Config-Version, Source-/Zielversion, QA und geänderte IDs dokumentiert | T-05, T-22 |
| REQ-045 | MUSS | Validierung inkl. Boundary, Topologie, Einheiten, LF, Round-trip | Verbindliche Matrix T-01…T-24 vorhanden; alle obligatorischen Prüfungen für gewählte Capability PASS | T-01–T-24 |
| REQ-046 | SOLL | Qualifizierter SV-basierter AC-Lastfluss-Abgleich | — | T-23 |
| REQ-047 | SOLL | Massenoperationen, Partitionierung, Spaltenformate skalierbar | — | T-24 |
| REQ-048 | OPTIONAL | Analytische Datenqualitäts-Dashboards | — | T-24 |

### E. Ausdrücklich außerhalb des Scopes

| ID | Klasse | Gegenstand |
|---|---|---|
| REQ-X01 | AUSSERHALB DES SCOPES | unsymmetrische Phasen-/Niederspannungs-Verteilnetzmodellierung |
| REQ-X02 | AUSSERHALB DES SCOPES | Schutz-, Kurzschluss- und vollständige dynamische Simulation (opake Weitergabe von Daten erlaubt) |
| REQ-X03 | AUSSERHALB DES SCOPES | Wetterjahrauswahl, Wetterdaten, PACD, Pmax/Inflows, Demand Forecast |
| REQ-X04 | AUSSERHALB DES SCOPES | Marktsimulation, Optimierungs-Dispatch und Zeitreihen-Erzeugung |
| REQ-X05 | AUSSERHALB DES SCOPES | Clustering, PTDF-basierte Reduktion, F0-Kalibrierung und zonale N-1-Äquivalentgrenzen |
| REQ-X06 | AUSSERHALB DES SCOPES | detaillierte VSC/LCC-HVDC-Dynamik, MTDC-Schutz und anspruchsvolle HVDC-Regelung |
| REQ-X07 | AUSSERHALB DES SCOPES | Auswahl, Fork oder Eigenimplementierung einer produktiven CGMES-RDF/XML-Engine |
| REQ-X08 | AUSSERHALB DES SCOPES | Behauptung einer ENTSO-E- oder IEC-CGMES-Konformitätszertifizierung allein aufgrund dieses Entwurfs |

## 3. Priorisierter Mindestlieferumfang / Definition of Ready

**DR-1 — Dokumentvertrag:** Tabellenregister und Feldtypen in 30 sowie Testkatalog in 50 behandeln jedes MUSS; die Gegenstücke haben identische Bedeutungen für IDs/Einheiten. **DR-2 — Backend- und Versionsneutralität:** verpflichtende Profile werden über versionsgebundene Interpretationen gelesen; kein generischer Reflex „RDF parse ⇒ elektrisches Netz“. **DR-3 — Verlusttransparenz:** jede projektionstreue, approximierte oder nicht rekonstruierbare Eigenschaft ist differenziert sichtbar. **DR-4 — Modul-1-Grenze:** das bestehende Reduktionsadapter-Gate wird nicht umgangen. **DR-5 — keine Ausführungsbehauptung:** diese Spezifikation enthält ausschließlich künftige Akzeptanz-/Testpflichten, keine ausgeführten Tests.

**Nicht verhandelbare fachliche Invarianten:** eindeutige Provenienz, exakte Referenzintegrität, keine Phantombusse, keine stillen geänderten Vorzeichen/Basen, keine stillen Löschungen, AC-Inseln getrennt von steuerbaren HVDC-Pfaden und explizite Grenzen der Exportierbarkeit.

## 4. Entscheidungen, konservative Annahmen und Restrisiken

1. **D-01:** Canonical v1.0 ist *logisch* tabellarisch, mit relationalen IDs und referenzierten Opaque-Attributen; ein physisches Format (Parquet, SQL, Arrow) ist noch keine Architekturvoraussetzung.
2. **D-02:** Für freigegebene Übertragungs-Busse ist `country_code` MUSS; Geokoordinaten sind nullable und müssen bei Fehlen im Quality-Report erscheinen. Eine Geolücke ist **kein** Anlass für fiktive Koordinaten. Für räumliche Folgealgorithmen kann dies ein eigenes nachgelagertes Blocking-Gate sein.
3. **D-03:** Ein 3-Wicklungstransformator wird für PyPSA als Stern-Ersatz mit künstlichem internem Bus modelliert; das **ursprüngliche** dreipolige Equipment bleibt im Canonical-Graph erhalten.
4. **D-04:** Die ungeprüfte Nutzung von PyPSA-`TransformerType` ist untersagt, wenn sie Quellparameter überschreiben würde; explizite Parameterübertragung hat Vorrang.
5. **D-05:** HVDC wird für einen begrenzten steady-state Transportfall als steuerbarer Link/Portverbund abgebildet; differenzierte Verlust-/Regelmodelle werden nicht „exakt“ genannt.
6. **D-06:** Standardeigenschaften aus PyPSA sind **keine** CGMES-Quelle. Jeder erzwungene Default mit elektrischem Effekt erfordert Policy und Auswirkungsanzeige.
7. **D-07:** Bei CGMES-Neuerzeugung wird kein historischer mRID erfunden. Neu erzeugte IDs bekommen einen dedizierten Namespace/Authority und nachvollziehbare Generierungsregel.
8. **D-08:** Konkrete Datensätze und Backendimplementierungen müssen gegen IEC/ENTSO-E-Constraints versioniert qualifiziert werden; die vorliegenden Dokumente sind **interne Implementierungsverträge**, keine externen Zertifikate.

## 5. Quellen und Vorrang

**Projektprimärquelle:** [README](../../../README.md), [REPOSITORY_AUDIT](../../REPOSITORY_AUDIT.md), [Band II](../IOSN_2026_Band_II_PyPSA_Implementierung.md), jeweils Basiscommit; außerdem `src/tyndp_reduce/pypsa_adapter.py` (gleicher Commit).

- **[C1]** ENTSO-E, [CGMES Library; v2.4 und v3.0, IEC-Bezüge und Dokumente](https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/).
- **[C2]** IEC, [TS 61970-600-2:2021, CGMES exchange profiles specification](https://webstore.iec.ch/en/publication/63867); und IEC TS 61970-600-1:2021 (*structure and rules*), siehe C1.
- **[C3]** ENTSO-E, [CGMES 2.4.15 (2014), Profilübersicht](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/140807_ENTSOE_CGMES_v2.4.15.pdf), sowie [Implementation Guide](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/160315_ImplementationGuide_CGMES_2_4_15.pdf).
- **[C6]** ENTSO-E, [Boundary and Reference Data Exchange Specification v1.0, §1](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/Boundary_and_reference_data_exchange_specification_v1.0.pdf): CGMES 3.0 ohne TPBD, EQBD im Übergang, Core-EQ bevorzugt.
- **[C4]** ENTSO-E, [Questions and answers on CIM/CGMES data exchange v1.0.1](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/QandA_on_CIM_CGMES_based_data_exchange_implementation_v1-0-1.pdf) (historische Versionseinordnung).
- **[P1]** PyPSA, [Components und Attributverträge](https://docs.pypsa.org/latest/user-guide/design/), [Power Flow](https://docs.pypsa.org/latest/user-guide/power-flow/).
- **[S1]** [SiennaSchemas – Single Source of Truth / unit-annotated schemas](https://github.com/Sienna-Platform/SiennaSchemas/blob/main/docs/PIPELINE.md).
- **[G1]** [Power Grid Model IO – Converter, Mapping/Units/IDs](https://power-grid-model-io.readthedocs.io/en/stable/).

**Quellenhierarchie:** (1) gültige IEC-/ENTSO-E-Profile und konkrete Exchange-Pakete, (2) geprüfte PyPSA-Komponentenimplementierung in gepinnter Version, (3) dieser interne fachliche Datenvertrag, (4) Backend-/Converter-Beispiele. Widersprüche sind zu dokumentieren, nicht zu überdecken.
