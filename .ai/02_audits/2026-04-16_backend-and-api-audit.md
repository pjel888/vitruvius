---
task: vitruvius-audit-pass-1
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Backend and API Audit

## Purpose
Audit the real backend surface of Vitruvius: CLI orchestration, graph/query commands, and file-contract interfaces.

## Scope
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/graph/**`
- `scripts/vitruvius/query/**`
- `scripts/vitruvius/ontology/**`
- `spatial-daemon/` file-contract boundary

## What Was Inspected
- `scripts/vitruvius/graph/builder.py`
- `scripts/vitruvius/graph/integrity.py`
- `scripts/vitruvius/query/cli.py`
- `scripts/vitruvius/query/engine.py`
- `scripts/vitruvius/query/nl_translator.py`
- `scripts/vitruvius/ontology/owl_exporter.py`
- `spatial-daemon/README.md`

## What Was Tested
- `python3 scripts/pipeline_cli.py build-graph`
- `python3 scripts/pipeline_cli.py query-graph --from law-national-building-code-of-the-philippines --to concept-building-permit`
- `python3 scripts/pipeline_cli.py query-structured --function neighbors --subject concept-occupancy-classification`
- `python3 scripts/pipeline_cli.py query "What governs occupancy classification?"`
- `python3 scripts/pipeline_cli.py export-graph-owl`

## What Works
- Graph snapshot build succeeds from canonical files.
- `query-graph` returns connected paths as JSON.
- OWL export writes a valid Turtle file.
- The spatial TypeScript sibling remains isolated by file contract, not RPC.

## What Fails
- Duplicate canonical source IDs are allowed into the graph snapshot.
- Integrity checks do not detect duplicate nodes.
- Query citations are synthetic and can display as “supporting evidence” with no evidence snippet or section ID.
- Natural-language query translation in the CLI defaults to regex fallback; it is not a true NL interface.

## What Is Misleading
- Backend output format implies stronger provenance than the implementation supplies.
- “Query layer complete” claims need caveats because the implemented path is topology lookup plus regex translation, not evidence-grounded QA.

## Severity-Ranked Findings
- `HIGH` Duplicate canonical IDs enter the graph silently. `003_Canonical-Knowledge-Layer/shared/sources/pd-1096-irr.md` and `.../implementing-rules-and-regulations-of-the-national-building-code.md` both declare `id: irr-implementing-rules-and-regulations-of-the-national-building-code`; `build_snapshot()` includes both nodes and `check_integrity()` never flags duplicate node IDs.
- `HIGH` Query citations are not real evidence. `scripts/vitruvius/query/engine.py:16-22` manufactures citations from edges with empty `source_section_id` and `evidence_snippet`, and `render_query_result()` still presents them as supporting evidence.
- `MEDIUM` Query confidence is effectively binary and shallow. `scripts/vitruvius/query/engine.py:12-13` maps confidence to `1.0` for `verified` edges and `0.5` otherwise; current snapshot edges are `unverified`, so outputs flatten to `0.50`.
- `MEDIUM` The CLI’s “natural language” path is regex-only by default. `translate_question()` falls back to keyword matching unless an LLM caller is explicitly injected, which `run_query()` does not do.

## Reproduction Steps
1. Run `python3 scripts/pipeline_cli.py build-graph`.
2. Inspect `005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.json` and observe duplicate `irr-implementing-rules-and-regulations-of-the-national-building-code` nodes.
3. Run `python3 scripts/pipeline_cli.py query-structured --function neighbors --subject concept-occupancy-classification`.
4. Observe `"(no snippet)"`, `"(no section)"`, and flat `0.50` confidence.

## Suspected Root Causes
- Graph integrity rules were designed around edge validity, not canonical node identity uniqueness.
- Query layer was built from graph topology first and provenance later; provenance was never closed.
- Docs evolved faster than the evidence model.

## Recommended Fix Direction
- Enforce duplicate-node detection in graph integrity and/or canonical source linting.
- Rebuild query citations from relationship evidence arrays, not bare edges.
- Downgrade query/docs claims until provenance-bearing answers are real.

## Validation Needed After Fix
- Re-run `build-graph` and confirm duplicate-node detection fails fast.
- Re-run `query` and `query-structured` and confirm non-empty section/snippet evidence.
- Re-run query tests plus full suite.

## Audit Verdict
The backend surface executes, but the graph/query trust boundary is not strong enough for confident downstream feature work.

## PASS 2 Note — 2026-04-16
- Duplicate node IDs are now surfaced as an explicit `duplicate_node_id` integrity error instead of silently passing.
- Query citations now use relationship evidence metadata (`source_section_id`, `evidence_snippet`, reviewer confidence) when present.
- The underlying duplicate canonical source ID remains unresolved pending a migration/curation decision.
