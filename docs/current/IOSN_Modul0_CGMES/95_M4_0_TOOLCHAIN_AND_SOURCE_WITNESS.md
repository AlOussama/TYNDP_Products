# M4-0 — Konsolidierter Toolchain-, Backend- und CGMES-Quellwitness

**Projekt:** IoSN / TYNDP / PyPSA — Modul 0, CGMES ↔ Canonical ↔ Detailed PyPSA  
**Datum:** 2026-11-01  
**Makro:** M4-0, einmalige dokumentarische Vorbereitung von PoC-M1 und T-06  
**Verbindlicher S-GOV-Baseline-Commit:** `b1e284996fa69f81651daf9150b829e6a42e4ce3`  
**Fachautorität:** [70 Readiness](70_IMPLEMENTATION_READINESS.md), [85 CAN/2.0.0 Repair](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md), [90 S-GOV Freeze](90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md)  
**Status:** `M4_0_STATIC_FACTS_AND_SOURCE_CANDIDATES_VERIFIED; RUNTIME_NOT_EXECUTED`

## 1. Ausführungsgrenze und Evidenzklassen

Dieses M4-0-Makro hat die GitHub-Quellen, Release-Metadaten, konkrete öffentlich erreichbare Testdateien und die bereits verabschiedeten Verträge **statisch geprüft**. Es hat **keine** produktive Implementierung, Paketinstallation, CGMES-Einlesung, Python-/Java-API-Lauf, Berechnung elektrischer Lastflüsse, Lizenzfreigabe, unabhängige T-06-Ausführung oder echte PoC-Qualifikation durchgeführt.

- `SRC_VERIFIED` = Inhalt/Blob am festen Git-Commit tatsächlich gelesen bzw. konkrete Originaldatei per API aufgelöst.
- `RELEASE_VERIFIED` = konkretes Paket/Artefakt samt Version und ggf. SHA-256 in PyPI belegt.
- `ARCH_DECIDED` = projektinterne verbindliche Entwurfsentscheidung; kein Upstream-/Runtime-Beweis.
- `RUNTIME_UNVERIFIED` = Installation/ABI, Backend-Write-Verhalten, Fixture-Import oder Konformität noch nicht ausgeführt.
- `RIGHTS_UNVERIFIED` = Quelle existiert öffentlich, aber Nutzungs-/Redistributionsberechtigung nicht unabhängig für den jeweiligen Datensatz bestätigt.
- `NOT_FOUND_OR_NOT_CHECKED` = kein hinreichender Nachweis in der durchgeführten Recherche; nicht die Behauptung, dass der Datensatz überhaupt nicht existiere.

Die Quellprüfung war *gezielt*, keine neue allgemeine Backendvergleichskampagne. Frühere Fachberichte bleiben unverändert. Der unabhängige M3-Historienstatus lautet weiterhin REPAIRS_REQUIRED, die spätere S-GOV-Entscheidung ARCHITECTURE_FROZEN_FOR_IMPLEMENTATION_PLANNING.

## 2. Exakte Repo-Basis und dokumentierter Buildvertrag

- S-GOV-Commit `b1e284996fa69f81651daf9150b829e6a42e4ce3` über GitHub direkt verifiziert; der eingefrorene Canonical-/DNR-Vertrag ist in 85 spezifiziert.
- `pyproject.toml`-Blob: `09b6f4b1d524dc5a2f6af79a6b39598ade53bcf8`. `requires-python = ">=3.11"`; Basispakete `numpy>=1.24`, `scipy>=1.10`, `pandas>=2.0`; optional `pypsa>=1.4,<2`; Test `pytest>=7`.
- Eine vollständige `M0`-Distribution oder `powsybl`-Versionpins existieren im unveränderten produktiven Buildvertrag **noch nicht**. Sie sind PoC-Artefakte, kein in M4-0 bereits aktualisierter Programmcode.
- Der bestehende `src/tyndp_reduce/pypsa_adapter.py` bleibt auf Single-Island/Line-only-DC beschränkt. `REDUCTION_ADAPTER_READY` ist **nicht** gegeben.

## 3. Vorgeschlagene, quellenbelegte initiale Toolchain-Kandidaten

