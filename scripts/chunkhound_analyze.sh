#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_PATH="$ROOT_DIR/.chunkhound.json"
DB_PATH="$ROOT_DIR/.chunkhound/db"

cd "$ROOT_DIR"

if ! command -v chunkhound >/dev/null 2>&1; then
  echo "chunkhound is not installed or not on PATH" >&2
  exit 127
fi

CMD=(chunkhound index "$ROOT_DIR" --config "$CONFIG_PATH" --db "$DB_PATH")
CMD+=(--config-file-size-threshold-kb 10)
CMD+=("$@")

"${CMD[@]}"
