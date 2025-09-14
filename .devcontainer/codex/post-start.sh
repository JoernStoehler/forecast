#!/usr/bin/env bash
# Codex Cloud: maintenance script (runs on every start). Idempotent.
set -u
say() { echo "[cloud start] $*"; }

WORKSPACE="$(pwd)"

# Ensure PATH for this non-interactive shell
export PATH="$HOME/.local/bin:${PATH}"

# Python deps via uv if config present
if command -v uv >/dev/null 2>&1; then
  if [ -f "$WORKSPACE/pyproject.toml" ]; then
    uv sync || say "uv sync failed (non-fatal)"
  elif [ -f "$WORKSPACE/requirements.txt" ]; then
    uv pip install -r "$WORKSPACE/requirements.txt" || say "uv pip install failed (non-fatal)"
  fi
fi

# Frontend deps if present (prefer pnpm)
if [ -f "$WORKSPACE/frontend/package.json" ]; then
  if command -v pnpm >/dev/null 2>&1; then
    pnpm -C "$WORKSPACE/frontend" install --frozen-lockfile || say "pnpm install failed (non-fatal)"
  elif command -v npm >/dev/null 2>&1; then
    npm ci --prefix "$WORKSPACE/frontend" || say "npm ci failed (non-fatal)"
  fi
fi

say "Maintenance done"
