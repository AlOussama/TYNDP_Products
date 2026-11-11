# ML-R03 — Data Governance, Provenance & Quality Rules
**Status:** NON_NORMATIVE_RESEARCH_DRAFT · **Baselinerisiko:** `G1_REMAINS_BLOCKED`, `AUTHORITY_UNCONFIRMED`, `NOT_DATA_QUALIFIED`

## 1. Verschiedene Freigabe- und Validierungsebenen
| Ebene | Prüft was? | Realer Baselinestatus | Kann diese Untersuchung positiv entscheiden? |
|---|---|---|---|
| T0 Schema/technische Struktur | Pflichtattribute, IDs, Formate, Datenachsen | neue synthetische Prototypen prüfbar | **Ja, nur technischer Vertragsentwurf** |
| T1 Semantische Referenzen | Objekt-/Profil-FKs, Dimension, Zuordnungen, Carrier | 93 vorgeschlagene Links strukturell vorhanden, fachlich unbestätigt | Struktur ja, Methodik nein |
| T2 Externe Datenqualität | Originaldatei, exakte Releaseversion, Byte-Hash, fachliche Werte, Frozen-Run-Nachweis | **87/87** ohne qualifiziertes tatsächliches IoSN-Originaldatenfile/-hash | **Nein** |
| T3 Transformationskorrektheit | Validierung gegen Originalnetz/Originalprofile mit definierter Toleranz | 28/28 ursprüngliche Datentests nicht an Originalpayload ausgeführt | **Nein** |
| T4 Fach-/Mathekonformität | Methodik, LP-Constraints, Outputdefinition, unabhängige Orakel | Ownerentscheidungen offen | **Nein** |
| T5 Governance-/Owner-Abnahme | anerkannte Methodik-/Daten-/KPI-Releases, Reviewer/Unterschrift | G1 blockiert; keine qualifizierte Ownerfreigabe | **Nein** |

**Verifikationsgrenzen:** `TECHNICAL_TEST_PASS` ist ein Nachweis nur für die getesteten synthetischen Invarianten. `SOURCE_QUALIFIED`, `MATHEMATICAL_CONFORM` und `OWNER_APPROVED` bedürfen jeweils eigener Evidenz.

## 2. Provenienzgraph — verbindliche *Felder*, nicht freigegebene originale Instanzen
**SourceNode:** `source_id, canonical_origin_url, owner, license/access, original_file_name, original_file_version, original_file_sha256|null, bytes_retrieved|null, publication_date, original_time/space/unit basis, source_qualification_status`.

**ExtractionNode:** `extraction_id, source_artifact_ref, extraction_query_or_spec, selected_year/scenario/CY, data_slice_identity, operator, executed_at, resulting_instance_id`.

**TransformNode:** `transform_spec_id, implementation_version, execution_id, input_instance_refs, output_instance_refs, parameter_values_and_status, mapping_version, conversion_history, conservation_evidence, start/end_utc, quality_outcome`.

**ModelNode:** `run_id, type(P10..P15), tool_id_and_version_for_reproduction_only, canonical_model_input_version, frozen_input_manifest_id, model_config, solver_status_and_witness_ref`.

**ReportNode:** `metric_definition_ref, calculation_version, raw_result_refs, aggregation_scope, filter_ref, evidence_status, owner_review_ref, published_need_id`.

Jede echte Datei muss vor Data-Qualification reale Bytes und **tatsächlich berechneten** SHA-256 erhalten. `NOT_COMPUTED`/`UNKNOWN`/`null` bleiben bis dahin sichtbar. Placeholder-Release-IDs in `synthetic_contract_examples/` beginnen ausdrücklich mit `SYN-` und dürfen **nicht** mit produktiven Quellen verglichen werden.

