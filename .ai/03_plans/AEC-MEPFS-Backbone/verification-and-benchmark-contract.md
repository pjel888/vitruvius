---
task: aec-mepfs-backbone
phase: readiness-verification-benchmark
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# Verification And Benchmark Contract

## Purpose

Define the verification commands and output artifacts required before and during
later bounded implementation.

These commands are specifications. They were not executed as part of this
readiness artifact unless separately recorded in validation.

Accepted-readiness scope: the command families, output report classes, and
quality thresholds are accepted as the verification contract skeleton. Runtime
implementation remains blocked until exact fixture paths, benchmark corpus,
hardware/runtime baseline, warmup/repetition policy, and percentile reporting
are recorded.

## Baseline Static Checks

```bash
git diff --check
rg -n "[ \t]$" .ai/03_plans/AEC-MEPFS-Backbone
```

## Focused Backend Tests

```bash
PYTHONPATH=scripts python3 -m pytest \
  scripts/tests/test_evidence_materializer.py \
  scripts/tests/test_kg_schemas.py \
  scripts/tests/test_kg_unified_snapshot_builder.py \
  scripts/tests/test_kg_serialization_contract.py \
  scripts/tests/test_kg_assertion_validator.py \
  scripts/tests/test_kg_quality_report.py \
  scripts/tests/test_kg_neo4j_loader.py \
  scripts/tests/test_vitruvian_context_resolver.py
```

## API / Explorer Tests

```bash
(cd api && bun test perspectiveContracts.test.ts)
(cd explorer && bun test src/utils/labels.test.ts src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts)
```

If test scripts differ at execution time, the execution packet must record the
actual package scripts and why they supersede these commands.

## Graph Smoke Checks

Later graph-backed validation must record:

```cypher
MATCH (n) RETURN count(n) AS nodes;
MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count ORDER BY count DESC;
MATCH (n:BackboneShadow) RETURN count(n) AS backbone_shadow_nodes;
```

S5 added a read-only preflight runner that records the current local graph
smoke evidence without mutating Neo4j:

```bash
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_rollback_preflight \
  --run-id <YYYYMMDDTHHMMSSZ> \
  --timeout-seconds 60
```

This command produces a preflight report only. It is not rollback proof until a
separate stopped or isolated database dump/load rehearsal is executed.

S6 added registry-candidate validation evidence:

```bash
PYTHONPATH=scripts python3 - <<'PY'
from pathlib import Path
from vitruvius.kg.backbone_contracts import validate_backbone_contract_file

for path in [
    Path(".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/predicate-registry.json"),
    Path(".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json"),
]:
    report = validate_backbone_contract_file(path).to_dict()
    assert report["ok"], report
PY
```

## Quality Thresholds

- no unregistered governed predicates
- zero vague governed `RELATED_TO` edges
- zero jurisdiction-mutated canonical nodes
- zero source rows with content-ingest use and unclear rights
- snapshot determinism: identical input produces identical semantic snapshot
- Neo4j FTS p95 <= 200 ms for agreed shadow query set unless a later benchmark
  plan explicitly revises the target
- resolver exact ID lookup p95 <= 100 ms
- resolver context resolve p95 <= 250 ms
- search p95 <= 300 ms

## Output Artifacts

Later implementation must produce:

- source-rights validation report
- registry-candidate validation report
- predicate-registry validation report
- backbone schema validation report
- shadow snapshot report
- Neo4j shadow load report
- API parity report
- Explorer smoke report
- latency report
- rollback preflight report
- stopped/isolated rollback proof report

## Pass / Fail Gate

Pass:

- exact commands and report paths are recorded before implementation
- tests are monotonic and do not weaken current v1/API/Explorer checks
- benchmark failures block cutover

Fail:

- readiness claims are made without reproducible commands
- implementation removes current tests to pass the new path
- latency or parity failures are treated as cosmetic
