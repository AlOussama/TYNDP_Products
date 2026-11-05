# MA-01 — Methodology Source Baseline

**Version:** 0.1.0 / 2026-11-05. **Status:** PROVISIONAL, NOT APPROVED. **Normative source claim:** only the cited official draft, not a final/approved methodology. **Historical branch:** research/iosn-formal-specification-2026-11-04, PR #16. **MA-01 branch:** research/iosn-ma01-requirements-baseline-2026-11-05.

## Authority and release check

- **O26** — ENTSO-E Planning Study Team/System Development Committee, *TYNDP 2026 Identification of System Needs Methodology*, **Version for Public Consultation, 25 February 2026**, 65 printed pages: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf.
- **P26** — ENTSO-E public consultation: https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/ ; open 26 February, closed 3 April 2026. A completed consultation is **not evidence of approval**. No later final/approved 2026 IoSN method was confirmed in the reviewed official results as of 2026-11-05. **BLOCKER B-01**: method owner must provide verified release/version, valid date and formal authority.
- **EXT-CBA4** — 4th ENTSO-E CBA guideline §2.5.1, referenced *by O26 §3.4* for starting-grid project eligibility: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/news/2024/entso-e_4th_CBA_Guideline_240409.pdf . This dependency is not an instruction to launch a CBA-interoperation workstream.
- **EXT-SCENARIO** — https://2026.entsos-tyndp-scenarios.eu/ for source-aligned PEMMDB/PECD/DFT/H2 datasets; individual dataset version, access rights and hashes are still **UNVERIFIED**.
- Research reports and PoC in this directory are **non-normative**, older method interpretations. The new `MA01-MR-*` / `MA01-SR-*` ID namespace is authoritative *within this draft MA-01 work package only*.

## Interpretation and classification

|Code|Meaning|
|---|---|
|O-explicit|Source makes a direct rule/statement; still conditional on draft-release acceptance|
|O-explicit-math|Mathematical formulation class/bounds explicitly published; solver/vendor remains free|
|O-descriptive|Source describes a methodology or source; derived system enforcement needs approval|
|O-conditional|Method applies only if optional branch is actually executed|
|O-open|Source notes parameter but leaves exact value/reference unresolved|
|SCOPE-EXTERNAL|The annex documents the *upstream* weather-year selection process; it creates **no** MA-01 implementation or selection-verification requirement|

## Clause-level register (stable MA01-MR IDs)

