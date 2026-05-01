#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

echo "== GitNexus =="
"$ROOT_DIR/scripts/gitnexus_analyze.sh"

echo
echo "== ChunkHound =="
"$ROOT_DIR/scripts/chunkhound_analyze.sh"

echo
echo "== code-review-graph =="
"$ROOT_DIR/scripts/code_review_graph_update.sh"
