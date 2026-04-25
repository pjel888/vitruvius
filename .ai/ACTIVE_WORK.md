# Active Work

**Updated:** 2026-04-25
**Scope:** only active and incomplete work belongs here

## NOW

### 1. AEC-MEPFS Backbone readiness gate
- **Status:** planned
- **Why it matters:** the planned architecture shift should start from an authored AEC-MEPFS Backbone, not another document-derived graph pass.
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/`, `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/IMPLEMENTATION_MATRIX.md`, `/.ai/05_logs/2026-04-23_aec-runtime-roots-audit-and-lane-decision.md`
- **Next concrete action:** use the validated `AEC-BB-S1` static contract validator as the foundation for authoring/migration QA fixtures and source-rights registry rows, while keeping runtime implementation blocked until the scorecard reaches `ready for bounded implementation`.
- **Dependency / blocker:** `AEC-BB-S1` is validated, but the readiness scorecard is still `not ready`; runtime implementation roots remain unverified.

### 2. Verification refresh for unverified claims
- **Status:** planned
- **Why it matters:** some success claims are log-backed but not freshly rerun.
- **Evidence:** `/.ai/05_logs/2026-04-20_full-test-suite-green-validation.md`, `/.ai/IMPLEMENTATION_MATRIX.md`
- **Next concrete action:** rerun targeted verification before making fresh “green” claims after future implementation changes.
- **Dependency / blocker:** none; triggered by future code changes.

## NEXT

### 3. Skills / agents consolidation
- **Status:** planned
- **Why it matters:** duplicated skill and agent layers create ambiguity about what is active.
- **Evidence:** `/.ai/11_skills/`, `/.ai/skills/`, `/.ai/12_agents/`
- **Next concrete action:** choose one canonical skill layer and demote imported/unrelated packs to archive/reference.
- **Dependency / blocker:** not blocking the core operating surface.

### 4. Historical transcript demotion
- **Status:** planned
- **Why it matters:** transcripts are useful history but not active planning state.
- **Evidence:** `/.ai/chatGPT-Conversations/`
- **Next concrete action:** move or formally demote transcript material into archive/reference navigation.
- **Dependency / blocker:** reference impact should be mapped before moving files.
