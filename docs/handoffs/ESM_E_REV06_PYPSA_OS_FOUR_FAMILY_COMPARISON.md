# ESM-E REV06 — Consolidated four-family comparison: PyPSA-OS, GEMS, ANTARES, PLEXOS

Stand 2026-11-28 | CONSOLIDATED_STATIC_COMPARISON | COMPARATIVE_SELECTION_OPEN
Parent a64f14e07b5407d04c3c48f7cac3a72adea638d3; owner scope: use PyPSA-OS for the entire qualified PyPSA-based portfolio, compare against GEMS, ANTARES and PLEXOS for processes, methods, functions, sector formulation depth and use cases. No implementation, installation, solver execution, license acquisition or Main merge. All historical A–E/REV01–05 files remain unchanged. This is a decision-oriented synthesis of pinned reviews, not a second exhaustive source audit or a new numerical validation.

## 1. Candidate boundaries and sources

- PyPSA-OS = umbrella defined by owner, not a released integrated engine: PyPSA Core/Linopy, Eur/DE, Open-TYNDP, GB, USA, IEI, Earth, AT, SPICE, DESOpt-Heat, stochUC, near-optimal spaces, MGA, RESILIENT, eGon/eTraGo/eDisGo/eGo and additional screened projects from [REV05 registry](./ESM_E_PYPSA_ECOSYSTEM_REUSE_REGISTRY.csv). atlite and technology-data inherited ESM-C. Local grid, stochastic and market research modules may require different languages/versions; no double counting of capability as simultaneously available. FlexPlan, M2, detailed independent AC/gas/dynamic solvers and other non-PyPSA tools are supplementary, not native OS features; available to every family.
- GEMS = model language, model libraries, GemsPy (Linopy compilation), standalone Antares Modeler, converter paths. ANTARES = Classic operational/MC, Hybrid (uses GEMS, label shared functionality), Xpansion annual and Trajectory (separate master/recourse). These two share technology but distinct use cases. PLEXOS = proprietary integrated phases LT/PASA/MT/ST, generic documented functionality separate from actual TYNDP/ERAA configuration.
- Evidence anchors: [A normative requirements](./ESM_A_20261127/ESM_A_PLANNING_PROCESS_REQUIREMENTS.md), [B](./ESM_B_20261127/ESM_B_ANTARES_GEMS_CAPABILITY_REVIEW.md), [C](./ESM_C_PYPSA_OPEN_TYNDP_CAPABILITY_REVIEW.md), [C2](./ESM_C2_OPEN_TYNDP_DEEP_REUSE_AUDIT.md), [D](./ESM_D_DISTRIBUTION_GRID_SECTOR_COUPLING_REVIEW.md), [REV01 PLEXOS](./ESM_E_REV01_PLEXOS_SCIENTIFIC_REVIEW.md), [REV02 reverse](./ESM_E_REV02_GEMS_TO_PYPSA_CONTRACT.md), [REV03](./ESM_E_REV03_FOUR_FAMILY_COMPARISON.md), [REV04 process/analytic](./ESM_E_REV04_PROCESS_TARGETED_COMPARISON.md), [REV05 specialized OS](./ESM_E_REV05_SECTOR_AND_PYPSA_ECOSYSTEM_AUDIT.md). REV05 Pxx denotes PY registry, not REV01 PLEXOS evidence ID. All inherited code/document/use/test evidence remains scope-specific, R=0 new target-engine runs. No assumption of missing capability from absent closed source.

Companion machine-readable [requirements V4](./ESM_E_REQUIREMENTS_MATRIX_V4_PYPSA_OS.csv): 50 exact A IDs/text/class/profiles/ref/line, four candidate families (ANTARES split Classic/hybrid and X/XT; PLEXOS generic and actual), new OS reuse and REV05 registry IDs/limitations/work classes, old V2 gap/benchmark/source fields. Other three candidates use V2 cells verbatim; GEMS-to-PyPSA reverse remains separate. [Process profiles V4](./ESM_E_PROCESS_FIT_MATRIX_V4_PYPSA_OS.csv): all 16 V3 profiles, 15 source process IDs, original fields retained for provenance (historical PyPSA column explicitly named), new OS reuse scope and boundary. No selection implied by qualitative assessments.

