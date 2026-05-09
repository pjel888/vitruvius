#!/usr/bin/env bash
set -euo pipefail

cd /c/Users/phili/Desktop/vitruvius
source /c/Users/phili/Desktop/vitruvius/.venv/Scripts/activate

REFRESH_SECONDS="${REFRESH_SECONDS:-5}"

if [[ -n "${RUN_ID:-}" ]]; then
  PYTHONPATH=scripts python scripts/pipeline_cli.py aec-watch-relationship-run \
    --run-id "$RUN_ID" \
    --progress-mode plain \
    --refresh-seconds "$REFRESH_SECONDS"
else
  PYTHONPATH=scripts python scripts/pipeline_cli.py aec-watch-relationship-run \
    --watch-latest \
    --progress-mode plain \
    --refresh-seconds "$REFRESH_SECONDS"
fi
