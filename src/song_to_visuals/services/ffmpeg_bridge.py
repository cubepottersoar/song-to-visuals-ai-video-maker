"""ffmpeg invocation built as argv (never shell=True)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from song_to_visuals.models.project import RenderConfig
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)


class FfmpegBridge:
    def __init__(self, out_dir: str | Path) -> None:
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        if shutil.which("ffmpeg") is None:
            raise RuntimeError("ffmpeg not found on PATH")

    def mux(self, frames_dir: Path, audio_path: str, cfg: RenderConfig) -> Path:
        out = self.out_dir / "music_video.mp4"
        argv = [
            "ffmpeg", "-y",
            "-framerate", "24",
            "-i", str(frames_dir / "frame_%06d.png"),
            "-i", str(audio_path),
            "-c:v", cfg.codec,
            "-b:v", cfg.bitrate,
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-shortest",
            str(out),
        ]
        log.info("ffmpeg mux -> %s", out)
        subprocess.run(argv, check=True)
        return out