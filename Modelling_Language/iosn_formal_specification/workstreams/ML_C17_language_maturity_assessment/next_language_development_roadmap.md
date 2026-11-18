# ML-C17 — Priorisierte Sprachentwicklungsroadmap

**Reiner Forschungshandoff ohne Bindung an ML-C09–ML-C16.** Diese Roadmap verschiebt normative Freigaben, echten produktiven Modell-/Solverbetrieb, Realdata-Qualifikation und den zweiarmigen Piloten ausdrücklich auf spätere Entscheidungen. D1–D6 bleiben bestehen. MD-01…MD-20 und MA02-CL-001 sind weiter Owner-TBD; **G1 BLOCKED**.

## 1. Drei vorangehende harte Entscheidungsgates

- **G-SEM:** Gleiche Semantik für alle 48 MA01-SR, P00–P17, M01–M18, 87 DataDefinitions, 38 TransformSpecs und 20 process-only-Objekte rekonstruierbar; Eigentümer-/Quellstatus korrekt.
- **G-EXP:** RC01–12 als wirklich getypte, maschinenprüfbare positive und negative Spezifikationen, in denen physikalische / Marktlink-Rollen, M01, D2 und P15 nicht fälschlich zusammenfallen.
- **G-IMP:** Zwei unabhängige Implementer können aus derselben fixierten Contract-Version wissenschaftliche Pflichten und zulässige Implementierungsfreiheiten rekonstruieren; keine zusätzliche unbelegte Fachentscheidung nötig.

Alle Gates sind **Entwicklungsgates** und ersetzen die separate spätere normative Gate-G1-Freigabe nicht.

## 2. Unmittelbar mögliche, voneinander unabhängige Forschungsaktivitäten

| Priorität / ID | Forschungspaket | Präzise Lieferung | Falsifikator / Ende des Pakets | Eigentumsgrenze |
|---|---|---|---|---|
| P0 / L17-R01 | vollständige abstrakte Contract-Semantik | deklarative semantische Rollen, 48 SR↔required predicates, Scope/Source/Unknown, mathematische AST-Binder | ein Pflicht-SR kann nur durch Freitext, verborgene Annahme oder reale Solverimplementierung ausgedrückt werden | Forschung, keine Ownerentscheidung |
| P0 / L17-R02 | Mathe-/Einheiten-/Guard-Sprachkern | Quantoren/Indexbinder, Delta t / MW-MWh / Carrier, pre-CY vs recourse, KCL/KVL/NTC, storage/H2, Stage, P15 three-valued guard | fehlerhafte CY-Variante, KVL-/Link-Verwechslung oder doppeltes CAPEX wird vom Formalbeispiel akzeptiert | Forschung, numerische Werte offen |
| P0 / L17-R03 | produktneutrale RC01–12 als echte Sprachfixtures | komplette 12 gültigen und kontrollierte invalid Mutanten, Oracle-/Error-ID pro Case | reine Objekt-ID-Existenz besteht ohne vollständige fachliche Pflicht | keine Modell-Solverläufe |
| P0 / L17-R04 | Minimierung S1/S2/S3 | Sprachkern-Inventory, Konzepte-/Relationen-/Pflichtfeldzählung, Ablation und semantischer Regressionstest pro entferntem Konstrukt | Verlust einer relevanten Invariante bei angeblich vereinfachtem Kern | keine Vorentscheidung B |
| P1 / L17-R05 | A/B/C Vergleich mit nativen Standardparsern | mindestens zwei echte Standard-Slices (z. B. ReqIF SR+Source, LinkML/SHACL Data+Guard; mathematischer Ausdruck gesondert), Roundtrip und SemanticDiff | eine obligatorische Status-, Operator-, Unit- oder Authority-Information geht verloren | Formatauswahl zunächst experimentell |
| P1 / L17-R06 | negative mathematische Witnesses ohne volles IoSN Modell | kleine generierte E04-Constraint-/Coefficient-Exemplare und Mutanten, E-FEAS/E-OPT/E-OBS jeweils getrennt | Match des Toy-Zielfunktionswerts ersetzt fälschlich Formulierungsprüfung | synthetische Mini-Modelle, kein produktiver Solver |
| P1 / L17-R07 | unabhängiges Implementer-Handover | zwei voneinander unabhängige Entwickler, identische Contract-Version, klassifizierte Rückfragen für PyPSA/Antares/Sienna-Paradigmen | zwei Leser treffen verschiedene undokumentierte Methodenannahmen | keine Zwei-Tool-Produktivprüfung |
| P1 / L17-R08 | semantischer Release-/Änderungstest | Source-/Unit-/Math-/Guard-/Version-Mutanten, Migration, invalidierte Evidenz und Recovery im A/B/C-Slice | inkompatibler Change wird still akzeptiert | Ownerfreigabe weiterhin später |
| P2 / L17-R09 | qualifizierte externe Forschungsreview | Person- und Team-unabhängige Formalsemantik-/Energiesystemmodell-Review der tatsächlichen Daten/Schemas/Fixtures | unbehobene widersprüchliche Sprachinterpretationen | Reviewer-Entscheid, nicht KI-interner Audit |
| Später / OUT-01 | Methodik/Data/Output-/Approval | MD/CL Ownerentscheide, reale SourceRelease-Data, KPI-Owner, normative Contractfassung | G1 bleibt bis dahin BLOCKED | **ausdrücklich nicht ML-C17** |
| Später / OUT-02 | produktive Toolrealisation | Toolarme und tatsächliche E01–E08 E04/E05 Nachweise, vollständige IoSN-Testläufe | keinesfalls aus Mock-C06 oder toy-C17 als erfüllt ausgeben | separater späterer Auftrag |

## 3. Entscheidungspunkte und minimaler Nachweis

- **Zwischenentscheidung nur als Forschungshypothese:** S2-Rollenmodell akzeptieren **als Testobjekt**, sofern alle Pflichtsemantiken nachweisbar repräsentiert bleiben; nicht die Alternative B wählen.
- **Sprach-L3-Vorbereitung:** formaler Syntax-/Semantikabschluss, alle 48 SR klassifiziert FULL/PARTIAL/REFERENCE/UNKNOWN, gesicherte 12 RC mit negativen Abweisungen; Owner-TBD wird ohne Default dargestellt.
- **Sprach-L4-Nachweis:** tatsächlich ausgeführter geeigneter Parser/Checker mit reproduzierbaren gültigen/ungültigen Dateien und struktur-/semantiktreuem Roundtrip. Eine fehlende Toolfunktion macht nur die Toolabdeckung schwächer.
- **Architekturentscheidung:** erst nach diskriminierenden A/B/C-Versuchen; K2/K3/K6/K7 als Pflicht-Gates, K1 minimaler Kosten-/Leselastvergleich, K8–K10 Änderungen/Standard; keine arithmetische Kompensation von semantischem Verlust.
- **Normative Entscheidung:** späterer Authoritative-Methodology-, Data-, KPI- und independent-assurance-Nachweis. Gate G1 bleibt durchgehend BLOCKED, bis separat beschlossen.

## 4. Erwarteter Forschungsnutzen

Eine übersichtliche, klein gehaltene, getypte und ausreichend ausdrucksfähige IoSN-Vertragssprache würde später zwei verschiedene Frameworkentwickler auf die **gleichen fachlich/mathematisch prüfbaren Verpflichtungen** verpflichten, während die native Implementation, algebraische Repräsentation und Solverwahl frei bleiben. Dies ist **das zu prüfende Ziel**, nicht der bereits bewiesene Projektstatus.
