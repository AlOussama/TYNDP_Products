# ML-R03 — Preprocessing & Transformation Contracts (P00–P17)
**Status:** NON_NORMATIVE_DRAFT · **Matrix:** `process_transformation_matrix.csv` mit **36** separaten Transformations- und Workflow-Verträgen; **alle 18** P00–P17 abgedeckt.

## 1. Contract-Signatur
Jeder `MLR03-Txx-yy` besitzt: `process_id`; Input-/Outputobjekte und deren semantische Typen; `required_if`; Vorbedingungen; Prozess-/Transformationssemantik; zu erhaltende technische/fachliche Eigenschaften; erlaubte Implementierungsfreiheit; kontrollierte Fehlercodes; Provenienz; Prüfverfahren; Owner-Entscheidungen. Die **Vollform je Operation** steht zeilenweise in der Matrix. `B01-Dxxx` sind Ausgangsinventar-IDs; `MLR03-I-...` sind **neu vorgeschlagene Zwischen-/Handover-Objekte**, ausdrücklich keine weiteren verifizierten MA03-Dateninventarpositionen.

Ein `input_object_id` eines Schritts kann ein Upstream-Payload, eine Konfiguration oder ein Output eines früheren Schritts sein. Der Matrixeintrag markiert nicht automatisch eine physische Quelldatei. Spezifikation und Ausführung sind getrennt: eine Transformation kann definiert und trotzdem `NOT_EXECUTED` sein.

## 2. Prozessbezogene Übersicht
| Prozess | Vertrag IDs | Kernübergang und Vorbedingungen | Nachbedingung / Erhaltung / Fehlerbehandlung |
|---|---|---|---|
| **P00** | `MLR03-T00-01` | Freigabeprofil und Run-Freeze, B01-D001/002 | eindeutige Methodik-/Datenvintage, sonst `RELEASE_BLOCKED` |
| **P01** | `T01-01/02` | Studien- und Variantenscope, Quell-Extracts | genau drei getrennte Zieljahre und source-version-FKs; fehlende Quelle blockiert |
| **P02** | `T02-01` | externe Auswahl der fünf CY-Fälle plus Profilreferenzen | CY1–CY5 je Jahr; dieselben noch offenen Gewichte; keinerlei Auswahlalgorithmus |
| **P03** | `T03-01/02` | Zeit-/Demand-/RES-/Hydro-/Kalenderdaten | UTC-Halboffenheit, Profilvollständigkeit und ggf. Energie-Reconciliation; keine stille Lückenfüllung |
| **P04** | `T04-01/02` | 2025-Topologie, 2035-Eligibility, fixe Offshore-Ziele | versioniertes Startnetz; keine unautorisierte Projektaufnahme |
| **P05** | `T05-01/02` | Detaillastfälle und belastete 225/400-kV-Leitungen | vollständiges eindeutiges Clustering; zusammenhängende Zonen; Qualitätsorakel TBD |
| **P06** | `T06-01/02/03` | Cluster, PTDF/LODF, Contingencies, HVDC/PST | Impedanzen, Offsets, Mesh, N−1-Kapazitäten und Abweichungsmessung; Grenzen TBD |
| **P07** | `T07-01/02` | Marktanlagen/-profile mit räumlicher Crosswalk | Zonale Ressourcen und Reihen ohne stillen Mengenverlust |
| **P08** | `T08-01/02` | Strom-/H2-/Hydro-/DSR-/Speicherreferenzen | gebundene Carrier-Bilanzen, deklarierte H2-Brennwertbasis, Hydro-Klassensemantik |
| **P09** | `T09-01/02/03` | Kandidaten-/Offshore-/Kostendaten | eindeutige Stage-/DC-Link-Semantik, Entfernung und Preisjahr, offene Faktoren sichtbar |
| **P10** | `T10-01/02` | Real-Kandidaten, LF-Semantik, 5 CY | gemeinsam über CY genutzte LP-Investitionsvariablen und Stage-1-Solve-Evidence |
| **P11** | `T11-01/02` | Stage 1 und restliche Kandidaten | deklarierte Carry-over-Regeln, kein doppeltes CAPEX/Portfolio |
| **P12** | `T12-01/02` | Stufe 2, Speicherpfade, Caps | nur 2040/2050; Bedarf nicht als einzelnes Investitionsprojekt ausgeben |
| **P13** | `T13-01/02` | Dispatch mit/ohne LF-Portfolio | vergleichbare Paare, signierter Differenzbezug und gleiche System-/Kostenbasis |
| **P14** | `T14-01/02` | Prä-Expansion Elektrolyseprofil | stundenweises H2-Freeze nach gebundener Baseline, Sensitivität getrennt |
| **P15** | `T15-01/02` | explizit entschiedene optionale OPF-Variante | Kapazitätsobergrenzen aus LF-Portfolio; OPF ersetzt LF nicht |
| **P16** | `T16-01/02/03` | Rohentscheidungen, P13/14/15 und Kosten | normalisierte Rohoutputs, needs/ONDP-Kennzahlen nur mit freigegebenen Definitionen |
| **P17** | `T17-01` | Testorakel, Signaturen, Herkunft und Ergebnisse | getrennte Evidenzklassen und offen sichtbarer Blockerstatus |