## 2. Compare functions and mathematical methods
Legend: F = existing scoped function (code or documented application; qualify activation), M = model/adapter extension or partial reuse, E = external workflow/physical solver, U = unverified. F does not imply deployment, all-year chronology, data coverage, or acceptance. GEMS expressive equations not ready sector library; ANTARES Hybrid reuses GEMS, not independent evidence. For PLEXOS D/U from REV01/04 are docs/application (not source). For PyPSA-OS F means at least one identified member implements the named function, with integration/validation open.

| Capability / model | PyPSA-OS | GEMS | ANTARES | PLEXOS |
|---|---|---|---|---|
| LP/MILP and custom constraints | F Core/Linopy, callbacks and component APIs | F typed ports/declarative AST, GP/GM parity | F Classic specific and hybrid GEMS | F D configurable model; arbitrary variables/expressions U |
| ED, imports/ENS/spill | F Core, OET, GB | F basic | F Classic | F D/U |
| UC/min up/down/ramp/start | F Core; GB proxy vs exact distinguish | F thermal and tutorial, interpreter modes | F Classic cluster/MILP or relax, X LP recourse | F D scheduling/production; active mode U |
| Hydro/seasonal energy | F stores/inflow; year-state exact | F generic stock, time/block qual | F hydro management, classic blocks; annual exact U | F D hydro, MT/ST bridge; state closure U |
| Reserve and activation | M Core/Eur, stochUC aFRR, GB | M custom | F/modes Classic, delivery M | F D reserve; location/duration U |
| Market-to-redispatch | F scoped GB wholesale-balancing; E AC | M/E | M/E | F D transmission/bids; actual paired config U/E AC |
| Market clearing vs revenue | F ED, GB capacity auction, PPA prototype; M EVA | M revenue/repeated run | F ED; France NRAA revenue EVA U, workflow rights U | F ED and historical ERAA; new EVA rollout U |
| Endogenous single/multi-year expansion | F Core/Eur/DE/IEI | F bounds, M interperiod policy | F X/XT, Classic external | F D LT Plan; exact stages U |
| Weighted common-x LP | F Core extensive; IoSN workflow M | F GP shared variables, scenario weights/GP-GM M | F X LP-Benders | D stochastic LT; common-x exact U |
| Benders LP recourse | U general native production; research or external | F build/split; X coupling | F Xpansion | D LT decomposition does not establish LP-Benders |
| Stochastic multistage investment | M/U explicit tree; IEI myopic NOT stochastic | M explicit nonanticipativity | F XT trajectory; scope qual, not arbitrary integer recourse | D tree controls, exact investment U |
| Stochastic operational stages | F scoped stochUC old Pyomo; modern port M | M | M/H or repeated study; MC not multistage | D MT/ST scenario/stage; exact U |
| Monte Carlo availability / LOLE/EENS | M/E external, GB diagnostic not MC | M/E | F Classic MC and RAA use | F D/U PASA/ERAA; sample config U |
| CVaR, risk-aversion | F Core CVaR | M explicit LP auxiliaries | M; France national process risk policy U not Classic native CVaR | U exact risk objectives |
| Minimax robust planning | M custom Linopy | M explicit constraints | M master objective/custom | U |
| Weather robust near-optimal space | F research near-opt intersections, MGA separate; port M | M | M | U |
| NTC/DC and HVDC/PST | F Core NTC/DC/KVL and PST, OET NTC | F transport/line; M affine PST | F transport, M binding KVL | F D zonal/nodal, phase/PTDF; exact U |
| FBMC / PTDF RAM | F Core HEAD, M pinned release; domain external | M linear constraints | F binding constraints, domain external | F D PTDF/interfaces, full domain U |
| N-1 and AC security | F DC SCLOPF; E full AC/corrective | M/E | M/E | F D SCUC/N-1, full AC U/E |
| AC PF / DSO AC OPF | F Core PF and eDisGo radial scoped NC/SOC; E transmission AC-OPF | E | E | U/E |
| Stability/dynamics/gas hydraulics | E | E | E | U/E |
| Open source and QA | F source and tests; multiple incompatible envs | F model/engine code, version/interpreter gaps | F open Classic/X, scoped CI | proprietary; D LP/MPS diagnostic export/API, license/version rights U |