| Rolle | Kandidat / überprüfte Evidenz | Aussage und noch offener Ausführungswitness |
|---|---|---|
| Referenzruntime | CPython **3.11 x86_64**, vorzugsweise Windows x64 als Referenzplattform; `>=3.11` aus Projekt; exakter Patch-Level noch nicht auf Host gemessen | `ARCH_DECIDED`; OS-Build/CPU/CPython-ABI/`pip freeze`/Wheel-Hashes in Hostmanifest erforderlich |
| PyPSA | `pypsa==1.4.0`; PyPI Release 2026-10-09, Python >=3.11, wheel `pypsa-1.4.0-py3-none-any.whl` SHA-256 `216d00376f82b3c8d6d19747bcc868bfaa634befcf34d1564ad0730984f448d1` | `RELEASE_VERIFIED`; tatsächliche PyPSA-Komponenten-API/ACPF/LPF auf Zielhost nicht getestet |
| Primärer CGMES-Python-Backend | `pypowsybl==1.16.1`; PyPI Release 2026-07-22, Python 3.10–3.14; Windows cp311 wheel `pypowsybl-1.16.1-cp311-cp311-win_amd64.whl` SHA-256 `9c280108aa34ac861442423d2a06dab991c5670eb36da36f59489eb37b3d49c6` | `RELEASE_VERIFIED`, native GraalVM-library wird mit ausgeliefert; tatsächliches Bundle-/CGMES-Verhalten noch ungetestet |
| Unabhängiger minimaler T-06-Backend | `VeraGridEngine==6.7.20`; PyPI Release 2026-10-22, `veragridengine-6.7.20.tar.gz` SHA-256 `f24c18ad039820df4c629e2d23828ca8b34b9dcc291eb7ecf0c6f58e3df15069` | `RELEASE_VERIFIED`; separates minimal installiertes read-only Fixture-Parsing, keine verpflichtende volle Produktionsruntime; Build-/Abhängigkeitsfähigkeit ungetestet |
| PowSyBl-Core-CGMES-Dokumentation | Unveränderlicher Git-Commit `f6749ad368fba8dd3776099c040fed07023a1ba3`; Import-/Export-Dokumentblobs `3e5c996c789ef32d93d90d5a0e71efede94f6307` / `53c81e680473419116537a58187d2b60b337c096` | `SRC_VERIFIED`; **kein** Nachweis, dass genau dieser Core-Commit im PyPowSyBl-1.16.1-Wheel enthalten ist |
| PyPowSyBl-Buildhinweis | Tag `v1.16.1`, `java/pom.xml`-Blob `1082723057fc95092b19d6859a6b0d9ce8217a84`: Buildziel Java 21, `powsybl-dependencies.version=2026.1.0` | `SRC_VERIFIED`; Java-21-Buildvorgabe **nicht** automatisch System-JRE-Laufzeitvoraussetzung eines installierten Native-Wheels; Core-/ABI-Bundle im Testhost ermitteln |

**Wichtige Versionierungsentscheidung:** Kein unabhängiges, mutmaßlich kompatibles `powsybl-core==7.4.2` neben `pypowsybl==1.16.1` festlegen. Die ältere Release-/Upstream-Dokumentation erklärt vorhandene Funktionalität, belegt aber **keine** native Kombinationskompatibilität. Der PoC pinnt zuerst das konkrete Python-Wheel; dessen tatsächlich enthaltene Core-/CGMES-/Native-Library-Versionsidentität ist separat zu erfassen. Auf Linux und anderen Python-ABIs sind jeweils **andere** Paket-Wheel-SHA-256 zu pinnen; ein Windows-Wheel-Hash darf dort nicht ungeprüft übertragen werden.

**Referenzlinks (geprüft):**
- https://pypi.org/project/pypowsybl/1.16.1/
- https://pypi.org/project/pypsa/1.4.0/
- https://pypi.org/project/VeraGridEngine/6.7.20/
- https://github.com/powsybl/pypowsybl/blob/v1.16.1/java/pom.xml
- https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/import.md
- https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/export.md

## 4. Statischer Backend-API-Witness und nicht gesicherte Funktionen

