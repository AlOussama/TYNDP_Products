# TYNDP-nahe Netzreduktion mit PyPSA — wissenschaftlicher Prototyp

Dies ist ein **Forschungsprototyp**, kein ENTSO-E-Referenzalgorithmus und keine N-1-sicherheitszertifizierte Implementierung. Der mathematische Kern verwendet NumPy und SciPy. PyPSA ist als gesonderte *optionale* Netz-Schnittstelle implementiert.

## Dateien

- `docs/Wissenschaftlicher_Methodenvergleich.md` — vollständige mathematische Studie.
- `tyndp_reduce/` — Kernmodule für DC-Netz, Clustering A/B, Aggregationsmatrizen, Technologien, Merit Order, PTDF-Projektion, F0 und N-1-Diagnostik.
- `examples/pypsa_real_network.py` — optionaler PyPSA-Adapter mit expliziten Hard-Stops.
- `outputs/` — reproduzierbare Ergebnisse aus einem **synthetischen**, nicht ENTSO-E-9-Bus-Test.
- `tests/test_core.py` — sieben Tests.
- `run_demo.py` — sofort ausführbare Demonstration ohne PyPSA.

## Schnellstart

```bash
python -m pip install -e '.[test]'
python -m pytest -q
python run_demo.py --output outputs
```

## Optional: PyPSA 1.4.0

```bash
python -m pip install -e '.[pypsa,test]'
python examples/pypsa_real_network.py /pfad/detailnetz.nc
```

**Grenzen:** Die echte PyPSA-Runtime war beim Erstellen des Pakets nicht verfügbar. Transformatoren, Links, Speicher und nichtneutrale Phase-Shifts sind im Adapter gesperrt. Die Rückgabe `reduced_unqualified.nc` ist noch **nicht** ein elektrisch kalibriertes Produktions-Ersatznetz. Der N-1-Estimator gibt bei fehlender Datenqualität `NaN`/Flags zurück.

**MCOE:** Die Abkürzung war in den zugänglichen Vorlagen nicht eindeutig definiert; im Bericht wird sie vorläufig als marginalkostenbasierte Merit-Order-Referenz interpretiert. Bitte ggf. durch Ihre konkrete Gleichung ersetzen.

## Reproduzierbarkeit

- `python=3.11+`, `numpy`, `scipy`, `pandas`; optionale PyPSA-Integration versioniert separat.
- Seed `20261016`; Netz, Kosten und Ratings künstlich.
- Train/Validation: 80/40 Stunden; gleiche Testzustände in A und B.
- Keine realen Systembedarfs-/Netzausbau- oder Security-Ergebnisse.
