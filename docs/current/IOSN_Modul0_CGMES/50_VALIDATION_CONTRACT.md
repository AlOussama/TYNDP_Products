# R-M0-CGMES-CONTRACTS-1 — 50 Validation, Import/Update/Export and Loss Contract

**Contract-ID:** IOSN-M0-VAL/1.0.0 · **Datum:** 2026-10-30 · **Status:** Testspezifikation; **keine Testläufe, kein Lastfluss, keine Implementierung**  
**Basiscommit:** `1595d6d38e77804760612621657721b3699d2fea` · Gegenstücke: [10 Anforderungen](10_REQUIREMENTS.md), [30 Canonical Data Contract](30_CANONICAL_DATA_CONTRACT.md).

## 1. Validierungsgrundsatz, Freigabeklassen und Fehlersemantik

Das Testziel ist nicht, eine beliebige RDF/XML-Datei einzulesen, sondern einen **reproduzierbar identifizierten, elektrisch plausiblen, referenziell vollständigen** und für den angegebenen Anwendungszweck geeigneten detaillierten Netzstand zu garantieren — ohne verschwiegene Approximationen. **IEEE/IEC/ENTSO-E-CGMES-Konformität ist von einer erfolgreichen internen Modul-0-Validierung zu unterscheiden**; externe Konformitätsprüfungen müssen separat durchgeführt werden [C1–C3].

Unabhängige Freigaben werden getrennt ausgewiesen:

| Capability | Prüfgegenstand | Obligatorische Gates |
|---|---|---|
| `CANONICAL_IMPORT_READY` | Quellgraph, IDs, FKs, Profil-/Boundary-Validität, Canonical Storage | G0/G1 + relevante T-01–T-11 |
| `PYPSA_ACPF_READY` | stationäre positive Sequenz unter AC-Komponentenfähigkeiten und Inselbehandlung | vorherige + G2/G3, T-12–T-20; T-23 nur bei geeigneter SV |
| `PYPSA_LPF_READY` | wirksame `x_pu`, Tap/PST-/HVDC-Offsets, AC-Island-Balance als Detaileingabe | vorherige + LPF-spezifische T-09/T-14/T-17/T-20 |
| `REDUCTION_ADAPTER_READY` | **bestehender** `src/tyndp_reduce/pypsa_adapter.py` akzeptiert das tatsächliche Netz | vorherige + T-20 und konkreter Adapter-Qualifikation |
| `UPDATE_EXPORT_READY` | identitäts-/graphentreue Aktualisierung importierter CGMES-Daten | G4, T-21, T-24, gültiges Raw-Graph-Artefakt |
| `CREATE_EXPORT_READY` | Neuerzeugung eines technisch vollständigen deklarierten CGMES-Profilsets | G4, T-22, T-24, genügend explizite CIM-Erzeugungsattribute |

**Gesamtstatus** je Capability: `PASS`, `CONDITIONAL_WITH_NAMED_GAPS`, `BLOCKED`, `NOT_ASSESSED`. Ein `PASS` ist nur für eine vollständig bezeichnete **geprüfte Fixture / Dataset / Importkonfiguration / Ziel-Capability** zulässig; der vorliegende Spezifikationsstand ist ausschließlich `DESIGNED_NOT_EXECUTED`.

**Schweregrade:** `FATAL` = Parse-/Profile-/Source-ID-Kollision, Graph nicht zuverlässig interpretierbar; `BLOCK` = harte Verletzung einer Capability (z. B. fehlender aktiver Anschluss, undefinierte elektrische Basis oder falsche Boundary); `WARN` = fachlicher Qualitätsverlust innerhalb einer ausdrücklich gewählten, zulässigen Approximation; `INFO` = nachvollziehbare Transformation ohne Qualitätsdefizit. Nur `WARN` kann je Policy formal quittiert werden; `FATAL/BLOCK` dürfen nicht durch bloße Waiver als bestanden markiert werden. Eine Fehlermeldung muss `rule_id, source_file_sha256, profile_uri, source_mrid, canonical_row, attribute, expected/observed, severity, remediation` enthalten. Unterdrückung ohne Ereignis-Ledger ist verboten.

## 2. Formale Invarianten und Prüftoleranzen

### 2.1 Harte, diskrete Invarianten (exakt)

