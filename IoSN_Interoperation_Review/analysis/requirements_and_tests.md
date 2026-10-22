# IoSN Interoperation — testbare Anforderungen, Contracts und Prüffälle

**Status:** vorgeschlagene IoSN-spezifische Requirements (nicht offiziell von ENTSO-E verabschiedet); Konsultationsmethodik 25.02.2026 [S01]. **Keine Tests ausgeführt**, keine eigens erzeugte produktive Implementierung. Vorrang hat die Durchsetzbarkeit beim M1/M2-Transfer.

## 1. Akzeptanz- und Verlustklassen

- `EXACT_VERIFIED`: mathematisches Mapping der **konkret angegebenen Modellklasse** für dieselben Daten/Constraints/Ziel nach getestetem unabhängigen Generator; inklusive Solver-Residuals.
- `SEMANTICALLY_EQUIVALENT`: nach begründetem mathematisch/physikalischem Nachweis äquivalente Darstellung trotz anderer Form; alternativer LP-Optima **können** gleichwertig sein.
- `DECLARED_NON_SEMANTIC_LOSS`: Entfall bloßer Label-/Darstellungsmetadaten ohne fachliche Auswirkung (Begründung nötig).
- `APPROVED_BOUNDED_APPROXIMATION`: quantifizierte, freigegebene **nicht** 1:1 Netz-/Zeit-/Methodenreduktion, einschließlich Gütegrenzen und Downstream-Auswirkung.
- `UNSUPPORTED_SEMANTIC`: z. B. PST, H₂-Lastkopplung, Storage-Gleichung, Stage-ID oder `pi_s` kann nicht ausgedrückt werden → **REJECT**.
- `UNKNOWN`: ungeprüfte Funktion/Version → **REJECT** im Konformitätsmodus, ausdrücklich als offene Grenze.
- `FAILED_CONFORMANCE`: Zielfunktion/Constraints oder erwartete numerische Invarianten weichen bei nominell gleicher Algebra ab → **QUARANTINE**.

**Wichtig:** Netzreduktion kann legitime `APPROVED_BOUNDED_APPROXIMATION` sein; sie ist nicht automatisch ein Fehler, darf aber nicht als exakter Tool-zu-Tool-Roundtrip etikettiert werden.

## 2. Prüfkatalog — Owner, Akzeptanz und Test

Pflicht/MUSS kennzeichnet vorgeschlagenes **Pilot-Abnahme-Gate**, keine verbindliche ENTSO-E-Norm. Schwellen für RMSE, Contingency-Compliance, ranking stability, Regret etc. müssen vor Durchführung vom fachlich zuständigen Owner gesetzt werden.

