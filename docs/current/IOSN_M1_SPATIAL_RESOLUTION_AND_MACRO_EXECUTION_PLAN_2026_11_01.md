# IoSN / TYNDP — M1 Spatial Resolution & Macro Execution Plan

**Datum:** 01.11.2026  
**Status:** M1-SPATIAL-MACRO-PLAN-PROPOSED — Dokumentation, keine Implementierung oder Ausführung  
**Autorität:** Ergänzung zum [M1 Architekturentwurf 30.10.2026](./IOSN_M1_PECD_PYPSA_REFERENCE_TIMESERIES_ARCHITECTURE_2026_10_30.md)  
**Module:** M0 = separater CGMES-Importer; M1 = Zeitreihen auf unveränderten Originalkomponenten; M2 = separate Netzaggregation  
**Harte Projektvorgabe:** exakt fünf extern festgelegte Wetterdatensätze; keine neue Auswahl, Bewertung oder zeitliche Reduktion.

## 1. Hauptentscheid: Elektrische Auflösung ist nicht meteorologische Auflösung

Das **detaillierte elektrische Netz** stammt aus M0 und enthält die originalen Bus-, Generator-, Last- und Speicherkennungen und deren Anschlussbeziehungen. M1 darf weder die vorhandene Busmap noch Leitungen, Generatoren, Lasten und Speicher technisch verändern oder aggregieren.

PECD liefert **keine einheitlich knotenscharfe Wetterauflösung**. Nach PECD v4.2 PUG sind wichtige Produktklassen:

| Datenquelle / Produkt | Meteorologischer Hintergrund | Tatsächliches PECD-Produkt für die Strommodellierung | M1-Relevanz |
|---|---|---|---|
| Wetter-Rohvariablen | ERA5/PECD Raster 0,25° × 0,25° | meteorologische Raster | Raster allein ist **kein** Kraftwerks-Kapazitätsfaktor |
| Wind Onshore CF | aus Wetter, Technologie und Standortmodell erzeugt | stündliche Profile typischerweise **PEON / P2ON** | Region/Technologie -> bestehende Generator-ID; keine erfundene raster-/busgenaue CF |
| Wind Offshore CF | dito | stündliche Profile **PEOF / P2OF** | Offshore-Standort/Zone, **nicht** automatisch landseitige Bus-Geokoordinate |
| Solar PV CF | Wetterdaten + PV-Technologie | stündliche Profile auf **ORIG**-Raster 0,25° (sofern bezogen) oder **NUT0/NUT2/SZON/PEON/P2ON** | Nur bei ORIG echtes rasterbasiertes Mapping; MW/MWp vs. Generator AC-MW beachten |
| Hydropower HP | hydrologisches/statistisches Modell | im Standard-PECD-4.2 **SZON** und **wöchentliche MWh-Energie** (HRG/HRI/HRO/HRR/HPO/HPI/HOL) | kein standortgenauer, stündlicher Inflow; eigenständige hydrologische Zuordnung und zeitliche Policy |
| Open-TYNDP 2024 | PECD v3.1 + PEMMDB/TYNDP-Dateien | Profile referenzieren TYNDP-Knoten und busmap_cluster_network.csv | Parser wiederverwenden, **Zonenknoten-Abhängigkeit ersetzen** |

**Wichtig:** Das installierte M0-Generatorobjekt hat eine feste elektrische Knoten-ID, aber die PECD-Profilauflösung ist weiterhin durch die Quellprofile festgelegt. Identische regionale Wind-CF an mehreren elektrischen Generatoren ist zulässig und **keine** Netzaggregation; es bewahrt die elektrischen Einspeisepunkte, nicht jedoch die meteorologische Unabhängigkeit innerhalb der Region. PECD-P2ON/P2OF sind zusätzliche, nicht beliebig zu PEON/PEOF austauschbare Zonensysteme. Tatsächlich gelieferte Produktversion und räumliche Ebene müssen explizit identifiziert werden.

