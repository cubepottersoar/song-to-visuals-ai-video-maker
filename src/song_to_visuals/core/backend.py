"""VisualBackend interface + factory."""
from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml
from PIL.Image import Image

from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)
BACKENDS_YAML = Path(__file__).resolve().parents[3] / "config" / "backends.yaml"


class VisualBackend(ABC):
    """A diffusion backend that renders one frame given a prompt + seed."""

    name: str = "base"

    @abstractmethod
    def warmup(self) -> None: ...

    @abstractmethod
    def render_frame(
        self, prompt: str, seed: int, size: tuple[int, int], strength: float
    ) -> Image: ...

    @abstractmethod
    def close(self) -> None: ...


def _load_registry() -> dict[str, Any]:
    with BACKENDS_YAML.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def build_backend(choice: str) -> VisualBackend:
    reg = _load_registry()
    order = reg["order"] if choice == "auto" else [choice]
    last_err: Exception | None = None
    for name in order:
        spec = reg["backends"].get(name)
        if not spec:
            continue
        try:
            mod = importlib.import_module(spec["module"])
            cls = getattr(mod, spec["class"])
            log.info("backend selected=%s device=%s", name, spec.get("device"))
            return cls(**{k: v for k, v in spec.items() if k not in ("module", "class")})
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            log.warning("backend %s unavailable: %s", name, exc)
    raise RuntimeError(f"no visual backend available: {last_err}")