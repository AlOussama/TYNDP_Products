# M2-MA1 – Cold-Start-Makroauftrag: Physical Foundation + Country-Quota Clustering

**Projekt:** AlOussama/TYNDP_Products  
**Rolle:** lokaler Implementierungskoordinator mit AC-Netzmodell-/PyPSA-, Graphoptimierungs- und ENTSO-E-IoSN-Expertise.  
**Auftragsart:** vollständiger **Ausführungs**auftrag mit parallelen Workern/Subagenten und unabhängigen Reviews. Kein reines Planungsgespräch.  
**Abhängigkeit:** M2-R0-REVIEW-20261103; MA2/MA3 sind ausdrücklich **noch nicht** freigegeben, sofern ihre Eingangsgates fehlen.

## 1. Verbindliche Quellen zuerst verifizieren

1. Remote-Commit **3dc719a35f57bd9516bef8486bf262b75509d6b1** und Review-Branch **review/iosn-m2-network-aggregation-plan-20261103** prüfen. Den **aktuellen Review-Commit** des Branchs vor Arbeitsbeginn protokollieren.
2. Lies vollständig:
   - [80 – unabhängig verifizierter M2-Review und Ausführungsleitfaden](80_M2_NETWORK_AGGREGATION_REVIEW_AND_EXECUTION_PLAN_2026_11_03.md)
   - [Offizielle 18-Punkte-Methodik-/Codematrix](../IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md)
   - [Offizielle 102-Zonen-CSV](../IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv)
   - [Band I – Wissenschaftliche Methodik](../IOSN_2026_Band_I_Wissenschaftliche_Methodik.md)
   - [Band II – Implementierung](../IOSN_2026_Band_II_PyPSA_Implementierung.md)
   - https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf – §3.8/3.9 und Annex 6.1.
3. Untersuche den bestehenden main-Code @ **1595d6d38e77804760612621657721b3699d2fea**, insbesondere dc.py, pypsa_adapter.py, screening.py, clustering.py, aggregation.py, equivalent.py, security.py und alle Tests. Baselines vor Änderungen pinnen.
4. Halte offiziell beschriebene Regeln D/T und eigene notwendige algorithmische Regeln I sauber getrennt.

## 2. Feste Modul- und Wissenschaftsgrenzen

- Nur **Modul 2**. **Keine** Änderung an Modul 0/CGMES, Modul 1/PECD, Wetterjahrselektion oder Netzimport und -export des jeweils anderen Moduls.
- Input ist eine fertige, detaillierte und synchronisierte Referenznetzrepräsentation. Fünf bereits festgelegte Wetterjahre bleiben exakt unverändert. Nicht mit den drei offiziellen Wetterfällen der IoSN-Investitionsoptimierung verwechseln.
- Ein europäisches gemeinsames elektrisches Modell: **keine** länderweise getrennte PTDF/Slack-Lastflussrechnung. Landesgrenzen sind strikte Zonierungsrestriktionen und unveränderlich.
- Offizielle **37 Einträge, 102 Zonen**, genaue Einzelquoten; ausdrücklich „Northern Ireland“ getrennt von „United Kingdom“ und kein stilles Merging. Vollständige Geographie vs. kleine Testfixtures unterscheiden.
- Engpassindikator: getrennt je vorgegebenem Jahr **jährliche Überlastungsenergie in MWh für 225-/400-kV-Zweige**, nicht eigene EE-/Last-Methode B.
- Keine erfundenen NETZ-/Rating-/Dispatch-/Kontingenzdaten für eine angeblich reale Abnahme.
- Bei unbekannter ENTSO-E-Algorithmik minimale, deterministische I-Entscheidungen implementieren und im Register kennzeichnen.
- Verwende stabile bestehende Bausteine weiter, aber verstecke vorhandene Grenzen nicht.

## 3. Interner paralleler Arbeitsplan

**W-PHY – physical-network/adapter worker (eigenes Worktree/Branch)**