1. **Referenzintegrität:** 100 % der nicht explizit als externe Boundary-Referenz deklarierten FK-/RDF-Referenzen sind auflösbar; 0 doppelte aktive `source_key` mit inkompatiblen Klassen, 0 doppelte `asset_id`-Bedeutungen. Referenzen, die nur durch das Boundary-Set auflösbar sind, müssen ihre Authority dokumentieren.
2. **Eindeutige Anschlüsse:** Equipment besitzt erwartete Zahl und Reihenfolge seiner Terminals, 2W genau zwei und 3W genau drei gültige Wicklungen. Pro aktivem Terminal gibt es je Zustand **genau eine** eindeutige Zuordnung zu einem TopologicalNode/Bus. Kein elektrischer Zweig mit Endport ohne Bus.
3. **Schalter-Topologie:** geschlossene leitfähige Switches vereinigen nur zulässige ConnectivityNodes; offene trennen diese. `normalOpen` überschreibt nie einen tatsächlich gegebenen `open`-Wert. Kein unbeabsichtigter Kurzschluss über geschaltete Netzkanten, keine künstliche AC-Inselverbindung über HVDC.
4. **Zustands-/Profilkonsistenz:** Topologie- und SSH-/SV-Modellheader beziehen sich auf kompatible Equipment-/Boundary-/Scenario-Versionen. Profile, die nicht geliefert sind, werden als `NOT_PROVIDED` notiert; „SV fehlend“ ist kein Fehler für einen **unsolved** Inputmodus.
5. **Anzahl-/Multiset-Erhaltung:** Zahl aller Original-Equipmentobjekte und ihrer mRIDs bleibt im Canonical/Raw-Ledger erhalten; Zahl der *aktiven PyPSA-Zeilen* darf wegen Switch-Faltung, isolierter Assets, 3W-Sternästen oder expliziter HVDC-Vereinfachung abweichen, **aber nur mit 1:n-Mapping und Summenregel**.
6. **Land:** jeder für Modul 1 freigegebene aktive Original-AC-Bus besitzt genau ein gültiges `country_code`; Ersatzsternen wird nicht ohne eigenen Ursprung ein Land vorgetäuscht. Country-FK-Quote 100 %. Geokoordinaten dürfen `null` sein, aber besitzen dann eindeutigen Missing-/Quality-Status und eine gezählte Coverage-Lücke.
7. **Identität/Update:** Alle nicht explizit neu generierten CGMES-Objekte behalten ihre mRID, Klasse und Originalbeziehung; ein neu erzeugtes synthetisches PyPSA-Objekt ist nicht automatisch ein neu erzeugbares CIM-Equipment.
8. **Einheiten:** Keine Dimensionskonvertierung ohne bekannte Einheiten und deklarierte Basis; `0`, `missing`, `defaulted`, `calculated` dürfen sich nicht gegenseitig maskieren.
9. **AC-Netz vs. Zeitreihen:** ein eingefrorenes `network_revision_id` verändert sich nicht durch später geladene Stunden-/Wetter-/Dispatchdaten. Reduktions-Busmaps gehören nicht zu Modul 0.

### 2.2 Mathematische Invarianten (vorgeschlagene interne QA-Policy)

Alle Schwellen **sind interne Initialvorgaben** zur späteren Prüfung und Kalibrierung gegen reale Datensatzpräzision, keine externen CGMES-Konformitätstoleranzen. Vor Durchführung werden Solver-Version, Frequenz, per-unit-Systembasis, Vergleichsobjekte, vollständige Vorzeichenkonvention und Toleranzprofil gepinnt.

| Regel | Prüfgröße | Initiale interne Schwelle / Interpretation |
|---|---|---|
| `NUM-01` Identitäts-/Einheiten-Round-trip | `Z_Ω → z_pu → Z_Ω`, `Y_S → y_pu → Y_S`, pro Wicklung | `abs_error ≤ 1e-10·max(1,abs(reference))` bei exakt bekannten Basen; andernfalls BLOCK |
| `NUM-02` Zweig-Pi | komplexes 2×2-`Y` aus Canonical und Projektionsmodell | relativer Frobeniusfehler `≤1e-9` gegen normierte Referenz, plus absolute Guard `1e-10` im gewählten pu-System |
| `NUM-03` Transformer | 2×2-Port-`Y`, Test bei Tap HV/LV, Ratio ±Step, Shift ±φ | `≤1e-9` relativ, Pole/Ports und positive-/negative-Phasenshift-Flussrichtung korrekt |
| `NUM-04` 3W | dreiportige Kron-reduzierte `Y` gegen Canonical-Sternmodell | `≤1e-9` relativ; bei singulärem Sternmodell **nicht** still regularisieren |
| `NUM-05` Topologischer Energiefluss | KCL-Residual je aktivem AC-Bus | `max|ΔP| ≤ max(1e-6 MW,1e-8·S_base MVA)` für **synthetisch exakt vorgegebene, gelöste** Cases; Realnetz-Toleranz separat festlegen |
| `NUM-06` AC-SV-Referenz | `V` pu/Angle sowie Port-`P/Q` | keine universelle feste PASS-Schwelle! Bericht mit `max,median,P95,P99`, z. B. Vorschlagsdiagnostik 1e-3 pu, 0.1 deg, 0.1 MW pro Terminal; qualifizierter Grenzwert hängt von SV-Konsistenz/Netzmodell ab |
| `NUM-07` HVDC-Bilanz | `P_bus0 + P_bus1 + P_loss` nach definierter Portkonvention | `abs_error ≤ max(1e-6 MW,1e-8·P_nom MW)` in künstlichem Test; exakte Loss-Funktion aus gewähltem Modell |
| `NUM-08` Current-Limit-Konversion | `S = √3 U I/1000` und umgekehrt | `NUM-01`-Skalierung; ohne deklarierte Spannung **keine** statische `s_nom`-Ableitung |
| `NUM-09` Graph Diff | Menge unveränderter semantic RDF triples / Original-mRIDs/Relations | exakt gleich für nicht geänderte Objekte; Namespace-Reihenfolge/Formatierung in XML ohne Bedeutung |

**Numerische Vorsicht:** zero/near-zero impedances, sehr kleine Shunts, degenerierte Tap-Stellungen, konditionsschlechte Netzmatrizen und mehrere Slack-Generatoren dürfen nicht durch absolute Toleranzen versteckt werden. Normprüfung gegen jede Invariante benötigt eine transparente Guard-Regel; die oben vorgeschlagenen Schwellen sind **noch unvalidiert**, insbesondere nicht als Optimierungs- oder Netzqualifikationsnachweis zu verwenden.

## 3. Zwei strikt getrennte Exportmodi

### 3.1 Exportmodus 1 — `UPDATE_IMPORTED`: originaler Graph als Autorität

