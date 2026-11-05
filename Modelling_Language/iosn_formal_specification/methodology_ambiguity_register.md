# MA-01 — Methodology Ambiguity & Decision Register

**Version 0.1.0, 2026-11-05 | alle Entscheidungen OPEN.** Methodikquelle: ENTSO-E TYNDP 2026 IoSN **Version for Public Consultation**, 25.02.2026. Keine Freigabe der endgültigen Fassung bestätigt. Die Rollen sind vorgeschlagene methodische Owner, keine bereits benannten Entscheidungsträger.

P0 = entscheidend für finale Quellen-/Gleichungs-/Output-Gültigkeit; P1 = blockiert betroffene methodische Teilkonformität; P2 = erforderliche Input- oder Interpretationsklärung. Jede Entscheidung benötigt Datum, zuständige Autorität, signiertes Quellen-/Formelartefakt, geänderte MA01-MR/SR-IDs, Nachweisgrenzen und Status.

## Priorisierte Entscheidungsmatrix

|ID|Priorität|Problem|Quelle|Erforderlicher fachlicher Entscheid|Verknüpfte SR|Status|
|---|---|---|---|---|---|---|
|MD-01|P0|Eine aktuelle genehmigte Fassung ist nicht bestätigt.|O26 O26 Titel und Konsultationsstatus|Gültige finale Fassung, Datum, Autorität und kontrollierte Revision bestätigen.|alle 48 SR|OPEN|
|MD-02|P0|Beschädigter interner Bezug des Diskontierungsblocks.|O26 §4.6 S.40|Gültige Diskontierungsformel, Zeitblock, Bezugsjahr und Referenzwerte.|SR-027, SR-043, SR-044|OPEN|
|MD-03|P0|Elektrische Äquivalenz, RMSE, LODF/N-1 und Grenzfälle ohne vollständig freigegebenes Testorakel.|O26 §3.8 / Anhang 6.1|Detail-/Aggregatnetz-Referenz, Kapazitäten, Schwellwerte und Ausnahmen.|SR-013–023|OPEN|
|MD-04|P0|KPI-Formeln, Filter und Aggregationsregeln sind nicht vollständig geschlossen.|O26 §2.2, §§3.1.2/3.10|KPI-Katalog mit Bezugsgröße, Einheiten, Berechnung, Aggregation, Sollbeispiel.|SR-001,045,046|OPEN|
|MD-05|P1|Uniformer 10–15%-Faktor, exakter Endwert fehlt.|O26 §3.11 S.30–31|Endwert, Anwendbarkeit, Geometriedefinition, Kostenformel.|SR-038|OPEN|
|MD-06|P1|Dauerklassen beschrieben, definitive Kosten im Konsultationsentwurf offen.|O26 §4.5.1 S.37|Finale Klassen, Kosten, Ländergrenzen, Lebensdauern und Anwendungsregeln.|SR-033–034|OPEN|
|MD-07|P1|Feinheiten der Stage-1-Übernahme in Stage 2, verbleibende Kandidaten und Stufe 3 nicht vollständig testbar.|O26 §§3.1.1/3.10|Stage-Transition inklusive Teil-/Restkandidaten, Beispiele und Formeln.|SR-003,031,032,033|OPEN|
|MD-08|P1|Primäres LF, internes Dispatch und optionale OPF-Kappung müssen exakt voneinander getrennt werden.|O26 §3.9|Grenzwerte LF, optionale OPF-Kappungsregel und verbindliche Dispatch-Vergleiche.|SR-024,025,026|OPEN|
|MD-09|P1|Kandidatenmodell ist ein steuerbarer DC-Marktlink trotz physischer AC-Technologie; Richtungsmapping uneindeutig.|O26 §4.5.2 S.37–38|NTC+/NTC−, Steuerbarkeits- und Kostenmapping, Testmodell.|SR-035,036|OPEN|
|MD-10|P1|Exogene H2-Topologie, gekoppelte Bilanz sowie eingefrorene stündliche Elektrolyselast bedürfen exaktem Profil.|O26 §§3.3/3.6|Umwandlungs-/Dispatchrestriktionen und Freeze-Referenztest.|SR-007–009,050|OPEN|
|MD-11|P1|PEMMDB/PECD/DFT/H2/Startnetzprojekte ohne vollständige kontrollierte Release- und Hashliste.|O26 §§3.4–3.5,4.1–4.4 / Anh.6.2|Datenversionen, Kennungen, Zeitschemata, Checksummen, Lizenz/Verfügbarkeit.|SR-004–006,011,039–040,048|OPEN|
|MD-12|P1|Kalender, Stunde, DST/Leap, Reihenlücken, numerische Input-Toleranzen offen.|O26 §§3.7/4.2/4.4|Versioniertes Studienzeit-/Zeitzonenprofil, Lückenregeln und zulässige Toleranzen.|SR-010,011,040,042|OPEN|
|MD-13|P1|Clustering-Heuristik, kritische Leitungen und Qualitäts-Sonderfälle nicht vollständig eindeutig.|O26 §3.8 / Anh.6.1|Referenzcluster, Netztopologie, kritische Leitungen und zulässige Freiheitsgrade.|SR-014–016,022|OPEN|
|MD-14|P1|Projekteligibilität gemäß referenziertem CBA-Dokument und finale Offshore-Ziele quellengebunden.|O26 §§3.4–3.5 / Anh.6.2|Signierte Projektliste, Eligibility-Crosswalk, RES-Zielwerttabelle.|SR-005,006,048|OPEN|
|MD-15|P1|Zulässige Zielfunktions-, Feasibility-, Dual-/Gap-Grenzen nicht festgelegt.|O26 §3.1.1, §5.1|Numerische Testorakel, Degeneracy-Regeln, Solverstatus, Fehlerschwellen.|SR-017,018,027–030|OPEN|
|MD-16|P2|Fünf Wasserkraftklassen und Markt-DSR vs implizite Flexibilität brauchen überprüfbare Grenzfälle.|O26 §§4.3–4.4|Klassenparameter, Stundendaten, Constraints, Ausnahmefälle.|SR-041,042|OPEN|
|MD-17|P1|Zwei optimale Lösungen müssen nicht dieselben Kandidaten umfassen.|O26 §§2.2/3.1.2|Orakel für wirtschaftliche/physikalische Äquivalenz statt blindem Tabellenvergleich.|SR-001,025,046|OPEN|
|MD-18|P2|Liefervertrag für ausgewählte ID/Anzahl/Gewicht, Studienjahr, Wetterreihe, Provenienz unbestätigt.|O26 §3.7|Vollständigen Übergabedatensatz definieren; keine Auswahlalgorithmusprüfung.|SR-010,011,040|OPEN|
|MD-19|P2|Mögliche Abweichungen der Quell-Fenster liegen im vorgelagerten Auswahlprozess.|O26 §3.7 vs Anhang 6.3|Nur IoSN-Inputabweichungen zur Zeitachse melden; kein PCA/K-Means-Review.|SR-010,011 (Datenvalidierung)|OPEN|
|MD-20|P1|Alte Auswahl-SR-005, UC-01 und PCA-Roadmap dürfen nicht aktiv bleiben.|O26 PR #16 frühere SR/UC/Gate-Dokumente|Altberichte archivieren/kennzeichnen, neue MA01-IDs als alleinige aktive Draft-Baseline.|MA01-MR-012/049; SR-010/011|OPEN|

