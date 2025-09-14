#!/usr/bin/env bash
# Codex Cloud: setup script (runs once for new container). Keep resilient.
set -u
say() { echo "[cloud setup] $*"; }

WORKSPACE="$(pwd)"

# Ensure ~/.local/bin on PATH for interactive shells
if ! grep -Fq "~/.local/bin" "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

# Install uv for Python toolchain (best effort)
if command -v curl >/dev/null 2>&1; then
  curl -fsSL https://astral.sh/uv/install.sh | sh || true
fi

# Enable pnpm via corepack if available
if command -v corepack >/dev/null 2>&1; then
  corepack enable || true
  corepack prepare pnpm@latest --activate || true
fi

# Install codex-cli if npm available
if command -v npm >/dev/null 2>&1; then
  npm i -g @openai/codex || true
fi

git config --global --add safe.directory "$WORKSPACE" >/dev/null 2>&1 || true
git -C "$WORKSPACE" config core.hooksPath .githooks >/dev/null 2>&1 || true
say "Setup done. Maintenance will hydrate deps."
