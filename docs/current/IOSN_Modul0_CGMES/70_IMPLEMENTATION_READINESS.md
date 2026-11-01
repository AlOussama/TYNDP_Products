# M2 — 70 IMPLEMENTATION READINESS
## Modul 0 CGMES/PyPSA: Capability-Matrix, vollständige REQ-Traceability, PoC-Makros und Releasegates

**Stand:** 2026-11-01. **Historischer Status:** `M2_IMPLEMENTATION_CONTRACT_DESIGNED_NOT_EXECUTED`. **Normative M3-Korrektur:** [85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md) (CAN/2.0.0, DNR/1.0.0, Publish/1.0.0); **dokumentarischer S-GOV-Freeze** nach [90](90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md), ausdrücklich ohne PoC-/Runtime-Freigabe; 80 bleibt ein unabhängiger unveränderter REPAIRS_REQUIRED-Bericht. Alle T-01…T-24 bleiben nicht ausgeführt. Dieses Dokument beauftragt **keine** produktive Implementierung und stellt **keinen** numerischen oder CGMES-Konformitäts-PASS dar.
**Fachliche Eingänge:** [10 Requirements](10_REQUIREMENTS.md), [20 Backend](20_BACKEND_ASSESSMENT.md), [30 Canonical](30_CANONICAL_DATA_CONTRACT.md), [40 Architecture](40_SOFTWARE_ARCHITECTURE.md), [50 Validation](50_VALIDATION_CONTRACT.md), [60 ADR](60_ARCHITECTURE_DECISION.md). Ursprüngliche R-M0-BACKEND und R-M0-CONTRACTS wurden unverändert aus den Arbeitercommits in S-GOV übernommen.

## 1. Entscheidung zur Implementierungsbereitschaft

**Historische M2-ARCHITEKTURBEREITSCHAFT (vor unabhängigen M3 REPAIRS_REQUIRED) für einen unabhängigen statischen M3-Review**, nicht bereits technik- oder systemqualifiziert. Alle 39 MUSS-Anforderungen haben einen geplanten Modulowner und einen erwarteten späteren T-Test; die jeweils gewählten Capabilities dürfen bewusst an fehlender Backend-API, unvollständiger Datenlieferung oder inkompatibler elektrischer Projektion scheitern. `DESIGNED_NOT_EXECUTED` gilt für sämtliche T-01…T-24 und `QUAL-*`. Schema-/Graph-Kompatibilität mit PowSyBl, Reimport-/Export-Identity-Fidelity, AC-Ybus, echte Testdatenlizenzen und bestehende M1-Integration sind nicht nachgewiesen.

**Minimaler erste Betriebsumfang:** Belegter einfacher Importpfad auf PowSyBl über das öffentliche Backend-Port-Interface → canonical object/terminals/topology + immutable original → elektrische positive-sequence View nach PyPSA, mit ausschließlicher **Import-/Projektion-Capability**. Exportfähigkeiten sind getrennt zu entwickeln und freizugeben; das Zieldesign muss sie jetzt berücksichtigen, aber ein erster Import-PoC wird nicht durch einen noch nicht gebauten Full-CGMES-Export blockiert.

## 2. Arbeitspakete, Modulowner und Implementierungsschnitt

| Implementierungspaket | Verantwortliche Module | Liefergegenstand / Schnittvertrag | Kritische Abhängigkeit | Aufwandklasse (relativ) |
|---|---|---|---|---|
| `P0 BACKEND-IN` | `backend`, `archive_provenance` | Pinned PyPowSyBl-Laufzeit, Original ZIP/XML+Manifest, Version-/Profile-Discovery, BackendSnapshot und gesicherter Quellenanker | CGMES-Version/Familienprofil, Header-/GL-/Identity-Zugänglichkeit | mittel bis hoch |
| `P1 CANONICAL` | `canonical`, `archive_provenance` | normierte SQLite-Tabellen, Original-RDF-Identity-/Occurrence-Ledger, null/quality, transaktionale Revisionen | P0 Tabellen/API, K-03/K-04-Design | hoch |
| `P2 ELECTRICAL` | `projection`, `pypsa_port` | Topologie, Units, Gen/Load, Lines, 2W/3W, Tap/PST, HVDC, Shunt/Limit-Loss, PyPSA DetailedNetworkReference v1 | Original SourceIDs, Backendedge-/Terminalpolicy, PyPSA Version | hoch |
| `P3 EXPORT-UPDATE` | `export`, `archive_provenance`, `backend`, `validation` | Quell-/Allowlist-basierter ChangeSet, Backmapping, SSH-/SV-Profile, FullModel Dependencies, semantische Diff, atomare Delivery | gültiger Originalgraph, Backend-Write-API und Referenz-/Identity-Witness | hoch / hohes Risiko |
| `P4 EXPORT-CREATE` | `export`, `backend`, `validation` | synthetische CIM-Objektkonstruktion, IDs, Profiles EQ/TP/SSH, spezielle SV-Regeln | zusätzliche Modellautoritäts-/Equipment-/Terminalattribute | sehr hoch; später |
| `P5 QA-OPS` | `validation` + alle | Fixtures, Contract/Capability-Testharness, Lizenz-/Hash-Manifest, elektrische Referenzen, Speicher-/Load-Monitor | M2-REQ/T-Matrix, Version pins, Datenverfügbarkeit | mittel bis hoch |
| `P6 M1-ADAPTER` | außerhalb M0, Folgeprojekt Modul 1 | komplexes DetailedNetworkReference mit PST/HVDC/Trafo/mehreren AC-Islands nutzen | eigener Owner-/Scopeentscheid nach P2 | nicht von M0 implizit geliefert |

