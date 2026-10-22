# Falsifizierender IoSN Architektur-Pilot: A/A+/B/B+ im Prozess

**Pilotstatus: konzipiert, nicht ausgeführt.** Keine Anpassungen an `src/tyndp_reduce/`, `docs/current/`, `tests/` oder `results/synthetic/`; nur Review-Dokumente im eigenständigen Ordner.

## 1. Drei getrennte Pilot-Lanes

### Lane I — Exact Conformance (B/Referenzmodus B+)

**Ziel:** Können zwei eigenständige Tools eine **vollständig formulierte kleine stochastische LP-Ausbauaufgabe** mit identischen Daten/Netzprofilen korrekt reproduzieren?

1. Genehmigte, explizite LP-Teilklasse und 2026er Szenariobegriff präzisieren: gemeinsame Ausbauvariable `x` über drei `s`, `pi_s`, Node-Bilanzen, Netzkapazitäten, Storage, Kosten, ENS, Candidate Bounds. Für noch nicht freigegebene Normteile **„review reference formulation“** statt „official 2026 identical“.
2. Synthetisches 3-Knoten-Modell gemäß Motiv aus [S01 `5.1] mit Variablen-/Constraint-Export, dann Erweiterung um **3 Wetterjahre + 1 Leitungsbauoption**. Wiedergabe offizieller Zahlentabellen ist **nicht** erforderlich und wird nicht behauptet.
3. M1 und M2 **separat modellgenerieren**, nicht nur dasselbe MPS mit anderem Solver lösen. `nonanticipativity`, Objective, Bounds, Primal/duale Restfehler und bei degenerierten Optima Epsilon-Kosten-/Feasibility-Klassen prüfen.
4. Negativtests: `x_s` statt `x`, falsches `pi_s`, Kandidat im falschen Stage, fehlender PST/Link/Storage.
5. Ausgaben: `reference_problem_spec`, `M1_model_manifest`, `M2_model_manifest`, `algebra_diff`, `conformance_tests`, `capability_report`.

**Go:** jede positive Instanz innerhalb vorab genehmigter mathematischer/numerischer Kriterien oder als deklarierte Nichtunterstützung; jeder negative semantische Fehler vor Ergebnisfreigabe abgefangen.

### Lane II — Process Interoperation (A+)

**Ziel:** Wird ein detaillierter Input konsistent in Zonen-/Marktdaten und Investitionsinstanzen überführt, einschließlich dokumentierter Näherungen?

1. Quellen-Netz, Dispatch und 30-Klimajahr-Referenzen einfrieren. Bei realem Datensatz nur nach Zugriffs-/Rechtefreigabe; synthetische Daten ausdrücklich als Forschung.
2. Wetterjahrauswahl und Gewichte fixieren; Reproduzierbarkeit der Features, PCA/KMeans, Seeds, Repräsentanten und Synchronisierung prüfen.
3. Detaillierter Dispatch → kritische Kanten → Busmap/`P/Gamma` → ersetzte Impedanzen/Kapazitäten/No-load-Flow → PECD-/Asset-/H₂-Mapping.
4. Führe Topologie-/Energy-Balance-/PTDF-/N-1-/Re-CNEC-Validierung an Quellnetz-Kontingenzen aus; kontingente Islandingfälle nicht still ausschließen.
5. Führe unter positiver und absichtlich korrumpierter Transferinstanz den **vollständigen Capability/Loss Report** aus. Kein `EXACT_VERIFIED` für generische AC→zonal-Reduktion.

**Go:** reproduzierbare Handoffs und einheitliche Identitäten; **alle** P0-Grenzen eingehalten; jeder Verlust freigegeben und mit der abhängigen Portfoliowirkung verknüpft.

### Lane III — Independent Need-/Decision Robustness (A+ mit Varianten bzw. B+)

**Ziel:** Ändern zugelassene Varianten der Wetterjahrauswahl, Netzreduktion, LF-/OPF-Interpretation oder H₂-Kopplung den **identifizierten Systembedarf**?

1. Methods Registry mit vorab freigegebenen Varianten (offizielle Baseline separat, Forschungsalternativen **niemals** als 2026er Norm deklarieren).
2. Läufe möglichst als faktorielles, **gepaartes** Design: gleiche Studie, wenn nur *eine* gewollte methodische Dimension variiert; Änderungen anderer Inputs sperren oder als Confounder markieren.
3. Für jedes validierte M1/M2-Portfolio `x_M1, x_M2` nach identischer Candidate-Feasibility jeweils im gleichen Modell re-evaluieren: 2×2-Kosten-/feasibility-Matrix.
4. Re-Evaluate bei **ungesehenen** Klima-/Netzsituationen (holdout-Wetterjahre, kritische Kontingenzen); prüfe Engpass-/Korridorrang, nicht nur total cost.
5. Trenne Unterschiede aufgrund des **Modells** von Unterschieden aufgrund **anderer Szenarioauswahl** oder **anderer Netzinformation**; „unvergleichbar“ bleibt zulässige Erkenntnis.

**Go:** jeder sichtbare Portfolio-Divergenzpunkt als methodisch erklärbar, confounded oder Fehler klassifiziert; Regret, Missed-Critical-Corridors und Holdout-Feasibility publizierbar mit vorher genehmigten Schwellen.

## 2. Pilotfälle und Failure Injection

| Mini-Pilot | Gezielt falsifizierbare Behauptung | Negativfall | Hauptmetrik |
|---|---|---|---|
| P1 | 3 Szenarien in gleicher Modellklasse → gleiche Investitionslogik | `x_s` statt `x`, Gewichtsvertauschung | objective/constraint/nonanticipativity |
| P2 | genaue Bilanz → gleicher Netzfluss | gleiche `P/Gamma`, aber falsche Ersatzimpedanz | Critical line recall, PTDF/Flow-RMSE, N-1 |
| P3 | M1 und M2 nach Sanity-Check voll konform | PST/Link/Storage-Annahme verschieden | Capability/Algebra-Diff |
| P4 | selbe Candidate Registry → gleicher Ausbau | Stagefilter, teilgebaute Leitungen unterschiedlich | Candidate set, Feasibility, Portfolio-Regret |
| P5 | 3 repräsentative Jahre → robuste Zukunftsentscheidung | ungesehene extreme Jahre | holdout cost/ENS + ranking |
| P6 | LF- und OPF-Portfolio direkt 1:1 vergleichbar | Internal limit mode vertauscht | method-id, violation count, cross-eval |
| P7 | H₂-Einbindung ohne separate Methodikgleichheit | frozen vs operativ optimiert | Elektrolyse-last/energy, Port balance |
| P8 | Zwei Solver liefern gleiche Modellentscheidung | gleiches LP mit alternativen Optima | objective/epsilon-optimal feasible-set |

## 3. Bewertungsmaßstab und Auswahl A+/B/B+

**Vorab dokumentieren:** (i) offizielle Muss-Methoden/zulässige wissenschaftliche Varianten; (ii) Anzahl und Laufzeit notwendiger Adapter-/Algebra-Tests; (iii) zusätzliche Daten-/Tool-Governance; (iv) Fehlerentdeckungsrate aus Negativtests; (v) Einfluss kritischer verlustbehafteter Handoffs auf Portfolio; (vi) Unterschied zwischen solver und mathematischer Modellimplementierungsunabhängigkeit.

**Resultatreife:**
- `DESK_REVIEW_ONLY`: aktueller Stand dieses PRs.
- `TECHNICAL_CONFORMANCE`: alle Lane-I-Gates für **abgegrenzte** Modelle erfüllt, nicht IoSN insgesamt.
- `PROCESS_INTEROP_VALIDATED`: Lane II gegen freigegebenen Testdatensatz und Handoffs bestanden.
- `INDEPENDENT_ROBUSTNESS_EVALUATED`: Lane III mit expliziten Varianten, Cross-Regret und Holdout erfolgreich.
- `OFFICIAL_TYNDP_REPRODUCTION`: nur nach dokumentierter Vollmethodenfreigabe, Datensatz-, Tool-/Regulatory- und unabhängiger externen Replikation. **Nicht** durch synthetische Ergebnisse erreichbar.

## 4. Entscheidungsgates und Folgeartefakte

| Gate | Freigabegegenstand | Stop wenn ... |
|---|---|---|
| G0 | versions- und regierungsrechtlicher Normstand | konsultative Regel wird als final ausgegeben |
| G1 | gleiche Auswertungsfrage, Daten-/Candidate-/Wetterdefinition | beliebige gemischte Methoden/Inputs |
| G2 | Converter Capability- und Loss-Bericht | Feature fehlt oder wird ohne deklarierte Folgen weggelassen |
| G3 | algebraische Instanzidentität (Lane I) | `x_s`, Objective/Bounds oder Solverstatus weicht ungerechtfertigt ab |
| G4 | Netzwerkphysik-/N-1-Validierung (Lane II) | kritischer Engpass/Outage ungeprüft verschwindet |
| G5 | unabhängiger Portfolio-Holdout-Test (Lane III) | Methodenänderung/Confounder ungeklärt |
| G6 | Architektur-TCO, Freigabe und reproduzierbarer Audit | wesentliche Critical Findings offen |

**Nach späterer Durchführung** statt vorherigem Vortäuschen: `pilot/contracts/*.yaml`, `pilot/validation/algebra_diff.csv`, `pilot/validation/network_loss.csv`, `pilot/validation/m1_m2_portfolio_matrix.csv`, `pilot/validation/robustness.csv`, `pilot/final_adr.md`. PoC-Code (falls beauftragt) unter einem **eigenen Pilotverzeichnis**, nicht im kanonischen Paket.