| Pfad | Explizit im festgepinnten Upstream-Quellstand gefunden | Eigene M0-Schnittstelle / noch zu prüfen |
|---|---|---|
| PyPowSyBl-Netz-API | `Network.update_from_file(...)`, `Network.save(..., format='CGMES', parameters=...)` und tabellarische `get_*`-Methoden in `pypowsybl/network/impl/network.py` am Tag `v1.16.1`; Blob `b0901c4a50d96e4193e2e5bb8940c58fa50ed353` | `FormatBackend.open_delivery/extract_tables/extract_identity_metadata` sind **eigene** Portmethoden und keine garantierten Upstream-Funktionen |
| CGMES-Input | Externer Core beschreibt RDF4J-/SPARQL-Import und NODE_BREAKER/BUS_BRANCH; nur Node/Breaker ohne TP bei bewiesener EQ/SSH-Ableitung | Buss/Branch benötigt geliefertes gültiges TP; Origin-Country-/Substation/Terminal-RDF-Beziehungen dürfen nicht allein aus möglicherweise gemergtem IIDM abgeleitet werden |
| Source-/ID-Preservation | Original-CGMES-mRID, ID/Alias-Parameter und Metadaten-Optionen in Upstream dokumentiert; Java-Extension für Triplestore möglich | Vollständige Python-Exponierung aller RDF-Subjects, BlankNodes, FullModel, MAS/Authority, ungemappter Attribute und Change-Inversen ist `UNKNOWN`; eigener unveränderlicher Originalgraph zwingend |
| CGM-Quick-Export | Upstream dokumentiert **immer** SSH pro IGM plus ein CGM-SV, Profile-Selektion ignoriert | `CGM_QUICK_SSH_SV` nur mit qualifiziert berechnetem SV; kein SSH-only per Profilfilter |
| Manueller IGM-/Subnetwork-Export | Upstream-Dokumentation zeigt Java-Sample mit expliziten Subnetworks, Header-Extensions, DependsOn/Supersedes und SSH-Profilwahl | `MANUAL_IGM_SSH` erfordert tatsächlich zugänglichen Python-/Java-Pfad + Backend-/Header-/Reimport-Witness; bis dahin `BLOCK_EXPORT_UNPROVEN` |
| VeraGrid | CGMES-2.4.15- und 3.0-Parser/Objektmodell im statischen Quellvergleich belegt | Als **read-only** zweiter unabhängiger T-06-Normalisierungs-/Fixture-Snapshot eingeplant; volle VeraGrid-Production-/Exporter-Qualifikation nicht erforderlich |

**Konkretes zusätzliches Risiko:** Der PowSyBl-Quick-Export konstruiert IGM-Dateinamen teilweise aus der *ersten IIDM-Substation und deren Country*. Dieses Verhalten ist **keine** Original-Source-MAS-/Country-Herkunft; für Exporte müssen Modelle/Authorities/Headers explizit verifiziert werden. Ein erfolgreiches `Network.save` ist kein `UPDATE_EXPORT_READY`.

## 5. Tatsächlich vorhandene CGMES-Ressourcen — eingefrorene Upstream-Dateien

Die Quelle ist `powsybl/powsybl-core` am Commit `f6749ad368fba8dd3776099c040fed07023a1ba3`. Katalog-Quellcode und folgende Beispiel-RDF/XML-Dateien wurden **einzeln per GitHub-Content-Zugriff nachgewiesen**, nicht nur aus README-Titeln abgeleitet. Ursprung: `cgmes/cgmes-conformity/src/main/resources/`.

