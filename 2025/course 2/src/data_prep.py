"""Data ingestion and preprocessing utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


AMES_URL = "http://jse.amstat.org/v19n3/decock/AmesHousing.txt"
SELECTED_COLUMNS = [
    "Overall Qual",
    "Overall Cond",
    "Gr Liv Area",
    "Central Air",
    "Total Bsmt SF",
    "SalePrice",
]


@dataclass
class DataPaths:
    raw_csv: Path
    processed_csv: Path


def download_data(output_path: Path, columns: Optional[list[str]] = None) -> Path:
    """Download the Ames dataset subset to `output_path`. Returns saved path."""

    columns = columns or SELECTED_COLUMNS
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(AMES_URL, sep="\t", usecols=columns)
    df.to_csv(output_path, index=False)
    return output_path


def preprocess(raw_path: Path, processed_path: Path) -> Path:
    """Clean the raw dataset and save the processed file."""

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(raw_path)

    # Basic cleaning
    df["Central Air"] = df["Central Air"].map({"N": 0, "Y": 1})
    df = df.dropna(axis=0)

    df.to_csv(processed_path, index=False)
    return processed_path


def load_processed(processed_path: Path) -> pd.DataFrame:
    """Load the processed dataset."""

    return pd.read_csv(processed_path)


__all__ = [
    "AMES_URL",
    "SELECTED_COLUMNS",
    "DataPaths",
    "download_data",
    "preprocess",
    "load_processed",
]
