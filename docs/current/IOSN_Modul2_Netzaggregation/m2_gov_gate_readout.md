# M2-METHOD-G1 — konsolidierte Gate-Matrix und Owner-Readout

**Datum:** 2026-11-11 · **Status:** **DOCUMENT_ONLY / SCOPED_SYNTHETIC_METHOD_BASELINE_PROPOSED**  
**Externe Autorität:** **ENTSOE_AUTHORITY_UNCONFIRMED** · **M2 Owner:** **NO_DECISION_RECORDED** · **Merge:** **NOT_AUTHORIZED**  
**Bezug:** Verbindlicher [Handoff 97 @ 27dfd810](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/97_M2_METHOD_G1_OWNER_AUTHORITY_DECISION_MACRO_20261111.md). Dies ist weder ein neuer vollständiger Methodenreview noch ein Implementierungsauftrag.

## 1. Verifikations-Readout (immutable Evidence Pins)

| Prüfquelle | Verifiziertes Artefakt | Feststellung für dieses Gate |
|---|---|---|
| **R-METH, PR #30** | [Commit 754a79e11370dca2c25f1102d83ced5beb251522](https://github.com/AlOussama/TYNDP_Products/commit/754a79e11370dca2c25f1102d83ced5beb251522), [Review 88](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_INDEPENDENT_METHODOLOGY_AUTHORITY_DELTA_REVIEW_2026_11_11.md), [18/18 CSV](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_METH_REQUIREMENT_DELTA_2026_11_11.csv) | O26 ist Konsultationsfassung; adopted/effective Nachfolgequelle B und Original-PDF-SHA-256 **nicht positiv verifiziert**. 0 nachgewiesene neue Anforderungen ist **kein** „keine Änderungen“-Bescheid. PR #30 offen, Draft, ungemergt. |
| **BUNDLE01R/A, PR #22** | [Head 09cff8a8f9d82282d2e307f32ba8b139c3eb3824](https://github.com/AlOussama/TYNDP_Products/commit/09cff8a8f9d82282d2e307f32ba8b139c3eb3824) | 21/21 MD/CL offen, 0/21 autorisierte Owner-Beschlüsse. SDC 03./04.02. TOP 15.3 berichtet geplante schriftliche Freigabe, nicht deren Vollzug. |
| **BUNDLE01R/B, PR #23** | [Head 3fd3b0e6ede30f863228d426389e880bdb09f1d0](https://github.com/AlOussama/TYNDP_Products/commit/3fd3b0e6ede30f863228d426389e880bdb09f1d0) | 87/87 inventarisierte Objekte klassifiziert, **kein** verbrauchsidentisches qualifiziertes Originaldatei-Set mit Hash; 0/28 reale Inhaltstests ausgeführt. 16 Projekt-Metadatenchecks sind **kein** Datenqualitäts-PASS. |
| **BUNDLE01R/C, PR #24** | [Head dfaf75c0a85e3ec4d9ba4a29b3864fb13d987883](https://github.com/AlOussama/TYNDP_Products/commit/dfaf75c0a85e3ec4d9ba4a29b3864fb13d987883) | 50 MR/48 SR als Draft strukturell geführt; 20/20 L1–L4-Strukturprüfungen bestanden, nicht semantisch freigegeben; keine normativ autorisierte SR-Änderung. |
| **BUNDLE01R/D, PR #25** | [Head 5c13d4d63f18d30c308997cd7a01f2977fcc6b7b](https://github.com/AlOussama/TYNDP_Products/commit/5c13d4d63f18d30c308997cd7a01f2977fcc6b7b), [G1-Assessment](https://github.com/AlOussama/TYNDP_Products/blob/5c13d4d63f18d30c308997cd7a01f2977fcc6b7b/Modelling_Language/iosn_formal_specification/workstreams/BUNDLE01R_D_independent_gate_review/gate_g1_readiness_assessment.md) | G1 **REMAINS BLOCKED**, 23/23 Findings offen (14 P0/9 P1), kein Personen-/Organisations-Signoff und kein Gate-Approver-Beschluss. Alle #22–25 offen/Draft/ungemergt. |
| **S-GOV-M2** | [Konsolidierung 93 @ 27dfd810](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md) | M2-MA1 unabhängig: PHY 4 P1; CLU 2 P1 und 3 P2; API-Empfehlung **C** ohne Owner-Entscheid; D-REAL BLOCKED_DATA; M2-MA2 und MA3 nicht produktiv freigegeben. |
| **R-API, D-REAL** | [API @ 075c509](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md); [D-REAL @ 6a8262](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/89_M2_D_REAL_GAP_GATES_AND_WITNESS_2026_11_11.md) | A = iosn_official als kanonische Empfehlung, B = m2 nur über kontrollierten Adapter. Kein realer AC/DC-Referenzlauf, Original-Dispatch, neutrale Kalibrierung, signiertes N-1-Paket oder D4-Witness. |

