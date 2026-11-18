# ML-C17 — Formale Prüf- und Validierungsmöglichkeiten

**Grenze:** Ein Validator prüft, ob ein Contract sprachlich/semantisch korrekt spezifiziert ist. Das beweist weder die Korrektheit einer späteren Optimierungsmodellimplementierung noch den Status der originalen IoSN-Methodik.

## 1. Sechs Ebenen, ihre Fehler und Evidenz

| Ebene | Prüfgegenstand | Prinzipiell auf Sprachebene prüfbar? | Bestehender Forschungsnachweis |
|---|---|---|---|
| V0 Syntax | Grammatik, bekannte Konstrukte, Pflichtfelder und strukturierte Serialisierung | ja, nach Syntaxdefinition | R02/C06 lokale JSON-Daten, keine komplette Contract-Grammatik |
| V1 Typen | Einheiten, Carrier, Indexdomänen, Variable/Parameter, Assetrolle, Time/Stage | ja, soweit statische Regeln vollständig definiert | C02 INV-Register und einzelne C06/C17 Checks, kein vollständiger Typchecker |
| V2 Referenzen | unbekannte SR-/P-/T-/D-IDs, Graphendpunkte, doppelte IDs, Versionstupel | ja | C17 erneuter 528/1323-C02-Join, 48 SR, 87 D, 38 T, 18 P |
| V3 Semantische Konsistenz | D2 Gleichheit über Jahre, M01 nichtantizipative x, P12/15 Guards, Herkunft | teilweise mit vollständig definierten Regeln | C02 invariantenbasiert, C06 shared custom, C17 boolesche Micro-Fixtures |
| V4 Formale mathematische Spezifikation | gebundene Quantoren, dimensional korrekte Ziel-/Nebenbedingungen, physikalische Invarianten, spezifizierte E-FEAS/E-OPT/E-OBS-Projektionen | ausgewählte statische Merkmale ja; allgemeine Äquivalenz nur mit zusätzlichen Annahmen/Beweisen | M01–M18 und C04 Toy-Orakel, kein vollständiger Math-Parser oder E04 native rows |
| V5 tatsächliche Modellkonformität | native erzeugte Gleichungen, Solverwitness, Ergebnis-KPIs, Datenprovenienz, unabhängige Implementierung | nein, benötigt reale Modellartefakte und getrennte Verifikation | 48/48 R04 native Tests NOT_EXECUTED |

**Testoutcome-Status:** PASS, FAIL, BLOCKED, UNSUPPORTED, NOT_EXECUTED, NOT_APPLICABLE. Separat SourceAuthority, DataQuality, ProofStrength, OwnerDecision und G1. Ein noch nicht ausgeführter Test ist nicht automatisch FAIL; ein nicht autorisierter Oracle ist nicht PASS; P15 UNKNOWN bleibt BLOCKED.

## 2. Gezielte Fehlerklassen und Negativbeispiele

| Fall | Erwartete Sprachreaktion | Abgrenzung |
|---|---|---|
| Referenz auf MA01-SR-099 oder nicht vorhandenes DataObject | REJECT REFERENTIAL | Sprache |
| Fehlendes obligatorisches Year- oder CY-Scope | REJECT TYPE/SCOPE | Sprache |
| Draft SourceClause fälschlich OWNER_APPROVED | BLOCK/CONFLICT | Governance |
| w(2040,CY3) verschieden von w(2035,CY3) | REJECT D2-SEMANTICS | Vertragliche Invariante |
| alle w(CY1) bis w(CY5) gleich | ACCEPT, falls übrige Bedingungen erfüllt | Gleichheit verschiedener CY ist **nicht** verboten |
| Investition x(y,c) ohne nichtantizipative Koppelregel | REJECT M01 | mathematische Sprache |
| PHYSICAL_BRANCH ohne KCL/KVL oder Marktlink als passive AC-Masche | REJECT ROLE/PHYSICS | Typ und Domänensemantik |
| 2 MW für 0,5 h werden 2 MWh statt 1 MWh | REJECT DIMENSION/ARITHMETIC | Units |
| frei endogene H2-Pipelineinvestition | REJECT EXOGENOUS-SCOPE | Modellpflicht |
| OPF P15 Guard UNKNOWN meldet NOT_APPLICABLE | REJECT GUARD/STATUS | Sprache |
| OPF TRUE mit x_OPF größer x_LF | REJECT CONSTRAINT | Mathematik |
| frei erfundene Stage-2/F_y Übergabe oder KPI B01-D081 Formel | BLOCKED OWNER_TBD | kein freier Sprachdefault |
| EvidenceRequest ohne echten Versuch führt zu PASS | REJECT EVIDENCE POLICY | Status |
| inkompatible Source-/Math-/Input-Revisionskombination | REJECT/BLOCK VERSION | Sprache/Governance |
| TransformSpec wird als ausgeführter TransformExecution deklariert | REJECT LIFECYCLE | Sprache |
| Originaldata ohne tatsächlich geprüfte Bytes/SourceRelease „qualifiziert“ | BLOCKED DATA | Data Governance |

Diese Reaktionen sind **Sollspezifikationen**, nicht Behauptungen über vollständig ausgeführte Validatoren. Lokale C17-Positiv-/Negativregeln liefern nur schmale Teilbelege; alle 16 Kategorien sind nicht auf einer vollständigen Grammatik durchgeführt worden.

## 3. Nicht auf reinem Sprachniveau nachweisbar

Echtheit und Akzeptanz der Quellmethodik, reale Eingangsdatengüte oder SourceRelease-SHA-256, tatsächlich erzeugte LP-Variablen/Koeffizienten, physikalische Reduktionsgüte für originale Netze, Solveroptimalität, ergebnistreue KPI-Berechnung, E-FEAS/E-OPT/E-OBS im realen Zielmodell, unabhängige Tool-Evidenz und Owner-/Reviewerfreigabe. Eine Spezifikation kann all diese **Nachweispflichten** deklarieren, sie jedoch nicht durch bloßes Parsen erfüllen.

## 4. Experimentelle Grenzen und Architekturunterschiede

A benötigt pro Profil lokale Typprüfung **plus** Cross-Profile-Konsistenz, sonst könnten gültige Einzelprofile zusammen widersprüchlich sein. B benötigt eine durchgehend getypte gemeinsame Semantik **plus** Math-Operatorchecker, nicht nur ein JSON-Schema. C benötigt Native-Standardprüfung, zentrale semantische Autorität, verlustfreien Roundtrip und semantisches Verlustprotokoll. Keiner der drei Prototypen hat dies vollständig belegt.

Als Sprachvalidierungsreife ist ein unabhängiger Parser-/Typ-/Semantik-Check über die 12 identischen Referenzfälle sowie tatsächlich zurückgewiesene Mutanten nötig. Dieser Schritt erfordert **keinen** produktiven Solverlauf. Das nachfolgende reale Toolkonformitätsgate ist gesondert.

**Votum: FORMAL_VALIDATION_READINESS = PARTIAL_STATIC_RESEARCH_ONLY; G1 BLOCKED.**
