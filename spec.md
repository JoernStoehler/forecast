Joern's Forecasting Model (JFM) — Repository Specification (MVP v0.1)

Owner: Joern Stoehler
Proposed repo: JoernStoehler/forecast
Date: 2025-09-13

Purpose: Hand this document to a developer. They return a working GitHub repo that loads a minimal causal graph, runs a one‑quarter Monte‑Carlo, exports a few artifacts, and is pleasant to iterate on. Keep the scope tight.


---

0) MVP Goals (what must exist after Day 1)

1. A Python repo that:

Parses model/current.yaml (graph + priors) and validates it against a schema.

Runs one-quarter Monte‑Carlo (no time dynamics yet) to estimate P(N12: Loss_of_Control_Event) and a few node summaries.

Computes one‑at‑a‑time sensitivity (±1σ) for top‑level outcome(s).

Renders the DAG to a PNG/SVG from the YAML.

Provides a single CLI jfm with validate, simulate, sensitivity, render subcommands.

Saves outputs under runs/<timestamp>/ (JSON/CSV + image).



2. A small test suite (pytest) covering: loader, validator, edge functions, and one integration test.


3. A minimal README that lets a contributor run everything in <10 minutes.



Out of scope for MVP: multi‑quarter dynamics, Sobol indices, notebooks, web UI. Add them later.


---

1) Repo Layout

jfm/                            # Python package
  __init__.py
  cli.py                        # click/typer entrypoint → `jfm` CLI
  io/
    loader.py                   # YAML load + normalization
    schema.py                   # JSON Schema + validation
  model/
    types.py                    # dataclasses / pydantic models
    edges.py                    # edge functions
    engine.py                   # one-quarter evaluator + MC sampler
    sensitivity.py              # one-at-a-time sensitivity
    render.py                   # graphviz rendering
  util/
    stats.py                    # distributions, RNG helpers
    log.py                      # structured logging

model/
  current.yaml                  # MVG-AXR-12 (provided below)
  schemas/
    graph.schema.json           # provided below
    evidence.schema.yaml        # provided below

forecasts/
  ledger.csv                    # header only (columns spec below)

runs/                           # gitignored; CLI writes outputs here

refs/                           # empty for MVP
  README.md

scripts/                        # optional helper scripts (empty OK)

tests/
  test_loader.py
  test_edges.py
  test_engine_integration.py

README.md
CHANGELOG.md
pyproject.toml                   # pinned deps & tooling
.pre-commit-config.yaml
LICENSE


---

2) Tooling & Environment

Python: 3.11.x

Dependencies (pin exact versions in pyproject.toml):

pydantic>=2,<3 (models/validation) or dataclasses + jsonschema (choose one approach; see below)

jsonschema>=4,<5 (YAML validation)

pyyaml>=6,<7

numpy>=1.26,<3 and scipy>=1.13,<2

click>=8,<9 or typer>=0.12,<0.13 (CLI)

graphviz>=0.20,<0.21 (Python bindings; require Graphviz system pkg)

pytest>=8,<9


Dev tools: ruff, black, pre-commit hook running both.

CI: GitHub Actions: Python 3.11 matrix, install, lint, test, and run jfm simulate on the sample to ensure repo is healthy.


Implementation choice: Prefer pydantic v2 for strong validation and helpful errors.


---

3) Data Model (MVP semantics)

3.1 Node Types

state ∈ [0,1] unless unit specified.

rate has units (e.g., incidents per 1000 deployments); prior typically lognormal.

event represented by a probability p ∈ [0,1] within the time window.

policy treated as state for math; semantic tag only.

resource may be unbounded positive; use lognormal prior.


3.2 Edge Functions (must implement)

All edge functions map source value(s) to a contribution that the target’s aggregator uses.

logistic: f(x; w, b) = sigmoid(w*x + b) where sigmoid(z)=1/(1+exp(-z)). Inputs assumed scaled to [0,1] unless the node’s unit dictates otherwise; developer should implement automatic scaling for [0,1] sources and unit‑aware passthrough otherwise.

inhibitory_logistic: same as logistic but intended for negative influence; w is typically negative and enforced by validation.

multiplicative (for rate targets): Given baseline v0 from the target’s prior and a source x, apply v = v0 * (1 + α*x); for multiple sources, multiply successive factors.

noisy_or (for event targets): With k inputs providing per‑path probabilities p_i, and a leak p_leak, p = 1 - (1 - p_leak) * Π_i (1 - p_i).

gate_max (policy gate on resource targets): With gate value g ∈ [0,1], compute a multiplier m = min_multiplier + (max_multiplier - min_multiplier)*(1 - g). Apply to the post‑prior value of the target (or to the upstream contribution as appropriate) so higher g reduces availability.

