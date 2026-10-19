# Tutorial 02 — Clustering-Methode A gegen Methode B

## Gegenstand und Bezug zur IoSN-Methodik

**A (IoSN-nah):** vollständig bilanziertes Marktdispatch `p_full(t)`, Leitungsflüsse `H_d p_full(t)` und jährlich kumulierte Überlastungsenergie:

```math
E^{A}_{\ell}=\sum_t\max(0, |f_{\ell,t}|-\bar f_\ell)\Delta t.
```

**B (eigene Erweiterung):** verfügbare Wind- und PV-Leistung minus Last, mit transparentem Bilanzausgleich `w` (keine wirtschaftliche Dispatch-Optimierung). Für das Ranking verwendet der Demonstrator die mittlere relative Gesamtbelastung:

```math
s^{B}_\ell=\sum_t\omega_t |f^{B}_{\ell,t}|/(\bar f_\ell\sum_t\omega_t).
```

Wichtig: B benötigt eine definierte Bilanzausgleichsverteilung, weil RES − Last allein i. A. nicht bilanziert ist. A/B sind **nicht dieselbe Zielfunktion**, und IoSN spezifiziert B nicht.

## Ausführung

```bash
python run_demo.py --output results/tutorial_demo --seed 20261016
```

Lesen und vergleichen:

```python
import pandas as pd
from pathlib import Path
root = Path("results/tutorial_demo")
a = pd.read_csv(root / "rank_A.csv")
b = pd.read_csv(root / "rank_B.csv")
map_a = pd.read_csv(root / "busmap_A.csv")
map_b = pd.read_csv(root / "busmap_B.csv")
print(a.sort_values("overload_MWh", ascending=False).head())
print(b.sort_values("loading_mean", ascending=False).head())
print("Knoten mit unterschiedlicher Zone:", (map_a.zone != map_b.zone).sum())
```

Beachte: Zonenlabels sind beliebig; für einen rigorosen partitionsinvarianten Vergleich sollte zusätzlich eine labelinvariante Metrik wie Adjusted Rand Index genutzt werden. Die obige Anzahl ist nur eine erste Diagnose.

## Aggregation und Erhaltungsbedingung

Für jede Busmap `m` bildet `build_aggregation` die Knotenmatrix `P_m` und die Leitungs-/Korridormatrix `Gamma_m`:

```math
p_z^{(m)}=P_mp_d,\quad f_z^{(m)}=\Gamma_mf_d,\quad A_z^{(m)}\Gamma_m=P_mA_d.
```

Mit einem bilanzierten Referenzdatensatz kann die letzte Identität als deterministischer Qualitätsnachweis getestet werden.

## Faire Bewertung

- Beide Methoden mit derselben Zonenzahl, Netzstruktur und Zeitbasis ausführen.
- Gleiche vollständige, zurückgehaltene Referenzstunden für die elektrische Validierung verwenden.
- Nicht nur Überlastungsabdeckung, sondern auch Flussfehler, Gegenläufigkeit, Netzmaschen und N-1-CNEC-Abdeckung auswerten.
- Die greedy-Busmap des Demonstrators ist kein vollständiger ENTSO-E-Zonenoptimierer.

Weiter: [Tutorial 03 — PTDF und F₀](03_ptdf_referenzen.md).
