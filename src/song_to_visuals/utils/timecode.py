"""Time <-> frame <-> SMPTE helpers."""
from __future__ import annotations


def sec_to_frame(t: float, fps: int) -> int:
    return int(round(t * fps))


def frame_to_sec(frame: int, fps: int) -> float:
    return frame / fps


def smpte(t: float, fps: int) -> str:
    total = sec_to_frame(t, fps)
    f = total % fps
    s = (total // fps) % 60
    m = (total // (fps * 60)) % 60
    h = total // (fps * 3600)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"