# Environments Guide (Local, Codespaces, Codex Cloud)

This repo ships three small, opinionated dev environments. Each mirrors the same lifecycle names (post-create, post-start), even if the hosting platform uses different terms.

Goals
- Keep developers productive with a single golden path per environment
- Avoid fragile scripting; never fail container creation/start due to workspace issues
- Minimize surprises across environments

What we explicitly avoid
- Telemetry, CLI aliases, auto-editing config files
- Multiple AI CLIs (we only support codex-cli)
- Heavy auto-setup; scripts are best-effort and idempotent

## Local DevContainer
- Path: `.devcontainer/local/`
- Image: `mcr.microsoft.com/devcontainers/universal:2` (Node.js 20 preinstalled)
- Secrets: local `.env` (optional). Never commit `.env`.
- Volumes: persisted for `~/.config/gh`, `~/.codex`, `~/.npm`, and shell history
- Lifecycle:
  - `post-create.sh`: ensures PATH; enables pnpm via corepack; installs uv and codex-cli; configures git hooks
  - `post-start.sh`: hydrates deps (uv for Python, pnpm for frontend)
- VS Code extensions: Python, Pylance, Jupyter, Ruff, ESLint, Prettier

## GitHub Codespaces
- Path: `.devcontainer/codespace/`
- Image: Universal (pre-cached). The `devcontainer.json` leaves the image commented, which selects the prebuilt Universal image in Codespaces.
- Secrets: injected as env vars from GitHub Secrets; no `.env`
- Lifecycle:
  - `post-create.sh`: ensures PATH; enables pnpm via corepack; installs uv and codex-cli
  - `post-start.sh`: hydrates deps (uv for Python, pnpm for frontend)
- VS Code extensions: Python, Pylance, Jupyter, Ruff, ESLint, Prettier

## Codex Cloud
- Path: `.devcontainer/codex/`
- No devcontainer.json; use the Codex Cloud UI
  - Setup script → `.devcontainer/codex/post-create.sh`
  - Maintenance script → `.devcontainer/codex/post-start.sh`
- Secrets: injected via the Cloud UI; no `.env`
- Behavior:
  - Setup: installs uv and codex-cli; appends PATH export to `~/.bashrc`
  - Start: ensures PATH; hydrates Python and frontend deps if config files are present

## Golden Commands
- Python: `uv sync` or `uv pip install -r requirements.txt`
- Tests: `pytest`
- Lint: `ruff check .`
- Type-check: `pyright`
- Frontend: `pnpm -C frontend install` then `pnpm -C frontend dev`
- Codex CLI: `codex --help` (installed globally via npm)

## Constraints and Practices
- Scripts never use `set -e` or `pipefail`; they log and continue
- We do not rely on volumes in Codespaces or Codex Cloud
- PATH is appended to `~/.bashrc` once on create; start scripts ensure PATH in non-interactive shells
- Python 3.12 and Node 20 across environments

## Picking an Environment
- Local: maximum performance and persistent caches
- Codespaces: hosted VS Code with GitHub-managed secrets
- Codex Cloud: headless agent-only environment

## Git Hooks
- Hooks live in `.githooks/` and are auto-configured via `core.hooksPath` during container creation.
- `pre-commit`: ruff format check + ruff lint + frontend eslint (pnpm).
- `pre-push`: pyright + pytest + frontend type-check and tests.
- Skip with `git commit --no-verify` or env `SKIP_HOOKS=1`.
