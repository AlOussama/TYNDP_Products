# ML-R02 — Independent Architecture Review (adversarial role-separated pass)
**Review-Stand:** 2026-11-11 · **Reviewed commit:** `edf8267046bcf7233316991ecf174b26fd2621f6` · **Status:** `RESEARCH_ACCEPTABLE_WITH_OPEN_FINDINGS` **nur für Draft-Forschung**, **nicht** `G1` / keine unabhängige institutionelle Freigabe.

## Identität und Unabhängigkeitsgrenze
Dies ist eine **gesondert durchgeführte Adversarial-Review-Perspektive** nach der Erstellungsphase. Sie ist **kein Review durch eine unabhängig beschäftigte natürliche Person/Organisation**; Erstellungs- und Reviewdurchlauf wurden innerhalb derselben KI-Assistenz durchgeführt. Die Anforderung an ein wirklich unabhängiges Audit und die Genehmigung bleiben unerfüllt. Keine ausdrückliche normative Autorisierung, keine abschließende Architektur-ADR.

## Gegenprüfung der Evidence-Baseline
Der tatsächlich vorliegende Commit wurde auf folgende strukturelle Invarianten geprüft:

| Prüfung | Ergebnis |
|---|---|
| baseline_ids_48 | **PASS_STRUCTURAL** |
| crosswalk_48 | **PASS_STRUCTURAL** |
| matrix_15_by_12 | **PASS_STRUCTURAL** |
| A_stages_P00_P17 | **PASS_STRUCTURAL** |
| B_stages_P00_P17 | **PASS_STRUCTURAL** |
| weight_ids_A_B | **PASS_STRUCTURAL** |
| weight_years_A_B | **PASS_STRUCTURAL** |
| symbolic_unfixed_A_B | **PASS_STRUCTURAL** |
| same_22_mutation_cases | **PASS_STRUCTURAL** |
| all_mutation_assertions_correct | **PASS_STRUCTURAL** |
| fail_closed_21_per_arch | **PASS_STRUCTURAL** |
| no_math_conformity_claim | **PASS_STRUCTURAL** |
| path_fix | **PASS_STRUCTURAL** |
| draft_only_deferred | **PASS_STRUCTURAL** |

Die 22 Tests pro Prototyp sind **21 Negativmutationen + 1 nur synthetisch strukturvalider Mikrofall**. Für beide stimmen die Testnamen und erwarteten Ausgänge überein. Die isolierten V8-Validatorfunktionen wurden bei der Härtung tatsächlich ausgeführt. **Nicht gesondert bestätigt** sind Node-Konsolenläufe, eine externe JSON-Schema-Engine oder ein unabhängiger GEMS-/mathspec-/SysML-/LinkML-Parser-Test. Die kopierten GitHub-Quelltexte bzw. Modelle sind wie angegeben auffindbar; ein `PASS_STRUCTURAL` in dieser Reviewliste bescheinigt nur eine Eigenschaft der **Dokumentation und Miniinstanz**, keine vollständige Fachformalisation.

## Adversariale Findings und Disposition
| Finding | Risiko | Status | Begründung / zwingende Folge |
|---|---|---|---|
| R02-F01 | P0 | **OPEN — normative gate** | G1 bleibt BLOCKED; O26 ist Konsultation, aktuell weder source-Owner-Entscheidung noch verbindlicher Nachfolger belegt. Keine Tool-/Sprachfreigabe. |
| R02-F02 | P0 | **OPEN — method conflict** | O26 beschreibt 3 Wetterfälle; D2 setzt 5 CY-IDs. Die Prototypen markieren den Unterschied als Forschungs-Override. Im Freigabeprofil ist Owner-Entscheid nötig. |
| R02-F03 | P0 | **OPEN — mathematical oracle** | P06-Netzreduktion ist nur typisiert (sechs **illustrative** output labels); weder Fluss-RMSE/PTDF/LODF/N-1-Oracles noch belastbare Schwellen gemessen. |
| R02-F04 | P0 | **OPEN — model realization** | Keine ausgeführten vollständigen LP-/Stufen-/Speicher-/H2-/H2-Sensitivitäts-/hydrologischen Referenzmodelle; Nichtantizipation nur Mikrofall. |
| R02-F05 | P1 | **OPEN — KPI oracle** | P16-Systembedarfsklasse semantisch unterschieden, aber KPI-Aggregation, wirtschaftliche Grenzen, Diskontierung und Publikationsfilter `TBD_OWNER`. |
| R02-F06 | P1 | **OPEN — standards conformance** | A und B nutzen eigene JS-Validatoren; JSON Schema nur Subsets, keine echte SysML-v2-/ReqIF-/LinkML-/GEMS-/mathspec-Ausführung oder Kompatibilitätszertifizierung. |
| R02-F07 | P1 | **OPEN — external data** | Synthetische Provenienz ist illustrativ; reale Dataset-SHA256, Release-Versionen, UTC-/Einheiten-/Originaldatenvalidierung fehlen. |
| R02-F08 | P1 | **OPEN — cross-tool independence** | Zwei Contract-Repräsentationen sind keine unabhängigen Implementierungen in zwei Energiesystem-Tools. Mathematische Semantikäquivalenz, Adapter-/Konverterverluste und KPI-Replay nicht belegt. |
| R02-F09 | P1 | **OPEN — version governance** | Negative Versionswechsel werden abgewiesen, echte migrations-/backward-compatibility Regeln und Semantic Profile Change-Impact fehlen. |
| R02-F10 | P1 | **OPEN — reviewer independence** | Kein unabhängiger Fachreview durch Dritte, keine Owner-Evidenz, keine unterschriebene Gate-Entscheidung. |
| R02-F11 | P2 | **CLOSED IN RESEARCH** | Ursprünglicher A-Registry-Pfad zum MA-01-Katalog war falsch (`../../`); auf `../../../iosn_requirements_catalogue.csv` korrigiert und überprüft. |
| R02-F12 | P2 | **CLOSED IN RESEARCH** | IEEE-`NaN` konnte bei fehlenden DC-Operanden/einer NTC-Grenze unbemerkt durchgleiten. Zusätzliche `Number.isFinite`-Prüfungen und negative Fixtures jetzt für A/B vorhanden. |
| R02-F13 | P2 | **CLOSED IN RESEARCH** | Wetterjahr-/Schrittlisten-Referenzen und 48-SR-Keyset verstärkt; bewusste Prozess-/Version-/Rollenmutationen werden abgewiesen. |

