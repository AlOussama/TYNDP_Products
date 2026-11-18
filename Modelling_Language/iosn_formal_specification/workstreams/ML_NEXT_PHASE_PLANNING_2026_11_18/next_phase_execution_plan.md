# ML-C09–ML-C16 — Verbindlicher Forschungs-Startplan als Vorschlag

**Planungsstichtag:** 18.11.2026 · **Forschungsbaseline:** ML-C08 Draft PR #51 HEAD \`8470add62fcbc7f39b1d90c0d5afdcee50ab811e\` · **Status:** PROPOSED_NOT_APPROVED, G1 BLOCKED. Dieser Plan **startet** keine neuen Forschungsexperimente, keine Freigabe und keinen produktiven Zwei-Tool-Piloten.

## 1. Warum eine neue technische Forschungswelle erforderlich ist

ML-C01–C08 schließt fachliche Traceability und beschreibbare Contract-Semantik weitgehend **strukturell**. Nicht abgeschlossen sind: native Modellgeneration und E04/E05, physikalische Reduktionsorakel, tatsächlich ausgeführte Daten-/Evidenzketten, native Standardparser und fachlich unabhängige Beurteilung. Deshalb **keine** Wiederholung von C01–C08 oder erneute pauschale Architektur-Workshops, sondern falsifizierbare ausführbare Wissenschaftsprototypen.

## 2. Aufträge und Parallelisierung

| Neue ID | Name | Direkter Start? | Eingänge | Wissenschaftlicher Kernnachweis | Bisheriges Defizit |
|---|---|---|---|---|---|
| **C09** | Executable Semantic Contract Kernel | **Jetzt parallel** | C01/C02/C03/C05/C08 | ausgeführte Typ-/ID-/Status-/Guard-Validierung inkl. Negative | C08-F-02/03/04/08/16 |
| **C10** | Native Micro-LP + E04/E05 | **Jetzt parallel** | C04/C08 | echte generierte Rows, Solve, Residuen, Mutationen | C08-F-05/21/28/30 |
| **C11** | DC reduction / PTDF/LODF/N−1 oracle | **Jetzt parallel** | C04/C08 | unabhängige physikalische Mikro-Netz-Orakel | C08-F-06/20 |
| **C12** | Synthetic data/transform/evidence lineage | **Jetzt parallel** | C03/C05/C08 | ausgeführte Teilketten + echte *synthetische* Datei-Hashes | C08-F-09/14/17/18/19 |
| **C13** | Native standard parsers, A/B/C | **Jetzt parallel** | C02/C06/C08 | echte Parser-Roundtrips + Verlust-/Migrationsmessung | C08-F-11/24/25/26 |
| **C14** | Executable conformance/evidence engine | **nach C09, C10, C12** | C05 + tatsächlich ausgeführte Input-Evidenz | sechs Status, E01–E08, negative Mutationen | C08-F-03/12/15/21/22/23 |
| **C15** | Conditional synthetic two-arm scientific benchmark | **nach C10/C11/C12/C14 und separatem Research-Go** | C07/C10/C11/C12/C14 | zwei getrennte Micro-Model-Pfade und independente Orakel, wenn autorisiert; andernfalls Readiness ONLY | C08-F-24/27/28 |
| **C16** | Executable research integration and review | **nach C09–C14, C15-Rücklauf** | alle neuen PR-HEADs | differenzierte Evidenz-/Fehler-Closure, keine voreilige ADR | C08-F-01…31 |

