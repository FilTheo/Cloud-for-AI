"""Train the regression model and persist artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .config import Settings, load_config
from .data_prep import SELECTED_COLUMNS, download_data, preprocess


def compute_feature_stats(df: pd.DataFrame) -> dict:
    """Compute summary statistics used by the simulator."""

    stats = {}
    for column in df.columns:
        if column == "SalePrice":
            continue
        series = df[column]
        stats[column] = {
            "min": float(series.min()),
            "max": float(series.max()),
            "mean": float(series.mean()),
            "std": float(series.std(ddof=0)),
        }
    return stats


def prepare_data(settings: Settings) -> pd.DataFrame:
    raw_path = settings.paths.data_raw / "ames_subset.csv"
    processed_path = settings.paths.data_processed / "ames_subset_clean.csv"

    if not raw_path.exists():
        download_data(raw_path, columns=SELECTED_COLUMNS)
    preprocess(raw_path, processed_path)
    return pd.read_csv(processed_path)


def train_model(settings: Settings) -> tuple[Pipeline, dict]:
    df = prepare_data(settings)
    target = settings.training.target
    features = settings.training.features

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=settings.training.test_size,
        random_state=settings.training.random_state,
    )

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("regressor", LinearRegression()),
        ]
    )

    pipeline.fit(X_train, y_train)

    stats = compute_feature_stats(df)
    stats["target_mean"] = float(y_train.mean())
    stats["target_std"] = float(y_train.std(ddof=0))
    stats["test_size"] = settings.training.test_size

    return pipeline, stats


def save_artifacts(model: Pipeline, stats: dict, settings: Settings) -> None:
    settings.paths.models.mkdir(parents=True, exist_ok=True)
    settings.paths.artifacts.mkdir(parents=True, exist_ok=True)

    model_path = settings.paths.models / "linear_regression.pkl"
    stats_path = settings.paths.artifacts / "feature_stats.json"

    joblib.dump(model, model_path)
    stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")


def main(config_path: str | Path = "configs/default.yaml") -> None:
    settings = load_config(config_path)
    model, stats = train_model(settings)
    save_artifacts(model, stats, settings)


if __name__ == "__main__":
    main()