## 3. Technische Invarianten (forschungsweise prüfbar)
| Rule-ID | Regel / Fehlermeldung | Technischer Test |
|---|---|---|
| `DQ-001` | pro Dateninstanz PK und Ref-Namespaces eindeutig | Duplicate ID → FAIL |
| `DQ-002` | jede FK auf existierende Dateninstanz, Definition, SourceRelease oder Run | Dangling reference → FAIL |
| `DQ-003` | `study_year∈{2035,2040,2050}` ohne implizite jahresübergreifende Verbindung | unbekanntes Jahr → FAIL |
| `DQ-004` | CY1–CY5 pro Studienjahr; keine Re-Selektion | fehlende/zusätzliche/doppelte CY → FAIL |
| `DQ-005` | der Gewichtsvektor je CY über alle drei Zieljahre identisch; reale Zahlen und Normalisierungstoleranz TBD | synthetische Gleichheitstestfälle; reale Freigabe offen |
| `DQ-006` | Halb-offene Zeitintervalle in UTC mit Dauer, `end > start` | Offset/DST/Überlappung → FAIL |
| `DQ-007` | Einheiten und Dimensionen konsistent; Umrechnung nach explizitem Operator | MW≠MWh; H2 LHV/HHV nicht still austauschen |
| `DQ-008` | Quell-/Zielreferenz für räumliche Zuordnungen, keine implizite Summierung | Crosswalk FK und Faktoren prüfen |
| `DQ-009` | technische Erhaltung ausschließlich bei geeigneten extensiven Größen; sonst `TBD_ORACLE` | Source-target integral unter deklarierter Toleranz |
| `DQ-010` | natürliche saisonale/direktionale Grenzen der Netzreferenz erhalten | Missing direction/season → FAIL |
| `DQ-011` | jede Ableitung besitzt validen Transform-/Run-Lineage-Pfad | fehlt → FAIL |
| `DQ-012` | jedes Ergebnis referenziert einen tatsächlich deklarierten Run und Solverstatus | Unknown run → FAIL |
| `DQ-013` | RawResult und DerivedMetric sind getrennte Typen | Output-of-solver als KPI ohne Definition → FAIL |
| `DQ-014` | Pflichtdaten nicht vorhanden ⇒ Lauf/Veröffentlichung `RELEASE_BLOCKED` | kein Default 0 / leer / Draft |
| `DQ-015` | optional P15 hat explizite `NOT_RUN`-Disposition | Nichtausführung ist kein Kernprozess-FAIL |
| `DQ-016` | jede echte Source-Qualification bindet Originalbytes+Release+Hash | source_hash=null => `SOURCE_UNVERIFIED` |
| `DQ-017` | Candidate stage tags / shared `x` über CY prüfbar | falscher Stage-Index → FAIL |
| `DQ-018` | offener Ownerparameter wird nicht auto-vorausgesetzt | TBD formula/factor/threshold → `BLOCKED` |
| `DQ-019` | veröffentlichter Bedarf darf nicht mit genehmigtem Projekt verwechselt werden | `PROJECT_APPROVED` ohne Externentscheid → FAIL |
| `DQ-020` | jedes Prüfresultat hat Testklasse, Ausführung, Oracle/Evidence und Reviewerstatus | `PASS` ohne Ausführungsnachweis → FAIL |

Diese Regeln sind **Contract-Vorschläge**. Sie ersetzen nicht die 28 in BUNDLE-01 beschriebenen, aktuell blockierten Originaldatentests; mathematische bzw. Datenqualitäts-Toleranzen müssen fachlich bestätigt werden.

## 4. Fail-Closed und Anwendbarkeitslogik
```text
if missing(required_object) or unresolved(required_identity_map):
    block(PRODUCTION_EXECUTION, reason)
if unresolved(methodology_profile_owner) or original_release_unqualified:
    block(RELEASE, reason)
if conditional_step == P15 and option_not_authorized:
    mark(OPF_NOT_RUN_BY_DESIGN)   # not the same as a failed core workflow
if formula_ref == TBD:
    emit(metric_status=UNDEFINED_METRIC, value=null)
if test_not_executed:
    emit(test_status=NOT_EXECUTED) # never PASS
```
Ein Objekt kann für einen spezifischen Lauf nicht anwendbar sein, etwa P12-Speicherausbau für 2035 oder P15 ohne explizite OPF-Entscheidung. `NOT_APPLICABLE` erfordert einen dokumentierten fachlichen Grund. `MISSING`, `UNKNOWN`, `UNAPPROVED` und `NOT_APPLICABLE` sind verschiedene Zustände.

