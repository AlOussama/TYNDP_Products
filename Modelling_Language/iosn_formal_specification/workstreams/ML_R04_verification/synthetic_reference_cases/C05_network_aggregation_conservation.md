# C05 — Netzaggregation – notwendige Erhaltung des Cut-Flusses

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-014, MA01-SR-016, MA01-SR-017, MA01-SR-019, MA01-SR-022, MA01-SR-023 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Detailnetz A1,A2,B. A1 und A2 werden zu Cluster X zusammengefasst; B bildet Y. Injektionen A1=+30, A2=+20, B=−50 MW. Orientierte Detailflüsse A1→A2=−10, A1→B=40, A2→B=10 MW. Test ist eine notwendige Cut-/KCL-Konservation, kein hinreichendes elektrisches Netzäquivalenzorakel.

### Synthetische Testparameter
```json
{
  "nodes": [
    "A1",
    "A2",
    "B"
  ],
  "clusters": {
    "A1": "X",
    "A2": "X",
    "B": "Y"
  },
  "injection_mw": {
    "A1": 30,
    "A2": 20,
    "B": -50
  },
  "flows_mw": {
    "A1_A2": -10,
    "A1_B": 40,
    "A2_B": 10
  },
  "duration_h": 1
}
```

## Analytische Herleitung
A1: −10+40=30 MW; A2: +10+10=20 MW; B: −40−10=−50 MW. Aggregiert P_X=30+20=50 MW, P_Y=−50 MW, Cut X→Y=40+10=50 MW. Beide lokalen und aggregierten KCL-Residuen sind exakt null.

### Unabhängiges Referenzorakel
```json
{
  "cluster_x_mw": 50,
  "cluster_y_mw": -50,
  "cut_x_y_mw": 50,
  "energy_through_cut_mwh": 50
}
```

## Absichtlich fehlerhafte Gegenprobe
Eine fehlerhafte Mapping-Tabelle lässt A2→B (10 MW) weg: ausgegebener Cut=40 MW, KCL-Residuum X = 10 MW ⇒ FAIL. Die gleiche Cut-Menge belegt nicht automatisch korrekte Impedanz, PTDF, N−1 oder RMSE.

## Erforderliche spätere Tool-Evidenz
Detailnetz-Knoten-/Branch-Ledger; Clusterpartition/Graphkonnektivität; signierte Cut-Flüsse; KCL-Residuen; getrennte Qualitätsnachweise.

## Geltungsgrenze und offene Entscheidungen
MD-03/13/15: Kein freigegebener IoSN-Grenzwert und kein qualifizierter Detailnetz-Oracle. Netzreduktionskonformität bleibt BLOCKED.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
