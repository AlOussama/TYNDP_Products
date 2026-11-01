# M4-0 — RunRelease-, Security-, Daten- und Qualifikationsvertrag

**Projekt:** IoSN / TYNDP / PyPSA — Modul 0  
**Datum:** 2026-11-01  
**Fachgrundlage:** [85 Normative Repairs](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md), [90 Freeze](90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md), [95 M4-0 Upstream/Fixture Witness](95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md), [50 Validation](50_VALIDATION_CONTRACT.md).  
**Endstatus M4-0:** `M4_0_STATIC_PREFLIGHT_COMPLETE; IMPLEMENTATION_AND_RUNTIME_RUNRELEASE_NOT_YET_GRANTED`.

## 1. Ausführungsautorität

M4-0 ist ein **durchgeführtes dokumentarisches Ausführungs-/Datenvorbereitungs-Makro**. Die unten beschlossenen Policies und identifizierten Quellressourcen werden für die späteren Worker zu verbindlichen Preconditions. **Nicht** erfolgt sind: Installation der Runtime, tatsächliche Backend-Import-/Exportaufrufe, Hostmessung, Fixture-Import, Originalgraph-Fidelity-Beleg, T-06, Lastfluss, Safety-Failure-Injection, PoC-Codeänderungen, Merge oder Produktivfreigabe.

Ein **separater ausdrücklicher Owner-/Nutzerentscheid** autorisiert die spätere Implementierung und Testausführung. Ein künftiger PoC-Auftrag darf nach diesem Entscheid im selben Makro seine G0-Host-/Dataset-Preflight durchführen und bei PASS direkt implementieren; bei einem Blocker muss er den betroffenen technischen Pfad **nicht** durch stillen Fallback umgehen. Damit wird kein zusätzlicher allgemeiner Architekturreview oder Micro-Iteration ausgelöst.

S-GOV gewährt hier **keinen unbedingten Runtime-RunRelease**, da Host-/Native-Version, Lizenz-/Entitlement-Matrix und Fixture-Inventar noch nicht ausgeführt bzw. bestätigt sind. PoC-M1 kann auf eigenem Branch eine **explizit autorisierte**, isolierte Probe-/Implementierungsumgebung aufbauen, sobald ein entsprechender Nutzerauftrag vorliegt.

## 2. Bindendes G0-Preflight-Gate für jeden späteren PoC-Worker

