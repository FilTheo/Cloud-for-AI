"""Synthetic data generator that simulates new house listings."""

from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generator, Iterable


@dataclass
class HouseEvent:
    payload: Dict[str, float]
    created_at: float


def load_feature_stats(stats_path: Path) -> dict:
    return json.loads(stats_path.read_text(encoding="utf-8"))


def sample_feature(stats: dict[str, float]) -> float:
    mean = stats["mean"]
    std = stats["std"] or 1.0
    value = random.gauss(mean, std)
    return float(max(stats["min"], min(stats["max"], value)))


def generate_event(stats: dict) -> HouseEvent:
    payload: Dict[str, float] = {}
    timestamp = time.time()
    for feature, values in stats.items():
        if feature.startswith("target") or feature == "test_size":
            continue
        payload[feature] = sample_feature(values)
    payload.setdefault("Central Air", round(payload.get("Central Air", 0)))
    return HouseEvent(payload=payload, created_at=timestamp)


def event_stream(
    stats: dict,
    interval_seconds: float = 30.0,
    batch_size: int = 1,
    seed: int | None = None,
) -> Generator[list[HouseEvent], None, None]:
    if seed is not None:
        random.seed(seed)

    while True:
        batch = [generate_event(stats) for _ in range(batch_size)]
        yield batch
        time.sleep(interval_seconds)


def iter_events(
    stats: dict, count: int, seed: int | None = None
) -> Iterable[HouseEvent]:
    if seed is not None:
        random.seed(seed)
    for _ in range(count):
        yield generate_event(stats)


__all__ = [
    "HouseEvent",
    "load_feature_stats",
    "generate_event",
    "event_stream",
    "iter_events",
]
