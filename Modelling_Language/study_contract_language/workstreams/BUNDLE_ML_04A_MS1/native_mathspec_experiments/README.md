# native mathspec experiments/README

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

## Actual run and reproduction
First CI: https://github.com/AlOussama/TYNDP_Products/actions/runs/45877500514 (native identity checks, 9 native static fragments, 4140 upstream passed/47 skipped, 50 R1 tests). Second run: https://github.com/AlOussama/TYNDP_Products/actions/runs/45878174824 (new finite consumer, original P5 oracle, explicit 57 R1 rerun). See observed log evidence file and gate report for final counts. 
On network-enabled host with Git and pixi:
```sh
git clone https://github.com/energy-models/mathspec mathspec-src
cd mathspec-src
git checkout 5f1464c334c1012cdee2947d4d55b4d1d6bef40a
test "$(git hash-object src/mathspec/_canonical.py)" = a8487b60f03839fc622834ffcaf76e1f9c99f6e9
test "$(git hash-object pixi.lock)" = dcf89e3e6b3794a1ae79d00a07978ceaec37daba
pixi install --locked -e py313
pixi run --locked -e py313 python /absolute/path/to/MS1/native_mathspec_experiments/native_probe.py
pixi run --locked -e py313 python /absolute/path/to/MS1/architecture_prototypes/experiment.py
pixi run --locked -e py313 pytest -q
```
Run from R1 directory: python -m unittest discover -v -p 'test*.py'; python pinned/test_freedom.py. Checkout original P5 SHA in a separate directory, invoke its original tools/cba_stress_oracle.js runSuite() and assert passed===total. Workflow pins GitHub Actions and checks native lock and source file identity. No simulated native execution. Use exact external lock (not regenerated): https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/pixi.lock.
