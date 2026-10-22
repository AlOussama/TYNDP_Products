# Reviewbericht — Interoperation von IoSN-Teilprozessen unter A, A+, B und B+

**23.10.2026 · Evidenzbasiertes Desktop-Review, keine ausgeführten Multi-Tool-Läufe.**  
Methodische Primärreferenz: ENTSO-E `TYNDP 2026 Identification of System Needs Methodology` **Konsultationsfassung vom 25.02.2026** [S01], `3.1, `3.7–3.10, `5.1, Annex 6.1/6.3. Kein Nachweis einer finalen späteren Fassung. Kanonische IoSN-Implementierungen bleiben unverändert.

## Executive Summary

**(1) Es geht um eine Prozesskette, nicht um eine universelle DSL.** Wetterjahrauswahl, Netz-/Zonenreduktion, sektorale Datenabbildung, Ausbaukandidaten, mehrszenarielle Investitionsoptimierung und Postprocessing sind fachlich verschiedene Abstraktionen. Ein einheitliches YAML/JSON-Schema oder eine einzelne LP-Formulierung stellt für sich genommen keine vollständige IoSN-Interoperation sicher.

**(2) Die normative Stoßrichtung unterscheidet sich von CBA.** Für IoSN ist die *gewichtet-stochastische Systembedarfsoptimierung* zentral, nicht ein paarweiser Projekt-/Referenzfall-Nutzenindikator B1. ENTSO-E beschreibt `min_x c^T x + sum_s pi_s Q(x,s)`, gemeinsame Ausbauvariablen über Wetter-Szenarien (Nichtantizipativität), drei repräsentative Klimajahre pro Studienjahr sowie mehrstufige Kandidaten-/Speicheroptimierung [S01 ``3.1, 3.7, 3.10]. **Ein Modell, das je Wetterjahr ein eigenes unabhängiges Ausbauportfolio optimiert, ist kein 1:1-Interpreter dieses Ansatzes.**

**(3) Die zwei beschriebenen Tool-Engines sind ein Primärbefund.** ENTSO-E nennt **PLEXOS und Antares** und dokumentiert Sanity Checks an einem vereinfachten **Drei-Knoten-Dispatch** mit zwei Leitungskapazitäten 500/450 MW [S01 `5.1]. Das ist ein Beispiel für **begrenzte Verhaltensvergleichbarkeit**, **kein** publizierter Nachweis der algebraisch identischen großen stochastischen Expansion-LPs, gleichen Investitionsportfolios oder garantierter Robustheit. Die methodischen Unterschiede sind im Dokument ausdrücklich erwähnt.

**(4) Netzreduktion ist eine wertende/nähernde Transformation.** [S01 `3.8/Anhang 6.1] beschreibt Clustering, impendanzbasierte Flusskalibrierung und LODF-/N-1-bezogene richtungs-/saisonabhängige Kapazitäten. Aggregationsidentitäten wie `A_z Gamma = P A_d` garantieren in geeigneter Definition **Bilanzkonsistenz**, **nicht** generelle PTDF-, N-1- und Portfolioäquivalenz. Hier liegt ein wichtiger Informations-/Common-Mode-Risikobereich.

**(5) Die Gesamtarchitektur sollte gestuft sein.** Vorläufig zweckmäßig erscheint **A+ über Prozessgrenzen**, ein **B-Mathematikprofil** dort, wo mathematisch strenge Reproduzierbarkeit gewollt/verbindlich ist (Expansion-LP, klar abgegrenzte DC- oder Speicherklasse), und ein **B+-Governanceprofil** für ausdrücklich zugelassene unabhängige Varianten und Entscheidungsrobustheit. **Eine Entscheidung zugunsten eines universellen B+ wird nicht aus der bloßen Nutzung zweier Tools abgeleitet.**

**(6) Der vorhandene Repository-Code ist ein wichtiger, aber begrenzter Forschungsinput.** [R01–R06] unterscheiden eigene Konstruktionen und Algorithmen von ENTSO-E-Anforderungen. Der PyPSA-Adapter weist z. B. Transformer, Phasenschiebung, Links und Speicherklassen ab [R05]; der Test-/Demo-Strang ist synthetisch und nicht auf einem echten TYNDP-Netz E2E validiert [R02]. Diese Software **ist nicht** als vollumfängliche Tool-zu-Tool-Übertragung des IoSN-2026-Systems auszugeben.

## 1. Fünf strikt getrennte Prüfgegenstände

| Kategorie | IoSN-Leitfrage | Geeigneter Nachweis |
|---|---|---|
| Requirements Clarification | Welches Studienjahr, Wetterensemble, Netzmodell, Ausbaukandidaten, Systemkosten, Variantenmodus und gültiger Normstand? | normative, freigegebene und versionierte IoSN Process/Study Contracts |
| Mathematische 1:1 Translation | Kann Modell M1 das *gleiche definierte Teilproblem* an M2 übertragen? | symbolische Daten-/Algebra-/Bounds-/Gewichte-Tests, identisches `x` über Wetter, Solverresiduen |
| Interoperation | Kann ein Übergang detailliertes Netz→Busmap→Ersatzmodell→Expansion reproduzierbar und mit erklärten Näherungen laufen? | Input-/Output-/Mapping-Manifeste, Erhaltung, Approximationsbudget, Rückbezug auf Quellnetz |
| Conformance | Führen **unabhängige Implementierungen derselben freigegebenen Formulierung** zur äquivalenten Optimierung? | doppelte, unabhängig generierte Instanz; primal/dual/gap; Portfolio-Gleichwertigkeit bei Degeneracy |
| Methodische/Entscheidungsrobustheit | Überlebt der Systembedarf legitime Wetterauswahl-, Modellstruktur-/Reduktions- und Zeit-/H₂-Varianten? | vorab registrierte Varianten, Cross-Evaluation, Engpass-/Bedarfsrank, maximaler Regret, Out-of-sample |

**2026er „robust optimisation“** bedeutet gemäß [S01 `3.1] ein erwartungskostenorientiertes stochastisches Programm mit einer *gemeinsamen* ersten Stufe. Das ist **nicht identisch** mit `min_x max_s Cost(x,s)`, nicht automatisch worst-case robust, nicht garantiert robust gegenüber **nicht beprobten** Wetterjahren, Netzaggregation oder Modellfehlern. Bei der Verwendung des Ausdrucks „robust“ muss immer die gemeinte Dimension angegeben werden.

