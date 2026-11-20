# ML-C18 / 05 – Component Behaviour Contract Reference
**Status: non-normative scientific reference.** Jede Zahl ist als *synthetische Beispielannahme*, nicht als ENTSO-E-/IoSN-Vorgabe zu verstehen. Keine DSL, kein Parsererfolg. Anforderungen: ML-C18/01 SLR12–26, 35–38, 40.

## 1 Kernhypothese und Substitutionsregel
Prüfhypothese `C=(Interface, A, G, Applicability, Observables, VariationPolicy, VerificationRequest)`. Objektidentitäten/Provenienz und Einheiten-/Zeitsemantik sind Metadaten, die teils in Interface/Scope integriert werden können. Minimalitätsentscheidung erst nach Ablation.

**Außensemantik:** Der Component Contract enthält eine Menge `L_C` zulässiger beobachtbarer Traces unter Annahmen A. Die Implementierung M hat bei festen exogenen Inputs und Profil `D` die Tracemenge `L_M`. Für eine als Safety Guarantee spezifizierte Verhaltenspflicht gilt `L_M | A ⊆ L_C`. Für zugesagte Flexibilitäts-/Servicefähigkeit muss zusätzlich die verlangte *Verfügbarkeit* nachgewiesen werden (Safety inclusion allein lässt ein "immer aus"-Modell fälschlich zu). Formalisierte Surjektivität/Abdeckung nur auf dem gewählten Observable- und Service-Niveau; nicht pauschal `L_M=L_C`. Prüftiefen: Syntax, statischer Typ, synthetischer Trace, mathematischer Witness, native Modellkonformität. `A=false` ist kein akzeptabler Beweis; A muss erfüllbar, kontrollierbar und für das Vergleichsszenario plausibel sein.

**Keine Black-Box-Verkürzung:** Bei zeitgekoppelten Komponenten reichen Portgrenzen nicht. Mindestens ein nach außen verifizierbarer intertemporaler Energie-/Stoff-Ledger, Endzustands-/Servicebedingung, Verlustsemantik oder ein zulässiger interner Witness muss die Bilanzpflicht sichern.

**Normativität:** `REQUIRED/PROHIBITED` determinieren Verhaltensregeln, `PERMITTED` legt zulässige Umsetzungen fest, `IMPLEMENTATION_DEFINED` erfordert Deklaration, `CONDITIONAL` wird über `guard` repräsentiert, `OWNER_TBD` blockiert ggf. konkrete Konformitätsentscheidung. Keine Annahmen als unbewiesene Defaults.

## 2 Batteriespeicher (RC01)
| Teil | Fachlich äußerer Contract | Keine automatische Festlegung |
|---|---|---|
| Grid-Port | Anschlussbus B, AC active power `P_grid` in MW, positive Einspeisung, negative Aufnahme; Zeitintervalle Δt in h | Variable `state_of_charge` |
| Leistung | `-P_charge,max(t) ≤ P_grid(t) ≤ P_discharge,max(t)` unter declared availability; net-only observable genügt nicht immer zum Prüfen von simultanem charge/discharge | ein- oder zweifacher Power-Var-Split |
| Energie | konsistente Summenbilanz über Δt: gespeicherte Energieänderung = aufgenommene elektrische Energie nach Ladewirkungsgrad - abgegebene Energie vor Entladewirkungsgrad - Standby-/Hilfsverluste; keine Energieerzeugung | algebraische Rekursion vs Integralkriterium |
| Randfälle | E0/Eend, Kapazität und Verlustgrundlage müssen bezogen auf den Profile-Scope definiert sein; wenn nicht festgelegt, OWNER_TBD | cyclicity ohne fachlichen Grund |
| Verifikation | Portchronologie, Energie-Witness oder äquivalenter Bilanznachweis, DC/AC Leis­tungsgrenze, Zeitindex, Vergleichsprojektion | solver-spezifischer Status |
**Rechnerisches Witness, nicht vorgeschriebene Implementierung:** `E_{t+1}-E_t=η_c·P_charge,t·Δt-P_discharge,t·Δt/η_d-L_t·Δt` für die gewählte Verlustdefinition und nichtnegative separate Lade-/Entladeflüsse. Eine alternative interne Net-Power-Form kann unter zusätzlichem Mode-/Richtungs- und Piecewise-Witness konform sein. Netto-Port `P_grid=0` allein beweist nicht, dass kein simultanes Laden/Entladen mit Verlusten stattfindet.

