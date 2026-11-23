# ML-C19/17 – Forschungs-Handoff zu ML-C20 (Syntax) und ML-C21 (Validator)
Stand 2026-11-23, research-r0. **CONDITIONAL_HANDoFF**, kein produktiver Engineering-Gate, kein Schema-/DSL-Beschluss. Alle Bezüge sind auf ML-C18 pin `5555be36f74d1d4f6e871d4503c1fc91e417e57c`, mathspec pin `5f1464c334c1012cdee2947d4d55b4d1d6bef40a`, GEMS pin `c463e30b610443c1f59b20074bb7acffa2844cce`, OMG SysML 2.0/KerML 1.0 normativ begrenzt.

## Verbindliche Forschungsgrenzen für Folgepakete, aber keine Domain-Freigabe
- CSNF ist normalisierte fachliche **Bedeutungsrepräsentation**, nicht solverfähige LP/MILP/NLP IR. Keine automatisch erforderliche SOC-State-/Constraintfamilie, Gleichungsnummer, PTDF, Solver, konkrete YAML/Textsyntax.
- Jede normative Pflicht hat Kontext, Predicate, Authority, Status und ein Prüforakel. Unterschiedliche Implementierungen können denselben Contract erfüllen und E5 zulässige strukturelle Nichtgleichheit aufweisen.
- Source-/Owner-/Evidence-Dimensionen sind weder Textannotation noch optionales Prüflog, sondern bedeutungsrelevante auditierbare Daten. `OWNER_TBD`, `NOT_EXECUTED`, `PERMITTED` explizit erhalten.
- KCL-only != KCL+KVL; physical branch != market link; 1MW import != 1MW injection; kg H2 != MWh ohne Energiebasis; gleiches Objective != gleicher Feasible Set.

## ML-C20 – Aufgabenpaket Syntax/Metamodellprofile
**Startinput:** 01,05,06,07,08,09,11; Source-Einordnung 02/03/04/12.
1. Mindestens zwei leicht authorbare konkrete Oberflächendarstellungen und eine SysML-/KerML-Profilexportvariante beschreiben. Eine Syntaxwahl *erst* nach Identität/Usability/Migrationtest.
2. Typ-/Reference-Registry für C1–C9 oder eine semantisch vollständig äquivalente reduzierte Struktur entwerfen (stable ID, qualified alias, provenance/source snapshot, schema/normalization/registry version).
3. Definierte primitiven Prädikate: Vergleichs-, Boolean3-, Scoped/A-G-, Service/Capability-, Quantity-, Time-/Scenario-/InformationSet-, Topology-, Observable-KPI- und Evidence-/Variation-Expressions. Eine endliche, konservative, kontrolliert erweiterbare Grammatik; nicht alle mathematischen Operatoren importieren.
4. Explicit opt-in Profile für Electricity, H2, EV, Storage, Network, Investment, CBA, Multi-Model; Role/Carrier/Sign/Unit/Time-Basis getrennt erfassen; LHV/HHV/Vintage and Currency semantics nur nach authority.
5. Canonical serialization plus raw source retention, semantic/audit hashes versionieren, target source spans und diff diagnostics.
6. Konfigurierbare Parser-Mappings statt unkontrollierte YAML-/SysML-/GEMS-/mathspec-Feldübernahme; Schema-Change-Policy und Migrationstest.
**Acceptance (vorläufig):** 42 SLR repräsentierbar oder als tatsächlich fehlende Syntaxfähigkeit/OWNER_TBD dokumentiert; 10 RC positive+negative vectors; 18 NFR nachvollziehbar; mindestens 2 unabhängige Autorinnen/Autoren je Kernfall; A/B/H0 Authoring-Kosten gemessen. Fehlende Fachentscheidungen sind nicht syntaktisch aufzufüllen.

