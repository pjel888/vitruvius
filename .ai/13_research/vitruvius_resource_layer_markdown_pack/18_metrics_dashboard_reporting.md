# 18 — Metrics, Dashboard, and Reporting

## Why metrics matter

This work can become endless unless the loop has measurable progress.

Metrics should answer whether source coverage is improving, accepted sources are high quality, broken/duplicate sources are being prevented, high-priority nodes are covered, Kimi/human reviews are happening, and sidebar results are useful rather than noisy.

## Core metrics

### Resource counts

- total resources,
- resources by type,
- resources by authority tier,
- resources by verification status,
- local resources,
- online resources,
- open-access resources,
- restricted/paywalled resources.

### Link counts

- total NodeResourceLinks,
- accepted links,
- candidate links,
- rejected links,
- needs-review links,
- links by relationship type,
- links by node type.

### Coverage metrics

- eligible nodes total,
- eligible nodes with at least 1 accepted resource,
- eligible nodes with at least 3 accepted resources,
- high-priority nodes with at least 3 accepted resources,
- Rule nodes with primary sources,
- Evidence nodes with evidence-bearing sources,
- Procedure nodes with procedure sources,
- Document nodes with complete metadata.

### Quality metrics

- average relevance score,
- average authority score,
- average confidence score,
- duplicate resources detected/merged,
- broken links found/fixed/rejected,
- accepted resources without page/section refs,
- accepted resources with local page refs.

### Review metrics

- Kimi-reviewed candidates,
- Kimi accepted/rejected/needs-review counts,
- human-reviewed resources,
- pending human review,
- sources downgraded after review.

## Quality score

| Dimension | Points |
|---|---:|
| Data model completeness | 15 |
| Verification/deduplication | 20 |
| Sidebar UX | 15 |
| Source authority/ranking | 15 |
| Local corpus support | 10 |
| API/source discovery support | 10 |
| Validation/test coverage | 10 |
| Kimi/human review workflow | 5 |

## Report format

Generate report at `docs/resource-layer/quality-report.md`.

Example:

```md
# Resource Layer Quality Report

Date: YYYY-MM-DD

## Summary

- Eligible nodes: 8,046
- Nodes with >=1 accepted resource: 243
- Nodes with >=3 accepted resources: 72
- Resources: 512
- Accepted links: 1,104
- Candidate links: 2,901
- Rejected links: 683
- Kimi-reviewed candidates: 240

## Quality Score

Total: 76/100

- Data model: 15/15
- Verification/deduplication: 14/20
- Sidebar UX: 13/15
- Source authority/ranking: 11/15
- Local corpus support: 8/10
- API/source discovery: 6/10
- Validation/test coverage: 7/10
- Review workflow: 4/5

## Critical gaps

- Rule nodes need jurisdiction validation.
- OpenAlex adapter not implemented.
- Local PDFs indexed but page refs incomplete.

## Next loop focus

Implement DOI metadata adapter and process top 25 structural concepts.
```

## Batch report format

Each backfill batch should report nodes processed, candidates found, accepted/rejected/needs-review counts, Kimi reviewed count, human review required count, top source families, validation results, and next actions.

## Progress/gap/decision logs

Maintain:

- `docs/resource-layer/progress.md`
- `docs/resource-layer/gap-log.md`
- `docs/resource-layer/decision-log.md`
- `docs/resource-layer/kimi-review-log.md`

These files are Ralph-loop memory.
