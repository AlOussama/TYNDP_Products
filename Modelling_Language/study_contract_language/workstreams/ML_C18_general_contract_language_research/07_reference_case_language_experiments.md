# ML-C18 / 07 – RC01–RC10 Cross-Language Reference Experiments
**Freeze:** SLR01–42, K01–K17 research-r1. **Status:** dokumentierter semantischer Mapping-Versuch, **keine nativen Parser-/Solverläufe**. Für alle zehn Fälle ist zuerst der toolneutrale Contract formuliert; Varianten danach. GEMS @ `9c52d63b...`, mathspec @ `5f1464c...`, IoSN-C17 @ `c8bbedad...`. Existing tests under GEMS/mathspec repositories are not ML-C18-case validations.

## Gemeinsame Experimentregeln
Einheitlicher Ablauf: externe Pflicht → zwei interne Modelle → Mapping in GEMS → Mapping in mathspec → zusätzliche durch jeweilige Sprache festgelegte Mathematik → positiven/negativen Witness → Verlustkontrolle → Evidenz. Pro RC: `quality = NOT_EVALUATED` und `evidence = E1/E2 (language documentation / mapping only)` für **native Testkonformität**; semantische Hypothesen sind prüfbar, aber weder erfolgreicher GEMS- noch mathspec-Parserlauf wird behauptet. K02/K03/K05/K06/K07/K08/K09 sind in jedem RC Pflichtfragen; übrige K01–K17 werden auf einen RC angewandt, soweit relevant (K16/K17 ohne native Tests = NOT_EVALUATED). RC09 Methodikautorität nicht fingieren.

## Illustrative synthetische Sprachskizzen
**GEMS – Port und interne Equation sind nicht selbst ein externer Contract (nur Sketch; NOT_PARSED):**
```yaml
library:
  id: battery_variant_a
  version: "research-0"
  port-types:
    - id: electricity
      fields: [{id: power}]
  models:
    - id: storage
      variables:
        - id: p_charge
        - id: p_discharge
        - id: e
      ports:
        - id: grid_port
          type: electricity
      port-field-definitions:
        - port: grid_port
          field: power
          definition: p_discharge - p_charge
      # intentionally incomplete: no time balance, bounds or objective
```
Diese Skizze demonstriert die Trennung zwischen Library-Port und Model-Formulation; sie **erfüllt RC01 nicht**. Komplette Referenzimplementierungen sind durch Pflichten und Datenprofil zu ergänzen.

**mathspec – konkretisierte Mathematik statt allgemeiner Verhaltenscontract (nur Sketch; NOT_PARSED):**
```yaml
version: 0
dimensions:
  snapshot: {dtype: int, ordered: true}
parameters:
  p_max: {dims: [snapshot]}
variables:
  p: {dims: [snapshot], bounds: {lower: 0, upper: p_max}}
constraints:
  upper_limit: {dims: [snapshot], expression: "p <= p_max"}
```
Die mathematische Variablen-/Constraint-Spezifikation kennt noch keine gemeinsame physikalische Systemrolle, Port-/Vorzeichenpolitik, Energie-Ledger oder erlaubte interne Variante.

**Toolneutraler Ausschnitt – ausdrücklich nur abstrakte Semantik, keine gültige YAML-DSL:**
```text
study RC01 scope=(bus=B, time=t, delta_t=hour)
require port(grid,carrier=electricity,quantity=active_power,unit=MW,sign=inject_positive)
require terminal_energy_service(minimum_E_end)
require energy_ledger(eta_charge,eta_discharge,losses,initial_E)
permit internal_formulation(alternative_state_coordinate)
implementation_defined solver, model_framework  [disclose]
observable grid_injection -> study_results.grid_MW
verification trace_invariant + feasibility_witness + source_reference
```

## Gemeinsame RC-Fälle
### RC01 – Batteriespeicher
**Toolneutraler Vertrag/Scope:** AC-Bus B, 1h oder 0.5h, MW/MWh, Abgabe positiv, E0/Eend und Wirkungsgrad explizit, Source synthetic. **Verbindliche externe Eigenschaften:** P_grid(t), zulässige Pmin/Pmax(t), Energie-Ledger mit Lade/Entlade/Loss, Servicefähigkeit, Terminal-Energy.

