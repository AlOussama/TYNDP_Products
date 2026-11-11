# ML-R01 — Handoff to Contract Design (nichtnormativ, D6-A)

**Stand:** 11.11.2026 · **Gegenstand:** Übergabe einer wissenschaftlichen IoSN-Referenz an eine **spätere**, toolunabhängige Requirements-Sprache und unabhängige Modellimplementierungen. **Kein** Vertragsrelease, kein Architektur- oder DSL-Entscheid, keine operative Freigabe. **G1 BLOCKED**.

## 1. Verbindlicher Forschungsumfang für die Übergabe

Die **48 aktiven vorläufigen MA01-SR** sind laut D1 die alleinige Requirements-Baseline. Alle 18 Prozessschritte P00–P17 sind im Paket beschrieben; 50 MR-Quellenlinks enthalten die zwei upstream-Wetterselektions-MR-012/-049, die **nicht** in aktive SR umgewandelt werden. Die Vorlage ist wissenschaftlich, nicht normativ. Sie spezifiziert **keine** konkrete Toolarchitektur, Serialisierung, API, DSL, Bibliothek, Netzsimulationstechnik oder Solverwahl. D6-A bezeichnet eine gemeinsame **fachlich-semantische** Requirements-Referenz mit getrennt zu prüfenden Implementierungen.

**Quellenprofil:** O26 ENTSO-E 2026 *Version for Public Consultation* vom 25.02.2026 ist die primäre nachweisbare Forschungsreferenz; eine spätere adopted/effective-Version ist nicht bestätigt. Das Projekt-D2-Profil **CY1–CY5, gleiche Gewichte in 2035/2040/2050**, ist ausdrücklich eine **Abweichung** von O26s drei jahresspezifisch gewichteten Fällen. Symbolische Gewichte statt erfundener Zahlen. Keine Wetterselektion. CBA4/H24 sind nur nachgewiesen entsprechend ihrem getrennten Geltungsbereich einzubeziehen.

## 2. Minimaler logischer Contract-Gegenstandsraum — **kein Schemaentscheid**

Ein späterer Contract muss mindestens die folgende wissenschaftliche Semantik *ausdrücken können*. Die Spalte „Ausdrucksfähigkeit“ ist eine **Capability**, nicht eine Entscheidung für YAML, JSON, GEMS, Math-Spec, Sienna oder ein anderes Sprachsystem.

