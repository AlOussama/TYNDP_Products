# ML-C19/02 – mathspec-Kanonisierung: Implementierungsanalyse
Stand 2026-11-23. PIN energy-models/mathspec @ 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; untersuchte Dateien: [source _canonical.py](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/_canonical.py), [tests](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/tests/test_canonical.py), [spec.py](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/spec.py). Quelle wurde in ML-C19 mittels Github-Dateiabruf gelesen; Tests selbst **nicht** mit mathspec-Paket neu ausgeführt.

## Tatsächlicher Pfad von to_yaml(canonical=True)
In spec.py ist Spec.to_yaml(canonical=True) an canonical_yaml delegiert. _canonical.py: canonical_yaml(spec) = dump_yaml(canonical_dict(spec)). canonical_dict nutzt spec.model_dump(exclude_defaults=True), traversiert abschnittsweise und schreibt Expressions und Conditions nach *Parse -> Normalise -> Print* um; es ist keine textuelle Regex-Sortierung. Normales to_yaml() bewahrt die eingelesene Schreibweise besser; der Test test_two_files_that_mean_the_same_thing_write_the_same_text stellt ausdrücklich beide Modi gegenüber.

AST-Grenze: ArithmeticNode, BinaryOperatorNode, UnaryOperatorNode, FunctionCallNode, ComparisonNode, NameListNode, ColumnsNode; Bedingungen mit And, Or, Not, BooleanLiteral, NameNode, UnresolvedComparisonNode, UnresolvedConditionCallNode, UnresolvedCountNode. Die Normalisierung arbeitet auf geparsten Syntaxbäumen und abgeleiteten validierten Spec-Daten, nicht auf einem Energie-System-Contract-Graphen.

| Mechanismus | Implementierte Behandlung | bewusst erhaltene Grenze |
|---|---|---|
| Summe | _signed_terms, _signed und _sum: Vorzeichen falten, unter Plus verschachtelte +/- Terme flatten, nach Text+Vorzeichen sortieren, linksassoziativ drucken | unter Minus geklammerte Summe NICHT distributiv umschreiben; a-(b-c) bleibt gruppiert |
| Produkt | _factors rekursiv flatten, Faktoren sortieren | Division ist einzelner Faktor; kein Umordnen von / und ** |
| Vergleich | beide Seiten jeweils normalisieren, Operator und Seitenreihenfolge erhalten | x<1 nicht gleich 1>x als E1 |
| Funktionsaufruf | Keyword-Argumente sortieren; Argumentausdrücke rekursiv behandeln | positionale Argumente bleiben in Reihenfolge, z.B. max(b,a) |
| Indizes | NameListNode und ColumnsNode lexikalisch sortiert, wenn die verwendete Grammatik eine Menge meint | geordnete Zeitachsen/Dimensionen und semantische Ordinalität bleiben |
| Bedingungen | AND/OR gleichartiger Ketten flatten/sort, boolsche Keywords normieren, passende Klammern | NOT bleibt als Struktur, keine beliebige de-Morgan-, Absorptions- oder Theorem-Prover-Transformation |
| Sections | Modellfeldreihenfolge, Einträge nach Name; nested given-Sections und cases nach Name | piecewise links bleiben in der ursprünglichen Reihenfolge |
| Textlayout | laid_out schreibt Summenterme zeilenweise für nachvollziehbare Diffs | Layout ist kein Beweis mathematischer Formulierungsäquivalenz |

Ein absichtlicher Sonderfall: numerische Default-/Missing-Angaben 1 vs 1.0 werden für geeignete Spec-Typen gleich serialisiert (Tests 293–306). Ergebnis von model_dump(exclude_defaults=True) ist nicht die ursprüngliche Quelle; source-preserving und normalized representation müssen als getrennte Artefakte behandelt werden.

## Vorhandene Testnachweise, präzise Grenzen
- test_canonical.py Zeilen 50–73: gleiche Normalform trotz Entry-/Summen-/Faktorreihenfolge; nichtkanonische Dumps bleiben verschieden.
- 76–87: Parser->kanonischer Dump->Parser->kanonischer Dump als Fixpunkt für vorhandene Test-Specs.
- 89–113: Vorzeichen, Summe, Produkt, Positionsargumente, Division, Exponent.
- 227–338: Bedingungen, Referenzspalten, Keywordargumente, Missing und NOT-Klammern.
- 341–367: gegenteilige Fälle mit geordneten piecewise Links und nicht umgekehrten Vergleichsseiten.
- 517–527: 2.000 generierte Ausdrucksbäume im vorhandenen Test (in diesem Auftrag Code inspiziert, nicht selbst gelaufen).
- 530–544: 500 erzeugte Bäume mit numerischem Vorher/Nachher-Vergleich und Toleranz (kein universeller algebraischer Beweis).
- 657–669: 500 generierte Boolesche Bedingungen, auf allen 16 Belegungen der vier Flags geprüft (vorhandener Test, nicht in ML-C19 ausgeführt).
- 564–600: Program-Frames und Constraint-/Variable-Domains nach Roundtrip geprüft; das garantiert nicht byte-identische Source-Objekte oder externe Contract-Metadaten.

## 5 zu trennende Gleichheitsbegriffe
T1 Kanonischer Text: gleicher String bei definiertem Renderer. T2 AST-Normalform: gleiche geparste strukturierte Terme. T3 definierte Ausdruckssemantik: Gleichheit über genau die zugelassenen Rewriteaxiome. T4 fachliche Contract-Verpflichtungssemantik: inklusive Scope, Authority, A/G, Witness, Status. T5 mathematische Modellgleichwertigkeit: z.B. Projektionsgleichheit aller zulässigen Lösungen; **nicht** von _canonical.py bewiesen. Das Header-Versprechen eines Textes für gleiche Spec ist auf mathspecs definiertes Sprach- und Regeluniversum zu begrenzen, nicht auf allgemeine logische Äquivalenz auszudehnen.

## Reuse-Entscheid
**Direkt als Prinzip wiederverwendbar:** parse-before-rewrite, gezielt definierte kommutative Operatoren, deklarierte nichtkommutative Grenzen, stabiler Ausdrucksdruck, idempotente Roundtrips, Negativtests und getrennte raw/canonical Sicht. **Adaption nötig:** typisierte Contract-Predicate-Sprache statt Algebra-Parser; Guard-Normalisierung nur mit festgelegtem Typ- und Unknown-Modell; Dimension/Unit-Prüfung vor Umordnung. **Nicht übernehmen:** Pflicht zu variables/constraints/objective/given als CSNF-Kern, beliebige algebraische Vereinfachung, Annahme dass Daten-assumptions externe A/G-Guarantees sind.

**Quellenstatus:** I_IMPL=Code inspiziert; T_EXISTING=Tests inspiziert; T_EXECUTED_ML_C19=NEIN. ML-C18/04 berichtet vorhandene CI-Erfolge am gleichen SHA, diese sind Vorarbeiten und keine hier neu ausgeführten Tests.
