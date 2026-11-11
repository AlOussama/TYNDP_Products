# ML-R03 — IoSN Data Semantic Model
**Version:** 0.1.0 · **Status:** NON_NORMATIVE_RESEARCH_DRAFT · **Baseline:** BUNDLE-01R PR #25, commit `5c13d4d63f18d30c308997cd7a01f2977fcc6b7b` · **Date:** 2026-11-11

## 1. Forschungsfrage und Geltungsgrenze
Dieser Entwurf beschreibt die **fachliche Außenschnittstelle** eines IoSN-Prozesses einschließlich Governance, externen Daten, Preprocessing-Artefakten, Modellinput, Rohoutput und Berichtsgrößen. Er definiert weder ein bestimmtes Solver-/Toolformat noch freigegebene Methodik, Originaldaten oder eine normative DSL. Eine erfolgreiche Prüfung synthetischer Objekte ist ausdrücklich **kein** Nachweis der IoSN-Originaldaten oder einer Modellimplementierung. Gate G1 bleibt laut BUNDLE-01R blockiert.

**Quellenrangfolge für die Forschung:** (1) tatsächlich verifizierte neueste Methodikfassung, soweit verfügbar, (2) ältere Methodik nur als explizit gekennzeichnete historische Ergänzung bei Lücken, (3) Ownerentscheidungen als noch zu liefernde Autorität. Die Konsultationsfassung O26 ist als verifizierte *Draftquelle*, nicht als angenommene Endfreigabe behandelt. Konflikte werden versioniert, nicht stillschweigend aufgelöst. MA-03/BUNDLE-01/BUNDLE-01R bleiben unverändert.

## 2. Nachprüfbare Coverage
| Baseline-Klasse | Objekte | Vertragsrolle |
|---|---:|---|
| `EXTERNAL_UPSTREAM_DATA` | 42 | Externe Eingänge, deren Quelldateien nicht als IoSN-Run qualifiziert sind |
| `IN_SCOPE_INTERMEDIATE_OR_PRIOR_STEP_OUTPUT` | 35 | Intern entstandene oder von vorherigen IoSN-Schritten übertragene Ergebnisse |
| `GOVERNANCE_OR_CONFIGURATION_INPUT` | 6 | Dokument-/Freigabe-/Kalender-/Laufsteuerungsdaten |
| `STUDY_CONFIGURATION_REFERENCE` | 1 | Studienjahre und Variante |
| `EXTERNAL_DATA_RELEASE_REFERENCE` | 1 | Upstream-Release-/Extraction-Referenz |
| `VERIFICATION_REFERENCE_OR_APPROVAL_INPUT` | 2 | Orakel/Prüf- und Reviewinput |
| **Summe** | **87** | **Vollständige 1:1-Daten-ID-Coverage** |

Die ursprünglichen `B01-D001`–`B01-D087` wurden **nicht** umnummeriert. `input_contract_catalogue.csv` führt je Objekt Klasse, Rolle, Quelle, Objekt-/Referenzschlüssel, vorgeschlagene Attribute, Dimension, Zeit-/Raumbezug, Studien-/CY-Achsen, vorgeschlagenen Produzenten und Verbraucher, MA01-SR-Verweise, 93 bestehende Link-IDs, bedingte Ausführung, Daten-/Reviewstatus und offene Eigenschaften. **67/87** Objekte besitzen direkte vorgeschlagene SR-Links, **20/87** sind nur Prozess-linked. Alle 93 Links bleiben fachlich unbestätigt. Erzeugerzuordnungen und hinzugefügte Attribute sind **Forschungshypothesen**, keine Rückänderung der ursprünglichen Inventur.

## 3. Technologieunabhängiges logisches Metamodell
Die folgende semantische Typschicht ist unabhängig von YAML, JSON, UML, SysML und sämtlichen Energiesystemtools.

