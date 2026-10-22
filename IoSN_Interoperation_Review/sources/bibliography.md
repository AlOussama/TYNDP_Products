# Quellenregister — IoSN Architektur & Interoperation

**Abruf-/Prüfstichtag: 23.10.2026.** Jede URL weist auf die Quelle selbst; methodische **Konsultationsentwürfe** sind von anerkannten/finalen Vorgaben sowie wissenschaftlichen Rekonstruktionen klar getrennt.

## Primärquellen (Methodik/Planungsprozess)

| ID | Primärquelle / URL | geprüfte Fassung | belegte, begrenzte Aussagen |
|---|---|---|---|
| **S01** | [ENTSO-E: TYNDP 2026 Identification of System Needs Methodology (65 S., PDF)](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf) | **Version for Public Consultation 25.02.2026, NICHT finale Methode**, ``3.1, 3.6–3.10, `5.1, Annex 6.1/6.3, PDF-Seiten 12–14, 18–30, 41–44, 45–62 | stochastischer gewichteter Ausbau mit gemeinsamem `x`, Zieljahre, Wetterauswahl, Netzreduktion, LF/OPF, PLEXOS/Antares-Sanity und begrenzte Evidenz |
| **S02** | [ENTSO-E: öffentliche Konsultation TYNDP 2026 IoSN](https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/) und [Mitteilung vom 26.02.2026](https://www.entsoe.eu/news/2026/02/26/entso-e-releases-public-consultation-on-the-system-needs-methodology/) | Konsultation 26.02.–03.04.2026 | Versions-/Stakeholderstatus; eine spätere finale Version ist **im Review nicht belegt** |
| **S03** | [ENTSO-E/ENTSOG TYNDP 2026 Scenarios Package / Methodology Report](https://2026.entsos-tyndp-scenarios.eu/download/) | Juni 2026, **Draft** Scenario Report und Methodology Package | Quelle für übergeordneten Szenariorahmen; Detaildaten nicht umfassend neu berechnet |
| **S04** | [ENTSO-E TYNDP 2024 Publikation und System Needs Study](https://www.entsoe.eu/outlooks/tyndp/2024/) | 2024er Veröffentlichungen auf offizieller Website | historische Systembedarfs- vs individuelle Projekt-CBA-Differenz, keine automatisierte 2026er Methodenumsetzung |

## Evidenz aus dem Stammrepository — ausdrücklich sekundäre Forschungsrekonstruktion

**Git-Stand für R01–R08:** `1595d6d38e77804760612621657721b3699d2fea` (Commit 19.10.2026). Verlinkt sind **dieselben Dateien auf genau diesem Commit**, nicht bewegliches `main`.

| ID | Datei, SHA (Git blob) | Vertrauensgrenze |
|---|---|---|
| **R01** | [README.md](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/README.md), Blob `8eb4a16b92d63ef9513b7f664d799055d61dc8ec` | offizielle Selbstbeschreibung: Forschungsprototyp/synthetisch |
| **R02** | [docs/REPOSITORY_AUDIT.md](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/docs/REPOSITORY_AUDIT.md), Blob `1b091e156f0df5d65c15580cc847b43fc09f2e9b` | offene Real-PyPSA-E2E-, Norm-/Topologie-/Sicherheitsfragen |
| **R03** | [Band I, Wissenschaftliche Methodik](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/docs/current/IOSN_2026_Band_I_Wissenschaftliche_Methodik.md), Blob `7b4ae2e480ce9aacf8b12d8ab5b45e754028f313` | Rekonstruktionen [D]/[R]/[E], getrennt von ENTSO-E-Norm |
| **R04** | [Band II, PyPSA-Architektur](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/docs/current/IOSN_2026_Band_II_PyPSA_Implementierung.md), Blob `6412d1e776ae0e8646c429250a439aadae2496b5` | **Prototyp**/Validierungsplan, keine vollständige offizielle Integration |
| **R05** | [pypsa_adapter.py](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/src/tyndp_reduce/pypsa_adapter.py), Blob `62c54669f5413598f9f5d231c6ebea7e9b4ca914`; [security_projection.py](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/src/tyndp_reduce/security_projection.py), Blob `523919c2e0bd122e1271c59cc50a035c731b2b16` | bewusste Reject-Gates und N-1-Domainrestriktionen |
| **R06** | [Wetterjahrauswahl V1](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/docs/current/IOSN_2026_Wetterjahrauswahl_konsolidierte_Methodik_2024_2022.md), Blob `04c0cc1d81b904ed80a1d8af04a2f7d81d477ed0` | wissenschaftliche Rekonstruktion, keine originale ENTSO-E-Software |
| **R07** | [Wetterjahrauswahl V2/FlexPlan](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/docs/current/IOSN_2026_Wetterjahrauswahl_V2_FlexPlan_Vergleich_und_Verfeinerung.md), Blob `b42d91ba6f3537d695cecbab150a2a85cd874202` | eigenständiger **Forschungsvorschlag; noch nicht numerisch validiert**, keine offizielle 2026er Alternative |
| **R08** | [aggregation.py](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/src/tyndp_reduce/aggregation.py), Blob `e1e306e3b2b344f389be8b6a52583efb279ddeaa`; [tests/test_core.py](https://github.com/AlOussama/TYNDP_Products/blob/1595d6d38e77804760612621657721b3699d2fea/tests/test_core.py), Blob `1a2e4ddcfab43031291da7fce41ff49658c75a30` | synthetische Belege für definierte mathematische Eigenschaften, **nicht** 2026er E2E-Integration |

## Anspruchsgrenzen

- **Official (draft):** Aussagen „ENTSO-E beschreibt“ sind nur im Geltungsbereich der **Fassung für Konsultation** belegt.
- **Repo-Forschung:** eigene Mathematik/Algorithmen bleiben wissenschaftliche Vorschläge oder analytische Ableitungen; Quelle [R03] unterscheidet sie bereits nach Evidenzklasse.
- **Review-Entwurf:** Begriffe wie Contract, Validator, B+-Governance, Portfolio-Regret und Pflicht-Tests sind hier **vorgeschlagene Prüf-/Architekturentscheidungen**, keine von ENTSO-E behaupteten normativen Pflichten.
- **Nicht verfügbar:** veröffentlichte vollständige Tool-Instanzen/Originaldaten/versionsgepinntes Antares-/PLEXOS-Konformitätstestpaket und final freigegebene 2026er IoSN-Methode. Keine fingierten Tool-Ergebnisse.
