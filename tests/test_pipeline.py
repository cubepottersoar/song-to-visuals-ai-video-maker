"""Smoke tests for the pipeline + timeline."""
from __future__ import annotations

from song_to_visuals.core.timeline import Timeline
from song_to_visuals.models.beats import BeatResult
from song_to_visuals.models.lyrics import LyricAlignment, LyricLine
from song_to_visuals.models.style import ResolvedStyle


def _style() -> ResolvedStyle:
    return ResolvedStyle(
        base_prompt="cinematic neon",
        prompt_suffix="film grain",
        negative_prompt="text",
        strength=0.7,
        seed=6767,
    )


def test_timeline_builds_expected_frame_count() -> None:
    beats = BeatResult(bpm=120.0, beats=[0.0, 0.5, 1.0], duration=2.0)
    lyrics = LyricAlignment(lines=[LyricLine(0.0, 1.0, "hello")], duration=2.0)
    tl = Timeline(fps=24)
    tl.build(beats