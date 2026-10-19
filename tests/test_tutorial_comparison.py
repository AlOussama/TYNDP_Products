"""Regression tests for the published method-comparison tutorial."""
import importlib.util
from pathlib import Path
import pandas as pd
import pytest

MODULE = Path(__file__).resolve().parents[1] / "tools" / "compare_methods.py"
spec = importlib.util.spec_from_file_location("tutorial_comparison", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_comparison_orders_methods_and_computes_gain(tmp_path):
    p = tmp_path / "comparison.csv"
    pd.DataFrame({
        "clustering": ["A", "B"], "reference": ["uniform", "capacity"],
        "validation_plain_RMSE_MW": [4.0, 2.0],
        "validation_corrected_RMSE_MW": [2.0, 1.5],
        "validation_joint_fit_RMSE_MW": [1.0, 1.1],
        "screening_coverage": [.8, .7], "n_zones": [5, 5],
        "cycle_rank": [1, 1]
    }).to_csv(p, index=False)
    out = module.compare(p)
    assert list(out.clustering) == ["B", "A"]
    assert out.loc[out.clustering == "A", "structural_correction_gain_pct"].iloc[0] == 50.

def test_comparison_rejects_missing_metric(tmp_path):
    p = tmp_path / "missing.csv"
    pd.DataFrame({"clustering":["A"]}).to_csv(p,index=False)
    with pytest.raises(ValueError,match="Missing comparison columns"):
        module.compare(p)
