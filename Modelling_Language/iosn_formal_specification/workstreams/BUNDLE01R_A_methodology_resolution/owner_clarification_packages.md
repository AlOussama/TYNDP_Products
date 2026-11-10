# BUNDLE-01R A — Owner Clarification Packages (21 unresolved)

**Date:** 2026-11-10 · **No owner replies or authorization obtained.** Each row is a **decision request**, not an adopted interpretation. The machine-readable full field-level register is `decision_resolution_register.csv`. Source evidence: O26 consultation PDF (https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf), official closed consultation (https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/), 113th SDC minutes (https://eepublicdownloads.entsoe.eu/clean-documents/sdc-documents/meeting-documents/2026/260203-04-SDC_Minutes_vFinal_for_publication.pdf), and original MA01/MA02/BUNDLE01 refs.

## MD-01 — P0 / ENTSO-E IoSN Methodology Owner

- **Source:** O26 cover; consultation 26.02-03.04; MR: MA01-MR-001;MA01-MR-002;MA01-MR-003;MA01-MR-004;MA01-MR-005;MA01-MR-006;MA01-MR-007;MA01-MR-008;MA01-MR-009;MA01-MR-010;MA01-MR-011;MA01-MR-013;MA01-MR-014;MA01-MR-015;MA01-MR-016;MA01-MR-017;MA01-MR-018;MA01-MR-019;MA01-MR-020;MA01-MR-021;MA01-MR-022;MA01-MR-023;MA01-MR-024;MA01-MR-025;MA01-MR-026;MA01-MR-027;MA01-MR-028;MA01-MR-029;MA01-MR-030;MA01-MR-031;MA01-MR-032;MA01-MR-033;MA01-MR-034;MA01-MR-035;MA01-MR-036;MA01-MR-037;MA01-MR-038;MA01-MR-039;MA01-MR-040;MA01-MR-041;MA01-MR-042;MA01-MR-043;MA01-MR-044;MA01-MR-045;MA01-MR-046;MA01-MR-047;MA01-MR-048;MA01-MR-050; SR: MA01-SR-001;MA01-SR-002;MA01-SR-003;MA01-SR-004;MA01-SR-005;MA01-SR-006;MA01-SR-007;MA01-SR-008;MA01-SR-009;MA01-SR-010;MA01-SR-011;MA01-SR-013;MA01-SR-014;MA01-SR-015;MA01-SR-016;MA01-SR-017;MA01-SR-018;MA01-SR-019;MA01-SR-020;MA01-SR-021;MA01-SR-022;MA01-SR-023;MA01-SR-024;MA01-SR-025;MA01-SR-026;MA01-SR-027;MA01-SR-028;MA01-SR-029;MA01-SR-030;MA01-SR-031;MA01-SR-032;MA01-SR-033;MA01-SR-034;MA01-SR-035;MA01-SR-036;MA01-SR-037;MA01-SR-038;MA01-SR-039;MA01-SR-040;MA01-SR-041;MA01-SR-042;MA01-SR-043;MA01-SR-044;MA01-SR-045;MA01-SR-046;MA01-SR-047;MA01-SR-048;MA01-SR-050.
- **Current position and evidence:** SDC26FEB item 15.3 confirms future written approval was envisaged in February 2026; O26 title and consultation explicitly draft; NO adoption act. Existing position remains **unapproved**.
- **Decision requested:** Welche Originalfassung ist für TYNDP 2026 verbindlich; wer hat an welchem Datum welche Version und Anhänge mit welchem Gültigkeitsbeginn beschlossen?
- **Possible consequences:** Entire method-to-contract baseline; all SR and downstream oracles on source-hold.
- **Alternative interpretations (illustrative only):** A: later adopted/effective revision B supplied; B: O26 expressly adopted for IoSN 2026 as-is; C: owner-specific interim method directive. All require official sign-off, file/hash and scope.
- **Minimum acceptability:** Originaldatei; SHA-256; Release/Decision-ID; Effective Date; Scope; Errata; Sign-off. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified ENTSO-E IoSN Methodology Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-02 — P0 / Economics Owner

- **Source:** O26 §4.6 p40; broken reference; MR: MA01-MR-027;MA01-MR-043;MA01-MR-044; SR: MA01-SR-027;MA01-SR-043;MA01-SR-044.
- **Current position and evidence:** O26 §4.6 printed page 40 visually rechecked: broken cross-reference persists in verified draft. Existing position remains **unapproved**.
- **Decision requested:** Welche exakte Diskontformel, Ratenkonvention und Zeitblockaggregation zum Basisjahr 2026 sind anzusetzen?
- **Possible consequences:** NPV and discount-year cost model, numeric KPI reference and economics test.
- **Alternative interpretations (illustrative only):** A: explicit annual discounting for modeled years; B: block-aggregated year discounting; C: externally approved coefficient table. Require numerical example; no implicit selection.
- **Minimum acceptability:** Versionierte Formel; Währung/Preisjahr; numerischer Validierungsfall. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Economics Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-03 — P0 / Network Reduction Owner

- **Source:** O26 §3.8 Annex 6.1; MR: MA01-MR-013;MA01-MR-017;MA01-MR-019;MA01-MR-022; SR: MA01-SR-013;MA01-SR-017;MA01-SR-019;MA01-SR-022.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welche Referenzfälle, RMSE/LODF/N-1-Güte- und Konnektivitätsschwellen entscheiden über Akzeptanz der Reduktion?
- **Possible consequences:** Network clustering/reduction physical equivalence and reference test tolerances.
- **Alternative interpretations (illustrative only):** A: strict reference thresholds; B: graded deviations with owner exception cases. No data-independent quality PASS.
- **Minimum acceptability:** Detailliertes Testnetz; erwartete Flüsse/Kapazitäten; pass/fail-Grenzen. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Network Reduction Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-04 — P0 / Reporting/KPI Owner

- **Source:** O26 §§2.2,3.1.2,3.10; MR: MA01-MR-001;MA01-MR-045;MA01-MR-046; SR: MA01-SR-001;MA01-SR-045;MA01-SR-046.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welche exakten Systembedarfs-KPIs, Aggregationsformeln und Kleinmengenschwellen gelten verbindlich?
- **Possible consequences:** Interpretation of system needs and validation of output KPIs.
- **Alternative interpretations (illustrative only):** A: candidate-level needs; B: corridor/zone-level needs with aggregation; confirm exact KPIs, filters and multi-optima handling.
- **Minimum acceptability:** Versioniertes KPI-Dictionary; Formeln; Testwerte; Filterregel. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Reporting/KPI Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-05 — P1 / Offshore Planning Owner

- **Source:** O26 §3.11 p31; MR: MA01-MR-038; SR: MA01-SR-038.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welcher endgültige gemeinsame Offshore-Umwegfaktor innerhalb 10–15% gilt für welche Geometrien und Kosten?
- **Possible consequences:** Offshore route length and candidate cost basis.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Freigegebene Zahl; Strecken-/Kostenreferenzfall. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Offshore Planning Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-06 — P1 / Storage/Economics Owner

- **Source:** O26 §§3.10,4.5.1; MR: MA01-MR-033;MA01-MR-034; SR: MA01-SR-033;MA01-SR-034.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welche Batterieproxy-Dauern, Investitionskosten und länderspezifischen Speichertrajektorien gelten 2040/2050?
- **Possible consequences:** Battery/storage proxies, duration/constraints, costs and 2040/2050 caps.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Parameterfreigabe; MW/MWh-/Länder-/Jahr-Matrix. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Storage/Economics Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-07 — P0 / Transmission Expansion Owner

- **Source:** O26 §3.10; MR: MA01-MR-003;MA01-MR-031;MA01-MR-032; SR: MA01-SR-003;MA01-SR-031;MA01-SR-032.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Wie werden reale Teilinvestitionen aus Stufe 1 in den Restkandidatensatz von Stufe 2 übernommen?
- **Possible consequences:** Stage 1/2 feasible sets and partial investment carry-over.
- **Alternative interpretations (illustrative only):** A: fixed stage 1 asset contributions; B: residual capacities with amortized costs; require same fixture and no double count.
- **Minimum acceptability:** Stage-Transition-Regel und vollständiges Zahlenbeispiel. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Transmission Expansion Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-08 — P1 / Network Expansion Owner

- **Source:** O26 §3.9; MR: MA01-MR-024;MA01-MR-025;MA01-MR-026; SR: MA01-SR-024;MA01-SR-025;MA01-SR-026.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welche LF-Unendlichkeitsregel und welche optionalen OPF-Portfoliokappungen gelten; welcher Dispatchvergleich ist verpflichtend?
- **Possible consequences:** LF baseline versus optional OPF study and paired dispatch comparability.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** LF/OPF-Laufspezifikation und Tests. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Network Expansion Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-09 — P1 / Market/NTC Owner

- **Source:** O26 §4.5.2; MR: MA01-MR-035;MA01-MR-036; SR: MA01-SR-035;MA01-SR-036.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Wie werden AC-realistische Kandidaten auf steuerbare DC-Marktlinks mit beiden NTC-Richtungen gemappt?
- **Possible consequences:** NTC direction, controllable DC market link semantics despite physical AC.
- **Alternative interpretations (illustrative only):** A: bilateral directional NTC effect; B: multi-border direct/indirect zonal impacts. Confirm link control and cost/flow conventions.
- **Minimum acceptability:** Zonenendpunkte; NTC+/NTC−; Beispiel/Netzverstärkungskosten. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Market/NTC Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-10 — P1 / Hydrogen Owner

- **Source:** O26 §§3.3,3.6; MR: MA01-MR-007;MA01-MR-008;MA01-MR-009;MA01-MR-050; SR: MA01-SR-007;MA01-SR-008;MA01-SR-009;MA01-SR-050.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welche exogenen H2-Kapazitäten, P2G-Gleichungen und Prä-Expansion-Elektrolyse-Zeitreihen sind fixiert?
- **Possible consequences:** H2 exogenous infrastructure, sector conversion, frozen electrolysis sensitivity.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** H2-Bilanzprofil; Frozen-H2-Zuordnung; Testfall. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Hydrogen Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-11 — P0 / IoSN Input Data Owner

- **Source:** O26 §§3.4,4.1–4.4 Annex 6.2; MR: MA01-MR-004;MA01-MR-005;MA01-MR-006;MA01-MR-039;MA01-MR-040;MA01-MR-048; SR: MA01-SR-004;MA01-SR-005;MA01-SR-006;MA01-SR-039;MA01-SR-040;MA01-SR-048.
- **Current position and evidence:** SCEN26 download index now records exact official input category links; these are not consumed file hashes. Existing position remains **unapproved**.
- **Decision requested:** Welche eingefrorenen Daten-Releases von PEMMDB, PECD, DFT, Hydro, H2, Projekten sind tatsächlich vom IoSN-Run verwendet worden?
- **Possible consequences:** Source data release versions, hashes, mapping to each year/weather/scenario.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Artifact-by-artifact Manifest mit URL/Datei/Version/Hash/Owner/Lizenz. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified IoSN Input Data Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-12 — P1 / Timeseries Governance Owner

- **Source:** O26 §§3.7,4.2,4.4; MR: MA01-MR-010;MA01-MR-011;MA01-MR-040;MA01-MR-042; SR: MA01-SR-010;MA01-SR-011;MA01-SR-040;MA01-SR-042.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welche Stunden-/Zeitkonvention, Leap/DST-Regeln, fehlende Werte und Gewichtssummentoleranz gelten für bereitgestellte Wetterdaten?
- **Possible consequences:** Calendar, DST/leap conventions, time series alignment and weight tolerances.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Studienkalender, ISO-Zeitbeispiele, DQ-Toleranzen. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Timeseries Governance Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-13 — P1 / Network Clustering Owner

- **Source:** O26 §3.8 Annex 6.1; MR: MA01-MR-014;MA01-MR-015;MA01-MR-016;MA01-MR-022; SR: MA01-SR-014;MA01-SR-015;MA01-SR-016;MA01-SR-022.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Wie sind kritische Leitungen, Kontiguität, Überlastungsenergie und Cluster-Ausnahmen abzugrenzen?
- **Possible consequences:** Clustering connectivity, critical lines and reference zonal boundaries.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Referenz-Zonen/Busmap und Prüfkriterien. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Network Clustering Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-14 — P0 / Starting Grid/Offshore Owner

- **Source:** O26 §§3.4,3.5 Annex 6.2; CBA4 §2.5.1; MR: MA01-MR-005;MA01-MR-006;MA01-MR-048; SR: MA01-SR-005;MA01-SR-006;MA01-SR-048.
- **Current position and evidence:** SDC26FEB approved project portfolio update (item 15.2), not an explicit 2035 IoSN maturity-crosswalk. Existing position remains **unapproved**.
- **Decision requested:** Welche Projektreifeklassen und Länder-Offshore-Ziele gehören zur signierten 2035-Referenz?
- **Possible consequences:** Eligibility and offshore targets within 2035 starting grid.
- **Alternative interpretations (illustrative only):** A: IoSN-specific starting-grid a/b/c; B: CBA4 first-midterm a/b; C: year-specific hybrid. Require approval, never infer.
- **Minimum acceptability:** Projekt-ID+Eligibility-Datensatz mit 2035-Crosswalk; Target-Release. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Starting Grid/Offshore Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-15 — P1 / Model Verification Owner

- **Source:** O26 §§3.1.1,5.1; MR: MA01-MR-017;MA01-MR-018;MA01-MR-027;MA01-MR-028;MA01-MR-029;MA01-MR-030; SR: MA01-SR-017;MA01-SR-018;MA01-SR-027;MA01-SR-028;MA01-SR-029;MA01-SR-030.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welche numerischen Feasibility-/Optimality-/MIP-Gap- oder LP-Residualschwellen werden akzeptiert?
- **Possible consequences:** Solver/constraint residual and mathematical acceptance limits.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Solverunabhängige numerische Orakel und Toleranzen. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Model Verification Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-16 — P1 / Hydro/DFT Owner

- **Source:** O26 §§4.3,4.4; MR: MA01-MR-041;MA01-MR-042; SR: MA01-SR-041;MA01-SR-042.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Welche fünf Hydro-Klassenparameter und Trennung impliziter/expliziter DSR samt Einheiten gelten?
- **Possible consequences:** Hydro categories, energy constraints and explicit/implicit DSR.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Hydro/DSR-Mapping und dimensionierte Grenzfallfixtures. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Hydro/DFT Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-17 — P1 / Results Owner

- **Source:** O26 §§2.2,3.1.2; MR: MA01-MR-001;MA01-MR-025;MA01-MR-046; SR: MA01-SR-001;MA01-SR-025;MA01-SR-046.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Wie wird Gleichwertigkeit bei mehrfachen optimalen Portfolios beurteilt, ohne Kandidaten-IDs gleichzusetzen?
- **Possible consequences:** Economic and physical equivalence under multiple optimal portfolios.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Zulässige Äquivalenzmetriken, Toleranzen, Kosten-/Flussreferenzfälle. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Results Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-18 — P0 / Upstream Weather Data Owner

- **Source:** O26 §3.7; MR: MA01-MR-010;MA01-MR-011;MA01-MR-040; SR: MA01-SR-010;MA01-SR-011;MA01-SR-040.
- **Current position and evidence:** O26 §3.7 draft source and public PECD link; no actual selected-weather handover. Existing position remains **unapproved**.
- **Decision requested:** Wer liefert und signiert bereits ausgewählte Wetterjahr-IDs, Gewichte, Profilreferenzen und deren Version je Studienjahr?
- **Possible consequences:** Selected weather year intake only; IDs/weights/profile/provenance, no algorithm.
- **Alternative interpretations (illustrative only):** A: O26 draft weather tuples as approved received intake; B: amended owner-selected tuples. In both cases no upstream algorithm reproduction.
- **Minimum acceptability:** Weather intake manifest; Provenienz; Annahmekriterien OHNE Auswahlrekonstruktion. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Upstream Weather Data Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-19 — P2 / Upstream Weather Source Owner

- **Source:** O26 §3.7 vs Annex 6.3; MR: MA01-MR-010;MA01-MR-040;MA01-MR-012;MA01-MR-049; SR: MA01-SR-010;MA01-SR-040.
- **Current position and evidence:** O26 draft source/repo rechecked; no newly verified owner directive or parameter release. Existing position remains **unapproved**.
- **Decision requested:** Sind differierende Rohdaten-Zeitfenster für die IoSN-Inputserie relevant, und welches finale übergebene Profil gilt?
- **Possible consequences:** Resolve upstream weather source period discrepancy only as delivered input impact.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Unterschriebene Übergabe-/Profilversionsklärung; kein PCA/K-Means-Test. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Upstream Weather Source Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MD-20 — P2 / Requirements Governance Owner

- **Source:** MA01 scope; historical PR #16; MR: MA01-MR-001;MA01-MR-002;MA01-MR-003;MA01-MR-004;MA01-MR-005;MA01-MR-006;MA01-MR-007;MA01-MR-008;MA01-MR-009;MA01-MR-010;MA01-MR-011;MA01-MR-013;MA01-MR-014;MA01-MR-015;MA01-MR-016;MA01-MR-017;MA01-MR-018;MA01-MR-019;MA01-MR-020;MA01-MR-021;MA01-MR-022;MA01-MR-023;MA01-MR-024;MA01-MR-025;MA01-MR-026;MA01-MR-027;MA01-MR-028;MA01-MR-029;MA01-MR-030;MA01-MR-031;MA01-MR-032;MA01-MR-033;MA01-MR-034;MA01-MR-035;MA01-MR-036;MA01-MR-037;MA01-MR-038;MA01-MR-039;MA01-MR-040;MA01-MR-041;MA01-MR-042;MA01-MR-043;MA01-MR-044;MA01-MR-045;MA01-MR-046;MA01-MR-047;MA01-MR-048;MA01-MR-050; SR: MA01-SR-001;MA01-SR-002;MA01-SR-003;MA01-SR-004;MA01-SR-005;MA01-SR-006;MA01-SR-007;MA01-SR-008;MA01-SR-009;MA01-SR-010;MA01-SR-011;MA01-SR-013;MA01-SR-014;MA01-SR-015;MA01-SR-016;MA01-SR-017;MA01-SR-018;MA01-SR-019;MA01-SR-020;MA01-SR-021;MA01-SR-022;MA01-SR-023;MA01-SR-024;MA01-SR-025;MA01-SR-026;MA01-SR-027;MA01-SR-028;MA01-SR-029;MA01-SR-030;MA01-SR-031;MA01-SR-032;MA01-SR-033;MA01-SR-034;MA01-SR-035;MA01-SR-036;MA01-SR-037;MA01-SR-038;MA01-SR-039;MA01-SR-040;MA01-SR-041;MA01-SR-042;MA01-SR-043;MA01-SR-044;MA01-SR-045;MA01-SR-046;MA01-SR-047;MA01-SR-048;MA01-SR-050.
- **Current position and evidence:** PR16–PR21 open draft; no owner review submissions/comments verified as of this check. Existing position remains **unapproved**.
- **Decision requested:** Sind sämtliche alten Research-SR/PoC/ADR als nichtaktive Artefakte markiert, ohne daraus IoSN-Contractpflichten abzuleiten?
- **Possible consequences:** Avoid accidental reinstatement of legacy PR16 requirements.
- **Alternative interpretations (illustrative only):** Owner to provide the exact applicable rule, exception scope, input/output grain, time/currency/units as applicable, and at least one discriminating test case. No default proposed.
- **Minimum acceptability:** Scope-Freigabe; Legacy-Migration-Matrix; MA01-only active IDs. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Requirements Governance Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

## MA02-CL-001 — P0 / Starting Grid Owner + IoSN Methodology Owner

- **Source:** O26 §3.4 pp16–17 vs CBA4 §2.5.1 p15; MR: MA01-MR-005;MA01-MR-048; SR: MA01-SR-005;MA01-SR-048.
- **Current position and evidence:** SDC26FEB project-list decision does not resolve separate O26 §3.4 vs CBA4 §2.5.1 interpretation. Existing position remains **unapproved**.
- **Decision requested:** Darf IoSN-2035 CBA4-Reifeklasse c berücksichtigen oder gilt first-midterm a/b; welche Study-Year-Regel hat Vorrang?
- **Possible consequences:** O26 starting-grid maturity criteria a/b/c versus CBA4 first mid-term a/b.
- **Alternative interpretations (illustrative only):** A: first mid-term a/b; B: IoSN-specific a/b/c; C: explicit project maturity override list. Not decided.
- **Minimum acceptability:** Genehmigter Jahr×Projekt×Reifeklasse-Crosswalk und Rechts-/Methodikbegründung. Include full official document/release reference, written answer, date, signatory/authority, impacted study-year scope, accepted verification oracle and change-log entry.
- **Gate:** OPEN; require qualified Starting Grid Owner + IoSN Methodology Owner decision + Methodology/Requirements owner check where normative. No `OWNER_APPROVED` before signed response.