|Methodology ID|Official source and printed pages|Evidence class|Faithful methodological statement / scope|Process|Open decision|
|---|---|---|---|---|---|
| MA01-MR-001 | §§2.1–2.2 (S. 9–11) | O-explicit | IoSN identifiziert Übertragungs-, Speicher- und Offshore-Systembedarfe; keine verbindlichen Projektentscheidungen. | P16 | OUTPUT-KPI |
| MA01-MR-002 | §3.2 (S. 15) | O-explicit | Eigenständige Studienhorizonte 2035, 2040, 2050; 2030 ist kein IoSN-Zieljahr. | P01 | – |
| MA01-MR-003 | §§3.1.1, 3.10 (S. 13–14, 30) | O-explicit | Separate Expansion-Optimierungen für die drei Zieljahre; 2035-Grenznetz als Ausgangspunkt. | P10–P12 | CAND-STAGES |
| MA01-MR-004 | §§3.1.2, 4 (S. 14, 32) | O-descriptive | Szenariokonforme PEMMDB-, PECD- und Planungsdaten als Modelleingang. | P01–P03 | DATA-VERSION |
| MA01-MR-005 | §3.4; Anhang 6.2 (S. 16–17, 52–56) | O-explicit | Startnetz an Grenzen als 2035-Netz auf Basis 2025 und qualifizierter Projekte. | P04 | GRID-ELIG |
| MA01-MR-006 | §3.5 (S. 18) | O-explicit | Offshore-RES-Ziele der Mitgliedstaaten als exogene feste Größen; Offshore-Hybridprojekte im Startnetz. | P04 | OFFSHORE-TARGET |
| MA01-MR-007 | §§3.3, 3.6 (S. 15, 18) | O-explicit | Strom- und Wasserstoffbetrieb samt P2G/H2-Rückverstromung sektorgekoppelt abbilden und betreiben. | P08 | H2-DETAIL |
| MA01-MR-008 | §3.6 (S. 18) | O-descriptive | Entwicklung der H2-Übertragungsinfrastruktur ist im vorliegenden Strom-Expansionsmodell vorgegeben. | P08 | H2-DETAIL |
| MA01-MR-009 | §3.6 (S. 18) | O-explicit | Wasserstoff-Sensitivität mit eingefrorenem H2-Dispatch auf Basis stündlicher Elektrolyselast aus Prä-Expansion. | P14 | H2-SENS |
| MA01-MR-010 | §3.7 (S. 19–20) | O-explicit | Je Zieljahr drei ausgewählte Wetterfälle und Gewichte als Eingaben; IDs/Anteile sind publiziert. | P02 | SOURCE-RELEASE |
| MA01-MR-011 | §§3.7, 4.2 (S. 19, 34) | O-explicit | Klimasensitive Nachfrage, RES und Hydroprofile als mit Wetterfall verknüpfte Eingaben. | P02–P03 | TIME-AXIS |
| MA01-MR-012 | Anhang 6.3 (S. 57–62) | SCOPE-EXTERNAL | Auswahlmethode ist in der Quelle beschrieben, gehört im MA-01-Implementierungsscope jedoch ausschließlich zum externen Vorgängerprozess. | EXT | WEATHER-BOUNDARY |
| MA01-MR-013 | §3.8.1 (S. 23–27) | O-explicit-2026 | Zonale Netzabbildung für TYNDP 2026 mit 102 genannten Zonen (Tabelle 3). | P05 | ZONE-GEOGRAPHY |
| MA01-MR-014 | §3.8.1 (S. 23–24) | O-descriptive | Clustering muss kritische/engpassrelevante Leitungen, homogene Austauschrichtungen und Rechenaufwand abwägen. | P05 | ZONAL-QUALITY |
| MA01-MR-015 | Anhang 6.1 (S. 45) | O-explicit | Kritische 225/400-kV-Leitungen durch stündliche Überlastung und jährliche Überlastungsenergie identifizieren. | P05 | GRID-INPUT |
| MA01-MR-016 | §3.8.1 (S. 24) | O-descriptive | Zusammenhängende Knoten je Cluster; Größenverhältnis und PECD-Kohärenz als weitere Qualitätsaspekte. | P05 | ZONAL-QUALITY |
| MA01-MR-017 | §3.8.2; Anhang 6.1 (S. 27, 48–49) | O-explicit | Äquivalente Impedanzen und Nullbilanz-Flusskorrekturen über Fehler-minimierende Optimierung ermitteln. | P06 | ZONAL-ORACLE |
| MA01-MR-018 | §3.8.2; Anhang 6.1 (S. 27, 49) | O-explicit | Vermaschungsregeln des reduzierten Netzes unter DC-Approximation abbilden. | P06/P09 | MESH-CONVENTION |
| MA01-MR-019 | §3.8.2; Anhang 6.1 (S. 27, 49–51) | O-explicit | Äquivalente N-1-Kapazitäten mit detaillierten Lastflüssen und LODF ableiten. | P06 | CAP-ORACLE |
| MA01-MR-020 | §3.8.3 (S. 28) | O-explicit | Je Interzonenverbindung vier Kapazitätswerte: Sommer/Winter je Richtung. | P06 | CAP-ORACLE |
| MA01-MR-021 | §3.8.3 (S. 28) | O-explicit | Sechs Reduktionsoutputs: No-load-Flüsse, Maschenbeziehungen, HVDC-Einfluss, Kapazitäten, Impedanzen, PST-Einfluss. | P06 | – |
| MA01-MR-022 | Anhang 6.1 (S. 45–51) | O-descriptive | Clustering-Iterationen mit RMSE-Priorität, Kapazitätsqualität und methodischen Sonderfällen dokumentieren. | P05–P06 | ZONAL-QUALITY |
| MA01-MR-023 | §3.8.4 (S. 28–29) | O-explicit | PEMMDB/PECD-Netz- und Lastdaten zonal aufteilen und Generatorkapazitäten sowie Profile reconciliieren. | P07 | ALLOC-TOLERANCE |
| MA01-MR-024 | §3.9 (S. 29) | O-explicit | Primäre Expansion im LF-Modus mit Maschenphysik, aber unbegrenzten Interzonen-Kapazitätsgrenzen. | P09–P12 | LF-SEMANTICS |
| MA01-MR-025 | §3.9 (S. 29) | O-explicit | Dispatch mit und ohne IoSN-Portfolio zur Wirkung interner Netzengpässe. | P13 | KPI-REPORT |
| MA01-MR-026 | §3.9 (S. 29) | O-conditional | Zusätzliche OPF-Expansion ist fakultativ; wenn durchgeführt, Kandidatenportfolio durch LF-Portfolio begrenzt. | P15 | OPF-CAP |
| MA01-MR-027 | §3.1.1 (S. 12–14) | O-explicit-math | Ziel: Investitionskosten + wahrscheinlichkeitgewichtete Betriebskosten + VoLL×nicht versorgte Energie. | P10–P12 | ECON-DISCOUNT |
| MA01-MR-028 | §3.1.1 (S. 13) | O-explicit-math | Knotenleistungsbilanz, DC-Netzfluss/Kirchhoff, technische Betriebsgrenzen und Policy-Constraints. | P09–P12 | BALANCE-DETAIL |
| MA01-MR-029 | §3.1.1 (S. 12–14) | O-explicit-math | Nichtantizipativität: dieselbe Investitionsentscheidung über alle Wetterfälle je Zieljahr. | P10–P12 | – |
| MA01-MR-030 | §3.1.1 (S. 13) | O-explicit-math | Lineare Investitionskandidaten durch 0 ≤ Ausbau ≤ zulässigem Maximum begrenzt. | P10–P12 | – |
| MA01-MR-031 | §3.10 (S. 30) | O-explicit | Expansionsstufe 1 als LP über reale Onshore-/Offshore-Übertragungskandidaten. | P10 | CAND-STAGES |
| MA01-MR-032 | §3.10 (S. 30) | O-explicit | Expansionsstufe 2 als LP mit verbleibenden realen, konzeptionellen Onshore- und theoretischen Offshore-Kandidaten. | P11 | CAND-STAGES |
| MA01-MR-033 | §3.10 (S. 30) | O-explicit | Speicherausbau separat nur 2040 und 2050, 2035 exogener Szenariobestand; Ländertrajektorien begrenzen Ausbau. | P12 | STORAGE-DETAIL |
| MA01-MR-034 | §4.5.1 (S. 37) | O-explicit | Mindestens zwei Speichergrößen/-dauern; standardisierte Batterie-Modellannahme als Stellvertreter für Speicherbedarf. | P09/P12 | STORAGE-DETAIL |
| MA01-MR-035 | §4.5.2 (S. 37) | O-explicit-method | Alle Übertragungs-Investitionskandidaten unabhängig von physischer AC/DC-Technologie als steuerbare DC-Markt-Links mit NTC-Effekt. | P09–P11 | CAND-MAPPING |
| MA01-MR-036 | §4.5.2 (S. 37–38) | O-explicit | Direkte/indirekte NTC-Zuwächse, Kosten interner Verstärkung, Anschlussknoten/RDFID und Projektmetadaten. | P09 | CAND-MAPPING |
| MA01-MR-037 | §4.5.3 (S. 38–39) | O-explicit-2026 | Theoretische Offshore-Kandidaten: geographisch/regional geprüft; Standard 525-kV-VSC-HVDC 2 GW mit Tabelle-4-Kosten. | P09 | OFFSHORE-COST |
| MA01-MR-038 | §3.11 (S. 30–31) | O-explicit-open | Theoretische Offshore-Längen/Kosten mit einheitlichem Meer-Nutzungsfaktor 10–15 % erhöhen; exakter Wert offen. | P09 | SEA-FACTOR |
| MA01-MR-039 | §4.1 (S. 33–34) | O-descriptive | PEMMDB liefert Erzeugung, Speicher, DSR/P2X, fixe Austausche, technische und variable Kosten sowie Reserven. | P01/P08 | DATA-VERSION |
| MA01-MR-040 | §4.2 (S. 34) | O-descriptive | PECD v4.2-Profile für Wind, Solar, temperaturabhängige Last, Hydro als externen Dateninput nutzen. | P02–P03 | DATA-VERSION |
| MA01-MR-041 | §4.3 (S. 35) | O-explicit | Fünf Hydroklassen und zugehörige Zuflüsse, Speicher- und Pumpgrenzen unterscheiden. | P08 | HYDRO-PROFILE |
| MA01-MR-042 | §4.4 (S. 35–36) | O-explicit | DFT-Stundenlast inkl. EV/HP; implizite DSR außerhalb des Markts von expliziter industrieller DSR unterscheiden. | P03/P08 | DSR-SEMANTICS |
| MA01-MR-043 | §4.6 (S. 39–40) | O-explicit | WACC 4 % für benannte Transmission-/Batteriekandidaten; wirtschaftliche Lebensdauer 25 Jahre für Transmission. | P09 | ECON-VINTAGE |
| MA01-MR-044 | §4.6 (S. 40) | O-open | Diskontierung bis 2026 mit in Quelle beschädigter Referenz zur Blockjahreslogik. | P09/P16 | ECON-DISCOUNT |
| MA01-MR-045 | §§3.1.2, 3.10 (S. 14, 30) | O-explicit-open | Unrealistisch kleine Ausbauwerte nachgelagert filtern; Schwelle nicht genannt. | P16 | FILTER-THRESHOLD |
| MA01-MR-046 | §2.2 (S. 9–11) | O-explicit | Infrastructure-Gaps-Bericht, ONDP-Ergebnisse und Methodiktransparenz sind erwartete Outputs. | P16 | OUTPUT-KPI |
| MA01-MR-047 | §5.1 (S. 41–44) | O-descriptive | Dreiknoten-Plexos/Antares-Sanity-Check ist Beispiel der Vergleichbarkeit, keine universelle Zertifizierung. | P17 | VERIF-ORACLE |
| MA01-MR-048 | Anhang 6.2 (S. 52–56) | O-data | Publizierte Startnetz-Projektliste mit NTC-Richtungen und Status als referenzierter Datensatz. | P04 | GRID-ELIG |
| MA01-MR-049 | Anhang 6.3 (S. 57–62) | SCOPE-EXTERNAL | PCA-/K-Means-Auswahl, Kenngrößen und Kandidaten-Fenster werden nur als externe Herkunft des erhaltenen Wettermanifestes dokumentiert. | EXT | WEATHER-BOUNDARY |
| MA01-MR-050 | §3.3 (S. 15) | O-explicit | Mehrere Stromzonen je Marktzone mit zonalen Preisvariablen, H2-Zonen, Offshore-Hubs und Sektorkopplung. | P08 | H2-DETAIL |