**Variante A:** Einzelakku/technology-resolved mit E(t), Pch,Pdis und expliziter zyklischer oder terminaler Randbedingung. **Variante B:** Aggregierter Speicherpool mit Energy-Envelope oder verlustkorrigiertem Boundary-Integral; nur konform, wenn gemeinsame äußere Leistungs-, Energie- und Verfügbarkeitsregion begründet abgedeckt wird. Aggregierte Powergrenzen allein genügen nicht. **Negative Mutation:** 10 MW Aufnahme während 0,5 h mit nur 0,5 MWh Speicherkapazität ohne weiterer Erklärungsquelle; oder Verluste ignoriert, obwohl `REQUIRED`. Positiv: alternative E-Variable statt SOC-Pu unter identischer Energie-/Powerprojektion.

## 3 EV-Fahrzeuge / Flotte (RC02)
- **Ports:** Bus/Anschluss, Richtung, kW/MW, Δt, tarif-/Netzbereich; `V2G=false` als `PROHIBITED` negative Einspeisung; `V2G=true` nur falls die jeweilige Studienquelle dies zulässt.
- **Mobilitätsservice:** Bedarf je Abfahrtszeit/Vehicle-group, Ankunftszeit, Maximal-Ladeleistung, Energieservice und Verlustgrenzen. Nutzerpräferenzen, Nichtverfügbarkeit und Chargeranzahl zuordnen.
- **Varianten:** A individuelle Fahrzeuge mit Lade-/Ankunftsentscheidungen; B Flottenmodell mit Zeit-/Energie-Flexibilitätsenvelope. Nur dann gleichwertig, wenn Pooling nicht die Zuverlässigkeit individueller Abfahrtsenergie verletzt. Abstraktion ist bewusst nichtäquivalent, wenn der Contract ausschließlich einen definierten Flottenservice verlangt und die Individualabweichung dokumentiert; nichtäquivalent heißt nicht unkonform.
- **Negativ:** Aggregation erfüllt Summe MWh, aber lässt für ein Fahrzeug vor dessen Abfahrt 0 MWh verfügbar; dies verletzt individuell spezifizierte Servicepflicht. V2G ohne Autorisierung ist Nonconformance. **Positiv:** zwei unterschiedliche Ladeprioritäten und SOC-Zustandsdarstellungen erfüllen identische Abfahrtswitnesses.

## 4 Elektrolyse und H2-Umwandlung (RC03)
- **Ports:** Stromnetz-Bus, positive AC-*Entnahme* in MW oder eindeutig negative Einspeisung; H2-Netz-Einspeisung in kg/h; optional Wärme in MWth, Wasser und O2 mit eigener Stoff-/Einheitenbeschreibung. Balance nur mit verbindlicher LHV- oder HHV-/Reinheitsdefinition; MWh/kg nicht direkt mit kg/h vergleichen.
- **Garantien:** P_el-Grenzen, Betriebsverfügbarkeit, Start-/Stopp- oder Ramp-Pflichten wenn Fachprofil fordert, H2-Ausstoß mit angegebenem Conversion-/Loss-Envelope, Hilfsenergie und ggf. Nutzwärme-Witness. Keine implizit 100%-Umwandlung; Variation in Teillast/Temperatur nur innerhalb erlaubter H2-Power Envelope.
- **Variante A:** linearer konst. spezifischer Energiebedarf; **Variante B:** zulässige stückweise Effizienz-/Betriebskennlinie. Wenn das Forschungsprofil nur Effizienzband fordert, dürfen Ergebnisse innerhalb des Bandes variieren (R3) und sind nicht algebraisch äquivalent. Verlangt das Profil exakte Kennlinie, scheidet A ggf. aus.
- **Negativ:** H2-Massenstrom als MW bilanziert ohne Heizwert und Referenzbasis; Output außerhalb specified loss band. **Positiv:** verschiedene interne Elektrolyse-Stackgrößen mit gleichem beobachtbaren Leistungs- und Produktbereich.