**Interne Variante A:** Zwei Power-Variablen p_ch/p_dis, Zustand e_t, lineare dynamische Bilanz. **Interne Variante B:** Nettoleistung mit Mode-spezifischer Effizienz und Energietransfer-Witness; ggf. Aggregat-envelope.

**Darstellung GEMS (konzeptionell):** Zwei verschiedene `library.models` mit identischem `port-types`-Feld für P; eigene `variables`, `constraints` und `port-field-definitions`. `taxonomy` auf Port-/Observable-only begrenzen.

**Darstellung mathspec (konzeptionell):** Zwei unabhängige Specs: `dimensions: snapshot`, `relations`/`parameters`, aber je andere `variables`/`constraints`; gleiche fachliche Beobachtungsprojektion wird außerhalb formuliert.

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** GEMS-Library schreibt pro Modell interne Algebra und ggf. lineare Form vor; mathspec-Datei schreibt mathematische Variablen, Grad und Constraints vor.

**Semantische Verlustgefahr (K08/K11/K14):** Aus `power` allein folgen weder korrekte E-Bilanz noch nicht-simultane unzulässige Betriebsmodi; Terminal-/Initial-Evidence benötigt.

**Positive Gegenprobe (Soll-Accept):** E_t und SOC_t=E_t/Emax unter gleicher E(t)-Projektion und identischer Effizienz. **Negative Mutation (Soll-Reject/Block):** 2 MW über 0,5 h als 2 MWh statt 1 MWh abgerechnet.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** A/B nur bei streng gleichen Randbedingungen formal äquivalent; Aggregat nur unter überprüfter Service-Projektion strukturell zulässig.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC02 – EV-Individual versus Flotte
**Toolneutraler Vertrag/Scope:** AC-Bus, An-/Abfahrtsfenster, Ladepunkte, Mobility-service, V2G Flag. **Verbindliche externe Eigenschaften:** Aufnahme/ggf. Rückspeisung in MW, je erforderliche Abfahrtsenergie, zeitliche Verfügbarkeit, max Charger.

**Interne Variante A:** Fahrzeugindividuelle Batteriestände, binäre Anschlusszeiten. **Interne Variante B:** Aggregiertes Flexibility-envelope mit garantierter Individualservice-Projektion.

**Darstellung GEMS (konzeptionell):** Komponenteninstanzen pro EV vs fleet model, gleiches Grid-port-Feld; eigenständige Modellbibliotheken, mit optional V2G-Bindings.

**Darstellung mathspec (konzeptionell):** Dimension `ev` bei Individualspec; Flottenspec ohne `ev` oder mit Relations/partitions und anderem Variablenraum. Gemeinsamer Ergebniscontract separat.

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** GEMS/Mathspec einzelne Modelle binden Zeit-/Variablen-/Constraintrepräsentation.

**Semantische Verlustgefahr (K08/K11/K14):** Aggregate MWh reicht nicht für pünktliche individuelle Abfahrt; V2G-permission ist nicht allein durch Vorzeichen ableitbar.

**Positive Gegenprobe (Soll-Accept):** zwei verschiedene Ladestrategien decken für jedes Fahrzeug den Abfahrtsbedarf. **Negative Mutation (Soll-Reject/Block):** V2G-Export bei Profileinstellung V2G=false; ein Fahrzeug verpasst Energie-Deadline.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** Individual-Aggregat nicht allgemein äquivalent; unter belegter Flotten-Service-Menge zulässige Strukturabweichung.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC03 – Elektrolyse
**Toolneutraler Vertrag/Scope:** Elektrizitätsbus, H2-Node, LHV/HHV, Wasser- und Wärmegrenzen falls relevant. **Verbindliche externe Eigenschaften:** P_grid MW, m_H2 kg/h, ggf. Q_heat MWth, definierter Umwandlungs-/Verlustbereich.

