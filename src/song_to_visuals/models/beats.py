"""Beat analysis result."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class BeatResult:
    bpm: float
    beats: list[float] = field(default_factory=list)
    duration: float = 0.0

    def nearest_beat(self, t: float, tol: float = 0.05) -> float | None:
        for b in self.beats:
            if abs(b - t) <= tol:
                return b
        return None