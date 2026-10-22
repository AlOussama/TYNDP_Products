# ADR-ML-001: Gemeinsame Architektur für Energiesystemmodell-Interoperation

- **Datum:** 23.10.2026
- **Status:** **PROPOSED / CONDITIONAL**, nicht endgültig freigegeben
- **Scope:** TYNDP-/NEP- und CBA-Interoperabilität; **nicht** IoSN-Architektur
- **Normative Abhängigkeit:** geprüfter/freigegebener CBA-Methodenstand [S01], 2026er Detailnorm noch zu verifizieren [S02]

## Entscheidung als prüfbare Hypothese

Für die **allgemeine heterogene Interoperation** einen minimalen normativen semantischen Kern, freigegebene Methoden- und Transformationsdeklarationen sowie einen versionierten **Planning/Comparison Contract** als A+-**Basis** pilotieren. Unterschiedliche Toolmathematik ist nur innerhalb genehmigter Methodenprofile zulässig. Ein B-**Referenzmathematikprofil** wird bei 1:1-Translation/Conformance gezielt verlangt. Ein B+-Profil wird in regulierten Verfahrensbereichen geprüft, wenn **gleichzeitig** Referenzmathematik und explizit zugelassene unabhängige Methodenvarianten erforderlich sind.

**Nicht entschieden:** A+ als immer „besser“ als B+; GEMS als ungeeignet; generisches Minimalmetamodell als ausreichender universeller Standard.

## Begründung / Trade-offs

| Kriterium | Präferenz A+ (vorläufig) | Gegenargument für B/B+ |
|---|---|---|
| heterogene Markt-/Netz-/Adequacy-Toolchain | vermeidet Pflichtangleichung aller Modellgleichungen | strikte Gleichheit ist in Teilklassen wichtig |
| Robustheit | genehmigte Methodenvariation sichtbar und testbar | B+ kann Methoden unter kontrollierter Referenz strenger vergleichen |
| Konformität | B-Zusatzprofil nötig | B stellt eindeutige algebraische Referenz bereit |
| Fehlerrisiko | heterogene Ansätze können Strukturfehler aufdecken | unbemerkte semantische Defaults gefährden A+ besonders |
| Governance/Adoption | erfordert Contract-/Adapterregeln statt Universal-Compiler | B+ kann trotz Mehrkosten in stark normierten Prozessen effizienter sein |

## Falsifikation / Rollback

**A+ zugunsten B/B+ revidieren**, falls (i) die CBA-Fachautorität exakt gleiche Algebra vorschreibt, (ii) B+-Profilerstellung nachweislich geringere Gesamtkosten und weniger ungeklärte Ergebnisabweichungen hat, (iii) unabhängige Modelle unter A+ selbst nach Methodenregeln fachlich nicht vergleichbar werden, oder (iv) die Kernsemantik unvermeidbar eine voll ausführbare Algebra erfordert.

**B/B+ ablehnen oder enger begrenzen**, falls (i) zwingende mathematische Normalisierung legitime wichtige Modellklassen verlustbehaftet abbildet, (ii) Common-Mode-Fehler nicht unabhängig geprüft werden können, (iii) mehrere genehmigte Methoden nicht als Profile abbildbar sind, oder (iv) Adapterverluste ohne Stop-Gate bleiben.

## Qualitäts- und Entscheidungsbedingungen

Vor einer verbindlichen Auswahl **alle** Critical Findings F02/F03 auflösen, Normstatus F11 klären, Fehler-Injection/1:1/Robustheits- und M1→M2-Tests aus [CBA Pilot](cba_pilot_plan.md) durchführen, Versionen/Capability-Gates pinnen, unabhängige fachliche Gegenprüfung einholen und anschließend den ADR auf **ACCEPTED/REJECTED** aktualisieren.

## Trennlinie des gemeinsamen Standards

- **MUSS gemeinsam:** Komponenten-/Port-/Commodity-Identität, Einheiten/Vorzeichen, Zeit/Raum/Szenarien, Referenz-/Projektfall, Methoden-/Tool-/Transformation-ID, Verlustklassen, KPI-Bedeutung, Audit und Governance.
- **Optional mathematisch verbindlich:** Algebra/Variablen/Bounds/Zielfunktion/LP-/MILP-/stochastische Formulierung für **benannte Modellprofile**, unabhängige Compiler-/Conformance-Tests.
- **Bewusst unabhängig:** sachlich zulässige Methoden-, Struktur- und Szenariovariation zur Robustheitsprüfung. Independente Toolimplementierungen müssen ihre Abhängigkeiten offenlegen.

### Entscheidungs-Owner

Noch **nicht** einer realen Organisation/Person zugewiesen. Erforderliche Rollen: CBA Method Owner, Regulatory Owner, Data Steward, Energy Modelling Leads, unabhängiger Reviewer. Ohne Sign-off dieser Rollen bleibt der ADR **PROPOSED**.