**Interne Variante A:** Konst. spezifische Energie [kWh/kg], linearer Konverter. **Interne Variante B:** Teillast-abhängiger stückweiser Wirkungsgrad, optionale Betriebsmodi.

**Darstellung GEMS (konzeptionell):** Mehrere carrierbezogen dokumentierte Port-Felder und unterschiedliche Model Libraries; Nichtlinearität ggf. linearisiert.

**Darstellung mathspec (konzeptionell):** Parameter/Relations/Expressions, unterschiedliche linear/piecewise Formulierungen je Spec

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** GEMS verlangt dokumentiert linear-affine variable expressions; mathspec spezifiziert mathematische Funktionen der jeweiligen Spec.

**Semantische Verlustgefahr (K08/K11/K14):** Ohne explicit kg/h->MW via LHV/HHV physikalisch mehrdeutige Umwandlung.

**Positive Gegenprobe (Soll-Accept):** zwei verschiedene Prozessmodelle erfüllen denselben tolerierten Outputband. **Negative Mutation (Soll-Reject/Block):** kg/h ohne Energiekonversion direkt gegen MW getestet.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** Bei Effizienzband sind Ergebnisse bewusst nicht äquivalent; beide können konform sein.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC04 – H2-Speicher und Rückverstromung
**Toolneutraler Vertrag/Scope:** H2- und Stromnetzanbindung, Inventory-Anfang/Ende, Verlust-/Heizwertbasis. **Verbindliche externe Eigenschaften:** m_in/m_out kg/h, P_el MW, optional Q_heat MWth, Masseninventar und Verlustledger.

**Interne Variante A:** Detaillierter H2-Massenbestand, Kompressor und Fuel cell. **Interne Variante B:** Energieäquivalentes H2-Inventar plus integriertes Conversion-Envelope.

**Darstellung GEMS (konzeptionell):** Mehrport-Komposition: H2 storage + turbine/fuel-cell Library; bind-constraints für gerichtete Flüsse

**Darstellung mathspec (konzeptionell):** Relationen für H2-Node/Bus, Inventory-Dim und Umwandlungs-Spec variieren

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** Explizite Model Libraries erzwingen interne state/constraints; mathspec lässt mehrere Dateien zu, nicht freie Mathematik derselben Datei.

**Semantische Verlustgefahr (K08/K11/K14):** Unterschied zwischen Massen- und Energiebuchführung wird ohne Heizwertbasis unsichtbar.

**Positive Gegenprobe (Soll-Accept):** kg- und MWh_H2-Zustände über feste LHV konvertiert, identische Portflüsse. **Negative Mutation (Soll-Reject/Block):** elektrische Rückspeisung ohne korrespondierende H2-Abnahme oder andere Energiequelle.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** nur bei dokumentierter LHV und Verlustgleichheit äquivalent.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC05 – Physikalisches Stromnetz
**Toolneutraler Vertrag/Scope:** Fixes verbundenes Netz, linearer lossless DC-Ansatz, gleiche Topologie, baseMVA, slack und Phase-shift-Konvention. **Verbindliche externe Eigenschaften:** Businjektionen, Branchflows, KCL/KVL, Grenzen, same branch orientation.

**Interne Variante A:** Knotenwinkel und Suszeptanzmatrix, KCL + Ohm DC. **Interne Variante B:** Cycle-flow/KVL-Formulierung oder korrekt berechnete PTDF-Projektion.

**Darstellung GEMS (konzeptionell):** `pypsa_models.yml` enthält Buswinkel- und Leitungsgleichungen; alternative Cycle/PTDF braucht andere library constraints.

**Darstellung mathspec (konzeptionell):** Verschiedene `line/bus/flow`-Variablen und Constraints mit Relations und Operators; gleiches Output-Mapping.

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** Gemeinsame einzelne Library oder mathspec-File setzt Angle/Flow- oder PTDF-Variable vorab fest.

**Semantische Verlustgefahr (K08/K11/K14):** PTDF bei Topologie-/Reactance-Änderung ohne Aktualisierung nicht mehr äquivalent.