Mathematical distinction: deterministic ED min c*p subject to balances, technical limits and state recursion. Two-stage min c*x + sum(pi_s Q_s(x)) uses one common x and scenario-specific y_s. Ordinary LP-Benders cuts rely on LP recourse and dual validity; integer master is different from integer recourse. Multistage scenario-tree decisions need information-set nonanticipativity; perfect foresight over a scenario, myopic rolling or independent MC dispatch do not provide this. CVaR uses tail cost auxiliary threshold/excess; finite-scenario minimax minimizes worst-case cost; near-optimal intersection constrains each weather-year regret; MGA explores alternative near-optimal designs, not uncertainty guarantee. N-1, robust feasibility, probabilistic risk, numerical robustness and method compliance are separate axes. Same source data, weights, chronology, investment/vintage, bounds/integer domains, objective constants, service constraints and independent physical residuals required. Compare native GP/GM/Classic/X/OS and authorized PLEXOS LP/MPS where available; no measured scaling ranking.

## 3. Sector modelling depth
Depth L1 exogenous profile; L2 aggregate energy/stock; L3 technology/time service; L4 physical network at local or regional resolution; L5 detailed component/dynamic physics. Descriptive only, no maturity score.

| Sector / use | PyPSA-OS | GEMS | ANTARES | PLEXOS |
|---|---|---|---|---|
| EV mobility adoption | USA vehicle classes and technology investment L3; EU data adapt | generic capacity/port model extension L2 | profiles and H model | U endogenous adoption; SB26 heavy/other vehicles fixed |
| EV V1G/V2G | Eur/OET/GB fleets and tariff/throughput cost L3 | generic stock, add availability/departure/shared rating | classic load/store proxy, H GEMS | SB26 actual flexible/fixed fleets, commuter/locations, SOC/V2G L3; degradation U |
| EV local delivery | eGon/eDisGo charging events/parks and bands with AC L4; V2G local unproven | E local AC | E local AC | active SB26 not DSO, U local |
| Heat demand/supply | Eur/DE central/decentral space/water, COP, CHP, renovation, industry L3; GB thermal inertia proxy | HP/storage/RC/CHP extensions L2 | fixed loads/stock; H | SB26 hybrid HP and boiler operation L3; broad detailed heat catalogue U |
| Heat networks | DESOpt-Heat local district heat investment, temperatures, cost surrogate; eGon local data; E hydraulics | M energy network, E physics | H/E | U specific thermo-hydraulics |
| Cold | USA explicit cold bus and AC, shared reversible HP L3, atlite demand; heating COP copied, independent EER and cold store/RC extension | M cold bus/link/storage/RC | H M or load | U active explicit cold; no negative general product claim |
| H2 supply/demand | Eur/IEI/DE/OET electrolysis/SMR/CCS/caverns/turbines/industry/e-fuels L3 | basic Andromede constant-efficiency electrolyser L2; add H2 chain | H/Classic proxy | SB26 electrolysis/SMR/CCS, imports, storage, e-fuels and dedicated RES L3 |
| H2 infrastructure and imports | IEI backbone/retrofit/planned vs endogenous network; Earth/TRACE PtX; USA CH4 linepack approximation only | generic network; M retrofit & import | H/LP recourse X | documented H2 CBA/IGI/gas use; exact retrofit and gas equations U |
| Gas/H2 pressure, linepack, compressor | E physics, USA aggregate CH4 store not validated H2; IEI diameter proxy | E | E | U/E exact hydraulic scope |
| DSO aggregated | Eur LV link, eTraGo asymmetric direction upgrades coupled CAPEX | M envelopes | M binding or H | documented market wheeling not physical DSO; detailed scope U |
| DSO explicit | eGon grid/asset data, eDisGo NC/SOC branch flow with P/Q, V/I and EV/TES L4; replay/slack needed | E | E | U/E |
| Integrated TSO-DSO | eGo sequenced top-down and eTraGo static bottom-up parameters; joint T&D M/E | M/E | M/E | U/E |
| L5 dynamic electrical, hydraulic, building component | E independent solvers | E | E | U/E |

Concrete validity requirements: EV state E_t=E_prev+dt*(eta_c p_c-p_d/eta_d)-E_drive, availability, departure, shared charger, user constraints and degradation proxy. Fleet aggregation not individual schedule proof. Heat Q=COP*P and cold Q=EER*P, thermal storage and RC comfort states, reversible shared capacity and heat rejection, avoid double counting historic electricity. GB thermal inertia Store is proxy. USA cold tests read not run; cooling efficiency copies heating series. DSO radial v_i*l=P^2+Q^2, SOC inequality not AC equality; hard V/I, slack, gap, feeder mapping, P/Q and individual schedule verification. eDisGo OPF variants differ; no all-network simultaneous global optimum. H2 shared stoichiometric outputs, LHV/HHV, mass/energy, compressor, build lead times and exclusive retrofit. IEI suspicious removed_gas_cap nonassignment and USA linepack chemical-energy/pressure issue retained. No verified full dynamic/hydraulic model asserted.

