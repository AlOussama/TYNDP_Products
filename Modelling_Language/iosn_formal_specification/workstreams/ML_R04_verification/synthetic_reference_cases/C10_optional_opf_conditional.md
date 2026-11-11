# C10 — Optionale OPF-Variante und bedingte Pflichtprüfungen

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-003, MA01-SR-024, MA01-SR-025, MA01-SR-026, MA01-SR-031, MA01-SR-032 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
LF-Baseline ist verpflichtend, OPF-Expansion ausdrücklich optional. Illustratives LF-Portfolio: Kandidat K besitzt 3 MW Ausbau. Falls OPF branch=false: C10-OPF-Constraints tatsächlich nicht instanziiert. Falls branch=true: die OPF-Investition y_K muss 0≤y_K≤3 MW einhalten.

### Synthetische Testparameter
```json
{
  "candidate": "K",
  "lf_cap_mw": 3,
  "opf_variant_off": false,
  "opf_variant_on": true,
  "opf_passing_investment_mw": 2,
  "opf_failing_investment_mw": 4
}
```

## Analytische Herleitung
Flag OFF und nachweislich kein OPF-Lauf ⇒ nur bedingter Test MA01-SR-026 NOT_APPLICABLE; LF-/Dispatch-Mandatorien weiterhin gesondert prüfen. Flag ON und y=2 ⇒ Constraint-Synthesetest PASS. Flag ON und y=4 ⇒ FAIL; Flag ON ohne OPF-Fähigkeit ⇒ UNSUPPORTED.

### Unabhängiges Referenzorakel
```json
{
  "off_test_status": "NOT_APPLICABLE",
  "on_pass_test_status": "PASS",
  "on_fail_test_status": "FAIL",
  "on_unsupported_test_status": "UNSUPPORTED"
}
```

## Absichtlich fehlerhafte Gegenprobe
OPF-Lauf bei branch=true heimlich unterlassen und als NOT_APPLICABLE berichten ⇒ falsch. Ebenso y=4 bei LF-Maximum 3 ⇒ FAIL. Die LF-Portfolio-Größe wird nicht durch die OPF-Lösung nachträglich umgeschrieben.

## Erforderliche spätere Tool-Evidenz
Flag und variant selection, LF-run ID, LF-Kandidateninventar, OPF-Bounds, generierte Restriktionen, Solver-/Run-Status.

## Geltungsgrenze und offene Entscheidungen
Die konkreten methodischen LF-/OPF-Übergangsdetails bleiben MD-07/08; dieses Beispiel testet nur das konditionale Steuerungsprinzip.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
