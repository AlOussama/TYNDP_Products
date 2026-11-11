# ML-R04 — Proposed risk-based Conformance Policy v0.1

**Status:** Nichtnormativer Entwurf gemäß Projektentscheidung D5-A1. Keine universelle Forderung nach algebraisch identischen Formulierungen; keine Freigabe.

## 1. Risikodefinition und gegenläufige Risiken

Die **fachliche Tragweite** einer falschen Eigenschaft, ihre **Fehleranfälligkeit** (Konvertierung/Indexierung/Einheiten/Generator) und die **Entdeckbarkeit** durch reine Output-Tests bestimmen die Tiefe. Nicht allein die Laufzeit. Besonders gefährlich ist ein stiller Formulierungsfehler mit plausibler Zielfunktion (C02) oder eine KCL-erfüllende, aber KVL-verletzende Lösung (C04).

Arbeitsregel für die **48 vorläufigen** MA01-SR: B01R-Baseline-P0 ⇒ A; B01R-P1 ⇒ B; B01R-P2 ⇒ C. **Unabhängig vom P-Ranking** werden mathematisch kritische Pflicht- oder konditionale Invarianten **SR-003, 007, 009, 018, 024, 026–030, 031–035, 041, 042, 050** auf A angehoben. Ergebnis der nachvollziehbaren *Forschungszuordnung*: **A=33, B=12, C=3**. Noch kein vom Owner freigegebenes Risiko-Assessment; Priorität und Risikoklasse bleiben getrennte Matrixfelder.

|Tier|Fachliche Gefahr|Minimale geplante Nachweise – falls anwendbar|Beweisgrenze|
|---|---|---|---|
|A (kritisch)|Falsche Systembedarfe, Bilanz, Sektorkopplung, Investment-/Netzsemantik, Quelle nicht rekonstruierbar|D0+D1; D2 (analytisch/metamorph), bei mathematischen Eigenschaften D3; D4 nur bei auslösendem Äquivalenzrisiko; V6 in jedem Fall|Verpflichtende fachliche Invarianten dürfen nicht durch erfolgreiche End-KPIs ersetzt werden|
|B (signifikant)|Falsche Prozesskonfiguration, zeitliche/oder semantische Abbildung|D0+D1, D2 bei Ergebnisbezug, D3 bei generatorisch verpflichtender Formel; V6|Einfacher Outputvergleich ohne Dimensionsprüfung unzureichend|
|C (kontrollierbar)|Dokumentations-/Scope-/Basissemantik|D0+D1+V6, Stichproben und Mutationskontrolle|Nicht als pauschale Ausnahme von Mandatory behandeln|

**Wichtig:** Die individuelle Spalte minimum_test_depth in der Matrix präzisiert notwendige Ebenen und kann für manche nichtmathematischen A-Anforderungen weniger als D3 umfassen. Ein leerer D3-Nachweis ist nicht PASS, falls tatsächlich eine D3-relevante Pflicht besteht.

## 2. Prüftiefen, Operationalisierung und Trigger

- **D0 — Structural/Schema:** deterministische Keys, JSON/CSV-Form, Pflichtfelder, Einheiten und FK; gegen kaputtes Fixture testen.
- **D1 — Semantic:** begutachtete Bedeutung, Bilanzkonservation, Zuordnung und Variantenabhängigkeit; Umbenennung von Feldern alleine kann keinen PASS liefern.
- **D2 — Synthetic numerical reference:** analytisch auswertbare Fälle, harte Gegenproben, metamorphe Konservation, separate Daten-/Modelldimensionen; Skalierung und Δt beachten.
- **D3 — Generated obligations inspection:** unabhängige Begutachtung von generierten Variablen, Bounds, Indexmengen, Constraint-Familien und Zielfunktionskoeffizienten. Keine Textgleichheit von Modell-Dateien.
- **D4 — Deep equivalence:** symbolische Transformation, Projektion (ggf. bidirektionale Beweisführung), Gegenbeispielsuche, Dualgrenzen oder Exhaustion nur *kleiner* diskreter Fixtures. Kein generelles 1:1-AST-/Algebra-Screening.