**Vorbedingung:** Original-CGMES-Graph/äquivalent verlustfreies Modell inkl. nicht abgebildeter Klassen/Attribute, File-/Profilpartitionierung, Identity-/Terminal-/Boundary-/Header-Informationen und Import-Mapping sind persistent, verifiziert und für Update verfügbar. Nur explizite `supported_write_fields` (z. B. ausgewählte SSH-P/Q/Tap/State-Attribute oder konsistente neu berechnete SV-Werte) dürfen geändert werden. Die tatsächliche Liste ist an CGMES-Familie, Version, konkretes Backend und Zielprofil gebunden. Eine Änderung einer topologieprägenden Klasse/eines Switches erfordert **Neuaufbau und vollständige Validierung** von TP/Referenzen, nicht nur einen XML-Zahlen-Patch.

**Algorithmischer Vertrag (keine Implementierung):**

1. Quellgraph nach `input_manifest_sha256` laden, Importscope/Profile/Model Authority validieren.
2. Änderung `Δ` auf *bekannte* `source_object_id + attribute + target_profile` zurückführen; bei abgeleiteter View (3W-Stern, HVDC-Link) nur dann ein Patch, wenn eine **eindeutige geprüfte inverse Abbildung** existiert.
3. Konflikte gegen ursprüngliche Quellversion erkennen (optimistischer Hash-/Revision-Check). Je Attribut unterscheiden: no-op, valid write, explicit delete, unsupported/ambiguous.
4. Neuer Zustand/Modelheader und Abhängigkeiten gemäß CGMES-Version erzeugen, mit konsistentem EQ/SSH/TP/SV-Modellset; erhaltene Original-mRIDs bleiben erhalten, **neue** Sv-/Header-Objekte erhalten neue mRIDs mit referenziertem Grund.
5. Vollständige Profil-/Referenzvalidierung; semantischen Graph-Diff bilden, ungewöhnliche Attribute/Quellprofile und Boundary-Sets auf Unverändertheit prüfen.
6. Nur atomar ausliefern, wenn Gates PASS; geänderte und unveränderte Teile, Annahmen, exportierte Dateien und Hashes protokollieren.

**Erhaltungsvertrag:** Unveränderte semantische RDF-Tripel/Quellobjekte/Beziehungen, vorhandene gültige mRIDs, fachlich nicht betroffene Header- und Profilzugehörigkeiten sowie unknown property bags werden beibehalten. RDF/XML-Serialisierung muss **nicht byteidentisch** zum Input sein. **No delete by omission**: ein Objekt/Feld fehlt in der PyPSA-View ≠ aus Original-CGMES löschen. Änderungen in einem Ergebnis-SV ersetzen nicht rückwirkend die Annahmen eines SSH-Modellsets.

**Verboten:** aus PyPSA-`Line.type`/`TransformerType` rückgerechnete Quellparameter ohne eindeutige Herkunft als native CGMES-Änderung ausgeben; alle Originalobjekte aus reduzierter Projektion rekonstruieren; Boundary-Referenzen „reparieren“ durch erfundene IDs; ohne Header-/Versionierungsupdate ein angeblich konsistentes CGMES-Modell ausgeben.

### 3.2 Exportmodus 2 — `CREATE_FROM_PYPSA`: neues Netz mit begrenzter Semantik

**Vorbedingung:** Als Minimum vorhanden sind eindeutige PyPSA-Bus-/Branch-/Generator-/Load-/Shunt/Link-IDs, gültige Spannungsbasen, zugeordnete Source-/Country-/Substation-Authority (ggf. bewusst neu konstruiert), zulässiger Geräteklassentyp, korrekte Endports, aktuelle SSH-/Switch-/Tap-/P-Q-Zustände, gewünschte CGMES-Familie und Profilset, Units, Stützmodell/Modelheader, ein konsistentes Boundary-Konzept und deklarierte Ersatzannahmen. Ein PyPSA-Netz allein erfüllt diese Vorbedingungen **typischerweise nicht**.

**Minimaler konstruktiver Ansatz:** neue CGMES-mRIDs in neuem, dokumentiertem Authority-Namespace; explizite `BaseVoltage`, `Substation`, `VoltageLevel`, `ConnectivityNode`, `Terminal`, Equipment-/Maschinen-/Last- und TransformerEnd-Objekte plus erforderliche EQ/SSH/TP-/Header-Verweise. Ein PyPSA-Bus kann in einem *als synthetisch gekennzeichneten bus-branch-Ersatzmodell* als ein TopologicalNode mit einer (oder mehreren nach definierter Policy erzeugten) ConnectivityNode modelliert werden; **fehlende reale Schaltfelder, originaler Node-Breaker-Aufbau, Positionen und bestehende mRIDs können nicht wiederhergestellt werden**. Ein solcher Export behauptet nicht, das historische TSO-IGM zu reproduzieren. SV nur nach geeignetem **tatsächlich ausgeführten** stationären AC-Lastfluss, nie aus unbekannten Zeitreihen oder initialen `p_set` ohne LF. 3W-View-Artefakte werden nur zurückgeführt, falls das 3W-Original im Sidecar verfügbar ist oder ein neuer konsistenter PowerTransformer mit drei Enden aus gesondertem Konfigurationsmodell konstruierbar ist. Verlustbehaftete bidirektionale HVDC-Links ohne fachliche Konverter-/DC-Spezifikation sind nicht „CGMES-HVDC-exakt“ erzeugbar.