**Positive Gegenprobe (Soll-Accept):** 3-Bus-DC-Toy mit identischem Branchflow aus Angle und PTDF. **Negative Mutation (Soll-Reject/Block):** zyklischer Circulation flow verletzt KVL, obwohl KCL erfüllt.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** Nur unter expliziten Annahmen math. äquivalent; AC, Verluste und Netzschaltung sind andere Profile.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC06 – Ausbaukandidat
**Toolneutraler Vertrag/Scope:** Kandidatenleitung/Capacity, Standort, Investitionskosten, Zielhorizont, Ausbaugrenzen. **Verbindliche externe Eigenschaften:** Investierbare zusätzliche Transferkapazität am Korridor, Kosten, Grenzen, Verfügbarkeit.

**Interne Variante A:** kontinuierliche Ausbaukapazität. **Interne Variante B:** ganzzahlige Module mit disjunkter Mindestgröße, nur bei gleicher zulässiger Ausbaugranularität.

**Darstellung GEMS (konzeptionell):** Model Library mit continuous vs integer capacity; system uses alternative model ref

**Darstellung mathspec (konzeptionell):** `variables` continuous vs integer und Kapazitätsrestriktionen in separaten mathspec files

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** Solverklasse/MILP vs LP wird auf matemathspec/GEMS-model-level gebunden, nicht automatisch fachlich vorgeschrieben

**Semantische Verlustgefahr (K08/K11/K14):** kontinuierlich vs modular sind nicht äquivalent, außer Contract erlaubt Kontinuum/Approximation

**Positive Gegenprobe (Soll-Accept):** zwei intern anders dargestellte Integer-Module mit gleicher MW- und Kostenprojektion. **Negative Mutation (Soll-Reject/Block):** Kontinuierliche 0,3-Module als tatsächlich baubare Option, obwohl whole-module REQUIRED.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** Modellierungsfreiheit nur innerhalb fachlicher discreteness-Pflicht.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC07 – Mehrstufige Investition
**Toolneutraler Vertrag/Scope:** Baustufen/Studienjahre, Szenariobaum, Beobachtungszeitpunkte, Lead times. **Verbindliche externe Eigenschaften:** Verbindlich vor Informationseintritt getroffene x, nach Szenario variierbarer Dispatch; Capex und Startdatum.

**Interne Variante A:** Szenario-unabhängige Stage-1-Variable mit scenariowise Dispatch. **Interne Variante B:** Szenario-indexierte x mit Gleichheitskopplung auf gemeinsamen Informationsknoten.

**Darstellung GEMS (konzeptionell):** Stage/time/scenario in library/optimization config; zusätzliche Nichtantizipativitäts-Bindings je konkrete Library

**Darstellung mathspec (konzeptionell):** Dims stages/scenario/node und `relations`/constraints für information-set coupling; alternative Indexform in anderer Spec

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** Szenariobaum/Variablenindices im konkreten mathspec/GEMS-Modell, nicht notwendig im fachlichen Contract

**Semantische Verlustgefahr (K08/K11/K14):** Nur gleicher Erwartungs-Kostenwert beweist keine nonanticipativity

**Positive Gegenprobe (Soll-Accept):** x_s1=x_s2 solange Info identisch, danach Szenario-Dispatch unterschiedlich. **Negative Mutation (Soll-Reject/Block):** wetterabhängige Erststufeninvestitionen vor Bekanntwerden des Wetters.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** A/B mathematisch äquivalent nur bei beweisbar identischen Informationsmengen.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC08 – Gesamtkosten und Ergebnisse
**Toolneutraler Vertrag/Scope:** Kostenbasisjahr, EUR real/nominal, Zeithorizont, Discount, Szenariogewicht. **Verbindliche externe Eigenschaften:** Gesamtsystemkosten, CAPEX/OPEX, Emission, Flüsse in definierter Einheit/Aggregation.

**Interne Variante A:** Direkte Summierung LP-Komponenten. **Interne Variante B:** Unabhängige postprocessed Cost Ledger aus Lösungstraces.

**Darstellung GEMS (konzeptionell):** `objective-contributions` und extra-outputs, Catalog/Views aggregieren auf Taxonomy; KPI-Semantik zusätzlich profilieren

