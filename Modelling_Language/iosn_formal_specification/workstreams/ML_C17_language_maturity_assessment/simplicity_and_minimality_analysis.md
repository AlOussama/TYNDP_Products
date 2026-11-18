# ML-C17 — Simplification Experiment S1 / S2 / S3

**Nichtnormative Forschungshypothese.** Reduktion von Anzahl sprachlicher Begriffe nur zulässig, wenn verpflichtende fachliche Bedeutungen vollständig erhalten bleiben. Keine „kompakte DSL“ als Architekturentscheid.

## 1. Gemessener Forschungsgraph

C02 @ 136b35e...: **528 NODE, 1.323 EDGE**, nach struktureller erneuter ML-C17-Prüfung referentiell geschlossen. Es existieren **15 materialisierte Knotentypen** und **14 materialisierte Relationsprädikate**. NODE-Typzählung: MethodologyProfile 1; ReviewStatus 1; GovernanceDecision 27; ProcessStep 18; MathematicalObligation 18; LanguageCapability 20; SyntheticFixture 10; DataObject 87; Transformation 38; IntermediateDataType 20; Requirement 48; SourceClause 48; VerificationCase 96; Oracle 48; EvidenceRequest 48. Relationen: LINKED_TO_PROCESS 87; INCLUDES 38; CONSUMES 123; PRODUCES 55; DERIVED_FROM 48; SCOPED_BY 48; VERIFIES 96; DEPENDS_ON 371; HAS_ORACLE 48; REQUIRES_EVIDENCE 48; APPLIES_TO 74; REFINES 63; REQUIRES_CAPABILITY 68; BLOCKED_BY 156.

Die Instanzen werden überwiegend durch einmalige Identitäten und Kanten, nicht durch 528 Sprachklassen, erzeugt. 96 VerificationCase-**Instanzen** enthalten 48 MA01-VN und 48 native R04-Testplanreferenzen. 27 GovernanceDecision-Nodes und 10 SyntheticFixture-Nodes sind nicht 37 zusätzliche Grammatikregeln. Es fehlt sogar Materialisierung wesentlicher logischer Rollen für mathematische AST, reale DataInstances und tatsächliche Evidence; damit ist der Graph **nicht** automatisch überkomplex **und** vollständig. Das Ziel ist semantische Minimalität, nicht reduzierte Zeilenzahl.

## 2. Drei gestufte Konfigurationen

| Stufe | Vorgeschlagene Kernrollen, nicht geprüfte Mindestzahl | Gegenwärtige Fähigkeit | Nicht zulässig abzuleiten |
|---|---|---|---|
| S1 Minimal Semantic Core | ca. 9 getypte Rollenfamilien: SourceClaim, Requirement, Scope/Applicability, DataReference, Process, Obligation, Output, Verification, Unknown/Authority | stabile IDs, Quellen-/Scope-/Guard-Referenzen, simple Pflicht und Testanforderung | vollständige M01–18 Operator-Semantik, Netzwerkgleichungen, Transformations- oder Provenienz-Ausführung |
| S2 Minimal Complete Scientific Contract | ca. 13–16 Rollenfamilien, S1 erweitert um AssetRole/Carrier, DataDefinition vs Instance, TransformationSpec, MathematicalRule (typed terms), OutputDefinition vs raw, EvidenceRequest vs Evidence, typed units/index/guards | RC01–RC12 *potenziell* in einer getypten wissenschaftlichen Sprache | Formalisierung bereits demonstriert; S2 exakt minimal oder alle SR FULL |
| S3 Extended Governance/Interop | S2 plus OwnerDecision/AuthorityLedger, SourceRelease, ChangeImpact, Migration/Adapter, TransformExecution, Reviewer-/Evidence-Profiles | native Views, ausführbare Release-/Provenienz- und Statusgovernance nach Entwicklung | S3 automatisch bessere Nutzbarkeit oder Pflicht für jeden einfachen SR |

