import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from jfm.model import edges  # noqa: E402


def test_logistic_monotonic():
    x1, x2 = 0.1, 0.9
    y1 = edges.logistic(x1, w=1.0, b=0.0)
    y2 = edges.logistic(x2, w=1.0, b=0.0)
    assert y1 < y2


def test_gate_min_never_increases():
    x = 0.8
    y = edges.gate_min(x, risk_multiplier=0.5)
    assert y <= x
