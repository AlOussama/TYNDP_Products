# S-GOV — Modul 0: Konsolidierung zweier Fachrückläufer und Makroplan zur Architekturfreigabe

**Projekt:** IoSN / TYNDP / PyPSA, eigenständiges Modul 0 (CIM/CGMES ↔ kanonisches Netz ↔ PyPSA)
**Datum:** 2026-10-30
**Status:** S_GOV_M0_RETURNS_CONSOLIDATED_READY_FOR_ARCHITECTURE_SYNTHESIS
**Wichtig:** statische Fachspezifikation; keine CGMES-Import-/Exportausführung, kein numerischer Test, keine produktive Implementierung, keine ENTSO-E-Konformitätszertifizierung.
**Basis:** TYNDP_Products main 1595d6d38e77804760612621657721b3699d2fea

## 1. Verbindliche Eingangsevidenz und unveränderte Arbeiterdokumente

1. R-M0-CGMES-BACKEND-1; Commit d3ab97e170eb6eeb5064dc3058b497f5c954af58; Status CONDITIONAL_WITH_NAMED_GAPS; Datei 20_BACKEND_ASSESSMENT.md, ursprünglicher Blob 6d5ac0af95ae2efbd94bdbd791c3e008b8c4e830.
2. R-M0-CGMES-CONTRACTS-1; Commit f2705338e3d79e12a46ae44a8d7a008a81c04b3b; Status CONTRACTS_READY_FOR_ARCHITECTURE_CONSOLIDATION; Dateien 10_REQUIREMENTS.md (Blob 71c9da068e2e7c814e6ebe60cc1a4a02a19ef578), 30_CANONICAL_DATA_CONTRACT.md (Blob 17c23531786759d9841905b9427069637963922e), 50_VALIDATION_CONTRACT.md (Blob de300923e63668b48334ed3321c8c82fad019c63).
3. Die vier fachlichen Originaldateien wurden ohne inhaltliche Überarbeitung in diesen Konsolidierungsbranch übernommen. Die ursprünglichen Commits bleiben als Provenienz maßgeblich.
4. Anforderungen: REQ-001 bis REQ-048, davon 39 MUSS, sechs SOLL, drei OPTIONAL, plus REQ-X01 bis REQ-X08 als Ausschlüsse. Testspezifikation: T-01 bis T-24; Status DESIGNED_NOT_EXECUTED.

Die getrennten Arbeitsergebnisse sind als Fachinput akzeptiert. Dies ist noch **kein Architektur-Freeze**.

## 2. Gemeinsame Festlegungen — zur Übernahme in die Architektur

- Externer versionsbewusster CGMES-Parser und Serializer; eigener CIM-/RDF-/XML-Komplettnachbau ausdrücklich nicht beabsichtigt.
- Bedingter Primärkandidat PowSyBl/powsybl-core über PyPowSyBl (Datentabellen/Änderungs-API). VeraGrid ist technischer Alternativpfad mit getrenntem CGMES-Objekt- und Netzmodell.
- CIMpy/CIMgen und PyCGMES dienen als ergänzende Schema-/Objektmodelloption, nicht als gleichwertige fertige Netzkonverter; PowerGridModel-IO, SOPTIM cgmes2pgm_converter und cgmes2pgm_suite als optionale Methoden- und Validierungsreferenzen, nicht als alleinige Quelle für rückexportierbare Übertragungsnetze.
- Unveränderlicher Originaldatensatz inklusive ZIP/XML, RDF-/Modellreferenzen, Modellautoritäten, Profile, Boundary, Datenhashes und Metadaten ist Autorität für provenance-sensitive Exporte.
- Backendneutraler logischer Tabellenvertrag mit Originalgraphanker, Identitäten, Terminal-/Topologiebeziehungen, Betriebszuständen, Einheiten, Landes-/Geo-Metadaten, granularen Limits, Qualitäts- und Annahmen-Ledger.
- Separate elektrische Projektion nach PyPSA als **bewusst partielle** positive-Sequenz-Übertragungsnetzansicht; 2W/3W, PST, HVDC, Shunts, externe Injektionen, Grenzen und Vorzeichen benötigen explizite fachlich geprüfte Transformationen.
- Deklaratives Mapping (YAML für Regeln und Parameter), komplexe physikalische Transformationen ausschließlich als testbare Funktionen. Keinerlei stiller Datenverlust, Default oder Merging.
- Exportmodus UPDATE_IMPORTED (Originalmodell + erlaubte Attribut-Delta-Änderungen) strikt getrennt von CREATE_FROM_PYPSA (synthetischer Neuaufbau aus ausreichend vollständigen expliziten CIM-Konstruktionsdaten).
- Keine Wetterdaten-/PACD-Arbeit, kein Dispatch, keine Netzreduktion, keine Erweiterung von PyPSA um unsymmetrische Verteilnetz- oder Schutzmodelle.

