"""Render frames by walking the timeline through the backend."""
from __future__ import annotations

from pathlib import Path

from tqdm import tqdm

from song_to_visuals.core.backend import VisualBackend
from song_to_visuals.core.timeline import Timeline
from song_to_visuals.models.project import RenderConfig
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)


class RenderHandler:
    def __init__(self, cfg: RenderConfig, backend: VisualBackend) -> None:
        self.cfg = cfg
        self.backend = backend

    def render(self, *, timeline: Timeline, out_dir: Path) -> Path:
        out_dir.mkdir(parents=True, exist_ok=True)
        size = (1280, 720)
        for plan in tqdm(timeline.frames, desc="render"):
            img = self.backend.render_frame(plan.prompt, plan.seed, size, plan.strength)
            img.save(out_dir / f"frame_{plan.index:06d}.png")
        log.info("render done frames=%d dir=%s", timeline.frame_count(), out_dir)
        return out_dir