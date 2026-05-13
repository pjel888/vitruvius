#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

if ! command -v uvx >/dev/null 2>&1; then
  echo "uvx is not installed or not on PATH" >&2
  exit 127
fi

uvx --isolated --with tree-sitter-yaml code-review-graph build --repo . "$@"
