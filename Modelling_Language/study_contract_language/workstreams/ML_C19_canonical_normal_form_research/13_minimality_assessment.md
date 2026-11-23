# ML-C19/13 – Minimalität, Redundanz, Ablation und K12/K17
Status Forschungsbewertung, 2026-11-23. Keine mathematisch bewiesene Minimalität, keine kontrollierte Human-Authoring-Studie. Ziel ist *minimale Semantik ohne Verlust*, nicht minimale Dateigröße.

## Prüfmodell
Total Complexity Cost T = w1*CoreConcepts + w2*PrimitiveOperators + w3*ValidatorRules + w4*CrossReferences + w5*AuthoringBurden + w6*SemanticLossRisk. Die Gewichte w1..w6 sind **OWNER_TBD**; daher wird weder eine willkürliche Gesamtzahl noch eine angeblich optimale Architektur ausgegeben. Jede Variante muss SLR01–42, NFR01–18, K02–K09 und identische RC01–10-Vektoren tragen. Unbekannter Fähigkeitsstatus = NOT_EVALUATED, nicht 0.

## Ablationsmatrix der 9 Kandidatenrollen
| Rolle | Ablation und konkrete falsche Akzeptanz | Möglicher struktureller Merge |
|---|---|---|
| ContractFrame C1 | RC09 CBA ohne gemeinsame Basis/Counterfactual akzeptiert | Scope zu Referent; Sinn und Geltung müssen bleiben |
| Referent C2 | RC03 Strom/H2 Port ohne Carrier-Identität | nicht sicher entfernbar |
| TypedRelation C3 | RC05 physikalischer Link vs Market Link verwechselt | zu getypten Kanten statt eigenständigen Objekten |
| Predicate C4 | RC07 Infoset/Guard als Prosa unprüfbar | als typed AST eingebettet in Assertion |
| ScopedAssertion C5 | RC01 Requirement vs Permission verliert Pflichtstärke | nicht ohne explizite Modalität |
| Observable C6 | RC08 gleiche KPI-Namen bei unterschiedlicher Preisbasis | als Referent-Unterart, Projektor muss bleiben |
| Variation C7 | RC10 Strukturunterschied irrtümlich E4-Fehler oder unbemerkt erlaubt | als spezialisierte Assertion mit Policy-Typ |
| Evidence C8 | RC10 nicht ausgeführter Test als PASS | Evidence unter Referent + typed Relation; Status bleibt |
| Authority C9 | RC09 N2E-OWNER_TBD und Quellenverlust | in getypte Referents + immutable provenance multiset |

Ablation beweist **Notwendigkeit der Unterscheidungen**, nicht notwendige Klassenanzahl. Formal mögliche technische Kodierungen: (i) 9 explizite Rollen, (ii) 5–6 generische node kinds mit strengem Tagsystem, (iii) KerML-Profile ohne eigene classes. Vergleich muss die Typcheck-/Fehlerdiagnostik-Mehrkosten im zweiten Fall berücksichtigen.

## NFR-Redundanz und Profilgrenzen
NFR01 determinism ≠ NFR02 idempotence; NFR03 semantic preservation ≠ NFR14 adapter roundtrip; NFR05 normative state ≠ NFR12 authority provenance. NFR08 time/scenario ≠ NFR07 physical quantity, trotz Energieintegration. NFR09 port structure ≠ NFR10 modelling freedom. NFR17 undecidable equivalence ≠ NFR18 unknown input. Reduktion auf 11 Klumpenkriterien würde Messbarkeit kosten; 18 Forschungs-NFR bleiben, können jedoch thematisch gruppiert berichtet werden.

## Quantitative Messgrößen und bisheriger Wert
| Metrik | Formel | ML-C19 Stand |
|---|---|---|
| Core size | Count(C_i) | 9 Kandidaten, keine Optimalaussage |
| Fully normalisable share | #SLR with sound + tested complete E1 rules / 42 | NOT_MEASURED |
| Obligation preservation | #preserved mandatory clauses / #source clauses | NOT_MEASURED |
| Owner preservation | #unchanged decision/status links / total | DESIGNED, not complete |
| Extra types/operators | #beyond C1-C9 and Bool typed predicates | formal inventory provisional |
| Negative detection | #rejected intended negative vectors / #tested | subset microcheck only, cannot generalize to all RC |
| Unresolved interpretations | #OWNER_TBD and ambiguous refs | open, nonzero; no fabricated count |
| Forced modelling decisions | #unnecessary internal states/constraints mandated | 0 by design hypothesis; NOT_TESTED |
| Roundtrip semantic loss | #lost obligation/status/provenance links | NOT_EXECUTED full export |
| Repeatability | N(N(C)) = N(C) on emitted outputs | subset demonstrator only |
| Normalizer complexity | transformation count, branches, critical pairs | 14 proposed rules, not final |
| Independent authoring | time/error/disagreement across blinded modelers | NOT_EXECUTED |

## Vergleichsprotokoll A vs B vs C vs H0
Fünf Gruppen sollen mit denselben Contract-Inputs die RC01/03/05/07/08/09/10 erstellen, (i) ohne Hilfen (ii) mit bewussten Fehlmutationen, (iii) export/reimport mit Version/Owner/Provenienz, (iv) alternative Algebra M1/M2. Erhebe median authoring time, first-pass errors, unclear-spec questions, validator actionable error ratio, required metaclass count und code paths. Human reviewers unabhängig von Erstellung notwendig. Anzahl Nodes/Dateizeilen allein wird nicht als Erklärvariable für semantische Reife akzeptiert.

**Ergebnis:** Minimal-core-Hypothese mit neun unterscheidbaren Bedeutungsrollen; Ablation KONZEPTUELL, gemessener Minimalitätsnachweis UNVOLLSTÄNDIG. Nullhypothese H0 (kleines SysML-Profil genügt) OFFEN.
