# ML-C17 — Gemeinsame IoSN-Referenzcontracts RC01–RC12

**Status:** nichtnormative semantische Forschungsdarstellungen, weder ausführbare IoSN-Modelle noch verbindliche DSL. Basis: C08 PR #51 @ 8470add62fcbc7f39b1d90c0d5afdcee50ab811e; C02 PR #42; C06 PR #50. Keine native ReqIF/SysML/GEMS/LinkML/SHACL-Repräsentation erzeugt.

**Einheitlicher Ablauf:** Fachanforderung → Sprachelemente → A/B/C Repräsentation → Implementer-Interpretation → zusätzliche Informationen → Negativfall → potentielle Verluste. A/B/C Darstellungen sind konzeptionelle Rollen-Mappings und dürfen nicht als tatsächliche lauffähige Standardsyntax gewertet werden.

## RC01 — Studienjahre und Wetterfälle

**Fachliche Anforderung:** Y=2035/2040/2050 getrennt; C=CY1..CY5 extern geliefert; w(y,c)=w(c) über dieselbe CY-ID je Jahr; w(c1) muss nicht w(c2) sein; reale Werte sind offen

**Source-SR-Anker:** MA01-SR-002;MA01-SR-010;MA01-SR-011. **Benötigte Sprachelemente (S2):** StudyCase;CaseIdentity;SourceClause;WeightParameter;IndexY/C;EqualityInvariant.

**A / modulare Registry:** Registry-ID RC01 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC01 mit getyptem Scope, StudyCase;CaseIdentity;SourceClause;WeightParameter;IndexY/C;EqualityInvariant, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Y/C Manifest und dieselbe CY-Semantik; kein Selektionsalgorithmus; kein interjähriger Investment-Zwang.

**Offene zusätzliche Informationen:** Numerische Gewichte und deren Norm, verbindliche CY Quellen; O26-Draft-3-CY im Konflikt mit D2-Forschungsprofil-5-CY. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** w(2040,CY3) ≠ w(2035,CY3); CY1..CY5 pauschal auf 0,2 setzen. **Semantisches Verlustrisiko:** Umindexieren/Uniformisieren oder O26 als freigegeben überschreiben.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. D2 Gewicht als Identität, nicht als numerischer Default. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC02 — Nichtantizipative Investition

**Fachliche Anforderung:** x[y,k,s] für alle CY eines Jahres gemeinsam; alternativ x[y,k,s,c] mit expliziter Gleichheitskopplung; Dispatch u[y,c,t] darf variieren

**Source-SR-Anker:** MA01-SR-027;MA01-SR-029;MA01-SR-030. **Benötigte Sprachelemente (S2):** DecisionVariable;InformationStage;IndexSet;Nonanticipativity;Projection.

**A / modulare Registry:** Registry-ID RC02 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC02 mit getyptem Scope, DecisionVariable;InformationStage;IndexSet;Nonanticipativity;Projection, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Gemeinsame erste Stufe und nachgelagerte CY-Rekursentscheidungen; native Kopien brauchen Koppelrestriktionen.

**Offene zusätzliche Informationen:** Kandidaten- und Kostenprofile; ggf. noch offene Stage-Übergabe MD-07. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** x(CY1)=0 und x(CY2)=1 zulässig modellieren. **Semantisches Verlustrisiko:** gleiches Ergebnisobjektiv belegt nicht gleiches zulässiges Investitionsset.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Keine ungebundene Wetterindexierung der Investitionsentscheidung. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC03 — Physikalischer DC-Lastfluss

**Fachliche Anforderung:** KCL pro elektrischem Knoten plus KVL/Netzphysik für PHYSICAL_BRANCH; angle-, cycle- und PTDF-Formulierung nur mit präzisierten Topologie-/Offset-Annahmen äquivalent; LF-Modus behält Impedanzen

**Source-SR-Anker:** MA01-SR-018;MA01-SR-019;MA01-SR-024;MA01-SR-028. **Benötigte Sprachelemente (S2):** PhysicalBranch;Topology;Incidence;KCL;KVL;ReferenceIsland;ModeGuard;Contingency.

**A / modulare Registry:** Registry-ID RC03 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC03 mit getyptem Scope, PhysicalBranch;Topology;Incidence;KCL;KVL;ReferenceIsland;ModeGuard;Contingency, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** bus/branch/topology, elektrische Injektionen, Slack/Angle oder Cycle-Repräsentation, Netzphysik und kontingente Limits.

**Offene zusätzliche Informationen:** Netzimpedanzen, PST/HVDC-Offset, Inselbehandlung, N-1- und Netzreduktionsorakel. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** KCL stimmt, aber im Dreieck ist ein zirkulierender unphysikalischer Flow frei. **Semantisches Verlustrisiko:** alle Branches zu steuerbaren Links zusammenfassen oder LF-Modus als kupferplatte missdeuten.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Differenzierung von physikalischer Masche und Kandidatenmarktlink. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC04 — Steuerbarer DC-Marktlink