**Exportfähigkeitsstufen:**
- `CGMES_SYNTHETIC_NETWORK_READY`: modelltechnisch gültiges, eindeutig neu erzeugtes vereinfachtes Netz, mit **ausdrücklichem** Verlust- und Synthetic-Status.
- `CGMES_IMPORTED_MODEL_EQUIVALENCE_READY`: im Modus 2 **nicht** automatisch erreichbar; erfordert externe Source-Evidenz/Graphvergleich und getrennte Qualifikation.
- `BLOCKED_FOR_CREATE`: Pflichtprofile/Terminal-/Elektrik-/Authority-/Headerinformationen fehlen und lassen sich nicht zulässig explizit festlegen.

### 3.3 Attributgenauer Verlustvertrag

**Legende:** `E` EXACT, `A` APPROX, `N` NONRECONSTRUCTIBLE. Die Klassifikation bezieht sich auf *Vorbedingung und Ziel repräsentierter Informationen*, nicht auf ein allgemeines CGMES-Zertifikat. Ein „E“ ist bei einem bereits verlustbehaftet modellierten Sonderfall nicht möglich. Für jedes exportierte Objekt/Feld wird die konkrete Stufe im `loss_manifest` gespeichert.

| Information | Import → Canonical | Canonical → PyPSA-View | Modus 1 UPDATE (mit Originalgraph, unveränderte Felder) | Modus 2 CREATE (PyPSA ohne Sidecar) |
|---|---|---|---|---|
| mRIDs, Modelheader, Profile, RDF-Referenzen | E, sofern Backend vollständig | N in Standard-PyPSA, E im Sidecar | E, geändert nur kontrolliert | N für historische IDs/Versionen, neue Daten E als **synthetisch** |
| Stationen, VoltageLevels, Länder | E bei Quelle/vollständiger Zuordnung | E für Bus-Kernfelder; A für Hierarchie | E | A oder N ohne eigene Hierarchiequelle |
| ConnectivityNodes, Terminals, Switches, Open-State | E | A (gefaltete Topologie) | E | N für originale Schaltanlagen, A für neue Bus-Branch-Struktur |
| AC-Leitungs-`r/x/g/b` und Endorientierung | E bei gültigen Source-Werten | E nach PI-/Basisprüfung | E | E für elektrisch belegte 2-Port-Parameter, ursprüngliche Klasse/Geometrie evtl. A/N |
| 2W, Tap-Ratios, PST | E bei vollständiger Quelle | E/A nach geprüftem Ybus/Step-Modell, Controls im Sidecar | E für erhaltene Originaldetails | A/N für nicht abgebildete Regelmechanik und Tap-Step-Tabelle |
| 3W-Original und Sternparameter | E | A strukturell (3× 2W plus Sternbus), ggf. E elektrisch bei Ybus-Äquivalenz | E für erhaltenes Original | N ohne 3W-Sidecar, A mit expliziter Neukonstruktion |
| Maschinenmodell, Generator-P/Q und Grenzwerte | E bei Quelle | E für stationäre Grundwerte, A für vollständige Q-Curves/Remote Control | E | A/N für unbekannte Maschinen-/Reglerdetails |
| Last-P/Q, ZIP-/Spannungsabhängigkeit | E | E bei Konstant-P/Q, A bei spannungsabhängiger Last | E | A/N bei fehlendem Lastmodell |
| Shunt g/b und Schaltstufen | E | E für fixierte Admittanz, A für Stufendynamik | E | A/N für unbekannte Kompensator-Controls |
| Boundary-Authority, Äquivalente, IGM-Verknüpfungen | E mit gültigen Boundary-Daten | N im PyPSA-Kern, E Sidecar | E | N ohne neue explizite MAS/Boundary-Konstruktion |
| Normale/temporäre/direktionale Limits | E | A/N im `s_nom`, E im Sidecar | E | A/N ohne limit type/duration/terminal validity |
| AC-State `SV` und Slack/Regelzustand | E bei geliefertem SV | A bei ungeprüftem neuem LF | E für alte SV, neuer SV nur nach LF | N ohne tatsächliche und geprüfte AC-LF-Lösung |
| HVDC Converter/DC-Port/Control/Losses | E im Raw/Canonical bei gültiger Quelle | A als qualifizierter Link, sonst N | E unverändert, Update nur bei eindeutiger Inverser | A/N ohne neues Converter-/DC-Schema |
| CRS, geografische Originalpunkte, DL | E bei Roh-/GL-Import | A: Bus x/y; N für volle Geometrie im Standard-PyPSA | E | N außer explizit neu gesetzte Geopositionen |
| unbekannte/noch nicht gemappte CIM-Felder | E im unveränderten Source Graph | N ohne Sidecar | E unverändert, sonst BLOCK | N |

**Datenverlustmeldung:** Jede Instanz von `A`/`N` mit Modellwirkung oder erforderlichem Exportinhalt erzeugt `loss_manifest(transaction_id, object, field_or_relation, reason, severity, physical_effect, acknowledgment)`; Summenbericht nach Typ und Profil. Kein automatisches „best effort“ ohne bestelltes Capability-Downgrade. Die Schwere richtet sich ausschließlich nach elektrischer oder semantischer Wirkung sowie nach dem ausgewählten Exportmodus und dessen Pflichtfeldern.

## 4. Validierungsstrategie und Prüfkatalog T-01…T-24

Die aufgeführten Tests sind **Arbeitsaufträge für spätere Implementierung**, nicht ausgeführt. Jeder Test spezifiziert Eingangsfixture, erwarteten Nachweis und ablehnende Negativfälle. Ein Backendwechsel benötigt Wiederholung der Black-Box-Testfälle zur Canonical-Gleichheit. **Datenfixture-Lizenz, Version und Hash müssen vor Verwendung verifizierbar sein; keine echten Netzmodelle mit unbekannten Rechten im Repository ablegen.**