## 4. Process fit (15 ESM-A IDs, 16 profiles)
The source authorities and study-specific application in REV04 are retained, especially IoSN26 consultation and ERAA method transition. Candidate prioritization is a research/reuse recommendation, not official-method approval.

| Profile | PyPSA-OS | GEMS | ANTARES | PLEXOS |
|---|---|---|---|---|
| PR01 EU SB | O24 open partial reference, O26 gaps, extend via Eur/GB/USA | explicit models + data/sector authoring | K ED/H sector models | actual SB26 use; input/rights |
| PR02 IoSN24 | Core expansion + O24 data, process extension | direct transfer model | X capacity/dispatch | documented participation, exact config U |
| PR03 IoSN26 | Core common-x/DC/IEI, O26 data and M2 separate | shared-x native declaration; weights/routing | X Benders LP + physical constraints/candidates | LT stochastic exact common-x/DC U |
| PR04 CBA electricity | O24 B1–4 partial; O26 HOLD | paired runs + indicators | documented use; indicator workflow | documented use; study/reference config U |
| PR05 H2 CBA/IGI | Eur/IEI/OET/TRACE, physical validation | multiport H2 extension | H + X LP scope | documented ENTSOG studies, hydraulics U |
| PR06-EVA | GB capacity market/PPA/ED pieces; outer revenue-risk loop missing | outer loop M | France NRAA revenue EVA U; access/process qualification | ERAA historic use, 2026 rollout exact U |
| PR06-ED | ED/UC and FB domain, MC+metrics missing | ED + external MC | Classic strong native MC, RAA U | actual ERAA U, PASA docs |
| PR07 DE SR | DE/Ariadne/IEI/eGon data and regional model | separate data pipe | separate regional data | integrated generic, actual DE method U |
| PR08 DE NEP Strom | GB market-to-redispatch, Core/DC, eGon/M2, full AC separate | DC custom, external grid | ED/binding and grid separate | nodal/SCUC D, actual NEP U |
| PR09 DE NEP Gas/H2 | IEI/DE retrofit and backbone; hydraulic external | generic multi-carrier, external | H, external | gas/H2 D/U, exact pressure method U |
| PR10 SES/LFS | Eur/DE/IEI plus USA/GB sector, robustness | custom sector library and interperiod | X/XT and H, more sector modelling | LT integrated commodity D, data/license |
| PR11 national adequacy | ED+GB market components, external sampling | external MC | France proven, German VSM distinct | ERAA reference, German VSM distinct |
| PR12 grid reserve | GB balancing, Core DC security, AC separate | custom reserve/AC | K/H ED+binding, AC | D SCUC/reserve, actual workflow U |
| PR13 stability | separate physical solver; model cuts | same | same | U/E |
| PR14 integrated DSO | eGon/eGo/eTraGo/eDisGo reuse and joint interface gap | external AC + envelopes | same + K/H | U full DSO; separate physics |
| PR15 municipal heat | DESOpt/Eur/DE/eGon + local GIS/thermal network | models+GIS extension | H+GIS external | SB26 heat not local planning; U/E |

TYNDP SB fixed scenario operation differs from free expansion. IoSN26 draft three weighted climates and common investment per target year; M2 not replaced by generic clustering. CBA PINT/TOOT, project-specific RES unlock, matched scenario/weather and reference membership, separate B1–4 and other indicator contracts. ERAA24 PLEXOS vs FR NRAA25 Antares is observed use, not controlled benchmark; revenue-based EVA transition from 2026 per implementation plan and pre/post sharing metrics and correlated outage/weather. Germany approved SR vs draft distinguish. German VSM has separate IIEM/PVSM and INTEGRAL, not equated with any arm. No claim final official 2026 study reproduction.