| Gate-ID | Eingang / messbare Ausführung | PASS-Voraussetzung | Fail-Policy / heutiger Stand |
|---|---|---|---|
| G0-SOURCE | Immutable M0-Baseline, 85/90/95/96/97-Referenzen, Branch/Commit-SHA | alle relevanten Gitblobs verifiziert; kein unzulässiger Rebase/Merge | `STATIC_PASS` für Baseline; neue Folgecommits erneut prüfen |
| G0-BOM | CPython/OS/ABI, `pypowsybl==1.16.1`, `pypsa==1.4.0`, unabhängiger `VeraGridEngine==6.7.20`-Prüfpfad | installierte Paketversionen **und transitive** OS-spezifische Wheel-/sdist-Hashes, Native-Core-Fingerprint, `pip freeze`/SBOM, reproduzierbarer Resolver-Lock | `NOT_ASSESSED_RUNTIME`; beim PoC fehlende Installierbarkeit ⇒ BLOCK für betroffene Capability |
| G0-API | echte Format-/Options-/Header-/ID-/Terminals-/SourceGraph-Lesezugriffe und Export-Profilrouten | versionsgenauer API-Discovery-Report mit Quellbelegen und tatsächlichen Probeoutputs, keine erdachten Python-Methoden | `STATIC_ONLY`; Update-Export-Route bleibt BLOCK bis eigener Witness |
| G0-DATA | konkrete Originalfixture-Dateien + SHA-256 + actual CGMES family/profile URIs/FullModel + Boundary/Authority/State | vollständig inhaltlich inventarisiert; keine F03/F04/EQBD/TPBD-Pflicht aus Dateinamen abgeleitet | `SOURCE_EXISTS_LICENSE_PENDING`; nicht verfügbare Profilreferenz BLOCK des entsprechenden Datensatzscopes |
| G0-RIGHTS | Permission-/Lizenz-/Verwendungs-/Weitergaberegister pro Datensatz | vom Worker einsehbare dokumentierte zulässige Nutzung, Ablage- und Redistributionspolicy; keine unbekannt berechtigte Realnetzdatei im öffentlichen Repo | `RIGHTS_UNVERIFIED`; ohne Klärung keine fragliche Originaldatennutzung oder Veröffentlichung |
| G0-SAFETY | Komprimierungs-/XML-Policy, Prozesslimits, Temp/Hash-/Filesystemschutz | technisch durchsetzbare und negativ testbare Limits vor Verarbeitung untrusted/large files | `POLICY_DEFINED_NOT_IMPLEMENTED` |
| G0-PUBLISH | Storage-/SQLite-/CAS-/Blob-fsync-Profil und Recovery-Fälle | vor jeder öffentlich freigegebenen Revision/Cgmes-Delivery passende T-05/T-21/T-22/T-24-Evidenz | `DESIGNED_NOT_EXECUTED`; keine Atomizitätsbehauptung |
| G0-QUAL | Fixture/Test/Capability-Matrix gemäß 50/70/85 | Testliste, Fixturehashes, Herkunft, erwartete Soll-/Negativfälle, numerische Guards, Ergebnisschema festgelegt | `DESIGNED_NOT_EXECUTED`; ein parse-PASS ist kein elektrisches/PyPSA-PASS |

**Entscheidungsmodell:** `STATIC_PASS` (belegte Fakten/Dokumente) ≠ `RUNTIME_PASS` (tatsächlich ausgeführt) ≠ `CAPABILITY_PASS` (gesamter benannter Testscope vollständig bestanden). `BLOCKED` und `NOT_ASSESSED` bleiben zulässig und verhindern Fehlclaims.

## 3. Konservative, numerische Referenzbudgets für kleine F-01…F-07-Fixtures

**Policy-ID:** `M0-OPS-SMALL-V1.0.0`. Dies sind hier getroffene **ingenieurmäßige Schutz-/Abbruchvorgaben**, **keine gemessenen Performancewerte**. Sie gelten nur für die autorisierte kleine synthetische/CAS-Fixture-Qualifikation; F-08 (großes echtes CGM) bekommt ein neues, explizites Budget auf Basis der berechtigten Datengröße. Wo OS- oder native Backendmechanismen die Limits nicht durchsetzen können, dürfen sie nicht als erfüllte Security-Gates ausgegeben werden.

