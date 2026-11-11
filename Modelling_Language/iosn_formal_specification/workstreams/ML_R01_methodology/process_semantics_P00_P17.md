# ML-R01 — Prozesssemantik P00–P17

**Referenz:** BUNDLE-01R Basiscommit 5c13d4d...; O26 = ENTSO-E IoSN Consultation Draft 25.02.2026, §§ wie angegeben. **Status RESEARCH_ONLY; G1 BLOCKED.** Dieses Dokument legt für jeden MA-01-Prozessschritt die neun verlangten Analysefelder dar. Der Ursprung ist die unveränderte MA-01-Prozessmatrix, erweitert um ausdrücklich als **SCI-DERIVED** gekennzeichnete wissenschaftliche Prüfsemantik. D1–D6 beziehen sich ausschließlich auf dieses Forschungsprofil.

**Abweichung O26 vs D2:** §3.7 O26 publiziert je Studienjahr drei Wetterfälle mit unterschiedlichen Gewichten. Für ML-R01 gelten **nur als Forschungsprofil** die fünf exogen gelieferten Fälle CY1–CY5 mit über 2035/2040/2050 identischen, noch unbekannten Gewichten; Wetterselektion ist ausgeschlossen. **O26 darf nicht stillschweigend als geändert ausgegeben werden.**

## 1. Prozessabhängigkeiten

~~~mermaid
flowchart LR
 P00-->P01-->P02-->P03
 P04-->P05-->P06-->P07
 P03-->P07-->P08
 P07-->P08
 P09-->P10-->P11-->P12
 P08-->P10
 P12-->P13-->P16-->P17
 P12-->P14-->P16
 P12-. optional .->P15-. optional .->P16
~~~

Die Pfeile sind fachliche Abhängigkeiten; P04/P09 werden aus separaten Eingangsdaten gespeist. Keine Orchestrierungsvorschrift.

## 2. Neun Analysefelder pro Schritt

### P00 — Source/profile release gate

**Quellennachweis:** O26 O26 cover; D governance (Draft); MA-01-Prozessmatrix P00, zugeordnete SR: keine direkte aktive SR (Governance-Forschungsauftrag).

1. **Fachliches Ziel und Einordnung:** Source/profile release gate. Document identity and authority traceable.
2. **Eingangsdaten/Referenzen:** O26 release metadata; approved overrides. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** No study profile silently defaults to draft status. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Dokumentidentität und Version sind diskrete Zustände; Validität der Methodik ist keine Variable eines LP. Entwurfsstatus darf durch formale Konsistenzprüfung nicht in Adoption übergehen.
5. **Zulässige fachliche Freiheitsgrade:** Freie Archivierung, Manifestform und Abfrageschnittstellen; die belegbare Statusklasse nicht verändern. MA-01-Freiheit: Document-management platform free.
6. **Ergebnis/Weitergabe:** **source_manifest** — Authority/vintage/scope. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P01 (Gate-Forschungsstatus), indirekt alle nachgelagerten.
8. **Verifikation:** Document review; wissenschaftliche Gegenprobe: Vergleich gegen Release-Entscheidung/Datum/Originalbyte-Hash und Signatur; fehlender Nachweis = NOT_VERIFIED / G1_BLOCKED. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** B-01; O26 nur Konsultation; Release, Autorität, Effective-Date, SHA256 und mögliche neuere Fassung (MD-01).

**Nichtkonformitätsrisiko / Testanlass:** Missing source or contested status. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P01 — Study horizon/scenario intake

**Quellennachweis:** O26 §§3.2,4.1 (Draft); MA-01-Prozessmatrix P01, zugeordnete SR: MA01-SR-002, MA01-SR-004, MA01-SR-039.

1. **Fachliches Ziel und Einordnung:** Study horizon/scenario intake. Horizon and data vintage identified.
2. **Eingangsdaten/Referenzen:** Scenario source slices; 2035,2040,2050. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** No inadvertent 2030 IoSN run; target years separate. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Studienjahre Y={2035,2040,2050} bilden *getrennte* Optimierungsprobleme; kein per Default gemeinsamer intertemporaler Investitionszustand.
5. **Zulässige fachliche Freiheitsgrade:** Szenarioverwaltung und Importverfahren frei, nicht die Studienjahr-Identitäten oder die einheitliche semantische Referenz. MA-01-Freiheit: Import/storage free.
6. **Ergebnis/Weitergabe:** **study_manifest** — Horizon identity, external data references. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P00, P02, P03, P08, P10–P12.
8. **Verifikation:** Manifest cross-check; wissenschaftliche Gegenprobe: Verhindern von 2030-Substitution, Vergleichen aller drei Zieljahrausgaben und Szenario-IDs; keine versteckte Cross-Horizon-Zielfunktion. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** DATA-VERSION; MD-11 Datenreleases; Abweichung der Szenarioobjekte und Szenariojahre; Quellenvintage.

