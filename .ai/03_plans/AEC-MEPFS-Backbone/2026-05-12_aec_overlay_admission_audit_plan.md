# AEC Overlay Admission Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert completed AEC relationship-improvement overlay runs into auditable Explorer approval states and guarded admission-ready relationship packets without mutating the active graph.

**Architecture:** Add a deterministic audit command that reads one semantic-overlay run directory, validates accepted relationship candidates against the admitted backbone, writes run-local audit artifacts, and marks node-consolidation candidates as steward-action-only. Update the API overlay reader so Explorer can render admission-ready relationships and steward-required node consolidation distinctly while preserving `pendingOnly: true`.

**Tech Stack:** Python pipeline CLI, JSON/JSONL artifacts, existing AEC relationship-improvement helpers, TypeScript API overlay reader, Bun/Pytest tests.

---

## Research Pack

- Active state permits file-backed AEC-MEPFS runtime and pending overlays but still blocks graph/canonical mutation, production Neo4j writes, protected payload admission, and AI-generated truth admission without reviewed gates.
- Run `aec_backbone_all_nodes_bounded_004` completed with `1,579` accepted relationship candidates and `76` accepted node-consolidation candidates.
- All `1,579` accepted relationship candidates passed the final deterministic guard, but `195` carry model risk flags.
- All `76` accepted node-consolidation candidates explicitly record `auto_merge_allowed=false`, `batch_merge_blocked=true`, and `requires_steward_decision=true`.
- Existing Explorer overlay reader is in `api/index.ts` and already keeps pending overlay edges separate from base expansion.

## Audit

Bulk admitting every overlay candidate would violate the current truth boundary. Relationship candidates can be classified into an admission-ready subset when deterministic checks pass and risk flags are absent. Node consolidation cannot be batch-applied because each accepted record requires a steward decision and may change canonical identity, aliases, redirects, tombstones, and relationship reassignment.

## Plan Critique

This plan intentionally does not create an active-graph apply path. It improves Explorer immediately by exposing review state and creates a packet that a future, separately gated admission command can consume. The tradeoff is that admitted graph counts do not change yet, but the workflow remains reversible and consistent with the repository governance contract.

## Execution Checklist

### Task 1: Python Audit Packet

**Files:**
- Modify: `scripts/vitruvius/kg/aec_relationship_improvement.py`
- Modify: `scripts/tests/test_kg_aec_relationship_improvement.py`

- [x] Add `audit_relationship_overlay_admission(run_dir, input_path, min_confidence)` that writes:
  - `overlay-approval-manifest.json`
  - `relationship-admission-ready.jsonl`
  - `relationship-admission-review-required.jsonl`
  - `node-consolidation-steward-actions.jsonl`
- [x] Treat relationship records as admission-ready only when final guard passed, predicate is allowed, predicate is not blocked, endpoints exist, edge key is not already active, confidence is high enough, evidence/rationale are present, and risk flags are empty.
- [x] Treat every node-consolidation accepted record as steward-action-only; do not write merge/apply artifacts.
- [x] Sanitize artifacts and write JSON atomically.
- [x] Add tests for ready relationship classification, risk-flag review classification, duplicate active-edge rejection, node steward-action-only classification, and no active fixture mutation.

### Task 2: CLI Wiring

**Files:**
- Modify: `scripts/pipeline_cli.py`
- Modify: `scripts/tests/test_kg_aec_relationship_improvement.py`

- [x] Add command `aec-audit-relationship-overlay-admission`.
- [x] Accept `--run-id`, `--output-root`, `--output-dir`, `--input-path`, and `--min-confidence`.
- [x] Print a concise JSON summary.
- [x] Add parser and smoke tests.

### Task 3: Explorer Overlay State

**Files:**
- Modify: `api/index.ts`
- Modify: `api/v2Backbone.test.ts`

- [x] Read audit artifacts when present.
- [x] Mark admission-ready relationship overlay edges as `PENDING_RELATIONSHIP_ADMISSION_READY`.
- [x] Mark node-consolidation steward actions as `PENDING_NODE_CONSOLIDATION_STEWARD_ACTION`.
- [x] Preserve `pendingOnly: true` and graph-mutation boundary fields.
- [x] Add overlay counts for admission-ready relationships and steward-required node candidates.
- [x] Add API tests proving render output includes the new states and expand output remains unpolluted.

### Task 4: Validation

**Files:**
- Update validation notes in this file after running tests.

- [x] Run focused Python tests.
- [x] Run focused API tests.
- [x] Run compile checks for Python.
- [x] Run TypeScript/Bun API tests that cover overlay behavior.
- [x] Scan generated audit packet for API keys and `reasoning_content`.

### Task 5: Pending Resolution Workqueue

