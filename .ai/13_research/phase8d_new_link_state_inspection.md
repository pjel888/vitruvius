# Phase 8D New Link State Inspection

Run date: 2026-05-06

## Inspected Files

- `006_System-Manifests/resource-layer/resources.json`
- `006_System-Manifests/resource-layer/node-resource-links.json`
- `006_System-Manifests/resource-layer/external-metadata-candidates.json`
- `006_System-Manifests/resource-layer/review-decisions.json`
- `.ai/13_research/phase8c_node_resource_link_report.md`
- API review workflow: `api/resourceLayer/reviewWorkflow.ts`
- Resource Layer validation: `api/resourceLayer/validation.ts`
- Source custody queue: `api/resourceLayer/sourceCustodyQueue.ts`

## Workflow Findings

- `decideNodeResourceLink` supports `accept`, `reject`, `needs_review`, `downgrade`, and `reopen`.
- The current schema does not support link statuses named `rights_review_needed` or `source_custody_review_needed`.
- The safe way to record those blockers without schema expansion is to keep the link as `needs_review` and append review notes plus a transaction-backed review decision.
- Accepted links are validated by `validateResourceLayerData`.
- `isLearnerSidebarEligible` requires accepted or human-reviewed link status, a non-rejected and non-unverified Resource, no protected rights classification, and complete standards context when applicable.
- Accepted external links to unverified Resources are blocked by validation unless an explicit validation option is used. The review workflow does not use that bypass.

## Link Inspection Table

| Link | Resource | Node | Relation | Current status | Resource verification | Learner eligible | Main acceptance blocker |
|---|---|---|---|---|---|---|---|
| `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7` | `res_9c586758-66e4-46f2-b62a-8720db1c0976` Industry Foundation Classes (IFC) - buildingSMART International | `VTN-DOM-0000092` BIM Schemas | `explains` | `needs_review` | `unverified` | false | accepted-link dry run fails: unverified Resource and missing `lastCheckedAt` |
| `nrl_68b933e6-36b9-4dbb-a628-8a5d923fc485` | `res_115f8683-e9a2-4ce8-9575-d6b9b6c9ce40` Fire Protection - WBDG | `VTN-DOM-0000056` Fire Protection | `provides_design_guidance` | `needs_review` | `unverified` | false | accepted-link dry run fails: unverified Resource and missing `lastCheckedAt`; stored locator without `www` redirects to WBDG home |
| `nrl_d2eb1f9c-7502-40bf-a7d8-ae2c50bd2477` | `res_4b0866ea-2ae0-4172-8f43-ea3d34ffd67c` Uniclass, delivered by NBS | `VTN-DOM-0000093` Classification Systems | `provides_classification` | `needs_review` | `unverified` | false | accepted-link dry run fails: unverified Resource and missing `lastCheckedAt` |

## Dry-Run Accepted-Link Probe

Command used:

`bun --eval <script importing decideNodeResourceLink with dryRun=true and decision=accept>`

Result:

| Link | Accept dry run | Validation details |
|---|---:|---|
| buildingSMART IFC -> BIM Schemas | blocked | accepted link points to unverified resource; accepted external resource missing `lastCheckedAt` |
| WBDG Fire Protection -> Fire Protection | blocked | accepted link points to unverified resource; accepted external resource missing `lastCheckedAt` |
| Uniclass -> Classification Systems | blocked | accepted link points to unverified resource; accepted external resource missing `lastCheckedAt` |

## Initial Disposition

No link should be forced to `accepted` in its current state.

Recommended conservative action before delegated review:

- Keep all three links as `needs_review`.
- Append transaction-backed review decisions documenting the exact blockers.
- Do not mark learner-visible or learner-eligible manually.
- Do not mutate Resource verification statuses in this task.
- Record WBDG locator correction need separately: `https://www.wbdg.org/do/secure/fire-protection` resolves to the expected page, while the stored non-`www` URL redirects to WBDG home.
