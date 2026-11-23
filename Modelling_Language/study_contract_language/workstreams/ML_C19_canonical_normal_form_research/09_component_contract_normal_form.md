# ML-C19/09 – Component Contract Normal Form und Assume-Guarantee
**Ergebnis:** vorgeschlagene Contract-Ansicht = Interface + Applicability/Scope + Environment/Data Assumptions + External Guarantees/Capabilities + Observables/Oracles + Variation/Disclosure + Verification Requests + Source/Authority. Gegenüber der Ausgangshypothese zusätzlich nötig sind Herkunft, Geltungsstatus und ausdrückliche Trennung safety-vs-capability.

## Semantik und Typstruktur
ComponentRole ist eine fachliche Rolle, keine Pflicht, für die Implementation die gleichen mathematischen Variablen zu verwenden.
ExternalPort: (port_id, component_role, carrier, physical_quantity, dimensional_signature, unit, sign_reference, direction/bidirectional, connection_point, temporal_support, scenario_support, multiplicity).
Assumptions: zulässige Außenbedingungen (Data Quality, Netzgrenzen, Umwelteingang, Service Requests); eine DATA_ASSUMPTION wird nicht als Garantie des Modells ausgegeben.
Guarantees: safety invariants (immer), Leistungs-/Servicefähigkeit (quantifizierte Nachfrage und Reaktion), zeitliche Verfügbarkeit und energie-/stoffphysikalische Trace-Ledger. Der Satisfaction-Test setzt explizite Annahmen voraus.
VariationPolicy: erlaubte interne Implementierungsentscheidungen, deklarationspflichtige Strukturdifferenzen, nicht erlaubte Approximationen und erforderliche Evidence.
VerificationRequest/Observable: prüfbarer äußerer Projektionswert, Einheit, Grenze, Zeitbasis, Toleranz, Prüftiefe, Konformitätsstatus.

## RC01 Batterie – äußerer kontraktueller Witness
Annahme: Stromanschluss BUS_A aktiv, Zeitdiskretisierung delta_t in h, bekannte initiale Energiemenge E0 und parametrisiertes Energieband [Emin,Emax]. Vorzeichen p_grid>0 Einspeisung, <0 Aufnahme.
Port: active_power [MW], connected_to BUS_A; keine implizite zweite Energiemenge.
Safety: -Pcharge_max <= p_grid(t) <= Pdischarge_max; AvailabilityGuard kann beide Grenzen weiter einschränken.
Externe zeitabhängige Ledger-Pflicht: Energieänderung in MWh muss aus gezeichnetem Aufnahme-/Abgabe-Trace und spezifizierten Wirkungsgrad- und Standby-Verlustannahmen nachvollziehbar sein. Beispiel für explizit erlaubte Richtungszerlegung:
  E(t+1)-E(t) = eta_c * max(-p_grid(t),0) * delta_t - max(p_grid(t),0) * delta_t / eta_d - L(t)
mit expliziten eta_c, eta_d, L und MWh-Support. Dies ist eine **mögliche fachliche I/O-Ledger-Formulierung**, keine Pflicht zu einer internen Gleichung oder SOC-Variable. Modellformen mit komplexeren Verlustkennlinien erfordern abgestimmten Garantie-Raum statt die vereinfachte Gleichung.
Boundary: E0 und Eterminal Bedingungen nach Source; fehlt Eterminal? => OWNER_TBD, kein zyklischer Default.
Service: falls zugesagt, für eine Menge zulässiger Abforderungsprofile muss ein Dispatch existieren, der alle Power/Inventory- und Terminal-Bedingungen erfüllt. Einzelne Trace-Übereinstimmung beweist keinen universellen Service.
Observable: signed p_grid(t), Ledger Check, Verlustbasis, Energieinventargrenzen/terminal witness, availability; Evidence darf eine geprüfte abstrakte Bound-/Certificate-Projektion nutzen.
Variation: A: SOC(t) dimensionslos, B: E(t) MWh, C: andere aggregierte interne Form; gleicher äußerer Contract ist möglich, sofern sie Nachweispflicht erfüllen. Negative Mutation: 2 MW 0.5 h = 2 MWh statt 1 MWh, oder Verletzung eta/Terminal; fail/block.

## RC02 EV-Flotte
Port elec.grid active_power [MW], connector identity, positive injection V2G nur wenn allowed. Assumptions: arrival/departure, charger constraints, exogenous mobility needs. Guarantees: individuelle Abfahrtsenergien bzw. explizit festgelegte Servicequantile; Aggregation darf Fristen einzelner Fahrzeuge nicht ausradieren. Variante A explizite Einzelfahrzeugbilanzen, B Envelope mit beweisbar gültiger Serviceprojektion. Negativ: erfüllte Flotten-MWh, aber ein Fahrzeug verpasst Deadline, oder V2G trotz Verbot. E5 möglich, E4 nicht generell.

## RC03 Elektrolyse
Ports: electric.grid MW consumption, hydrogen.h2_output kg/h, optional heat MWth/water kg/h; Point IDs und Richtungen getrennt. Guarantees: konversionsphysikalisches Verhältnis unter festgelegter LHV/HHV-Basis, Teillast/Availability und Emissions-/Wärmegrenzen soweit REQUIRED. Varianten: konstante kWh/kg vs nichtlineares/piecewise Effizienzband. Nichtgleichheit der verschiedenen Kennlinien ist bei verbindlichem externem Envelope ggf. E5. Negativ: elektrische MW unmittelbar gegen kg/h verglichen.

## RC04 Wasserstoffspeicher/Rückverstromung
H2 mass-flow Port kg/h, optional power Port MW und heat Port MWth; ledger mass inventory kg (oder Energieinventar MWh_LHV mit expliziter Konversionsgrundlage), Leak/Conversion, initial/terminal Guards. Varianten: kg-Massenmodell + separate FuelCell versus MWh_LHV-Äquivalent + integrierter Converter. Negativ: p_out ohne entsprechenden H2-Abgang oder erlaubte andere Energiequelle; HHV/LHV ohne Basiswechsel. Service Guarantee muss die Wahl des Umwandlungspfades zulassen.

## GEMS / mathspec / SysML Vergleich
GEMS Ports/Fields/Connections können Form und Modellkomposition abbilden, algebraische Constraints stammen aus Libraries; Carrier/Unit/A-G/Ownerstatus als äußeres Profil ergänzen. mathspec kann mathematische Invarianten im jeweiligen konkreten Spec modellieren, aber sein Assumptions-Abschnitt beschreibt Datenbedingungen, keinen externen Component Contract. SysML Part/Port Definition-Usage, Connection, Requirement assumption/requiredConstraint sind für den äußeren Contract strukturell sehr geeignet, benötigen Energiesystem-/Governance-/Variation-Profile. Keiner der drei Zielmechanismen beweist auf bloße Deklaration die tatsächliche E3/E4-Konformität.

## Prüfbare drei Ebenen
INTERFACE_OK: statische Port-/Carrier-/Type-/Sign-/Cardinality-Checks. BEHAVIOUR_CONFIRMED: dokumentiertes External-A/G/Witness-Orakel unter S, U und E. INTERNAL_MODEL_COMPATIBLE: konkrete Toolinterpreter und Model Libraries können das mathematische Modell aufbauen. Ein PASS der einen Ebene ist kein PASS der anderen.
Quellen: [GEMS Library pinned](https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/library.md); [mathspec Data Assumptions](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/assumptions.md); [SysML Specification](https://www.omg.org/spec/SysML/2.0/Language/PDF).
