"""Validate imported result statuses in the synthetic lab-results CSV."""
from __future__ import annotations

import argparse
import pandas as pd

from .range_status import calculate_status


def validate(path: str) -> tuple[int, int, int]:
    df = pd.read_csv(path)
    calculated = df.apply(
        lambda r: calculate_status(
            None if pd.isna(r["MeasuredValue"]) else float(r["MeasuredValue"]),
            None if pd.isna(r["ReferenceLow"]) else float(r["ReferenceLow"]),
            None if pd.isna(r["ReferenceHigh"]) else float(r["ReferenceHigh"]),
        ),
        axis=1,
    )
    expected = df["ResultStatus"].astype(str).str.strip().str.upper()
    matches = int((calculated == expected).sum())
    return len(df), matches, len(df) - matches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    args = parser.parse_args()
    rows, matches, mismatches = validate(args.csv_path)
    print(f"rows={rows}")
    print(f"status_matches={matches}")
    print(f"status_mismatches={mismatches}")
    raise SystemExit(0 if mismatches == 0 else 1)


if __name__ == "__main__":
    main()
