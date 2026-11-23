# ML-C19/06 – Formale Semantik und Invarianten (CSNF research-r0)
**Formaler Forschungsentwurf**, bewusst keine vollständige Entscheidungsprozedur für mathematische Gleichwertigkeit. Bezug: [05](05_csnf_core_concepts.md), [07](07_normalization_rules.md), [08](08_equivalence_and_freedom.md). Notation ist metasprachlich, keine zukünftige DSL-Syntax.

## 1 Syntax, Typen, referenzielle Struktur
Ein Contract ist der endliche Tupelgraph C=(H,R,L,P,A,O,V,E,U), entsprechend C1–C9. In H sind Schema-, Regel- und Einheitenregistrierungs-Version gespeichert. Jeder Knoten hat eine stabile eindeutige ID, einen kind-Tag und referenzierbare SourceSpan-IDs. L enthält ausschließlich im Typsystem deklarierte Relationsarten. Die Menge der Symboldefinitionen Γ(C) bindet Qualified IDs auf getypte Referents, Einheitentypen, Aussagen, Owner und Regeln.

**Syntaktische Gültigkeit** W(C): Wohlgeformtheit gegenüber einer versionierten abstrakten Grammar/Schema-Definition, eindeutig parsbare Token/Strukturen, deklarierte Knotenarten und korrekte Kardinalitäten. Kein konkretes Text/YAML gewählt.
**Typkorrektheit** Γ ⊢ C : ok: jede Referenz löst eindeutig auf; alle Operatoren haben definierte Domain-/Codomain-Typen; Port/Connection-Carrier und QuantityType kompatibel; Einheiten sind physikalisch kompatibel einschließlich Sign, support und conversion basis; Gauards sind Bool3/Bool-typed; Source-/Status-Referenzen valide. Die Unit-Dimension allein garantiert keinen gleichen Energieträger und keine gleiche physical_kind.
**Lokale Widerspruchsfreiheit** Cons_local(C): kein REQUIRED(P) und PROHIBITED(P) für dieselbe Sachbehauptung und überlappenden Guard/Scope; no incompatible exclusive scalar bounds; no contradictory policy. Wo Scope-Overlap/Prädikat-Entailment nicht entscheidbar: UNKNOWN statt CONSISTENT.
**Globale Erfüllbarkeit** Sat(C): es existiert mindestens ein zur Semantik gehörendes zulässiges System-/Umweltverhalten, welches alle Pflichtaussagen erfüllt. Diese Aussage kann unentscheidbar sein; Cons_local ist notwendig, nicht hinreichend für Sat.

## 2 Bedeutung
Definiere D=(PhysicalWorlds, Time, Scenarios, EvidenceWorlds, Authorities); eine Interpretation I ordnet Referents fachliche Rollen, QuantityTypes physikalische Größen, Predicates dreistufige Wahrheitswerte {true,false,unknown}, und Observables total/partielle Projektionen zu. T(M,e) ist die Menge der von einer Implementierung M in zulässiger Umwelt e erzeugbaren Traces. pi_{C,M}(t) ist ihre getypte Contract-Projektion; pi ist nicht automatisch injektiv und nicht zwingend total.

Applicability eines Assertions a: Scope_a(w) AND Guard_a(w) im expliziten dreiwertigen/partiellen Sinn. Unknown Guard löst keine implizite Pflichtfreigabe aus; die Konformitätsentscheidung wird BLOCKED/INCONCLUSIVE, je Policy.

Die effektive REQUIRED-Garantie hat bedingte Bedeutung:
  fuer jedes zulaessige e, jedes Trace t in T(M,e), falls Scope_a(t,e) und Assumptions_a(e,t) nachweislich true, dann Guarantee_a(pi(t)) = true.
Eine REQUIRED Service/Capability-Aussage besitzt zusätzlich quantifizierte Bedeutung, z.B.
  fuer jede zulässige Service-Anforderung d existiert eine zulässige Kontrolle/Antwort u, so dass der geforderte Service in allen zugelassenen Umweltentwicklungen gewährleistet ist.
Die Quantorenfolge muss Teil des Predicate sein; ein einzelner erfolgreicher Dispatch belegt diese universelle Fähigkeit nicht.
PROHIBITED(P) = REQUIRED(not P) nur wenn Scope/Guard/Unknown-Semantik gleich und Negation im gewählten Fragment wohldefiniert ist; andernfalls getrennte Operatoren konservieren.
PERMITTED(P) legitimiert eine Option relativ zur VariationPolicy, erzwingt keine Existenz, physikalische Zulässigkeit oder tatsächlichen Einsatz.
IMPLEMENTATION_DEFINED erfordert Offenlegung einer gewählten Alternative samt Provenienz, kein Eigentümer-Default.
DATA_ASSUMPTION validiert Eingangsdaten und ist keine Verhaltensgarantie.

