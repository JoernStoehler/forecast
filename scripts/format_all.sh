#!/usr/bin/env bash
set -euo pipefail

echo "[format] Python (ruff format + check)…"
if command -v ruff >/dev/null 2>&1; then
  ruff format .
  ruff check --fix .
else
  echo "ruff not installed; skip"
fi

echo "[format] Frontend (prettier)…"
if [ -f frontend/package.json ]; then
  if command -v pnpm >/dev/null 2>&1; then
    pnpm --dir frontend format || true
  else
    npx --yes prettier --write "frontend/**/*.{ts,tsx,js,jsx,json,css,md}" || true
  fi
fi

echo "[format] Done"