**Quellen:** [Copernicus PECD v4.2 Product User Guide](https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=540941752), [Copernicus v4.2 Release-/Versionsvergleich](https://confluence.ecmwf.int/spaces/CKB/pages/540941872/Climate%2Band%2Benergy%2Brelated%2Bvariables%2Bfrom%2Bthe%2BPan-European%2BClimate%2BDatabase%2Bversions%2Bcomparison), [Open-TYNDP Scripts](https://github.com/open-energy-transition/open-tyndp/tree/5b25904496150b889b321dd8d76f393ef09a0f2e/scripts/sb).

## 2. Bindende Raum- und Zeitverträge vor MA-2

### 2.1 Elektro-Asset -> Profil; nicht Bus -> Raster als pauschale Regel

Erforderlicher Metadata-Vertrag:

- **asset_id**: unveränderte eindeutige M0-Komponentenkennung.
- **bus_id / mRID**: unveränderter elektrischer Anschluss.
- **asset_location**: falls vorhanden reale Anlagenkoordinate; alternativ dokumentierte Bus-/Umspannwerkskoordinate **nur bei gültiger Repräsentativität**.
- **technology_variant**: onshore/offshore PV-Typ (rooftop / utility fixed / tracker), Wind-Turbinenspezifikation und passende PECD-Variante.
- **source_profile_id**: versionierte PECD-Region oder (wenn im tatsächlich gelieferten Produkt verfügbar) Rasterzelle.
- **spatial_basis**: EXPLICIT_SOURCE_LINK / VERIFIED_PLANT_POINT / VERIFIED_BUS_PROXY / CAPACITY_WEIGHTED_MULTIREGION / UNRESOLVED.
- **weather_id**: eine der fünf festgelegten Quellkennungen; time index & horizon separat.
- **assignment_quality / evidence_ref**: Herkunft und Prüfentscheidung.

Geografische Masken sind nicht zwangsläufig externe Shapes. Die PECD-4.2-Dokumentation nennt für die regionalen Systeme insbesondere auf dem CDS verfügbare **fractional NetCDF region masks**, während die zugrunde liegenden Shapefiles teilweise nicht öffentlich sind. Regionmasken sind daher als offizieller bevorzugter Raumbezug zu untersuchen. Für grenznahe Punkte, Mehrfachzugehörigkeit oder fehlende Standorte gilt **keine stillschweigende Nearest-Zone-Regel**.

Formal für bestehende Generatoren g, zulässige Profile p, Wetterdatensätze s:

A(g,p) >= 0, Summe_p A(g,p) = 1 (sofern Quelle und Einheit eine eindeutige Zuordnung erlauben)

CF(g,s,t) = Summe_p A(g,p) * CF(p,s,t)

P_avail(g,s,t) = p_nom(g) * CF(g,s,t)

Standard ist eine genau **ein** validiertes Profil je passend modelliertem Generator. Bei echten *aggregierten Generatorobjekten*, die mehrere Wetterregionen umfassen, braucht A(g,p) explizite **Kapazitätsgewichte**. Standort-/Gebietsfläche allein ist kein gültiger Ersatz für Kapazitätsverteilung.

**PV-Sonderfall:** PECD-CF in **MW/MWp** und M0-p_nom ggf. in **MW_AC**. Direkte Zuordnung zu p_max_pu ist nur bei kompatibler Nennleistungsdefinition gültig; sonst dokumentierter DC/AC- und Clip-/Verlustkonverter, ohne bestehende statische M0-Daten zu überschreiben.

**Keine unbelegte Rekonstruktion feiner meteorologischer Profile:** Verfügbare Wind-CF für eine PEON/PEOF-Zone liefern nicht automatisch standortgenaue Windleistung für jedes 0,25°-Rasterpixel. Die wetterseitige Genauigkeit darf im M1-Report nicht als Knoten- oder Rasterauflösung ausgegeben werden, wenn sie nur regional ist.

### 2.2 Hydro-Energie und hydrologische Flächen

Für jede Hydro-Quelle: eindeutig HRI/HRR/HPI/HOL usw. (Inflow) versus HRG/HRO/HPO (Generation). Quelle, Gebiet, Hydrotyp, Zeitraum, physikalische Energieeinheit und Bedeutung im PyPSA-Speichermodell festhalten. Die Geokoordinate eines elektrischen Netzknotens allein bestimmt **nicht** das hydrologische Einzugsgebiet oder die Aufteilung eines regionalen Zuflusses.

Falls E(z,w) in MWh über Hydro-Gebiet z und Quellwoche w vorliegt, nur bei begründeter hydrologischer Verteilung B(h,z) auf die vorhandenen Speicher h:

E_h,w = B(h,z) * E(z,w); und wenn ein konstantes intraweek-Profil explizit genehmigt wird:
P_inflow(h,t in w) = E_h,w / DeltaT_w [MW]
mit Vergleich: Summe_{t in w} P_inflow(h,t) DeltaT_t = E_h,w.

Intervall-Grenzen sind tatsächliche Zeitstempel (keine pauschale 168h bei abweichenden partiellen Intervallen). Für hydrologische Energieäquivalente die PyPSA-Speicher-Wirkungsgradkonvention prüfen; unterschiedliche Energiegrößen nicht blind gleichsetzen. Open-/closed-loop PHS differenzieren, Zufluss nicht künstlich hinzufügen.

### 2.3 Zeitindizes und vollständiger Source-Contract

- Genau fünf festgelegte weather_id; eigenständige planning_horizon, calendar_year, timestamp, timezone (vereinheitlicht auf UTC), ggf. Klimadatenstream.
- Keine Neuauswahl, kein Zeitclustering; native Stundenreihen ohne unkontrollierte Leap-/DST-Verschiebung.
- Keine stillen Daten-Fallbacks in andere Wetterjahre, 0 oder Mittelwerte.
- Quellhashes, Datenversion, Dateischnittstelle und räumliche Auflösung (ORIG/PEON/P2ON/PEOF/P2OF/SZON etc.) für jede Variable manifestieren.
- Keine Annahme, dass die drei verschiedenen PECD-Produktfamilien wind/pv/hydro dieselbe Fläche und denselben Zeitindex nutzen.

## 3. Vier konsolidierte Makros; nur eine harte Architekturfreigabe vor Parallelisierung

| Makro | Umfang und Owner | Eingang / Arbeitsauftrag | Definition of Done / Gate | Parallelisierung |
|---|---|---|---|---|
| **M1-MA1 Spatial & Source Contract Freeze** | Architekt + Datenauditor; **noch kein produktiver Code** | Open-TYNDP Reuse-Ledger vervollständigen; repräsentative echte PECD-/Hydro-Dateiheader und M0-Netz-/Asset-Schema prüfen; alle fünf festgelegten Sets inventarisieren; Technologie-, Region-/Masken- und Einheitenverträge, A/B-Methodik, QA-Schwellwerte festlegen | **G1: M1-SPATIAL-SOURCE-CONTRACT-FROZEN** oder explizit BLOCKED mit einer gebündelten Klärungsliste; keine unbewiesenen Geometrie-/Semantikannahmen | Muss MA2/MA3 vorangehen; M0 kann unabhängig weiterarbeiten, M0-Schema/Beispiele für Freeze nötig |
| **M1-MA2 RES/PECD Adapter + Spatial Match** | Umsetzung Wind/PV, 1 Implementierungsmakro | Aus Open-TYNDP clean_pecd_data / build_renewable_profiles_pecd kompatible Parser übernehmen; onshore/offshore/pv-Profilvarianten und region masks bzw. ORIG-Grid den **bestehenden** Generator-IDs zuordnen; A(g,p), vollständige 5-Sets-Arrays, Fixtures | **G2: RES-PROFILE-MAPPING-QUALIFIED**: 100 % der verpflichtenden betroffenen Kapazität explizit zugeordnet, keine stillen Fallbacks, passende Einheiten, nachgewiesener Quellprofil-Roundtrip | Nach MA1 **parallel zu Hydro** |
| **M1-MA3 Hydro Inflows + Time Semantics** | Umsetzung Hydro, 1 Implementierungsmakro | Tatsächliche Hydroquelle / Wochen- bzw. Tagesintervalle spezifizieren; Open-TYNDP hydro-Skripte selektiv adaptieren; Hydroklassifikation, hydrologische Verteilungsfaktoren B(h,z), Energieerhaltung, 5-Set-Arrays, Tests | **G3: HYDRO-SOURCE-ENERGY-QUALIFIED**: physikalisch korrekte Größe, regionale Quellen vollständig zuordenbar oder qualifizierter Blocker, Integral per Quellintervall geprüft | Nach MA1 **parallel zu RES** |
| **M1-MA4 Composer, End-to-End QA & M2 Handoff** | Integrator + unabhängiger Reviewer in einem konsolidierten Abnahmemakro | Komplettes M0-Netz laden, ausschließlich erlaubte Zeitreihen setzen, fünf Netz-/Zeitreihenoutputs exportieren, vollständige Quell- und Mappingledger abgleichen, NetCDF-Roundtrip + statischen Fingerprint vor/nach schreiben, M2-Schnittstelle qualifizieren | **G4: M1-REFERENCE-TIMESERIES-ACCEPTED-FOR-M2** oder **M1-BLOCKED/CONDITIONAL** mit vollständigem, priorisiertem Befund | Nach MA2 **und** MA3; finaler unabhängiger Review innerhalb des Makros |

**Durchlaufspolitik:** Jedes Makro liefert ein vollständiges Arbeitspaket mit Tests und Report statt vielen Einzelaufträgen. MA2 und MA3 haben im Freeze definierte gemeinsame Datenverträge; keine Änderungen der Schnittstellen während der parallelen Umsetzung ohne dokumentierte Governance-Entscheidung. G4 ist eine einzige konsolidierte Endabnahme. Von MA2/MA3 unüberwindlich offene Datenlücken bleiben sichtbare BLOCKER statt fingierter Zeitreihen.

### Scope-Abgrenzung

- M0 als separater Producer des CGMES-Referenznetzes, M1 liefert keine eigene Netzkonvertierung.
- M1 liefert keine Ersatzknoten, kein Clusterverfahren, keine PTDF-basierte Aggregation und keine neue Wetterjahrauswahl.
- DFT/Last- und thermische nicht-wetterabhängige Zeitreihen sind eine separate optionale Inputsparte; sie werden bei Bedarf mit demselben Original-ID-Vertrag injiziert, aber nicht aus PECD-Neuberechnungen erfunden.
- Vollständiger Dispatch/AC-Lastfluss ist nicht G4-Abnahmepflicht, sofern keine bilanzierten Betriebsfälle vorhanden sind. Die M1-Ausgabe ist ein modellierbares **Input-Netz**, nicht automatisch ein gelöster Netzzustand.

## 4. Räumliche Akzeptanzmatrix (G1/G2/G3/G4)

| Fall | Verhalten / erforderliche Evidenz | Abnahme |
|---|---|---|
| 1 Onshore-Windgenerator mit expliziter PEON/P2ON-Zuordnung | Region & Technologieprofil -> original generator_id; bus_id bleibt | PASS bei vollständig passender Quelle |
| Mehrere Generatoren in derselben Windregion | gleiches Profil zulässig; alle elektrischen Einspeisepunkte bleiben | PASS, keine Behauptung feinerer Windkorrelation |
| PV-Standort und geliefertes ORIG-Grid | definierte Standort-/Zellenzuordnung, PV-Typ, DC-/AC-Normierung | PASS bei geprüften Daten |
| PV-Quelle nur PEON/NUT2 regional | regionale Profile verwenden, keine scheinbar feine Auflösung interpolieren | PASS, Qualität als regional gekennzeichnet |
| Offshore-Generator am landseitigen Bus | Offshore-Standort / PEOF/P2OF-Anschluss-IDs notwendig | BLOCKED ohne gültige Zuordnung |
| Generatorgruppe deckt mehrere PECD-Regionen ab | kapazitätsgewichtete A(g,p), Herkunft notwendig | BLOCKED ohne Kapazitätsanteile |
| Regionengrenze / keine öffentliche Shape | offizielle fractional masks oder geprüfter Lookup; Mehrdeutigkeit dokumentieren | BLOCKED ohne disambiguierte Zuordnung |
| Hydro auf SZON und Woche, Speicherstandort CGMES | B(h,z) mit hydrologischer Quelle + zulässige Stunden-Policy | BLOCKED ohne belegte Allokation |
| Last/DFT bereits generatorfremd an Original-Load-ID | stündliche Last per Original-ID übernehmen, niemals neu clustern | PASS bei Quell- und Lastsicherheit |
| Fehlende Wetterdatei oder unpassendes Jahr | keine Ersetzung durch anderes Klima- oder Nullprofil | FAIL |

### Teststrategie

Eine repräsentative Fixture-Suite in MA2/MA3 muss mindestens PEON/P2ON, PEOF/P2OF, ORIG-PV, regionales PV, Regionengrenze, Offshore-Landanschluss, aggregierten Generator, Hydro-SZON mit Wochenenergie, Leap-/DST- und fehlendes-Profil-Fälle umfassen. Danach **eine vollständige gemeinsame fünf-Sets-Kampagne** in MA4.

Prüfungen umfassen:
1. **100 % statische Invarianz** aller ursprünglichen M0-Netzobjekte, technischen Stammdaten und Anschlussknoten. Ausnahmen müssen explizit separat genehmigt sein; Default = keine.
2. **100 % der verpflichtenden wetterabhängigen Generatoren** haben ein passendes Profil oder erhalten ein transparentes BLOCKED. Coverage zusätzlich in % der installierten MW, nicht nur Anzahl.
3. **Keine erfundene meteorologische Detailauflösung.** Output-Ledger weist explizit aus, welche Profile regional und welche tatsächlich rasterbasiert sind.
4. **Profilwerte und Zeithashes** stimmen nach Import/Export überein; Wertebereiche technologiespezifisch prüfen, nichts implizit clippen.
5. **Rückaggregation** nur dann gegen PECD-Regionenzeitreihen als Gleichheit prüfen, wenn dieselbe Kapazitäts-/Technologiegewichtung verwendet wird. Ansonsten nur interne Erhaltung und klar bezeichnete Abweichungsanalyse. Insbesondere kein erzwungener Gleichheitsanspruch zwischen ORIG-PV und PEON-PV mit anderen Gewichtungen.
6. **Hydro**: Wochen-/Tages-MWh-Energie mit korrektem Zeitintegral in MW überführen; Speicher-/Wirkungsgrad- und Hydrotyp-Semantik validieren.
7. **PyPSA-NetCDF Roundtrip** und Speicher-/Datenvolumenprüfung über alle fünf Datensätze; optionale physikalische Plausibilisierung nur bei passenden Betriebsfallzeitreihen.

## 5. Konkrete nächste Aufträge und Empfehlung

**Sofort freigeben: M1-MA1 Spatial & Source Contract Freeze** als **ein einziger** Fachmakroauftrag. Es muss die *real gelieferten* fünf Wetterdatensätze und ein M0-Beispielnetz verwenden. Fehlen diese Daten aktuell, darf es Format-Contracts und Testfixtures vorbereiten, aber **nicht** "FROZEN" oder "PASS" behaupten.

Nach G1:
- **Parallelauftrag RES/PECD**: M1-MA2.
- **Parallelauftrag Hydro/Inflow**: M1-MA3.
- Final gemeinsamer **M1-MA4 Integrations- und unabhängiger Abnahmemakro**.

**Handoff-Paket aus MA1:** (1) SOURCE_SCHEMA_LEDGER, (2) PECD_SPATIAL_RESOLUTION_MATRIX, (3) M0_ASSET_ID_CONTRACT, (4) RES_PROFILE_MAPPING_SPEC, (5) HYDRO_ENERGY_MAPPING_SPEC, (6) TECH_CARRIER_CROSSWALK, (7) QA_ACCEPTANCE_CONTRACT, (8) handoff/auftrag für MA2 und MA3. Alles unter docs/current oder einer konsistenten M1-Dokustruktur versionieren, ohne produktiven Code in MA1.

**Relevante Branch/PR:** [M1 Architektur-Draft PR #6](https://github.com/AlOussama/TYNDP_Products/pull/6). Dieses Addendum ergänzt die vorhandene Dokumentation; es sind noch keine Produktionsdaten oder CI-Ergebnisse untersucht.