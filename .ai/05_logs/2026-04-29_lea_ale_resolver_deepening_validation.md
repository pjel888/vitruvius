# 2026-04-29 LEA/ALE Resolver Deepening Validation

## Outcome

PASS. The file-backed AEC-MEPFS/LEA-ALE backbone was deepened for practical
Philippine Architecture Licensure Examination query paths and cross-subject
reasoning without protected payload ingestion or live graph mutation.

## Baseline Before This Phase

- Backbone nodes: 9,403
- Governed relationships: 10,979
- LEA/ALE subject-domain nodes from prior phase: 236
- LEA/ALE relationships from prior phase: 1,193
- Source-rights registry rows: 79
- Duplicate IDs/path codes: 0
- Missing edge endpoints: 0
- Missing parent paths: 0

## Content Changes

- Added 108 real metadata-only nodes:
  - 51 utilities/building-systems nodes.
  - 41 structural-concept nodes.
  - 16 source-reference/raw-custody metadata nodes.
- Improved 30 existing nodes with aliases/source-family metadata.
- Added 656 governed relationships:
  - 410 relationships touching utilities/building systems.
  - 138 relationships touching structural concepts.
  - 272 cross-domain relationships.
  - 321 relationships touching Philippine law/code/source-family nodes.
- Added 45 LEA/ALE resolver golden cases, bringing resolver golden cases to 52.
- Added 16 metadata-only source-rights rows, bringing registry rows to 95.
- Added 475 aliases/source/path labels on new or improved nodes.

## Current Counts After This Phase

- Backbone nodes: 9,511
- Governed relationships: 11,635
- L1/L2/L3/L4 counts: 24 / 402 / 1,470 / 7,615
- Architecture records: 1,254 total, 1,068 L4
- Source-rights registry rows: 95
- Resolver golden cases: 52

## Raw PDF Source-Rights Handling

Inspected/represented only as metadata-only custody signals:

- `001_Raw-Source-Layer/005-Utilities/Building Laws _ Utilities Mock Test with Key.pdf` — private/third-party mock test with answer key; no payload ingested.
- `001_Raw-Source-Layer/002-History/History of Architecture Sample Exam.pdf` — private/third-party sample exam; no payload ingested.
- `001_Raw-Source-Layer/002-History/Theory of Architecture Reviewer.pdf` — private/third-party reviewer PDF; no payload ingested.
- `001_Raw-Source-Layer/002-History/George Salvan Architectural Character and the History of Architecture.pdf` — private copyrighted book candidate; no payload ingested.
- `001_Raw-Source-Layer/002-History/Filipino Architecture.pdf` — unknown/private-rights architecture reference; no payload ingested.
- `001_Raw-Source-Layer/003-Theory/TOA 4 (Tropical Architecture).pdf` — unknown/private handout/reviewer candidate; no payload ingested.

## Kimi / Provider Evidence

- Kimi advisory synthesis was run with `/Users/philiplewis/.local/bin/kimi` and
  recorded in `/tmp/kimi-lea-deepening-advisory.md`.
- Kimi final read-only audit was run after implementation and validation and saved at `/tmp/kimi-lea-resolver-deepening-final-audit.md`; verdict PASS.
- `opencode.json` continues to route KG enrichment research to
  `moonshot/kimi-k2.6`.
- Safety scans found no active Codex Spark enrichment routing.

## Validation Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m py_compile scripts/vitruvius/kg/lea_ale_resolver_deepening.py scripts/vitruvius/kg/backbone_resolver_qa.py scripts/tests/test_kg_lea_ale_resolver_deepening.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_lea_ale_resolver_deepening.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_lea_ale_semantic_enrichment.py` → 79 passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg*.py` → 582 passed.
- `cd api && bun test v2Resolver.test.ts v2Backbone.test.ts` → 83 passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging --run-id 20260429T101500Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json` → ok true.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_report_reader --run-id 20260429T101500Z` → ok true, 9,511 nodes / 11,635 edges, `content_ingest_source_count=0`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_resolver_qa --fixture scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json --run-id 20260429T102000Z` → ok true, 52/52 cases passed, default-on file-backed route policy accepted.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_api_route_inventory --run-id 20260429T102100Z` → default-on file-backed resolver policy with disable flag and 24 routes.
- JSON validation, duplicate ID/path, missing endpoint, missing parent, source-rights, and safety scans were run after generated artifact refresh → 8 JSON files valid, duplicate IDs/path codes 0, missing edge endpoints 0, missing parent paths 0, invalid predicates 0, duplicate source IDs 0, unsafe source classes 0, protected payload key hits 0.
- Safety pattern scans for protected content, Neo4j/live promotion, KG rebuild/reload/reset, destructive graph operations, and active Codex Spark enrichment routing found only boundary/negative-test references or Kimi routing evidence; no active unsafe routing or payload fields.
- `git diff --check` passed.

## Safety Confirmation

No protected source payloads, reviewer text, exam questions, answer keys,
protected code clauses/tables, figures, or diagrams were ingested. No Neo4j/live
graph promotion, KG rebuild/reload/reset, or destructive graph operation was
performed.

## Remaining Limitations

- LEA/ALE resolver cases are deterministic fixture/API golden paths, not a live
  LLM or Neo4j reasoning engine.
- Public source-family rows remain metadata-only; source currentness and legal
  clearance must be rechecked before any content admission.
- The next highest-value follow-up is adding more examiner-style path coverage
  for site-planning/zoning, environmental planning, and professional-practice
  scenario conflicts.