| Entität | Identität und Mindestfelder | Relationen / Kardinalität |
|---|---|---|
| `MethodologyProfile` | profile_id; version; authority_status; effective_from; clause_refs | 1 Profil pro deklariertem Vertragslauf; niemals implizit als genehmigt |
| `GovernanceDecision` | decision_id; owner_role; state; evidence_ref; effective_scope | 0..n pro Profil oder Parameter; `TBD` bleibt eigenständig |
| `SourceRelease` | source_id; release_id; source_owner; licensing/access; published_at; frozen_at; signature_state | 0..n reale Quellartefakte; unqualifizierte Quellen kennzeichnen |
| `SourceArtifact` | artifact_id; source_release_ref; file_name; file_version; sha256_or_missing_status; extraction_spec | 1 Release pro Datei; echter Hash nur aus tatsächlich beschafften Bytes |
| `DataObjectDefinition` | `B01-Dxxx`; class; type; mandatory_if; dimensions; keys; quality_rules | 1 pro Inventar-ID; mehrere Instanzen je Lauf möglich |
| `DataInstance` | instance_id; object_definition_ref; source/prod_ref; axes; unit; value_form; status | 1 Definition; 0..n Herkunftskanten |
| `AxisBinding` | study_year; scenario; CY_id; time_interval; spatial_id; carrier; direction | Dimensionen nur dort verpflichtend, wo fachlich anwendbar |
| `IdentityCrosswalk` | source_namespace/id; target_namespace/id; mapping_rule/version; effective_scope; weighting | n:m mit expliziten Faktoren und Ausnahmezustand |
| `TransformationSpec` | transform_id; inputs; outputs; preconditions; invariants; error_policy; verif_oracle | P00–P17; 38 vorgeschlagene Einträge im Matrixkatalog |
| `TransformationExecution` | execution_id; transform_spec_ref; run_id; input_instance_refs; output_instance_refs; parameters; event_time | 1 Spec; n tatsächliche Ausführungen; gerichteter DAG |
| `IoSNRun` | run_id; profile_ref; data_freeze_ref; study_year; variant; CY_set; model_config; execution_state | 1 Studienjahr pro Optimierungsproblem, CY-Szenarien als innere Fälle |
| `ModelInputBundle` | bundle_id; run_id; sets; parameters; network_semantics; candidate_set; provenance | 1 oder n fachliche Batches je Run/Stage |
| `ModelRunResult` | result_id; run_id; stage; solver_status; feasibility_state; raw_records | Rohresultate nicht automatisch freigegebene Bedarfe |
| `OutputDefinition` | metric_id; display_unit; dimension; aggregation_axes; formula_ref; status | Kennzahl ohne bestätigte Formel `UNDEFINED` |
| `PublishedNeed` | need_id; category; target_scope; quantity/ref; run_lineage; approval_disclaimer | Ergebnis ist **Bedarf/Opportunität**, keine Bau- oder Projektfreigabe |
| `VerificationEvidence` | evidence_id; test_id; oracle_version; execution_result; reviewer/signoff | technische Prüfung ≠ Ownerfreigabe |

**Gültige Statusgruppen (nicht mischen):** `DECLARED`/`STRUCTURALLY_VALID`/`STRUCTURAL_INVALID` (Struktur), `SOURCE_UNVERIFIED`/`SOURCE_QUALIFIED` (Quellen), `METHOD_TBD`/`METHOD_OWNER_APPROVED` (Fachsemantik), `TEST_NOT_EXECUTED`/`PASS`/`FAIL` (Test), `RELEASE_BLOCKED`/`RELEASE_AUTHORIZED` (Lauffreigabe). Eine erfolgreiche niedrigere Stufe impliziert keine höhere.

### 3.1 Identitätsregeln
- `object_definition_id` ist eine stabile semantische Klasse; `instance_id` referenziert ein konkretes Objekt in genau einem Daten-/Konfigurationszustand. Keine implizite Gleichsetzung von Quelldateinamen, RDFID, Anlagen-ID, Marktzone, IoSN-Zone und Korridor-ID.
- Namespaces sind Bestandteil jedes Identitätsschlüssels. Eine n:m-Zuordnung benötigt Regel, Priorität, Faktor, gültige Geografie und Vergleichs-/Ausnahmestatus. Eine automatische Zuordnung mit Mehrdeutigkeit ohne Freigabe ist ein Fehler.
- Netz-ID und Zonen-ID haben eine versionierte räumliche Referenz. Kandidat und physische AC/DC-Technologie sind unterschiedliche Identitäten.
- Dataset-/Model-Run- und Report-IDs sind eindeutig und per Foreign Key nachvollziehbar. Protokollierte Korrekturen sind neue Versionen, keine stille Überschreibung.

