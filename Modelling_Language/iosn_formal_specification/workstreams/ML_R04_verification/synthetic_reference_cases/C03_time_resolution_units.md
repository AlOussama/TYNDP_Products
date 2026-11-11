# C03 — Zeitauflösung, UTC, MW-/MWh-Bilanz

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-007, MA01-SR-011, MA01-SR-028, MA01-SR-034, MA01-SR-042 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Ein einstündiger UTC-Zeitraum wird durch zwei halbstündige Intervalle repräsentiert: 2026-01-01T00:00Z und 00:30Z. Leistung (2,0) MW; Δt=(0,5;0,5) h. Äquivalente Stundenauflösung: (1 MW) für 1 h. Keine DST-Ambiguität in UTC. Kosten 50 EUR/MWh als Testpreis.

### Synthetische Testparameter
```json
{
  "timestamps_utc": [
    "2026-01-01T00:00:00Z",
    "2026-01-01T00:30:00Z"
  ],
  "half_hour_power_mw": [
    2,
    0
  ],
  "half_hour_duration_h": [
    0.5,
    0.5
  ],
  "hourly_power_mw": 1,
  "hourly_duration_h": 1,
  "cost_eur_per_mwh": 50
}
```

## Analytische Herleitung
E = ∑ P_t·Δt_t = 2·0,5 + 0·0,5 = 1 MWh. Bei 1-h-Aggregation E=1·1=1 MWh. Kosten=1·50=50 EUR. Das bloße Addieren von (2+0) MW liefert keine MWh und ist als KPI ungültig.

### Unabhängiges Referenzorakel
```json
{
  "energy_mwh": 1,
  "cost_eur": 50,
  "bad_naive_sum_of_mw": 2
}
```

## Absichtlich fehlerhafte Gegenprobe
Führe bei Resampling fälschlich ein ungewichtetes MW-Summenaggregat ein; das erzeugt numerisch 2 statt 1 MWh. Ein Zeitschrittduplikat oder lokaler DST-String ohne disambiguierte UTC-Zeitachse muss V1 blockieren.

## Erforderliche spätere Tool-Evidenz
UTC-Instants, explizite Δt-Dimension, Prüfprotokoll vor/nach Aggregation, Einheitentransformation und Energie-Residual.

## Geltungsgrenze und offene Entscheidungen
Die operative Kalender- und DST/Leap-Policy ist MD-12 und bleibt TBD; das Testbeispiel fixiert nur einen konfliktfreien Mini-Zeitraum.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