### 4.1 Profil, Raw Graph und Identitäts-/Boundary-Qualität

| Test | Prüffall / Fixture | Erwartetes prüfbares Ergebnis |
|---|---|---|
| **T-01** | 2.4.15 EQ+SSH(+TP/SV) und 3.0 EQ+SSH(+TP/SV) mit korrekten Headern; gemischte und falsch deklarierte Profile | Version/Profil/Modellhash erkannt; zulässige incomplete-profile-Modi korrekt markiert; Versionsmix/URI-Fehler BLOCK |
| **T-02** | Unsolved EQ+SSH ohne SV, solved mit SV, geändertes SSH bei gleicher EQ | Unsolved importierbar ohne erfundenes SV; `operating_state_id` trennt Zustände; SV nur bei korrekter Referenz |
| **T-03** | Single-IGM, zwei IGMs mit gemeinsamem Boundary-Objekt/X-Node, CGM; fehlende/falsche EQ_BD/TP_BD-Referenz; 3.0 ohne TPBD | Modelle/Authorities richtig assembliert; keine Doppelzählung; 2.4.15-spezifische Boundary-Regeln; 3.0 verlangt kein fiktives TPBD |
| **T-04** | Wiederholte mRID across EQ/SSH/TP/SV, unterschiedliche Authority, kollidierende Source-Klassen; unbekannte Prädikate | exakt eine kanonische Identität pro gültigem Source-Objekt, volle Occurrence-/Raw-/Provenienzbezüge; Konflikt BLOCK |
| **T-05** | Reimport identischer Archive mit stabiler Config; ein zulässiges Feld geändert; paralleler konkurrierender Delta-Stand | gleiche Canonical IDs/Hashes bei identischen Inputs; nur deklarierte Revision/Änderungen; Konflikt atomar BLOCK |
| **T-06** | Zwei backend-spezifische Parse-Adapter lesen semantisch identischen Graph; YAML Mapping v1; veränderte Function-ID | Kanonische Werte/Relationen gleich; Backendobjekte nicht im Schema; nicht registrierte Transformationsfunktion BLOCK |

### 4.2 Topologie, Geo und elektrisches Netzmodell

| Test | Prüffall / Fixture | Erwartetes prüfbares Ergebnis |
|---|---|---|
| **T-07** | 4 ConnectivityNodes, Breaker ON/OFF, Disconnector OFF, isolierter Terminal, Out-of-Service-Zweig, normalOpen ≠ open | deterministische Fusion/Trennung; korrekte Anzahl TopologicalNodes/Islands; kein Phantombus |
| **T-08** | geliefertem TP identische und absichtlich abweichende SSH-Switch-Topologie gegenüberstellen | gleiche Projektion PASS, Widerspruch als konkreter TP-/Terminal-Konflikt BLOCK oder ausdrücklich neues Policy-Revisionsartefakt |
| **T-09** | zwei AC-Inseln mit gemeinsamem HVDC-Link, Slack vorhanden/fehlend, Insel nur mit Last, inaktiver Branch | HVDC verschmilzt Inseln nicht; fehlende Referenz/Balance nach angefragter Capability BLOCK; exakte Inzidenz je Insel |
| **T-10** | gültige ISO-Länder, Cross-border-Line mit Ports in verschiedenen Ländern, fehlendes/mehrdeutiges Land, synthetischer Sternbus | 100 % Country-FK der freigegebenen Originalbusse; Cross-border Endpoints korrekt; Sternbus nicht als reales Land ausgegeben |
| **T-11** | GL mit EPSG/WKT CRS, mehreren `PositionPoint` und Line-Route; fehlendes CRS, fehlende Koordinaten, Station-Ableitung | Originalpunkte unverändert; Projektion nur mit CRS; Coverage- und Approximation-Report; kein stilles WGS84 |
| **T-12** | ACLineSegment r/x/gch/bch, per-length vs total, Reverse-Port, 0-Zweig, EquivalentBranch, shunt-only | `NUM-01/02`, End-S-Vorzeichen, `z≠0`; keine doppelte Längenmultiplikation; EquivalentBranch als solche erkennbar |
| **T-13** | 2W-CGMES-End1-Impedanz, ratedU/ratedS mit unterschiedlichen Seitenbasen, 3W-Stern inkl. Shunts | `NUM-01/03/04`, korrekte EndNumber-FKs; 3W-Graph zurückführbar; singulär/nicht-darstellbar BLOCK |
| **T-14** | RatioTapChanger HV/LV, neutral/low/high steps, PhaseTap ±shift, tabellierter Typ, Remote Control | Phase-/Leistungsflussrichtung korrekt, Ybus-Äquivalenz; fehlende Tap-Tabelle/Schritt BLOCK statt neutralem Default |
| **T-15** | Generator Source-`p<0`; Last `p>0`; negative Last; Q-Limits, PV, PQ, Slack und RegulatingControl | korrekte Vorzeichen und `p_nom`/`p_set`-Trennung; mindestens ein qualifizierter Slack pro AC-Insel oder Capability-BLOCK |
| **T-16** | lineare/nichtlineare Shunts, Sections und q-/b-Zeichen; spannungsabhängige Last | fixe g/b exakt, Stufen/ZIP als APPROX mit Grenzen; Quellgeräte erhalten |
| **T-17** | HVDC point-to-point lossless, verlustbehaftet vorwärts/rückwärts, zwei AC-Inseln, unbekannter Converter, MTDC | `NUM-07`, keine falsche Reverse-Link-Effizienz, kein AC-Inselmerge; Unsupported-Vermutungen BLOCK |
| **T-18** | `Ω ↔ pu`, `S ↔ pu`, Transformer-Datenblattbasen, Einheitsetikett fehlt, implizites PyPSA-0 | `NUM-01`, Provenienz für alle elektrischen Werte; missing ≠ default ≠ zero |
| **T-19** | mehrere CurrentLimits pro Terminal mit forward/reverse, dauerhaft/zeitlich begrenzt, Saison und Spannungsspanne | alle Original-Limits erhalten; `NUM-08` nur bei Spannungshypothese; kein blindes `s_nom` mit Notfallgültigkeit |
| **T-20** | PyPSA-View: Line-only, 2W, 3W, PST, Link, mehrere Inseln; gleiche Daten an bestehenden Reduktionsadapter | PyPSA-Komponenten, FK/Portzuordnung/`active` korrekt; bestehender Adapter verweigert unqualifizierte Sonderfälle ausdrücklich, **keine** Drop-/Success-Verwechslung |