## 4. Verbindliche Projektprämissen für den **Forschungsentwurf**, keine Methodikfreigaben
| Dimension | Vertragsausprägung | Ausführungszustand |
|---|---|---|
| Studienjahre | **2035, 2040, 2050**; methodisch getrennte Runs | syntaktisch prüfbar |
| Externe Wetterfälle | **CY1, CY2, CY3, CY4, CY5** je Studienjahr; Auswahl vollständig upstream | strukturell prüfbar |
| Wetterfallgewichte | `w(CY_i,2035)=w(CY_i,2040)=w(CY_i,2050)`; Werte **TBD** | numerisch nicht produktiv laufbereit |
| Zeit | Referenz `UTC`, Intervalle `[start_utc,end_utc)`; Quelldaten-Zeitzone, DST-Konversion und Kalender explizit | UTC-Form technisch prüfbar, Kalenderentscheidung teils offen |
| Größen | `unit` und physikalische `dimension` explizit, Umrechnungen einschließlich Bezugsbasis protokolliert | Einheitenkompatibilität prüfbar |
| Pflichtdaten | fehlende/nicht eindeutige Quell-, Zuordnungs- oder Modellparameter: **Fail-Closed** | `RELEASE_BLOCKED` statt Null-/Defaultwert |
| Toolkopplung | nur fachlicher Vertrag; keine PyPSA-, GenzOE-, Antares- oder Sienna-Datenfelder als Norm | Adapter frei |
| Wetterselektion | Auswahlalgorithmus, Ranking und Repräsentativitätsprüfung außerhalb IoSN | keine Rekonstruktion |

Die alten O26-Draft-Wetterkennzeichen und die im Draft genannten drei Fälle je Zieljahr sind **nicht** als aktive ML-R03-Vorgabe übernommen. Ihre Existenz wird als methodischer Delta-/Authority-Konflikt für spätere Klärung geführt. Nach Benennung `CY1–CY5` sind auch die physischen Quellprofilreferenzen noch zuzuordnen. Ein synthetisches Beispiel mit 0,2 je CY ist **keine** Festlegung der realen Gewichte.

## 5. Zeit-, Einheiten- und Raummodell
- Zeitindex `TimeInterval(start_utc,end_utc,calendar_id,duration_seconds,source_timezone,conversion_rule_ref)`, halb-offen; alle Grenzen in ISO 8601 UTC (`Z`), monotone Intervalle, keine Überlappung je vollständigem Reihen-Key. Vollständigkeitslücken gegen geforderte Abdeckung prüfen; Sommer-/Winterzeit nur am Originalquellzeitbezug.
- Zustands-/Leistungsgrößen unterschiedlich behandeln: **MW** als Leistung über Intervall vs. **MWh** als Energie. Beispiel rein dimensional: `E[MWh] = P_mean[MW] × Δt[h]`. Zeitaggregation ist damit keine gewöhnliche Summe von Leistungswerten. Ungeklärte Messart (`instantaneous`, `interval_mean`, `interval_energy`) bleibt blockiert.
- Umrechnungen `GW↔MW` (Faktor 1000), `MWh↔GWh` (Faktor 1000) nur bei dimensionaler Kompatibilität. Wärme/H2/Strom nicht ohne modellierte Umwandlung konvertieren; `MWh_H2_LHV` und `MWh_H2_HHV` sind ohne Brennwertbasis **nicht austauschbar**.
- Flussrichtung benötigt `from`, `to`, `direction`, `sign_convention`. NTC+, NTC− und sommer-/winterbezogene Sicherheitskapazitäten dürfen nicht in einen ungerichteten Skalar kollabieren.
- `CurrencyAmount(currency,price_year,real_nominal,discount_basis,component)`; keine Preisjahres- oder WACC-Defaults. Geometrie benötigt `crs`, `geometry_version`, `length_basis`, und bei offshore ggf. geschützte Gebiete.
- Für extensive Mengen kann eine Aggregation eine deklarierte Erhaltungsprüfung fordern (`sum source = sum target + documented exceptions`); Intensitäten wie Kosten/MWh, Faktoren und Wirkungsgrade erfordern eigene Operatoren. Toleranzen und verlustbehaftete Netzreduktion bleiben ownerabhängig.