**Welle 1**: C09–C13 gleichzeitig, unterschiedliche Workstream-Verzeichnisse. **Welle 2**: C14 nach drei konkret benötigten technischen Inputs. **Welle 3**: C15 nur mit **separater, ausdrücklich erklärter Genehmigung für das synthetische Forschungs-Zwei-Arm-Experiment**; wenn diese nicht vorliegt, nur Readiness mit \`NOT_EXECUTED\`. C15 ist **nicht** der reale C07-P2/P3-IoSN-Pilot. **Welle 4**: C16 als kritische, nachweisorientierte Zusammenführung.

## 3. Akzeptanzkriterien, die Fehlbewertungen vermeiden

- **E04:** ein nachvollziehbarer, tatsächlich erzeugter mathematischer Zeilen-/Variablen-/Koeffizientensnapshot, mit semantischer M-/SR-Referenz und Quell-/Fixture-Version. Angekündigte Constraint-Familien oder gleiche Variablenanzahl zählen nicht.
- **E05:** tatsächliche Solver-/Lösungsinstanz, unabhängige Zielfunktions-/Primal-/wenn möglich Dualprüfung und dokumentierte numerische Toleranz im **synthetischen** Scope. Native echte Modellzulässigkeit wird nicht allein aus \`OPTIMAL\`-String abgeleitet.
- **Physik:** KCL/KVL, PTDF/LODF und Contingency-Negativfälle mit korrektem Graph/Islanding, sechs P06-Outputklassen; Energie-Cut-Erhaltung allein ist kein Equivalent-Grid-Nachweis.
- **E01–E03 / E06–E08:** \`SYNTHETIC_FIXTURE\` versus echtes Originalfile; SHA-256 tatsächlicher synthetischer Bytes erlaubt, aber niemals real qualifizierter TYNDP-Input daraus ableiten.
- **Standards:** native Parser-Engine mit benanntem Tool/Version/Command und absichtlich falschen Instanzen, nicht nur eigener JSON-/JS-Validator. Parser-Test ist kein Solverkonformitätsnachweis.
- **Kritische Mutationen:** tatsächlich injizierte fehlerhafte **generierte** Constraint-Rows und deren gezielte Entdeckung, getrennt von 26 nur konzipierten Fehlern.
- **Eigene Review:** unabhängiger Prüfrollendurchgang als \`AI_INTERNAL_REVIEW\`; keine personelle/organisatorische Unabhängigkeit ohne echte qualifizierte Unterschrift.
- **Forschungsumsetzung:** tatsächlicher Teststatus pro Objekt, kein globales \`PASS\` aus synthetischem Einzelfall oder 48 verknüpften SR-IDs.

## 4. Repository-Handoff und zeitliche Konsistenz

Alle acht Prompts befinden sich unter \`macro_prompts/ML_C09...\` bis \`ML_C16...\` mit **vollständigen Einzelaufträgen**, Rollen, Quellen, Aufgaben, Liefergegenständen und Stopregeln. Jeder soll einen **separaten neuen Branch direkt vom ML-C08-Commit** \`8470add62fcbc7f39b1d90c0d5afdcee50ab811e\` erhalten. Die C01–C07-Quellen sowie abhängige spätere PR-HEADs sind **read-only, commitgepinnt** zu laden. Weder Cherry-Pick noch ein gemeinsames produktives Repository-Merge ist durch diesen Plan autorisiert. Jeder Workstream darf nur seinen eigenen neuen Ordner schreiben; eigener DRAFT-PR gegen ML-C08, vorhandene C01–C08 nicht verändern.

Die in C08 erstellte 86-zeilige Forschungs-Traceability ist keine neue 86-SR-Baseline; die aktive vorläufige MA01-Größe bleibt 48. Die 31 C08-Findings sind über \`next_phase_findings_crosswalk.csv\` eindeutig auf Forschungsaufgaben und gesonderte später erforderliche Ownerentscheide verteilt. **Die Zuordnung ist Planungs-, nicht Closure-Status.**

## 5. Späterer Freigabepfad bleibt außerhalb

Methodology Authority/Originalrelease, dokumentierter D2↔O26-Konflikt, 87 Originaldatentypen mit tatsächlich konsumierten Dateien und Original-SHA256, Ausgangsnetzqualität, proprietäre Kosten/KPI/Storage/H2-Formeln, G1/Governance-Signaturen und echte unabhängige wissenschaftliche Review sind **Owner-/Freigabearbeiten für später**. Keine neue Phase darf behaupten, sie durch Eigenprüfungen oder synthetische Prototypen ersetzt zu haben. Kein zusätzliches allgemeines Robustheitsprofil, keine Wetterfall-Auswahlimplementierung.

**Empfehlung zur Umsetzung:** C09–C13 sind das fachlich nützlichste nächste parallel startbare Paket; C14 macht daraus eine prüfbare Evidenzkette. C15 ist optional/autorisationabhängig; C16 schließt nur die Forschung, nicht G1.
