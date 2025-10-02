"""Streamlit UI for the Ames housing price demo."""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import List

import streamlit as st

from src.config import load_config
from src.predict import load_default_model, predict_price
from src.simulator import HouseEvent, load_feature_stats, iter_events


LOG_PATH = Path("logs/events.log")


def setup_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        filemode="a",
    )


def format_payload(payload: dict) -> str:
    items = [f"{key}: {value:.0f}" for key, value in payload.items()]
    return " | ".join(items)


def draw_sidebar(
    refresh_rate: float, default_interval: float, default_batch: int
) -> tuple[float, int]:
    st.sidebar.header("Simulation Controls")
    interval = st.sidebar.slider(
        "Seconds between batches",
        min_value=5,
        max_value=120,
        value=int(default_interval),
        step=5,
    )
    batch = st.sidebar.slider(
        "Houses per batch",
        min_value=1,
        max_value=5,
        value=default_batch,
    )
    st.sidebar.caption(
        "Adjust how often new house listings appear. Try faster intervals to mimic high traffic."
    )
    st.sidebar.markdown("---")
    st.sidebar.metric("UI refresh rate (sec)", refresh_rate)
    return float(interval), int(batch)


def display_events(events: List[HouseEvent], predictions: List[float]) -> None:
    for event, prediction in zip(events, predictions):
        st.toast(f"New house added – estimated price ${prediction:,.0f}")
        logging.info(
            "House event | payload=%s | prediction=%s", event.payload, prediction
        )


def main() -> None:
    setup_logging()
    config = load_config("configs/default.yaml")
    st.set_page_config(page_title=config.app.title, layout="wide")
    st.title(config.app.title)

    model, _settings = load_default_model("configs/default.yaml")
    stats_path = config.paths.artifacts / "feature_stats.json"
    if not stats_path.exists():
        st.error("Feature stats not found. Run `python -m src.train` first.")
        st.stop()

    stats = load_feature_stats(stats_path)

    interval, batch = draw_sidebar(
        refresh_rate=config.app.refresh_rate,
        default_interval=config.simulator.interval_seconds,
        default_batch=config.simulator.batch_size,
    )

    placeholder = st.empty()
    history = []

    while True:
        events = list(iter_events(stats, batch))
        predictions = [predict_price(model, e.payload) for e in events]
        history.extend(
            {
                "timestamp": time.strftime("%H:%M:%S", time.localtime(e.created_at)),
                **e.payload,
                "prediction": p,
            }
            for e, p in zip(events, predictions)
        )

        display_events(events, predictions)

        with placeholder.container():
            st.subheader("Latest batch")
            st.write(history[-batch:])
            st.subheader("Prediction history")
            st.dataframe(history[-50:])

        time.sleep(interval)


if __name__ == "__main__":
    main()
