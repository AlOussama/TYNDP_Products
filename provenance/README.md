# Provenance and version policy

`artifact_manifest.json` is a preserved **historic upload manifest**, not a map of the current canonical repository paths. Its path references predate the 2026-10-19 reorganisation.

Current authoritative locations:

| Data class | Location |
| --- | --- |
| Scientific methodology (current) | `docs/current/` |
| Legacy reports (unaltered) | `docs/archive/` |
| Executable research package | `src/tyndp_reduce/` |
| Tests | `tests/` |
| Synthetic outputs | `results/synthetic/` |
| Original ZIP artifact bundles | `artifacts/bundles/` |
| Older original revision reports/results | `artifacts/snapshots/` |
| Restored historical validation manifest | `artifacts/snapshots/VALIDATION_MANIFEST_2026-10-16.json` |

Do not confuse duplicate report filenames in the archived revision with the latest renderings in `docs/current/`. Do not treat synthetic test outcomes as independent ENTSO-E validation. GitHub Actions validates mathematical core logic; real-network PyPSA integration remains a separate open qualification gate.
