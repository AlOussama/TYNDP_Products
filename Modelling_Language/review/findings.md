# Kritische Findings — Modelling Languages & CBA Interoperation

Stand 23.10.2026. Nachweise referenzieren die Primärquellen [S01–S14](../sources/bibliography.md). Severity ist nach **potenzieller CBA-Entscheidungswirkung**, nicht nach behaupteter Fehlerhäufigkeit gewählt. Vertrauen bezieht sich auf den **Befund**, nicht auf einen produktiven Nachweis.

| ID | Severity | Kategorie | Befund | Primärbeleg / Gegenposition | CBA-Konsequenz | Korrektur / Owner | Evidenzlage |
|---|---|---|---|---|---|---|---|
| **F01** | High | Robustness vs Conformance | Identische Gleichungen in mehreren Solvern testen keine Modellstrukturunsicherheit. | theoretische Unterscheidung; GEMS spezifiziert explizite Mathematik [S04]; unabhängige Modellvalidierung bleibt möglich | falsche Robustheitszertifizierung | zwei getrennte Testmodi; Architektur-Governance | Konzept hoch, Experiment offen |
| **F02** | **Critical** | 1:1 Translation | Konverter kann relevante Komponenten/Parameter **stillschweigend ignorieren**. | PyPSA→GEMS-Kompatibilitätsliste [S05], ines-pypsa-Verlustliste [S08]; Gegenposition: manche nicht exportierten Parameter sind für begrenzte DC-LOPF irrelevant | Änderung der zulässigen Lösung/Investitionsentscheidung ohne Warnung | Blockierung unbestätigter Übersetzung, explizite Loss-Klassen und Capability-Gates; Adapter-Owner | Quellen hoch |
| **F03** | **Critical** | CBA Vergleichbarkeit | Ohne gepaarte Fälle Referenz/Projekt pro Engine/Szenario entsteht ungültiger B1-Vergleich. | [S01] `5.1, [S02] `5.1; Gegenposition: unter identischer geprüfter Normierung könnten Ergebnisse über Engines normalisiert werden, aber nicht „roh“ gekreuzt | Nutzen-Bias / Rangfolge kippt | Pair-ID, gleiches Methodenprofil innerhalb jedes Paares, Delta zuerst pro Engine; CBA-Methodik-Owner | normativ hoch |
| **F04** | High | B1/B6-Methodik | B1 und B6 sind nicht durch denselben reduzierten Wetter-/Modelllauf ersetzbar. | [S01] ``5.1/5.6; [S02] `5.6 **nur Entwurf** | verfehlte Adequacy-Aussage | getrennte B6-Sampling-, VOLL-, EENS-Contracts; CBA-Owner | B6-Grundprinzip hoch; 2026-Details revisionsbedürftig |
| **F05** | High | Common-mode error | Eine formal gemeinsame, aber fachlich falsche Referenzmathematik kann Fehler in mehrere Engines propagieren. | Logische Implikation; Gegenbeleg: externe Physiktests können common-mode Fehler entdecken | scheinbare Bestätigung | unabhängige physikalische/ökonomische Benchmarks und Fehler-Injection; Independent Validator | Konzept hoch |
| **F06** | High | Modell M1→M2 | „M2 erhält M1-Ergebnisse“ kann Pipeline, Konformitätsprüfung oder unabhängigen Methodenvergleich bedeuten. | Prozesslogik; [S01] Markt/Netz/Redispatch als verschiedene Tools; Gegenposition: kontrollierte Kopplung ist oft fachlich notwendig | irreführender Unabhängigkeitsanspruch | `handoff_role` Pflichtfeld, getrennte Vergleichsdesigns; Architect | Konzept hoch |
| **F07** | Medium | Architektur | A+ ist kein nachgewiesener Universalsieger; für regulierte Mathematikprofile kann B/B+ überlegen sein. | Architektur-Falsifikation; [S04] ermöglicht Referenzformulierung; Gegenposition: B+ Governance-/Adoptionslast | falsche Investitions-/Standardentscheidung | Pilot mit A+/B+-Profile und Kostenmessung; Standards Board | offen |
| **F08** | Medium | Semantic integrity | Schema-Gültigkeit ist nicht vollständige referentielle/semantische Konsistenz. | CESM dokumentiert fehlende Referenzprüfungen im LinkML-Schema [S06]; Gegenposition: Runtime-Validation ist vorgesehen | verwaiste Port-/Link-Referenzen | Cross-reference/Unit/Invariance-Validator; Data Governance | Quellen hoch |
| **F09** | Medium | Governed release | SiennaSchemas ist im zugänglichen README pre-1.0, mathspec nennt Alpha-Status. | [S09,S10]; Gegenposition: gezielt gepinnte Versionen können produktiv genutzt werden | unkontrollierte Semantikdrift | Version-Pinning und Compatibility-Gates; Release Owner | Quellen hoch |
| **F10** | High | Method identity | Gleiche Eingabedaten mit anderem Speicher-Endzustand, Verlustmodell oder Referenzfall können andere CBA-Delta-B1 ergeben. | mathematische Gegenbeispiele in [CBA-Use-Cases](../analysis/cba_interoperation_scenarios.md); kein realer Multitool-Benchmark | falsche Äquivalenzannahme | Method Profile mit expliziten Defaults; Model Owners | Konzept hoch, empirisch offen |
| **F11** | High | Standard version | Für TYNDP 2026 liegt als hier geprüfte Quelle ein Konsultationsentwurf vor; finale 2026er Detailregel wurde nicht unabhängig bestätigt. | [S02] Deckblatt „Draft version“; [S01] ist EC-approved | fälschliche Normbehauptung | normativen Freigabestand aktiv erneut verifizieren; CBA Regulatory Owner | hoch für geprüfte Datei; endgültiger Stand offen |

## Priorisierung

**Blocker vor einem Entscheidungs-Piloten:** F02 (stille Verluste), F03 (Pairing/KPI), F04 (B6-Methodenpflicht), F05 (unabhängige Benchmark), F06 (M2-Rolle), F10 (Methodenidentität). Ohne geklärte Freigabefassung ist F11 zusätzlich ein regulatorischer Stopper für **offizielle** TYNDP-Claims.

**Offene Fragen:**
- Welcher Teil der Projektmethodik ist verbindlich gleich, welcher darf als begründete Sensitivität variieren?
- Welche mathematischen Funktionen jedes konkreten Konverters sind tatsächlich implementiert und **testweise** nachgewiesen?
- Ist eine Änderung des Projekt-NPV/Vorteilsvorzeichens methodisch erklärbar oder ein Fehler?
- Welche Unsicherheitsfamilien und Akzeptanzschwellen werden **vorab** vom zuständigen CBA-Owner genehmigt?
- Welche Version der TYNDP-2026-Implementation-Guidelines ist zum Studienzeitpunkt offiziell gültig?

**Terminologie:** „Critical“ bezeichnet ein hohes Risiko und erfordert ein Pilot-Gate; es behauptet nicht, dass im aktuellen CBA ein konkreter Fehler festgestellt wurde.
