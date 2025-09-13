"""Simple Monte Carlo engine."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import json
from datetime import datetime

import numpy as np

from ..io.loader import load_graph
from ..util import stats
from .edges import noisy_or


def simulate(path: str | Path, runs: int = 1000, seed: int = 0) -> Dict[str, float]:
    """Run a one-quarter Monte Carlo simulation."""
    graph = load_graph(path)
    rng = np.random.default_rng(seed)

    node_ids = [n["id"] for n in graph["nodes"]]
    summaries = {nid: [] for nid in node_ids}
    n12_vals = []

    # find parameters for special edges
    noisy_edge = next(e for e in graph["edges"] if e["function"] == "noisy_or")
    gate_edge = next(e for e in graph["edges"] if e["function"] == "gate_min")

    for _ in range(runs):
        values: Dict[str, float] = {}
        for node in graph["nodes"]:
            prior = node.get("prior")
            if prior:
                values[node["id"]] = stats.sample(prior, rng)
        n5 = values.get("N5", 0.0)
        n9 = values.get("N9", 0.0)
        p = noisy_or([n5, n9], noisy_edge["params"]["p_leak"])
        n11 = values.get(gate_edge["source"], 1.0)
        risk_mult = gate_edge["params"].get("risk_multiplier", 1.0)
        p = min(p, p * risk_mult * n11)
        n12_vals.append(p)
        for nid in values:
            summaries[nid].append(values[nid])

    summary = {
        "seed": seed,
        "runs": runs,
        "P(N12)": float(np.mean(n12_vals)),
        "nodes": {
            nid: {"mean": float(np.mean(vals))} for nid, vals in summaries.items()
        },
    }

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("runs") / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary
