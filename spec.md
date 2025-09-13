Joern's Forecasting Model (JFM) — MVP Specification v0.1
=======================================================

**Owner:** Joern Stoehler  
**Repository:** JoernStoehler/forecast  
**Date:** 2025-09-13

**Goal:** Deliver a Python package and CLI that loads a causal graph from YAML, runs a one-quarter Monte-Carlo simulation, saves results, and is straightforward for new contributors.

---

## 1. MVP Deliverables

- `jfm` Python package with a Typer-based CLI exposing commands:
  - `validate model/current.yaml` – schema validation.
  - `simulate model/current.yaml` – one-quarter Monte-Carlo estimating `P(N12: Loss_of_Control_Event)` and node summaries.
  - `sensitivity model/current.yaml` – one-at-a-time ±1σ sensitivity for top-level outcomes.
  - `render model/current.yaml` – write DAG image (SVG/PNG).
- Outputs stored under `runs/<timestamp>/` as JSON/CSV plus rendered graph.
- Minimal test suite covering loader, validator, edge functions, and one integration test.
- README enabling a new contributor to run all commands in <10 minutes.

Out of scope: multi-quarter dynamics, Sobol indices, notebooks, web UI.

---

## 2. Repository Layout

```
jfm/
  __init__.py
  cli.py               # Typer entrypoint for `jfm` CLI
  io/
    loader.py          # YAML load + normalization
    schema.py          # JSON Schema validation
  model/
    types.py           # Pydantic models
    edges.py           # edge functions
    engine.py          # one-quarter evaluator + MC sampler
    sensitivity.py     # one-at-a-time sensitivity
    render.py          # graphviz rendering
  util/
    stats.py           # distributions, RNG helpers
    log.py             # structured logging
model/
  current.yaml         # sample graph
  schemas/
    graph.schema.json
    evidence.schema.yaml
forecasts/
  ledger.csv           # headers only
runs/                  # gitignored output directory
refs/
  README.md
scripts/               # optional helper scripts
tests/
  test_loader.py
  test_edges.py
  test_engine_integration.py
README.md
CHANGELOG.md
pyproject.toml         # pinned deps & tooling
.pre-commit-config.yaml
LICENSE
```

---

## 3. Dependencies & Tooling

- Python 3.11.x
- `pydantic>=2,<3`
- `jsonschema>=4,<5`
- `pyyaml>=6,<7`
- `numpy>=1.26,<3`
- `scipy>=1.13,<2`
- `typer>=0.12,<0.13`
- `graphviz>=0.20,<0.21` (requires system Graphviz)
- `pytest>=8,<9`
- Dev: `ruff` and `black` via `pre-commit`
- Use `python -m venv .venv` and `pip install -e .` for local setup.
- CI: GitHub Actions on Python 3.11 running lint, tests, and `jfm simulate model/current.yaml`.

---

## 4. Data Model

YAML input is validated against `model/schemas/graph.schema.json`. Nodes capture priors and metadata; edges define functional relationships; justifications document assumptions. `forecasts/ledger.csv` tracks forecast questions with columns:

`qid,question,open_date,close_date,p,resolution_rule,primary_sources,top_drivers,rationale_stub,last_updated`

---

## 5. Sample Graph (`model/current.yaml`)

```
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
```

---

## 6. Testing

- Loader and schema validation raise clear errors for invalid files; valid files pass.
- Edge functions include property tests (e.g., logistic output increases with input; `gate_min` never increases risk).
- Integration test confirms `jfm simulate model/current.yaml` returns a probability in [0,1] and writes `summary.json`.
- Run tests with `pytest`.

---

## 7. README Requirements

- Setup using `python -m venv .venv` and `pip install -e .`.
- Note system Graphviz dependency.
- Examples for `validate`, `simulate`, `sensitivity`, and `render` commands.
- Explain output files under `runs/<timestamp>/`.
- Contribution guidelines: run `pre-commit run --files <files>` and `pytest` before committing.

---

## 8. License & Notice

- License: MIT (unless owner specifies otherwise).
- Notice: repository models high-level risk pathways only and must not include operational misuse instructions.

---

## 9. Backlog (post-MVP)

- Multi-quarter dynamics with lagged feedback.
- Global sensitivity (Sobol) via SALib.
- Jupyter notebooks for exploratory runs.
- Evidence card ingestion and parameter update rules.
- Forecast ledger operations (open/close questions, scoring).
- Static site docs via MkDocs.

---

## 10. Delivery Checklist

- [ ] `jfm` CLI with `validate`, `simulate`, `sensitivity`, `render` commands works on `model/current.yaml`.
- [ ] `runs/<timestamp>/summary.json` contains seed, runs, `P(N12)`, and node summaries.
- [ ] `runs/<timestamp>/graph.svg` renders without errors.
- [ ] `pytest` tests pass in CI on Python 3.11.
- [ ] `README` demonstrates end-to-end run.
