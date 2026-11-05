# MA-02 — Methodology Version Comparison
**Scope:** O26 consultation version 25.02.2026 vs. ggf. spätere *für TYNDP 2026 nachweisbar maßgebliche* ENTSO-E-IoSN-Methodik. **Comparison state: SOURCE_UNAVAILABLE_FOR_TWO-WAY_DIFF.**

## 1. Versionsgegenstände und Vergleichsfähigkeit
|Gegenstand|Version / Herkunft|Authority|Vergleichbar?|
|---|---|---|---|
|A (MA-01 Grundlage)|**O26**, 25.02.2026, 65 Druckseiten, ENTSO-E|Konsultation bestätigt|**Ja, als Source A**|
|B (spätere maßgebliche 2026-IoSN-Fassung)|**Keine verifizierte Fassung**|Nicht belegbar|**Nein**|
|C (Webinar 27.03.2026)|44 Slides, Erläuterung zu A|Nicht normsetzend|Nur Kontext, **nicht B**|
|D (2025 Scope-Consultation Summary)|6.05.2025, anderer Dokumenttyp|Finaler Scope-Report|**Nicht B**|
|E (4th CBA guideline)|Final EC-approved, andere Methodik|Verifizierte externe Autorität nur für referenzierten Teil|**Nicht B**|

**Konsequenz:** Es gibt **keinen** nachgewiesenen methodischen Content-Delta A→B. Die einzig belastbare Klassifikation sämtlicher B-bezogener Deltas ist **„weiterhin unklar“** (nicht „unverändert“). Redaktionell/erweitert/eingeschränkt/geändert/entfernt/neu sind **nicht** aus Metadaten, begleitenden Slides oder anderen Methoden ableitbar.

## 2. Themenweiser Baseline-Ausschnitt und Delta-Status
|Untersuchungsgegenstand|O26-Fundstelle|MA01-MR / MA01-SR|Delta zu freigegebenem B|
|---|---|---|---|
|Studienziele, Outputs|§§1–2, S.7–11|MR-001/046, SR-001/046|**weiterhin unklar**|
|Getrennte Horizonte, Prozess|§§3.1.2,3.2, S.14–15|MR-002/003, SR-002/003|**weiterhin unklar**|
|Investitionsziel, Nebenbedingungen, Nichtantizipativität|§3.1.1, S.12–14|MR-027–030, SR-027–030|**weiterhin unklar**|
|LP-Stufen und Kandidatenfreigabe|§3.10, S.30|MR-031–033, SR-031–033|**weiterhin unklar**|
|Strom-Wasserstoff und Freeze-Sensitivität|§§3.3,3.6, S.15/18|MR-007–009/050, SR-007–009/050|**weiterhin unklar**|
|Startnetz, Projekteligibilität|§3.4, Anh.6.2, S.16–17/52–56|MR-005/048, SR-005/048|**weiterhin unklar**; MA02-CL-001 zusätzlich|
|Clustering und 102 Zonen|§3.8.1, S.23–27|MR-013–016/022, SR-013–016/022|**weiterhin unklar**|
|Äquivalente Impedanzen, N-1/LODF, RMSE|§3.8.2–3.8.4, Anh.6.1, S.27–29/45–51|MR-017–021/023, SR-017–021/023|**weiterhin unklar**|
|LF / interner Dispatch / optionale OPF|§3.9, S.29|MR-024–026, SR-024–026|**weiterhin unklar**|
|Speicherhorizonte, Proxy und Kosten|§3.10 / §4.5.1, S.30/37|MR-033/034, SR-033/034|**weiterhin unklar**|
|Investitions-Marktlinks, NTC und Offshore|§§4.5.2–4.5.3, S.37–39|MR-035–037, SR-035–037|**weiterhin unklar**|
|Offshore-Meer-Routenfaktor|§3.11, S.30–31|MR-038, SR-038|**weiterhin unklar**, exakter Faktor selbst in A offen|
|PEMMDB/PECD/Hydro/DFT/DSR|§§4.1–4.4, S.33–36|MR-004/039–042, SR-004/039–042|**weiterhin unklar**|
|Diskontierung, WACC, Lebensdauern|§4.6, S.39–40|MR-027/043/044, SR-027/043/044|**weiterhin unklar**, beschädigter Referenzverweis in A|
|Outputs, Filter, Tool-Sanity-Check|§§2.2,3.1.2,5.1, S.9–11/14/41–44|MR-045–047, SR-045–047|**weiterhin unklar**|
|Wetterjahre als extern gelieferter Input|§3.7 S.18–20; Anh.6.3 S.57–62|MR-010/011/012/049, SR-010/011 (012/049 **excluded**)|**weiterhin unklar**; Auswahlalgorithmus ausdrücklich OUT OF SCOPE|