**PoC-Modulgrenze:** `P0`/`P1` werden bevorzugt im selben konsolidierten Implementierungsauftrag gestartet, nicht als isolierte Parser-Mikroaufträge. `P2` ergänzt die technische Gerätebreite; `P3` ist der priorisierte, aber separat freizugebende Exportpfad. `P4` kann unabhängig nach P2/Provenienzgrundlage geplant werden, ist nicht Voraussetzung für `P3`. `P6` bleibt im IoSN-Folgeprojekt.

## 3. Fachliche Capability- und QA-Gates

| Capability (extern sichtbarer Status) | Voraussetzungen | Qualifizierung / Tests | Kein zulässiger Ersatz |
|---|---|---|---|
| `CANONICAL_IMPORT_READY` | Version-/Profil-/Boundary-/Header-Gates, Quelle/Identität/FK-Integrität **und REQ-009/T-06 mit zwei unabhängigen BackendSnapshots** | `QUAL-FORMAT`, `QUAL-IDENTITY`, `QUAL-TOPO-GEO`, verpflichtender T-06; T-01…T-11 je relevant | Ohne T-06 ausschließlich CANONICAL_IMPORT_PROVISIONAL, kein READY-PASS |
| `PYPSA_ACPF_READY` | geeignete Stationär-AC-Geräte, Vorzeichen/Ybus/Slack/Islands, Loss | `QUAL-ELECTRICAL` + `QUAL-PYPSA`; T-12…T-20 und ggf. T-23 | Zeilenzahl gleich CGMES-Equipmentzahl |
| `PYPSA_LPF_READY` | effective x_pu und PST-/Tap-/HVDC-affine Effekte, Isolierung/Balance qualifiziert | T-09, T-14, T-17, T-20 + LPF-Referenz | reine DC-Simplifikation durch Weglassen von PST/Links |
| `REDUCTION_ADAPTER_READY` | M1 akzeptiert das typisierte DetailedNetworkReference/1.0.0 mit Quell-/State-/Canonical-/Projection-Hashes und echten Komponenten | `QUAL-M1-INTEGRATION`; T-20 + eigens autorisierter E2E-M1-Test | `PYPSA_ACPF_READY` oder `PYPSA_LPF_READY` |
| `UPDATE_EXPORT_READY` | RawGraph, Quelle-/ID-Backmapping, allowlisted Delta und Header/Graph-Witness | `QUAL-UPDATE-EXPORT`; T-21, T-24 | Pfad `Network.save` existiert |
| `CREATE_EXPORT_READY` | komplette explizite CIM-Neukonstruktionsattribute | `QUAL-CREATE-EXPORT`; T-22, T-24 | PyPSA-Tabellen ohne CIM-Semantik |
| `SV_REFERENCE_QUALIFIED` | konsistente solved-EQ/TP/SSH/SV und qualifizierter AC-Referenzzustand | `QUAL-SV-REF`; T-23 | SV fehlt oder ist widersprüchlich |
| `PERFORMANCE_QUALIFIED` | pinned CGM-Mehr-IGM-Dataset/Runtime/RAM/Timeout | `QUAL-OPS-PERF`; T-24 und Skalierungsfälle | kleines synthetisches 2-Bus-Netz |

**Teststatusfelder:** pro (`backend name/version`, `CGMES family + actual URIs`, `dataset fixture hash`, `mapping policy hash`, `operating_state`, `target capability`) ein unabhängiger Status `PASS / CONDITIONAL_WITH_NAMED_GAPS / BLOCKED / NOT_ASSESSED`. `NOT_APPLICABLE_NO_SV` ist ein begründeter Nichttest, kein bestandener SV-Abgleich. Zusätzlich getrennte dokumentarische `ARCH-STATIC`-Abnahme in M3. Performance-/Datensicherheitsstatus darf nicht mit Standard-CGMES-Zertifizierung gleichgesetzt werden.

## 4. Vollständige REQ-001…REQ-048-Traceability

**Quellenklasse** aus `10_REQUIREMENTS.md` bleibt normativ. Spalte **Owner** benennt das vorwiegend zuständige Paket (weitere Module implizit beteiligt). **T** sind spätere Nachweise, nicht durch M2 ausgeführt. Alle MUSS, SOLL und OPTIONAL werden als zukünftige Scope-/Verifikationstabelle erhalten.

