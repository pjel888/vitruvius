# Architecture Civil Structural Gap Log

Date: 2026-05-01

## Closed in gap-closure pass
1. API edge detail metadata exposure: closed with an allowlisted sanitizer for taxonomy/node/explorer detail surfaces. Compact render payloads remain metadata-bounded and unsafe raw source fields are not exposed.
2. Historical self-loops: closed by removing 11 self-loop relationships and making graph-quality validation block self-loops globally, not only for introduced content.
3. Deferred ACS utility/flood/slope paths: closed with Subsurface Utility Conflict Review, Design Flood Elevation Interface, and slope-stability traversal relationships plus resolver cases `RES-ACS-009` through `RES-ACS-011`.
4. Graph-quality diagnostics: closed with duplicate-label samples, same-parent duplicate checks, introduced non-hierarchy orphan reporting, and generic `predicate`/`edge_type` checks.

## Remaining non-critical gaps after gap-closure pass
1. Global duplicate label hygiene: 514 duplicate normalized label groups remain from historical graph slices. Same-parent duplicates are now 0, but full-graph deduplication needs a separate steward-reviewed merge/alias pass. Priority: medium.
2. Civil jurisdiction specificity: stormwater, accessibility, flood, and emergency access relationships are source-family grounded but not project/AHJ-calibrated. Priority: medium.
3. Structural design criteria depth: load combinations, numerical criteria, material-specific code checks, and design-standard edition adoption remain out of scope because they require project basis and adopted standard editions. Priority: medium.
4. Civil infrastructure expansion: road geometry, pavement design, flood modeling, SUE quality-level details, and utility corridor network depth can be improved in later loops. Priority: medium.
5. Operations handoff from ACS assets: maintainability/access and resolver paths exist, but a later pass could deepen asset-register/O&M links for civil and structural elements. Priority: low/medium.

## Blocked items
- Production Neo4j/live graph promotion remains blocked by production credentials and rollback proof.
- Protected source payload admission remains blocked by external source-rights/legal/steward authority.
- Numerical/jurisdiction-specific design criteria remain blocked until the project/AHJ basis and adopted standard editions are explicitly admitted.
- Kimi external critique was attempted during this pass, but the CLI did not return a usable final response before its step limit. Peer subagent reviews were used instead; repeat Kimi review when the internet/agent issue is resolved.

## Closed in remaining-gap follow-up pass
1. Global duplicate label usability: closed for non-destructive reporting by adding `duplicate-label-context-index.json` and summary metrics. Full canonical renaming/alias merging remains a separate steward decision because current duplicates are contextual and same-parent blockers are 0.
2. Civil jurisdiction specificity: closed for this file-backed scope by adding `applicability_basis`, `jurisdiction_context`, and `design_basis_status` metadata plus AHJ adoption-gate edges for flood elevation, accessible transitions, emergency access, live load, wind load, seismic load, and rain ponding.
3. Structural numerical criteria boundary: closed for coordination reasoning by adding explicit non-numeric adopted-basis edges. Numeric criteria remain intentionally blocked until project/AHJ basis and editions are admitted.
4. Civil infrastructure expansion: expanded SUE quality/test-hole verification, pavement subgrade/structure, curb-ramp geometry, emergency-access geometry, and stormwater maintenance access.
5. Operations handoff: expanded civil asset handover relationships from stormwater maintenance access, as-built survey, utility service entry, and pavement/access assets to operations-facing asset records.
6. Shadow consumer metadata contract gap: closed by adding the AHJ/project-basis fields to `BackboneShadowGraphPreview.edges` and a frontend contract test.
7. Predicate-registry compatibility gap: closed by adding a shadow-staging check that rejects governed relationship predicates absent from the staged predicate registry.

## Remaining non-critical gaps after remaining-gap follow-up pass
1. Steward-reviewed canonical duplicate merge/alias pass: still needed if the product wants fewer duplicate human-readable labels. Current context index makes the debt auditable without unsafe renames. Priority: low/medium.
2. Jurisdiction/project-specific criteria admission: still blocked for numeric load, accessibility, stormwater, flood, and fire-service geometry values until AHJ/project basis and source-rights admission exist. Priority: medium but externally gated.
3. Deep civil specialty modeling: flood hydraulics, pavement design, and utility-network modeling remain intentionally high-level. Priority: medium for a future civil-specialty loop.