| Mess-/Sicherheitsgröße | Initiales Schutzbudget (kleine Fixtures) | Durchsetzung / Abbruch |
|---|---|---|
| Einzelnes ZIP/komprimierte Lieferung | maximal **256 MiB** | Abweisung vor Dekompression |
| Kumulierte unkomprimierte Daten eines Imports | maximal **1 GiB** | Streaming-Zählung vor/bei Extraktion, harte Abweisung |
| Dekompressionsverhältnis einer Datei und insgesamt | maximal **25:1**, Ausnahmen nur als neu freizugebende Rule-Version | ZIP-Bomb-Abweisung, keine stillen Ausnahmen |
| Anzahl ZIP-Mitglieder pro Lieferung | maximal **2.000** | Eintragzählung vor Processing |
| Einzelnes XML/ZIP-Member | maximal **128 MiB** | per Member harte Grenze |
| Relative Pfadtiefe beim Auspacken | maximal **16 Komponenten** | normalisierte Paths, kein `..`/absolute Paths/Drive/UNC/ADS, keine Links oder out-of-root Symlinks |
| XML-Parsing-Security | externe Entities/DTD/Netzauflösung **verboten**; keine undefinierte Entity-Expansion | Parser-Härtung oder sandboxed reject; Fuzz-/Negativfixture |
| Prozess-Parallelität | **1** Import-/Export-Worker pro isolierter Fixture-Session, maximal **4 CPU-Threads** | Limit/Report; Parallelisierung nur nach eigenem Bench-Gate |
| Peak RSS / Native plus Python für kleinen PoC | Budget **8 GiB**, 10%-Reserve und klare Messmethode | überwachen, Abbruch vor unkontrolliertem Speicherverbrauch; native GraalVM-Last separat ausweisen |
| Java-Heap (nur bei separatem Java-Prozess) | maximal **4 GiB**, **nicht** automatisch für Python-Native-Wheel anwendbar | Heap-Grenze nur bei echter JVM-Session; native footprint anders erfassen |
| Wallclock pro kleiner Import-/Exportfixture | **600 s**; pro maschineninternem Einzelprozess | Prozess nach Frist abbrechen, gesicherter Rollback/Quarantäne |
| Freier Scratch-Speicher | mindestens **4 GiB** vor dem kleinen Run; benannter Stage-Root mit per-Run-Quota | BLOCK vor Run bei unzureichendem Platz |
| Logs/Manifest | nur gehashte/zugelassene Paths, keine sensitiven Inhalte/Token; UTC-Zeitstempel | Sorgfältige Redaction, Zugriffskontrolle, Git-Commit nur ohne Original-Netzdateien |

**Hinweis:** 600 Sekunden, 8 GiB oder 25:1 sind **Schutzbudgets**, keine versprochenen Import-/Lastflussleistungen. Ein qualitativer Performance-PASS benötigt zusätzlich vorab festgelegte messbare Zielgrößen und einen geeigneten vollständigen Dataset-/Maschinenkontext. Bei legitimen, über Budget liegenden Testdateien darf nach neu versionierter Policy ein größerer Run genehmigt werden; das initiale Limit ist kein fachlicher Netzfehler.

## 4. Reproduzierbare technische Runtime-Spezifikation (zu materialisieren)

Spätere Worker erstellen ein maschinenlesbares Manifest **pro tatsächlichem Run** (kein leeres Platzhaltermanifest als PASS):

~~~json
{
  "schema": "iosn-m0-runtime-preflight/1.0.0",
  "repository_commit": "<immutable-consumed-git-sha>",
  "policy_id": "M0-OPS-SMALL-V1.0.0",
  "os": "<name-build-arch>",
  "python_executable_sha256": "<sha256>",
  "python_version": "<actual-full>",
  "dependency_lock_sha256": "<sha256>",
  "pypowsybl_version": "<actual>",
  "pypowsybl_native_build": "<actual-or-UNKNOWN>",
  "powsybl_core_cgmes_version": "<measured-or-UNKNOWN>",
  "pypsa_version": "<actual>",
  "veragridengine_version": "<actual-if-T06>",
  "wheel_hashes": {"<exact-platform-filename>": "<sha256>"},
  "fixture_manifest_sha256": "<sha256>",
  "fixture_license_status": "<verified-allowed-or-BLOCKED>",
  "limits": {"zip_mib": 256, "inflated_mib": 1024, "max_ratio": 25, "max_members": 2000, "max_member_mib": 128, "cpu": 4, "rss_gib": 8, "wall_seconds": 600},
  "network_egress_policy": "DENY_DURING_UNTRUSTED_XML_PARSE",
  "capability_results": [],
  "execution_status": "NOT_EXECUTED"
}
~~~

Der PoC muss die Platzhalter **vor einer tatsächlichen RunRelease** ersetzen. Keine Original-TYNDP-, ENTSO-E-, CGMES-TSO- oder Personen-/Zugangsdaten in öffentlichem Git speichern. Sensible Fixture-Inhalte in separatem privat verwalteten Raw-Data-Store; öffentliche Evidenz besteht aus erlaubten Hash-/Descriptor-/Testdaten mit Entitlement.

