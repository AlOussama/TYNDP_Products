# ML-C19/16 – Tatsächliche Forschungsvalidierung und Evidenzgrenzen
Stichtag 2026-11-23, Research-r0, NON-NORMATIVE. „Validiert“ bezieht sich **ausschließlich** auf die im Abschnitt Executed aufgeführten Kontrollen. Unterscheide SOURCE_VERIFIED, NORMATIVE_SPEC, DOCUMENTED, I_IMPL, T_EXISTING, EXECUTED_SYNTHETIC, NATIVE_EXECUTED, CONCEPTUAL, NOT_EXECUTED, BLOCKED.

## Source und Branch-Verifikation – tatsächlich ausgeführt
1. GitHub `compare_commits`: `AlOussama/TYNDP_Products`: base `5555be36f74d1d4f6e871d4503c1fc91e417e57c` vs `research/ml-c18-general-study-contract-2026-11-20`: IDENTICAL, ahead=0, behind=0.
2. Externe Pin-Dateien via GitHub `fetch_file` geladen: mathspec canonical `_canonical.py`, `tests/test_canonical.py`, `spec.py`; GEMS README, `library.md`, `system.md`, `COMPATIBILITY.md`; ML-C18 01/02/03/04/07/08/13. Einige externe technische Mechanismen sind zusätzlich über ML-C18-Quellen belegt, **nicht erneut vollständig Dateipfad für Dateipfad geprüft**.
3. Externe Branch-Differenz `compare_commits`: GEMS pinned `c463e30b610443c1f59b20074bb7acffa2844cce` vs main = IDENTICAL. mathspec pinned `5f1464c334c1012cdee2947d4d55b4d1d6bef40a` vs main = AHEAD 2, latest `9e9b356df9d7236ff3c9d4f4b89f92c3edd8fbc4` (release 0.5.0a1). Geänderte Pfade umfassen Changelog, SOS implementation/test/fixtures und einige Dokumente; **keine Änderungen** an den direkt untersuchten `_canonical.py` und `test_canonical.py` im Vergleich. Forschungsvergleich bewusst am gepinnten Stand.
4. OMG-SysML/KerML: offizielle Spezifikationsseiten/zugehörige PDF-Auszüge recherchiert; Normativversionsgrenzen von Pilotimplementierungen getrennt; kein OMG-Standards-Conformance-Lauf.
5. Separater ML-C19-Branch `research/ml-c19-canonical-normal-form-2026-11-23` wurde aus exakt ML-C18-Pin angelegt; neue ML-C19-Pfade (01–17) dokumentiert. Keine Änderungen an bestehenden ML-C18-/IoSN-Dateien vorgesehen.

## Executed: isolierter synthetischer Mikrocheck
Python 3 Standardbibliothek, einmalig per ausführbarem lokalem Script `ml_c19_csnf_synthetic_checks.py` ausgeführt, **22 Tests, 22 PASS, 0 FAIL/ERROR**; nicht Bestandteil der mathspec/GEMS/SysML-Toolchains. Geprüfter Funktionsumfang:
- **6 positive Checks:** deterministic source ordering, idempotent canonicalization, Guard AND/OR commutativity, AND associativity, exact kW to MW conversion, order-insensitive assertion set.
- **12 differenzierende Mutationen:** injection-vs-consumption, KCL-vs-KCL+KVL, physical-vs-market-link, REQUIRED-vs-PERMITTED, OWNER_TBD-vs-APPROVED, NOT_EXECUTED-vs-PASS, DATA_ASSUMPTION-vs-GUARANTEE, Source A-vs-B, scope/scenario, carrier, guard, identical-objective-only vs full constraint.
- **4 Rejection Tests:** H2 mass vs energy without LHV basis, invalid owner status, absent source list, duplicate Assertion-ID.
Test-Typ: EXTRACTED/SIMPLIFIED-SCHEMA SYNTHETIC_MICROCHECK, **kein** universeller NFR03-Soundness-Beweis und **kein** nativer RC01–10 Parserlauf. Für einen konservativen Anteil gilt: 22/22 Mikrochecks bestanden, aber *nicht* 10/10 RC nativ validiert und nicht 42/42 SLR vollständig normalisiert.

