"""Lyric alignment handler (whisperx optional)."""
from __future__ import annotations

from pathlib import Path

from song_to_visuals.models.beats import BeatResult
from song_to_visuals.models.lyrics import LyricAlignment, LyricLine
from song_to_visuals.models.project import LyricConfig
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)


class LyricHandler:
    def __init__(self, cfg: LyricConfig) -> None:
        self.cfg = cfg

    def align(self, audio_path: str | Path, beats: BeatResult) -> LyricAlignment:
        if not self.cfg.enabled or self.cfg.aligner == "none":
            return LyricAlignment(lines=[], duration=beats.duration)
        try:
            import whisperx  # type: ignore
        except ImportError:
            log.warning("whisperx not installed; falling back to beat-only prompts")
            return LyricAlignment(lines=[], duration=beats.duration)

        model = whisperx.load_model("small", device="cpu", compute_type="int8")
        audio = whisperx.load_audio(str(audio_path))
        result = model.transcribe(audio, language=self.cfg.language)
        lines: list[LyricLine] = []
        for seg in result.get("segments", []):
            if (seg["end"] - seg["start"]) * 1000 < self.cfg.min_segment_ms:
                continue
            lines.append(LyricLine(start=seg["start"], end=seg["end"], text=seg["text"].strip()))
        log.info("lyric align lines=%d", len(lines))
        return LyricAlignment(lines=lines, duration=beats.duration)