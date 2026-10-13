# Contributing to song-to-visuals-ai-video-maker

Thanks for wanting to push the AI music video generator forward. This repo turns a song into a
synced visual sequence — beat detection, lyric segmentation, style transfer, and frame diffusion
stitched into an MP4.

## Ground rules

- Python 3.11+ is the floor. 3.12 is what CI runs.
- One feature per PR. Big refactors get an issue first.
- Run `pytest -q` and `ruff check src` before you open the PR. Both must be green.
- Keep GPU assumptions out of the core. The renderer talks to a `VisualBackend` interface; CUDA,
  DirectML, and CPU fallbacks all implement it.

## Layout

```
src/                    # bootstrap + package root
  song_to_visuals/      # main package
    core/               # engine: pipeline orchestration, timeline
    handlers/           # per-feature handlers (beat, lyrics, style, render)
    services/           # external-facing services (model server, ffmpeg bridge)
    models/             # dataclasses + pydantic schemas
    utils/              # shared helpers
config/                 # default YAML + presets
tests/                  # pytest suite
```

## Adding a backend

1. Subclass `song_to_visuals.core.backend.VisualBackend`.
2. Implement `warmup()`, `render_frame(prompt, seed, size)`, `close()`.
3. Register it in `config/backends.yaml`.
4. Add a test in `tests/test_backends.py`.

## Style

- Ruff config lives in `pyproject.toml`. Line length 100.
- Type hints everywhere public. `from __future__ import annotations` at the top.
- Logging via `song_to_visuals.utils.logging.get_logger`, never `print`.

## Commit messages

`scope: short imperative summary` — e.g. `beat: handle 6/8 time signatures`.