**Abgrenzung der offenen Findings:** Die **23 BUNDLE01R-G1-Findings** sind ein **übergreifender** Rückstand, nicht zusätzlich 23 bewiesene M2-MA1-Fehler. Die **6 MA1-P1** in PHY/CLU sind gesondert auf integriertem Repair-SHA nachzuprüfen. Die 9 R-API-P1 beschreiben Vertrags-/Kompatibilitätsrisiken, nicht zusätzliche neun festgestellte Fehler in A.

## 2. Übergreifende G1-A–H-Matrix (aus PR #25, kein neuer Gate-Beschluss)

| Gate | Ist-Status | Fehlender positiver Evidenzakt | Zuständige Autorität | Gültiger Schluss |
|---|---|---|---|---|
| **G1-A – Source Authority** | **BLOCKED** | Originale adopted/effective ENTSO-E-Fassung oder formelle O26-Adoption, SHA-256, Approval, Effective Date, Annex/Errata, kontrollierter Delta-/No-Change-Nachweis | Autorisierter ENTSO-E IoSN Methodology Owner | Kein normativer M2-Go |
| **G1-B – Entscheidungen** | **BLOCKED** | 21/21 MD/CL schriftlich entschieden, versions- und laufbezogen, signiert; M2-Teilauswahl ersetzt Gesamtgate nicht | Je Domain-/Methoden-Owner und G1 Approver | Keine stillschweigende Ownerentscheidung |
| **G1-C – Datenquellen** | **BLOCKED** | Frozen, tatsächlich verbrauchtes Primärdatei-/Release-/Lizenz-/Hash-Manifest, einschließlich 2035-Netz- und Modellzuordnung | Data/TSO/Source Owners | Katalog-URLs reichen nicht |
| **G1-D – Validierungen** | **BLOCKED** | 28 originäre Inhaltstests anhand originaler Bytes mit nachvollziehbaren Orakeln und Ergebnissen | Data QA und unabhängiger Reviewer | 0/28 REAL_EXECUTED |
| **G1-E – MA01-Anforderungen** | **BLOCKED_SEMANTICS** | Owner-bestätigtes 48-SR-Mapping, kontrollierte A/B-Änderungen, 20 process-only Objektzuordnungen, L3/L4-Verhaltensorakel | Requirements/Method Owners | 20/20 Strukturprüfungen ≠ fachliche Freigabe |
| **G1-F – Findings/Orakel** | **BLOCKED** | 14 P0 beheben und unabhängig nachweisen; P1 beheben oder explizit bereichsbegrenzt signiert ausnehmen | Review- und Gate Owners | 23/23 offen; kein Befund erlassen |
| **G1-G – Unabhängigkeit** | **BLOCKED** | Kompetenter personell/organisatorisch unabhängiger Review und benannte Approvalberechtigung, Signatur | Independent Reviewer + zuständiger G1 Approver | AI-/Eigenreview ersetzt nicht Signoff |
| **G1-H – Änderungsdisziplin** | **CONTROLLED_DRAFT_ONLY** | Signierte Release-/Änderungsfreigabe und überprüfte Baseline/PR-Grenzen | Repository/Configuration/Requirements Owners | Draft-Separation nur Dokumentationskontrolle |

