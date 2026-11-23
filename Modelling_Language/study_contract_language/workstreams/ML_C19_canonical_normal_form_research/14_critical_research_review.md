# ML-C19/14 – Adversarial Critical Research Review (KI-intern)
2026-11-23. Dieses Review ist eine getrennte **Argumentationsrolle**, kein personell unabhängiger Audit, kein Owner-Signoff. Jeder Angriff bewertet gerade auch Entwürfe 05–13.

| Angriff | Falsifizierungsversuch / Gegenbeispiel | Schwere und Ergebnis |
|---|---|---|
| AR01 mathspec als E2/E4 missverstanden | a-(b-c) darf nicht beliebig über +/− sortiert; gleicher canonical yaml != gleiche external duties | HIGH: durch präzise E1-Abgrenzung abgefangen; native Probe fehlt |
| AR02 GEMS-Port als physikalische Vollsemantik | field power an Bus ohne carrier/sign/effizienz | HIGH: C2/C5/QuantityType ergänzt, noch kein End-to-End |
| AR03 SysML-Part erzwingt intern Modellstruktur | SOC-Ausprägung als PartUsage für alle Varianten | HIGH: Verbotsregel für unnötige interne Claims, Mapper ungetestet |
| AR04 KerML-Komplettimport bläht Kern auf | Inheritance/Multiplicity ohne fachliche Anwendung | MEDIUM: H0 gegen A/B/C offen; kognitive Last noch ungemessen |
| AR05 Unit-Konversion schafft falsche Physik | kgH2 gegen MW ohne Heizwertbasis, MW injection vs consumption | HIGH: Unit + physical_kind + sign + carrier guard, Converter incomplete |
| AR06 ähnliche Syntax verschmilzt Pflichten | KCL gegen KCL+KVL, Objective gleich gegen andere feasible region | CRITICAL: ausdrücklich verschiedene Assertions, E4 nur mit Proof |
| AR07 Source-/Owner-Wegnormalisierung | zwei Autoritäten A,B vereinigt; OWNER_TBD auf numerischen Default | CRITICAL: C9 plus audit_hash/immutable IDs, real roundtrip fehlt |
| AR08 Variablennamen als Identitätsbeweis | e und soc erscheinen verschieden, gemeinsame p-Spalte erscheint gleich | HIGH: Role- und Observable-Projektionen statt interne Identität |
| AR09 Normalform = mathematisch ausführbares Modell | C4 enthält frei gewählte Algebra-Operatoren/solver args | HIGH: keine Solver-/IR-Anforderungen im Kern |
| AR10 Parser-Normalisierung = Konformität | test_canonical success ohne Storage-/EV-Service-Zeugnis | CRITICAL: klare E1 vs C_pass/Pass Evidence |
| AR11 unbemerkte Freiheitsvernichtung | alle implementierer müssen PTDF oder ein storage state benutzen | HIGH: VariationPolicy enthält internal choice whitelist und Non-Mandate |
| AR12 full standard ohne Bedarf | komplette SysML-KerML-Zusammenführung | HIGH: Minimalitätsablations- und H0-Prüfung vorgesehen |
| AR13 canonical Hash bei Versionsdrift | gleiche Dateien, verschiedene Registry-Versionen/Defaultwerte | HIGH: versioned Hash + UNKNOWN migration |
| AR14 verteilte Alias-/Importschleife | recursive merges oder zwei namespace collisions | HIGH: R00/R10 fail-closed; Konfluenz unbewiesen |
| AR15 E5 als gefälschte Gleichheit | verschiedene Flexibility-Approximationen liefern gleiche Einzelzahl | CRITICAL: E5 nur joint contract conformance, nicht E4 |
| AR16 nicht geprüfte Servicefähigkeit | Batterie erfüllt einen Dispatch, kann aber kein zugesagtes Reserveprofil liefern | CRITICAL: getrennte Capability-Quantoren und EvidenceRequest |

## Besonders angreifbare Kernannahmen
1. **9 Rollen als kleinster Kern**: unbewiesen. Die Ableitbarkeit von AuthorityRecord, Observable und Variation aus Referent+Relation kann technisch weniger Klassen ergeben, aber mehr Validatorregeln. Kein signifikanter Vergleich A/B/C/H0 ausgeführt.
2. **Zulässige AND/OR-Rewrites in Bool3**: dreiwertige Guard-Logik und Partialitätsregeln müssen formal fixiert werden. Bei orderabhängigem Missing/short-circuit mit Nebenwirkung ist Sortieren unzulässig; R03 setzt reine Ausdrücke voraus.
3. **Vergleich Source/Authority-E2**: E2_obligation vs E2_audit muss als zwei getrennte Abfragen implementiert werden. Derselbe semantische Body mit zwei Quellen darf im Audit nicht auf eine Quelle schrumpfen.
4. **Kanonische Units**: Dimensionen/SI reichen nicht für H2 Heizwertbasis, Emissionsfaktoren, reale/nominale Währungen oder Wärme-/Elektrizitätsqualitäten.
5. **Funktionale Garantie ohne internal state**: Wärme-/Energieerhaltung kann nur mit einem vollständigen Trace, genügend Observables oder einem anerkannten Zertifikat nachgewiesen werden. Zu wenige Observables bedeuten INCONCLUSIVE, nicht automatisch PASS.
6. **SysML Nullhypothese**: Standards dokumentieren umfangreiche Semantik; um deren erforderliche **Eigenentwicklung** wirklich zu widerlegen oder zu bestätigen, braucht es profilierte tatsächliche Modellerstellung und export/import.

## Ausstehende Evidenz, Risiko und Mitigation
| Lücke | Risiko | Nächster Test |
|---|---|---|
| Native mathspec/GEMS/SysML mapping | hohe Map-Fehler | ML-C21 native examples + negative parser tests |
| Roundtrip Owners/Provenance | hohe Audit-Verluste | two-authority sources, owner TBD, evidence run import/export |
| Normalizer Soundness/Confluence | hohe fachliche Falschverschmelzung | property tests + critical pairs + formal small-step semantics |
| E3/E4 für Netz/Speicher | hohe falsche Konformitätsbehauptung | math proof protocol + independent reference cases |
| A/B/C Minimalität | hohe Komplexitäts-Spekulation | controlled blind authoring/ablation |
| Domain authority N2E, IoSN | High Governance Risk | Owner entscheidet; G1 BLOCKED |

## Kritisches Votum
**Konzeptuell gut begründeter Forschungsentwurf, aber ausdrücklich weder minimalitätsbewiesen noch native-validiert.** Die gefährlichste offene Hypothese ist, dass ein kleiner frei gestalteter Predicate-Baukasten ohne Domänen- oder Beweisverlust alle relevanten Guarantees trägt. Dieses Risiko ist nur mit formal typisierten Profilen, negativen Referenzfällen und Evidenzpolitik kontrollierbar. **Personell unabhängiger Review: NOT_EXECUTED.**