| REQ | Klasse | Fachziel (kompakt) | Owner (Paket) | Verifikation | Externe Voraussetzung / Witness | Architekturrisiko |
|---|---|---|---|---|---|---|
| REQ-001 | MUSS | 2.4.15/3.0 profilgebunden | P0 | T-01 | PowSyBl-Versionpin; CGMES 2.4.15/3.0 URIs | HOCH: nicht erkannte Profilvariante |
| REQ-002 | MUSS | EQ/SSH, optional/differenziert TP/SV | P0 | T-01, T-02 | PowSyBl State-/TP-/SV-Import; Exchange-Policy | MITTEL: fehlendes TP / falscher solved-Status |
| REQ-003 | MUSS | Single-/Multi-IGM/CGM | P0, P1 | T-03 | PowSyBl CGM Subnetworks; echte Multi-IGM-Fixture | HOCH: inkorrekte Assembly |
| REQ-004 | MUSS | versionsgerechtes EQBD/TPBD/Boundary | P0 | T-03 | Versionierte ENTSO-E-Boundary-Regeln; IGM/CGM-Fixture | HOCH: inkorrekte 3.0-TPBD-Annahme |
| REQ-005 | MUSS | Datei-/Modell-/RDF-/Profilmanifest | P0, P1 | T-01, T-04 | Original-ZIP/XML; FullModel- und SHA256-Metadaten | HOCH: Backend-Metadaten fehlen |
| REQ-006 | MUSS | Original-mRID und eigene IDs trennen | P1 | T-04 | Original-mRID/RDF-Subject und IIDM-Alias-Witness | HOCH: profilübergreifende Identitätskollision |
| REQ-007 | MUSS | unbekannte Attribute nicht still verwerfen | P1, P3 | T-04, T-21 | Originalgraph vollständig gesichert; unbekannte RDF-Felder | HOCH: nicht exponierte Quellattribute |
| REQ-008 | MUSS | deterministischer Reimport/Update | P1, P3 | T-05 | Originalsnapshot und deterministische Config-Hashes | MITTEL: unstabile IDs bei Revisionen |
| REQ-009 | MUSS | backendneutrales Canonical | P1 | T-06 | Zwei unabhängig erzeugte Parser-/BackendSnapshots: PowSyBl + minimaler read-only VeraGrid-Prüfadapter; gleicher Fixture-Graph | HOCH: nicht repräsentierte Backend-Attribute |
| REQ-010 | MUSS | Originalgraph für Export 1 erhalten | P0, P3 | T-21 | Verlustfreies Originalgrapharchiv; Graph-Diff-Witness | HOCH: unbelegter verlustfreier Update |
| REQ-011 | SOLL | GL/DL-Preservation | P0, P1 | T-11, T-21 | GL-/DL-Originalprofile und Python-Geo-Zugriff | MITTEL: nicht verfügbare Profilattribute |
| REQ-012 | OPTIONAL | opake OP/SC/DY-Weitergabe | P0, P1 | T-21 | Optional gelieferte SC/OP/DY-Graphen | GERING: Pass-through nachzuweisen |
| REQ-013 | MUSS | Terminal/Connectivity/TopologicalNode-FKs | P1, P2 | T-07 | PowSyBl-Terminal- und Connectivity-API; EQ-/TP-Fixture | HOCH: unaufgelöste Terminals |
| REQ-014 | MUSS | Switch-/Terminal-/Equipment-Status separat | P1, P2 | T-07 | SSH-Service-/Switch-/Terminal-Zustandsdaten | HOCH: fehlerhafte elektrische Fusion |
| REQ-015 | MUSS | TP gegen EQ/SSH-Topologie | P2 | T-08 | Geliefertes TP plus EQ/SSH-Ableitungsreferenz | MITTEL: divergente TP-Topologie |
| REQ-016 | MUSS | korrekte AC-Inseln | P2 | T-09 | AC-Graph/Slack-Island-Fixtures mit HVDC | HOCH: künstliches AC-Island-Merging |
| REQ-017 | MUSS | Country-/Substation-/VoltageLevel | P1 | T-10 | Substation/VoltageLevel/Country-Authority-Ledger | HOCH: fehlende Länderreferenz |
| REQ-018 | MUSS | Geopositionen inkl. CRS-/Missing-Status | P1 | T-11 | GL-/CRS-Quellwerte oder erklärte Missing-Quelle | MITTEL: ungeprüfte Koordinatenbasis |
| REQ-019 | SOLL | Line-Geometrie/PositionPoints | P1 | T-11 | GL-Line-Routen / mehrfache PositionPoints | MITTEL: Geometrieabdeckung unvollständig |
| REQ-020 | SOLL | abgeleitete Substation-Zentroiden markieren | P1 | T-11 | CRS, Station-Geometrie und Ableitungs-Policy | MITTEL: Zentroiden fälschlich als SOURCE |
| REQ-021 | MUSS | ACLine vs EquivalentBranch | P2 | T-12 | ACLineSegment/EquivalentBranch-Daten; Y-Zweitor-Witness | MITTEL: unzutreffende PI-Parameter |
| REQ-022 | MUSS | 2W/3W-Transformatoren | P2 | T-13 | 2W-/3W-Enddaten; Kron-Y-Referenzfälle | HOCH: Sternmodell elektrisch nicht äquivalent |
| REQ-023 | MUSS | Tap-/PST-Semantik und Control | P2 | T-14 | Ratio/Phase-Tap-Tabellen; PyPSA-Port-Witness | HOCH: Tap-/PST-Richtung falsch |
| REQ-024 | MUSS | Generator/Load/ExternalInjection | P2 | T-15 | CIM-Maschinen-/Load-/ExternalInjection-Attribute | MITTEL: P/Q-/Kontrollsemantik unvollständig |
| REQ-025 | MUSS | Shunt linear/nichtlinear | P2 | T-16 | Linear-/NonlinearShunt-Sections; elektrische Referenz | MITTEL: Stufennichtlinearität vereinfacht |
| REQ-026 | MUSS | HVDC Converter-/DC-Ports | P1, P2 | T-17 | CGMES-Konverter/DC-Port-Objekte und Terminalreferenzen | HOCH: HVDC-Topologie/Regelung approximiert |
| REQ-027 | MUSS | Basis-/Einheitenumrechnung | P2 | T-12, T-13, T-18 | CGMES-Units plus Gerätedatenblattbasen; PyPSA-Pin | HOCH: falsche pu-/Spannungsbasis |
| REQ-028 | MUSS | Status vs. operationelle Limits | P1, P2 | T-19 | SSH-Service-/LimitSet-/Terminal-Daten | MITTEL: Limit mit Status verwechselt |
| REQ-029 | MUSS | Dauer-/Saison-/Richtungslimits | P1, P2 | T-19 | OperationalLimitType, Dauer, Richtung und Saison | HOCH: nicht belastbare Grenzwert-Proxys |
| REQ-030 | MUSS | Missing/Zero/Singularity/Conflict | P2, P5 | T-18 | Null-/Missing- und singularer Gerätefall als Fixture | HOCH: implizite PyPSA-Defaults |
| REQ-031 | MUSS | korrekte P/Q-/Branch-/HVDC-Vorzeichen | P2 | T-15, T-17 | Vorzeichen-/Portkonvention plus KCL/HVDC-Witness | HOCH: falscher Nettofluss |
| REQ-032 | SOLL | RegulatingControls/Capability Curves | P1, P2 | T-15 | RegulatingControl/Q-Kurve soweit geliefert | MITTEL: fehlende vollständige Regelungsdaten |
| REQ-033 | OPTIONAL | erweiterte Generatortechnologie | P1 | T-15 | Kuratierter Technologievokabular-Vertrag | GERING: nichtnormierte Technologielabels |
| REQ-034 | MUSS | versionierte YAML-Mapping-Policies | P2 | T-06 | Validiertes YAML-Schema, Konfigurations-/Hash-Policy | MITTEL: nicht kompatible Policyversion |
| REQ-035 | MUSS | geprüfte Funktions-ID statt YAML-Formel | P2, P5 | T-12…T-18 | Geprüfte versionierte Rechenfunktionen / unabhängige Orakel | HOCH: ungültige Transformationsgleichung |
| REQ-036 | MUSS | SOURCE/DERIVED/DEFAULT/MISSING | P1, P5 | T-04, T-18 | Raw-Werte/Backend-Feldzugang, Wert- und Herkunftsledger | MITTEL: fehlende SOURCE-Belegkette |
| REQ-037 | MUSS | PyPSA detaillierte View | P2 | T-20 | Gepinnte PyPSA-API; geeignete Komponenten-Fixtures | HOCH: nicht darstellbare Sondergeräte |
| REQ-038 | MUSS | aktuelle M1-Adaptergrenzen belegen | P2, P6 | T-20 | Bestehender tyndp_reduce.pypsa_adapter; unabhängiger M1-Test | HOCH: Adapter verweigert 3W/PST/HVDC |
| REQ-039 | MUSS | gefrorenes Originalnetz, getrennte Zeitreihen | P1, P2 | T-20 | Unveränderliche Netzrevision und separate Zeitreihenkennung | MITTEL: unbeabsichtigte Detailnetzmutation |
| REQ-040 | MUSS | identitätstreuer UPDATE_IMPORTED | P3 | T-21 | Source-Graph, Allowlist, Backend-Update-/CGM-Export-API | HOCH: fehlende Inverse/Originalmetadaten |
| REQ-041 | MUSS | CREATE nur bei vollständigen CIM-Daten | P4 | T-22 | CGMES-Serializer + neuer Authority-/CIM-Konstruktionsvertrag | HOCH: unvollständiges synthetisches EQ/TP |
| REQ-042 | MUSS | eigener Loss Contract pro Exportmodus | P3, P4 | T-21, T-22 | Originalgraph & Target-Field-Matrix für beide Exportmodi | HOCH: nicht rekonstruierbare Informationen |
| REQ-043 | MUSS | Import-/Export-Capabilities getrennt | P5 | T-21…T-24 | Backend-/Profil-/Fixture-gebundene Quality-Witnesses | MITTEL: Capability-Übertragung ohne Beleg |
| REQ-044 | MUSS | atomare Exporte, reproduzierbares Audit | P3, P4, P5 | T-05, T-22 | Atomarer Filesystem-/DB-Commit; Staging-/Audit-Manifest | HOCH: Teil-Export nach Fehler |
| REQ-045 | MUSS | Validierung von Profil/Boundary/Elektrik/LF/RT | P5 | T-01…T-24 | T-01…T-24-Fixture-Suite und unabhängige elektrische Referenzen | HOCH: reale Backend-/Netztests fehlen |
| REQ-046 | SOLL | qualifizierte SV-AC-Referenz | P5 | T-23 | Gelöstes geeignetes EQ/SSH/TP/SV und Solver-Pin | MITTEL: inkompatibler SV-Betriebspunkt |
| REQ-047 | SOLL | Massen-/Partitionierungs-/Spaltenleistung | P1, P5 | T-24 | Lizensierter großer CGM; RAM-/Laufzeitinstrumentierung | MITTEL: Speicherbedarf unbekannt |
| REQ-048 | OPTIONAL | Data-Quality-Dashboard | P5 | T-24 | Versionierte QA-Metriken und Reporter | GERING: Dashboard optional |

