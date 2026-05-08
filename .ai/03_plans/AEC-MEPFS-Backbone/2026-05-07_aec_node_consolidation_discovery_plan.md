# AEC Node Consolidation Discovery Plan

Date: 2026-05-07

## Goal

Add a pending-only node-improvement lane to the existing AEC relationship-improvement workflow. The extended workflow will still discover candidate relationships, and when explicitly enabled it will also identify nodes that may be duplicates, aliases, label variants, or near duplicates that require steward review.

This is not a merge workflow. It is a discovery and review-artifact workflow.

## Research Pack

Authoritative local state checked before implementation:

- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/01_roadmap/master-roadmap.md`
- existing AEC relationship workflow in `scripts/vitruvius/kg/aec_relationship_improvement.py`
- CLI wiring in `scripts/pipeline_cli.py`
- existing relationship workflow tests in `scripts/tests/test_kg_aec_relationship_improvement.py`
- duplicate/steward review patterns in `scripts/vitruvius/kg/architecture_civil_structural_gate_review.py`
- exact-match review-only merge pattern in `scripts/vitruvius/kg/merge_adjudicator.py`

No external web research is required or allowed for this implementation because the requested feature is local workflow behavior and must not use internet lookup.

## Audit Findings

- The current relationship workflow already has the right durable-run shell: run bootstrap, checkpointing, event JSONL, validation errors, summary text, TSV review files, progress mode, watcher, DeepSeek-local routing, and pending-only safety gates.
- The existing embedding layer already creates deterministic node text and caches embeddings. Node consolidation can reuse that work without adding another embedding pass.
- The current candidate-pair generator is streaming top-k per node and avoids full all-pairs materialization. Node consolidation should use the same pattern with stricter defaults.
- Existing duplicate stewardship code explicitly blocks automatic merge application and exports review candidates only. The new node lane must copy that boundary language into artifacts.
- The active roadmap/current-state files explicitly prohibit graph mutation, merge/alias/redirect/tombstone actions, protected payload admission, and production promotion.
- The CLI currently duplicates most module parser flags manually in `pipeline_cli.py`; new flags must be wired in both places.

## Governing Boundaries

- Active Backbone files remain read-only.
- Neo4j and Postgres are not touched.
- `--apply` remains rejected.
- No AI output is admitted as truth.
- No node is automatically merged, redirected, retired, tombstoned, or canonicalized.
- Kimi remains disabled by default.
- Cloud calls require `--allow-cloud-ai`.
- Local Ollama calls remain sequential.
- Artifacts are sanitized and must not include API keys, bearer tokens, reasoning content, full embeddings, or giant raw responses.

## Blast Radius

Primary code blast radius is low to moderate and isolated to:

- `scripts/vitruvius/kg/aec_relationship_improvement.py`
  - configuration dataclasses
  - node decision schema and prompt construction
  - node-pair candidate generation
  - optional processing lane in `run_relationship_improvement`
  - checkpoint/report/summary/review TSV additions
- `scripts/pipeline_cli.py`
  - CLI flag wiring for `aec-improve-relationships`
- `scripts/tests/test_kg_aec_relationship_improvement.py`
  - mocked unit tests

No API/Explorer changes are planned. No active graph fixture mutation is planned. Existing relationship behavior remains default because the new lane is off unless `--improve-nodes` or `--node-consolidation-mode candidates` is passed.

Impact checks already performed:

- `run_relationship_improvement`: LOW, direct caller `main`
- `RunConfig`: LOW
- `add_cli_arguments`: LOW, direct caller `build_arg_parser`
- `config_from_args`: LOW, direct caller `main`
- `RelationshipCouncil`: LOW
- `Checkpoint`: LOW
- `generate_candidate_pairs`: LOW, direct caller `run_relationship_improvement`

## Feature Design

### CLI

Add:

- `--improve-nodes`
- `--node-consolidation-mode off|candidates|audit_only`, default `off`
- `--node-candidate-top-k`, default `10`
- `--node-min-similarity`, default `0.82`
- `--node-max-pairs`, default `1000`
- `--node-accept-threshold`, default `0.90`
- `--node-review-threshold`, default `0.75`
- `--node-judge-provider ollama|deepseek|auto`, default `auto`

Effective behavior: `--improve-nodes` enables `candidates` mode unless the operator explicitly sets `--node-consolidation-mode off`.

### Candidate Generation

Reuse the node embeddings already generated for relationship discovery. Generate node-pair candidates with top-k similarity search, mirroring the existing relationship candidate generator so the workflow does not materialize all 10k x 10k pairs.

Efficiency controls:

- strict default similarity threshold
- top-k per node
- global `--node-max-pairs`
- deterministic skip rules before model calls
- reuse embedding cache and run-local embeddings

### Deterministic Guards

Pre-model and final guards classify obvious non-merge cases without spending model calls:

- same node id: skip
- path-code parent/child hierarchy: keep separate
- clear different root path/discipline/lifecycle/record-type context: downgrade to review or keep separate
- exact label/alias normalized match is a strong signal but still requires review artifacts, not mutation
- safety-critical or P0-like labels are never auto-accepted as merge; they require explicit steward review

### Node Decision Schema

Add `NodeConsolidationDecision`:

- `same_concept`
- `decision`: `same_concept`, `alias_or_label_variant`, `near_duplicate_needs_review`, `keep_separate`
- `canonical_survivor`: `A`, `B`, or `none`
- `confidence`
- `rationale`
- `evidence`
- `suggested_canonical_label`
- `suggested_aliases`
- `field_merge_notes`
- `relationship_reassignment_notes`
- `risk_flags`
- `review_recommendation`: `accept_candidate`, `needs_review`, `reject`

Final acceptance means "accepted as a review candidate", not admitted graph mutation.

### Provider Routing

Reuse the current local + DeepSeek council mechanics:

- `local_only`: Ollama judge only.
- `deepseek_local` / `adaptive_cloud`: DeepSeek Flash judge when cloud is explicitly enabled and budgeted; Ollama fallback.
- No Kimi default routing.

The node lane should call the judge role only in v1. A later pass can add dedicated verifier/adjudicator policies if review outcomes show it is worth the extra cost.

### Output Artifacts

Add run-local artifacts:

- `node-consolidation-candidates.jsonl`
- `accepted-node-consolidations.jsonl`
- `rejected-node-consolidations.jsonl`
- `node-consolidation-review.tsv`

Each accepted/review record must include:

- `schema_version`
- `run_id`
- `node_pair_key`
- node ids, labels, path codes, record types
- similarity and embedding model
- decision fields
- provider/council metadata
- deterministic guard metadata
- `review_status: candidate`
- `auto_merge_allowed: false`
- `batch_merge_blocked: true`
- `requires_steward_decision: true`
- allowed steward actions
- explicit pending-only boundaries

### Checkpoint, Report, Summary, Watcher

Add counters:

- `node_consolidation_candidate_count`
- `node_consolidation_processed_count`
- `node_consolidation_accepted_count`
- `node_consolidation_review_count`
- `node_consolidation_rejected_count`
- `node_consolidation_skipped_guard_count`
- `node_consolidation_model_call_count`

Add `node_improvement_summary` to the JSON report and concise summary text. The watcher can continue tolerating unknown files; if practical, include node counts in snapshot/render output.

## Testing Plan

Add focused pytest coverage:

1. CLI parser accepts node-improvement flags.
2. Default relationship-only mode does not process node consolidation.
3. `--improve-nodes` enables candidate mode.
4. Node candidate generation returns top-k pairs without all-pairs materialization.
5. Parent/child path hierarchy is not accepted as a merge.
6. Strong duplicate/alias fake judge output writes accepted pending artifact only.
7. Ambiguous role/facet variant writes needs-review candidate.
8. Missing rationale/evidence is rejected safely.
9. Node artifacts and TSV are written under the run directory.
10. Node records include `auto_merge_allowed=false`, `batch_merge_blocked=true`, and `requires_steward_decision=true`.
11. Report and summary include node-improvement counts.
12. Sanitizer removes secrets and reasoning content from node artifacts.
13. `--apply` remains rejected.
14. Existing relationship tests continue passing.
15. Existing graph quality/shadow staging tests continue passing.

## Implementation Checklist

1. Add node config/checkpoint/summary fields.
2. Add node output files.
3. Add node decision schema and prompt.
4. Add node candidate generator and deterministic guards.
5. Add node-processing lane after embeddings and before/after relationship decisions without changing relationship defaults.
6. Add TSV/report/summary support.
7. Wire CLI flags in module parser and `pipeline_cli.py`.
8. Add tests first for parser/schema/generation/output safety.
9. Implement until targeted tests pass.
10. Run compile and relevant regression tests.
11. Refresh code intelligence and detect changes before finalizing.

## Plan Critique

Main risks and mitigations:

- False-positive merges are more harmful than missed candidates. Mitigation: artifacts only, high default similarity threshold, deterministic hierarchy/context guards, and `auto_merge_allowed=false` everywhere.
- Running node consolidation on top of relationship discovery could double model costs. Mitigation: feature is off by default, uses separate `--node-max-pairs`, strict similarity threshold, pre-model guards, and reuses embeddings.
- Candidate generation could accidentally materialize all pairs. Mitigation: implement a streaming top-k generator mirroring `generate_candidate_pairs`.
- Provider metadata could become confusing when DeepSeek falls back to Ollama. Mitigation: reuse existing `ProviderEnvelope` metadata and write effective provider/model for each node decision.
- CLI drift is likely because the module parser and `pipeline_cli.py` are duplicated. Mitigation: add parser tests for both new flags and runtime `RunConfig` values.
- Node consolidation can conflict with existing gated duplicate-review semantics. Mitigation: use language consistent with existing gate review: steward review required, batch merge blocked, mutation flags false.

## Validation Report Template

Completed after implementation:

- Unit tests:
  - `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q`
  - Result: 123 passed.
- Regression tests:
  - `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q`
  - Result: 18 passed.
- Compile:
  - `python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py`
  - Result: passed.
- No-model smoke:
  - `PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships --dry-run --run-id node_consolidation_no_model_smoke --council-mode local_only --max-nodes 0 --max-pairs 0 --improve-nodes --node-max-pairs 0 --progress-mode plain --no-use-global-ledger`
  - Result: passed; report showed `node_consolidation_mode: candidates`, zero model calls, and pending-only summary. Throwaway smoke run directory was removed after verification.
- Code intelligence refresh/detect changes:
  - `bash ./scripts/refresh_code_intelligence.sh`
  - Result: completed; GitNexus already current, ChunkHound/code-review-graph refreshed with known YAML parser warnings and embedding-provider enrichment errors.
  - `bash -lc "npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius"`
  - Result: exit 0; GitNexus reported CRITICAL blast-radius because the central workflow, CLI parser, and relationship-improvement tests changed. This is expected for this scoped feature and was mitigated with focused workflow tests, graph-quality regressions, compile checks, and a no-model CLI smoke.

## Known Limitations

- v1 produces merge/consolidation recommendations only; it does not apply steward decisions.
- v1 uses one node judge decision by default; verifier/adjudicator for node consolidation can be added later if manual review shows false positives.
- Similarity-based duplicate discovery can miss semantically equivalent nodes with weak embeddings; stricter thresholds reduce cost but reduce recall.
- Existing duplicate-label gate review remains a separate preflight/gated review workflow; this feature complements it with semantic candidate discovery.
