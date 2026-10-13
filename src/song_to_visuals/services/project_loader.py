"""Load + validate a .s2v project file (YAML)."""
from __future__ import annotations

from pathlib import Path

import yaml

from song_to_visuals.models.project import ProjectConfig
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)


def load_project(path: str | Path) -> ProjectConfig:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"project not found: {p}")
    with p.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    cfg = ProjectConfig.model_validate(raw)
    log.info("project loaded name=%s", cfg.project.name)
    return cfg