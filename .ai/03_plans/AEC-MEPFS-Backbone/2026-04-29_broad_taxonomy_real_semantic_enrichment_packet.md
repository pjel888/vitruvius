# Broad Taxonomy Real Semantic Enrichment Packet

Status: BOUNDARY_APPROVED  
Date: 2026-04-29  
Authority: project-owner directive to continue broad taxonomy work after Architecture-first correction and remove scaffold placeholders.

## Purpose

Finish the scaffold-removal direction across all non-Architecture AEC-MEPFS roots by replacing generic L4 placeholder nodes with real semantic taxonomy children.

## Allowed scope

- Replace non-Architecture L4 labels ending in `Concepts`, `Concept Anchor`, `Rule Context`, or `Topics`.
- Add deterministic generator and idempotency tests.
- Update fixture count expectations and API artifact expectations.
- Generate taxonomy expansion report and shadow staging artifacts.
- Update roadmap/state docs and validation evidence.

## Blocked scope

- No protected content ingestion or source payload copying.
- No Neo4j writes, graph reset, reload, rebuild, or production promotion.
- No API route implementation change.
- No Explorer runtime code change.
- No broad live-runtime authorization.

## Implementation target

- Remove all 2496 remaining non-Architecture L4 scaffold nodes.
- Add 6240 real semantic non-Architecture L4 nodes, exactly five per non-Architecture L3 parent.
- Preserve the Architecture-first real semantic branch from commit `15dae0d0`.
- Preserve file-backed preview/read-only boundaries.

## Verification plan

- Run broad taxonomy generator and idempotency test.
- Assert global L4 scaffold count is zero across all roots.
- Run backbone contract tests, shadow staging tests, and route inventory tests.
- Run API `/v2/backbone*` tests against the refreshed file-backed run.
- Run safety grep for forbidden production mutation, protected ingest, and live-authorization strings.
- Attempt Kimi advisory review using pasted summary only from `/tmp` to avoid repo mutation.

## Rollback

Revert the commit. The change is file-backed fixture/test/docs/evidence only; no live graph or runtime mutation is performed.
