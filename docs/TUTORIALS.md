# Tutorials — Ausführen, Vergleichen und Einordnen

Diese Tutorials verwenden die **kanonische** Codebasis unter `src/tyndp_reduce/`. Die Methoden sind Forschungsprototypen; die mitgelieferten Datensätze sind synthetisch und **keine** ENTSO-E-/Core-Marktdaten.

## Empfohlene Reihenfolge

1. **[01 — Installation und Schnellstart](tutorials/01_schnellstart.md):** Installation, 24+ Tests und vollständiger Demonstrator.
2. **[02 — Clustering A vs. B](tutorials/02_clustering_a_b.md):** Dispatch-Überlastung gegenüber RES/Last-Belastung, Busmaps und Qualitätsindikatoren.
3. **[03 — PTDF, Referenzverteilung und F₀](tutorials/03_ptdf_referenzen.md):** uniform, capacity, merit_order; RMSE, strukturelle Korrektur, Ersatzreaktanzen.
4. **[04 — N-1, duale LODF und FBMC](tutorials/04_n1_fbmc.md):** analytische Sicherheitsprojektion versus empirische Kapazitätsproxies sowie GSK-Vergleich.
5. **[05 — Eigene PyPSA-Netze und Grenzen](tutorials/05_reale_pypsa_netze.md):** Voraussetzungen, Adapter, Stop-Bedingungen und realistisch nächster Implementierungsschritt.

## Ein Befehlssatz für den gesamten synthetischen Vergleich

Ab Repository-Wurzel:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
python run_demo.py --output results/tutorial_demo --seed 20261016
python tools/compare_methods.py --input results/tutorial_demo/comparison.csv --output results/tutorial_demo/summary.csv
python examples/run_security_projection.py
python examples/run_fbmc_bridge.py
```

**Hinweis:** Das historische FBMC-Beispiel schreibt derzeit in `outputs/fbmc/`, nicht in `results/tutorial_demo/`. Die Dateien sind synthetisch.

Die beiden Hauptstudien sind [Band I (Methodik)](current/IOSN_2026_Band_I_Wissenschaftliche_Methodik.md) und [Band II (Software)](current/IOSN_2026_Band_II_PyPSA_Implementierung.md). Der [Repository-Audit](REPOSITORY_AUDIT.md) enthält offene Validierungslücken.