## 6. Minimaler logischer Ablauf (Pseudocode, **keine Sprachwahl**)
```text
profile := resolve_research_profile(methodology_version, historical_fallbacks_labeled)
manifest := reconcile_source_releases_and_run_freeze(profile, input_catalogue)
for y in {2035, 2040, 2050}:
    W_y := accept_upstream_selection({CY1, CY2, CY3, CY4, CY5}, weights=TBD)
    if mandatory_data_or_mapping_unresolved: block(PRODUCTION_RUN)
    aligned := transform_and_validate_utc_timeseries(manifest, y, W_y)
    reference_grid := construct_grid_with_approved_project_eligibility(manifest, y)
    zones, reduced_grid := cluster_and_reduce(reference_grid, approved_oracle=TBD)
    model_contract := assemble_tool_neutral_input(y, W_y, aligned, reduced_grid, candidates)
    raw_results := execute_expansion_stages_and_record_solver_evidence(model_contract)
    needs := derive_metrics_only_with_approved_definition(raw_results, formula_ref)
    release(needs) only if required approvals and evidence exist
```
Die Reihenfolge ist eine Konzeption. P12 gilt gesondert für 2040/2050, P14 für eine separate H2-Sensitivität, P15 nur bei bewusster Entscheidung. Eine nicht freigegebene Formel erzeugt `UNDEFINED_METRIC`, nicht einen geschätzten Wert.

## 7. Beziehung zur Ausgangsinventur und offenen Entscheidungen
Die Werte der Felder `identity_key_grain`, `unit_or_dimension_requirement`, `time_reference_requirement`, `spatial_reference_requirement`, `scenario_weather_requirement`, `upstream_dependencies`, `direct_MA01_SR_links` und `qualification_disposition` stammen aus `BUNDLE01R_B_data_qualification/qualified_input_inventory.csv` am Baseline-Commit. Das zusätzliche `expected_attributes_proposed` und `producer_step_proposed` sind neue nichtnormative Forschungsdefinitionen. Wo Produzent/Verbraucher nicht aus ursprünglichen Nachweisen belegt ist, bleibt eine Owner-/Traceability-Prüfung erforderlich.

**Offene Gating-Punkte:** MD-01 Methodology Authority; MD-02 Economics/Discount; MD-03/13 Reduktions- und Clustering-Orakel; MD-04/17 KPI und Resultatgleichwertigkeit; MD-05 Offshore-Faktor; MD-06 Speicher; MD-07 Stufenübergabe; MD-08 LF/OPF; MD-09 Kandidatenlink-Semantik; MD-10 H2; MD-11 Originaldaten/Freeze; MD-12 Kalender/Toleranzen; MD-14 Startnetz; MD-15 Solver-/Verifikation; MD-16 Hydro/DSR; MD-18/19 Wetterdatenübergabe; MD-20 Scope, MA02-CL-001 Projekteligibilität. Entscheidungsträger, Werte, Beweise und Datenversionen **TBD**. D1–D6 sind als im Auftrag genannte Projektprämissen berücksichtigt; unbereitgestellte Einzelbeschlusstexte werden nicht nachträglich erfunden.

## 8. Schnittstelle und Konformitätsstufen
Ein Adapter erhält `ModelInputBundle` und muss entweder (a) Semantik + Dimensions-/Achsen- und Id-Repräsentation nachweislich verlustfrei abbilden oder (b) explizite `UNSUPPORTED`/Transformationsabweichungen melden. Ein outputfähiger Solver ersetzt keine Datenkonformität. Konformität nur in Schichten berichten: `SCHEMA`, `REFERENTIAL`, `DIMENSIONAL`, `TRANSFORMATION`, `MATHEMATICAL`, `SOURCE_DATA`, `DOMAIN_APPROVAL`. Diese Forschungsdokumente qualifizieren ausschließlich prüfbare Entwürfe und synthetische technische Beispiele.

**Source references:** Baseline-Repository `iosn_process_matrix.csv`, `iosn_requirements_catalogue.csv`, `BUNDLE01_B_input_data/input_data_inventory.csv`, `BUNDLE01_B_input_data/source_data_requirement_traceability.csv`, `BUNDLE01R_B_data_qualification/qualified_input_inventory.csv`, `BUNDLE01R_D_independent_gate_review/bundle01r_consolidated_closure_report.md`. Keine Baseline-Datei geändert.
