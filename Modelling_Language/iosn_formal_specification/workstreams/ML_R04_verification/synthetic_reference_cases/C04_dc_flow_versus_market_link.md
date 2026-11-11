# C04 — Vermaschtes DC-Flussgesetz gegenüber steuerbarem Marktlink

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-018, MA01-SR-024, MA01-SR-035, MA01-SR-036 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Drei Knoten A,B,C bilden ein Dreieck. Für physische AC-Bestandszweige mit DC-Näherung sei b_AB=b_AC=b_CB=1 MW pro Winkel-Einheit; orientierte Kanten A→B, A→C, C→B. Injektion (A,B,C)=(+90,−90,0) MW. Referenz θ_A=60, θ_C=30, θ_B=0. Gegenvariante: A→B ist statt physischem Zweig ein steuerbarer Marktlink; die beiden übrigen Zweige bleiben physisch.

### Synthetische Testparameter
```json
{
  "nodes": [
    "A",
    "B",
    "C"
  ],
  "orientation": [
    "A>B",
    "A>C",
    "C>B"
  ],
  "injection_mw": {
    "A": 90,
    "B": -90,
    "C": 0
  },
  "susceptance_mw_per_angle": 1,
  "angles": {
    "A": 60,
    "B": 0,
    "C": 30
  },
  "physical_flows_mw": {
    "AB": 60,
    "AC": 30,
    "CB": 30
  },
  "controllable_link_variant_mw": {
    "AB": 90,
    "AC": 0,
    "CB": 0
  }
}
```

## Analytische Herleitung
Physischer DC-Fluss: f_AB=θ_A−θ_B=60; f_AC=θ_A−θ_C=30; f_CB=θ_C−θ_B=30 MW. Nodalbilanzen erfüllt, zugleich f_AB=f_AC+f_CB als KVL-Konsistenz. Als controllable Link kann f_AB=90 MW und f_AC=f_CB=0 gelten, ohne die AC-KVL-Gleichung für den Link zu erzwingen.

### Unabhängiges Referenzorakel
```json
{
  "dc_physical_AB_mw": 60,
  "dc_physical_AC_mw": 30,
  "dc_physical_CB_mw": 30,
  "link_variant_AB_mw": 90,
  "physical_link_flow_difference_mw": 30
}
```

## Absichtlich fehlerhafte Gegenprobe
Für den physischen Zweig A–B einen freien 90-MW-Link verwenden: nodale Bilanz zwar PASS, KVL FAIL. Umgekehrt einen regelbaren Kandidatenlink fälschlich an Kirchhoff-Winkel koppeln: verletzt zulässige Kandidatenfreiheit.

## Erforderliche spätere Tool-Evidenz
Zweigtypen, Inzidenzmatrix, Suszeptanzen, Branch-/Link-Variablen, KCL/KVL-Zeilen oder gleichwertige PTDF/Zyklusnachweise.

## Geltungsgrenze und offene Entscheidungen
Alle Koeffizienten rein illustrativ; ohne akzeptierten echten Detailnetzfall wird keine IoSN-Netzreduktion zertifiziert.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
