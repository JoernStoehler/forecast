#!/usr/bin/env bash
set -u
say() { echo "[codespace post-create] $*"; }

WORKSPACE="${WORKSPACE:-/workspaces/forecast}"

# Ensure ~/.local/bin on PATH for uv and other tools
if ! grep -Fq "~/.local/bin" "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

# Universal image includes Node.js 20. Enable corepack/pnpm.
corepack enable || true
corepack prepare pnpm@latest --activate || true

# Install uv (Python toolchain)
curl -fsSL https://astral.sh/uv/install.sh | sh || true

# Install codex-cli globally
npm i -g @openai/codex || true

git config --global --add safe.directory "$WORKSPACE" >/dev/null 2>&1 || true
git -C "$WORKSPACE" config core.hooksPath .githooks >/dev/null 2>&1 || true
say "Ready"