## Closed in external-gated follow-up pass
1. Steward-reviewed canonical duplicate merge/alias pass: closed to the safe pre-apply stage by adding a gated duplicate-merge review artifact with allowed steward actions, default actions, display disambiguation options, `auto_merge_allowed: false`, and `canonical_label_mutation_performed: false`. Canonical renames/alias application remain blocked until a later steward-approved apply pass.
2. Jurisdiction/project-specific criteria admission: closed to the safe preflight stage by adding a numeric criteria packet validator, external authority ledger validator, payload-leak audit, and live-promotion dry-run gate. Numeric criteria, AHJ adoption, protected payloads, and production writes are still not admitted.
3. Deep civil specialty modeling: expanded with public-way crossing tie-ins, culvert drainage interfaces, pavement subgrade interfaces, runoff/overflow/flood-scour reasoning, pavement restoration/settlement interfaces, drainage inlet maintenance planning, and bioretention/retaining-wall/movement-joint operations handoff.

## Remaining externally blocked items after this pass
- Canonical merge/alias application still requires explicit steward decisions selecting survivor IDs, aliases, retirement records, and migration evidence.
- Actual numerical criteria admission still requires a valid project/AHJ packet, adopted editions, source-rights clearance, steward approval, and no protected payloads.
- Production Neo4j/live graph promotion still requires credentials plus backup/restore/rollback proof; the new gate only reports readiness and performs no write.
- Kimi final critique remains tooling-gated in this environment; Kimi CLI attempts did not produce a usable review.


## Closed in external-gate apply-path follow-up
1. Canonical duplicate merge/alias application: closed to a dry-run apply-plan surface. The runner validates steward decision packets and writes `steward-duplicate-apply-plan-dry-run.json`, but still performs no canonical label mutation, alias application, node retirement, or migration write.
2. Protected payload admission: closed to a hash-only/source-rights manifest preflight surface. The runner validates content hashes and evidence references but still rejects payload text and performs no ingest or public exposure.
3. Production Neo4j/live promotion: closed to a stricter dry-run preflight surface requiring credential names, a production promotion plan, backup evidence, restore-test evidence, and rollback transcript evidence. The runner never prints credential values and performs no connection or write.
4. External packet operator usability: closed by adding CLI flags for all packet paths, packet path-escape rejection tests, persisted report schema tests, and external-gate packet template documentation.

## Remaining hard external inputs after apply-path follow-up
- Applying duplicate merges or aliases still requires concrete steward packets naming survivor IDs, aliases or display-disambiguation actions, evidence paths, source-rights IDs where required, and migration evidence. The current implementation validates and plans only.
- Admitting numeric/project/AHJ criteria still requires concrete project and jurisdiction packets with adopted editions, units, effective dates, source-rights clearance, and steward approval. The current implementation validates and reports only.
- Ingesting protected payload content remains blocked unless a future rights-cleared admission workflow is implemented. The current implementation validates hash-only metadata only.
- Production Neo4j promotion remains blocked unless real production credentials and backup/restore/rollback evidence are supplied; the current implementation is dry-run only.

## Closed in hard-blocker readiness automation
1. External packet schema hand-authoring gap: closed by automatically generating draft skeleton packet files for steward duplicate preservation, AHJ criteria, authority ledger, protected payload manifest, and live promotion plan on every gated-review run.
2. Operator readiness visibility gap: closed by generating `external-gate-readiness-bundle.json` with gate statuses, skeleton paths, missing inputs, and operations explicitly not performed.
3. Secret-file safety gap: closed for repo root by adding `.env.local` and `.env.*.local` to `.gitignore`; `.env.example` now lists blank production Neo4j variable names only.

## Remaining irreducible hard inputs after readiness automation
- Steward identity, authority record, evidence paths, and final rationale cannot be truthfully auto-filled for duplicate actions.
- AHJ adoption basis, adopted editions, values, units, effective dates, and source-rights clearance cannot be truthfully auto-filled for numerical criteria.
- Legal/source-rights decisions and rights-cleared content hashes cannot be truthfully auto-filled for protected payload manifests.
- Secret production credential values, backup proof, restore proof, and rollback transcripts cannot be truthfully auto-filled for live Neo4j promotion.
