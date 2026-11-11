# M2-METHOD-G1 — Owner-Entscheidungsregister (Entscheidungsvorlage, nicht Beschluss)

**Stand:** 2026-11-11 (Europe/Berlin) · **Projekt:** AlOussama/TYNDP_Products · **Koordination:** S-GOV-M2  
**Gesamtstatus:** **DECISION_PREPARATION_ONLY / OWNER_PENDING / ENTSOE_AUTHORITY_UNCONFIRMED**. Die unten genannten Empfehlungen sind **nicht angenommen**, keine Signatur wird behauptet. Keine Implementierung, keine Runtime-/Realnetzfreigabe und kein Merge.

## 1. Quellenhierarchie und unveränderliche Referenzen

| Ebene | Dokument oder Nachweis | Tragweite |
|---|---|---|
| **E1: ENTSO-E-Primärquelle, konsultativ** | [O26: TYNDP 2026 Identification of System Needs Methodology — Version for Public Consultation, 25.02.2026](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf), insbesondere §3.8, §3.9, Anhang 6.1 | Offiziell veröffentlichter **Entwurf**, keine nachgewiesene verabschiedete/effective 2026-Methodik. Originalbyte-SHA-256 **nicht verifiziert**. |
| **E2: autorisierte Nachfolgefassung** | **NOT_VERIFIED**. Erforderlich: Original-PDF und Anhänge/Errata, Byte-SHA-256, Approval-Entscheidung mit kompetentem Approver, Datum, Geltungsbereich und Wirksamkeit. | **Kein** A/B-Delta oder endgültiger Konformitätsanspruch ableitbar. Ein negativer Suchbefund beweist nicht, dass E2 nicht existiert. |
| **E3: eigene wissenschaftliche Ableitung** | [NR-01–18-Matrix am Commit 3dc719a](https://github.com/AlOussama/TYNDP_Products/blob/3dc719a35f57bd9516bef8486bf262b75509d6b1/docs/current/IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md); [R-METH 88 am Commit 754a79e](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_INDEPENDENT_METHODOLOGY_AUTHORITY_DELTA_REVIEW_2026_11_11.md); [18/18-Trace-CSV](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_METH_REQUIREMENT_DELTA_2026_11_11.csv) | O26-gebundene Interpretation und Projekt-I-Vorschläge; **nicht** Originalsoftware/autorisiertes ENTSO-E-Regelwerk. |
| **E4: offene Governance** | [PR #22](https://github.com/AlOussama/TYNDP_Products/pull/22), [#23](https://github.com/AlOussama/TYNDP_Products/pull/23), [#24](https://github.com/AlOussama/TYNDP_Products/pull/24), [#25](https://github.com/AlOussama/TYNDP_Products/pull/25) (alle OPEN/DRAFT/UNMERGED am 11.11.), [S-GOV 93](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md) | 21/21 MD/CL ohne Ownerfreigabe, 87 Objekte ohne qualifizierte verbrauchte Originaldateien, 0/28 echte Datenvalidierungen, 48 provisorische MA01-SR und gesamtes G1 blockiert. |
| **E5: künftiger Projekt-Owner-Beschluss** | Noch **kein** M2-METHOD-G1-Owner-Beschluss nachgewiesen | Darf E3 als eingeschränktes Forschungsprofil autorisieren, **nicht** E2 ersetzen. |

**Kontrollierte Auslegung:** Im Projektbestand mit „normativ“ bezeichnete O26-Regeln gelten hier lediglich als zur Konsultationsfassung rückverfolgbare **vorläufige technische Baseline**. 0 positiv verifizierte neue Anforderungen bedeutet **nicht** 0 tatsächliche Änderungen. Eine schriftlich geplante ENTSO-E-Freigabe (SDC-Protokoll 03./04.02.2026, TOP 15.3) ist kein nachgewiesener Approval-Akt.

## 2. Entscheidungsübersicht (alle PENDING)

| ID / Referenz | Entscheidung und zuständige Instanz | Defaultempfehlung **nur Vorschlag** | Gate |
|---|---|---|---|
| **OD-M2-METH-01 / MD-01** | Autoritätsstatus; ENTSO-E Methodology Owner für E2, Projekt-Owner nur für E3-Nutzung | E2 einfordern, bis dahin O26 nur als benannte Forschungsbasis | GA-A; G1-A |
| **OD-M2-CLUSTER-02 / MD-13** | Länder-, Topologie- und Screeningvertrag; Network Clustering Owner | O26 37/102 als synthetisches Referenzprofil; dokumentierte Projekt-Heuristik | GA-C |
| **OD-M2-EQV-03 / MD-03** | x/c0-/KVL-Netzäquivalenz; Network Reduction Owner + unabhängige Numerik | Positives x, explizite Eichung, bilanziertes c0, **affine** KVL als Projekt-I | GA-E |
| **OD-M2-RMSE-04 / MD-03/13** | Metriken, Plateau und Kandidatenvergleich; Network Reduction/Verification Owners | Feste Monitoringbasis und Train/Selection/Holdout; **keine** erfundene Normschwelle | GA-R |
| **OD-M2-N1-05 / MD-03** | Kontingenzen und vier Kapazitätsorakel; TSO/Grid Security Owner | Reale N-1-Ausgabe fail-closed, isolierte synthetische Proxies markiert | GA-N |
| **OD-M2-DATA-06 / MD-11/12/18** | Daten, Zeit, Gewichte und Original-Hashes; TSO/Data/Time Owners | Zweistufig: Forschungsfixture zulassen, Realqualifikation bis Quellenfrost sperren | GA-D |
| **OD-M2-DEVICE-07 / MD-03/11** | HVDC/PST/Trafos/Ratingkonversion, Toleranzen; Device/TSO/Numerics Owners | Striktes capability/fail-closed; keine stillen Loss-/Tap-/Klassifikationsannahmen | GA-V |
| **OD-M2-LF-08 / MD-08** | LF-/Investitions- vs Dispatch-/OPF-Modus; Network Expansion Owner | Modus-Metadaten und Verträge, kein LF-/Markt-/OPF-Solver in M2 | GA-L |
| **OD-M2-API-09 / OD-M2-API** | A/B/C-Kanonik; M2 Project Owner + API Architect | **C empfohlen:** iosn_official kanonisch; B nur selektiv mit validiertem B→A-Adapter | GA-P |
| **OD-M2-I-10 / Projekt-I** | Implementierungsfreiheiten und numerische Projektkriterien; M2 Project Owner + unabhängiger Methodik-/Numerikreview | Versioniertes enges Forschungsprofil mit getrennten Testorakeln | GA-I |
| **OD-M2-SCOPE-11 / OD-M2-SCOPE** | Synthetische Arbeiten vs produktive MA2/MA3-/Real-Freigabe; M2 Project Owner | **DOCUMENT_AND_ISOLATED_FIXTURE_PREP_ONLY_NOW** | GA-S |
| **OD-M2-MERGE-12 / OD-M2-MERGE** | Branch-/Release-Grenze; Repository/Project Owner | **NO_MERGE_NOW** | GA-M |

### OD-M2-METH-01 — autorisierte Methode vs Forschung

- **Option A:** ENTSO-E Methodology Owner liefert genehmigte effective Fassung inklusive Annex/Errata oder expliziten formellen O26-Adoptionsakt; danach A/B-Klauseldiff und erst danach normative Änderungsvorlage. **Für endgültigen Konformitätsanspruch zwingend.**
- **Option B (empfohlen als Zwischenprofil):** O26 ausdrücklich **nur** als provisorische wissenschaftliche/synthetische Methodikreferenz führen; keinerlei offizielle IoSN- oder G1-Freigabe behaupten.
- **Option C (nicht zulässig):** aus Entwurfsdatum, geschlossener Konsultation, SDC-Beratungsnotiz oder eigenem Code auf verabschiedete Methodik schließen.
- **Gate-Nachweis:** Originalbytes und SHA-256 **des offiziellen Dokuments** (nicht Git-Blob), Autorisierungskette, Approval-ID, Geltungs-/Wirksamkeitsdatum, vollständige Annex-/Errata-Liste, unterschriebener Source-Owner-Bescheid; §-genauer Abgleich NR-01–18 und MA01-SR-013–026 oder autorisiertes No-Change-Attest. Bis dahin **GA-A BLOCKED**.
- **Impact:** MA1/2/3 bleiben O26-kontextualisiert; keine Rückdatierung einer normativen Änderung, keine Umbenennung von Tests in IoSN-Konformität.

### OD-M2-CLUSTER-02 — 37/102, Leitungen und Feasibility

- **A (empfohlen):** 37 separat benannte Gebietsquoten/102 Zonen **nur für die vollständige O26-Geographie** als unveränderte Forschungs-Referenz übernehmen; NI und UK getrennt; verbundene Ländercluster, aber **ein europaweit verbunden berechnetes AC-Netz**. Anwendbare 225-/400-kV-Screeningklassen mit expliziter Behandlung von 220/225 und 380/400; jährliche Überlastungsenergie in MWh und kritische Leitungen als überprüfbare Ranking-/Protection-Inputs. Deterministischer **feasibility-safe** Seed mit alternativen Merges, wenn ein Greedy-Merge blockiert.
- **B:** ausschließlich owner-gelieferte Original-Busmap, Kritikalitätsliste und verbindliche Clustering-Software/Regeln zur Realreproduktion; ohne Daten noch nicht ausführbar.
- **C (abzulehnen):** vorläufige harte Top-K-Sperren, Landes-Slacks, NI/UK-Fusion, pauschales 380→400 oder künstliche Kanten als angebliche ENTSO-E-Pflicht.
- **Gate-Nachweis:** Original-Country-Resolver je Rohbus, signierte Referenzgebiete/Quoten, AC-Connectedness und Infeasibility-Beispiele, Klassen- und Ratingsregister, Schutzpolicy samt feasible Gegenbeispielen und unabhängiger Graphprüfung. MA1-Synthetic wird nicht ohne Reparatur der PHY-/CLU-P1 zum PASS erklärt.
- **Impact:** MA1: Seed/Screening-/Country-Vertrag; MA2: zulässige gekoppelte Länder-Kandidaten; MA3: Zonenschnitte/Monitore. **GA-C: SYNTHETIC_SPEC_PROPOSED / REAL_BLOCKED**.

### OD-M2-EQV-03 — europaweite Netzäquivalenz und Maschengleichung

- **A (empfohlen als Projekt-I):** globale Ersatzreaktanzen x>0 und bilanzneutrale No-load-/Zero-balance-Korrektur c0; feste Netz-/Zonenorientierungen; Rang-/Identifizierbarkeits- und Skalenanker; verifizierte KCL sowie als **eigene konsistente Formalisierung** die affine KVL: Cᵀ diag(x) (f−c0)=0. Auf passenden neutralen HVDC-/PST-Kalibrierfällen fitten, nicht bloß Flags umschalten.
- **B:** nur x und c0=0; begründete eingeschränkte Forschungsvariante, aber **keine** automatische Äquivalenz zu O26-No-load-Flüssen.
- **C:** x/c0 und homogene KVL über den Gesamtfluss ohne konsistente Erklärung kombinieren; **unzulässig** für einen Physik-PASS.
- **Gate-Nachweis:** Detail- und Aggregatnetz, A_d/A_z, P/Γ, A_zΓ=P A_d, KCL-/Maschenresiduen, bilanzierter neutraler Dispatch, skalen-/gauge-fixiertes Identifizierbarkeitszeugnis, Solver-/Parameter-/Provenienzversion, unabhängiges Replay und akzeptierte numerische Toleranzen.
- **Impact:** MA1-Projektionsorakel, MA2 G06–G08, MA3-Export. **GA-E: MODEL_DESIGN_ONLY**, realer Fit nicht freigegeben.

### OD-M2-RMSE-04 — reproduzierbare Qualitätsakzeptanz

- **A (empfohlen):** globaler Refit für **jeden** Clustering-Kandidaten; stabile physische Referenzmonitore mit eindeutigem Mapping statt wechselnder Linkmengen; feste Stundenmengen für Training, Kandidatenselektion und ungesehenen Holdout; RMSE in MW plus expliziter dimensionsloser Nenner/Definition, saisonal/je Link und gesamt; Kapazitätsvergleich erst nach definiertem Plateau. Regressions- und Fairnessdiagnostik für Inseln, fehlende Monitore und Null-Nenner.
- **B:** owner-geliefertes exakt reproduzierbares originales RMSE-Verfahren und Schwellenwerte übernehmen, sobald authentifiziert.
- **C (abzulehnen):** Abb.-13-Farbwerte (200/350/500 MW bzw. 10/20/30 %) als ENTSO-E-PASS-Schwellen oder RMSE über ungleiche Linkmengen vergleichen.
- **Gate-Nachweis:** signiertes Monitor-/Orientierungsschema, train/select/holdout-IDs und Zeitmasken, vollständiges Normalisierungs- und Gewichtungsprotokoll, Suchbudget/Plateau-Regeln, Unsicherheits-/Sensitivitätsbericht, freigegebene Metrik- und Toleranzgrenzen, unabhängige Replay-Daten.
- **Impact:** MA2 Kandidatenentscheidung und MA3 Qualitätsübergabe. **GA-R: NO_OFFICIAL_ACCEPTANCE_THRESHOLD**.

### OD-M2-N1-05 — reale Netzsicherheit und vier Kapazitäten

- **A (empfohlen):** Sommer/Winter × beide Richtungen als **vier getrennte** Outputs je zonalem Ersatzlink, jeweils Source-/Qualitätsflag. Echte N-1-Werte erst bei originaler Ausfallliste, LODF-Gültigkeit, überwachten physikalischen Grenzzweigen, saisonalen Normal-/Notfallgrenzen, TSO-Maßnahmen/Exceptions und signierten Transferorakeln. Inselbildung/undefinierte LODF **fail-closed**. O26-Anhang-Fälle >99,5 % gerichteter Flüsse, >1 % Belastung und >99,5 % Punkte über 130 % explizit testen; diffuse Punktwolken kennzeichnen, nicht erfinden.
- **B:** getrennte **synthetische** LODF-/Regressions-Fixtures als Algorithmustest, alle Exporte PROXY_ONLY/UNQUALIFIED.
- **C (abzulehnen):** reale Kapazitätswerte allein aus synthetischem Netz/normalen Ratings oder fehlenden LODF extrapolieren und als qualified publizieren.
- **Gate-Nachweis:** outage×monitor×season-Register, signierte Grenzwerte/TSO-Ausnahmen, Topologie-/Islanding-Status, vier gerichtete Kapazitäts-Witnesses, Vertrauensintervalle/Abbruchfälle, unabhängig geprüfte N-0/N-1-Lastflüsse.
- **Impact:** MA3 G09/G10 bleibt REAL_BLOCKED. **GA-N BLOCKED_REAL_SECURITY**.

### OD-M2-DATA-06 — Primärdaten, Kalender, Quellprovenienz

- **A (empfohlen):** pro tatsächlich verwendetem Netz/Dispatch/Rating/Profillauf genau ein eingefrorenes physisches Artefakt mit Originalbyte-SHA-256, Release-ID, Lizenz, Source-Owner, URL/Access, Geographie, UTC-Stunden/Zeitschritten/DST/Leap, Basen/Einheiten, Netz-/Device-IDs, 5 bereits **extern** ausgewählten Projektjahr-IDs, Zeit-/Gewichtsmasken und vorab definierten Datenqualitätsorakeln; eigenes neutrales Kalibrierszenario als physikalisch bilanzierter Originalinput.
- **B:** öffentliches offenes Netz, Testdispatch oder synthetische Fixture als **separater Entwicklungsdatensatz**, namentlich nicht als ENTSO-E-Verbrauchsdatensatz führen.
- **C (abzulehnen):** Downloadseite/Line-Node-Dateiverweis, Git-SHA oder Schematest als Beweis einer signierten vollumfänglichen IoSN-Referenzdatenfreigabe.
- **Gate-Nachweis:** vollständiges Manifest inkl. Einzeldateien und Bytehashes, Bus-/Asset-Joins, saisonale Ratingmatrix, TSO-Netz-/Referenzflussorakel, eigener Neutralfall, Zeitzonen-/Bilanzresiduen, Sourceowner-Freigabe, unabhängiger D4-Replay. Der O26-Entwurf spricht in §3.7 von **drei repräsentativen Wetterfällen**; die **fünf fixen Projektjahre** sind ein abweichendes, extern bestimmtes Forschungsprofil, kein ENTSO-E-Methodikakt. **Keine** Wetterjahrselektion in M2.
- **Impact:** MA1/2/3 REAL_BLOCKED; M0 liefert ggf. Netz, M1 Profiloutputs nur als getrennte unveränderte Eingaben. **GA-D BLOCKED_DATA**.

### OD-M2-DEVICE-07 — Gerätetoleranzen und Nachmodellierung

- **A (empfohlen):** deklarierter Device Capability Contract mit Supported/Approximation_Approved/Reject je AC-Leitung, Trafo/Tap/Phase, PST, HVDC mit Verlust-/Richtungs-/Terminalbilanz, 3W-/Sternkonversion, 110-kV-Ties, saisonalen Ratings. Im engen synthetischen Kern ausschließlich mathematisch explizit unterstütztes lossless-DC-Profil; unbekannte oder semantisch inkompatible Daten **fail-closed**.
- **B:** konkrete verlust-/tap-/PST-behaftete Geräteerweiterung **erst** nach eigenem Sourceowner- und Physik-Replay-Gate; Toleranzen pro Einheit und Residuentyp signieren.
- **C (abzulehnen):** lossless='False' oder in_service='False' nach Python-Truthiness interpretieren, nicht-endliche/überhöhte KCL-Toleranzen zulassen, B-HVDC-Verluste nach A ohne Energiebilanz überführen, 380-kV-Screening oder Trafophase still verlieren.
- **Gate-Nachweis:** vollständiger Geräteinventar-/Abbildungsledger, Einheiten-/Basisberechnung, Bus-/PST-/Tap-Konventionen, lossless/lossy-HVDC-Bilanz und Referenzvergleich, finite relative/absolute Toleranzen auf plausibler MW-/pu-Basis mit adversarial Grenztests, unabhängige Reviewer-Replays; **keine numerische Akzeptanzgrenze wird hier fingiert**.
- **Impact:** MA1 PHY-/CLU-P1 und G11 (derzeit PARTIAL_LOSSLESS_DC_ONLY), MA2 Adapterneutralität, MA3 N-1-Trafoverhalten. **GA-V BLOCKED_REAL_DEVICE**.

### OD-M2-LF-08 — Grenze zu Netzwerkexpansion und Dispatch

- **A (empfohlen):** im M2-Export explizite Modusflags/Constraint-Gültigkeit für LF-Investitionsbaseline, spätere Dispatch-Bewertung und optionale OPF-Kappung; keine Gleichsetzung „infinite“ mit ungeprüfter physischer N-1-Kapazität.
- **B:** nachgelagertes, eigenständiges LF-/Markt-/OPF-Orakel mit gepaarten Fällen beim Network Expansion Owner.
- **C (abzulehnen):** M2 baut selbst einen LF-/OPF-/Marktoptimierer oder übernimmt aus §3.9 eine globale numerische Konvention ohne Referenzfall.
- **Gate-Nachweis:** schriftlicher §3.9-Modusvertrag einschließlich Constraint-Aktivierung, endlicher/unendlicher Limits, Vergleichs-Dispatch und Testprofil, Owner-Signoff.
- **Impact:** MA3-Output-Kontaktfläche; MA1/MA2 bleibt reine Netzreduktion. **GA-L OWNER_PENDING**.

### OD-M2-API-09 — Kanonische Software-Schnittstelle

- **A:** iosn_official sofort und ausschließlich kanonisch, ohne Wiederverwendung aus m2.
- **B:** alternative m2-API kanonisch setzen; erfordert neue Migrations- und Parity-Beweise.
- **C (empfohlen):** **iosn_official ist kanonischer Zielvertrag**; m2 nur **selektiv** hinter prüfbarem B→A-Adapter und nur für semantisch äquivalente Fähigkeiten. Kein stilles Importieren oder Konvertieren von verlustbehafteten HVDC-Schedules, UTC-Zeitachsen, Tap-/Phasenparametern, 380/400-Klassen oder abweichender Seed-Protection. R-API ist eine **Empfehlung**, kein Owner-Freeze.
- **Gate-Nachweis:** expliziter Projekt-Owner-Beschluss und signierter Input/Output-Contract v1, A/B-Source-Pins, Testvektoren/Parity je Feature, fail-closed Conversion-Matrix, MA1-P1-Re-Reviews auf integriertem SHA und API-Versionierungs-/Hashledger.
- **Impact:** MA2 kann erst nach Architektur-/MA1-Gate produktiv auf dem Kanon starten. **GA-P OWNER_PENDING**.

### OD-M2-I-10 — genaue Projekt-I-Regeln (nicht ENTSO-E-Originalcode)

- **A (empfohlen):** nur als versionierte **PROJECT_IMPLEMENTATION_CHOICES_PROPOSED**: (I-01) quoten-/konnektivitätswahrender Seed mit Backtracking/Alternativ-Merges; (I-02) x>0, Skalenanker, deterministische Gauge, c0-Zonenbilanz und affine KVL; (I-03) fixer Train/Selection/Holdout und vergleichbares Monitororakel; (I-04) Suchbudget, Plateau, coupled-country Moves mit vollständigem globalem Refit und reproduzierbaren Ties; (I-05) N-1-Proxys nur synthetisch mit expliziten NO_VALUE/UNQUALIFIED-Codes; (I-06) endliche toleranzskalierte Residuen und fail-closed Gerätepolitik.
- **B:** diese Freiheitsgrade bis zu externem Sourceowner-Algorithmus suspendieren; keine eigene numerische Forschungsimplementierung.
- **C (abzulehnen):** I-01..06 als offiziell veröffentlichte ENTSO-E-Parameter oder vollständige Reproduktion etikettieren.
- **Gate-Nachweis:** pro I-Regel Version, Motiv, Sicherheitsinvariante, Bereich, Grenzfallfixture, Parametervorgabe (mit Unit), Wertekatalog und separate M2-Owner-Unterschrift; unabhängige numerische Review- und Vergleichsmessungen, sobald Code existiert.
- **Impact:** MA1/2/3 synthetische Reproduzierbarkeit, nicht offizielle Kompatibilitäts- oder Realfreigabe. **GA-I PROJECT_OWNER_PENDING**.

### OD-M2-SCOPE-11 — separat erlaubte synthetische Tätigkeiten

- **A (empfohlen):** **jetzt** erlaubt: dokumentarische Spezifikation, Verträge, synthetische Mini-Netze, Test-/Oracle-Design, unabhängige Review-Vorbereitung, isolierte nichtproduktive Fixtures und separate Datenakquisition. Bestehende MA1-Repair-Makros nur unter ihrer eigenen Reparatur- und Review-Autorisierung. **Nicht** dadurch erlaubt: produktive MA2-Implementierung/Runtime, MA3-Release, realer ENTSO-E-Netzlauf als qualifiziert, M0/M1-Änderungen oder Wetterjahrauswahl.
- **B:** Forschungs-Code/MA2-Implementierung erst bei ausdrücklichem zusätzlichem M2-Projektgate auf integriertem MA1-Repair-SHA und angenommener kanonischer API; auch dann maximal SYNTHETIC_ONLY bis zur Realfreigabe.
- **C:** vollständiger Arbeitsstopp bis adopted/effective ENTSO-E-Methodik; konservativ, aber wissenschaftlich für eng begrenzte synthetische Vorbereitung nicht erforderlich.
- **Gate-Nachweis:** Owner-Scope-Entscheidung mit expliziten Positiv-/Negativlisten, Branch-/Run-ID, festem Datenlabel SYNTHETIC_ONLY, unabhängigen MA1-Re-Reviews und API-Freeze für B. **Aktuell noch kein Owner-GO**.
- **Impact:** keine stillschweigende Freigabe aus diesem Register. **GA-S SCOPED_SYNTHETIC_METHOD_BASELINE_PROPOSED**.

### OD-M2-MERGE-12 — Repository-/Release-Gate

- **A (empfohlen):** **NO_MERGE_NOW**. Dokumentationsbranch + Draft-PR separat zur Owner-Konsultation; PR #13, #22–25, #30 und alternative B-Linie bleiben bis zu explizitem Review/Owner-Release ungemergt.
- **B:** späterer eng begrenzter Dokumentationsmerge nach Owner-/Reviewer-Freigabe, ohne Ableitung eines MA1/MA2/Real-GO.
- **C (nicht autorisiert):** automatischer Code-/Dokument-/Methodikmerge aufgrund dieses analytischen Entscheids.
- **Gate-Nachweis:** autorisierter Repository Owner, betroffene exakte Branches/SHA und PRs, Änderungsumfang, unabhängiger Review, schriftliches ausdrückliches Merge-Statement.
- **Impact:** keinerlei Release-Statusänderung. **GA-M HOLD**.

## 3. Entscheidungsakt — verpflichtendes Aufnahmeformat

Jede tatsächlich getroffene Entscheidung muss als **neue**, getrennte Owner-Akte dokumentiert werden; dieser Entwurf ist keine Vorwegnahme. Mindestfelder: Entscheidungs-ID; **Option A/B/C oder begründeter abweichender Wortlaut**; Kompetenz-/Delegationsnachweis; Person/Organisation; Zeitpunkt; Scope/Studienlauf; Quellversion/Originalbyte-Hash; numerische Parameter mit Einheit und gültigem Bereich; betroffene NR-/SR-/MA-Gates; erlaubte/gesperrte Aktionen; unabhängige Prüfstelle; signierter Artefakt-/Commit-Link; Wirksamkeit; Revisionsweg. Ohne Nachweis **OWNER_PENDING**. Für E2 entscheidet allein die extern autorisierte Methodikinstanz, nicht der lokale Project Owner.

**Unveränderliche Quergrenzen:** 37/102 nur vollständiges O26-Referenzprofil; ein gesamteuropäisches AC-Netz; Länderreinheit nur Clustergrenze; fünf feste extern bereitgestellte Projektjahre niemals ENTSO-E als Zahl zuschreiben; M0/CGMES, M1/PECD und Wetterjahrselektion nicht verändern. Die PR22-übergreifenden 21 MD/CL bleiben durch diese M2-Priorisierung **offen**.

**Verbundene Artefakte:** [Methodenautoritätsledger](m2_method_authority_ledger.json) · [nur verifizierte NR-Änderungen](m2_nr01_nr18_delta.csv) · [Gate-Matrix](m2_gov_gate_readout.md).
