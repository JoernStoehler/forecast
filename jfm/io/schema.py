"""Schema helpers."""

from __future__ import annotations

from pathlib import Path
import json

SCHEMA_PATH = (
    Path(__file__).resolve().parents[2] / "model" / "schemas" / "graph.schema.json"
)


def load_graph_schema() -> dict:
    """Load and return the graph JSON schema."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
