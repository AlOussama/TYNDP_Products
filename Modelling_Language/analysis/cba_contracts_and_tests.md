# CBA Interoperability Contracts und Akzeptanztests — Pilot-Spezifikation

**Normativer Status:** vorgeschlagene *Review*-Anforderungen, **kein veröffentlichter ENTSO-E-Standard** und **kein implementiertes Validierungssystem**. Quellen [S01,S02,S05,S06,S08,S12](../sources/bibliography.md). Die zuständigen Prozess-/Methodenowner müssen Normscope, KPI-Formeln und Toleranzen vor Piloteinsatz freigeben.

## 1. Versionierte Artefakte und Zuordnung

Fachlich unterschiedliche Artefakte haben unterschiedliche IDs:

- `planning_contract_id`: CBA-Frage, Normbasis, R/P-Gegenfälle, projektbezogene Grenzen.
- `scenario_dataset_id`: Szenario, Zieljahr, Klima-/Zeitreihe und deren *inhaltlicher Hash*, Gewichtungs- und Mappingversion.
- `model_id`: Topologie/Komponenten/Datenausprägung eines Tools.
- `method_profile_id`: mathematische Annahmen und verpflichtende Defaults einschließlich Zielfunktion, Sektorkopplung, Verluste, Speicherterminal, Netzmodell, Simulationstechnik.
- `engine_id`: Tool, Interpreter, Solver, Version, ggf. Generatorcode-Hash.
- `transformation_id`: Quell-/Zielschema, Mapping, Erhaltungsbedingungen, Verlustfreigaben.
- `run_id`/`pair_id`: konkrete M1/M2-Rechnung für **ohne P** / **mit P** und gepaarte Deltaauswertung.
- `kpi_definition_id`: formale Berechnungs- und Aggregationslogik, Einheiten, Referenzsystem, Double-counting-Policy.
- `decision_rule_id`: vorab definierte Bewertungs-/Ranking-/Robustheitsschwelle.

Eine echte gemeinsame *Methodenidentität* kann nicht allein aus der Komponentenliste rekonstruiert werden.

## 2. Minimaler Contract, illustrative YAML-Struktur

**Nur Illustrationsschema.** IDs/Hashes sind Platzhalter und **keine TYNDP-Projekt-/Originaldaten**.

```yaml
contract_id: "CBA-PILOT-INTERCONNECTOR-v0.1"
status: "proposed-not-authoritative"
normative_basis:
  guideline: "ENTSO-E-4th-CBA-2024"
  implementation_guideline: "VERIFY_FINAL_2026_VERSION"
question: "Impact of project P relative to approved reference R"
assessment:
  boundaries: ["region_A", "region_B", "other_in_scope"]
  reference_case_id: "R-BASE"
  project_case_id: "P-INTERCONNECTOR"
  project_definition_hash: "sha256:REPLACE_WITH_REAL_DIGEST"
  currency_base_year: "SET_BY_METHOD_OWNER"
scenarios:
  - scenario_id: "S-YEAR-WEATHER-A"
    study_year: "SET_STUDY_YEAR"
    input_hash: "sha256:REPLACE_WITH_REAL_DIGEST"
    time_resolution: "PT1H"
    timezone: "UTC"
    timestep_hours: 1.0
    weather_weight: "SET_AND_VALIDATE"
    probability_role: "separate_from_weather_weight"
model_roles:
  M1:
    role: "independent_market_model"
    model_id: "M1-MODEL-VERSION"
    method_profile_id: "METHOD-A"
  M2:
    role: "choose_one:conformance|independent_method|downstream"
    model_id: "M2-MODEL-VERSION"
    method_profile_id: "METHOD-B_OR_IDENTICAL_METHOD-A"
methods:
  require_explicit_storage_terminal_condition: true
  require_explicit_network_approximation: true
  require_explicit_losses_and_defaults: true
  require_solver_capability_declaration: true
kpis:
  B1:
    formula_id: "APPROVED_GLOBAL_SEW_OR_DERIVED_COST_PROXY"
    calculation: "with_project_minus_reference"
    unit: "EUR/year"
    aggregation_weights: "APPROVED_WEATHER_WEIGHTS"
  B6:
    formula_id: "APPROVED_MC_EENS_AVOIDED"
    separate_monte_carlo_sampling: true
    value_of_lost_load: "SET_BY_METHOD_OWNER"
    unit: "MWh/year"
controls:
  reject_undeclared_loss: true
  prohibit_cross_model_reference_project_mixing: true
  require_independent_validation_of_data_and_kpi: true
  pre_register_method_variations: true
  approve_decision_thresholds_before_runs: true
```

**Wichtig:** Für B6 ist häufig eine andere Szenario-/MC-Stichprobenstruktur erforderlich als für B1. Diese müssen *nebeneinander* in getrennten Method-Contracts liegen. Eine einheitliche `weather_weight` darf nicht stillschweigend als MC-Wahrscheinlichkeit gelten.

## 3. Konsolidierter Requirements-Katalog speziell für CBA-Interoperation

