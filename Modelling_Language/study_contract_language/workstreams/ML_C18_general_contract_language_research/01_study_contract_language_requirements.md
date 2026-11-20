# ML-C18 / 01 – Requirements an eine generische Energy-System Study Contract Language
Version: **research-r1 / requirements freeze**, 2026-11-20. Status: **NON-NORMATIVE**. Erarbeitet unabhängig von GEMS, mathspec und dem ML-C17-Ansatz; keine Aussage über deren Erfüllung. Der Freeze gilt nur für den Vergleich innerhalb ML-C18 und ist kein Owner-Signoff.

## Zweck und kontraktuelle Abstraktion
Eine Studie beschreibt *was* untersucht, verglichen, bewertet oder optimiert werden soll, *unter welchen Bedingungen* und *wie Eigenschaften und Resultate beobachtet werden*. Nicht automatisch Bestandteil: Optimierungsvariablen, algebraische Darstellung, Solver, Programmiersprache, Tool-Artefakt, Algorithmus. Ein Kontrakt kann bei methodischer Notwendigkeit konkrete Eigenschaften oder Formelklassen verlangen, muss jede solche Einschränkung begründen.

Konzeptuelle Semantik: `StudyContract = Context + Obligations + Assumptions + Observables + Verification + AllowedVariation + Provenance`. Dies ist eine **prüfbare Hypothese**, kein bereits verabschiedetes Metamodell. Repräsentationsunabhängige Konformität bedeutet: Für eine Implementierung M, Daten/Annahmen D und beobachtbare Historie h muss die Projektion `π(M,D)=h` die im Gültigkeitsbereich geltenden Guarantees erfüllen; zugleich müssen deklarierte Variationen innerhalb der erlaubten Menge liegen. Allgemeine dynamische Garantien können zusätzliche geeignete Witnesses / Trace-Nachweise benötigen; Portwerte allein genügen für Energieerhaltung mit verborgenen Zuständen nicht. Ein korrekt spezifizierter Contract ist nicht automatisch konsistent oder erfüllbar.

## SLR-Forschungskatalog und beobachtbare Akzeptanz
Nachfolgende 42 Anforderungen sind Kandidaten, ausdrücklich **keine normative Baseline**. Pro SLR ist nachzuweisen: (i) syntaktische Darstellung, (ii) wohldefinierte Semantik, (iii) positives und fehlerhaftes Gegenbeispiel, (iv) toolunabhängige Interpretation. Fehlende Evidenz ist nicht mit Nichterfüllung gleichzusetzen.

### Study

| ID | Anforderung | Minimaler Akzeptanznachweis |
|---|---|---|
| SLR-01 | Studienzweck und Entscheidungsfrage | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-02 | System und funktionale/geographische Grenze | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-03 | Varianten, Baseline und Gegenfaktum | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-04 | Szenarien, Zeit/Raum, Stichproben und Gewichtungen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-05 | Fachliche Anforderungen mit Normativitätsstatus | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-06 | Datenvertrag: Wertebereich, Einheit, Identität, Qualität, Provenienz | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-07 | Pre-/Postprocessing und Prozesspflichten | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-08 | Mathematische Invarianten ohne Pflicht zu einer Repräsentation | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-09 | Outputs, Kennzahlen und Vergleichsprojektionen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-10 | Prüfpflichten und Evidenzidentität | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-11 | Anwendbarkeit, Quelle, Version, Genehmigungsstand | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |

### Component

| ID | Anforderung | Minimaler Akzeptanznachweis |
|---|---|---|
| SLR-12 | Komponentenrolle und semantische Identität | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-13 | Externe Ports und Anschlusstopologie | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-14 | Energieträger, Flussrichtung, Einheit, Vorzeichen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-15 | Externe Betriebsgrenzen und Kapazitäten | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-16 | Physikalische Energie-/Stoff-/Umwandlungsbilanz | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-17 | Zeit-/zustands-/ereignisabhängiges Verhalten | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-18 | Assumptions und Gültigkeitsbedingungen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-19 | Erlaubtes/verbotenes externes Verhalten | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-20 | Observables und komponentenspezifische Prüforakel | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |

### Freedom

