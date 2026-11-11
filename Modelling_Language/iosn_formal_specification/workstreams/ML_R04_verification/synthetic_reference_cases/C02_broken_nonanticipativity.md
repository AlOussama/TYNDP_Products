# C02 — Absichtlich fehlende Nichtantizipativität

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-027, MA01-SR-029 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Gleiche Eingangsdaten wie C01, aber fehlerhafte First-Stage-Variablen x_CY1,...,x_CY5 ohne Gleichheitskopplung. Zu jedem Fall wird ein eigener CAPEX-Block mit w_c gewichtet; mathematisch anderes Problem, nicht bloß andere algebraische Darstellung.

### Synthetische Testparameter
```json
{
  "based_on": "C01",
  "fault": "independent_first_stage_by_weather",
  "candidate_x_by_cy_mw": [
    1,
    1,
    2,
    2,
    2
  ]
}
```

## Analytische Herleitung
Einzelfalloptima x_c=min(d_c,2) liefern je Szenario Kosten (3,3,6,6,26) EUR; deren arithmetisches Mittel = 44/5 = 8,8 EUR, während das gültige C01-Modell 10 EUR ergibt. Die besseren Kosten sind ein Verstoß, kein Qualitätsgewinn.

### Unabhängiges Referenzorakel
```json
{
  "faulty_objective_eur": 8.8,
  "valid_objective_eur": 10,
  "investment_values_mw": [
    1,
    1,
    2,
    2,
    2
  ],
  "test_status": "FAIL"
}
```

## Absichtlich fehlerhafte Gegenprobe
Auch fünf zyklisch gleich benannte Variablen ohne Equality-Constraints sind falsch; ein zusätzlicher Mittelwertvergleich alleine reicht nicht als Beweis. Der Test muss Zeugen für fehlende gemeinsame Bindung aus dem Modellgenerator liefern.

## Erforderliche spätere Tool-Evidenz
Erzeugte Investitionsspalten, Non-Anticipativity-Constraints oder ein gemeinsamer Variablenindex, unabhängiger Zielfunktionsvergleich.

## Geltungsgrenze und offene Entscheidungen
Bei rein numerisch zufällig gleichen x_c ist die strukturelle Nichtantizipativitätsprüfung weiterhin obligatorisch.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
