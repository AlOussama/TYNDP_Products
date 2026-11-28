# C4 retained normalization rules
Original ML-C19 ruleset retained below verbatim; these are requirements, not a claim that every rule has a general soundness proof. C2/C3 admitted subset and current C4 evidence govern supported scope.

# ML-C19/07 – Formale Normalisierungsregeln, Präbedingungen und Negativzeugen
Ruleset CSNF-R0, 2026-11-23; keine sichere Übernahme mathematischer Optimierungsäquivalenz. Jede Regel enthält Ausgangstyp, Precondition, Effect, Witness und Non-Witness. Fehlende Precondition => REJECT/BLOCKED, nicht automatische Umschreibung.

| Regel | Voraussetzungen und formale Wirkung | Positives Beispiel | Negatives Beispiel |
|---|---|---|---|
| R00 Parse/Type | wohlgeformtes endliches C, eindeutiger Symbolraum Γ; fail-closed | vollständig qualifizierte id | zwei gleichnamige Porttypen ohne Namespace |
| R01 Reference | Name mit eindeutiger qualified/stable ID -> diese ID, Aliasledger behalten | alias battery.grid -> urn:study:batt1:grid | gleiche lokale Namensform für zwei Anlagen |
| R02 Set-order | nur vom Typ als unordered ausgezeichnete Collection sortieren, set semantics mit expliziter Multiplicity | Assertions im Registry-Set permutiert | Stage-Reihenfolge, piecewise Links, Pipeline-Schritte |
| R03 Commutativity | ausschließlich pure bool AND/OR und im Unit/Domain-Profil geprüfte commutative Scalar-Operators sortieren | A AND B -> B AND A normal identisch | matrix multiplication, nichtassoziative FP-Reduktion, Side-effects |
| R04 Associativity | bool AND/OR mit totaler/definierter Unknown-Logik flatten; mathematische Summe nur wo Typ, Semantik, Precision/aggregation permit | (A AND B) AND C -> A AND B AND C | durch Rundung sensitive floating-point cumulative aggregation |
| R05 Negation/Guard | unary NOT nur Druck/Klammern/Klein-/Großschreibung, definierte Bool3-Gleichheit | not (a and b) -> NOT (a AND b) | fehlender Guard darf nicht TRUE werden; De Morgan nicht ohne logisches Fragment |
| R06 Quantity | gleiche physical_kind, dimensions, carrier, sign, temperature/energy basis und exakte Konversionskonstante; value' = f(value), unit'=canonical | 1000 kW injection -> 1 MW injection | MW load -> MW injection; kgH2 -> MWh ohne LHV/HHV |
| R07 Time | eindeutige explizite Zeitbasis und Zone; normalisiere bekannte Intervalldaten *mit Dauer* | 30 min -> 0.5 h, 2 MW*0.5h=1 MWh | 2 MW Snapshot -> 2 MWh ohne Dauer; DST-Zeitsprung ignorieren |
| R08 Port/Link | Roles/Types/Carrier/Units/Sign/ConnectionPoint explizit kompatibel; canonical orientation **mit Signadjustment** sofern definiert | reverse oriented branch plus korrekt negierter Flow | reverse oriented bus injection ohne Signänderung; branch -> market link |
| R09 ScopedAssertions | normatives role, guard, authority status identisch; nur gemeinsame identische Inhaltspredikate referenzieren, provenance multiset unverändert | zwei identische textuelle Guaranties als 1 semantic body mit zwei source links | REQUIRED vs PERMITTED, Quelle A vs Quelle B verloren |
| R10 Composition | eindeutige Versionen, keine referenziellen Zyklen, explizite precedence und Owner-genehmigte Overrides | disjunkte Module durch scoped union | stiller Override löscht KCL/KVL oder ändert Owner Decision |
| R11 Default | nur expliziter genehmigter und typisierter Default im Profile mit versionierter Authority; sonst unknown | scope 'all scenarios' bei explizitem approved profile | OWNER_TBD -> 0, omitted capacity -> unendlich |
| R12 Observable | quantity, basis, temporal/spatial/scenario aggregation, weights und selection rules semantisch gleich | 1000 kEUR -> 1 MEUR bei gleicher Preisbasis | discounted cost vs undiscounted cost |
| R13 Evidence | canonical type+reference normalisieren, Status und Run-IDs unverändert; kein Assessment aus Request ableiten | gleiche test request id mit normalisiertem ref | NOT_EXECUTED -> PASS; proof request -> evidence result |

Zusätzliche explizit **verbotene** Verschmelzungen: KCL != KCL+KVL; Objective gleich != Feasible Set gleich; gleiche Batterienamen != gleiche externe Servicefähigkeit; zwei verschiedene interne Zustände dürfen dagegen innerhalb derselben fachlichen Rolle existieren; Datennutzungs-Guard != externe Verhaltensgarantie. Unterschiedliche Quellen bleiben separate Authority-Knoten selbst wenn sie dieselbe Proposition unterstützen.

## Phasen und Terminationsargument (auf dem definierten Fragment)
Phase P0 validate/resolve references. P1 typecheck guards, units, time/role; P2 expand **nur** autorisierte Defaults und explizit kontrollierte Imports (zyklische Dependencies BLOCKED). P3 canonicalise finite AST leaves/bool fragments. P4 canonicalise typed quantities. P5 sort und deduplicate nur als unordered getypte Collections und body-Hashes mit separaten AuthorityLinks. P6 stable encoding. Keine Regel schreibt von Phase Pi zurück zu früheren syntaktischen Varianten; innerhalb Pi verringern Sorts ihre Inversionszahl, Flattening die Zahl unnötiger gleichartiger Klammerbäume, Aliasauflösung die Zahl unaufgelöster Aliases. Endlichkeit + keine rekursiven Imports sind Voraussetzungen, **keine** universelle Terminationsgarantie für beliebige externe Erweiterungen.

## Konfluenz und Idempotenz
Ein deterministisch angeordnetes, abgeschlossenes Rewrite-System kann den kanonischen *Output* eindeutig erzeugen, ohne dass die ungerichtete Sammlung aller Regelschemata konfluent wäre. Kritische Paare: Unit-Converting + Bound-Comparison; Flatten-Guards + Unknown-Propagation; Port-Orientation + Sign; Merge + Source-Dedup; Import+Override. Die erforderliche Lösung ist **priorisierte Pipeline + versionierte Typ-/Unit-/Alias-Registry + kritische-Paar-Tests**. Ein globaler Church-Rosser-Beweis liegt NICHT vor.
Erwartete Property-Tests: N(N(C))=N(C), N(permute_unordered(C))=N(C), AuditLedger-Coverage, targeted syntactic mutation yields DIFFERENT/BLOCKED, randomized valid AST Guard-Truth-Tables mit dreiwertiger Logik. Original/normalisiert/re-importiert müssen separat nachvollziehbar bleiben.

## Beweispflichten für ML-C20 und ML-C21
Je Regel: (1) typisierte Domain, (2) formal definierte Wirkung, (3) lokale Soundness, (4) Idempotenz und stabiler Byte-Output, (5) positive/negative RC-Witnesses, (6) source-preserving diff, (7) Rule-ID in Diagnostic, (8) versionsgebundene test vectors. Bis diese Prüfungen gelaufen sind: RULES_SPECIFIED, SOUNDNESS_NOT_PROVED.
