# ML-C17 — K1–K10 Bewertungsrahmen und Messmethoden

**Forschungsskala, keine genehmigte Standardpolicy.** Bewertet wird die Anforderungen beschreibende Sprache und deren Übergabe an unabhängige Modellimplementierer, nicht PyPSA-/Antares-/Sienna-Ausführung, reale Daten oder produktive Toolzertifizierung.

## Bewertungsobjekte und harte Trennung

(1) Fachanforderung/Autorität, (2) Ausdruck in der Sprache, (3) Interpretation durch Frameworkentwickler, (4) tatsächlicher Toolkonformitätsnachweis. ML-C17 prüft (1)/(2) und Plausibilität des Übergangs (2)→(3). Die Werte 528 Knoten/1323 Beziehungen messen **Instanzen**, nicht Sprachumfang oder kognitive Last.

**Qualität 0–5 (nur als ordinales Forschungsurteil):** 0 nachgewiesener grundlegender Konflikt; 1 stark unzureichendes Konzept; 2 teilweise plausibel mit schweren offenen Punkten; 3 logisch angemessen mit unbewiesenen Details; 4 an echten Sprach-/Validator-Prototypen geprüft; 5 extern reproduzierbar für definierten Scope validiert. Bei fehlender Prüfung NOT_EVALUATED statt 0. A/B/C-CSV enthält **30 hypothesenbasierte** Konzept-Scores, nicht empirische Messwerte; **36 RC Zeilen** sind ausdrücklich NOT_EVALUATED.

**Evidenz unabhängig vom Quality-Score:** E0 keine Evidenz; E1 konzeptionelle Dokumentation; E2 tatsächlich geprüfte IDs/Typstruktur; E3 ausgeführte lokale Custom-Checks mit Negativmutation; E4 native Parser-/Sprachprototypen, semantische Proofs im definierten Scope; E5 qualifizierter unabhängiger externer Review. E2+E3 ergeben nicht automatisch E4; C06 verwendet gemeinsamen Prüfkern.

## A-priori operationalisierte Indikatoren

| K | Messgegenstand und Messmethode | Quell-/Nennerbasis | Aussagegrenze |
|---|---|---|---|
| K1 Einfachheit | primitive Konzepte, Relationstypen, Pflichtattribute, Profil-/Cross-Ref-Zahl; bei nativer Syntax zusätzlich Tokens/Zeilen je identischem Fall und Verständnisfragen | C02 Graph 15 Knotentypen/14 Kantenprädikate; RC01–RC12 | 528/1323 sind keine Lernobjekte; keine Human-Usability-Studie |
| K2 Vollständigkeit | FULL, PARTIAL, REFERENCE_ONLY, NOT_EXPRESSIBLE, INSUFFICIENT_EVIDENCE je ursprünglichem SR, getrennt im Scope; Quotienten jeweils /48; Fälle /12 | Original MA01-48 + C08 + C02 + RC | 48 Referenzen = 0 belegte vollständige formale Ausdrücke, nicht 48 FULL |
| K3 Eindeutigkeit | Zahl unabhängiger semantischer Restentscheidungen je RC und Ursache (LANGUAGE, OWNER, DATA, TOOL_FREEDOM); Interpretation mit zwei Entwicklerparaphrasen | C01/C02 und RC Negativfälle | Gedanklicher Implementer-Handover ist keine reale Entwicklerstudie |
| K4 Toolneutralität | Anzahl Anforderungen, die mit unterschiedlicher nativer Daten-/Modellstruktur semantikgleich implementierbar sind | drei Paradigmen PyPSA, Antares, Sienna, 12 RC | Toolfeature fehlt ≠ Sprachfeature fehlt; praktisch NOT_TESTED |
| K5 Implementer-Handover | pro RC offene Fragen nach Contract-determined, external-data, owner-TBD, acceptable-tool-choice, language-unexpressible | RC + Requirements und Tooldocs | keine Native-Implementierung, keine quantifizierte Handover-Zeit |
| K6 Math | Darstellung der 18 M-Familien: Index/Einheit/Variable/Operator/Invariant/Projection/Testbedarf; negative Differenzierbarkeit | R01-M01–18, C02 math, C04 | synthetischer Kostenwert beweist keine äquivalente zulässige Menge |
| K7 Prüfungen | sechs Prüfebenen, Anzahl statisch erkannter Fehlerklassen mit positiven/negativen Gegenbeispielen; Ablehnung vor Native-Tool | C02 INV01–30, C06 45/45 je A/B/C, C17 lokale Regeln | C06 shared harness; kein unabhängiger Parser oder LP-E04 |
| K8 Evolution | betroffene Referenzen/Verträge bei Source, Unit, Math, Guard und Version Änderung; dokumentierte Reparaturen | C06 8 Mutationen×3; RC12 | keine Migrationsstunden oder akzeptierte Version-Policy gemessen |
| K9 Standards | NATIVE parse-serialize-parse über 2 Standards und modellierter Semantikdiff/Verluste; Zahl IoSN-Extensions | OMG ReqIF/SysML, LinkML/SHACL, GEMS, C06 Gap-Katalog | generischer Standardnutzen ≠ spezifische IoSN-Eignung |
| K10 Governance | Pflicht-Provenienz für SourceClaim, Scope, Release, Test/Oracle, Evidence, Approver; zeugeninvalidierender Change-Diff | C08/C02/C05/C06 | Owner-Signoff und unabhängiger Reviewer fehlen |