**MUSS-Abdeckung:** 39/39 erhalten explizite Architektur-/Implementierungsowner, separate externe Voraussetzungen/Risiken und geplante Testzuordnung. Die zuvor zusammengefassten Test-/Witness-Spalten sind in dieser konsolidierten M3-Korrektur in **sieben maschinenlesbare Tabellenfelder** aufgelöst. REQ-009 bleibt **MUSS**; T-06 benötigt unabhängige BackendSnapshot-Parität (85 §6). Alle REQ-X01…REQ-X08 bleiben **AUSSERHALB DES SCOPES** (keine positiven Implementierungsgates). Die Tabelle ist **Plan-Traceability**; kein Test ist damit ausgeführt. Bei der Implementierung muss später die REQ→Test→Fixture→Evidenz-Traceability pro Zeile maschinenlesbar ausgegeben werden.

## 5. Alle T-01…T-24, Fixtures und Negativfälle

Die Details und vorgeschlagenen numerischen internen Toleranzen in `50_VALIDATION_CONTRACT.md` bleiben maßgeblich. Hier werden Testpakete zugeordnet, sodass keine kleinen Subchats für Testfälle nötig sind.

| Tests | Inhalt und relevante Fixture | Definierte Capability |
|---|---|---|
| T-01 / T-02 | `F04`: 2.4.15 und 3.0 Profiles/Headers, unsolved vs solved/SSH update | FORMAT / CANONICAL |
| T-03 | `F04/F08`: Multi-IGM, Authority, versionierte Boundary, 3.0 ohne TPBD | FORMAT/IDENTITY |
| T-04 | `F04`: MRID/RDF-Subject/cross-profile, opaque attrs, Identity-Kollision negativ | IDENTITY |
| T-05 | `F04`: deterministischer Reimport, optimistischer Delta-Konflikt | IDENTITY/UPDATE |
| T-06 | `F04`: **zwei unabhängig durch verschiedene Parser erzeugte** BackendSnapshots + YAML/Canonical-Parität; minimaler read-only VeraGrid-Prüfadapter verpflichtend für Import-READY | CANONICAL PARITY; nicht optional für REQ-009 |
| T-07 / T-08 | `F02`: NODE_BREAKER ON/OFF/normalOpen, **BUS_BRANCH mit TP bzw. fehlendem TP (BLOCK)**, TP-/SSH-Abweichung | TOPO; Originalhierarchie und Terminalport-Witness |
| T-09 | `F02/F05`: AC-Islands, HVDC, Slack/Balance | TOPO/ELECTRICAL |
| T-10 / T-11 | `F04/F06`: country endpoints, synthetic-star NULL, CRS/GL-/Missing-Policy | GEO |
| T-12 | `F01`: AC-Line PI, Ohm/Siemens, EquivalentBranch/Portumkehr | ELECTRICAL |
| T-13 / T-14 | `F03`: 2W/3W, Ybus, RatedU, Ratio/PST und ±φ | ELECTRICAL |
| T-15 / T-16 | `F01/F03`: P/Q-zeichen, Generator/PV/PQ/Slack, Shunts/ZIP | ELECTRICAL |
| T-17 | `F05`: HVDC forward/reverse loss, two AC islands, MTDC unsupported | ELECTRICAL |
| T-18 | `F01/F03`: Units/Base/Missing/Zero/NaN/singular | ELECTRICAL |
| T-19 | `F06`: Grenzen nach Dauer, Terminal, Richtung, Saison | ELECTRICAL |
| T-20 | `F01/F03/F05`: Detailed PyPSA, line-only positiv, komplexe M1-Adapter-REJECTION negativ | PYPSA / M1 |
| T-21 | `F07`: originalgraphbasierter unchanged/delta reimport; Unknown Attr/Boundary; **CGM_QUICK_SSH_SV ohne geeigneten SV BLOCK**, MANUAL_IGM_SSH nur mit Header-/Python-/Graph-Witness | UPDATE EXPORT; SSH-only nie Quick-CGM |
| T-22 | `F07`: synthetischer CREATE mit vollständiger/unvollständiger Authority-/CIM-Spezifikation | CREATE EXPORT |
| T-23 | `F01/F08`: eligible solved SV/PF, KCL, P/Q/V/Angle, gezielte Inkonsistenz | SV REF |
| T-24 | `F07/F08`: Quality-/ProjectionLoss-Metadaten, Versionspins, **Crash/CAS/Retry/Orphan/Hash-/Recovery-Fixtures** und skalierte Performanceberichte | OPS/QA; vor Ausführung Budget-/Rechtepolicy pinnen |