**Gesamtausgang:** **G1_REMAINS_BLOCKED / AUTHORITY_UNCONFIRMED.** Keine Rückwirkung eines strukturellen PASS auf Source-/Owner-/Real-/Independent-Gates.

## 3. M2-spezifische Owner- und Methoden-Gates

| Gate / Entscheidung | Jetzt | Minimaler Exit-Nachweis | Freigabe-/Reject-Instanz | MA1/MA2/MA3-Grenze |
|---|---|---|---|---|
| **GA-A / OD-M2-METH-01** | **EXTERNAL_AUTHORITY_PENDING** | Verabschiedete/für Lauf gültige Fassung mit Originalhash und Approval oder dokumentiertes formelles O26-Adopt; A/B-Diff NR-01–18, SR-013–026 | ENTSO-E Methodology Owner; unabhängiger Quellprüfer | Alle offizielle Claims BLOCKED; synthetische O26-Arbeit als solche möglich |
| **GA-C / OD-M2-CLUSTER-02** | **OWNER_ORACLE_PENDING** | 37 rohe Label inkl. NI/UK, 102 Quoten, reale Busmap, Countryresolver, AC-Connectedness; 225/400-MWh und Klassen-Mapping; Protection-/Feasibility-Witness | Network Clustering Owner + Graph-Reviewer | MA1 synthetische Spezifikation; reale Busmap BLOCKED |
| **GA-E / OD-M2-EQV-03** | **MODEL_DESIGN_ONLY** | Globaler x>0/c0-Fit, eindeutige Eichung/Gauge, A_zΓ=P A_d, KCL/affine KVL, bilanziertes neutrales PST/HVDC-Szenario, unabhängige Residuen | Network Reduction Owner + Numerik-Reviewer | MA2 G06–G08 nicht implementiert/autorisert |
| **GA-R / OD-M2-RMSE-04** | **THRESHOLD_NOT_APPROVED** | Fixierte Monitorgruppe, Metrik/Nenner/Gewichte, Zeit-Train/Select/Holdout, globaler Refit pro Kandidat, Plateau und Akzeptanzwerte, Replay | Network Reduction/Verification Owners | Keine RMSE-O26-PASS-Schwelle; MA2 nur Forschungsdesign |
| **GA-N / OD-M2-N1-05** | **BLOCKED_REAL_SECURITY** | Originale Ausfälle, gültige LODF/Islanding-Maske, Lastfluss-/Notfallgrenzen, TSO-Ausnahmen, vier Sommer/Winter × +/- Orakel, Grenzfallreplay | TSO/Grid Security Owner + Independent Reviewer | MA3 synthetische Proxy-Spezifikation möglich; reale Kapazitäten NO_VALUE |
| **GA-D / OD-M2-DATA-06** | **BLOCKED_DATA** | Source-/Release-/Bytehash-, Stunden-/DST-/Leap-/MW-/pu-/Rating-/Bus-Manifest; 5 feste extern übergebene IDs; neutrale und normale Referenz-Dispatch-/Flow-Sets; D4 | TSO/Data/Time/Weather Input Owners + D4 | Real MA1–MA3 BLOCKED |
| **GA-V / OD-M2-DEVICE-07** | **DEVICE_PROFILE_PENDING** | Supported/approx/reject-Matrix und Loss-/Tap-/Phase-/HVDC-/PST-/3W-/110kV-Tests; **finite** Akzeptanztoleranzen mit Einheiten und Quelle | Device/TSO Owner + unabhängiger Physik-Reviewer | G11 nur PARTIAL_LOSSLESS_DC_ONLY, real BLOCKED |
| **GA-L / OD-M2-LF-08** | **DOWNSTREAM_CONTRACT_PENDING** | LF-/Investment-/Dispatch-/OPF-Flags, Aktivierungs- und Infinity-Semantik, Vergleichsorakel; signierter Modusvertrag | Network Expansion Owner | M2 exportiert, implementiert keine LF-/OPF-Solver |
| **GA-P / OD-M2-API-09** | **OWNER_PENDING** | A/B/C Ownerakt (C empfohlen), A-Contract v1, featureweise B→A-Reject-/Parity-Matrix, Replay und MA1-Re-Reviews | M2 Project Owner + API Architect | Produktive MA2-Grenze gesperrt |
| **GA-I / OD-M2-I-10** | **PROJECT_I_PROPOSED** | I-01..06 Protokoll (Seed, Eichung, c0, Monitor/Split, Plateau, N-1-Proxy, numerische Toleranzen); Fixtures/Unabhängigkeit/Ownerakt | M2 Project Owner + Numerik-Reviewer | Forschungsprofil ≠ veröffentlichter ENTSO-E-Algorithmus |
| **GA-S / OD-M2-SCOPE-11** | **DOCUMENT_FIXTURE_PREP_ONLY** | Eigentlicher Projekt-Scope-Beschluss vor zusätzlichem Runtime-Code; integrierter Repair-Code-SHA, P1=0, unabhängige PHY/CLU-Replays, API-Freeze vor produktivem MA2 | M2 Project Owner / S-GOV-M2 | Docs, Prüfdesign, isolierte synthetische Fixtures jetzt; MA2/MA3 Runtime nicht |
| **GA-M / OD-M2-MERGE-12** | **NO_MERGE_NOW_RECOMMENDED** | Explizite PR-/SHA-/Owner-/Reviewer-bezogene Merge-Erlaubnis | Repository/Project Owner | Kein Merge durch diese Dokumentation |

