# ML-C18 / 08 – Generalisierungsanalyse des ML-C02/ML-C17-Contract-Kerns

**Quellenfreeze:** ML-C17 @ `c8bbedad390d0ba00604a0f499e79e9cff087138`; ML-C18 SLR01–42/K01–K17 research-r1. Status **nichtnormative Auswertung nach Abschluss der Requirements-/Metrikphase sowie GEMS-/mathspec-Quellenanalyse (ML-C18/01–07)**. Kein neuer normativer IoSN-Contract.

## 1 Ausgangsevidenz und Reife
[Minimal Viable IoSN Contract Language](https://github.com/AlOussama/TYNDP_Products/blob/c8bbedad390d0ba00604a0f499e79e9cff087138/Modelling_Language/iosn_formal_specification/workstreams/ML_C17_language_maturity_assessment/minimal_viable_iosn_contract_language.md) charakterisiert die S2-Semantik als *Forschungshypothese ohne Grammatik/Runtime*. [Simplicity and Minimality](https://github.com/AlOussama/TYNDP_Products/blob/c8bbedad390d0ba00604a0f499e79e9cff087138/Modelling_Language/iosn_formal_specification/workstreams/ML_C17_language_maturity_assessment/simplicity_and_minimality_analysis.md) berichtet **528 NODE und 1.323 EDGE als Instanzgraph**, materialisiert über **15 NODE-Typen und 14 Relationsprädikate**; diese Zahlen sind weder 528 Sprachklassen noch der Beweis einer minimalen Sprache. Die S2-Hypothese umfasst etwa 13–16 semantische Rollenfamilien, keine nachgewiesene Kardinalität. [Formal Language Validation Capabilities](https://github.com/AlOussama/TYNDP_Products/blob/c8bbedad390d0ba00604a0f499e79e9cff087138/Modelling_Language/iosn_formal_specification/workstreams/ML_C17_language_maturity_assessment/formal_language_validation_capabilities.md) unterscheidet V0–V5 und stellt fest: kein vollständiger Typchecker/math Parser, keine native vollständige Konformitätsprüfung. [Language Maturity Brief](https://github.com/AlOussama/TYNDP_Products/blob/c8bbedad390d0ba00604a0f499e79e9cff087138/Modelling_Language/iosn_formal_specification/workstreams/ML_C17_language_maturity_assessment/language_maturity_decision_brief.md) berichtet 20/20 Source-Strukturprüfungen und 26/26 boolesche Mikroprüfungen **im vorigen Forschungsstand**, nicht als in ML-C18 neu ausgeführte Tests. Die originale Methodik, Owner D1–D6, alle MD/CL-Entscheidungen und G1 bleiben unberührt.

## 2 Semantische Elemente: behalten, generalisieren, verschieben, vereinfachen

| Bestehendes Konzept | Generische Bedeutung | Nötige Abgrenzung | Forschungsentscheidung |
|---|---|---|---|
| SourceAssertion | versionierte Behauptung mit Quelle, Klausel, Authority/Status | bloßer Quellenhinweis ≠ verbindliche Anforderung | **BEHALTEN**, kompakte Provenienz-/Authority-Metadaten |
| Requirement | getypte, scopebezogene fachliche Verpflichtung | Input-/Outputpflicht vs Methodenentscheidung | **BEHALTEN**, als Rule/Obligation-Untertyp |
| Scope, Applicability | Zeit, Raum, Szenario, Asset, Guard, Gültigkeit | D2-CY, IoSN Studienjahre nur Profile | **BEHALTEN**, gemeinsame `Context`/Guard-Werte |
| EnergyObjectRole | System- bzw. Komponentenrolle/Carrier | IoSN PHYSICAL_BRANCH vs MARKET_LINK nicht universal als feste Zweiertypenliste | **GENERALISIEREN** zu ComponentRole + domain profiles |
| DataDefinition | Datenidentität, Schema, Unit, Granularity, Qualität | reale Dateninstanz != Definition | **BEHALTEN**, DataInstance/Release optional und unterscheidbar |
| ProcessStep / TransformSpec | vertragliche Pre-/Postprocessing- und Workflowpflichten | P00–P17 / T01–T38 gehören IoSN-Profil | **BEHALTEN** als optionales Process-Profil |
| MathematicalObligation / MathematicalRule | physikalische/optimierungstheoretische Invarianten | konkrete GAMS-/GEMS-/mathspec-Variablen gehören nicht per default in Kern | **GENERALISIEREN** zu invariant/observable property; optionale Math-Spec |
| ResultDefinition | Ergebniskategorien, Einheiten, KPI-Aggregation | SystemNeed/CBA-Maßnahmenranking mit fachlichem Profil | **BEHALTEN**, `Observable`/MetricDefinition/Projection |
| VerificationRequest | Prüfobjekt, Oracle/Proofkind, Evidenzanforderung | EvidenceRequest ≠ tatsächlicher EvidenceBlob ≠ Outcome | **BEHALTEN** mit typed status & provenance |
| Unknown, Owner-TBD | benannte nicht geklärte Quellen-/Methodikentscheidung | darf kein Default und kein FAIL werden | **BEHALTEN**, als Governance DecisionStatus |
| TypedRelations | provenance/refinement/depends_on/applies_to/verification | 1.323 Beziehungen ≠ notwendige Grammar-Operatoren | **VEREINFACHEN** via wenige getypte Relationfamilien |
| StudyCase / Variant | Referenzsystem, Alternative, Vergleichs- und Datenidentität | in ML-C17 primär als IoSN-Cases repräsentiert | **KERNERGÄNZUNG** |
| Component Interface | Ports, direction, carrier, sign, unit, connection, observation | bisher AssetRole ohne vollgetypten A/G-Port-Vertrag | **KERNERGÄNZUNG** |
| Assume-Guarantee / Service | Voraussetzungen, Garantien, Capability vs Safety | nicht nur Portgrenze; Energie-/Stoffledger/Witness | **KERNERGÄNZUNG** |
| VariationPolicy | REQUIRED, PROHIBITED, allowed structure, disclosure | C17 `allowed freedom` noch nicht präzisiert | **KERNERGÄNZUNG** |
| ComparisonContract | identische exogene Basis, KPI-Projektion, R1–R4 | gemeinsame Variable-ID genügt nicht | **KERNERGÄNZUNG** |
| MathematicalProfiles | alternative intern implementierbare Specs | GEMS-/mathspec-Model Library ist nicht Contract Authority | **OPTIONALES PROFIL** |

**Abgrenzung:** `Required/Prohibited` können über `Rule(effect, guard, scope)` dargestellt werden; `PERMITTED/IMPLEMENTATION_DEFINED` in VariationPolicy; `CONDITIONAL` als Guard; `OWNER_TBD` als separate DecisionStatus. Diese Minimalitäts-Hypothese ist *nicht formal bewiesen*. Explizite Differenzierung von Verboten ist wichtig, selbst falls die Syntax eine vereinheitlichte Rule verwendet.

## 3 Verwerfbare oder auslagerbare IoSN-Spezifika
Die folgenden Werte gehören grundsätzlich in versionierte IoSN-Methodikprofile und nicht in den generischen Kern:
- IoSN P00–P17, 38 Transformationen, 87 Datendefinitionen, 48 MA01 SR und R04-Verifikationsreferenzen sind **Instanzen**, keine universellen Grammatikkonstrukte.
- D1–D6-Ownerentscheidungen, offene 21 MD/CL-Fragen, externe Wetterfall-IDs CY1–CY5, konkrete Y=2035/2040/2050 sowie deren Gewichtungs- und Szenariobindung.
- M01–M18 konkrete IoSN-Regeln, physikalische Branch- vs Marketlink-Restriktionen in ihrer IoSN-Parametrisierung, LF-/OPF-P15-Guards, Portfolio-Nachweise und je nach IoSN-Methodik exogene H2-Netzentwicklung.
- `SystemNeed`-/TYNDP-Ausgabekategorien, spezifische Kosten-/Nutzenindizes und Quellenautoritätsprofile.
Die generische Sprache muss ein *Profil mit solchen Regeln* darstellen können; sie muss diese Werte nicht für jede Studie vorschreiben.

## 4 Generalisierung über drei Studienklassen
| Studienklasse | Gemeinsamer Kern | Nur Profilinhalt | Offene Evidenz / Quelle |
|---|---|---|---|
| UC1 IoSN Infrastructure Needs | Studie/Source/Scenario/Component/Data/Process/Output/Evidence/Variation | IoSN-Methodik SR, CY/Y, NTC/KVL, Stages, Referenz-SystemNeeds | vorhandener C17/C08-Katalog, native Interpretation ausstehend |
| UC2 N2E-CBA | Counterfactual, project variants, common data, indicators, time/discounter provenance, comparison | N2E-spezifische Methodikautorität, Indikatorlisten, Bewertungssystem | **N2E authority NOT_IDENTIFIED**; keine fachlichen Defaults |
| UC3 Netzentwicklungsplanung | Network boundary, topology roles, scenarios, asset variants, physical/security guarantees, outputs | spezifisches Regelwerk (N-1 vs probabilistisch, AC vs DC, GridCode, outage requirements) | methodische Quelle vor Pflichtdefinition benennen |

**Generalisierungsgrenze:** Ein Konzeptelement wird nur Kern, wenn mindestens zwei Studienklassen es brauchen und die Notwendigkeit begründet wird, oder wenn eine orthogonale Sicherheits-/Verifikationsregel es unabhängig davon zwingend verlangt. Es gibt keine automatische Aufnahme in den generischen Kern wegen bloßer Existenz im IoSN-Graphen.

## 5 Präzise Lücken relativ zu SLR und K
1. SLR12–20, K02: fehlender formal typisierter Port/Carrier/Sign/Unit sowie explizite Assume-Guarantee-/Capability-/Trace-Semantik.
2. SLR21–26, K03/K05: `AllowedFreedom` besteht bislang semantisch, jedoch ohne maschinenprüfbare Erlaubnismenge, dokumentierte Abstraktionsentscheidung oder Non-equivalence/Equivalence Status.
3. SLR27–34, K07: ein überprüfbarer `ComparisonContract`, Modellstrukturdeklaration, R1–R4-Unterscheidung und Unabhängigkeitsledger fehlen.
4. SLR35–41, K08/K09: vollständige typisierte Unit-Semantik (inkl. Heizwert), Zeit-/Boundary- und Szenarienbaum-/Information-set-Semantik fehlen oder sind nur unvollständig formalisiert.
5. K12/K17: die S1/S2/S3-Minimalität wurde nicht durch systematische Ablation und nicht mit unabhängigen Autorenprüfungen belegt.
6. K14/K16: keine GEMS- oder mathspec-Adapter-/Parser-/Serialization-Validierungen und keine unabhängige Tool-Handoff-Probe.

## 6 Konsequenzen für eine Architekturentscheidung
Der bestehende ML-C17-S2-Ansatz besitzt einen **plausiblen generischen semantischen Ausgangspunkt** (Source/Rule/Scope/Data/Process/Output/Evidence/Unknown). Für Component Contracts und multi-modell Robustheit ist er jedoch noch **unvollständig** und technisch **nicht ausreichend verifiziert**. Ein Beibehalten der *Abstraktionsidee* ist fachlich plausibel; eine Entscheidung für den existierenden Code, eine neue DSL oder ein 528-Knoten-Metamodell lässt sich daraus nicht ableiten. K02–K09 sind vor normativem Einsatz echte Gating-Kriterien.

## 7 Kritische Gegenprobe
Ein Sprachentwurf, der alle 48 IoSN-SRs per Source-ID abbildet, jedoch für RC01 nur `Storage` ohne Energie-Ledger typisiert, ist **nicht** universell korrekt; er ist nur referenziell vollständig. Ebenso ist ein GEMS/mathspec-Parsererfolg ein Nachweis korrekter Grammatik, nicht fachlicher Konformität. Eigentümlich semantische Äquivalenz kann niemals durch Dateiumfang oder Anzahl Graphknoten begründet werden.