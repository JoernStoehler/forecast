"""Sensitivity analysis stubs."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from .engine import simulate


def one_at_a_time(path: str | Path, runs: int = 100, seed: int = 0) -> Dict[str, float]:
    """Very small placeholder one-at-a-time sensitivity analysis."""
    base = simulate(path, runs=runs, seed=seed)
    return {"baseline": base["P(N12)"]}