**Verbindliche Fixturepolicy:** `F01` einfacher stationärer AC-Test, `F02` Switch-/TP-Topologie, `F03` 2W/3W/Tap/PST, `F04` IGM/CGM/Boundary/Identität, `F05` AC-Inseln mit HVDC, `F06` Limits/GL/CRS, `F07` Export-Profilpakete, `F08` lizenzierter echter CGMES-CGM/IGM-Fall. Im PoC müssen beide CGMES-Versionen getrennt mit Version/Profil-URI/Hash und Datasetlizenz qualifiziert werden; Release-/Profilabdeckung darf nicht aus einem Test einer einzigen Familie extrapoliert werden. Negative Fixturefälle (fehlerhafte Referenz, mRID-Kollision, unbekannter Tap, unvollständige Konstruktionspflichten) gehören zum Mussumfang der jeweiligen qualifizierten Capability. RealGrid-Größe oder die im SOPTIM-README behaupteten Fremdtests sind **keine hier ausgeführte Evidenz**.

**Initiale numerische Schwellen** NUM-01…NUM-09 aus `50` sind Vorschläge, deren Einheiten-/Konditions-/Rundungs-Guards und reale Referenzqualität im PoC belegt werden müssen. Kein universeller AC-SV-Abnahmefehler aus einer einzigen Faustregel. `source_untouched_triples_changed_count=0` betrifft definierte, nicht veränderte semantische Quellmodelle bzw. unveränderte pass-through graph scopes, nicht eine pauschale byteidentische Ausgabe; XML-Reihenfolge und Präfixnamen sind kein semantischer Unterschied.