## 5. Import- und Persistenz-Testpolitik

**Format/Identity/Topologie:** T-01…T-11 mit beiden tatsächlichen Profilfamilien, FullModel/MAS/Boundary, validem NODE_BREAKER und BUS_BRANCH+TP; Bus/Branch ohne TP BLOCK; identische Quellidentität EQ/SSH nicht doppeln; mRID-lose RDF-Subjekte und lokale BlankNodes erkennen; original Country nicht aus IIDM-Sammelstation erraten.

**T-06 (MUSS):** Zwei echte unabhängig erzeugte Snapshots des **selben Originaldatensatzes**, Primärpfad PowSyBl und Minimalprüfpfad VeraGrid; vergleichen normalisierte SourceEntities, Terminal-/Equipment-Referenzen, elektrische Werte mit expliziter Einheiten-/Toleranzpolicy sowie FKs/Origins. Difference-ledger je Feld/Quelle; bei Nichtparität kein `CANONICAL_IMPORT_READY`, sondern `CANONICAL_IMPORT_PROVISIONAL`. Voller zweiter Produktionsbackend ist nicht erforderlich.

**Elektrik/PyPSA:** T-12…T-20 mit unabhängig qualifizierten NUM-01…NUM-09-Guards aus 50. Je Device/Field `EXPECTED_EXACT`, `APPROX` oder `UNSUPPORTED`; ein `EXACT`-Runtimeurteil nur bei tatsächlich durchgeführtem passendem Witness. Jeder elektrischen View gehört eine **exportunabhängige** ProjectionQuality-Tabelle/Sidecar und ein eigener Revisionshash.

**Export:** CGM-Quick-SSH/SV unterscheidet sich von manuellem IGM-SSH-only. Eine neue SV-Seri­alisierung benötigt tatsächlich geeignete LF-/State-Variable-Evidenz, keine Schätzung aus SSH. UPDATE_IMPORTED/CREATE_FROM_PYPSA haben getrennte Gates und separate Manifest-/Loss-/SemanticDiff-Nachweise. F-07 Negative: falsches SV/Quick-Profil, nicht verfügbare Manual-Bridge, unbekannte RDF-Relationen, nicht inverse synthetische Star-/HVDC-Werte.

**Storage/Atomizität:** für M0-PUBLISH/1.0.0 [85 §7](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md) gilt: vollständige Immutable-Blobs + Manifest **durabel vor** SQLite-CAS-Pointercommit; nur DB-COMMITTED-Pointer macht Lieferung sichtbar. Pflicht-Injection: Crash vor Blob-Fsync, nach Blob/vor Manifest, nach Manifest/vor DB-Commit, nach DB-Commit/vor Antwort; zwei konkurrierende Writer; gleicher Idempotenzkey mit gleichem bzw. anderem Payload; corrupted committed Blob; GC/Leases. Ohne tatsächlichen Nachweis **keine** `QUAL-UPDATE-EXPORT`-/`QUAL-CREATE-EXPORT`-Atomizitätsfreigabe.

## 6. Capability-Zuordnung und Stopregeln