| ID | MUSS/SOLL (prüfbar) | Akzeptanzkriterium / Negativtest | Owner, Priorität |
|---|---|---|---|
| **IO-R01** | **MUSS** eine versionierte Planungs-/Gültigkeitsgrundlage | `norm_document_id`, Fassung, Draft/Final, `study_year`; ohne Version kein „official“-Claim | IoSN Method Owner, P0 |
| **IO-R02** | **MUSS** alle Inputblobs/PECD/PEMMDB/Hydro/H₂/Startnetz verlinken und hashen | exakter Datendigest, Gerät/Region/Asset-Referenz validiert | Data Steward, P0 |
| **IO-R03** | **MUSS** einheitliche Einheiten, Vorzeichen, Zeitdauern, Zeitzone/Kalender und `pu`-Bases | Einspeisungs-/Fluss-/Energie-/CAPEX-Unit-Tests; falsche MW/GW fail | Data Steward, P0 |
| **IO-R04** | **MUSS** Klimajahresauswahl vollständig definieren: Kandidatenensemble, Feature/Normalisierung, Seed/Selector/Representative, `pi_s` | 30→3-Review; genau 3 distinct; `sum pi≈1` und Zeitreihenidentität | Climate Methods Owner, P0 |
| **IO-R05** | **MUSS** synchronen Klimazeitverlauf aller betroffenen Energiegrößen und Originalraster erhalten | Cross-region/technologies timestamp alignment; kein mis-joined Jahr | Scenario Owner, P0 |
| **IO-R06** | **MUSS** alle Netz- und Zonengraphen mit stabilen IDs, Ports, Transformatoren, PST/HVDC referenzieren | jedes Asset und Bus/Port konsistent, Island/Slack definiert | Network Owner, P0 |
| **IO-R07** | **MUSS** `P,Gamma,busmap`, Orientierungen und Bilanzrelation freigeben | `A_z Gamma = P A_d`; `A_d f_d=p_d → A_z Gamma f_d=P p_d` | Network Reduction Owner, P0 |
| **IO-R08** | **MUSS** Netzreduktions-Güte **jenseits** Bilanz prüfen | vorab akzeptierte Flow/RMSE, Peak, critical-edge recall, impedance/flow correction, seasonal direction metrics | Network Owner, P0 |
| **IO-R09** | **MUSS** N-1-Contingency-Set, LODF-Bezug und Islanding explizit abbilden | kein stiller Ausschluss von islanding; Pass/Fail für N-1 Sicherheitsset | Security Owner, P0 |
| **IO-R10** | **MUSS** vollständiges zonales Markt-/Asset-Mapping inkl. PECD-SRC und Bedarfsarten | `sum` MW, MWh/Kapazität, technologische Energieprofile, flexible vs fixe Last | Market Data Owner, P0 |
| **IO-R11** | **MUSS** H₂ exogen/operativ/frozen und Elektrolyse-Port-/Wirkungsgradprofile fixieren | H₂→Electricity energy/Port checks; falsch „endogenous H₂ network“ abweisen | Multi-Energy Owner, P0 |
| **IO-R12** | **MUSS** alle real/konzeptionell/offshore/storage Kandidaten mit bounds/stage/economics übergeben | Candidate-Registry und Stage-1→2-Snapshot konsistent, H2-/Offshore-/Storage-Scope je Zieljahr | Investment Owner, P0 |
| **IO-R13** | **MUSS** dieselbe Ausbauentscheidung über alle ausgewählten Wetterszenarien belegen, wenn Conformance verlangt | eine `x` oder äquivalente `x_s = x_{s'}`-Constraints; absichtliches `x_s`-Fehlen fail | Optimisation Owner, P0 |
| **IO-R14** | **MUSS** Operationskosten/ENS/VOLL, CAPEX/FOM, `pi_s`, Discounting/Stage festhalten | Zielfunktionskomponenten + Handelskriterien + all bounds diffbar; reale Inputdaten nicht „estimatorisch“ füllen | Investment Owner, P0 |
| **IO-R15** | **MUSS** LF/OPF-/Internal Constraint-Profile und PST-/HVDC-Semantik deklarieren | fehlende Limits/Phasenverschiebung führt Reject, abweichende LF-/OPF-Methode als `NON_COMPARABLE_1to1` | Physical Model Owner, P0 |
| **IO-R16** | **MUSS** Engine, Model Generator, Solver, Seeds, Optimizerstatus, Version und Capability-Report sichern | vollständiger geprüfter Run-Manifest; kein silent drop/versionsloser Report | Tool Owner, P0 |
| **IO-R17** | **MUSS** Conformance-, Interoperation- und Robustheitsmode **unverwechselbar** kennzeichnen | keine Robustheitsbehauptung aus zwei Solvern; M2-Rolle explizit | Validation Board, P0 |
| **IO-R18** | **MUSS** Portfolio-/Engpass/Kosten-KPIs/Mapping und räumliche Aggregation normieren | Korridor-/Region-ID konsistent, objective/cost component nachvollziehbar | Results Owner, P0 |
| **IO-R19** | **SOLL** genehmigte Sensitivitäten inkl. unabhängiger Holdout-Klimajahre, Netzmodelle und Variationen bewerten | Out-of-sample und Cross-Regret mit freigegebenen Schwellen | Robustness Board, P1; P0 bei Robustheitsclaim |
| **IO-R20** | **MUSS** Fehlerprovenienz/Run-Abhängigkeiten und unveränderliche Release-Manifeste sichern | Defect-Injection invalidiert alle abhängigen Runs; Audit Trail vorhanden | Governance, P0 |