**Wichtig:** P0/P1 sind hier methodische *Research Findings*, keine neu erteilte Owner-Prioritätsklassifizierung. Die zehn offenen Findings bleiben als Fragen für Integration und spätere fachliche Freigabe. Geschlossene P2 betreffen nur den lokalen Prototyp.

## Architekturkritik nach denselben zwölf Kriterien
1. **Traceability (C01):** 48 externe SR-IDs formal referenziert, neun Mini-Cases verlinkt. **Nicht** 48 vollständige Testoracles oder beidseitig validierte Source-Clausen.
2. **Semantik (C02):** Rollen L1/C1, gewichtete Szenariosymbole, Zeitintervalle sind explizit. Aber viele Bedeutungen stehen nur als String oder `TBD_OWNER`.
3. **Data (C03):** Provenienztyp und UTC-Intervall vorhanden; authentische Datei-Herkunftskette und Prüfdigests fehlen.
4. **Preprocessing (C04):** P06 als Transformation beschrieben; keine mathematische Erhaltungsgarantie und kein reales P05-Clustering.
5. **Math (C05):** DC-Mikroformel und Nichtantizipation getestet, aber keine Generierung/Analyse vollständiger mathematischer Modelle.
6. **Prozess (C06):** P00–P17 und P15-Mutationen lokal; vollständige Guard-/Workflow-Ausführung offen.
7. **Output (C07):** System Need vs. approved project abgrenzbar, KPI-Formel offen.
8. **Verification (C08):** 22/22 Sollklassifikationen pro Ansatz, **nur** Mini-Evidenz. Missverständliche `PASS`-Übertragung wäre ein Fehler.
9. **Independence (C09):** keine Runtime-spezifischen Bibliotheken, aber noch keine Tooladapter. Kein empirisch nachgewiesener End-to-End-Toolwechsel.
10. **Evolution (C10):** Profilpin A, Schema-/AST-Pin B; Migrations- und Provenienzgraph ungetestet.
11. **Standards (C11):** plausible Anschlussfähigkeiten, aber keine extern zertifizierte Normkonformität.
12. **Governance (C12):** Schätzung, keine gemessenen Kosten. A kann durch Profile differenziert gepflegt, B einheitlicher geprüft werden; keine belastbare Gewinneraussage.

## Unabhängiges Research-Votum
**Ja**, beide Architekturideen und das gemeinsame Referenz- und Mutations-Testset sind ausreichend differenziert, um **als nichtnormative Forschungsgegenstände weiterverwendet** zu werden. **Nein**, aus der Evaluation folgt keine Architekturfestlegung oder Konformitätsbescheinigung. Die *bedingte* Arbeitspräferenz für A ist nur eine Annahme über Profil-Governance, kein experimenteller Sieg; für B könnte eine durchgängige MBSE-Toolchain sinnvoller sein, sofern reale Parser-/Math-Extension-Tests das stützen.

**G1_REMAINS_BLOCKED**, `AUTHORITY_UNCONFIRMED`; Entscheidung, Datenprüfung, Normativität und echte unabhängige Personensignatur werden in einen späteren Owner-/Integrations-/Reviewprozess verschoben.