## 6. Vier gebündelte Implementierungs-/Qualifikationsmakros nach späterer Owner-Freigabe

### PoC-M1 — Import/Canonical/Kernmodell

**Pflicht aus M3-P1-05:** PoC-M1 kann den ersten PowSyBl-Import zunächst als CANONICAL_IMPORT_PROVISIONAL liefern. Für `CANONICAL_IMPORT_READY` gehört ein eigener unabhängig erzeugter zweiter read-only BackendSnapshot (T-06; minimaler VeraGrid-Prüfadapter genügt) jedoch **verpflichtend** in denselben Qualifikationsumfang. Ein voller alternativer produktiver VeraGrid-Backenddienst bleibt optional. **Auftrag in einem Makro:** P0 + P1 + Kern-P2 + P5. Backendversionen/Core/PyPSA pinnen, geeignete 2.4.15 und 3.0 EQ/SSH(+TP, plus erforderliche Boundary) synthetische/lizenzierte Referenzfälle verwenden, immutable Original, Source Graph/ID-Ledger, Canonical/SQLite, Geobasis/Status, Line/Generator/Load/2W sowie einfache PyPSA-View. Die Interface-Verträge aller künftigen Module bleiben implementierbar, werden aber nicht künstlich als vollständige Prototypen angelegt.

**Akzeptanz:** T-01…T-12, T-15, T-18, T-20 nach Kernfixture und capability-spezifischer Liste; 2.4/3.0-Version- und Boundary-Checks; dokumentierte Ablehnung statt stiller Sonderkomponentendrops. Erreichbare erste Stufe: `CANONICAL_IMPORT_PROVISIONAL` ohne T-06; `CANONICAL_IMPORT_READY` **erst nach unabhängigem T-06** und allen relevanten Tests, danach ggf. ein **eng begrenztes** `PYPSA_ACPF_READY` für tatsächlich geprüfte Geräte. BUS_BRANCH erfordert TP, NB kann TP nachweisbar ableiten; kein Source-Country aus repräsentativer IIDM-Station. Kein Export-PASS.

### PoC-M2 — Sondergeräte, Multi-IGM/Boundary und Elektrik

**Normatives Schema:** 85 §§1–4 verlangt exportunabhängiges projection_quality/witness-Register, SourceHierarchy und beide TopologyKinds sowie getrennte Source-/State-/Canonical-/Projection-IDs. **Auftrag in einem Makro:** Vollständige P2-Gerätequalifikation: 3W-Stern-Y, Ratio-/Phase-Tap, PST-Offsets, Shunts, Generator Control, externe Netze, HVDC-Port/Loss-/Fahrtrichtungsmodelle, mehrdimensionale Limits, Geo/CRS, echte Multi-IGM-Assembly, elektrische Qualifikation von PyPSA-ACPF und LPF. Keine Integration der Zeitreihen oder Netzreduktion als verdeckte Zusatzaufgabe.

