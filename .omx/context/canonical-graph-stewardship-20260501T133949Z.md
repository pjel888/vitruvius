# Canonical Graph Stewardship Context Snapshot

Task: Build canonical duplicate stewardship workflow after graph relationship visibility and resource reviewer loops.

Desired outcome:
- Duplicate candidate API/service/UI for review.
- Dry-run merge/alias/keep-separate model preserving edges and Resource Layer links.
- Canonical search preference based on approved decisions.
- Resource Layer reviewer hardening: local/dev gate, structured forms, diff preview, transaction manifests/locking, schema validation, metrics naming.
- Tests, validation, docs, Kimi reviews.

Constraints:
- No reckless production duplicate merges.
- No fake resources/placeholders.
- Preserve relationship visibility and Resource Layer routes/tests.
- File-backed conventions preferred.
- Current workspace has many pre-existing dirty/untracked files from prior loops; isolate this loop's changes in reports.

Likely touchpoints:
- api/graph/relationshipVisibility.ts
- api/index.ts
- api/resourceLayer/*
- api/validateGraphRelationships.ts
- explorer/src/App.tsx
- explorer/src/api/graphApi.ts
- explorer/src/components/resource-review/*
- Explorer routing/dev admin UI
- 006_System-Manifests/graph-canonical/
- .ai/13_research/*