| Semantischer Vertragstyp | Erforderliche fachliche Informationen | Provenienz und wissenschaftliche Eigenschaft | Status |
|---|---|---|---|
| SourceProfile | Dokument-ID, Originalversion, Herausgeber, relevante §§, Geltungsjahr, Status published/consulted/adopted/effective | O26 Draft, MD-01; ältere Quellen als CONTEXT mit Fundstelle und Rechtsrang | CAPABILITY_REQUIRED; RELEASE_TBD |
| StudyCase | Studienjahr 2035/2040/2050, getrennte Laufidentität, Szenariovintage | O26 §3.2, D1 | SCI_DEFINED |
| WeatherManifest | extern ausgewählte CY1..CY5, identische symbolische Gewichte \(\pi_c\), Quelle/Signatur, Datenfamilien | D2 vs O26 §3.7 in getrennten Profilen, Wetterauswahl EXTERNAL | PROFILE_DEFINED / VALUES_TBD |
| TimeCoordinate | UTC-Start/Ende, \(\Delta t\), Quellkalender, Fehlstunden-/Leap-/DST-Behandlung, Repräsentativität | D4, MD-12; MW/MWh-Erhaltung | PARTIAL_DEFINED |
| SpatialIdentity | Detailed-grid Bus, IoSN-Zone, Marktzone, Strom-/H2-Zone, Offshore Hub, Asset-ID, Direction | §§3.3/3.8, P04–P08 | ID_MAPPING_TBD |
| DetailedReferenceGrid | 2025-Netz/Vintage, qualified 2035 projects, Offshore-Ziele, Eligibility-Referenz | §§3.4–3.5, Anhang 6.2, CBA4 nur referenziert | SOURCE_OWNER_TBD |
| ReductionEvidence | Graphpartition/Kontiguität, sechs P06-Parameterklassen, 4 saisonal/richtungsabhängige Ratings, Detailed-vs-Reduced Oracle | §§3.8.1–3.8.3, Anhang 6.1 | ORACLE_TBD |
| SectorSystem | getrennte Strom-/H2-/Storage-/Hydro-/DSR-Bilanzen, Einheiten/Portgrenzen, exogenes H2-Netz | §§3.3/3.6/4.3/4.4 | SCI_PARTIAL; PARAMS_TBD |
| CandidateRegister | Kategorien real/konzeptionell/theoretisch, Zonenendpunkte, ID/RDFID, Marktlänks, NTC-Direction und Expansionbounds | §§3.10/4.5.2; DC **market** links vs physical LF | CAND_MAPPING_TBD |
| EconomicAccount | Kostenjahr, CAPEX/OPEX, VoLL/ENS, Preisszenario, Diskont-/Blockoperator | §§3.1.1/4.6, MD-02 | FORMULA_TBD |
| StageState | S1 reales LP, S2 residual/konzeptionell/theoretisch LP, S3 Speicher nur 2040/2050; Stage-Transition | §3.10; keine freie gemeinsame LP-Zusammenlegung | TRANSITION_TBD |
| ModelMode | LF: Maschenphysik ohne bindende interne Interzonencaps; Paired Dispatch; optional OPF mit LF-Deckel; Frozen-H2 sensitivity | §§3.6/3.9, MD-08/-10 | MODE_DEFINED / DETAILS_TBD |
| MathematicalObligation | O26-/D-/SCI-/ILLUSTRATIVE-/TBD-Klasse, Invariante, mathematische Relation, units, Voraussetzungen | M01–M18; keine implizite Ownerfreigabe | SCI_DEFINED |
| VerificationCase | Source-Version, Inputdataset, Oracle, beobachtete Größen, unabhängiger Reviewer, Residuen, akzeptierte Toleranz | D3, D5-A1, D6-A; MD-15/-17 | DESIGN_ONLY |
| RunEvidence | Input-/Output-Hashes, Modellmodus, Status, Solverergebnis, Kontrollwerte, Abweichungsbericht, Ownerparameter | QA-Evidenz, **nicht** Normadoption durch Structure PASS | NOT_EXECUTED |
| NeedsRegister | Systembedarfs-Definition, Korridor/Land/Offshore, Richtung/Kapazität, Kosten-/KPI-Lineage, kein Projektbeschluss | §§2.1–2.2/3.10–3.11, MD-04/-17 | SEMANTIC_DEFINED / KPI_TBD |

**Grenze:** Der Vertrag darf einen unbekannten Parameter als **TBD** mit Verantwortungs-/Quellenstatus darstellen, ohne dass die Datensprache oder ein Ausführungsprozess daraus einen numerischen Default erzeugt.

## 3. Vertragsverpflichtung ≠ Toolinterne Strategie

| Gemeinsame, wissenschaftlich beobachtbare Verpflichtung | Unabhängig zulässige Implementierungen | Unzulässige implizite Substitution |
|---|---|---|
| Ein \(x_y\) über CY1..CY5, wetterfallgewichtetes \(Q\), Investition einmal | extensive LP vs mathematisch identische Dekomposition | pro Wetterfall getrennte Investments oder Worst-Case/CVaR |
| Physikalisches reduziertes DC-Netz mit Maschengesetzen, kalibrierter Nullfluss-/PST-/HVDC-Wirkung | Winkel- vs PTDF-/Zyklus-Balance, eigenständige Reduktionssoftware | NTC-only-Freiheitsfluss statt physikalischem Bestandsnetz |
| Ausbaukandidaten als steuerbare DC-Marktlinks trotz physischem AC-Technologiehinweis | einzelne vorzeichenbehaftete Linkvariable vs korrekt gepaarte directional Variablen | Kandidat als neue Kirchhoff-AC-Branch |
| Drei **separate** LP-Stufen mit defined Stage1/2 carryforward | verschiedene LP-Solver, Daten-/Szenariozerlegung | alle Stufen als gemeinsames LP lösen, obwohl Entscheidungsklasse verändert |
| Speicher/Hydro/DSR/H2-Erhaltung mit jahres- und wetterfallbedingten Zeitachsen | verschiedene Zustands-/Port-/Einheitenrepräsentationen mit belegter Abbildung | freie Energie, implizite DSR doppelt, H2-Pipelineinvestment |
| P13/P14/P15 als getrennte Untersuchungen mit ausgewiesenen Modellmodi | unabhängige ED-/OPF-Löser, wo gleiches Constraintset | optionalen OPF-Pfad in primäre LF-Analyse einschleusen |
| Methodik- und Report-Ergebnisstatus | beliebige Berichtstemplates/Container | Systembedarf mit genehmigtem Projekt verwechseln |

