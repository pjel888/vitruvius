# ACS final gated gaps context snapshot

Timestamp UTC: 20260501T075556Z

## Task statement
Proceed with remaining non-critical and externally gated Architecture/Civil/Structural knowledge-graph gaps, using Ralph/UltraWork/UltraQA and parallel-agent review.

## Desired outcome
Implement every repository-actionable safe improvement: close non-critical usability/modeling gaps, add gate/validation machinery for externally blocked work, keep graph metadata source-backed and non-numeric unless admitted by a project/AHJ evidence packet, and prove no regression.

## Known facts/evidence
- Prior ACS follow-up reached 10,014 nodes, 13,645 governed relationships, 139 resolver cases, 100/100 ACS quality.
- Remaining gaps documented: steward-reviewed duplicate merge/alias pass, project/AHJ numeric criteria admission, deeper civil specialty modeling, and production Neo4j/live promotion.
- Production Neo4j promotion, protected payload admission, and numerical design criteria are explicitly blocked unless credentials/legal/steward/AHJ evidence exists.

## Constraints
- Do not mutate live Neo4j or rebuild/reset production KG.
- Do not ingest protected source payloads or quote/copy standards text.
- Do not admit jurisdiction-specific numeric criteria without project/AHJ/adopted-edition evidence.
- Do not add placeholder nodes or shallow related_to edges.
- Maintain file-backed shadow-only safety and existing tests.
- Use code-intelligence refresh before/after code edits; record tool warnings.

## Unknowns/open questions
- Whether any real project/AHJ credential/evidence packet exists locally; assume absent unless discovered.
- Whether canonical duplicate labels can be safely renamed; assume no without steward approval, but generate candidate review artifacts.

## Likely touchpoints
- scripts/vitruvius/kg/* quality/admission/report scripts
- scripts/tests/test_kg_*.py
- scripts/tests/fixtures/aec_mepfs_backbone/*
- docs/knowledge-graph/*
- .ai/05_logs and roadmap/state docs
- 006_System-Manifests/aec-mepfs-backbone/* generated reports
