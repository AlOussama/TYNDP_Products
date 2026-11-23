# ML-C19/04 – KerML 1.0 / SysML v2.0 Semantik und Contract-Eignung
**Normative Hauptquellen:** [KerML 1.0 formal/2026-03-01](https://www.omg.org/spec/KerML/1.0/PDF), [SysML v2.0 Part 1 formal/2026-03-02](https://www.omg.org/spec/SysML/2.0/Language/PDF), [API 1.0](https://www.omg.org/spec/SystemsModelingAPI/1.0). Die OMG-Spezifikationsseiten führen ergänzende maschinenlesbare XMI, JSON-Schema und Bibliotheks-KPAR auf. Pilot [SysML-v2-Release 2026-09.1](https://github.com/Systems-Modeling/SysML-v2-Release/releases/tag/2026-09.1) ist **nicht** die normative Neudefinition SysML 2.1/KerML 1.1. Status: Standardspezifikationen gelesen, keine ausgeführte Pilotparser-E2E-Konformitätsprüfung.

## KerML-Konzepte und Reduktionshypothesen
| Standardkonzept | Kernbeitrag | benötigte Teilmenge / Vorsicht |
|---|---|---|
| Type und Feature | explizite Typisierung mit Feature-Membership | typed Entity/Property; nicht vollständigen allgemeinen Type-Graph importieren |
| Definition/Usage als Modellierungsmuster | Trennung Klassifikation und Verwendung | wiederverwendbare Rollen-/Interface-Definition vs Komponenteninstanz |
| Membership / Relationships | eindeutige Ownership, Referenz und semantische Beziehungen | typed relation, URI/ID; Alias kollisionssicher |
| Specialization, Redefinition, Subsetting | Untertyp-/Einschränkungsbeziehungen und Ersetzungsprüfung | nur kontrollierte Semantik; Re-Definition darf REQUIRED nicht stillschweigend lockern |
| Namespace resolution | stabile Referenzauflösung | fully-qualified IDs; nicht durch lokale Namensähnlichkeit gleichsetzen |
| Multiplicity | Port-/Teilbeziehungs-Kardinalität | externe Port/Connection Constraints; kein interner Komponentenbaumzwang |
| Expression/Constraint | auswertbare Bedingungen und formale Constraints | nur benötigter decidable typed predicate subset für automatische E1 |
| Metadata | Annotationen | Authority, Status, Traceability als **CSNF-eigene**, unverlierbare Fachdaten |

KerML 1.0 §Type/Feature-Semantik (u.a. PDF S. 148 gedruckt, PDF-Seite 173) definiert abgeleitete Feature-Memberships und deren Typ-/Richtungseigenschaften; daraus wird **nicht** bereits eine Energie-Contract-Massenbilanz.

## SysML v2 Fachbegriffe
- PartDefinition/PartUsage und PortDefinition/PortUsage unterstützen Typ/Instanz-Trennung. SysML PDF §8.3.12.5 PortDefinition (gedruckt S. 294, PDF-Seite 325) bezeichnet den externen Verbindungspunkt. Konjugierte Ports tauschen input/output-Semantik; die Umkehr ist ein semantischer Vorgang, keine freie Umbenennung.
- Connections/Interfaces modellieren Interaktion und Endpunktstruktur. Ein physikalischer Einspeisebegriff, Strom-/H2-Carrier oder Energieerhaltung sind **zusätzliche fachliche Constraints**, nicht aus jeder Connection ableitbar.
- RequirementDefinition/RequirementUsage plus ConstraintDefinition/ConstraintUsage: Im PDF §8.3.21 (PDF-Seiten 388–391) besitzt RequirementDefinition getrennte assumedConstraint und requiredConstraint (RequirementConstraintKind assumption vs requirement), subject/stakeholder und optionale Dokumentation. Das liefert ein geeignetes A/G-Strukturmuster; es definiert jedoch nicht automatisch die gesamte CSNF-Governance für REQUIRED/PERMITTED/OWNER_TBD oder prozessübergreifende Ergebnis- und Vergleichssemantik.
- VerificationCase/RequirementVerificationMembership (§8.3.24, PDF-Seite 406) liefert formale Verifikationsbeziehungen; eine solche Relation ist nicht dasselbe wie bereits vorhandene PASS-Evidence.
- Quantities and Units Domain Library / Analysis Domain Library, Views und Traceability sind relevant für Units, Prüfkontexte und Austausch; CBA- und modellübergreifende unabhängige Evidence-Identitäten bleiben zu profilieren.

## Assume-Guarantee und Modelling Freedom
Die mögliche CSNF-Abbildung lautet: Part/Port Usage -> Referent, Connection -> TypedRelation, assumedConstraint -> Assume-Klausel, requiredConstraint -> Guarantee-Klausel, RequirementUsage -> ScopedAssertion, VerificationCase -> EvidenceRequest. Eine modellierbare **Schnittstelle** verlangt dabei nicht, dass die innere mathematische Optimierungsvariable als SysML PartUsage repräsentiert wird. Zwei Modelle mit verschiedener interner Speicher-/PTDF-Algebra können dieselbe externe Part-Rolle implementieren.

**Profile-Gap:** explizite Normativität PERMITTED/PROHIBITED/IMPLEMENTATION_DEFINED, Governance-Status OWNER_TBD, Authority-Prioritäten, versionierte physikalische Carrier-/Sign-/LHV-Semantik, garantierte Servicefähigkeit, Modellvariations- und nichtäquivalente Robustheitsregeln, Evidence-Status. Diese sind CSNF-Hypothesen; normativ gegebene Standardsemantik wird nicht neu behauptet.

## Nullhypothese und Kosten
KerML/SysML liefert **viele notwendige Mechanismen**, aber eine systematische implementierte Normalisierungs-/äquivalenzentscheidende Contract-Semantik für alle SLR01–42 ist in den genannten Standards nicht als vorhandener nativer CSNF-Dienst nachgewiesen. Profile können einen CSNF-Export erlauben; vollständige Metamodellübernahme erzeugt zusätzliche Ownership-, Inheritance-, Multiplicity- und Library-Komplexität. Vergleich A/B/C deshalb ergebnisoffen; kein formaler SysML-Compliance-Claim für die konzeptionellen Mappings.

**Evidenz:** NORMATIVE_SPEC inspected, IMPLEMENTATION_REPO located, PILOT_MAPPING conceptual, NATIVE_TEST_ML_C19 NOT_EXECUTED. Offene Frage: verlustfreier bidirektionaler Export *inklusive* Provenienz und Normativität benötigt einen realen Pilotversuch in ML-C21.
