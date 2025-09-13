import pathlib
import sys
from pathlib import Path

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from jfm.model import engine  # noqa: E402


def test_simulate_writes_summary(tmp_path):
    summary = engine.simulate(Path("model/current.yaml"), runs=10, seed=1)
    assert 0.0 <= summary["P(N12)"] <= 1.0
    runs_dir = Path("runs")
    assert any((d / "summary.json").exists() for d in runs_dir.iterdir())
