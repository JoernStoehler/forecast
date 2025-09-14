# Joern's Forecasting Model

This repository contains notes on, and computational implementations of, a simplified version of Joern's forecasting model.
The model is highly opinionated, and the focus is less on explaining its origin, in particular the historically considered but ultimately rejected hypotheses, or low-probability marginals, but more on formalizing forecasts of the highest impact features Joern can provide a formal prior and likelihood for.

## Development Milestones

Current Version in development: 0.1

Version 0.1 - Planned the project goal and initial roadmap. Set up the repository structure.
Version 0.2 - Gathered notes on the high-level modular structure of the model, i.e. breakdown into domains and reusable components.
Version 0.3 - Gathered notes on latent and observed variables and their interdependencies, with a focus on capturing the most impactful correlations.
Version 0.4 - Implemented a manual algorithm utilizing natural language reasoning to sample from the model.
Version 0.5 - Implemented a probabilistic programming algorithm to sample from the model.
Version 1.0 - Implemented a user-friendly interface for conditioning on observations, causally intervening on policies, and communicating posterior distributions or samples thereof.

Version 1.1 - Developed a gamified interface for engagement with the model, with a focus on AI x-risk policy decisions.
Version 1.2 - Released and advertised the gamified interface to relevant communities for engagement and feedback.

Version 1.3 - Post-release analysis of engagement data and feedback to identify areas for improvement.

## Tech Stack

- Markdown for documentation and notes
- ChatGPT Codex (CLI, IDE, Cloud) for AI assistance in documentation, coding, research, and project management
- Backend
  - Python for computational implementations (accessible to a wide audience)
  - FastAPI, Pydantic for 0.5, 1.0, 1.1 backends
  - Pytest for testing
- Frontend
  - TypeScript with React for user interfaces (1.0, 1.1)
  - Vite, Vitest, Storybook, Eslint, Prettier for development environment
  - TailwindCSS for styling
  - D3.js for data visualization
  - Cloudflare for data storage and hosting

## Project Structure

Here is an incomplete, concise overview of the project folders and files:

- `docs/`:
  - `project/`: Notes on development milestones and project management.
  - `conventions/`: Documentation of workflow, coding, and documentation best practices.
  - `research/`: Notes on the model's structure, variables, and interdependencies.
  - `user/`: Documentation for end-users, including installation instructions, usage examples, and API references.
- `jfm/`: Probabilistic programming backend, versions 0.5 and 1.0.
  - `pyproject.toml`
  - `src/jfm/`
  - `tests/`
- `frontend/`: Source code for the user interface.
  - `package.json`
  - `vite.config.ts`
  - `src/`
  - `tests/`
- `scripts/`: Utility scripts for developers and maintainers.
- `.devcontainer/`: Configuration for our development environments.
  - `codespace/`: GitHub Codespaces configuration.
  - `local/`: Local development container configuration.
  - `codex/`: Codex Cloud configuration.
- `.gitignore`
- `.github/`
  - `workflows/`: GitHub Actions workflows for CI/CD.
  - `ISSUE_TEMPLATE/`: Templates for reporting issues and feature requests.
  - `PULL_REQUEST_TEMPLATE.md`: Template for pull requests.
- `README.md`: GitHub README file.
- `AGENTS.md`: Onboarding for AI agents contributing to the project.
- `LICENSE`
- `CHANGELOG.md`: Semantic versioning changelog.

## Contribution Guidelines

- AI agents can submit pull requests, which will be automatically reviewed by another AI agent, and by the human project owner Joern.
