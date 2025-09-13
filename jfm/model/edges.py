"""Edge functions for the causal graph."""

from __future__ import annotations

import math
from typing import Iterable


def logistic(x: float, w: float, b: float) -> float:
    return 1 / (1 + math.exp(-(w * x + b)))


def inhibitory_logistic(x: float, w: float, b: float) -> float:
    return logistic(x, w, b)


def multiplicative(x: float, alpha: float) -> float:
    return x * alpha


def gate_min(x: float, risk_multiplier: float) -> float:
    return min(x, x * risk_multiplier)


def gate_max(
    x: float, policy: float, max_multiplier: float, min_multiplier: float
) -> float:
    mult = min_multiplier + (max_multiplier - min_multiplier) * policy
    return x * mult


def noisy_or(sources: Iterable[float], p_leak: float) -> float:
    prod = 1.0
    for s in sources:
        prod *= 1 - s
    return 1 - (1 - p_leak) * prod