**Nichtkonformitätsrisiko / Testanlass:** Missing/incompatible scenario or unit. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P02 — Previously selected weather-scenario intake

**Quellennachweis:** O26 §3.7 p.20 (Draft); MA-01-Prozessmatrix P02, zugeordnete SR: MA01-SR-004, MA01-SR-010, MA01-SR-011, MA01-SR-040.

1. **Fachliches Ziel und Einordnung:** Previously selected weather-scenario intake. Selection completed *upstream*; no raw candidate pool.
2. **Eingangsdaten/Referenzen:** External IDs, number, weights, PECD reference. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Bind IDs+weights and declare annual/profile source; reject invalid metadata. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Für C={CY1..CY5}: pi_c>=0, sum(pi_c)=1; pi_(y,c)=pi_c für alle y. Nur *Eingangsprüfung*; O26 verwendet drei andere Fälle pro Jahr.
5. **Zulässige fachliche Freiheitsgrade:** Manifestformat/ETL frei; kein PCA, K-Means, Wetterjahrentscheid oder Statistikreplikation in ML-R01. MA-01-Freiheit: Serializer free; no selection algorithm.
6. **Ergebnis/Weitergabe:** **selected_weather_manifest** — Study-year-specific weight/ID sets. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P00, P01, externes Wettermanifest; liefert P03.
8. **Verifikation:** Contract/data test; wissenschaftliche Gegenprobe: Fünf eindeutige CY-IDs je Zieljahr; in allen Jahren gleiche Gewichte; nichtnegative endliche Werte und Zeitreihenverweise; keine numerische Summentoleranz ohne Freigabe. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** WEATHER-BOUNDARY; MD-12/18/19; Werte der fünf Gewichte, Profilmanifest, Quelle/Zeitraum und Toleranzen offen.

**Nichtkonformitätsrisiko / Testanlass:** Unresolved ID, negative weight, duplicate, inconsistent sum. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P03 — Temporal/market input preparation

**Quellennachweis:** O26 §§3.7,4.1–4.4 (Draft); MA-01-Prozessmatrix P03, zugeordnete SR: MA01-SR-004, MA01-SR-011, MA01-SR-040, MA01-SR-042.

1. **Fachliches Ziel und Einordnung:** Temporal/market input preparation. Explicit calendar, carrier, spatial/temporal alignment.
2. **Eingangsdaten/Referenzen:** Weather-indexed hours, hydro time axes, market data, DFT. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Align only needed IoSN series; document any transforms; do not redo selection. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Leistung MW wird über Intervalldauer in Energie MWh überführt; ein UTC-Intervall darf keiner zweiten lokalen Stunde ohne eindeutiges Mapping zugeordnet werden. Wetterprofil und Stundenindex sind getrennte Achsen.
5. **Zulässige fachliche Freiheitsgrade:** ETL, Resampling und Speicherlayout frei, *sofern* freigegebene zeitliche/sachliche Erhaltung und Provenienz belegt werden. MA-01-Freiheit: ETL/time-container free.
6. **Ergebnis/Weitergabe:** **aligned_timeseries** — Generation/demand/hydro with units and provenance. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P01, P02; liefert P07 und P08.
8. **Verifikation:** Series alignment/reconciliation; wissenschaftliche Gegenprobe: UTC-Schlüssel, Intervallgrenzen, Δt und Einheitenprüfung; Reaggregation, Vorher/Nachher-Energiesummen und Lückenbehandlung (soweit entschieden). **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** TIME-AXIS; MD-12: DST/Leap, Zeitzonen-, Fehlstellen-, Resampling- und repräsentative Stundenregeln; keine fiktive Toleranz.

**Nichtkonformitätsrisiko / Testanlass:** Time shifts, gaps or unsupported temporal conversion. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P04 — 2035 starting grid and fixed offshore reference

**Quellennachweis:** O26 §§3.4–3.5; Annex 6.2 (Draft); MA-01-Prozessmatrix P04, zugeordnete SR: MA01-SR-005, MA01-SR-006, MA01-SR-048.

