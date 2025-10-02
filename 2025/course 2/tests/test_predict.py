"""Basic tests for prediction helpers."""

from pathlib import Path

import joblib
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.pipeline import Pipeline

from src import predict


def dummy_model(tmp_path: Path) -> Path:
    model_path = tmp_path / "dummy.pkl"
    pipeline = Pipeline(steps=[("regressor", DummyRegressor(strategy="median"))])
    pipeline.fit(np.array([[1], [2]]), np.array([100000, 150000]))
    joblib.dump(pipeline, model_path)
    return model_path


def test_predict_price_returns_float(tmp_path: Path) -> None:
    model_path = dummy_model(tmp_path)
    model = predict.load_model(model_path)

    price = predict.predict_price(model, {"feature": 1})

    assert isinstance(price, float)
    assert price > 0


def test_batch_predict_handles_multiple_rows(tmp_path: Path) -> None:
    model_path = dummy_model(tmp_path)
    model = predict.load_model(model_path)

    predictions = predict.batch_predict(model, [{"feature": 1}, {"feature": 2}])

    assert isinstance(predictions, list)
    assert len(predictions) == 2
