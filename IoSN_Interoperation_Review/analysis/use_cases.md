# IoSN — High-Level-Use-Cases und Gegenbeispiele (UC1–UC9)

**Methodischer Status:** definierte Prüfdesigns, nicht durchgeführte Multi-Tool-Versuche. Quelle [S01](../sources/bibliography.md) ist **Konsultationsentwurf** (25.02.2026); Repo [R01–R08] ist **IoSN-near-Forschung**. Zahlen in **UC8** sind **rein illustrativ**, nicht aus offiziellen TYNDP-Modellen.

## UC1 — „M1 fertig, wie soll M2 genutzt werden?“

**Planungsfrage:** Ist das aus M1 (z. B. PLEXOS) abgeleitete Ausbauportfolio ein reproduzierbarer Optimallösungsbefund oder ein modellspezifisches Ergebnis?

**Vier klar verschiedene M2-Rollen:**

| M2-Rolle | M2 erhält | Was wird getestet? | Welche Interpretation ist untersagt? |
|---|---|---|---|
| **C1: Independent Conformance** | **identisches formales LP-/stochastisches Referenzproblem**, Kandidaten, Netz, Wetter, Bounds und Gewichte; eigener Modellgenerator | Constraints, objective und numerische Solution/Portfolio-Gleichwertigkeit | „andere Modellmethode ist robust“, obwohl Algebra identisch |
| **C2: Independent Method** | gefrorene ursprüngliche Quellinputs, Study Contract, **genehmigtes abweichendes Methodenprofil** | Robustheit der **Systembedarfs-/Portfoliowahl** gegenüber Modellstruktur | 1:1 Konformität |
| **C3: Downstream Physical Checker** | M1-Ausbauportfolio `x`, Dispatch-/Einspeisungen, Topologie-ID, Mapping und Testkontingenzen | Prüfung der physischen Feasibility des Portfolios am detaillierten Netz | dass ein nachgelagertes Netztool einen unabhängigen optimalen Ausbau berechnet hat |
| **C4: Second Solver** | dieselbe von M1 erzeugte LP/MPS-Datei | Numerik/Optimalität, Solververhalten | unabhängige Erzeugung der Gleichungen oder Methodendiversität |

**Ablauf nach Abschluss von M1:** Quellstudiensnapshot inkl. Wetter-/Netz-/Candidate-Hashes, Stufe, Solver/Seeds, Optimallösungsstatus **einfrieren**; M2-Modus und zugehörige Contract-IDs wählen; Tests gegen positive/negative Kontrollinstanzen; nur gleichartige Läufe vergleichen. **Abweichung ist zunächst Finding**, nicht automatisch Fehler oder Robustheitsnachweis.

**Architektureignung:** A+ ist Querschnittsvertrag; **B** für C1, **B+** für C1+C2, A+ mit Netzprofil für C3. Die `5.1-Sanity Tests sind begrenzte Vorbilder, **keine** endgültige Portfoliokonformität.

## UC2 — Modellfehler im gemeinsamen stochastischen LP: Nichtantizipativität

**Fehler:** M1 optimiert ein gemeinsames `x` über alle drei Wetterjahre; M2 übersetzt fälschlich in drei separate Investitionsvariablen `x_s`, wählt je Klimajahr unterschiedliche Leitungen. Die gewichtete mittlere Zielfunktion könnte sinken; die Lösungen beschreiben aber **nicht dieselbe realisierbare Planungsentscheidung**.

**Input-/Output Contract:** dieselben 3 `weather_scenario_id` und `pi_s`, `same_stage_1_decision_id`, identische Candidate-Bounds, Zieljahr, Zielfunktion, Betriebskosten, ENS/VOLL und Netz-/Speicherconstraints. Outputs `investment_vector_x`, `objective_cost`, `operational_cost_by_s`, `constraint_residuals`.

**Fehlerdiagnose:** Die Existenz von nur einer `x`-Dimension pro Kandidat in einer grafischen Toolansicht reicht **nicht**; die erzeugte Algebra muss geprüft werden. Pflicht: symbolische/LP-Instanzprüfung, Szenario-Kopplungsbedingungen, Primär-/Dualtests, gleiche Szenariogewichte.

**Eignung:** B im Conformance Mode. A+ allein erkennt dies nur, wenn ein zusätzlicher mathematischer Validator eingebunden ist. B+ erlaubt als Robustheit **andere Zukunftsgewichte**, darf `x_s` aber nicht als gleichwertige offizielle Referenz verschleiern.

## UC3 — Unterschiedliche Wetterjahrauswahl (30→3) und Gewichte

**Fehlerquellen:** andere Kandidatenklimadaten, andere Standardisierung, PCA-Vorzeichen-/Rangkonvention, K-Means-Initialisierung, anderer Seed, anderes Repräsentantenjahr oder Clustergewicht. Gleiche Label `WS032` bei unterschiedlichen Time Series ist nicht dieselbe Instanz.

**Gleich:** ursprünglicher PECD-Snapshot, Klima-/Modelljahr, Feature-Definition, regionale Technologiegewichte, saison-/stundenbezogene Zeitordnung; offizielle 2026er Beispielgewichte aus [S01 `3.7]: 2035 `0.24/0.43/0.33`; 2040 `0.20/0.40/0.40`; 2050 `0.23/0.57/0.20`, **Stand Konsultation**.

