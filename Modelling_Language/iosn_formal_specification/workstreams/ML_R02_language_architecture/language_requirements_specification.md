# ML-R02 — Language Requirements Specification
**Stand:** 2026-11-11 | **Status:** NONNORMATIVE_RESEARCH | **Basis:** BUNDLE-01R `5c13d4d63f18d30c308997cd7a01f2977fcc6b7b`

## Forschungsgrenze und Quellenrang
Nur MA-01 `iosn_requirements_catalogue.csv` ist aktive **vorläufige** Requirements-Baseline: genau 48 SR, IDs 001–050 ohne 012/049. Diese beiden fehlenden L2-IDs gehören zu Upstream-Wetterselektion (MR-012/MR-049), die **nicht** neu implementiert wird. 18 Prozessschritte P00–P17 sind unverändert referenziert. Ursprungsquelle O26: [ENTSO-E Konsultationsfassung 25.02.2026](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf); ihre Gültigkeit bleibt unbestätigt. Jüngerer verbindlicher Methodiknachfolger derzeit **nicht verifiziert**; ältere Fassungen nicht substituierend heranziehen.

**Dokumentierter Konflikt:** O26 §§3.7/6.3 nennt 3 ausgewählte Wetterfälle je Jahr; Projektbeschluss D2 setzt **5 extern selektierte IDs CY1–CY5** je 2035/2040/2050 mit **denselben, noch unbestimmten symbolischen Gewichten**. Forschungstests benutzen D2 und markieren den O26-Dissens; sie ersetzen keine autorisierte Methodikänderung. Es gibt **keine Pflicht zur PCA/K-Means-Rekonstruktion**.

## Vollständige Forschungsabbildung MA01-SR → Sprachfähigkeiten
Sprachbedarfe sind L3/L4-Forschungshypothesen, **keine neue L2 Requirements-Baseline**. `requirements_language_crosswalk.csv` enthält alle 48 SR mit ihrem vorläufigen FR-/VN-Referenzpaar.

| Spracheigenschaft | Obligation | Exemplarische MA-01-Abdeckung | Prozesse |
|---|---|---|---|
| LR01 | Quellenautorität, Revision und Normativitätsstatus | SR-004, SR-039, SR-040, SR-047 | P00,P01 |
| LR02 | Studienjahre/Run-Identität und getrennte Untersuchungen | SR-002, SR-003 | P01,P10,P11,P12 |
| LR03 | Externe Wetterfall-IDs und symbolisch gemeinsame Gewichte | SR-010 | P02 |
| LR04 | UTC-Zeitintervalle, Datenachsen, Zonal-Zuordnung | SR-011, SR-023 | P03,P07 |
| LR05 | Input-Provenienz, Unit-/Szenario- und Dataset-Identität | SR-004, SR-039, SR-040, SR-042 | P01,P03,P08 |
| LR06 | 2035-Startnetz und feste Offshore-Referenzen | SR-005, SR-006, SR-048 | P04 |
| LR07 | Netzreduktion als referenzierte Transformation samt Güte-Oracle | SR-017, SR-019, SR-020, SR-021, SR-022 | P06 |
| LR08 | Zonen, Cluster, Leitungsengpässe, Graphinvarianten | SR-013, SR-014, SR-015, SR-016 | P05 |
| LR09 | Physikalischer DC-Lastfluss und Netzkopplung | SR-018, SR-028 | P06,P08 |
| LR10 | Steuerbare NTC-/Marktlinks und Kandidatenattribute | SR-035, SR-036, SR-037, SR-038 | P09,P10,P11 |
| LR11 | Sektorkopplung, H2, Hydro, DSR und Multicarrier-Semantik | SR-007, SR-008, SR-041, SR-042, SR-050 | P08 |
| LR12 | Stochastische LP-Obligationen, Nichtantizipation, Kosten | SR-027, SR-028, SR-029, SR-030, SR-043, SR-044 | P09,P10,P11,P12 |
| LR13 | Stufen, Rückkopplung, Dispatchvergleich und optionale OPF | SR-003, SR-024, SR-025, SR-026, SR-031, SR-032 | P10,P11,P13,P15 |
| LR14 | Speicherausbau, Speicherklassen und Horizonte | SR-033, SR-034 | P12 |
| LR15 | H2-Dispatch-Fixierung in der Sensitivität | SR-009 | P14 |
| LR16 | Systembedarfs- statt Investitionsfreigabe-Outputs | SR-001, SR-046 | P16 |
| LR17 | KPI-Formel, Diskontierung, kleine Ausbauanteile | SR-044, SR-045, SR-046 | P16 |
| LR18 | Requirement-to-Test, Evidence/Oracle, unabhängige Prüfung | SR-047 | P17 |
| LR19 | Fail-Closed und Status PASS/FAIL/BLOCKED | SR-010, SR-011, SR-017, SR-029, SR-035, SR-047 | P00,P17 |
| LR20 | Semantische Versionierung, Profilbindung, Change Impact | SR-001, SR-004, SR-029, SR-035, SR-047 | P00,P17 |

**Abdeckungsmetrik:** 48/48 aktive SR mindestens einer LR-Hypothese zugeordnet. Ein erfüllter Verweisschlüssel beweist **nicht** 48/48 formalisiert oder verifiziert. Jede LR braucht später fachlich freigegebene Semantik, Prüforacle und Evidenz.

