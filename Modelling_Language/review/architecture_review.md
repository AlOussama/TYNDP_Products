# Unabhängiges Architektur-Review — Modellierungssprachen und Interoperation

**Review-Stichtag 23.10.2026. Status:** kritische Desktop-/Primärquellenprüfung; **vorläufig**, keine unabhängigen Konformitäts- oder CBA-Mehrtool-Experimente.  
**Scope:** TYNDP-/NEP-Interoperabilität und Prozess-CBA; IoSN-Implementierung ist ausdrücklich ausgeklammert.  
**Auftragsgrundlage:** `../REVIEW_PROMPT.md`, insbesondere `` 1, 2, 5–10, 13–14. Status aller 14 Kapitel: [review_status.md](review_status.md).

## Executive Summary

**Bestätigt/hohe Plausibilität:** Datengleichheit ≠ Mathematikgleichheit ≠ Verhaltensgleichheit ≠ Vergleichbarkeit einer Planungsentscheidung. Der obligatorische Kern einer heterogenen CBA muss Eingangssemantik, Szenarioidentität, Einheiten, Referenz-/Projektfall, Methoden- und Transformationsidentität und KPI-Formeln definieren. Eine externe semantische Norm kann *interoperable Vergleiche* unterstützen, ohne alle Tools zur gleichen Modellgleichung zu verpflichten.

**Wichtige Gegenposition:** Wird strikte mathematische 1:1-Konformität verordnet, ist eine gemeinsame mathematische Normalform (B) effizienter und prüfbarer als A+; bei zugleich legitimer Modellvielfalt kann B+ besser sein. A+ erlaubt Variationen, garantiert aber nicht, dass unterschiedliche Modelle fachlich dieselbe CBA-Frage beantworten. Eine vollständige B-Referenz kann zudem unentdeckte Common-Mode-Fehler verbreiten. Aus identischen Solver-Ergebnissen folgt keine Entscheidungsrobustheit.

**Entscheidende Befunde:**
1. [F01] Conformance und Robustheit müssen in **getrennten Experimentdesigns** nachgewiesen werden.
2. [F02] Konverter können fachlich wesentliche Funktionen stillschweigend ignorieren. Konkreter Primärbeleg: `PyPSA-to-GEMS-Converter/COMPATIBILITY.md` dokumentiert `Enforced=No` unter anderem für bestimmte Multi-Port-/Komponenten- und Parameterfälle [S05].
3. [F03] CBA benötigt ein **gepaartes** Referenz-/Projektfall-Design pro Modell, Szenario und Methode. Das Gegenmodell M2 darf weder mit M1s Referenzfall gemischt noch ohne Kennzeichnung als unabhängig bezeichnet werden.
4. [F04] B1 (SEW, `5.1) und B6 (Adequacy, `5.6) haben verschiedene Methoden- und Stichprobenanforderungen [S01]. Die 2026er Ergänzungen sind nur für den **nachweislich geprüften Entwurfsstand** heranzuziehen [S02].
5. [F05] GEMS ist als formale Optimierungs-DSL nicht per se über-spezifiziert; als universeller verpflichtender Austauschvertrag für alle TYNDP-/NEP-Workflows kann diese Annahme überzogen sein. Ob ein zusätzlicher semantischer Minimalstandard wirtschaftlicher ist, ist offen.

**Bedingte Entscheidung:** A+ als *Startprofil für heterogene Tool-Interoperation* pilotieren, B als mathematisches Conformance-Profil gezielt ergänzen und B+ für regulierte alternativ-methodische Profile testen. Kein Architektur-Go, bevor kritische Konvertierungsverluste ausgeschlossen, KPI-Methoden gemeinsam definiert und mindestens zwei unabhängige Modelläufe gepaart verglichen wurden.

## 1. Prüfbegiffe (nicht synonym)

