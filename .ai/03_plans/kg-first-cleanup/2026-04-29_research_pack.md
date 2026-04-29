---
task: kg-first-cleanup
phase: research-pack
created: 2026-04-29
author: CODEX
status: COMPLETE
---

# KG-First Cleanup Research Pack

## Research Question

What can be safely cleaned up now that Vitruvius is moving from a
raw-source-layer -> raw-conversion-layer -> canonical-knowledge-layer operating
story to a KG-first operating story?

## Current Repo State

- Branch: `main...origin/main`
- Starting commit: `e4fe2aff` (`Replace remaining taxonomy scaffolds with semantic topics`)
- Working tree at intake: clean.
- Current authoritative phase: AEC-MEPFS file-backed runtime is implemented
  locally; production Neo4j promotion and protected payload admission remain
  hard-blocked.

## Tool Evidence Collected

### GitNexus status/query

`npx --yes gitnexus@1.6.2-rc.10 status` reported the index is up to date at
commit `e4fe2af`.

GitNexus query for raw/conversion/canonical/source-ingestion concepts surfaced:

- `scripts/pipeline_cli.py`
- `scripts/tests/test_dataset_pipeline_cli.py`
- `scripts/tests/test_dataset_source_to_graph_pipeline.py`
- `scripts/tests/test_kg_pipeline_force_path.py`
- `scripts/tests/test_pdf_evidence_integration.py`
- `scripts/vitruvius/kg/evidence_ingestor.py`
- `scripts/tests/test_evidence_ingestor.py`
- processes around `run_all_laws_dry_run`, `run_dataset_graph_pipeline`, and
  `run_build_graph`.

GitNexus context/impact evidence:

- `EvidenceIngestor` is imported by `scripts/pipeline_cli.py` and
  `scripts/tests/test_evidence_ingestor.py`.
- `EvidenceIngestor` upstream impact: **MEDIUM**, 37 impacted symbols, direct
  callers/importers include `pipeline_cli.main`, `test_ingest_markdown`, and
  `test_ingest_idempotent`.
- `pipeline_cli` file-level context/impact lookup by bare file name was not
  available as a symbol target; function-level impact must be rerun before any
  exact function edit.

### OMX Explore

`omx explore` initially attempted `gpt-5.3-codex-spark`, hit the Spark usage
limit, then fell back to `gpt-5.5` and returned repository-backed maps.

Legacy layer-first map:

- `scripts/pipeline_cli.py` orchestrates legacy raw/conversion/canonical/KG
  commands.
- `scripts/vitruvius/conversion.py` reads `001_Raw-Source-Layer` and writes
  conversion artifacts.
- `scripts/vitruvius/normalization/refine.py` produces refined markdown.
- `scripts/vitruvius/canonicalize.py` writes canonical source files.
- `scripts/vitruvius/source_identity.py` maps refined/conversion paths to
  canonical source IDs.
- `scripts/vitruvius/graph/cli.py` builds graph snapshots from canonical shared
  material.
- `scripts/vitruvius/dataset_pipeline.py` is a bridge path for dataset
  source-to-graph orchestration.

KG-first/AEC preservation map:

- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/vitruvius/kg/backbone_shadow_staging.py`
- `scripts/vitruvius/kg/backbone_source_admission.py`
- `scripts/vitruvius/kg/backbone_resolver_qa.py`
- `scripts/vitruvius/kg/backbone_runtime_thresholds.py`
- `scripts/vitruvius/kg/taxonomy_v2_schemas.py`
- `scripts/vitruvius/kg/broad_taxonomy_semantic_enrichment.py`
- `api/index.ts`, including `/v2/backbone*`, `/v2/search`, `/v2/sources/:source_id`, `/v2/resolve`, `/v2/resolve/trace/:trace_id`
- `explorer/src/constants/perspectives.ts`, `explorer/src/api/graphApi.ts`,
  `explorer/src/App.tsx`, and backbone preview/graph interaction tests.

### ChunkHound

ChunkHound regex search found more than 2,000 references to old layer naming,
including load-bearing system docs:

- `.ai/00_system/EXECUTION_LOOP.md` still defines the six-layer architecture.
- It marks `001_Raw-Source-Layer/**` as identity-locked/immutable.
- It classifies edits to `scripts/pipeline_cli.py`, `config/vitruvius.yaml`,
  schemas, and non-curator-owned canonical layer files as high-risk.

ChunkHound also found current code touchpoints:

- `scripts/pipeline_cli.py` imports/uses `run_scan`, `run_convert`,
  `run_refine`, and review/conversion helpers.
- `scripts/AGENTS.md` still describes `pipeline_cli.py` as the main pipeline
  command surface and references standalone PDF conversion tests.
- Multiple tests still intentionally validate raw/conversion/canonical behavior.

### Code graph / AST MCP

`omx_code_intel` AST MCP calls failed with `Transport closed`. This is recorded
as a tool limitation, not as proof of low blast radius. The implementation phase
must rerun code-intel or use a fresh GitNexus impact pass for exact symbols.

### Kimi / Team Runtime

A tmux OMX team was launched for read-only planning audit. The Codex Spark
workers hit the `gpt-5.3-codex-spark` usage limit before producing useful
results. The team was shut down with no code changes and no diffs.

Kimi CLI is available at `/Users/philiplewis/.local/bin/kimi`. It may be used as
an advisory review lane for the next implementation plan or exact diffs, but it
must not replace repo-backed tests and impact analysis.

## Key Finding

The old layer-first machinery is not simply dead code. It is still the source
staging/evidence-preparation substrate for source material, laws datasets,
canonical source IDs, evidence ingestion, and historical graph pipelines.
Cleanup should therefore **reframe, wrap, and deprecate** before any deletion.

## Research Conclusion

The safe cleanup path is incremental:

1. Reconcile docs/operator language to KG-first.
2. Preserve legacy layer paths as compatibility/staging terms.
3. Add adapters/aliases only after tests pin current behavior.
4. Delete only after GitNexus proves no callers and test coverage proves no
   behavior loss.