**Files:**
- Modify: `scripts/vitruvius/kg/aec_relationship_improvement.py`
- Modify: `scripts/pipeline_cli.py`
- Modify: `api/index.ts`
- Modify: `explorer/src/types/index.ts`
- Modify: `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- Modify: tests

- [x] Add `build_overlay_pending_resolution_workqueue(output_dir, input_path)`.
- [x] Write `relationship-admission-review-workqueue.tsv`.
- [x] Write `node-consolidation-review-workqueue.tsv`.
- [x] Write `pending-resolution-decisions-template.tsv`.
- [x] Write `pending-resolution-manifest.json`.
- [x] Add CLI command `aec-build-overlay-review-workqueue`.
- [x] Expose workqueue counts and artifact paths through the Explorer overlay API.
- [x] Show total resolution queue count in the Explorer preview panel.

### Task 6: Review Decision Recording

**Files:**
- Modify: `scripts/vitruvius/kg/aec_relationship_improvement.py`
- Modify: `scripts/pipeline_cli.py`
- Modify: `api/index.ts`
- Modify: `api/v2Backbone.test.ts`
- Modify: Explorer preview types/panel

- [x] Add `record_overlay_pending_resolution_decisions(output_dir, decisions_path)`.
- [x] Add CLI command `aec-record-overlay-review-decisions`.
- [x] Validate relationship and node-consolidation decision vocabularies.
- [x] Write `pending-resolution-decisions.jsonl`.
- [x] Write `pending-resolution-decision-manifest.json`.
- [x] Read recorded decisions in the Explorer overlay API.
- [x] Render recorded decisions as distinct pending-only overlay states.
- [x] Show recorded decision counts in the Explorer preview panel.

## Validation Report

- `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q` passed: 133 tests.
- `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q` passed: 18 tests.
- `python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py` passed.
- `bun test api/v2Backbone.test.ts --filter "audited improvement overlays expose admission-ready"` passed: 79 tests.
- `bun test explorer/src/app.searchInspector.integration.test.tsx` passed: 10 tests.
- `git diff --check` passed with line-ending warnings only.
- Generated `aec_backbone_all_nodes_bounded_004` audit packet:
  - `relationship_admission_ready_count=1384`
  - `relationship_review_required_count=1373`
  - `node_consolidation_steward_action_count=1255`
- Generated `aec_backbone_all_nodes_bounded_004` pending resolution workqueue:
  - `relationship_review_required_count=1373`
  - `node_consolidation_steward_action_count=1255`
  - `total_resolution_workqueue_count=2628`
- Secret/reasoning scan over generated audit artifacts found no `reasoning_content`, bearer token, or `sk-*` secret.
- Secret/reasoning scan over generated workqueue artifacts found no `reasoning_content`, bearer token, or `sk-*` secret.
- Latest `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q` passed: 135 tests.
- Latest `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q` after decision recording passed: 138 tests.
- Latest `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q` passed: 18 tests.
- Latest `bun test explorer/src/app.searchInspector.integration.test.tsx` passed: 10 tests.
- Latest `python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py` passed.
- Latest `bun test api/v2Backbone.test.ts --filter "recorded overlay review decisions update Explorer"` passed: 80 tests.
- Generated zero-decision manifest for `aec_backbone_all_nodes_bounded_004` from the blank decision template:
  - `pending-resolution-decisions.jsonl`
  - `pending-resolution-decision-manifest.json`
  - `decision_count=0`
- Recorded operator-requested bulk pending overlay decisions for `aec_backbone_all_nodes_bounded_004`:
  - `bulk-pending-resolution-decisions.nobom.tsv`
  - `pending-resolution-decisions.jsonl`
  - `pending-resolution-decision-manifest.json`
  - `decision_count=4011`
  - `approve_for_admission=1384`
  - `approve_alias_only=76`
  - `needs_more_evidence=2551`
  - `active_graph_mutation=false`
  - `neo4j_writes=false`
  - `postgres_writes=false`
- Live API overlay read for `aec_backbone_all_nodes_bounded_004` confirmed:
  - `PENDING_RELATIONSHIP_STEWARD_APPROVED=1384`
  - `PENDING_RELATIONSHIP_NEEDS_EVIDENCE=1372`
  - `PENDING_NODE_CONSOLIDATION_ALIAS_APPROVED=76`
  - `PENDING_NODE_CONSOLIDATION_NEEDS_EVIDENCE=1179`
  - `totalResolutionDecisions=4011`
  - `skippedInvalid=1` for a non-displayable candidate with no valid edge key.
- Latest `bun test api/v2Backbone.test.ts --filter "recorded overlay review decisions update Explorer"` passed: 80 tests.
- Secret/reasoning scan over bulk decision artifacts found no `reasoning_content`, bearer token, or `sk-*` secret.
- Post-change `refresh_code_intelligence.sh` completed successfully; retained known warnings for ChunkHound oversized embeddings and missing `tree-sitter-yaml` in code-review-graph YAML parsing.
- `gitnexus detect-changes` via `cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius` reported high risk because common Explorer graph/overlay flows are affected; targeted API, Explorer, Python, and backbone regression suites passed.
