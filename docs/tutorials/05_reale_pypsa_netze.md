# Tutorial 05 — Eigene PyPSA-Netze: Vorbereitung und harte Grenzen

## Installation

```bash
python -m pip install -e ".[test,pypsa]"
```

Optionaler, noch nicht end-to-end qualifizierter Adapter:

```bash
python examples/pypsa_real_network.py /pfad/zum/validierten_netz.nc
```

Die Netzdatei muss ein vorab validiertes PyPSA-netCDF-Netz enthalten. Der Adapter bricht bewusst ab, wenn er vorhandene Transformatoren, Links, Speicher oder andere nicht unterstützte Elemente nicht verlustfrei übertragen kann.

**Das resultierende `reduced_unqualified.nc` ist eine topologische Initialisierung**, kein vollständiges IoSN-Äquivalent. Seine Ersatzimpedanzen, No-Load-Flows und N-1-sicheren Transfergrenzen sind noch nicht produktiv angefügt. `real_busmap.csv` enthält die initiale Knoten-Zonen-Zuordnung.

## Vor der Verwendung realer Datensätze dokumentieren

1. Netzversion, Snapshotliste, Topologiestatus, Spannungsebenen, Leitungsparameter und thermische Grenzwerte.
2. Bilanzierte nodale Zeitscheiben für Methode A; exogene RES-Verfügbarkeit/Last + explizite Balancingannahme für B.
3. Anschlussknoten von Erzeugung, Verbrauch, Speichern, HVDC und Transformatoren samt zeitabhängigen Vorzeichenkonventionen.
4. Kalibrierungsstunden, unabhängige Validierungsstunden und tolerierte Fluss-RMSE-/N-1-Fehler.
5. Umgang mit Inselungen, Remedial Actions, PSTs und 4 saisonal-/gerichteten Kapazitätsparametern.

## Technische Stop-Bedingungen

Die Ergebnisse sind **nicht** als TYNDP/ENTSO-E-validiert zu deklarieren, solange: (i) einzelne Komponenten ignoriert werden; (ii) N-1-Inselungen unbewertet bleiben; (iii) aus bilateralen Handelsgrenzen universelle Leitungsgrenzen abgeleitet werden; oder (iv) ein konstanter `F₀` ohne unabhängige Validierung angenommen wird.

Die methodische Primärquelle für den IoSN-Vergleich ist die Konsultationsfassung: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf

Zurück zur [Tutorial-Übersicht](../TUTORIALS.md).
