# MAKRO-BUNDLE BUNDLE-ML-04B
## General Study Contract Language — CBA End-to-End B2 Validation, Comparative Reuse & Architecture Readiness

**STATUS:** CONDITIONAL EXECUTION PROMPT, NOT YET EXECUTED.
**START-GATE:** Only start substantive B2 integrated execution after inspecting the actual BUNDLE-ML-04A handoff and its B1 interface contract. If B1 remains PARTIAL, conduct only clearly labelled preparatory/blocked research and do NOT assert B2_MET/B3_READY.

### 1. Rolle und Forschungsfrage
Agiere als Expertenteam aus Formal-Language/Typed-CSNF Architect, Sector-Coupled Energy-System Modeller, CBA/Counterfactual/Indicator Expert, Mathematical/Scientific Verification Expert, Test/Mutation/Benchmark Architect, Software Interoperability & Data Governance Expert, Human Factors/Usability Researcher sowie Independent Critical Scientific Reviewer.

**Forschungsfrage:** Kann eine ALLGEMEINE Study Contract Language eine methodisch frei konfigurierbare, synthetische CBA-Studie vollständig und überprüfbar beschreiben, ohne die interne Mathematik unterschiedlicher Energiesystemmodelle zu normieren? Welche Ausdrucks-, Interoperabilitäts-, Minimalitäts- und Verifikationsgrenzen sind mit reproduzierbaren Tests tatsächlich nachgewiesen?

ENTSO-E 4th CBA Guideline = VERSIONIERTE FACHLICHE REFERENZ; CBA = STRESSTEST/USE CASE; allgemeine SLR/NFR/K/RC bleiben unverändert. Methodik, Szenariogewichte, Diskontierung, Preisjahr/Einheit, KPI-Definitionen und Annahmen sind austauschbare Profile, KEINE hart codierten Konstanten oder CBA-spezifischen Sprachkern-Funktionen. No owner-approved CBA/compliance claim.

