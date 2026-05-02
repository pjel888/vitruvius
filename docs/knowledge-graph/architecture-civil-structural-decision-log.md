# Architecture Civil Structural Decision Log

Date: 2026-05-01

## Decisions
1. Use file-backed shadow/backbone enrichment only. Rationale: current state allows authored backbone/source-overlay work but blocks live Neo4j, KG rebuild/reset, and protected source admission.
2. Use metadata-only source-family provenance. Rationale: source families support relationship rationale without copying standard/code text.
3. Prefer mechanism edges over broad relatedness. Rationale: required traversal questions depend on specific mechanisms such as load transfer, runoff conveyance, accessible grade control, bearing capacity, utility conflict avoidance, flood-elevation coordination, and movement-joint waterproofing.
4. Keep inverse edges selective. Rationale: the current schema does not require explicit inverse edges; adding many inverse edges would inflate graph density without stronger semantics.
5. Treat graph-wide duplicate labels as a future cleanup, but block same-parent duplicates and report duplicate samples now. Rationale: historical duplicates predate this loop; ACS duplicate labels were disambiguated while preserving compatibility.
6. Close API edge metadata through a safe allowlist rather than raw row exposure. Rationale: `buildShadowBackboneTaxonomyPreview` impact was HIGH, but a bounded sanitizer can expose relation type/category/nature, weight, confidence, lifecycle, discipline, source-family IDs, rationale, generation method, review status, and overlay category while excluding URLs, raw paths, quotes, source text, and protected payload fields.
7. Remove historical self-loop relationships. Rationale: self-loops in admitted Backbone relationships confuse traversal and quality metrics; removal was paired with global self-loop validation and contract count updates.
8. Add the remaining ACS gap paths as small, source-backed clusters. Rationale: utility conflict review, design flood elevation interface, and slope stability materially improve Architecture-Civil-Structural reasoning without broad unbounded expansion.

## Kimi and review handling
Accepted from subagent review: API allowlist instead of raw spread, duplicate-label/same-parent diagnostics, global self-loop cleanup, utility-conflict/flood/slope candidates, and stronger traversal tests.

Kimi status: Kimi CLI was invoked for external critique, but it repeatedly reached its step limit without a final usable review. No Kimi-specific recommendation was blindly implemented. Repeat Kimi review is recommended once the internet/agent issue is resolved.

Rejected/deferred: numerical criteria, universal jurisdiction claims, excessive inverse edges, broader MEPFS utility additions outside this ACS loop, live Neo4j promotion, and protected source payload admission.

## Remaining-gap follow-up decisions
9. Use a duplicate-label context index rather than canonical renaming. Rationale: graph-quality confirmed 514 duplicate normalized label groups but 0 same-parent duplicate labels; blind renaming would risk breaking intended contextual concepts. The new index gives steward-reviewable path/parent disambiguation.
10. Preserve AHJ and project-basis limits through metadata and edges, not numeric claims. Rationale: `applicability_basis`, `jurisdiction_context`, and `design_basis_status` make source-family-only status explicit while avoiding jurisdictional overreach.
11. Keep new pavement/access/SUE/stormwater additions within existing predicate vocabulary. Rationale: `depends_on` and `supports` are useful relation-type words but unsupported governed predicates in the current predicate registry, so new rows use registered predicates (`requires`, `constrains`, `part_of`) with mechanism-specific `relation_type` values.
12. Expose applicability/design-basis metadata through the same allowlisted API/shadow path. Rationale: consumers need to see that relationships are source-family-only and non-numeric, but raw URLs, quotes, source paths, and protected payload fields remain excluded.
13. Treat the shadow-staging predicate registry as the runtime compatibility source of truth. Rationale: static contract validation blocks unknown governed predicates, but shadow staging must also prove that the actual staged predicate registry includes every governed predicate used by the file-backed shadow graph.
14. Keep applicability metadata visible in both graph-detail and backbone-preview TypeScript contracts. Rationale: `GraphEdge`/`RelationDetail` and `BackboneShadowGraphPreview.edges` are separate Explorer surfaces; both need the same non-numeric AHJ/project-basis metadata.

## Kimi and review handling for follow-up
Accepted from Kimi: treat global duplicates as a reference/usability issue rather than hierarchy corruption, avoid blind deduplication, and add explicit generic-vs-adopted applicability metadata.

Accepted from subagent review: add a non-destructive duplicate context index, expand civil/SUE/pavement/access/O&M paths, and quality-gate the new resolver/traversal cases.

Accepted from architect review: add missing `BackboneShadowGraphPreview` metadata fields and a predicate-registry compatibility gate for shadow staging.

Rejected/deferred: canonical duplicate label renames without steward review, numerical structural/civil criteria, and universal AHJ/code claims.

## External-gated follow-up decisions
15. Close duplicate-label work only to the non-destructive review-candidate stage. Rationale: current duplicate groups are contextual with 0 same-parent blockers; applying renames or aliases would require steward survivor/retirement decisions and migration evidence.
16. Add fail-closed preflight validators for externally gated criteria instead of admitting the criteria. Rationale: project/AHJ numerical criteria, adopted editions, and source-rights clearances remain external evidence, so the repo can validate packet shape but must not write graph criteria.
17. Add a payload-leak audit to the gated-review path. Rationale: externally supplied criteria or authority packets must be screened for protected source text, raw-source paths, secrets, and numeric/design-payload keys before any future admission path.
18. Expand civil specialty depth with non-numeric mechanism nodes rather than formulas or design values. Rationale: public-way tie-ins, culvert interfaces, pavement subgrade interfaces, and maintenance handoff improve traversal while staying source-family-only and jurisdiction-safe.
19. Reject duplicate shadow edge IDs by preserving one governed predicate per source-target-predicate pair. Rationale: shadow graph edge IDs are compatibility-facing and do not include `relation_type`, so additional mechanisms between the same nodes must use distinct target concepts or remain represented by the existing edge.

## Kimi and review handling for external-gated follow-up
Kimi CLI was attempted twice. One invocation returned no review, another failed on Windows encoding for a Unicode arrow, and a retry hit the step limit without final critique; a continuation then reported no queued review. Accepted review input came from parallel subagents instead: add gate-review scaffolding, preserve non-destructive duplicate review, and deepen civil specialty modeling without numerical criteria. No unsupported Kimi output was implemented.


## External-gate apply-path decisions
20. Treat project-owner authorization as permission to implement safe preflight/apply-plan tooling, not as substitute evidence for production credentials, source-rights/legal records, project/AHJ criteria, or steward duplicate decisions. Rationale: repository authority cannot manufacture external facts or source rights.
21. Emit duplicate-merge apply intent as a dry-run artifact. Rationale: this gives stewards a concrete next action while preserving canonical label stability and preventing accidental alias/migration writes.
22. Validate protected payloads by hash and metadata only. Rationale: hash-only/source-rights manifests can support custody review without copying or exposing protected text.
23. Keep production promotion as a credential/rollback preflight. Rationale: reporting missing credential names and evidence paths is safe; connecting to or writing Neo4j is not safe without a dedicated promotion workflow and live credentials.

## Hard-blocker readiness automation decisions
24. Convert hard blockers into draft readiness skeletons rather than fabricated solutions. Rationale: the repo can generate schema-correct packet starting points from known duplicate counts, gate fields, and required evidence lists, but it cannot invent steward, AHJ, legal/source-rights, protected-payload, credential, backup, restore, or rollback facts.
25. Keep skeletons in System Manifests beside the gated-review report. Rationale: they are operational readiness artifacts, not canonical knowledge or raw source custody.
