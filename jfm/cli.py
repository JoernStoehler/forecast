"""Typer-based CLI for JFM."""

from __future__ import annotations

from pathlib import Path
import json
import typer

from .io.loader import load_graph, ValidationError
from .model import engine, sensitivity, render as renderer

app = typer.Typer()


@app.command()
def validate(path: Path) -> None:
    """Validate a model YAML file against the schema."""
    try:
        load_graph(path)
    except ValidationError as e:
        typer.echo(f"Invalid: {e}")
        raise typer.Exit(code=1)
    typer.echo("valid")


@app.command()
def simulate(path: Path, runs: int = 1000, seed: int = 0) -> None:
    """Run a Monte Carlo simulation."""
    summary = engine.simulate(path, runs=runs, seed=seed)
    typer.echo(json.dumps(summary, indent=2))


@app.command()
def sensitivity_cmd(path: Path, runs: int = 100, seed: int = 0) -> None:
    """Placeholder sensitivity analysis."""
    result = sensitivity.one_at_a_time(path, runs=runs, seed=seed)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def render(path: Path, out: Path = Path("graph")) -> None:
    """Render the model graph to an SVG file."""
    renderer.render(path, out)
    typer.echo(f"wrote {out.with_suffix('.svg')}")


if __name__ == "__main__":
    app()
