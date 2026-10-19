# Tutorial 04 — Analytische N-1-Sicherheit, duale LODF und FBMC

## 1. Analytischer N-1-Test

```bash
python examples/run_security_projection.py
python -m pytest -q tests/test_security_projection.py
```

Der dreieckige 3-Knoten-DC-Test besitzt N-0-Transfergrenze 150 MW und eine **N-1-Transfergrenze von 80 MW** für A → B. Er prüft die Übereinstimmung der nodalen und dualen LODF-Berechnung sowie konservatives Derating.

Für einen überwachten Zweig `l` und Ausfall `k`:

```math
f_l^{(k)}=f_l+LODF_{lk}f_k.
```

`cnec_operator` konstruiert `K` für N-0 und N-1. Bei definierter räumlicher Referenzverteilung `R` ergibt sich:

```math
H_{C,z}=K H_d R,\quad
f_{0,C}=K H_d(I-RP)p_{ref},\quad
-\bar f_C\le H_{C,z}p_z+f_{0,C}\le\bar f_C.
```

Diese gekoppelte CNEC-Region bleibt **nur unter der definierten intrazonalen Verteilungsannahme** exakt im linearen Modell. Ein bilaterales Transfermaximum ist keine gleichzeitig nutzbare, unabhängige Kapazität aller Zonenverbindungen.

## 2. Empirische IoSN-nahe N-1-Schätzung

Im vollständigen A/B-Demonstrator entstehen `security_limits_A.csv` und `security_limits_B.csv`. Die Datenpunkte verknüpfen aggregierte Interzonenflüsse mit N-1-Belastungsgraden. Nicht identifizierbare Beziehungen erhalten Status-/NaN-Felder; solche Felder **niemals** stillschweigend auf null setzen oder als zertifizierte RAM interpretieren.

```bash
python run_demo.py --output results/tutorial_demo
python -c "import pandas as pd;print(pd.read_csv('results/tutorial_demo/security_limits_A.csv').status.value_counts())"
```

Die veröffentlichte IoSN beschreibt vier jahreszeit-/richtungsabhängige Transfergrenzen je Korridor; die implementierte Regressionsroutine ist ein **wissenschaftlicher Proxy**, nicht der unveröffentlichte originale Schätzer.

## 3. Flow-Based Market Coupling

```bash
python examples/run_fbmc_bridge.py
```

Dieses Beispiel schreibt nach `outputs/fbmc/`:

- `fbmc_gsk_comparison.csv` für uniform/capacity/merit_order,
- `fbmc_domain_uniform.csv`, `fbmc_domain_capacity.csv`, `fbmc_domain_merit_order.csv` für CNEC-Koeffizienten und synthetische RAM.

Die Marktgebotszonen im Beispiel sind **nicht** automatisch mit den A/B-Planungszonen identisch. Die GSK verteilt **marginale Änderungen** zonaler Nettopositionen:

```math
H_{FB}=K H_d G,\quad
H_{FB}\,NP\le RAM.
```

Das Beispiel ist **keine** operative Core-CCR-Kapazitätsberechnung; insbesondere werden tatsächliche TSO-GLSKs, FRM-, Remedial-Action- und Validierungsschritte nicht reproduziert.

## 4. Vergleichslogik

| Ansatz | Output | Wissenschaftliche Bedeutung |
|---|---|---|
| IoSN-naher Regressionstest | Vier saisonal-/richtungsabhängige Grenzschätzungen | Empirische Betriebszustands-Approximation |
| Analytische CNEC-Projektion | Gekoppelte N-1-Ungleichungen | Referenz für einen spezifizierten DC-/GSK-Fall |
| Robuste Derating-Regel | Konservative einheitliche thermische Absenkung | Hinreichende, oft restriktive Sicherheit |
| FBMC-GSK-Vergleich | Synthetische Marktdomänen | Sensitivität auf räumliche Änderungsschlüssel |

Weiter: [Tutorial 05 — echte PyPSA-Netze](05_reale_pypsa_netze.md).
