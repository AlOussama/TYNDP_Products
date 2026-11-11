# C01 — Fünf gewichtete Wetterfälle – eine Investition

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-010, MA01-SR-027, MA01-SR-029, MA01-SR-030 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Ein Zieljahr (illustrativ 2035), Wetterfälle CY1 bis CY5 mit genau einer gemeinsamen First-Stage-Kapazität x. In jedem Fall existiert eine Second-Stage-ENS-Leistung u_c. LP: min 3 x + ∑_c w_c·10 u_c·1h; s.t. 0≤x≤2 MW, u_c≥d_c−x, u_c≥0. Investitionspreis 3 EUR/MW (für die *eine* Testperiode); ENS-Preis 10 EUR/MWh. Keine realen wirtschaftlichen Parameter.

### Synthetische Testparameter
```json
{
  "year": 2035,
  "weather_ids": [
    "CY1",
    "CY2",
    "CY3",
    "CY4",
    "CY5"
  ],
  "weights": [
    0.2,
    0.2,
    0.2,
    0.2,
    0.2
  ],
  "demands_mw": [
    1,
    1,
    2,
    2,
    4
  ],
  "duration_h": 1,
  "capex_eur_per_mw": 3,
  "voll_eur_per_mwh": 10,
  "invest_max_mw": 2
}
```

## Analytische Herleitung
Die Zielfunktion ist stückweise linear. Links von x=1 sinkt sie mit Steigung −7; zwischen 1 und 2 mit −3; am zulässigen rechten Rand x=2 ist das Minimum erreicht. ENS=(0,0,0,0,2) MW; erwartete ENS = 0,4 MWh; CAPEX = 6 EUR; erwarteter ENS-Wert = 4 EUR; Zielfunktion = 10 EUR.

### Unabhängiges Referenzorakel
```json
{
  "common_x_mw": 2,
  "ens_mw": [
    0,
    0,
    0,
    0,
    2
  ],
  "weighted_ens_mwh": 0.4,
  "capex_eur": 6,
  "weighted_ens_cost_eur": 4,
  "objective_eur": 10
}
```

## Absichtlich fehlerhafte Gegenprobe
Ersetze x durch fünf unabhängige x_c. Dann sinkt der Erwartungswert auf 8,8 EUR (C02): beobachtbare Verletzung der Nichtantizipativität. Gewichte 0,2 sind ausschließlich illustrative Testparameter; echte gleiche Gewichte bleiben numerisch TBD.

## Erforderliche spätere Tool-Evidenz
Investment-Index, Wettermanifeste, erzeugte Koeffizienten/Beschränkungen, pro-CY-ENS und unabhängige Zielfunktionsrekonstruktion.

## Geltungsgrenze und offene Entscheidungen
Je Zieljahr unabhängig; denselben Fixtureaufbau später getrennt für 2040 und 2050 anwenden. Keine Cross-Year-Coupling-Annahme.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
