"""Inference helpers for the regression model."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from .config import Settings, load_config


def load_model(model_path: Path) -> Pipeline:
    """Load the persisted scikit-learn pipeline."""

    return joblib.load(model_path)


def predict_price(model: Pipeline, features: dict[str, float]) -> float:
    """Predict a single house price given feature values."""

    df = pd.DataFrame([features])
    prediction = model.predict(df)
    return float(prediction[0])


def batch_predict(model: Pipeline, rows: Iterable[dict[str, float]]) -> list[float]:
    """Predict prices for multiple houses."""

    df = pd.DataFrame(rows)
    predictions = model.predict(df)
    return np.asarray(predictions, dtype=float).tolist()


def load_default_model(
    config_path: str | Path = "configs/default.yaml",
) -> tuple[Pipeline, Settings]:
    settings = load_config(config_path)
    model_path = settings.paths.models / "linear_regression.pkl"
    model = load_model(model_path)
    return model, settings


__all__ = [
    "load_model",
    "predict_price",
    "batch_predict",
    "load_default_model",
]