## 2. Hypothesen und Falsifikationskriterien

| Hypothese | Stärkster Pro-Punkt | Stärkster Gegenpunkt | Urteil / Vertrauen / zu liefernder Beleg |
|---|---|---|---|
| I-H1: A+ über alle IoSN-Handoffs | frühe Erkennung von Mapping- und Provenienzverlusten | reiner Contract lässt falsche Expansion-Gleichungen unentdeckt | **plausibel / mittel**; End-to-End-Transfer mit positiven und negativen Gate-Tests |
| I-H2: B ist für den Expansion-LP-Kern überlegen | gemeinsame Nichtantizipativität, Zielfunktion, Kandidaten und Constraints verifizierbar | veröffentlichter Entwurf spezifiziert nicht notwendigerweise jede Solver-/Tool-Formulierung vollständig; Vollnormalform teuer | **plausibel / mittel**; 2 unabhängige LP-Generatoren, objekt-/constraintgenau |
| I-H3: B+ maximiert Transparenz von Alternativmethoden | vereint Referenz-Conformance und Variantenrobustheit | Methodenvielfalt kann normative Vergleichbarkeit unterminieren; Governance hoch | **offen / mittel**; genehmigter Variantenkatalog, validierter 2×2 Cross-Eval |
| I-H4: Ein einziges B für die gesamte IoSN-Kette genügt | ein normativer ausführbarer Referenzprozess könnte transparente Reproduktion erlauben | Statistik/PCA/KMeans, Zoning, Datenprovenienz, diskrete Kandidatenfilter, N-1-Mappings sind nicht das gleiche wie ein LP | **nicht belegt / mittel**; formal beschriebener kompletter End-to-End-Prozess samt Erweiterungen |
| I-H5: Gleiche PLEXOS-/Antares-Dispatchresultate beweisen Portfoliogleichheit | `5.1 gibt reale Sanity-Checks für zwei Testfälle an | 3-Knoten-Dispatch kann komplexe Multiweather/Expansion-/Postprocessingfehler nicht aufdecken | **widerlegt als Schlussfolgerung / hoch**; Vollinstanz- und Portfolio-Sensitivitätsprüfungen |
| I-H6: Aggregierte Bilanzidentität genügt für Netzreduktionsqualität | `A_z Gamma = P A_d` wahrt korrekt definierte Knotenschnittbilanz | kritische Zweige, Impedanz, loop flows und N-1 können trotz exakter Bilanz differieren | **widerlegt / hoch**; unabhängige detaillierte Fluss-/N-1-Tests |
| I-H7: gleiche 3 Wetterjahre garantieren Zukunftsrobustheit | explizite Variation/Weights decken Klima-Diversität besser ab als 1 Jahr | Auswahl und Repräsentativität, Gewichte, Tail-Risiko und neue Jahresdaten bleiben offen | **widerlegt als allgemeine Garantie / hoch**; out-of-sample Bewertung gegen Kandidatenjahre |
| I-H8: Repository IoSN-Prototyp kann reale unabhängige Toolkonformität belegen | ausführbarer Forschungsdemonstrator mit physikalischen Tests | nur synthetisch, schmaler Adapter, keine reale E2E-Integration | **nicht belegt / hoch**; gepinnter realer Datensatz + M1/M2-Läufe |

## 3. Architektururteil nach Aufgabe

| IoSN-Aufgabe | A | A+ | B | B+ | Konsequenz |
|---|---|---|---|---|---|
| Szenariodaten/PECD/PEMMDB/H₂ | Format | **nötiger semantischer Vertrag** | punktuell | bei Methodenvarianten | A allein riskiert falsche Einheiten/Gewichte |
| PCA/KMeans Auswahl vollständiger Wetterjahre | Eingabe | **Kandidaten-/Weight-/Seed-/Outputvertrag** | reproduzierbare mathematische Auswahl | alternative erlaubte Auswahlverfahren | zwei ähnliche Clusterlabels sind nicht dieselben Jahre |
| Zonal clustering und Netzreduktion | Busmap | **Mapping/Verlust/Qualität notwendig** | definierte Formulierung nur für enge Teilklasse | robuste alternative Methoden | PTDF-/N-1-Differenzen messbar halten |
| PLEXOS ↔ Antares Expansion | Rohdaten | fachlicher Prozessvertrag | **besonders sinnvoll als identische LP-Referenz** | kontrollierte Modellvarianten | `5.1 Sanity-Checks allein ungenügend |
| LF baseline vs OPF study, H₂-Freeze | ggf. Dateitransfer | **Pflicht-Method-ID und Scope** | je definierter Basisklasse | Variantenstudie | keine Gleichsetzung von LF und OPF |
| Bedarfs-/Portfoliovergleich | Ergebnisse | gleiche Bedarfs-/Region-/KPI-Semantik | Objective/Feasibility-Conformance | unabhängige Entscheidungssensitivität | Robustheit ist keine Output-RMSE allein |

