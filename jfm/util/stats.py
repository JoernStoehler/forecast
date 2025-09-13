"""Distribution helpers."""

from __future__ import annotations

from typing import Dict

import numpy as np


def sample(prior: Dict[str, float], rng: np.random.Generator) -> float:
    """Sample a value from a prior definition."""
    dist = prior.get("dist")
    if dist == "Beta":
        a = prior["a"]
        b = prior["b"]
        return float(rng.beta(a, b))
    if dist == "LogNormal":
        mu = prior["mu"]
        sigma = prior["sigma"]
        return float(rng.lognormal(mean=mu, sigma=sigma))
    raise ValueError(f"Unsupported distribution: {dist}")
