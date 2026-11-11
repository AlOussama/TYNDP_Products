# ML-R02 — Evidence and Source Ledger
**Abruf-/Bewertungsstand 2026-11-11.** D = dokumentiert, nicht automatisch unabhängig verifiziert. Die in den beiden Prototypen erreichte Validierung ist gesondert als S = synthetisch ausgeführt ausgewiesen. Kein Normativitätsanspruch aus GitHub-/Workshop-Selbstauskünften.

| Identifier | Quelle und Version/Snapshot | belegte Teilfähigkeit / Einschränkung | Eignung |
|---|---|---|---|
| O26 | [ENTSO-E IoSN Consultation, 25 Feb 2026](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf) | 65 S., §§3.1,3.7,3.8,4.5; ***Consultation, nicht adopted***; drei Wetterfälle | primäre methodische Ausgangsquelle, Autorität unbestätigt |
| P26 | [Consultation hub](https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/) | konsultiert 26 Feb–3 Apr 2026; Abschluss ≠ Annahme | Governance-Kontext |
| B01R | [Base commit](https://github.com/AlOussama/TYNDP_Products/commit/5c13d4d63f18d30c308997cd7a01f2977fcc6b7b) | MA01 48 SR, P00–P17 und G1 blocked | bindende Forschungsbaseline (nicht freigegeben) |
| SysMLv2 | [OMG formal v2.0](https://www.omg.org/spec/SysML/2.0) | Requirements, Verhalten, API, KerML; IoSN-Profile fehlen | MBSE |
| ReqIF | [OMG v1.2](https://www.omg.org/spec/ReqIF/1.2) | Req-Speicher/Interchange, XSD | RM |
| GEMS | [AntaresSimulatorTeam/GEMS](https://github.com/AntaresSimulatorTeam/GEMS), [Guide](https://gems-energy.readthedocs.io/en/latest/user-guide/introduction/) | graphbasierte und algebraische Optimierung; eigenständige Methodikprüfung erforderlich | Math/energy |
| CESM | [CommonEnergySystemModel](https://github.com/G-PST/CommonEnergySystemModel), [G-PST Schema Sheet](https://github.com/G-PST/data-schema-exercise/blob/main/data_schemas/common_energy_system_model.yaml) | LinkML-basierte Strukturen, laut Sheet keine AC/DC-Power-flow- und keine implementierte Stochastik | Data |
| INES | [ines-spec](https://github.com/ines-tools/ines-spec) | Austauschschema, stochastic_forecast_weights, solve_pattern | Data |
| Sienna | [SiennaSchemas](https://github.com/NREL-Sienna/SiennaSchemas), [G-PST Sheet](https://github.com/G-PST/data-schema-exercise/blob/main/data_schemas/sienna-griddb_data_model.yaml) | JSON-Schema/OpenAPI Datenmodell; pre-release Selbsteinordnung | Data |
| mathspec | [mathspec docs](https://mathspec.readthedocs.io/en/latest/), [GitHub](https://github.com/energy-models/mathspec) | dimensionsvalidiertes mathematisches YAML, ohne Solver | Math |
| JSON Schema | [Draft 2020-12](https://json-schema.org/draft/2020-12) | strukturelle Datenvalidierung, keine native LP-Äquivalenz | Structural |
| LinkML | [LinkML validation](https://linkml.io/linkml/data/validating-data.html) | schema-/RDF-generierte Prüfpfade | Semantics |
| SHACL | [W3C 2017 Recommendation](https://www.w3.org/TR/shacl/) | Validierung von RDF-Daten gegen Shapes | Graph |
| BPMN | [OMG](https://www.omg.org/spec/BPMN/2.0.2) | Prozesskontrolle, keine LP-Constraintsemantik | Process |
| Pyomo | [Docs](https://pyomo.readthedocs.io/) | solverunabhängige algebraische Modellierung im Python-Runtime | Experiment |
| Prototype A/B | Unter `prototype_A`/`prototype_B` in diesem Workstream | 14/14 **erwartete synthetische Klassifikationen je Ansatz**; keine Normkonformität | S / toy only |

**Quellhierarchie:** aktuell bestätigte Methodikfassung zuerst; ältere Fassungen nur bei nachgewiesener Ergänzungsrelevanz und explizitem Versionsvorbehalt. Eine spätere offiziell genehmigte Quelle kann die O26-Forschungsbasis ändern, ohne die aktuelle Studie rückwirkend normativ zu legitimieren. Ein G-PST self-reported data sheet ist keine unabhängige Standardprüfung.