## 3. Aufgelöste Interpretationsunterschiede und verpflichtende M2-Fixpunkte

### K-01 — Versionsabhängige Profil- und Boundary-Anforderungen

Die Backend-Bewertung listet einen umfassenden Full-Profil-Datensatz als späteres Test-Gate. Der Vertragsbericht unterscheidet korrekt zwischen tatsächlicher Importscope-Policy und Fixture-Abdeckung:
- EQ + SSH bilden den grundsätzlichen Importkern des vereinbarten unsolved-Betriebskontexts; geliefertes TP muss ausgewertet/abgeglichen werden, fehlendes TP nur nach nachweisbar zulässiger deterministischer Topologieableitung; SV ist für Referenzvergleich/solved-Capabilities erforderlich, nicht pauschal bei jedem unsolved Import.
- CGMES 2.4.15 kann EQBD/TPBD als Boundary-Lieferung benötigen.
- Für CGMES 3.0 darf TPBD **nicht** künstlich als Pflicht eingefordert werden; EQBD ist abhängig von aktueller Exchange-/Übergangspolitik. Profil-URI und versioniertes Austauschregelwerk sind maßgeblich.
- GL ist optional lieferbar, muss bei Vorhandensein korrekt gelesen und mit CRS/Quality geführt werden. Fehlen von Geo ist keine Erlaubnis zu fiktiven Koordinaten.
**M2-Aufgabe:** eine einzige Capability-/Profilmatrix je Version, Inputmodus und Exportmodus schreiben; Backend-G1 nicht als universal erforderliche Inputdateiliste interpretieren.

### K-02 — Update-Export nicht mit vollständigem CGMES-Round-trip verwechseln

PowSyBl dokumentiert den CGM-Quick-Export von SSH je IGM und SV für CGM, nicht automatisch die semantisch verlustfreie Rückserialisierung aller nicht abgebildeten RDF-Tripel/Headers/GL/Boundary-Profilinhalte. Der CONTRACTS-Updatemodus verlangt dagegen exakten Erhalt unveränderter semantischer Quellinformation.
**M2-Aufgabe:** Originalarchive dauerhaft erhalten, expliziten Allowlist-/Delta-Vertrag, Provenienz-ID-Rückabbildung, Source-Graph-/Backend-State-Lebenszyklus, Export-Witness/Graph-Diff und Blockregel definieren. Alles, was PowSyBl/Python nicht nachweislich exponiert oder garantiert, bleibt offene PoC-Gate-Voraussetzung. Nicht automatisch einen eigenen generischen CGMES-Patcher oder 1:1-Profil-Serializer erfinden.

### K-03 — Identitätsregeln, Quellenobjekte ohne mRID und Profil-Occurrences

Die source_key-Definition im CANONICAL-Dokument verwendet cgmes_profile_family; Profile (EQ/SSH/SV/TP) dürfen nicht dazu führen, dass dasselbe logische Objekt mit identischer Authority/mRID mehrfach angelegt wird. Nicht jedes RDF-/CIM-Objekt hat ein mRID-Feld (insbesondere Zustandsobjekte); seine ursprüngliche RDF-subject/URI-Identität ist daher getrennt und vollständig zu behandeln.
**M2-Aufgabe:** eindeutige source-identity/occurrence/asset/view-ID- und Namespace-Regeln, optionales mRID ohne erfundenen Ersatzwert, RDF-subject als Primär-Quellkennung bei mRID-losen Objekten, Authority-/Kollisionsbehandlung und bekannte revidierte Objektidentität festlegen.