## 5. Use-case specific comparative priorities (H, not ranking)
| Use case | First comparison arms and reason | Decisive missing qualification |
|---|---|---|
| European integrated scenarios | PLEXOS SB actual vs OS OET/Eur; GEMS native models, ANTARES H | scenario data, identical active sectors and calendar |
| IoSN shared investment with H2/offshore | ANTARES X vs OS Core vs native GEMS; PLEXOS LT if authorized | M2/physical topology, probability, CAPEX once, dual/cuts |
| Project CBA | OS O24 vs actual Antares/PLEXOS where rights; GEMS paired ED | exact reference, indicators, RES unlock, 2026 gaps |
| Probabilistic adequacy | ANTARES/PLEXOS empirical reference, OS/GEMS research arms | same outage/weather traces, full-year state, LOLE/EENS and sharing |
| Revenue-based EVA | France ANTARES vs ERAA PLEXOS; OS GB/PPA and GEMS outer loop | method cycle, iterative plant NPV, CM and risk, stopping criterion |
| EV and HP at market level | OS OET/GB/Eur/USA vs PLEXOS SB; GEMS reusable library; ANTARES H | shared SOC/comfort, investment vs fixed fleet, availability |
| EV/HP/DSO flexibility and local grid investment | OS eGon/eDisGo/eTraGo vs all others via same physical complement | feeder P/Q/time state, disaggregation and AC witness |
| National heat/cooling transformation | OS Eur/DE/USA/DESOpt vs GEMS custom and PLEXOS; H optional | independent EER, RC, cold storage, network cost |
| H2 backbone, retrofit and PtX imports | OS IEI/DE/Eur/TRACE vs PLEXOS actual H2; GEMS/H | exclusive retrofit, pressure/compressors and mass units |
| European market FBMC and national redispatch | OS Core HEAD/GB, ANTARES binding, GEMS explicit constraints, PLEXOS D | external CNEC/GSK/RAM, AC/corrective actions |
| Risk/weather resilient long-term planning | OS CVaR/intersections vs X expected cost, GEMS custom, PLEXOS U | compare *same* risk objective, finite set, holdout and scalability |

## 6. Strengths, weaknesses and effort
PyPSA-OS: broadest observed open sector reuse, physical regional grid complements, flexible algebra, reusable data and workflow examples. Heterogeneous pins, old Pyomo and separate Julia OPF, fragmented evidence and data rights; no fully integrated OS, mature complete MC/EVA chain or general Benders proven. GEMS: modular explicit equation/port contracts, cross-interpreter representation, very attractive for new library authoring. Much sector/data/process work, two runtimes and converter parity. ANTARES: strong actual hydrothermal MC/RAA and LP-Benders/trajectory capabilities; classic rigid sector and network semantics, hybrid depends on GEMS, ordinary Benders integer recourse not exact. PLEXOS: integrated configured assets/phases, real TYNDP/ERAA use, commercial support possible; exact version, rights, pricing, formulation and API extensibility not inspected. LP/MPS diagnostic export can qualify matched cases without internal source, but actual availability unknown. No source-access penalty as feature absence. No license/cost/time or reliability ranking. Work classes W1 configure+qualify, W2 model/data/adapter work, W3 separate workflow/physical coupling, WU access blocker; not measured person-days.

GEMS ↔ PyPSA-OS: direct GEMS->GemsPy->Linopy exists (not PyPSA Network). Forward PyPSA->GEMS has subset and silent-drop risks (multiport, PST, storage, weights, UC, extra constraints and investment routing). Reverse Network not verified; restricted class adapter or custom Linopy augmentation requires exact domains, coordinates, units, clocks, objective and projected feasible-set equivalence. Reusing equation/data modules can benefit both families. No mandatory universal converter.

## 7. Decision gate and next matched benchmark
Recommendation: process-specific shortlist, keep four-family comparison open, no compulsory hybrid. A feasible minimal pilot includes prior 12 analytical oracles and REV02 reverse tests, 24–168h EV/V2G, thermal/independent EER reversible HP, H2/CH4 retrofit and DSO envelope, then full 8760h IoSN common-x and ERAA common trace samples. Measure model build and solver separately, memory, constraints/variables/nonzeros, gap, status, residuals, state/service and cost decomposition, sample error and authoring effort with same inputs. O24 published evidence not own runs; PLEXOS proprietary export/access and versioned actual study unavailable. No claim fastest or most robust numerical method. The provisional process and requirement matrices trace all source rows, preserve all blockers, do not overwrite M2 governance, and do not authorize a solver campaign or production architecture. 
