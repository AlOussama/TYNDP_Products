# ML-C05 — Verification Status and Failure Test Cases

**2026-11-12 · NONNORMATIVE TEST DESIGN, NOT EXECUTED · ML-R00 PR #32, commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2 · G1 = BLOCKED.**

## 1. Baseline coverage and test semantics

This catalogue is derived by parsing the **actual ML-R04 requirements_verification_matrix.csv** at the pinned ML-R00 commit, not by renumbering or substituting requirements. Exactly **48 unique provisional active MA01-SR**, 48 unique primary R04-T-SR-NNN tests, **33 tier A / 12 tier B / 3 tier C**. Sparse SR numbering remains intact: **SR-012 and SR-049 do not exist** in the active 48. The proposed D4 deep-equivalence trigger SR IDs are **017, 018, 019, 027, 029, 035**.

**Critical test status fact:** Every one of these **48 productive native tool-run tests** currently remains **NOT_EXECUTED**. The negative mutations and scenarios in this document are **designs with expected dispositions**, not executed or certified results. Earlier R04-C01–C10 synthetic arithmetic outcomes are separate source-workstream evidence and must not be represented as a native tool PASS here.

The table includes the source test ID, targeted V layers, *highest* planned depth (not a substitute for the full list in R04 CSV), falsifiable assertion (source text), and **new proposed negative mutant**. Mutants exercise detection power; catching them does not by itself certify a correct implementation.

## 2. Complete 48-SR coverage matrix

