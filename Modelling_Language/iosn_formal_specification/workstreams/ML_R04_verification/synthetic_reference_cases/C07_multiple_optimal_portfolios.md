# C07 — Mehrfach optimale Investitionsportfolios

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-001, MA01-SR-025, MA01-SR-046, MA01-SR-047 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Zwei kapazitätsgleichwertige Investitionen x und y mit 0≤x≤1,0≤y≤1 und x+y=1 MW. Zielfunktion min x+y in künstlichen Test-Geldeinheiten. Die gesamte optimale Fläche ist die Streckenmenge {(x,y)|x+y=1,x,y≥0}.

### Synthetische Testparameter
```json
{
  "total_required_mw": 1,
  "cap_each_mw": 1,
  "cost_x_per_mw": 1,
  "cost_y_per_mw": 1,
  "portfolios_mw": [
    [
      1,
      0
    ],
    [
      0,
      1
    ],
    [
      0.5,
      0.5
    ]
  ]
}
```

## Analytische Herleitung
Alle drei Portfolios (1,0), (0,1), (0,5;0,5) erfüllen die identischen Restriktionen und haben denselben Zielfunktionswert 1. Die Summe der Investitionskapazität ist invariant 1 MW; komponentenweise Vektoren sind nicht invariant.

### Unabhängiges Referenzorakel
```json
{
  "all_objectives": 1,
  "invariant_total_mw": 1,
  "distinct_vectors": 3
}
```

## Absichtlich fehlerhafte Gegenprobe
Ein Cross-Tool-Comparator, der den Vergleich aufgrund (1,0) ≠ (0,1) auf FAIL setzt, meldet einen falschen negativen Befund. Portfolios mit anderem Gesamtniveau oder unzulässigen Limits dürfen dagegen nicht als gleichwertig gelten.

## Erforderliche spätere Tool-Evidenz
Beide Tool-Primallösungen, Kapazitäts- und KCL-Prüfung, Zielfunktions-/Optimalitätszertifikat, Invariant- und solution-set-envelope-Bericht.

## Geltungsgrenze und offene Entscheidungen
Bei portfoliobezogenen, nicht-invarianten KPIs müssen Werte als Intervall/Menge oder solverabhängige Realisierung kenntlich gemacht werden.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
