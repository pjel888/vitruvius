#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GITNEXUS_VERSION="${GITNEXUS_VERSION:-1.6.2-rc.10}"
PRESERVED_SKILLS_DIR="$ROOT_DIR/.ai/skills/gitnexus"
BACKUP_DIR=""

restore_preserved_skills() {
  if [[ -z "$BACKUP_DIR" ]]; then
    return
  fi
  while IFS= read -r -d '' file; do
    rel_path="${file#$BACKUP_DIR/}"
    cp "$file" "$ROOT_DIR/$rel_path"
  done < <(find "$BACKUP_DIR" -type f -print0)
}

EMBEDDINGS_FLAG=()
if [[ -f "$ROOT_DIR/.gitnexus/meta.json" ]]; then
  EMBEDDINGS_COUNT="$(
    python3 - <<'PY' "$ROOT_DIR/.gitnexus/meta.json"
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
try:
    data = json.loads(path.read_text(encoding='utf-8'))
    print(int(data.get('stats', {}).get('embeddings', 0)))
except Exception:
    print(0)
PY
  )"
  if [[ "${EMBEDDINGS_COUNT}" =~ ^[0-9]+$ ]] && (( EMBEDDINGS_COUNT > 0 )); then
    EMBEDDINGS_FLAG+=(--embeddings)
  fi
fi

cd "$ROOT_DIR"
if [[ -d "$PRESERVED_SKILLS_DIR" ]]; then
  BACKUP_DIR="$(mktemp -d)"
  while IFS= read -r -d '' file; do
    rel_path="${file#$ROOT_DIR/}"
    mkdir -p "$BACKUP_DIR/$(dirname "$rel_path")"
    cp "$file" "$BACKUP_DIR/$rel_path"
  done < <(find "$PRESERVED_SKILLS_DIR" -type f -name '*.md' -print0)
fi

CMD=(npx --yes "gitnexus@${GITNEXUS_VERSION}" analyze --skip-agents-md)
if (( ${#EMBEDDINGS_FLAG[@]} > 0 )); then
  CMD+=("${EMBEDDINGS_FLAG[@]}")
fi
CMD+=("$@")
set +e
"${CMD[@]}"
STATUS=$?
set -e

if [[ -n "$BACKUP_DIR" ]]; then
  restore_preserved_skills
  for _ in 1 2 3 4 5; do
    sleep 0.2
    restore_preserved_skills
  done
  rm -rf "$BACKUP_DIR"
fi

exit "$STATUS"