**Evidenzregel:** Jedes geschlossene Gate benötigt versionierte Originalquelle (wenn extern), Quellbyte-Fingerprint, Zuständigkeits-/Approvalnachweis, Einheiten-/Rechen-/Testartefakt und unabhängige Reproduzierbarkeit. Eine Projektempfehlung allein erfüllt kein externes Methodengate. Numerische Grenzwerte (KCL, RMSE, LODF, Gerätefehler) werden **nicht** aus den Berichtsdarstellungen oder synthetischen Standardtoleranzen als offizielle ENTSO-E-PASS-Grenze abgeleitet.

## 4. NR-01 bis NR-18: echte Delta-Disziplin

Die [R-METH-Anforderungsmatrix](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_METH_REQUIREMENT_DELTA_2026_11_11.csv) enthält **18/18 O26-basiert beschriebene Regeln und offene Lücken**. Die neue Datei [m2_nr01_nr18_delta.csv](m2_nr01_nr18_delta.csv) enthält **nur den Header, null Zeilen**. Bedeutung: **Kein autoritativ nachgewiesener geänderter NR-Text**, weil Quelle B weder mit nachweisbaren Originalbytes noch Approval verifiziert wurde; **kein** Urteil, dass sich nichts geändert hat. Quelle B später: Old/New-Klausel und Hash vergleichen, 18 NR einzeln dispositionieren, zu SR-013–026 und MA1–3 mappen, freigeben und erst dann maschinenlesbare Delta-Zeilen ergänzen.

