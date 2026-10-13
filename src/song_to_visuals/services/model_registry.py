"""Download + checksum-verify model artifacts."""
from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from song_to_visuals.utils.logging import get_logger

log = get_logger(__name__)
MANIFEST = Path(__file__).resolve().parents[3] / "config" / "models.yaml"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(name: str, cache_dir: str | Path = "models") -> Path:
    with MANIFEST.open("r", encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh)
    art = manifest["artifacts"][name]
    p = Path(cache_dir) / art["file"]
    if not p.exists():
        raise FileNotFoundError(f"missing artifact {name}: {p}")
    got = _sha256(p)
    if got != art["sha256"]:
        raise ValueError(f"checksum mismatch for {name}: {got}")
    log.info("artifact verified name=%s", name)
    return p