## 4. Beispielhafte logische Verpflichtungsinstanz (Pseudocode, keine DSL)

~~~text
OBLIGATION M01:
  source = O26 §3.1.1 [draft] + D2 [project research profile]
  applies_to = for each y in {2035,2040,2050}; c in externally selected CY1..CY5
  requires:
    shared investment x[y] for all c
    distinct operational recourse u[y,c]
    objective = investment_cost_once[y] + expectation_c(operating_cost[y,c])
    scenario_weights = identical across y; symbolic pi_CY1 ... pi_CY5
  forbidden:
    scenario-specific free x[y,c], minimax, arbitrary CVaR or substituted weather selection
  evidence:
    source-clause linkage, units, input manifest, mathematical counterexample,
    later qualified optimizer witness and numerical oracle
  current_status = SCIENTIFIC_SPEC_ONLY / MODEL_TEST_NOT_EXECUTED / G1_BLOCKED

OBLIGATION M07:
  source = O26 §4.5.2 [draft] + MA01-SR-035/-036
  applies_to = transmission expansion candidates
  requires:
    controllable market-link flow, directional NTC effects, linear capacity bounds
    explicit relation to existing physical DC-mesh but no forced AC-branch equation
  owner_TBD = MD-09 directional/project mapping and reference case
  evidence = link-feasible-set witness, qualified original candidate mapping
  current_status = SCIENTIFIC_SPEC_ONLY / ORACLE_BLOCKED
~~~

Diese Darstellung dient allein dazu, das **notwendige Ausdrucksvermögen** einer späteren Spezifikationssprache zu erklären. Sie ist **weder** syntaktischer Standard noch maschinenlesbarer Releasecontract.

## 5. D5-A1: testfähige Trennung der Evidenzschichten