### 4.3 Export, Referenz-Lastfluss und Systemqualität

| Test | Prüffall / Fixture | Erwartetes prüfbares Ergebnis |
|---|---|---|
| **T-21** | Import → unveränderter Export 1 → Reimport; gezieltes SSH/SV-Feld-Delta; mRID/Unknown Attribute/Boundary-Stresstest; 3W-Star-Änderung ohne Inverse | `NUM-09` auf unveränderte Tripel und Original-IDs; erlaubte Deltaänderung mit aktualisiertem Modellheader, keine stillen Deletes; nicht invertierbare Änderung BLOCK + Loss-Report |
| **T-22** | Plain PyPSA mit vollständiger synthetischer Equipment-/Authority-Vorgabe, anschließend derselbe ohne Spannung/Terminal/Boundary-/Datenquelle; bidirektionales lossy HVDC | neues **synthetisch markiertes** valides EQ/SSH/TP-Profilset nur bei Vollständigkeit; fehlende obligatorische CIM-Eigenschaften BLOCK; historische mRIDs niemals behauptet |
| **T-23** | geeignetes CGMES EQ/SSH/TP/SV mit lösbarer AC-Referenz und vollständig erklärter Slack-/Tap-/Converter-Policy; widersprüchlicher SV-Snapshot | reproduzierbarer AC-PF-Vergleich in p.u., Winkel, P/Q je Terminal, Verlust-/Inselbilanz; Messgrößen je Gerät, diagnostisches PASS nur bei geeigneter SV; Widerspruch objektbezogen markiert |
| **T-24** | QA-/Audit-Manifest aus positiven und negativen Prüffällen, Konfigurationsänderung, neues Schema-Minor, gestörte Daten | Report mit Abdeckung, Profilen, Versionen, Seeds falls nötig, Hashes, PASS/BLOCK und Count/Types der Annahmen/Verluste; Regression/SemVer-/Snapshotgates |

### 4.4 Nachweis-Datenmatrix und spätere Durchführung

| Fixture | Größe / Eigenschaften | Primäre Tests | Erwarteter Zweck |
|---|---|---|---|
| F-01 | 2-Bus AC-Leitung + Generator + Last + Shunt | T-12, T-15, T-16, T-18, T-23 | Grund-P/Q-/Einheiten-/PI-Konvention |
| F-02 | Node-Breaker mit 4 ConnectivityNodes/3 Switches, TP-Soll | T-07, T-08, T-09 | Schalter-/Topologie-Faltung |
| F-03 | 2- und 3W-Transformer mit Ratio/Phase Taps | T-13, T-14, T-20 | Stern-/Ybus-/PST-Gleichheit |
| F-04 | zwei IGMs/Boundary Set/Äquivalentinjektion | T-01–T-06, T-10, T-21 | Version, Authority, mRID, Referenzen |
| F-05 | 2 AC-Inseln über point-to-point HVDC mit Verlusten | T-09, T-17, T-20 | AC-Island und Port-/Loss-Physik |
| F-06 | mehrere Limits/Dauern/Richtungen, GL mit CRS | T-10, T-11, T-19 | Geo und Betriebsgrenzen |
| F-07 | exportierte 2.4.15- und 3.0-Profilsets aus F-01–F-06 | T-21, T-22 | semantische Round-trips, Original-/Synthetic-Vertrag |
| F-08 | **lizenziertes echtes** IGM/CGM mit verlässlichem LF/SV | T-01–T-24 nach Relevanz | unabhängige Realnetzqualifikation, **noch nicht vorhanden/geprüft** |

Mindestens zwei voneinander unabhängige validierte Backend-Abbildungen sind für das spätere Black-Box-Paritätsexperiment T-06 **SOLL**, nicht eine vorgreifende Backendauswahl. Alle Datenfixture-Objekte erhalten Version/Hash/Profil-/Lizenzmetadaten.

## 5. Konsistenzregeln für Energiebilanz, Inseln und SV

### 5.1 Sign- und Bilanzregeln

Positives Generator-`injection_p_mw` speist den AC-Bus; positives Last-`demand_p_mw` entnimmt Leistung; ein positiver terminalbezogener Branch-P-Wert bedeutet (in der eigenen definierten Orientierung) Entnahme aus dem Bus ins Branchmodell. Bei passiver AC-Leitung gilt inklusive Verlusten üblicherweise `P_0+P_1=P_loss≥0` (solange keine aktiven Einbauten). Ein HVDC-Link besitzt eigene deklarierte Bus-Portzeichen und `P_loss`, niemals die Annahme `P_0+P_1=0` bei verlustbehaftetem Transport. `Q`-Bilanz umfasst Leitungs-/Transformator-Ladesuszeptanz, Shunts und Spannungs-/Tap-Wirkung.