Die folgenden IDs **CBA-R01–R15** sind für einen Pilot operationalisiert und ersetzen **nicht** ohne Stakeholder-Review die vollständigen R01–R14/K01–K12 des Hauptauftrags.

| ID | MUSS/SOLL und Akzeptanzkriterium | Test / Owner / Priorität |
|---|---|---|
| **CBA-R01** | **MUSS** referenzierte Komponenten-/Port-/Commodity-/Netz-IDs und Bilanzgrenzen besitzen; alle Referenzen existieren | Cross-ref/Balance-Lint / Data Steward / P0 |
| **CBA-R02** | **MUSS** physikalische und monetäre Einheiten, Vorzeichen, Kalender, Dauer und Währungsvintage definieren | MW↔GW, EUR/MWh, leap/DST-Vektoren / Data Steward / P0 |
| **CBA-R03** | **MUSS** Szenario-ID, Wetterjahr-ID, Input-Hash, Study-Year, Exogenität, Zeit-/Raumauflösung und Gewichtssemantik binden | identische Inputs trotz anders benannter Dateien; positive Gewichte; Summe/Normierung / Scenario Owner / P0 |
| **CBA-R04** | **MUSS** projektunabhängige Referenz R und nur den zulässigen Projekt-Delta P identifizieren; Abhängigkeiten anderer Projekte explizit | Diff R→P, Hash-/Graphvergleich / CBA Owner / P0 |
| **CBA-R05** | **MUSS** vollständige Method-ID inkl. Defaults, Zielfunktionsklasse, Speicherterminal, Netz/Verluste/UC, stochastische Annahmen erfassen | negative Cases für leere Defaults / Method Owner / P0 |
| **CBA-R06** | **MUSS** Tool-, Modellgenerator-, Solverversion, Konverterschritte und Fähigkeitseinschränkungen dokumentieren | Run manifest und signed capability list / Tool Owner / P0 |
| **CBA-R07** | **MUSS** transformationsbedingt verlorene Funktionen als semantisch/nichtsemantisch/approximiert/abgelehnt klassifizieren; stille Verluste blockieren | PyPSA Multiport/Gewicht/FixSOC Fälle / Adapter Owner / P0 |
| **CBA-R08** | **MUSS** bei beantragter 1:1-Übertragung Struktur/Algebra/Ziel/Nebenbedingungen/Indizes/Gewichte nachweisen | Roundtrip+symbolisches Diff+LP-Microbenchmark / Compiler Owner / P0 |
| **CBA-R09** | **MUSS** M2-Rolle deklarieren: Interpreter, unabhängiges Modell, Downstream oder nur Solver | falsche Unabhängigkeitsbehauptung abweisen / Validation Owner / P0 |
| **CBA-R10** | **MUSS** B1-KPI inkl. globalem SEW bzw. begründeter Cost-Proxy-Gültigkeit, Sektor-/CO₂-Doppelzählung und Aggregation versionieren | unabhängige KPI-Rechnung / CBA Owner / P0 |
| **CBA-R11** | **MUSS** B6-EENS/LOLE/MC/Outage/Climate/VOLL-Contract getrennt von B1 führen | MC-Input-Kontrolle und EENS-Gegenfall / Adequacy Owner / P0 |
| **CBA-R12** | **MUSS** nur paarweise `(R,P)` je Tool und Szenario werten; keinerlei `(M1 R,M2 P)` | automated pairing gate / CBA Owner / P0 |
| **CBA-R13** | **MUSS** Raum-/Zeitaggregation und Netz-Mapping mit Erhaltungs- und referenzierten Näherungsregeln dokumentieren | Bilanz, PTDF/AC-Profile, Jahresenergie / Network Owner / P0 |
| **CBA-R14** | **SOLL** methodisch unabhängige Varianten und Zukunftsunsicherheiten in einem vorab genehmigten Robustheitsexperiment auswerten; Schwellen vorab freigeben | Entscheidungsvorzeichen/-rang, Regret, CI / Governance / P1 |
| **CBA-R15** | **MUSS** Defect-Quarantäne, Abhängigkeitstracking, Versionswechsel, Review-Audit und Freigabe der Normversion unterstützen | Fehler-Injection und automatisches Invalidate / Governance / P0 |

**MUSS:** zwingend für einen gültigen Pilotreport, unabhängig von der erst später entschiedenen A+/B+-Architektur. **SOLL:** relevant für belastbare Entscheidungsrobustheit, Pilot-Pflicht wenn diese behauptet wird. „Owner“ bezeichnet Rollen, nicht existierende zugewiesene Mitarbeiter.

## 4. Capability und Loss Report — vereinheitlichte Zustände

```yaml
transformation:
  source: "M1/native-model@pinned-version"
  target: "M2/native-model@pinned-version"
  converter: "converter@pinned-version"
  status: "REJECTED"
  mathematical_equivalence_claim: false
  checks:
    - feature: "link.bus2"
      classification: "UNSUPPORTED_SEMANTIC"
      action: "FAIL"
    - feature: "unit_metadata"
      classification: "NON_SEMANTIC"
      action: "DECLARE_LOSS"
  tested_with_real_solver: false
  reviewer_approval: null
```