| Schicht | Was der Contract später ausdrücken können muss | Was ML-R01 heute liefern kann | Was offen bleibt |
|---|---|---|---|
| E0 SourceAuthority | exakte Methodikversion, Adoption, Geltungsbereich, Hash | O26-Draft/Quellenhierarchie und Version-Delta-Hold | signierter Release/MD-01 |
| E1 SemanticStructure | Typen, Indizes, Dimensionen, Referenzen und 48 SR | Beschreibungen, 115 Trace-Records und 18 P-Schritte | ownerfreigegebene Detailbelegung |
| E2 Mathematics | zulässige Mengen, Restriktionen, Zielfunktionen, Modus-/Stufenregeln | M01–M18, symbolische und illustrative Klassen | endgültige Parameter, Stage2-Operator, Netzorakel |
| E3 WitnessTests | echte kleine LP-/Netz-/Wasser-/H2- und Negativfälle | Risiko-/Gegenbeispieldesign | Originaldaten, freigegebene numerische Grenzen, ausführbare Orakel |
| E4 Independence | getrennte Implementierungen plus unabhängige Review | D6-A-Vorgabe und Kriterien für Vergleich | zwei echte Implementierungen/qualifizierter unabhängiger Reviewer |
| E5 Gate | genehmigte wissenschaftliche/technische/Normabnahme | explizite \`BLOCKED\`-Evidenz | zuständiger späterer G1-Beschluss |

**Bewertungsstatus:** Die Regel **D3 Fail-Closed** bedeutet bei fehlender verpflichtender Evidenz **kein PASS**, nicht automatisch „inhaltlich falsch“. Ein strukturell vollständiges Contract-Objekt kann deshalb \`SPECIFIED\` und zugleich \`NUMERIC_ORACLE_BLOCKED\` sein.

## 6. Übergabe der acht Forschungsartefakte

| Datei | Vollständiger Übergabeinhalt | Erwartete spätere Verwendung |
|---|---|---|
| scientific_methodology_specification.md | Scope/Quelle/Geltung, D1–D6-Profil, wissenschaftliche Kernaussagen, Prozessdiagramm | Domain-/Contract-Modellierungsrahmen |
| process_semantics_P00_P17.md | 18 × neun Prozessfelder mit P-Quellen und SR-/TBD-Bezügen | prozessbezogene Constraint-/Output-/Input-Definition |
| mathematical_obligations.md | M01–M18, Formulierungsvoraussetzungen, Beispielkontraindikatoren und D5-Tests | mathematische Semantik/Orakelvorbereitung |
| methodological_degrees_of_freedom.md | Invarianten, äquivalente Klassen, toolinterne Freiheiten, nicht entschiedene Parameter | späterer unabhängiger Modellvergleich |
| source_and_assumption_traceability.csv | 115 Zeilen, davon 48 SR, 18 P, 18 M, sechs Entscheidungen, 21 MD/CL, vier Historik-/Abweichungsfälle | Provenienz und kontrollierte Coverage |
| unresolved_methodology_parameters.md | 21 offene MD/CL mit Original-Ownerfragen und zwölf Forschungslücken | spätere Entscheidungs-/Freigabekette |
| scientific_review.md | adversarielle Eigenprüfung, 16 offene Forschungs-Findings, Tests und Nicht-Ausführungsstatus | kritische unabhängige Anschlussbegutachtung |
| handoff_to_contract_design.md | semantische Capability-Zielmenge ohne Architektur-/Sprachwahl | Übergangsbriefing für spätere Contractgestaltung |

**Keine** Änderung an bestehenden MA-01-/MA-02-/BUNDLE-01R-Artefakten. Der gemeinsame aktive SR-Katalog ist weiterhin ausschließlich MA01. G1 bleibt BLOCKED.

## 7. Konkrete nachfolgende Prüf- und Forschungsaufgaben (startbar, nicht freigegeben)

1. **Semantic capability mapping:** Prüfe für jede M- und SR-Pflicht, **welche Ausdrucksfähigkeit** eine spätere Requirements-Sprache benötigt (Zeit, Szenario, Bilanz, Stadien, Operatoren, Oracle, Provenienz) — ohne ein Sprachformat festzulegen.
2. **Mathematical micro-fixtures:** Entwirf drei trennscharfe symbolische Testfamilien: (a) gemeinsame Investition/wettergewichteter Betrieb, (b) Dreiknoten-KVL vs steuerbarer Marktlink plus LF/OPF, (c) Storage-/H2-/Hydro-Energiebilanz und stündlicher H2-Freeze. **Keine** numerischen Defaultdaten als „2026-Methode“ deklarieren.
3. **Cross-tool observability:** Lege *als Vorschlag* fest, welche Größen zwei unabhängige Implementierungen für mathematische Vergleichbarkeit offenlegen müssten; kennzeichne optionale vs zwingende Outputs, Mehrfachoptima und numerische Orakel **TBD**.
4. **Evidence trace refinement:** Ordne pro MA01-SR Quelle/M-, P-, Datenfamilie, verifizierbare Invariante und offenes Oracle zu. Die 115 Zeilen sind ein Startpunkt, keine freigegebene L1–L4-Baseline.
5. **Review boundary:** Ein personell unabhängiger Scientific Reviewer kann M01–M18 auf Unvollständigkeit/unnötige Annahmen prüfen; seine spätere Abnahme ist **nicht** durch ML-R01 vorweggenommen.

Die Arbeiten können methodisch unabhängig von ML-R02, ML-R03 und ML-R04 vorbereitet werden. **Keine blockierende Wartebedingung für wissenschaftliche Forschung; keine Aushebelung späterer Owner-/G1-Gates.**

## 8. Abbruch- und Änderungsregeln für spätere Contractreife

Bei einer später positiv identifizierten, freigegebenen Methodikfassung:
- Ursprüngliche Bytes und SHA-256 sowie Adoption, Effective Date, Appendix-/Errata-Geltung einholen.
- O26 zu dieser Fassung klausel- und semantikgenau abgleichen; historische H24-Supplements **nur** dort übernehmen, wo neue Version sie nicht ersetzt und die Übernahme ausdrücklich dokumentiert ist.
- Für 48 SR einen **kontrollierten Änderungsprozess** durchführen, nicht ML-R01-Dateien stillschweigend zur aktiven Baseline erheben.
- D2-Wetterprofil separat auf gültige Methodik und Owner-Entscheidung prüfen; keine erneute Wetterjahrselektion implementieren.
- Detailnetze, eingefrorene Eingabedaten, Gewichtszahlen und Oracle-Parameter **später** fachlich qualifizieren; erst danach sind eigenständige mathematische Conformance-/Tool-Audits verantwortbar.

**Handoff-Fazit:** Die wissenschaftliche IoSN-Referenz ist als *nichtnormatives* Contract-Design-Input vollständig dokumentiert. Sie belegt **nicht** die Normkonformität oder Freigabe einer IoSN-Implementierung. **G1 bleibt BLOCKED.**
