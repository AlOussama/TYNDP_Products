# ML-C06 — Conditional Architecture Recommendation

**Ergebnis:** `ADR_DEFERRED`, `G1_BLOCKED`, `OWNER_ORACLES_TBD`. Keine normative Architektur- oder Sprachfestlegung.

## 1. Gemeinsame Architekturpflicht — unabhängig von A/B/C

Ein zukünftiger toolunabhängiger IoSN Requirements Contract benötigt einen unveränderlichen semantischen Referenzkern: SourceClause/Autorität + MA01-SR-IDs + Version/Scope + 87 R03 DataObjects und Prozess-Transformationen + mathematische M01–M18-Obligationen + Prozess P00–P17 + Output/KPI-Provenienz + R04 Verification/Evidence-Status. Physische Branch-/NTC-Link-Rollen, Entscheidungstiming über CY, eigene Jahrstudien, UTC/Δt, Stage-Guards, Evidenz/OwnerApproval und 6 Teststatus sind harte **semantische** Bedingungen. Der Kern ist eine Verantwortlichkeit, **nicht** die Festlegung auf einen bestimmten zentralen Software-Service oder auf Model-to-Model-Translation.

## 2. Bedingte Wahlhypothesen

|Situation / nachzuweisende Bedingung|Geeignete Hypothese|Gegennachweis / Umkehrbedingung|
|---|---|---|
|Fachprofile werden unabhängig gepflegt, Versionsmatrix ist klein und kontrollierbar, eindeutiger Cross-Profile-Resolver besteht|**A** als bevorzugter Evaluierungskandidat|Wenn Release-Tupel oder referenzielle Mehrdeutigkeit überproportional Fehler erzeugen: B prüfen|
|Ein domänenübergreifendes AST und zentrales Semantic-Versioning werden organisatorisch akzeptiert und echte Mathe-Primitiven sauber integriert|**B** als bevorzugter Evaluierungskandidat|Wenn jeder kleine Input-/Math-Change globale Adapter-Umbauten auslöst: A prüfen|
|Nachweisbare Standardsysteme sollen die führenden Fachviews bleiben, es gibt ein Governance-Ledger und bezahlbaren **verlustfreien** Mapper-/Parserbetrieb|**C** als bevorzugter Evaluierungskandidat|Wenn zwei Quellen Anspruch auf dieselbe Semantik erheben oder notwendige Prädikate verloren gehen: C nicht freigeben|
|Mehrere Fachrollen mit offenen wissenschaftlichen Orakeln und begrenzter Parser-Reife|**A/B/C weiter parallel evaluieren**|Kein unbedingter Sieger aus 135 lokalen Klassifikationen|
|Normative Methodik/Datenschnittstelle oder reproduzierbare End-to-End-Toolverifikation soll freigegeben werden|**keiner** auf Basis dieser Arbeit|G1 BLOCKED, Ownerentscheidungen und wissenschaftliche Nachweise fehlen|

**Nächster Forschungsversuch (kein Beschluss):** zwei ausgewählte echte Standardparser-/Serializer-Slices als beidseitig prüfbare Mini-Experimente (beispielsweise ReqIF-Export für SR+Sources, LinkML/JSON-Schema-Input und ein mathspec/GEMS-Repräsentationsslice) mit exaktem Semantikdiff. Diese Auswahl ist ein **Testplan**, keine empfohlene Pflichtarchitektur.

## 3. Falsifizierbare Entscheidungsgates für spätere ADR

1. 100 % unveränderte IDs inkl. 20 process-only Daten und jeweils referenzierte Ownerblocker über **nativen** Roundtrip, nicht nur Custom JSON.
2. Mindestens ein wirksamer Standardparser pro erwogenem Standard und dokumentierter inkompatibler Fall.
3. Positiv-/Negativnachweis auf erzeugten Matrixkoeffizienten für B01/B04/B06/B07/B08/B10, insbesondere gemeinsame x-CY, KCL/KVL versus Marktlink, Stage Carry und H2.
4. Explizite E-FEAS/E-OPT/E-OBS-Projektionen samt Gegenbeispiel; Degeneracy-policy ohne Portfolio-Elementgleichheit.
5. Mutation einer Clause, eines Input-Profils und eines Operators mit ermitteltem Impact, gebrochenem Profilversions-Tupel und kontrollierter Recovery/Migrationsprozedur.
6. Unabhängige Re-Implementierungen zweier später ausgewählter Tools, keine zwingende Übersetzung von Tool A nach B.
7. Autorisierte Quell-/Daten-/KPI-Profile und V6-Evidenz unter Governance; **nicht** im Rahmen dieser Forschung vorziehen.

## 4. Nicht entschieden

Keine DSL/Serialisierung, kein Architekturpattern als ADR, kein vollständiger IoSN-LP, keine zu nutzenden native Toolprodukte, keine eingereichte produktive Schema-API, keine robusten/min-max-Anforderungen, kein in-scope Weather-Year-Selection-Modul, keine CY-Numerik oder Discount-/KPI-Defaultwerte. D1–D6 werden als Forschungsprofil respektiert; MD-01…MD-20 und CL bleiben Owner-TBD.

**Konditionale Schlussfolgerung:** Eine **kanonisch identifizierte, versionierte, evidenzgebundene Contract-Semantik** ist notwendiger als die Entscheidung für A, B oder C. Solange die demonstrierte Unterschiedsstärke nur auf Custom-Struktur und synthetischer Arithmetik beruht, ist die sachgerechte Architekturentscheidung **offen**.