### K-04 — Länder-Integrität versus künstliche Sternbusse

REQ-017/VALIDATION verlangen vollständige, begründete country_code-Zuordnung je **reellem, freigegebenem** AC-Bus. Das Tabellenregister führt country_code für buses formal als Pflichtfeld, während künstliche 3W-Sternbusse explizit kein fingiertes reales Land bekommen sollen.
**M2-Aufgabe:** real/synthetic bus_role und konditionale Länder-FK-Regel im Datenvertrag unmissverständlich präzisieren; Originalbusse bleiben hart geprüft, synthetische innere Busse erhalten Source-3W-Relation und eigene Darstellung ohne erfundene Länder-/Geo-Wahrheit. Grenzflüsse weiterhin über richtige Terminal-/Endport-Zuordnung.

### K-05 — Einheitliche Gates statt zweier konkurrierender Nummerierungen

Der Backendbericht benutzt ein G0–G6-Profil (Versions-/Bibliothekspins, Multi-IGM, Topologie, Spezialgeräte, Export, PyPSA, Performance). Der Datenvertrag benutzt G0–G5 (Import, Identität, Elektrotechnik, PyPSA, Export, qualifizierter SV-LF).
**M2-Aufgabe:** Namen und eindeutige Capability-ID statt Zahl als alleiniger Schlüssel; die 24 Testfälle T-01…T-24 sind kanonische Traceability. Dokumentenabnahme (ARCH) und zukünftige Ausführungsevidenz (QUAL) sind getrennt. Leistung/Speicher aus Backend-G6 bleiben eigenes QUAL-PERFORMANCE-Gate. ENTSO-E-Zertifizierung darf niemals aus internen PASS-Gates abgeleitet werden.

### K-06 — Modul-0-Netzfreigabe ist nicht Modul-1-Adapterfreigabe

Der bestehende src/tyndp_reduce/pypsa_adapter.py ist laut CONTRACTS-Bericht ein enger, eininseliges und leitungsbasiertes Modell annehmender DC-Adapter. Transformer, PST, HVDC, Storage und weitere Sonderfälle sind momentan keine belegte End-to-End-Funktion des Netzreduktionsprototyps.
**M2-Aufgabe:** DetailedNetworkReference v1 als stabile Schnittstelle aus Modul 0 spezifizieren. REDUCTION_ADAPTER_READY separat ausweisen; keinerlei automatische Übergabe mit Drop/Proxy ohne fachliche Qualifikation. Anpassung des Folgeadapters ist eigenes späteres Implementierungsmakro, nicht Teil dieser statischen Architekturstufe.

### K-07 — Qualifizierung und Einschränkung von Sondergeräten

2W/3W-PIs, Tap-Seiten/PST-Winkel, HVDC-Portzeichen und Verluste, CurrentLimits und temporäre Grenzwerte sind nicht aus schlichter Attributgleichheit ableitbar. Insbesondere kann ein reversibler verlustbehafteter PyPSA-Link die Rückwärtsflussverluste falsch abbilden.
**M2-Aufgabe:** pro Capability eine explizite EXACT/APPROX/UNSUPPORTED-Matrix samt zulässigem Downscope und Loss-/Quality-Report; keine fiktive physikalische Gleichheit.

## 4. Nächste Ausführungsmakros und Artefakte

### M2 — S-GOV integrierte Softwarearchitektur / ADR; **jetzt, dokumentarisch, in diesem Chat**

**Eingang:** vier übernommene Fachberichte plus dieser K-01–K-07-Entscheidungsrahmen. Ohne weitere allgemeine Recherche oder zusätzliche Peerworker.

**Einmalig zu liefern:**
- 40_SOFTWARE_ARCHITECTURE.md: Modulgrenzen/Abhängigkeiten; Backend-Port/Adapter-Vertrag; Import-/Reimport-/Update-/Export-Sequenz; Datenartefakte, Relationen, Persistenz-/Transaktionslebenszyklus; schemaorientierte Mapping-Regeln; Protokoll für Runtime-Backendwechsel; fachliche Capability-Matrix.
- 60_ARCHITECTURE_DECISION.md: bedingte Wahl von PowSyBl/PyPowSyBl, VeraGrid als Alternative, begründete Nichtwahl anderer Backends, Unbekannte, Sicherheits-/Lizenz-/Betriebsrisiken, M0↔M1-Grenze und Exportmodus-Entscheidung.
- 70_IMPLEMENTATION_READINESS.md: konkrete Module/Aufwandsklassen, Akzeptanz- und Testmatrix REQ→T→Capability, Fixtures, getrennte PoC-Gates/Verantwortung und exakte PoC-Startvoraussetzungen.

