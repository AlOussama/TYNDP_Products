# MD1 — Eigenständige M1-Join-Grenze: source-native regional profiles → M0 assets

**Architektur:** PECD/TYNDP liefern netzunabhängige regionale Profile und Hydro-Intervalle. M0/CGMES liefert unabhängig elektrische Busse, vorhandene Generatoren, Lasten und Speicher. **Nur diese dritte Schicht** koppelt Profile/Quellen mit M0-Anlagen und später dynamischen PyPSA-Attributen; keine Quellseite muss den jeweils anderen Provider kennen.

```text
PECD/TYNDP native source ── source-native manifest/profile/time/geometry ──┐
                                                                          ├─> M1 explicit spatial/hydro asset join ─> MA4F/MA4R PyPSA dynamic-only composer
CGMES -> M0 DNR v1 ──────── source/view/asset/port/geo-quality revision ──┘
```

## Voraussetzungen an **dieser** Grenze, nicht am PECD-/M0-Provider

1. **Unveränderliche getrennte Identitäten:** source-native `profile_id`, `region_id`, `weather_id`, `planning_horizon`; elektrisch `source_entity_id`/`asset_id`, `view_id`, `existing_generator_id`, `existing_bus_id` und `projection_id`. Join-Witness enthält beide unveränderten Quellrefs und die Mapping-Approval/Version, niemals ein ID-Namespace-Alias.
2. **Wind:** Region/Technologie → bestehender M0-Generator; gleiches PEON/PEOF-Regionalprofil kann auf mehrere unterschiedliche Generatoren wirken, ohne Busse zu ändern. Originalknotenauflösung ist keine meteorologische Rasterauflösung. Für Offshore ist Plant-/Offshore-Region maßgeblich, **nicht** landseitiger Anschlusspunkt.
3. **PV:** Rasterprodukt `ORIG` nur wenn tatsächlich geliefert, sonst regionale Quelle wie geliefert. PECD `MW/MWp` mit M0 `p_nom[MW_AC]` nur mit nachweislich freigegebenem DC-/AC-/Clipping-Transformationsvertrag. Die PECD-Quelle darf unabhängig davon als richtiges `MW/MWp`-Produkt zertifiziert werden.
4. **Composite:** ein bereits existierender multi-region M0-Generator hat geprüfte MW/MWp-Anteile `A[g,p,h]≥0` und `Σ_p A=1`. Fractional Zellflächen-Masken sind **nicht** Ersatz für MW-Anteile.
5. **Hydro:** hydrologische `hydro_area_id`, Hydrotyp und nativer Energiezeitraum → bestehende Hydro-Anlage und freigegebener Port mit hydrologischem/TSO-`B[a,z]` und Umwandlungsfaktor. Ein elektrischer Bus und dessen Koordinate sind **kein** Basin-Nachweis. Nativer Source-MWh-Abschluss und Model-MWh-Abschluss getrennt.
6. **Legacy-Adapterrevisionen:** MA2/MA3 referenzieren `network_revision_id`. Das ist kein vollständiger M0 CAN/2.0.0→DNR/1.0.0-Versionswitness; MA4F-Bridge benötigt `canonical_revision_id` plus `projection_id`, `reference_id`, Sidecar-HASH und Source-Map. Kein stiller Null-/Default-/Alias-Brückenschritt.
7. **Dateiformate:** MA2 ist für TYNDP-RAW10/DateHour/ISO **CSV** ausgelegt; gridded PV-ORIG-`.nc` ist nicht direkt sein Native-Parser. GeoJSON-Polygon-Reader ist nicht identisch mit offiziellen PECD fractional **NetCDF**-Regionmasken. Vor realem Join ggf. verlustbewahrenden, prüfbaren Source-Format-/Regionmask-Adapter vom MA4F/RES-Owner freigeben.
8. **Write-Policy:** Nur MA4F-/MA4R-Composer materialisiert Netze und schreibt whitelisted dynamische Attribute. Wind/PV und HRR können beide `Generator.p_max_pu` adressieren → disjunkte Target-Ownership und Konflikt-Audit notwendig. HRI/HPI/HOL nur auf genehmigte `StorageUnit.inflow`- oder staged Store/Link-Ports; Lasten nur bei DFT/M0 freigegebenem `Load.p_set`-Scope. Statische M0-IDs/`bus`/`p_nom`/Topology bleiben unverändert.

**Ergebnis:** Ohne echte PECD/Hydro-Bytes, fünf Projekt-IDs, real erzeugtes DNR/Sidecar, geprüfte Masken-/Geo-/Basinanteile und Version-Bridge kann **kein** produktiver Join-PASS erfolgen. Keine dieser Bedingungen ist angeblich ein Bestandteil der netzunabhängigen PECD-Quelldaten.
