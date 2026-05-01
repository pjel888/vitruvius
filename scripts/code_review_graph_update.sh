#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

if ! command -v uvx >/dev/null 2>&1; then
  echo "uvx is not installed or not on PATH" >&2
  exit 127
fi

if command -v powershell.exe >/dev/null 2>&1 && [[ $# -eq 0 ]]; then
  ROOT_DIR_WIN="$(cygpath -w "$ROOT_DIR" 2>/dev/null || printf '%s' "$ROOT_DIR")"
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "Set-Location -LiteralPath '$ROOT_DIR_WIN'; uvx --with tree-sitter-yaml code-review-graph build --repo ."
  exit $?
fi

uvx --with tree-sitter-yaml code-review-graph build --repo . "$@"