**Akzeptanz:** T-03, T-07…T-20 und T-23, falls Referenz-SV tatsächlich geeignet. Genau ausgewiesene EXACT/APPROX/UNSUPPORTED pro Gerät; T-17 muss Reverse-Efficiency-Fehler ablehnen. Fehlende M1-Adapter-Fähigkeit bleibt `REDUCTION_ADAPTER_READY=NOT_ASSESSED/BLOCKED`, nie implizit grün.

### PoC-M3 — Graphbasierter Update-Export

**Auftrag in einem Makro:** P3; per Backend/CGMES-Version belegte `supported_write_fields`, Originalgraph-Lebenszyklus, eindeutiges mapping back zu Source IDs, SSH-/SV-Profilgenerierung samt Modelheader/Dependencies, Graph-Diff, atomare Freigabe, No-Delete-by-Omission, Cross-IGM-/Boundary- und unbekannte-CIM-Attribut-Gates. **Explizite Routen gemäß 85 §5:** CGM_QUICK_SSH_SV gibt immer IGM-SSH und CGM-SV aus, nur bei validem tatsächlich neu gelösten SV; MANUAL_IGM_SSH für SSH-only erfordert eigene Python-/MAS-/FullModel-/Dependency-/Graph-Diff-/Reimport-Qualifikation, sonst BLOCK. Kein Profilfilter über Quick und kein ungeprüfter SV. Die Deltaklassen STATE_NON_TOPOLOGY/STATE_TOPOLOGY_AFFECTING/STRUCTURAL_EQ_TP/SYNTHETIC_CREATE besitzen jeweils eigene Sperren.

**Akzeptanz:** T-05, T-21 und T-24 für beide Versionen/qualifizierte Profile, einschließlich negativem SSH-only/Quick-CGM, Nicht-Invertierbarkeit sowie crash-/CAS-/Retry-/Recovery-Fixtures; neues SV nur zusätzlich nach eligible T-23. `UPDATE_EXPORT_READY` **nur** falls der konkrete PowSyBl-Pfad Originalidentitäten-/Graph-Witness tatsächlich liefert; sonst `BLOCKED` mit ausgewiesener Alternative/Downscope, kein stiller eigener XML-Patcher.

### PoC-M4 — Create-Export, Performance und Folgeadapter

**Operative Vorbedingung P2-04:** Vor Ausführung versioniert fixierte ZIP/XML-Sicherheits-, CPU-/Timeout-/JVM-RAM-/FS-Recovery-/Datennutzungs- und realistische Performance-Budgets gemäß 85 §9; bei fehlenden Werten bleibt QUAL-OPS-PERF/SECURITY/DATASET gesperrt. **Auftrag in einem Makro und nur separat freizugeben:** P4 + erweiterte P5-QA und ggf. Owner-getrennter M1-Adapter. Der generische Synthetic-Export aus vollständiger PyPSA-/Authority-/Equipment-Konstruktion wird eigenständig qualifiziert; Performance- und echte europäische Multi-IGM-Testsets nur mit zulässigen Datennutzungsrechten. Eine Änderung des aktuellen M1-Reduktionsadapters ist ein **eigener**, ausdrücklich autorisierter Folgeauftrag und darf nicht durch M0-Create-Export ausgelöst werden.

**Akzeptanz:** T-22/T-24, vollständige EQ-/TP-/SSH-Profile mit kontrollierten mRIDs, ggf. SV nur nach tatsächlichem AC-PF, unabhängiger Reimport. `CREATE_EXPORT_READY` ≠ nachgewiesene ursprüngliche TSO-IGM-Äquivalenz; Performance und `REDUCTION_ADAPTER_READY` separate Gates.

## 7. M3-Review-Gate, Freigabelogik und Entscheidungsbefugnis

**Historischer M3-Prüfvertrag, tatsächlich abgeschlossen am Commit ea62050a867c27036552af28d3e0102a8689f4ec (REPAIRS_REQUIRED; sieben P1):** Der unabhängige statische Reviewer prüfte vollständig `00/10/20/30/40/50/60/70`, echte GitHub-Blobs/Commit und keine erfundene Evidenz. Er prüft Architektur/API-Konsistenz, sämtliche K-01…K-07, REQ-001…REQ-048, alle Pflicht-Traceabilitys, alle 24 T-Cases, CGMES-3.0/2.4.15-Profile, IDs, SourceGraph/Export, M0/M1-Grenze und Dokumentwidersprüche. Ohne Code-/Solver-/Parser-Ausführung, ohne Korrektur produktiver Dateien. Ergebnis `80_INDEPENDENT_ARCHITECTURE_REVIEW.md` auf eigenem Branch (M3-Handoff wird S-GOV nach verifiziertem M2-Commit ausgegeben).

**M3 kann** `PASS` / `CONDITIONAL_WITH_NAMED_GAPS` / `REPAIRS_REQUIRED` beurteilen; bei P0/P1 wird maximal ein konsolidierter Korrekturdurchgang durch S-GOV empfohlen. Ein statischer PASS bedeutet `ARCHITECTURE_FROZEN_FOR_IMPLEMENTATION_PLANNING`, **nicht** `CANONICAL_IMPORT_READY` oder `UPDATE_EXPORT_READY`. Die spätere ausdrückliche Ownerfreigabe ist vor PoC-M1 bis PoC-M4 einzuholen; keine Asynchron-/Auto-Ausführung der Umsetzungsaufträge.

