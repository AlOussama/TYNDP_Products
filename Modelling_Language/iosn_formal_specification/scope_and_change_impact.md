# MA-01 — Scope and Change Impact Assessment

**Stand: 2026-11-05 / Rev. 0.1.0 / PROVISIONAL.** Geltungsbereich ist ausschließlich die toolunabhängige IoSN-Systemanforderungsbaseline. Alle früheren 'MR-*', 'SR-*', 'UC-*', 'VC-*', 'LRC-*' bleiben aus Provenienzgründen erhalten, sind aber **nicht mehr aktiv**. Es gelten ausschließlich die als vorläufig gekennzeichneten MA01-SR in iosn_requirements_catalogue.csv. Unveränderte IoSN-Implementierungen werden nicht umgebaut.

## Verbindliche Scope-Grenze

|Im IoSN-Contract|Explizit außerhalb des IoSN-Contracts|
|---|---|
|Identitäten, Anzahl, Studie-/Szenariozuordnung, Gewichte der bereits ausgewählten Wetterjahre als extern gelieferter Input|Entscheidung über Repräsentativjahre, PCA, Feature Engineering, K-Means, Clustering, Optimierung der Auswahl|
|Zeitreihen, Zeitachsen, Quellen, Einheit, räumliche Zuordnung und Provenienz der ausgewählten Jahre|Reproduktion/Verifikation des vorgelagerten statistischen Auswahlverfahrens und der Auswahlentscheidung|
|Formale Input-Konsistenzprüfungen: IDs, eindeutige Zuordnung, Gewichte, Vollständigkeit, Stundenindex|Vorgelagerte Datenaufbereitung für Wetterjahrauswahl und Audit der statistischen Begründung|
|Netzaggregation, sektorübergreifendes Modell, Kandidaten, verbindliche LP-Methodik, Ergebnisausgabe, Systembedarfsprüfung|Spezifikationssprache, Metamodell, Code, neue Validatoren/PoCs, PyPSA/Antares/Sienna-Adapter, CBA-Interoperation, allgemeine Robustheit|

Eine fehlerhafte Gewichtsdatei ist ein **Input-Validierungsproblem** des IoSN, nicht die Ermächtigung, Wetterjahre neu auszuwählen. Das System kann invalid/unverifiable melden und eine korrigierte Datei anfordern. Die Auswahl-/Repräsentativitätsentscheidung ist aus jeder aktiven IoSN-Anforderung entfernt.

## Requirements- und Use-Case-Migration

|Alt-Element|Alte Verpflichtung|MA-01-Korrektur|
|---|---|---|
|MR-002 / SR-004|Das Modell produziert selektierte Wetterfälle bzw. Wettermanifest|MA01-SR-010 **übernimmt/validiert** ausgewählte Wetterfälle als externen Input|
|SR-005|PCA-/KMeans-/Auswahlprozess reproduzierbar verifizieren (konditional)|**RETIRED / OUT_OF_SCOPE**, kein aktiver Nachfolger|
|SR-003 / SR-006|Zeitreihen, Wetter- und Zeitschemadaten|MA01-SR-010/-011/-040, nur Daten- und Zeitreihenprüfung|
|UC-01|Weather-year selection / preprocessing|**RETIRED** als IoSN Use Case; historische Demonstration bleibt sichtbar|
|VC-13 und andere Auswahlalgorithmustests|Nachweis PCA-/Clusteringauswahl|**NOT_APPLICABLE** zum IoSN-Contract|
|Roadmap Gate 2|Vollständiges Wetterjahrselektionsverfahren umsetzen|**RETIRED**, nur separater externer Prozess|
|Alle alten SR-001–SR-036|Vorläufiger Katalog aus PR #16|Superseded durch genau 48 aktive vorläufige MA01-SR-IDs; nicht ID-gleichsetzen|

Die zwei MA01-MR-IDs **012** und **049** im Quellenregister dokumentieren Annex 6.3 ausschließlich als upstream Kontext; sie besitzen bewusst keine MA01-SR und keine Verification Needs.

## Bestehende Dokumente: konkrete Impact-Klassifikation

