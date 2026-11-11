# ML-R02 — Architecture Decision Proposal (NOT AN ADR)
**Datum:** 2026-11-11 · **status:** RESEARCH_PROPOSAL_ONLY / DECISION_DEFERRED · **G1:** BLOCKED.

## Entscheidungsvorschlag (bedingt und falsifizierbar)
**Kein Architekturbeschluss.** Für die spätere Evaluierung ist eine **modulare Registry-/Profilarchitektur (A)** als *Arbeits-Hypothese* sinnvoll, **falls** eindeutig versionierbare Fach-/Math-/Data-Profile unterschiedliche Governance-/Änderungszyklen haben und ihre Cross-Profile-Closure reproduzierbar überprüfbar ist. Bei anderen Integrationsbedingungen kann ein einheitliches **integriertes Metamodell (B)** zweckmäßiger sein. Weder A noch B hat hier einen nachgewiesenen wissenschaftlichen IoSN-Konformitätsvorsprung.

**Nicht delegierbarer Kern:** stabile MA01-SR-IDs, Quelle/Gültigkeitsstatus, Identität/Units/UTC, widerspruchsfreie Energie-/Netzrollen, Invarianten-/Verification-Registry, Evidenzstatus und fail-closed guards. **Erweiterungskandidaten statt Pflichtsprachen:** ReqIF für RM-Austausch; SysML v2 für MBSE/Prozess; LinkML/JSON Schema + ggf. SHACL für Daten/semantische Referenzen; GEMS/mathspec für mathematische Repräsentation; INES/CESM/SiennaSchemas als Input- oder Modellstruktur-Adapter mit verpflichtender methodischer Gap-Dokumentation. Keine dieser Komponenten wird hier als Sieger erklärt.

## Abhängige Forschungsfragen
1. **L3/L4-Vollständigkeit:** Welche Verpflichtungen brauchen eigene formale Operatoren, welche reichen als Mess-/Prozess-/Review-Oracle? P05/P06 Netzreduktion und P10–P12 Mathematik getrennt untersuchen.
2. **D2 vs O26:** Fünf gemeinsame CY-IDs sind Projektforschungsprofil, keine automatisch gültige O26-Methodiknorm. Versionen und Ausnahmecharakter im Contract halten.
3. **Math-Äquivalenz:** Nicht algebraische Identität, sondern source-gebundene Constraint-Familien, Dimensions-/Indexprüfungen, risk-based Golden Fixtures und äquivalente resultierende Modellpflichten verlangen.
4. **Standards-Referenzimplementation:** Parsbare **native** SysML-/ReqIF-/LinkML-/GEMS-/mathspec-Mikromodelle erstellen, bevor technische Machbarkeit behauptet wird.
5. **Version/Migration:** Pinning, controlled change, semantische Backward-Compatibility, Audit-Trail, Profile-Owner und Regression über zwei Modellierungswerkzeuge.
6. **Governance:** Wer kann Profile, Ontologie, Testoracles und Konformitätsberichte autorisieren? Workflow bereiten, Freigabe aber verschieben.

## Spätere entscheidungsrelevante Experimente
Metriken: 48/48 maschinenlesbare Quell-/SR-/L3-/L4-Kanten; P00–P17 mit Guards; 8/8 Referenzfamilien prüfbar; mindestens zwei unabhängig entwickelte Tool-Implementierungsmodelle; explizite `UNSUPPORTED`-Abbildung; definierte echte Datenhashes und mathematische Golden Oracles; Simulationsfehler-Injektion; Change-Impact und kontrollierte Migration; Aufwand pro Profiländerung, Parser-/Adapter-Wartung und Operator-Coverage. **Nicht jetzt ausführbar:** vollständiger Daten-/Methodik-Runtime-Test mangels G1.

## Abnahmegrenze
`G1_REMAINS_BLOCKED`, `AUTHORITY_UNCONFIRMED`; 21 Owner-/Methodik-Entscheidungen und reale Daten-/Testoracles fehlen. Keine normative Sprache, keine verpflichtende Modellübersetzung, keine Produktionsadapter, keine endgültige ADR, kein Merge/Ready. Integration mit anderen unabhängigen Forschungszweigen **erst später**, keine gegenseitige Vorwegnahme.