### M3-Korrekturpaket: Freigaberelevante Nachträge (Referenz zu 85)

- **CAN/2.0.0:** tatsächlich bindendes Tabellenregister für mRID-lose Source-Objects, Occurrences, Country- und TopologyKind-FKs sowie Source-/OperatingState-/Canonical-/Projection-Revisionshashes.
- **ProjectionQuality:** eigenständige append-only, exporttransaktionsunabhängige EXACT/APPROX/UNSUPPORTED/Witness-Evidenz.
- **Export:** MANUAL_IGM_SSH und CGM_QUICK_SSH_SV sind unterschiedliche, getrennt zu qualifizierende Upstream-Routen; SSH-only ist nicht Quick.
- **Persistenz:** einzige SQLite-COMMITTED-Pointer-Sichtbarkeit nach durable Blob-/Manifest-Staging, CAS, Crash-/Retry-/Orphan-Policy.
- **DNR/1.0.0:** typisierter Referenz-Handshake mit obligatorischer Original-/View-/Unit-/Port-/Limit-/Sidecar-Provenienz. `REDUCTION_ADAPTER_READY` ist nur ein späterer unabhängiger M1-E2E-Nachweis.
- **REQ-009:** T-06 bleibt Pflicht; ohne unabhängige Zweitbackend-Parität kein READY, nur PROVISIONAL. Die ursprünglichen **48 REQ**, 39 MUSS und T-01…T-24 bleiben erhalten.

## 8. Versions-/BOM- und Reproduzierbarkeitsregeln

Vor dem ersten M4-PoC erfassen und pinnen: tatsächliche `PyPowSyBl`-Releaseversion, kompatibles PowSyBl-/Core/CGMES-Modul, verfügbare Import-/Exportformate/Parameter, Python- und Java-/Native-Runtime-Version, PyPSA Version (bestehender Projektbereich `pypsa>=1.4,<2` **nicht als installierter Befund**), SQLite-/Pandas-/Unit-/CRS-/XML-Sicherheitsabhängigkeiten, Schema- und Mappingvertrag, Datenfixture-Rechte/Hashes/Profil-URIs/Authority. VeraGrid-Version wird nur bei aktiviertem Fallback-PoC gepinnt. Paket-Lizenzen (MPL-2.0 / Apache-2.0 / PyPSA MIT u. a.) und Verbreitungsbedingungen getrennt verifizieren; keine Redistribution realer CGMES-IGMs ohne Nutzungsfreigabe.

**Negative technische Ausführungsannahmen:** Keine automatischen API-Konvertierungen für unbekannte CGMES-Sonderklassen; keine Vollständigkeit durch gemappte Pfade allein; kein Formatwechsel ohne Canonical-Paritätscheck; keine unsichtbare Erstellung von Slack/Limit/Country/GL; keine volle lossless round-trip Behauptung; kein serielles Vollnetz in einem nativen GUI-abhängigen Arbeitsprozess, wenn Backend-CLI/API genügt.

## 9. M2-Abschluss-Check

| Kriterium | Entwurfsstatus |
|---|---|
| Vier Fachberichte und S-GOV-Evidenz berücksichtigt | `DOCUMENTED` |
| K-01…K-07 explizit entschieden | `DOCUMENTED_IN_60` |
| Architekturschichten/APIs/Port/Routing/Sequenzen definiert | `DOCUMENTED_IN_40` |
| 39 MUSS mit Modulowner + T abgebildet | `DOCUMENTED_IN_70` |
| T-01…T-24 mit Fixture-/Capability-/Negativrollen | `DESIGNED_NOT_EXECUTED` |
| Primär/Fallback/technische Grenzen | `DOCUMENTED_IN_60` |
| UPDATE_IMPORTED vs CREATE_FROM_PYPSA | `SEPARATE_CONTRACTS` |
| Physische PoC-Persistenz, Canonical/Source ID, Länder | `DESIGN_ADOPTED_PENDING_REVIEW` |
| Modul-1-Adapter Grenze | `SPECIFIED_UNQUALIFIED` |
| Runtime-/CGMES-/PyPSA-/Export-Konformität | `NOT_ASSESSED` |

**Historische M2-Disposition:** `M2_ARCHITECTURE_DESIGNED_READY_FOR_INDEPENDENT_STATIC_REVIEW`, *sofern* alle drei neuen Dokumente vollständig und unverändert am finalen Commit lesbar sind und keine P0-Stellen im statischen Crosscheck verbleiben. Dies ist ein Governance-Dokument-Status, **kein ausgeführter technischer Gate-PASS**.

**Fundament:** [Requirements](10_REQUIREMENTS.md), [Backend](20_BACKEND_ASSESSMENT.md), [Canonical](30_CANONICAL_DATA_CONTRACT.md), [Validation](50_VALIDATION_CONTRACT.md), [Architecture](40_SOFTWARE_ARCHITECTURE.md), [ADR](60_ARCHITECTURE_DECISION.md).