1. **Fachliches Ziel und Einordnung:** 2035 starting grid and fixed offshore reference. Project eligibility from §3.4 / EXT-CBA4; starting year 2035.
2. **Eingangsdaten/Referenzen:** 2025 grid; eligible project list; fixed national offshore targets. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Include qualified 2035 grid and offshore hybrid baseline. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Für 2035 gilt exogenes Ausgangsnetz plus nachgewiesen qualifizierte Projektliste; Netzinvestitionen werden *nicht* rückwirkend zu Baselineelementen. Offshore-Ziele sind Inputs.
5. **Zulässige fachliche Freiheitsgrade:** Elektrisches Datenmodell, Projektverknüpfung und Zonen-IDs intern frei; Eligibility-/Kapazitätsnachweis muss prüfbar bleiben. MA-01-Freiheit: Network serialization free.
6. **Ergebnis/Weitergabe:** **reference_grid** — Baseline project identities, directional capacity, offshore fixed targets. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P00, P01; liefert P05/P06 und P08.
8. **Verifikation:** List-to-source audit; wissenschaftliche Gegenprobe: Projekt-ID/RDFID/Status, Commissioning- und Länderregeln gegen Originalquelle; 2035-Baseline und fixe Offshore-Ziele als Kontrollvektoren. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** GRID-ELIG;OFFSHORE-TARGET; MD-11/14, MA02-CL-001; O26 §3.4 vs CBA4 und H24 kein freigegebener 2035-Crosswalk.

**Nichtkonformitätsrisiko / Testanlass:** Unjustified project include/exclude, RES target mismatch. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P05 — Zonal clustering

**Quellennachweis:** O26 §3.8.1; Annex 6.1 (Draft); MA-01-Prozessmatrix P05, zugeordnete SR: MA01-SR-013, MA01-SR-014, MA01-SR-015, MA01-SR-016, MA01-SR-022.

1. **Fachliches Ziel und Einordnung:** Zonal clustering. Network connectivity and traceable bus-zone assignment.
2. **Eingangsdaten/Referenzen:** Detailed synchronous grid; critical-line exposure. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Prioritize constrained branches/annual overload energy, avoid disconnected clusters; 102 zones for O26 case. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Partition b:V_detail→Z, eindeutige Zuordnung, jede induzierte Zone connected; kritisch belastete Zweige werden auf Zonenränder abgebildet oder begründet behandelt. 102 Zonen ist O26-Quellprofil.
5. **Zulässige fachliche Freiheitsgrade:** Graphpartitionierung/Optimierungsheuristik frei, wenn kritische Leitungen, Flussrichtungen und Qualitätsgüte berücksichtigt und belegt sind. MA-01-Freiheit: Clustering algorithm implementation free within method class.
6. **Ergebnis/Weitergabe:** **zonal_clusters** — Busmap, connected zones, critical line mapping, metrics. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P04; liefert P06.
8. **Verifikation:** Graph & congestion tests; wissenschaftliche Gegenprobe: Partitonsvollständigkeit; Subgraph-Konnektivität; Liste kritischer Leitungen, stündlicher Überlastungen, jährlicher Energie; Quellenvergleich 102 nur für O26-Profil. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** ZONAL-QUALITY; MD-03/13; Referenznetz, Stundengewichtung, Schwellen, Sonderzonen und Abweichungsregeln.

**Nichtkonformitätsrisiko / Testanlass:** Disconnected zone, missing bus, unaddressed congested line. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P06 — Equivalent network reduction

**Quellennachweis:** O26 §§3.8.2–3.8.3; Annex 6.1 (Draft); MA-01-Prozessmatrix P06, zugeordnete SR: MA01-SR-017, MA01-SR-018, MA01-SR-019, MA01-SR-020, MA01-SR-021, MA01-SR-022.

1. **Fachliches Ziel und Einordnung:** Equivalent network reduction. Synchronous reference flows and seasonal/directional context.
2. **Eingangsdaten/Referenzen:** Busmap; PTDF/LODF; detailed branch flows; PST/HVDC parameters. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Optimize equivalent impedances/zero-flow corrections, N-1 capacities and mesh relations. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Äquivalenzparameter (X, f0, N-1-Caps, Mesh, HVDC, PST) aus Referenzflussvergleichen/Optimierung; Ratings vierfach nach Saison und Richtung. Nicht einfach Ratings addieren.
5. **Zulässige fachliche Freiheitsgrade:** Rechner, PTDF-Auswertung und Impedanzoptimierung frei, jedoch physikalische DC-Äquivalenz- und sechs Outputklassen erhalten. MA-01-Freiheit: Numerical implementation free if behavior compliant.
6. **Ergebnis/Weitergabe:** **reduced_grid** — Six specified output classes plus seasonal directional capacities. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P05, P04; liefert P07, P08–P13.
8. **Verifikation:** Physical reference comparison; wissenschaftliche Gegenprobe: Flow-/Impedanzfehler gegen detaillierte Orakel, PTDF/LODF und N-1; Richtung/Saison; HVDC/PST in Nullfluss und Maschengleichungen. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** ZONAL-ORACLE;CAP-ORACLE; MD-03/13/15; akzeptierte RMSE-/Kapazitätsgrenzen, Grenzfallbehandlung und Referenzfälle.