| Ressourcenfamilie / Kandidat | Beispielpfad relativ zum Resources-Root | Verified Git blob | Belegstatus |
|---|---|---|---|
| CAS-1.1.3, CGMES 2.4.15, BE EQ | `conformity/cas-1.1.3-data-4.0.3/MicroGrid/BaseCase/CGMES_v2.4.15_MicroGridTestConfiguration_BC_BE_v2/MicroGridTestConfiguration_BC_BE_EQ_V2.xml` | `ce6ea01a997dd44f71c7e09efc8c44fc340bbbf7` | Datei vorhanden |
| 2.4.15, BE SSH / TP / SV | Gleiches Verzeichnis; Dateinamen `MicroGridTestConfiguration_BC_BE_{SSH,TP,SV}_V2.xml` | `3d1f09fff90a843be2bd34125686f19efb10edf4` / `e1801bb9789cf865f09108e1bb39d4bd9ea07800` / `5e29239c8d80ccbb0ac352093e545020a4d81f60` | jede Datei vorhanden |
| 2.4.15, Boundary EQ/TP | `conformity/cas-1.1.3-data-4.0.3/MicroGrid/BaseCase/CGMES_v2.4.15_MicroGridTestConfiguration_BD_v2/`; `MicroGridTestConfiguration_EQ_BD.xml` / `MicroGridTestConfiguration_TP_BD.xml` | `629193c34f1467c053e8ca078a0f5f5bfb5f295e` / `29b21079254f1558b7c4ab06ab26fc6c951a2c1c` | beide Dateien vorhanden |
| 2.4.15, BE GL | `conformity/cas-1.1.3-data-4.0.3/MicroGrid/BaseCase/CGMES_v2.4.15_MicroGridTestConfiguration_BC_BE_v2/MicroGridTestConfiguration_BC_BE_GL_V2.xml` | `9902cc801f2e3b4b391bb7ffe5d228e0a5549fea` | Datei vorhanden |
| CAS-3, CGMES 3.0, BE EQ/SSH/TP/SV | `conformity/cas-3-data-3.0.2/MicroGrid/BaseCase/MicroGrid-BE-MAS/`, `20210325T1530Z_1D_BE_{EQ,SSH,TP,SV}_001.xml` | `39e8ca67679f4378cf389c8d552ceffe2260155a` / `f0d34bbb0d80e02859ac5e1d20bcb7ceb6fabbf8` / `abb852260433fa8afe7c2385f0cdd0a08fcca542` / `62ac657a54ed0b50d51aa2b29a100fc4a2709989` | alle vier vorhanden |
| 3.0, BE GL | `conformity/cas-3-data-3.0.2/MicroGrid/BaseCase/MicroGrid-BE-MAS/20210325T1530Z_1D_BE_GL_001.xml` | `2dce68f8dcb2b9e7e9ffc537e70fff100c57bfa8` | Datei vorhanden |
| 3.0, NL EQ/SSH | `conformity/cas-3-data-3.0.2/MicroGrid/BaseCase/MicroGrid-NL-MAS/20210325T1530Z_1D_NL_{EQ,SSH}_001.xml` | `60af914251bb1ed1e2475eaf57d9486a74258f3f` / `17c734cb0f6e8e44dd0c893e72aa7080d301a316` | beide vorhanden |
| 3.0, CGM Assembled TP/SV | `conformity/cas-3-data-3.0.2/MicroGrid/BaseCase/MicroGrid-BaseCase-Merged/20210325T1530Z_1D_ASSEMBLED_{TP,SV}_001.xml` | `0562197570b2be18139383c606f0efd54ba9dfe5` / `a649d3e8222266ca1602ed95affd8e85e7a6a382` | beide vorhanden |
| 3.0, Boundary EQ | `conformity/cas-3-data-3.0.2/MicroGrid/BaseCase/MicroGrid-BD-MAS/20171002T0930Z_ENTSO-E_EQ_BD_2.xml` | `6c4a50e5603c7aa15ce752901af6c72296bc1612` | Datei vorhanden |
| 2.4.15 MiniGrid Bus/Branch EQ/TP | `conformity/cas-1.1.3-data-4.0.3/MiniGrid/BusBranch/CGMES_v2.4.15_MiniGridTestConfiguration_BaseCase_v3/MiniGridTestConfiguration_BC_{EQ,TP}_v3.0.0.xml` | `054b6b8ad41870db13040b1f2e195ee6688d736c` / `621c551ed7b42eb9f70bac000081b9b31771ea49` | beide vorhanden |

**Entscheidender Versionshinweis:** Ein Dateiname `..._v3.0.0.xml` in einem **CGMES-2.4.15-MiniGrid-Katalog** ist *kein* Beweis der CGMES-3.0-Profilfamilie. Familienzuordnung erfolgt anhand der tatsächlichen Profile-URIs/FullModel-Header, nicht aus dem Dateinamen.

Die Git-Blobs sind **SHA-1 Git-Objektkennungen**, *keine* SHA-256-Checksummen der heruntergeladenen Rohdateien. Für jede verwendete Fixture sind Downloadbytes, ursprünglicher Upstream-Pfad/Commit, SHA-256, Dateigröße, Profile-URI, Lizenz/Weitergabestatus sowie ggf. CGMES-Validierungsergebnis **vor Testbeginn neu** zu erfassen. Der Upstream-Quellzugriff ist kein unabhängiger Nachweis, dass sämtliche Kombinationen aktuell problemlos importierbar oder die Datensätze frei redistribuierbar sind.

**Katalogreferenzen:**
- https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/cgmes/cgmes-conformity/src/main/java/com/powsybl/cgmes/conformity/CgmesCatalogsConstants.java
- https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/cgmes/cgmes-conformity/src/main/java/com/powsybl/cgmes/conformity/CgmesConformity1Catalog.java
- https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/cgmes/cgmes-conformity/src/main/java/com/powsybl/cgmes/conformity/CgmesConformity3Catalog.java

## 6. F-01…F-08: real verfügbare Quellen versus noch anzulegende Varianten

