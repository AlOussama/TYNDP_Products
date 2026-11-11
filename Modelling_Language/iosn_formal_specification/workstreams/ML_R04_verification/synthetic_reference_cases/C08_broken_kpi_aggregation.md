# C08 — KPI-Zeit- und Wetteraggregation – positive/negative Fälle

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-001, MA01-SR-025, MA01-SR-027, MA01-SR-045, MA01-SR-046 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Fünf illustrative CY mit w=0,2; zwei Intervalldauern Δt=(0,5;1,5) h. ENS-Leistung in MW je CY: (2,0); (0,2); (1,1); (0,0); (2,2). ENS-KPI ist ∑_CY w_CY·∑_t ENS_MW·Δt_h. VoLL im Test = 100 EUR/MWh.

### Synthetische Testparameter
```json
{
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
  "durations_h": [
    0.5,
    1.5
  ],
  "ens_mw_by_weather": [
    [
      2,
      0
    ],
    [
      0,
      2
    ],
    [
      1,
      1
    ],
    [
      0,
      0
    ],
    [
      2,
      2
    ]
  ],
  "voll_eur_per_mwh": 100
}
```

## Analytische Herleitung
ENS je CY = (1,3,2,0,4) MWh. Erwartete ENS=(1+3+2+0+4)/5=2 MWh; entsprechende ENS-Kosten=200 EUR. Ungewichtete Summe 10 MWh wäre kein Erwartungswert; Summe bloßer MW-Werte 10 hat falsche Dimension.

### Unabhängiges Referenzorakel
```json
{
  "ens_mwh_by_weather": [
    1,
    3,
    2,
    0,
    4
  ],
  "weighted_ens_mwh": 2,
  "weighted_ens_cost_eur": 200,
  "unweighted_ens_mwh": 10
}
```

## Absichtlich fehlerhafte Gegenprobe
Ungewichtete Energie = 10 MWh fälschlich als erwartete ENS ausgeben ⇒ FAIL. Roh-MW addieren ⇒ Einheiten-FAIL. Ein Filter ohne genehmigten Schwellenwert (MD-04) darf keinen vollständigen produktiven KPI-PASS auslösen.

## Erforderliche spätere Tool-Evidenz
Roh-ENS nach Wetter/UTC/Δt, verwendete Gewichte, Outputformel-Version und unabhängige KPI-Rechnung.

## Geltungsgrenze und offene Entscheidungen
Nur dimensions- und aggregationsbezogenes Testorakel. Finale Systembedarfs-/ONDP-Definitionen und reale Schwellen bleiben MD-04/TBD.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