**Vorsicht:** B setzt eine **tatsächlich normierte, vollständig formulierte Modellklasse** voraus. Der 65-seitige Entwurf [S01] und die Repository-Forschung erlauben die Feststellung von **Referenzanforderungen**, aber noch nicht die Behauptung, dass bereits eine vollständige ausführbare einheitliche IoSN-2026-Referenzmathematik samt freigegebenen Conformance-Tests öffentlich vorliegt.

## 4. Red-Team-Befunde gegen die Lieblingsarchitektur

- **Gegen A+:** Ein gemeinsames Daten-/Methodenregister erkennt nicht, ob M1 eine Investition pro Wetterjahr separat wählen durfte. Für den Kern braucht es algebraische Gate-Tests (B).
- **Gegen B:** Die beste Übereinstimmung zweier Solver mit demselben reduzierten Modell erkennt **nicht**, ob ein kritischer realer Korridor bei der Clustering-Reduktion verloren ging.
- **Gegen B+:** „Alternativmethode“ ist ohne normativen Geltungsbereich kein Robustheitstest; ein LF-Portfolio und ein frei optimiertes OPF-Portfolio dürfen nicht als gleichwertige Resultate desselben offiziell vorgeschriebenen Verfahrens ausgewiesen werden.
- **Gegen A:** Stille Änderungen von Wetterjahresgewichten oder `x_s` statt `x` können andere Bedarfsrangfolgen erzeugen, obwohl YAML/CSV parsebar bleiben.
- **Toolabhängigkeit:** PLEXOS+Antares ist nicht automatisch „Compilerdiversität“; die unabhängig verwendeten Modellgeneratoren, gemeinsam genutzte Daten, eventuell gemeinsam genutzte Algorithmen und Toolversionen müssen separat nachgewiesen werden.
- **Veröffentlichungsstatus:** Die geprüfte IoSN-2026-Methodik ist ein **Konsultationsentwurf**. Eine offizielle Konformitätsbehauptung muss den tatsächlichen finalen Stand bzw. freigegebenen internen Method Contract nachweisen.

## 5. Fünf kritische Review-Runden (analytisch, nicht als ausgeführte Experimente)

| Review | Analysebefund | Offenes Quality Gate |
|---|---|---|
| R1 Requirements | gemeinsame Kandidaten, Wetterjahre, Gewichte, Ausbauhorizonte und LF-/OPF-Modus nötig | Regulatory/Methode-Owner bestätigt Scope + finale Fassung |
| R2 1:1 Translation | stochastisches `x`, Raten, PST, H₂-Elektrolyse, Speicher, Netzlimits haben kritische Defaults | negative Algebra-/Feature-Tests und Roundtrip |
| R3 Interoperation | Netzreduktion und Marktaufteilung transformieren Physik und Identitäten | Mapping- und Qualitäts-/Loss-Reports je Übergabe |
| R4 Independent Validation | 3-Knoten-Sanity sind begrenzte Evidenz; robust weighted LP ≠ Methoden-/Decision-Robustness | 2 Toolinstanzen + out-of-sample + Cross-Evaluation |
| R5 Red Team | A+ allein zu schwach im LP, B allein zu eng in Netzreduktion; B+ teuer | Architektur-TCO und mindestens zwei echte Gegenbeispiele |

## 6. Ergebnis

**Vorläufig bevorzugt:** explizite A+-Prozessverträge mit eng definierten B-Referenzprofilen für kontrollierte mathematische Teilprobleme; **B+-Methodenprofile** zur extern/independently validierten Robustheit. **Kein endgültiger universeller Gewinner.** Der verfügbare Evidenzstand genügt zur Priorisierung von Tests, nicht zur Wahl einer für ENTSO-E verbindlichen Zielplattform.

Siehe [Befunde](findings.md), [Handoff-Verträge](../analysis/process_contracts.md), [Use Cases](../analysis/use_cases.md), [Pilotplan](../analysis/pilot_plan.md), [ADR](../analysis/recommendation_adr.md).
