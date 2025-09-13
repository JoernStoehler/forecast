"""Graph loader and validator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema
import yaml

from .schema import load_graph_schema


class ValidationError(Exception):
    """Raised when the input graph fails schema validation."""


def load_graph(path: str | Path) -> dict[str, Any]:
    """Load a YAML graph and validate against the JSON schema."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    schema = load_graph_schema()
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        raise ValidationError(str(e)) from e
    return data