gate_min (risk‑reducer on event targets): With capacity c ∈ [0,1] and risk_multiplier ∈ (0,1], adjust event probability p ← p * (1 - (1 - risk_multiplier)*c).


3.3 Target Aggregators (MVP)

For state targets with logistic‑type inbound edges: sum contributions then clamp01. (Simple and transparent.)

For rate targets: apply chained multiplicative adjustments to the prior draw.

For event targets: use noisy_or across inbound event‑like contributions, then apply any gate_min effects.


> Note: This is deliberately simple for MVP. We can swap in better aggregators (e.g., softmax, 1−Π(1−s_i) for states) after first sensitivity pass.




---

4) Monte‑Carlo & Sensitivity (MVP)

Draws: Default 100,000 (configurable via CLI).

Sampling: Use numpy.random.Generator(PCG64); allow --seed for reproducibility.

Priors:

Beta(a,b) on [0,1].

LogNormal(mu, sigma) where parameters are for the log (natural log).

Normal(mu, sigma) as needed (clip or transform if mapping into [0,1]).


Evaluation: For each draw, sample node priors, propagate edges once (single quarter), compute p(N12).

Outputs:

summary.json: mean/median/std for all nodes; P(N12); seed and config hash.

samples_parquet (optional later) — skip for MVP; CSV is enough.


Sensitivity (OAT): Perturb each top‑level parameter (edge weights and key node priors) by ±1σ (or ±10% for parameters without σ), recompute P(N12), record delta.



---

5) CLI Spec

# Validate YAML against schema and basic semantics
jfm validate --config model/current.yaml

# Run one-quarter MC and write results under runs/<timestamp>/
jfm simulate --config model/current.yaml --runs 100000 --seed 42

# One-at-a-time sensitivity report (CSV)
jfm sensitivity --config model/current.yaml --runs 20000 --seed 43

# Render graph to SVG/PNG using Graphviz
jfm render --config model/current.yaml --out runs/<timestamp>/graph.svg

CLI returns non‑zero exit codes on validation or run failures.


---

6) Graph Rendering (minimal)

Use graphviz.Digraph.

Node label: name\n(type); color code by type (pastel palette, consistent; exact colors not critical).

Edge label: function (short) and key params.

Save as graph.svg and graph.png.



---

7) Schema Files (include in repo)

7.1 model/schemas/graph.schema.json

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "JFM Graph Schema",
  "type": "object",
  "required": ["meta", "nodes", "edges"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["id", "version", "timestep"],
      "properties": {
        "id": {"type": "string"},
        "version": {"type": "string"},
        "timestep": {"enum": ["quarter"]}
      }
    },
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type"],
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"},
          "type": {"enum": ["state", "rate", "event", "policy", "resource"]},
          "unit": {"type": "string"},
          "range": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
          "prior": {"type": "object"},
          "window": {"type": "string"}
        }
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["target", "function"],
        "properties": {
          "source": {"type": "string"},
          "sources": {"type": "array", "items": {"type": "string"}},
          "target": {"type": "string"},
          "function": {"enum": ["logistic", "inhibitory_logistic", "multiplicative", "noisy_or", "gate_max", "gate_min"]},
          "params": {"type": "object"},
          "justification": {"type": "string"}
        },
        "oneOf": [
          {"required": ["source"]},
          {"required": ["sources"]}
        ]
      }
    },
    "justifications": {"type": "object"}
  }
}

7.2 model/schemas/evidence.schema.yaml

$schema: "https://json-schema.org/draft/2020-12/schema"
title: JFM Evidence Card
 type: object
 required: [id, claim, direction, strength]
 properties:
  id: { type: string }
  claim: { type: string }
  direction: { enum: ["+", "-", "mixed"] }
  strength: { enum: [VeryLow, Low, Medium, High] }
  sources: { type: array, items: { type: string } }
  applicability: { type: string }
  update_rule: { type: string }
  adversarial_checks: { type: string }

7.3 forecasts/ledger.csv (columns only)

qid,question,open_date,close_date,p,resolution_rule,primary_sources,top_drivers,rationale_stub,last_updated


---

8) Sample Graph (model/current.yaml)

meta:
  id: MVG-AXR-12
  version: 0.1
  timestep: quarter
