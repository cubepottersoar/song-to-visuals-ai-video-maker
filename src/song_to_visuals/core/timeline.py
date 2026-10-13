"""Frame timeline: maps audio time -> prompt + seed + transition."""
from __future__ import annotations

from dataclasses import dataclass, field

from song_to_visuals.models.beats import BeatResult
from song_to_visuals.models.lyrics import LyricAlignment
from song_to_visuals.models.style import ResolvedStyle


@dataclass(slots=True)
class FramePlan:
    index: int
    t: float
    prompt: str
    seed: int
    strength: float
    transition: str


@dataclass(slots=True)
class Timeline:
    fps: int
    frames: list[FramePlan] = field(default_factory=list)

    def frame_count(self) -> int:
        return len(self.frames)

    def build(
        self, *, beats: BeatResult, lyrics: LyricAlignment, style: ResolvedStyle
    ) -> None:
        self.frames.clear()
        duration = max(beats.duration, 1.0)
        total = int(duration * self.fps)
        beat_set = {round(b, 3) for b in beats.beats}
        for i in range(total):
            t = i / self.fps
            line = lyrics.line_at(t)
            base = line.text if line else style.base_prompt
            prompt = style.compose(base)
            seed = style.seed + (i // max(1, self.fps // 2))
            strength = style.strength
            transition = "beat-cut" if round(t, 3) in beat_set else "hold"
            self.frames.append(FramePlan(i, t, prompt, seed, strength, transition))