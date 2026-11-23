# ML-C19/15 – CSNF Research Decision Brief, F1–F15 und 15-teiliges Abschlussvotum
2026-11-23, Version research-r0, **NON-NORMATIVE**. Kein verbindlicher Architektur-, DSL-, Source- oder Ownerentscheid. Ausgangsstand ML-C18 `5555be36f74d1d4f6e871d4503c1fc91e417e57c`; ML-C18 SLR01–42, K01–K17 und RC01–RC10.

## Kernergebnis
Die fachlichen Unterscheidungen **Scope/Guard, Normativität, Außenkomponentenrolle/Port, Annahme-vs-Garantie, Observable/Beleg, zulässige Variation und Quellen-/Owner-Autorität** sind nicht optional. Dagegen ist ihre Implementierung als 9 Rollenfamilien (C1–C9 aus 05) lediglich ein Designkandidat. Der benötigte Contract ist strenger als eine GEMS-Portdeklaration, semantisch höher angesiedelt als eine mathspec-Formulierung und schmaler als das vollständige KerML/SysML-Metamodell.

### Explizite Antworten auf F1–F15
| Frage | Forschungsergebnis | entscheidender Vorbehalt |
|---|---|---|
| F1 kleinster vollständiger Kern | C1–C9 mit getypten Scopes, Predicates, Sources; Semantikdifferenzen zwingend | Klassenzahl 9 **hypothetisch**, nicht minimalitätsbewiesen |
| F2 mathspec direkt | Parse/typed AST/kanonisches Drucken, geordnete/ungeordnete Kollektionen, lokale kommutative Regeln, negative/fixed-point/roundtrip Testmuster | keine universelle mathematische oder fachliche E2/E4-Normalisierung |
| F3 GEMS-Konzepte | Library/System Definition/Instance, port-types/fields, Verbindungen, Taxonomie, Binding/Views als semantische Inspirationsquellen | GEMS Port überträgt mathematische Felder, kein vollständiger Energiemengenvertrag |
| F4 KerML/SysML Reuse | Type, Feature, Membership, Namespace, Multiplicity, Part/Port Definition & Usage, Connection, Requirement/Constraint, VerificationCase | keine native CSNF-Governance/Variation garantiert |
| F5 SysML/KerML als Grundlage? | grundsätzlich möglich mit kontrolliertem Profil und externer Contract-Scope-Regel | komplette KerML-Oberfläche nicht als Minimalitätsnotwendigkeit belegt |
| F6 sichere Normalisierungen | typisierte Aliasauflösung, ungeordnete Mengen, reine AND/OR, explizite exakte Unit/Time-Konversion, Audit-preserving Ref/Status Sort | nur mit Guards und RuleSet R00–13, keine freien algebraischen Umschreibungen |
| F7 nicht automatisch | REQUIRED vs PERMITTED; OWNER_TBD vs Default; PASS vs NOT_EXECUTED; MW Injektion/Verbrauch; KCL vs KCL+KVL; branch vs market-link; Source-ID | unbekannt => BLOCKED/INCONCLUSIVE |
| F8 Modelling Freedom | VariationPolicy betrifft interne Zustände, Koordinaten, Variablen, Constraints, Solver bei gleichen äußeren Verpflichtungen | Capability/Service & Trace Guarantees müssen weiterhin nachgewiesen werden |
| F9 E2/E3/E4 | E1 kanonische Gleichheit, E2 Pflichtgleichheit, E3 sichtbare Äquivalenz, E4 math feasible/projection & objective, E5 erlaubte Nichtäquivalenz | E5 kein E4; E3 kann stichprobenbezogen sein |
| F10 Source, Owner, Provenance | C9 AuthorityRecord + unverlierbares Audit Ledger und differenzierte semantic/audit hashes | keine reale Export/Import-Verlustprüfung |
| F11 ohne Solver | syntactic graph/type/unit/ref/status-Checks, endliche Bool-Guards, lokale Widersprüche, konservative Unknown-Prüfung | keine allgemeine Sat/E2/E3/E4-Entscheidung |
| F12 Erweiterungen | fachlich getypter Port+Carrier/Sign, scoped A/G & service capability, Variation/Status/Authority, Observables/Evidence, ComparisonContract | nur nach Test entscheiden, ob eigene Sprachklassen oder SysML-Profile |
| F13 eigenständiger Kern notwendig? | gemeinsame Bedeutungsreferenz für Föderation höchst plausibel | Nullhypothese kleines SysML-/KerML-Profil **offen** |
| F14 geringste belegte Komplexität | **nicht nachgewiesen**; A, B, C, H0 gleichartig verglichen, aber nicht in Aufwand/Roundtrips gemessen | kein Sieger aufgrund gefühlter Einfachheit |
| F15 Übergabe | C1–C9, R00–13, I01–I10, E1–E5, RC01–10 + negative Witnesses, Quellenpins, Statussemantik an C20/C21 | Handoff konzeptionell, Validator und Parser nicht implementiert |