| Begriff | Zu prüfende Aussage | Minimaler Nachweis |
|---|---|---|
| Requirements Clarification | Welche fachliche Frage und welche Norm-/Methodenfassung gelten? | signierter, versionierter Planning/Comparison Contract |
| 1:1 Translation | Struktur, mathematische Gleichungen und Werte werden erhalten | Round-Trip + symbolischer/LP-Mikrotest + Capability-Bericht |
| Interoperation | Ein Toolverbund führt eine fachlich korrekte Prozesskette oder vergleichbare unabhängige Läufe durch | referenzierte Übergaben, KPIs, Daten-/Methoden-Lineage |
| Conformance | Zwei Implementierungen interpretieren **dieselbe** freigegebene Formulierung korrekt | gleiches algebraisches Modell + unabhängige Generatoren + Ergebnis-/Residualtests |
| Methodische Robustheit | Zulässige Modellmethoden verändern Schlussfolgerungen nur innerhalb vordefinierter Grenzen | factorial/paired Methodensensitivität, Fehler- und Abweichungsdiagnostik |
| Decision Robustness | Projektwahl oder Ranking bleibt gegenüber wesentlichen Unsicherheiten tragfähig | Entscheidungsstabilität, Regret, Schwellen, Gegenbeispiele |
| Numerische Stabilität | Rechenverfahren verändert die Lösung bei Toleranzen/Skalierung nicht unvertretbar | Toleranz-/Solver-/Seed-Tests |
| Reproduzierbarkeit | Gleicher Run kann wiederholt werden | Versionen, Seeds, Eingaben, ausführbares Manifest |

**Wichtiger methodischer Unterschied:** unabhängige Solver für dasselbe LP liefern vorrangig numerische/Implementierungsprüfung, **keinen Test verschiedener physikalischer oder ökonomischer Methoden**.

## 2. Kritische Prüfung H1–H8

| Hypothese | Stärkstes Argument dafür | Stärkstes Gegenargument | Evidenzbedarf | Urteil / Vertrauen |
|---|---|---|---|---|
| **H1 A+** verbessert Robustheit heterogener CBA | unabhängige Mathematik deckt Modellstruktur-Risiken potenziell auf | frei variierende Methoden erzeugen unvergleichbare KPIs; hoher Governance-Aufwand | zwei Toolmodelle mit identischem Contract + methodischem A/B-Test | **eingeschränkt / mittel** |
| **H2 B** prüft mathematische Konformität, nicht gemeinsamen Fehler | exakte Gleichungen sind zwischen Engines falsifizierbar | unterschiedliche Compiler können Fehler aufdecken; Referenz kann physisch validiert werden | gemeinsames Fehler-Injection-Beispiel in zwei unabhängigen Engines | **konzeptionell bestätigt / hoch** |
| **H3 B+** kann bei normierten Prozessen überlegen sein | freigegebene Referenz und getrennte Variantenprofile bieten eindeutige Vergleichsgrundlage | Zulassung/Governance kann Kosten und Methodefreiheit aufheben | Profil- und Kostenvergleich gegen A+ | **offen / mittel** |
| **H4 GEMS über-spezifiziert** | Pflichtmathematik im Austausch bindet Tools an einen Modellansatz | für 1:1 ausführbare Mathematik ist das genau der Zweck und kein Mangel | CBA-Prozesscontract vs. GEMS-Funktionsumfang und Übersetzungstests | **nur relativ zu Daten-Exchange plausibel / mittel** |
| **H5 sieben Komponenten minimal** | Bus/Load/Generator/Storage/Line/Link/Converter sind leicht zu implementieren | generische Balance/Port/Process/Connection-Klassen erweitern sich konsistenter; physische Netztopologie braucht Spezialprofile | Verlusttests für Strom/H2/Wärme + CGMES-Projektion | **offen / niedrig** |
| **H6 Compiler ersetzt Modellgenerator, nicht gesamtes Tool** | DSL→Algebra/LP deckt Modellgenerierung ab | solverseitige Semantik und Tool-Pipelines sind komplex; Compiler kann auch Workflowfunktionen aufnehmen | reproduzierbarer Compiler-gegen-Tool-Test für begrenzte Klasse | **eingeschränkt / mittel** |
| **H7 Common-Mode-Fehler und stille Adapter-Differenzen** | Fehler in gemeinsamer Algebra propagieren; dokumentierte Konverterverluste existieren | unabhängige Unit-/Physics-/Empiriechecks können Fehler finden | absichtlich fehlerhaftes Modellschema + Loss-Report-Test | **bestätigt als Risiko / hoch** |
| **H8 gleiche Daten/KPI-Namen reichen nicht** | Referenzfall, Gewichtung, Aggregation und SEW-Definition beeinflussen Werte | bei strikt definiertem eng begrenztem Modell können standardisierte Daten genügen | CBA-KPI-Doppelrechnung mit/ohne Harmonisierung | **konzeptionell bestätigt / hoch** |

