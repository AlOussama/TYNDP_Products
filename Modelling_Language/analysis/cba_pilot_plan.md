# Nächster Schritt: CBA Scenario Interoperation — kleiner falsifizierender Pilot

**Status:** ausführbarer Versuchsplan; keine durchgeführten Multi-Tool-Läufe. Zweck ist der **Architekturtest**, nicht die Produktion offizieller TYNDP-Ergebnisse.

## 1. Experimentfragen und falsifizierbare Hypothesen

- **Q1 — Fehler in M1:** Können unabhängige Validierungen und ein zweites Tool Fehler in Input, mathematischer Formulierung, Interpreter und Übersetzung **unterschiedlich zuverlässig** erkennen?
- **Q2 — M1 fertig, M2:** Welche zusätzlichen Erkenntnisse liefert M2 als **1:1-Interpreter**, als **unabhängiges Modell** oder als **nachgelagerte Netz-Engine**?
- **Q3 — Robustheit:** Bleibt das B1-Projekturteil bei genehmigten Methoden- und Szenariovarianten stabil? Wenn nicht, an welchem Parameter kippt die Entscheidung?
- **Q4 — Tool-Übersetzbarkeit:** Welche PyPSA-/GEMS-/CESM-/INES-Funktionsmenge lässt sich **verlustfrei** übertragen, welche nur approximieren, welche muss abgelehnt werden?

**Pilot-Hypothese:** A+ mit optionalen B-Konformitätsprofilen kann diese unterschiedlichen Fragen sauberer trennen als reiner Datenaustausch (A). **Gegenhypothese:** Ein streng vorgegebenes B+-Referenz-/Variantenprofil bietet für einen regulierten CBA-Fall bessere Prüfbarkeit bei akzeptablen Gesamtkosten.

## 2. Pilotmatrix

| Schritt | Aufgabenstellung | Erzeugtes Artefakt | Go-Kriterium |
|---|---|---|---|
| P0 | Normfassung/B1/B6/Projektrahmen, R/P und KPI freigeben | signierter Planning Contract + Input-Manifeste | valide G0–G2 |
| P1 | synthetischer 2-Zonen-Interkonnektor, zwei Wetter-/Nachfrageszenarien, Speicher | unabhängige Daten- und Methodenmanifest-Dateien | keine unmarkierten Defaults |
| P2 | M1 lösen, **R und P**, Seed/Version/LP/Status exportieren | reproduzierbares Pair `M1-R,P` | Konsistenz und KPI-Residualtests |
| P3 | M2 als **1:1-Interpreter**, mit bewusst falschem Speicher-/Link-Export | `EXACT_VERIFIED` oder **REJECTED**-Feature-Bericht | T04/T05/T08 bestanden |
| P4 | M2 als **unabhängiges Gegenmodell** aus Original-Inputs, nicht aus M1-Dispatch | Pair `M2-R,P`, Method Registry | T12/B1 normalisierbar |
| P5 | optional M2 als **Downstream** Markt→Netz, getrennte API/Model ID | Mapping-/Verlust-/Netzvalidierungsbericht | T13 bestanden |
| P6 | B6-Adequacy ausschließlich mit dafür geeigneten MC-/EENS-Profilen (optional im ersten Pilot) | gesonderter `B6-Report` | T10 bestanden und CIs dokumentiert |
| P7 | Fehler-Injection (Daten, Algebra, Adapter, KPI) und Entscheidungs-Falsifikation | Finding/Impact-Register und Robustness-Report | T11/T14/T15 und ex-ante Schwellen |
| P8 | Aufwand/Benefit/TCO der Architekturvarianten vergleichen | nach Evidenz gewichteter ADR | keine Critical-Befunde ungeklärt |

**Wichtig:** Das Pilot-Setup darf **zunächst rein synthetisch** sein; es belegt dann *nur* technische Eigenschaften, nicht reale CBA-Entscheidungsrobustheit. Eine spätere reale CBA ist ein eigener Freigabeschritt.

## 3. Minimale zwei Modelle

- **M1:** z.B. PyPSA-basierter Energie-/Marktoptimierer, eigene Speicher- und Transport-/DC-Semantik, R/P-Output.
- **M2a — Conformance:** GEMS + unabhängigem Interpreter/Modellgenerator, soweit Funktions-/Versionsabdeckung tatsächlich gegeben ist. Bei nicht unterstützten Parametern **keinen** falschen Erfolg annehmen.
- **M2b — Independent Method:** zweite eigenständige Implementierung desselben *Planning Contract*, mit vorab registrierten Alternativmethoden und eigener R/P-Rechnung. M2a und M2b dürfen technische Infrastruktur teilen, diese Abhängigkeit ist aber offenzulegen.
- **Netz-M2:** bei Bedarf separat, als **Downstream**, ohne irreführende unabhängige B1-Interpretation.

## 4. Akzeptanz und Stop/Go

**Stop:** unsicherer Normstand für offizielle Anwendung; stille semantische Verluste; nicht reproduzierbare Inputs; unvollständige M1/M2-R/P-Paare; inkonsistentes B1-/B6-KPI; unmarkiertes Mapping; „robust“ ohne Methodenvarianten.

**Go für *technisches* Architektur-Pilotfazit:** 1:1-Tests bestanden **oder** klar begründet abgelehnt; zwei gepaarte unabhängige CBA-Läufe; negative Fehler-Injections erkennen Defects; Capability/Loss-Report vollständig; Abweichung von B1/Projektentscheidung methodisch erklärt oder als Risikobefund offen ausgewiesen.

**Noch kein Go für reale Investitionsentscheidungen:** reale validierte Daten, methodische/regulatorische Freigabe, quantitative Robustheitsgrenzen und unabhängige Audits fehlen.

## 5. Zu liefernde Berichte (nach Durchführung, nicht vorwegnehmen)

`contracts/*.yaml`, `manifests/*.json`, `run_outputs/*`, `validation/conformance.csv`, `validation/loss_report.csv`, `validation/robustness.csv`, `validation/error_injection.md`, `decision/adr_after_pilot.md`. Ein späterer PoC gehört ausschließlich nach `Modelling_Language/prototypes/` und `Modelling_Language/tests/`; keine Änderungen am IoSN-Code.
