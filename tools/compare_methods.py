"""Compare synthetic A/B clustering and reference-PTDF methods from run_demo.py.

Usage:
  python tools/compare_methods.py --input results/tutorial_demo/comparison.csv
  python tools/compare_methods.py --input results/tutorial_demo/comparison.csv --output results/tutorial_demo/summary.csv
The RMSE values are synthetic validation figures, not ENTSO-E accuracy claims.
"""
import argparse
from pathlib import Path
import pandas as pd

REQUIRED = (
    "clustering", "reference", "validation_plain_RMSE_MW",
    "validation_corrected_RMSE_MW", "validation_joint_fit_RMSE_MW",
    "screening_coverage", "n_zones", "cycle_rank"
)

def compare(path):
    df = pd.read_csv(path)
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"Missing comparison columns: {sorted(missing)}")
    if df.duplicated(subset=["clustering", "reference"]).any():
        raise ValueError("Repeated clustering/reference rows")
    cols = ["validation_plain_RMSE_MW", "validation_corrected_RMSE_MW",
            "validation_joint_fit_RMSE_MW"]
    for col in cols:
        if df[col].isna().any() or (df[col] < 0).any():
            raise ValueError(f"Invalid nonnegative RMSE values in {col}")
    df = df.copy()
    df["structural_correction_gain_pct"] = (
        100 * (df["validation_plain_RMSE_MW"] - df["validation_corrected_RMSE_MW"])
        / df["validation_plain_RMSE_MW"].where(df["validation_plain_RMSE_MW"] > 0)
    )
    return df.sort_values(["validation_corrected_RMSE_MW", "clustering", "reference"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    table = compare(args.input)
    print(table[[
        "clustering", "reference", "validation_plain_RMSE_MW",
        "validation_corrected_RMSE_MW", "validation_joint_fit_RMSE_MW",
        "structural_correction_gain_pct", "screening_coverage", "cycle_rank"
    ]].to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(args.output, index=False)
        print(f"Wrote {args.output}")