**Nichtkonformitätsrisiko / Testanlass:** Invalid equivalent topology/units; poor quality without disposition. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P07 — Zonal data disaggregation

**Quellennachweis:** O26 §3.8.4 (Draft); MA-01-Prozessmatrix P07, zugeordnete SR: MA01-SR-023.

1. **Fachliches Ziel und Einordnung:** Zonal data disaggregation. All assets and demand families resolvable to zones.
2. **Eingangsdaten/Referenzen:** PEMMDB, DFT, PECD and grid asset-to-zone mapping. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Reconcile spatial allocation and generation profile sources. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Aggregation über Zonen muss Summe von Referenztechnologien/Kapazitäten erhalten, sofern die ursprüngliche Bilanzgröße additiv ist; Quellprofil/Netzanschlusspunkte werden nicht vermischt.
5. **Zulässige fachliche Freiheitsgrade:** Spatial ETL frei, mit dokumentiertem Mapping und physikalisch dimensionsrichtiger Reaggregation. MA-01-Freiheit: Data transformation technology free.
6. **Ergebnis/Weitergabe:** **zonal_market_data** — Loads, technology capacities and profiles by IoSN zone. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P03, P06; liefert P08.
8. **Verifikation:** Reaggregation & spot checks; wissenschaftliche Gegenprobe: Aggregation zurück auf Ursprungsraum; Erzeugungsvolumen, Leistung, Profile, fest/flexibel, thermische Aggregate separat prüfen. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** ALLOC-TOLERANCE; MD-11/12; zonale Übertragungsregeln, Konfliktpriorität Netz vs PECD und tolerierbare Restfehler.

**Nichtkonformitätsrisiko / Testanlass:** Unaccounted capacity/load, profile mismatch. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P08 — Coupled model construction

**Quellennachweis:** O26 §§3.3,3.6,4.1,4.3,4.4 (Draft); MA-01-Prozessmatrix P08, zugeordnete SR: MA01-SR-007, MA01-SR-008, MA01-SR-039, MA01-SR-041, MA01-SR-042, MA01-SR-050.

1. **Fachliches Ziel und Einordnung:** Coupled model construction. Scenario-consistent H2 infrastructure exogenous.
2. **Eingangsdaten/Referenzen:** Zonal Strom/H2, storage, hydro, P2G and DSR. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Hydrogen dispatch/sector conversion, five hydro classes, DSR participation semantics. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Getrennte Strom- und H2-Flussbilanzen, Wirkungsgrade und Energiereservoir-Zustände; exogener H2-Netzausbau. Hydro fünf Betriebsformen; implizit vs explizit DSR.
5. **Zulässige fachliche Freiheitsgrade:** Native Komponentenwahl (Knoten/Port/Branch/Constraint), Variablensplitting frei, falls Projektion der zulässigen Betriebsmenge gleich ist. MA-01-Freiheit: Native component decomposition free.
6. **Ergebnis/Weitergabe:** **model_semantics** — Sectors, ports, conversion, balances, constraints. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P03/P06/P07 und P01; liefert P10–P15.
8. **Verifikation:** Structural and balance tests; wissenschaftliche Gegenprobe: Kleines Strom-H2-Kopplungsorakel, Energiebilanz inkl. Elektrolyse/Rückverstromung; Hydro-/DSR-Einzelfälle, Null-Energie-Erzeugung ausschließen. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** H2-DETAIL;DSR-SEMANTICS; MD-06/10/16; P2G-/H2-Einheiten, Konversionsfaktoren, Speicher-Endzustände, DSR-Restbedingungen.

**Nichtkonformitätsrisiko / Testanlass:** Missing conversion or unauthorized H2 investment variables. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P09 — Candidate and economic preparation

**Quellennachweis:** O26 §§3.10–3.11,4.5–4.6 (Draft); MA-01-Prozessmatrix P09, zugeordnete SR: MA01-SR-018, MA01-SR-024, MA01-SR-028, MA01-SR-034, MA01-SR-035, MA01-SR-036, MA01-SR-037, MA01-SR-038, MA01-SR-043, MA01-SR-044.

