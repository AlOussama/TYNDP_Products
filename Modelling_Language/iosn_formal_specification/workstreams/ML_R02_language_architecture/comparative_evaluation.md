# ML-R02 — Comparative Evaluation of A and B
**Version:** Research 0.1 · 2026-11-11 · ohne Methodik-/Datenfreigabe.

## Identischer Testkatalog und Falsifizierungsziel
Der Dateiname `test_results.json` pro Prototyp enthält alle beobachteten Resultate. Beide verwenden dieselben synthetischen Quellen-/Gleichungswerte und dieselben neun fallbezogenen Trace-IDs. Ein Basistest sollte **nur strukturell** bestehen. Jede Mutation zielt auf einen klar definierten semantischen oder referenziellen Fehler. Es wurden **keine** Originaldaten geladen, keine unabhängigen Solver gestartet, keine Toolmodelle übersetzt.

| Fall | Positives Merkmal | Negative Mutation | Erwartung |
|---|---|---|---|
| RC01 | CY1–CY5 für 2035, 2040, 2050; gleiche `w_CYi`; numerische Testbindung sum=1 | geänderte CY-ID / unnormiertes Gewicht | FAIL_CLOSED |
| RC02 | $x_{y,c}$ unabhängig von Wetter, synthetisch gleiche Entscheidung | Wetter in Investment-Index / abweichende $x$-Werte | FAIL_CLOSED |
| RC03 | Physikalischer Zweig $f=b(\theta_i-\theta_j)$, Kandidat NTC-steuerbar | DC-Zweig als NTC / Marktlink als Kirchhoff-Zweig | FAIL_CLOSED |
| RC04 | referenzierte reduzierte Netztopologie, Busmap, sechs **illustrative Labels**, offener Güte-Oracle | Busmap/Provenienz entfernt | FAIL_CLOSED |
| RC05 | P15 als optionales deaktiviertes Profil | aktiviert ohne Cap-Referenz | FAIL_CLOSED |
| RC06 | Bedarf als `SYSTEM_NEED`, KPI-Formel `TBD_OWNER` | Umdeklaration als `APPROVED_PROJECT` | FAIL_CLOSED |
| RC07 | Requirement↔VC-Referenzen konsistent | Referenz zu falschem SR | FAIL_CLOSED |
| RC08 | explizite synthetische Quelle, UTC-Zeitachse, eindeutige Rollen | Quellenreferenz fehlt / Assettyp-Konflikt | FAIL_CLOSED |
| Version | A Profilv0.1.0; B ASTv0.1.0 | nicht akzeptierte Versionsmutation | FAIL_CLOSED |

## Wiederholbare Testauswertung
Die Testfunktionen wurden in einer isolierten ECMAScript-V8-Umgebung ausgeführt. Die **identischen Funktionsdefinitionen** sind im Repository als `node run_tests.mjs` pro Ansatz enthalten; ihre direkte Ausführung mit Node >=18 ist dokumentiert, wurde in diesem Durchlauf aber **nicht separat als Node-Prozess bestätigt**. Die Tests liefern je **14/14 erwartungskonforme Klassifikationen** (1 gültige synthetische Struktur + 13 negative Varianten). Eine erwartungskonforme Negativklassifikation ist kein mathematischer Toolnachweis. Der als gültig akzeptierte Mikrofall führt ausdrücklich `math_conformity=NOT_DEMONSTRATED`.

| Vergleichspunkt | A: Registry + Profile | B: Typed AST |
|---|---|---|
| Lesbarkeit | Fachprofile separat und bearbeitbar, aber Cross-Refs | eine kohärente Objektstruktur, stark verschachteltes Modell |
| Ausdrückbare Math-Semantik | Obligation-IDs + begrenzte Mikrogleichungen, keine allgemeine Algebra | Decision + Branch/MarketLink-Typen, keine allgemeine Algebra |
| Scope & Autorität | D2/O26 Konflikt in Registry | D2/O26 Konflikt im WeatherSet |
| Validierung | Profilversion, Struktur, Referenzen, UTC, Rollen, Toy-Arithmetik | Knoten-/Kantentypen, globale Referenzen, Toy-Arithmetik |
| Optionalität | `process.optional_opf` | `ConditionalStage` |
| Erweiterbarkeit | Einzelprofile je Version, Cross-Profile-Verträge erforderlich | AST-Änderung zentral, entkoppelte Semantikversionierung fehlt |
| Standard-Nähe | JSON Schema, perspektivisch LinkML/ReqIF/mathspec/GEMS | typisiertes AST, perspektivisch SysML/KerML/LinkML |
| Semantik-Beweis | **Nein**: bezogene Quellen-/Netz-/KPI-Oracles fehlen | **Nein**: identische offene Oracles |

## Objektive und offene Kriterien C01–C12
Beide treffen die minimale Forschungs-Traceability (C01), Eingabestruktur (C03), optionale Guard-Form (C06) und Testrepräsentation (C08). C02/C04/C05/C07 bleiben **partiell**: P06 ist nur **deklariert**, LP-Gleichungen lediglich mikrogeprüft; Aggregations-, Bilanz-, Stufentransfer- und KPI-Semantik nicht voll spezifiziert. C09: kein Solverzwang in den Prototypen; **tatsächliche** Toolunabhängigkeit noch durch zwei unabhängige Implementierungen zu demonstrieren. C10: nur Versionsablehnung, nicht Migration. C11: Schema-Dialekte referenziert, **keine** externe Standardparser-Ausführung. C12: governance-/pflegekosten geschätzt, keine Benchmark-Messung.

## Versionstest und Fehlerklassifikation
Versionsänderung allein wird in A wegen Profilpin und in B wegen Modellvertragsversion abgewiesen. Korrekte Folge wäre registrierter Change mit Impact-Analyse über betroffene Requirement/Source/Test/Adapter-Kanten; kein stiller Roll-forward. Im Positivfall muss als übergeordneter Vertragsstatus `BLOCKED_PENDING_METHOD_AND_DATA_ORACLES` gelten, obwohl der synthetische Struktursubtest `PASS_SYNTHETIC_STRUCTURAL` ist.

## Wissenschaftliche Grenzen
Es gibt keinen Reproduzierbarkeitsnachweis für die **vollständigen 48 mathematischen SR**, keine tatsächlichen LinkML-/SysML-/mathspec-/GEMS-Parserläufe, keine Netzreduktion, keinen Optimierer, keine Quellhash-Qualifikation und keinen unabhängig geprüften Soll-/Ist-Vergleich. Beide Validatoren sind kleine projektspezifische Prüfer; gleiche 14 Resultate zeigen weder Funktionsgleichheit noch Sprachäquivalenz. Weitere Benchmarks müssen externe Golden Models, Property-based Mutationen, Round-trip-Differenzen, Laufzeitmessungen und getrennte Expertenreviews einschließen.