| ID | Anforderung | Minimaler Akzeptanznachweis |
|---|---|---|
| SLR-21 | Freiheit der internen Formulierung | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-22 | Konformitätsfehler versus zulässige Modellabweichung | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-23 | Abstraktionsgrade und Aggregationsnachweise | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-24 | Deklaration zusätzlicher Annahmen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-25 | Nachgewiesene Äquivalenz vs erlaubte Nichtäquivalenz | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-26 | Keine implizite Normierung von Variablen/Gleichungen/Solver | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |

### Multi-model

| ID | Anforderung | Minimaler Akzeptanznachweis |
|---|---|---|
| SLR-27 | Gemeinsame Studienbasis mit eindeutiger Identität | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-28 | Harmonisierte Inputs, Szenarien und exogene Annahmen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-29 | Gemeinsame Observables/Projektionen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-30 | Versionierte Strukturdifferenzdeklarationen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-31 | Metrik, Aggregation, Toleranz, Entscheidungsregel | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-32 | Fehler/Nonconformance vs strukturelle Unsicherheit | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-33 | Robustheitsdesign, Varianzzerlegung, Sensitivität | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-34 | Implementierungsunabhängigkeit, Herkunft, Evidenz | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |

### Cross-cutting gap candidates

| ID | Anforderung | Minimaler Akzeptanznachweis |
|---|---|---|
| SLR-35 | Explizite Einheiten-/Dimensions- und Konversionssemantik inkl. Energieinhalt H2 | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-36 | Unknown/OWNER_TBD/NOT_APPLICABLE und Konfliktauflösung | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-37 | Temporal boundary semantics: Anfang/Ende, Auflösung, Interpolation und cyclicity | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-38 | Szenarienbaum, Informationszeitpunkt und Nichtantizipativität falls anwendbar | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-39 | Nichtoptimierende Studien: Simulation, Screening, Bewertungsworkflow | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-40 | Mehrfachoptima, Ergebnisauswahl und numerische Toleranzen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-41 | Konformitätsstatus inkl. nicht prüfbarer und bedingt erfüllter Aussagen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |
| SLR-42 | Daten-/Modelllizenz, Zugriffs- und Reproduzierbarkeitsbedingungen | Im passenden RC/UC explizit definieren; absichtlich widersprüchliche/fehlende Information detektieren oder als OPEN deklarieren. |

## Semantik von Verpflichtung, Freiheit und Ungewissheit
- `REQUIRED`: In ihrem Scope verbindliche Eigenschaft; Beobachtungs-/Evidenzregel zuweisen.
- `PROHIBITED`: Verbotene Eigenschaft/Annahme; bei Anwendung Konformitätsverstoß.
- `PERMITTED`: Option in expliziter Menge; *keine* automatische Positivaussage über die physikalische Zulässigkeit einer Option.
- `IMPLEMENTATION_DEFINED`: Auswahl durch Implementierenden; Wert, Herkunft und Begründung dokumentieren; Standardsichtbarkeit je Profil.
- `CONDITIONAL`: keine eigenständige Modalität; strukturiert als `(Guard, Obligation)`.
- `OWNER_TBD`: nicht entschiedene Vorgabe; kein positiver Nachweis, keine stillschweigende Defaultsetzung, `OPEN` bzw. `BLOCKED` je Kritikalität.
Minimalitätsprüfung: REQUIRED/PROHIBITED über ein allgemeines `Rule(effect, guard, scope)`; PERMITTED/IMPLEMENTATION_DEFINED als `VariationPolicy`; OWNER_TBD als `DecisionStatus`. Ob diese Dreierstruktur genügt, wird in ML-C18 getestet.

## Interface, Behavior und Assume-Guarantee
Ein Komponentenvertrag legt Rolle, Topologie, Portträgerschaft, Injektionskonvention, Zeitbezug, beobachtbares zulässiges Verhalten, Bedingungen und Prüfbarkeit fest; er soll keine spezifische SOC-Variable, Intervall-Nebenbedingungsfamilie oder Solverlösung voraussetzen. `A => G` darf nicht als bloßes logisch vacuous Resultat eines immer falschen A gelten: Annahmen sind auf **Erfüllbarkeit**, **Kontrollierbarkeit durch die Umgebung** und **Kompositionsverträglichkeit** zu prüfen. Zusätzlich wird festgelegt, ob Guarantee für sämtliche zulässigen Verläufe, mindestens einen Verlauf oder lediglich beobachtete Testläufe gilt. Für Optimierungsmodelle: existenzielle Zulässigkeit, optimale Auswahl und universelle Fähigkeit nicht verwechseln.