## Messwerte aus den Quellen, nicht als Sprachreife verwechseln

- **Graph:** 528 NODE (15 materialisierte Typen), 1.323 EDGE (14 materialisierte Prädikate); darunter 48 SR, 48 Clause, 87 DataObject, 38 Transformation, 18 P, 18 M, 96 VerificationCase, 48 Oracle, 48 EvidenceRequest. In C02 sind AST-Variablen, ConstraintFamilies, echte TransformExecutions und Evidence nicht als vollzählige Sprachobjekte materialisiert.
- **C06:** 45/45 lokale erwartungskonforme Tests je A/B/C = 135/135; 8/8 gezielte Change-Checks je Adapter = 24/24. Standard-native Parser/E04/E05 nicht ausgeführt.
- **C08:** 48/48 MA01-SR referenziert; 86 Trace-Zeilen aus 48 SR, 20 process-only und 18 P. Alle 48 R04-native Tests NOT_EXECUTED.
- **C17:** 48 Coverage-CSV-Zeilen und 66 A/B/C-Vergleichszeilen, davon 36 RC-Zeilen nur konzeptionell; keine messbaren nativen DSL-Token- oder realen Toolentwicklerfragen.

## Verhindern einer irreführenden Gesamtwertung

Keine Gewichtung ohne Begründung und keine berechnete Rangfolge aus 0–5-Hypothesen. Präregistrierte Sensitivität für **spätere** valide Messdaten: (a) gleiches Gewicht für K1–K10, (b) doppeltes Gewicht K1, (c) lexikografischer Vorrang von K2/K3/K6/K7, dann K1, danach übrige. In allen Fällen sind nicht kompensierbare Semantik-Pflichtverletzungen Ausschlusskriterien: CY geteiltes x, Branch/MarketLink, P15, D2, UTC/Δt, Evidence-Status. Ein höherer K1-Wert darf keinen K2-/K6-Verlust ausgleichen.

## Ergebnisstatus und Reproduzierbarkeit

Bereits messbar: Identität, materialisierte Typ-/Relationenzahl, C06 Custom-Harness, Dokument-/Datei-Zeilen und RC-Abdeckung. **NOT_EVALUATED:** reale native Syntaxlänge, unabhängige Lesezeit, Standardparser-Roundtrip, alle mathematischen Operator-Formaltests, reale Migration und Energie-Toolimplementierung. **G1 BLOCKED.**