## Source-Inspektion gegenüber vorhandenen Testdateien
| Quelle | Direkt untersuchte Funktion | Evidenz |
|---|---|---|
| mathspec `_canonical.py` | sort/flatten für plus, times, AND/OR; Nichtsortierbarkeit division/exponent/compare; canonical_dict | tatsächlicher Code I_IMPL inspiziert |
| mathspec `tests/test_canonical.py` | 2000 AST Fixed Points, 500 generated arithmetic values, 500 bool conditions x16 inputs, negative orderings | vorhandene Tests T_EXISTING inspiziert, **in ML-C19 nicht ausgeführt** |
| GEMS library/system docs | Ports, Fields, Instances, Connections, Binding Constraints | D_DOC; konkrete native Funktionsausführung unbewiesen |
| GEMS Compatibility | Sprache/Interpreter-Kompatibilität | D_DOC, kein E2E |
| SysML/KerML | Type/Features, Definition/Usage, A/G Requirements, Ports/Connections, VerificationCases | Normativspezifikationsanalyse, keine native Conformance |
| ML-C18 | 42 SLR, 17 K, 10 Referenzfälle und historische 27/27 Mikrochecks | historische Vorarbeiten, **nicht** erneute ML-C19-Tests |

## Explizit nicht ausgeführt
- `pytest` der *installierten* mathspec-Distribution im ML-C19-Lauf, mathspec-to-CSNF Mapping/Parser, neue mathspec-RC01–10; mathspec CI war im vorigen ML-C18-Stand separat bewertet.
- GEMS/GemsPy/Antares Interpreter/Parser, GEMS-Library Battery-Swap, reale Grid-Berechnung/Unit Checker, CI E2E.
- SysML v2 Pilotparser, API import/export, KerML-Profilexport oder native Requirement Verification.
- Konsistenzbeweise für alle Scope/Guard-Formeln, globale Terminierungs-/Konfluenz-/Soundness-Beweise, E2–E5 für beliebige mathematische Systeme, R1–R4 Multi-Model Robustness.
- 42/42 SLR authoring coverage mit unabhängigen Autoren, gesonderte Personenaudits, produktiver IoSN/G1-End-to-End, reale Datenqualifizierung, Solverbenchmarks.

## Daten und offene Risiken
Alle Zahlen auf klarer Grundgesamtheit berichten: 18/18 Anforderungen im Katalog (nur als Anforderungen erfasst), 14/14 Regeln spezifiziert (kein beweisender Soundness-Test), 10/10 RC als Designwitnesses (keine native Ausführung), 22/22 eigene synthetische Testfälle (nur Teilmuster), 9 vorläufige Kernrollen, 17 definierte Forschungsdokumente. Eine höhere Evidenzstufe darf nur nach separatem Run mit versioniertem Code, Eingaben, Umgebungs- und Testlog behauptet werden.

## Repo-Isolation / Draft-PR-Check
Abschließende GitHub-Diff-Prüfung der Branchänderungen und Link zur Draft-PR wird nach Erzeugung separat verifiziert; dieser Bericht behauptet **keine** vorausgreifend durchgeführte Merge-/Ownerfreigabe. Gate G1 BLOCKED, D1–D6 unberührt.

## Reproduzierbarkeit
Mikrotestquelle ist als separate benutzerseitig bereitgestellte Python-Datei `ml_c19_csnf_synthetic_checks.py` verfügbar; jeder unabhängige Reproduktionslauf muss die Datei, Python-Version und Testresultate protokollieren. Für umfassende CSNF-Regression fehlen die vollständige versionierte AST-Implementierung und Normalisierungs-Rule-Registry, die ML-C20/21 als spätere Arbeitspakete erhalten.