| Provisional SR | Process | Proposed tier | V layers | Highest planned D | Primary test ID | Falsifiable assertion (ML-R04 source) | Proposed incorrect-model mutant |
|---|---|---|---|---|---|---|---|
| MA01-SR-001 | P16 | A | V2 V5 V6 | D2 | R04-T-SR-001 | Systembedarf und Projektstatus explizit verschieden; kein automatisches Bau-Freigabefeld aus Optimierungsergebnissen. | Systembedarf als genehmigtes Bauprojekt exportiert |
| MA01-SR-002 | P01 | C | V1 V2 V6 | D1 | R04-T-SR-002 | Läufe nur mit Studienjahren 2035/2040/2050 und separaten Run-IDs; kein 2030-IoSN-Lauf. | unzulässiges Studienjahr 2030 oder Cross-Year-Lauf |
| MA01-SR-003 | P10–P12 | A | V2 V3 V4 V6 | D3 | R04-T-SR-003 | LP-Sequenz und Start-/Endzustand je Zieljahr; keine unbestätigte Investitionsverkettung. | LP-Stufen ohne getrennte Jahres-/Endzustände |
| MA01-SR-004 | P01–P03 | B | V1 V2 V6 | D1 | R04-T-SR-004 | Jede eingelesene Referenzmenge trägt Source-Release, Zieljahr, native Einheit und nachgerechnete Einheitenkonversion. | Quellrelease/Unit-Konversion fehlt |
| MA01-SR-005 | P04 | B | V1 V2 V6 | D1 | R04-T-SR-005 | 2035-Startnetz enthält nur projektspezifisch zulässige, vollständig identifizierte Maßnahmen aus dem Referenzstand. | nicht zulässiges 2025/2035-Startnetzprojekt hinzugefügt |
| MA01-SR-006 | P04 | B | V1 V2 V3 V6 | D3 | R04-T-SR-006 | Offshore-Ziele sind exogen fixiert; keine unzulässige Offshore-Baseline-Entscheidungsvariable. | exogene Offshore-Baseline als Entscheidungsvariable |
| MA01-SR-007 | P08 | A | V1 V2 V3 V4 V6 | D3 | R04-T-SR-007 | Jede Umwandlung bilanziert Strom und H2 auf expliziter Energiebasis und mit konsistentem Wirkungsgrad. | H2-MWh mit Elektro-MWh ohne η gleichgesetzt |
| MA01-SR-008 | P08 | B | V2 V3 V6 | D3 | R04-T-SR-008 | H2-Pipeline-Investitionen sind in der Stromausbauoptimierung exogen, nicht frei entscheidbar. | H2-Pipeline-Ausbau endogen gemacht |
| MA01-SR-009 | P14 | A | V1 V2 V3 V4 V5 V6 | D3 | R04-T-SR-009 | H2-Freeze-Sensitivität verwendet nachweislich identische stündliche Elektrolysewerte und einen getrennten Run. | P14-Lauf verändert eingefrorene Elektrolyselast |
| MA01-SR-010 | P02 | B | V1 V2 V6 | D1 | R04-T-SR-010 | Externe CY1–CY5-IDs je Zieljahr genau einmal und gleiche Gewichte; keine Wetterselektion im IoSN. | ungleiche CY-Gewichte zwischen 2035/2040/2050 |
| MA01-SR-011 | P02–P03 | B | V1 V2 V6 | D1 | R04-T-SR-011 | Für alle erforderlichen Wetter-/Studienjahr-/Zonen-/UTC-Schlüssel genau eine dimensionsrichtige Zeitreihe. | DST-/UTC-Offset oder Δt fehlt |
| MA01-SR-013 | P05 | A | V1 V2 V6 | D2 | R04-T-SR-013 | Zonengeographie wird gegen freizugebende gültige Zonendefinition und Knotenregister geprüft. | Zone ohne freigegebene Quelle erfunden |
| MA01-SR-014 | P05 | A | V2 V5 V6 | D2 | R04-T-SR-014 | Clustering berücksichtigt dokumentierte Engpass-/Austauschmerkmale; Entscheidungen und Ausnahmen rückrechenbar. | Clusterentscheidung ohne Engpass-/Exchange-Beleg |
| MA01-SR-015 | P05 | A | V1 V2 V3 V5 V6 | D3 | R04-T-SR-015 | Kritische Leitungen aus Überlastungsstunden und Überlastungsenergie mit Ratings und Δt rekonstruierbar. | Überlastungsenergie ohne Δt/Ratings berechnet |
| MA01-SR-016 | P05 | A | V1 V2 V3 V6 | D3 | R04-T-SR-016 | Jeder detaillierte Knoten genau einer Zone zugeordnet und je Zone induzierter Subgraph verbunden. | Cluster enthält getrennte Graphkomponenten |
| MA01-SR-017 | P06 | A | V1 V2 V3 V4 V5 V6 | D4 | R04-T-SR-017 | Reduktionsimpedanz und Referenzflusskorrektur werden auf Referenzgraph und Cut-Flüsse rückgerechnet. | beliebige Impedanz trotz gleichem Cut-Injection-Wert |
| MA01-SR-018 | P06/P09 | A | V2 V3 V4 V6 | D4 | R04-T-SR-018 | Physikalische AC-Branches erfüllen DC-Winkel-/Zyklusgesetze; Marktlinks sind von KVL ausgenommen. | physische Masche nur mit KCL, ohne KVL |
| MA01-SR-019 | P06 | A | V1 V2 V3 V4 V5 V6 | D4 | R04-T-SR-019 | N-1-Äquivalenzkapazitäten stammen aus bezeichneter LODF-/Outage-Basis, nicht aus freier Skalierung. | N−1-Kapazität ohne LODF/Outage-Referenz |
| MA01-SR-020 | P06 | A | V1 V2 V6 | D2 | R04-T-SR-020 | Pro verbindlicher Verbindung sind Sommer/Winter mal beide Richtungen vollständig und getrennt vorhanden. | Sommer-Rückrichtungskapazität fehlt |
| MA01-SR-021 | P06 | A | V1 V2 V6 | D2 | R04-T-SR-021 | Sechs Reduktions-Ausgabeklassen vorhanden: No-load; Mesh; HVDC; Capacity; Impedance; PST. | PST-/HVDC-Ausgabeklasse still ausgelassen |
| MA01-SR-022 | P05–P06 | A | V2 V4 V5 V6 | D2 | R04-T-SR-022 | Fluss-RMSE und Sicherheitskapazitätsabweichung aus identischen Referenzfällen; Grenzwert ungeklärt = BLOCKED. | RMSE ohne identischen Reference Case oder Schwelle erfunden |
| MA01-SR-023 | P07 | A | V1 V2 V5 V6 | D2 | R04-T-SR-023 | Zonale Datenallokation konserviert definierte physikalische Größen in richtigen Achsen ohne Doppelzählung. | räumliche Disaggregation verdoppelt Last |
| MA01-SR-024 | P09–P12 | A | V2 V3 V4 V6 | D3 | R04-T-SR-024 | Primäre LF-Expansion: KVL aktiv und ausdrücklich zu entfernende Interzonenkapazitätsschranken inaktiv. | LF begrenzt verbotenerweise Interzonen-Transfer |
| MA01-SR-025 | P13 | B | V2 V3 V4 V5 V6 | D3 | R04-T-SR-025 | Dispatch mit/ohne LF-Portfolio nutzt identische Exogene, getrennte Netzrestriktionen und gekennzeichnete KPIs. | mit/ohne-Portfolio vergleicht unterschiedliche Exogene |
| MA01-SR-026 | P15 | A | V2 V3 V4 V6 | D3 | R04-T-SR-026 | Optionaler OPF nur bei aktiviertem Branch; jede investierbare OPF-Kandidatenkapazität ≤ LF-Vorportfolio. | P15 aktiv; OPF-Kandidat über LF-Limit |
| MA01-SR-027 | P10–P12 | A | V1 V2 V3 V4 V6 | D4 | R04-T-SR-027 | Ziel enthält CAPEX plus ∑ CY-Gewicht×(OPEX+VoLL×ENS); Kosteneinheiten, Δt, Diskontfaktor separat. | CY-Gewicht, ENS oder CAPEX aus Ziel vergessen |
| MA01-SR-028 | P09–P12 | A | V1 V2 V3 V4 V6 | D3 | R04-T-SR-028 | Stromknotenbilanzen, Betriebslimits und tatsächlich geltende Policies je Zeitfall ohne Auslassung. | Knotenbilanz oder Policy-Zeilen fehlen |
| MA01-SR-029 | P10–P12 | A | V2 V3 V4 V6 | D4 | R04-T-SR-029 | Ein Investitionsvektor je Zieljahr über alle fünf Wetterfälle; kein freier CY-indexierter First-Stage-Parameter. | Investitionsvariable unabhängig je CY |
| MA01-SR-030 | P10–P12 | A | V1 V3 V4 V6 | D3 | R04-T-SR-030 | Für jedes investierbare Asset 0≤x≤spezifisches Xmax; kontinuierliche LP-Freiheit. | x negativ oder über Xmax |
| MA01-SR-031 | P10 | A | V2 V3 V4 V6 | D3 | R04-T-SR-031 | Stage 1 enthält nur methodisch zugelassene reale Kandidaten und keine anderen Ausbauentscheidungen. | konzeptioneller Kandidat schon in Stufe 1 |
| MA01-SR-032 | P11 | A | V2 V3 V4 V6 | D3 | R04-T-SR-032 | Stage 2 übernimmt Stage-1-Investition eindeutig und begrenzt die verbleibende Kandidatenmenge. | Stage-1-Kapazität oder Kosten doppelt |
| MA01-SR-033 | P12 | A | V1 V2 V3 V6 | D3 | R04-T-SR-033 | 2035 kein endogener Speicherausbau; 2040/2050 nur innerhalb Kandidaten-/Ländergrenzen. | 2035 endogener Speicherausbau freigegeben |
| MA01-SR-034 | P09/P12 | A | V1 V2 V3 V4 V6 | D3 | R04-T-SR-034 | Zwei unterscheidbare Speicherproxy-Klassen mit SoC-Gleichungen, Leistungen, Energie und Dauer. | zweite Speicherdauer fehlt / SOC ohne Δt |
| MA01-SR-035 | P09–P11 | A | V2 V3 V4 V6 | D4 | R04-T-SR-035 | Übertragungskandidaten sind regelbare DC-Marktlinks auch bei AC-Material; nicht in Kirchhoff-Zykluszwang. | AC-Technologiekandidat als physische KVL-Branch |
| MA01-SR-036 | P09 | B | V1 V2 V3 V6 | D3 | R04-T-SR-036 | NTC+/NTC− und Kandidaten-CAPEX erhalten eindeutige Richtung, Zone und ID auch bei asymmetrischem Zuwachs. | NTC +/− zusammengelegt oder CAPEX-ID verloren |
| MA01-SR-037 | P09 | C | V1 V2 V6 | D1 | R04-T-SR-037 | Offshore-VSC-Technologie und source-spezifische Preisannahme sind versioniert und im Modell zugeordnet. | VSC-Costannahme ohne Source-Version |
| MA01-SR-038 | P09 | B | V1 V2 V3 V6 | D3 | R04-T-SR-038 | Umwegfaktor wird als unbekannter Owner-Parameter innerhalb veröffentlichter Bandbreite geführt, kein erfundener Punktwert. | unfreigegebener Umwegfaktor als Default eingesetzt |
| MA01-SR-039 | P01/P08 | B | V1 V2 V6 | D1 | R04-T-SR-039 | PEMMDB-Referenzen mit Szenario-/Studienjahr-/Anlagen-/Version-IDs ohne verdeckte Quellenmischung. | PEMMDB-Szenarien ohne Quell-/Jahres-Trennung gemischt |
| MA01-SR-040 | P02–P03 | B | V1 V2 V6 | D1 | R04-T-SR-040 | PECD-Klimareihen werden als fertig gelieferte externe Daten verarbeitet, nicht als eigene Wetterwahl produziert. | PECD-Wetterwahl erneut innerhalb IoSN ausgeführt |
| MA01-SR-041 | P08 | A | V1 V2 V3 V4 V6 | D3 | R04-T-SR-041 | Fünf Hydroressourcenklassen sind unterscheidbar, mit jeweils adäquaten zeitlichen Bilanzen. | Hydroklasse oder zeitliche Bilanz fehlt |
| MA01-SR-042 | P03/P08 | A | V1 V2 V3 V4 V6 | D3 | R04-T-SR-042 | DFT inklusive EV und HP passt zur UTC-Zeitachse; implizite DSR nicht fälschlich nochmals als explizite Flexibilität. | DFT-Flexibilität durch DSR doppelt gezählt |
| MA01-SR-043 | P09 | A | V1 V2 V3 V4 V6 | D3 | R04-T-SR-043 | WACC, Lifetime, Vintage und Wirtschaftlichkeitsgruppen sind transparent und dimensionskonsistent angewendet. | WACC, Vintage oder Lifetime ohne Unit-Basis |
| MA01-SR-044 | P09/P16 | A | V1 V2 V3 V4 V5 V6 | D3 | R04-T-SR-044 | Diskontierung zum Bezugsjahr 2026 explizit und funktionsfähig; beschädigte Quellenreferenz nicht automatisch ersetzt. | falsches Bezugsjahr/Discount ohne Quellbezug |
| MA01-SR-045 | P16 | A | V1 V2 V5 V6 | D2 | R04-T-SR-045 | Filter markiert sehr kleine Investitionsanteile anhand freigegebenem Schwellwert; Rohwerte bleiben erhalten. | Rohportfolio vor genehmigtem Filter gelöscht |
| MA01-SR-046 | P16 | A | V1 V2 V4 V5 V6 | D2 | R04-T-SR-046 | Infrastructure-Gap- und ONDP-KPIs aus Rohoutputs unabhängig rekonstruierbar und fachlich gekennzeichnet. | ONDP-KPI aus unverifizierter Eigenformel |
| MA01-SR-047 | P17 | C | V2 V6 | D1 | R04-T-SR-047 | Evidenz ist unabhängig vom Tooltyp; keine Plexos/Antares-Zwangsbedingung und kein Tool als Oracle. | bestimmter Solver als einziges wissenschaftliches Oracle |
| MA01-SR-048 | P04 | B | V1 V2 V6 | D1 | R04-T-SR-048 | Startnetzprojekt-IDs und Eligibility-Status lassen sich lückenlos bis Appendix und Startnetz-Zeilen verfolgen. | Startnetzprojekt ohne Appendix/Eligibility-Link |
| MA01-SR-050 | P08 | A | V1 V2 V3 V4 V6 | D3 | R04-T-SR-050 | Mehrzoniges Strom-H2-Netz hat definierte Kopplungs-, Austausch-, Offshore-Hub- und Zonenpreissignale. | H2-Zonenkopplung oder Preis-/Offshore-Hub-Signal fehlt |

