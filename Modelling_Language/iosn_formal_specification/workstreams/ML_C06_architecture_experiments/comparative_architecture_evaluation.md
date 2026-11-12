# ML-C06 — Comparative Architecture Evaluation

**Ausgewerteter Stand:** Code-Mode V8-Lokalausführung, identische gespeicherte Eingaben (ML-C02-Graph-Blob `d10e...`, ML-C04-Case-Blob `3ce...`), Prüferstatus `CUSTOM_TESTS_ONLY`. Im ersten Code-Durchlauf war der B09-Wasserenergie-Feldname im Testcode falsch: 132/135 erwartete Klassifikationen; korrigierte Code-Mode-Wiederholung: **135/135**. Der Fehler lag im Experimentprüfer, nicht nachweisbar in C04 oder einem Energiemodell. Node-CLI als **separater Prozess** wurde im aktuellen Forschungsdurchlauf nicht gestartet; der identische Source ist für spätere Reproduktion eingecheckt.

## 1. Reproduzierbare Beobachtungen

|Messobjekt|A|B|C|
|---|---:|---:|---:|
|Quellzeilen graphisch/referenziell erhalten|1851/1851|1851/1851|1851/1851|
|NODE / EDGE|528 / 1323|528 / 1323|528 / 1323|
|Orig. 12 Felder/Zeile bei Roundtrip|ja, lokal|ja, lokal|ja, lokal|
|Originale 48 SR / 87 DataObject / 38 T / 48 R04 native Tests|vollständig|vollständig|vollständig|
|C04 Toy-Orakel positiv|15/15|15/15|15/15|
|Gefrorene gezielte Toy-Mutationen entdeckt|15/15|15/15|15/15|
|Semantische Mutationen entdeckt|12/12|12/12|12/12|
|Gezielter Lifecycle-Field-Loss erkannt|1/1|1/1|1/1|
|Zusätzlich Graph- und Profilsemantik-Basistest|2/2|2/2|2/2|
|**Erwartungskonforme lokale Klassifikationen**|**45/45**|**45/45**|**45/45**|
|Native SysML-/ReqIF-/GEMS-/LinkML-/SHACL-Prüfung|NOT_TESTED|NOT_TESTED|NOT_TESTED|
|D3 erzeugte LP-Matrix und nativer Solver|NOT_TESTED|NOT_TESTED|NOT_TESTED|
|Prod. IoSN-Konformität / G1|BLOCKED|BLOCKED|BLOCKED|

Die gemeinsame Rechenkernfunktion prüft B01–B15 gegenüber eingefrorenen Minibeispielwerten, nicht sämtliche zulässigen LP-Formulierungen. Die 15 Mutanten ändern ausgewählte Input-/Oracle-Felder und sind **kein** Beweis, dass jede falsche Gleichung eines konkreten Modellgenerators erkannt würde. Für B06 wird explizit nur der **konditionale** Fixed-Stage-Test geprüft, nicht eine autorisierte Stage-1-Transferregel.

## 2. Fachlicher Kriterienvergleich

|ID|A: Module/Registry|B: Typed Meta|C: Föderierte Views|Gemeinsame Grenze|
|---|---|---|---|---|
|C01 Traceability|Explizite Cross-Profile-Edges; lokal geprüft|Ein Graph; lokal geprüft|Ledger + Canonical IDs; lokal geprüft|Quell-/SR-Mapping fachlich weiter UNCONFIRMED|
|C02 Typen/Semantik|gemeinsamer externer Kernel nötig|Typisierte AST-Objekte, lokale Typprüfer|Shape-/Mapper-Verträge nötig|keine vollständige formale Semantik oder externer Parser|
|C03 Achsen|Input-/Math-Profile getrennt|einheitliche Scope-Werte|mehrfache View-Bindung mit Mapping|symbolische Gewichte, kein reales CY/UTC-Paket|
|C04 Mathe|Math-Profil und C04-Oracle|Typed Math-Objekte geplant|GEMS/mathspec-View theoretisch|kein D3/D4 realer Equivalence-Witness|
|C05 Preprocessing|Transformprofil und Datenedges|Typed Transformation Nodes|Prozess-/Datenview-Koordination|38 Definitionen ≠ Executions|
|C06 Prozessbedingungen|Process-Profil P12/P15-Guard|Guard im integrierten Zustand|DMN/BPMN-View als Option|keine native Workflowausführung|
|C07 Provenienz|referenzierte Quelldaten|gemeinsame Provenienzattribute|globales Herkunftsledger|keine echten Daten-/Outputs-Hashes|
|C08 Verification|Verification-Profil|typed Verification/Evidence-Felder|review-/evidence-View|48 native Tests NOT_EXECUTED|
|C09 Änderung/Extension|separate Profilzyklen möglich|zentrale AST-Evolution|separate Views möglich|keine gemessene Produktionsmigration|
|C10 Semantic Migration|Versionstupel-Konsistenzrisiko|schemaweite Änderungskopplung|Mapper-Verlust-/Dual-Owner-Risiko|Annahmen für Breaking-Change-Policy noch Forschung|
|C11 Standards|ReqIF/LinkML/GEMS-Adapter denkbar|SysML/LinkML-Derivate denkbar|bestehende Fachviews denkbar|native Parser alle NOT_TESTED|
|C12 Aufwand|Cross-Profile Closure aufwendig|zentrale Governance kompakter, Releasekopplung|Mapping- und Versionenpflege hoch|keine reale Lifecycle-Kostenerhebung|