## 3. Detaillierte exemplarische Verträge

### TC-P02 — Externe Wetterfallübernahme `MLR03-T02-01`
**Inputs:** B01-D006 externe bereits ausgewählte CY-IDs/Gewichte, B01-D007 Auswahl-Handover, B01-D008 Profilquelle, B01-D003 Studienjahrscope. **Output:** `MLR03-I-P02-weather_manifest`.

**Preconditions:** externe Auswahl abgeschlossen, definierte Profile mit vollständigen Quellreferenzen; keine selbständige Bewertung/Re-Rangierung. Für formale Forschungsprüfung können numerische Gewichte offen bleiben. **Constraints:** `years={2035,2040,2050}`; `cases(y)={CY1,...,CY5}`; `weight(y,CYi)=w_i`; `w_i` über Studienjahre gleich; endgültige `w_i=TBD`. Für produktive Ausführung benötigen Gewichte reale, ownerbestätigte Werte; `w_i ≥ 0` und Normalisierung werden als technische Plausibilitätskandidaten getestet, **Toleranz TBD**.

**Postcondition:** jeder Kontext weist auf externe CY-/PECD-Quellprofilidentität, Selector-Owner und Provenienz. **Invalidity:** fehlendes Profil, doppelte CY, widersprüchliche Gewichte, fehlende Freigabe. **Verification:** Quervergleich des 3×5-Manifests, FK-Integrität und gemeinsame Gewichte; keine Selektionstestpflicht.

### TC-P03 — UTC-Zeitachsenharmonisierung `MLR03-T03-01/02`
**Inputs:** B01-D009/010/011/012/013 plus Wettermanifest. **Outputs:** expliziter UTC-Intervalldatensatz und ausgerichtete Reihen. Vorbedingung sind Quelldaten mit Kennzeichnung von Zeitbasis, DST-Status, Originalgranularität, Intervallmessart und Einheit. Konversion zu `[start,end)`, `duration`, `source_interval_id`; Abbildung zwischen unterschiedlicher zeitlicher Auflösung braucht eine dokumentierte resampling-Regel. Bei Energiemengen ist Summenerhaltung über das Vergleichsfenster möglich, bei Leistung die durational gewichtete Integralerhaltung. **Nicht zulässig:** unprotokollierte Interpolation, implizite Leapday-Elimination, doppelte DST-Stunde ohne Originalunterscheidung. Toleranzen und Jahreskalenderdetails bleiben MD-12.

### TC-P05/P06 — Zonierung und elektrische Reduktion
**Inputs:** detaillierter synchroner Netzstand, Überlastreferenzen, Flüsse/Injektionen, PTDF/LODF, PST/HVDC. **Outputs:** B01-D021/022, B01-D026–030, B01-D086/087. Die Abbildung `bus→zone` muss total sein oder explizit ausgenommene Nodes aufführen; für jedes Cluster wird Zusammenhang geprüft. Reduktionsparameter tragen `orientation`, `base_power`, `unit`, `reference_case`. Äquivalenz- und N−1-Tests vergleichen **dieselben** Referenzfälle und Kontingenzen. RMSE-Definition, N−1-Kapazitätskalibrierung, 102-Zonen-Interpretation und Akzeptanztoleranzen sind keine ungefragt übernommenen bindenden Parameter. Netzreduktion darf physikalisch begründete Abweichungen haben, aber nicht als verlustfrei behauptet werden.

### TC-P07 — Extensive vs. intensive Aggregation
Für echte Mengen wie `power_MW` auf gleicher zeitlicher Basis sei eine **illustrative** Zuordnung `p_target(z,t)=Σ_a α(a,z)p_source(a,t)` nur dann korrekt, wenn `Σ_z α(a,z)=1` und eine Doppelzuordnung ausgeschlossen ist; Ausnahmen und Toleranzen sind zu dokumentieren. Bei Verfügbarkeitsfaktoren/Wirkungsgraden darf dieselbe Summenregel **nicht** angewandt werden; expliziter gewichteter bzw. quellenspezifischer Operator erforderlich. Identitätswechsel und Reconciliation-Evidence sind Teil der Transformation.