## Detailverantwortung

### MD-01: Genehmigung/aktuell geltende Methodik

**Quelle:** O26 O26 Titel und Konsultationsstatus. **Owner (vorzuschlagen):** ENTSO-E Methodology Owner. **Unklarheit:** Eine aktuelle genehmigte Fassung ist nicht bestätigt. **Benötigter Entscheidungsnachweis:** Gültige finale Fassung, Datum, Autorität und kontrollierte Revision bestätigen. **Betroffene Anforderungen:** alle 48 SR. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-02: Wirtschaftliche Diskontierung

**Quelle:** O26 §4.6 S.40. **Owner (vorzuschlagen):** Economics Owner. **Unklarheit:** Beschädigter interner Bezug des Diskontierungsblocks. **Benötigter Entscheidungsnachweis:** Gültige Diskontierungsformel, Zeitblock, Bezugsjahr und Referenzwerte. **Betroffene Anforderungen:** SR-027, SR-043, SR-044. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-03: Validierung Netzaggregation

**Quelle:** O26 §3.8 / Anhang 6.1. **Owner (vorzuschlagen):** Network Reduction Owner. **Unklarheit:** Elektrische Äquivalenz, RMSE, LODF/N-1 und Grenzfälle ohne vollständig freigegebenes Testorakel. **Benötigter Entscheidungsnachweis:** Detail-/Aggregatnetz-Referenz, Kapazitäten, Schwellwerte und Ausnahmen. **Betroffene Anforderungen:** SR-013–023. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-04: Systembedarfsoutputs und KPIs

