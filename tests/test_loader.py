import pathlib
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from jfm.io.loader import load_graph, ValidationError  # noqa: E402


def test_load_valid_graph(tmp_path: Path):
    data = load_graph(Path("model/current.yaml"))
    assert "nodes" in data
    assert "edges" in data


def test_invalid_graph(tmp_path: Path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("invalid: true")
    with pytest.raises(ValidationError):
        load_graph(bad)