**Pro AC-Insel:** `Σ P_gen_inj + Σ P_external_inj − Σ P_load − Σ P_shunt_withdrawal − Σ P_net_branch_withdrawal − Σ P_hvdc_net_withdrawal = 0`, wobei Branch-Portleistungen **nur an den betrachteten Inselgrenz-/Bus-Porten** summiert werden und bei `Σ` über alle Busse die passiven Leitungsverluste korrekt als positive Restentnahme erscheinen. Eine Unausgeglichenheit des unsolved SSH-Inputs ist **keine** Rechtfertigung, unbemerkt einen Slack-Generator mit Quelle zu erfinden. Bei AC-LF ist die berechnete Slack-Leistung als `DERIVED` zu dokumentieren und mit Annahmen zu vergleichen.

**SV-Vergleich:** Solved `SvVoltage` und `SvPowerFlow` enthalten Referenzgrößen, deren exakte Reproduktion nur bei vereinbarer Netzgrundlage (EQ/TP/SSH), Netzstatus, Tap-Stellungen, stationärer Methoden-/Slack-Definition und Konvertervereinfachung zu erwarten ist. Im Report werden gemessene Abweichungen und **Eligibility** pro Insel/Gerät getrennt ausgewiesen; ein offener/stiller Widerspruch blockiert eine angeblich exakte LF-Qualifikation, aber nicht zwangsläufig den verlustbewahrenden Import.

### 5.2 Grenzwerte und Verluste

Ein normales, dauerhaftes `CurrentLimit` ist kein universelles N-1- oder saisonales MW-Kapazitätslimit. Grenzwerte werden nach `equipment, terminal, direction, duration, type, valid_from/to, season, contingency_context` gesichtet; mehrere gleichzeitig wirksame Regeln bilden eine Restriktionsmenge. PyPSA-`s_nom` darf nur nach festgelegtem konservativem Modellannahmeprotokoll entstehen. `0` Grenzwert ist ggf. ein tatsächliches Verbot, `null` ist ein fehlender Grenzwert, `∞` als Default aus PyPSA ist **keine** Quellenmessung. Insel- und Gleichspannungslimits bleiben getrennt. Spätere N-1-basierte Äquivalentgrenzen entstehen erst in Modul 1, nicht hier.

### 5.3 Identitätserhaltungs-Metriken

Mindestens ausgeben:

- `source_object_count_by_class_profile`, `unique_mrid_count_by_authority`, `canonical_equipment_count`, `active_view_count_by_pypsa_component`, `synthetic_star_bus_count`, `inferred_topological_node_count`.
- `unresolved_ref_count = 0` (ausgenommen ausdrücklich bekannte externe Boundary-Refs in dokumentiertem Pending-Scope); `duplicate_mrid_conflict_count = 0`; `source_to_view_unmapped_relevant_count = 0` oder listet jede zulässige Auslassung mit Capability-Freigabestatus.
- `country_missing_active_bus_count = 0` für Modul-1-Freigabe; `geo_missing_count` + Coverage nach Land/Klasse; `coordinate_crs_unknown_count`; `wrong_tp_membership_count = 0` für akzeptierte Topologie.
- `source_untouched_triples_changed_count = 0` für Modus 1; `original_mrid_preservation_rate = 100%` für unveränderte Objekte. Ein neues SV-Resultat darf zusätzliche neue mRIDs haben, muss diese jedoch ausdrücklich unterscheiden.
- `electrical_value_origin_counts` SOURCE/DERIVED/DEFAULT/MISSING, `assumption_count_by_severity`, `loss_manifest_count_by_class`, `export_created_ids_count` und `export_removed_ids_count`.

## 6. Traceability, Nachweisergebnisse und Freigabecheckliste

**Anforderung→Prüfungen:** die Spalte „Testnachweis“ in [10_REQUIREMENTS.md](10_REQUIREMENTS.md) ist die verbindliche zeilenbezogene Traceability für **REQ-001 bis REQ-048**. In dieser Datei sind genau `T-01` bis `T-24` spezifiziert. `REQ-X01…X08` sind Scope-Ausschlüsse, keine positiven Tests. Bei Umsetzung verlangt das Freigabemanifest für jedes MUSS: `requirement_id, test_id, fixture_hash, result, evidence_uri, exception_id`; wenn ein Test mehrere Anforderungen abdeckt, muss er die jeweilige Invariante einzeln bewerten.

**G0 – Import/Versionskonformität:** Profile/Modelheader/Dateihashes/Authorities vollständig und syntaktisch zugeordnet; Unsolved-/Solved-Modus explizit.  
**G1 – Netz-/Identity-Integrität:** FK, mRID, Boundary, Ports, Switch-/TP-Abgleich und aktive Bustransparenz ohne offene BLOCKs.  
**G2 – Elektrotechnik:** Geräteparameter/Einheiten/Basen/PQ-Sign, PI/Ybus, Tap/3W/HVDC und Grid Islands nach Fähigkeit qualifiziert.  
**G3 – PyPSA/Modul 1:** Originaldetailnetz gefroren, keine unbegründeten Komponentenverluste, Capability der nachgelagerten Adapter tatsächlich geprüft.  
**G4 – Export:** jeweils Modus 1 oder Modus 2 separat, Loss-Manifest vollständig, Graph-/Identity-Transaktionsgates bestanden.  
**G5 – SV/Lastfluss:** **nur falls Input-SV geeignet**; ohne geeignetes SV „NOT_APPLICABLE_NO_SV“, kein vorgetäuschtes PASS.

### 6.1 Minimaler zukünftiger QA-Report (Schema-Skizze)

