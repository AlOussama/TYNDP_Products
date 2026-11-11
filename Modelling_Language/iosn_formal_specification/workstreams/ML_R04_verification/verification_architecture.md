# ML-R04 — Scientific Verification Architecture v0.1

**Status:** NONNORMATIVE_RESEARCH; no productive certification, no approved source oracle. **Baseline:** BUNDLE-01R PR #25, commit 5c13d4d63f18d30c308997cd7a01f2977fcc6b7b. **G1:** BLOCKED.

## 1. Prüfgegenstand und Claims

Contract-under-test: eine versionierte, toolunabhängige Menge von MA01-Anforderungen, Prozessbedingungen, Achsen-/Datenregeln, mathematischen Eigenschaften, Outputdefinitionen und Nachweisobligationen. Eine Implementierung kann unabhängig in jedem Tool erstellt werden; *kein* direkter M1→M2-Übersetzer ist verlangt.

Separate Aussagen:
1. **Fixture validity:** Sind synthetische Testdaten und berechnete Sollwerte intern richtig?
2. **Property validity:** Erfüllt ein konkreter Tool-Run eine spezifische Pflicht-Eigenschaft auf einem validen Input?
3. **Scope-bound conformance:** Sind alle anwendbaren verbindlichen Anforderungen mit anerkannten Evidenzen und Orakeln erfüllt?
4. **Independent review / normative approval:** Separater menschlich/organisatorisch unabhängiger Audit und zuständige Owner-Entscheidung.

Ein PASS auf Ebene 1 oder 2 impliziert **weder** 3 **noch** 4. Im jetzigen Forschungsstand ist nur Ebene 1 konzipiert und mit Teilrechnungen kontrolliert, nicht 2–4. 48 MA01-SR bleiben vorläufig.

## 2. Verifikations-DAG und Trennung von Quellen

~~~text
Source authority & requirement applicability (owner gated)
       │
       ├── Input data manifest ── V1 ── V2 transformation lineage
       │                               │
       │                         Generated model ── V3 mathematical obligations
       │                               │
       │                         Solver execution ── V4 numerical certificates
       │                               │
       └── Reference KPI formulas ──────┴── V5 independent output/KPI checks
                                               │
                               V6 immutable evidence and review ledger
~~~

**V1** bis **V6** sind orthogonale Nachweisdimensionen; V6 durchläuft alle Schichten. V1-V6 sind keine garantiert streng sequenziellen Rechenschritte: V2 und V3 können unabhängig geprüft werden, doch ein nicht validierter V1-Input verhindert einen vollständigen datenbezogenen Gesamt-PASS.

|Ebene|Unmittelbare prüfbare Assertions|Nachweise|Typisches Gegenbeispiel|Scopegrenze|
|---|---|---|---|---|
|V1 Data & Schema|Schlüssel-Eindeutigkeit, Datentypen, Unit-Semantik, finite Werte, FK/Identität, externer Release, Studienjahr/CY, UTC-Zeit + Δt|Data manifest, Schema-Validator-Protokoll, Quellhash, Zeitindex|Duplikat CY, MW→MWh ohne Δt, fehlende Zone|Numerische Wettergewichte/UTC-Kalenderpolicy owner-TBD|
|V2 Semantic|Asset-Bedeutung, exogen/endogen, Kandidat/Bestand, physikalische AC-Branch vs regelbarer Market-Link, transformierte Erhaltungsgrößen, Prozessvarianten|Source-to-target mapping, semantic witness, Parameterinventar, Transformationsbilanz|Nationale Last bei Disaggregation verdoppelt, H2-Ausbau irrtümlich endogen|Nicht veröffentlichte Domain-Regeln bleiben BLOCKED|
|V3 Mathematical|Zielfunktionsstruktur, Non-anticipativity, KCL/KVL, Multi-Carrier, Kapazitäts-/SoC-Grenzen, LP-Stages, LF und OPF getrennt|Semantische Equation IDs, generierte Koeffizienten, Indexdomänen, Variablenbounds, symbolischer oder projektionserhaltender Nachweis|CY-spezifische First-Stage-Variablen, AC-Kandidatenlink mit KVL gekoppelt|Keine pauschale algebraische Identitätsprüfung|
|V4 Numerical|Primal feasible, angemessenes Optimalitätszeugnis, objektive Nachrechnung, Residuen, Degeneracy/Multiple-Optimum|Solverstatus **und** Rohlösung, unabhängig normalisierte Residuen, feasible/dual-bound/Gap|Solver sagt OPTIMAL, aber KCL-Residuum ≠0|Produktive Toleranzen und Referenzdaten fehlen|
|V5 Output & KPI|Vollständige Rohoutputs, Energie- und Gewichtungsaggregation, korrekte Dimensionen, KPI-Formelversion, unabhängige Rekonstruktion|Roh-CY×Zeit-Werte, Δt, weights, KPI-Code/Version, comparison report|Ungewichtete ENS; Bauentscheid aus Systembedarf abgeleitet|KPI-Formeln und Filter-Schwellen MD-04 offen|
|V6 Conformance Evidence|Run-Identität, Tool/Adapter/Modell/Solver-Version, Daten-/Config-Hashes, ausgeführte Tests, Fähigkeiten, Lücken, Reviewer|Evidence bundle, capability manifest, status ledger, Signaturfeld|Feature als SKIPPED statt UNSUPPORTED|Formal audit / G1-Approval nicht vorhanden|