## ML-C21 – Aufgabenpaket Validator, Konformität, semantische Normalform
**Startinput:** 06,07,08,09,11,12,14,16; ML-C20 Schema + Quelle.
1. Phase P0–P6 R00–R13 als explizites versioniertes und typisiertes Rewrite-System implementieren; `N(N(C)) = N(C)`; Terminierung/Kritische-Paar-Prüfungen in definiertem Fragment.
2. Statik prüfen: qualified references, type/subtype, multiplicity, carrier/physical_kind/dimension/unit, sign-orientation, time duration, scenario/info-set; guard overlap und lokale Regelkonflikte, bei unentscheidbar BLOCKED/UNKNOWN.
3. Source, Owner, Evidence und Variation in jeder Transformation als Nebenbedingungen und Roundtrip-Assertions überwachen; negative cases müssen mit ID, Quellpfad, Regel-ID und Befund fehlerschlagen.
4. Adapter-Gegentests in mathspec `to_yaml(canonical=True)`, GEMS Library/System und SysML-Pilot selbst **ausführen**; wörtliche Gleichheit ist nicht ausreichend; source+audit canonical diff anfertigen.
5. E1-Entscheid strikt nur im Ruleset-Fragment; E2–E5 labels mit Scope und ProofStatus; keine automatisch erfundene Volläquivalenz oder wissenschaftliches PASS.
6. RC01–10 synthetische Fälle mit zwei unabhängigen Modellstrukturen + fehlerhaften Varianten; minimale externe Trace/Witness-Projektionen; Netz-KCL/KVL, H2-Unit, EV-Service, Nonanticipativity, CBA baselines, KPI aggregation.
7. Zwei Reproduktions-Läufe mit selben registrierten Snapshots und Umgebungen; aus CI keine Solver- oder Multi-Model-Claims ableiten.
**Acceptance (vorläufig):** alle 18 NFR überprüft, 14 R mit Testwitness, 10 RC negative cases abgelehnt oder korrekt BLOCKED, Roundtrip-Fehler null in Pflichtfeldern, keine erzwungenen unnötigen internen Algebra-Entscheidungen, Fehlerraten/Bearbeitbarkeit gemessen. Globale E2/E3/E4 bleiben ggf. proof-obligations.

## Übergabeartefakte und ihre Funktion
| Pfad | Rolle |
|---|---|
| `01` / `05` / `06` | NFR, Kernhypothese, formale Gültigkeits-/Äquivalenzsemantik |
| `02` / `03` / `04` / `12` | mathspec/GEMS/KerML source pins, Reuse + Gap |
| `07` / `08` | konkrete Rewrite-Whitelist und E1–E5 Grenzen |
| `09` / `11` | Referenzkomponenten und RC01–RC10 Orakel |
| `10` / `13` | Architekturvergleich, H0, Minimalität |
| `14` / `15` / `16` | Adversarial Findings, 15-fach Decision Vote, Test Evidence |

## Follow-up-Sequenz und Dependencies
ML-C20 (Schema-/Syntax-Entwurf) und ML-C21 (Prüffälle/Test-Orakel/Validatorarchitektur) können methodisch parallel starten, **solange** ML-C21 die von ML-C20 abhängige Parser-Implementierung erst bei stabilisiertem Schema integrieren darf. H0/KerML-Profil sowie unabhängig gepflegte GEMS/mathspec-Adapter als separate Forschungszweige vergleichen; nicht auf eine Engine als Referenzsemantik reduzieren. R1–R4 Studien-Kampagne bleibt späteres Work-Package, Daten- und Ownerfreigaben weiterhin separat.

## Offene Entscheidungen und Gates
D1–D6 UNVERÄNDERT, MD/CL OPEN, N2E Domain Authority NOT_IDENTIFIED, Syntax NOT_SELECTED, Architecture NOT_SELECTED, Owner Signature NOT_GRANTED, GitHub PR DRAFT_ONLY, Human Independent Audit NOT_EXECUTED, **G1 BLOCKED**. Source Drift: mathspec main nun `9e9b356df9d7236ff3c9d4f4b89f92c3edd8fbc4` (2 Commits nach Pin); kanonische Source-Dateien im Diff unverändert; GEMS pin aktuell main.