1. **Fachliches Ziel und Einordnung:** Candidate and economic preparation. Study-year and stage applicability; source-vintage and directional NTC.
2. **Eingangsdaten/Referenzen:** Real/conceptual/theoretical transmission candidates, storage, cost sets. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Model every transmission expansion as controllable DC market link; cost units WACC and limits. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Kandidaten-Investitionen 0<=x<=Xmax als LP-Kapazitäten; für Transmission *steuerbare DC-Marktlinks* mit gerichtetem NTC-Effekt, ohne Kirchhoff-Zwang des physischen Bestandsnetzes. Kostenwerte tragen Währung und Preisjahr.
5. **Zulässige fachliche Freiheitsgrade:** Interne Kandidatenrepräsentation und Kostenbewertungstool frei; gleiche NTC-Richtungs-/Kostensemantik verpflichtend nachvollziehbar. MA-01-Freiheit: Internal representation free subject to link semantics.
6. **Ergebnis/Weitergabe:** **candidate_cost_register** — Class, endpoints, directional NTC, limit, costs and provenance. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P04/P06/P08 und Kandidatenkosten; liefert P10/P11/P12.
8. **Verifikation:** Schema and economics audit; wissenschaftliche Gegenprobe: Kandidatentyp vs Stufe, NTC+/- und Standorte/RDFID, CAPEX/OPEX, Internal-Reinforcement-Abgleich; jährliche Kosten und Barwert nicht vermischen. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** CAND-MAPPING;ECON-DISCOUNT; MD-02/05/06/09/11; Kosten- und Offshorefaktoren, Cashflow/Discount/Annuity und Technologieparameter.

**Nichtkonformitätsrisiko / Testanlass:** AC candidate mistakenly included in meshed branches, missing costs. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P10 — Real-candidate LP expansion

**Quellennachweis:** O26 §§3.1.1,3.9–3.10 (Draft); MA-01-Prozessmatrix P10, zugeordnete SR: MA01-SR-003, MA01-SR-024, MA01-SR-027, MA01-SR-028, MA01-SR-029, MA01-SR-030, MA01-SR-031, MA01-SR-035.

1. **Fachliches Ziel und Einordnung:** Real-candidate LP expansion. Primary LF mode; year-specific runs.
2. **Eingangsdaten/Referenzen:** P08 model, P09 eligible real candidates; weather weights. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** First LP stage: real onshore/offshore candidates, shared investment x across weather. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Für jedes y eigenes LF-LP mit realen On-/Offshore-Kandidaten, wetterfallübergreifendem x_y, Zielfunktion I+sum_c pi_c Qc. Elektrische Maschenregeln vorhanden; interne Interzonenlimits entfallen.
5. **Zulässige fachliche Freiheitsgrade:** LP-Löser, Variableneliminierung, Dekomposition frei, falls primal/dual und Zielfunktionssemantik gleich. MA-01-Freiheit: LP solver/modeling language free.
6. **Ergebnis/Weitergabe:** **stage1_portfolio** — Bounded real investments and objective decomposition. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P08 + P09; liefert P11.
8. **Verifikation:** Generated LP + optimum witness; wissenschaftliche Gegenprobe: Stufenklassen, LP-Zulässigkeit, x_y über C identisch, Abschaltung nur interner Ratings, exemplarischer Optimumswitness. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** CAND-STAGES;LF-SEMANTICS; MD-02/07/08/09/15; genaue Kandidaten- und Kosten-, LF-Modus-/Stage-Auswahl.

**Nichtkonformitätsrisiko / Testanlass:** Wrong stage set, scenario-specific x, wrong flow interpretation. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P11 — Remaining/conceptual/theoretical LP expansion

**Quellennachweis:** O26 §3.10 (Draft); MA-01-Prozessmatrix P11, zugeordnete SR: MA01-SR-003, MA01-SR-024, MA01-SR-027, MA01-SR-028, MA01-SR-029, MA01-SR-030, MA01-SR-032, MA01-SR-035.

