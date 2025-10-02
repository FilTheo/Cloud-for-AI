"""Simple configuration helper for the MLOps regression demo."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass
class Paths:
    project_root: Path
    data_raw: Path
    data_processed: Path
    models: Path
    artifacts: Path
    logs: Path


@dataclass
class TrainingConfig:
    target: str
    features: list[str]
    test_size: float
    random_state: int


@dataclass
class SimulatorConfig:
    interval_seconds: float
    batch_size: int


@dataclass
class AppConfig:
    title: str
    refresh_rate: float


@dataclass
class Settings:
    paths: Paths
    training: TrainingConfig
    simulator: SimulatorConfig
    app: AppConfig


def load_config(path: str | Path) -> Settings:
    """Load configuration from a YAML file."""

    config_path = Path(path)
    raw: Dict[str, Any] = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    root = config_path.parent.parent
    paths = Paths(
        project_root=root,
        data_raw=root / "data" / "raw",
        data_processed=root / "data" / "processed",
        models=root / "models",
        artifacts=root / "artifacts",
        logs=root / "logs",
    )

    training = TrainingConfig(**raw["training"])
    simulator = SimulatorConfig(**raw["simulator"])
    app = AppConfig(**raw["app"])

    return Settings(
        paths=paths,
        training=training,
        simulator=simulator,
        app=app,
    )


__all__ = [
    "Settings",
    "Paths",
    "TrainingConfig",
    "SimulatorConfig",
    "AppConfig",
    "load_config",
]
