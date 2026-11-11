# C09 — Fehlende verpflichtende Toolfunktion

**Status:** SYNTHETIC_ONLY / ILLUSTRATIVE · **Requirements:** MA01-SR-006, MA01-SR-008, MA01-SR-029, MA01-SR-033 · **Test nature:** analytic oracle + adversarial mutation; **not** a tool run.

## Modell und vollständiger Testaufbau
Tool X kann zwar Inputschemata parsen, bietet aber keine Implementierung für die erforderliche gemeinsame First-Stage-Investitionsentscheidung über Wetterfälle (MA01-SR-029). Das Capability-Manifest sagt supported=false, der Test wird daher nicht ausgeführt. Eine fiktive Solver-Meldung OPTIMAL ist irrelevant.

### Synthetische Testparameter
```json
{
  "tool": "Tool-X-synthetic",
  "mandatory_requirement": "MA01-SR-029",
  "supported": false,
  "executed": false
}
```

## Analytische Herleitung
Für eine verpflichtende Eigenschaft ist capability=false ein tatsächlich nachgewiesenes Fehlen der Funktion: test_result=UNSUPPORTED; requirement_status=UNSUPPORTED; full_conformance=NOT_GRANTED. Nicht mit NOT_APPLICABLE verwechseln.

### Unabhängiges Referenzorakel
```json
{
  "test_status": "UNSUPPORTED",
  "overall_conformance_pass": false
}
```

## Absichtlich fehlerhafte Gegenprobe
Eine fehlende Pflichtfunktion als SKIPPED/PASS oder NOT_APPLICABLE behandeln ⇒ fail-closed-Verletzung. Ist die Funktion verfügbar, aber mangels Ressource nicht ausgeführt: NOT_EXECUTED; fehlen akzeptierte Owner-Parameter: BLOCKED.

## Erforderliche spätere Tool-Evidenz
Capability-Manifest mit Toolversion und Feature-ID, Attempt-/Skip-Log, erforderlicher Vertragszweig und Fehlermeldung.

## Geltungsgrenze und offene Entscheidungen
Keine realen Toolbehauptungen. Daten- und Modellkonformität anderer Funktionen können separat nachgewiesen sein, ersetzen aber diesen Nachweis nicht.

**Wichtig:** Keine realen Wettergewichte, fachlichen Grenzwerte, Methodikparameter oder produktiven Toleranzen werden aus diesem Fixture abgeleitet. Ein arithmetischer Fixture-PASS ist kein IoSN-/Tool-CONFORMANCE-PASS.