1. **Fachliches Ziel und Einordnung:** Remaining/conceptual/theoretical LP expansion. Previously chosen candidate impacts carried forward.
2. **Eingangsdaten/Referenzen:** Stage 1 results, remaining and conceptual/theoretical candidates. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Second LP stage, correct candidate set, no double counting. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Zweite LF-LP-Stufe erhält reale Rest- und konzeptionelle Onshore-/theoretische Offshoreoptionen und rechnet Stufe-1-Portfolio ohne Doppelzählung an; exakte Übergabefunktion nicht bestimmt.
5. **Zulässige fachliche Freiheitsgrade:** Workflow-/Solvertechnik frei; keine Neuinterpretation als zeitliche Mehrjahresinvestition. MA-01-Freiheit: Solver free within LP and carry-forward semantics.
6. **Ergebnis/Weitergabe:** **stage2_portfolio** — Incremental/final expansion by candidate. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P10 und P09; liefert P12.
8. **Verifikation:** Stage transition/oracle; wissenschaftliche Gegenprobe: Orakel für Teilinvestition aus Stufe 1, Restkapazitätsgrenze, verbindliche Basiszustandsrechnung und Kosten-Doppelerfassung. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** CAND-STAGES; MD-07/02/09; explizite Stage-1/2-Transition und Filterregel TBD.

**Nichtkonformitätsrisiko / Testanlass:** Ignoring stage1 state, incorrect availability. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P12 — Storage expansion for 2040/2050

**Quellennachweis:** O26 §§3.10,4.5.1 (Draft); MA-01-Prozessmatrix P12, zugeordnete SR: MA01-SR-003, MA01-SR-024, MA01-SR-027, MA01-SR-028, MA01-SR-029, MA01-SR-030, MA01-SR-033, MA01-SR-034.

1. **Fachliches Ziel und Einordnung:** Storage expansion for 2040/2050. No 2035 endogenous storage additions.
2. **Eingangsdaten/Referenzen:** Stage 2 portfolio, storage durations, caps and costs. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Linear separate storage stage bounded by country trajectories. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Eigene Speicher-LP-Entscheidungsstufe für y∈{2040,2050}, nicht 2035; Speicherkapazitäten und Energie über Leistungs-/Dauerrelation und Ländertrajektorien begrenzt.
5. **Zulässige fachliche Freiheitsgrade:** Speicherzustandsrepräsentation, LP-Implementierung und Klassencodierung frei, sofern Klasse/Zeithorizont/Kosten erhalten. MA-01-Freiheit: Representation and LP implementation free.
6. **Ergebnis/Weitergabe:** **storage_portfolio** — Generic storage need, not battery-project prescription. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P11/P09; liefert P13–P15.
8. **Verifikation:** Stage/horizon tests; wissenschaftliche Gegenprobe: Kein endogener x_storage(2035); mindestens zwei Profile, nationale Ausbaulimits, intertemporale Energieerhaltung. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** STORAGE-DETAIL; MD-06/07/15; Klassenparameter, Batteriespeicherproxy und Stage-Übernahme.

**Nichtkonformitätsrisiko / Testanlass:** 2035 storage decision or exceeded trajectory. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P13 — Internal grid dispatch comparison

**Quellennachweis:** O26 §§3.9,4.1 (Draft); MA-01-Prozessmatrix P13, zugeordnete SR: MA01-SR-025.

1. **Fachliches Ziel und Einordnung:** Internal grid dispatch comparison. Must preserve baseline identity.
2. **Eingangsdaten/Referenzen:** LF investment result and internal grid representation. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Dispatch comparison with/without IoSN portfolio for internal network effect. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Gepaarte Dispatchläufe mit gleicher Eingabe, Wetterfällen und inneren N-1-Ratings, nur definierter Portfolioeingriff variiert; Unterschiede sind signierte Deltas, nicht automatisch KPI nach Formel.
5. **Zulässige fachliche Freiheitsgrade:** Betriebsoptimierungsverfahren frei; keine Vermischung von LF-Portfolioentscheidung und internem OPF-Lauf. MA-01-Freiheit: UC/ED engine and numerical solution free.
6. **Ergebnis/Weitergabe:** **dispatch_comparison** — Cost/volume differences and run mode provenance. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P12 (mit/ohne Portfolio) und beschränktes internes Netz; liefert P16.
8. **Verifikation:** A/B dispatch witness; wissenschaftliche Gegenprobe: Paarweise Inputidentität, knappe Energie-/Kostendifferenzen und Residuen, Abgleich von Zulässigkeit/Dispatchvolumina. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** KPI-REPORT; MD-08/17/04; Referenzstatus, interner Congestion-Mapping und Kennzahlenformeln.

**Nichtkonformitätsrisiko / Testanlass:** Labeled OPF expansion as primary LF; missing comparator. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P14 — Frozen-H2 sensitivity

