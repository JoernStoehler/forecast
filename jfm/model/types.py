"""Pydantic models for nodes and edges."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel


class Prior(BaseModel):
    dist: str
    a: Optional[float] = None
    b: Optional[float] = None
    mu: Optional[float] = None
    sigma: Optional[float] = None


class Node(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[str] = None
    prior: Optional[Prior] = None


class Edge(BaseModel):
    source: Optional[str] = None
    sources: Optional[List[str]] = None
    target: str
    function: str
    params: Dict[str, float] = {}