nodes:
  - {id: N1, name: Frontier_Capability_Level, type: state, range: [0,1], prior: {dist: Beta, a: 2, b: 3}}
  - {id: N2, name: Training_Compute_Available, type: resource, unit: H100eq, prior: {dist: LogNormal, mu: 10, sigma: 0.6}}
  - {id: N3, name: Algorithmic_Efficiency, type: state, prior: {dist: LogNormal, mu: 0, sigma: 0.4}}
  - {id: N4, name: Deployment_Intensity_HighStakes, type: state, range: [0,1], prior: {dist: Beta, a: 2, b: 2}}
  - {id: N5, name: Deceptive_Alignment_Prevalence, type: state, range: [0,1], prior: {dist: Beta, a: 1.5, b: 3}}
  - {id: N6, name: Eval_Efficacy, type: state, range: [0,1], prior: {dist: Beta, a: 2.5, b: 2.5}}
  - {id: N7, name: Governance_Stringency, type: policy, range: [0,1], prior: {dist: Beta, a: 1.8, b: 2.2}}
  - {id: N8, name: Org_Risk_Incentives, type: state, range: [0,1], prior: {dist: Beta, a: 2.5, b: 2}}
  - {id: N9, name: Incident_Rate_Severe, type: rate, unit: per_1000, prior: {dist: LogNormal, mu: -2, sigma: 0.8}}
  - {id: N10, name: Public_Opinion_Risk_Salience, type: state, range: [0,1], prior: {dist: Beta, a: 1.6, b: 2.4}}
  - {id: N11, name: Emergency_Response_Capacity, type: state, range: [0,1], prior: {dist: Beta, a: 2.2, b: 1.8}}
  - {id: N12, name: Loss_of_Control_Event, type: event, window: quarter}
edges:
  - {source: N2, target: N1, function: logistic, params: {w: 0.8, b: -1.0}, justification: J1}
  - {source: N3, target: N1, function: logistic, params: {w: 0.7, b: -0.6}, justification: J2}
  - {source: N7, target: N2, function: gate_max, params: {max_multiplier: 1.0, min_multiplier: 0.4}, justification: J3}
  - {source: N8, target: N4, function: logistic, params: {w: 1.0, b: -0.5}, justification: J4}
  - {source: N1, target: N4, function: logistic, params: {w: 0.6, b: -0.3}, justification: J4}
  - {source: N1, target: N9, function: multiplicative, params: {alpha: 0.02}, justification: J5}
  - {source: N4, target: N9, function: multiplicative, params: {alpha: 0.03}, justification: J5}
  - {source: N6, target: N5, function: inhibitory_logistic, params: {w: -1.2, b: 0.0}, justification: J6}
  - {source: N1, target: N5, function: logistic, params: {w: 0.9, b: -0.7}, justification: J7}
  - {sources: [N5, N9], target: N12, function: noisy_or, params: {p_leak: 0.005}, justification: J8}
  - {source: N10, target: N7, function: logistic, params: {w: 0.9, b: -0.7}, justification: J9}
  - {source: N9, target: N10, function: logistic, params: {w: 1.1, b: -1.0}, justification: J9}
  - {source: N11, target: N12, function: gate_min, params: {risk_multiplier: 0.3}, justification: J10}
justifications:
  J1: "Compute enables capability; governance can cap effective compute."
  J2: "Algorithmic efficiency gains substitute for compute growth."
  J3: "Policy can constrain access to top-tier hardware/runs."
  J4: "Risk incentives and capability drive high-stakes deployment."
  J5: "Higher capability/deployment → more severe incidents per unit time."
  J6: "Better evals reduce deceptive alignment prevalence detected before deployment."
  J7: "At higher capability, deception becomes easier/more instrumentally useful."
  J8: "Either prevalent deception or severe incidents can precipitate loss-of-control."
  J9: "Incidents move public salience, which drives governance stringency (lagged)."
  J10: "Emergency levers (audit, shutdown, rollback) reduce realized catastrophe."


---

9) Tests (minimum set)

Loader/Schema: invalid/missing fields raise clear errors; valid file passes.

Edge functions: property tests (e.g., higher x increases logistic output; gate_min never increases risk beyond baseline).

Engine integration: simulate on current.yaml returns a probability in [0,1] and writes summary.json.



---

10) README Requirements (short)

Setup (pyenv/uv/pip; Graphviz install note).

Commands (the four CLI examples above).

Where outputs go, and how to read summary.json.

Contributing: style (ruff+black), tests, PR checklist.



---

11) License & Credits

License: MIT (unless the owner specifies otherwise).

NOTICE: This repository models high‑level risk pathways only. It must not include operational instructions for misuse or harm.



---

12) Backlog (after MVP)

Multi‑quarter dynamics (DID, quarter‑lag feedback).

Global sensitivity (Sobol) via SALib.

Jupyter notebooks for exploratory runs.

Evidence card ingestion + parameter update rules.

Forecast ledger operations (open/close questions, scoring).

Simple static site docs via MkDocs.



---

13) Acceptance Checklist (what the developer delivers)

[ ] jfm CLI with validate | simulate | sensitivity | render commands working against model/current.yaml.

[ ] runs/<timestamp>/summary.json containing: seed, runs, P(N12), and basic node summaries.

[ ] runs/<timestamp>/graph.svg renders without errors.

[ ] Unit + integration tests pass in CI on Python 3.11.

[ ] README explains setup and one successful run end‑to‑end.


