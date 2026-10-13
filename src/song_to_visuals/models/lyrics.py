"""Lyric alignment result."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LyricLine:
    start: float
    end: float
    text: str


@dataclass(slots=True)
class LyricAlignment:
    lines: list[LyricLine] = field(default_factory=list)
    duration: float = 0.0

    def line_at(self, t: float) -> LyricLine | None:
        for line in self.lines:
            if line.start <= t < line.end:
                return line
        return None