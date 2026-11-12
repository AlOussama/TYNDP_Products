# ML-C06 — Semantic Change & Migration Analysis

**Status: Forschungsvergleich; kein freigegebener Migrationsvertrag.** Die C02-Logik benötigt Ref=(Namespace, ID, semantic_revision), Versionen und Herkunft getrennt von Approval. Unveränderte externe PRs können trotz künftiger eigener Profile ohne Ownerentscheid nicht autoritativ werden.

## 1. Änderungsfälle und Sollverhalten

|Case|Eingriff|Pflichtverhalten A|Pflichtverhalten B|Pflichtverhalten C|Freigabe-/Testgrenze|
|---|---|---|---|---|---|
|CH01 Methodology|O26-Clause/D2-Aussage ändern|Source+SR+Profile+Test-Diff; Authority nicht automatisch ändern|Referenzierten Clause-Node und abhängige Prüfungen invalidieren|Source-View und Identitätsledger auf dieselbe Version pinnen|Owner MD-01 offen, keine Normänderung|
|CH02 Data profile|MW→MWh oder Carrier-Basis wechseln|Input-Major + Math-/Output-Verbraucher erneuern|Breaking Meta/Quantity-Typ und Migration|Neue Data-View-Revisions-ID, verlustfreies Mapping|TBD-Owner, keine Null-/Einheiten-Automatik|
|CH03 Math operator|Nichtlinearen/mehrstufigen Operator ohne Semantik hinzufügen|Math-Profil Major; BLOCKED bis Prüforakel|Neuer AST-Konstrukt und Validator/Codegenerator|Math-View benötigt kontrollierte Ext/Semantic-Ledger|S11-Mutation lokal erkannt, native Sprache NOT_TESTED|
|CH04 Mandatory field|UTC Δt, P06-PST oder Evidence-Provenienz löschen|Cross-Profile-Closure FAIL|Type-/Invariant-Check FAIL|Loss register / shape FAIL|S04/S06-Mutationen lokal erkannt|
|CH05 Bad source ref|Referenz auf nicht existierenden O26-Clause|Registry-FK FAIL|AST-Graph-Endpoint FAIL|Mapping/URI Resolution FAIL|Graph-Endpunkt-Validator als Code vorhanden; Native standard NOT_TESTED|
|CH06 Mixed revisions|Input 0.2 vs Math 0.1 inkompatibel|Versionstupel reject+gezielte Adaptermigration|integriertes Major/Minor-Paketwechsel-Regime|federated view revision map reject; ledger pinned|Vollständiger Migrationstest noch NOT_TESTED|
|CH07 Lossy mapping|Lifecycle-Status oder Assetrolle beim Export verlieren|Roundtrip/semantic diff reject|AST-Codec diff reject|Ledger/Mapping-certificate diff reject|V01-Lifecycle-Loss im Test 3/3 erkannt|
|CH08 Process-only ID|B01-D001 entfernen oder neuen SR dafür erfinden|Canonical-graph closure fail|AST cardinality fail|View-identity/closure fail|P00 hat keine direkte SR; 20 objects bleiben|

Für CH01/CH02 sind Quell- und Datenversion **nicht** mit Methodikautorität, Laufereignis oder der wissenschaftlichen Wirksamkeit des neuen Werts gleichzusetzen. CH06 ist aktuell als **Versionierungsregel/Modell** zu behandeln, nicht als bereits qualifizierter produktiver Migrationstest.

## 2. Inkompatibilitätsregeln (Forschungspolitik, kein ADR)

- **PATCH** nur bei nachweislich bedeutungsneutralem Inhalt/Metadaten: Canonical IDs und mathematische Operatorsemantik bleiben gleich; Changelog, Quellenhash und Testrevision dennoch pinnen.
- **MINOR** für additive, rückwärtskompatible Aspekte ohne Veränderung bereits erlaubter Ergebnisse oder Statussemantik; Rückwärtskompatibilität muss durch Regression belegt werden.
- **MAJOR** bei geändertem Typ, Einheit/Basis, Scope, verpflichtendem Feld, zeitlicher Indexierung, Marktlink-/Branch-Rolle, Teststatus, Quellautorität, mathematischem Operator oder Verlust einer erforderlichen View-Aussage.
- **Kein automatisches Migration-PASS:** unbekannte Methode, fehlender Datenkatalog, nicht ausführbarer Operator, offene externe Parserfähigkeit oder nicht zuordenbare semantische Relation → BLOCKED, NOT_TESTED oder UNSUPPORTED mit Ursachen-ID.

## 3. Abhängigkeitsgraph statt Dateiänderung allein

Ermittle für jede neue Clause-/Data-/Math-Revision die transitiv betroffenen SR, T, M, VC, Oracles, Output-Definitionen und Tool-Adapter; verwende die **getypten** C02-Kanten statt bloße Dateinamen. Die 528/1323-Graphgröße ist ein Forschungs-Input-Stand, **kein** Beleg, dass die fachliche Ursache jeder Kante validiert ist. Eine Änderung von DataObject-Definition muss nach unten auf DataInstances/TransformationExecutions propagiert werden — diese produktiven Instanzen sind in C02 gerade **nicht** qualifiziert, weshalb ihre konkrete Zahl nicht angegeben werden kann.

**A:** potenziell kleinerer autorenseitiger Änderungsradius pro Profil, aber kombinatorische kompatible Versionstupel. **B:** weniger Cross-File-Mismatch, aber größeres gemeinsames AST-Release-Risiko. **C:** getrennte Fachstandard-Releases können zusätzliche Mappings, Semantik-Duplizierung und Round-trip-Zertifikate erfordern. Dies sind qualitative Architekturhypothesen, keine gemessenen Aufwandsstunden.

## 4. Minimaler akzeptabler Migration-Nachweis

`change_id,old_ref,new_ref,source_claim_diff,changed_semantics,affected_graph_ids,compatibility_class,profile_version_tuple,dependent_tool_capability,generated_constraint_diff,view_roundtrip_certificate,benchmark_regression,evidence_review,approval_state`.

Werden bei einer Änderung SourceScope/O26-D2-Konflikt, gemeinsame CY-Entscheidung, UTC Δt, physikalische Netzrolle, Stufenübergabe, P15-Guard, Raw/KPI oder EvidenceStatus beeinflusst, ist **semantische Neubewertung** erforderlich. D3/D4-Oracle und echte native Implementierungsevidenz können erst nach MD-/Datenfreigaben erbracht werden.

**G1 bleibt BLOCKED.**
