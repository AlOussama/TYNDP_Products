# Tutorial 03 — Technologiespezifische PTDF, Referenzverteilungen, F₀ und Ersatzimpedanzen

## Fragestellung

Für jede Busmap aus A oder B werden drei **räumliche Verteilungen** verglichen:
`uniform`, `capacity`, `merit_order`.

Die elektrische PTDF `H_d` bleibt dieselbe. Die Technologie-/Referenzabhängigkeit entsteht allein aus den räumlichen Gewichten `R_k(t)`:

```math
H_z^{(k)}(t)=\Gamma H_d R_k(t),\quad PR_k(t)=I.
```

Die Merit-Order-Variante benutzt **feste** Grenzkosten- und Kapazitätsgewichte. Sie ist ein Forschungsproxy und **keine** endogene Strommarktoptimierung.

## Vollständige Ausführung und Auswertung

```bash
python run_demo.py --output results/tutorial_demo --seed 20261016
python tools/compare_methods.py --input results/tutorial_demo/comparison.csv --output results/tutorial_demo/summary.csv
```

Zur Anzeige der Einzelwerte:

```python
import pandas as pd
df = pd.read_csv("results/tutorial_demo/summary.csv")
print(df[["clustering", "reference", "validation_plain_RMSE_MW",
          "validation_corrected_RMSE_MW", "validation_joint_fit_RMSE_MW",
          "cycle_rank"]].to_string(index=False))
```

### Interpretation

- `validation_plain_RMSE_MW`: Referenz-PTDF + konstanter, kreisflusskonsistenter Offset, ohne explizite Wind/PV/Last-Strukturkorrektur.
- `validation_corrected_RMSE_MW`: derselbe Referenzansatz **plus** hochaufgelöste exogene Strukturkorrektur.
- `validation_joint_fit_RMSE_MW`: separat kalibrierte reduzierte Ersatzimpedanzen und `c0`, nicht zwingend dieselbe Basismethodik.
- `cycle_rank=0`: auf einem Baum sind Flüsse durch Zonenbilanzen festgelegt; daraus lässt sich keine eindeutige Ersatzreaktanz identifizieren.
- Ein negativer `structural_correction_gain_pct` ist möglich und muss als Verschlechterung berichtet werden.

## Zwei verschiedene Offsets explizit unterscheiden

Mit einer Referenzverteilung `R`:

```math
f_0^{structure}(t)=\Gamma H_d(I-RP)p_d(t),\quad
f_z(t)=\Gamma H_dR p_z(t)+f_0^{structure}(t).
```

Ein zeitlich **konstanter** kalibrierter `c0` ist hingegen nur eine Approximation über mehrere Betriebszustände:

```math
\widehat f_z(t)=H_{eq}(x_{eq})p_z(t)+c_0.
```

Darum ist `f_0^{structure}(t)` nicht automatisch identisch mit `c_0` und auch nicht mit dem FBMC-Nullpositionsfluss.

## Methodischer Abgleich

Die IoSN-Beschreibung enthält Impedanz- und No-Load-Flow-Kalibrierung, aber keine Vorgabe, uniform/capacity/merit_order als Referenz zu wählen. Diese Varianten sind eigenständige Hypothesen.

Weiter: [Tutorial 04 — N-1 und FBMC](04_n1_fbmc.md).