## Required source-data baseline for already selected weather years

|Study year|Number|Externally supplied IDs and probabilities|
|---|---:|---|
|2035|3|WS032: 0.24; WS037: 0.43; WS059: 0.33|
|2040|3|WS065: 0.20; WS071: 0.40; WS077: 0.40|
|2050|3|WS091: 0.23; WS092: 0.57; WS106: 0.20|

These tuples are published in **O26 §3.7, printed pp. 19–20**. They are **example of authoritative expected data for this document revision**, not the output of an in-scope selection algorithm. Data intake validates year–ID linkage, uniqueness, finite/nonnegative weights, expected count, sum-to-one subject to approved numeric tolerance, time-series references, spatial mapping and provenance. **It does not validate why these years were selected.** A later approved source may supersede them. Do not hardwire them as timeless properties of the future language.

## Source chapter / annex coverage register

|Coverage area|Reviewed source|Disposition|
|---|---|---|
|§§1–2 Introduction / objectives|pp.7–11|In scope: study objective, outputs, non-project-decision semantics|
|§§3.1–3.3 expansion, horizons, topology|pp.12–15|In scope: objective, balances, LP structure, year-independent investment and coupling|
|§§3.4–3.6 starting grid/offshore/H2|pp.16–18|In scope: exogenous input, eligibility and H2 sensitivity|
|§3.7 weather|pp.18–20|Only **selected manifest + timeseries intake**. Selection stages excluded|
|§§3.8.1–3.8.4 clustering, reduction, data splitting|pp.21–29|In scope, including physical equivalents and output classes|
|§§3.9–3.11 LF/OPF, investments, sea use|pp.29–31|In scope; optional OPF separate, unresolved sea factor flagged|
|§§4.1–4.6 databases, candidates, economics|pp.32–40|In scope; third-party datasets and references are external dependencies|
|§§5–5.1 software/sanity example|pp.41–44|Example evidence only; no Plexos/Antares mandate for a tool-neutral contract|
|Anhang 6.1 network detail|pp.45–51|In scope, including critical-line and impedance/capacity derivation|
|Anhang 6.2 starting-grid project list|pp.52–56|In scope as source input dataset (verify release and project applicability)|
|Anhang 6.3 weather selection|pp.57–62|**External/historical only**; neither implementation nor reproduction required|
|§7 glossary|pp.63–65|Terminology reference, not a separate algorithmic obligation|

