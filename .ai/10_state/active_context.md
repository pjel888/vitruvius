# Active Context — Vitruvius

**Updated:** 2026-04-27
**Live branch:** `main`

## Current Operating Truth

- The control-surface consolidation phase is **completed**.
- The repository has already shipped the core pipeline, graph/query surface, KG v2 transition, laws-wave bounded automation, Graph Explorer, and nested AGENTS coverage.
- The current work is the next bounded decision on top of that stabilized planning surface, not another control-surface cleanup pass.

## Execution Note — 2026-04-21 (Autonomous implementation run)

- **Selected focus (completed):** finish the highest-leverage control-surface slice by slimming active plan families and removing invalid plan references from the live index.
- **Why this was chosen:** active-roadmap consistency depends on the plan index; keeping invalid or overly broad “active” entries causes execution misrouting in later sessions.
- **Expected deliverables (completed):**
  1. active AEC plan family reduced to a minimal execution-readiness packet,
  2. broken plan-path references removed from live docs,
  3. roadmap/state statuses reconciled so completed cleanup work no longer presents as active.
- **Validation plan used:**
  1. grep checks for broken/stale active references,
  2. targeted pytest smoke commands,
  3. post-change consistency read of `ACTIVE_WORK.md`, `current-phase.md`, `master-roadmap.md`, and `03_plans/INDEX.md`.

## High-Signal Repo State

### Shipped capabilities
- **Core pipeline through promotion:** `scripts/pipeline_cli.py`, `scripts/vitruvius/promotion_validator.py`, `003_Canonical-Knowledge-Layer/shared/relationships/`
- **Graph build/query surface:** `scripts/vitruvius/graph/cli.py`, `scripts/vitruvius/graph/visualize.py`, `005_Operational-Intelligence-Layer/graph/`
- **KG v2 transition:** `scripts/vitruvius/kg/`, `scripts/tests/test_kg*.py`, `005_Operational-Intelligence-Layer/graph/kg-v2/`
- **Graph Explorer:** `explorer/src/components/graph/`, `api/index.ts`, `explorer/README.md`
- **Nested AGENTS:** `**/AGENTS.md`, `.ai/05_logs/2026-04-20_nested-agents-governance-validation.md`

### Laws-wave operating state
- `status = saturated_truth_complete`
- machine-readable state: `/.ai/10_state/laws-wave-status.json`
- artifact stack:
  - `config/datasets/laws-completed-lanes.yaml`
  - `config/datasets/laws-remaining-dispositions.yaml`
  - `config/datasets/laws-source-provenance.yaml`
  - `config/datasets/laws-manifest-index.yaml`
  - `.ai/03_plans/laws-wave/LAWS_WAVE_ARTIFACT_INDEX.md`
- completion evidence: `/.ai/05_logs/2026-04-20_ra-386-residual-hardening-validation.md`

## Active Priorities

1. Complete only the AEC-MEPFS non-protected resolver fixture expansion packet.
2. Keep broader live runtime blocked: no unguarded/default-on `/v2/resolve*` behavior, Neo4j mutation, KG rebuild/reload, protected ingest, Explorer default adoption, default-on feature flags, runtime threshold claims, or primary graph promotion.
3. Keep roadmap/state docs contradiction-free.
4. Refresh unverified claims only when implementation changes warrant it.

## AEC-MEPFS Boundary Approval Checkpoint — 2026-04-27

- governance packet: `/.ai/03_plans/AEC-MEPFS-Backbone/runtime-governance-admission-packet.md`
- completed bounded packet: `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_bounded_resolver_runtime_contract_packet.md` (`618a659b`)
- completed default-off packet: `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_default_off_resolver_runtime_packet.md` (`6e91b96a`)
- active bounded packet: `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_resolver_fixture_expansion_packet.md`
- current truth: implemented runtime is limited to default-off, file-backed `/v2/resolve*` routes guarded by `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME`; active work is non-protected resolver fixture coverage expansion
- still blocked: unguarded/default-on `/v2/resolve*` behavior, Neo4j writes/reset/reload/backup/restore/mutation, KG rebuild/reload, protected ingest, Explorer default adoption, default-on feature flags, runtime threshold claims, and broad live runtime promotion

## AEC Runtime Roots Checkpoint — 2026-04-23

- audit log: `/.ai/05_logs/2026-04-23_aec-runtime-roots-audit-and-lane-decision.md`
- current truth: no real AEC runtime roots exist yet in executable code
- planning decision: AEC remains the next planned lane, but runtime implementation is still not open

## Unverified / Log-Backed Claims

- Full test suite counts remain log-backed rather than freshly rerun in this phase:
  - `/.ai/05_logs/2026-04-20_full-test-suite-green-validation.md`

## Latest Validation Checkpoint

- validation log: `/.ai/05_logs/2026-04-24_post_laws_kg_rebuild_relationship_graph_validation.md`
- post-audit `001-Laws` KG rebuild checkpoint:
  - snapshot: `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json`
  - scope: 181 source pages, all with `source_relative_markdown_path` under `001-Laws/`; 2 are under `001-Laws/refined_markdown/test/...`
  - Neo4j: cleared to 0 nodes, loaded 5911/5911 statements with 0 errors, final count 2429 nodes
  - rule display-title quality: 214 rules, 0 duplicate display labels, 0 generic display labels, 0 display-title truncation markers
  - caveat: semantic relationship distribution remains shallow and cross-subject enrichment is deferred

## Previous Validation Checkpoint

- validation log: `/.ai/05_logs/2026-04-21_control-surface-consolidation-validation.md`
- standalone checks passed:
  - `python3 scripts/test_odl_one.py`
  - `python3 scripts/test_pdf_text_detection.py "001-Laws/PD-1096/PD 1096 - National Building Code.pdf"`
- targeted pytest passed:
  - `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_graph_builder.py -q` → `27 passed`
- active-doc correction completed in this pass:
  - `README.md` testing commands now use repo-proven `PYTHONPATH=scripts python3 -m pytest ...`

## Current Execution Focus — 2026-04-21 (Post-consolidation)

- Control-surface consolidation is complete enough that it should no longer be treated as the active execution lane.
- The next bounded decision has narrowed: AEC should remain the next live planning family, while runtime stays deferred until a bounded execution packet is accepted.

## Read Next

- `/.ai/01_roadmap/current-phase.md`
- `/.ai/ACTIVE_WORK.md`
- `/.ai/STRATEGIC_NEXT_MOVE.md`