### TC-P08/P09 — Sektorkopplung und Kandidatensemantik
Stromleistung, Elektrolyse und H2-Energie/-Masse führen separate Carrier- und Einheitenkonten. Effizienz, Umrechnungsbasis LHV/HHV und Zeitintervall sind Pflichtparameter, wenn die Konversion verwendet wird. Ein Netzausbaukandidat kann physisch AC sein, erhält in der LF-Expansion aber die methodisch festgelegte **steuerbare DC-Marktlink-Semantik**; dies ist keine automatische physische Netzreduktion. Kandidaten-IDs, RDFIDs, Stufenklassen, NTC-Richtungen und Längen sind explizit. Distanzfaktor 10–15% ist **Draft-Information**, nicht als faktischer Endwert festgelegt. Economics mit Preisbasis, WACC und Blocks ohne numerischen Default.

### TC-P10/P11/P12 — Gestufter Investitionslauf
P10 verwendet ausschließlich zulässige reale Kandidaten; `x(candidate,year)` ist innerhalb eines Studienjahres über alle fünf CY-Fälle dieselbe Entscheidungsvariable (nicht fünf unabhängige Investitionsentscheidungen). P11 überträgt das Stage-1-Portfolio nach dokumentierter `fix/carry/incremental`-Regel; bei unklarer Carry-over-Semantik ist eine produktive Berechnung nicht freigebbar. P12 berechnet getrennt für 2040 und 2050 generische Speicherbedarfe unter nachvollziehbaren Ländergrenzen. Jede Stufe exportiert Solver-Status, Feasibility-Witness und getrennte Kostenkomponenten. Datenformat und LP-Engine sind frei.

### TC-P13/P14/P15 — Vergleich und Nebenläufe
P13 kontrolliert ein Vergleichspaar: Studienjahr, CY, externes Profil, Startnetz-/Binnenleitungsstatus, Kostenparameter und Technologieparametrisierung sind auf gleiche Vergleichsbasis zu bringen; einzige bewusst variierende Dimension muss dokumentiert sein. P14 fixiert die Referenz-Elektrolyseleistung für **jeden** UTC-Zeitpunkt der H2-Sensitivität. P15 ist optional, bedarf expliziter Owner-/Run-Entscheidung, führt Kandidatenobergrenzen aus LF fort und muss getrennt als OPF gekennzeichnet werden.

### TC-P16/P17 — Berechnungs- und Evidenzgrenzen
Rohresultate (Optimierungsvariablen, Dispatch, Solverstatus) werden in `MLR03-I-P16-raw_result_index` mit Run-/Stufenidentität registriert. KPI-Definition fehlt? Dann `formula_status=TBD`, Ergebnis `UNDEFINED`, keine Zahl. Untergrenze für Kleinstausbau bleibt `TBD`. P17 führt Struktur, referenzielle, dimensionsbezogene, fachliche, mathematische und freigabegebundene Prüfungen **separat**; kein `PASS` ohne Ausführung.

## 4. Verifikation der Matrix und unverbindliche Invarianten
**Struktur:** jede referenzierte `B01-Dxxx` muss im Inventar vorkommen; jedes neue `MLR03-I-...` muss mindestens als Transformationsoutput deklariert sein; alle P00–P17 mindestens einmal vertreten; `transformation_id` eindeutig; ein Producer-/Consumer-DAG darf keine unkommentierten Zyklen erzeugen.

**Semantik:** vollständige Quell-/Ziel-Grains; keine Doppelzählung; kohärente Mengen-/Zeiteinheiten, Wahl zwischen bilanzierbaren vs. verlustbehafteten Transformationen; verbindliche numerische Schwellenwerte nur mit Owner-/Methodikreferenz. Fehler erhalten Status, Schwere, Quelle, betroffene Runs und Disposition. Ein fehlender originaler Input ist kein `zero`; ein optionaler P15-Nebenlauf ist kein obligatorischer Kernlauf.

**Lücken:** Ursprungstreue des 2025-Netzes, Projekteligibilität, Äquivalenz-/Clustering-Kalibrierung, LF-/OPF-Detailsemantik, Storage- und KPI-Formeln, Datenversionen und Einheiten-Konversionsbasis bleiben MD/CL-gesteuert. Keine produktive Transformation und keine behauptete physische Validierung sind Bestandteil dieses Pakets.