**Evidence limitation:** This is a source-grounded, chapter/subsection-and-clause inventory, not a certified full sentence-by-sentence legal extraction or a validated model. Open issues and potential missing fine-grained clauses remain review findings, not implicit defaults.

## Known official-document defects and unresolved dependencies

1. **B-01** No independently confirmed final effective methodology. Reconcile any later document *before* release.
2. **B-02** §4.6 printed p.40 contains “Error! Reference source not found.” for discounted blocks: economics cannot receive a complete acceptance oracle.
3. **B-03** §3.11 printed p.31 leaves exact uniform sea-route uplift (between 10 and 15%) to the final version.
4. **B-04** §4.5.1 p.37 defers full storage costs to a final version; minimum class specification can be described but not fixed numerically.
5. **B-05** Process parameters for zonal equivalent quality, solution acceptance and reporting KPI rules are not sufficiently closed for complete tool-independent proof.
6. **B-06** O26 §3.7 and Annex 6.3 give inconsistent ten-year climate windows; **outside selection scope** but relevant if external weather inputs are mismatched; intake must use selected dataset metadata, not infer a window.
7. **B-07** §3.9 says dispatch with/without portfolio is performed but optional OPF additional study; treat them as **different** obligations.
8. **B-08** §3.1.1 calls weighted expected-cost two-stage decision “robust”; do not silently rewrite as minimax or add generic robustness requirements.

## Evidence and handoff guard

Each ID represents a **draft O26 finding**. Only released/approved source excerpts, affirmed methodological decisions, reviewed requirement derivations and acceptance oracle definitions may become binding in successor work. No language or architecture is selected by this file.
