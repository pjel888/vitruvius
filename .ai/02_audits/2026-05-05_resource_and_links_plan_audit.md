# Resource-And-Links Promotion Plan Audit

**Date:** 2026-05-05
**Plan:** `.ai/13_research/autopilot_resource_and_links_plan.md`
**Verdict:** PASS_ALLOW_RESOURCE_AND_LINKS_IMPLEMENTATION_WITH_TEMP_FIXTURES

## Audit Findings

The plan stays inside the authorized Resource/Evidence Layer boundary:

- It does not authorize graph, canonical, P0, high-risk P1, merge, alias, redirect, tombstone, or graph-edge mutation.
- It does not require external verification, URL fetching, DOI lookup, ISBN lookup, book APIs, PDF fetches, or source truth invention.
- It keeps ASCE 7 and ACI 318 incomplete and blocked unless real reviewer-supplied context already exists.
- It keeps learner exposure computed through `isLearnerSidebarEligible`, not asserted by request input.
- It requires transaction manifests and rollback plans before any write-capable operation.
- It requires per-node rationale and explicit node IDs before nodeResourceLink creation.
- It keeps production registries unchanged when production external candidate count is 0.

## Implementation Conditions

Implementation may proceed only under these conditions:

1. Use temp registries/tests for creation flows unless a real production candidate exists and passes all gates.
2. Keep newly promoted external resources `unverified` unless a real prior review decision supports a stronger non-external status.
3. Default new links to `needs_review`.
4. Reject or downgrade any accepted-link request that does not pass `isLearnerSidebarEligible`.
5. Block duplicate Resource creation rather than silently reusing an existing Resource in this phase.
6. Rollback must remove created links before removing or marking the created Resource.
7. Production resources must remain 7 and production nodeResourceLinks must remain 9 in the current baseline.

## Tooling Notes

- GitNexus query located Resource Layer validation/ranking/source-custody touchpoints.
- ChunkHound regex search found relevant Resource Layer audit/source-custody records but failed after partial output with a Windows `UnicodeEncodeError` while printing an arrow character. The partial result was sufficient for planning, and GitNexus plus direct targeted reads covered the needed code paths.
- code-review-graph refreshed successfully through the wrapper, but this session did not expose a callable MCP `detect_changes` tool.

## Audit Result

No plan blocker was found. The next safe action is resource_and_links implementation with focused temp-fixture tests and full no-write validation.
