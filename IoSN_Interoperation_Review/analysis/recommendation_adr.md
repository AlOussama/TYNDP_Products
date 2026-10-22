# ADR-IO-001 — Interoperationsarchitektur im IoSN-Prozess

- **Entscheidungstyp:** Architektur-ADR für *IoSN-Prozessinteroperation*; **kein** allgemeiner Modelling-Language-ADR.
- **Datum:** 23.10.2026
- **Status:** **PROPOSED / CONDITIONAL**, fachlicher Desktop-Review.
- **Ausgangspunkt:** ENTSO-E TYNDP 2026 IoSN **Konsultationsmethodik 25.02.2026** [S01] und klar gekennzeichnete Repo-Forschung [R01–R08]. **Nicht** als finale ENTSO-E-Architektur/Implementierung deklariert.

## Entscheidung als falsifizierbare Arbeitshypothese

**Ein einzelnes Architekturmodell für alle Prozessschritte ist nicht begründet.** Pilotiert werden soll:

1. **A+ als verbindlicher IoSN-Process-/Data-/Transformation- und Results-Contract über die ganze Kette:** identische Datenidentitäten und -versionen, Inputs/Wetterjahrgewichtung, Quellen-/Zielgranularität, Clustering- und Netzreferenz, Kandidaten-/H2-/Storage-Profile, Provenienz/Verluste/Governance.
2. **B als optional verpflichtendes mathematisches Referenzprofil für klar definierte Kernteilmodelle** mit 1:1-Konformitätsbedarf: mehrszenarielles Expansion-LP mit gemeinsamer `x`-Entscheidung, candidate-stage/linear network/storage constraints; sowie definierte PTDF-/Netz-/Speicher-Submodelle. Der vollständige mathematische Normkern muss vor Freigabe *geschrieben und geprüft*, nicht aus einer knappen Prozessbeschreibung unterstellt werden.
3. **B+ als gesondertes, methodisch reguliertes Robustheitsprofil**, sofern ein normativer Referenzmodus und **zugelassene** unabhängige Varianten zugleich benötigt werden: Wetterselektion, Netzreduktion, LF-/OPF-, H₂-Freeze- oder Methodenannahmen. Nachweis mit identischen Grenz-/KPI-/Candidate-Definitionen und Cross-Evaluation.

**Keine allgemeine Empfehlung „A+ ist besser als B+“:** Für die **offizielle, streng harmonisierte Ausbauformulierung** kann B die geeignetere Lösung sein; falls regulierte Alternativmodelle verbindlich Teil des Entscheidungsprozesses werden, kann B+ die beste Governancestruktur bieten.

## Was die vorhandene offizielle Evidenz stützt

- Die [2026er Draft-Methode S01] besitzt eine mathematisch strukturierte, gewichtete LP-Beschreibung und beschreibt PLEXOS/Antares **verschiedene Modellierungsansätze**. Ihr `5.1 bietet nur statische Drei-Knoten-Vergleichstests, die mathematische Vollkonformität **nicht** nachweisen.
- Weather selection, zonal clustering, optimierte Ersatznetzparameter und N-1-Sicherheit sind *reale Transformations-/Methodenstufen*, nicht bloße Dateikonvertierung.
- Die im Stammrepo ausgewiesenen zwei **Clustering-Methoden A/B** und der schmale PyPSA-Prototyp sind **Forschungsinput**, nicht offizielle IoSN-Methode und **nicht** die Architekturvarianten A/B.

## Alternativen und echte Gegenargumente

| Alternative | Warum besser sein könnte | Warum nicht pauschal wählen |
|---|---|---|
| Nur A | minimaler Datenintegrationsaufwand | versteckte Gewichte, Netzlimits und methodische Unterschiede |
| Nur A+ | hohe Toolneutralität und geringer verpflichtender Algebra-Overhead | für identische Expansion-Problemklasse fehlen echte Conformance-Garantien |
| Nur B | maximaler eindeutig mathematischer Referenzvertrag für definiertes Modell | Statistik-/Geometrie-/Transformationen nicht allein in einem LP beschrieben; Common-mode Fehler |
| Nur B+ | Referenzkonformität plus genehmigte Varianten in einem Framework | größte Einführungs-, Review- und Release-Governance-Last; nicht alle Variationen regulatorisch zulässig |
| **A+-Prozess + B-Kern + optional B+-Varianten** | hält unterschiedliche Prüfziele getrennt und normiert Schlüsselgleichungen | erfordert Profilgrenzen, Adaptertests und dokumentierte Eigentümerschaft; keine Garantie minimalster TCO |

## Bedingtes Stop-/Go und Falsifikation

**A+-Prozesskern verwerfen oder stark vereinfachen**, wenn ein vollständig normiertes B-/B+-Metamodell nachweislich *alle* erforderlichen Handoffs und Qualitäts-/Datenherkunftsregeln besser und günstiger abdeckt.

**B als zwingendes Kernprofil reduzieren**, wenn (i) keine hinreichend vollständig freigegebene Mathematik definiert werden kann, (ii) unabhängige M1/M2-Generatoren die exakte Modellklasse nicht unterstützen, oder (iii) referenzpflichtige Anforderungen regulatorisch Methodevariation fordern, die B ausschließt. **Nicht** einfach die B-Typbezeichnung vergeben, ohne die Algebra zu verifizieren.

**B+ als produktives Profil nur einführen**, wenn (i) alle genehmigten Varianten einen Vergleichsvertrag teilen, (ii) ihre Unterschiedlichkeit tatsächlich unabhängig ist und (iii) die Cross-Portfolio-Holdout-Evaluation zusätzliche robuste Entscheidungsevidenz im Verhältnis zum Aufwand liefert.

**Absolute Stopper:** I-F01/I-F02/I-F03/I-F08, ungeklärte Normversion I-F10, nicht deklarierte LF-/OPF-/Candidate-/Hydrogen-Profile; keine Portfolio-Entscheidungsrobustheit behaupten ohne Lane III des Pilotplans.

## Normative Rollenverteilung

- **Muss gleich bleiben:** Planungsfrage, Datensystemgrenzen, Wetter/Szenariozeitreihen-ID und `pi_s` für Conformance, Candidate Set/Stage/Cost, physikalische IDs/Einheiten/Netzreferenzen, Methodenidentität und zulässige Transformationen, Outcome-/Security-Qualitätskriterien, Versions-/Auditinformationen.
- **Optional formal gleich:** Algebra für freigegebene Submodelle einschließlich `x`/Nichtantizipativität, Jahres-/Zeit-/Szenarioindices, objective/bounds, DC-/H₂-/Storage-Profile.
- **Darf bewusst unabhängig sein:** alternative **genehmigte** Wetter-/Clustering-/Netz-/Sektorkopplungsmethoden, Implementierungen und Solver; zusammen mit messbaren Abweichungs- und Plausibilitätsbedingungen, ohne den offiziellen Basismodellmodus umzubenennen.

**Owner-Freigabe ausstehend:** IoSN Method Owner, Climate/PECD Steward, Network Reduction Owner, Security Owner, Optimisation/Tool Owner, unabhängige externe Reviewer. Status bleibt **PROPOSED** bis zur [Pilotvalidierung](pilot_plan.md).