**Zwei klare Tests:**
1. **Conformance:** M1/M2 selektieren bei identischer Daten-/Algorithmusversion **dieselben** Jahre und Gewichte; Delta bei Seeds/Clustergrenzen wird erklärt, nicht toleriert, falls die Norm Determinismus verlangt.
2. **Robustheit:** andere **vorab registrierte**, sachgerechte Selektionsmethoden [R07 ist nur *wissenschaftlicher Vorschlag*] dürfen andere Jahre erzeugen; der **Ausbaukern** ist dann mit methodisch konsistenten Inputs neu zu rechnen. Zusätzlich **holdout**-Bewertung mit nicht als Vertreter genutzten Klimajahren.

**KPI:** Gewichtskonsistenz, Coverage in Merkmalen/extremen Systemzuständen, Worst/Quantile ENS, Investitionsranking und Cross-Regret. **Eignung:** A+ + Algorithmusprofil; B für exakten Algorithmus; B+ für genehmigte Selektionsexperimente.

## UC4 — Clustering und Netzreduktion: gleiche Bilanz, falsche Engpässe

**M1:** Busmap 1 mit dispatchbasierter Überlastungsenergie (in [R03] als IoSN-naher Forschungsrekonstruktionsansatz).  
**M2:** Busmap 2 mit alternativer RES-/Load-Sensitivität [R03, **eigener wissenschaftlicher Ansatz**]. **A/B der Clusteringmethoden sind nicht die A/B-Architekturen.**

**Übersetzung:** Detailliertes Netz `A_d` und nodale `p_d`, Branchflüsse `f_d`, Busmap→`P,Gamma,A_z`, Kalibrierungsreference, Ersatzimpedanzen/`F^eq`, richtungs-/saisonabhängige N-1-Limits.  
Die Identity `A_z Gamma = P A_d` belegt **Erhaltung der Knotenbilanz unter den definierten Operatoren**, nicht die Erhaltung von PTDF-/LODF-Sensitivitäten.

**Fallstrick:** Optimiert ein Ersatznetz einen geringeren Flow-RMSE, kann es einen seltenen **kritischen** Engpass verbergen; Investitionen werden eventuell auf einen falschen Korridor verschoben.

**Tests:** alle Quellknoten genau eine Zone, Zonenkonnektivität, `P/Gamma`, Peak-/RMS-Flow-Fehler, screening critical-edge recall, relative N-1-CNEC-Limitverletzung, negative LODF/Inselungsfälle, Portfolio-Rank im detaillierten Holdout-Netz. **Eignung:** A+ plus physischer Loss-/Quality-Contract; B für enges kalibriertes Matheprofil; B+ für Clustering-Methodendiversität.

## UC5 — Investitionsworkflow: real candidates, Erweiterung und Speicher

