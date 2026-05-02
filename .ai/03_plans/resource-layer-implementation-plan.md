# Resource Layer Implementation Plan

Status: implemented for loop 1
Date: 2026-05-01

## Goal
Implement a file-backed Resource Intelligence Layer that powers selected-node sidebar references without polluting graph nodes, exposing protected payloads, or treating unreviewed links as verified truth.

## Executed steps
1. Added TypeScript resource-layer model and services under `api/resourceLayer/`.
2. Added starter file-backed registries under `006_System-Manifests/resource-layer/`.
3. Integrated API selected-node resources through `resources` on `NodeDetail` and `/node/:id/resources`.
4. Added resource metrics and individual resource read routes.
5. Updated Explorer types and `NodeInspector` Sources tab with resource cards and empty states.
6. Added API tests for normalization, dedupe, ranking, validation, local scanner, Open Library adapter, and API routes.
7. Added Explorer component test coverage for resource cards.
8. Ran QA, Kimi final review, code-intelligence refresh, change detection, and final reporting.

## Plan critique outcomes
- [C001] Existing source-rights rows were not treated as resources. Implemented a separate registry.
- [C002] Compact render graph remained unchanged. Resources load through node detail and explicit resource endpoints only.
- [C003] Broad standards landing pages were not accepted as primary references. ASCE 7 remains `needs_review`; ACI 318 single-node column mapping is `rejected`.
- [C004] Candidate adapters do not run during sidebar render. Open Library is candidate-only and test-covered with mocked fetch.
- [C005] Kimi final review requested stronger custody fields. Added `sourceRights` and `admissionProvenance` to the model and seed resources.

## Remaining planned next loop
1. Add admin/debug UI affordance for needs_review/candidate resources if the product wants reviewer workflows in the sidebar.
2. Add additional adapters such as Crossref/OpenAlex/Google Books with mocked tests.
3. Add section/edition-specific reviewed standards records before promoting ASCE/ACI links.
4. Admit local indexed resources into the primary registry only after explicit review and node-specific rationales.
