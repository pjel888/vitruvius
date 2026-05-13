# Source-Grounded Explorer Context Audit

Date: 2026-05-13

## Current Reality

- The AEC relationship-improvement campaigns now produce pending relationship and node-consolidation overlays with ledgers, summaries, review TSVs, and Explorer overlay integration.
- Those outputs are visible as pending overlay edges in Explorer, but they are not source-grounded answer context yet.
- The resource layer already has accepted node-resource links and source-rights metadata.
- The active backbone fixture remains the governed graph input; pending overlay outputs are separate artifacts under `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/`.

## Gap

Explorer can show improved graph structure, but an operator still needs a source-grounded packet that separates:

- governed graph facts,
- pending proposal edges,
- admitted source/resource references,
- source gaps,
- and no-write safety boundaries.

Without this, the next answer-composer step would risk mixing pending AI proposals with admitted source-backed facts.

## Blast Radius

Expected changed areas:

- New read-only Python inventory module under `scripts/vitruvius/kg/`.
- New CLI command in `scripts/pipeline_cli.py`.
- Read-only API helper and endpoint in `api/index.ts`.
- Type additions and a compact Explorer inspector tab.
- Focused tests for the inventory, API context, and Explorer rendering.
- `.ai` status/docs updates.

Out of scope:

- Active graph mutation.
- Neo4j/Postgres writes.
- Admitting overlay edges or node consolidations.
- Cloud/model calls.
- Protected source text ingestion.

## Risk Assessment

Risk is moderate because API and Explorer types are touched, but write risk is low: all new behavior is read-only except inventory report artifacts under `006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/`.