Die Zahlen „9“ und „13–16“ sind **Designhypothesen**, keine präzise belegte Untergrenze. Ein Datentyp kann als Tagged Union statt als physische Klasse existieren. S1/S2/S3 repräsentieren Profile und Abstraktionsebenen, keine drei zu beschließenden Produkte.

## 3. Vereinfachungskandidaten und unverzichtbare Trennungen

**Sinnvoll zu prüfen:** SyntheticFixture als Testdatenprofil statt Kernobjekt; LanguageCapability als Annotation zur Requirement statt 20 Pflichtklassen; MethodologyProfile/StudyCase/Revision als getypte Scope-Werte; 27 GovernanceDecision-Einträge als eigene Versionseinträge außerhalb der Kern-Grammatik; 48 Clause-Referenzen als sourceRef-Records; eine gemeinsame Relation mit typisiertem role/code für strukturell verwandte DEPENDS_ON-Kanten (aber nicht semantische Verwechselbarkeit); OracleRequest/VerificationCase als klar getrennte Subtypen.

**Nicht zusammenlegen:** SourceClaim vs zugelassene Requirement; echte Date/Instance vs DataDefinition; vorgeschlagene Transformation vs ausgeführte Transformation; PHYSICAL_BRANCH (KCL/KVL) vs CONTROLLABLE_MARKET_LINK (NTC); Investition vor CY vs Dispatch nach CY; MW/MWh und H2-Basis; Verpflichtung vs optionaler Guard; RawResult vs MetricDefinition/MetricEvaluation vs SystemNeed vs ProjectApproval; EvidenceRequest vs Evidence; Teststatus vs Owner/G1.

## 4. Semantik-erhaltende Ablationsproben (nur Solltests, nicht ausgeführt)

- Entferne explizites CY-InformationTiming: RC02 lässt wetterfallunabhängige x-Kopplung nicht mehr sicher ausdrücken → **unzulässige Reduktion**.
- Verschmelze Branch und MarketLink ohne Tagged-Role: RC03/RC04 widersprechen sich → **unzulässig**.
- Lösche UNDEFINED_OWNER_TBD: RC05/RC09 erzwingen erdachte Parameter oder nicht berichtbare Lücken → **unzulässig**.
- Ersetze Oracle/EvidenceRequest durch PASS-Flag: RC10/RC11 vermischen nicht ausgeführt, blocked und N/A → **unzulässig**.
- Verschiebe SyntheticFixture aus Kern nach optionales Test-Profil: alle Fachpflichten in S2 bleiben grundsätzlich adressierbar, **hypothesenweise** zulässig.
- Entferne sourceRef/version: RC12 erkennt semantisch inkompatible D2/O26-Aussage nicht → **unzulässig**.

Ein tatsächlicher Minimalitätsnachweis benötigt native A/B/C-Repräsentation **jeder** 48 SR und 12 RC, ein Removal-Test je Kandidat sowie erfolgreiche vollständige Rekonstruktion der unverzichtbaren Invarianten. Als nächster Versuch: S2-Layout zuerst als **Abstraktionsmodell** (keine zwingende B-Architektur), A/B/C gleichberechtigt abbilden, danach Gaps messen.

## 5. Konflikte der Architektur-Stile

A bringt mindestens sieben getrennte Scopes/Profiles mit potenziell mehr versionierten Cross-Refs; diese Fragmentierung ist erst problematisch, wenn sichtbare Semantik fehlerhaft oder unbenutzbar wird. B kann wenige externe Dateien, aber hohen internen Typ-/Migrationsaufwand haben. C kann Standards wiederverwenden, aber zusätzliche Adapter- und Ownership-Komplexität verursachen. Keine echte Wartung, Lernlast oder Releasekosten wurden gemessen.

**Zwischenurteil:** C02 ist als Identitäts- und Traceability-Forschungsgraph angemessen, als minimaler Sprachkern **nicht bewiesen** und als konkrete vollständige Math-DSL **unvollständig nachgewiesen**. S2 ist nur eine Forschungspräferenz für den zu testenden Umfang. **G1 BLOCKED.**
