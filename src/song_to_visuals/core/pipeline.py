"""Top-level render pipeline: audio -> beats -> lyrics -> frames -> mp4."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from song_to_visuals.core.backend import VisualBackend, build_backend
from song_to_visuals.core.timeline import Timeline
from song_to_visuals.handlers.beat_handler import BeatHandler
from song_to_visuals.handlers.lyric_handler import LyricHandler
from song_to_visuals.handlers.render_handler import RenderHandler
from song_to_visuals.handlers.style_handler import StyleHandler
from song_to_visuals.models.project import ProjectConfig
from song_to_visuals.services.ffmpeg_bridge import FfmpegBridge
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class RenderResult:
    output_path: Path
    frame_count: int
    elapsed_s: float


class Pipeline:
    """Orchestrates the full song-to-visuals render."""

    def __init__(self, cfg: ProjectConfig) -> None:
        self.cfg = cfg
        self.timeline = Timeline(fps=cfg.project.fps)
        self.backend: VisualBackend = build_backend(cfg.render.backend)
        self.ffmpeg = FfmpegBridge(cfg.output.dir)

    def run(self, dry_run: bool = False) -> RenderResult:
        log.info("pipeline start project=%s", self.cfg.project.name)
        beats = BeatHandler(self.cfg.audio).analyze(self.cfg.project.audio_path)
        log.info("beats=%d bpm=%.1f", len(beats.beats), beats.bpm)

        lyrics = LyricHandler(self.cfg.lyrics).align(self.cfg.project.audio_path, beats)
        style = StyleHandler(self.cfg.style).resolve()

        self.timeline.build(beats=beats, lyrics=lyrics, style=style)
        if dry_run:
            return RenderResult(Path(""), frame_count=self.timeline.frame_count(), elapsed_s=0.0)

        self.backend.warmup()
        frames_dir = RenderHandler(self.cfg.render, self.backend).render(
            timeline=self.timeline, out_dir=Path(self.cfg.output.dir) / "frames"
        )
        out = self.ffmpeg.mux(frames_dir, self.cfg.project.audio_path, self.cfg.render)
        self.backend.close()
        return RenderResult(out, frame_count=self.timeline.frame_count(), elapsed_s=0.0)