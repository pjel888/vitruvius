#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${1:-.}"

echo "Initializing Vitruvius structure at: $ROOT"

top_dirs=(
  "001_Raw-Source-Layer"
  "002_Raw-Conversion-Layer"
  "003_Canonical-Knowledge-Layer"
  "004_Derived-Content-Layer"
  "005_Operational-Intelligence-Layer"
  "006_System-Manifests"
  "config"
  "docs"
  "scripts"
)

categories=(
  "001-Laws"
  "002-History"
  "003-Theory"
  "004-Technology"
  "005-Utilities"
  "006-Structural"
  "007-Planning"
  "008-Design"
  "009-Practice"
)

for dir in "${top_dirs[@]}"; do
  mkdir -p "$ROOT/$dir"
done

# 001 Raw Source Layer
for category in "${categories[@]}"; do
  mkdir -p "$ROOT/001_Raw-Source-Layer/$category"
done

# 002 Raw Conversion Layer
for category in "${categories[@]}"; do
  mkdir -p "$ROOT/002_Raw-Conversion-Layer/$category/raw_markdown"
  mkdir -p "$ROOT/002_Raw-Conversion-Layer/$category/sidecar_json"
  mkdir -p "$ROOT/002_Raw-Conversion-Layer/$category/assets"
  mkdir -p "$ROOT/002_Raw-Conversion-Layer/$category/failed"
  mkdir -p "$ROOT/002_Raw-Conversion-Layer/$category/logs"
done

# 003 Canonical Knowledge Layer
for category in "${categories[@]}"; do
  mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/$category/topics"
  mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/$category/concepts"
  mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/$category/glossary"
  mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/$category/indexes"
  mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/$category/logs"
  mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/$category/sources"

  if [ ! -f "$ROOT/003_Canonical-Knowledge-Layer/$category/index.md" ]; then
    cat > "$ROOT/003_Canonical-Knowledge-Layer/$category/index.md" <<EOF
# ${category#*-}

## Scope

## Index

## Notes
EOF
  fi

  if [ ! -f "$ROOT/003_Canonical-Knowledge-Layer/$category/log.md" ]; then
    cat > "$ROOT/003_Canonical-Knowledge-Layer/$category/log.md" <<EOF
# ${category#*-} Change Log

EOF
  fi
done

mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/shared/glossary"
mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/shared/concepts"
mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/shared/relationships"
mkdir -p "$ROOT/003_Canonical-Knowledge-Layer/shared/templates"

if [ ! -f "$ROOT/003_Canonical-Knowledge-Layer/shared/index.md" ]; then
  cat > "$ROOT/003_Canonical-Knowledge-Layer/shared/index.md" <<'EOF'
# Shared Knowledge

## Cross-domain concepts

## Global glossary

## Cross references
EOF
fi

# 004 Derived Content Layer
derived_sections=(
  "articles"
  "questions"
  "flashcards"
  "learning-paths"
  "summaries"
  "explainers"
  "drafts"
  "exports"
)

for section in "${derived_sections[@]}"; do
  mkdir -p "$ROOT/004_Derived-Content-Layer/$section"
done

for category in "${categories[@]}"; do
  mkdir -p "$ROOT/004_Derived-Content-Layer/articles/$category"
  mkdir -p "$ROOT/004_Derived-Content-Layer/questions/$category"
  mkdir -p "$ROOT/004_Derived-Content-Layer/flashcards/$category"
  mkdir -p "$ROOT/004_Derived-Content-Layer/learning-paths/$category"
  mkdir -p "$ROOT/004_Derived-Content-Layer/summaries/$category"
  mkdir -p "$ROOT/004_Derived-Content-Layer/explainers/$category"
done

# 005 Operational Intelligence Layer
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/chunks"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/embeddings"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/graph/nodes"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/graph/edges"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/graph/exports"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/graph/snapshots"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/indexes/bm25"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/indexes/vector"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/indexes/hybrid"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/cache"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/retrieval"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/models"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/pipelines/ingest"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/pipelines/canonicalize"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/pipelines/derive"
mkdir -p "$ROOT/005_Operational-Intelligence-Layer/pipelines/graph-build"

# 006 System Manifests
manifest_dirs=(
  "tree-snapshots"
  "checksums"
  "conversions"
  "duplicates"
  "lineage"
  "registries"
  "runs"
  "logs"
)

for dir in "${manifest_dirs[@]}"; do
  mkdir -p "$ROOT/006_System-Manifests/$dir"
  touch "$ROOT/006_System-Manifests/$dir/.gitkeep"
done

if [ ! -f "$ROOT/006_System-Manifests/registries/source_registry.csv" ]; then
  cat > "$ROOT/006_System-Manifests/registries/source_registry.csv" <<'EOF'
source_id,category,raw_path,file_name,sha256,status,last_seen_utc
EOF
fi

if [ ! -f "$ROOT/006_System-Manifests/registries/conversion_registry.csv" ]; then
  cat > "$ROOT/006_System-Manifests/registries/conversion_registry.csv" <<'EOF'
source_id,raw_path,markdown_path,json_path,parser,ocr_used,status,converted_at_utc
EOF
fi

if [ ! -f "$ROOT/006_System-Manifests/registries/canonical_registry.csv" ]; then
  cat > "$ROOT/006_System-Manifests/registries/canonical_registry.csv" <<'EOF'
canonical_id,category,title,canonical_path,status,last_updated_utc
EOF
fi

if [ ! -f "$ROOT/006_System-Manifests/registries/graph_registry.csv" ]; then
  cat > "$ROOT/006_System-Manifests/registries/graph_registry.csv" <<'EOF'
entity_id,entity_type,source_ref,status,last_updated_utc
EOF
fi

# Config
if [ ! -f "$ROOT/config/vitruvius.yaml" ]; then
  cat > "$ROOT/config/vitruvius.yaml" <<'EOF'
project_name: Vitruvius
version: 0.1.0

categories:
  - 001-Laws
  - 002-History
  - 003-Theory
  - 004-Technology
  - 005-Utilities
  - 006-Structural
  - 007-Planning
  - 008-Design
  - 009-Practice

paths:
  raw: 001_Raw-Source-Layer
  conversion: 002_Raw-Conversion-Layer
  canonical: 003_Canonical-Knowledge-Layer
  derived: 004_Derived-Content-Layer
  ops: 005_Operational-Intelligence-Layer
  manifests: 006_System-Manifests
EOF
fi

# Docs
if [ ! -f "$ROOT/docs/CONTENT_RULES.md" ]; then
  cat > "$ROOT/docs/CONTENT_RULES.md" <<'EOF'
# Vitruvius Content Rules

1. Raw source files are evidence, not truth.
2. Raw conversion files are machine-readable extraction, not editorial knowledge.
3. Canonical knowledge files are the trusted knowledge layer.
4. Derived content must point back to canonical knowledge.
5. Canonical knowledge should preserve source references and update history.
EOF
fi

if [ ! -f "$ROOT/docs/CANONICAL_FRONTMATTER_TEMPLATE.md" ]; then
  cat > "$ROOT/docs/CANONICAL_FRONTMATTER_TEMPLATE.md" <<'EOF'
---
id: ""
title: ""
category: ""
subtopic: ""
status: draft
source_refs: []
related_topics: []
last_updated: ""
---

# Title

## Overview

## Main Content

## Related Topics
EOF
fi

touch "$ROOT/scripts/.gitkeep"

echo "Vitruvius structure created successfully."