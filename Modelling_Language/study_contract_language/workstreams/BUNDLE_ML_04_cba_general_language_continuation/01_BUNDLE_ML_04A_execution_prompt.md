# MAKRO-BUNDLE BUNDLE-ML-04A
## General Study Contract Language — B1 Interface Closure, Typed Semantics & Interchangeable Method Profiles

**STATUS:** EXECUTION PROMPT — NOT YET EXECUTED.
**GOVERNANCE:** NON-NORMATIVE / RESEARCH ONLY. Independent critical review required; no owner sign-off, production compliance, architecture selection, merge or G1 approval.

### 1. Rolle und Ziel
Agiere als koordiniertes Expertenteam aus Senior Sector-Coupled Energy-System Modelling Architect, Formal Language/DSL & Canonical-Semantics Expert, Mathematical Specification & Verification Expert, Data/Method Governance Architect, Software Interoperability Architect, SysML v2/KerML/GEMS/mathspec Reuse Expert und Independent Critical Research Reviewer. Trenne Erstellung und kritische Prüfung; ein KI-interner Review ist kein unabhängiger menschlicher Audit.

**Ziel:** Die *allgemeine* Study Contract Language (SCL) technisch in eine ausführbare, strikt typisierte Schnittstelle überführen und die CBA als EINEN synthetischen Stresstest einsetzen. **CBA ist weder Sprachscope noch Architekturvorgabe.** Die ENTSO-E 4th CBA Guideline dient als versionierte fachliche Referenz, nicht als fest eingebauter Algorithmus.

### 2. Verbindliche Nutzerentscheidungen
1. Allgemeine SCL beibehalten; die CBA-Methodik als referenzierte, versionierte Quelle nutzen.
2. Vollständige Sprachkette zuerst mit synthetischen CBA-Daten prüfen; erst danach verschiedene Energiesystemmodelle vergleichen.
3. B1 und B2 priorisieren; native SysML/KerML-, GEMS- und mathspec-Untersuchungen parallel, ohne B1/B2 dadurch zu blockieren.
4. Noch offene Regeln sind **versionierte und ausdrücklich markierte Forschungsannahmen** bis zur fachlichen Freigabe.
5. **Keine Methodik oder Methodenparameter im Sprachkern/Validator fest verdrahten.** Methodische Formeldefinitionen, KPI-Definitionen, Diskontierungsannahmen, Zeithorizonte, Szenariogewichte, Fallselektion, Währungs-/Preisjahrkonventionen und Quellenpräzedenz müssen als extern verwaltete, typisierte, validierbare und austauschbare Methoden-/Studienprofile darstellbar sein. Ein Wechsel zwischen bereits unterstützten Profilen darf keine Codeänderung erfordern. Neue nicht unterstützte Operatoren als expliziten Erweiterungsbedarf melden, statt Freitext oder Code-Injektion zuzulassen.

