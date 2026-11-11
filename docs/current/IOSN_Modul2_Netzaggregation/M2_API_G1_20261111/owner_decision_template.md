# M2-API-G1 — Owner-Entscheidungsvorlage (unausgefüllt)

**Projekt:** `AlOussama/TYNDP_Products`  
**Vertragsstand:** `M2.API.v1-DRAFT` / `M2.MA2Input.v1-DRAFT`  
**Status:** `PENDING_OWNER_DECISION` · **Review-Quellen:** A `70e92ba9`, B `88374dd3`, R-M2-API `075c5090`.  
**Wirkungsbereich:** M2 API-/MA1→MA2-Eingang; ein Owner-Beschluss ist **nicht** gleich Merge-/MA2-Implementierungs-/Runtime-/REAL-Freigabe.

## Entscheidungsregister – ausdrücklich auszufüllen

| ID | Auswahl – genau ein Wert | Empfehlung, noch unbestätigt | Tatsächlicher Ownerwert |
|---|---|---|---|
| `OD-M2-API-01` | `A_ONLY` / `B_ONLY` / `C_A_CANONICAL_OPTIONAL_B_TO_A` | `C_A_CANONICAL_OPTIONAL_B_TO_A` | **PENDING** |
| `OD-M2-API-02` | `STRICT_LOSSLESS` / `SIGNED_LOSSES_WITH_NEW_DEVICE_GATE` | `STRICT_LOSSLESS` | **PENDING** |
| `OD-M2-API-03` | `FORCE_DC_EQUALITY_AT_1E-6_MW` / `SEPARATE_MODEL_DISCREPANCY_QA` | `SEPARATE_MODEL_DISCREPANCY_QA` | **PENDING** |
| `OD-M2-API-04` | `NOMINAL_EXACT_WITH_IMPLICIT_PROTECTION` / `AUDITED_CLASS_AND_PROTECTION` | `AUDITED_CLASS_AND_PROTECTION` | **PENDING** |
| `OD-M2-API-05` | `DOC_GATE_ONLY_NO_MERGE` / `ADDITIONAL_IMPLEMENTATION_AUTHORIZATION` | `DOC_GATE_ONLY_NO_MERGE` | **PENDING** |

## Kopiervorlage für eine **zukünftige** ausdrückliche Ownerantwort

```text
Ich entscheide als Project Owner von AlOussama/TYNDP_Products
auf Grundlage von M2-API-G1 / R-M2-API (075c50903b7d51ec19befb4a4b8db1322ae33b2a):

OD-M2-API-01 = [A_ONLY | B_ONLY | C_A_CANONICAL_OPTIONAL_B_TO_A]
OD-M2-API-02 = [STRICT_LOSSLESS | SIGNED_LOSSES_WITH_NEW_DEVICE_GATE]
OD-M2-API-03 = [FORCE_DC_EQUALITY_AT_1E-6_MW | SEPARATE_MODEL_DISCREPANCY_QA]
OD-M2-API-04 = [NOMINAL_EXACT_WITH_IMPLICIT_PROTECTION | AUDITED_CLASS_AND_PROTECTION]
OD-M2-API-05 = [DOC_GATE_ONLY_NO_MERGE | ADDITIONAL_IMPLEMENTATION_AUTHORIZATION]

Geltungsbereich / zusätzliche Vorbehalte: [text]
Datum (UTC): [YYYY-MM-DDTHH:MM:SSZ]
Referenz zur Owner-Aussage: [Issue/Kommentar/Commit-URL]

Eine Änderung an main, PR-Merge, MA2-Implementierung, MA2/MA3-Runtime
oder REAL_QUALIFIED wird durch diesen Beschluss nicht automatisch autorisiert.
```

## Nach Eingang prüfen und dokumentieren

1. Originalzitat und Autorisierung belegen (Link, UTC-Datum, vollständiger Wortlaut); nicht aus einer Empfehlung, einem CI-Lauf oder einer früheren allgemeinen Governance-Aussage rückschließen.
2. Jede Option exakt auf einen zulässigen Enum-Wert abbilden; widersprüchliche, fehlende oder nicht eindeutig zugelassene Optionen bleiben `PENDING` und gehen zur Klärung an den Owner zurück.
3. Falls `OD-M2-API-01=B_ONLY`: **nicht** den A-Vertrag als B-freigegeben markieren; zunächst Handoff 85, Quellen-, Zeit-, Geräte-, Ausgabe- und MA2-Contract neu spezifizieren und vorlegen.
4. Falls `OD-M2-API-01=C_A_CANONICAL_OPTIONAL_B_TO_A`: keine B-Code-Übernahme ohne separaten Adapter-Review. B bleibt unabhängig, MA2 akzeptiert nur A-Schema.
5. Bei `SIGNED_LOSSES_WITH_NEW_DEVICE_GATE`: **kein** automatischer lossless-Ausnahmebetrieb; Loss-Accounting, Terminals, KCL, Provenienz und externen Solververgleich separat bewilligen.
6. Bei `AUDITED_CLASS_AND_PROTECTION`: die numerische Schwelle, Ausnahme-/Country-Provenienz und Protected-Union-Regel zusätzlich in einem versionierten I-Entscheidungsregister konkretisieren; Policy-ID/Hash einfrieren.
7. Das auf GitHub veröffentlichte Owner-Ledger setzt erst dann `OWNER_ACCEPTED_A/B/C`, wenn ein neues, unveränderliches Owner-Zitat existiert. **Dieses Dokument setzt bewusst keinerlei solchen Status.**

## Unverändert offene technische Gates

- MA1: PHY-R01..04 und R-CLU-001..002 Reparatur + getrenntes Review am **gleichen integrierten Repair-SHA**; R-CLU-P2 dispositionieren.
- R-API-P1-01..09: MA2-kompatible Disposition und fail-closed Tests; G05 unverändert nachweisen.
- MA2: G06–G08 und R-NUM `NOT_IMPLEMENTED/NOT_RUN`.
- Real: vollständige 37/102-Eingaben, unabhängiger D4-Originalbytes-/Dispatch-/Device-/Ratings-Witness und O26 Authority-Gate `BLOCKED`.
- `NO_MERGE` / `NO_M0_M1_WEATHER_CHANGE` / `NO_MA2_RUNTIME_GO` bleiben bis gesonderter Freigabe bestehen.