| Ziel | Frühestmögliche positive Aussage | In keinem Fall daraus ableiten |
|---|---|---|
| `CANONICAL_IMPORT_PROVISIONAL` | Einfache geprüfte Primärdaten-/Canonical-Fälle, T-06 noch offen | `CANONICAL_IMPORT_READY` |
| `CANONICAL_IMPORT_READY` | Passende T-01…T-11 einschließlich **unabhängigem T-06**, vollständiger identitäts-/version-/fixturegebundener Nachweis | PyPSA LF/LPF, Export oder M1 |
| `PYPSA_ACPF_READY` | zusätzlich tatsächlich geprüfte elektrisch relevante T-12…T-20, Snapshot/Islands/Slacks und ggf. T-23 | universelle historische CGMES-Gleichheit |
| `PYPSA_LPF_READY` | zusätzlich qualified effective x_pu und PST-/HVDC-/Tap-/Island-Offsets | REDUCTION_ADAPTER_READY |
| `UPDATE_EXPORT_READY` | getrennt nach Route/Profil und T-05/T-21/T-24, ggf. T-23, Graph-Diff/Original-IDs/Manifest/Atomicity | CREATE_EXPORT_READY |
| `CREATE_EXPORT_READY` | vollständige neue CIM-Konstruktion, T-22/T-24, neuer Originalnetzanspruch ausdrücklich ausgeschlossen | historische TSO-IGM-Identität |
| `REDUCTION_ADAPTER_READY` | gesonderter M1-End-to-End-Test T-20 auf tatsächlichen Komponenten | automatisch aus M0-DNR/ACPF/LPF |
| `QUAL-OPS-PERF` | gemessene Multi-IGM-/6k+-Bus-Benchmarkwerte auf lizenziertem F08 und eigenem versioniertem großen Budget | Performance aus MicroGrid oder einem nicht ausgeführten Test |

Für **F08** gilt bis zu konkreter Rechtefreigabe, Dataset-SHA-256, Varianten-/Authority-/Profileinventory und separatem großen Ressourcenbudget: `BLOCKED_FOR_REAL_CGM_EXECUTION`. Es wird keine stillschweigende Ersatzvalidierung durch die fünf Wetterjahre oder PECD vorgenommen.

**Machine-readable Input für künftige Worker:** [98_M4_0_PREPARED_EXECUTION_CONTRACT.json](98_M4_0_PREPARED_EXECUTION_CONTRACT.json) (statisch vorbereitet, kein Runtime-Resultat). Der Worker darf die dortigen Kandidaten nicht ungeprüft als erfolgreiche Host-Pins ausgeben.

## 7. Abschlussdisposition M4-0

| Auftragsteil | Status am 01.11.2026 |
|---|---|
| M0-M2/M3-Freeze- und CAN/DNR-Vertrag verifiziert | `STATIC_PASS` |
| Python/PyPSA/PyPowSyBl/VeraGridEngine-Kandidaten und Artefakt-Hashes recherchiert | `RELEASE_VERIFIED` |
| Original-CGMES-Dateien in zwei Familien gezielt am festen Upstream-Git-Commit nachgewiesen | `SOURCE_VERIFIED`; Lizenz/Bundle-Hash offen |
| F-01…F-08 und spezielle Negativfixtures klassifiziert | `PLAN_COMPLETE_NOT_EXECUTED` |
| Versionierte kleine Resource-/Security-Budgets, Isolation und Failure-Policy beschlossen | `POLICY_ADOPTED_EXECUTION_UNVERIFIED` |
| G0-/QUAL- und Stop-/Fallback-Gates einschließlich T-06 spezifiziert | `DESIGNED` |
| Runtime-Host-/Backend-/CGMES-/PyPSA-PASS | `NOT_ASSESSED` |
| Permission/Redistribution realer Netzdaten | `RIGHTS_UNVERIFIED` |
| Produktive Implementierung und PoC-RunRelease | `NOT_AUTHORIZED_IN_THIS_M4_0_DOCUMENT` |

**M4-0-Endklasse:** `M4_0_STATIC_PREFLIGHT_COMPLETE_WITH_NAMED_RUNRELEASE_HOLDS`.

**Nächste Freigabebedingung:** ausdrückliche Owner-Autorisierung des PoC-M1-Implementierungs-/Testmakros auf eigenem Branch; darin zuerst die Host-/Bundle-/Fixture-/Entitlement-G0-Prüfung und danach bei PASS die Implementierung. Unabhängiger T-06-Worker darf auf eigener Arbeitskopie **parallel** starten und ausschließlich seinen eigenen read-only Minimaladapter/Fixture-Paritätsnachweis implementieren. Diese Aufträge sind detailliert in [97](97_M4_0_NEXT_MACRO_ASSIGNMENTS.md) vorbereitet; ihre Erstellung ist keine automatische Startfreigabe.
