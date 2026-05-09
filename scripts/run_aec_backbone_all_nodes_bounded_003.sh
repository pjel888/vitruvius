#!/usr/bin/env bash
set -euo pipefail

cd /c/Users/phili/Desktop/vitruvius
source /c/Users/phili/Desktop/vitruvius/.venv/Scripts/activate

export DEEPSEEK_API_KEY="$(
  powershell.exe -NoProfile -Command "[Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY','User')" |
    tr -d '\r'
)"

RUN_ID="${RUN_ID:-aec_backbone_all_nodes_bounded_003}"

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id "$RUN_ID" \
  --council-mode deepseek_local \
  --allow-cloud-ai \
  --cloud-preflight \
  --all-nodes \
  --max-pairs 20000 \
  --candidate-top-k 20 \
  --min-similarity 0.35 \
  --accept-threshold 0.85 \
  --verify-threshold 0.65 \
  --verify-uncertain \
  --adjudicate-disagreements \
  --high-impact-pro-adjudication \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --improve-nodes \
  --node-max-pairs 8000 \
  --node-candidate-top-k 10 \
  --global-ledger-path 006_System-Manifests/aec-mepfs-backbone/semantic-overlays/aec_backbone_all_nodes_bounded_001-ledger.jsonl \
  --node-consolidation-ledger-path 006_System-Manifests/aec-mepfs-backbone/semantic-overlays/aec_backbone_all_nodes_bounded_001-node-consolidation-ledger.jsonl \
  --cloud-cost-budget-usd 15.00 \
  --deepseek-flash-max-calls 32000 \
  --deepseek-pro-max-calls 300 \
  --cloud-total-max-calls 32500 \
  --fallback-to-local-on-cloud-exhaustion \
  --fallback-to-local-on-cloud-error \
  --fallback-to-local-on-rate-limit \
  --progress-mode plain \
  --sleep-seconds 2 \
  --deepseek-sleep-seconds 1