## 5 H2-Speicher / Rückverstromung (RC04)
- **Ports:** H2-in und -out kg/h am H2-Netz, elektrische Rückspeisung MW am Bus, ggf. Abwärme MWth, jeweils getrennte Vorzeichen. Umrechnungen ausschließlich unter H2-Nutzenergie LHV/HHV, Zeitintegration Δt, Rückverstromungs-Wirkungsgrad, Verlustannahmen.
- **Garantie:** Wasserstoffinventar Anfang/Ende und kumulierte Massenerhaltung inkl. Leckage/Boil-off; Rückverstromung darf nicht mehr Energie abgeben als stoffliche Wasserstoffverfügbarkeit und Umwandlungsverlust zulassen. Druck-/Kompressionsenergie falls relevant.
- **Variante A:** expliziter Inventarzustand und Gas-/Powergrößen; **Variante B:** integrierte Netzfluss-/Speicher-Energiebuchhaltung mit nachgewiesener Massen-Energie-Witness. Kompressor- oder Gasdynamikaggregation nur, falls die resultierenden externen Grenzen gültig sind.
- **Negativ:** elektrische Rückspeisung ohne H2-Entnahme oder ohne sonstige Energiequelle; behauptetes η > 1 (bei konsistenter LHV-Systemgrenze) bei Verlustfreiheitspflicht. **Positiv:** intern massenbasierte oder energieäquivalente Zustände unter fester Heizwertkonvention.

## 6 Minimale notwendige Pflicht und Freiheiten
| Vertragsdomäne | Benötigt für Korrektheit | Zulässige Freiheit |
|---|---|---|
| Anschluss/Semantik | Port-ID, physikalischer Carrier, Position, Richtung, Einheit und Basis | interner Graph/Arraylayout |
| Restriktionen | externer Capability-/Operating Envelope, Szenario/Zeitraum | Variable-/Constraintanzahl |
| Intertemporalität | Energie-/Stoffledger, erforderliche Dienste und Randfälle | Zustandskoordinaten und Diskretisierungsform bei hinreichender Genauigkeit |
| Vergleich | eindeutig berechenbare Observables + Aggregation + Metadaten | Model Library/Engine/Solver |
| Assurance | Nachweis-/Coveragepflicht, Guardstatus und Traceability | Engineinterne Nachweisart bei identischer Beweistiefe |
| Strukturdifferenzen | Dokumentierte abstraktionsbedingte Hypothesen und physikalische Grenzen | zugelassene Nichtäquivalenz, aber kein Verletzen von Required |

## 7 Quellen, Test- und Reviewstatus
- GEMS Port-/Library-Definitionen: https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/library.md
- mathspec typed expressions and assumptions: https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/assumptions.md
- ML-C17 S2 only conceptual: https://github.com/AlOussama/TYNDP_Products/blob/c8bbedad390d0ba00604a0f499e79e9cff087138/Modelling_Language/iosn_formal_specification/workstreams/ML_C17_language_maturity_assessment/minimal_viable_iosn_contract_language.md
All component guarantees are **research-reference semantics**; no GEMS/mathspec native parser run, no real asset verification; explicit multi-model implementation witness: `NOT_EXECUTED`.