**Quelle:** O26 §2.2, §§3.1.2/3.10. **Owner (vorzuschlagen):** Reporting Owner. **Unklarheit:** KPI-Formeln, Filter und Aggregationsregeln sind nicht vollständig geschlossen. **Benötigter Entscheidungsnachweis:** KPI-Katalog mit Bezugsgröße, Einheiten, Berechnung, Aggregation, Sollbeispiel. **Betroffene Anforderungen:** SR-001,045,046. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-05: Routenfaktor Offshore

**Quelle:** O26 §3.11 S.30–31. **Owner (vorzuschlagen):** Offshore Owner. **Unklarheit:** Uniformer 10–15%-Faktor, exakter Endwert fehlt. **Benötigter Entscheidungsnachweis:** Endwert, Anwendbarkeit, Geometriedefinition, Kostenformel. **Betroffene Anforderungen:** SR-038. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-06: Speicherproxy und Kosten

**Quelle:** O26 §4.5.1 S.37. **Owner (vorzuschlagen):** Storage Owner. **Unklarheit:** Dauerklassen beschrieben, definitive Kosten im Konsultationsentwurf offen. **Benötigter Entscheidungsnachweis:** Finale Klassen, Kosten, Ländergrenzen, Lebensdauern und Anwendungsregeln. **Betroffene Anforderungen:** SR-033–034. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-07: LP-Stufenwechsel und Teilinvestition

**Quelle:** O26 §§3.1.1/3.10. **Owner (vorzuschlagen):** Expansion Owner. **Unklarheit:** Feinheiten der Stage-1-Übernahme in Stage 2, verbleibende Kandidaten und Stufe 3 nicht vollständig testbar. **Benötigter Entscheidungsnachweis:** Stage-Transition inklusive Teil-/Restkandidaten, Beispiele und Formeln. **Betroffene Anforderungen:** SR-003,031,032,033. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-08: LF- vs OPF-Portfolio

**Quelle:** O26 §3.9. **Owner (vorzuschlagen):** Network Expansion Owner. **Unklarheit:** Primäres LF, internes Dispatch und optionale OPF-Kappung müssen exakt voneinander getrennt werden. **Benötigter Entscheidungsnachweis:** Grenzwerte LF, optionale OPF-Kappungsregel und verbindliche Dispatch-Vergleiche. **Betroffene Anforderungen:** SR-024,025,026. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-09: Marktlinks und NTC-Richtungszuordnung

**Quelle:** O26 §4.5.2 S.37–38. **Owner (vorzuschlagen):** Market Model Owner. **Unklarheit:** Kandidatenmodell ist ein steuerbarer DC-Marktlink trotz physischer AC-Technologie; Richtungsmapping uneindeutig. **Benötigter Entscheidungsnachweis:** NTC+/NTC−, Steuerbarkeits- und Kostenmapping, Testmodell. **Betroffene Anforderungen:** SR-035,036. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-10: H2-Gleichungen und Freeze-Sensitivität

**Quelle:** O26 §§3.3/3.6. **Owner (vorzuschlagen):** Hydrogen Owner. **Unklarheit:** Exogene H2-Topologie, gekoppelte Bilanz sowie eingefrorene stündliche Elektrolyselast bedürfen exaktem Profil. **Benötigter Entscheidungsnachweis:** Umwandlungs-/Dispatchrestriktionen und Freeze-Referenztest. **Betroffene Anforderungen:** SR-007–009,050. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-11: Datenversionen und Herkunft

**Quelle:** O26 §§3.4–3.5,4.1–4.4 / Anh.6.2. **Owner (vorzuschlagen):** Data Owner. **Unklarheit:** PEMMDB/PECD/DFT/H2/Startnetzprojekte ohne vollständige kontrollierte Release- und Hashliste. **Benötigter Entscheidungsnachweis:** Datenversionen, Kennungen, Zeitschemata, Checksummen, Lizenz/Verfügbarkeit. **Betroffene Anforderungen:** SR-004–006,011,039–040,048. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-12: Zeitachse und Gewichtstoleranzen

**Quelle:** O26 §§3.7/4.2/4.4. **Owner (vorzuschlagen):** Timeseries Owner. **Unklarheit:** Kalender, Stunde, DST/Leap, Reihenlücken, numerische Input-Toleranzen offen. **Benötigter Entscheidungsnachweis:** Versioniertes Studienzeit-/Zeitzonenprofil, Lückenregeln und zulässige Toleranzen. **Betroffene Anforderungen:** SR-010,011,040,042. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-13: Netzcluster-Kriterien

