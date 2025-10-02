"""Basic tests for data preprocessing."""

from pathlib import Path

import pandas as pd

from src import data_prep


def test_preprocess_removes_nulls(tmp_path: Path) -> None:
    raw_csv = tmp_path / "raw.csv"
    processed_csv = tmp_path / "processed.csv"

    df = pd.DataFrame(
        {
            "Overall Qual": [5, None],
            "Overall Cond": [7, 8],
            "Gr Liv Area": [1500, 1800],
            "Central Air": ["Y", "N"],
            "Total Bsmt SF": [800, 900],
            "SalePrice": [200000, 250000],
        }
    )
    df.to_csv(raw_csv, index=False)

    result_path = data_prep.preprocess(raw_csv, processed_csv)

    cleaned = pd.read_csv(result_path)
    assert cleaned.isnull().sum().sum() == 0
    assert len(cleaned) == 1