## Minimum-Contract-Typen und wohldefinierte Semantik
1. **Identität und Status:** immutable `requirement_id`, source clause/version, obligation type (REQUIRED/CONDITIONAL/OPTIONAL), applicability, owner_status, document revision; neue IDs dürfen nicht vorgeblich alte Quelltexte überschreiben.
2. **Datenverträge:** dataset/source identity, external release/hash when real, confidentiality, carrier, physical dimension, canonical unit, spatial entity, scope (year/weather/scenario), canonical `[start_utc,end_utc)` half-open time interval, no silent timezone offsets or mixed MW/MWh.
3. **Prozesse:** typed input/output edges between P00–P17; precondition/guard, stage state, trace to method; P15 optional and only executed on explicit profile selection, prerequisite cap semantics remain OPEN; do not treat disabled as successful OPF verification.
4. **Transformationen:** input type, output type, source/reference topology, busmap, algorithm family/version, policy, reproducibility/provenance, possible reversibility/loss, oracle and tolerance status (BLOCKED if unresolved).
5. **Mathematisches Profil:** linear optimization class when source-derived; decision indices; variable bounds; objective term meaning and units; network branch-vs-market-link semantics; stochastic stage/nonanticipativity; scenario weights; admissible implementation transformations/equivalence tests, no generic 1:1-algebra mandate.
6. **Output/KPI:** product category `SYSTEM_NEED` not approved project, carrier/geography/target year/scenario aggregation, unit, denominator, aggregation/formula/version, calculation lineage, planned recomputation/test and publication state.
7. **Evidenz:** requirement→verification case→oracle→execution→evidence artifact with result `PASS/FAIL/BLOCKED/NOT_EXECUTED`, responsible reviewer and execution method. Never upgrade `PASS_STRUCTURAL` to scientific verification.

## Formale Miniobligationen (illustrativ, keine O26-Spezifikationsersetzung)
Für jedes Zieljahr $y\in\{2035,2040,2050\}$, Kandidat $c$ und den D2-Wettersatz $\Omega=\{CY1,\dots,CY5\}$:
\[
\min_{x_y}\; C_y^{\mathrm{inv}}(x_y)+\sum_{\omega\in\Omega}w_\omega Q_{y,\omega}(x_y),\quad
0\le x_{y,c}\le\overline{x}_{y,c},\quad w_{y,\omega}=w_\omega.
\]
Die Gewichte sind **Variablen-/Inputreferenzen** und nicht freigegebene Zahlen; ihre probabilistische Normalisierung $w_\omega\ge 0,\sum_\omega w_\omega=1$ ist im reinen Mikrofixture illustrativ geprüft, nicht durch Owner belegt. Investitionsentscheidungen sind für gleiches $y,c$ **nicht wetterspezifisch**: $x_{y,c,\omega}=x_{y,c}$; operative Dispatchgrößen dürfen wetterabhängig sein. Verschiedene Studienjahre bilden keine behauptete endogene Langfrist-Kopplung.

*Physikalischer reduzierter AC-Äquivalentzweig in DC-Näherung* (Richtung/Shift abhängig vom Quellprofil): $f_{\ell,t,\omega}=b_\ell(\theta_{i,t,\omega}-\theta_{j,t,\omega})+f_{\ell}^{\mathrm{ref}}$. *Ausbaukandidat als steuerbarer Marktlink:* $-NTC^-_c(x)\le q_{c,t,\omega}\le NTC^+_c(x)$, **ohne** Gleichsetzung mit Kirchhoff-DC-Zweig. Quelltyp, Trägereinheit und Referenzflusskorrektur müssen klar typisiert sein.

*Netzreduktion:* $T(G_\mathrm{detail},\operatorname{busmap},\mathrm{params},\mathrm{version})\to (G_\mathrm{red},\mathrm{metadata},\mathrm{quality})$. Sechs durch MA-01 geforderte Kategorien müssen einem versionierten Katalog zugeordnet werden; Prototyp-Labels und numerische Akzeptanzschwellen bleiben **illustrativ/nicht freigegeben**. PTDF/LODF, N-1/seasonal/directional ratings, RMSE und Güteschwellen erfordern Owner-Oracles.

## Syntax-, Semantik-, Realisierungs- und Verifikationsebenen
`syntactically_valid` → `reference_consistent` → `semantic_contract_valid` → `mathematical_implementation_conformant` → `results_replayed` → `independently_approved`. Schritte sind **nicht äquivalent**; Übergänge erfordern Evidenz. Pflichtdaten fehlen, Fachsemantik widerspricht sich oder sind kritische Oracles ungelöst, lautet Akzeptanz **BLOCKED/FAIL_CLOSED**, auch wenn eine Schema-Prüfung erfolgreich war.

## Nicht abgedeckte L3/L4-Details
Reale Wettergewichte und Datensignaturen; O26↔D2-Entscheidung; Projekt-Eignung 2035; numerischer PTDF/LODF/RMSE-Orakel; Marktlink-NTC-Richtungen; wirtschaftliche Diskontfaktoren und WACC-Gruppen; LP-Stufentransfer; Hydro/H2/DSR-Energiebasis; Speicherparameter; kleine Ausbaufilter; KPI-Formeln; optionales OPF-Cap; tatsächliche Evidenz und qualifizierter unabhängiger Reviewer. Alle bleiben explizit offen, ohne Forschungsfortschritt zu blockieren.