## 3. Eingefrorene technische Referenz aus A — keine Änderungserklärung
- Drei Studienhorizonte 2035/2040/2050, getrennte Expansionsfälle.
- Je 3 bereits ausgewählte Wetterfälle pro Studienjahr, deren IDs und Gewichte aus O26 §3.7 stammen; die **Auswahl** selbst ist upstream.
- Stromnetz mit zonaler DC-Physik; steuerbare DC-**Marktlinks** für Kandidaten selbst bei physisch AC-Technologie; exogenes H2-Netz mit gekoppelt optimiertem Dispatch.
- Erwartungswertgewichtete Betriebskosten, gemeinsamer Investitionsvektor über Wetterfälle (nicht automatisch minimax oder neue Robustheit).
- LF-Expansion, getrennter interner Dispatchvergleich, fakultative zusätzliche OPF-Expansion.
- Stufe 1 reale Übertragungskandidaten, Stufe 2 verbleibende reale/konzeptionelle/theoretische Kandidaten; Speicherexpansion nur 2040/2050.
- WACC 4 %/Transmission 25 Jahre (O26-Anwendungsrahmen); Diskontierungsblock, Offshore-Aufschlag und Speicherendkosten nicht abschließend.

**Diese Liste bedeutet „Beschreibung von A“, nicht „B ist unverändert“ und auch nicht „A ist genehmigt“.**

## 4. Source-Delta-Matrix und spätere Reconciliation
Die begleitende Datei **methodology_delta_matrix.csv** enthält 18 Themenzeilen einschließlich der Autoritätsentscheidung, Quellennachweise und MA01-ID-Links. Kein hypothetischer Änderungsdatensatz wird als real markiert.

Wenn B nachgereicht wird, sind pro Eintrag verbindlich: (1) dokumentierte Authorität + SHA-256; (2) A-Textabschnitt mit Seite; (3) B-Textabschnitt mit Seite; (4) wortlautnaher/geregelter Semantic Diff; (5) Klassifikation **unverändert, redaktionell, fachlich erweitert, fachlich eingeschränkt, geändert, entfernt, neu hinzugefügt, weiterhin unklar**; (6) betroffene MR/SR/Verifikation; (7) Owner-Entscheid und Review-Nachweis. Nicht als „unverändert“ klassifizieren, bevor A und B **beide** vorliegen und vollständig je Regel verglichen wurden.

## 5. Quellen und offene Blocker
O26: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf. P26: https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/. W26: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYDNP_2026_IoSN_Methodology_Public_Webinar.pdf. CBA4: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/news/2024/entso-e_4th_CBA_Guideline_240409.pdf. **MD-01**, **MD-02** bis **MD-20** bleiben methodische Governance-Feststellungen; zusätzlicher Klärfall **MA02-CL-001** für CBA4 §2.5.1.

**Endergebnis:** **VERSION_DELTA_NOT_EXECUTABLE / AUTHORITY_UNCONFIRMED**. Keine normative Change-Reconciliation freigegeben.