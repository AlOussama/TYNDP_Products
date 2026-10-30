# R-M0-CGMES-BACKEND-1 — Unabhängige Backend- und Reuse-Architekturbewertung

**Projekt:** IoSN / TYNDP / PyPSA, Modul 0  
**Stand:** 30.10.2026  
**Repository-Basis:** [1595d6d38e77804760612621657721b3699d2fea](https://github.com/AlOussama/TYNDP_Products/commit/1595d6d38e77804760612621657721b3699d2fea)  
**Untersuchung:** Statische Remote-Quellcode-, Dokumentations-, Testinventar- und Releaseprüfung; **keine Installation, keine Testausführung, keine produktive Implementierung**.  
**Disposition:** **CONDITIONAL_WITH_NAMED_GAPS** – primär **A (PowSyBl/PyPowSyBl)**, Fallback **B (VeraGrid)**; C ist keine wirtschaftliche gleichwertige Fallback-Architektur.

## 1. Executive Summary

1. **A ist der vorzuziehende Backend-Pfad.** PowSyBl/powsybl-core besitzt einen eigenständigen, aktiv fachlich gepflegten CGMES-Import/-Export-Stack für **2.4.15 und 3.0**, inklusive Node-Breaker-Topologie, Transformatoren, Phasenschiebern, HVDC, Boundary-Zuordnung, CGM-Subnetzwerken und explizitem **IGM-/CGM-Update-Export**. PyPowSyBl stellt bereits eine breite **pandas-DataFrame-Lese-/Änderungs-API** bereit. Fachliche CGMES-Commits vom **06. und 22.10.2026** sind belegt. [E1–E5]
2. **B ist der echte technische Fallback.** VeraGrid hält Parser, versionsspezifische CGMES-Objektmodelle, elektrische Modellkonvertierung und Serializer in Python bereit; beide Zielversionen können importiert und exportiert werden. Sein exportierbares **Profilregister ist nicht mit nachgewiesener verlustfreier Profilvollständigkeit gleichzusetzen**. Die tägliche Bearbeitung erfolgt im elektrischen MultiCircuit-Modell, das keine vollständige 1:1-CIM-Objektgraph-Ersatzdatenbank ist. Round-Trip-Tests existieren; der konkret geprüfte CGMES→CGMES-Test verwendet 2.4.15. [E6–E9]
3. **Keiner der beiden Pfade ist heute als verlustfreier CGMES↔PyPSA↔CGMES-Round-Trip qualifiziert.** Bei PowSyBl sind Standard-IGM-Exportprofile **EQ, TP, SSH, SV** dokumentiert, **nicht** das eigenständige Neuschreiben von EQBD/TPBD/GL. GL muss beim Import explizit aktiviert werden. Auch bei VeraGrid sind Provenienz und vollständige Modelltreue nach Bearbeitung noch zu demonstrieren. Die Original-CGMES-Lieferung und ihre Modellidentitäten müssen deshalb separat unverändert archiviert werden. [E2–E3, E6]
4. **SOPTIM Converter und Suite sind wertvolle Ergänzungen, aber kein Universalbackend.** Der Converter bildet CGMES nach PowerGridModel für Zustandsschätzung ab; HVDC wird mangels PGM-DC-Komponenten durch Lasten ersetzt. Die **separate** Suite orchestriert Fuseki, YAML, Konvertierung, Messungssimulation, State Estimation und **SV-Profil-Erzeugung**, aber keinen vollständigen EQ/TP/SSH-Ersatzexport. [E13–E16]
5. **Empfehlung zur Modulschnittstelle:** Originalpakete + Identitäts-/Profil-/Boundary-Ledger → externes CGMES-Backend → kanonische, versionierte Tabellen → verlustbehaftete, explizit deklarierte **PyPSA-Projektion**. Änderungen, die rückexportiert werden sollen, laufen über den Backend-Objektzustand, **nicht** durch eine unbelegte Rekonstruktion aus dem PyPSA-Netz. Ein **referenzierender Update-Export** (SSH/SV) ist von einem **elektrisch/strukturell neu aufgebauten Full-Export** strikt zu unterscheiden.

**Entscheidungsstatus:** Die Architekturpräferenz ist beweisgestützt, die Freigabe für einen produktiven, revisionssicheren EU-CGMES-Workflow jedoch **bedingt**, insbesondere wegen ID-/Boundary-/GL-Round-Trip, Transformator/PST/HVDC-Parametrisierung, Python-Zugriff auf Importmetadaten und nicht ausgeführten Realnetztests.

### 1.1 Verbindlicher Projektbezug

Geprüft am eingefrorenen Basiscommit: README.md, docs/REPOSITORY_AUDIT.md und docs/current/IOSN_2026_Band_II_PyPSA_Implementierung.md. Dort ist das Modul **network_adapter** bereits als PyPSA-Eingang zur detaillierten Netzreduktion konzipiert; die Verträge verlangen AC-Knoten, ursprüngliche Zweige/Transformatoren, Parameter/Basen, Status, HVDC/PST-Typen, Inseln, Grenzen, verlässliche IDs und Quellenmetadaten. Die reale PyPSA-Integration ist ausdrücklich **offen**. Modul 0 ist vorgelagert und darf die zwei nachfolgenden Clustering-/Äquivalenzstufen nicht umdefinieren. Wetterjahrauswahl und PACD/Zeitreihenaufbereitung gehören nicht in dieses Makro. Die späteren Projektarbeiten dürfen nicht mit einer bestätigten CGMES-Pipeline verwechselt werden. [P1–P3]

## 2. Evidenz- und Bewertungsregeln

- **D** = öffentlich dokumentierte API/Funktion, **C** = in Quellcode identifizierte Implementierung, **T** = vorhandene Tests (nicht hier ausgeführt), **M** = datierter fachlicher CGMES-Commit/Release, **P** = Architekturvorschlag, **U/UNKNOWN** = ohne passende Beweise.
- Eine vorhandene Klasse, ein Profilname oder ein Release **beweist nicht** fehlerfreie Verarbeitung eines vollständigen europäischen Datensatzes. Ein vorhandener Test **beweist nicht**, dass er hier oder in CI erfolgreich ausgeführt wurde.
- **Import (I)** und **Export (E)** werden getrennt betrachtet; ein **Update-Import** ist kein **Update-Export**. „Referenziert ein Boundary Set“ ist nicht „serialisiert dessen Profile neu“. „mRID im Arbeitsmodell“ ist nicht „sämtliche ursprünglichen RDF-Identitäten und Profildatensätze bleiben bei Round-Trip erhalten“.
- Wartungsevidenz bezieht sich ausdrücklich auf die **CGMES-Funktion**, nicht allein auf Aktivitäten der Entwicklerorganisation. Daten- und Testinventare sind keine aktuell bestandenen Konformitätsprüfungen.
- **Qualitative Gewichtung:** I/E 25 %, CGMES-Wartung 25 %, Python-/Tabellenschnittstelle 20 %, Provenienz/Round-Trip 15 %, Konfiguration 10 %, Lizenz/Integration 5 %. Keine künstlichen Gesamtpunkte: Wo Profile oder End-to-End-Ergebnisse fehlen, bleibt die entsprechende Teilbewertung **UNKNOWN**. Die erste Gewichtsklasse (70 % zusammen) dominiert die Priorisierung; Provenienzlücken sind zusätzlich **Ausschluss-/Abnahmegates**, nicht durch Punkte kompensierbar.

## 3. Vergleich aller Kandidaten

**Legende:** 2.4 = CGMES 2.4.15; 3 = CGMES 3.0; „bedingt“ = nachgewiesene Funktion mit expliziten Grenzen; „UNKNOWN“ = nicht überprüft/ausreichend belegt. Profilabdeckung und Update-Verhalten im folgenden Abschnitt präzisiert.

| Kandidat | Versionen | CGMES-I | CGMES-E | Update-Export | API/Mapping | Wartung CGMES, nachweisbar | Erstbewertung |
|:--|:--|:--|:--|:--|:--|:--|:--|
| **A PowSyBl + PyPowSyBl** | 2.4, 3 | D/C | D/C (EQ/TP/SSH/SV) | **Ja**, CGM SSH pro IGM + SV CGM | **pandas read/update**, Java-IIDM | **stark**, fachliche Commits 22.10.2026 | **primär** |
| **B VeraGrid** | 2.4, 3 | D/C | D/C, versionsabhängig | **UNKNOWN** für quelltreuen SSH/SV-Delta-Export | Python-CGMES-Objekte + MultiCircuit | fachlicher CGMES-Quellcode/Tests, 2026 fortgeführt; spezifische Regressionsergebnisse offen | **Fallback** |
| **C CIMpy** | 2.4 belegt; 3 nicht im gelieferten Runtime-Paket | C | C | UNKNOWN | generierter CIM-Objektgraph, eigene elektrische Abbildung nötig | **weniger aktuell**: letzte relevante Importkorrektur 13.08.2024; Release 09.03.2025 | Roh-CIM-Fallback, nicht Systembackend |
| **CIMgen (separat)** | Schemaquellen 2.4/3 | **kein Laufzeitimporter** | **kein elektrischer Exporter** | nein | Generator für Programmiersprachen/Klassen | aktive Generatorentwicklung 23.–28.10.2026; **keine Aussage zu CIMpy-Laufzeitpflege** | Hilfswerkzeug |
| **Alliander PyCGMES** | primär 3 | vollständiger RDF-Eingang UNKNOWN | C: profilgetrennter RDF/XML-Writer | UNKNOWN | Python-Dataclasses, Profilmetadaten, SHACL | generierte Modelle zuletzt fachlich 2025; CI/Schemas vorhanden | Schema-/Validierungshilfe |
| **PowerGridModel-IO** | CGMES nativ **nein** | **nein** | **nein** | nein | PGM JSON, pandapower, Excel/Tabellen | aktive PGM-IO-Releases 2026, **kein Beleg einer gewarteten CGMES-Schnittstelle** | PGM-Adapter, nicht CGMES-Backend |
| **SOPTIM cgmes2pgm_converter** | 2.4, 3 | C über SPARQL → PGM | kein CGMES-EQ/TP/SSH-E | nein | Python, PGM-Arrays/ID-Mapping | Transformator-/Netzformeländerungen 30.10.2025; Okt. 2026 Deprecation-Fix | Spezialadapter |
| **SOPTIM cgmes2pgm_suite** | via Converter 2.4, 3 | SPARQL-/Fuseki-Orchestrierung | **SV-Teilprofil**, nicht Full-CGMES | SV-Schreiben, kein allgemeiner Update-Export | YAML, Python, RDF/PGM | Konfig-/SV-Änderungen 30.10.2025; Okt. 2026 Deprecation-Fix | Ergänzung, separat |
| **pandapower CIM-Importer** | 2.4, 3 | D/C | kein entsprechender CGMES-E | nein | pandapowerNet/pandas | aktuelle CIM-Verzeichnisänderungen 2026, jüngst überwiegend Lint; fachliche Semantikregression UNKNOWN | Import-Vergleich |
| **PyPowSyBl↔pandapower** | über PowSyBl | **pandapower → PyPowSyBl** belegt | **Gegenrichtung UNKNOWN/nicht als API belegt** | nein | Python-Netzkonverter | pypowsybl-Tests vorhanden; Reverse-Issue offen | keine Rückexportbrücke |
| **Sparlectra.jl** | CGMES-Import 2.4, 3; Exportquelle explizit 2.4 | D/C | C (2.4; 3 UNKNOWN) | deterministische mRID-Ausgabe, kein eigener SSI/SV-Deltadienst belegt | Julia-Netzmodell, **nicht Python** | fachliche CGMES-Importcommits 19.–24.10.2026; Release 1.0.0 25.10.2026 | unabhängige Referenz |
| **SiennaSchemas** | **keine CGMES-Implementierung** | nein | nein | nein | JSON/OpenAPI, Python-/Julia-/SQL-Modellgeneratoren | lebhaftes Schema-Projekt 2026, aber **keine CGMES-Wartung** | evtl. Tabellen-/Units-Idee, nicht Parser |

**Quellen:** [E1–E23] sowie die jeweils verlinkten Source-/Release-Anker. Die Feindifferenzierung in „ja/bedingt/UNKNOWN“ ist wichtiger als eine pauschale Unterstützt-Flagge.

### 3.1 Strikte Profilabdeckung (Untersuchungsstand, nicht Konformitätszertifikat)

| Backend | EQ / TP / SSH / SV – Import | EQ / TP / SSH / SV – Export | EQBD / TPBD | GL | Schluss |
|:--|:--|:--|:--|:--|:--|
| **PowSyBl** | alle vier Kernprofile in der dokumentierten Importkonvertierung; auch separater EQ→SSH/TP/SV-Update-Import | alle vier als **separat wählbare IGM-Ausgabe**; CGM-Quick-Export nur SSH/SV | I: Boundary-Dateien, Tie-/Dangling-/Grenzreferenzen; E: **Abhängigkeiten/Referenzen**, kein allgemeines Neuerzeugen von Boundary-Profilen belegt | I: **optional** über cgmesGLImport-Postprozessor; E: GL **nicht** in dokumentierter Liste | **bedingt** |
| **VeraGrid 2.4** | Parser + CGMES-Circuit/elektrische Konvertierung | Profilregister **EQ, SSH, TP, SV, GL** | Boundary-Input unterstützt; **2.4-EQBD/TPBD-Neuschreiben nicht im 2.4-Exportregister** | I/E dokumentiert/registriert | **bedingt** |
| **VeraGrid 3.0** | parsergestützt, eigener CGMES-v3-Assetbaum | Register u. a. **EQ, EQ_BD, TP, TP_BD, SSH, SV, GL** + weitere NCP-Profile | Import und Ausgabeprofile vorhanden; vollständige Serialisierungs-/Beziehungssemantik **UNKNOWN** | I/E-Register | **bedingt** |
| **CIMpy 2.4** | XML-Import mit Profilattributen; EQ_BD/TP_BD im CGMESProfile | XML-Export mit Profilzuordnung | Klassen/Profilmetadaten nachweisbar, korrekter vollständiger Round-Trip **UNKNOWN** | Profilschema vorhanden; Vollständigkeit UNKNOWN | **bedingt** |
| **CIMgen / PyCGMES** | Schema- und Objektmodell, kein qualifizierter elektrischer CGMES→Netzimport | PyCGMES hat Writer für CGMES 3; CIMgen generiert Klassen | PyCGMES Profildefinitionen vorhanden | PyCGMES Profildefinitionen vorhanden | keine vollständige Import-/Exportpipeline |
| **pandapower CIM** | 2.4/3 → pandapowerNet | kein entsprechender CGMES-Exporter | Parser liest Teilmodelle; Erhaltung der gesamten Boundary-Graph-Semantik **UNKNOWN** | Parser/Netzattributqualität je Profil UNKNOWN | Einweg |
| **SOPTIM Converter/Suite** | SPARQL-Datensicht; konvertiert benötigte elektrische Objekte in PGM | **nur Suite-SV** aus Ergebnissen belegbar | Ressourcenzugriff möglich; vollständiger Boundary-Graph/Full-Export **nicht belegt** | kein umfassender GL-Round-Trip belegt | spezialisiert |
| **Sparlectra.jl** | 2.4/3 (Readme, Importcode, Testinventar) | 2.4 im Exportcode (EQ/TP/SSH/SV); 3 **UNKNOWN** | Import unterstützt Boundary Sets; Full-Boundary-Writer UNKNOWN | UNKNOWN | alternative unabhängige Referenz |

**Achtung:** Eine Liste „exportierbare Profile“ ist ein Serializer-/Schemaindikator. Bei komplexen v3-NCP-Profilen sind Instanzvollständigkeit und inhaltliche Konsistenz ohne Testevidenz UNKNOWN. Ebenso darf nicht behauptet werden, dass PowSyBl die bei Import möglichen Metadaten automatisch in PyPowSyBl-DataFrames ausliefert.

## 4. Technische Detailbefunde und tatsächlich wiederverwendbare APIs

### 4.1 A — PowSyBl/powsybl-core und PyPowSyBl

**D/C: Importarchitektur.** CGMES XML/RDF wird von powsybl-core in einen **RDF4J-Triplestore** eingelesen und über SPARQL zu **IIDM** konvertiert. Import unterstützt Node/Breaker (als IIDM Node/Breaker) und Bus/Branch (als Bus/Breaker); die Geräte-/Topologiebeschreibung umfasst 2W/3W-Transformatoren, TapChanger/PST, Switches, Shunts, AC/DC-Konverter, reduziertes und optional detailliertes DC-Modell, Limits und Boundary/Dangling Lines. CGM kann nach **Modelling Authority** in IIDM-Subnetzwerke eingelesen werden. [E1, E2]

**D/C: Export.** Standard-IGM-EQ/TP/SSH/SV-Export in **CGMES 2.4.15 (CIM16)** oder **3.0 (CIM100)**; Equipment wird beim Export stets in **Node/Breaker-Detailtiefe** erzeugt, selbst wenn das interne Netz anders modelliert ist. Header/Dependencies stammen aus Import-Metadaten oder Exportparametern. **CGM-Quick-Export** schreibt aktualisierte **SSH je IGM und ein gemeinsames SV**, mit Dependency-/Supersedes-Beziehungen zu originalen EQ/TP/Boundary-IDs. Das ist **kein allgemeiner Patch-Exporter für beliebige EQ-Strukturänderungen**. [E3]

**D/C: Python.** In PyPowSyBl u. a. pypowsybl.network.load(...), Network.update_from_file(...), Network.get_generators/loads/lines/2_windings_transformers/3_windings_transformers/phase_tap_changers/hvdc_lines/terminals/aliases(), Network.update_loads(...), Network.save(..., format="CGMES", parameters=...). Import, Export und Netzänderungen müssen auf **derselben** Backend-Version erfolgen; Core/Python-Versionen zusammen pinnen. [E4, E5]

**Identitäts-/Speicheroptionen (entscheidend):**
- Import-IDs per iidm.import.cgmes.source-for-iidm-id = mRID (Default); rdfID ist Alternative. **Nicht** Namen als Identität verwenden.
- iidm.import.cgmes.remove-properties-and-aliases-after-import = false für spätere Updates und Terminal-ID-Aliase; true zerstört die nötige Update-Herkunft.
- iidm.import.cgmes.cgm-with-subnetworks = true und ...defined-by = MODELING_AUTHORITY, um Modellbesitz zu erhalten.
- iidm.import.cgmes.post-processors = cgmesGLImport, **wenn GL/Geokoordinaten benötigt werden**; per Default wird GL nicht auf Netzkoordinaten abgebildet.
- iidm.import.cgmes.store-cgmes-model-as-network-extension ist in der **aktuellen** Core-Dokumentation **standardmäßig false**. Optional true behält den Triplestore, erhöht Speicherbedarf und verlangt explizite Lebenszyklusbehandlung. Die Java-Extension ist **nicht** als stabile Python-Provenienz-API nachgewiesen. Auch ...store-cgmes-conversion-context-as-network-extension ist standardmäßig false.
- iidm.import.cgmes.use-detailed-dc-model = false per Default; für DC-Detailevidenz optional true, die PyPSA-Abbildung bleibt separat zu spezifizieren.
- ...use-previous-values-during-update = true kann partielle aufeinanderfolgende SSH-Änderungen vervollständigen; **SV wird als vollständiger Satz behandelt, nicht partiell**. [E2, E4]

**Wartungsbeweis, nicht nur Organisation:** powsybl-core CGMES-Pfad: **8a18567** (22.10.2026, ID-Optionen auf Update anwenden), **aec82b1** (22.10., Ratio-Tap-Regelung exportieren), **b1ff9dd** und **a81fa63** (06.10., Spannungsregelungsupdate/Generatorregulierung). Releases v7.4.0 (15.10.2026) und v7.4.2 (23.10.2026). In Release Notes finden sich zusätzlich spezielle CGMES Import-/Update-/Exportkorrekturen und Regressionstests. Dies ist die belastbarste nachgewiesene Wartung der Schnittstelle im Vergleich. [E5]

**Restlücken A:** GL-Eigenexport nicht dokumentiert; EQBD/TPBD werden referenziert, nicht generell neu gebaut; Core-CIM-Typkonvertierung ist nicht automatisch semantisch bijektiv; Terminal- und FullModel-/ModellingAuthority-Details sind nur teils über die Python-API nachweisbar; erhaltener Rohtriplestore in Java und ein PyPSA-DataFrame ergeben keine automatische Round-Trip-Garantie. Java-/Native-Laufzeit und großer Triplestore sind Integrationsrisiken.

### 4.2 B — VeraGrid

**D/C:** Parser **CgmesDataParser** mit Versionserkennung, versionsspezifische Objektbäume **cgmes_v2_4_15** und **cgmes_v3_0_0**, **CgmesCircuit**, elektrische Überführung nach **MultiCircuit**, **CimExporter** sowie **save_cgmes_file**. Dateien können als XML, ZIP, gemischte Liste und Boundary-ZIP gelesen werden. Python-API erlaubt Zugriff auf ursprüngliche Klassenobjekte vor elektrischer Konvertierung. Der Exporter hat für 2.4 nur EQ/SSH/TP/SV/GL und für 3.0 zusätzlich EQ_BD/TP_BD sowie zahlreiche NCP-Profilregister. [E6, E7]

**T:** Unter src/tests/FileFormats/CGMES befinden sich Parser-, Netzkomponenten-, v3-CAS-Import-/Power-Flow- und Round-Trip-Testdateien. Konkret zeigt test_cgmes_roundtrip_cgmes_to_cgmes.py die Einstellung **CGMESVersions.v2_4_15**; test_cgmes_cas_v3_load.py prüft das Laden von v3-Datensätzen, nicht automatisch den vollständigen v3-Round-Trip. Keine Testläufe hier. [E8]

**M mit Vorbehalt:** Der CIM-Ordner wurde 22.10.2026 unter Commit **54aac3a** mit Release-Version 6.7.20 verändert; die Commitnachricht ist **nur** eine Versionskennung. Das belegt Aktualisierung des Codes, nicht die Semantik jeder CGMES-Klasse. Tests/Quellcode und vorhandene 2026-Versionen sind positive Strukturindikatoren; eine mit PowSyBl vergleichbare Liste datierter fachlicher CGMES-Bugfixes wurde in dieser Untersuchung **nicht** hinreichend nachgewiesen. [E9]

**Risiken:** Die originäre CIM-Objektbeziehung ist nach Konvertierung zu MultiCircuit nicht 1:1 als editierbarer Gegenpart garantiert. Export kann neue IDs/Assets konstruieren. Boundary Set ist im typischen Exportworkflow nötig. Umfangreiche v3-Exportregistrierungen sind kein Zertifikat für alle enthaltenen Felder. Eine direkte robuste pandas-Vertragsoberfläche wie PyPowSyBl ist hier nicht der vorrangige CGMES-API-Typ. Der eigene PyPSA-Adapter bleibt erforderlich.

### 4.3 C — CIMpy und CIMgen als Roh-CIM-Schicht

**CIMpy C:** cimpy/cimimport.py importiert über cim_import(xml_files, cgmes_version, ...); cimpy/cimexport.py sortiert serialisierte Klassen/Attribute nach Profilen. Die Runtime importiert explizit **cimpy.cgmes_v2_4_15.CGMESProfile**; dieser enthält EQ_BD/TP_BD/GL. Tests mit CIGRE-MV-Datensätzen und Exporttests sind vorhanden, die 3.0-Runtime ist in diesem Repo **nicht** nachgewiesen. 13.08.2024 gab es einen fachlichen Fix zur Boundary-Profilzuordnung; letzte hier gefundene Importdateiänderung 16.02.2025 war Pre-commit-Hygiene; Release v1.2.0 09.03.2025. [E10, E11]

**CIMgen C:** Generator mit Schemaverzeichnissen für **CGMES 2.4.13, 2.4.15 und 3.0.0** und mehreren Zielsprache-Backends. Fachliche Codegenerator-Änderungen 23.–28.10.2026; **nicht** gleichbedeutend mit aktualisiertem CIMpy-Importer/Exporter. Er kann Klassen liefern, aber weder AC/DC-Topologie noch Transformator-/PST-/HVDC-Mapping oder Round-Trip in PyPSA abnehmen. [E12]

**Konsequenz:** Als Primärpfad wäre C eine weitgehende Eigenentwicklung des elektrischen Mappings und der Rückkonvertierung; das widerspricht dem Wiederverwendungsziel. Als gezielter *schema-level diagnostic fallback* ist C sinnvoll, nicht als zweites vollständiges elektrisches Backend.

### 4.4 Alliander PyCGMES

**D/C:** Python-Dataclasses und Profilmetadaten für **CGMES 3**, Schema-/SHACL-Artefakte; in pycgmes/utils/chevron_writer.py ein **ChevronWriter.write/generate** für profilgetrennte RDF/XML-Ausgabe; die Base-Klasse verwaltet Profilattribute und mRID. Tatsächlicher generischer Import vollständiger XML/RDF-Lieferungen inkl. EQ/TP/SSH/SV/Boundary in einen editierbaren elektrischen Netzgraphen ist **UNKNOWN** und darf nicht aus dem Paketnamen abgeleitet werden. [E17]

**M:** generierte CGMES-Modelle/fachliche Veränderungen zuletzt im März 2025 gefunden, Repo-HEAD Sept. 2025 (Security-Dokumentation); aktueller 3.0-Profil-/SHACL-Wert bleibt nützlich, aber nicht als autonom gepflegter bilateraler CGMES-Backend-Stack qualifiziert.

### 4.5 PowerGridModel-IO

**C:** Der Converter-Index unter src/power_grid_model_io/converters/__init__.py exportiert **PandaPowerConverter, PgmJsonConverter, VisionExcelConverter**; die pandas-basierte PandapowerConverter-Implementierung ist bidirektional zwischen **PGM und pandapower**, nicht CGMES↔CGMES. Ein offenes Repository-Issue **#207** fordert „CGMES conversion to PGM“ (Stand dieser Prüfung). **Release v2.0.36 vom 27.10.2026** und viele aktuelle Dependency-Commits belegen Pflege von PGM-IO, **nicht** der noch fehlenden CGMES-Funktion. [E18]

**Nutzung:** Möglicher PGM-/pandapower-Vergleich oder ergänzende Table-/Dataset-Validierung, keine Auswahl als Modul-0-Parser/Serializer.

### 4.6 SOPTIM cgmes2pgm_converter (eigenständig)

**D/C:** Liest CGMES 2.4/CIM16 und 3.0/CIM100 über **SPARQL** aus einem bereits bereitgestellten RDF-Triplestore; CgmesDataset, CgmesToPgmConverter.convert() ergeben PGM-Inputdatensatz plus **ExtraInfo** als Identitätszuordnung. Unterstützt mehrere 2W/3W-Trafo-/TapChanger-Typen, Strom-/Leistungsmessungen, Erzeuger/Lasten, Shunts. **Wichtig:** DC-Komponenten wie CsConverter/VsConverter werden wegen fehlender PGM-DC-Komponenten **durch Loads ersetzt**. Damit sind relevante HVDC-Regel- und Portinformationen für den symmetrischen europäischen Übertragungsnetzvertrag **nicht verlustfrei verfügbar**. [E13, E14]

**M:** 30.10.2025 fachliche Änderungen an Trafoformeln/Links; 14.10.2026 Quellcode-Fix für Deprecation-Warnungen, Release **v0.4.5 15.10.2026**. Keine Gleichsetzung von Paketrelease mit neuem CGMES-Profilnachweis. Apache-2.0. Kein allgemeiner CGMES-Full-Exporter.

### 4.7 SOPTIM cgmes2pgm_suite (separat!)

**D/C:** Eigenes Paket mit Python-Kommando **python -m cgmes2pgm_suite --config ...**, YAML-Konfiguration, Docker/Apache-Jena-Fuseki-Management, RDF/XML-ZIP-/Verzeichnisimport, SPARQL, Messungssimulation (SV→Operation), Zustandsschätzung, Text-/Excel-Ausgaben und **SvProfileBuilder**. SvProfileBuilder.build() schreibt **SvVoltage** und **SvPowerFlow** mithilfe von PGM-Ergebnissen und aus ExtraInfo rekonstruierter Terminalreferenz. [E15, E16]

**T:** Das README beschreibt Integrationstests mit ENTSO-E-CAS-Datensätzen (u. a. PST, 167-Knoten SmallGrid, ca. 6k-Knoten RealGrid) und nennt dort bereits unterschiedliche Konvergenz-/Vollständigkeitsfälle. Dies sind **projektseitig dokumentierte Tests**, nicht in diesem Makro reproduziert. Einige Tests benötigen einen Fuseki-Dockercontainer. **SV-Export ist nicht FullModel-Neubau für EQ/TP/SSH/EQBD/TPBD/GL.**

**M:** fachliche Konfig-/SV-/Query-Änderungen 30.10.2025; 14.10.2026 Deprecation-Warnungen; Release v0.4.5 15.10.2026. Der Suite-Einsatz würde neben Python/Docker auch Fuseki/SPARQL und PGM-Resultatkonventionen einführen. Für Modul 0 höchstens **optional** als unabhängiger SV-/Zustandsschätzungsdiagnostikpfad; keine verpflichtende Abhängigkeit.

### 4.8 pandapower CIM-Importer und PyPowSyBl-Konverter

**D/C:** pandapower.converter.cim.cim2pp.from_cim.from_cim(..., cgmes_version="2.4.15") akzeptiert 2.4.15 und 3.0 und erzeugt **pandapowerNet**; zusätzliche konfigurierbare Converter-Klassen/Reparaturschritte. Es gibt **keinen entsprechend dokumentierten bidirektionalen CGMES-Exporter**. Zuletzt 29.10.2026 Dateipflege, vor allem Importorganisation/Lint; jüngste fachliche CGMES-Regressionsnachweise nicht gesichert. [E19]

**C:** pypowsybl.network.convert_from_pandapower(pandapowerNet) mit tests/test_pandapower.py vorhanden. Die Gegenrichtung PyPowSyBl→pandapower ist **nicht als stabile Funktion belegt**; Issue powsybl/pypowsybl#895 (Stand 30.10.2026: offen). Ein Pfad CGMES→pandapower→PyPowSyBl→CGMES trägt zusätzliche irreversible Mappings und ist nicht vorzuziehen. [E20]

### 4.9 Sparlectra.jl und SiennaSchemas

**Sparlectra.jl D/C/T:** Julia-Referenz mit CGMES-Eingang für 2.4.15 und 3.0, Boundary-/Multi-Area-Behandlung und SV-Vergleich laut README; Implementierung unter src/adapters/cgmes. **cgmes_export.jl beschreibt explizit einen CGMES-2.4.15-EQ/TP/SSH/SV-Exporter**, mit ursprünglichen mRIDs wo vorhanden und deterministischer UUID5 für neue Objekte. Ein vollwertiger **3.0-Export** ist durch diese Codequelle nicht belegt. Fachliche CGMES-Änderungen 19.–24.10.2026; Release v1.0.0 25.10.2026; Testdateien für CGMES-Import und Export vorhanden. Wertvoll als **unabhängiger Implementierungs- und SV-Vergleich**, aber Julia-Runtime, abweichendes Netzmodell und keine direkte pandas-API verhindern einfachen Einsatz als Modul-0-Backend. [E21, E22]

**SiennaSchemas D:** versionierte, noch **pre-1.0**-JSON/OpenAPI-Schemata für domänenübergreifende Stromnetzmodelle; erzeugt separate Python-/Julia-/SQL-Datenmodelle. **Kein IEC-CGMES-RDF/XML-Importer/-Exporter, keine CGMES-Profilkonformität.** Allenfalls konzeptionell wertvoll für Einheiten, Schemakatalog und Provenienzattribute – keine Ersatzbibliothek für CIM. [E23]

## 5. Gewichtete Architekturqualifikation

Die vorgeschlagenen Gewichte werden als **Entscheidungsprioritäten**, nicht als unbelegte numerische Maturitätsscores eingesetzt. Der Vergleich ist nach fachlicher Evidenz gegliedert:

| Dimension | Gewicht | A PowSyBl/PyPowSyBl | B VeraGrid | C CIMpy/CIMgen |
|:--|--:|:--|:--|:--|
| **CGMES Import/Export** | **25 %** | **führend**: beide Versionen, spezifizierter CGM-SSH/SV-Update-Export; GL/Boundary-Full-Export-Lücken | **stark/bedingt**: beide Versionen, v3-Profilregister; Delta-Update UNKNOWN | **lückenhaft**: CIMpy-2.4 Runtime; 3.0 nur Codegen belegt, elektrisches Mapping fehlt |
| **CGMES-spezifische Wartung** | **25 %** | **führend**: mehrere fachliche Import-/Export-/Update-Fixes Oktober 2026 | **bedingt**: neue CIM-Codeversion 2026 + Testinventar, spezifisches fachliches Änderungsdelta schwächer belegt | **schwach/mischt Ebenen**: CIMpy CGMES-Runtime älter, CIMgen-Generator aktuell |
| **Python/tabellarische API** | **20 %** | **führend**: DataFrames für Netzassets, Terminals, Limits, Taps, Edit-API | **geeignet**: direktes Python-CIM-Objektmodell, jedoch eigener Adapter auf MultiCircuit/Tabellen | **geeignet nur roh**: editierbare CIM-Objekte, elektrischer Mapping-Stack fehlt |
| **Provenienz/Round-Trip** | **15 %** | **bedingt**: IDs/Aliase/Metadaten und IGM/CGM-Update, Vollständigkeit UNKNOWN | **bedingt**: CGMES-Objekte + 2.4-Round-Trip-Test; durch MultiCircuit 1:1-Erhalt UNKNOWN | **bedingt**: Profilattribute und mRIDs, aber 3.0/Energieobjekt-Round-Trip UNKNOWN |
| **Konfigurierbarkeit** | **10 %** | **hoch**: Import-/Exportparameter, Namensstrategien, Extension/Postprozessoren | **hoch/bedingt**: Parser-/Exporter-Optionen, eigener API-Eingriff | **hoch auf Schemaebene**, zusätzlicher eigener elektrischer Code nötig |
| **Lizenz/Integration** | **5 %** | **MPL-2.0**, Java/Native-Komponenten und RDF4J | **MPL-2.0**, Python-Stack mit Netz-/GUI-Paketabhängigkeiten | **Apache-2.0**, jedoch hoher selbst zu pflegender Implementierungsumfang |
| **Gesamtscore** | **100 %** | **UNKNOWN** bis unabhängige Ziel-Datensatzgates | **UNKNOWN** bis unabhängige Ziel-Datensatzgates | **UNKNOWN** (unvollständiger Zielpfad) |

**Begründete Reihung A > B > C:** A vereint belegten CGMES-**Update-Export**, 2026er **CGMES-fachliche Wartung** und breite **DataFrame-API** in den drei am höchsten gewichteten Dimensionen (70 %). B bietet native Python-Objekte und einen aktiven Serializer, aber kein gleichermaßen belegtes Subnetwork-/Dependency-Update-Verhalten; C zieht die größte Eigenimplementierung nach sich. Der Rang ist **Architekturpräferenz**, keine nachgewiesene Konformitäts- oder Performancewertung.

## 6. Architekturvarianten und Systemgrenzen

### 6.1 Verbindlicher gemeinsamer Datenfluss (P)

    CGMES 2.4.15 / 3.0 EQ, TP, SSH, SV, EQBD, TPBD, GL
               + Modellautoritäten + originales Boundary Set
                           |
             [Unveränderlicher Originalspeicher]
               Hashes, Dateien, Profile, Zeitbezug
                           |
               [Extern gepflegtes CGMES-Backend]
           A: PowSyBl IIDM  |  B: VeraGrid CGMES/MultiCircuit
                           |
              [Modul-0-Normalisierungs-/QA-Schicht]
          Identität / Topologie / Einheiten / Betriebsmittel
                           |
          +----------------+-----------------------+
          |                                        |
    [Kanonische Tabellen]                  [Backend/CGMES-State]
    plus Provenienz-Ledger                  plus Originalmanifest
          |                                        |
     [PyPSA-Projektion]                    [Export-Gate]
      nur geeignete Sicht                      |          |
          |                               SSH/SV-Update   Full-EQ/TP/SSH/SV
     Modul 1 und folgende                Originalreferenz  Strukturprüfung
     (unverändert im Scope)              erforderlich       erforderlich

**P: Strenge Zwei-Sichten-Regel.** PyPSA ist das elektrische Simulations-/Planungsmodell, **nicht** die rückexportfähige vollständige CIM-Datenbank. Ein durch Bus-Clustering reduziertes PyPSA-Modell kann nicht ohne neue Identitäts-/Topology-Entscheidungen als dasselbe originale CGMES-Liefermodell ausgegeben werden. „CGMES-konformer Rückexport“ muss sich auf **explizit definierte, zulässige Änderungen am Detailed Model** beziehen; Rückexport eines **reduzierten** Netzes ist ein gesondertes, hier nicht freigegebenes Produkt.

### 6.2 Variante A — PowSyBl/PyPowSyBl + Tabellenadapter

**Direkt wiederverwenden (D/C):** CGMES-Parser/RDF4J, Profilinterpretation, Node-Breaker, Topologie, Transformer/PST/HVDC-Modelle, CGM/Subnetwork, ID/Alias-System, DataFrame-Read-/Update-API, IGM-/CGM-Exporter inkl. SSH/SV-Updates.

**Eigene Komponenten (P):**
- klein gehaltene Python-Adapterklassen für Normalisierung nach tabellarischem Zielvertrag; ausschließlich benötigte elektrische Felder und eindeutig dokumentierte semantische Verluste.
- ein Provenienz-Ledger für **(CGMES mRID, rdfID, Terminal, profile, source model, ModellingAuthority, Boundary-Referenz) → IIDM-ID → Tabellen-ID → PyPSA-ID**; Einträge mit NULL/UNKNOWN statt generierten IDs ohne Kennzeichnung.
- PST-/HVDC-/Transformator-Repräsentationspolicies und Einheitenkonvertierung mit rückverfolgbarem Parameterursprung.
- gesperrter Export-Gate: direkt aus dem persistenten IIDM-Netz unter Erhalt des Originalmanifests, nicht aus einer nachträglich interpretierten PyPSA-Kopie.

**Plus:** technisch breiter, gut gewarteter CGMES-Stack, direktes pandas, wenig XML-/CIM-Eigencode. **Minus:** Java/Graal/native Packaging, RDF4J-/Speicherlebenszyklus, GL-Postprozessor und nicht vollumfängliche Python-Provenienzsicht, Exportprofile-Limit.

### 6.3 Variante B — VeraGrid CGMES + eigener Tabellenadapter

**Direkt wiederverwenden:** 2.4/3 Parser, Raw-CIM-Objekte und Referenzen, geometrische/elektrische Übersetzung, MultiCircuit, Full-CGMES-Serializer und Profilregister.

**Eigene Komponenten:** identisches Tabellen-/Provenienz-/PyPSA-Vertragsmodul wie A, zusätzlich bewusste Speicherung des **originalen CGMES-Objektgraphs** neben MultiCircuit; Diff-/Rückübertragungsmechanismus der explizit änderbaren Attribute; fachliche Export- und v3-Round-Trip-Gates. **Plus:** Python-native CGMES-Objekte, vielfältige Parser-/Exporter-Extension-Points. **Minus:** höheres Mapping-Risiko zwischen Rohobjekten/MultiCircuit, weniger tabellarische Standard-API, Delta-Update/FullModel-Beziehungen noch UNKNOWN.

### 6.4 Variante C — CIMpy/CIMgen und eigener elektrischer Mapper

**Direkt wiederverwenden:** XML/RDF-Objekte, Profilzuordnungen, Klassen-/Schema-Codegenerierung, Serialisierungsansätze. **Selbst zu bauen:** vollwertige Node-Breaker-/TP-Auflösung, 2W/3W-/PST-/HVDC-Netzabbildung und Verlust-/Limits-/Boundary-Handling, Konsistenzkontrolle, PyPSA-Kopplung, Modellautoritäts- und Update-Exportregeln, Regressionstests für 2.4 und 3.0.

**Plus:** maximale CIM-Kontrolle und Apache-2.0. **Minus:** größter fachlicher Wartungsaufwand bei jeder Standardänderung und höchstes Risiko semantischer Abweichungen. **Nicht empfohlen** als produktiver Fallback.

### 6.5 SOPTIM-/PGM-Ergänzung

**P:** Die SOPTIM-Suite darf **optional** zur unabhängigen Zustandsschätzungs-/SV-Plausibilisierung auf separater Kopie desselben CGMES-Datensatzes laufen. PowerGridModel-IO kann optional bei PGM-/pandapower-Vergleichen helfen. **Nicht** als Vorstufe für alle Moduldaten, weil Converter/DC-Ersatzmodell, SPARQL/Fuseki und PGM-Tabellen nicht den identitätstreuen vollständigen Rückexport bieten. Kein Parser-Fork von SOPTIM; keine CGMES-Doppellogik im PyPSA-Core.

## 7. Minimaler Modul-0-Tabellen- und Provenienzvertrag (P)

Jede technische Tabelle erhält ein internes stabiles **source_key** und – soweit vorhanden – **cgmes_mrid**; keine Ableitung von Identitäten aus freiem Namen oder Geo. Originalobjekt, elektrisches Rechenobjekt und PyPSA-Bus dürfen nicht stillschweigend dieselbe ID erhalten.

| Tabelle / Ledger | Pflichtfelder / Beziehungen |
|:--|:--|
| **delivery_manifest** | delivery_hash, original ZIP/XML hashes, cgmes_version, source URI, profile, FullModel rdfID/version/created/scenarioTime/ModellingAuthority, dependsOn/supersedes, boundary-set hashes |
| **cim_identity** | cim_class, mRID, rdfID, original_profile(s), source_file, modeling_authority, backend_id, generated_flag, alias_type, cross-model ownership |
| **topology_nodes / connectivity_nodes / switches** | original IDs, voltage level, busbar/cnodes, terminal links, active/open state, topological-node assignment, topology_kind |
| **terminals** | Terminal mRID/rdfID, ConductingEquipment-Referenz, ConnectivityNode/TopologicalNode, sequenceNumber, connected status, boundary-side |
| **buses / substations / areas** | backend/topological IDs, v_nom, AC-Island, country, nominal voltage, coordinate source/projection, provenance/conflict flag |
| **lines / transformers / taps** | original per-unit/physical r,x,b,g; Basen, 2-/3-W-Kopplung, Side/End, winding/terminal refs, PST angle/phase tap, ratio/step limits |
| **hvdc / converters** | Konverter-/DC-Line-IDs und Terminals, Typ (LCC/VSC), DC-Topologie, P/Q-/Spannungsregelung soweit im Modell, Verluste, Projektionspolicy |
| **injections / shunts / limits** | Generator/Load/Shunt IDs und Bus-/Terminalanschluss, P/Q/Regime/Status; Strom-/MVA-Limits und Zeit-/Richtungsbasis |
| **pypsa_mapping** | source_key, component class, pypsa_component, pypsa_id, conversion rule, dropped_fields, approximation, no_roundtrip_flag |
| **change_ledger** | old/new value, unit, changed_field, provenance, edit_kind (SSH/SV/structural), authorization, expected export profiles |

**Einheitengate:** Kein stiller Import von Prozentwerten/Ohm/kV/MW in per-unit ohne dokumentierte Ausgangsbasis und Transformator-/Konverter-Side-Definition. Country-Clusterung wird erst in späteren Modulen umgesetzt; die Original-Landes-/Grenzreferenzen müssen in M0 intakt bleiben. Geokoordinaten über GL sind **optional vorhanden, nicht garantiert**; fehlende Geometrie ist als Datenlücke auszuweisen, nicht künstlich aus Bus-IDs abzuleiten.

## 8. Getrennte Import-, Update- und Full-Export-Policy (P)

| Operation | Zugelassener Grundpfad | Nicht stillschweigend behaupten |
|:--|:--|:--|
| **Erstimport** | Originaldateien/Boundary vollständig inventarisieren, extern importieren, ID-/Profil-Ledger füllen, Tabellen projizieren | dass ein fehlerfreier Parse alle Originalfelder erhält |
| **Update-Import** | dieselbe Backend-Instanz, partielle SSH gemäß Core-Updatekonvention, SV nur als kompletten Satz behandeln | dass ein EQ-Update durch dieselbe API zulässig ist |
| **SSH/SV-Update-Export** | primär PowSyBl CGM-Quick-Export mit IGM-Subnetzwerken/Dependencies; exportierte SSH/SV verweisen auf unveränderte ursprüngliche EQ/TP/Boundary-Modelle | dass EQ/TP/EQBD/TPBD/GL mitgeschrieben wurden |
| **Full-Export** | externes PowSyBl-/VeraGrid-Serializer-API, ausdrücklich ausgewählte Profile, neue FullModel-Dependency-/Versionierungsprüfung | verlustfreie Übernahme aller CIM-Extensions/GL/Boundary-Objekte |
| **Strukturänderung** | zunächst blockieren; separate wissenschaftliche/technische Entscheidung für ID- und Endtopologie-Abgleich | exaktes Round-Trip aller Terminals und mRIDs nach Aggregation |
| **Reduziertes PyPSA-Netz** | eigenes abgeleitetes Modell, Provenienz zu Originalnetz; KEIN impliziter CGMES-Rückexport | identischer Modellautoritäts-/Boundary-Kontext |

## 9. Unausgeführte Qualifikations- und Akzeptanzgates

Diese Gates sind **Anforderungen an den späteren Implementierungsauftrag**, keine in diesem Makro ausgeführten Testläufe.

| Gate | Zu beweisende Eigenschaft | Daten / Fail-Bedingung |
|:--|:--|:--|
| **G0** | Fixierte Versionen + Dependency-/Licensing-BOM, reproduzierbare API-Konfiguration | PowSyBl-Core↔PyPowSyBl-Version-Pin, VeraGrid-Pin, Parser-/Java-/Speicherlimits |
| **G1** | CGMES 2.4.15 **und** 3.0, jeweils Full-EQ/TP/SSH/SV + GL + EQBD/TPBD; definierter Fall ohne GL | Profilinventar/FullModel-/Boundary-Querverweise, Fail bei referenzierten fehlenden Objekten |
| **G2** | Node-Breaker-/TP-Korrektheit, AC-Inseln und mRID-/Terminal-/ModellingAuthority-Bijection soweit physikalisch möglich | Geräte-/Terminalzählung, Status, Boundary-Endpunkte, keine stillen merges |
| **G3** | 2W/3W/PST/ratio tap, Shunt, Generator/Load, Converter/HVDC; elektrische Parameter/Seiten/Einheiten | numerisch/semantisch unabhängige Vergleichstabelle, Fail bei undeklarierter Approximation |
| **G4** | **Export geteilt prüfen**: (i) SSH/SV-Update mit unverändertem EQ/TP/Boundary, (ii) Full-EQ/TP/SSH/SV-Ausgabe; mRID/FullModel/Dependencies/GL-Checks | Externe Re-Importprüfung, Referenzauflösung; keinen 1:1-Gesamt-Round-Trip vorwegnehmen |
| **G5** | Vollständig und zeit-/länderübergreifend PyPSA-kompatible projektionierte Netztabellen | energiebilanzierte AC-Inseln, HVDC-Terminalleistung/Verluste, PST-Wirkung und Status; keine Geofiktion |
| **G6** | Performanz und Speicher auf repräsentativem europäischen Multi-IGM-Datensatz, auch ca. 6k+ Busse | peak RAM, Import-/Exportdauer, JVM/Triplestore-Lebenszyklus, keine behaupteten Benchmarks |

**Akzeptanzformel:** „Backend ausgewählt“ ≠ „CGMES zertifiziert“. Architektur darf vor G0–G6 spezifiziert werden, produktive Freigabe erst nach den je Version und Profileinsatz relevanten Gates.

## 10. Risiko- und Nachweisregister

| ID | Risiko / offener Nachweis | Bedeutung | Behandlung |
|:--|:--|:--|:--|
| **R-01** | mRID/rdfID/Terminal-Aliase und FullModel-Metadaten nicht durchgehend über **Python** zugänglich | hoher Round-Trip-/Audit-Schaden | G2/G4; eigenes Ledgerschema, Java-Extension-Zugriff gesondert prüfen |
| **R-02** | Boundary EQBD/TPBD und GL im PowSyBl-Export nicht als vollständige neue Profile dokumentiert | hoher Liefervertrags-Konformitätsbedarf | Original-Boundary unveränderlich referenzieren; G1/G4 |
| **R-03** | CGM-Quick-Update nur SSH/SV, EQ-Strukturmutation ohne gesicherte Profilneuplanung | falscher „Update“-Begriff | getrennte Exportmodi; strukturelle Änderungen zunächst sperren |
| **R-04** | Verlust elektrischer Sonderfälle im PyPSA-Abbild: 3W, PST, DC-Converter, operative Limits, Shunts | materiell falsche Lastflüsse | Gerätemapping-Matrix und G3/G5 |
| **R-05** | Geo/Region-Country-Mapping unvollständig oder GL nicht geladen | falsche Landeszuordnung | GL explizit laden, Länderidentität und Koordinate getrennt validieren |
| **R-06** | VeraGrid MultiCircuit nicht identischer CGMES-Rohobjektgraph; v3-Full-RT nicht bewiesen | Fallback mit ID-Verlust | Rohobjekte/Originalmanifest parallel bewahren; G4 |
| **R-07** | Java/RDF4J/CGMES-Modellerweiterung Speicher und Ressourcenschließung | große CGM-RAM-Last | G0/G6; Extensions nur nach Zugriffsklärung aktivieren |
| **R-08** | SOPTIM ersetzt HVDC-Konverter durch Lasten | für M0-Transmission unzulässige Informationseinbuße | nur separater SV/SE-Vergleich, nicht Primärpfad |
| **R-09** | Original-CGMES/ENTSO-E-Datensätze und Conformity-Testsets können Lizenz-/Weitergaberegeln haben | Reproduzierbarkeit/Datenschutz | Berechtigung und Versionierung vor Tests klären; keine Testdaten ins Repo kopieren |
| **R-10** | Code-/Profilregister oder grüner Testname als vollständige Konformität interpretiert | falsche Reifeaussage | D/C/T/M/U strikt trennen; G1–G6 vor Produktivgates |

## 11. Entscheidung und S-GOV-Handoff

**Primäres Backend (P):** **PowSyBl/powsybl-core über PyPowSyBl**, mit eigenem **tabellarischem PyPSA-Adapter und Provenienz-Ledger**. **Fallback (P):** **VeraGrid** als alternative Python-CGMES-Objekt-/Serializer-Schicht mit identischem kanonischen Tabellenvertrag. **Nicht wählen:** CIMpy/CIMgen als vollständiges elektrisches Hauptbackend, SOPTIM/PGM als CGMES-System-of-Record, SiennaSchemas als vermeintlichen CGMES-Parser.

**Endstatus:** **CONDITIONAL_WITH_NAMED_GAPS**, weil keine reale 2.4/3.0-Datensatzkonformität ausgeführt und weder GL/Boundary-Full-Export noch End-to-End-PyPSA↔CGMES-Round-Trip für alle Sondergeräte nachgewiesen sind.

**Maximal fünf S-GOV-Entscheidungspunkte:**

1. **Backend-Freeze:** A als M0-Primärpfad und B als unabhängiger Fallback freigeben; C ausschließlich Diagnose-/Schemaoption.
2. **Export-Scope:** Nur Detailnetz-**SSH/SV-Updates** als erste rückexportierbare Operation erlauben; **Full-EQ/TP** und strukturelle Veränderungen ausdrücklich separat qualifizieren.
3. **Provenienz:** Unveränderliche Original-CGMES-Lieferungen und vollständiges Source-/ID-/Profile-/Authority-/Boundary-Ledger **verbindlich**; PyPSA ist nie exklusiver Quellspeicher.
4. **Mindestgeräte:** 2W/3W, PST, HVDC/Converter, Generator, Last, Shunt, geographische / Landes- und Boundary-Referenzen sowie GL optional/negativ prüfen – ohne stillschweigende Informationsverluste.
5. **Nächstes Gate:** G0–G6 in einem konsolidierten Implementierungs-/Qualifikationsmakro für **beide** CGMES-Versionen spezifizieren und später durchführen; **in diesem Auftrag keine Test- oder Source-Code-Ausführung**.

## 12. Verifizierbare Quellen (Quelltext/Tests/Releases)

**Lokales Projekt**

- **[P1]** [Repository-README am Basiscommit](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/README.md).
- **[P2]** [REPOSITORY_AUDIT.md am Basiscommit](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/docs/REPOSITORY_AUDIT.md).
- **[P3]** [Band II, insbesondere Kap. 2, 8–10](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/docs/current/IOSN_2026_Band_II_PyPSA_Implementierung.md).

**PowSyBl / PyPowSyBl**

- **[E1]** [powsybl-core CGMES-Import: Parser/Triplestore, Node-Breaker, Geräte](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/import.md); [CGMES Versionsspezifikation](https://powsybl.readthedocs.io/projects/powsybl-core/en/v7.4.0/grid_exchange_formats/cgmes/format_specification.html).
- **[E2]** [Core CGMES-Import-Optionen, Modelling Authority, mRID, Update, Extensions (Code-Doku)](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/import.md#options); [PyPowSyBl GL-Import-Postprozessor](https://powsybl.readthedocs.io/projects/pypowsybl/en/stable/user_guide/network_visualization.html).
- **[E3]** [CGMES-Export, IGM- und CGM-Quick-Update, CIM-Versionen, Profilumfang](https://powsybl.readthedocs.io/projects/powsybl-core/en/v7.2.0/grid_exchange_formats/cgmes/export.html); [Versioniertes Export-Markdown](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/export.md).
- **[E4]** [PyPowSyBl Netz-, DataFrame- und Update-API](https://powsybl.readthedocs.io/projects/pypowsybl/en/latest/user_guide/network.html); [Python-Implementierung](https://github.com/powsybl/pypowsybl/blob/1405d4e64a3a4df1c1fc5ce417457c56723ee4ed/pypowsybl/network/impl/network.py); [CGMES-Alias-Beispiel](https://powsybl.readthedocs.io/projects/pypowsybl/en/latest/_modules/pypowsybl/network/impl/network.html).
- **[E5]** CGMES-spezifische Commits [#4172 22.10.2026](https://github.com/powsybl/powsybl-core/commit/8a18567d6fb17749bd5c605147a86bd88768cf03), [#4170 22.10.2026](https://github.com/powsybl/powsybl-core/commit/aec82b15ee2dc0b714688afcd6379662340fb06b), [#4123 06.10.2026](https://github.com/powsybl/powsybl-core/commit/b1ff9ddf8e7c1857daa53361ccb377694679d89e); [Releases v7.4.2](https://github.com/powsybl/powsybl-core/releases/tag/v7.4.2).

**VeraGrid**

- **[E6]** [VeraGrid File/API-Dokumentation](https://veragrid.readthedocs.io/en/latest/md_source/file_operations.html); [CgmesDataParser](https://github.com/SanPen/VeraGrid/blob/54aac3a08de1339eeb10a1f2c73df3e3b03cc1d3/src/VeraGridEngine/IO/cim/cgmes/cgmes_data_parser.py).
- **[E7]** [CgmesCircuit](https://github.com/SanPen/VeraGrid/blob/54aac3a08de1339eeb10a1f2c73df3e3b03cc1d3/src/VeraGridEngine/IO/cim/cgmes/cgmes_circuit.py); [CgmesExporter und Profilregister](https://github.com/SanPen/VeraGrid/blob/54aac3a08de1339eeb10a1f2c73df3e3b03cc1d3/src/VeraGridEngine/IO/cim/cgmes/cgmes_export.py#L28-L99).
- **[E8]** [CGMES→CGMES-Test 2.4](https://github.com/SanPen/VeraGrid/blob/54aac3a08de1339eeb10a1f2c73df3e3b03cc1d3/src/tests/FileFormats/CGMES/test_cgmes_roundtrip_cgmes_to_cgmes.py); [v3 CAS Load-Test](https://github.com/SanPen/VeraGrid/blob/54aac3a08de1339eeb10a1f2c73df3e3b03cc1d3/src/tests/FileFormats/CGMES/test_cgmes_cas_v3_load.py).
- **[E9]** [CGMES-Code-Verzeichnis-Commit 22.10.2026](https://github.com/SanPen/VeraGrid/commit/54aac3a08de1339eeb10a1f2c73df3e3b03cc1d3); [VeraGrid-Releases](https://github.com/SanPen/VeraGrid/releases).

**CIMpy / CIMgen / PyCGMES**

- **[E10]** [CIMpy Import v2.4](https://github.com/sogno-platform/cimpy/blob/ac400d43c015afc4ac58e7e833b91fcba6f32812/cimpy/cimimport.py), [Export](https://github.com/sogno-platform/cimpy/blob/ac400d43c015afc4ac58e7e833b91fcba6f32812/cimpy/cimexport.py), [CGMESProfile inkl. Boundary/GL](https://github.com/sogno-platform/cimpy/blob/ac400d43c015afc4ac58e7e833b91fcba6f32812/cimpy/cgmes_v2_4_15/CGMESProfile.py).
- **[E11]** [CIMpy CGMES-Boundary-Korrektur 13.08.2024](https://github.com/sogno-platform/cimpy/commit/4cfe83e23d7b4196640e62d7489bd8b01a8aabe2); [Release v1.2.0](https://github.com/sogno-platform/cimpy/releases/tag/v1.2.0); [Tests](https://github.com/sogno-platform/cimpy/tree/ac400d43c015afc4ac58e7e833b91fcba6f32812/tests).
- **[E12]** [CIMgen Schemaquellen 2.4/3.0](https://github.com/sogno-platform/cimgen/tree/5526eef5bc2be764f9f96bf5b65ec8daee5b5cca/cgmes_schema); [CIMgen Quellcode](https://github.com/sogno-platform/cimgen/blob/5526eef5bc2be764f9f96bf5b65ec8daee5b5cca/cimgen/cimgen.py); [Codegenerator-Commit 28.10.2026](https://github.com/sogno-platform/cimgen/commit/5526eef5bc2be764f9f96bf5b65ec8daee5b5cca).
- **[E17]** [Alliander PyCGMES](https://github.com/alliander-opensource/pycgmes/tree/282db60eefff2186dac35a11f588170cbcbe3af2), [Base-Profil-/mRID-Datenmodell](https://github.com/alliander-opensource/pycgmes/blob/282db60eefff2186dac35a11f588170cbcbe3af2/pycgmes/utils/base.py), [ChevronWriter](https://github.com/alliander-opensource/pycgmes/blob/282db60eefff2186dac35a11f588170cbcbe3af2/pycgmes/utils/chevron_writer.py), [SHACL/Tests](https://github.com/alliander-opensource/pycgmes/tree/282db60eefff2186dac35a11f588170cbcbe3af2/tests).

**SOPTIM / PowerGridModel**

- **[E13]** [SOPTIM Converter README inkl. CGMES-Versionen, PGM-Komponenten und DC-Ersatz](https://github.com/SOPTIM/cgmes2pgm_converter/blob/56702bb18a21c344533a57ff52791b75298c1138/README.md).
- **[E14]** [Converter-API CgmesToPgmConverter](https://github.com/SOPTIM/cgmes2pgm_converter/blob/56702bb18a21c344533a57ff52791b75298c1138/src/cgmes2pgm_converter/converter.py); [Converter-Releases](https://github.com/SOPTIM/cgmes2pgm_converter/releases).
- **[E15]** [Suite README: Fuseki, YAML, Tests, SV](https://github.com/SOPTIM/cgmes2pgm_suite/blob/3c56fe98752db354ef5062e590f163ec91dba2f7/README.md); [app.py Orchestrierung](https://github.com/SOPTIM/cgmes2pgm_suite/blob/3c56fe98752db354ef5062e590f163ec91dba2f7/src/cgmes2pgm_suite/app.py).
- **[E16]** [SvProfileBuilder](https://github.com/SOPTIM/cgmes2pgm_suite/blob/3c56fe98752db354ef5062e590f163ec91dba2f7/src/cgmes2pgm_suite/export/sv_builder.py); [Fuseki-Integration](https://github.com/SOPTIM/cgmes2pgm_suite/tree/3c56fe98752db354ef5062e590f163ec91dba2f7/src/cgmes2pgm_suite/rdf_store); [Suite-Releases](https://github.com/SOPTIM/cgmes2pgm_suite/releases).
- **[E18]** [PGM-IO Converter-Index](https://github.com/PowerGridModel/power-grid-model-io/blob/449946be3bbdef1467cd7328dc01f29ff960bee3/src/power_grid_model_io/converters/__init__.py), [PandaPowerConverter](https://github.com/PowerGridModel/power-grid-model-io/blob/449946be3bbdef1467cd7328dc01f29ff960bee3/src/power_grid_model_io/converters/pandapower_converter.py), [CGMES-Issue #207](https://github.com/PowerGridModel/power-grid-model-io/issues/207), [v2.0.36](https://github.com/PowerGridModel/power-grid-model-io/releases/tag/v2.0.36).

**pandapower / Julia / Sienna**

- **[E19]** [pandapower CIM from_cim](https://github.com/e2nIEE/pandapower/blob/8775573581e2bbec4e1e133c91db8ffeb2a602cc/pandapower/converter/cim/cim2pp/from_cim.py#L108-L184); [offizielle Konverterdokumentation](https://pandapower.readthedocs.io/en/v3.5.5/converter/cgmes.html).
- **[E20]** [PyPowSyBl pandapower-Konvertierungstest](https://github.com/powsybl/pypowsybl/blob/1405d4e64a3a4df1c1fc5ce417457c56723ee4ed/tests/test_pandapower.py), [Reverse-Konverter-Issue #895](https://github.com/powsybl/pypowsybl/issues/895).
- **[E21]** [Sparlectra README, CGMES-Import-/Exportumfang](https://github.com/Welthulk/Sparlectra.jl/blob/15831717458272197b2611264f05cdcf34cb1963/README.md), [CGMES-Adapter](https://github.com/Welthulk/Sparlectra.jl/tree/15831717458272197b2611264f05cdcf34cb1963/src/adapters/cgmes), [CGMES-2.4-Exporter/mRID](https://github.com/Welthulk/Sparlectra.jl/blob/15831717458272197b2611264f05cdcf34cb1963/src/adapters/cgmes/cgmes_export.jl).
- **[E22]** [Sparlectra CGMES-Tests](https://github.com/Welthulk/Sparlectra.jl/tree/15831717458272197b2611264f05cdcf34cb1963/test), [Release v1.0.0](https://github.com/Welthulk/Sparlectra.jl/releases/tag/v1.0.0), [CGMES-Fachcommit 21.10.2026](https://github.com/Welthulk/Sparlectra.jl/commit/ef0368b7bbf71d17aaa46bbdca2a31f77bcaa1c9).
- **[E23]** [SiennaSchemas README (kein CGMES)](https://github.com/Sienna-Platform/SiennaSchemas/blob/53cbffec27376b23a9ced996131e0fcf8f1ee1f9/README.md), [Schemas-Pipeline](https://github.com/Sienna-Platform/SiennaSchemas/blob/53cbffec27376b23a9ced996131e0fcf8f1ee1f9/docs/PIPELINE.md).

**Lizenzbefund:** powsybl-core, pypowsybl, VeraGrid, PowerGridModel-IO: **MPL-2.0**; CIMpy, CIMgen, PyCGMES, SOPTIM Converter/Suite, Sparlectra: **Apache-2.0**; pandapower und SiennaSchemas: **BSD-3-Clause** (Repository-LICENSE-Dateien, geprüft 30.10.2026). Kompatibilität der **gesamten** transitive Dependency-BOM bleibt G0, nicht durch das Hauptlizenzkürzel entschieden.

---

**Forschungsumfang abgeschlossen; keine produktiven Dateien verändert.** Dieser Bericht ist ein unabhängiger statischer Vergleich und **keine** positive CGMES-Konformitäts- oder Realnetz-Validierung.