**Coverage rule:** The complete source row's oracle/owner/MD blockers, full multi-depth list, scope guard and synthetic fixture references remain in ML-R04 requirements_verification_matrix.csv. This is a *transparent overlay*, not an approval of the proposed tier, source texts or oracle. Each mutant must be tested in its own versioned fixture and recorded with exact assertion/expected status/witness; otherwise detection coverage stays NOT_EXECUTED.

## 3. Status-classification table: discriminating scenarios

The following **ST-01…ST-32 are specified expected behaviours**. No ST case has been run in this research task. They are falsifiable conformance-ontology tests, not new MA01 requirements. Scope matters: an expectation of FAIL is a *hypothetical applicable bad implementation or input*, not a FAIL of the current untested tools.

| Case | Condition and controlled fixture | Atomic expected status | Evidence/cause and anti-inference |
|---|---|---|---|
| **ST-01** | Mandatory SR-029 required; tool definitively cannot couple investment across CY | **UNSUPPORTED** | Versioned feature probe, no NOT_APPLICABLE/NOT_EXECUTED substitution |
| **ST-02** | Mandatory SR-029 feature available; scenario-coupling test not run | **NOT_EXECUTED** | Declared plan only; no executed evidence |
| **ST-03** | Generated model inspected: unlinked x(CY1) and x(CY2), valid fixed invariant | **FAIL** | D3 row/index witness; meaningful even if objective matches fixture |
| **ST-04** | Shared x or scenario copies with correctly enforced equalities, valid synthetic D3 inspection executed with accepted fixture oracle | **PASS (SYNTHETIC_FIXTURE only)** | Generated obligation witness; does not conclude production-source conformance |
| **ST-05** | Source approval/owner oracle required for a *productive claim*, but only O26 draft available | **BLOCKED** | AUTHORITY_UNCONFIRMED remains orthogonal; no owner approval |
| **ST-06** | No actual original data file and source hash only a placeholder | **BLOCKED (data qualification)** | DQ-016; unrelated synthetic schema test can still pass in own scope |
| **ST-07** | Original input actually inspected; known mandatory UTC interval malformed | **FAIL (V1 input assertion)** | Recomputed time/Δt counterexample; downstream V3 can be BLOCKED |
| **ST-08** | Run/manifest available, objective-gap acceptance tolerance necessary and TBD | **BLOCKED (V4 optimality assertion)** | Native solver tolerance is not owner acceptance |
| **ST-09** | Solver states OPTIMAL, but exported primal violates established KCL equality | **FAIL (V4 feasibility assertion)** | E04 row and E05 primal residual; V3 need not FAIL automatically |
| **ST-10** | Solver states OPTIMAL but no inspectable primal/dual/bound witness available | **BLOCKED** | Evidence incomplete; no independent optimality PASS |
| **ST-11** | Optional P15 disabled **and no invocation proved by complete run trace** | **NOT_APPLICABLE (SR-026 only)** | Condition witness and variant config; LF SR-024 remains required |
| **ST-12** | P15 flag absent; no OPF file generated | **BLOCKED (SR-026 applicability)** | Absence of output is not proof optional branch disabled |
| **ST-13** | P15 invoked, OPF cap cannot be implemented/exported by tool | **UNSUPPORTED** | Conditional becomes mandatory; feature deficit evidenced |
| **ST-14** | P15 invoked; an observed x_OPF > allowed x_LF under established cap | **FAIL** | Stage/variant E04 witness; optional does not weaken active cap |
| **ST-15** | P15 disabled; verifier also marks SR-024 LF as N/A | **FAIL (status-protocol check)** | Invalid exclusion; restore SR-024 to applicable tests |
| **ST-16** | Two independently feasible, certified optimal portfolios differ by candidate IDs only; equal physical/semantic claims | **PASS (scoped objective/feasibility assertions)** | Do not demand equal portfolio vectors; KPI-specific invariance separate |
| **ST-17** | Same nominal optimal objective but one implementation lacks physical mesh KVL | **FAIL (V3 KVL assertion)** | Same objective is not E-FEAS; requires E04 counterexample |
| **ST-18** | Cut-flow and nodal injection conserve but LODF/RMSE oracle absent | **BLOCKED (grid-equivalence claim)** | Conservation PASS on separate synthetic property cannot suffice |
| **ST-19** | Synthetic CY weights [0.05,0.10,0.20,0.25,0.40] identical **by case across all years** | **PASS (synthetic D2 identity)** | Intentionally nonuniform case vector; no general 0.2 default |
| **ST-20** | CY vector same within each year but weights mismatch across 2035 and 2040 | **FAIL (synthetic weight-identity check)** | Proves intended cross-year equality sensitivity |
| **ST-21** | Tool requires every weather weight to be 0.2 despite valid nonuniform synthetic D2 fixture | **FAIL (synthetic property check)** | Distinguish D2 weather from project D4 UTC |
| **ST-22** | Published expected ENS omits valid Δt or actual w(c), arithmetic replay is executable | **FAIL (V5 arithmetic assertion)** | Independent E07 recomputation with units |
| **ST-23** | KPI formula/filter owner definition is TBD; raw outputs are available | **BLOCKED (V5 approved KPI assertion)** | Preserve E06; metric FORMULA_TBD/null, no invented value |
| **ST-24** | Technical R02-like schema validator reports PASS, no E04 native generator execution | **NOT_EXECUTED (native model test)** | Prior schema PASS kept only on C-STRUCT scope |
| **ST-25** | Required function present but no E04 export because inspection capability proved absent | **UNSUPPORTED (required inspectability)** | Distinguish absent feature from missing collection |
| **ST-26** | E04 export is temporarily not collected, capability unknown | **BLOCKED** | No unsupported claim without proof; complete evidence required |
| **ST-27** | A valid FAIL has also an unresolved unrelated oracle in same claim | **FAIL (display headline)** | Preserve individual FAIL and BLOCKED status counts/IDs |
| **ST-28** | 47 applicable tests PASS and one mandatory test NOT_EXECUTED | **NOT_EXECUTED (display headline)** | No C-FULL claim despite favorable other tests |
| **ST-29** | Only optional tests exist and all are legitimately excluded | **NOT_APPLICABLE + EMPTY_SCOPE** | No universal PASS due to empty applicable set |
| **ST-30** | Historical PASS reused after changed original input hash | **NOT_EXECUTED for new target** | Old PASS retained as historical; claim STALE_UNTIL_RECOMPUTED |
| **ST-31** | Same AI operator labels its adversarial review 'independent approval' | **BLOCKED (independence-dependent claim)** | Self-review recorded, qualified independent signoff missing |
| **ST-32** | All synthetic checks PASS, but program attempts automatic G1 GO | **BLOCKED (G1 gate; reject transition)** | No software-authorised governance action |

