"""Resolve style preset into a prompt template + params."""
from __future__ import annotations

from pathlib import Path

import yaml

from song_to_visuals.models.project import StyleConfig
from song_to_visuals.models.style import ResolvedStyle
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)
PRESETS = Path(__file__).resolve().parents[3] / "config" / "presets"


class StyleHandler:
    def __init__(self, cfg: StyleConfig) -> None:
        self.cfg = cfg

    def resolve(self) -> ResolvedStyle:
        preset_file = PRESETS / f"{self.cfg.preset}.yaml"
        data: dict = {}
        if preset_file.exists():
            with preset_file.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
        base = data.get("base_prompt", "cinematic, moody lighting")
        suffix = data.get("prompt_suffix", "")
        log.info("style resolved preset=%s", self.cfg.preset)
        return ResolvedStyle(
            base_prompt=base,
            prompt_suffix=suffix,
            negative_prompt=self.cfg.negative_prompt,
            strength=self.cfg.strength,
            seed=self.cfg.seed,
        )