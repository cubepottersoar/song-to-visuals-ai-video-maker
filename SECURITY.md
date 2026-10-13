# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

Email `security@song-to-visuals.dev` with a description, a reproducer, and the affected
version. We aim to acknowledge within 72 hours.

Do not open a public issue for anything that could let a crafted `.s2v` project file
execute arbitrary code — that path runs through `song_to_visuals.services.project_loader`
and we treat it as high severity.

## Threat model

This is a desktop tool that reads local audio, local images, and a project file. The
project file may reference absolute paths and shell-adjacent ffmpeg arguments. We sandbox
ffmpeg invocation through `services/ffmpeg_bridge.py`, which builds an argv list rather
than a shell string. Any PR that reintroduces `shell=True` will be rejected.

Model weights are downloaded over HTTPS from a pinned manifest in `config/models.yaml`.
Checksums are verified in `services/model_registry.py` before load.