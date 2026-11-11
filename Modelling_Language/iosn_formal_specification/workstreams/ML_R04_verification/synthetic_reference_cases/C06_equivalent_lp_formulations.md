# C06 — Äquivalente algebraische LP-Formulierungen

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-018, MA01-SR-027, MA01-SR-043, MA01-SR-044, MA01-SR-047 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Formulierung A: min 2x+3y unter x+y≥4, x≥0,y≥0. Formulierung B: min 2x+3y unter 2x+2y−2s=8 und x,y,s≥0. B enthält eine zusätzliche nichtnegative Slackvariable und eine skalierte Zeile.

### Synthetische Testparameter
```json
{
  "rhs": 4,
  "objective_coefficient_x": 2,
  "objective_coefficient_y": 3,
  "row_scale": 2
}
```

## Analytische Herleitung
Für jede (x,y) in A gibt es genau ein s=x+y−4≥0 in B. Jede zulässige Lösung in B projiziert auf eine zulässige (x,y) in A. Die Zielfunktion in Originalvariablen bleibt gleich. Optimale Lösung: x=4,y=0,s=0, Wert 8. Somit ist die Projektion der gesamten zulässigen Menge und nicht nur der beste Zielfunktionswert äquivalent.

### Unabhängiges Referenzorakel
```json
{
  "opt_x": 4,
  "opt_y": 0,
  "opt_slack": 0,
  "optimal_objective": 8,
  "projection_equivalent": true
}
```

## Absichtlich fehlerhafte Gegenprobe
Entferne in B die Restriktion s≥0. Dann sind x=y=0,s=−4 zulässig und Zielfunktionswert 0 statt 8: aus zufälliger numerischer Übereinstimmung einzelner Lösungen kann keine mathematische Äquivalenz abgeleitet werden.

## Erforderliche spätere Tool-Evidenz
Symbolischer Variablen-/Constraint-Crosswalk, Eliminationsbeweis, Parameterauszug, numerische Referenzwerte und Negativmutation.

## Geltungsgrenze und offene Entscheidungen
Vollständige A↔B-Projektion hier bewiesen; im produktiven Modell erfordert D4 nur risikobedingt zusätzliche strukturelle oder symbolische Beweise.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