## 3. Beispiel eines IoSN-Study-Contracts (illustrativ, kein offizielles YAML-Schema)

```yaml
contract_id: "IOSN-ARCH-TEST-2026-v0.1"
contract_status: "proposed-not-authoritative"
methodology:
  authority: "ENTSO-E"
  document: "TYNDP_2026_IoSN_2026-02-25_PUBLIC_CONSULTATION"
  final_version_verified: false
study:
  target_year: 2040
  question: "identify robust cross-border enhancement and storage needs"
datasets:
  pe_cd_version: "PIN_EXACT_VERSION_AND_HASH"
  pemmdb_version: "PIN_EXACT_VERSION_AND_HASH"
  hydro_profile_hash: "sha256:REPLACE"
  h2_network_reference_hash: "sha256:REPLACE"
  detailed_network_hash: "sha256:REPLACE"
weather:
  selector_method_id: "PCA_KMEANS_CONSULTATION_PROFILE"
  candidate_ensemble_hash: "sha256:REPLACE"
  representative_years:
    - {id: "WS065", weight: 0.20, timeseries_hash: "sha256:REPLACE"}
    - {id: "WS071", weight: 0.40, timeseries_hash: "sha256:REPLACE"}
    - {id: "WS077", weight: 0.40, timeseries_hash: "sha256:REPLACE"}
  weights_role: "scenario_probabilities"
  common_investment_decision_across_weather: true
spatial:
  detailed_network_id: "FULL_GRID_V1"
  busmap_hash: "sha256:REPLACE"
  reduction_method_id: "DECLARED_REDUCTION_METHOD"
  reference_flow_hash: "sha256:REPLACE"
  loss_policy: "explicit_quantitative"
  security_profile_id: "N-1_PIN_CONTINGENCY_SET"
  internal_network_mode: "LF"
hydrogen:
  method: "exogenous_h2_network_operationally_optimised"
  electrolysis_port_map_hash: "sha256:REPLACE"
investment:
  candidate_registry_hash: "sha256:REPLACE"
  stage_sequence: ["real_candidates", "remaining_plus_conceptual_offshore", "storage"]
  storage_horizon: ["2040", "2050"]
  nonanticipativity: "shared_first_stage_x"
  objective_profile: "EXPECTED_TOTAL_SYSTEM_COST_PINNED"
tools:
  - {model_id: "M1", engine: "PIN_VERSION", role: "conformance"}
  - {model_id: "M2", engine: "PIN_VERSION", role: "conformance"}
result:
  compare_portfolio_id: true
  compare_objective_and_feasibility: true
  robustness_claim: "not_yet_validated"
```

