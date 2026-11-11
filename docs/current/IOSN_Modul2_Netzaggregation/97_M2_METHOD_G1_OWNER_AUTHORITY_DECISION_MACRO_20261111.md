# M2-METHOD-G1 — Methodology Authority & Owner Decision Package

**Projekt:** AlOussama/TYNDP_Products. **Rolle:** S-GOV-M2 + wissenschaftlicher Methodikkoordinator; Read-only-Entscheidungsvorbereitung, **nicht** neue Komplettrecherche oder stillschweigende Normfestlegung. **Jetzt startbar.**

## 1. Verbindliche Quellen

- [R-M2-METH vollständiger Delta-Review](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_INDEPENDENT_METHODOLOGY_AUTHORITY_DELTA_REVIEW_2026_11_11.md)
- [PR #30 – R-METH](https://github.com/AlOussama/TYNDP_Products/pull/30)
- [18 NR-01–18 Methodikmatrix](https://github.com/AlOussama/TYNDP_Products/blob/3dc719a35f57bd9516bef8486bf262b75509d6b1/docs/current/IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md)
- [ENTSO-E O26 — Public Consultation 25.02.2026](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf)
- [Übergreifende Methodengates PR #22](https://github.com/AlOussama/TYNDP_Products/pull/22), [#23](https://github.com/AlOussama/TYNDP_Products/pull/23), [#24](https://github.com/AlOussama/TYNDP_Products/pull/24), [#25](https://github.com/AlOussama/TYNDP_Products/pull/25)
- [S-GOV Konsolidierung 93](93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md).

## 2. Auftrag

Erzeuge aus den bereits belegten Findings ein **kurzes, vollständiges** Owner-Entscheidungspaket für M2. Die ENTSO-E O26-Konsultationsfassung ist öffentlich vorhanden; eine adopted/effective Nachfolgeversion und deren originale Bytes/Approval wurden am 11.11. **nicht** positiv verifiziert. Behandle `AUTHORITY_UNCONFIRMED` als echte Grenze. Keine behauptete Quellenänderung ohne beide autoritativen Versionen und dokumentierten Diff. Bestehende NR-01–18 technischen Anforderungen für **provisorische wissenschaftliche/synthetische** Entwicklung unverändert halten, solange kein belegter Delta vorliegt.

Für jeden tatsächlich offenen Owner-/Source-Punkt dokumentiere: Entscheider, Optionen, Defaultempfehlung (nicht bestätigt!), benötigter Beleg, Auswirkung auf MA1/MA2/MA3 und stop/go:
- **MD-01:** tatsächlich adopted/effective ENTSO-E IoSN-Version, Approval/Effektivdatum, Original-PDF SHA-256; keine Ersatzentscheidung durch internen Code.
- **MD-03:** qualifizierte Referenzmodelle, x/c0/Gauge/Affine-KVL, RMSE-Normalisierung und Topologie-Monitororakel; echte N-1-/LODF- und vier Kapazitätsorakel.
- **MD-13:** 37-Gebiets-102-Zonen Quotenlandkarte, Country-Resolver, Screening-, kritische-Line-Protection, Greedy-Zulässigkeit als Projekt-I und Re-Clustering-Ziele.
- **MD-11/12:** TSO-Quellen, Netz-/Dispatch-/Rating-/Zeit-/Einheiten-/Hash-/Neutralfall-Manifeste; fünf externe Jahre nur als fixe Inputs.
- **MD-08:** LF-Investitions- vs spätere Dispatch-/OPF-Modusgrenzen, kein LF-/Marktsolver-Import in M2.
- **OD-M2-API:** A/B/C aus unabhängigem R-API; C empfohlene Option mit A-Kanonik/optional B→A.
- **OD-M2-SCOPE:** Scope der synthetischen Weiterentwicklung vs. endgültige Methodik- und Realfreigabe; keine neue implizite M0/M1-Abhängigkeit.
- **OD-M2-MERGE:** `NO_MERGE_NOW`, falls keine ausdrückliche weitergehende Ownerfreigabe.

Definiere die minimalen transparenten Projekt-I-Entscheidungen (feasibility-safe Seed, Positive x und Skalenanker, c0/affine KVL, fixe Train/Select/Holdout-Fenster, vergleichbare Monitorgruppe, Suchbudget/Plateau, N-1-Proxystatus) als **Projektvorschläge**, nicht ENTSO-E-Originalcode.

## 3. Output und Gate

Liefere `m2_owner_decision_register.md`, `m2_method_authority_ledger.json`, `m2_nr01_nr18_delta.csv` (nur tatsächliche Änderungen), `m2_gov_gate_readout.md`. Neue Belege nur mit Quellversion, Fingerprint und Approver. Interne Eigenfreigabe ist keine offizielle externe Approval. Auf dediziertem Dokumentationsbranch veröffentlichen.

**Zulässiger Status:** `SCOPED_SYNTHETIC_METHOD_BASELINE_PROPOSED`; oder `OWNER_SCOPED_APPROVED` nur nach einer wirklichen Ownerentscheidung. `ENTSOE_AUTHORITY_UNCONFIRMED` bleibt bis positivem Nachweis. Keine Implementierung, kein Merge, keine echte Runtime-/Realnetzfreigabe.