Implementiere/integriere:
- explizite Typen für detaillierte AC-Zweige, Transformatoren, PST, steuerbare HVDC-Terminals, AC-Inseln, Limits, Referenznetzinjektionen und Richtungs-/Einheitenkonventionen;
- sparse PTDF-/Lastfluss-Ansatz oder geeigneten bestehenden PyPSA/SciPy-Solver statt dichtem N×N-inverse und Ranktests für europaweite Netze;
- korrekte Nodal-/Island-Bilanzen bei HVDC-Terminaleinspeisungen und PST-Phasenschüben; identische Semantik in Referenzrechnung und Export, klare Abgrenzung neutraler x-Kalibrierung und aktivem Betrieb;
- datenkontraktbasiertes Preflight mit Fail-Closed für unvollständige Daten; unveränderlichen und gehashten Referenzfluss-Cache.
- Referenztests: zwei AC-Inseln mit kontrollierter HVDC-Brücke; Trafo im AC-Graphen; PST neutrales/aktives Betriebsfenster; Branch-Orientation; saisonale MW-Limits; Injektionstests und Vergleich gegen unabhängige direkte DC-Rechnung.

**W-CLU – constrained country clustering and screening worker (eigenes Worktree/Branch)**

Implementiere/integriere:
- Loader/Validator für die offizielle 102-Zonen-/37-Gebiete-Tabelle und einen expliziten Country-Label-Identifier-Vertrag;
- zwingende Länderreinheit, exakte Country-Quoten und zusammenhängende AC-Cluster;
- deterministische initiale Region-Growing/Graph-Contraction auf ganzem Referenzgraph mit **länderinternen** Merges; physische grenzüberschreitende Kanten bleiben im Netz und in der Aggregationsprojektion;
- Screening mit 225/400-kV-Filter, stunden-/jahresscharfen Limitvorgaben und MWh-Energie, die fünf externen Jahres-IDs getrennt;
- Konnektivitäts-/Quoten-/Kritikalitätserhalt-Nachweise, gerichtete Gegenflussdiagnostik, unvollständige 110-kV-Ties; exakte P/Gamma/Az-Kontrollen.
- Negative Fixtures: unauflösbares Country-Label, unterbudgetierte Insel, gemischtes Cluster, falsche Quoten, gegenläufige Parallelflüsse, kritische Leitung innen verschluckt, widersprüchlicher Country-Graph. Keine stillen Korrekturen.

**R-PHY und R-CLU – zwei unabhängige Reviewer**

- Andere Agenten als W-PHY/W-CLU; Review auf eingefrorenen Worker-Commits.
- Prüfen offizielles Kapitel/Anhang gegen Code **zeilen- und testfallbezogen**; falsche unbelegte Behauptungen über offizielle Gleichungen markieren.
- Je Review: PASS / REPAIRS_REQUIRED / BLOCKED_DATA; P0/P1/P2 mit reproduzierbarem Test, Codepfad und vorgeschlagenem minimalem Fix.
- Beanstandete Punkte im selben Makro durch zuständigen Worker beheben und erneut unabhängig prüfen; nicht als spätere unbestimmte „Micro-Aufgabe“ zurückgeben.

**Integration owner W-INT (kann ein Worker koordinieren)**

- Führe beide Ergebnisse in einen gemeinsamen Integrationsbranch, Commit-Freeze und Tests, erst nach unabhängigen Reviews.
- Kein Direkt-Merge auf main ohne projektspezifische Owner-Freigabe.
- Bereite stabile Ein-/Ausgangsobjekte für **M2-MA2** (globale x/c0-Fit- und Re-Clustering-Engine) vor.

## 4. Konkrete Acceptance Gates dieses Makros