| Fixture | Vorgesehener Testzweck | M4-0-Befund / sichere nächste Handlung |
|---|---|---|
| F-01 | 2-Bus AC, Generator, Last, Shunt, Units / KCL | **Noch nicht als vollständig testbereite CGMES-Datei im Projekt nachgewiesen.** Aus den kleinen geprüften Originalprofilen ableiten oder eigenständig klar gekennzeichnet synthetisch erzeugen; Quelle/License/Hashes getrennt dokumentieren |
| F-02 | NODE_BREAKER, BUS_BRANCH, Switch/TP, Negativfall TP fehlt | 2.4.15 MiniGrid Bus/Branch EQ/TP **dateibasiert nachgewiesen**; Node/Breaker-/TP-negative Varianten als separate Hash-Fixtures erst erstellen und prüfen |
| F-03 | 2W/3W, Tap/PST, Ybus | Katalog nennt Gerätefälle; geeignetes vollständiges 3W/PST-Resultat und unabhängiger Ybus-Witness **nicht** hier geprüft; konstruktive negative Varianten für PoC-M2 vorbereiten |
| F-04 | Single-/Multi-IGM/CGM, Boundary, Identität | 2.4.15 BE+Boundary und 3.0 BE+NL+Assembly-TP/SV+Boundary **Originaldateien teilweise/gezielt nachgewiesen**; tatsächliche Gesamtsatzvollständigkeit/Importscope/Lizenz/Hashes müssen im Worker erhoben werden |
| F-05 | zwei AC-Islands mit HVDC, vorwärts/rückwärts | Quellen/Kataloge für HVDC vorhanden, aber kein kompletter validierter F-05-Testbeweis; negative Reverse-Loss-Fixture erst im PoC-M2 |
| F-06 | granulare Limits und GL/CRS | GL-Dateien beider Familien **verifiziert**; Limit-/CRS-Qualität und negative Testvarianten nicht ausgeführt |
| F-07 | SSH-only/Quick-SV/CREATE/Crash-Semantik | **Neues reproduzierbares Export-/Recovery-Fixture zu erzeugen**, inkl. ungeeignetem SV, Graph-Diff, Idempotenz, FS-/CAS-Crash |
| F-08 | Lizenzierter echter IGM/CGM-Multiarea-Realnetz-/Skalierungsfall | **NICHT_QUALIFIZIERT**: kein konkreter lizenz-/reuse-geprüfter europäischer Realnetzdatenstand, keine 6k+-Bus-Gate-Evidenz; getrennte spätere Dateneigentümerfreigabe erforderlich |

Die fünf bereits festgelegten Wetterjahre sind nicht Teil dieses Makros. Clustering, PECD, Markt-/Dispatchzeitreihen und die IoSN-Netzreduktion werden **nicht** neu geplant.

## 7. Fünf tatsächlich relevante Restwitnesses

1. **RUNTIME-PIN:** PyPowSyBl 1.16.1/PyPSA 1.4.0/VeraGridEngine 6.7.20 installierbar, Python-ABI, vollständige transitive `pip freeze`-BOM, native/Core-CGMES-Version und Feature-/Parameterausgabe noch nicht gemessen.
2. **SOURCE-ACCESS:** Originalgraph-/RDF-/MAS-/Substation-/Terminal-/Unmapped-Attribute-Zugriff durch tatsächlichen PoC-Datenpfad unbewiesen; GL/Boundary-Originale separat sichern.
3. **DATASET-ENTITLEMENT:** Quellpfade sind vorhanden, aber Rechte und Redistribution der ENTSO-E/CAS-Originaldaten noch nicht **rechtsverbindlich** dokumentiert. Kein Kopieren in öffentliche Repo-Branches ohne Rights-Witness.
4. **T-06:** unabhängige VeraGrid-BackendSnapshot-Erzeugung/Canonical-Parität noch nicht ausgeführt; REQ-009 bleibt NOT_ASSESSED.
5. **F-08/PERFORMANCE/EXPORT:** kein qualifizierter echter großer Datensatz, kein Runtime-/Graph-Update-/Recovery-/ACPF-PASS.

**S-GOV-Verwendung:** Dieser Bericht begründet die Wahl einer konkret überprüfbaren **Kandidatenumgebung und Quellfixture-Liste**, **nicht** eine unbedingte M4-RunRelease-Freigabe. Der nächste Bericht 96 definiert verbindliche Ausführungs- und Abbruchgates.