### 3. Repository und unveränderliche Baseline
Repository: AlOussama/TYNDP_Products.
- B0/ML-C19: 2f0297b754e3a96a2523a34d3af98782b26181f3 (PR #55).
- ML-C20: b81edeb7551aa786e0d309ccd5bc2271d244e450 (PR #57).
- ML-C21: cad6d30edf32476ee5e915dbea7566127cbffa5f (PR #59).
- ML-C22: 828c87eb100646da6fcce5f8751af5f3f42c7600 (PR #58).
- ML-C23: d3d5362231d81a00fd6a19501bc7187f4ad12da5 (PR #56).
- ML-C24-P1: 506be1607e1e8a6eb50db2f1317961d5bbaffcce (PR #60).
- ML-C24-P2: 01f4eb798aff5391a51aff2365e6841850907464 (PR #61).
- ML-C24-P3: 0e85be6d9d2a84dffd7bb2685e6548671be3ef17 (PR #62).
- ML-C24-P4: 4b61addb0e87205e6670e253bd65cb0428e08681 (PR #63).
- ML-C24-P5: eaea6dd99b736f2560866abda722cde78b908bce (PR #64).
- Mathspec/GEMS: die in P3 definierten externen Quellpinnungen ermitteln und unverändert dokumentieren.
Verifiziere die tatsächlichen Referenzen/HEADs vor Beginn. Neue Ergebnisse gehören in getrennte Forschungsbranches/Draft-PRs, abgeleitet von B0 mit expliziten Source-Pins, ohne alte Draft-PRs umzuschreiben oder zu mergen. Bestehende RC01-RC10, SLR01-SLR42, NFR01-NFR18, K01-K17, C1-C9, R00-R13 und E1-E5 bleiben erhalten.

**Methodenquellen:** ENTSO-E 4th CBA Guideline (https://tyndp.entsoe.eu/resources/guideline-for-cost-benefit-analysis-4.0); TYNDP 2026 Implementation Guidelines (https://consultations.entsoe.eu/tyndp/tyndp-2026-cba-imp-public-consultation/); TEN-E (EU) 2022/869. Ermittle Dokumentversion, Publikations-/Freigabestatus, Retrieval-Datum und Dateihash. Entwirf keine nicht belegten ENTSO-E-Schwellen oder owner-genehmigten Rechenregeln.

### 4. Vier koordinierte, getrennte Workstreams

#### ML-C24-N1 — Ausführbarer B1-Schnittstellenabschluss (P0)
- Vergleiche C20 Candidate A/B, C21 Validator und P1 Bridge auf Syntax, Version, AST-Felder, Mengen/Units, Ports, Bool3/Scopes, Authority, Evidence und Audit.
- Implementiere **realen Candidate-A-Parser** (keine EBNF-Behauptung als ausführbarer Parser) und streng typisierten Candidate-B-Decoder; beide auf einen dokumentierten AST/CSNF-Schnittstellenvertrag. Keine stille Umbenennung, ungültige Fallbacks, untypisierte Escape-Hatches oder Akzeptanz doppelter JSON-Schlüssel.
- Führe tatsächlich die positive RC01-Probe und einen typisierten CBA-Basisvertrag durch: Syntax -> Parser/Decoder -> AST -> CSNF -> unverändert gepinnter C21-Python-Validator -> prüfbare Status-/Audit-Ausgabe. Führe zusätzlich das ursprüngliche negative RC01 und neue Typ-/Versions-/Authority-/Unit-Mutationen aus.
- Prüfe deterministische Normalisierung, verlustarme semantische UND separate Audit-Projektion, Roundtrip soweit definiert; Ablehnung fremder Prädikate statt Freitext. OWNER_TBD bleibt BLOCKED.
- Liefere maschinell ausführbare Tests, exakte Kommandos, Runtime-/Dependency-Versionen, reproduzierbare Logs, Fehlertaxonomie, Coverage-Denominator und einen konservativen B1-Gate-Bericht.

#### ML-C24-N2 — Generische Prädikate, Observables und konfigurierte Methoden (P0)
- Spezifiziere **allgemeine**, typisierte Operatoren/Kompositionsregeln für referenzierte Fallpaare, geteilte Exogenitäten, Zeit-/Szenariomengen und -gewichtsrollen, Aggregation, diskontierte Projektion, KPIs, Auswahlregeln, Units/Price Base, Guard/Scope/Quantoren, Evidenzstatus und VariationPolicy.
- Untersuche für jeden Kandidaten zuerst Komposition bereits vorhandener Operatoren und Wiederverwendung; neue Primär-Operatoren nur mit Gegenbeispiel, Minimalitätsbegründung und Nicht-CBA-Wiederverwendung. Keine fest eingebaute CBA-Algebra.
- Entwirf einen **extern versionierten MethodProfile/StudyProfile-Kontrakt**: method_id, schema/operator version, source_uri + exact version/hash, publication/approval state, owner authority, assumptions, expression AST/rules, parameter schema + units/ranges, price-year and currency basis, scenario weight roles, applicability/scope, dependency references, immutable resolved run-snapshot, provenance/evidence signatures.
- Beweise experimentell die Austauschbarkeit mit mindestens **zwei ausdrücklich synthetischen, methodisch verschiedenen Profilen** (z.B. verschiedene Diskontierungskonventionen oder Aggregationsregeln): gleiche Parser-/Kern-/Validator-Binaries, nur externe Profil-/Parameterdateien wechseln, absichtlich nachvollziehbar geänderte Ergebnisse, unterschiedliche Provenienz- und Versionsidentitäten. Konfigurationsänderung darf keine Quellcodeänderung, Rebuild oder Deployment des Sprachkerns erfordern.
- Negativtests: Einheit-/Dimensionsfehler; unzulässige Währung/Preisjahr-Kombination; fehlende/inkonsistente Szenariogewichte; ungültige Referenz-/Projektpaarung; Doppelzählung; inkompatible Operatorversion; ungelöste Methodenreferenz; abweichende Hashes; Owner-/Evidence-Promotion; unerlaubte dynamische Ausführung. Unbekannte Operatoren = UNSUPPORTED/BLOCKED, niemals vermeintlicher PASS.
- N2-Design startet parallel zu N1; ausführbare N2-Integration verwendet erst die eingefrorene N1-Schnittstelle.

#### ML-C24-N4 — Native Standards-Reuse und SysML-H0 (parallel, P1)
- Isolierte, gepinnte native Experimente für SysML v2/KerML, GEMS und mathspec; Profile/Imports und Export-Reimport mit demselben CBA-Kernfall, mindestens einem nicht-CBA-Komponentenfall und Methodenwechsel.
- Werte C1-C9, Typsemantik, semantischen Verlust UND separaten Authority-/Audit-Verlust aus; vergleiche Profilumfang, benötigte Zusätze und native Ausführbarkeit. SysML-H0 darf weder ohne native Tests widerlegt noch allein wegen eines fehlenden Parsers bestätigt werden.
- Wenn Installations-/Runtime-Zugang fehlt: reproduzierbaren Preflight, Blocker und Status NATIVE_NOT_EXECUTED dokumentieren. Keine gefälschten native Testresultate.

#### ML-C24-N5 — Generalitäts- und Modelling-Freedom-Kontrollen (parallel, P1)
- Bewahre unabhängige RC01 Batterie, RC02 EV, RC03 Elektrolyse, RC04 H2-Speicher, RC05 Netz, RC07 Informationsbaum/Nichtantizipativität und die übrigen RCs als explizite Abdeckungsmatrix.
- Prüfe externe Assume-Guarantee-Verträge, Port-/Carrier-/Unit-Invarianten, zeitliche/quantifizierte Service-Semantik und zulässige Variationen der internen mathematischen Formulierung. Teste positive/negative synthetische Beispiele.
- Zeige, dass gemeinsame Verpflichtungen nicht zu identischen internen Gleichungen oder Solverstrukturen zwingen. Ergebnisgleichheit allein = kein allgemeiner E4-Beweis. Ungeprüfte RCs bleiben offen.

### 5. Koordination, Artefakte und Review
N1/N2 priorisiert; N4/N5 parallel ohne Gate-Umgehung. Jeder Workstream erhält eigenen Research-Branch/Draft-PR und dokumentiert exakten Ausgangs-SHA; keinen integrierten ML-C24-PR erstellen. Gemeinsame Austauschobjekte: versioniertes AST/CSNF-Schema, Operator-/Type-Registry, MethodProfile-Schema, synthetische Daten, immutable Testmanifeste, ausführbare Logs, getrennte semantic/audit digests, Authority/Evidence-Register, SLR/NFR/K/RC Traceability, kritische Gegenprüfung und offene Blocker.

Ergebnisse müssen strikt als EXECUTED, DESIGN_ONLY, SYNTHETIC, NOT_EXECUTED, BLOCKED oder PROVED (nur mit echten Beweisen) klassifiziert werden. Konkrete Limitierungen und Tests niemals als geschlossen ausgeben, wenn sie noch offen sind.

### 6. Abnahme-Gates und Übergabe an BUNDLE-ML-04B
- B1 kann erst MET sein, wenn beide vereinbarten Syntaxpfade ausführbar sind, die echte gepinnte C21-Python-Schnittstelle aufgerufen wurde, fachlich getypte positive und relevante negative Fälle korrekt behandelt werden und Semantik/Audit/Authority erhalten bleiben. Ein reiner JS-Mikrotest oder nur Candidate B = B1_PARTIAL.
- Method-Swap ist **eigenständiges Muss-Kriterium**: mindestens zwei externe versionierte Profile ohne Codeänderung; Quell-/Versions-/Evidenzbindung; negative Konfigurationsprüfungen.
- N4/N5 werden vollständig dokumentiert, dürfen B1 nicht künstlich verzögern. B2 bleibt bis zum vollständigen Sprachbenchmark aus 04B PARTIAL; B3 bleibt NOT_READY und G1 BLOCKED.
- Übergabe: ein maschinenlesbarer Gate-/Evidence-Report mit den tatsächlich ausgeführten Tests, dem eingefrorenen Schnittstellenkontrakt und den 04B-Startvoraussetzungen. Falls blockiert: präzise Blocker statt Scheinabschluss.

**Beginne die zulässigen Arbeiten in diesem Bundle jetzt, ohne weitere Rückfragen bei technisch auflösbaren Detailfragen.**