## 3 Definition der Normalform und Gleichheitsklassen
Wähle eine endliche versionierte Regelmenge R_v und deterministische Phasenfolge. N_v(C) ist das Ergebnis von parse -> type/resolve -> expand-known-explicit (nur sichere Defaults) -> rewrite -> sort unordered -> canonical serialize mit getrenntem Original- und Audit Ledger. C ist normalisiert gdw N_v(C)=C im kanonischen Strukturraum.

E1(C,D) gdw N_v(C).semantic_graph = N_v(D).semantic_graph **einschließlich** für Gleichheit relevanter Guards, Normativität, Policy/Scope und getypter Relation, mit gleicher Registry-/Regelversion. Für audit-identischen Contract ist zusätzlich Audit Ledger incl. Quellenmultimenge gleich. E1 impliziert nur Gleichheit **im Regelfragment R_v**, keine universelle E2-Erkennung.

E2(C,D): gleiche Menge von fachlichen Geltungspflichten und Rechte-/Normativitätsbedingungen in allen zugelassenen Interpretationen des vereinbarten Domain-Modells, inklusive Gültigkeit und relevanten Governance-Status. Die Authorities können unterschiedliche einzelne Nachweise derselben Pflicht referenzieren: daher unterscheiden wir E2_obligation und E2_audit. Ein E2_obligation Urteil darf niemals Source-/Approval-Provenienz löschen oder als vollständiger E2_audit ausgegeben werden.

E3(M1,M2; O,S,epsilon): relevante beobachtbare Projektionsmengen stimmen unter angegebenem Scope S, relevanten Observables O und Vergleichsregel epsilon überein (ggf. Verteilung/äquivalente Decision-Rule statt punktweise Gleichheit). Ein identischer zufälliger Einzeloutput reicht nicht.
E4(F1,F2; H,pi): unter dokumentierten Modellvoraussetzungen H stimmen Projektionen der gesamten zulässigen Lösungsräume und die verglichenen Zielfunktionswerte/Präferenzrelationen auf den definierten Projektionen überein. Ein Objective-Skalar allein reicht nicht.
E5(M1,M2; C): beide erfüllen Contract C, obwohl ihre internen zulässigen Lösungsräume/Strukturen verschieden sein dürfen. E5 ist *keine* Äquivalenzrelation im mathematischen Sinne, sondern ein Zulässigkeitsurteil über Nichtäquivalenz.

**Bedeutungserhaltung:** für jeden einzelnen erlaubten Rewrite r mit Γ ⊢ C ok gilt Interpret(C)=Interpret(r(C)) auf dem definierten typisierten/guarded Fragment und AuditProjection(C)=AuditProjection(r(C)); vollständige Nachweise für alle Domänen sind noch offen.

## 4 Unveränderliche semantische Invarianten
I01 source IDs, Dokumentversionen und authority-ranked claims erhalten; I02 normative and decision statuses erhalten; I03 scope/guards und A/G Richtung erhalten; I04 carrier, dimension, quantity kind, unit basis und sign erhalten; I05 temporal support, weights und scenario info-set erhalten; I06 Portidentität, Verbindungstyp und Cardinality erhalten; I07 Service-/Capability-Quantifizierung erhalten; I08 Variations-/Disclosure- und interne Freiheitsmengen erhalten; I09 Observable-Projektoren, Basis und Toleranzen erhalten; I10 VerificationRequest vom tatsächlich gelieferten EvidenceRecord trennen.

## 5 Status der algorithmischen Prüfbarkeit
- Rein statisch: W(C), Γ-Typchecks und eindeutige IDs, known unit conversions, deklarierte status enums, deterministic sort, lokale Konfliktmuster im eingeschränkten Predicate-Fragment.
- Statisch oder SMT/Constraint-gestützt nach Profil: Scope-Overlap, kleine finite Guards, Symbolic unit consistency, stage information-set-Consistency.
- Im Allgemeinen nicht automatisch: globale Erfüllbarkeit beliebiger dynamischer Contracts, E2 in freier Logik, E3 über unendlich viele Traces, E4 mit Integer/Nonconvex/Optimierungsbedingungen, E5 wissenschaftliche Echtheit.
- Ergebnisstatus jeweils PASS / FAIL / BLOCKED / INCONCLUSIVE / NOT_EXECUTED plus Evidenzart und Run-ID.

## 6 Normalform-Dualität
semantic_hash := Hash(schema_version, ruleset_version, registry_ids, canonical normative graph); audit_hash := Hash(semantic_hash, ordered canonical multiset of authority/source/decision/evidence IDs). Beide sind *HYPOTHESEN* bis ein kanonisches Binary/Text-Encoding festgelegt ist; Hash-Kollisionen sind nicht ausgeschlossen. Gleichheit nur nach vergleichbarer Versions-/Registry-Basis oder belegtem Migration-Mapping. Originalsprache mit SourceSpans wird separat bewahrt; kanonische Darstellung verliert keine fachliche Herkunft.