| Klasse | Konvention | Annahme |
|---|---|---|
| **EXACT_VERIFIED** | verlustfreie Struktur+Mathematik nach konkretem Test | nur getestete Modellklasse/Version gültig |
| **NON_SEMANTIC_DECLARED** | reine Visualisierung/Metadaten ohne Wirkpfad zur Fragestellung | als Begründung im Profil festhalten |
| **BOUNDED_APPROXIMATION_APPROVED** | methodische Näherung explizit genehmigt und quantitativ getestet | **nicht** 1:1; nur für Interoperation und Robustheitsmodus |
| **UNSUPPORTED_SEMANTIC** | Optimierungs-/Physik-/KPI-Funktion fehlt | **REJECTED**, niemals silent drop |
| **UNKNOWN** | Converterabdeckung/Implementierung unklar | **REJECTED** bis geklärt |
| **FAILED_CONFORMANCE** | nominell gleiches LP aber Zielfunktion/Constraints/Residuen verschieden | **REJECTED**, unabhängiger Defectprozess |

## 5. Abnahme-/Testmatrix für den CBA-Piloten (noch nicht ausgeführt)

| Test | Input | Expected Pass/Fail | Bewertet | Kritisches Finding |
|---|---|---|---|---|
| T01-SCHEMA | fehlerhafte Port-ID, Commodity, Unit | **Fail** vor Modellstart | Struktur/Semantik | F08 |
| T02-TIME | DST, 8760/8784, Dauer vs. Szenariogewicht | **Fail** bei inkonsistenten Gewichten | zeitliche Referenz | F03 |
| T03-PAIR | `M1:R` + `M2:P` | **Fail** | gepaarte CBA | F03 |
| T04-STORAGE | EndSOC zyklisch vs. frei | **Fail** im 1:1-Profil; deklarierbar in Method-Diversity | Methodenidentität | F10 |
| T05-LINK | PyPSA Multi-Port-Link → 2-Port-Konverter | **Fail** falls nicht vollständig erhalten | semantischer Verlust | F02 |
| T06-WEIGHTS | PyPSA Snapshotgewicht ≠1 im Konverter | **Fail**, kein stilles Gewicht=1 | 1:1-Daten+Mathematik | F02 |
| T07-LINE | Transport → DC/PTDF als „exact“ | **Fail** als 1:1, ggf. methodisches Profil | Netzphysik | F10 |
| T08-ROUNDTRIP | A→Normalform→A auf unterstützter Modellklasse | **Pass** nur mit Algebra-Diff und Daten-Diff | Conformance | F02 |
| T09-B1 | gleicher Name „SEW“, aber andere Wohlfahrts-/CO₂-Abgrenzung | **Fail** vor KPI-Vergleich | KPI-Semantik | F03 |
| T10-B6 | nur repräsentative B1-Wetterjahre als B6-MC deklariert | **Fail** | adequate sampling | F04 |
| T11-ERROR | bewusst falsch skaliertes MW/GW in gemeinsamem Input | **Fail** unabhängig von M2-Lösungsgleichheit | Common-mode | F05 |
| T12-COMPARISON | gleiches genehmigtes S, M1/M2 jeweils R/P; andere Methoden | **Pass** als *vergleichbar*, nicht als 1:1 | Robustheitsfähigkeit | F01,F06 |
| T13-DOWNSTREAM | zonale Marktbilanz→nodales Netz mit Mapping | **Pass** nur bei geprüften Summen/Netzprofilen | Prozessinteroperation | F06 |
| T14-DECISION | M1/M2 ändern Nettovorteil-Vorzeichen | **Flag**, nicht automatisch „Modellfehler“ | Entscheidungsrobustheit | F07 |
| T15-DEFECT | absichtliches fehlerhaftes Contract-Update | abhängige Runs/KPIs auf **QUARANTINED** | Provenienz/Release | F05,F11 |

**Wichtig:** Dies sind **spezifizierte**, keine ausgeführten Tests. Es liegen keine unabhängigen realen PyPSA/Antares/GemsPy/PLEXOS-Benchmark-Ergebnisse in diesem Review vor.

## 6. Gate-Reihenfolge und Freigabe

`G0` regulatorische Quelle/finale Methodversion bestätigt → `G1` Contract und R/P-Definition freigegeben → `G2` Szenarien-/KPI-Semantik konsistent → `G3` Adapter-Capability/Loss geprüft → `G4` einzeln M1/M2 reproduzierbar → `G5` Pairing und Conformance/Robustness-Modus geklärt → `G6` Fehler-Injection/B1/B6-Negativtests → `G7` unabhängige KPI-Differenzprüfung → `G8` Vorzeichen-/Regret-Auswertung → `G9` Audit und Entscheidungsfreigabe.

Stop bei G0–G7-Fail. Ohne G8 darf keine **Robustheit** der Entscheidung behauptet werden. Die Verbindlichkeit von Toleranzen und Schwellen liegt beim jeweiligen CBA-Methoden-Owner.
