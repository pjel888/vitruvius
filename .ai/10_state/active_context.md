# Active Context — Vitruvius

**Updated:** 2026-04-21  
**Live branch:** `main`

## Current Operating Truth

- The control-surface consolidation phase is **completed**.
- The repository has already shipped the core pipeline, graph/query surface, KG v2 transition, laws-wave bounded automation, Graph Explorer, and nested AGENTS coverage.
- The current work is the next bounded decision on top of that stabilized planning surface, not another control-surface cleanup pass.

## Execution Note — 2026-04-21 (Autonomous implementation run)

- **Selected focus:** finish the highest-leverage control-surface slice by slimming active plan families and removing invalid plan references from the live index.
- **Why this was chosen:** active-roadmap consistency depends on the plan index; keeping invalid or overly broad “active” entries causes execution misrouting in later sessions.
- **Expected deliverables:**
  1. active AEC plan family reduced to a minimal execution-readiness packet,
  2. broken plan-path references removed from live docs,
  3. roadmap/state statuses reconciled so completed cleanup work no longer presents as active.
- **Validation plan:**
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

1. Make the AEC execution-readiness decision from the stabilized control surface.
2. Keep roadmap/state docs contradiction-free.
3. Refresh unverified claims only when implementation changes warrant it.

## Unverified / Log-Backed Claims

- Full test suite counts remain log-backed rather than freshly rerun in this phase:
  - `/.ai/05_logs/2026-04-20_full-test-suite-green-validation.md`

## Latest Validation Checkpoint

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
- The next bounded decision is whether AEC remains the next live implementation family or is demoted further until runtime roots exist.

## Read Next

- `/.ai/01_roadmap/current-phase.md`
- `/.ai/ACTIVE_WORK.md`
- `/.ai/STRATEGIC_NEXT_MOVE.md`
