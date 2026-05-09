#!/usr/bin/env bash
set -euo pipefail

cd /c/Users/phili/Desktop/vitruvius
source /c/Users/phili/Desktop/vitruvius/.venv/Scripts/activate

REL_LEDGER="006_System-Manifests/aec-mepfs-backbone/semantic-overlays/aec_backbone_all_nodes_bounded_001-ledger.jsonl"
NODE_LEDGER="006_System-Manifests/aec-mepfs-backbone/semantic-overlays/aec_backbone_all_nodes_bounded_001-node-consolidation-ledger.jsonl"

if [[ ! -f "$REL_LEDGER" ]]; then
  echo "Missing relationship campaign ledger: $REL_LEDGER" >&2
  exit 2
fi

if [[ ! -f "$NODE_LEDGER" ]]; then
  echo "Missing node-consolidation campaign ledger: $NODE_LEDGER" >&2
  exit 2
fi

export DEEPSEEK_API_KEY="$(
  powershell.exe -NoProfile -Command "[Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY','User')" |
    tr -d '\r'
)"

RUN_ID="${RUN_ID:-aec_backbone_all_nodes_bounded_004}"

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id "$RUN_ID" \
  --council-mode deepseek_local \
  --allow-cloud-ai \
  --cloud-preflight \
  --all-nodes \
  --max-pairs 50000 \
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
  --node-max-pairs 20000 \
  --node-candidate-top-k 10 \
  --global-ledger-path "$REL_LEDGER" \
  --node-consolidation-ledger-path "$NODE_LEDGER" \
  --cloud-cost-budget-usd 35.00 \
  --deepseek-flash-max-calls 50000 \
  --deepseek-pro-max-calls 800 \
  --cloud-total-max-calls 51000 \
  --fallback-to-local-on-cloud-exhaustion \
  --fallback-to-local-on-cloud-error \
  --fallback-to-local-on-rate-limit \
  --progress-mode plain \
  --sleep-seconds 2 \
  --deepseek-sleep-seconds 1