**Quellennachweis:** O26 §3.6 (Draft); MA-01-Prozessmatrix P14, zugeordnete SR: MA01-SR-009.

1. **Fachliches Ziel und Einordnung:** Frozen-H2 sensitivity. Correctly mapped node, hour and weather case.
2. **Eingangsdaten/Referenzen:** Pre-expansion hourly electrolyser load, base grid. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Freeze H2 dispatch/coupling as specified, solve electrical expansion sensitivity. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Freeze setzt stündlichen/zonal-/wetterindizierten elektrolytischen Betrieb auf exogen vorliegenden Prä-Expansionsvektor. Elektrisches Anpassungsproblem separat beurteilen.
5. **Zulässige fachliche Freiheitsgrade:** H2-Dispatch-Engine und Profilserialisierung frei; nicht zulässig: Freeze nur als Kostenannahme mit variablen Lasten. MA-01-Freiheit: Native H2 representation free.
6. **Ergebnis/Weitergabe:** **h2_frozen_sensitivity** — Electric-only effect with fixed H2 dispatch. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P12 und präexpansives H2-Profil; liefert P16.
8. **Verifikation:** Dispatch comparison; wissenschaftliche Gegenprobe: Werteidentität jeder fixierten Elektrolyse-Stunde/Zone/Wetter; getrennte Investition und Betriebsergebnisse. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** H2-SENS; MD-10/12; Definition Pre-Expansion, Umfang des eingefrorenen H2-Dispatches und Netzbezug.

**Nichtkonformitätsrisiko / Testanlass:** H2 not frozen or wrong baseline. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P15 — Optional OPF investment study

**Quellennachweis:** O26 §3.9 (Draft); MA-01-Prozessmatrix P15, zugeordnete SR: MA01-SR-026.

1. **Fachliches Ziel und Einordnung:** Optional OPF investment study. Explicit optional-study authorization.
2. **Eingangsdaten/Referenzen:** LF expansion portfolio, internal capacities. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** If run: OPF with candidate expansion capped by LF selected portfolio. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Optionales OPF-Expansionsproblem mit internen Kapazitätsrestriktionen; Portfolio muss auf LF-Kandidaten-/Kapazitätsauswahl begrenzt sein, keine zusätzlichen Abkürzungsausbausignale.
5. **Zulässige fachliche Freiheitsgrade:** Gleichwertige OPF-Formulierungen frei; optionaler Zweig darf nicht heimlich zum Pflichtpfad werden. MA-01-Freiheit: OPF solver/model platform free.
6. **Ergebnis/Weitergabe:** **optional_opf_result** — Separate from baseline; cap provenance. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P12 und P13; optional liefert P16.
8. **Verifikation:** Constraint inspection; wissenschaftliche Gegenprobe: Aufrufentscheid explizit; A/B Modus, Netzrestriktionen, LF-Deckel nach Komponenten, Status nicht verschleiern. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** OPF-CAP; MD-08/17; genaues Portfoliocapping, notwendige Studienfälle und Vergleichsorakel.

**Nichtkonformitätsrisiko / Testanlass:** Uncapped OPF, silent replacement of LF. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P16 — Postprocessing and needs reporting

**Quellennachweis:** O26 §§2.2,3.1.2,3.10–3.11 (Draft); MA-01-Prozessmatrix P16, zugeordnete SR: MA01-SR-001, MA01-SR-044, MA01-SR-045, MA01-SR-046.

1. **Fachliches Ziel und Einordnung:** Postprocessing and needs reporting. Defined target year, candidate and run lineage.
2. **Eingangsdaten/Referenzen:** Investments, costs, dispatch, offshore route geometry. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Filter small expansions (threshold open), publish needs not investment decisions, ONDP offshore distances/costs. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Fachlicher Need-Record: Kategorie, Y, Raum/Korridor, Richtung, Herkunft/Portfolio, Einheiten und Status; keine Projektautorisierung. Filter ist nur anzuwenden, wenn Quellregel bestimmt ist.
5. **Zulässige fachliche Freiheitsgrade:** KPI-/Berichtswerkzeug frei, nicht der semantische Unterschied Systembedarf vs Projekt. MA-01-Freiheit: Reporting tool free; KPI semantics not arbitrary.
6. **Ergebnis/Weitergabe:** **needs_register** — Identified capacity/corridor/storage opportunities, KPI and provenance. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** P10–P15 (P15 optional) und P04/P09; liefert P17.
8. **Verifikation:** Independent KPI recomputation (currently blocked); wissenschaftliche Gegenprobe: Report-Linie bis Input, Kandidat und Kosten; wo keine Formel vorliegt BLOCKED_ORACLE, kein KPI-PASS; Filter-Metadaten. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** FILTER-THRESHOLD;OUTPUT-KPI; MD-02/04/05/17; Kosten-/Offshore-/Aggregation/Kleinmengen-/Gaps-/ONDP-Formeln.