Die Urteile „konzeptionell bestätigt“ sind **keine experimentellen Produktzertifizierungen**.

## 3. Kandidaten: Rollen statt Scheinkonkurrenz

| Artefakt | Primärrolle | Aus dem Quellenstand begründete Stärke | Nicht daraus ableitbar |
|---|---|---|---|
| **GEMS** [S04] | objekt-/graphorientierte ausführbare Optimierungs-DSL | explizite mathematische Modellierung; Antares und GemsPy als Interpreter genannt | generelle fehlerfreie Tool-zu-Tool-Äquivalenz, vollständige CBA-Methodik |
| **G-PST CESM** [S06] | sektorübergreifender Daten-/Methoden-Hub auf LinkML | Balance, Unit, Storage, Commodity, Link; deklarierte Methoden | algebraische Gleichheitsgarantie; Referenzintegrität vollständig im Schema |
| **INES/ines-spec** [S07, S08] | Datenaustausch und Transformationsworkflows | interoperabler Parameter-/Szenariorahmen | verlustfreier bidirektionaler Austausch: PyPSA-Adapter nennt Einschränkungen |
| **SiennaSchemas** [S09] | versionierte, typisierte Schemafamilie | OpenAPI-Datenmodelle für Topologie, Operation, Investitionen, Zeit | vollständiger toolneutraler Mathematical-DSL-Contract; Versionen <1.0 sind pre-release |
| **energy-models/mathspec** [S10] | YAML-beschriebene Optimierungsspezifikation | schematischer Ausdruck von Dimensionen, Parametern, Variablen, Gleichungen | reife Multi-Engine-Konformität; Projekt nennt Alpha-Status |
| **DynamicalSystemsGroup/MSML** [S11] | mathematische/verfahrenstechnische Spezifikationsabbildung | JSON, Block-/Wiring-Reports, optionale Python-Funktionen | gleichzusetzen mit energy-models/mathspec oder als LP-Translator vorauszusetzen |
| **CIM/CGMES** [S12] | elektrische Netzmodellprofile | spezifizierter TSO-Netzmodellaustausch und Konformitätsprofile | vollständige CBA-Markt-/Wohlfahrtsmathematik |
| **IAMC/pyam, OEO** [S13, S14] | Szenario-/Ergebnisformate und Ontologie | definierte Variablen-/Einheits-/Begriffsschicht | LP/MILP-Interpretersprache |

**Wichtiger konkreter Gegenbeleg zu „verlustfreier GEMS-Normalisierung“:** In [S05] sind stille Nichtübernahmen dokumentiert, u.a. `Process`, zusätzliche Link-Ports und ausgewählte Parameter. Der entsprechende Adapter muss daher explizit **FAIL** oder **DECLARED_LOSS** liefern; die GEMS-Sprache selbst ist damit nicht widerlegt.

## 4. GEMS-These differenziert

