"""Project + config schemas loaded from .s2v files."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ProjectMeta(BaseModel):
    name: str = "untitled"
    fps: int = 24
    resolution: tuple[int, int] = (1280, 720)
    duration_mode: str = "full"
    clip_seconds: int = 30
    audio_path: str = ""


class AudioConfig(BaseModel):
    sample_rate: int = 22050
    hop_length: int = 512
    beat_sensitivity: float = 0.65
    min_bpm: int = 60
    max_bpm: int = 200


class LyricConfig(BaseModel):
    enabled: bool = True
    language: str = "en"
    aligner: str = "whisperx"
    min_segment_ms: int = 400


class StyleConfig(BaseModel):
    preset: str = "neon-noir"
    strength: float = 0.72
    seed: int = 6767
    negative_prompt: str = "text, watermark, logo, lowres"


class RenderConfig(BaseModel):
    backend: str = "auto"
    batch_size: int = 4
    motion_amount: float = 0.35
    transition: str = "beat-cut"
    codec: str = "libx264"
    bitrate: str = "12M"


class OutputConfig(BaseModel):
    dir: str = "./renders"
    keep_frames: bool = False


class ProjectConfig(BaseModel):
    project: ProjectMeta
    audio: AudioConfig = Field(default_factory=AudioConfig)
    lyrics: LyricConfig = Field(default_factory=LyricConfig)
    style: StyleConfig = Field(default_factory=StyleConfig)
    render: RenderConfig = Field(default_factory=RenderConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)