**Fachliche Anforderung:** Kandidat ist CONTROLLABLE_MARKET_LINK mit gerichteten NTC Grenzen abhängig von x und möglichen indirekten Effekten, auch wenn geplante AC-Technologie als Attribut notiert ist; keine passiven KVL-Zwänge für Kandidat

**Source-SR-Anker:** MA01-SR-035;MA01-SR-036. **Benötigte Sprachelemente (S2):** MarketLinkRole;TechnologyAttribute;Direction;NTCMap;CapacityBound;Candidate.

**A / modulare Registry:** Registry-ID RC04 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC04 mit getyptem Scope, MarketLinkRole;TechnologyAttribute;Direction;NTCMap;CapacityBound;Candidate, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Variablen für bidirektionalen Marktaustausch mit gerichtetem Ausbauzuwachs, nicht als AC-Mesh-Branch.

**Offene zusätzliche Informationen:** Kandidatenidentität, NTC Richtungsbeiträge, indirekte Wirkungsmatrix und Kosten. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** AC-geplante Marktlink-Kapazität erhält dennoch DC-Branch-KVL. **Semantisches Verlustrisiko:** Technologieattribut mit Modellrolle verwechselt.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Reiner Gleichname Link ist nicht semantisch ausreichend. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC05 — Investitionsstufen

**Fachliche Anforderung:** Stage 1 nur reale Übertragungskandidaten; Stage 2 verbliebene reale, konzeptionelle, theoretische Kandidaten; Stage 3 Speicher ausschließlich 2040/2050; unbekannte Übergaberegel F_y bleibt Owner-TBD

**Source-SR-Anker:** MA01-SR-031;MA01-SR-032;MA01-SR-033. **Benötigte Sprachelemente (S2):** Stage;EligibilitySet;Guard;StateTransfer;DecisionScope;Unknown.

**A / modulare Registry:** Registry-ID RC05 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC05 mit getyptem Scope, Stage;EligibilitySet;Guard;StateTransfer;DecisionScope;Unknown, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Erkennen der Stufen, Fixieren/Übergeben vorhandener Entscheidungen nur gemäß spezifiziertem Regelobjekt.

**Offene zusätzliche Informationen:** MD-07 Stufenübergabe und Kosten F_y, genehmigte Kandidatenstati. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** S2 setzt S1-Kapazität ohne deklarierte Anrechnung zurück; 2035 Speicherneubau. **Semantisches Verlustrisiko:** fehlende methodische Formel fälschlich als Spracheigenschaft oder Nullwert behandeln.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Die Sprache muss unbekannte Regel ausdrücken und blockieren können. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC06 — Speicher

**Fachliche Anforderung:** Charge/Discharge MW; State und Energieobergrenze MWh; eine mögliche Bilanz: E(t+1)=E(t)+eta_c Pcharge(t) Δt - Pdis(t) Δt/eta_d; Grenzen und Endbedingungen müssen source-scoped sein

**Source-SR-Anker:** MA01-SR-033;MA01-SR-034. **Benötigte Sprachelemente (S2):** StateVariable;TemporalSuccessor;Power/EnergyDimension;Bounds;BoundaryPolicy.

**A / modulare Registry:** Registry-ID RC06 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC06 mit getyptem Scope, StateVariable;TemporalSuccessor;Power/EnergyDimension;Bounds;BoundaryPolicy, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Einheitengetrennte Leistungs- und Energieströme sowie Zeitverknüpfung; keine Solverimplementierung vorgegeben.

**Offene zusätzliche Informationen:** Start-/Endzustand, Verluste, Effizienzen, Speicherproxy und Capacity-to-Power Regeln. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** 2 MW in 0,5 h ohne Verluste ergeben fehlerhaft 2 statt 1 MWh. **Semantisches Verlustrisiko:** Normiertes SOC ohne positive Ecap und Definition als äquivalent deklarieren.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Beispielgleichung ist keine Owner-freigegebene Boundary Policy. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC07 — Wasserstoff und Sektorkopplung

**Fachliche Anforderung:** Getrennte MW_e und H2-Energie-/Massenbilanz; Elektrolyse und Rückverstromung mit expliziter Umwandlungsbasis; H2-Netz exogen; P14 nutzt unabhängigen PRE-EXPANSION-Run für stündlichen H2-Freeze

**Source-SR-Anker:** MA01-SR-007;MA01-SR-008;MA01-SR-009;MA01-SR-050. **Benötigte Sprachelemente (S2):** Carrier;Converter;Port;EnergyBasis;ExogenousNetwork;RunDependency;TimeIndexedFreeze.

