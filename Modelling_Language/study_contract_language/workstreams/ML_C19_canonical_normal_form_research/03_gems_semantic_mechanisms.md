# ML-C19/03 – GEMS Component-, Interface- und Graphmechanismen
PIN AntaresSimulatorTeam/GEMS @ c463e30b610443c1f59b20074bb7acffa2844cce. Code-/Dokumentationsinspektion: [library.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/library.md), [system.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/system.md), [Compatibility](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/COMPATIBILITY.md). Stand 2026-11-23; dokumentierte Funktion ist noch kein nativer ML-C19-Interpreternachweis.

## Nachweisbare Struktur
Library enthält port-types mit fields; models mit ports, Parametern, Variablen, constraints, binding-constraints und weiteren Formulierungsobjekten. Porttypen können libraryübergreifend referenziert werden. Systemdatei instanziiert Komponenten über library_id.model_id, weist Daten zu und definiert connections mit component1/component2 und port1/port2. Das Beispiel Bus-Balance verwendet sum_connections(flow_port.flow) = 0; es instanziiert ein mathematisches Balancegesetz, nicht automatisch einen physikalischen universellen Einspeisebegriff. Felder sind laut library.md skalare float-Werte, die mathematische Ausdrücke über Verbindungen austauschen. Explizite typisierte Carrier-, SI-Units-, Sign- und Verhaltensgarantie als universelle semantische Portpflicht ist durch diese Dokumentation NICHT belegt.

| GEMS-Begriff | Wiederverwendung für CSNF | verwerfbare Implementierungsbindung |
|---|---|---|
| model vs component | Rollendefinition vs Instanz mit stabiler ID | konkrete Library-Modellform als einziger Implementierungstyp |
| port-type + field | getyptes externes Interface, Field-Identität | Annahme: field=power definiert Carrier, Richtung, Einheit |
| connection + graph | getypte Topologie und Referenzprüfung | zwingend ein portgebundenes algebraisches Gleichungsschema |
| binding-constraint | Beispiel eines expliziten Balance-/Verbindungs-Guards | Pflicht zur GEMS-Gleichungsgrammatik für jede CSNF |
| taxonomy | kontrollierte Rollenklassifikation, kompatible View-Zuordnung | Taxonomie fordert identische interne Variable-IDs |
| library version | Referenz auf externe Implementierung und Kompatibilität | Versionskonformität = fachliche Konformität |
| time/scenario parameter | Gültigkeit nach Zeit und Szenario | implizite Stundenlänge, Szenariowahrscheinlichkeit oder Exogenitätsregel |
| output catalog / views | Observable-Mapping, Aggregationsidee | gleichnamige KPI ohne gleiche Semantik |

## Drei getrennte Kompatibilitäten
1. **Interface compatibility:** Carrier, Größe, Dimension, Unit, absolute Sign-Konvention, Richtung, Zeitbasis und Verbindungspunkt sind typkorrekt; auch Connect-Cardinality.
2. **Behavioural conformance:** Bei geltenden Annahmen werden externe Guarantees und ggf. erforderliche Servicefähigkeiten erfüllt; benötigt Trace/Orakel/Witness.
3. **Internal mathematical compatibility:** konkrete GEMS-Model-Libraries und Interpreter können gemeinsam in ein Mathemodell übersetzt werden. Eine bestehende globale Library kann diesen dritten Punkt fördern, die ersten beiden nicht ersetzen.

Beispiel Batterie: Port elec_grid, active_power MW, sign positive injection (injektion), feste Netzanschlussreferenz BUS_A; -P_charge_max <= p_grid <= P_discharge_max, AvailabilityGuard, ausgelagerte Energieledger- und Boundary-Condition-Pflicht, gewünschtes Evidence/Observable. Modell A verwendet SOC (dimensionslos), Modell B einen Energiezustand in MWh oder allgemeine dynamische Algebra. CSNF verlangt nicht denselben Variablennamen und nicht zwingend ein explizites state variable, sofern die äußere Leistungs-/Energiegarantie nachweisbar bleibt. Eine GEMS Library kann eine konkrete mathematische Implementierung liefern, aber nicht automatisch die gesamte äußere fachliche Vertragssemantik.

## Graph und Versionierungsgrenzen
Physikalische Branches, Busanbindung und steuerbare Market Links benötigen getrennte fachliche Rollen; bloße Adjazenz definiert weder KVL noch Marktregel. Port-Orientierungen werden nicht ohne Sign-Tabelle zusammengeführt. system.yml-Datenabhängigkeit time-dependent/scenario-dependent ist von fachlichem Informationszeitpunkt oder nonanticipativity zu trennen. COMPATIBILITY.md nennt v0.6.1 und Interpreter-Versionen: Dokumentations-/Language-Version und Engine-Version bleiben explizite, separate Identitäten.

## Bewerteter Stand
Dokumentation D_DOC für Library, System, Graph, Typfelder; vorhandene Models und Tests I_EXAMPLE/T_EXISTING nach ML-C18/03. Kein GEMS-parser-run, keine Batterieswap-Simulation, kein A/G-Nachweis, keine verifizierte dimensionsphysikalische Portprüfung in ML-C19. Fehlende Evidenz zu Unit-Safety = NOT_VERIFIED, nicht Beweis der Unfähigkeit. **Reuse: ADAPT_PORT_GRAPH; kein vollständiges GEMS-Schema als CSNF-Kern.**
