# IoSN Modul 1 — Reduzierte Architektur (02.11.2026)

**Status:** REDUCED_ARCHITECTURE_PROPOSAL, keine neue Implementierung. **Basis:** V2 @ f8c29f67d23e1e064f1e158d2e6ac992e450cd27; MA4F @ 1ab3eb1aed54975e69586cc3d958a24d97a6288f; MD1 @ 5c68198984b6f2f430a49ff3e23d17c0b27320e1.

## Ziel und Grenzen

M0 liefert ein bereits bestücktes, hochaufgelöstes PyPSA.Network aus einem Netzformat. PECD, Hydro und DFT sind **davon unabhängige** Quellen. M1 ergänzt nur Zeitreihen an existierenden IDs; M2 aggregiert später. Keine Änderungen an PyPSA-Core, der Netzstruktur, dem Solver oder der Wetterjahrauswahl. Exakt die fünf extern festgelegten Wetterdatensätze.

## Drei Bausteine, keine neue Parallelpipeline

1. **Source Adapter:** Open-TYNDP tyndp-2026 und MA2 für regionale PECD-v4.2-Wind-/PV-CF; MA3 für Hydro. Nur bei tatsächlich gelieferten griddierten SPV-ORIG-NetCDF: kleiner nativer xarray-Reader. Wetter-Rohvariablen sind nicht fertige Wind-CF; Wind-CF regional PEON/P2ON bzw. PEOF/P2OF, PV-CF auch ORIG 0,25°, Hydro SZON-Intervallenergie. Version, Zeitbasis, Raumprodukt, Technologie und Hash dokumentieren.
2. **Spatial/Technology Mapper:** GeoPandas/Atlite-GIS und MA2-Validator verwenden; zusätzlich einen Mapper implementieren, der aus realen PECD-Regionen/Rasterzellen und belegten Anlagenstandorten eine `asset_profile_map` für bestehende Generator-IDs erzeugt. Buskoordinaten nur als qualifizierter Proxy; Offshore-Landanschluss nicht als Windparkposition; Fläche nicht mit MW-Anteil verwechseln. Hydro-Basin/TSO-Allokation bleibt im vorhandenen MA3-Fachadapter.
3. **Time-Series Composer:** vorhandenen MA4F-`scripts/iosn_m1/compose.py` unverändert bevorzugen; nur kompatible Inputs liefern. Zielattribute `generators_t.p_max_pu`, `storage_units_t.inflow`, ggf. `loads_t.p_set` mit eigener Lastquelle. Alle statischen PyPSA-Komponenten und ursprünglichen Busanschlüsse unverändert. Ein NetCDF pro Planungshorizont/Wetter-ID.

## Minimaler Snakemake-DAG

```
network.nc (M0 or other qualified import) -----+
                                               |
PECD native files -> normalize -> spatial map -+-> existing MA4F compose -> detailed_reference_*.nc
Hydro source -----> existing MA3 --------------+
DFT (only if needed) -> qualified load mapping-+
```

Keine Wiederholung von `build_cutout`, `determine_availability_matrix`, `build_renewable_profiles` bei bereits gelieferten fertigen PECD-CF; keine vollständige PyPSA-Eur-`compose_network`-Ausführung, da diese Komponenten neu erzeugt und vom clustered network ausgeht. Atlite nur für räumliche Hilfsoperationen oder explizit gesonderte meteorologische CF-Neuberechnung.

## Bestehende Implementierungen nicht neu entwickeln

- MA2 @ 11700baa8df8cafc6bd71b96998f8b2bca647ca0: regionaler CSV-Reader und Mapping-Validator; 20 synthetische Tests laut Bericht.
- MA3 @ b3b9bf133d1b5c968323a31f8ac76090f1f2e182: Hydro-Adapter; CI mit 62 Gesamttests, Fixture-Scope.
- MA4F @ 1ab3eb1aed54975e69586cc3d958a24d97a6288f: 92 bestandene Tests, 16 Snakemake-Jobs, fünf synthetische PyPSA-NetCDF und statische Invarianz laut Bericht; CI 41315496732 erfolgreich.
- MD1 @ 5c68198984b6f2f430a49ff3e23d17c0b27320e1: keine echten fünf Quelljahre, nativen PECD-/Hydro-Dateien oder reales Netzpaket qualifiziert.

## Nur zwei nächste konsolidierte Schritte

**R1 – Real-Input-Check / Delta-Freeze:** Repräsentative echte PECD-Datei je benötigtem Produkt, offizielle Masken/CRS, Hydro-Quellintervalle, bereits festgelegte fünf Weather-IDs und vorhandene Netz-Asset-/Standort-IDs prüfen. Ergebnis ist eine kurze Entscheidung, ob ORIG-NetCDF und automatisches Region-Mapping erforderlich sind. Keine neue Wetterjahrauswahl und kein großer Architektur-Review. Quellenqualifikation unabhängig vom M0-Netz möglich.

**R2 – Minimaler Patch + reale Qualifikation:** Nur fehlende Reader-/Mapper-Funktionen ergänzen; vorhandenen MA2/MA3/MA4F-Stack wiederverwenden; alle bestehenden Regressionstests, NetCDF-Roundtrip, Source-Coverage, statische Netzinvarianz, Hydro-MWh und fünf reale Wetterdatensätze qualifizieren. Reales End-to-End-Netz erfordert ein unabhängig qualifiziertes importiertes Netz. Optional DFT-Load-Mapper nur falls keine belastbaren Lastzeitreihen existieren. Unabhängige Abnahme vor Übergabe an M2.

## Status-/Risiko-Politik

Ohne echte PECD-/Hydro-Dateien ist ein Fixture-PASS möglich, **kein** Real-Data-PASS. Kein fingierter 0,25°-Wind-CF, kein stiller Null-/Jahres-Fallback, keine ungeprüfte MWp↔MW_AC-Konversion. Der größere V2-Makroplan bleibt historischer Plan; dieser reduzierte Vorschlag ersetzt ihn erst nach ausdrücklicher Owner-Freigabe.