**D4-Trigger im aktuellen Research-Katalog:** SR-017 (elektrisches Äquivalent), SR-018 (Winkel/PTDF/Zyklus), SR-019 (N−1), SR-027 (Zielfunktions-/Discount-Alternativen), SR-029 (gemeinsame Variablen vs Nonanticipativity-Gleichungen), SR-035 (Marktlink-Semantik). Ergänzende Trigger: hoher Output-Unterschied bei gleichen validen Eingaben, unerklärtes KPI-Mismatch, fehlende Constraint-Provenienz, mögliche Relaxation, Kandidaten-/Kosten-Mapping oder math-projection-Änderung.

## 3. Begrenzte Conformance Claims

**Claim C-DATA:** V1 + relevante V2 + V6; sagt nichts über LP.
**Claim C-SEMANTIC:** V2, relevante V3, Referenz-Oracle und V6.
**Claim C-MATH:** V3 und ausreichende D2/D3/D4-Nachweise; gleiche LP-Objective-Werte alleine nicht ausreichend.
**Claim C-NUMERIC:** V4 für einzelne Instanz, inkl. primal residual, unabhängig nachgerechneter Zielfunktion, optimality evidence.
**Claim C-RESULT:** V5 für definierte KPI-Revision.
**Claim C-FULL:** Konjunktion *aller anwendbaren* mandatory Claims mit freigegebenen Orakeln; hier nicht erreichbar.

Die sechs Achsen dürfen getrennt PASS/FAIL/BLOCKED/UNSUPPORTED/NOT_EXECUTED/NOT_APPLICABLE tragen. Ein Claim muss Scope (Quellenstand, Studienjahre, Cases, Feature-Set, Tool-Version) angeben; keine unqualifizierte Bezeichnung „tool conformant“.

## 4. Grundsätze der Bewertung

1. **Pflicht bleibt Pflicht:** Fail-closed bei FAIL, BLOCKED, UNSUPPORTED und NOT_EXECUTED. Verifikationstiefe ist eine evidenzbegründete Entscheidung, keine Aushebelung.
2. **Optional ist konditional:** Für SR-026 mit OPF=false und *nachgewiesener Nichtausführung* NOT_APPLICABLE. Bei OPF=true sind mathematische Kandidatenkappen verpflichtend; fehlende Fähigkeit ⇒ UNSUPPORTED.
3. **Nichterfüllung vs. Nichtprüfbarkeit:** Ein vorhandener KCL-Gegenzeuge ist FAIL. Fehlende Owner-Toleranz ohne nachgewiesene Verletzung ist BLOCKED. Ein nicht gestarteter Test trotz bereitstehender Voraussetzungen ist NOT_EXECUTED.
4. **Fehlersuche mit Mutanten:** Für kritische Eigenschaften muss ein absichtlich fehlerhafter Generator von mindestens einem geeigneten Test erkannt werden; andernfalls die Sensitivität des Testkatalogs offenlassen.
5. **Ebenen nicht kompensierbar:** Mehr PASS bei V1 ersetzen kein V3; Übereinstimmung mehrerer Tools ist keine unabhängige mathematische Wahrheit.
6. **Keine künstliche Norm:** Realweltliche Quellen-/Economic-/Netz-Grenzwerte und numerische Toleranzen TBD; keine erfundenen Prozentschwellen. Die 0,2 aus C01/C08 sind lediglich synthetisch.

## 5. Rigorose Freigabebedingungen später

Vor einem vollständigen Profilclaim: (i) maßgeblicher Methodik-/Anforderungsstand autorisiert, (ii) Daten und native Transformationen mit Hash qualifiziert, (iii) per Requirement anwendbare D0–D4 sowie V1–V6-Obligationen mit anerkanntem Orakel geschlossen, (iv) offene MD/CL, besonders MD-02/03/04/07/08/09/12/15/17/18, entschieden, (v) echte Tool- und numerische Läufe mit nachvollziehbarer unabhängiger Reviewer-Attestation. Ein vorläufiger wissenschaftlicher Prototyp darf unabhängig davon fertiggestellt werden.

### Risikopolitik vs. Produktivstatus
Diese Dokumentation definiert *künftige* Testtiefen; sie autorisiert nicht den Start eines Zwei-Tool-Piloten oder G1/BUNDLE-02. Aktueller Conformance-Status **NOT_ASSESSED**; bestehender G1-Status **BLOCKED**.