```yaml
report_schema_version: "1.0.0"
repository_baseline: "1595d6d38e77804760612621657721b3699d2fea"
dataset:
  input_hashes: ["<sha256>"]
  cgmes_family: "2.4.15"  # oder "3.0"
  model_header_ids: ["<source-id>"]
  graph_hash: "<sha256>"
  profile_set: ["EQ", "SSH", "TP", "SV"]
canonical:
  contract_version: "1.0.0"
  network_revision_id: "<id>"
  config_hash: "<sha256>"
  backend_name_and_version: "<name/version>"
  source_object_counts: {}
  canonical_component_counts: {}
  pypsa_component_counts: {}
  synthetic_mapping_counts: {}
  geo_country_coverage: {}
  island_count: null
checks:
  - requirement_id: "REQ-013"
    test_id: "T-07"
    fixture_hash: "<sha256>"
    status: "NOT_EXECUTED"
    evidence_uri: null
    exceptions: []
capabilities:
  CANONICAL_IMPORT_READY: "NOT_ASSESSED"
  PYPSA_ACPF_READY: "NOT_ASSESSED"
  PYPSA_LPF_READY: "NOT_ASSESSED"
  REDUCTION_ADAPTER_READY: "NOT_ASSESSED"
  UPDATE_EXPORT_READY: "NOT_ASSESSED"
  CREATE_EXPORT_READY: "NOT_ASSESSED"
loss_manifest:
  exact_count: null
  approximated_count: null
  nonreconstructible_count: null
overall: "DESIGNED_NOT_EXECUTED"
```

## 7. Wissenschaftliche Unterscheidungen und verbleibende Nachweise

1. **CGMES-Profilkonformität ≠ funktionale PyPSA-Repräsentierbarkeit.** Ein gültiger CGMES-Import kann Sonderkomponenten enthalten, die nicht als exakte `Line/Transformer/Link`-Kombination abbildbar sind.
2. **Elektrische Äquivalenz ≠ Identität.** 3W-Sternäste, gefaltete Switches und ersetzte HVDC-Ports können beim Lastfluss äquivalent, aber keine 1:1 historischen CIM-Equipmentobjekte sein.
3. **Steady-state ≠ vollständiger Steuerungs-/Grenzwertvertrag.** Vereinfachte Generatorregelung und HVDC-Verlustannahmen müssen gesondert qualifiziert werden; Schutz-/Dynamikmodelle außerhalb Scope.
4. **Round-trip von unverändertem Originalgraph ≠ Neuerzeugung aus PyPSA.** Ohne Raw-Graph und Sidecar fehlen reale Node-Breaker-, Boundary- und Provenienzdetails irreversibel.
5. **CGMES-2.4.15 ≠ CGMES-3.0.** TPBD/EQBD sowie Profilpfade und Pflichtassoziationen dürfen nicht unbesehen wiederverwendet werden [C1–C3].
6. **Modul 0 ≠ Modul 1.** Hochaufgelöste Zeitreihen/Wetter/Dispatch, Clustering und Grenzwertkalibrierung bleiben strikt außerhalb. Der realnetzbezogene Modul-1-PyPSA-End-to-End-Nachweis fehlt am Basiscommit weiterhin.

**Keine numerischen Ergebnisse oder PASS-Nachweise wurden erzeugt.** Die Abnahme dieser Forschungsarbeit betrifft ausschließlich Spezifikationsvollständigkeit und fachliche Konsistenz.

## 8. Quellen

- **[R1]** [IoSN Band II — Architektur und Detailnetz-Input-Verträge](../IOSN_2026_Band_II_PyPSA_Implementierung.md), [Repository Audit](../../REPOSITORY_AUDIT.md), [README](../../../README.md), `src/tyndp_reduce/pypsa_adapter.py`, jeweils verbindlicher Ausgangscommit.
- **[C1]** ENTSO-E, [CGMES Library v2.4/v3.0, IEC-Verweise](https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/).
- **[C2]** IEC, [61970-600-2:2021, Exchange Profiles](https://webstore.iec.ch/en/publication/63867), 61970-600-1:2021 (*Structure and Rules*).
- **[C3]** ENTSO-E, [2.4.15 Profile](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/140807_ENTSOE_CGMES_v2.4.15.pdf), [Implementation Guide](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/160315_ImplementationGuide_CGMES_2_4_15.pdf), [Quality of CGMES Datasets and Calculations](https://www.entsoe.eu/Documents/Network%20codes%20documents/Implementation/cacm/cgmm/Quality_of_CGMES_Datasets_and_Calculations.pdf).
- **[P1]** PyPSA, [Power Flow: transformer/line equations and controls](https://docs.pypsa.org/latest/user-guide/power-flow/), [Design/Components](https://docs.pypsa.org/latest/user-guide/design/).
- **[P2]** PyPSA, [Links: signed ports, efficiency and controllable flow](https://docs.pypsa.org/latest/user-guide/components/links/).
- **[S1]** [SiennaSchemas: unit-annotated schemas](https://github.com/Sienna-Platform/SiennaSchemas/blob/main/docs/PIPELINE.md).
- **[G1]** [Power Grid Model IO: mapping configurations and units](https://power-grid-model-io.readthedocs.io/en/stable/).

**Dokumenten-Abnahmestand:** Die Anforderungen, kanonischen Beziehungen, mathematischen Prüfungen und beide Exportmodi sind **spezifiziert**, nicht evaluiert. Für produktive Erfüllung sind echte Versionen/Backends, geeignete CGMES-Fälle und unabhängige Prüfergebnisse erforderlich.