**Nichtkonformitätsrisiko / Testanlass:** Unspecified filter used as binding, KPI without formula. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.

### P17 — Independent verification and acceptance

**Quellennachweis:** O26 §5.1; D (Draft); MA-01-Prozessmatrix P17, zugeordnete SR: MA01-SR-047.

1. **Fachliches Ziel und Einordnung:** Independent verification and acceptance. Source authority, test oracles, unresolved decision register.
2. **Eingangsdaten/Referenzen:** All model inputs, generated problems, results. Quelle/Fall/Jahr/Einheit in einem auswertbaren Manifest; fehlende Daten sind nicht durch Modellannahmen aufzufüllen.
3. **Transformation/Berechnung:** Perform static/semantic/math/run review; no false ENTSO-E certification. Als MA-01-Interpretation, nicht als formell autorisierte Umsetzungsreihenfolge zu lesen.
4. **Mathematische/algorithmische Eigenschaften (SCI-DERIVED, soweit nicht explizit O26):** Risikobasierter Prüfpfad D5-A1: strukturelle Integrität ≠ mathematischer Laufbeleg ≠ externe Ownerfreigabe. Toolvergleiche brauchen gleichwertige Inputs/Orakel.
5. **Zulässige fachliche Freiheitsgrade:** Unabhängige Implementierungen (D6-A), Testorganisation und Werkzeugwahl frei; personelle Unabhängigkeit nicht simulierbar. MA-01-Freiheit: Review automation free.
6. **Ergebnis/Weitergabe:** **review_evidence** — PASS/FAIL/BLOCKED with evidence type. Status, Release-/Szenario-/Zeit-/Einheitsbezug mitliefern.
7. **Abhängigkeiten:** Alle P00–P16; nachgelagertes wissenschaftliches QA.
8. **Verifikation:** Independent R1–R5; wissenschaftliche Gegenprobe: 18 Prozessfälle, 48 SR, Source-Abdeckung, kontradiktorische LP-/Netz-/Energiebeispiele, nicht ausführbare Tests als NOT_EXECUTED/BLOCKED. **Nicht ausgeführt**, kein positives Orakel behauptet.
9. **Offene Parameter/Ownerentscheidungen (TBD):** VERIF-ORACLE;B-01; MD-01/15/17/20; unabhängiger qualifizierter Review und Quellen-/Datenfreigaben fehlen.

**Nichtkonformitätsrisiko / Testanlass:** Unrun test reported PASS, unknown source declared final. **Status:** SPECIFIED_FOR_RESEARCH / NOT_EXECUTED / OWNER_HOLD.


## 3. Abdeckung und Quellentrennung

- **18/18** Prozesse P00–P17 aus der unveränderten MA-01-Matrix verarbeitet; P00 und P17 enthalten Governance-Ableitungen, keine eigenständigen O26-Optimierungspflichten.
- **48/48 aktive** MA01-SR wurden anhand des unveränderten MA-01-Katalogs zu Prozessschritten aufgelöst. Das im Repository verwendete SR-Namensschema besitzt die Lücken SR-012 und SR-049; es werden **keine** neuen Anforderungen mit diesen IDs erfunden.
- SR-Multizuordnungen P02–P03, P05–P06, P09–P12, P06/P09 wurden expandiert, ohne bestehende SR umzuschreiben. Die vollständige SR-Einzellinienliste steht in source_and_assumption_traceability.csv.
- Ein prozessbezogener Bezug beweist **noch nicht**, dass jedes fachliche Detail mathematisch verifiziert oder implementiert wurde. P00/G1-Blocker und P17-Abnahme bleiben explizit offen.
- Fachübergreifende technische Definitionen: scientific_methodology_specification.md, mathematical_obligations.md und methodological_degrees_of_freedom.md.

**Zusatzkontrolle:** Historische H24 §7.3.2, Druckseite 42, darf für P10/LF als erläuternder Beleg zur Beibehaltung der Impedanzen bei ausgeschalteten internen Limits dienen, ist aber weder eine Freigabe noch ein neuer O26-Kapazitätswert. H24 §7.3.1, Druckseiten 36–38, darf die ungeklärte 2035-Projektreife nicht ersetzen. MD-14/MA02-CL-001 bleiben TBD.