- **Austauschvertrag:** vollständige Algebra kann unerwünscht sein, wenn Modellmethoden legitim unabhängig bleiben sollen.
- **Mathematische Normalform:** Gleichungen, Zielfunktionen, Stochastik und zeitliche Indizierung sind **notwendig**, wenn *tatsächlich* mathematische 1:1-Konformität verlangt wird.
- **Prozessvertrag:** selbst ein vollständig spezifiziertes LP schreibt nicht automatisch die CBA-Grenzen, Referenznetzversion, Projektgegenfälle, Aggregationslogik, B1-/B6-Berichtspflichten, freigegebenen Varianten und Entscheidungsregeln fest.
- **Möglicher Fehlentwurf:** „wir lassen Mathematik aus dem Austauschvertrag heraus“ darf nicht dazu führen, dass Adapter sie per implizitem Default neu erfinden.
- **Maßgebliche Abgrenzung:** `model_id` (Daten-/Strukturmodell), `method_id` (verwendete Formulierung), `engine_id`/`capabilities` (Implementierung) und `planning_contract_id` (Planungsfrage) sind unabhängige Identitäten.

Weitere Architekturdiagramme, Mindestklassen und Sensitivitätsgewichtungen: [../analysis/architectures.md](../analysis/architectures.md).

## 5. Fünf getrennte Review-Runden (Desk Review, keine Experimente)

| Runde | Fragestellung | Befund | Ausstehender Nachweis |
|---|---|---|---|
| R1 Requirements Clarification | Was muss CBA verbindlich gleich bleiben? | F03/F04: Projekt-/Referenzfall, Version, KPI-Bedeutung fehlen als explizite cross-tool Contracts | Abstimmung und Normfreigabe |
| R2 1:1 Translation | Welche Semantik fällt bei Konvertierung weg? | F02: Primärquellen zeigen dokumentierte stille Konvertierungslücken [S05,S08] | Round-Trip + LP-/Constraint-Diff |
| R3 Interoperation | Kann eine Toolkette CBA vollständig übertragen? | F03/F06: unabhängiger Modellvergleich ≠ sequentielle Übergabe | Marktergebnis→Netzmodell + Back-Mapping-Test |
| R4 Independent Validation/Robustness | Was überprüft die jeweilige Modellvielfalt? | F01/F07: Solver-Diversität ist keine Methodendiversität | 2 Methoden × 2 Szenarien × paired CBA |
| R5 Red Team | Wann versagt A+? | B/B+ überlegen, wenn strikte Mathematik/Nachvollziehbarkeit verordnet ist; A+ scheitert bei verdeckten Defaults | regulatorischer Freigabetest + Aufwandmessung |

Die Runden sind **inhaltliche Prüfpfade**, nicht fälschlich als erfolgreich ausgeführte Tooltests dargestellt.

## 6. Vorläufige Schlussfolgerung

**Zwingend gemeinsam:** fachliche Identitäten/Ports/Commodities/Einheiten, Auflösung und Gewichtung, Modell-/Methoden-/Szenario-/Provenienzidentität, explizite Transformationen und Verlustregeln, Referenz-/Projektfall sowie **KPI-Semantik und Vergleichslogik**.

**Optional oder use-case-spezifisch verbindlich:** mathematische Referenzprofile mit Gleichungen, Variablen, Ziel, Randbedingungen, Solverfähigkeiten und Interpreter-Conformance-Tests.

**Absichtlich unabhängig für Robustheit:** zugelassene, transparent deklarierte alternative mathematische Methoden, Modellstrukturen und unabhängige Implementierungen. Variationen müssen so eingeschränkt werden, dass die *Planungsfrage* invariant bleibt; anderenfalls darf kein gemeinsames CBA-Ranking publiziert werden.

**Entscheidung ausdrücklich nicht abschließend:** Siehe [ADR](../analysis/recommendation_adr.md), [Findings](findings.md), [CBA-Szenariofälle](../analysis/cba_interoperation_scenarios.md) und [Quellen](../sources/bibliography.md).