**Kommentar:** Gewichte für 2040 sind aus [S01 `3.7] als **Konsultationsstand** übernommen; alle `sha256:REPLACE` und Engine-IDs sind absichtlich **ungültige Platzhalter**. Das Beispiel ist nicht produktiv einsetzbar.

## 4. Falsifizierende Testmatrix (spezifiziert, nicht ausgeführt)

| Test | bewusst erzeugter Fehler / Variante | Erwartetes Ergebnis | Architektur/Requirement |
|---|---|---|---|
| **T01** | anderes PECD-CSV trotz identischer Szenario-ID | REJECT | A+/IO-R02 |
| **T02** | Klimajahre einzeln mit unterschiedlichen Klima-Modellen, falscher Join | REJECT | A+/IO-R04/05 |
| **T03** | drei `pi_s` fehlen oder Summe ≠1 | REJECT | B, A+/IO-R04/14 |
| **T04** | `x_s` frei pro Wetter statt shared x | REJECT als 1:1 | B/IO-R13 |
| **T05** | Konzeptexpansion in Stage 1 oder Kandidat doppelt | REJECT | B, A+/IO-R12 |
| **T06** | `storage_expand` für 2035 im 2026-Referenzprofil | REJECT oder eigener Varianten-Contract | B/IO-R12 |
| **T07** | Port-ID, Leitungsorientierung oder slack/base inkonsistent | REJECT | A+/IO-R03/06 |
| **T08** | `A_z Gamma != P A_d` | REJECT | A+/IO-R07 |
| **T09** | `A_z Gamma == P A_d`, aber kritische N-1-Linie verloren | PASS Bilanz; **FAIL Netzqualitätsgate** | A+/B+/IO-R08/09 |
| **T10** | äquivalente Leitungskapazität als Summe Einzelratings angenommen | REJECT als behauptete exakte 2026er Methode | B, A+/IO-R08/09 |
| **T11** | islanding-Kontingenz ohne Kennzeichnung entfernt | REJECT Security Claim | A+/IO-R09 |
| **T12** | variable/fixe Nachfrage in Zonen vertauscht | REJECT Markt-/Asset-Mapping | A+/IO-R10 |
| **T13** | H₂-Freeze als operativ optimiertes Modell ausgegeben | REJECT Conformance; separate Sensitivität ggf. zugelassen | A+/B+/IO-R11 |
| **T14** | LF-Expansion mit aktiven internen Limits anstelle freier LF-Limits | REJECT als 1:1, APPROVED_VARIANT nur als explizite OPF-Studie | B/B+/IO-R15 |
| **T15** | PST in Zielengine ignoriert (oder schmaler Adapter lehnt ab) | REJECT; nicht still approximieren | A+/B/IO-R15/16 |
| **T16** | optimierte Gesamtkosten annähernd gleich, Portfolios stark verschieden | keine automatische „Fail“/„Pass“; degeneracy/objective/Regret prüfen | B+/IO-R17/18/19 |
| **T17** | identisches LP in 2 Solvern als „methodisch robust“ bezeichnet | **FAIL claim gate**, Solverdiversität ist andere Dimension | B+/IO-R17 |
| **T18** | holdout-Extremjahre decken ungesehene ENS/Korridorausfälle auf | `ROBUSTNESS_FINDING`, nicht zwingend Modellfehler | B+/IO-R19 |
| **T19** | ein Source-Asset wird neu zu einer anderen Zone gemappt, downstream unverändert | Quarantäne aller abhängigen Runs/Portfolios | A+/IO-R20 |
| **T20** | unabhängige Engine erzeugt gleiches LP, aber anderes primal-feasible Portfolio mit gleichem Objective | **PASS** nur bei Feasibility/Optimalitäts-/Degeneracyprüfung, nicht Byte-Gleichheit von x | B/IO-R13/14/17 |
| **T21** | unbekannte Konverterfähigkeit oder unpinned Version | REJECT im offiziellen Conformance Mode | A+/IO-R16 |
| **T22** | Forecast-Wetterjahre mit Zeitschrittgewicht statt Szenariowahrscheinlichkeit multipliziert | REJECT | B, A+/IO-R03/04/14 |
| **T23** | Modell-M1-Portfolio in M2-Detailnetz infeasible, aber Kosten numerisch niedriger | `NON_COMPARABLE` und Security Finding vor Kostenranking | A+/B+/IO-R08/09/18 |
| **T24** | stabiler Korridorrang nur bei anderem Candidate Set | REJECT gemeinsame Robustheitsaussage | B+/IO-R12/19 |

**Nicht gemessen:** numerische Schwellen, Solver-Toleranzen, AC-/N-1-Benchmarks und reale/industrielle Regressionen. Diese Tests sind eine **Abnahmespezifikation**.

## 5. Go-/Stop-Regeln

`G0` finale Geltungsfassung + Sicherheits-/Toolscope freigegeben; `G1` Input-/Weather-/Candidate-/Network-Manifeste gültig; `G2` negative Source- und Adaptertests fail-closed; `G3` exakte B-Teilmodellklasse in 2 unabhängigen Generatoren nachgewiesen; `G4` zonale Qualitäts-/N-1-Tests akzeptiert; `G5` M1/M2 auf gleichartigem Study Contract reproduzierbar; `G6` independent severity-/robustness experiment; `G7` fachlicher Sign-off.

- **Vor G0–G5 nur Forschungspilot.**
- **Vor G6 niemals „robuste Systembedarfe“ als empirisch belegt formulieren.**
- **Keine erfundenen Zahlen-Schwellen:** Akzeptanzschwellen vor Pilotlauf schriftlich genehmigen.
