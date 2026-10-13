"""Bootstrap entry point for the `s2v` CLI."""
from __future__ import annotations

import sys

import typer
from rich.console import Console

from song_to_visuals import __version__
from song_to_visuals.core.pipeline import Pipeline
from song_to_visuals.models.project import ProjectConfig
from song_to_visuals.services.project_loader import load_project
from song_to_visuals.utils.logging import configure_logging

app = typer.Typer(add_completion=False, help="AI music video generator: song to visuals.")
console = Console()


@app.command()
def render(
    project: str = typer.Argument(..., help="Path to a .s2v project file."),
    out: str | None = typer.Option(None, "--out", "-o", help="Override output dir."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Plan without rendering frames."),
) -> None:
    """Render a project to MP4."""
    configure_logging()
    cfg: ProjectConfig = load_project(project)
    if out:
        cfg.output.dir = out
    pipe = Pipeline(cfg)
    result = pipe.run(dry_run=dry_run)
    console.print(f"[bold green]done[/] -> {result.output_path}")


@app.command()
def version() -> None:
    console.print(f"song-to-visuals-ai-video-maker {__version__}")


def main() -> None:
    try:
        app()
    except KeyboardInterrupt:
        console.print("[yellow]interrupted[/]")
        sys.exit(130)


if __name__ == "__main__":
    main()