## 4. Mathematical counterexample mini-fixtures (no actual solver use)

**F-A — Nonanticipativity (SR-027/029).** Define two CY cases with equal availability of one candidate, and allow copies x_CY1, x_CY2 without equality. Construct operating demands where independent investments lower the expected objective relative to a shared x. A correct test must reject the erroneous relaxation even when another scenario coincidentally produces equal investments. V3/D3 inspect index/equality constraints; D4 can prove the equality-copy projection. No synthetic value is an actual IoSN parameter.

**F-B — DC triangle versus independent transport (SR-018/035).** In a three-bus physical AC triangle with equal nonzero susceptances and zero offsets, circulation f12=f23=f31=k ≠ 0 satisfies KCL with zero nodal injection but violates physical KVL (sum voltage angle differences cannot produce nonzero cycle circulation). A nonphysical controllable market link may contribute to KCL without AC KVL. The test must distinguish object types, not reject every link with nonzero circulation. This is an illustrative sign-normalised graph, not a reference grid.

**F-C — Weight and time (SR-010/011/027/046).** Use five *synthetic* CY weights [0.05,0.10,0.20,0.25,0.40], same vector for each of the three years, but differing by CY. For two 0.5-h intervals with 2 MW, energy is 2 MWh per case, not 4 MWh. Recompute expected energy with w and Δt; a uniform-weight assumption must be detected. Final owner calendar/acceptance tolerances remain TBD.

