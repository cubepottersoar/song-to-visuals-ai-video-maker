"""Beat + tempo detection using librosa."""
from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np

from song_to_visuals.models.beats import BeatResult
from song_to_visuals.models.project import AudioConfig
from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)


class BeatHandler:
    def __init__(self, cfg: AudioConfig) -> None:
        self.cfg = cfg

    def analyze(self, audio_path: str | Path) -> BeatResult:
        y, sr = librosa.load(str(audio_path), sr=self.cfg.sample_rate, mono=True)
        tempo, beat_frames = librosa.beat.beat_track(
            y=y, sr=sr, hop_length=self.cfg.hop_length, tightness=100
        )
        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=self.cfg.hop_length)
        bpm = float(np.atleast_1d(tempo)[0])
        duration = float(librosa.get_duration(y=y, sr=sr))
        log.info("beat analyze bpm=%.1f beats=%d dur=%.1fs", bpm, len(beat_times), duration)
        return BeatResult(bpm=bpm, beats=beat_times.tolist(), duration=duration)