**M2-Gate:** ARCHITECTURE_DESIGNED_READY_FOR_INDEPENDENT_STATIC_REVIEW oder CONDITIONAL_WITH_NAMED_DESIGN_GAPS. Jede MUSS-Anforderung erhält Modulverantwortung und geplanten Prüfnachweis. Keine Programmausführung, kein Python-Code, keine neuen Solver-Ergebnisse.

### M3 — Ein unabhängiger konsolidierter Architektur-Review; **nach M2**, separat im neuen Fachchat

**Einziger Reviewauftrag**, kein paralleles Sammeln von Mikroberichten: vollständige statische Bewertung von 10/20/30/40/50/60/70 und diesem Governance-Bericht; überprüfe K-01–K-07, 39 MUSS und 24 T, Backend/API-Annahmen, source-key, FK-Bedingungen, Export, Modell-1-Grenze; prüfe exakte Branch-/Commitinhalte. Liefere einen Bericht 80_INDEPENDENT_ARCHITECTURE_REVIEW.md mit P0/P1/P2-Findings und PASS/CONDITIONAL/REPAIRS_REQUIRED. Keine Codeänderungen/Tests. Höchstens eine konsolidierte fachliche Korrekturrunde für nachgewiesene P0/P1-Befunde.

### M4 — Ein gebündelter Python-/CGMES-PoC- und Validierungsmakro; **erst bei neuer ausdrücklicher Umsetzungsfreigabe**

Qualifiziere gepinnte Backend-Versionen und zulässig verfügbare 2.4.15/3.0-Fixtures, dieselbe kanonische Schema-API, Basisgeräte und Sonderfälle, die benannten T-01–T-24 sowie SSH-/SV-Update-Export als eigene Testcapability. Eigene Erzeugung (CREATE_FROM_PYPSA) und vollständiger Full-Profile-Round-Trip nur nach expliziter getrennter Freigabe. Realnetz-/Multi-IGM-Skalierung und Modul-1-Integration erhalten separate Gates. Nachweisstatus pro Fixture/Version/Capability, keine pauschalen Erfolgsclaims. Dies ist hier **nur geplant, nicht autorisiert oder ausgeführt**.

## 5. Governance-Regeln und kritischer Pfad

- Kritischer Pfad: M2 (in diesem Chat) → M3 (genau ein neuer Reviewerchat) → Entscheidung über dokumentarischen Architektur-Freeze. M4 folgt nur bei ausdrücklich genehmigter Implementierung.
- Kein dritter paralleler Architekturworker: Die unabhängigen Ausgangsanalysen sind abgeschlossen. Zusatzchats nur für einen klar nachgewiesenen, architekturrelevanten Blocker und dann als ein konsolidierter Auftrag.
- Die Originalberichte werden weder überschrieben noch rückwirkend auf PASS umetikettiert. Neue Architekturentscheidungen dokumentieren ausdrücklich ihre Geltung gegenüber Quellberichten.
- Alle Makroberichte auf getrennten Branches mit exakten Commit-SHAs. Kein Merge nach main ohne Freigabe. Keine Änderung an produktiven src-/tests-Dateien in M2/M3.
- Architektur-Freeze ≠ Importkonformität ≠ exportierbare verlustfreie vollständige CGMES-Lieferung ≠ REDUCTION_ADAPTER_READY.

## 6. Vorläufige Disposition für S-GOV

**CONSOLIDATED_FOR_M2_ARCHITECTURE_SYNTHESIS.** Der fachliche Grundansatz ist konsistent; K-01 bis K-07 sind innerhalb eines großen M2-Architekturmakros aufzulösen, nicht durch sieben kleine Folgechats. Die erste reale ausführbare Freigabe wird später getrennt von einer bloßen Architektur-Freigabe entschieden.
