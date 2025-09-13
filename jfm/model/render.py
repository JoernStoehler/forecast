"""Graph rendering utilities."""

from __future__ import annotations

from pathlib import Path

from graphviz import Digraph

from ..io.loader import load_graph


def render(path: str | Path, out_path: str | Path) -> None:
    graph = load_graph(path)
    dot = Digraph()
    for node in graph["nodes"]:
        dot.node(node["id"], node.get("name", node["id"]))
    for edge in graph["edges"]:
        sources = edge.get("sources") or [edge.get("source")]
        for src in sources:
            dot.edge(src, edge["target"], label=edge["function"])
    dot.render(out_path, format="svg", cleanup=True)