**A / modulare Registry:** Registry-ID RC07 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC07 mit getyptem Scope, Carrier;Converter;Port;EnergyBasis;ExogenousNetwork;RunDependency;TimeIndexedFreeze, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Elektrizitäts- und H2-Knoten mit gekoppelt begrenzten Energiebilanzen und getrennter Run-Provenienz.

**Offene zusätzliche Informationen:** LHV/HHV, η, Quellen, H2-Topologie, B01-D072 echte pre-expansion reference. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** H2-Pipelineinvestition frei, MWh_e=MWh_H2 ohne η, Sensitivität mit post-expansion Referenz. **Semantisches Verlustrisiko:** Toolnative Carrier- oder Link-Typen können die Semantik nicht ersetzen.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. H2-Basis und Sensitivitätsreferenz sind fachlich wesentlich. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC08 — Preprocessing und Netzreduktion

**Fachliche Anforderung:** Detailliertes Netz → Zonen- und ReducedNetz über versionierte Transformationsregeln; zusammenhängende, disjunkte Partitionszuordnung; extensive Mengen erhalten; PTDF/LODF/N-1 und Kalibriergüte separat prüfen

**Source-SR-Anker:** MA01-SR-016;MA01-SR-017;MA01-SR-019;MA01-SR-022;MA01-SR-023. **Benötigte Sprachelemente (S2):** DataDefinition;TransformSpec;SpatialCrosswalk;GraphPartition;QualityInvariant;Provenance.

**A / modulare Registry:** Registry-ID RC08 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC08 mit getyptem Scope, DataDefinition;TransformSpec;SpatialCrosswalk;GraphPartition;QualityInvariant;Provenance, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Inputs/Outputs, Netzklassenzuordnung, Konservierung und unabhängige Netzäquivalenz-Oracle-Bereitschaft.

**Offene zusätzliche Informationen:** Netz-Source, genaue Reduktionsmethode, Schwellen, detaillierte und reduzierte Netzeigenschaften. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** Aggregierte Lastsumme stimmt, aber PTDF/LODF-Eigenschaften differieren. **Semantisches Verlustrisiko:** TransformSpec als ausgeführte Transformation zählen; RMSE nur als vollständigen E-FEAS Nachweis.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Qualität ist mehrdimensional, nicht ein Label. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC09 — Modelloutputs und Postprocessing

**Fachliche Anforderung:** RawResult → MetricDefinition (Formel, Filter, Version) → DerivedMetric → SystemNeed; B01-D081 KPI-Formel/Schwelle Owner-TBD; SystemNeed ist keine ProjectApproval

**Source-SR-Anker:** MA01-SR-001;MA01-SR-045;MA01-SR-046. **Benötigte Sprachelemente (S2):** RawResult;MetricDefinition;DerivedMetric;Provenance;PublicationGuard;ProjectStatus.

**A / modulare Registry:** Registry-ID RC09 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC09 mit getyptem Scope, RawResult;MetricDefinition;DerivedMetric;Provenance;PublicationGuard;ProjectStatus, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Rohmodellgrößen, berechenbare KPI und publizierbare Bedarfe getrennt ausweisen.

**Offene zusätzliche Informationen:** Reporting-Owner-Freigabe der KPI/Filter/Threshold und veröffentlichbarer Status. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** KPI-ID mit willkürlicher Formel als approved; Bedarf als Investmentprojekt. **Semantisches Verlustrisiko:** Referenzielle Output-Knoten ersetzen nicht Rechen- und Quellsemantik.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. KPI-Ableitbarkeit unterscheidet sich von genehmigter Publikation. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC10 — Verifikation und Evidenz

**Fachliche Anforderung:** Requirement → Test → Oracle → EvidenceRequest; echte Evidence/Run/Reviewer separat. Teststatus exakt PASS, FAIL, BLOCKED, UNSUPPORTED, NOT_EXECUTED, NOT_APPLICABLE. G1/Source/Data-Status unabhängig

**Source-SR-Anker:** MA01-SR-022;MA01-SR-047. **Benötigte Sprachelemente (S2):** VerificationCase;Oracle;EvidenceRequest;Evidence;TestAttempt;ScopedStatus;Review.

**A / modulare Registry:** Registry-ID RC10 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC10 mit getyptem Scope, VerificationCase;Oracle;EvidenceRequest;Evidence;TestAttempt;ScopedStatus;Review, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Zielinvarianten und später zu erbringende Nachweise ohne native Gleichungscode-Vorschrift.

**Offene zusätzliche Informationen:** Autorisiertes Oracle, echtes E04/E05, Reviewer, akzeptierte Toleranz. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** NOT_EXECUTED wird automatisch FAIL oder ein C04 Toy-Test zu produktivem PASS. **Semantisches Verlustrisiko:** Testanforderung/Evidence request mit tatsächlicher Evidence verschmolzen.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Strukturprüfung bescheinigt keine Toolkonformität. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC11 — Optionale OPF

**Fachliche Anforderung:** P15 Guard TRUE/FALSE/UNKNOWN. Nur nachgewiesen FALSE und nicht ausgeführt → NOT_APPLICABLE; UNKNOWN → BLOCKED; TRUE → OPF Ausbau begrenzt durch referenziertes LF-Portfolio und eigene Evidenz

**Source-SR-Anker:** MA01-SR-026. **Benötigte Sprachelemente (S2):** ThreeValuedGuard;Witness;ConditionalObligation;PortfolioRef;Bound;Status.

**A / modulare Registry:** Registry-ID RC11 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC11 mit getyptem Scope, ThreeValuedGuard;Witness;ConditionalObligation;PortfolioRef;Bound;Status, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Unterschied von verpflichtender LF und optionaler OPF; kein freier Skip ohne Proof.

**Offene zusätzliche Informationen:** Freigabe/Aktivierungsentscheidung, LF-Portfolio-ID, Detailrestriktionen MD-08. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** UNKNOWN → NOT_APPLICABLE oder x_OPF > x_LF. **Semantisches Verlustrisiko:** OPTIONAL und NOT_APPLICABLE als gleichwertig deuten.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Nicht ausgelöst ist kein Nachweis für Guard FALSE. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## RC12 — Quellen- und Versionsänderung

**Fachliche Anforderung:** Quellclaim mit Dokumentversion, Clause Locator und Authority; Research D2 fünf CY versus O26 Draft drei CY parallel als Konflikt führen; unveränderte Requirements-ID kann dennoch semantischen Major Change erhalten

**Source-SR-Anker:** MA01-SR-004;MA01-SR-010;MA01-SR-044. **Benötigte Sprachelemente (S3):** SourceClause;MethodologyProfile;SemanticRevision;Conflict;Compatibility;ChangeImpact;EvidenceInvalidation.

**A / modulare Registry:** Registry-ID RC12 mit Requirement-Source-Record; getrennte passende Input/Process/Math/Output/Verification Profile, deren Cross-References und semantischer Versionstupel geprüft werden müssen.

**B / integriertes typisiertes Metamodell:** Ein Contract-Aggregat für RC12 mit getyptem Scope, SourceClause;MethodologyProfile;SemanticRevision;Conflict;Compatibility;ChangeImpact;EvidenceInvalidation, Version/Authority und Validierungspflicht; nicht automatisch eine konkrete mathematische AST-Syntax.

**C / föderierte Standardsichten:** gemeinsames Identitäts- und Autoritätsledger + geeignetes Requirements-/Data-/Process-/Math-/Evidence-View; alle Pflichtoperatoren und Status müssen durch kontrollierte Adapter semantisch wiederherstellbar sein. **Native View/Parser NOT_TESTED.**

**Toolentwickler-Lesart:** Gepinnte Source-/Contract Version, inkompatible Änderung erkennen, alte Zeugen invalidieren.

**Offene zusätzliche Informationen:** MD-01 Methodikautorität, Owner-Signoff, Versionsrichtlinie und Migration approval. Zu klassifizieren als Owner-Entscheidung, externe Daten, kontrollierte Toolwahl oder genuine fehlende Sprachsemantik; nicht pauschal alles als Sprachlücke behandeln.

**Gezielter Negativfall:** 3→5 ohne Profilversion und Wiederverwendung alter PASS-Zeugen. **Semantisches Verlustrisiko:** latest source automatisch approved; durch bloßen SHA formale Gleichheit behaupten.

**Bewertung:** Die relevante fachliche Rolle ist konzeptionell in A/B/C ausdrückbar. Vollständige formale Ausdrucksfähigkeit, native Satzprüfung und Interpretation durch reale unabhängige Entwickler sind **INSUFFICIENT_EVIDENCE**. Governance-Claims und Forschungsprofil sind verschieden. Weder Einfachheits- noch Eindeutigkeitsvorsprung darf aus dem kurzen Pseudotext abgeleitet werden.

## Fallübergreifendes Protokoll und Ausführungsstatus

12 einheitliche fachliche Fälle × 3 alternative **konzeptionelle** Sichttypen = 36 verfasste Mapping-Ansichten; das ist kein nativer Standardroundtrip und keine Ausführung von Optimierungsmodellen.
Die analytischen Gegenbeispiele sind erwartete Negativfälle, nicht Belege einer ausgeführten Sprachvalidierung. Neun atomare, getrennt dokumentierte Positiv-/Negativ-Gegenchecks der ML-C17-Sitzung decken nur ausgewählte Eigenschaften ab (CY, nonanticipativity, Rolle, Einheiten, H2, P15, Source). **G1 BLOCKED.**