|Bestand im Arbeitsverzeichnis|Widerspruchs- / Abhängigkeitsrisiko|Disposition|
|---|---|---|
|README.md|Frühere Projekt-Landingpage kennt aktive Sprache/PoC und Wetterauswahl als Research Use Case|**REPLACED as MA-01 entry point**|
|01_executive_summary.md|PoC zur Wetterauswahl erscheint als empfohlener erster Schritt|**LEGACY / historical**|
|02_iosn_process_analysis.md|Alte P02/P03 durchlaufen Wettervorbereitung und Auswahlalgorithmus im IoSN-Prozess|**LEGACY; MA-01 P02 nimmt nur Ergebnis entgegen**|
|03_system_requirements.md|Legacy SR-005 enthält konditionale Auswahlalgorithmus-Konformität; SR-004 produziert Auswahlmanifest|**LEGACY; MA01-SR-010 verarbeitet externen Input**|
|04_language_requirements.md|Sprachfähigkeiten noch vor der SyRS-Konsolidierung abgeleitet|**LEGACY; keine LRC-Pflicht in MA-01**|
|05_existing_languages_review.md|Vergleich von SysML/GEMS/CESM/INES als Architekturvorarbeit|**LEGACY non-normative**|
|06_language_capability_matrix.csv|Bisherige LRC-Zuordnung und Architekturvergleich|**LEGACY non-normative; in README klassifiziert**|
|06_matrix_interpretation.md|Interpretiert vorläufige Sprachfähigkeit|**LEGACY non-normative**|
|07_architecture_options.md|Kann eine Architekturauswahl suggerieren|**LEGACY; keine Architekturentscheidung**|
|08_formalisation_use_cases.md|UC-01 Weather-year selection / preprocessing außerhalb neuen Prozessscopes|**LEGACY; UC-01 retired for IoSN**|
|09_verification_traceability.md|Alte VC-Auswahlalgorithmus/Modellnachweise nicht zu neuer MA01-Baseline identisch|**LEGACY; MA01-VN ist aktiver Bedarf**|
|10_poc_specification.md|Historischer Manifest-PoC, keine vollständige Auswahl- oder Energie-Modell-Prüfung|**LEGACY demonstrator**|
|11_critical_review.md|Früherer Review identifiziert Auswahlalgorithmus als Reproduzierbarkeits-Gate|**LEGACY; GATE für IoSN retired**|
|12_architecture_decision.md|Provisorische ADR kann als MA-01 Architekturentscheid missinterpretiert werden|**LEGACY and conditional**|
|13_implementation_roadmap.md|Gate 2 implementiert PCA/KMeans nach Wetterauswahl|**LEGACY; Gate 2 out of scope**|
|source_clause_coverage.csv|Auswahl-Anhang verknüpft mit alter SR-005|**LEGACY historical inventory**|
|sources_inventory.csv|Quellenstatus im alten Forschungskontext|**LEGACY historical inventory**|
|poc/**|Mock Adapter, Validator, synthetische Testfälle und Tests; keine echte Model-/Toolkonformität|**UNMODIFIED; historical demonstration only**|

## Vorgehen bei Legacy-Artikeln

1. README.md ist der aktive Einstieg; sämtliche früheren Markdown-Forschungsberichte werden mit sichtbarem "MA-01 LEGACY" Vorspann und Links auf die neue Baseline geführt.
2. Bestehende CSV-Tabellen bleiben unverändert als **historische Quell-/Sprachforschungsartefakte**. Ihr historischer Status ist im README und in dieser Datei verankert; keine Spalten werden wegen einer nachträglichen Statusumdeutung verändert.
3. Der vorhandene gesamte Ordner poc/ bleibt unverändert, einschließlich Mock-Quellen, Tests und Ergebnisdateien. Die frühen 11/11 synthetischen Outcome-Checks belegen lediglich das damals spezifizierte Testfixture, keine Auswahlalgorithmus-, Netz-, LP- oder produktive IoSN-Konformität.
4. Kein anderes Repository-Verzeichnis und keine bestehende IoSN-Implementierung darf durch MA-01 modifiziert werden.
5. Eine später genehmigte Methodik wird per Änderungsanalyse (Quelle→ID→Akzeptanz) eingepflegt; eine zweite parallele aktive Requirements Baseline ist nicht zulässig.

## Release-/Governance-Regeln

**Quellenhierarchie:** maßgebliche freigegebene ENTSO-E-Methodik (noch unbestätigt) → kontrollierte, explizit als vorläufig markierte MA01-Quellen-/Requirements-Baseline → Forschungsberichte (nur historical evidence). Kein Synthetic-PoC begründet methodische Verbindlichkeit. Neue Baseline erst final einfrieren, wenn externe Methodikautorität und widerspruchsfreie Anforderungen durch einen unabhängigen Review bestätigt sind.