Die Mindest-Portsemantik verlangt Verbindungspunkt, Energieträger/Stoff, Ein-/Ausgang, Einheit, Referenzrichtung, Zeitintervall und Aggregationsniveau. Ein allgemeines `power >= 0` ist ohne Vorzeichen-/Portdefinition unbrauchbar. Umwandlung muss insbesondere Wasserstoff-Massen- und Heizwertkonvention (LHV/HHV), Strom-Energie- und Wärmebilanz trennen.

## Mindestbedingung für Modellierungsfreiheit
Mindestens zwei fachlich kompatible, intern verschiedenartige Implementierungsskizzen müssen denselben Contract interpretieren können, ohne die unvermeidbaren Pflichten zu relativieren. `angle` / `cycle` / `PTDF` dürfen nur unter präzisen DC-Netzannahmen und korrekter Netzprojektion als äquivalent bezeichnet werden. Ein einfacher Ersatz ohne Rückverfolgbarkeit gilt nicht als erwiesene Äquivalenz. Ein EV-Fleet-Aggregat ist nur dann konform, wenn individuelle Mobilitätsanforderungen nicht unzulässig verloren gehen oder explizit auf ein gerechtfertigtes Aggregationsniveau projiziert werden.

## Trennung der Prüftiefen
`Syntax` ≠ `type/unit` ≠ `internal semantic consistency` ≠ `model conformance` ≠ `scientific validity` ≠ `robustness`. Negative Testfälle für jede Stufe vorsehen. Ein Parsererfolg ist kein Beweis korrekter Batteriebilanzen oder wissenschaftlicher Ergebnisse.

## Anwendungsprofile und Governance
- **UC1 IoSN:** IoSN-spezifische P00–P17-Prozesse, Stufen, CY1–CY5, fachliche Owner-Entscheidungen und offene MD/CL ausschließlich im Profil.
- **UC2 N2E CBA:** Methodikautorität zunächst offen; EU-/ENTSO-E-CBA-Dokumente sind nicht stillschweigend identisch mit einer spezifischen N2E-Methodik. Kennzahlen, Referenzfall und Diskontierung nur bei identifizierter Quelle konkretisieren.
- **UC3 Netzplanung:** Sicherheitskriterien, N-1, Netzrestriktionen, technische Prüfpflichten kommen aus dem benannten Prüf-/Methodikprofil; nicht pauschal in den Kern.
- **Governance:** keine Änderung der IoSN D1–D6, keine G1-Freigabe; G1 bleibt BLOCKED. Neue Requirements nicht automatisch IoSN-normativ.

## Redundanz-/Minimalitätsentscheidungen (Forschungsstand)
SLR-03/27 und -04/28 teilen Referenzidentitäten, bleiben aber in *Studiengestaltung* und *Vergleichsdurchführung* überprüfbar getrennt. SLR-08/16: globale vs lokale physikalische Invarianten. SLR-09/29: Outputpflicht vs identische modellübergreifende Projektion. SLR-10/20: Evidenz allgemein vs komponentenbezogen. SLR-18/35/37: Annahmen versus Einheiten/zeitliche Semantik. SLR-25/40: mathematische Äquivalenz versus Auswahl aus Mehrfachoptima. SLR-34/42: Provenienz vs rechtliche Reproduzierbarkeitsgrenzen. Zusammenlegbar im abstrakten Kern, getrennt prüfbar im Katalog.

## Qualitätssicherung / Ausgangsquellen
Source-first für externe Kandidaten: versionierte Code-/Dokumentations-/Testpfade; vordefiniertes RC01–RC10; Evidenz `D_DOC`, `I_IMPL`, `T_EXISTING`, `T_EXECUTED`, `H_HYPOTHESIS` gesondert. Für Power-Agent gilt: Skills/QA-Antworten sind **sekundäre** technische Hilfsmittel; originaler Modellcode, methodische Autorität, technische Nachweise haben Vorrang. Der bloße Hinweis auf eine Power-QA-Wissensbasis autorisiert keine erfundenen Inhalte.