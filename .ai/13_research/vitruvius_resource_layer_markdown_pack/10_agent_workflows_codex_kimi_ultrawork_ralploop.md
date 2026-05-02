# 10 — Agent Workflows: Codex + Kimi + Ultrawork + Ralph-loop

## Operating model

Use Codex as the primary implementation agent and Kimi as a review/research/critique partner. Use Ralph-loop/ralploop for persistence and repeated progress. Use Ultrawork-style parallelization for independent workstreams.

## Ralph-loop persistence

Each iteration should read and update durable files such as:

```text
docs/resource-layer/prd.md
docs/resource-layer/progress.md
docs/resource-layer/quality-report.md
docs/resource-layer/gap-log.md
docs/resource-layer/decision-log.md
docs/resource-layer/kimi-review-log.md
docs/resource-layer/source-registry-plan.md
```

If the repo already has equivalent paths, use existing conventions.

## Loop sequence

Every iteration:

1. Inspect repo status.
2. Read PRD/progress/gap/decision/Kimi logs.
3. Select one coherent task.
4. Run parallel agents if supported.
5. Implement changes.
6. Run validation/tests.
7. Update metrics.
8. Ask Kimi for review where appropriate.
9. Accept/reject Kimi suggestions with notes.
10. Commit or summarize according to repo workflow.
11. Update progress.
12. Continue until quality gates pass.

## Ultrawork-style agent roles

### Repository Cartographer

Locate graph data, node schemas, sidebar UI, validation/tests, docs, local resources, storage conventions, and files likely affected.

### Data Model Engineer

Implement Resource model, NodeResourceLink model, source-family registry, candidate/review/check tables or files, and backward compatibility.

### Local Corpus Agent

Scan local files, extract metadata, hash files, extract/chunk text where feasible, and generate local candidates.

### API Adapter Agent

Implement adapters or documented interfaces, cache and rate-limit API calls, normalize identifiers, and store candidates.

### Verifier/Ranker Agent

Implement URL checks, local file checks, DOI/ISBN normalization, deduplication, relevance/authority scoring, and acceptance thresholds.

### Kimi Critic

Review source-node candidate batches, flag weak sources/jurisdiction issues/duplicates, suggest better relationship types and missing source types.

### Sidebar UI Agent

Implement card rendering, filters, empty state, candidate/admin view if applicable, and tests for zero/one/many resources.

### QA/Validation Agent

Implement validation scripts, unit tests, integration tests, graph-resource link consistency checks, and final quality report.

## Kimi review payload structure

```json
{
  "node": {
    "id": "...",
    "name": "Retaining Wall",
    "type": "Concept",
    "taxonomyPath": ["AEC", "Civil Engineering", "Site/Geotechnical"],
    "description": "...",
    "aliases": ["earth retaining wall"]
  },
  "candidateResources": [
    {
      "title": "...",
      "url": "...",
      "resourceType": "professional_guidance",
      "sourceAuthority": "government",
      "relationship": "provides_design_guidance",
      "rationale": "...",
      "scores": {
        "relevance": 0.88,
        "authority": 0.9,
        "confidence": 0.8
      }
    }
  ],
  "reviewQuestions": [
    "Is this source actually relevant to the node?",
    "Is the relationship type correct?",
    "Does this overclaim jurisdiction or authority?",
    "Should any source be rejected?",
    "What better source category is missing?"
  ]
}
```

## What to do if Kimi is unavailable

Continue implementation, mark Kimi review as blocked, queue risky candidates as `needs_review`, do not over-promote risky sources, and document the blocker.
