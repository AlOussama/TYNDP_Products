# TYNDP 2026 / IoSN — Netzreduktion mit PyPSA (wissenschaftlicher Prototyp)

**Revisionsstand:** 16. Oktober 2026. Wissenschaftliche Autorität für den
Vergleich ist ausschließlich ENTSO-E, *TYNDP 2026 Identification of System
Needs Methodology*, Konsultationsfassung vom 25.02.2026, Kapitel 3.8 und
Anhang 6.1. Erweiterungen sind explizit als solche gekennzeichnet.

## Dokumente

- `docs/Band_I_Wissenschaftliche_Methodik.md`: konsolidierte wissenschaftliche
  Theorie mit durchgehendem IoSN-Abgleich.
- `docs/Band_II_PyPSA_Implementierung_und_Validierung.md`: Softwaredesign,
  Datenverträge, Prüfverfahren und Reproduzierbarkeit.
- `docs/archiv_vor_revision/`: frühere Entwürfe, **durch die beiden obigen
  Revisionen ersetzt**, nicht als aktuelle Spezifikation verwenden.

## Inhalte und methodische Grenzen

Zwei Clustering-Varianten: **A** vollständiger Marktdispatch mit jährlicher
Überlastungsenergie (IoSN-nahe) und **B** exogene RES-/Last-Verfügbarkeit mit
expliziter Bilanzregel und Leitungsbelastung (Forschungsalternative).
Aggregation `P`/`Gamma`, technologieabhängige `R_k`, Referenz-PTDF und
kosten-/kapazitätsbasierte Gewichte, Ersatzimpedanzidentifikation und `F0`,
saisonale/richtungsbezogene empirische K1-Grenzen, analytische N-1-Polyeder K2,
konservatives Derating K3, duale LODF und Woodbury sowie FBMC-Research-Bridge.

Die **volle physikalische** PyPSA-Integration, reale ENTSO-E-/TYNDP-Daten,
HVDC/PST/Transformator-Sonderfälle und operative Core-FBMC-RAM sind **nicht
validiert**. Die Ergebnisse des Beispiels sind **synthetisch**.

## Getesteter Schnellstart (NumPy/SciPy/Pandas, ohne PyPSA)

```bash
python -m pip install -e '.[test]'
python -m pytest -q
python run_demo.py --output outputs
python -m examples.run_security_projection
python -m examples.run_fbmc_bridge
```

In der aktuellen Ausführungsumgebung: **24 Kerntests bestanden**. Der 9-Bus-
Vergleich wurde erneut reproduziert. Der analytische 3-Bus-Test liefert
`A->B 80 MW N-1`, die separate N-0-Grenze beträgt 150 MW.

## Optional: PyPSA-Integration (noch nicht hier ausgeführt)

```bash
python -m pip install -e '.[pypsa,test]'
python examples/pypsa_real_network.py /pfad/detailnetz.nc
```

PyPSA wird für die reale Modellierung und den Produktivlauf benötigt,
**nicht** für die unabhängig testbaren mathematischen Kernmodule. Der Adapter
ist ausdrücklich kein fertiger produktiver IoSN-Workflow.

## Quellen

- https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf
- https://docs.pypsa.org/stable/user-guide/clustering/
- https://docs.pypsa.org/latest/api/networks/subnetwork/
- https://arxiv.org/abs/1606.07276
- https://arxiv.org/abs/2211.00970