**Input:** Candidate Registry mit eindeutigem physical corridor, CAPEX/FOM, Größen-/Obergrenzen, Offshore/Konzept/Real-Kategorie; Zieljahre 2035/2040/2050; `stage_id`; bereits gebaute/teilweise gebaute Kandidaten aus Stufe 1.

**Fehler:** M2 überträgt nur Stufe-2-Eingangsdaten, löscht teilweise gebaute Stufe-1-Kandidaten oder ermöglicht theoretische Offshorekorridore schon in Stufe 1. Durch veränderte zulässige Menge ändert sich das Ausbauportfolio, obwohl gleiche Kandidatennamen vorhanden sind. Die 2026er Konsultationsfassung beschreibt **zweistufige** reale/konzeptionelle Erweiterung, gefolgt von Storage für 2040/2050 [S01 ``3.1.2,3.10].

**Tests:** Stufe-1-/2-Candidate-Set-Diff, transferierte Restkapazität, identische Upper Bounds, Storage im korrekten Horizon, objective components, optimal gaps; ein Kandidat darf nicht doppelt gebaut werden. **Eignung:** B für formalen optimierungsmathematischen Kern, A+ für orchestrierte Stage-/Candidate-Provenienz, B+ für explizit alternative Filtermethoden.

## UC6 — LF versus OPF und N-1: „gleiche Netzdaten“ ist keine gleiche Optimierungsfrage

**Methodisch konkreter Unterschied aus [S01 `3.9]:** Die zentral betrachtete LF-Expansion hält Netzphysik/Impedanzbeziehungen, setzt interne Interzonenübertragungslimits in diesem Modus jedoch auf unendlich. Eine begrenzte OPF-Variante betrachtet interne Constraints; die Methodik diskutiert die **Kappung** ihres Kandidatenportfolios auf LF-Expansion, um Umgehungsinvestitionen aus bestehenden internen Engpässen nicht falsch zuzulassen.

**Fehler:** M2 schaltet interne Limits ein, M1 nicht, und man erklärt die unterschiedlichen Optima fälschlich zum Converter-Bug. **Richtig:** andere **`method_id`**, andere Szenarioaussage. *Kein* mathematisch gleiches LP.

**Test:** LF-/OPF-Profile und Limitmetadaten eindeutig, gleicher Referenznetzstand, Nonanticipativity, Cross-Portfolio-Re-Evaluation, N-1-Feasibility **nur** im geprüften Contingency-/Injection-Set. **Eignung:** B für gleiche Variante, B+ für vordefinierte Varianten, A+ für Datenvertrag.

## UC7 — Sektorkopplung: H₂-/Elektrolysemodell

**Primärmethodik [S01 `3.6]:** H₂-Netzinfrastruktur wird **exogen** angenommen, H₂-Betrieb/Elektrolyse mit Elektroenergiebedarf gekoppelt. Die Option, H₂-Dispatch einzufrieren und daraus Elektrolyse-Lastzeitreihen je elektrischen Knoten zu übernehmen, ist eine **separate Sensitivität**.

**Fehler:** M1 optimiert den H₂-Betrieb, M2 übernimmt einen falsch verorteten/fixierten Elektrolyse-Lastblock; oder M2 investiert eigenständig in H₂-Netze, ohne dass dies als andere Methode gekennzeichnet ist. Die resultierende Stromaustausch-/Netzausbauentscheidung kann divergieren.

**Tests:** elektrochemische Wirkungsgrade/Einheiten, H₂- und Strom-Portidentitäten, Aggregation, jährliche Energie, Flexibilität, `hydrogen_mode=operational|frozen`, getrennte Bewertungslogik; nur explizite Szenariovarianten vergleichen. **Eignung:** A+ für Port- und Zustands-/Transformationen; B für formale Sektorkopplungsbilanz; B+ für methodische Sensitivität.

## UC8 — Unterschiedliche Portfolios trotz ähnlicher Zielfunktionswerte: Cross-Evaluation