**F-D — Conditional OPF (SR-024/026).** When OPF is disabled with a versioned false guard and audit trail, SR-026 alone is N/A. Enable OPF and set a synthetic LF portfolio limit 3 capacity units; an OPF candidate quantity 4 violates x_OPF ≤ x_LF, therefore FAIL for the applicable cap assertion. Numbers are *synthetic-only*.

**F-E — Alternative optima (SR-001/027/046).** Minimise x_A+x_B subject to x_A+x_B≥1 and 0≤x≤1. Distinct (1,0) and (0,1) are both feasible optima. Require objective/certificate and common physical mapping, do not FAIL because the strings A/B differ. A project-specific KPI such as x_A is non-invariant and must not be claimed equal.

**F-F — Network reduction and multiple proof levels (SR-017/019/022/023).** A 50 MW injection and 50 MW cut flow can meet a conservation check while a wrong PTDF, LODF, impedance or N−1 capacity still violates the relevant electrical obligations. Positive conservation is necessary not sufficient; real original-grid and quality-oracle checks are BLOCKED/TBD.

## 5. Mutation coverage controls and acceptance of the test catalogue

Every SR's negative mutant must have (i) a versioned input/model modification, (ii) an assertion it is expected to fail, (iii) an independent reference calculation or valid contradiction, and (iv) evidence that the negative case was **actually executed** before claiming detection sensitivity. At least one key critical mutant must be detectably rejected per relevant assertion family; absence of a detector is an unresolved test-design gap, not a successful property test. Future runs require distinct results for good fixture, wrong fixture and actual tool implementation.

Acceptance rules for this **document** (not for tools): exact 48/48 unique SR and test IDs; tier split 33/12/3; no SR-012/049; six status vocabulary; explicit P15 antecedent witness; mixed-status aggregation; nonuniform cross-year CY identity; D4 collision avoided; every test remains NOT_EXECUTED in productive scope; all owner oracles/tolerances left TBD.

**Source:** ML-R04 requirements_verification_matrix.csv, test_catalogue.csv, C01–C10, failure_and_evidence_semantics.md; ML-R00 INT-01/02/03/15. No Tool A/B, original IoSN dataset or qualified reviewer evaluated here.