## 5. Governance-Prämissen und Authority-Auflösung
Die Nutzerentscheidungen **D1–D6** gelten für die Forschungsverträge gemäß ML-R03-Brief: neueste maßgebliche Methodik, historische Fassung bei dortigen Lücken **nur gekennzeichnet**; endgültige Methodik-/Ownerantworten werden verschoben; CY1–CY5 für 2035/2040/2050, gleiche numerisch offene Gewichte; Wetterauswahl außerhalb; UTC, explizite Intervalle und Umrechnungen; Fail-Closed; toolneutrale fachliche Schnittstelle. Nicht überlieferte Einzelbeschlusstexte/MD-12-Toleranzdetails bleiben `TBD` statt einer behaupteten Beschlussrekonstruktion.

**Konfliktregister:** O26-Draft nennt drei konkrete Wetterfälle je Studienjahr; aktive Forschungsprämisse nennt fünf identische CY-IDs je Studienjahr. Das ist ein **bewusster nichtnormativer Profil-Override**, keine Aussage über eine offiziell geänderte ENTSO-E-Methodik. Ebenso gilt eine Draft-Angabe wie 102 Zonen oder 4% WACC nicht ohne Ownerbeschluss als exekutierbare Defaultregel.

**Ownerrollen (vorgeschlagen):** Methodology Release; Data/Scenario Freeze; Weather and Calendar; TSO Grid & Reduction; Market/H2/Hydro/Storage; Investment & Economics; KPI & Reporting; Independent QA. Rollen sind keine bestätigten Personen/Freigaben.

## 6. Kausalität, Versionsführung und Änderungswirkung
`MethodologyProfile → DataObjectDefinition/TransformSpec → Dataset/SourceRelease → ModelInputBundle → RunResult → MetricDefinition/Value → PublishedNeed → ReviewEvidence`. Das Modell führt zwei disjunkte Versionen: (a) normative/reale Quellen- und Ownerakte (derzeit nicht verfügbar), (b) versionierte **Forschungsannahmen**. Änderungswirkung ist über `B01-Dxxx`, `MA01-SR-xxx`, `MLR03-Txx-yy` und `MD-xx` rückverfolgbar.

Bei Wechsel eines Dataset-Release, Geo-/Temporal-Mappings oder einer Formeldeklaration müssen abhängige Outputs als `STALE_UNTIL_RECOMPUTED` markiert werden. Weder gilt ein Versionswechsel als automatisch austauschbar noch eine formal gültige Datei als fachlich kompatibel.

## 7. Adversarial-Review-Fokus und unabhängiger Sign-off
Fehlerfälle: falscher Zeit-Offset; doppelte Profile; stilles 2030; Gleichheitsbruch Wettergewichte; fehlender Originalfile-Hash; ungerichtete NTC; H2 LHV/HHV vermischt; Kandidat als physischer AC-Mesh-Zweig; doppelte Stage-1-Kosten; P12 in 2035; P14-Baseline nicht eingefroren; ungebundene P15-OPF; Kosten unterschiedlicher Preisjahre; ungenehmigte KPI-Formel; gewichtslose Veröffentlichung.

Unabhängigkeit ist **organisatorisch**: Ein separater KI-Reviewdurchgang in `data_contract_review.md` ist nur ein adversarielles Selbstreview des Forschungspakets, keine unabhängige menschliche Zertifizierung. **G1 weiterhin BLOCKED.**