### 2. Ausgangsquellen und verifizierbarer Start
Repository: AlOussama/TYNDP_Products.
Verwende die in BUNDLE-ML-04A dokumentierte unveränderte Baseline und tatsächlichen Ergebnis-SHAs. Unveränderliche Forschungsreferenzen:
- B0 ML-C19 = 2f0297b754e3a96a2523a34d3af98782b26181f3.
- ML-C20 = b81edeb7551aa786e0d309ccd5bc2271d244e450; C21 = cad6d30edf32476ee5e915dbea7566127cbffa5f; C22 = 828c87eb100646da6fcce5f8751af5f3f42c7600; C23 = d3d5362231d81a00fd6a19501bc7187f4ad12da5.
- P1 = 506be1607e1e8a6eb50db2f1317961d5bbaffcce; P2 = 01f4eb798aff5391a51aff2365e6841850907464; P3 = 0e85be6d9d2a84dffd7bb2685e6548671be3ef17; P4 = 4b61addb0e87205e6670e253bd65cb0428e08681; P5 = eaea6dd99b736f2560866abda722cde78b908bce (PR #64).
- Original ML-C23-Golden-RC01–RC10 plus 18 registrierte Mutationen und original P5 30 Negativmutationen unverändert halten. Neue Testrevision separat versionieren.
- ENTSO-E original document/version/publication status/hash in der 04A-Quellenregistratur pinnen, ohne die konkrete Methodik als genehmigt zu fingieren.

Vor der Ausführung: B1-Status und Schnittstellen-SHA prüfen, MethodProfile-Schema/-Version fixieren, Testdenominatoren vorab registrieren, Machine/Runtime/Dependency-Voraussetzungen festhalten. Keine stillschweigende Schemamigration.

### 3. ML-C24-N3 — End-to-End-Validierung der Sprache (P0, abhängig von N1/N2)
1. Baue mindestens eine **vollständige synthetische CBA-Studie** mit Projekt/Referenzpaaren pro Szenario und pro Modell, Zeit- und Szenarioidentität, getypten Gewichten, gemeinsamem Input-Snapshot, Einheiten/Währungs-/Preisjahresregeln, CBA-Indikatoren, Aggregations-/Diskontierungsregeln, fehlenden/nicht monetarisierbaren Indikatoren, Input- und Ergebnisprovenienz, Owner-/Evidence-Status und zulässigen Modellvariationen. Keine offizielle Benefit-Berechnung vortäuschen.
2. Durchlaufe für **beide unterstützten Syntaxkandidaten** real und vollständig: source -> Parser/Decoder -> typed AST -> CSNF -> pinned validator -> semantic/audit normalisation -> Report. Vergleiche das semantische Ergebnis, separate Authority/Audit-Digests, Versions- und Quellenidentitäten sowie Fehlermeldungen. Ein eingeschränkter alleiniger Candidate-B-Lauf ist kein vollständiger Dual-Candidate-Nachweis.
3. Integriere das ursprüngliche C23-Golden-Protokoll **RC01–RC10** in soweit formal unterstützter und vollständig deklarierter Form. Bewahre auch Kontrollfälle außerhalb der CBA: EV, Batterie, Elektrolyse, H2, Stromnetz, Nichtantizipativität, mathematische Freiheitsgrade.
4. Führe **alle ursprünglich 18 C23-Mutations-IDs** und **alle ursprünglich 30 P5-CBA-Negativmutationen** über die echte Sprachkette aus, soweit deren getypte Repräsentation überhaupt möglich ist. Weise pro Mutation die erwartete Fehlerklasse, tatsächliche Erkennung und die genaue Stelle der Kette aus; nicht portierte Tests = NOT_EXECUTED, nicht PASS. Ergänze gezielte Methoden-Konfigurations-Mutationen aus N2.
5. **Methodik-Austauschbarkeit als ausführbaren Regressionstest:** mindestens zwei verschiedene synthetische MethodProfile/Parameter-Snapshots; gleicher unveränderter Sprachkern/Parser/Validator-Code und gleiche Binaries; Profilwechsel durch externen Referenz- und Parameterwechsel; erklärbar unterschiedliche Indikator-/NPV-Resultate; unverwechselbare methodische Provenienz. Eine unerwartet unveränderte Kennzahl oder ein stiller Fallback ist Fehler, kein impliziter Pass.
6. Prüfe E1–E5 **jeweils mit korrekt begrenzter Nachweistiefe**: Darstellung/Normalform, Vertragskonformität, Observable-Eigenschaften, Feasible-Set-/mathematische Äquivalenz und zulässige Modellvielfalt separat. Gleiche KPI = weder E4 noch Modellkonformität. Ein fehlender unabhängiger Solver-/Zwei-Tool-Pilot erlaubt keine realen E4/E5-Aussagen.
7. Dokumentiere sämtliche ausgeführten Positiv-/Negativtests mit reproduzierbaren Aufrufkommandos, Inputs, Fehlercodes, Checksums, Versionslocks, Erfolgs-/Blocker-Matrix und unabhängigem Fachorakel. Definiere B2-Teil- und Gesamtabschluss nur für tatsächlich getesteten Geltungsbereich.

### 4. ML-C24-N6 — Architektur-/Minimalitäts-/Usability-Evaluation (P1; erst nach vergleichbaren Builds)
- Evaluiere A: modulare Registry/Views, B: integriertes typisiertes Metamodell, C: föderierte CSNF-Referenzen, H0: kleinster tragfähiger SysML/KerML-Standardprofilansatz. Ergänze GEMS-/mathspec-Reuse ohne Scheinvergleich; benutze **IDENTISCHE RC/CBA-Daten, Oracle-Erwartungen und methodische Profile**.
- Erfasse K01–K17, NFR01–18, SLR01–42 mit vorab fixierten Messdefinitionen und vollständigen Nennern; technische Metriken: Typ-/Operatorumfang, Anzahl zusätzlicher Primitive, Ausdruckslänge, Schema-/Versionsaufwand, semantischer vs Audit-Verlust, Parser-/Validierungsfehler, Reproduzierbarkeit, Profilwechsel-Aufwand, Authoring-Zeit und Verständlichkeit.
- Prüfe Minimalität nicht anhand einer isolierten Klassenanzahl. Nutze kontrollierte Ablationen, Reifikationen, Komplexität und Gegenbeispiele; Generalität muss RCs unabhängig von CBA einschließen.
- Eine unabhängige Autor*innenstudie/Blind-Interpretation **nur bei tatsächlich durchgeführter Teilnahme** als empirisch ausgeben; andernfalls NOT_EXECUTED und Konsequenz für K-Metriken. KI-interne Rollen gelten nicht als menschlich unabhängiges Review.
- Erstelle einen vergleichenden Evidenzbericht mit pro Ansatz: implementiert/ausgeführt/nicht verfügbar, gemessene Fähigkeiten und Verluste, minimaler zusätzlicher Profilumfang, Reuse-Wirkung, Grenzen und Unsicherheit. Keine gewichtete Gesamtnote ohne explizit begründete und freigegebene Gewichtung.

### 5. Bedingte ML-C24-Integration — nur bei echten Gates
Erst nach **B1_MET plus wissenschaftlich hinreichendem, scope-klaren B2-Nachweis** darf ein separater integrierter ML-C24-Forschungsbranch begonnen werden. Er muss:
- Source-Pins und alle Audit-Evidenz der Teilstudien konsistent zusammenführen;
- dokumentieren, welche Metriken/Gates wirklich MET bzw. PARTIAL/NOT_READY sind;
- zwischen folgenden konditionalen Voten unterscheiden: EXISTING_STANDARD_SUFFICIENT, MINIMAL_OWN_CORE_JUSTIFIED, FEDERATED_CSNF_JUSTIFIED, HYBRID_PROFILE_RECOMMENDED oder EVIDENCE_INSUFFICIENT;
- fehlende SysML-native/Human-/Modellbeweise explizit berücksichtigen;
- keine Architektur oder eigenständige DSL vorschnell freigeben und G1 grundsätzlich BLOCKED belassen, bis reale Ownerentscheidungen vorliegen.

Falls B1 nicht MET oder B2 nicht hinreichend: **keinen integrierten ML-C24-PR eröffnen**, stattdessen Gate-/Blockerbericht und objektive Wiederanlaufbedingungen.

### 6. Erwartete Ergebnisse und Qualitätsregeln
Neue Research-Branches und Draft-PRs getrennt nach N3 und N6; keines der ursprünglichen C19–C23/P1–P5-Artefakte ändern oder mergen. Pro Arbeit: Quellen- und Testmanifeste, lauffähige Tests soweit Umwelt verfügbar, Evidence-Register, unabhängige kritische Überprüfung, aktualisierte SLR/NFR/K/RC/E1-E5-Matrizen, Verlierer-/Negativfallanalyse, Gate-Entscheidung und reproduzierbare Handoffs. Entscheidung über neue generische Primitive nur mit Kompositions-/Reuse-Gegenprüfung.

### 7. Abnahmekriterien
**B2_MET** nur wenn die vorher festgelegten durchgängigen Sprach-/RC-/CBA-Nachweise, relevante negative Fälle, typisierte Methodik-Austauschbarkeit und Traceability tatsächlich ausgeführt und entsprechend dem vereinbarten Validierungsumfang bestanden wurden; Einschränkungen/E2–E5 explizit. **B3_READY** nur bei reproduzierbarem, metrisch vergleichbarem, kritisch überprüftem Architekturvergleich. Sonst PARTIAL/NOT_READY; G1 BLOCKED.

**Führe alle nach Start-Gate zulässigen Forschungsarbeiten ohne weitere Rückfragen durch; für blockierte Arbeiten präzise Voraussetzungen dokumentieren.**
