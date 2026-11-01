# MA1C — Einmalige gebündelte offene Inputliste und verifizierbare Exit-Kriterien

**Gesamtentscheidung:** `M1_SOURCE_CONTRACT_BLOCKED`. Diese Liste ist die **einzige** konsolidierte Übergabe an Datenhalter/M0-Owner, nicht mehrere Mikrofragen. Die Listenpunkte beschreiben benötigte Lieferartefakte, **keine** neu zu wählenden Wetterjahre.

| ID | Einmalig erforderlicher Input | Prüfbarer Exit / Owner | Gate |
|---|---|---|---|
| `IN-01` | **Exakt fünf bereits extern festgelegte Weather-IDs** mit `planning_horizon`, `climate_year/model`, Quell- und Freigabereferenz; keine neue Auswahl | je 1 echte ID in Slots 1–5, eindeutige Zuordnung `(horizon,weather_id)`, keine Duplikation/unbelegte WS-Substitution; Data Owner | G1-D/E |
| `IN-02` | **PECD-Wind-/PV-Dateien** für benötigte Horizonte/alle fünf IDs, inkl. originaler CSV-/NetCDF-Header, Zeitachsen, Release/Revision, Asset-/Region/Tech-Katalog, SHA256 + Nutzungsrecht | echte Zeitreihen pro erforderlicher Technologie und WS, originaler `Date/Hour`-Index und vollständige Stunden/Quality, kein Fill oder 3→5-Fallback; Source Owner | G1-D |
| `IN-03` | **Räumliche PECD-Produkte:** echte PEON/P2ON/PEOF/P2OF-Zonen, ggf. PV-ORIG-Grid, fractional NetCDF masks/version/CRS/Registry + source profile IDs | echte Masken-Byteprobe und fachliche Zuordnung für Onshore/Offshore/PV, Grenzlage und Composite mit dokumentierten MW-Anteilen; Geo/RES Owner | G1-D |
| `IN-04` | **M0 DetailedNetworkReference v1** in unveränderlicher Revision mit PyPSA-Netz, `m0_sidecar`, Source-/ID-/Terminal-/View-Maps, Manifesthashes, Geo-/Country-/Synthetic-Bus-Klasse, Komponenten-Support und Capabilitystatus | M0-Owner bestätigt DNR/1.0.0 bzw. abweichende Version, `source_revision_id,operating_state_id,canonical_revision_id,projection_id`; Source-ID→PyPSA-ID + bereits vorhandenes Bus/Asset + `p_nom` real geprüft; G1-C | G1-C |
| `IN-05` | **Hydro-Quellfiles** `HRR/HRI/HPI/HOL` und tatsächlich relevante `HCL`-Portinformation je fünf Wetter-IDs/Regionen, Quelle `MWh_inflow` vs `MWh_generation`, native `WEEK`-/Daily-Intervalle, SHA256/Revision | verifizierte echte Intervallanfangs-/Endstempel + Quellwerte; kein `/168` ohne Längenprüfung; HCL nicht als automatische natürliche Quelle; Hydro Owner | G1-E |
| `IN-06` | **Hydrologisches Asset-/Basin-/TSO-Mapping:** reale Anlage, Hydroregion, Zuordnungsmethodik, Allokationsanteil, Original-M0 Speicher-/RoR-/Pumpen-Turbinen-Portklasse, Wirkungsgrad/SOC | nachvollziehbare B-Quellanteile, regionale Restenergie explizit, `sum P Δh = E` je Quelle/Asset; M0/Hydro Owner | G1-C/E |
| `IN-07` | **PV-Nennleistungs-Schnittstellenfestlegung**: M0-AC-`p_nom`, PECD-MWp/DC-Basis, Wechselrichter/Clipping-/Loss-Interpretation pro PV-Portfolio | schriftliche und anhand realer Profil- und Kapazitätswerte reproduzierbare MWp→MW_AC-`p_max_pu`-Transformation; RES/M0 Owner | G1-D |
| `IN-08` | **Demand/DFT-Sourcepaket** nur soweit in MA4 als Pflicht definiert: realer fünf-WS-Abdeckungsnachweis, Load-ID-/TSO-Allokation, unverändertes M0-`loads_t.p_set`-Overwrite-Policy | keine drei regulären TYNDP-WS als fünf vollständige behauptet, `p_set` nur bei echter Quelldeckung; Demand/MA4 Owner | G1-D / MA4 |
| `IN-09` | **Reproduktions-/Rechtepaket**: Datei-SHA256/Größe, PECD prebuilt 2026-08-13 vs korrigiert 2026-08-21 vs 2026-10-07, Lizenz/Access, Pin von Reader/Core | pro Datei eindeutiger Ursprung und nachgewiesener Versionsmix bzw. freigegebene Kompatibilitätsmatrix; Source/QA Owner | G1-C/D/E |
| `IN-10` | **Binärarchive** nur sofern als tatsächliche Quelle beansprucht: entpacktes kontrolliertes Inventar + Herkunft und SHA256 der enthaltenen Rohdateien | nicht lesbare Projekt-ZIPs entweder zweifelsfrei klassifiziert oder explizit außerhalb des maßgeblichen Real-Source-Sets; Data Owner | Scope evidence |

## Akzeptanzabfolge ohne Mikroschleifen

1. Liefernde M0-/Data-Owner geben **ein einziges** versioniertes, hash-basiertes Paket mit obigen Bestandteilen und deklarierter Dateiabdeckung ab. Fehlende, wirklich nicht relevante Technologien/Quellklassen sind begründet `NOT_APPLICABLE`, nicht pauschal als null gefüllt.
2. Unabhängige spätere Datenabnahme liest reale Filebytes/Headers/Geo-/Hydrointervall- und M0-Assetproben, qualifiziert G1-C/D/E **pro Scope** und aktualisiert maschinenlesbare Source- und Crosswalk-Ledgers. Ein formal validiertes, aber physisch nicht geliefertes Schema bleibt `DESIGN_ONLY`.
3. MA2/MA3 prüfen die reale Datenabdeckung zusätzlich in einem konsolidierten Lauf; wo nicht gegeben bleibt `IMPLEMENTED_FIXTURE_ONLY` oder `BLOCKED`; erst MA4 hat Integrations-/NetCDF-/Review-Zuständigkeit.

**Keine unbelegten Schwellenwerte:** `100%` bedeutet für verpflichtend abgedeckte, im echten Paket vorhandene Source-/Asset-Klassen vollständige Zuordnung oder explizite Blockierung; numerische Energietoleranzen sind nach tatsächlicher Datei-Präzision und PyPSA-Port vor Ausführung festzulegen, nicht erfunden.

**Nicht zulässige „Lösungen“:** Wiederwahl anderer Wetterjahre; Wechsel auf `[0]` der drei TYNDP-WS; Zero-/Mean-/Hour-/Horizon-Fallback, hydro generation als inflow, bus-station-centroid als Windparkstandort, 3W-Stern-Geopunkt oder synthetischer CW/Geo-Witness.
