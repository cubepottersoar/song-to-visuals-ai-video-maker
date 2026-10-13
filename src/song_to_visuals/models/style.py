"""Resolved style used by the timeline."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ResolvedStyle:
    base_prompt: str
    prompt_suffix: str
    negative_prompt: str
    strength: float
    seed: int

    def compose(self, lyric_or_base: str) -> str:
        parts = [lyric_or_base.strip(), self.base_prompt.strip(), self.prompt_suffix.strip()]
        return ", ".join(p for p in parts if p)