**Quelle:** O26 §3.8 / Anh.6.1. **Owner (vorzuschlagen):** Network Reduction Owner. **Unklarheit:** Clustering-Heuristik, kritische Leitungen und Qualitäts-Sonderfälle nicht vollständig eindeutig. **Benötigter Entscheidungsnachweis:** Referenzcluster, Netztopologie, kritische Leitungen und zulässige Freiheitsgrade. **Betroffene Anforderungen:** SR-014–016,022. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-14: Anrechenbare Projekte und Offshore-Ziele

**Quelle:** O26 §§3.4–3.5 / Anh.6.2. **Owner (vorzuschlagen):** Starting Grid Owner. **Unklarheit:** Projekteligibilität gemäß referenziertem CBA-Dokument und finale Offshore-Ziele quellengebunden. **Benötigter Entscheidungsnachweis:** Signierte Projektliste, Eligibility-Crosswalk, RES-Zielwerttabelle. **Betroffene Anforderungen:** SR-005,006,048. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-15: Solverakzeptanz/Modellresiduen

**Quelle:** O26 §3.1.1, §5.1. **Owner (vorzuschlagen):** Verification Owner. **Unklarheit:** Zulässige Zielfunktions-, Feasibility-, Dual-/Gap-Grenzen nicht festgelegt. **Benötigter Entscheidungsnachweis:** Numerische Testorakel, Degeneracy-Regeln, Solverstatus, Fehlerschwellen. **Betroffene Anforderungen:** SR-017,018,027–030. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-16: Hydro/DSR-Detailregeln

**Quelle:** O26 §§4.3–4.4. **Owner (vorzuschlagen):** Hydro/DFT Owner. **Unklarheit:** Fünf Wasserkraftklassen und Markt-DSR vs implizite Flexibilität brauchen überprüfbare Grenzfälle. **Benötigter Entscheidungsnachweis:** Klassenparameter, Stundendaten, Constraints, Ausnahmefälle. **Betroffene Anforderungen:** SR-041,042. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-17: Mehrfachoptima und Portfoliogleichwertigkeit

**Quelle:** O26 §§2.2/3.1.2. **Owner (vorzuschlagen):** Results Owner. **Unklarheit:** Zwei optimale Lösungen müssen nicht dieselben Kandidaten umfassen. **Benötigter Entscheidungsnachweis:** Orakel für wirtschaftliche/physikalische Äquivalenz statt blindem Tabellenvergleich. **Betroffene Anforderungen:** SR-001,025,046. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-18: Externes Wettermanifest

**Quelle:** O26 §3.7. **Owner (vorzuschlagen):** Weather Data Owner. **Unklarheit:** Liefervertrag für ausgewählte ID/Anzahl/Gewicht, Studienjahr, Wetterreihe, Provenienz unbestätigt. **Benötigter Entscheidungsnachweis:** Vollständigen Übergabedatensatz definieren; keine Auswahlalgorithmusprüfung. **Betroffene Anforderungen:** SR-010,011,040. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-19: Wetterdatenquelle widersprüchliche Zeitraumangaben

**Quelle:** O26 §3.7 vs Anhang 6.3. **Owner (vorzuschlagen):** Upstream Weather Owner. **Unklarheit:** Mögliche Abweichungen der Quell-Fenster liegen im vorgelagerten Auswahlprozess. **Benötigter Entscheidungsnachweis:** Nur IoSN-Inputabweichungen zur Zeitachse melden; kein PCA/K-Means-Review. **Betroffene Anforderungen:** SR-010,011 (Datenvalidierung). **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

### MD-20: Legacy-Scope-Konflikt

**Quelle:** O26 PR #16 frühere SR/UC/Gate-Dokumente. **Owner (vorzuschlagen):** MA-01 Governance Owner. **Unklarheit:** Alte Auswahl-SR-005, UC-01 und PCA-Roadmap dürfen nicht aktiv bleiben. **Benötigter Entscheidungsnachweis:** Altberichte archivieren/kennzeichnen, neue MA01-IDs als alleinige aktive Draft-Baseline. **Betroffene Anforderungen:** MA01-MR-012/049; SR-010/011. **Status:** OPEN, keine verbindliche Freigabe und kein vorhandenes vollständiges Akzeptanzorakel.

## Freigaberegel

Eine ungeklärte Anforderung erhält **BLOCKED** bei abschließender Konformitätsprüfung. Wo eine Teilprüfung möglich ist (z.B. Form und Konsistenz eines **bereits ausgewählten** Wettermanifests), darf sie als Teilnachweis durchgeführt werden; daraus folgt **keine** Prüfung der Auswahlentscheidung oder vollständige IoSN-Verifikation. Die Originalmethodik darf nicht durch solver- oder toolseitige Defaults ergänzt werden.
