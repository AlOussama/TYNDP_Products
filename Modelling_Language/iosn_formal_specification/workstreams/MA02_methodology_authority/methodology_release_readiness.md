# MA-02 — Methodology Release Readiness
**Datum:** 05.11.2026 · **Decision:** **NO-GO FOR NORMATIVE IoSN REQUIREMENTS RELEASE** · **Reason code:** **AUTHORITY_UNCONFIRMED**.

## 1. Gate Matrix
|Gate|Abnahmeanforderung|Befund|Status|Freigabeverantwortung|
|---|---|---|---|---|
|G01|MA01-Commit und sechs Eingabedateien überprüft|SHA a86bbeb8377ac1c9a5c77d900ad287691397e506; 48 aktive SR; 50 MR|PASS|MA02 Auditor|
|G02|Offizielle konsultierte Version identifiziert|O26 25.02.2026, veröffentlicht und konsultiert|PASS|MA02 Auditor|
|G03|Finale/nachweislich maßgebliche IoSN-Version + Zustimmung/Effective Date|Kein amtlich bestätigter Entscheidungsnachweis verfügbar|**FAIL/BLOCK**|ENTSO-E Methodology Owner|
|G04|Original-Binärdatei und SHA256/Anlage-Release identifiziert|PDF via Webtext/Titelseite verifiziert, Hash nicht berechnet|OPEN|Document/Release Owner|
|G05|Nachfolgeversion inhaltlich vollständig gegen O26 verglichen|A vorhanden; B nicht verifizierbar; kein Delta behauptet|**BLOCKED_BY_G03**|Requirements Auditor|
|G06|48/48 SR in Impact-Analyse|48 eindeutige Zeilen; 0 definitive Änderungsurteile; neue Fundstelle **nicht verifiziert**|PASS – provisional analysis only|MA02 Auditor|
|G07|Methodikthemen Prozess, LP, H2, Netze, Economics, Offshore, Verifikation|Thematische Coverage in Delta-Matrix|PASS – source inventory, not comparison|MA02 Auditor|
|G08|Offene Quellendefekte geklärt|Discount, Offshore-Faktor, Storage-Kosten, KPI/Orakel offen|**FAIL/BLOCK for affected assertions**|Methodology + Domain Owners|
|G09|CBA4 §2.5.1 und IoSN 2035 Eligibilitätslogik eindeutig|Ungeklärte study-specific Anwendung (MA02-CL-001)|**BLOCK for SR-005/SR-048**|Starting Grid + Methodology Owner|
|G10|Wetterjahrauswahl aus Implementierungsscope ausgeschlossen|MR-012/MR-049 upstream only, keine aktiven SR; Inputs inkl. Gewichte|PASS|Requirements Owner|
|G11|Unveränderte MA-01-Files / separater MA-02-Branch|MA02 liefert nur neue Workstream-Dateien|PASS – vorbehaltlich Git-Prüfung nach Commit|Repo Reviewer|
|G12|Keine Implementierungs- oder formale Spezifikationskonformität behauptet|0/48 Implementationstests; MA01/VN verbleiben NOT_EXECUTED|PASS – disclosure|Verification Owner|

## 2. Release-Verdikt: Welche Nutzung ist zulässig?
- **ALLOW**: vorläufige Anforderungsanalyse, Vorbereitung von Methodology-Owner-Fragen, fachliche Traceability, gezielte Konzept- und mathematische Anforderungen **mit unmissverständlicher O26-DRAFT-Kennzeichnung**.
- **NOT ALLOWED**: normative oder regulatorische Konformitätsaussage, Freigabe der 48 SR, Behauptung „finale 2026-Methodik“, feste Offshore-/Speicher-/Discount-Parameter ohne Beleg, Freigabe der Netzreduktionsgüte ohne Referenzorakel.
- **Wetter**: bereits ausgewählte Wetterjahre einschließlich Studie/IDs/Anzahl/Gewichte/Datensätze übernehmen; kein Auswahl-/PCA-/K-Means-Audit.
- **No additional workstream**: keine Spracharchitektur, kein Metamodell, keine Software/Adapter, keine MA-03-Dateninventur, kein PoC, keine CBA-Interoperation.

## 3. Minimale Evidenz für späteren GO-Entscheid
1. **Autorität**: veröffentlichter oder formal dem Projekt autorisierter IoSN-Methodikstand mit Titel, Version, Herausgeber, kontrollierter PDF-Kopie, **SHA256**, Beschluss-/Sign-off-Verweis, Veröffentlichungs- und wirksamem Geltungsdatum, räumlicher/zeitlicher Scope (TYNDP 2026).
2. **Reconciliation**: tatsächlicher PDF/Abschnitt/Fundstellen-A→B-Diff, Klassifikation aller thematischen Änderungen und Reverse-Links auf MA01-MR-/SR, dokumentierte Ausnahmen; bei identischer Fassung **nachweisbar** identischer Content/Hash.
3. **Offene Fachentscheidungen**: mindestens MD-02/03/04/05/06/07/08/09/10/14/15 und MA02-CL-001 mit vollständigen parametrischen/gleichungsbezogenen Akzeptanzbelegen, soweit von konkreten Anforderungen benötigt.
4. **Änderungskontrolle**: eigenständiger freigegebener Change Request zur MA-01-Baseline, Impact auf L1–L4 und Versionierung; kein direkter Edit durch MA-02.
5. **Reviewer**: Requirements Owner, ENTSO-E Methodology Owner, relevante Domain Owner, unabhängiger Verifikationsreview, mit Datum und eindeutigem Freigabeumfang.

## 4. Aktueller Befund
- 48/48 **inhaltlich für kontrollierte Draft-Arbeit weiterverwendbar**, aber **0/48 endgültig methodisch freigegeben**.
- 45/48 mit bereits aus MA-01 dokumentierten spezifischen offenen Fach-/Daten-/Verifikationsentscheidungen; 3/48 ausschließlich im globalen Authority-Hold (Zählung auf Basis der zugeordneten MD-Register-IDs).
- 20 SR priorisiert P0, 25 SR P1, 3 SR P2 **zusätzlich zum globalen MD-01-Blocker**. Prioritäten sind Audit-Triage, **keine** neuen normativen Requirements.
- 18 Themenzeilen der Source-Delta-Matrix mit **„weiterhin unklar“**, weil B fehlt; **kein** bestätigter Content-Delta und **kein** verifizierter unveränderter Nachfolgestand.

**Disposition:** MA-02 als Rechercheauftrag verwertbar abschließen, **MD-01 OPEN / AUTHORITY_UNCONFIRMED**; normative Requirements-Release sperren.