**Testmethoden je SR:** D0 Struktur/Schema; D1 semantische Assertions; D2 numerische analytische oder metamorphe Referenz; D3 generierte mathematische Verpflichtungen; D4 vertiefte Projektion/Äquivalenz. D0..D4 sind *Prüftiefen*, V1..V6 sind *Gegenstands-Ebenen* – nicht zu verwechseln.

## 3. Fall- und Zeitsemantik als Forschungs-Overlay

D4 des Projekts fordert für jeden der **drei Zieljahrläufe 2035/2040/2050** genau fünf extern ausgewählte Fälle CY1–CY5, mit gleichen numerisch noch offenen Gewichten. Der alte MA01-SR-010-Akzeptanztext nennt dagegen drei Fälle. Der Matrix-Overlay weist auf den Konflikt hin. Keine Neuentscheidung über Wetterselektion, PCA oder K-Means gehört zu ML-R04.

UTC bezeichnet eindeutig normalisierte Zeitinstants; zusätzlich sind Intervallbeginn/-ende oder Dauer Δt, Resampling-Regel, Last-Einheit und Multi-Carrier-Energiebasis explizit zu prüfen. Für jede Leistung P in MW gilt über eine Zeitintervallmenge E[MWh] = ∑ P[MW] × Δt[h]. Fehlendes DST-/Leap-Profil bleibt MD-12, nicht heimlich per Softwaredefault ausgefüllt.

## 4. Atomare Testdefinition und Evidence Traceability

Jeder auszuführende Test erhält:
- **Test ID und requirement ID**, MA01-VN/L4, Quellenrevision und Prozessschritt.
- Gültigkeitsvorbedingung und Variante (required/optional; true/false Antezedens).
- Eingabefixture mit Quellen, Hash und synthetisch vs produktiv.
- Eine scharf formulierte, falsifizierbare Testassertion, eventuell zulässige Realisierungsalternativen.
- Erwartete Evidenzklasse, Vergleichsgröße, Dimension, Orakel-Revision und Toleranzreferenz (numerischer Wert ggf. TBD).
- Positiven Fall und negative Mutation; tatsächliches Executed-at/Status, unabhängige Reviewer-ID nur wenn wirklich vorhanden.

48 originale MA01-SR sind in der **requirements_verification_matrix.csv** mit 48 MA01-VN und individuellen Prüfbehauptungen belegt; **test_catalogue.csv** ergänzt 48 atomare Testentwürfe. Keine generisch automatische L4-Konformität aus dem Quellenfeld verification_method.

## 5. Scientific cross-tool comparison

Vergleiche zunächst **feste Semantik und Invarianten**, dann auf denselben eingefrorenen Eingaben **Feasible Sets unter Projektion**, **Zielfunktion und zulässige Optima**, **KPI-Semantik**, schließlich Tool-spezifische Darstellungen. Ein abweichender Primal-Investitionsvektor ist bei Mehrfachoptima nicht allein ein Verstoß. Umgekehrt beweist gleiche Zielfunktion **nicht** gleiche Modellsemantik.

Synthetische Fälle C01–C10 sind im Unterordner dokumentiert; aufgelistete Gegenbeispiele zeigen, dass passende Endwerte allein mathematische Fehler verdecken können. Generator- und Solve-Evidenz müssen deshalb für SR-018, 027–030, 035 und kritische Prozessbedingungen kombiniert werden.

## 6. Stop-Regeln / Ergebnis

Fail-closed: keine Gesamt-Konformitätsaussage bei offenem Pflicht-Fail, fehlender Pflichtfunktion, ungeklärtem Owner-Orakel oder nicht ausgeführtem Pflicht-Test. Fehlende Quellenfreigaben bleiben **BLOCKED**; veröffentlichte Synthese-Fälle ersetzen keine realen Daten. Alle Tool- und Real-Data-Tests sind **NOT_EXECUTED**; normative/produktive Bewertung **NOT_ASSESSED**; **G1 bleibt BLOCKED**.

**Wissenschaftliche Bezugspunkte (nicht Projektfreigaben):**
- NIST, Conformance Testing: https://www.nist.gov/itl/ai/applied-ai-research-group/conformance-testing
- NIST, What is this thing called Conformance?: https://www.nist.gov/itl/ai/applied-ai-research-group/what-thing-called-conformance
- HiGHS, Feasibility and optimality / KKT, Solver-Toleranzen: https://github.com/ERGO-Code/HiGHS/blob/master/docs/src/guide/kkt.md
- PyPSA, Power Flow (als illustriertes Gleichungsbeispiel, **kein** Referenztool): https://docs.pypsa.org/v1.4.0/user-guide/optimization/power-flow/
