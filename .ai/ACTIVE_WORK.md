# Active Work

**Updated:** 2026-05-13
**Scope:** only active and incomplete work belongs here

## Purpose Anchor

Vitruvius is being driven toward source-grounded KG AI: raw documents are preserved as immutable custody, converted and canonicalized into reviewable evidence, attached to graph nodes and relationships through governed source/resource links, and then used with admitted graph reasoning so AI answers can cite real materials and expose reasoning paths.

Primary tracker: `/.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md`.

## NOW

### 1. Source-grounded KG AI program tracking
- **Status:** active governance/documentation alignment
- **Why it matters:** graph enrichment, source custody, Resource Layer work, embeddings, and future database projections need one project-manager surface that tracks the actual goal instead of treating edge count as the product.
- **Evidence:** `README.md`, `/.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md`, `/.ai/03_plans/2026-05-03_source_grounded_kg_ai_program_plan.md`, `/.ai/03_plans/2026-05-03_vitruvius_database_projection_architecture_plan.md`.
- **Next concrete action:** keep tracker status current whenever graph relationships, source-resource links, canonical source coverage, or AI retrieval behavior changes.
- **Guardrails:** no fake sources, no protected payload copying, no unreviewed graph mutation, no Resource Layer mutation without review workflow, no production graph writes without rollback proof.

### 2. Source-grounded KG AI execution sequence
- **Status:** active implementation sequence, first context packet implemented
- **Why it matters:** the next step is not direct answer generation or more raw edge count; it is the missing middle that joins questions, graph paths, learner-safe resources, payload-free evidence selectors, and claim classes.
- **Evidence:** `/.ai/03_plans/2026-05-03_source_grounded_kg_ai_execution_acceleration_plan.md`, `/.ai/13_research/2026-05-03_source_grounded_kg_ai_acceleration_research_pack.md`, `/.ai/02_audits/2026-05-03_source_grounded_kg_ai_plan_improvement_audit.md`.
- **Next concrete action:** review the new no-write source-grounding gap workqueue and source-link proposal artifacts before creating any source-link/evidence admission packet.
- **Guardrails:** no graph admission, no Resource Layer mutation, no protected payload copying, no cloud AI on protected/unknown source text, no production DB writes, and no Rust for governance/source/admission semantics.

### 3. Graph relationship quality and reasoning coverage
- **Status:** active, quality-first
- **Why it matters:** admitted relationships are the semantic skeleton that lets AI traverse from concepts to materials, systems, standards context, and source-backed evidence. Relationship work is valuable when it improves reasoning paths, not just when it increases count.
- **Evidence:** `006_System-Manifests/graph-canonical/admitted-relationships.json`, `/.ai/13_research/phase5_next_graph_quality_queue.md`, `api/graphReasoningPaths.test.ts`.
- **Next concrete action:** prioritize quality audits, reasoning-path tests, relation-family coverage, and targeted gap closure over raw admission volume.

### 4. Source-to-node and source-to-relationship attachment path
- **Status:** active but gated by source-rights/protected-payload review
- **Why it matters:** the eventual AI answer path depends on every important node and relationship being traceable to real source resources, evidence spans, or explicitly marked domain-synthesis rationale.
- **Evidence:** `001_Raw-Source-Layer/`, `002_Raw-Conversion-Layer/`, `003_Canonical-Knowledge-Layer/`, `006_System-Manifests/graph-canonical/`, Resource Layer validators.
- **Next concrete action:** use `source-grounding-gap-workqueue.jsonl` and `source-link-proposals.jsonl` as the review queue for high-value nodes and answer-critical relationships that are still domain-synthesis only.

### 5. Explorer source-grounded context surface
- **Status:** implemented as a read-only first pass with selected-node and graph-wide source-gap review visibility
- **Why it matters:** Explorer can now show graph paths, pending proposals, learner-safe resources, evidence selectors, and source-grounding classes without admitting pending overlay work as truth.
- **Evidence:** `POST /v2/answer/context`, `GET /v2/backbone/source-gap-workqueue`, AEC `/node/:id` details, and the NodeInspector Context tab.
- **Next concrete action:** use the Explorer source-gap browser to select high-value source/resource attachment targets, then add answer-composer tests only after target paths have enough resource support.
- **Guardrails:** no protected source text, no graph admission, no Resource Layer mutation, no production database writes.

## NEXT

### 4. AI-assisted relationship/source-link proposal script
- **Status:** deterministic no-write workqueue scaffold implemented; AI/cloud proposal engine still planned/gated
- **Why it matters:** AI can accelerate candidate discovery across documents and graph neighborhoods, but it must only propose candidates. Admission still requires deterministic gates, source/context review, steward approval, manifests, rollback preview, and validation.
- **Next concrete action:** design the script as a proposal engine with no direct canonical mutation by default.

### 5. Database projection architecture
- **Status:** planning reference
- **Why it matters:** future speed should come from canonical file/manifests as current truth plus deterministic projections: Postgres as import-only/queryable custody prototype until a future AD authorizes any custody switch, Memgraph for projection-only graph traversal, and API in-memory compiled adjacency for hot UI/runtime paths.
- **Evidence:** `/.ai/03_plans/2026-05-03_vitruvius_database_projection_architecture_plan.md`.
- **Next concrete action:** benchmark Vitruvius workloads before selecting production projection storage.

### 6. KG-first cleanup remnants
- **Status:** bounded docs/operator cleanup only
- **Why it matters:** the older pipeline remains source custody and evidence-prep infrastructure under the source-grounded KG AI purpose.
- **Next concrete action:** do not delete legacy source/evidence modules until no-caller proof, tests, replacement paths, and rollback evidence exist.

## LATER / BLOCKED

- Production graph database/live promotion: blocked without target credentials and backup/restore/rollback transcript.
- Protected source payload admission: blocked without valid external legal/steward/source-rights authority.
- P0 duplicate/canonical resolution: blocked unless a future steward packet explicitly authorizes non-destructive action.
- Legacy pipeline deletion: out of scope until exact no-caller proof, reference cleanup, replacement documentation, regression tests, and rollback proof exist.