## Drei Sprachquellen: belegte Trennung
**mathspec:** aktuell angegebener Analyse-Pin `5f1464c334c1012cdee2947d4d55b4d1d6bef40a` enthält `_canonical.py` und `tests/test_canonical.py` mit implementierten AST-Normalisierungen, Idempotenz-/Roundtrip- und Negativtests. Re-Check am 23.11.2026: `main` steht zwei Commits weiter bei `9e9b356df9d7236ff3c9d4f4b89f92c3edd8fbc4`; Vergleich umfasst `_sos.py`, Changelog/Docs/Tests, **nicht** `_canonical.py` oder `tests/test_canonical.py`. Die Forschung analysiert unverändert den expliziten Pin, Versionsdrift dokumentiert.
**GEMS:** `main` identisch mit `c463e30b610443c1f59b20074bb7acffa2844cce`. Library/System/Port sind **dokumentiert**; keine nativen ML-C19-RC-Interpreterläufe.
**OMG:** SysML Language 2.0, KerML 1.0 und Systems Modeling API 1.0 normative Basis, getrennt von Pilot Release `2026-09.1`. Quellen-/Profil-Mapping **konzeptionell**, keine native Prüfung.

## 15-teiliges Forschungsvotum
| Prüfgebiet | Status | Begründung / Gate |
|---|---|---|
| CSNF_REQUIREMENTS_COMPLETENESS | RESEARCH_REQUIREMENTS_SPECIFIED | 18 NFR mit SLR/K-Bezug; externe Bestätigung fehlt |
| MATHSPEC_CANONICALIZATION_REUSE | SOURCE_SUPPORTED_PARTIAL | echte AST-Regeln und vorhandene Tests; CSNF-Adaption unimplementiert |
| GEMS_COMPONENT_SEMANTICS_REUSE | DOCUMENTED_SUPPORTED_PARTIAL | Port-/Graph-Muster belegt; physikalische Contract-Felder ergänzen |
| SYSML_KERML_SEMANTICS_REUSE | NORMATIVE_CONCEPTS_IDENTIFIED | Requirements/Constraints/Ports/Types; Profile getestet? nein |
| MINIMAL_CANONICAL_CORE | HYPOTHESIS_9_ROLES | Klassen-/Operator-Ablation offen |
| NORMALIZATION_SOUNDNESS | PARTIAL_SYNTHETIC_ONLY | ruleset v0, kleine Probe 22/22; kein universeller Beweis |
| SEMANTIC_EQUIVALENCE_BOUNDARIES | CONCEPTUALLY_SPECIFIED | E1–E5 und Beweisgrenzen explizit |
| MODELLING_FREEDOM_PRESERVATION | DESIGN_INTENT_NOT_PROVED | interner algebraischer Freiheitsraum nicht gemessen |
| SOURCE_AND_PROVENANCE_PRESERVATION | DESIGN_INTENT_NOT_ROUNDTRIPPED | dual ledger, source multiset, Statusbedingungen |
| COMPONENT_CONTRACT_SUITABILITY | DESIGN_CASES_NOT_NATIVE_VALIDATED | Batterie/EV/Electrolysis/H2 externe A/G-Skizzen |
| ARCHITECTURE_OPTIONS_COMPARISON | QUALITATIVE_NOT_SCORED | A/B/C und H0 untersucht, 17 K im Vergleich |
| MINIMALITY_EVIDENCE | INSUFFICIENT | 9-Rollen-Ablation nur Argument, kein unabhängiger Authoring-Test |
| FORMAL_VALIDATION_READINESS | PARTIAL | typed diagnostics + negative Orakel spezifiziert, kein Parser |
| ARCHITECTURE_DECISION_READINESS | NOT_READY | H0 und Kosten-/Human-Experiment offen |
| HANDOFF_TO_ML_C20_AND_ML_C21 | CONDITIONAL_RESEARCH_HANDOFF | versionierte RuleSet-/Profile-Baseline, keine produktive Freigabe |

## Konditionale Empfehlung
**Empfohlene Forschungsrichtung, keine Architekturentscheidung:** A als **prüfbares minimales semantisches Referenzmodell** prototypisieren und gleichzeitig B/H0 mit ausschließlich externen SysML-Konstrukten sowie C mit verlustkontrollierten Adaptern auf denselben Testfällen vergleichen. Eine formal profilierte SysML-/KerML-Repräsentation kann den eigenen Kern ersetzen, falls die vollen fachlichen Verpflichtungen/Owner- und Audit-Informationen bei weniger real gemessener Komplexität erhalten bleiben. mathspec liefert das Rewrite-/Testmuster; GEMS die Schnittstellen-/Graphmuster. Kein solches Fremdformat soll automatisch die gemeinsame Optimierungsalgebra erzwingen.

**Governance:** Keine neue DSL, keine normative IoSN-Entscheidung, D1–D6 unverändert, offene MD/CL und N2E-Authority offen; **Gate G1 bleibt BLOCKED**. Kein personell unabhängiger Audit.

## Forschungsquellen
[ML-C18 r1](https://github.com/AlOussama/TYNDP_Products/tree/5555be36f74d1d4f6e871d4503c1fc91e417e57c/Modelling_Language/study_contract_language/workstreams/ML_C18_general_contract_language_research), [mathspec source](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/_canonical.py), [mathspec canonical tests](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/tests/test_canonical.py), [GEMS Library](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/library.md), [SysML](https://www.omg.org/spec/SysML/2.0/Language/PDF), [KerML](https://www.omg.org/spec/KerML/1.0/PDF).