**Keine Scheinquantifizierung:** 45/45 ist eine Eigenschaft des vergleichenden *Testharness* und der äquivalenten, verlustfreien Mockups. Daraus folgt **nicht**, dass A/B/C gleich gute Produktarchitekturen oder alle mathematischen Operatoren ausdrücken. Umgekehrt ist A durch existierende R02-Prototypen nicht methodisch besser; C erhält einen eigenen Custom-Adapter für dieselbe Testbasis, aber **keine** Standardparser-Vorzugswertung.

## 3. Wichtige fachliche Beobachtungen

1. Nichtantizipativität verlangt über alle drei Jahre denselben **symbolischen CY-Gewichtsvektor**, nicht Gleichgewicht der fünf CY-Werte und nicht Jahre-übergreifende endogene Kapazitätsentscheidungen. Die Toy-Orakel B01/B02 mit ungleichen Zahlen sind ausdrücklich künstlich.
2. B04/B05 prüfen lokale Winkel-/Flow- und LODF-Arithmetik am Dreieck; weder P06-Reduktion noch PTDF-Äquivalenz an einem echten Netz ist demonstriert. Physikalischer Branch und steuerbarer Candidate-Link sind getrennte Kategorien.
3. B07–B09 umfassen nur definierte Speicher-/H2-/Hydro-/DSR-Kleinstfälle. H2-LHV/HHV und Hydro-Grenzbedingungen bleiben OWNER_TBD.
4. B11 beweist über den bekannten Beispielvertrag nur eine bedingte Slack-Projektion. B12 toleriert verschiedene optimale Portfolio-Vektoren; ein produktiver KPI kann dennoch eine bislang offene Tie-Break-Regel benötigen.
5. Ohne Formel-/Filter-/Status-Freigabe ist eine abgeleitete „System Need“-Kennzahl kein genehmigtes Projekt. Bezeichner `EvidenceRequest` und `Evidence` dürfen nicht gleichgesetzt werden.

## 4. Abhängigkeiten zu Standards

Die 132 Einträge in `standards_and_extension_gap_matrix.csv` sind eine **Dokumentationsprüfung der generischen Relevanz** für 12 Kriterien, keine externe Parser-Zertifizierung. Standards sind typischerweise nach Rollen wiederverwendbar (z. B. ReqIF-Requirements, LinkML-Input, GEMS/mathspec-Mathematik, BPMN-Prozess). Die Realisierbarkeit eines vollständigen IoSN-Contracts entsteht erst durch zusätzlich prüfbare Domänensemantik, Autorität und Evidenz. Für SiennaSchemas ist vor produktiver Nutzung insbesondere das vom Projekt dokumentierte Pre-1.0-Änderungsrisiko zu berücksichtigen.

## 5. Bewertungsurteil

**Keine belastbare Rangfolge** aus lokalen Gleichstandszahlen. A begünstigt unabhängige Profilpflege, B verringert Fragmentierung auf Kosten gemeinsamer Evolutionszyklen, C fördert Wiederverwendung unter der Bedingung eines eindeutigen Identitätsledgers und nachgewiesener verlustfreier View-Mappings. Alle drei erhalten vorläufig den Status `RESEARCH_FEASIBLE_WITH_CRITICAL_GAPS`; Entscheidung nur konditional (siehe `conditional_architecture_recommendation.md`), G1 BLOCKED.

## 6. Zusätzlicher beobachteter Änderungsregressionslauf

Die eigenständig protokollierten 8 Änderungsmutationen (Quellautorität, Datenprofilstatus, inkompatibler Operator, Zeitpflichtfeld, fehlerhafte Quellkante, inkompatible Profil-/Metamodell-/View-Revision, verlustbehaftete View und process-only-Objekt) ergaben **24/24** korrekt erkannte Fehler über drei Varianten. Positive Ausgangszustände wurden jeweils vorher mit derselben lokalen Änderungsregel geprüft. CSV: `semantic_change_test_results.csv`, wiederholbarer Runner: `run_change_experiments.mjs`. Es wurde keine vollständige Migrationsreparatur implementiert, keine native Standard-View serialisiert und kein Parser oder zwei unabhängige Energie-Modellgeneratoren ausgeführt; diese Prüftiefen bleiben `NOT_TESTED`.
