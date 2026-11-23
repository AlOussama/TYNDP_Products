# Running the local prototype
Python 3.13.5 or compatible standard-library interpreter. No pip dependencies.

```sh
cd Modelling_Language/study_contract_language/workstreams/ML_C21_formal_validator_research/tools
python -m unittest -v test_csnf_validator.py
```

This executes a static synthetic fragment only. `csnf_validator.py` does not parse C20 DSL, run a solver or certify implementations. Expected executed result in initial local environment: 31 tests / OK. Recheck SHA256 in execution report against the actual source files before relying on the claim.