**G01:** Daten-Provenienz, Einheiten, referenzielle Integrität, Jahr-/Zeitachsenkontrakt; unveränderte externe Wetterjahre; BLOCKED_DATA bei realem Quellmangel.  
**G02:** Offizielle CSV enthält 37 Einträge, Summe 102; für vollständigen europäischen Input jeweils k_c exakte Quoten und Country-Purity; nicht stillschweigend UK/Northern Ireland zusammenfassen.  
**G03:** alle Zonen AC-topologisch zusammenhängend; AC-Inseln und HVDC-Semantik explizit, keine künstlichen AC-Leitungen; grenzüberschreitende Zweige in gesamter Referenz enthalten.  
**G04:** Screening reproduziert bekannte 225/400-kV-MWh-Fixtures mit stundenabhängigen Grenzen, sommerlichen/winterlichen Zeitblöcken und separaten Jahresscores; keine Methode-B-Substitution.  
**G05:** orientierte Aggregationsoperatoren: A_z Γ=P A_d, f_cut=Γ f_detail, p_z=P p_detail, A_z f_cut=p_z und kontrollierte Nullbilanz je AC-Island.  
**G11-Teil:** transformatorische und steuerbare Betriebsmittelsemantik separat qualifiziert; wenn ein echter Input noch nicht unterstützt wird, ausdrücklich REJECTED_COMPONENT statt eines still unvollständigen Netzprodukts.  
**Regression:** bestehende 24 Python-Testfälle erneut ausführen und Ergebnis mit Baseline vergleichen; ergänzte Gate-Tests mit Artefakten und deterministischen Seeds ausführen. Keine neue erfolgreiche CI behaupten ohne Laufbeleg.

Die offiziellen IoSN-Fehlerklassen aus Abb. 13 sind **keine** MA1-PASS-Metrik; RMSE-Fit/Optimierungs-Review gehört in MA2. Vollständige Kapazitätsqualifikation gehört in MA3.

## 5. Verlangte Liefergegenstände

1. Produzierter Code auf dediziertem Branch mit nachvollziehbarem Commit, direkt referenzierbar für Folgechat/Worker.
2. Neue fokussierte synthetische Tests mit Fixturn-Expected-Values und Negative Cases; Testreport inklusive alten 24 Tests.
3. Vertragsschemas und Test-Fixtures für DetailedGridSnapshot, ReferenceDispatchSet, CountryZoneBudget, TimeSet und Normal/ContingencyRatings.
4. Maschinenlesbares Preflight-Ledger mit Modellgrößen, verbundenen AC-Inseln, Country-Mapping und Komponentenstatus.
5. *M2-MA1_EXECUTION_REPORT.md* mit Evidence-Tabelle: jede D/T/I/B-Regel, konkrete Codepfade, Testname, PASS/FAIL/BLOCKED.
6. Zwei unabhängige Reviewer-Berichte und dokumentierte Reparatur-/Re-Review-Schleife.
7. MA2-Übergabe (keine neue Planungsschleife): eingefrorene APIs, globales Referenzflow-Format, Busmap/Quota-Output, offene echte Datenblocker und reproduzierbare Commit-SHAs.

## 6. Definition of Done

Ein Ergebnis darf **MA1_SYNTHETIC_QUALIFIED** nur heißen, wenn die oben genannten algorithmischen G01–G05 und die unterstützten G11-Teiltests in CI/lokal reproduziert sind und R-PHY/R-CLU ohne offene P0 freigeben. Falls Transformator/HVDC/PST-Realinputs nicht verfügbar sind: die Fixture-Funktionalität darf qualifiziert sein, **REAL_QUALIFIED** bleibt BLOCKED_DATA. Kein vorgeblicher IoSN-Konformitäts-PASS durch einen 9-Bus-Test.

Abschlussbericht mit Branch, Commit, Testlogs, Review-Links und kurzem Handoff für M2-MA2 im selben Durchlauf veröffentlichen. Maximal interne parallele Worker und ihre unterschiedlichen Reviewer verwenden; Nutzer nicht um einzelne Mini-Aufgaben bitten.
