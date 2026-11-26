# integrated method swap report

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

Actual native run: https://github.com/AlOussama/TYNDP_Products/actions/runs/45878174824/job/140110475360. Exact observed receipts in native_mathspec_experiments/method_receipts.json. Same public native parsing, typing, canonicalization and typed Program consumer for all four. Frozen R1 source bytes checked against original study method/data SHA256 before compilation. New profiles are explicit JSON artifacts, not new engine branches.

| Profile | Independent exact oracle | Result | Output |
|---|---|---|---|
| R1 begin | (1/2)(20+30/1.1+10+20/1.1)=415/11 | 415/11 | EUR real 2024 |
| R1 end | (415/11)/(11/10)=4150/121 | 4150/121 | EUR real 2024 |
| gross | 2·1/2+4·1 | 5 | MWh |
| eligible | 2·1/2·1+4·1·1/2 | 3 | MWh |

Adapter and checked parser/lowering/canonical source hashes identical for all four, no rebuild or code change between methods. Canonical leaf, method and audit digests differ; data identity matches within each pair. Owner TBD preserved; unknown operator and incompatible declared output unit rejected. Rules compiled generically from the same bounded AST operator map (not hard-coded per method). Independent expected results are exact arithmetic, not computed by adapter. Native parser/source identities verified on runner.

Limit: the new non-CBA profiles are deliberately bounded research inputs. The R1 engine's original A/B trust/ledger tests pass independently but are not wired into the native consumer. Receipt output_observable is a prototype label, not validated canonical CSNF projection; authority, full evidence lifecycle, contribution overlap, signed ledger and context receipt are not integrated. Checked code hashes cover named modules + adapter, not all transitive runtime code, which is separately pinned. No claim of complete MS06 or MS-G5. B1-04/05 remain. No approved CBA methodology; only synthetic cost proxy.
