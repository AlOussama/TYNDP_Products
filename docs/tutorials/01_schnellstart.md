# Tutorial 01 — Installation und erster Methodenvergleich

**Ziel:** Vom frisch geklonten Repository zu reproduzierbaren synthetischen Fluss- und Clustering-Ergebnissen.

## Voraussetzungen

- Python 3.11 oder neuer, `git` und Zugang zu den Python-Paketquellen.
- **PyPSA ist für den synthetischen Kernvergleich nicht erforderlich.** Die Rechnungen verwenden NumPy/SciPy/Pandas.
- Alle Befehle aus dem **Repository-Wurzelverzeichnis** ausführen.

```bash
git clone https://github.com/AlOussama/TYNDP_Products.git
cd TYNDP_Products
python -m venv .venv
source .venv/bin/activate         # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest -q
```

Danach:

```bash
python run_demo.py --output results/tutorial_demo --seed 20261016
python tools/compare_methods.py --input results/tutorial_demo/comparison.csv --output results/tutorial_demo/summary.csv
```

Der Prototyp generiert ein deterministisches **synthetisches 9-Knoten-DC-Netz** mit 120 Stunden. Er verwendet für A/B dieselbe physikalische Topologie, erstellt unterschiedliche Busmaps und prüft sechs Kombinationen aus A/B und drei Referenzgewichten.

## Erwartete Ausgaben

| Datei | Inhalt |
|---|---|
| `comparison.csv` | Sechs A/B × Referenz-Kombinationen mit RMSE und Screening-Abdeckung |
| `summary.csv` | Nach korrigiertem RMSE sortierte Vergleichstabelle mit prozentualem Korrekturgewin |
| `rank_A.csv`, `rank_B.csv` | Leitungsranking nach Überlastung beziehungsweise allgemeiner Belastung |
| `busmap_A.csv`, `busmap_B.csv` | Detaillierter Knoten → Cluster |
| `cuts_A.csv`, `cuts_B.csv` | Interzonenverbindungen |
| `security_limits_A.csv`, `security_limits_B.csv` | Empirische, nicht garantierte N-1-Grenzschätzungen |
| `validation_A.json`, `validation_B.json` | Diagnose und nicht interpretierbare Ausfälle |
| `manifest.json` | Seed, Snapshotzahl, Herkunft und PyPSA-Ausführungsstatus |

## Wissenschaftlicher Status

Die hier berechneten RMSEs sind **synthetische Modellvergleiche**. Weder reale TYNDP-Busmaps noch operative N-1-/Core-Grenzen werden damit nachgewiesen. Ein niedriger RMSE ist kein N-1-Sicherheitszertifikat.

Weiter: [Tutorial 02 — Clustering](02_clustering_a_b.md).
