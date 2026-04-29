---
task: lea-ale-resolver-deepening
phase: 05
created: 2026-04-29
author: CODEX
status: PASS
supersedes: null
---

# LEA/ALE Resolver and Building-Technology Deepening Packet

## Scope

Improve the file-backed AEC-MEPFS/LEA-ALE knowledge graph so it is more useful
for Philippine Architecture Licensure Examination study, retrieval, and
cross-subject reasoning. This packet deepens LEA/ALE utilities and structural
concepts, adds resolver/API golden cases for practical exam-style query paths,
and strengthens metadata-only source-rights handling for local raw LEA/ALE PDF
signals.

## Audit Findings

- Baseline before this phase: 9,403 `BackboneNode` records, 10,979 governed
  relationships, 236 LEA/ALE phase nodes, 1,193 LEA/ALE phase relationships,
  79 source-rights rows, zero duplicate IDs/path codes, zero missing edge
  endpoints, and zero missing parent paths.
- Existing LEA/ALE enrichment was subject/domain organized, but utilities and
  structural-concept nodes were intentionally identified as a high-value next
  deepening area.
- Existing resolver fixture had only seven static golden cases and did not prove
  LEA/ALE law/code/practice/history/utilities/structures query paths.
- Resolver QA route-boundary logic still encoded a guarded-default-off era while
  the implemented API is now default-on file-backed with an explicit disable
  flag.
- Raw-source LEA/ALE PDFs remain mixed-rights custody artifacts and must stay
  metadata-only unless external legal/steward clearance is supplied.

## Implementation Plan

1. Add a deterministic, idempotent LEA/ALE resolver-deepening script that updates
   the true file-backed backbone fixture, resolver fixture, and source-rights
   registry.
2. Add real L4 utilities/building-systems nodes and structural-concept nodes
   under existing LEA/ALE Architecture branches without creating L5 depth.
3. Add governed relationships for utilities coordination, equipment rooms,
   shafts/risers, RCP/ceiling coordination, fire/ICT/security systems,
   structural grids/load paths/foundations/lateral systems, and cross-subject
   law/code/design/practice reasoning paths.
4. Add LEA/ALE resolver golden cases for law/practice, National Building Code,
   Fire Code, accessibility, water/sanitation, history/theory, materials,
   structures, utilities, construction administration, and protected-content
   negative outcomes.
5. Add metadata-only source-rights rows for public source-family references and
   raw-source custody signals, with explicit no-payload/no-question/no-answer
   boundaries.
6. Refresh shadow staging/consumer artifacts and resolver QA reports through the
   approved file-backed workflow only.
7. Update contract/API tests and validation/state documents to reflect the new
   counts and resolver default-on policy.

## Plan Critique

- [C001] Do not add placeholder or test-only graph nodes; all added nodes must
  be study/reasoning-useful LEA/ALE concepts.
- [C002] Do not ingest PDF payloads, reviewer text, exam questions, answer keys,
  protected code tables/clauses, figures, or diagrams.
- [C003] Keep the enrichment file-backed and shadow-staged; do not run KG
  rebuild/reload/reset or Neo4j/live graph promotion.
- [C004] Use only governed predicates already present in the registry.
- [C005] Preserve deterministic IDs, three-letter path segments, max depth 4,
  and existing source-rights conventions.

## Execution Checklist

- [x] Capture baseline counts and integrity status.
- [x] Run Kimi advisory review for LEA/ALE query-path/source-rights deepening.
- [x] Add deterministic LEA/ALE resolver-deepening script.
- [x] Apply file-backed graph, resolver fixture, and source-rights enrichment.
- [x] Add resolver/API golden-case regression tests.
- [x] Update backbone/API count expectations.
- [x] Refresh shadow staging and shadow consumer reports.
- [x] Refresh resolver QA report with default-on route policy accepted.
- [x] Run focused and broad KG/API validation.
- [x] Run safety scans for protected payload, Neo4j/live promotion, KG rebuild,
  destructive graph operations, and Codex Spark active routing.
- [x] Run Kimi final read-only audit.

## Explicit Non-Goals

- No Neo4j write, production/live graph promotion, or live KG mutation.
- No KG rebuild/reload/reset.
- No protected source payload, reviewer text, exam question, answer key, code
  table/clause, figure, or diagram ingestion.
- No schedule tracking or transient current-event enrichment.
- No invented non-registry relationship predicates.

## Evidence

- Enrichment report:
  `006_System-Manifests/aec-mepfs-backbone/lea-ale-resolver-deepening/20260429T100900Z/lea-ale-resolver-deepening-report.json`
- Shadow staging and consumer report:
  `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T101500Z/`
- Resolver QA report:
  `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260429T102000Z/resolver-qa-report.json`
- Validation log:
  `.ai/05_logs/2026-04-29_lea_ale_resolver_deepening_validation.md`