**Schlüsselproblem:** M1 und M2 können nahezu gleiche optimierte Systemkosten nennen, aber andere Leitungs-/Speicherportfolios bevorzugen. Daher: **beide** Portfolios unter **beiden** vollständig deklarierten Bewertungsmodellen testen (fixiere `x`, optimiere nur operationellen Recourse mit gleichen `s,pi_s`). Alle Tests erfolgen auf erlaubter Feasibility-Menge, je identischem Study Contract.

**Illustrative Zahlen, keine realen TYNDP-Ergebnisse, normierte Gesamtkosten in Mio. €/a:**

| Evaluator | Portfolio `x_M1` | Portfolio `x_M2` | lokal bevorzugt |
|---|---:|---:|---|
| M1 | 100 | 106 | x_M1 |
| M2 | 108 | 101 | x_M2 |

**Illustrative Cross-Regrets:** im M1-Maßstab `106−100=6` für `x_M2`, im M2-Maßstab `108−101=7` für `x_M1`. Vergleich von nur „optimale Kosten 100 vs 101“ würde diese Modellunsicherheit verschleiern. **Nicht zulässig**, wenn die Portfolios auf verschiedenen Candidate Bounds/Startnetzen beruhen oder harte Feasibility-Constraints in einer Evaluierung verletzen.

**KPI:** Projekt-/Korridorranking, feasible project capacity deltas, Top-k overlap, Entscheidungsvorzeichen je Bedarfsregion, max-/weighted-regret und Out-of-sample ENS. **Eignung:** B+ oder A+ mit registrierten unabhängigen Methoden; B-Conformance testet zusätzlich Gleichwertigkeit innerhalb ein und derselben LP-Klasse.

## UC9 — Toolübersetzung: DC/PST/HVDC/Storage und schmaler PyPSA-Adapter

**Spezifikation:** Transfer M1→M2 kann nur dann `EXACT_VERIFIED` sein, wenn zu jedem gesetzten Merkmal das Zielmodell mathematisch äquivalente Semantik besitzt und dies getestet wurde. Dazu gehören u.a. Transformatortap/Phase-Shift, Link/Elektrolyse, Storage-State, Strom/Leistung, Szenariogewichte, saisonale Grenzwerte und Investitionsvariablen.

**Repo-Gegenbeispiel [R05]:** `src/tyndp_reduce/pypsa_adapter.py` ist bewusst ein **narrow lossless DC adapter**, der Transformer, nichtnullige Phasenschiebungen, Links, Stores und StorageUnits **ablehnt**; es wäre falsch, hier eine vollständige 2026er IoSN-Repräsentation zu behaupten.

**Tests:** (i) line-only DC mit genehmigter Source-/Target-Funktionsliste ist Kandidat für exakten Transfer; (ii) PST/Elektrolyse/Storage wird vor Conversion **REJECTED**, sofern Target kein Mapping hat; (iii) zonale `x^eq` oder N-1-Kapazitäten werden als **APPROVED_APPROXIMATION** klassifiziert, niemals als verlustfreie Rekonstruktion des Detailnetzes; (iv) Rückübersetzung prüft nur die erklärte Funktionsmenge.

**Eignung:** B für echte algebraische LP-Profile; A+ für Transformations-/Loss-Registry; B+ für bewusst andere Netzmethoden/Portfolioeffekte.

## Defect-Handling (gilt für alle UC)

**DETECTED → QUARANTINE → ROOT CAUSE → IMPACT GRAPH → REBUILD → RE-RUN → REVALIDATE → RELEASE.**

- Root Cause-Quellen: `source_dataset`, `selector`, `busmap`, `network_reduction`, `candidate_registry`, `reference_math`, `engine`, `KPI/postprocess`.
- Ein Fehler in der *gemeinsamen Quelle* betrifft **beide** Toolmodelle trotz perfekter Conformance.
- Bei geänderter Wetterjahrauswahl, Netzbusmap oder Candidate Registry **alle davon abhängigen** Ausbau-/Bewertungsergebnisse ungültig setzen.
- Speichere alte Versionen als `superseded`; keine stillschweigende Überschreibung der veröffentlichten Systembedarfsränge.
