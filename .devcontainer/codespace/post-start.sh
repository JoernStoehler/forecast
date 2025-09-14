#!/usr/bin/env bash
set -u
say() { echo "[codespace post-start] $*"; }

WORKSPACE="${WORKSPACE:-/workspaces/forecast}"

# Ensure PATH for this non-interactive shell
export PATH="$HOME/.local/bin:${PATH}"

# Python deps via uv if config present
if [ -f "$WORKSPACE/pyproject.toml" ]; then
  uv sync || say "uv sync failed (non-fatal)"
elif [ -f "$WORKSPACE/requirements.txt" ]; then
  uv pip install -r "$WORKSPACE/requirements.txt" || say "uv pip install failed (non-fatal)"
fi

# Frontend deps if present
if [ -f "$WORKSPACE/frontend/package.json" ]; then
  pnpm -C "$WORKSPACE/frontend" install --frozen-lockfile || say "pnpm install failed (non-fatal)"
fi

say "Done"
