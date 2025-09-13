# JFM

Joern's Forecasting Model (JFM) is a minimal forecasting engine driven by a
causal graph defined in YAML. The project exposes a small CLI for validating
and simulating the sample graph.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
```

System Graphviz is required for the `render` command.

## CLI

All commands operate on the sample graph in `model/current.yaml`.

```bash
python -m jfm.cli validate model/current.yaml
python -m jfm.cli simulate model/current.yaml
python -m jfm.cli render model/current.yaml
```

Simulation outputs are written under `runs/<timestamp>/`.

## Contributing

Run `pre-commit run --files <files>` and `pytest` before committing.