**Konkrete konstante Forschungsinvarianten, keine frisch freigegebenen Normen:** ein pan-europäisches AC-Referenzmodell; Länderreinheit der Zonen; O26-37/102-Quoten nur im Vollprofil, NI und UK separat; 225-/400-kV-Jahresüberlastung in MWh als Screening ohne Entfernen sonstiger Netzteile; global x/c0 mit kohärenter KVL; vier gerichtete/saisonale N-1-Kapazitäten mit Qualifikationsflags. O26-§3.7 enthält drei repräsentative Wetterfälle je Zieljahr, während fünf bereits extern ausgewählte Projektjahre als **fixe Forschungseingaben** geführt werden: kein Quellen-PASS, keine interne Auswahl.

## 5. Welche Arbeit ist unabhängig von der endgültigen Methodenfreigabe zulässig?

**Ohne vorgespiegelte externe Freigabe sofort wissenschaftlich vertretbar** sind Quellenledger/Ownerklärung, die projektinternen Verträge, formale Netz-/Graph-/Einheiten-Invarianten, dokumentierte Projekt-I-Alternativen, Test-/Oracle- und isolierte synthetische Fixture-Designs, Review-Planung sowie parallele D0–D3-Quellenbeschaffung. Ein synthetischer Test kann **PASS_SYNTHETIC** liefern, **nie** automatisch AUTHORITY_ADOPTED, REAL_QUALIFIED oder MA2_RUNTIME_READY.

**Nur mit einem separaten positiven projektinternen Implementierungs-Gate** dürfen Worker die MA1-Reparaturen/Integrations- und unabhängigen Re-Reviews (RP1/RR1), produktiven B→A-Adapter oder MA2-Code beginnen. Der [Governance-Handoff 98](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/98_M2_MA2_PRE_DOCUMENT_FIXTURE_MACRO_20261111.md) autorisiert durch seine Existenz **keine** MA2-Runtime; die vorliegende Vorlage erweitert dessen Mandat nicht. MA3-Code benötigt zusätzlich eine spätere spezifische Autorisierung. D4-Realprüfung erst nach Originalbytes und Freeze-Manifests.

**Verboten als Abschlussbehauptung:** offiziell angenommene IoSN-Fassung ohne Sourceowner-Approval; Methoden-Konformität; reale 37/102-Netzwitness, numerische ENTSO-E-RMSE-Akzeptanz, belastbare N-1-Realtransferkapazität, G1-Freigabe oder automatischer Merge. M0/CGMES, M1/PECD und externe Wetterjahrauswahl bleiben unberührt.

## 6. Entscheidungseinholung / minimaler Abschluss

1. Autorisierte ENTSO-E Methodikinstanz: Quelle B oder ausdrückliche O26-Adoption (mit Originaldatei, Hash, Approval, Geltung); nicht ersetzbar durch einen Repository-Owner.
2. Domain Owners: **MD-03, MD-13, MD-11/12, MD-08** und ggf. MD-18/MD-14 nur als **Input-Grenze**; signierte Referenzfälle, Toleranz- und Quellenmanifeste. Die übrigen 21 MD/CL aus PR #22 bleiben für übergreifendes G1 offen.
3. M2 Project Owner: getrennte Akten zu **OD-M2-METH-01..OD-M2-MERGE-12**, insbesondere Projekt-I, API-Option C, Scope und NO_MERGE_NOW; bis dahin **PENDING**.
4. Review/Gate: personell unabhängige Prüfungen auf exakten SHAs; vor Real-GO originale Topologie/Dispatch/LODF- und Kapazitätswitness, D4 und G1 A–H.

**Vorliegendes Resultat:** Vier neue Dokumentationsartefakte, im dedizierten Branch vorbereitet. **Kein** Owner-Beschluss eingetragen, **keine** Implementierungsdatei verändert, **kein** Merge und **kein** synthetischer oder realer Lauf als neu ausgeführt behauptet.

**Artefakte:** [m2_owner_decision_register.md](m2_owner_decision_register.md) · [m2_method_authority_ledger.json](m2_method_authority_ledger.json) · [m2_nr01_nr18_delta.csv](m2_nr01_nr18_delta.csv) · diese Gate-Matrix.
