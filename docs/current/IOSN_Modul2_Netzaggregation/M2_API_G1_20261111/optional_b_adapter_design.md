# Optionaler `tyndp_reduce.m2` → `tyndp_reduce.iosn_official` Adapter – **Design only**

**Status:** `PROPOSED_NOT_IMPLEMENTED`; **Ownerwahl C nicht bestätigt**.  
**Zweck:** begrenzter, einseitiger, versionierter Import von ausdrücklich physikalisch kompatiblen B-Eingabedaten/QA-Zeugen in den einzigen A-Kanon; B bleibt separat und kann unabhängige Numerik-/Regressionsorakel liefern. **Keine A→B-Rückkonvertierung, keine gemeinsame Source-of-Truth, kein neuer obligatorischer MA2-Pfad.**

**Verbindliche Prüfstände:** [A-Contracts](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/src/tyndp_reduce/iosn_official/contracts.py), [B-Contracts](https://github.com/AlOussama/TYNDP_Products/blob/88374dd38792146ca55fa3fe2d4b35dac842c0b9/src/tyndp_reduce/m2/contracts.py), [A-MA1](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/src/tyndp_reduce/iosn_official/ma1.py), [Review](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md).

## 1. Ausführungsgrenze und Namespace (nur Design)

Zukünftige, **optionale** Schnittstelle, z. B. `tyndp_reduce.m2_adapters.b_to_iosn_v1.validate_convert(...) -> CanonicalAInput + AdapterAudit` (genauer Namespace erst bei genehmigter Implementierung). Eingabe: ausschließlich exakt auf B SHA `88374dd38792146ca55fa3fe2d4b35dac842c0b9` bezogene, bytegehashte strukturierte B-Objekte plus vorgeschriebene Source-/Class-/Country-Provenienz. Ausgabe: validierte A-Objekte und separat versioniertes Audit (B-Hash, A-Hash, tatsächlicher Transformationsplan, Geräte-/ID-Mapping, Warnungen und Zurückweisungen).

**Nicht** Aufgabe des Adapters: A `execute_ma1` verändern, A `MA1Result`/15 Exporte mit B-JSON ersetzen, B-Kruskal-Seed ohne erneuten A-Check übernehmen, realen lossy HVDC als verlustlos umdeuten, implizit re-dispatchen, fehlende Gerätedaten synthetisieren, UTM/Zeiten automatisch korrigieren, einen MA2/Real-Gate-Status setzen.

## 2. Deterministische Feldkonvertierung – nur vollständig darstellbare Fälle

| B-Feld (exakt geprüft) | A-Feld | Designregel |
|---|---|---|
| `Evidence(source,revision,sha256,target_year)` | `Provenance(dataset_id,source_uri,version,source_sha256,synthetic)` + Adapter-Sidecar | Source/Revision mit verified original-byte SHA; `target_year` bleibt Provenienz **und ersetzt nie** fünf externe `weather_year_ids`; `fixture`→`synthetic` nur mit auditiertem Fixtureflag |
| `Bus(name,country,voltage_kv)` | `grid.bus_ids` / `raw_country_ids`, Country-Map/Sidecar Bus-Spannung | Eindeutige stabile IDs und Reihenfolge, keine verdeckte Bus-Voltage-/Base-Konversion; erforderliche bus_voltage-Provenienz als verlustfreie Sidecar; wenn für Gerätesemantik zwingend, sonst Reject |
| `grid.base_mva` / `ACBranch.x_pu` | `base_mva` / `x_pu` | numerisch exakt, positive endliche Werte auf **derselben Base**; kein stilles x-Rescaling oder Tap-Normalisieren |
| `ACBranch.name,bus0,bus1,kind,voltage_kv` | `ACBranch.identifier,bus0,bus1,kind,voltage_kv` | Orientierung unverändert; `kind` line/transformer/pst; bekannte, aktiv geschaltete AC-Topologie; eindeutige IDs |
| `ACBranch.tap_ratio` | kein entsprechendes A-Feld | Nur `tap_ratio = 1` innerhalb deklarierter numerischer Eingangsprüfung UND nachgewiesen keine weitere unrepräsentierbare Off-Nominal-/Reglerwirkung. Jede Nicht-Einheit/ungeklärte Provenienz ⇒ `UNSUPPORTED_SEMANTICS` |
| B ohne `phase_shift_rad`-Feld | A `ACBranch.phase_shift_rad` | Für nicht-PST ausschließlich **nachgewiesen** feste Phase=0 setzen; unbekannte oder nonzero feste Trafo-Phase kann **nicht** aus B rekonstruiert werden ⇒ `UNSUPPORTED_SEMANTICS` |
| `HVDCTerminalPair(name,bus0,bus1)` | `HVDCTerminals(identifier,bus0,bus1,lossless=True)` | linke/rechte Seite beibehalten; **nur** wenn alle zugehörigen p0/p1-Schedules strikt verlustlos sind; kein pauschales `lossless=True` ohne Datenprüfung |
| `HVDCDispatch(name,p0_MW,p1_MW)` | `hvdc_transfer_mw[id] = -p0_MW` | `p0 + p1 = 0` für jeden Zeitpunkt, endliche Werte, vorab deklarierte und im Audit gemessene winzige Rundungstoleranz (nicht 1 MW!). B `p0<0` Export, A `transfer>0` Export; negative Transferumkehr erlaubt bei exakter Bilanz |
| `PSTDispatch(name,phase_rad)` | `pst_phase_rad[name]` | Exakt T Werte in Radian und Originalorientierung, PST fixed phase A=0; fehlende, doppelte oder anders referenzierte Schedules Reject |
| `TimePoint(key,timestamp,weather_year,season,duration_h)` / `TimeSet` | A `TimeSet(snapshot_ids,year_for_snapshot,weather_year_ids,duration_hours,season,timezone="UTC")` | Auf absolute UTC instants normalisieren und ISO-8601-UTC-IDs eindeutig ableiten; **keine** stillschweigende Zeitachsen-Sortierung oder Auswahl. B-Original-`key`→A-Timestamp Bijektion und identische Timeseries-Reindizierung im Hash-Audit |
| `ReferenceDispatchSet(bus_order,time_keys,nodal_injections_MW,...)` | A `injections_mw (N,T)` und Schedule Maps | N×T gegen gehashte reindexierte Bus-/Zeitachse; sämtliche aktiven PST und HVDC genau einmal; kein unberechtigtes MW-Slack; frozen operational |
| `NormalContingencyRatings(normal_MW,contingency_MW,unit)` | A `normal_mw` / `contingency_mw` by active branch ID | Beide L×T geordnet und **vorhanden**, strikt MW>0, unabhängiger MVA/A→MW-Konversionsnachweis; B `None` emergency ⇒ `BLOCKED_DATA` |
| B `CountryZoneBudget(quotas, official, evidence)` | A `CountryZoneBudget(quotas,official,source_sha256)` | Exakte Table-3-Quoten/37+102 nur bei vollständigen Europe-Daten; NI/UK separat; Original-SHA nachrechnen |
| B `grid.ties_110kv_complete` | A `incomplete_110kv_ties` | nur Vollständigkeitswitness `True` => A `False`; fehlende 110-kV-Ties nicht stillschweigend als vollständig labeln |
| B `grid.branches` erlaubt nur aktives `in_service=True` | A `in_service` | kein Entfernen oder Reordering bekannter inaktiver Leitung ohne Source-/Fingerprint-Proof; nicht repräsentierbare Topologie ⇒ `UNSUPPORTED_SEMANTICS` |
| B nominale 220/380 und exakte 225/400 kV | A `screening_class_kv` | 225/400 exakt zuordnen; 220→225 und 380→400 **nur mit expliziter Source-Line-Class Policy und Audit**. B selbst überspringt nominale 380, deshalb keine Vererbung des B-Eligibility-Ergebnisses |
| B `observed_ac_flows_MW` | getrenntes `ObservedACFlowQA` Sidecar | Optionaler realer signed Original-Flow-Witness, mit Source/Time/Branch-SHA und definierter Modellabweichung; **kein** B-Gate der exakten 1e-6-MW-Gleichheit als A-Eintrittsvoraussetzung |

`raw_country_ids` und `explicit_country_map` werden aus B-Labels nur dann identity-basiert aufgebaut, wenn deren Quelle nachweisbar eindeutig ist und A die injektive Relation akzeptiert; sonst braucht es eine **vorherige**, reversible Upstream-Alias-Kanonisierung. Ein B-Datensatz, der Northern Ireland und United Kingdom gemeinsam codiert, ist **nicht** konvertierbar.

**B-Seed/Zone-IDs:** Falls eine B-`busmap` als unabhängige QA eingelesen wird, ausschließlich via Bus-ID-basierter Zuordnung und stabiler deterministischer, in Sidecar geloggter Konvertierung in A-Namen `Country::NNN`; Reihenfolge durch Country und kleinste kanonische Bus-ID festlegen; `validate_busmap` einschließlich Schutz prüfen, danach **neu** `build_oriented_projection` auf dem A-Originalgraphen. B- und A-Seeds dürfen verschieden bleiben (K4 5 MW vs 10 MW). **MA2-Baseline bleibt ausschließlich der A-`MA1Result.seed`**; B-QA-Map darf diese nicht stillschweigend überschreiben.

## 3. Pflichtvalidierungsreihenfolge (vorgeschlagene reine Preflight-Pipeline)

1. **Pinned input:** B-Commit/Tree/Source-File-Hashes, B Evidence-SHA und Originalbytes prüfen; B-Schema-Version, positive finite Basis-/Gerätewerte, unique IDs und Originalordnung validieren. Wer keine echten Quellbytes belegen kann: `BLOCKED_DATA` für realen Import, Teststatus `SYNTHETIC_ONLY`.
2. **Geräte-Fail-Closed:** `tap_ratio` und transformer fixed phase qualifizieren; jede aktive Komponente identifizieren; alle HVDC p0+p1 und Einheiten/Orientierungen pro T prüfen; unbekannte/lossy Fälle `UNSUPPORTED_SEMANTICS`; no implicit droop/slack.
3. **Zeit-/Jahr-Freeze:** genau fünf externe Jahre, TimePoint.Timestamp absolute UTC, eindeutig und **streng monoton** in ursprünglicher B-Sequenz; original B Keys auf neue ISO-UTC-Timestamps bijektiv und ohne stille Sortierung; negative/fehlende Stunden zurückweisen. Per-Schedule Time-Keys entsprechen B-TimeSet.
4. **Länder/Quoten:** Alle originalen Busse, vollständige Country-Mapping-/Alias-Provenienz und getrennte NI/UK-Areas; 37/102 nur official full-geography; sonst `SYNTHETIC_BUDGET`.
5. **Screen/Protect:** vollständiger `SCREEN_AUDITED_225_400_v1`- und `PROTECT_CRITICAL_UNION_v1`-Nachweis einschließlich Authorisierung jeder class=0 Ausnahme. Bei `THRESHOLD_PENDING` kein MA2-Run. Quoten nicht unter Force-Merge verletzen.
6. **A-Domain instanziieren:** ausschließlich defensive immutable A-Objekte; strikte Typen; einmaliger operationaler globaler `reference_flows`-Solve auf kompletter AC-Topologie; geprüftes eigenes neutrales Dispatchset/Result nur aus validierter separater Eingabe.
7. **Re-Verification:** A `preflight.require_pass`, country feasibility, `execute_ma1(...)` mit explizit gefrorener Schutz-ID-Tuple und Year-Weights, G01–G05 inklusive `A_z Γ=P A_d`, SHA gegen Sidecar und exportierten 15 Dateien.
8. **Independent QA:** Dasselbe B-Witness-Modell nur in erlaubter lossless Teilmenge erneut numerisch lösen; A/B-Flow-Parität mit gemeinsamer Orientation / Reindexierung; keine Aussage über nonshared Geräte, 100%-Realnetz oder heuristische Gleichheit.
9. **Publish:** erst nachdem Reviewer einen **eigenen** Test-Run auf gepinntem Adapter-SHA akzeptiert, als **optionaler** versionierter B→A-Input. No A/B branch merge und kein MA2-Go aus bloßem Adapter-Test.

### Fail-closed Klassen

| Error-Code | Beispiel | Wirkung |
|---|---|---|
| `UNSUPPORTED_SEMANTICS` | B lossy HVDC p0=-10 p1=+9 MW; nonunity tap; nicht belegter fixer Trafo-Winkel | Kein A-Objekt und kein verlustloser Ersatz erzeugen |
| `INVALID_TIME_AXIS` | B fünf, aber unsortierte UTC-Snapshots, Offset-Alias-Duplikat, fehlendes Jahr | Kein Sortieren/Ersetzen; fail |
| `BLOCKED_POLICY` | 380-kV-Branch ohne explizite 400-kV-Klassifikation; 400-kV class=0 ohne Exclusion-Witness | Kein verdecktes Überspringen |
| `BLOCKED_DATA` | kein Emergency-Rating, unvollständige 110-kV-Ties, unbewiesener Bus-Country-Alias oder Sourcebyte | Kein realer Import |
| `INVALID_FINGERPRINT` | B-Input/Source/Adapter-Manifest inkonsistent | Kein stilles Re-Hash eines manipulierten Runs |
| `G03_FAIL` / `G05_FAIL` | unbalancierte AC-Insel, fehlende PST-Schedule, falsche orientierte Projection | Kein A-MA1Result |
| `ALTERNATIVE_SEED_ONLY` | B-Kruskal und A-Dynamic-Greedy bilden verschiedene gültige Cluster | Nur QA-Information, **kein** Seed-Override |

## 4. Test-/Re-Review-Matrix (vor optionalem Produktionsimport)

**Positive Replay Fixtures:** 3-Bus-PST-Mesh gegen independent Dense/Loop Oracle; zwei echte AC-Inseln mit lossless HVDC; 3 gekoppelten Ländern und exakten Synthetic-Koten; signierte Rückwärts-HVDC; exakt klassifizierte 380→400 und 220→225; monotone fünf UTC-Jahre; 500-Bus sparse chain mit identischer Bus-/Branch-/Time-Reindexierung; B alternative valide K4-Zonen als **different valid seed**. Als Referenz nur die [11 unabhängigen R-API-Tests](https://github.com/AlOussama/TYNDP_Products/actions/runs/43078255397) verwenden; Adaptertests sind **noch nicht geschrieben**.

**Negative Replay:** `p0+p1≠0`, positiver Energiedefekt/Gain, non-unit tap, nonzero/unknown fixed transformer phase, missing PST, 380 kV without qualified class, 400 class=0 without signed exclusion, unsorted/duplicate/offset UTC, B fewer than five years, missing emergency MW ratings, unequal bus/time order, unbalanced AC islands, NI/UK folding, illegal many→one mapping, absent 110-kV tie evidence, altered input SHA, altered export manifest, illegal B-zone direct MA2 import, false AC/observed equality requirement. **All** such inputs must reject deterministically with documented code.

**Implementation admission:** Owner `OD-M2-API-01=C` plus device/screening decisions; repaired, independently approved A MA1 contracts; optional B adapter PR/commit in isolated namespace; B-source byte-identity and independent tests; documented Source/Target Schema and rejects; performance regression. No worker may self-attest independent approval.

## 5. B-Ideen ohne B→A-Produktionsmigration

| B-Fähigkeit | Nutzen | Kosten/Risiko | Entschluss |
|---|---|---|---|
| Self-verifying JSON `ReferenceFlowCache.payload()` and SHA | Guter externer Witness für Testbarkeit/Run-Identität | großer numerischer JSON-LxT-Footprint, zweite Schemavariante | **OPTIONAL** as Sidecar/test oracle; A-NPZ bleibt primär |
| `write_once(path.open("x"))` | Schutz einzelner eingefrorener Belegdateien | kein atomarer Gesamt-Run; NFS/FS-Semantik beachten | **OPTIONAL** oder A-Staging-Transaktion nach separatem Test |
| `SparseACReference` hält LU-Faktoren pro AC-Insel | Reduziert wiederholte Referenzfaktorisierung | Cache invalidation bei Topologie/SHA/Mode, zusätzlicher Peak-RAM | **OPTIONAL** nach A-spezifischem Benchmark/Regression; kein stiller Cache |
| B Signed-HVDC Terminalmodell | Potenzielle spätere reale Loss-/Terminal-Erweiterung | andere Energiebilanz und Identifizierbarkeit, neue Validierungsquelle | **OUT OF MA2-v1**; separates future device gate |

Review schätzte Option C auf **4–7 Personentage nur für Interface-/Testmigration** (unsicher, kein Messwert), B-Solo 8–14. Der optionale Adapter darf den freigegebenen A-MA2-Kern **weder blockieren noch verändern**.

## 6. Artefakt- und Statusvertrag

Pro **zukünftigem** Adapterlauf: `adapter_manifest.json` (schema/version, B input/source SHA, A target SHA, code SHA, policy hashes, exact fields/ID/transforms, nondestructive warnings), `conversion_ledger.json` (jede numerische/class/country/zone Transformation), `device_rejection_ledger.json`, `independent_parity_result.json`, 15 standardmäßige **A**-Ausgabedateien falls optionaler A-`execute_ma1` tatsächlich autorisiert wurde. Diese Zusatzdateien gehören **nicht** in das fest definierte 15-Dateien-A-MA1-Exportverzeichnis, sondern in eine getrennte versionierte Sidecar-Directory. Die vorgeschlagenen Dateinamen sind keine Behauptung aktueller Artefakte.

**Schluss:** `DESIGN_ONLY` / `OWNER_PENDING` / `ADAPTER_NOT_IMPLEMENTED` / `MA2_NOT_AUTHORIZED` / `NO_MERGE`.