**Darstellung mathspec (konzeptionell):** `objective` plus expressions; separate `typeset`-Dokumentation der Rechenformel

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** GEMS/mathspec objective intern ggf. andere addend-Zerlegung; gemeinsame KPI nicht als Solverziel identisch voraussetzen

**Semantische Verlustgefahr (K08/K11/K14):** Eine Solver-Objective schließt sunk/fixed cost oder transfer payments ggf. anders ein

**Positive Gegenprobe (Soll-Accept):** identische CAPEX/OPEX-Klassifikation und weighted time aggregation. **Negative Mutation (Soll-Reject/Block):** MWh × EUR/MWh ohne Zeitgewicht oder doppelte CAPEX-Anrechnung.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** KPI-Funktionsäquivalenz auf gemeinsamen Kostenkomponenten statt identischen nativen Zielen.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC09 – Kosten-Nutzen-Analyse
**Toolneutraler Vertrag/Scope:** Methodikautorität N2E nicht identifiziert; synthetischer baseline/project counterfactual, Rechnung ohne normative Kennzahlendefaults. **Verbindliche externe Eigenschaften:** Einheitlicher Ohne-/Mit-Projektfall, festgelegte Indikatoren, Bewertungshorizont und Diskontkonvention.

**Interne Variante A:** Direkte End-to-End-CBA-Modellkette. **Interne Variante B:** Getrennte markt-/netzseitige Simulation plus unabhängige CBA Postprocessing-Pipeline.

**Darstellung GEMS (konzeptionell):** Systemmodell/Simulation möglich, N2E-CBA-Methodik-/Referenzvertrag als externes Profil

**Darstellung mathspec (konzeptionell):** Konkrete mathematische Sub-Specs möglich, höherer Counterfactual-/Governance-Contract extern

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** Wenn Studien-CBA mit nativer Objective gleichgesetzt wird, ungewollte Festlegung der Berechnungsarchitektur

**Semantische Verlustgefahr (K08/K11/K14):** Benchmark-Basisfall, Nutzenzeitraum oder Währung ändern Vergleichssemantik

**Positive Gegenprobe (Soll-Accept):** zwei Berechnungspipelines liefern gleich definierte Differenz mit auditierbaren Ledgern. **Negative Mutation (Soll-Reject/Block):** Mit-/Ohne-Projektfall nutzen verschiedene exogene Nachfrageszenarien ohne deklarierte Abweichung.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** Verschiedene Berechnungsansätze konform, wenn Indikatordefinition/Counterfactual gleich; konkrete N2E Regel ist OWNER_TBD.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.


### RC10 – Multi-Model Study
**Toolneutraler Vertrag/Scope:** UC1/2/3, identische exogene Szenarioidentitäten, independent provenance, ComparisonContract. **Verbindliche externe Eigenschaften:** Vereinbarte Outputs, Einheit, Aggregation und Decision Ranking; R1-R4, Unsicherheits- und Biasprotokoll.

**Interne Variante A:** GEMS-basiertes Modell für eine Implementierung + anderes GEMS-Submodell. **Interne Variante B:** mathspec-basiertes Modell oder PyPSA/Sienna mit unabhängiger mathematischer Struktur.

**Darstellung GEMS (konzeptionell):** Eigenständige GEMS Modellbibliotheken und Views können Observables liefern; robustheitsbezogene Vertragssemantik extern

**Darstellung mathspec (konzeptionell):** Verschiedene Specs/Engine-Programme mit protokollierter Abbildungsfunktion; R3/R4-Verträge extern

**Sprachlich induzierte zusätzliche Festlegungen (K03/K05):** Eine *gemeinsame* detaillierte GEMS Library/mathspec Spec würde Modellstruktur auf R1/R2 reduzieren

**Semantische Verlustgefahr (K08/K11/K14):** identische Ergebnisnamen ohne identische Aggregation sind nicht vergleichbar; gemeinsame Codebasis mindert Unabhängigkeit

