# Source-Grounded KG AI Program Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans only after a concrete implementation packet is approved. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn Vitruvius from a strong file-backed AEC-MEPFS knowledge graph into a source-grounded KG AI system whose answers cite real resources and use admitted graph reasoning paths.

**Architecture:** Keep raw/canonical custody and stewardship manifests as truth, use AI only for proposal and review assistance, attach sources/resources/evidence spans to nodes and relationships through governed admission, and project the validated graph into fast retrieval/runtime surfaces. Graph relationship enrichment remains the reasoning skeleton; source/resource attachment makes that skeleton trustworthy for AI answers.

**Tech Stack:** Vitruvius file-backed layers, graph-canonical manifests, Resource Layer, Python proposal scripts, Bun API validators, Explorer graph surfaces, future PostgreSQL/Memgraph/API-memory projections.

---

## File Structure

- `README.md` — public project purpose and source-grounded AI north star.
- `.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md` — live project-manager tracker for the main goal.
- `.ai/ACTIVE_WORK.md` — current active work aligned to the north star.
- `.ai/STRATEGIC_NEXT_MOVE.md` — next highest-leverage move.
- `.ai/01_roadmap/current-phase.md` — authoritative current phase note.
- `.ai/01_roadmap/milestone-tracker.md` — milestone truth.
- `.ai/10_state/decisions.md` — architecture decision record for the purpose reconciliation.
- Future implementation files should be added only after a dedicated packet defines coverage metrics and no-write validators.

### Task 1: Establish the north-star tracker

**Files:**
- Create: `.ai/14_project_management/README.md`
- Create: `.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md`

- [x] State that the product goal is source-grounded KG AI, not raw edge count.
- [x] Track achieved graph, resource, custody, and validation baselines.
- [x] Track open workstreams for source coverage, AI proposal workflow, reasoning quality, retrieval, and fast projections.
- [x] Add tracker update rules so future graph/source/retrieval work keeps the tracker current.

### Task 2: Reconcile public purpose docs

**Files:**
- Modify: `README.md`

- [x] Add a Source-Grounded AI North Star section.
- [x] Explain the raw source to AI answer path.
- [x] Link the project-manager tracker.
- [x] Preserve guardrails: no fake sources, no protected payload copying, no direct AI truth admission.

### Task 3: Reconcile `.ai` operating docs

**Files:**
- Modify: `.ai/README.md`
- Modify: `.ai/ACTIVE_WORK.md`
- Modify: `.ai/STRATEGIC_NEXT_MOVE.md`
- Modify: `.ai/01_roadmap/current-phase.md`
- Modify: `.ai/01_roadmap/master-roadmap.md`
- Modify: `.ai/01_roadmap/milestone-tracker.md`
- Modify: `.ai/10_state/active_context.md`
- Modify: `.ai/03_plans/INDEX.md`

- [x] Make the tracker discoverable from `.ai/README.md`.
- [x] Update active work and strategic next move around source grounding and reasoning quality.
- [x] Add roadmap/milestone entries without claiming unverified implementation.
- [x] Keep production graph, protected payload, Resource Layer, and destructive graph gates intact.

### Task 4: Record the architecture decision

**Files:**
- Modify: `.ai/10_state/decisions.md`

- [x] Add an AD entry that codifies source-grounded KG AI as the product north star.
- [x] State that graph enrichment is a reasoning skeleton, source/resource attachment is the grounding layer, and AI proposals are not truth.
- [x] State that future database projections must remain rebuildable from canonical custody.

### Task 5: Validate docs-only reconciliation

**Commands:**

```powershell
git diff --check -- README.md .ai/README.md .ai/ACTIVE_WORK.md .ai/STRATEGIC_NEXT_MOVE.md .ai/01_roadmap/current-phase.md .ai/01_roadmap/master-roadmap.md .ai/01_roadmap/milestone-tracker.md .ai/10_state/active_context.md .ai/10_state/decisions.md .ai/03_plans/INDEX.md .ai/14_project_management .ai/03_plans/2026-05-03_source_grounded_kg_ai_program_plan.md
```

Expected: no whitespace errors.

```powershell
git status --short --branch
```

Expected: only intended docs plus pre-existing unrelated dirty/untracked files.

## Self-Review

- No implementation is authorized by this plan.
- No database migration is authorized by this plan.
- No graph admission is authorized by this plan.
- No Resource Layer mutation is authorized by this plan.
- No protected payload handling is authorized by this plan.

## 2026-05-03 Acceleration Addendum

This addendum incorporates API, Explorer, database projection, Rust, and cloud-AI analysis from:

- `.ai/13_research/2026-05-03_source_grounded_kg_ai_acceleration_research_pack.md`
- `.ai/02_audits/2026-05-03_source_grounded_kg_ai_plan_improvement_audit.md`
- `.ai/03_plans/2026-05-03_source_grounded_kg_ai_execution_acceleration_plan.md`

### Task 6: No-write source/resource coverage inventory

**Files:** future implementation packet only; no implementation authorized here.

- [ ] Count graph nodes with learner-safe resources.
- [ ] Count admitted relationships with resource/evidence support.
- [ ] Classify graph paths as source-backed, domain-synthesis, unsupported, proposal-only, or blocked by rights.
- [ ] Prove zero canonical/Resource Layer mutation during report generation.

### Task 7: SourceGroundedAnswerContext contract

- [ ] Define the backend answer-context contract before any AI composer.
- [ ] Include resolved nodes, admitted graph paths, resources, evidence claims, claim classes, and safety boundaries.
- [ ] Add fail-closed behavior for no evidence, protected payload, and conflict cases.

### Task 8: Edge/resource/evidence joins

- [ ] Use existing `NodeResourceLink.supportsEdgeIds` and `evidenceClaimIds` fields.
- [ ] Add resource lookup by edge/path.
- [ ] Preserve rights-safe selectors rather than protected source payload snippets.

### Task 9: Non-mutating Explorer answer panel

- [ ] Design an answer panel that does not merge query/answer results into the current graph by default.
- [ ] Group citations by claim.
- [ ] Distinguish source-backed facts, admitted graph reasoning, proposal-only content, and insufficient evidence.

### Task 10: Proposal-only local/cloud AI acceleration

- [ ] Standardize an append-only proposal queue.
- [ ] Keep Ollama/local review as baseline.
- [ ] Use cloud AI only with explicit opt-in, provider allowlists, budgets, redaction, and source-rights preflight.
- [ ] Never let cloud AI write admitted truth.

### Task 11: Projection architecture benchmark packets

- [ ] Formalize API in-memory projection versioning and benchmark first.
- [ ] Keep Postgres import-only until hash parity and a future AD authorize any custody switch.
- [ ] Treat Memgraph/Neo4j as projection-only graph traversal stores.

### Task 12: Rust optimization benchmark packets

- [ ] Benchmark `spatial-daemon/src/cli.ts` pairwise geometry before any Rust implementation.
- [ ] Require at least 2x end-to-end improvement and deterministic output parity.
- [ ] Keep Rust out of source custody, graph admission, evidence governance, and AI orchestration.

### Task 13: Validation and review

- [ ] Run no-write graph/canonical/resource validators for each implementation packet.
- [ ] Keep the project tracker current after each packet.
- [ ] Record tool failures and stale-index caveats honestly.
