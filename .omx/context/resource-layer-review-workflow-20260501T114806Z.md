# Resource Layer Review Workflow Context Snapshot

Timestamp: 20260501T114806Z

## Task statement
Build Resource Layer loop 2: reviewer/admin workflow for candidates, needs_review links, rejected links, and local indexed resources.

## Desired outcome
File-backed API mutation/review endpoints, decision history, Explorer review UI, improved validation/reporting, tests, docs, and logs. No broad backfill, no fake sources, no auto-promotion, no paid APIs.

## Known facts/evidence
Loop 1 implemented resource registries, resource ranking/validation, local file index, Open Library adapter, API resource routes, and sidebar resource cards. ASCE/FHWA are needs_review; ACI broad column mapping is rejected; WBDG contextual guidance.

## Constraints
Follow AGENTS SEL/state-first workflow. Refresh code intelligence before edits. Preserve dirty working tree and existing decisions. Keep file-backed registries. Do not invent auth; label UI as local/dev admin tool.

## Unknowns/open questions
Exact Explorer route/navigation pattern; best route location for reviewer page; mutation validation edge cases; whether current tests expect API export shape.

## Likely touchpoints
api/resourceLayer/types.ts, registry.ts, validation.ts, new review workflow module; api/index.ts; api/resourceLayer.test.ts; explorer src API/types/components/App routing; docs/knowledge-graph/resource-layer.md; .ai progress/log/decisions.
