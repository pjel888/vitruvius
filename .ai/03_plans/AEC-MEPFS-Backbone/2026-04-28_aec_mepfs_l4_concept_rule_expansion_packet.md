# AEC-MEPFS L4 Concept and Rule-Context Expansion Packet

Status: BOUNDARY_APPROVED
Date: 2026-04-28
Owner: Philip Lewis
Run ID: 20260428T063500Z

## Purpose

Expand the already-expanded AEC-MEPFS taxonomy from an L1/L2/L3 backbone into a denser Explorer-ready structure with L4 concept and rule-context anchors under every L3 subtopic.

The previous 984-node graph provided broad taxonomy/topic/subtopic coverage. The current project-owner instruction is to keep populating the backbone with more topics, subtopics, concepts, and rules until the current taxonomy structure is substantially more complete. This packet authorizes a safe static/file-backed expansion pass only.

## Authority and source basis

This is a steward-governed static taxonomy expansion. It uses high-level public-domain/public-web topic calibration and repo-local research synthesis only. It does not copy protected source text, standards clauses, tables, figures, datasets, course packets, or proprietary outlines.

Public calibration sources used at high level:

- NAAB accreditation criteria page for architecture accreditation context.
- ABET 2025-2026 engineering criteria for breadth/depth engineering curriculum calibration.
- NCEES PE exam pages/specification surfaces for licensure-topic calibration.
- AICP exam content outline for urban planning topic calibration.
- Repo-local `.ai/13_research` AEC-MEPFS and governed-taxonomy research documents.

## Allowed scope

- Append L4 `BackboneNode` records beneath existing L3 nodes.
- Add one concept anchor and one rule-context anchor under each L3 node.
- Preserve all existing IDs and path codes.
- Append deterministic IDs after `VTN-DOM-0000984`.
- Regenerate file-backed shadow staging artifacts.
- Update API/Explorer tests for counts, max depth, and L4 concept/rule typing.
- Keep runtime surfaces file-backed and sanitized.

## Blocked scope

- No protected content ingest.
- No standards clause/table/figure copying.
- No Neo4j writes or production graph promotion.
- No KG rebuild/reload/reset.
- No secret/credential exposure.
- No runtime threshold claims from this content expansion.

## Implementation summary

- Prior graph: 984 nodes, 960 hierarchy edges, 24 L1 roots, 240 L2 topics, 720 L3 subtopics, max depth 3.
- New graph: 2424 nodes, 2400 hierarchy edges, 24 L1 roots, 240 L2 topics, 720 L3 subtopics, 1440 L4 concept/rule-context anchors, max depth 4.
- Added per-L3 children:
  - `.CON` — `<L3 Label> Concepts`
  - `.RUL` — `<L3 Label> Rule Context`
- API node typing now maps L4 `.CON` rows to `concept` and `.RUL` rows to `rule`.

## Verification plan

- Contract validation for the admitted fixture.
- Shadow staging regeneration and report-reader validation.
- API route inventory regeneration.
- API tests for `/v2/backbone*`, `/v2/search`, source preview, and Explorer graph surfaces.
- Explorer tests for default graph counts, graph guardrails, and UI behavior.
- Lint/build/typecheck for Explorer.
- Safety greps for unauthorized runtime mutation/protected content terms.

## Evidence artifacts

- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T063500Z/`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T063500Z/`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T063500Z/explorer-taxonomy-l4-expansion-report.json`
- `.ai/05_logs/2026-04-28_aec_mepfs_l4_concept_rule_expansion_validation.md`

## Completion criteria

- Fixture validates.
- Generated artifacts report 2424 nodes and 2400 edges.
- API/Explorer tests pass.
- No protected payloads introduced.
- No Neo4j/KG mutation introduced.
- Working tree clean after commit/push.