**Positive Gegenprobe (Soll-Accept):** zwei zulässige Nichtäquivalenzen liefern unterschiedliche Kosten, aber gleiche Maßnahme-Rangfolge. **Negative Mutation (Soll-Reject/Block):** model B nutzt zusätzliche Lastreduktion ohne Deklaration und Unterschied wird als Robustheitsvarianz gezählt.

**Äquivalenz-/Nichtäquivalenzregel (K06/K07):** Konformität getrennt von Dispersion, Rang-/Entscheidungsrobustheit, Solvermehrfachoptima.

**Evaluationsstatus:** GEMS `CONCEPTUAL_MAPPING/E2` für die belegten Sprachmechanismen; mathspec `CONCEPTUAL_MAPPING/E2`; `NATIVE_PARSED=NO`, `EQUIVALENCE_PROVED=NO`, `ROBUSTNESS_MEASURED=NO`; pro RC `K02,K03,K05,K06,K07,K08,K09` offen für einen gemeinsamen ausgeführten Test.
## Cross-Case-Readiness-Matrix
| RC | Pflichtprofil / Fokus | GEMS native | mathspec native | Positive + negative Mutation dokumentiert | Nachweistiefe |
|---|---|---|---|---|---|
| RC01 | Batteriespeicher | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC02 | EV-Individual versus Flotte | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC03 | Elektrolyse | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC04 | H2-Speicher und Rückverstromung | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC05 | Physikalisches Stromnetz | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC06 | Ausbaukandidat | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC07 | Mehrstufige Investition | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC08 | Gesamtkosten und Ergebnisse | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC09 | Kosten-Nutzen-Analyse | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |
| RC10 | Multi-Model Study | NOT_EXECUTED | NOT_EXECUTED | YES (design only) | E1/E2 documentation; E0 RC-native |

## Wissenschaftliche Bewertung nach K01–K17
- K01–K02: Die zehn Contracts decken Study-/Component-/Network-/CBA-Fälle ab; sprachliche Konzeption plausibel, native Vollabdeckung **nicht bewiesen**.
- K03–K06: Bei allen Paaren ist zu prüfen, ob dieselbe äußere Pflicht alternativ erfüllbar ist. Darstellbarkeit zweier verschiedener Libraries/Specs allein beweist keine Verhaltensgleichheit.
- K07: In RC10 Vergleichs- und Robustheitsprotokoll separat, nicht Solver-Ergebnisgleichheit.
- K08–K09: Negativfälle enthalten Unit, physical constraints, nonanticipativity, comparison-base und evidence gaps. Parser/Validator-Aufdeckung bislang `NOT_EXECUTED`.
- K10–K11: Elektrizität/Storage/EV/H2/Netz/Investition/Kosten/Pre-Postprocessing vertreten; reale Data Contract- und Prozesskonformität offen.
- K12–K15: Syntaxgröße, Modelliererinterpretation, verlustfreies Exportmapping und Governance noch nicht experimentell gemessen.
- K16–K17: Vorhandene Tooling-/Test-Evidenz ist in 03/04 referenziert; **keine** dieser RC-Fälle von unabhängigen Autoren oder nativen Parsern durchlaufen.

## Für reproduzierbare Folgeexperimente
Pro RC sollen zwei vollständige Spec-Dateien je Sprache inkl. verknüpftem externen Contract, synthetischem Datensatz, erwarteten Parserausgaben, positivem und negativem Witness, Ergebnisprojektion und Assertion-Log erstellt werden. Ein nativer Parserlauf erfordert tatsächlichen GEMS-Interpreter/GemsPy bzw. mathspec-Installationen. Die Ausgangsdaten hier erlauben *Forschungsplanung*, keine Toolzertifizierung. Der separat erstellte numerische Micro-Check (siehe `15_research_validation_report.md`) ist unabhängig vom nativen Parsing zu behandeln.

## Quellen
- GEMS: https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/library.md
- mathspec: https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/file.md
- ML-C17: https://github.com/AlOussama/TYNDP_Products/blob/c8bbedad390d0ba00604a0f499e79e9cff087138/Modelling_Language/iosn_formal_specification/workstreams/ML_C17_language_maturity_assessment/reference_contract_examples.md
